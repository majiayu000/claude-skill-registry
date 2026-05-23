---
name: session-management
description: Apply when initializing, saving, resuming, or closing a work session
---

# Session Management Guide

## Phase Tracking

Sessions track EDIRD phases:
- NOTES.md: "Current Phase" section with phase, last verb, gate status
- PROGRESS.md: "Phase Plan" section with 5 phases and status

## MUST-NOT-FORGET

- Session folder location: `[DEFAULT_SESSIONS_FOLDER]/_YYYY-MM-DD_[SessionTopicCamelCase]/`
- Default: `[DEFAULT_SESSIONS_FOLDER]` = `[WORKSPACE_FOLDER]` (override in `!NOTES.md`)
- Required files: NOTES.md, PROBLEMS.md, PROGRESS.md
- Lifecycle: Init → Work → Save → Resume → Close → Archive
- Sync session PROBLEMS.md to project on /session-close
- Phase tracking: NOTES.md has current phase, PROGRESS.md has full phase plan

## Session Lifecycle

1. **Init** (`/session-new`): Create session folder with tracking files
2. **Work**: Create specs, plans, implement, track progress
3. **Save** (`/session-save`): Document findings, commit changes
4. **Resume** (`/session-resume`): Re-read session documents, continue work
5. **Close** (`/session-close`): Sync findings to project files, archive

## Session Folder Location

**Base:** `[DEFAULT_SESSIONS_FOLDER]` (default: `[WORKSPACE_FOLDER]`, can be overridden in `!NOTES.md`)

**Format:** `[DEFAULT_SESSIONS_FOLDER]/_YYYY-MM-DD_[SessionTopicCamelCase]/`

**Example:** `_PrivateSessions/_2026-01-12_FixAuthenticationBug/`

## Required Session Files

Use templates from this skill folder:

- **NOTES.md** (`NOTES_TEMPLATE.md`): Key information, agent instructions, working patterns
- **PROBLEMS.md** (`PROBLEMS_TEMPLATE.md`): Problems found and their status (Open/Resolved/Deferred)
- **PROGRESS.md** (`PROGRESS_TEMPLATE.md`): To-do list, done items, tried-but-not-used approaches

## Assumed Workflow

```
1. INIT: User initializes session (`/session-new`)
   └── Session folder, NOTES.md, PROBLEMS.md, PROGRESS.md created

2. PREPARE (one of):
   A) User prepares work manually
      └── Creates INFO / SPEC / IMPL documents, tracks progress
   B) User explains problem, agent assists
      └── Updates Problems, Progress, Notes → researches → creates documents

3. WORK: User or agent implements
   └── Makes decisions, creates tests, implements, verifies
   └── Progress and findings tracked continuously

4. SAVE: User saves session for later (`/session-save`)
   └── Everything updated and committed

5. RESUME: User resumes session (`/session-resume`)
   └── Agent primes from session files, executes workflows in Notes
   └── Continue with steps 2-3

6. CLOSE: User closes session (`/session-close`)
   └── Everything updated, committed, synced to project/workspace

7. ARCHIVE: User archives session
   └── Session folder moved to _Archive/
```

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` rule (always-on) for complete ID system.

**Quick Reference:**
- Document: `[TOPIC]-[DOC][NN]` (IN, SP, IP, TP)
  - Example: `CRWL-SP01`, `AUTH-IP01`
- Tracking: `[TOPIC]-[TYPE]-[NNN]` (BG = Bug, FT = Feature, PR = Problem, FX = Fix, TK = Task)
  - Example: `SAP-BG-001`, `UI-PR-003`, `GLOB-TK-015`
- Topic Registry: Maintained in project NOTES.md

## Session Init Template

### NOTES.md
```markdown
# Session Notes

## Session Info
- **Started**: [DATE]
- **Goal**: [Brief description]

## Key Decisions

## Important Findings

## Workflows to Run on Resume
```

### PROBLEMS.md
```markdown
# Session Problems

## Open

## Resolved

## Deferred
```

### PROGRESS.md
```markdown
# Session Progress

## To Do

## In Progress

## Done

## Tried But Not Used
```
