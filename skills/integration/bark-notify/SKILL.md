---
name: bark-notify
description: Send Bark (day.app) push notifications after Codex completes a task. Use when one Codex or Claude run is finished, or when you need to notify on task completion with device name, project name, status, and summary.
---

# Bark Notify

## Overview

Send a Bark push notification after each Codex task. Use the helper script to resolve the project name and post to the Bark API.

## User Preparation

### 1) Configure environment variables

You can add the following lines to `~/.bashrc` (Linux) or `~/.zshrc` (macOS) to set environment variables:
```
export CODEX_MACHINE_NAME="Machine-name" # e.g., Macbook
export CODEX_BARK_KEY="" # https://api.day.app/<CODEX_BARK_KEY>/
export CODEX_BARK_BASE_URL="https://api.day.app"
```

### 2) Add instruction in project AGENTS.md

For example, you can add this instruction to AGENTS.md:
> Use skill bark-notify to notify users when each agent run is finished or when any notifications would be sent to users.

## Workflow

### 1) Provide a project name source (optional)

- To override the folder name, define a project name in `AGENTS.md` using one of:
  - YAML frontmatter: `project_name: My Project` (or `name:`)
  - A plain line: `Project Name: My Project` or `项目名称：我的项目`
- If no name is found, the script uses the project folder name.

### 2) Send the notification at task completion

- Generate a short task title (3-8 words).
- Pick an execution status: `success`, `failed`, `partial`, `blocked`, etc.
- Write a brief result summary; avoid secrets.

Run:

```bash
python3 ~/.codex/skills/bark-notify/scripts/send_bark_notification.py \
  --task-title \"...\" \
  --status \"success\" \
  --summary \"...\" \
  --project-name \"...\"
```

## Resources

- `scripts/send_bark_notification.py`: Send the Bark notification and resolve the project name.
