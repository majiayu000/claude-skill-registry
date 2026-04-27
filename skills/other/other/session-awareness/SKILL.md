---
name: session-awareness
description: >
  Project state awareness and session recovery for GSD-managed projects.
  Use this skill whenever: starting a new work session, resuming after
  a break, the user asks "where did we leave off" or "what's the current
  state", before making substantial code changes (to check for existing
  plans), the user seems disoriented about project status, or when
  something seems off and STATE.md might have relevant context. Also
  activates when the user references .planning/ files, milestones,
  phases, or project progress.
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - the user references
updated: 2026-04-25
status: ACTIVE
---

# Session Awareness

## GSD Artifact Map

| File | Purpose | When to Read |
|---|---|---|
| `.planning/PROJECT.md` | Vision, constraints, decisions | Understanding project context |
| `.planning/REQUIREMENTS.md` | What we're building (REQ-IDs) | Scoping work |
| `.planning/ROADMAP.md` | Phase structure and status | Finding current position |
| `.planning/STATE.md` | Session memory, blockers, decisions | **Always on resume** |
| `.planning/config.json` | Workflow preferences | Checking mode (yolo/interactive) |
| `.planning/phases/XX-name/XX-YY-PLAN.md` | Detailed task plans | Executing work |
| `.planning/phases/XX-name/XX-YY-SUMMARY.md` | What was built | Reviewing completed work |

### skill-creator Artifacts

| File | Purpose | When to Read |
|---|---|---|
| `.planning/patterns/sessions.jsonl` | Session observations | Pattern detection input |
| `.claude/commands/*.md` | Project-level skills | Before GSD phase execution |
| `.claude/agents/*.md` | Composed agents | Agent selection |
| `~/.claude/commands/*.md` | User-level skills | Fallback when no project skill matches |

## Response Pattern: Before Substantial Work

```
Let me check the current project state...
[Read ROADMAP.md, STATE.md]

This falls under Phase X. There's already a plan at `.planning/phases/...`.
Should I execute that plan, or are you looking to do something different?
```

## Response Pattern: Fresh Session Recovery

```
/gsd:progress  (or)  /gsd:resume-work
```

## Response Pattern: No GSD Structure

```
This project doesn't have GSD initialized yet. Want me to run
`/gsd:new-project` to set up the planning structure?
```

## Response Pattern: Work Conflicts with Plans

```
Heads up — this would modify files that Phase N is planning to create.
Options:
1. Execute Phase N first (recommended)
2. Update the Phase N plan to account for this
3. Proceed anyway and reconcile later
```

## Core Rule

**Always check STATE.md** when resuming or when something seems off — it is the project's memory.
