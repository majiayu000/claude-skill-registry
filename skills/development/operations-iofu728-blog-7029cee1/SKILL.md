---
title: git rebase 的另解
date: 2018-09-07 13:38:52
tags: [Git]
description: git rebase 另解
---

我们都知道 git rebase 在合并的时候能把这一段时间内一堆 commit 变成一个，对理清开发思路有着不可磨灭的功效

rebase 冲突处理的数量与 commit 一致，但当 commit 数过多时，处理冲突可以说是烦死人

以下是我同事给出的一种解决方案

```bash
git checkout develop # 需要合并入的目标分支
git pull origin develop # 拉取最新的目标分支的代码
git checkout -b new_branch # 一个新的分支，该分支需要合入到目标分支，请起一个有意义的名字
git merge --squash feature_branch # 本地改动所在的分支
git commit # 不要带-m参数

# 修改commit message，合并成一次提交的message
git push origin new_branch # 将改动push到远端
# 用new_branch提一个merge request
```
