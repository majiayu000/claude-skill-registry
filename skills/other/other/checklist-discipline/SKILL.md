---
name: checklist-discipline
description: Maintain rigorous checklist discipline with incremental updates
category: Thinking Analysis
---

# Skill: checklist-discipline

## What I do

I enforce the rigorous use of checklists to prevent cognitive overload and avoidable errors. I distinguish between different checklist types and ensure they are used as living documents during complex operations.

## When to use me

- During repetitive but high-stakes operations (e.g. deployments, migrations)
- When executing complex multi-step tasks that span multiple sessions
- When creating standardised procedures for a team
- To verify the "Definition of Done" for a task

## Core principles

1. **DO-CONFIRM vs READ-DO** — Choose the right style. READ-DO for unfamiliar tasks; DO-CONFIRM for expert routines to verify completeness.
2. **Incremental updates** — Tick off items immediately upon completion, never at the end.
3. **Granularity balance** — Ensure steps are actionable but not trivial. Focus on the "killer steps" where errors often occur.
4. **Living documents** — Update the checklist if a new edge case or error is discovered during execution.

## Patterns & examples

**Surgical Checklist Pattern:**
Focus on high-risk transition points:
- **Pre-flight:** Verify environment variables, backup status, and access permissions.
- **Execution:** Atomic steps with specific verification commands.
- **Post-flight:** Validate logs, health checks, and stakeholder notification.

**Checklist Design:**
- **Actionable:** "Run npm test" instead of "Check tests".
- **Verifiable:** "Ensure build/ folder exists" instead of "Check build".
- **Concise:** Keep checklists to 5-9 items per logical section.

## Anti-patterns to avoid

- ❌ **Batch ticking** — Marking items as done after the work is finished (defeats the purpose).
- ❌ **Checklist bloat** — Including trivial steps that lead to "checklist fatigue" and skipping.
- ❌ **Stale checklists** — Following a list that doesn't reflect the current state of the codebase.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Checklist Discipline.md`

## Related skills

- `task-completer` — Ensuring all requirements are met
- `task-tracker` — Managing task lists and progress
- `pre-action` — Deliberate planning before checklist execution
- `documentation-writing` — Creating clear, usable procedures
