---
name: memorylane
description: Persistent memory and context compression for Claude Code. Use when setting up or operating MemoryLane in a project, recalling or storing memories, reviewing insights, curating low-quality memories, or checking cost/token savings and automatic context injection.
---

# MemoryLane

## Setup

Run `bash install.sh` from the repo root to initialize `.memorylane/` and make the CLI executable.

Ensure `.claude/settings.json` points at `.claude/hooks/*.py` so automatic context injection and learning run.

Verify the install with:
```bash
python3 src/cli.py status
```

## Core commands

Check status and savings:
```bash
python3 src/cli.py status
```

Recall memories:
```bash
python3 src/cli.py recall "<query>"
```

View insights and costs:
```bash
python3 src/cli.py insights
python3 src/cli.py costs
```

Learn from history:
```bash
python3 src/learner.py initial
```

## Memory management

List and curate memories:
```bash
python3 src/cli.py curate --list
python3 src/cli.py curate --apply '<JSON>'
```

Manage an individual memory:
```bash
python3 src/cli.py memory get <id>
python3 src/cli.py memory update <id> --content "New content"
python3 src/cli.py memory delete <id>
```

## Server

Start or stop the sidecar:
```bash
python3 src/server.py start
python3 src/server.py status
python3 src/server.py stop
```

## Notes

Do not edit `.memorylane/memories.json` directly; use the CLI.

Context rot guard: injected context is capped to a safe fraction of the model window via `context_rot.*` config keys.
