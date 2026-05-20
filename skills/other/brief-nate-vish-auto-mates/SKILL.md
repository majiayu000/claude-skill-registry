---
name: brief
description: Catch up on parallel sessions and brief the user on project state
allowed-tools:
  - Read
  - Glob
---

# /brief - Catch Up & Brief

Two jobs: (1) catch yourself up on what happened in parallel sessions, (2) tell the user what's going on.

## Usage

```
/brief
```

## Instructions

### Step 1: Catch Up (for the agent)

Read `Dashboard/Brief.md` and scan **Recent Activity** for entries you haven't seen yet — anything from other agents or sessions since your last read. Internalize what changed: new decisions, status updates, completed work, blockers.

Also check for handoff messages or new files:
- `Dashboard/Work_Space/HANDOFF_*.md` — pending handoffs
- `Dashboard/Work_Space/KNOWLEDGE_REQUEST_*.md` — unfulfilled research requests
- `Dashboard/Work_Space/**/MESSAGE_FROM_*.md` — messages left by other agents

### Step 2: Brief the User

Present a concise summary covering what's new AND overall state:

```
=== BRIEF ===

WHAT'S NEW (since last check)
=============================
[Bullet list of Recent Activity entries the user likely hasn't seen.
Focus on what OTHER agents did in parallel sessions.
If nothing new, say "No new activity."]

CURRENT FOCUS
=============
[Current focus from Brief.md — 1-2 lines]

ACTIVE PROJECTS
===============
[Active projects table — status + next action]

TEAM STATUS
===========
[Team status table]

PENDING
=======
[Any HANDOFF files, KNOWLEDGE_REQUEST files, or MESSAGE_FROM files.
If none, say "None"]

NEXT STEPS
==========
[Next steps list from Brief.md]

=============
```

## Rules

- **"What's New" comes first** — the user wants to know what they missed, not re-read what they already know
- **Be specific** in "What's New" — "Gal reviewed Sunny and approved with conditions" not "Gal did some work"
- **Keep it concise** — this is a quick catch-up, not a report
- **Don't read full agent memory files** — this is project-level only
- **If running as a specific agent**, note which Recent Activity entries are from OTHER agents (that's what you're catching up on)
