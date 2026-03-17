---
name: tachikoma-frontmatter
description: Analyze Context Lake entities and fix frontmatter issues. Use when asked to run frontmatter cleanup, fix missing fields, validate frontmatter against schema, or standardize entity metadata.
allowed-tools: Read, Write, Glob, Grep
---

# Tachikoma Frontmatter Cleanup

You are running frontmatter cleanup on a Context Lake workspace. Your job is to analyze entities and propose frontmatter fixes by creating decision files.

## Context Lake Structure

The workspace IS the Context Lake. Entity directories live at the workspace root:
- `.claude/schema.yaml` - Entity type definitions (REQUIRED for this mode)
- `.claude/tachikoma-summary.yaml` - Previous observations
- `{entity_type}/` - Entity directories (tasks/, notes/, roles/, etc.)
- `decisions/` - Where you write proposals

## What to Look For

1. **Missing required fields**: Entities missing fields defined as required in schema
   - Example: Task has no status → propose adding `status: open`

2. **Invalid values**: Fields with values that don't match schema constraints
   - Example: Status is 'DONE' → should be 'done' (lowercase)

3. **Missing optional fields**: Content suggests fields that should be added
   - Example: Task mentions 'due Friday' → propose adding due date

4. **Inconsistent formatting**: Dates, slugs, etc. that don't match patterns
   - Example: Date is '1/15/24' → should be '2024-01-15'

## Process

1. Read `.claude/schema.yaml` to understand required fields (STOP if missing)
2. Read `.claude/tachikoma-summary.yaml` for previous observations
3. For each entity type in schema, glob all files in that directory
4. Read each entity and check frontmatter against schema
5. Create decision files for issues found
6. Update `.claude/tachikoma-summary.yaml` with findings

## Decision Format

Write decisions to `decisions/` directory:

```markdown
---
title: "fix: add required status field to tasks"
status: pending
decision_type: frontmatter_update
subject_path: tasks/example-task.md
confidence: 0.9
created_at: {ISO timestamp}
---

## Current State

Current frontmatter in tasks/example-task.md:
---
title: Example Task
---

## Suggested Change

Updated frontmatter:
---
title: Example Task
status: open
---

## Reasoning

Task is missing required 'status' field per schema. Based on content mentioning 'working on', suggesting 'open'.
```

## Batching

If many entities have the same issue:
- **< 5 issues**: Create individual decisions
- **>= 5 issues**: Create one decision listing all affected entities

Example batch decision:
```markdown
---
title: "fix: add date frontmatter to journal entries"
status: pending
decision_type: frontmatter_update
confidence: 0.9
---

## Current State

7 journal files missing required 'date' frontmatter field.

## Suggested Change

Add date frontmatter to each file (extract from filename):
- journal/2025-11-10-day-zero.md → date: 2025-11-10
- journal/2025-11-11-ceuta.md → date: 2025-11-11
...

## Reasoning

Schema requires 'date' field for journal entries. All files follow YYYY-MM-DD naming, so date can be extracted from filename.
```

## Guidelines

- Schema must exist before running frontmatter cleanup
- Check existing pending decisions to avoid duplicates
- Be specific about what needs to change
- Provide reasoning for suggested values

## Output

When done, update `.claude/tachikoma-summary.yaml`:

```yaml
last_scan: {ISO timestamp}
cleanup_mode: frontmatter
entity_counts:
  tasks: 10
  notes: 5
observations:
  - All tasks have required fields
  - 3 notes missing tags field
pending_decisions:
  - frontmatter-fix-notes-tags.md
```
