---
name: hcom
description: |
  multi-agent communication and coordination for Claude Code, Gemini CLI & Codex. Use this skill when the human user needs help, status, or reference about hcom - when user asks questions like "how to setup hcom", "hcom not working", "explain hcom", or any hcom troubleshooting.

---

# hcom — realtime messaging + context sharing for AI coding agents

## What is hcom?

Local message bus + event log. Agents message each other, share transcripts, get notified on events, and spawn new agents. Messages arive when agents are active and idle.

```
pip install hcom
hcom claude                     #launch
hcom codex
hcom gemini
hcom                            # TUI dashboard
```

---

## Features

**Messaging** - send to all or @mention specific agents
`hcom send --help`

**Transcripts** - read other agent's conversation history
`hcom transcript --help`

**Subscriptions** - get notified when events match (real-time file collisions, agent idle, shell commands)
`hcom events --help`

**Spawn** - launch agents into new terminals
`hcom 3 claude` | `HCOM_TAG=team hcom 2 gemini` (group) | `hcom claude -p "task"` (headless)

**Workflow Scripts** - pre-built workflows (background reviewer, debate, clone, ensemble)
`hcom run --help`

**Cross-device** - connect agents across machines via HuggingFace relay
`hcom relay --help`

**Config** - terminal, tags, hints, timeouts
`hcom config` | `hcom config terminal --info` (set any terminal)


---

## Quick Setup

**Check current state:**
```bash
hcom status
```

| Output | Meaning | Action |
|--------|---------|--------|
| `[~] claude` | Tool exists, hooks not installed | `hcom hooks add` then restart tool |
| `[✓] claude` | Hooks installed | Ready - use `hcom claude` or `hcom start` |
| `[✗] claude` | Tool not found | Install the AI tool first |

**After `hcom hooks add`:** You MUST restart your AI tool for hooks to activate.

**Verify participation:**
```bash
hcom list
```

| Tool Display | Meaning |
|--------------|---------|
| `[CLAUDE]` | Full features (launched via `hcom claude`) |
| `[claude]` | Hooks-only mode (vanilla `hcom start`) |
| `[claude*]` | Ad-hoc mode - **restart AI tool for full features** |

Same pattern for `[GEMINI]`/`[gemini]`/`[gemini*]` and `[CODEX]`/`[codex]`/`[codex*]`.

The asterisk `*` means hooks aren't active for this session. Close and reopen the AI tool.

---


## Starting hcom

**Option A - Launch with hcom (recommended):**
```bash
hcom claude       # or: hcom gemini, hcom codex
```

**Option B - Connect existing session:**
> Run `hcom start`

## Using hcom

**Send messages:** Talk to agents naturally - "send a message to gemini saying check the tests"

**TUI dashboard:** `hcom` (no args) - event stream, broadcast, status, launch

---

## Troubleshooting

### "hcom not working"

```bash
hcom status          # Check installation
hcom hooks status    # Check hooks specifically
```

**Hooks missing?** `hcom hooks add` then restart tool.

**Still broken?**
```bash
hcom reset all && hcom hooks add
# Close all claude/codex/gemini/hcom windows
hcom claude          # Fresh start
```

### "messages not arriving"

1. **Check recipient:** `hcom list` - are they `listening` or `active`?
2. **Check message sent:** `hcom events --sql "type='message'" --last 5`
3. **Check TUI** - shows delivery blockers:
   - Agent processing (not listening)
   - User typing (delivery pauses)
   - Uncommitted text in prompt
   - Tool in submenu/not at prompt
4. **Recipient shows `[claude*]`?** They need to restart their AI tool

### "identity not found"

Run `hcom start` first, or use `hcom claude` to launch with automatic identity.

### Sandbox / Permission Issues

```bash
export HCOM_DIR="$PWD/.hcom"     # Project-local mode
hcom hooks add                   # Installs to project dir
```

### Fresh Start

```bash
hcom reset all # arhive db, reset config, remove hooks, stop all agents
pip uninstall hcom && pip install hcom
# Restart AI tool
```

---

## Tool Support

| Tool | Message Delivery | Notes |
|------|------------------|-------|
| Claude Code | idle + mid-turn | Full hooks, subagents work |
| Gemini CLI (v0.24.0+) | idle + mid-turn | Full hooks |
| Codex | idle + `hcom listen` | 1 hook |
| Any AI tool | manual | Ad-hoc mode via `hcom start` |


---

## Files

| What | Location |
|------|----------|
| Database | `~/.hcom/hcom.db` |
| Config | `~/.hcom/config.env` |
| Logs | `~/.hcom/.tmp/logs/hcom.log` |

With `HCOM_DIR` set, uses that path instead of `~/.hcom`.

---

## Archives & Reset

`hcom reset` archives the database and starts fresh. Similar to `/clear` in AI tools.
- Interactive agents get "stopped" but terminal stays open - can reclaim with `hcom start --as NAME`
- Headless agents get killed

Query archives:
```bash
hcom archive            # List (lowest = most recent)
hcom archive 1          # Query most recent
```

### Remove hcom

```bash
hcom hooks remove # Safely remove only hcom hooks/config from all tool settings files
```


---

## More Info

```bash
hcom --help              # All commands
hcom <command> --help    # Command details
hcom run docs            # Full CLI + config + API reference
```

GitHub: https://github.com/aannoo/hcom