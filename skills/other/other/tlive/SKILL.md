---
name: tlive
description: |
  IM bridge for AI coding tools — chat with Claude Code / Codex from
  Telegram, Discord, or Feishu. Approve permissions, get streaming responses,
  manage sessions from your phone.
  Use for: starting IM bridge, configuring IM platforms, checking status,
  diagnosing issues.
  Trigger phrases: "tlive", "IM bridge", "消息桥接", "手机交互", "启动桥接",
  "连接飞书", "连接Telegram", "诊断", "查看日志", "配置".
  Do NOT use for: building bots, webhook integrations, or general coding tasks.
argument-hint: "setup | stop | status | logs [N] | reconfigure | doctor"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Grep
  - Glob
---

# TLive — IM Bridge Skill

You are managing the TLive IM Bridge — bidirectional chat with AI coding tools from Telegram, Discord, or Feishu.

The Bridge uses the Claude Agent SDK (or Codex SDK) to interact with the AI coding tool. It is completely independent from the optional Go Core web terminal server.

User data: `~/.tlive/`

## Command Parsing

| User says (examples) | Subcommand |
|---|---|
| (no args), `start`, `启动`, `启动桥接` | start |
| `setup`, `configure`, `配置`, `帮我连接 Telegram` | setup |
| `stop`, `停止`, `关闭` | stop |
| `status`, `状态`, `运行状态` | status |
| `logs`, `logs 200`, `查看日志` | logs |
| `reconfigure`, `修改配置`, `换个 bot`, `改 token` | reconfigure |
| `doctor`, `diagnose`, `诊断`, `挂了`, `没反应了` | doctor |
| `help`, `帮助`, `怎么用` | help |

**Disambiguation: `status` vs `doctor`** — Use `status` when the user just wants to check if the bridge is running. Use `doctor` when the user reports a problem or suspects something is broken. When in doubt and the user describes a symptom (e.g., "没反应了", "挂了"), prefer `doctor`.

## Runtime Detection

- `AskUserQuestion` available → Claude Code → interactive wizard
- Not available → Codex / other → show config example, non-interactive

## Config Check (all commands except `setup`)

Before any command except `setup`, check `~/.tlive/config.env`:
- **Missing** → Claude Code: auto-start `setup` wizard. Codex: show `~/.tlive/docs/config.env.example` and stop.
- **Exists** → proceed

## Subcommands

### `/tlive` (no args) or `start` — Start Bridge

```
1. Check config.env → if missing, auto-start setup
2. Check Bridge PID → if running, show status instead
3. Start Bridge: tlive start (uses TL_RUNTIME from config, default: claude)
4. Wait 2s, verify alive: tlive status
5. Report runtime, channels + web terminal status
```

### `setup`

Interactive wizard. Collect **one field at a time**, confirm each (mask secrets to last 4 chars).

Before asking for platform credentials, read `~/.tlive/docs/setup-guides.md` internally. Only mention the specific next step the user needs — don't dump the full guide. Show the relevant guide section only if the user asks for help.

**Step 1 — Choose IM platforms:**
```
AskUserQuestion: "Which IM platforms to enable?
1. Telegram — streaming preview, inline permission buttons
2. Discord — team use, channel-level access control
3. Feishu (飞书) — streaming cards, tool progress
Enter numbers (e.g., 1,3):"
```

**Step 2 — Collect credentials per platform:**

- **Telegram**: Bot Token → confirm (masked) → Chat ID (optional) → Allowed User IDs (optional). **Important:** At least one of Chat ID or Allowed User IDs should be set.
- **Discord**: Bot Token → confirm (masked) → Allowed User IDs → Allowed Channel IDs (optional). **Important:** At least one of Allowed User IDs or Allowed Channel IDs should be set.
- **Feishu**: App ID → confirm → App Secret → confirm (masked) → Allowed User IDs (optional).

**Step 3 — General settings:**
- Runtime: claude (default) or codex
- Port (default 8080)
- Public URL (optional, for web links in IM messages)
- Auto-generate TL_TOKEN (32-char hex)

**Step 4 — Write config and validate:**
1. Read `~/.tlive/docs/config.env.example` as the template — use its exact variable names (e.g., `TL_TG_*` for Telegram, `TL_DC_*` for Discord, `TL_FS_*` for Feishu). Do NOT invent variable names.
2. Show a summary table (secrets masked to last 4 chars)
3. Ask user to confirm before writing
4. `mkdir -p ~/.tlive/{data,logs,runtime}`
5. Write `~/.tlive/config.env` using the template's variable names, then `chmod 600`
6. Validate tokens — read `~/.tlive/docs/token-validation.md` for exact commands per platform
7. Report results. If validation fails, explain what's wrong.
8. On success: "Setup complete! I'll start the Bridge now." Then auto-start.

### `reconfigure`

1. Read current config from `~/.tlive/config.env`
2. Show current settings in a table (secrets masked to last 4 chars only)
3. Ask what the user wants to change
4. Collect new values one at a time, show where to find each value (show full guide from `~/.tlive/docs/setup-guides.md` only if asked)
5. Update config file
6. Re-validate any changed tokens
7. Remind: "Run `/tlive stop` then `/tlive start` to apply changes."

### `stop`

```
tlive stop
```

### `status`

```
tlive status
```

### `logs`

Extract optional line count N from arguments (default 50).
```
tlive logs [N]
```

### `doctor`

Run diagnostics and suggest fixes. For complex issues, read `~/.tlive/docs/troubleshooting.md`.

```
tlive doctor
```

Then validate IM tokens if configured — read `~/.tlive/docs/token-validation.md` for commands.

### `help`

Show a clear overview of the TLive system and available commands:

```
TLive — Three features, use any combination:

In Claude Code (/tlive):
  /tlive               Start IM Bridge (chat from phone)
  /tlive setup         Configure IM platforms (AI-guided)
  /tlive reconfigure   Modify specific config fields
  /tlive stop          Stop Bridge
  /tlive status        Show Bridge + Web Terminal + Hooks status
  /tlive logs [N]      Show last N log lines
  /tlive doctor        Diagnose issues + suggest fixes

In terminal (tlive):
  tlive <cmd>          Wrap command with web terminal (e.g. tlive claude)
  tlive setup          Configure IM platforms (interactive)
  tlive install skills Install /tlive skill + hooks to Claude Code
  tlive hooks pause    Auto-allow permissions, no IM notifications
  tlive hooks resume   Resume IM approval flow

In IM (from phone):
  /new                       Start new conversation
  /model <name>              Switch model (e.g. claude-sonnet-4-6)
  /runtime claude|codex      Switch AI provider
  /settings user|full|isolated  Claude settings scope
  /perm on|off               Permission prompts on/off
  /effort low|medium|high|max  Thinking depth
  /stop                      Interrupt execution
  /verbose 0|1               Detail level (quiet/terminal card)
  /sessions                  List recent sessions
  /session <n>               Switch to session
  /hooks pause|resume        Toggle hook approval
  /status                    Check status
  /help                      Show commands
```

## Notes

- Always mask secrets in output (show only last 4 characters)
- Always check for config.env before starting — without it the daemon crashes and leaves a stale PID file
- Bridge and Go Core web terminal are independent — Bridge works without Go Core
- Go Core is started separately via `tlive <cmd>` in a terminal, not by this skill
- Config at `~/.tlive/config.env` — shared by both Bridge and Go Core
- The daemon runs as a background Node.js process
