---
name: wtpr
description: 在 git worktree 分支上执行完整的 PR 提交流程：自动识别当前 worktree、处理未提交改动、rebase 到最新 origin/dev、force push、创建或更新 GitHub PR。当用户在 worktree 中想提交 PR、追加新 commit 到已有 PR、或执行 wtpr 命令时使用。
---

# wtpr — Worktree PR 提交流程

base 分支固定为 `dev`，合并策略默认 **rebase and merge**。

## Phase 1：Gather（批量采集，无副作用）

```bash
git worktree list                              # 确定 WORKTREE 上下文
git status --short                             # DIRTY 检查
git fetch origin                               # 同步远端（只读）
git rev-list origin/dev..HEAD --count          # UNPUSHED 数量
gh pr view --json state,url,title,number 2>/dev/null  # PR_STATE
```

`git fetch origin` 失败（网络/认证）→ 硬退出并报错，后续判断依赖远端数据。

## Phase 2：Compute（纯判断，无执行）

| 变量 | 含义 |
|------|------|
| `WORKTREE` | 当前目录 / 命令参数 / 对话上下文，三者任一可确定目标 |
| `DIRTY` | git status 非空 |
| `UNPUSHED` | HEAD 超出 origin/dev 的 commit 数 |
| `PR_STATE` | none / open / merged / closed |

**PR_STATE 判断优先级**：
1. 对话上下文中有 PR URL → `open`
2. 否则用 `gh pr view` 结果
3. 两者都不确定 → 询问用户

## Phase 3：Execute（按序执行）

### Step 1：确定目标 worktree

- 能确定 → 继续
- 不能确定 → 列出所有 worktree，询问用户选择哪个

### Step 2：处理 DIRTY

DIRTY = false → 跳过

DIRTY = true：
1. 分析 diff，**自动生成** commit message（不让用户输入）
2. 询问：用这个 message **commit**，还是 **stash**？
3. 用户不满意 message → 重新生成，循环直到确认
4. 执行 `git add -A && git commit` 或 `git stash`
5. 重新检查 DIRTY，直到干净

### Step 3：Rebase（无条件执行）

```bash
git rebase origin/dev
```

`git rebase` 通过 **patch-id**（diff 内容哈希）自动识别并跳过内容相同但 SHA 不同的 commit（rebase-and-merge 副产品），无需预先判断是否需要 rebase。

有冲突：
1. 列出冲突文件
2. 等待用户解决
3. 用户确认解决后执行 `git rebase --continue`
4. 循环直到无冲突

### Step 4：Push

```bash
git push --force-with-lease
```

rebase 重写了 commit SHA，必须 force push。`--force-with-lease` 在覆盖前校验远端分支未被他人修改。

### Step 5：PR 操作

| PR_STATE | 动作 |
|----------|------|
| `none` | 自动生成 title/body，直接 `gh pr create`（无需用户确认） |
| `open` | 显示 PR URL + 提示新 commit 已追加 |
| `merged` / `closed` | 提示 PR 已关闭，建议执行 `wtrm` 清理 |

## 参考

完整流程状态机见 [prototype.md](prototype.md)
