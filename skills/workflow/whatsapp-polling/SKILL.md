---
name: whatsapp-polling
description: Manage the WhatsApp Web group polling workflow (cron-driven) for Lucas’s groups. Use when enabling/disabling the polling behavior, adjusting backoff/state in wa-poll-state.json, or running a manual poll via browser-use to check groups for mentions of Lucas/Cleber.
---

# WhatsApp Polling

## Overview
Control the WhatsApp group polling behavior: enable/disable the cron job, run a manual poll, and update the backoff state file.

## Workflow

### 1) Check whether polling should run
- Read `/home/zanoni/clawd/scripts/wa-poll-state.json`.
- If `now - lastPollTime` < `currentIntervalMin`, **do nothing**.

### 2) Run a poll (when due)
- Spawn a sub-agent to:
  - Open WhatsApp Web in Brave **light mode** and use **browser-use**.
  - Check both groups: **“aplicações bethais”** and **“Rinha de IA”**.
  - Only respond to messages directed at **Lucas/Cleber**.
  - In **Rinha de IA**: be playful/competitive (AI vs AI vibe).
  - In **aplicações bethais**: be casual/friendly in Portuguese.

### 3) Update state file
- If activity found: `consecutiveEmpty = 0`, `currentIntervalMin = 2`.
- If no activity: `consecutiveEmpty += 1`, `currentIntervalMin = backoffSchedule[min(consecutiveEmpty, len-1)]`.
- Always update `lastPollTime`.

### 4) Enable/disable the cron
- Cron job name: **whatsapp-group-monitor**.
- Use `cron list` / `cron update` to toggle `enabled`.
- Keep WhatsApp polling **off** unless Lucas explicitly asks.

## References
- State schema and fields: `references/wa-poll-state.md`
