# Git

开梯子后拉github的项目一直拉不下来，一看是所有的请求都走了梯子的代理，需要手动配置git config --global http.proxy http://127.0.0.1:7890，让git的请求也走代理。

如果后面不想让请求都走代理，那么可以git config --global --unset http.proxy移除掉。



**gitbash新建远程库之后上传本地整个文件夹的过程：**

首先进入路径cd /d/else/else/Ghosten-Player 

其次初始化git init（注意自己的分支名称）

建立远程连接git remote add origin https://github.com/你的用户名/仓库名.git

所有文件加入暂存区 git add .

添加说明 git comment -m "首次提交"

想改名字的话git branch -M main

最后提交 git push origin main



**gitbash远程库中已经有内容，本地文件夹首次提交的操作**

首先进入路径cd /d/else/else/Ghosten-Player 

其次初始化git init（注意自己的分支名称）

建立远程连接git remote add origin https://github.com/你的用户名/仓库名.git

先拉一下，拉到本地git pull origin main --allow-unrelated-histories（因为本地分支没有提交过，所以要允许没有提交历史的分支进行拉取）

所有文件加入暂存区 git add .

添加说明 git comment -m "首次提交"

想改名字的话git branch -M main

最后提交 git push -u origin main 首次的话尽量带u，相当于为本地分支设置一个默认对应的远程分支



**改动更新：**

首先可以 git status 看下那些文件修改过

git add . 改动的添加到暂存区

添加说明git commit -m "更新"

提交推送分支git push origin main





切换分支 git checkout main

新建分支 git checkout -b new

合并分支若切换到main分支里，然后git merge new,则是将new合并到main中

**合并冲突**时会出现(main|MERGING)，要手动去冲突文件删除冲突标志信息

然后 git add 文件名，提交合并信息git commit -m "合并冲突"，最后删除分支 git branch -d new 

 查看远程分支 git branch -r

删除分支 git branch -d new

删除远程分支 git push origin --delete  new 

git fetch origin



中文乱码 git config --global core.quotepath false

查看历史版本：git log --oneline



某个场景：如果你的远程仓库某个文件修改过，你本地仓库的该文件也修改过，你想先pull一下该文件，那么 需要用到git stash，先把该文件的修改藏起来，然后git pull，最后git stash pop 这时候可能会冲突。
