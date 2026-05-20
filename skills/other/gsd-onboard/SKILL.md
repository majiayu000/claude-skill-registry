---
name: gsd-onboard
description: GSD tutorial and command reference. Use when user is new to GSD or asks about commands.
---

# GSD Quick Start

**GSD** = question → research → plan → execute → verify.

## Files

```
.planning/
├── PROJECT.md       # Vision, decisions
├── REQUIREMENTS.md  # REQ-IDs
├── ROADMAP.md       # Phases
├── STATE.md         # Current position
├── config.json      # Settings
├── phases/NN-name/  # Plans + summaries
└── milestones/      # Archives
```

## Commands

| Command | Purpose |
|---------|---------|
| /gsd:new-project | Init project |
| /gsd:new-milestone | New version |
| /gsd:progress | State + next action |
| /gsd:discuss-phase N | Gather context |
| /gsd:plan-phase N | Create plans |
| /gsd:execute-phase N | Build plans |
| /gsd:quick | Small tasks |
| /gsd:verify-work N | Test deliverables |
| /gsd:audit-milestone | Completion check |
| /gsd:complete-milestone | Archive |
| /gsd:debug | Debug with state |
| /gsd:pause-work | Checkpoint |
| /gsd:resume-work | Restore |

## Workflow

```
plan-phase N → /clear → execute-phase N → verify-work N
```

## Concepts

- **Atomic commits:** One per plan, surgical rollback
- **Fresh context:** /clear + STATE.md
- **Wave execution:** Parallel independent plans
- **Modes:** yolo (auto) or interactive
