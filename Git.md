# Git

开梯子后拉github的项目一直拉不下来，一看是所有的请求都走了梯子的代理，需要手动配置git config --global http.proxy http://127.0.0.1:7890，让git的请求也走代理。

如果后面不想让请求都走代理，那么可以git config --global --unset http.proxy移除掉。



**gitbash新建库之后上传整个文件夹的过程：**

首先进入路径cd /d/else/else/Ghosten-Player 

其次初始化git init（注意自己的分支名称）

建立远程连接git remote add origin https://github.com/你的用户名/仓库名.git

所有文件加入暂存区 git add .

添加说明 git comment -m "首次提交"

想改名字的话git branch -M main

最后提交 git push origin main



改动更新：

首先可以 git status 看下那些文件修改过

git add . 改动的添加到暂存区

添加说明git commit -m "更新"

git push origin main



切换分支 

git checkout main

git fetch origin

