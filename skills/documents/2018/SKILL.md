---
title: git常用技巧
category: study
---

## git常用技巧

### 1.fork后想更新源仓库的改动

```javascript

git remote -v //查看远程状态

git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git //确定一个将被同步给 fork 远程的上游仓库 

git fetch upstream //从上游仓库 fetch 分支和提交点，提交给本地 master，并会被存储在一个本地分支 

git checkout master

git merge upstream/master //把 upstream/master 分支合并到本地 master 上，这样就完成了同步，并且不会丢掉本地修改的内容。 

git push origin master //提交到远程

```

### 2.暂存

```javascript

git stash  //把当前改动放入暂存区

git stash list //查看有哪些暂存

git stash pop stash@{0} //取出暂存内容

```

### 3.新建/删除分支

```javascript

git checkout -b iss53

//相当于

git branch iss53

git checkout iss53

git push origin --delete <branchName> //删除远程分支

git branch -D <branchName> //删除本地分支

git remote show origin // 查看remote地址，远程分支

git fetch --prune origin // 清理远程已删除本地还存在的分支 git fetch -p 或者 git pull -p

git remote update origin -p // 更新分支列表


```

### 4.撤销

```javascript

//文件被修改了，但未执行git add操作(working tree内撤销)
git checkout fileName
git checkout .

//同时对多个文件执行了git add操作，但本次只想提交其中一部分文件
git add .
 git status
//取消暂存
 git reset HEAD <filename>

//文件执行了git add操作，但想撤销对其的修改（index内回滚）
//取消暂存
git reset HEAD fileName
//撤销修改
git checkout fileName

//修改的文件已被git commit，但想再次修改不再产生新的Commit
//修改最后一次提交 
git add sample.txt
git commit --amend -m"说明"

//已在本地进行了多次git commit操作，现在想撤销到其中某次Commit
git reset [--hard|soft|mixed|merge|keep] [commit|HEAD]

```

### 5.回滚

```javascript

//使用reset

git log

git reset --hard COMMITID

git push origin master -f

//使用revert删除最后一次远程提交
git revert HEAD
git push origin master

//如果你每次更新线上，都会打tag
git checkout <tag>

```