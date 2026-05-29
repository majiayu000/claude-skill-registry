---
name: exploration
description: "Select mode, delegate to analysis skill."
---

# /exploration - Analysis Mode Router

Route to the appropriate analysis mode. You select the mode, then delegate.

## The Process

1. **Ask which mode** - Use AskUserQuestion with options below
2. **Delegate** - Invoke the selected skill

## Modes

Use AskUserQuestion, then invoke the corresponding skill:

| Mode | Skill | Purpose |
|------|-------|---------|
| Brainstorm | `exploration-brainstorm` | Explore ideas → `ideas/` folder |
| Plan | `exploration-plan` | Structure work → `planned/` folder → Beads |
| Review | `exploration-review` | Code review → bugs |
| Debug | `exploration-debug` | Investigate → bugs |

Invoke with: `Skill: exploration-brainstorm`, `exploration-plan`, `exploration-review`, or `exploration-debug`

## Folder Structure

```
exploration/
  ideas/       ← /brainstorm output
  planned/     ← /plan output (has plan.md)

mission/
  staged/      ← /plan output (has Beads)
  complete/    ← /land archives here
```
