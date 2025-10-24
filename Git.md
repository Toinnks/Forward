# Git

开梯子后拉github的项目一直拉不下来，一看是所有的请求都走了梯子的代理，需要手动配置git config --global http.proxy http://127.0.0.1:7890，让git的请求也走代理。

如果后面不想让请求都走代理，那么可以git config --global --unset http.proxy移除掉。



#### **gitbash新建远程库之后上传本地整个文件夹的过程：**

首先进入路径cd /d/else/else/Ghosten-Player 

其次初始化git init（注意自己的分支名称）

建立远程连接git remote add origin https://github.com/你的用户名/仓库名.git

所有文件加入暂存区 git add .

添加说明 git comment -m "首次提交"

想改名字的话git branch -M main

最后提交 git push origin main



#### **gitbash远程库中已经有内容，本地文件夹首次提交的操作**

首先进入路径cd /d/else/else/Ghosten-Player 

其次初始化git init（注意自己的分支名称）

建立远程连接git remote add origin https://github.com/你的用户名/仓库名.git（这是https连接方式）

先拉一下，拉到本地git pull origin main --allow-unrelated-histories（因为本地分支没有提交过，所以要允许没有提交历史的分支进行拉取）

所有文件加入暂存区 git add .

添加说明 git comment -m "首次提交"

想改名字的话git branch -M main

最后提交 git push -u origin main 首次的话尽量带u，相当于为本地分支设置一个默认对应的远程分支



#### 改动更新：

首先可以 git status 看下那些文件修改过

git add . 改动的添加到暂存区

添加说明git commit -m "更新"

提交推送分支git push origin main



#### 分支操作

切换分支 git checkout main

新建分支 git checkout -b new

查看远程分支 git branch -r

合并分支：若切换到main分支里，然后git merge new,则是将new合并到main中

删除分支 git branch -d new

删除远程分支 git push origin --delete  new 



**合并冲突**时会出现(main|MERGING)，要手动去冲突文件删除冲突标志信息

然后 git add 文件名，提交合并信息git commit -m "合并冲突"，最后删除分支 git branch -d new 



中文乱码 git config --global core.quotepath false

查看历史版本：git log --oneline



某个场景：如果你的远程仓库某个文件修改过，你本地仓库的该文件也修改过，你想先pull一下该文件，那么 需要用到git stash，先把该文件的修改藏起来，然后git pull，最后git stash pop， 这时候可能会冲突。



**git使用SSH方式连接github**

```
#打开git bash，输入
ssh-keygen -t ed25519 -C "007sun6@gmail.com"

# 启动 ssh-agent
eval "$(ssh-agent -s)"

# 将 SSH 私钥添加到 ssh-agent
ssh-add ~/.ssh/id_ed25519

cat ~/.ssh/id_ed25519.pub
#复制输出的全部内容（以 ssh-ed25519 开头），进入github，点击头像，点击设置，选择ssh密钥，将粘贴的内容保存上去。

#测试ssh连接
ssh -T git@github.com
#设置远程连接
git remote set-url origin git@github.com:Toinnks/Forward.git

```



#### git中回滚有多种情况

文件未修改不需要回滚

1. 文件已经修改但舍弃修改的情况

   1. 文件已经git add

      git restore

   2. 文件已经git commit

      如果是撤销commit，此时会保留修改，那么就git restore --staged 文件名，否则就git restore

   3. 文件已经push

      你git restore，远程

2. 文件已经修改但保存修改版本的情况

   1. 文件已经git add

      使用git stash暂存，然后git stash pop恢复

   2. 文件已经git commit

   3. 文件已经push

      git revert <commit_id>

git rm --cached 文件名（取消追踪）
