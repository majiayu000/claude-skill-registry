---
name: compact
description: Compact agent memory by archiving old sessions and updating Context.md
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# /compact - Memory Compaction

Compact an agent's memory: archive old sessions, summarize them, and refresh Context.md.

## Usage

```
/compact                    # Compact current agent's memory
/compact <agent>            # Compact a specific agent's memory
/compact all                # Compact all 9 agents
```

## Available Agents

planner, builder, checker, brainstorm, gal, legal, gitdude, fetcher, orca

## Instructions

When invoked, perform these steps for the target agent(s):

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

### Step 2: Count Sessions

List all files in `Memory_Logs/Sessions/`. If there are 5 or fewer files, skip compaction (memory is fine).

### Step 3: Archive Old Sessions

If there are more than 5 session files:

1. **Sort by date** (filename or content date)
2. **Keep the latest 3** verbatim in Sessions/
3. **Move older files** to `Memory_Logs/Archive/[YYYY-MM]/`
4. **Create summary** at `Memory_Logs/Archive/[YYYY-MM]/sessions_summary.md`:

```markdown
# Session Archive — [YYYY-MM]
**Agent:** [Agent Name]
**Compacted:** [today's date]
**Sessions archived:** [count]

## Summaries

### [Original filename]
**Date:** [date from content]
- [2-3 bullet summary of what happened]
- [key decisions or outcomes]

### [Next filename]
...
```

### Step 4: Refresh Context.md

Read the agent's current state and update `Memory_Logs/Context.md`:

```markdown
# Context — [Agent Name]
**Last updated:** [today's date]

*Quick startup snapshot. Read this first instead of scanning all memory files.*

---

## Project Summary
[2-3 sentences about current project state from Dashboard/Brief.md]

## Current Task
[From Checkpoint.md — current status, or "None — ready for assignment"]

## Recent Lessons
[Last 3 entries from Lessons.md]

## Active Preferences
[Key preferences from Preferences.md]

## Team Status
See Dashboard/Brief.md for full team status.

## My Recent Sessions
[1-2 line summary of each of the 3 kept sessions]

## Archived Sessions
[Count] sessions archived in Archive/. See Archive/[YYYY-MM]/sessions_summary.md for summaries.
```

### Step 5: Report

```
=== COMPACTION COMPLETE ===
Agent: [name]
Sessions before: [count]
Sessions kept: [count] (latest 3)
Sessions archived: [count]
Archive location: Memory_Logs/Archive/[YYYY-MM]/
Context.md: Updated
===========================
```

## Notes

- **Memory is SACRED:** Never delete session files — always move to Archive/
- **READ before WRITE:** Always read files before modifying
- **Keep latest 3 sessions verbatim** — they're the most relevant context
- **Context.md is a snapshot** — it gets overwritten on each compaction (that's OK, it's generated)
- If `compact all` is used, process agents in order and report for each
- Compaction threshold: 5+ session files triggers archival

---
*Part of AutoMates.AI memory management system*
