---
name: email-notify
description: Send SMTP email notifications after Codex completes a task. Use when one Codex or Claude run is finished, or when you need to notify on task completion with device name, project name, status, and summary via email.
---

# Email Notify

## Overview

Send an email notification after each Codex task. Use the helper script to resolve the project name and send via SMTP.

## User Preparation

### 1) Configure environment variables

Add the following lines to `~/.bashrc` (Linux) or `~/.zshrc` (macOS):

```
export CODEX_MACHINE_NAME="Machine-name" # e.g., Macbook
export CODEX_EMAIL_SMTP_HOST="smtp.example.com"
export CODEX_EMAIL_SMTP_PORT="587"
export CODEX_EMAIL_USERNAME="user@example.com"
export CODEX_EMAIL_PASSWORD="..."
export CODEX_EMAIL_FROM="user@example.com"
export CODEX_EMAIL_TO="recipient1@example.com,recipient2@example.com"
export CODEX_EMAIL_USE_TLS="false" # true/false, default false
export CODEX_EMAIL_USE_SSL="true" # true/false, default true
```

If your SMTP server does not require auth, leave `CODEX_EMAIL_USERNAME` and `CODEX_EMAIL_PASSWORD` unset.
Set `CODEX_EMAIL_USE_SSL` to `true` for SMTPS (typically port 465) and `CODEX_EMAIL_USE_TLS` to `true` for STARTTLS.
Do not set both `CODEX_EMAIL_USE_TLS` and `CODEX_EMAIL_USE_SSL` to `true`.

### 2) Add instruction in project AGENTS.md

For example, add this instruction to AGENTS.md:
> Use skill email-notify to notify users when each agent run is finished or when any notifications would be sent to users.

## Workflow

### 1) Provide a project name source (optional)

- To override the folder name, define a project name in `AGENTS.md` using one of:
  - YAML frontmatter: `project_name: My Project` (or `name:`)
  - A plain line: `Project Name: My Project`
- If no name is found, the script uses the project folder name.

### 2) Send the notification at task completion

- Generate a short task title (3-8 words).
- Pick an execution status: `success`, `failed`, `partial`, `blocked`, etc.
- Write a brief result summary; avoid secrets.

Run:

```bash
python3 ~/.codex/skills/email-notify/scripts/send_email_notification.py \
  --task-title "..." \
  --status "success" \
  --summary "..." \
  --project-name "..."
```

## Resources

- `scripts/send_email_notification.py`: Send the email notification and resolve the project name.
