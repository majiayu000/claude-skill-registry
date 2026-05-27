---
name: catchup
description: Catchup — Resume Work After Time Away
user-invocable: true
argument-hint: "[days] - number of days to look back (default: 7)"
---

# Catchup — Resume Work After Time Away

Analyze recent project activity and provide a narrative summary of where the developer left off.

## Usage

- `/catchup` — Last 7 days (default)
- `/catchup 3` — Last 3 days
- `/catchup 14` — Last 2 weeks
- `/catchup 30` — Last month

## Instructions

Parse the argument as number of days. Default to 7 if not provided.

### Step 0: Detect Time Since Last Activity

```bash
git log -1 --format="%cr (%ci)"   # e.g. "14 days ago (2026-01-27 15:30:00 +0100)"
git stash list                     # check for stashed work
git branch -a --sort=-committerdate | head -10  # recently active branches
```

- If last activity is older than the requested window, **auto-expand** the window to include it. Cap at 60 days max. Note: *"No activity in the last N days. Last commit was X days ago — expanding window."*
- Always lead the summary with: **"Last activity: X days ago (date)"**
- If stashes exist, note them prominently — they often represent interrupted work.
- If non-master branches were recently active, note them — they may represent in-progress features.

### Step 1: Find Active Specs & Plans (Highest Priority)

Use the Glob tool (NOT git log with `**` globs — those are unreliable on Windows) to find spec/plan files:

```
Glob: **/spec.md, **/tasks.md, **/plan.md, **/requirements.md
```

Then for each file found, check if it was modified within the window:

```bash
git log -1 --format="%ai" -- <filepath>
```

**Only read files modified within the (possibly expanded) window.** Do not read all spec/plan files in the repo — that wastes context.

For each relevant file:

**tasks.md (implementation tasks):**
1. Read the full file
2. Count `[x]` (done) vs `[ ]` (pending) checkboxes
3. Identify in-progress task groups (some checked, some not)
4. List actual uncompleted task descriptions

**spec.md with `[ ]` items (acceptance criteria — NOT implementation tasks):**
1. Read the file
2. Count checked/unchecked acceptance criteria
3. Cross-reference with recent commits — if criteria appear implemented but unchecked, note the discrepancy: *"Acceptance criteria appear implemented based on commits but not checked off in spec."*
4. Label these as "Acceptance Criteria", not "Tasks"

**plan.md without checkboxes (numbered headings or prose):**
1. Read the file
2. Cross-reference numbered tasks/headings with commit history to infer completion
3. Report inferred completion status

### Step 2: Gather Git Activity

```bash
# Recent commits — cap at 15, note total count if more
git log --since="$DAYS days ago" --oneline --all | head -15

# Total commit count (for "...and N more")
git log --since="$DAYS days ago" --oneline --all | wc -l

# Current branch
git branch --show-current
```

### Step 3: Check Uncommitted Work

```bash
git status --short
git diff --stat
```

### Step 4: Present the Summary

Always include these sections regardless of tier:
- **Last activity** line at the top
- **Stashes** (if any)
- **Active branches** (if non-master branches have recent activity)
- **What Was Happening** — a 2-4 sentence narrative synthesizing the work, even in Tier 1
- **Likely Next Steps** — inferred from evidence

**If specs/plans were found (Tier 1):**

```
## Catchup Summary (last N days)

**Last activity:** X days ago (date)
**Branch:** <branch> | Working tree: <clean/N changes>
**Stashes:** <none or list>
**Active branches:** <master only, or list others with last commit date>

### What Was Happening
<2-4 sentence narrative synthesizing the work direction, grouped by theme/feature>

### Active Specs & Plans

📋 **<Spec/Plan Title>** (from first heading)
   <path/>
   Tasks: X/Y completed (Z%)

   **In-progress: <Task Group Name> (A/B)**
   - [ ] Actual uncompleted task description
   - [ ] Another uncompleted task

   **Not started: <Task Group Name> (0/C)**
   - [ ] Task description

📋 **<Spec Title>** — Acceptance Criteria
   <path/>
   Criteria: 0/6 checked (but appear implemented — verify manually)
   - [ ] Criteria description
   - [ ] Criteria description

📋 **<Another Spec>** ✓ Complete
   All N/N tasks done.

### Recent Commits
- <hash> <message> *(date)*
- ...
- (...and N more)

### Likely Next Steps
<Inferred from uncompleted tasks, commit patterns, and branch state>

### Uncommitted Changes
<git status output or "(none)">
```

**If NO specs/plans found (Tier 2) — deeper git analysis:**

```
## Catchup Summary (last N days)

**Last activity:** X days ago (date)
**Branch:** <branch> | Working tree: <clean/N changes>
**Stashes:** <none or list>

### What Was Happening
<2-4 sentence narrative>

### Focus Areas (grouped by feature/theme from commit messages)
- **<Feature/Area>** (N commits) — description of what was being built
- **<Feature/Area>** (N commits) — description

### Recent Commits
- <hash> <message> *(date)*
- ...

### Likely Next Steps
<Inferred from patterns>

### Uncommitted Changes
<git status output or "(none)">
```

**If NO commits AND no specs (Tier 3):**

```
## Catchup Summary (last N days)

**Last activity:** X days ago (date)

No commits found in the last N days.

### Uncommitted Changes
<git status/diff output — analyze what's in progress>
```

**If completely clean (Tier 4):**

```
## Catchup Summary (last N days)

No activity found in the last N days. Working tree is clean.
Last commit: <hash> <message> (<relative date>)
```

## Key Principles

- **Specs and plans are the highest signal** — always check for them first
- **Show actual uncompleted task text** — not just "3 remaining", show what they are
- **Distinguish tasks from acceptance criteria** — tasks.md `[ ]` = implementation tasks; spec.md `[ ]` = acceptance criteria. Label differently. If criteria appear implemented (based on commits) but unchecked, say so
- **Handle plans without checkboxes** — infer completion from commit history when plan uses numbered headings instead of `[x]`/`[ ]` syntax
- **Always include narrative synthesis** — even in Tier 1, add a "What Was Happening" section grouping work by theme
- **Cap commit lists at 15** — show count of remaining. Group by theme in the narrative, not the raw list
- **Use Glob tool for file discovery** — do not use `git log -- "**/*.md"` glob patterns (unreliable on Windows)
- **Only read recently modified specs** — do not load all specs in the repo. Check modification date first
- **Check stashes and branches** — these reveal interrupted and in-progress work invisible in commits
- **Auto-expand window, cap at 60 days** — if no activity in requested window, expand to last commit but never beyond 60 days
- **Lead with temporal orientation** — "Last activity: X days ago" is always the first line
- **Infer next steps from evidence** — uncompleted tasks, recent focus areas, branch state
