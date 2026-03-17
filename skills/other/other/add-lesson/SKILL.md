---
name: add-lesson
description: Add a new lesson learned to shared rules and sync to context files.
version: 1.1.0
tags: [lessons, governance, rules]
owner: orchestration
status: active
---

# Add Lesson Skill

Add a new lesson learned to the shared rules.

## Overview

When you discover a bug, mistake, or useful pattern, use this skill to document it so all agents learn from it.

## Usage

```
/add-lesson
```

## Prerequisites

- Access to `shared-rules/` and permission to run `scripts/sync-rules.py`.

## Lesson Template

```markdown
### YYYY-MM-DD - Brief Title

- **Issue**: What went wrong or was discovered
- **Root Cause**: Why it happened
- **Fix**: How it was fixed
- **Prevention**: Rule or check to prevent recurrence
- **Applies To**: all | claude | cursor | gemini
- **Files Changed**: List of affected files
```

## Process

1. **Gather information**:
   - What was the issue?
   - What caused it?
   - How was it fixed?
   - How can we prevent it?

2. **Add to lessons file**:
   - Open `shared-rules/lessons-learned.md`
   - Add new entry at TOP of "Recent Lessons" section
   - Use the template format

3. **Run sync**:
   ```bash
   python scripts/sync-rules.py
   ```

4. **Verify propagation**:
   - Check CLAUDE.md updated
   - Check timestamp

## Example

```markdown
### 2026-01-22 - Task Tool Token Efficiency

- **Issue**: Spawning Claude workers via subprocess was expensive (~13k tokens overhead)
- **Root Cause**: Full context duplication to each subprocess
- **Fix**: Use native Task tool with context filtering
- **Prevention**: Always prefer Task tool over subprocess for Claude workers
- **Applies To**: claude
- **Files Changed**:
  - `.claude/skills/implement-task/SKILL.md`
  - `CLAUDE.md`
```

## Categories

Lessons should be categorized by:
- `all` - Applies to all agents
- `claude` - Claude-specific
- `cursor` - Cursor-specific
- `gemini` - Gemini-specific

## Archiving

After 30 days or when list gets long:
- Move old lessons to "Archived Lessons" section
- Keep for historical reference

## Outputs

- Updated `shared-rules/` content and synced context files (e.g. `CLAUDE.md`).

## Error Handling

- If sync fails, do not proceed; resolve and rerun `scripts/sync-rules.py`.
- If lesson template is incomplete, request the missing fields before adding.

## Related Skills

- `/sync-rules` - Sync shared rules into context files
