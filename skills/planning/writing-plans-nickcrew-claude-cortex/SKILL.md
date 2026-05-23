---
name: writing-plans
description: Structured plan-writing skill adapted from obra/superpowers. Produces actionable plans that map directly to cortex workflows and tasks.
license: MIT (obra/superpowers)
---

# `/collaboration:writing-plans`

Transforms brainstorm output into a concrete execution plan that cortex can enforce.

## Inputs

- Brainstorm summary (see `/ctx:brainstorm`).
- Relevant workflows in `workflows/` and rules in `rules/Planning.md`.
- Any mandated modes (e.g., `modes/Super_Saiyan.md`, `modes/Security_Audit.md`).

## Steps

1. **Restate Objective**
   - One paragraph referencing ticket/issue + constraints.
2. **Identify Workstreams**
   - Break work into 2–5 streams (frontend, backend, docs, infra, etc.).
   - For each, list required agents/modes/rules.
3. **Define Tasks per Stream**
   - Bullet tasks with Definition of Done + validation (tests, lint, visual review).
   - Include verification hooks (`rules/`, `commands/testing.yaml`).
4. **Risk / Mitigation**
   - Capture open questions, dependencies, rollback steps.
5. **Task Sync**
   - For each bullet, create a Task TUI entry (press `T` → `A`).
   - OR run `/ctx:execute-plan` after this skill to auto-seed tasks (coming soon).

## Output template

```
## Objective

## Workstreams
### Stream 1 – <name>
- Task … (agent/mode/rule, validation)
- Task …

### Stream 2 – …

## Risks & Mitigations
- …
```

Store the plan in chat + `docs/plans/<date>-<slug>.md` if long-lived. Then move to `/ctx:execute-plan`.

## Resources

- Plan template snippet: `skills/collaboration/writing-plans/resources/template.md`.
