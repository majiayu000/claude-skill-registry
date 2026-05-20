---
name: review-deferred
description: Review deferred verification items. Use when you want to check or clear the deferred review queue without waiting for project completion.
allowed-tools: Read, Edit, Bash, Glob, Grep, AskUserQuestion
---

Review the deferred verification queue and optionally clear reviewed items.

## Context Detection

Determine working context:

1. If current working directory matches pattern `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD (e.g., `/project/features/foo` → `/project`)
   - MODE = "feature"

2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

## Workflow

Copy this checklist and track progress:

```
Review Deferred Progress:
- [ ] Step 1: Read deferred queue
- [ ] Step 2: Present items grouped by phase
- [ ] Step 3: Collect user decisions
- [ ] Step 4: Update queue file
```

## Step 1: Read Deferred Queue

Read `.claude/deferred-reviews.json` from PROJECT_ROOT.

**If file doesn't exist or queue is empty:**

```
NO DEFERRED ITEMS
=================
The deferred review queue is empty. No items pending human review.
```

**Stop here** if no items to review.

**If file fails to parse:**

Back up the corrupt file to `.claude/deferred-reviews.json.bak`, report the issue,
and stop:

```
QUEUE FILE CORRUPT
==================
.claude/deferred-reviews.json could not be parsed.
Backed up to .claude/deferred-reviews.json.bak

Run /go to continue — a fresh queue will be created automatically.
```

## Step 2: Present Items

Filter to items where `reviewed: false`. Group by phase:

```
DEFERRED REVIEW QUEUE
=====================
{N} items pending review across {P} phases.

Phase 1:
- [ ] "{criterion}" (Task {task_id})
  Context: {file}:{line} — {summary}
  Deferred: {deferred_at}

Phase 3:
- [ ] "{criterion}" (Task {task_id})
  Context: {file}:{line} — {summary}
  Deferred: {deferred_at}
```

## Step 3: Collect User Decisions

Use AskUserQuestion with options:

- **"All look good"** — Mark all items as `reviewed: true`, then clear
- **"Review individually"** — Present each item one by one (see Individual Review below)
- **"Cancel"** — No changes, keep queue as-is

### Individual Review

For each unreviewed item, use AskUserQuestion:

```
Item {i}/{N}: "{criterion}" (Task {task_id})
Context: {file}:{line} — {summary}
```

Options:
- **"Looks good"** — Mark `reviewed: true`
- **"Needs fix"** — Keep `reviewed: false`, note for follow-up
- **"Skip"** — Leave unchanged, move to next item

After reviewing all items, summarize:
```
REVIEW COMPLETE
===============
Approved: {X}
Needs fix: {Y}
Skipped: {Z}
```

## Step 4: Update Queue File

1. Set `reviewed: true` on approved items
2. Remove all `reviewed: true` items from the queue array
3. Update `last_drained` and `last_drain_reason` fields:
   ```json
   {
     "last_drained": "{ISO timestamp}",
     "last_drain_reason": "explicit_review"
   }
   ```
4. Write using atomic pattern: write to temp file, rename to `.claude/deferred-reviews.json`

**If items marked "Needs fix" exist:**

```
FOLLOW-UP NEEDED
================
{Y} items need attention:

- "{criterion}" (Task {task_id})
  Context: {file}:{line}

These items remain in the queue and will surface again at the next drain trigger.
```

## Drain Reasons

When invoked by other skills, the drain reason is passed as context:

| Caller | Drain Reason |
|--------|-------------|
| `/review-deferred` (direct) | `explicit_review` |
| `/go` Case E (completion) | `project_completion` |
| `/go` Case F (blocker) | `blocker_drain` |
| `/phase-checkpoint` (max queue) | `max_queue_reached` |
