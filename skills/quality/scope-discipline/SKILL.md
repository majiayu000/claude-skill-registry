---
name: scope-discipline
description: Use when implementing features, editing source code, or responding to task handoffs. Enforces doing exactly what was requested - no scope creep, no "while I'm here" additions.
---

# Scope Discipline

## Hard Rule

Do exactly what the task asks. Nothing more.

## Warning Signs

If you catch yourself thinking:

- "While I'm here, I should also..."
- "This would be cleaner if I refactored..."
- "Let me add error handling for edge cases that might..."
- "I'll add a helper function for future use..."
- "This needs better types/documentation..."
- "Let me make this more configurable..."

STOP. Complete the task as specified first. Note improvements in handoff if genuinely valuable.

## What Counts as Scope Creep

| In Scope | Out of Scope |
|----------|--------------|
| Fix the bug reported | Refactor surrounding code |
| Add requested feature | Add "nice to have" extras |
| Handle specified cases | Handle hypothetical cases |
| Use existing patterns | Introduce new patterns |
| Modify listed files | "While I'm here" changes |

## The Test

Before making a change, ask: "Did the task explicitly ask for this?"

- **Yes** → Do it
- **No, but necessary for task** → Do it, explain why
- **No, but would be nice** → Don't do it. Note in handoff if important.

## Recovery

If you've already gone out of scope:

1. Revert uncommitted scope creep
2. Complete original task
3. Propose extras as separate follow-up task
