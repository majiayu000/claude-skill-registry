---
name: let-me-know
description: Notify the user before starting any long-running task and keep them updated. Use when a task will take noticeable time (>2-3 minutes). Send a start message, schedule a 5‑minute heartbeat update, and send a completion message immediately when done.
---

# Let Me Know

## Purpose
Ensure the user is informed **before** long-running tasks start, gets periodic updates on a **configurable interval** (default 5 minutes), and receives an immediate completion/failure notice. Heartbeat messages must reflect **real-time progress**, not a repeated template.

## Trigger
Use this skill whenever a task will take noticeable time (>2–3 minutes) or involves long-running installs/builds/tests.

## Workflow (required)

1) **Pre-flight message** (before starting):
- Send a short message: what will run, estimated time, and explicitly state:
  - “完成或失败都会立刻通知你；期间我每 **X 分钟** 发一次进度心跳，您也可以修改心跳时间间隔。”

2) **Start a heartbeat (configurable interval, with pre-check)**
- **Default interval = 5 minutes** (`everyMs=300000`). If the user specifies a different interval, use it.
- Schedule repeating updates while the task runs.
- **Before each heartbeat message**, read the latest progress (state file/logs) and send **current** progress (no repeated template):
  - Running → include latest step, progress metrics, and next step.
  - Failed → send failure notice **and stop the heartbeat**.
- **优先推荐：同一条 agentTurn 内“原地心跳”**（不创建额外 cron）：
  - 在长任务执行期间，用循环 `sleep <interval>` → 读取进度 → `message send` 发一次动态进度。
  - 任务结束自然停止，不会遗留心跳任务。
- **只有在必须脱离当前执行流时才用 cron 心跳**，并且必须满足：
  - 通过 `cron add` 创建心跳 job 时，**payload.deliver=false**（避免“收到/启动”之类消息被转发给用户）。
  - 心跳 job 内部用 `message send` 主动推送进度。
  - 创建后把返回的 **heartbeatJobId** 写入状态文件（例如 `<task>-state.json`），供清理使用。
  - 创建前先 `cron list`，若已存在同名心跳 job，先 remove（去重）。
- Content template (dynamic):
  - Running: `进度：<最新步骤/阶段>（<关键指标>）。下一步：<next>。完成/失败会立刻通知你。`
  - Failed: `失败：<task> 发生错误（简述原因）。已停止心跳提醒。`

3) **Run the task**
- Execute the long-running command(s).

4) **Completion message** (immediately after finish)
- Send result summary (success/failure + key output).

5) **Stop heartbeat（必须做到）**
- 如果你使用了“原地心跳”（推荐）：任务结束即可，不会遗留任何 cron。
- 如果你使用了 cron 心跳：
  - 在任务**成功/失败的 finally** 里调用 `cron remove <heartbeatJobId>`。
  - 若 remove 失败（gateway timeout）：至少重试 2 次（指数退避 2s/8s）。
  - 仍失败：创建一个 2 分钟后的一次性 cleanup cron 再次 remove（避免永远刷屏）。

## Heartbeat interval (user-configurable)
- Default: **5 minutes**.
- If the user specifies an interval (e.g., “每 2 分钟/10 分钟”), use that value.
- If the user changes the interval mid-task, update the cron schedule and acknowledge in the next heartbeat.

## Message Delivery
Prefer outbound normal chat messages:
- Use `message send` with the correct target format.
- Example for Discord DM: `user:<id>`.

## Safety
- Do not start long tasks without the pre-flight message.
- If blocked/failed, notify immediately, set state=failed, and stop the heartbeat.
- If cron removal fails due to gateway timeout, retry removal; if still stuck, use gateway restart (requires `commands.restart: true`) and retry.

## Example (Discord DM)

**Start message:**
- `即将开始：安装依赖并运行测试（预计 5–10 分钟）。完成或失败都会立刻通知你；期间我每 5 分钟发一次进度心跳，你也可以修改心跳时间间隔。`

**Heartbeat (every 5 min, example):**
- `进度：已完成安装依赖（1/2），测试运行中（已用时 4 分钟）。下一步：汇总测试结果。完成/失败会立刻通知你。`

**Completion:**
- `完成：安装成功，测试通过。`
