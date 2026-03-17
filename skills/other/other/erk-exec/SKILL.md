---
name: erk-exec
description: >
  Guide for erk exec subcommands. Use when running erk exec commands
  to understand syntax, find the right command for a task, or learn
  common workflows. Always check syntax with -h or load this skill
  before running erk exec commands.
---

# erk exec Guide

## Quick Start

Before running any `erk exec` command, check syntax with `-h`:

```bash
erk exec <command> -h
```

## Commands by Workflow

### PR Review Operations

When addressing PR review comments or resolving threads:

| Command                       | Purpose                              |
| ----------------------------- | ------------------------------------ |
| `get-pr-review-comments`      | Fetch review comments (use `--pr N`) |
| `resolve-review-thread`       | Resolve a thread (use `--thread-id`) |
| `reply-to-discussion-comment` | Reply to discussion comment          |
| `get-pr-discussion-comments`  | Fetch discussion comments            |

**Typical workflow:**

1. `erk exec get-pr-review-comments --pr 123`
2. Make code changes
3. `erk exec resolve-review-thread --thread-id PRRT_xxx`

### Plan Operations

When working with erk-plan issues:

| Command                     | Purpose                            |
| --------------------------- | ---------------------------------- |
| `plan-save-to-issue`        | Save plan to GitHub issue          |
| `get-plan-metadata`         | Get metadata from plan issue       |
| `setup-impl-from-issue`     | Set up .impl/ from issue           |
| `plan-submit-for-review`    | Extract plan content for PR review |
| `plan-create-review-branch` | Create review branch with plan     |
| `get-issue-body`            | Fetch issue body (REST API)        |
| `update-issue-body`         | Update issue body (REST API)       |

### Session Operations

When working with Claude Code sessions:

| Command                   | Purpose                           |
| ------------------------- | --------------------------------- |
| `list-sessions`           | List sessions for current project |
| `preprocess-session`      | Compress session for analysis     |
| `upload-session`          | Upload session to gist            |
| `download-remote-session` | Download session from gist        |

### Marker Operations

For inter-process communication:

| Command         | Purpose                |
| --------------- | ---------------------- |
| `marker create` | Create marker file     |
| `marker exists` | Check if marker exists |
| `marker read`   | Read marker content    |
| `marker delete` | Delete marker file     |

All marker commands require `--session-id`.

## Full Reference

For complete syntax details on all 65+ commands:

@reference.md
