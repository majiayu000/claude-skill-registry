---
name: memorize
description: Update agent memory (Sessions, Lessons, Preferences, Checkpoint, Context) and Brief.md
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
---

# /memorize - Save Agent Memory + Update Dashboard

One command to update all memory files and Brief.md. Replaces manually asking "update your memory."

## Usage

```
/memorize                    # Save current agent's memory + update Brief.md
/memorize <agent>            # Save a specific agent's memory
```

## Available Agents

planner, builder, checker, brainstorm, gal, legal, gitdude, fetcher, orca

## Instructions

When invoked, perform these steps IN ORDER for the target agent:

### Step 1: Identify the Agent

Determine the agent's Memory_Logs path:
- planner: `AgenTeam/Planner/Memory_Logs/`
- builder: `AgenTeam/Builder/Memory_Logs/`
- checker: `AgenTeam/Checker/Memory_Logs/`
- brainstorm: `AgenTeam/BrainStorm/Memory_Logs/`
- gal: `AgenTeam/Gal/Memory_Logs/`
- legal: `AgenTeam/Legal/Memory_Logs/`
- gitdude: `AgenTeam/GitDude/Memory_Logs/`
- fetcher: `Library/Fetcher/Memory_Logs/`
- orca: `AgenTeam/Orca/Memory_Logs/`

If no agent specified, use the current agent (the one active in this session).

### Step 2: Read Current State

Read these files to understand what needs updating:
1. `Memory_Logs/Checkpoint.md` — current task status
2. `Memory_Logs/Lessons.md` — existing lessons
3. `Memory_Logs/Preferences.md` — existing preferences
4. Latest file in `Memory_Logs/Sessions/` — recent session context
5. `Dashboard/Brief.md` — current project state

### Step 3: Append to Sessions/

Create or append to `Memory_Logs/Sessions/Session_[YYYY-MM-DD].md`:

```markdown
# Session — [YYYY-MM-DD]

**Agent:** [Agent Name]
**Task:** [Brief description of what was worked on]

---

## What Happened
- [Key actions taken]
- [Decisions made]
- [Files created/modified]

## Outcome
[Result of the work]

---
```

**IMPORTANT:** If a session file for today already exists, APPEND to it — never overwrite.

### Step 4: Update Lessons.md

**READ first**, then APPEND if something was learned this session:

```markdown
## [YYYY-MM-DD] - [Brief title]
- **Context:** [what happened]
- **Lesson:** [what to remember]
- **Apply when:** [future trigger]
```

If nothing new was learned, skip this step.

### Step 5: Update Preferences.md

**READ first**, then APPEND if user expressed new preferences:

```markdown
## [Category]
*[YYYY-MM-DD]*
- **Preference:** [detail]
```

If no new preferences, skip this step.

### Step 6: Update Checkpoint.md

**READ first**, then update:
- If task is complete: mark status as complete, add to Checkpoint History
- If task is in progress: update progress steps, current state, next action
- If no active task: ensure status shows "No active task"

### Step 7: Refresh Context.md

Overwrite `Memory_Logs/Context.md` with a fresh snapshot:

```markdown
# Context — [Agent Name]
**Last updated:** [YYYY-MM-DD]

*Quick startup snapshot. Read this first instead of scanning all memory files.*

---

## Project Summary
[2-3 sentences from Dashboard/Brief.md current focus]

## Current Task
[From Checkpoint.md — status and description, or "No active task"]

## Recent Lessons
[Last 3 entries from Lessons.md — one line each]

## Active Preferences
[Key preferences from Preferences.md]

## Team Status
See Dashboard/Brief.md for full team status.

## My Recent Sessions
[1-2 line summary of last 2-3 sessions]
```

### Step 8: Update Dashboard/Brief.md

**Only if project-wide changes happened.** READ first, then:

- **Recent Activity:** Add row: `| [YYYY-MM-DD] | [Agent] | [what happened] |`
- **Team Status:** Update agent state if changed (e.g., "Ready" → "Working on X")
- **Active Projects:** Update project status/next if a project changed
- **Next Steps:** Add or remove items if priorities shifted

If this session was internal work (no project-wide impact), skip Brief.md.

### Step 9: Report

```
=== MEMORIZED ===
Agent: [name]
Sessions/:    [created/appended Session_YYYY-MM-DD.md]
Lessons.md:   [appended X new / no change]
Preferences:  [appended X new / no change]
Checkpoint:   [updated / no change]
Context.md:   [refreshed]
Brief.md:     [updated / no change]
=================
```

## Critical Rules

- **Memory is SACRED:** ALWAYS read before write, ALWAYS append (except Context.md)
- **Context.md IS overwritten** — it's a generated snapshot, not accumulated data
- **Sessions/ gets one file per date** — append if same day, new file if new day
- **Never delete memory** — only add to it
- **Brief.md is project-level** — only update for project-wide changes, not routine work
- **Be honest** — only log lessons actually learned, not filler

---
*Part of AutoMates.AI memory management system*
