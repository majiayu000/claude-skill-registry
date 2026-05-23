---
name: memory-bank
description: Manage Memory Bank development logs in .ai_memory/. Use when starting a new feature, updating progress on current work, adding implementation log entries, or checking log status. Triggers on: (1) Starting new features/tasks, (2) "update memory bank" or "log progress", (3) Adding dated entries to implementation logs, (4) Checking Memory Bank status. Always prepends entries with YYYY-MM-DD dates, newest first.
---

# Memory Bank

Manage development logs in `.ai_memory/` with chronological date ordering.

## Date Ordering Rule

**All entries use YYYY-MM-DD format. Newer entries appear FIRST (top of section).**

This ensures recent context takes precedence when reading logs.

## Operations

### 1. Create New Log

When starting a new feature/task:

```bash
# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
DATE=$(date +%Y-%m-%d)
```

1. Check if log exists: `ls .ai_memory/`
2. Copy template: `.ai_memory/TEMPLATE.md` → `.ai_memory/<branch-name>.md`
3. Fill Context section with current date and branch
4. Complete Problem Statement

### 2. Update Existing Log

When adding progress to an existing log:

1. Read current log
2. Identify section to update (Research, Proposed Solution, Status)
3. Add content while preserving structure

### 3. Add Implementation Entry

Add dated entries to the Implementation Log section. **Always prepend (newest first):**

```markdown
## Implementation Log

### 2025-12-29    ← NEW (add here)
- [x] Completed task A
- [ ] Started task B

### 2025-12-28    ← OLDER (stays below)
- [x] Initial setup
```

**Process:**
1. Get today's date: `date +%Y-%m-%d`
2. Check if today's entry exists
3. If exists: Add items to existing date section
4. If not: Create new date header at TOP of Implementation Log

### 4. Show Status

Report current Memory Bank state:

```
Memory Bank Status
==================
File: .ai_memory/<name>.md
Last Updated: YYYY-MM-DD

Sections:
- [x] Context (complete)
- [x] Problem Statement (complete)
- [ ] Research (incomplete)
- [ ] Proposed Solution (incomplete)

Implementation Progress:
- 3 entries logged
- Latest: YYYY-MM-DD
```

## Quick Reference

| Action | Command Pattern |
|--------|-----------------|
| Create | Copy TEMPLATE.md, fill Context |
| Update | Read → Modify section → Write |
| Add Entry | Prepend dated entry to Implementation Log |
| Status | List sections, check completion |

## File Structure

```
.ai_memory/
├── README.md      # Documentation
├── TEMPLATE.md    # Copy for new logs
└── <branch>.md    # Active development logs
```

## Completion Report

After any operation, report:

```
Memory Bank: <operation>
========================
File: .ai_memory/<name>.md
Date: YYYY-MM-DD

Changes:
- <what was added/modified>

Next Steps:
- <suggested actions>
```
