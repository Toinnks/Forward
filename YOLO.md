# YOLO

### 服务器cuda设备冲突的问题：

**1.显卡可见，要在导包前**

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "3"
import torch
from ultralytics import YOLO

训练指定device=0

**2.指定显卡，导包后**

import torch
from ultralytics import YOLO

device = torch.device("cuda:3")
model = YOLO('./yolov8n.pt')

训练指定device=device.index

