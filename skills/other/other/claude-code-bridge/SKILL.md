---
name: claude-code-bridge
description: >
  Bridges OpenClaw (QQ, Telegram, WeChat, and other messaging channels) to a
  persistent Claude Code CLI session running in a background tmux process.
  Enables starting, stopping, restarting, and monitoring Claude Code sessions
  directly from any chat interface. Supports specifying a working directory or
  launching in sandbox mode (temp directory, auto-cleanup on stop). Automatically
  detects session state on every message, routes user input to the active Claude
  Code session, and handles tool-approval prompts so the user can approve or deny
  Claude Code actions without leaving their chat app.
  Trigger phrases: "start claude code", "open claude code", "cc status",
  "stop claude code", "restart cc", "启动claude code", "开启claude code",
  "启动cc", "开启cc", "连接cc", "cc状态", "关闭cc", "退出cc", "重启cc",
  "在...打开cc", "沙盒打开cc", "沙盒模式启动cc",
  "/cc start", "/cc stop", "/cc restart", "/cc status".
version: 0.3.0
---

# Claude Code Bridge

Bridge every incoming message to a live, persistent `claude` CLI process running
in a background tmux session. The user interacts via QQ/Telegram/any channel;
Claude Code responds as if they were typing in a real terminal.

## Session State Detection (CRITICAL — CHECK EVERY TURN)

**At the start of EVERY incoming message**, determine session state:

```bash
~/.openclaw/workspace/skills/claude-code-bridge/scripts/claude-code-bridge.sh "<SESSION_ID>" status
```

- `✅ Claude Code 会话运行中` → **CC mode active**, route message to CC
- `⭕ 没有活跃` → **CC mode off**, respond normally
- `⚠️  CC 正在等待审批` → tell user and await their approval choice

Construct `<SESSION_ID>` as `<channel>_<chat_id>` using only `[a-zA-Z0-9_]`.

## Routing Logic

```
Every incoming message:
  1. Run status check
  2. Is it a CC control command?
       ──── Startup (with workdir) ────
       "在 <path> 打开cc"        → start <path>
       "沙盒打开cc" / "沙盒模式" → start --sandbox
       "启动cc"（no path）       → ASK workdir first (see Startup Flow below)
       ──── Other controls ────
       "关闭cc"    → stop
       "重启cc"    → restart
       "cc状态"    → status
       "cc在哪" / "cc目录" → workdir
       "/cc peek"  → peek
       "/cc history [N]" → history
  3. Is CC in approval-waiting state?
       YES → parse user's intent (y/n/1/2/3) → approve
  4. Is CC session active?
       YES → forward as send
       NO  → respond normally as OpenClaw agent
```

## Startup Flow — Working Directory

When the user wants to start Claude Code **without specifying a directory**:

1. Ask briefly: `"工作目录放哪？发路径就在那里打开，不指定就用临时沙盒。"`
2. Parse the reply:
   - User sends a path (e.g. `~/projects/paper`) → `start ~/projects/paper`
   - User says "沙盒" / "随便" / "临时" / doesn't specify → `start --sandbox`

When the user specifies a directory **in the startup command itself**:
- "在 ~/Documents/Code 打开cc" → extract the path → `start ~/Documents/Code`
- "沙盒打开cc" / "沙盒模式启动cc" → `start --sandbox`

**Do NOT ask if the path is already provided in the command.**

## Executing Actions

```bash
SCRIPT="$HOME/.openclaw/workspace/skills/claude-code-bridge/scripts/claude-code-bridge.sh"

"$SCRIPT" "<ID>" start '/path/to/workdir'   # 在指定目录启动
"$SCRIPT" "<ID>" start --sandbox             # 沙盒模式启动
"$SCRIPT" "<ID>" send '<message>'            # 发送（90s 超时）
"$SCRIPT" "<ID>" send '<message>' --long     # 长任务（5min 超时）
"$SCRIPT" "<ID>" approve 1                   # 审批：选 Yes
"$SCRIPT" "<ID>" approve 2                   # 审批：选 Allow always
"$SCRIPT" "<ID>" approve 3                   # 审批：选 No
"$SCRIPT" "<ID>" approve esc                 # 审批：取消
"$SCRIPT" "<ID>" stop                        # 停止（沙盒自动清理）
"$SCRIPT" "<ID>" restart                     # 重启（保留原工作目录）
"$SCRIPT" "<ID>" restart '/new/path'         # 重启到新目录
"$SCRIPT" "<ID>" status                      # 状态（含工作目录信息）
"$SCRIPT" "<ID>" workdir                     # 查询当前工作目录
"$SCRIPT" "<ID>" peek                        # 原始终端画面
"$SCRIPT" "<ID>" history 200                 # 最近 200 行历史
```

**IMPORTANT — message quoting**: Use `tmux send-keys -l` (literal mode) so
special characters (`$`, `!`, `\`) are sent verbatim. The script handles this
internally; just pass the raw message as argument 3.

## CC Slash Commands — Direct Passthrough

CC's own slash commands work by sending them via `send`:

| User says | Forward as |
|-----------|-----------|
| `/plan` | `send '/plan'` |
| `/model sonnet` | `send '/model sonnet'` |
| `/compact` | `send '/compact'` |
| `/cost` | `send '/cost'` |
| `/help` | `send '/help'` |
| `/clear` | `send '/clear'` |
| `/diff` | `send '/diff'` |
| `/fast` | `send '/fast'` |
| `/vim` | `send '/vim'` |
| `/context` | `send '/context'` |
| `/export` | `send '/export'` |
| `/copy` | `send '/copy'` |
| `/rewind` | `send '/rewind'` |
| `/fork` | `send '/fork'` |
| `/permissions` | `send '/permissions'` |
| `/tasks` | `send '/tasks'` |
| `/status` | `send '/status'` |
| `/stats` | `send '/stats'` |
| `/review` | `send '/review'` |
| `/theme` | `send '/theme'` |
| `/sandbox` | `send '/sandbox'` |
| Any `/xxx` command | `send '/xxx'` |

These are NOT OpenClaw commands — forward them verbatim to CC.
All CC slash commands work via passthrough, including ones not listed above.

## Handling CC Approval Prompts

When CC encounters a tool it needs permission to run, it shows a TUI selection
menu (arrow-key navigation, not text input). The `approve` action handles this:

```
CC shows:
  Do you want to proceed?
  ❯ 1. Yes
    2. Yes, allow from this project
    3. No
```

The user's reply should be interpreted:
- "y" / "是" / "好" / "1" / "同意" → `approve 1`
- "2" / "允许" / "一直允许" → `approve 2`
- "n" / "否" / "不" / "3" / "拒绝" → `approve 3`
- "取消" / "cancel" → `approve esc`

## Long Tasks & Streaming

For tasks that take a long time (refactoring, writing large codebases):

1. Detect intent: if the user's message implies a large task (e.g. "重构整个项目",
   "帮我写一个完整的 XXX"), use `--long` flag (5-minute timeout)
2. If the output is empty after timeout, use `peek` to check CC's current state
3. If CC is still working, inform the user: `CC 仍在处理中，稍后再查`
4. Then use `peek` or `history` to get progress updates

## Formatting — Seamless Mode

**Goal: make the user feel like they're talking to Claude Code directly.**

When CC session is active:
- **Do NOT prefix every reply with `🤖 CC →`** — just relay CC's output directly
- Only add brief status markers for:
  · Session startup / shutdown
  · Approval prompts (show the options)
  · Errors / timeouts
- CC's code blocks, file paths, tool output → relay as-is, no reformatting
- Empty output → brief `CC 处理中...` then try `peek` after 3s
- Output >3000 chars → show last 2000 chars, note `/cc history` for full output
- Approval prompt → show options directly, minimal decoration

## Error Handling

| Situation | Action |
|-----------|--------|
| `send` returns empty | Wait 3s, run `peek`, relay result |
| Session not found | Inform user, offer to `start` |
| Session crashed | Detect via `status`, offer `restart` |
| CC shows error | Relay error verbatim |
| Timeout on long task | Inform user, suggest `peek` or `history` |

## Additional Resources

- **`scripts/claude-code-bridge.sh`** — Full session management (start/send/approve/stop/restart/status/workdir/peek/history)
- **`references/usage.md`** — User-facing help text and example conversations
