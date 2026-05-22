---
name: guard
description: >
  Protect Claude Code sessions from context overflow by running a background
  daemon that monitors session size and auto-prunes before compaction hits.
  Use when the user says "guard", "protect session", "context getting long",
  "prevent compaction", "session management", or is running agent teams that
  need continuous context protection.
disable-model-invocation: true
allowed-tools: Bash(cozempic *)
---

Start the cozempic guard daemon for continuous session protection.

## Default (recommended)

```bash
cozempic guard --daemon --threshold 50 -rx standard --interval 30
```

This runs in the background and:
1. Checkpoints team state every 30 seconds
2. At 60% of threshold (30MB): applies gentle prune, no reload
3. At threshold (50MB): applies full prescription + auto-reload with team state preserved

## For agent teams

Guard mode is **essential** for sessions running agent teams. Without it, auto-compaction triggers and the lead agent loses team state (TeamCreate, SendMessage, tasks are discarded).

## Options

- `--threshold N` — hard threshold in MB (default: 50)
- `--soft-threshold N` — soft threshold in MB (default: 60% of hard)
- `--threshold-tokens N` — hard threshold in tokens (fires whichever hits first)
- `--no-reload` — prune without restarting Claude
- `--no-reactive` — disable kqueue/polling file watcher
- `-rx NAME` — prescription at hard threshold (default: standard)

## Check status and stop

The daemon writes to `/tmp/cozempic_guard_*.log`. Check with:
```bash
ls /tmp/cozempic_guard_*.pid 2>/dev/null        # is it running?
tail -20 /tmp/cozempic_guard_*.log 2>/dev/null   # recent activity
kill "$(cat /tmp/cozempic_guard_*.pid)"           # stop it
```
