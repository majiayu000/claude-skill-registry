---
name: coding-runner
description: Simple guideline for running coding CLIs (Codex/Claude/pi/OpenCode) **only via tmux skill**.
metadata:
  {
    "pi-gateway": {
      "emoji": "🧪",
      "notes": "No custom scripts. Reuse tmux skill: create session, then return start/inspect/stop commands."
    }
  }
---

# coding-runner (tmux-only, docs-only)

> 目标：不再实现单独脚本/入口，只用一份文档说明
> **如何复用现有 tmux 技能** 来运行代码类 CLI。
>
> 你只需要告诉 agent 要做什么；agent 内部用 tmux 起会话，
> 并按照下述规范返回：socket、session、启动/查看/停止命令。

---

## 1. 统一原则

1. **只用 tmux，不用 interactive_shell**
   - 所有需要“跑 CLI 写代码 / 起 dev server / 长任务”的场景，一律通过 tmux。
2. **不写新脚本，不实现新入口**
   - 这个技能只有这份 Markdown 文档，没有 `index.ts` 之类的实现文件。
   - Agent 在需要时，直接参考本说明，用现有 tmux skill / tmux 命令完成任务。
3. **始终返回 3 类命令（满足网关协议）**
   - `start`：已经执行过的启动命令（说明用）。
   - `inspect`：查看 / attach 会话的命令。
   - `stop`：停止会话的命令。

---

## 2. tmux 会话约定

### 2.1 Socket 路径

统一使用（示例约定，可按实际 tmux skill 调整）：

```bash
SOCKET="/tmp/pi-tmux-sockets/pi.sock"
```

### 2.2 Session 命名

- 使用简短、无空格的名字，例如：
  - `pi-task-<slug>`
  - `pi-dev-<project>`
- 例子：

```bash
SESSION="pi-task-auth-fix"
```

---

## 3. 典型用法模板

### 3.1 起一个代码任务（Codex / pi / Claude / OpenCode）

> 例：在 `/path/to/project` 里用 Codex 修 bug。

1. 构造要执行的命令（示例）：

```bash
CMD="cd /path/to/project && codex exec --full-auto 'Fix the auth bug in auth.ts'"
```

2. 启动 tmux 会话：

```bash
SOCKET="/tmp/pi-tmux-sockets/pi.sock"
SESSION="pi-task-auth-fix"

mkdir -p "$(dirname "$SOCKET")"
tmux -S "$SOCKET" new -d -s "$SESSION" "$CMD"
```

3. 返回给用户 / 网关的三条命令：

```bash
# 启动命令（已执行，仅供记录）
tmux -S /tmp/pi-tmux-sockets/pi.sock new -d -s pi-task-auth-fix "cd /path/to/project && codex exec --full-auto 'Fix the auth bug in auth.ts'"

# 查看 / 进入会话
tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t pi-task-auth-fix

# 停止会话
tmux -S /tmp/pi-tmux-sockets/pi.sock kill-session -t pi-task-auth-fix
```

Agent 在回答中应至少提供后两条命令（inspect/stop），并说明 socket 和 session 名称。

---

### 3.2 起一个 dev server 服务

> 例：在 `/path/to/project` 运行 `npm run dev`。

```bash
SOCKET="/tmp/pi-tmux-sockets/pi.sock"
SESSION="pi-dev-myproj"

CMD="cd /path/to/project && npm run dev"
mkdir -p "$(dirname "$SOCKET")"
tmux -S "$SOCKET" new -d -s "$SESSION" "$CMD"

# 返回给用户：
# 查看
#   tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t pi-dev-myproj
# 停止
#   tmux -S /tmp/pi-tmux-sockets/pi.sock kill-session -t pi-dev-myproj
```

---

## 4. 安全与约束

1. **禁止在敏感目录起会话命令**
   - 不要使用以下目录作为工作目录：
     - `~/.pi/agent`
     - `~/.pi/gateway`
   - 如果需要操作这些目录，应通过专门维护脚本，而不是 coding tmux 会话。

2. **尊重用户明确要求**
   - 用户如果特别指定 command / session 名 / socket，按用户来。
   - 用户如果只描述目标，agent 自己决定合理的命令与命名。

3. **非阻塞**
   - 起会话后立刻返回，不在对话中等待命令完成。
   - 所有后续操作（查看日志、停止）都通过用户执行 tmux 命令完成。

---

## 5. 行为总结（给 Agent 看）

- 当用户提出“需要跑一个代码类任务 / 起一个 dev server / 开一个长期 CLI”的需求时：
  1. 确定工作目录与要执行的 CLI 命令（Codex / Claude / pi / OpenCode 等）。
  2. 选择一个合适的 tmux session 名。
  3. 按本文件模板在 `/tmp/pi-tmux-sockets/pi.sock` 上创建 tmux 会话。
  4. 在回答中返回：socket 路径、session 名，以及 **attach / kill** 的命令。
- 不再创建新的技能脚本或入口文件，一切逻辑通过本说明 + tmux skill/命令完成。
