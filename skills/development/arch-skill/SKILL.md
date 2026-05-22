---
name: arch_skill
description: Formalize architecture planning into a single, iterative workflow and produce one canonical architecture document (no doc sprawl). Use for architectural changes, refactors, or new system design.
---

# arch_skill

## Purpose
This skill turns architecture work into a **repeatable, interactive** process that yields a single high‑quality architecture document. It prioritizes clarity, falsifiability, and execution readiness.

## Primary outcome
A **single canonical architecture document** that:
- Follows the template in `docs/arch_skill_raw_notes.md`.
- Captures research grounding, current/target architecture, call‑site audit, phased plan, test strategy, rollout, and decision log.
- Is updated throughout execution and remains the single source of truth.

## Operating rules (non‑negotiable)
1) **Single‑document rule:** Every architectural discussion is worked out in **one** doc (the canonical architecture document). Do not create multiple planning docs or split phases into separate files. References are allowed, but planning and decisions live in the single canonical doc.
2) **Code is ground truth:** Internal references must point to code paths and runtime behavior. No speculative claims without anchors.
3) **Phase‑gated workflow:** Research → Architecture → Implementation plan → Execution. Pause for user sign‑off between phases.
4) **Explicit invariants:** Call out stop‑the‑line invariants and acceptance tests early.
5) **No parallel solutions:** Avoid competing sources of truth or duplicate patterns.

## Inputs
- Target repo path and change request.
- The architecture template: `docs/arch_skill_raw_notes.md`.
- Access to internal code and external references.

## Execution flow (high level)
- **Phase 1 — Research:** gather internal/external anchors and open questions.
- **Phase 2 — Architecture:** define North Star, current + target architecture, tradeoffs, call‑site audit.
- **Phase 3 — Implementation plan:** phased plan + tests + rollout/telemetry.
- **Phase 4 — Execution:** implement iteratively, update the canonical doc as work progresses.

## UI work requirement
If the architecture touches UI/UX:
- Include **ASCII mockups** for current and target states in the canonical doc.

## Interaction protocol (lightweight)
- Ask for clarification **only** when there are multiple viable options or the request is ambiguous.
- If there’s a single obvious path, proceed without blocking.
- When asking, present 2–4 concrete options and a recommended default.

## Alignment checkpoints (lightweight)
- End of Phase 1: ask if research is sufficient **only** if there are unresolved forks.
- End of Phase 2: ask for sign‑off **only** if target architecture has open tradeoffs.
- End of Phase 3: ask for sign‑off **only** if plan sequencing/rollout is still in question.
- End of Phase 4: ask for confirmation of outcome vs North Star.

## Where to start
- Read: `docs/arch_skill_skill_outline.md`
- Use: `docs/arch_skill_raw_notes.md` as the canonical architecture doc template.
