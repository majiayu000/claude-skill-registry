---
name: git-kingreatwill-open
description: 1. 通过 git blame 找到谁动了某行代码
---

1. 通过 git blame 找到谁动了某行代码
```
$ cd linux-stable
$ git blame -L 50,50 init/main.c
78634061 (Frederic Weisbecker 2017-10-27 04:42:28 +0200 50) #include <linux/sched/isolation.h>
```
2. 通过 git log 获取某笔 commit 或 tag 的提交时间

在分析衰退时，如果找到了某笔变更，然后，又想进一步确定这笔变更是在哪个版本（Tag）引入的，这个时候可以先找一下该 commit 的时间，然后再比对 Tag 的修订时间。那么如何查看 commit 和 tag 的引入时间呢？以 HEAD 这笔 commit 举例如下：
```
$ date -d @`git log -1 --format=%ct HEAD` +%Y%m%d-%H%M%S
20190719-172216
```
把 HEAD 替换为具体的 commit 和 tag 号即可获得对应时间。对于 Linux 而言，通常不需要这么复杂，在找到某个变更之后，用下面这个方法就可以确定该变更对应的内核主版本：
```
$ git show HEAD:Makefile
```
因为 Makefile 中记录了内核的版本号。

3. 通过 git bisect 自动二分法快速定位问题

某个系统，在开发过程中一直都没测试出问题，突然有一天，发现 Bug。这种蛮多情况是衰退，如果这个 Bug 的复现几率很大的话，就可以直接用二分法快速定位了。git bisect 就可以辅助进行自动二分法。

简单的话，就是不停地告诉 git bisect，哪一个是好的，哪一个是坏的，如果有固定的复现脚本，那么在获得第一对 bad, good 的 commit 后，就可以直接让 git bisect 自动二分法。举例说明：
```
$ git bisect start
$ git bisect bad efa5cf
$ git bisect good b6fcf0
$ git bisect run grep -q UCONFIG Makefile
```
说明：

- efa5cf：第一个发现有问题的版本

- b6fcf0：某个确认没问题的版本

- grep -q UCONFIG Makefile：能找到 UCONFIG 就是好的，找不到就是有问题

在设定完 bad, good 后，git bisect 会自动切出中间某个版本，然后针对这个版本，可以进行配置、编译、运行，然后根据测试结果设定该版本为 bad or good，例如：git bisect bad HEAD，以此类推，git bisect 会不停地切出中间版本，直到可以判断第一个 bad 的版本，这个版本就是引入衰退的变更。

这个完整的测试过程如果可以自动化，就可以写成脚本，作为 git bisect run 的参数，这样就可以避免手动跑测试。上面的 grep 命令是经过初步分析后，找出的简化策略。如果都能这样通过检索代码变更本身就可以判断问题，那确实可以省去不少力气。

4. 用 git submodule sync 更新 git submodule 的远程仓库地址

前段我们把很多仓库从 github 搬到了 gitee，搬完以后 Linux Lab 下的 .gitmodules 和 .git/config 都得更新 url 地址，但是更新完以后并不能直接用，还得用 git submodule sync 同步一下：
- 第 1 步，用 sed 替换 .gitmodules 和 .git/config 中的 url

- 第 2 步，执行 git submodule sync

5. 为不同 Git 仓库配置不同的 ssh key

为优化下载效率，最近把 Linux Lab 迁移到了码云，配置了不同的 ssh 私钥/公钥。为了避免在命令行每次都要额外指定不同的参数，可以添加一个配置文件。

例如，给码云的私钥文件命名为 gitee.id_rsa，把它放到 ~/.ssh 目录下并修改权限。
```
$ chmod 600 ~/.ssh/gitee.id_rsa
$ chmod 700 ~/.ssh
```
之后，新增一个 ~/.ssh/config，加入如下配置：
```
$ cat ~/.ssh/config
Host gitee
HostName gitee.com
IdentityFile ~/.ssh/gitee.id_rsa
User git
```
这样就可以直接类似下面下载和上传，而无需每次输入密码或指定密钥了，同时省掉了 git@。
```
$ git clone gitee:aaaa/yyyy.git

$ cd cloud-lab
$ touch xxxx
$ git add xxxx
$ git commit -s -m "add xxxx"

$ git push gitee:aaaa/yyyy.git master
```

6. 用 git fetch 取代 git clone，实现断点续传

用 git clone 下载大型代码仓库时，一旦网络中断，后果是哭爹喊娘，但是于事无补，叫天天不应。

因为 git clone 没有实现断点续传，不知道开发者脑子“进了什么水”？Linus 求骂 ;-)

没关系，用 git fetch 可以实现类似效果，而且极其简单。

先用 git init 创建一个空目录：
```
$ mkdir test-repo
$ cd test-repo
$ git init
```
再在里头用 git fetch 要 clone 的仓库：
```
$ git fetch https://gitee.com/tinylab/cloud-lab.git
$ git checkout -b master FETCH_HEAD
```
git fetch 只能一个一个 branch fetch，fetch 完，把 FETCH_HEAD checkout 出来新建对应的分支即可。如果 git fetch 中途中断网络，可以再次 git fetch，git fetch 可以续传，不至于一断网就前功尽弃。



[Git科普文，Git基本原理&各种骚操作](https://www.cnblogs.com/iisheng/p/13425658.html)

## git commit提交类型规范
init: 初始化
feat: 新特性
fix: 修改问题
refactor: 代码重构
docs: 文档修改
style: 代码格式修改, 注意不是 css 修改
test: 测试用例修改
build: 构建项目
chore: 其他修改, 比如依赖管理,构建过程或者辅助工具的变动
ci: 对ci配置文件和脚本的改动
scope: commit 影响的范围, 比如: route, component, utils, build...
subject: commit 的概述
format: 格式化代码
perf: 提高性能/优化
test: 增加测试代码
patch: 添加重要补丁
file: 新加文件
publish: 发布新版本
tag: 发布版本/添加标签
config: 修改配置文件
git: 修改.gitignore文件
revert: 恢复,把这次提交的修改还原

## 导入一个已有的代码仓库到新的代码仓库
```
git clone --bare https://git.example.com/your/project.git your_path
cd your_path
git remote set-url origin https://new.example.com/new.git
git push origin --tags && git push origin --all
```

## 从 Git 历史记录中生成 Changelog 文件
https://github.com/orhun/git-cliff