---
name: git-commit
description: "**Must use before every git commit.** Use when staging files, writing commit messages, or committing changes."
---

# Git Commit 规范

## 1. 暂存与提交

- `md/指令/` 下的文件视同普通代码文件，正常一起 `git add` 和 `commit`
- 禁止查看 `md/指令/` 文件内容
- 提交后运行 `git status --short`，确认工作区干净

## 2. 提交颗粒度

| 场景 | 做法 |
|------|------|
| 独立的修复/功能/文档 | 各自单独 commit |
| 对同一处的反复修改 | `git commit --amend` 合并 |
| 合并多个连续 commit | `git reset --soft` + 重新 commit |
| 合并非连续 commit | `git rebase -i` |

## 3. Commit Message

```
type: 简短中文说明

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

## 4. 禁止事项

- ❌ `git add -f`
- ❌ 添加额外参数禁用 git 功能
- ❌ 多个不相关修改合为一个 commit
- ❌ commit message 使用英文
