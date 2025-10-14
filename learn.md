# 爬虫

爬虫

iframe允许在一个网页里嵌套另一个独立的网页，如果遇到iframe需要先定位到iframe

```
frame=page.frame_locator('iframe#login_frame')

button=frame.locator('a#switcher_plogin.link')
```

浏览器滚动的两种方式：

```
1、
for i in range(100):
    page.mouse.wheel(0, random.randint(10,20))
    page.wait_for_timeout(50)
    if i%20==0:
        page.wait_for_timeout(1000)
2、
page.evaluate("window.scrollBy(0, 500)")
```

本地浏览器打开：

```
broswer = p.chromium.launch_persistent_context(
    # 指定本地谷歌浏览器安装目录的绝对路径
    executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

    # 指定本地谷歌浏览器用户数据目录的绝对路径
    user_data_dir=r"C:\Users\jiuge\AppData\Local\Google\Chrome\User Data",

    # 开启有界面模式
    headless=False
)
```

远程连接：

```
import subprocess
import os
import time
from playwright.sync_api import sync_playwright

path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
params = "--remote-debugging-port=6789"
user_data_dir=r"D:ChromeProfile"

cmd = f'"{path}" {params} --user-data-dir="{user_data_dir}"'
# 4.1 执行命令：通过 subprocess 执行终端命令
subprocess.Popen(cmd,shell=True)
# 4.2 执行命令：通过os模块执行终端命令
# os.popen(cmd)
time.sleep(2)

with sync_playwright() as p:
    # 连接本地启动的浏览器               本机(远程)IP:监听端口
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:6789')
    if browser:
        print("成功连接")
    context=browser.contexts[0]
    page=context.new_page()
    page.wait_for_timeout(3 * 1000)

    page.goto("https://www.dianping.com/")
    page.wait_for_timeout(30*1000)
    browser.close()
```



**referer反爬**：从哪个页面跳转的，或者从哪个页面来的api请求，该页面可能生成一个动态token，如果来源不对，就可能被视为爬虫。

### scrapy

```
pip install scrapy==2.9.0 scrapy-redis==0.7.3 Twisted==22.10.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```



# Linux

nvidia-smi查看gpu

cd ..返回上级,中间有个空格

mkdir 创建目录

pwd 显示当前目录

ls 当前目录下的所有文件

删除文件夹及其里面的内容 rm -r file

删除文件 rm file

ps aux显示所有进程信息

grep "关键词"  筛选包含关键字的行

grep -v "grep"

‘|’ 是将前一个命令的输出作为后一个命令的输入，如：ps aux | grep "uvicorn air_api:app" | grep -v "grep"

/data/sgy/daily/

scp D:\projects\pythonProjects\daily\china_cities.json root@10.0.4.28:/data/sgy/daily/

scp是从本地向服务器传文件，D:\projects\pythonProjects\daily\china_cities.json是本地文件路径， root是服务器用户，10.0.4.28服务器地址，/data/sgy/daily/是要传入的目标文件夹。

lsof -i :9632 查看端口号对应进程

docker ps （process status）只显示 **正在运行** 的容器

docker ps -a 看所有的容器

docker stop air-api 停掉容器

docker restart air-api 重启容器

利用镜像创建容器

示例1：

docker run -d  --name air-playwright  -v /data/sgy:/data/sgy  -p 9634-9635:9634-9635   mcr.microsoft.com/playwright/python tail -f /dev/null

示例2：

docker run -dit   --gpus '"device=3"'   --shm-size 16g   --name low_altitude_container_gpu3   -v $(pwd):/app   low-altitude-detection:latest   bash



docker exec -it air-api-mcp bash 进入容器

docker rmi 镜像名 ：移除镜像

docker rm 容器名 ： 移除容器

docker images 查看镜像

nohup python3 air_mcp_xiecheng_pro.py > air_mcp_xiecheng_pro.log 2>&1 & 执行

sudo chmod -R a+rw /data/sgy/daily  给相应目录读写权限

- **nohup uvicorn air_api:app --reload --host 0.0.0.0 --port 9632 > uvicorn.log 2>&1 &**

  nohup - 使命令在用户退出登录后继续运行

  uvicorn.log - 将标准输出重定向到 uvicorn.log 文件

  2>&1 - 将标准错误也重定向到同一日志文件

& - 在后台运行进程

```
pip install mcp -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install chromium
playwright install-deps
```

**下面这句命令的解释：**

```
docker run -d --name air-mcp -v /data/sgy:/data/sgy -p 9633:9633 ocr-image:1.0.1 tail -f /dev/null
```

------

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

 uvicorn mytest:app --reload --host 0.0.0.0 --port 9632

 python air_api_not.py > test.log 2>&1

# YOLO

TP（true positives）：正确的正例

FP（false positives）：错误的正例

TN（true negatives）：正确的负例

FN（false negatives）：错误的负例

精度=TP/(TP+FP)

召回=TP/(TP+FN)

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





# Anaconda

#### anaconda创建虚拟环境的方法

conda env list						看anaconda虚拟环境列表
conda create -n daily python=3.12.4    anaconda创建虚拟环境，名称是ana-sgy，3.8.10
conda activate ana-sgy                                进入创建的虚拟环境
conda deactivate						退出虚拟环境

conda remove -n xxxx --all				删除环境

# MySQL

##### 命令行进入mysql：

mysql -u 用户名 -p

# 概念类

ocr是字符识别
RAGflow
spark
flink
agent

**MCP**

MCP模型上下文协议，agent与外部交互的标准协议。

cs模式，客户端和服务端，运行后一直监听客户端操作

mcp是llm与自己写的工具的中间层，让大模型可以顺利调用自己的工具。

**SSE**

单向的，server端向client端推送

简单的http，不需要复杂握手

**agent**

自己使用工具处理任务 

**UV（不重要）**

UV是Unique Visitor，独立访客的意思。

UV 是互联网和数据分析领域的核心指标，用于统计在一定时间内访问某个网站或应用的不重复用户数量。与 PV（Page View，页面浏览量）不同，UV 更关注实际用户的数量，而非单纯的访问次数。

**RAG**

**RAGFLOW**

**镜像**

**拉镜像**

**搜索引擎**

搜索引擎的前置步骤就是一个 爬虫，爬取各个网页，然后从网页中获取其他网页的链接继续爬取，爬取数量级数增加，而且其他网站也乐意被爬虫获取来增加被访问的渠道。获得网页后会对网页打标签进行网页分类，进行评分（网页打开速度、内容相关性、链接数量），然后通过评分来排序。爬虫获取到的网页都会存在数据库中。

**幻觉**

提示词不够好

模型自我认知不够（数据量不足，训练不到位）

解决：RAG，模型微调

**mcp和传统接口有什么不同**



**报错多看看日志**

**DNS**

将域名解析为IP地址：www.baidu.com--->1.1.1.1,只有IP地址才能访问服务器



**Nginx**

WEB服务器，最基础且最重要的功能就是处理http请求。

# 零碎

1. win+K投屏。或者点击设置，点击屏幕，点击无线显示器。

2. ipconfig 查看本机IP地址

3. win+r 输入msinfo32可以查看系统各项配置

4. 显示文件后缀名：资源管理器-查看-显示-文件后缀名

5. **excel表格批量翻译**：可以先将文件另存为xlsm格式，修改一下文件---选择另存为--选择格式--xlsm格式

   然后打开为https://docs.google.com/spreadsheets谷歌表格网站，打开刚刚的xlsm文件，对整列应用=BYROW(AH2:AH, LAMBDA(x, IF(x<>"", GOOGLETRANSLATE(x, "auto", "fr"), "")))

1. win+x

2. 在win10及以上系统使用wsl --install即可启用wsl2服务和下载ubantu

   验证docker是否安装好用docker run hello-world

   docker image ls 查看镜像列表

   后面 我要使用dify，它和docker有什么关系

   github下载dify-main，终端进入文件的docker文件夹，执行docker-compose up -d

   

   本地dify链接ollama失败：原本的url是http://localhost:11434，但一直失败，要注意docker映射应当是

   http://host.docker.internal:11434

# Python

### 0、操作

1. 命令行进入requirements.txt文件的父级目录，输入pip install -r requirements.txt（pip install -r requirements.txt)
2. 卸载pip uninstall 库名

### 1、语法

- / 除法，得到一个小数

- //除法，得到一个整数

- **是乘方，xy是x的y次方

- with语句可以安全的打开关闭文件，with open('xx.txt','w',encoding='utf-8') as file ,w是写，没有该文件会创建文件，r是读

- 0的布尔值是false，非0的布尔值是true，空字符串的布尔值是0，非空字符串的布尔值是true

- 列表是方括号，元组是小括号。元组数据不可修改，元组适用一些不会发生改变的情况，比如颜色分类

- id 是查看数据的内存地址

- **字典的简单语法**：

  ```
  dic = {"小明": ["6岁", 120], "小红": ["5岁", 110], "小华": ["7岁", 140], "张三": ["10岁", 150]}
  print(dic)
  dic["小黑"]=['11岁',190]
  print(dic)
  dic.pop("小明")
  print(dic)
  for i,(key ,value) in enumerate(dic.items(),1):
      print(f"{i}. {key}: {value}")
  v = dic.values()#取出所有的值
  k = dic.keys()#取出所有的键
  ```

- 字典的键只能是不可变的数据类型，而值可以是任意数据类型，使用字典的fromkeys可以将字符串的各个字符转换为键，也可以将列表内各项转换成键

- set是创建一个集合，对于集合se1和se2,可以交并差，如se1-se2是取差集，不过是以se1为主导

  ```
  se1 = {2, 4, 6, 7}
  se2 = {2, 5, 7, 3}
  #交，并，差
  temp1=se1&se2
  print(temp1)
  temp2=se1|se2
  print(temp2)
  temp3=se1-se2
  print(temp3)
  ```

- str的join函数：用逗号连接列表中的字符串

  ```
  words = ["Python", "Java", "C++"]
  result = ", ".join(words)  # 用 ", " 连接
  print(result)
  ```

- **json**:

  ```
  python数据 >> json数据：json.dumps(python数据，ensuer_ascii=False)
  python数据 >> json文件：json.dump(python字典，json文件对象，ensuer_ascii=False)
  json数据 >> python数据：json.loads(json数据)
  json文件 >> python数据：json.load(json文件对象)
  ```


- ##### Counter

  可以统计列表中各元素出现次数并生成字典

  ```
  from collections import Counter
  
  words = ["苹果", "香蕉", "苹果", "橙子", "香蕉", "苹果"]
  word_counts = Counter(words)
  
  print(word_counts)
  # 输出: Counter({'苹果': 3, '香蕉': 2, '橙子': 1})
  
  print(type(word_counts))  # <class 'collections.Counter'>
  print(isinstance(word_counts, dict))  # True（Counter是dict的子类）
  ```


- ##### zip

  zip 对象是迭代器，迭代一次后会被耗尽，再次使用时为空。代码中 dict(result2) 被调用了两次，第二次尝试迭代时 zip 已无数据。

  ```
  ls = [1, 2, 3, 4, 1, 2]
  ji = set(ls)          # ji = {1, 2, 3, 4}
  ls2 = [0] * 4         # ls2 = [0, 0, 0, 0]
  
  result2 = zip(ji, ls2)  # 创建zip对象
  print(dict(result2))    # 第一次迭代：正常输出（如 {1:0, 2:0, 3:0, 4:0}）
  print(len(dict(result2)))  # 第二次迭代：zip已耗尽，输出0！
  ```


- ##### map函数

  map函数处理列表数据很舒服，对每个元素进行函数操作后在放到另一个对象中，原本操作的列表不会发生改变。

  ```
  ls1=[12,23,389,23,45]
  sum_temp=0
  temp=map(lambda x:x*x,ls1)
  print(ls1)
  print(type(temp))
  print(temp)
  print(list(temp))#具体的使用还要强转
  ```


#### 异常处理流程

```
try:
    #写代码，可能会抛出异常
    pass
except ZeroDivisionError:#异常类型1
    pass
except ValueError:#异常类型2
    pass
except Exception:#异常类型3
    pass
else:#不出现异常会执行的
    pass
finally:#出不出现异常会执行的
    pass
```

也可以使用raise自己写异常内容：

```
try:
    desc=input('请输入信息')
    if desc=='大家好':
        raise Exception ('有多好')
except Exception as e:
    print(e)
```

#### 多条件列表型判断

```
#列表类型的判断方法
conditions=[
    num!=10,
    num<15,
    num>5
]
if all(conditions):#all 是里面全部符合才行
    print("全部符合")
elif any(conditions):#any是只有一个符合就行
    print('只有一个符合')
else :
    print('要你何用')
```

#### 类

在python中，属性的访问可以分为三种：

**1. 公开（Public）**

- **命名方式**：直接命名（如 `self.name`）

- **访问权限**：类内、子类、类外均可自由访问和修改。

  

  ```
  class Person:
      def __init__(self, name):
          self.name = name  # 公开属性
  
  p = Person("张三")
  print(p.name)  # 可以直接访问
  p.name = "李四"  # 可以直接修改
  ```

------

**2. 受保护（Protected）**

- **命名方式**：单下划线开头（如 `self._name`）

- **访问权限**：

  - **约定俗成**表示该属性或方法**仅供类内部和子类使用**，但 Python **不强制限制**，外部仍然可以访问和修改。
  - **只是一种编码规范**，告诉其他开发者"尽量不要在类外直接使用"。

  ```
  class Person:
      def __init__(self, name):
          self._name = name  # 受保护属性
  
  p = Person("张三")
  print(p._name)  # 仍然可以访问（但不推荐）
  p._name = "李四"  # 仍然可以修改（但不推荐）
  ```

------

**3. 私有（Private）**

- **命名方式**：双下划线开头（如 `self.__name`）

- **访问权限**：

  - **Python 会进行名称改写（Name Mangling）**，变成 `_类名__变量名`，外部无法直接访问原名称。
  - **仍然可以强行访问**，但强烈不建议这样做。

  ```
  class Person:
      def __init__(self, name):
          self.__name = name  # 私有属性
  
  p = Person("张三")
  # print(p.__name)  # ❌ 直接访问会报错：AttributeError
  print(p._Person__name)  # ✅ 可以强行访问（但不推荐）
  p._Person__name = "李四"  # ✅ 可以强行修改（但不推荐）
  ```

**实例属性和类属性**

```
class Student:
    school='赤峰学院'          #就是类属性，定义的每一个student对象都会有这个默认赤峰学院

    def __init__(self,name,age,gender):#构造方法里面定义的属性称之为实例属性，会因为对象创建不同而不同
        self._name=name      
        self.__age=age        
        self.gender=gender    

    def bro(self):#定义在类中的函数，自带一个属性self
        print('你是我%s的兄弟'% self._name)
```

**property的使用**

property翻译是财产、属性、不动产的意思

**1、将方法变成属性的感觉**

```
# 方式1：普通方法
class Circle:
    def area(self):
        return 3.14 * self.radius ** 2

c = Circle()
print(c.area())  # 需要括号

# 方式2：@property
class Circle:
    @property
    def area(self):
        return 3.14 * self.radius ** 2

c = Circle()
print(c.area)  # 无需括号，更简洁
```

**2、进行验证**

```
class Person:
    name='张三'
    def __init__(self, age):
        self._age = age  # 实际存储的私有属性

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value
```

上面的验证是绕过构造方法的，也可以**不绕过构造方法进行验证：**

```
class Person:
    def __init__(self, age):
        self.__age = None  # 先初始化为None
        self.age = age     # 通过setter赋值

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("年龄不能为负数")
        self.__age = value
```

**继承**

```
class Person:
    def __init__(self, age):
        self.__age = age  
       
class Student(Person):
    school='xhs'
    def __init__(self,age,name):
       Person.__init__(self,age)
        self.name=name
```

还有方法重写，多态（多态没有要求要继承）

```
class Animal:
    def speak(self):
        raise NotImplementedError("子类必须实现此方法")

class Dog(Animal):
    def speak(self):
        return "汪汪！"

class Cat(Animal):
    def speak(self):
        return "喵喵~"

def animal_talk(animal):
    print(animal.speak())

# 多态调用
dog = Dog()
cat = Cat()
animal_talk(dog)  # 输出: 汪汪！
animal_talk(cat)  # 输出: 喵喵~
```

#### 多线程

首先是import concurrent.futures 导入，然后是使用with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor创建线程池，这里max_workers=4指定最大线程数是4，对于要调用的方法直接放进去就行了，不用指定每个方法的线程，因为会自动分配未正在使用的线程给函数，同时会自动回收线程。

```
import concurrent.futures
def fun1():
def fun2():
def fun3():
def fun4():
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.submit(fun1)
    executor.submit(fun2)
    executor.submit(fun3)
    executor.submit(fun4)
print("All tasks submitted")
```



### 2、库

#### pymysql&sqlalchemy 

pip install pymysql

pip install sqlalchemy 

engine = create_engine(
    'mysql+pymysql://root:123456@localhost/media_crawler?charset=utf8mb4',
    pool_size=5,          # 连接池大小
    max_overflow=10,      # 最大溢出连接数
    pool_recycle=3600     # 连接回收时间(秒)
),连接池数量5是正常情况下有五条并发的线路，但允许临时创建不超过溢出数量的路，建立的连接会在 pool_recycle时间到达后销毁，若要使用则会建立新的链接，重置 pool_recycle时间。

#### pandas

创建空的Series

使用pd.Series可以创建空的series，并且使用dtype指定类型

`result = pd.Series(index=series.index, dtype='float64')`
或者自己指定的序列：

`result = pd.Series(index=range(0,20,2), dtype='float64')，result = pd.Series(index=ls1, dtype='float64')`

**下面这句代码的解释**

```
df['liked_count'] = df['liked_count'].apply(lambda x: str_to_num(str(x)) if pd.notna(x) else 0)
```

1. **`df['liked_count']`**
   - 这是一个 Pandas **Series（列数据）**，可以看作是一个带索引的列表。
2. **`.apply()` 方法**
   - 对 Series 中的 **每一个元素** 应用指定的函数。
   - 类似 Python 的 `map()`，但针对 Pandas 优化。
3. **`lambda x: ...`**
   - 这是一个匿名函数，`x` 代表 Series 中的 **单个值**（不是整个列表）。
   - 对每个 `x` 依次处理，类似循环遍历。
4. **`str_to_num(str(x))`**
   - 将当前值 `x` 转为字符串（`str(x)`），再传给 `str_to_num()` 函数处理。
   - 例如：`"1万+"` → `10000`，`"500"` → `500.0`。
5. **`if pd.notna(x) else 0`**
   - 先检查 `x` 是否非空（`pd.notna(x)`）。
   - 如果是有效值，执行 `str_to_num(str(x))`；
   - 如果是空值（`NaN`），返回 `0`。

#### random

```
import random
# random.seed(10)#随机数种子,随机数种子不同，随机数也不同
print(random.random())#生成一个[0.0,1.0)的随机小数
print(random.randint(0,10))#生成一个[0,10]的随机整数
print(random.uniform(0,10))#生成一个[0,10]的随机小数
choice(seq)#从seq中随机选择一个元素
shuffle(seq)#将seq打乱返回
```

#### time

Python 的 `time` 模块是处理时间的核心模块，以下是 **10 个最常用函数**的详细说明和示例：

---

**1. `time.time()` → 获取当前时间戳**

- **作用**：返回从 **1970-1-1 00:00:00 UTC** 到现在的秒数（浮点数）
- **用途**：计算代码运行时间、生成唯一时间戳

```python
import time
timestamp = time.time()  # 例如：1630000000.123456
```

---

**2. `time.sleep(seconds)` → 暂停程序**

- **作用**：让程序暂停指定秒数（支持小数）
- **用途**：延迟执行、控制循环速度

```python
print("开始")
time.sleep(2.5)  # 暂停2.5秒
print("结束")
```

---

**3. `time.localtime()` → 本地时间结构体**

- **作用**：将时间戳转换为本地时间的 **命名元组**（包含年、月、日等字段）
- **字段**：`tm_year`, `tm_mon`, `tm_mday`, `tm_hour`, `tm_min`, `tm_sec`, `tm_wday`（星期）, `tm_yday`（一年中的第几天）, `tm_isdst`（夏令时）

```python
local_time = time.localtime()
print(local_time.tm_year)  # 当前年份，如2023
print(local_time.tm_hour)  # 当前小时（24小时制）
```

---

**4. `time.strftime(format)` → 格式化时间**

- **作用**：将时间结构体转为 **自定义格式字符串**
- **常用格式符**：
  - `%Y`：4位年份（2023）
  - `%m`：月份（01-12）
  - `%d`：日（01-31）
  - `%H`：小时（00-23）
  - `%M`：分钟（00-59）
  - `%S`：秒（00-59）

```python
formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 输出：2023-08-20 14:30:15
```

---

**5. `time.strptime(string, format)` → 解析时间字符串**

- **作用**：将时间字符串解析为时间结构体
- **用途**：处理用户输入的时间数据

```python
time_struct = time.strptime("2023-08-20", "%Y-%m-%d")
print(time_struct.tm_year)  # 输出：2023
```

---

**6. `time.mktime(struct_time)` → 时间结构体转时间戳**

- **作用**：将本地时间结构体转为时间戳

```python
struct_time = time.localtime()
timestamp = time.mktime(struct_time)  # 转换为时间戳
```

---

**7. `time.perf_counter()` → 高精度计时器**

- **作用**：返回高精度的性能计数器值（用于基准测试）
- **特点**：不受系统时间更改影响

```python
start = time.perf_counter()
# 执行代码...
end = time.perf_counter()
print(f"耗时：{end - start:.4f}秒")  # 精确到微秒
```

---

**8. `time.process_time()` → 进程CPU时间**

- **作用**：返回当前进程的CPU时间（不包括sleep时间）
- **用途**：分析代码的实际CPU占用

```python
start = time.process_time()
# 执行CPU密集型代码...
end = time.process_time()
print(f"CPU耗时：{end - start}秒")
```

#### Pillow

| 功能分类          | 具体能力                             | 示例场景                     |
| :---------------- | :----------------------------------- | :--------------------------- |
| **图像打开/保存** | 支持 JPEG、PNG、GIF、BMP 等 30+ 格式 | 读取用户上传的图片，转换格式 |
| **基本图像处理**  | 裁剪、旋转、缩放、翻转               | 生成缩略图，调整图片方向     |
| **颜色调整**      | 亮度、对比度、色相、饱和度           | 照片滤镜效果                 |
| **高级处理**      | 滤镜（模糊、锐化）、透明度处理       | 添加艺术效果                 |
| **绘图功能**      | 绘制文字、几何图形                   | 添加水印或标注               |
| **像素级操作**    | 直接访问/修改像素数据                | 自定义图像算法               |

下载：pip install pillow

使用：from PLI import Image 

#### prettytable

```
pip install prettytable
```

1. **创建简单表格**

```
from prettytable import PrettyTable

# 创建表格对象
table = PrettyTable()

# 添加列
table.field_names = ["Name", "Age", "City"]

# 添加行数据
table.add_row(["Alice", 25, "New York"])
table.add_row(["Bob", 30, "Los Angeles"])
table.add_row(["Charlie", 35, "Chicago"])

# 打印表格
print(table)
```

输出结果：

```
+---------+-----+-------------+
|   Name  | Age |     City    |
+---------+-----+-------------+
|  Alice  | 25  |   New York  |
|   Bob   | 30  | Los Angeles |
| Charlie | 35  |   Chicago   |
+---------+-----+-------------+
```

2. **逐列添加数据**

```
table = PrettyTable()

table.add_column("Name", ["Alice", "Bob", "Charlie"])
table.add_column("Age", [25, 30, 35])
table.add_column("City", ["New York", "Los Angeles", "Chicago"])

print(table)
```

#### datetime

引用是：from datetime import datetime

可以使用年月日的数字坐标创建一个时间对象dt = datetime(2023, 5, 15, 14, 30, 15)

获取当前时间是now = datetime.now()，格式为2025-07-12 13:52:31.756449

也可以使用时间间隔计算时间

```
import time
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
from datetime import datetime
from datetime import timedelta
delta = timedelta(days=5, hours=3, minutes=30)

# 日期时间计算
now = datetime.now() 
future = now + delta
past = now - delta

print(future)
print(past)
```

#### moviepy

处理视频音频的库

#### jsonpath

用来在 JSON 数据结构中快速定位和提取想要的字段。

| JSONPath 表达式                 | 说明                         | 示例结果                                                     |
| ------------------------------- | ---------------------------- | ------------------------------------------------------------ |
| `$`                             | 根节点                       | 整个 JSON                                                    |
| `$.store.book`                  | 选中所有书本                 | `[ {..}, {..}, {..} ]`                                       |
| `$.store.book[*].title`         | 选中所有书的标题             | `["Python入门", "哈利波特", "冰与火之歌"]`                   |
| `$..price`                      | 选中所有 price 字段（递归）  | `[10, 20, 30, 100]`                                          |
| `$.store.book[0]`               | 选中第一本书                 | `{ "category":"reference","title":"Python入门","price":10 }` |
| `$.store.book[1:3]`             | 选中第 2 到第 3 本书（切片） | `[{"哈利波特"...}, {"冰与火之歌"...}]`                       |
| `$.store.book[?(@.price < 25)]` | 选中价格小于 25 的书         | `[{"Python入门"...}, {"哈利波特"...}]`                       |
| `$..*`                          | 选中所有元素                 | 返回所有值                                                   |

