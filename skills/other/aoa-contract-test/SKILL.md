---
name: aoa-contract-test
scope: core
status: canonical
summary: Design or extend contract-oriented validation at module, service, or workflow boundaries.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0003
  - AOA-T-0015
---

# aoa-contract-test

## Intent

Strengthen boundary reliability by making expected inputs, outputs, and validation summaries explicit.

## Trigger boundary

Use this skill when:
- two modules or services interact across a meaningful boundary
- a smoke path or interface needs a stable validation contract
- a change risks breaking downstream assumptions

Do not use this skill when:
- the change is entirely local and does not affect a meaningful boundary
- the boundary itself is still semantically unclear and naming is drifting; use `aoa-bounded-context-map`
- the main problem is expressing a broad invariant rather than a boundary contract; use `aoa-property-invariants`
- the main problem is auditing whether existing checks really cover a stable rule; use `aoa-invariant-coverage-audit`
- a broad system rewrite is needed before the boundary itself is stable

## Inputs

- boundary under review
- expected inputs and outputs
- current verification surface
- known downstream dependencies

## Outputs

- explicit contract assumptions
- tests or smoke summary changes
- verification notes
- downstream impact notes

## Procedure

1. identify the boundary and its consumers
2. state the expected input/output behavior
3. express the contract in tests, smoke summaries, or structured checks
4. verify both the boundary behavior and the reporting shape
5. report what became explicit and what remains weak

## Contracts

- the contract should be visible to another human or agent
- verification should be tied to the boundary, not only to internals
- downstream assumptions should be named when relevant

## Risks and anti-patterns

- vague contracts that do not actually constrain behavior
- treating a smoke summary as proof when it does not cover the real boundary
- changing interface behavior without downstream impact notes

## Verification

- confirm the contract is visible and reviewable
- confirm validation is tied to the interface or boundary
- confirm downstream impact was considered when relevant

## Technique traceability

Manifest-backed techniques:
- AOA-T-0003 from `8Dionysus/aoa-techniques` at `fe7df9aba3937435b431489ed0f9c5d52690a37c` using path `techniques/evaluation/contract-first-smoke-summary/TECHNIQUE.md` and sections: Intent, When to use, Outputs, Contracts, Validation
- AOA-T-0015 from `8Dionysus/aoa-techniques` at `fe7df9aba3937435b431489ed0f9c5d52690a37c` using path `techniques/evaluation/contract-test-design/TECHNIQUE.md` and sections: Intent, Inputs, Core procedure, Risks

## Adaptation points

Project overlays should add:
- local endpoints or module boundaries
- local smoke or test commands
- boundary-specific invariants
