---
name: git-commit-assistant
description: 该技能用于在任意 Git 仓库中安全执行规范化提交与推送（Conventional Commits），并处理 pull/rebase 冲突与 worktree 管理等常见 Git 工作流问题。
---

# Git Commit 智能助手

## 触发条件

- 需要完成一次规范的 Git 提交/推送
- 需要根据变更生成 Conventional Commits 提交消息
- 需要在 `git pull` / `git pull --rebase` 之间做选择或处理冲突
- 需要创建、列出、清理 Git worktree

## 总体原则（必须遵守）

- 禁止使用 `--force` / `--force-with-lease`、`--no-verify`
- 默认在本地提交成功后执行 `git push`（除非安全检查阻止）
- 提交前执行敏感文件检查；发现疑似敏感文件时停止并提示处理
- push 前确认本地提交成功且工作区状态符合预期

## 快速开始：规范提交并推送

### 0) 并行获取仓库状态

尽可能并行运行以下命令，并将输出用于后续分析：
- `git status`
- `git diff --staged`
- `git diff`
- `git log --oneline -5`

可选：运行 `scripts/git_snapshot.sh` 一次性输出上述信息。

### 1) 分析变更并确定提交类型

按变更意图选择 `type`（必要时结合 `git log --oneline -5` 的风格）：
- `feat`：新增对外可感知能力
- `fix`：修复缺陷、回归预期行为
- `docs`：仅文档
- `style`：仅格式/样式（不改逻辑）
- `refactor`：重构（不引入新功能/不修 bug）
- `test`：测试相关
- `build`：构建/依赖/CI
- `chore`：杂项

确定 `scope`：
- 优先使用顶层目录/模块/包名（例如 `api`、`cli`、`auth`、`docs`）
- 若变更跨多个模块，选择最主要影响面；无法归类时省略 scope

### 2) 生成提交消息（Conventional Commits）

按模板生成（subject ≤ 50 字符，祈使句，首字母小写）：

```text
<type>(<scope>): <subject>

<body>
```

body 仅解释“为什么”（动机/背景/约束/权衡），避免复述 diff。

更多细则与示例：加载 `references/conventional-commits.md`。

### 3) 安全检查（敏感文件）

在 `git add` 或提交前执行：
- `scripts/check_sensitive_files.sh`

如脚本输出警告：
- 停止提交/推送流程
- 将文件移出暂存区：`git restore --staged <path>`
- 添加到 `.gitignore` 或替换为 `.env.example`
- 如已泄露，执行凭证轮换；必要时清理历史（需要人工确认后再进行）

更多规则与处理建议：加载 `references/sensitive-files.md`。

### 4) 暂存、提交、确认

如存在未暂存变更且本次提交应包含全部改动，执行：
- `git add .`

然后用 HEREDOC 执行提交（将生成的消息填入）：

```bash
git commit -F - <<'EOF'
<type>(<scope>): <subject>

<body>
EOF
```

提交后确认：
- `git status`

### 5) 推送并展示结果

执行：
- `git push`

如提示未设置 upstream：
- 获取当前分支：`git branch --show-current`
- 优先使用 `origin`：`git push -u origin <branch>`

push 失败或被环境阻止时，保留错误输出并提示用户下一步。

## 工作流：拉取更新（merge vs rebase）

### 选择策略

- 需要保持线性历史、且本地提交未共享：优先 `git pull --rebase`
- 需要保留合并提交或分支已共享：使用 `git pull`

### 冲突处理（核心命令）

- 发生 rebase 冲突：解决后 `git add ...`，继续 `git rebase --continue`，必要时 `git rebase --abort`
- 发生 merge 冲突：解决后 `git add ...`，完成合并 `git commit`（或按提示完成）

详细步骤与常见坑：加载 `references/pull-rebase-conflicts.md`。

## 工作流：Git worktree 管理

- 列出现有 worktree：`git worktree list`
- 新增 worktree：`git worktree add <path> <branch>`
- 删除 worktree：`git worktree remove <path>`
- 清理失效引用：`git worktree prune`

详细用法：加载 `references/worktree.md`。

## 资源

- scripts：
  - `scripts/git_snapshot.sh`：输出 status/diff/log 快照
  - `scripts/check_sensitive_files.sh`：按路径规则扫描疑似敏感文件
- references：
  - `references/conventional-commits.md`
  - `references/pull-rebase-conflicts.md`
  - `references/worktree.md`
  - `references/sensitive-files.md`
