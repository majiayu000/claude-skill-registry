---
name: aoa-core-logic-boundary
scope: core
status: evaluated
summary: Clarify which logic belongs in the reusable core and which parts should remain glue, orchestration, or infrastructure detail.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-PENDING-CORE-LOGIC-BOUNDARY
---

# aoa-core-logic-boundary

## Intent

Use this skill to separate reusable core logic from surrounding glue, orchestration, or infrastructure detail so future changes land in the right place.

## Trigger boundary

Use this skill when:
- a module mixes stable rules with wiring or execution detail
- the same logic is starting to appear in several places
- tests or reviews are muddy because the center of responsibility is unclear
- you need to decide whether something belongs in the core or at the edges

Do not use this skill when:
- the task is a tiny isolated fix with no meaningful boundary ambiguity
- the code is already clearly partitioned
- the result would only rename folders without improving understanding
- the main problem is recording decision rationale rather than boundary placement; use `aoa-adr-write` first
- the boundary is already clear and the main task is introducing a port or adapter around a concrete dependency; use `aoa-port-adapter-refactor`

## Inputs

- target module, service, or slice
- current responsibilities
- repeated or reusable logic candidates
- surrounding glue or orchestration context

## Outputs

- clarified boundary between core logic and surrounding glue
- notes on what should stay reusable versus edge-specific
- small refactor proposal or bounded implementation
- verification summary

## Procedure

1. identify which rules or behaviors are stable enough to count as reusable core logic
2. identify which parts are mostly wiring, orchestration, I/O, or environment detail
3. separate the concerns conceptually before moving code
4. move or propose moving only the bounded subset that clearly belongs in the core
5. avoid renaming or restructuring for ceremony alone
6. verify that the new boundary improves changeability and review clarity

## Contracts

- reusable logic should not stay trapped in glue if that blocks testing or reuse
- glue should not be over-promoted into domain logic without reason
- the boundary should improve clarity, not just aesthetics
- the change should remain reviewable and bounded

## Risks and anti-patterns

- treating all logic as core logic and over-abstracting the system
- moving orchestration detail into the core under the label of purity
- renaming layers without reducing actual confusion
- hiding a broad rewrite inside a boundary-cleanup task

## Verification

- confirm the core candidate is genuinely reusable or stability-shaped
- confirm edge-specific code remains at the edge when appropriate
- confirm the refactor improved clarity for future changes
- confirm no unrelated structural churn was introduced

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-CORE-LOGIC-BOUNDARY from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local layering conventions
- preferred directories or module boundaries
- repository-specific examples of core versus glue
- local verification commands
