---
name: jira:sync
description: Sync local changes with Jira issue. Use when the user wants to "sync to jira", "update jira", "push progress", or "sync status".
version: 4.0.0
---

# Jira Sync

Synchronize local development progress with the Jira issue.

## Usage

```
/jira:sync [issue-key]
```

## Features

- Updates issue status
- Adds progress comments
- Logs work time
- Syncs commits
- Updates labels

## Related Commands

- `/jira:status` - Check current status
- `/jira:commit` - Create smart commit
