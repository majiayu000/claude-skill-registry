---
name: git-advanced
description: Git 高级操作
version: 1.0.0
author: terminal-skills
tags: [devops, git, version-control, branch]
---

# Git 高级操作

## 概述
分支策略、rebase、cherry-pick、hooks 等高级 Git 技能。

## 分支管理

### 分支操作
```bash
# 创建分支
git branch feature/new-feature
git checkout -b feature/new-feature
git switch -c feature/new-feature

# 切换分支
git checkout main
git switch main

# 删除分支
git branch -d feature/merged
git branch -D feature/unmerged        # 强制删除

# 删除远程分支
git push origin --delete feature/old

# 重命名分支
git branch -m old-name new-name

# 查看分支
git branch -a                         # 所有分支
git branch -v                         # 带最后提交
git branch --merged                   # 已合并分支
git branch --no-merged                # 未合并分支
```

### 分支追踪
```bash
# 设置上游分支
git branch --set-upstream-to=origin/main main
git push -u origin feature/new

# 查看追踪关系
git branch -vv
```

## Rebase 操作

### 基础 rebase
```bash
# 变基到 main
git checkout feature
git rebase main

# 交互式 rebase
git rebase -i HEAD~5
git rebase -i main

# 交互式命令
# pick   - 保留提交
# reword - 修改提交信息
# edit   - 修改提交内容
# squash - 合并到上一个提交
# fixup  - 合并但丢弃提交信息
# drop   - 删除提交

# 继续/中止 rebase
git rebase --continue
git rebase --abort
git rebase --skip
```

### 合并提交
```bash
# 合并最近 3 个提交
git rebase -i HEAD~3
# 将后两个 pick 改为 squash 或 fixup

# 修改历史提交信息
git rebase -i HEAD~3
# 将 pick 改为 reword
```

## Cherry-pick

```bash
# 选择单个提交
git cherry-pick commit-hash

# 选择多个提交
git cherry-pick commit1 commit2 commit3

# 选择范围（不包含起始）
git cherry-pick start-commit..end-commit

# 不自动提交
git cherry-pick -n commit-hash

# 解决冲突后继续
git cherry-pick --continue
git cherry-pick --abort
```

## Stash 暂存

```bash
# 暂存修改
git stash
git stash push -m "work in progress"

# 暂存包括未跟踪文件
git stash -u
git stash --include-untracked

# 查看暂存列表
git stash list

# 恢复暂存
git stash pop                         # 恢复并删除
git stash apply                       # 恢复但保留
git stash apply stash@{2}             # 指定暂存

# 查看暂存内容
git stash show -p stash@{0}

# 删除暂存
git stash drop stash@{0}
git stash clear                       # 清空所有
```

## 撤销操作

### 撤销工作区修改
```bash
# 撤销单个文件
git checkout -- file.txt
git restore file.txt

# 撤销所有修改
git checkout -- .
git restore .
```

### 撤销暂存区
```bash
# 取消暂存
git reset HEAD file.txt
git restore --staged file.txt

# 取消所有暂存
git reset HEAD
```

### 撤销提交
```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃修改）
git reset --hard HEAD~1

# 创建撤销提交
git revert commit-hash
git revert HEAD

# 撤销多个提交
git revert HEAD~3..HEAD
```

### 修改提交
```bash
# 修改最后一次提交
git commit --amend
git commit --amend -m "new message"
git commit --amend --no-edit          # 不修改信息

# 添加遗漏文件
git add forgotten-file
git commit --amend --no-edit
```

## 远程操作

```bash
# 查看远程
git remote -v

# 添加远程
git remote add upstream https://github.com/original/repo.git

# 获取远程更新
git fetch origin
git fetch --all

# 拉取并变基
git pull --rebase origin main

# 强制推送（谨慎使用）
git push --force-with-lease origin feature
```

## Git Hooks

### 常用 hooks
```bash
# hooks 位置
.git/hooks/

# 常用 hooks
pre-commit      # 提交前
prepare-commit-msg  # 准备提交信息
commit-msg      # 提交信息验证
post-commit     # 提交后
pre-push        # 推送前
```

### pre-commit 示例
```bash
#!/bin/bash
# .git/hooks/pre-commit

# 运行 lint
npm run lint
if [ $? -ne 0 ]; then
    echo "Lint failed. Commit aborted."
    exit 1
fi

# 运行测试
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

exit 0
```

### commit-msg 示例
```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# 检查提交信息格式
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"; then
    echo "Invalid commit message format."
    echo "Format: type(scope): message"
    exit 1
fi

exit 0
```

## 常见场景

### 场景 1：同步 fork 仓库
```bash
# 添加上游仓库
git remote add upstream https://github.com/original/repo.git

# 获取上游更新
git fetch upstream

# 合并到本地
git checkout main
git merge upstream/main

# 推送到 fork
git push origin main
```

### 场景 2：清理历史中的大文件
```bash
# 使用 git-filter-repo（推荐）
git filter-repo --path large-file.zip --invert-paths

# 或使用 BFG
bfg --delete-files large-file.zip
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 场景 3：二分查找 bug
```bash
# 开始二分
git bisect start

# 标记当前为坏
git bisect bad

# 标记已知好的提交
git bisect good v1.0.0

# Git 会自动切换到中间提交
# 测试后标记
git bisect good  # 或 git bisect bad

# 找到后重置
git bisect reset
```

### 场景 4：子模块管理
```bash
# 添加子模块
git submodule add https://github.com/user/repo.git path/to/submodule

# 初始化子模块
git submodule init
git submodule update

# 克隆时包含子模块
git clone --recursive https://github.com/user/repo.git

# 更新子模块
git submodule update --remote
```

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| 合并冲突 | 手动解决后 `git add` + `git commit` |
| rebase 冲突 | 解决后 `git rebase --continue` |
| 误删分支 | `git reflog` 找回 |
| 推送被拒绝 | `git pull --rebase` 后重试 |

```bash
# 查看操作历史
git reflog

# 恢复误删的提交
git checkout -b recovery commit-hash
```
