---
name: dev-team
description: "Multi-agent development team orchestration. Use when managing coding agents (Codex, Claude Code, Gemini, Cursor) for automated software development: (1) Spawning agents for tasks, (2) Monitoring agent status, (3) Managing git worktrees, (4) Automated code review, (5) Handling notifications via Feishu."
---

# Dev Team

One-person dev team orchestration using Levi as the orchestrator.

## Main Agent Rules (入口摘要)

主 Agent 是编排器（orchestrator），不是默认主力编码器。

关键准则：

- `PR` 优先：正式开发默认使用 `--completion-mode pr`
- 禁止 SubAgent 在 `main/master` 上直接开发（`spawn-agent.sh` 已拦截）
- 主 Agent 使用最小上下文：优先看状态机与聚合结果，而不是全量日志
- 阶段化编排：明确 `--phase build|review|fixup`
- 自动化负责推进与收口（`check/review/fixup/cleanup/prune`），人工保留最终产品决策与 GitHub `approve`
- `SubAgent DONE` 不等于任务完成：合并前必须做 post-task review（DoD + 真实验证 + 指标门禁）

详细说明见：

- `references/AGENTS.md`（主 Agent 行动准则）
- （已合并入 `references/AGENTS.md`）编排模型与状态机
- （已合并入 `references/AGENTS.md`）主 Agent 最小上下文操作手册

## Quick Start

### 首次使用

```bash
# 运行设置检查
scripts/setup-check.sh
```

### 启动内置 dev-board 控制面板

`dev-team` 已内置 `scripts/dev-board/`，可直接启动：

```bash
./scripts/run-dev-board.sh
```

默认地址：`http://localhost:4310`

### Spawn an Agent

正式功能开发（推荐 `PR` 流程）：

```bash
scripts/spawn-agent.sh \
  --agent auto \
  --phase build \
  --repo-path ./scripts/dev-board \
  --branch feat/auth-timeout-fix \
  --description "修复登录超时错误" \
  --completion-mode pr \
  --prompt-file /tmp/task-prompt.txt
```

本地 smoke / 临时探索（仅无 PR 场景使用 `session`）：

```bash
scripts/spawn-agent.sh \
  --agent auto \
  --repo-path ./scripts/dev-board \
  --branch fix/auth-error \
  --description "修复登录超时错误" \
  --phase build \
  --completion-mode session \
  --prompt-file /tmp/task-prompt.txt
```

### Check Agent Status

```bash
cat assets/active-tasks.json
```

### Monitor Agents

```bash
scripts/check-agents.sh
```

### Mandatory: Post-task Review Gate (合并前必做)

当 SubAgent 报告完成（例如 `TASK_*_DONE`）后，主 Agent 必须执行：

```bash
# 1) 看任务状态与日志摘要
scripts/check-agents.sh

# 2) 审核 subagent 提交内容（示例）
git -C <subagent-worktree> show --name-only --oneline -n 1 <commit>

# 3) 在目标仓库执行任务 DoD 规定的真实验证命令（示例）
# 例如：真实 ingestion/validate、真实 API 调用、非 mock 链路
```

通过标准：
- DoD 条款全部满足
- 至少 1 条真实链路验证通过（非 mock）
- 指标达到任务阈值（如 successRate/evidenceBindingRate/citationNonEmptyRate/fallbackRate）

不通过处理：
- 不合并
- 立即派发 fixup（同分支或新分支）
- 在 docs 中记录“未通过项 + 修复输入”

---

## Supported Agents

| Agent | Use Case | Command |
|-------|----------|---------|
| **Codex** | 后端逻辑、复杂 bug、多文件重构 | `codex exec --dangerously-bypass-approvals-and-sandbox -C "/path" "prompt"` |
| **Claude Code** | 前端、git 操作、快速任务 | `claude --dangerously-skip-permissions -p "prompt"` |
| **Gemini** | UI 设计、生成规范 | `gemini -p "prompt"` 或 `gemini -y -p "prompt"` (YOLO 模式) |
| **Cursor** | 前端产品化、IDE 协同、界面 polish；版本前差异分析（plan） | `cursor agent -f -p --workspace "/path" --model composer-1.5 "prompt"` |

---

## Scripts

### spawn-agent.sh

创建新任务并启动代理。

**参数：**
- `--agent` (必需): codex | claude | gemini | cursor | auto（推荐）
- `--repo` (必需二选一): 仓库名（位于 skill 上级目录时使用）
- `--repo-path` (必需二选一，推荐): 仓库绝对/相对路径；用于 skill 根目录外的仓库
- `--branch` (必需): 分支名
- `--description` (必需): 任务描述
- `--prompt` (三选一): 代理提示词（短文本时可用）
- `--prompt-file` (三选一，推荐): 从文件读取提示词，避免 shell 转义问题（尤其包含反引号、`$()`、多行内容）
- `--prompt-b64` (三选一): Base64 提示词，适合脚本自动化调用
- `--agent-model` (可选): 指定模型（例如 `--agent cursor --agent-model composer-1.5`）
- `--cursor-mode` (可选): `dev|plan`（仅 cursor 生效，默认 `dev`）
  - `plan` 时会自动使用模型 `gpt-5.3-codex`
- `--phase` (可选): `build|review|fixup`（默认 `build`）；会受 `config/user.json.agentPolicy` 限制
- `--completion-mode` (可选): `pr`(默认) | `session`；本地测试仓库无 PR 时建议用 `session`
- `--auto-merge` (可选，`pr` 模式): 当 CI 与 review 满足条件后触发 `gh pr merge --auto`
- `--merge-method` (可选，`pr` 模式): `squash|merge|rebase`，默认 `squash`
- `--cleanup-after-seconds` (可选): 临时 worktree 清理 TTL；`session` 模式默认 `3600`

### check-agents.sh

监控所有运行中的代理。

**功能：**
- 检查 tmux 会话是否存活
- 检查 PR 是否已创建（`completionMode=pr`）
- 跟踪 PR 状态机（`waiting_checks` / `checks_failed` / `waiting_review` / `changes_requested` / `merge_ready` / `merge_queued` / `merged`）
- 检查 required CI checks（`gh pr checks --required`）
- 检查 reviewDecision（`gh pr view --json reviewDecision`）
- 可选自动触发 `gh pr merge --auto`（任务级 `autoMerge` 或 `config/user.json.pr.autoMerge`）
- 失败自动重试（按配置延迟，最多3次；依赖任务记录中的命令元数据）
- 写入通知到 `notifications.json` (由 OpenClaw 发送飞书通知)
- 结束后可自动触发 `cleanup-worktrees.sh` 与 `prune-history.sh`（避免 worktree / active-tasks 膨胀）

注意：
- `session exit mode` 仅表示会话结束，不代表质量达标。
- 质量达标必须由主 Agent 的 post-task review 判定。

### review-agent.sh

多 reviewer 代码审查（默认三审：`codex + gemini + claude`）。

**参数：**
- `--repo` (必需): 仓库名
- `--branch` (必需): 分支名或 PR 号
- `--reviewers`: 审查者 (默认: codex,gemini,claude；默认要求至少 3 个)
- `--allow-fewer-reviewers`: 调试用，允许少于 3 个 reviewer
- `--no-post`: 只生成本地审查产物，不回写 PR 评论

**行为（新版）：**
- 每个 reviewer 生成结构化审查结论（Verdict / Findings / Validation / Next Steps）
- 自动抓取 `gh pr diff` 并注入 reviewer prompt（截断版）
- 每个 reviewer 单独在 PR 下发表评论（正文带 `[dev-team][reviewer=...]` 标识）
- 会按 `config/user.json.agentPolicy` 过滤禁用/阶段不允许的 reviewer
- 生成聚合结果 `assets/logs/reviews/review-<pr>-<ts>.aggregate.json`
- 聚合策略会结合 reviewer 权重、severity 和 reviewer 角色偏好，输出：
  - `waiting_human_approve`
  - `review_changes_requested`
  - `review_human_attention`
- 写回 `assets/active-tasks.json`：
  - `checks.reviewAggregate`
  - `checks.reviewSummary`
  - `checks.fixupSuggested`
  - `checks.fixupTarget`（用于后续优先回原 subagent 返工）

### aggregate-reviews.sh

聚合多 reviewer 的审查产物，输出单一决策（通过 / 需修改 / 人工关注）。

示例：
```bash
./scripts/aggregate-reviews.sh --file assets/logs/reviews/review-1-1234567890.json
```

### request-fixup.sh

根据 `review-agent` 聚合结果，为原 PR 负责 subagent 生成返工 prompt，并优先发回原 subagent（如会话仍存活）。

**参数：**
- `--branch <branch>` 或 `--pr <number>`：定位任务
- `--dry-run`：只生成返工 prompt，不执行
- `--spawn-if-dead`：原 subagent 会话已退出时，按同 branch 重新派工（谨慎使用）

**行为：**
- 读取 `checks.reviewAggregate` / `checks.reviewAggregateFile`
- 若 `fixupSuggested=true`，生成结构化返工 prompt（按 severity 排序）
- 写回 `checks.fixupRequestedAt` / `checks.fixupRequestMode`
- 默认优先回原 subagent（同 branch owner）处理

---

## Agent Adaptation & Policy

- 统一 agent 适配与全流程使用建议：`references/agent-adapters.md`
- 可配置 agent 启用开关与阶段允许列表：`config/user.json` -> `agentPolicy`
- 推荐器支持阶段参数（会过滤禁用 agent）：

```bash
./scripts/recommend-agent.sh --description "前端看板优化" --phase build
./scripts/recommend-agent.sh --description "PR 代码审核" --phase review
```

### cleanup-worktrees.sh

清理已合并的 worktree。

补充说明：
- 对 `completionMode=session` 且 `cleanupMode=session_ttl` 的任务，会在 `cleanupEligibleAt` 到期后自动清理 worktree
- 清理后任务状态会写回为 `cleaned`（保留历史记录）

### prune-history.sh

归档 `assets/active-tasks.json` 中过旧的已完成任务（`done/failed/cancelled/cleaned/...`），避免注册表无限增长。

常用参数：
- `--keep-days <days>`: 仅归档早于 N 天的记录（当前默认配置为 `0`，更偏热数据）
- `--keep-count <n>`: 无论时间如何，至少保留最近 N 条非失败/取消终态记录（当前默认配置为 `12`）
- `--keep-fail-cancel-days <days>`: `failed/cancelled` 独立归档天数（默认可更激进）
- `--keep-fail-cancel-count <n>`: 至少保留最近 N 条 `failed/cancelled`
- `--dry-run`: 预览归档数量，不落盘

自动化建议：
- `cleanup-worktrees.sh` 执行后自动触发 `prune-history.sh`（可在 `config/user.json.archive` 配置）
- 也可单独配置每日归档 cron

说明：
- `cleanup-worktrees.sh` 会清理孤儿 worktree（任务已归档但同级目录仍残留）
- `session_ttl` 会受全局 TTL 上限约束，避免历史任务长时间占用磁盘

### setup-check.sh

首次使用检查脚本，验证配置完整性。

### recommend-agent.sh

根据任务描述/提示词关键词、当前运行负载、CLI 健康状态推荐最合适的 agent（含理由）。

示例：
```bash
./scripts/recommend-agent.sh \
  --description "dev-board 前端 UI 产品化改版，优化筛选与日志面板" \
  --prompt-file /tmp/task-prompt.txt \
  --format json
```

### list-agent-models.sh

列出 agent 模型（当前主要用于 Cursor）。

示例：
```bash
./scripts/list-agent-models.sh cursor
```

### enqueue-task.sh / list-queue.sh / claim-task.sh

Queue/Claim 模式（推荐演进路径，现已提供最小可用版本）：

- `enqueue-task.sh`：主 Agent 添加任务到队列（`assets/tasks.json`）
- `list-queue.sh`：查看队列（支持状态/阶段过滤）
- `claim-task.sh`：认领一个 queued 任务并调用 `spawn-agent.sh` 派工
- `sync-queue-status.sh`：根据 `assets/active-tasks.json` 回写队列任务状态（`running/done/cleaned/...`）
- `prune-queue-history.sh`：归档 `assets/tasks.json` 中过旧终态队列任务到 `assets/logs/archives/queue-history-YYYY-MM.jsonl`

示例：
```bash
./scripts/enqueue-task.sh \
  --repo-path ./scripts/dev-board \
  --branch feat/dev-board-action-history \
  --description "dev-board 操作历史列表" \
  --phase build \
  --completion-mode pr \
  --prompt-file /tmp/task.txt

./scripts/list-queue.sh --status queued
./scripts/claim-task.sh --agent auto
```

---

## Task Registry

位置：`assets/active-tasks.json`

编码约定：
- 所有任务与通知 JSON 文件统一使用 UTF-8 保存
- 写入时使用 `ensure_ascii=False`，中文会以可读形式保存（不再显示 `\\uXXXX`）

归档约定：
- `assets/active-tasks.json` 保存热数据（运行中 + 近期终态任务）
- 历史记录归档到 `assets/logs/archives/task-history-YYYY-MM.jsonl`

任务状态以脚本实现为准，详见 [references/state-machine.md](references/state-machine.md)。

补充字段（新任务会记录）：
- `requestedAgent`: 用户请求的 agent（可能是 `auto`）
- `agentModel`: 实际使用模型（如 `composer-1.5`）
- `agentSelectionReason`: 自动派工的简要理由（关键词/健康回退等）

---

## References

- **状态机**: [references/state-machine.md](references/state-machine.md)
- **CLI / tmux**: [references/cli-reference.md](references/cli-reference.md)
- **Prompt 模板**: [references/prompt-templates.md](references/prompt-templates.md)（推荐 Subagent Task Contract）
- **完成后验收清单**: [references/post-task-review-checklist.md](references/post-task-review-checklist.md)
- **初始化 / Cron**: [references/initialization.md](references/initialization.md)

---

## Troubleshooting

### 1) Claude 子任务启动失败（常见于复杂 prompt）

常见根因：
- 在 shell 中直接使用 `--prompt "..."`，内容包含反引号、`$()` 等，导致 shell 提前展开，实际传给脚本的 prompt 被污染。

修复方式（推荐顺序）：
1. 使用 `--prompt-file`（首选）
2. 自动化调用使用 `--prompt-b64`
3. 仅短 prompt 使用 `--prompt`

### 2) Cursor agent 无法使用 / 很少被选中

如果 `cursor agent status` 显示 `Not logged in`，`spawn-agent` 会在启动前直接失败并提示：
```bash
cursor agent login
```

你提到常用模型 `composer 1.5`，当前已在 `config/agents.json` 中设为 Cursor 默认模型（`composer-1.5`）。
如需覆盖：
```bash
./scripts/spawn-agent.sh --agent cursor --agent-model composer-1.5 ...
```

Cursor plan 模式（用于版本前差异分析）：
```bash
./scripts/spawn-agent.sh \
  --agent cursor \
  --cursor-mode plan \
  --repo-path /path/to/repo \
  --branch feat/version-plan \
  --description "版本规划与差异分析" \
  --completion-mode session \
  --prompt-file /tmp/plan.txt
```
说明：
- 该模式等价于 `cursor agent --mode plan`（只读规划，不改代码）
- `spawn-agent` 会强制模型为 `gpt-5.3-codex`

### 3) PR / CI / review 流程不推进

必要前置条件：
1. 仓库已配置 GitHub `origin` remote
2. `gh auth status` 有效（token 未过期）
3. subagent 的 prompt 明确要求：
   - 提交 commit
   - `git push -u origin <branch>`
   - `gh pr create ...`

如果缺一项，`check-agents.sh` 无法推进 PR 状态机。

### tmux
```bash
tmux new-session -d -s <name> -c <dir> "command"
tmux send-keys -t <session> "text" Enter
tmux list-sessions
tmux kill-session -t <session>
```
