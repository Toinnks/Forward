# Linux

nvidia-smi查看gpu

mkdir 创建目录

pwd 显示当前目录

ls 当前目录下的所有文件

删除文件夹及其里面的内容 rm -r file

删除文件 rm file

ps aux显示所有进程信息

lsof -i :9632 查看端口号对应进程

sudo chmod -R a+rw /data/sgy/daily  给相应目录读写权限

```
grep "关键词"  筛选包含关键字的行
grep -v "grep"
‘|’ 是将前一个命令的输出作为后一个命令的输入，如：ps aux | grep "uvicorn air_api:app" | grep -v "grep" /data/sgy/daily/
```

### 镜像类指令

```
docker rmi 镜像名 ：移除镜像

docker rm 容器名 ： 移除容器

docker images 查看镜像
```



### 容器类指令

**常用指令：**

```
docker ps （process status）只显示 **正在运行** 的容器

docker ps -a 看所有的容器

docker stop air-api 停掉容器

docker restart air-api 重启容器

docker exec -it air-api-mcp bash 进入容器
```

**创建容器：**

```
docker run -itd --name yolov11-sgy -v /data/sgy/yolov11:/yolov11 --ipc=host -p 6020-6021:6020-6021 --gpus all ultralytics/ultralytics:latest
```

**创建容器后挂起：**

```
docker run -d --name air-mcp -v /data/sgy:/data/sgy -p 9633:9633 ocr-image:1.0.1 tail -f /dev/null

1. **docker run**
- 作用：创建并启动一个新的容器实例。
------
2. **-d**
- 作用：以“分离模式”（后台运行）启动容器。
- 效果：容器会在后台运行，不阻塞当前终端。 
------
3. **--name air-mcp**
- 作用：为容器指定一个名称 `air-mcp`。
- 用途：方便后续通过名称管理容器（如启动/停止/删除）。
------
4. **-v /data/sgy:/data/sgy**
- 作用：挂载宿主机的目录到容器内（数据卷映射）。
  - 第一个 `/data/sgy`：**宿主机**的目录路径。
  - 第二个 `/data/sgy`：**容器内**的挂载路径。
- 效果：
  - 容器可以访问宿主机 `/data/sgy` 下的文件。
  - 容器内对 `/data/sgy` 的修改会同步到宿主机（反之亦然）。
- 典型用途：
  - 持久化存储容器数据。
  - 共享配置文件或代码。
------
5. -p 9633:9633
- 作用：端口映射，格式为 `宿主机端口:容器端口`。
  - 第一个 `9633`：**宿主机**的端口。
  - 第二个 `9633`：**容器内**的端口。
- 效果：
  - 访问宿主机的 `9633` 端口会转发到容器的 `9633` 端口。
- 为什么两个端口相同？
  - 如果容器内服务监听 `9633`，且宿主机也想通过 `9633` 访问，则这样配置。
  - 如果宿主机 `9633` 已被占用，需改为其他端口（如 `-p 9634:9633`）。
------
6. ocr-image:1.0.1
- 作用：指定使用的 Docker 镜像名称及标签。
  - `ocr-image`：镜像名称。
  - `1.0.1`：镜像版本标签。
- 注意：运行前需确保该镜像已通过 `docker pull ocr-image:1.0.1` 拉取或本地构建。
------
7. tail -f /dev/null
- 作用：保持容器持续运行的“占位”命令。
  - `/dev/null`：Linux 的空设备文件，写入它的内容会被丢弃。
  - `tail -f`：持续跟踪文件变化（这里无实际意义）。
- 效果：
  - 容器启动后执行此命令，由于 `/dev/null` 永远不会变化，`tail -f` 会一直挂起。
  - 这样容器不会立即退出（否则完成命令后会停止）。
```



### 本机使用命令行向服务器传文件

```
scp D:\projects\pythonProjects\daily\china_cities.json root@10.0.4.28:/data/sgy/daily/

scp是从本地向服务器传文件，D:\projects\pythonProjects\daily\china_cities.json是本地文件路径， root是服务器用户，10.0.4.28服务器地址，/data/sgy/daily/是要传入的目标文件夹。
```



### 其他

nohup python3 air_mcp_xiecheng_pro.py > air_mcp_xiecheng_pro.log 2>&1 & 执行

```
nohup uvicorn air_api:app --reload --host 0.0.0.0 --port 9632 > uvicorn.log 2>&1 &
nohup - 使命令在用户退出登录后继续运行
uvicorn.log - 将标准输出重定向到 uvicorn.log 文件
2>&1 - 将标准错误也重定向到同一日志文件
& - 在后台运行进程
```

```
pip install mcp -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```
下面这句命令的解释：

 uvicorn mytest:app --reload --host 0.0.0.0 --port 9632

 python air_api_not.py > test.log 2>&1
```

