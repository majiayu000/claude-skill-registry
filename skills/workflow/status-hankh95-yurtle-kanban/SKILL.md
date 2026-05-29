---
name: status
description: Show kanban board status, agent workload, and work distribution
disable-model-invocation: false
allowed-tools: Bash(yurtle-kanban *), Bash(git *)
---

# Kanban Status

Show the current state of the kanban board and work distribution.

## Overview

```bash
# Board statistics
yurtle-kanban stats

# Current git branch
git branch --show-current

# Recent commits
git log --oneline -5
```

## In Progress

```bash
yurtle-kanban list --status in_progress
```

## Ready to Start

```bash
yurtle-kanban list --status ready --limit 10
```

## In Review

```bash
yurtle-kanban list --status review
```

## Recently Completed

```bash
yurtle-kanban list --status done --limit 5
```

## Blocked Items

```bash
yurtle-kanban list --status blocked
```

## Summary

Provide a brief summary of:
- What's currently being worked on
- What's ready to pick up (highest priority)
- What's waiting for review
- Any blocked items that need attention
- Recommendations for next steps
