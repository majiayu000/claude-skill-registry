---
name: memory-keeper
description: Copy and snapshot all important agent context (MEMORY.md, memory/*.md, AGENTS.md, SOUL.md, etc.) into a dedicated archive directory or repo. Use this skill when you want to back up your memories, context, or configuration files in preparation for maintenance, corruption recovery, or transferring to another host.
---

# Memory Keeper

Memory Keeper is a simple CLI that copies the critical OpenClaw context files (daily memory logs, DESCRIPTION.md, personality documents, heartbeat reminders) into a safe archive destination and optionally commits/pushes them to a configured git repo. It keeps the same file layout so you can restore or inspect the history without grabbing the whole workspace.

## Features

- **Snapshots**: Copies `memory/*.md`, `MEMORY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, and optional extras into the archive path while preserving directory structure.
- **Git-friendly**: If the target archive is a git repo, Memory Keeper can initialize it, create commits, and push changes to your remote branch (configurable via CLI flags).
- **Portable**: Works on any platform; just point `--workspace` to a workspace root containing those files.

## Get started

```bash
python3 skills/memory-keeper/scripts/memory_sync.py --target ~/clawdy-memories --commit --message "Sync up" --remote https://github.com/your-org/clawdy-memories.git --push
```

See `references/usage.md` for configuration tips, automation recipes, and a troubleshooting guide.

## Resources

- **GitHub:** https://github.com/CrimsonDevil333333/memory-keeper
- **ClawHub:** https://www.clawhub.ai/skills/memory-keeper
