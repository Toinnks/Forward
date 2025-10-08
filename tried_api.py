from flask import Flask, jsonify, request
import threading
import subprocess
# from ultralytics import YOLO  
import cv2
import numpy as np
import time
import os
import requests
from datetime import datetime, timedelta
import pytz
import concurrent.futures
import warnings
import json
from collections import deque
import torch

# ---- YOLOv5 imports ----
from models.experimental import attempt_load
from utils.general import non_max_suppression, check_img_size, scale_coords
from utils.augmentations import letterbox
# from ffmpeg_live import ffmpeg_live

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000"

warnings.filterwarnings("ignore")

app = Flask(__name__)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



# 加载 YOLOv5 权重
model = attempt_load('./best.pt', map_location=device)
model.eval()

# API 端点
send_url1 = "http://10.0.101.1:9062/slalarm/add"

polling_interval = 5  # 轮询间隔（秒）
batch_size = 10       # 每轮处理的视频流数量
num_threads = 4       # 线程池大小
# 全局状态
video_streams = {}
frame_counter = {}
stream_locks = {}

WINDOW_SEC = 180  # 3分钟窗口
eye_events = {}    # {stream_name: deque([ts, ...])}  —— 记录“闭眼”事件时间
mouth_events = {}  # {stream_name: deque([ts, ...])}  —— 记录“张嘴”事件时间
EVENT_THRESHOLD = 3   # 满足3次即预警
conf = 0.5      # 置信度阈值（≥0.5 才计事件）

# 类别映射（确保与训练时顺序一致）
classes = ['closed_eye', 'closed_mouth', 'open_eye', 'open_mouth']

def read_frame_from_rtsp(rtsp_url):
    """使用 OpenCV 读取 RTSP 视频流的一帧"""
    try:
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            print(f"[{rtsp_url}] 无法连接到 RTSP 流")
            return None

        ret, frame = cap.read()
        if not ret:
            print(f"[{rtsp_url}] 读取帧失败")
            cap.release()
            return None

        cap.release()  # 读取完毕后释放

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    except Exception as e:
        print(f"[{rtsp_url}] 读取 RTSP 流时发生错误: {e}")
        return None


def infer_yolov5(frame_bgr, conf, imgsz=640):
    """使用 YOLOv5 进行推理，返回检测结果"""
    device = next(model.parameters()).device
    stride = 32  # 默认步长
    # 手动处理图像尺寸
    if imgsz % stride != 0:
        imgsz = (imgsz // stride) * stride

    img0 = frame_bgr
    img = letterbox(img0, imgsz, stride=stride, auto=True)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR->RGB, HWC->CHW
    img = np.ascontiguousarray(img)

    im = torch.from_numpy(img).to(device).float() / 255.0
    if im.ndimension() == 3:
        im = im.unsqueeze(0)

    with torch.no_grad():
        pred = model(im)[0]
        pred = non_max_suppression(pred, conf_thres=conf, iou_thres=0.45, classes=[0, 1, 2, 3])

    dets = pred[0]
    if dets is not None and len(dets):
        dets[:, :4] = scale_coords(im.shape[2:], dets[:, :4], img0.shape).round()
    return dets


def detect_frame(stream_name, rtsp_url, frame, conf):
    """
    简化逻辑：
      - 3分钟窗口内：闭眼事件≥3 或 张嘴事件≥3 -> 触发预警
      - 单帧同一类型最多计1次（防止一帧多框重复累计）
      - 只统计置信度≥0.5的 closed_eye / open_mouth
      - 预警图上用 红=闭眼、蓝=张嘴，并标出置信度
    """
    try:
        if frame is None or not isinstance(frame, np.ndarray):
            print(f"[{stream_name}] invalid frame")
            return

        now = datetime.now(pytz.timezone('Asia/Shanghai'))

        # —— 初始化流状态/计数容器 ——
        global video_streams, eye_events, mouth_events, frame_counter
        video_streams.setdefault(stream_name, {})
        eye_events.setdefault(stream_name, deque())
        mouth_events.setdefault(stream_name, deque())
        frame_counter.setdefault(stream_name, 0)
        stream_locks.setdefault(stream_name, threading.Lock())

        st = video_streams[stream_name]
        st.setdefault("last_seen_time", now)
        st.setdefault("last_alarm_time", None)

        # 先拿锁，保证同一流不并发
        with stream_locks[stream_name]:
            # ===== 冷却检查放最前 =====
            last_alarm = st.get("last_alarm_time")
            if last_alarm and (now - last_alarm).total_seconds() < 300:
                print(f"[{stream_name}] 距离上次报警不足5分钟，跳过报警")
                # 在冷却期，直接返回，不做任何计算/IO
                return

        # —— 推理：你的 read_frame 返回的是 RGB，这里转回 BGR 以匹配 YOLO/OpenCV ——
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        dets = infer_yolov5(frame_bgr, conf)  # det: [x1,y1,x2,y2,conf,cls]

        # —— 遍历检测结果：只关心 closed_eye / open_mouth 且 conf>=0.5 ——
        counted_eye = False     # 本帧是否已计过“闭眼事件”
        counted_mouth = False   # 本帧是否已计过“张嘴事件”

        # 为了画框，记录本帧要画的两个类型的框
        eye_boxes = []    # [(x1,y1,x2,y2,conf,label)]
        mouth_boxes = []  # [(x1,y1,x2,y2,conf,label)]

        if dets is not None and len(dets):
            # 如果是 tensor，转 cpu 后迭代更安全
            dn = dets.detach().cpu().numpy()
            for x1, y1, x2, y2, s, c in dn:
                s = float(s); c = int(c)
                if c < 0 or c >= len(classes):
                    continue
                label_name = classes[c]
                if s < conf:
                    continue
                # 只考虑闭眼/张嘴
                if label_name == "closed_eye":
                    eye_boxes.append((int(x1), int(y1), int(x2), int(y2), s, label_name))
                    if not counted_eye:
                        eye_events[stream_name].append(now)
                        counted_eye = True
                elif label_name == "open_mouth":
                    mouth_boxes.append((int(x1), int(y1), int(x2), int(y2), s, label_name))
                    if not counted_mouth:
                        mouth_events[stream_name].append(now)
                        counted_mouth = True

        # —— 维护3分钟滑窗 —— 
        cutoff = now - timedelta(seconds=WINDOW_SEC)
        while eye_events[stream_name] and eye_events[stream_name][0] < cutoff:
            eye_events[stream_name].popleft()
        while mouth_events[stream_name] and mouth_events[stream_name][0] < cutoff:
            mouth_events[stream_name].popleft()

        eye_cnt = len(eye_events[stream_name])
        mouth_cnt = len(mouth_events[stream_name])
        should_alarm = (eye_cnt >= EVENT_THRESHOLD) or (mouth_cnt >= EVENT_THRESHOLD)

        print(f"[{stream_name}] eye_cnt={eye_cnt}, mouth_cnt={mouth_cnt}, "
              f"eye_boxes={len(eye_boxes)}, mouth_boxes={len(mouth_boxes)}")

        if not should_alarm:
            return

        st["last_alarm_time"] = now
        eye_events[stream_name].clear()
        mouth_events[stream_name].clear()

        # —— 触发报警：画框 + 保存图片 —— 
        alarm_time_str = now.strftime('%Y-%m-%d_%H-%M-%S')
        alarm_filename = f"{stream_name}-{alarm_time_str}-tried.jpg"
        video_filename = f"{stream_name}-{alarm_time_str}-tried.mp4"

        alarm_pic_dir = "/data/clearingvehicle/pic_vid/tried/alarmpic"
        alarm_video_dir = "/data/clearingvehicle/pic_vid/tried/alarmvideo"
        os.makedirs(alarm_pic_dir, exist_ok=True)
        os.makedirs(alarm_video_dir, exist_ok=True)
        alarm_pic_path = os.path.join(alarm_pic_dir, alarm_filename)

        vis = frame_bgr.copy()

        # 红色 = 闭眼；蓝色 = 张嘴；都标出 conf
        for (x1, y1, x2, y2, s, label_name) in eye_boxes:
            color = (0, 0, 255)
            label = f"{label_name} {s:.2f}"
            cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
            cv2.putText(vis, label, (x1, max(0, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        for (x1, y1, x2, y2, s, label_name) in mouth_boxes:
            color = (255, 0, 0)
            label = f"{label_name} {s:.2f}"
            cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
            cv2.putText(vis, label, (x1, max(0, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.putText(vis, "Fatigue Alert", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imwrite(alarm_pic_path, vis)

        # —— 发送告警 + 录制视频 —— 
        payload = {
            "alarmName": "tried",
            "alarmType": "tried",
            "targetCode": stream_name,
            "alarmTime": now.strftime('%Y-%m-%d %H:%M:%S'),
            "alarmPic": f"/tried/alarmpic/{alarm_filename}",
            "alarmVideo": f"/tried/alarmvideo/{video_filename}",
            "source": video_streams.get(stream_name, {}).get("stream_source", ""),
            "cameraCode": video_streams.get(stream_name, {}).get("stream_vehicleCode", ""),
            "oid": video_streams.get(stream_name, {}).get("stream_vehicleOid", ""),
            "alarmCode": video_streams.get(stream_name, {}).get("stream_vehiclePlateNo", "")
        }
        print(f"[{stream_name}] payload: {payload}")

        send_alarm(payload, send_url1, stream_name, 1)
        save_alarm_video(video_filename, rtsp_url)

        # —— 更新冷却时间，并清空计数，避免连发 —— 
        st["last_alarm_time"] = now
        eye_events[stream_name].clear()
        mouth_events[stream_name].clear()

    except Exception as e:
        print(f"[{stream_name}] detect_frame error: {e}")





def save_alarm_video(video_filename, rtsp_url):
    """使用 FFmpeg 在后台线程中录制 5 秒报警视频"""
    video_output_file = f'/data/clearingvehicle/pic_vid/tried/alarmvideo/{video_filename}'
    command = [
        "ffmpeg", "-y",
        "-i", rtsp_url,
        "-t", "6",
        "-vf", "scale=704:576",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-an",                      
        "-movflags", "+faststart",
        video_output_file
    ]
    def run_ffmpeg():
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 以后台线程执行 FFmpeg 录制，避免阻塞主线程
    threading.Thread(target=run_ffmpeg, daemon=True).start()


def send_alarm(payload, primary_url, stream_name, event_count):
    """发送报警信息到第一个接口"""
    try:
        header = {"Content-Type": "application/json"}
        response = requests.post(primary_url, json=payload, headers=header)
        print(f"[{stream_name}] 预警发送状态: {response.status_code}")
        if response.status_code == 200:
            print(f"[{stream_name}] 预警发送成功")
            try:
                response_data = response.json()
                print(response_data)
            except ValueError:
                print("响应不是有效的 JSON")
        else:
            print(f"[{stream_name}] 预警失败: {response.status_code}")
    except requests.RequestException as e:
        print(f"[{stream_name}] 预警发送异常: {e}")


def process_batch(stream_batch, video_streams):
    """批量处理一组视频流"""
    for stream_name in stream_batch:
        input_stream = video_streams.get(stream_name)
        if not input_stream:
            continue

        conf = input_stream.get("conf", 0.5)

        # 读取 RTSP 视频帧
        frame = read_frame_from_rtsp(input_stream["input_stream"])
        if frame is None:
            print(f"[{stream_name}] 读取视频帧失败")
            continue

        detect_frame(stream_name, input_stream["input_stream"], frame, conf)


def process_video_streams(video_streams):
    """轮询所有视频流，按批次分组处理"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            active_streams = list(video_streams.keys())
            if not active_streams:
                time.sleep(1)
                continue

            print(f"[轮询] 发现 {len(active_streams)} 个视频流，按批次处理...")

            for i in range(0, len(active_streams), batch_size):
                stream_batch = active_streams[i:i + batch_size]
                executor.submit(process_batch, stream_batch, video_streams)

            time.sleep(polling_interval)

# API 路由
@app.route('/streams/status', methods=['POST'])
def get_video_stream_status():
    """查询正在检测的视频流"""
    if not video_streams:
        return jsonify({"message": "没有正在检测的视频流"}), 200

    active_streams = list(video_streams.keys())  # 获取所有正在检测的视频流的名称
    return jsonify({"active_video_streams": active_streams}), 200


@app.route('/streams/add', methods=['POST'])
def add_streams():
    """添加多个视频流"""
    data = request.json
    streams = data.get('streams', [])
    conf = data.get('conf', 0.5)

    if not streams or not isinstance(streams, list) or not isinstance(conf, float):
        return jsonify({"error": "Invalid streams format"}), 400

    for stream in streams:
        stream_name = stream.get('stream_name')
        input_stream = stream.get('input_stream')
        stream_source = stream.get('stream_source')   # 车来源 hik、rm
        stream_vehicleCode = stream.get('stream_vehicleCode')  # 车辆编码
        stream_vehicleOid = stream.get('stream_vehicleOid') # 车辆oid
        stream_vehiclePlateNo = stream.get('stream_vehiclePlateNo')  #车牌号

        if not stream_name or not input_stream:
            continue

        if stream_name in video_streams:
            continue

        video_streams[stream_name] = {
            "input_stream": input_stream,
            "conf": conf,
            "stream_source": stream_source,
            "stream_vehicleCode": stream_vehicleCode,
            "stream_vehicleOid": stream_vehicleOid,
            "stream_vehiclePlateNo": stream_vehiclePlateNo
        }

    return jsonify({"status": "Streams added", "streams": list(video_streams.keys())}), 200


@app.route('/streams/delete', methods=['POST'])
def delete_streams():
    """删除视频流"""
    data = request.json
    stream_names = data.get('stream_names', [])

    if not stream_names or not isinstance(stream_names, list):
        return jsonify({"error": "Invalid stream_names format"}), 400

    for stream_name in stream_names:
        if stream_name in video_streams:
            del video_streams[stream_name]

    return jsonify({"status": "Streams deleted"}), 200


# 维护所有推流任务的字典
stream_threads = {}
stream_controls = {}


@app.route('/live/start', methods=['POST'])
def start_stream():
    success_add_lst = []
    data = request.get_json()
    streams = data.get('streams')
    if not streams or not isinstance(streams, list):
        return jsonify({"error": "Invalid streams format, must be a list"}), 400

    for stream in streams:
        stream_name = stream.get("stream_name")
        input_stream = stream.get("input_stream")
        stream_source = stream.get('stream_source')   # 车来源 hik、rm
        stream_vehicleCode = stream.get('stream_vehicleCode')  # 车辆编码
        stream_vehicleOid = stream.get('stream_vehicleOid') # 车辆oid
        stream_vehiclePlateNo = stream.get('stream_vehiclePlateNo')  #车牌号

        if not stream_name or not input_stream:
            return jsonify({"error": "缺少 stream_name 或 input_stream"}), 400

        if stream_name in stream_threads:
            return jsonify({"error": f"流 {stream_name} 已在推流"}), 400

        # 控制变量，动态启停推流
        stream_controls[stream_name] = {
            "is_live_stream": True,
            "stream_source": stream_source,
            "stream_vehicleCode": stream_vehicleCode,
            "stream_vehicleOid": stream_vehicleOid,
            "stream_vehiclePlateNo": stream_vehiclePlateNo
        }

        # 创建并启动推流线程（保持你的调用）
        thread = threading.Thread(target=ffmpeg_live, args=(model, stream_name, input_stream, stream_controls),
                                  daemon=True)
        thread.start()

        stream_threads[stream_name] = thread
        success_add_lst.append(stream_name)

    return jsonify({"message": f"推流{str('、'.join(success_add_lst))}已启动"}), 200


@app.route('/live/stop', methods=['POST'])
def stop_stream():
    success_delete_lst = []
    error_lst = []
    data = request.json
    stream_names = data.get('stream_names')  # 接收一个流名称列表

    if not stream_names or not isinstance(stream_names, list):
        return jsonify({"error": "Invalid stream_names format, must be a list"}), 400

    for stream_name in stream_names:
        if not stream_name or stream_name not in stream_threads or stream_name not in stream_controls:
            error_lst.append(stream_name)
            continue

        # 关闭推流 & 检测
        stream_controls[stream_name]["is_live_stream"] = False
        time.sleep(2)

        # 停止推流线程
        stream_threads[stream_name].join()  # 等待线程完成
        del stream_threads[stream_name]
        del stream_controls[stream_name]
        success_delete_lst.append(stream_name)
    if len(error_lst) == 0:
        return jsonify({"message": f"推流 {str('、'.join(success_delete_lst))} 已停止"}), 200
    elif len(success_delete_lst) == 0:
        return jsonify({"error": f"流 {str('、'.join(error_lst))} 不在推流"}), 200
    else:
        return jsonify({"message": f"推流 {str('、'.join(success_delete_lst))} 已停止",
                        "error": f"流 {str('、'.join(error_lst))} 不在推流"}), 200


if __name__ == '__main__':
    video_streams = {}

    # 启动视频流处理线程
    video_thread = threading.Thread(target=process_video_streams, args=(video_streams,), daemon=True)
    video_thread.start()

    app.run(host='0.0.0.0', port=1221, debug=False)
