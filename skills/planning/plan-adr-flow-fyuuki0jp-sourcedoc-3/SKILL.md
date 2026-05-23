---
name: plan-adr-flow
description: Plan and document coding tasks with PLAN.md and ADRs in docs/ADR. Use when a task can be decomposed, when asked to create or update PLAN.md, or when capturing technical decisions.
---

# Plan + ADR Flow

## Goal

Keep task planning and technical decisions documented in `PLAN.md` and `docs/ADR/...` before, during, and after implementation.

## Workflow

1. **Triage task size**
   - If the task is not meaningfully decomposable, proceed without creating `PLAN.md` or ADR unless requested.
   - If the task is decomposable, draft a plan and confirm with the user before implementation.

2. **Create plan and ADR when planning**
   - Create or replace `PLAN.md` at repo root with the implementation plan.
   - Create `docs/ADR/YYYYMMDD-title.md` for the technical decision record before coding.
   - Create `docs/ADR/` if missing.
   - Use a short, lowercase, hyphenated slug for `title`.

3. **Update during implementation**
   - Treat `PLAN.md` as a living memo; update it frequently to reflect reality.
   - Append ADR updates when technical issues or new decisions appear; keep prior entries.

4. **Finalize after implementation**
   - Update ADR with outcomes, changes, and follow-ups.
   - Mark `PLAN.md` as complete or reflect the final state.

## ADR template (minimum)

```markdown
# <Title>

Date: YYYY-MM-DD
Status: Proposed | Accepted | Superseded

## Context
- <Why this decision is needed>

## Decision
- <What is decided>

## Consequences
- <Impact, tradeoffs, follow-ups>

## Change log
- YYYY-MM-DD: <What changed and why>
```

## Notes

- Keep ADR updates additive; never delete past entries.
- Keep `PLAN.md` specific to the current task; do not modify `PLANS.md` unless explicitly asked.
