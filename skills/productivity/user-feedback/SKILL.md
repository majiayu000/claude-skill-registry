---
name: user-feedback
description: Use when asked to check, read, triage, or act on user feedback
---

# User Feedback Protocol

Use this skill to keep USER_FEEDBACK.md in sync with actionable tasks. Monitor and process USER_FEEDBACK.md in the workspace root: check if new feedback exists, turn actionable feedback into tasks using the repo's preferred task system, and update the read timestamp after processing.

## File format

- Line 1: last-read timestamp in local time, format `YYYY-MM-DDTHH:MM:SS`.
- Line 2: human note: Do not delete the timestamp above; it records the last time this file was read by an agent.
- Lines 3+: free-form user feedback.

## Commands

Use the bundled script:

```
python3 ~/.codex/skills/user-feedback/scripts/user_feedback.py check_user_feedback
python3 ~/.codex/skills/user-feedback/scripts/user_feedback.py init_user_feedback
python3 ~/.codex/skills/user-feedback/scripts/user_feedback.py update_user_feedback
```

### Check

1) Run `check_user_feedback` from the workspace root (defaults to `./USER_FEEDBACK.md`).
2) If it exits with code 2 and stderr contains `File not found`, run `init_user_feedback`.
3) If it returns `false` (exit code 1), ignore the file and stop.
4) If it returns `true` (exit code 0), open the file and process feedback.

### Process feedback

- Read lines 3+ for actionable items (fixes, requests, bugs, improvements, questions).
- Create one task per actionable item using the repo's preferred task system.
  - If a `.tasks/` directory exists, use the `sv` task workflow.
  - If a `.tickets/` directory exists, use the `tk` ticket workflow.
  - If neither exists, look for repo instructions (AGENTS.md) or ask the user.
- Keep each task concise and specific; include any needed context from the feedback.
- Check existing tasks for overlap and duplicates, especially if they are still open.

### Update

After all actionable feedback is represented in tasks, run `update_user_feedback` to update the timestamp and mark the file as read.

## Script details

The script lives at `scripts/user_feedback.py` inside this skill and implements:
- `check_user_feedback` (compares file mtime vs first-line timestamp with a 1s threshold)
- `init_user_feedback` (creates the file with timestamp + note)
- `update_user_feedback` (replaces first line with current timestamp)

Use `--path` to override the default file path and `--force` to overwrite on init.
