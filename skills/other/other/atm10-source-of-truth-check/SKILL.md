---
name: atm10-source-of-truth-check
scope: project
status: scaffold
summary: Thin atm10 overlay for clarifying repo-local document authority, canonical files, and review posture without changing the base workflow.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-PENDING-SOURCE-OF-TRUTH-CHECK
  - AOA-T-0002
---

# atm10-source-of-truth-check

## Intent

Use this skill to adapt `aoa-source-of-truth-check` to an `atm10-*` repository when the base workflow is right but the local doc map needs repo-relative detail.

## Trigger boundary

Use this skill when:
- the base `aoa-source-of-truth-check` workflow is already correct, but an `atm10-*` repo needs local canonical-file patterns, repo-relative docs, or doc review rules
- contributors need a thin overlay that maps repo-relative docs such as `README.md`, `docs/ARCHITECTURE.md`, or `docs/[canonical-guide].md`
- confusion exists between overview docs and authoritative files inside one local repo

Do not use this skill when:
- the main need is broader policy design rather than local document authority mapping
- the task is purely code-local and has no meaningful docs or guidance ambiguity
- the work would introduce new upstream technique meaning instead of thin local adaptation
- the main need is recording rationale for a decision rather than clarifying authority; use `aoa-adr-write`

## Inputs

- repo-relative docs or guidance surfaces
- local canonical-file candidates
- local review rules for doc changes
- contributor confusion points
- base skill reference

## Outputs

- local source-of-truth map
- bounded clarification note
- repo-relative canonical-file pattern
- verification summary for the local docs surface

## Procedure

1. start from `aoa-source-of-truth-check` instead of inventing a family-specific docs doctrine
2. name the repo-relative docs and guidance files involved in the ambiguity
3. map which file should stay authoritative for each local concern
4. keep the adaptation bounded to the local repo surface under review
5. make explicit what still depends on downstream human review or unpublished local policy

## Contracts

- preserve the base skill meaning
- keep local file maps repo-relative and explicit
- surface local authority and review posture without hiding it
- keep the overlay public-safe and reviewable

## Risks and anti-patterns

- inventing a broader docs governance framework inside a thin overlay
- using family labels without reducing local ambiguity
- hiding local review rules in prose that looks canonical
- silently replacing the base skill with project doctrine

## Verification

- confirm the base skill is still the right workflow
- confirm authoritative repo-relative files are named explicitly
- confirm local review posture is visible rather than implied
- confirm the adaptation reduces ambiguity without widening scope

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-SOURCE-OF-TRUTH-CHECK from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `ea49abf4f7e96506feed56eb87a9052cbe4408a5` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- local doc hierarchies
- repo-relative canonical-file patterns
- local review rules for doc changes
- repository-specific authority examples
