---
name: file-todos
description: Manage file-based todo tracking in the todos/ directory
---

# File-Based Todo Tracking

Provides workflows for creating, managing, and completing todos stored as markdown files.

## Overview

The `todos/` directory contains markdown files with YAML frontmatter for tracking work items.

## File Naming Convention

```
{issue_id}-{status}-{priority}-{description}.md

Examples:
001-pending-p1-security-fix.md
002-ready-p2-performance-opt.md
003-complete-p3-cleanup.md
```

## Status Lifecycle

```
pending → ready → complete
   ↓
(deleted if skipped)
```

## What do you want to do?

1. **Create a todo** → See "Creating Todos" below
2. **Triage pending items** → Use `/triage`
3. **Work on todos** → Use `/resolve_todo`
4. **Check dependencies** → See "Dependency Management" below

---

## Instrumentation

```bash
# Log usage when using this skill
Call MCP `call_tool_logger_manager` { action: "logSkill", name: "file-todos", outcome: "manual" }
```

## Creating Todos

```bash
# Get next ID
next_id=$(ls todos/*.md 2>/dev/null | grep -o '[0-9]\+' | sort -n | tail -1 | awk '{printf "%03d", $1+1}')
[ -z "$next_id" ] && next_id="001"

# Copy template
cp todos/todo-template.md todos/${next_id}-pending-{priority}-{description}.md
```

## Dependency Management

```yaml
# In YAML frontmatter
dependencies: ["001", "002"]  # Blocked by these issues
dependencies: []               # No blockers
```

Check blockers:
```bash
grep "dependencies:" todos/{file}.md
```

## Quick Commands

```bash
# List by status
ls todos/*-pending-*.md
ls todos/*-ready-*.md
ls todos/*-complete-*.md

# List by priority
ls todos/*-p1-*.md

# Count by status
for s in pending ready complete; do
  echo "$s: $(ls todos/*-$s-*.md 2>/dev/null | wc -l)"
done
```
