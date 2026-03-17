---
name: mcaf-feature-spec
description: "Create or update a feature spec under `docs/Features/` using `docs/templates/Feature-Template.md`: business rules, user flows, system behaviour, Mermaid diagram(s), verification plan, and Definition of Done. Use before implementing a non-trivial feature or when behaviour changes; keep the spec executable (test flows + traceability to tests)."
compatibility: "Requires repository write access; produces Markdown docs with Mermaid diagrams and executable verification steps."
---

# MCAF: Feature Spec

## Outputs

- `docs/Features/<feature>.md` (create or update)
- Update links from/to ADRs and architecture map when needed

## Spec Quality (anti-guesswork checklist)

Write a spec that can be implemented and verified **without guessing**:

- **No placeholders**: avoid “TBD”, “later”, “etc.”; if something is unknown, list it as an explicit question.
- **Concrete modules**: use real module/boundary names from `docs/Architecture/Overview.md`.
- **Rules are testable**: numbered business rules with clear inputs → outputs (no vague adjectives).
- **Flows are executable**: scenarios include preconditions, steps, expected results (happy + negative + edge).
- **Verification is real**: commands copied from `AGENTS.md`, and scenarios mapped to test IDs.
- **Stakeholders covered**: Product / Dev / DevOps / QA each get the information they need to ship safely.

## Workflow

1. Start from `docs/Architecture/Overview.md` to pick the affected module(s).
2. Create/update the feature doc using `docs/templates/Feature-Template.md`.
   - follow `AGENTS.md` scoping rules (do not scan the whole repo; use the architecture map to stay focused)
   - keep the feature’s `## Implementation plan (step-by-step)` updated while executing
3. Define behaviour precisely:
   - purpose and scope (in/out)
   - business rules (numbered, testable)
   - primary flow + edge cases
4. Describe system behaviour in terms of **entry points, reads/writes, side effects, idempotency, and errors**.
5. Add a Mermaid diagram for the main flow (modules + interactions; keep it readable).
6. Write verification that can be executed:
   - test environment assumptions
   - concrete test flows (positive/negative/edge)
   - mapping to where tests live (or will live)
   - traceability: rules/flows → test IDs (so tests reflect the spec)
7. Keep Definition of Done strict:
   - behaviour covered by automated tests
   - static analysis clean
   - docs updated (feature + ADR + architecture overview if boundaries changed)

## Guardrails

- If the feature introduces a new dependency/boundary, write an ADR and update `docs/Architecture/Overview.md`.
- Don’t hide decisions inside the feature doc: decisions go to ADRs.
