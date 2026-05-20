---
name: swarm-self-heal
version: 0.1.1
description: Swarm reliability watchdog for OpenClaw — validates gateway/channel and every lane, performs bounded recovery, and emits auditable receipts.
author: Anvil AI
license: MIT
homepage: https://github.com/cacheforge-ai/cacheforge-skills
user-invocable: true
tags:
  - openclaw
  - reliability
  - watchdog
  - self-heal
  - swarm
  - operations
  - incident-response
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"🩺","homepage":"https://github.com/cacheforge-ai/cacheforge-skills","requires":{"bins":["bash","jq","openclaw"]}}}
---

## When to use this skill

Use this skill when the user wants to:
- Diagnose why a multi-agent swarm feels "stuck" or partially offline
- Check gateway + channel + lane liveness in one run
- Perform bounded auto-recovery (restart + retry only)
- Capture auditable receipts for incident timelines
- Keep a primary watchdog lane plus a backup lane in place

## Commands

```bash
# Install/refresh watchdog scripts + cron wiring
bash skills/swarm-self-heal/scripts/setup.sh

# Run an immediate canary check
bash skills/swarm-self-heal/scripts/check.sh

# Run watchdog directly (uses deployed workspace path)
bash ~/.openclaw/workspace-studio/scripts/anvil_watchdog.sh

# Optional: increase lane ping timeout for slower providers
PING_TIMEOUT_SECONDS=180 bash ~/.openclaw/workspace-studio/scripts/anvil_watchdog.sh
```

## What it checks

- **Gateway health** via `openclaw health`
- **Channel readiness** via `openclaw channels status --json --probe`
- **Passive lane recency** via `openclaw status --json` (latest OpenClaw-compatible)
- **Active lane probe only when stale** for `main`, `builder-1`, `builder-2`, `reviewer`, `designer`
- **Bounded recovery** with a single restart pass + targeted re-probe of infra failures

## Output contract

The watchdog output includes:
- `timestamp`
- `targets`
- `ok_agents`
- `failed_agents`
- `actions`
- `VERDICT`
- `RECEIPT`

## Safety model

- Bounded recovery only (single restart pass per run)
- No destructive state wipes
- No blind reinstall behavior
- Recovery actions are explicit in output

## Notes

- Cron wiring sets both primary and backup watchdog lanes to `xhigh` thinking.
- Telegram target is auto-derived from config when available, with a safe fallback.
- Healthy runs can be summarized as a single line to reduce operator noise.
