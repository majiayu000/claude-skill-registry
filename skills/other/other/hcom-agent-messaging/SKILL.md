---
name: hcom-agent-messaging
description: |
  Let AI agents message, watch, and spawn each other across terminals. Claude Code, Gemini CLI, Codex, OpenCode. Use this skill when the human user needs help, status, or reference about hcom - when user asks questions like "how to setup hcom", "hcom not working", "explain hcom", or any hcom troubleshooting.

---

# hcom — Let AI agents message, watch, and spawn each other across terminals. Claude Code, Gemini CLI, Codex, OpenCode.

AI agents running in separate terminals are isolated from each other. Context doesn't transfer, decisions get repeated, file edits collide. hcom connects them.

```
pip install hcom
hcom claude
hcom gemini
hcom codex
hcom opencode
hcom                            # TUI dashboard
```

---

## What humans can do

Tell any agent:

> send a message to claude

> when codex goes idle send it the next task

> watch gemini's file edits, review each and send feedback if any bugs

> fork yourself to investigate the bug and report back

> find which agent worked on terminal_id code, resume them and ask why it sucks

---

## What agents can do 

- Message each other (@mentions, intents, threads, broadcast)
- Read each other's transcripts (ranges, detail levels)
- View agent terminal screens, inject text/enter for approvals
- Query event history (file edits, commands, status, lifecycle)
- Subscribe and react to each other's activity in real-time
- Spawn, fork, resume, kill agents in new terminal panes
- Build context bundles (files, transcript, events) for handoffs
- Collision detection — 2 agents edit same file within 20s, both notified
- Cross-device — connect agents across machines via MQTT relay

---

## Setup

If the user invokes this skill without arguments:

1. Run `hcom status` — if "command not found", run `pip install hcom` first
2. Tell user to run `hcom claude` or `hcom gemini` or `hcom codex` or `hcom opencode` in a new terminal (auto installs hooks on first run)

| Status Output | Meaning | Action |
|--------|---------|--------|
| command not found | hcom not installed | `pip install hcom` |
| `[~] claude` | Tool exists, hooks not installed | `hcom hooks add` then restart tool (or just `hcom claude`) |
| `[✓] claude` | Hooks installed | Ready — use `hcom claude` or `hcom start` |
| `[✗] claude` | Tool not found | Install the AI tool first |

After adding hooks or installing hcom you must restart the current AI tool for hcom to activate.

---

## Tool Support

| Tool | Message Delivery |
|------|------------------|
| Claude Code (incl. subagents) | automatic |
| Gemini CLI | automatic |
| Codex | automatic |
| OpenCode | automatic |
| Any AI tool | manual - via `hcom start` |


---

## Troubleshooting

### "hcom not working"

```bash
hcom status          # Check installation
hcom hooks status    # Check hooks specifically
hcom daemon status
hcom relay status
```

**Hooks missing?** `hcom hooks add` then restart tool.

**Still broken?**
```bash
hcom reset all && hcom hooks add
# Close all claude/codex/gemini/opencode/hcom windows
hcom claude          # Fresh start
```

### "messages not arriving"

1. **Check recipient:** `hcom list` — are they `listening` or `active`?
2. **Check message sent:** `hcom events --sql "type='message'" --last 5`
3. **Recipient shows `[claude*]`?** Restart the AI tool

### Sandbox / Permission Issues

```bash
export HCOM_DIR="$PWD/.hcom"     # Project-local mode
hcom hooks add                   # Installs to project dir
```

---

## Files

| What | Location |
|------|----------|
| Database | `~/.hcom/hcom.db` |
| Config | `~/.hcom/config.toml` |
| Logs | `~/.hcom/.tmp/logs/hcom.log` |

With `HCOM_DIR` set, uses that path instead of `~/.hcom`.

---

## More Info

```bash
hcom --help              # All commands
hcom <command> --help    # Command details
hcom run docs            # Full CLI + config + API reference
```

GitHub: https://github.com/aannoo/hcom
