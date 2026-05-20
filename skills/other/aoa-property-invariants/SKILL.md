---
name: aoa-property-invariants
scope: core
status: canonical
summary: Express stable system or domain truths as invariant-oriented tests and checks rather than only enumerating examples.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0017
  - AOA-T-0007
---

# aoa-property-invariants

## Intent

Use invariant-oriented thinking to test broad behavior through properties rather than only through a short list of fixed examples.

## Trigger boundary

Use this skill when:
- a rule should hold across many inputs or states
- examples alone feel too narrow
- the system has conservation, monotonicity, idempotency, or structural invariants
- safety or correctness depends on broad input coverage

Do not use this skill when:
- the behavior is mostly about presentation details or narrow snapshots
- the main problem is checking whether existing checks really cover the invariant; use `aoa-invariant-coverage-audit` first
- the main problem is a boundary contract rather than a stable invariant; use `aoa-contract-test`
- no meaningful invariant is yet understood

## Inputs

- target rule or domain truth
- current examples or tests
- input space or generators
- known edge cases

## Outputs

- explicit invariants
- property-oriented tests or checks
- notes on generator assumptions
- verification summary

## Procedure

1. identify what must remain true across many cases
2. separate strong invariants from weak hopes or vague expectations
3. express those invariants as property-oriented tests or repeated checks
4. keep the generators or inputs bounded and reviewable
5. run the checks and report what properties now constrain behavior

## Contracts

- each property should express a real invariant, not a wish
- the test should broaden coverage beyond a small handpicked set
- generator assumptions should remain understandable

## Risks and anti-patterns

- writing weak properties that prove almost nothing
- confusing random data with meaningful coverage
- using property checks where a small set of concrete examples would be clearer
- hiding domain confusion behind fancy generator logic

## Verification

- confirm the property expresses a meaningful invariant
- confirm the invariant broadens coverage beyond fixed examples
- confirm the result is understandable to another human or agent

## Technique traceability

Manifest-backed techniques:
- AOA-T-0017 from `8Dionysus/aoa-techniques` at `fe7df9aba3937435b431489ed0f9c5d52690a37c` using path `techniques/evaluation/property-invariants/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0007 from `8Dionysus/aoa-techniques` at `fe7df9aba3937435b431489ed0f9c5d52690a37c` using path `techniques/evaluation/signal-first-gate-promotion/TECHNIQUE.md` and sections: summary, Validation

## Adaptation points

Project overlays should add:
- local generator tools
- domain-specific invariants
- rules for when property-based checks are mandatory, optional, or out of scope
