---
name: mcaf-adr-writing
description: "Create or update an ADR (Architecture Decision Record) under `docs/ADR/` using `docs/templates/ADR-Template.md`: context, decision, alternatives, consequences, rollout, and verification. Use when changing architecture, boundaries, dependencies, data model, or cross-cutting patterns; ensure it is self-contained, has a Mermaid diagram, and defines testable invariants."
compatibility: "Requires repository write access; produces Markdown docs with Mermaid diagrams."
---

# MCAF: ADR Writing

## Outputs

- `docs/ADR/ADR-XXXX-<short-title>.md` (create or update)
- Update `docs/Architecture/Overview.md` when boundaries/interactions change

## Decision Quality (anti-guesswork checklist)

Before writing, make the ADR executable (no placeholders, no hand-waving):

- **Decision**: one sentence. If you can’t write it, you don’t have a decision yet.
- **Scope**: what changes / what does not + which module(s) are affected (match `docs/Architecture/Overview.md` names).
- **No invented reality**: every component you mention exists in the repo today, or is explicitly part of this change (named + where it will live).
- **Invariants**: write as **MUST / MUST NOT** statements and say how we prove each (test or static analysis).
- **Verification**: use exact commands from `AGENTS.md` and link scenarios → test IDs.
- **Stakeholders**: Product / Dev / DevOps / QA — what each role must know to execute safely.

## Workflow

1. Confirm the decision scope:
   - what changes (and what does not)
   - what module(s) are affected
   - follow `AGENTS.md` scoping rules: Architecture map → linked ADR/Feature → entry points (do not scan everything)
2. Start from `docs/templates/ADR-Template.md`.
   - keep the ADR’s `## Implementation plan (step-by-step)` updated while executing
3. Write the ADR as a decision record:
   - **Context**: constraints + why this is needed now
   - **Decision**: a short, direct statement
   - **Diagram** (mandatory): include at least one Mermaid diagram for the decision (boundaries/modules/interactions)
   - **Alternatives**: 1–3 realistic options with pros/cons
   - **Consequences**: trade-offs, risks, mitigations
4. Make it executable for the team:
   - follow `AGENTS.md` Task Delivery rules (analysis → plan → execute → verify)
   - include the invariants that must be proven by tests
   - include verification commands copied from `AGENTS.md`
   - include rollout/rollback and “how we know it’s safe”
5. Make impacts explicit:
   - code/modules affected
   - data/config changes (including migration/rollback)
   - backwards compatibility strategy
6. Add verification that proves the decision:
   - which tests must exist/change
   - which suites must stay green
7. If the decision changes boundaries, update `docs/Architecture/Overview.md` (diagram, modules table, dependency rules).

## Guardrails

- ADRs are self-contained: no hidden context, no “as discussed”.
- ADRs justify *why*; feature docs describe *what the system does*.
- If you can’t state the decision in 1–2 sentences, the ADR is not ready.
