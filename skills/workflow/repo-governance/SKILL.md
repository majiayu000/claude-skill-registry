---
name: repo-governance
description: Repository governance rules, task status, and UX→UI→FE order.
---

# Repository Governance (Cross-cutting Rules)

## Global Terminology Rule
- Any agent performing translation, rewriting, or copy editing MUST load and respect `docs/terminology.md`.
- Terms listed in `docs/terminology.md` MUST NOT be translated, reworded, or localized.
- If a term is missing or ambiguous, MUST ask for clarification or propose a glossary update.
- QA MUST flag terminology violations as blockers.

## UX → UI → FE Development Order
- Product Designer defines UX intent first, then UI specifications.
- UI / Frontend agents implement approved UI specs in code.
- Frontend agents should not invent UX or UI decisions.
- If UX or UI intent is unclear, implementation should pause and request clarification.

## Implementation Placement
- Implementation agents should stage work under `tasks/NNN-*/output/` first, then integrate as directed by task docs.

## Admin Escalation
- Admin / Maintainer actions must be explicit (no implicit admin behavior).
- Significant changes require intent + expected impact described up front.
- Prefer minimal, focused edits; avoid broad “cleanup” changes with unclear scope.

## Task Status Recording
- Record `Status: Done` or `Status: In Progress` at the bottom of `task.md` when updating a task.
