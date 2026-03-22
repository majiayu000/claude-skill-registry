---
name: aoa-source-of-truth-check
scope: core
status: evaluated
summary: Check whether repository guidance, canonical docs, and operational instructions have clear ownership and do not silently conflict.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-PENDING-SOURCE-OF-TRUTH-CHECK
  - AOA-T-0002
---

# aoa-source-of-truth-check

## Intent

Use this skill to clarify which files are authoritative for status, architecture, run instructions, policy, and change guidance.

## Trigger boundary

Use this skill when:
- a repository has several docs that may overlap or conflict
- contributors may not know which file to trust first
- a change touches docs, process, or operational guidance and the question is which file is authoritative
- confusion exists between overview docs and authoritative docs
- one authoritative source must stay aligned across multiple downstream consumer surfaces

Do not use this skill when:
- the repository is tiny and has no meaningful source-of-truth ambiguity
- the task is purely code-local with no documentation or policy impact
- the authoritative files are already clear and the main need is recording rationale for a decision; use `aoa-adr-write`
- the main problem is deciding whether logic belongs in the core or at the edge; use `aoa-core-logic-boundary` first
- the main problem is broader policy design rather than document authority or ownership

## Inputs

- repository docs surface
- target area of ambiguity or overlap
- known canonical files if any
- current contributor confusion points

## Outputs

- clearer source-of-truth map
- fan-out map when one source feeds multiple downstream consumers
- note of overlaps or conflicts
- proposed or implemented document role clarification
- verification summary

## Procedure

1. identify the main docs or guidance files involved in the target area
2. determine which file should be authoritative for each concern
3. note any overlap, contradiction, or role ambiguity
4. if one source feeds multiple consumers, name each consumer and refresh them from the same source
5. clarify or propose clarifying document ownership and purpose
6. keep the change bounded to the guidance surface under review
7. verify that the result reduces ambiguity for future changes

## Contracts

- authoritative sources should be visible and named explicitly
- overview documents should not silently replace canonical ones
- role separation should reduce confusion, not create extra ceremony
- the resulting guidance should be understandable to another human or agent

## Risks and anti-patterns

- over-formalizing a tiny docs surface
- creating many labels without reducing ambiguity
- moving truth across files without clearly signaling the change
- letting summaries masquerade as canonical instructions

## Verification

- confirm the main source-of-truth ambiguity was reduced
- confirm authoritative files are named explicitly
- confirm overlaps or conflicts were surfaced rather than hidden
- confirm the result helps future contributors orient faster

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-SOURCE-OF-TRUTH-CHECK from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `ea49abf4f7e96506feed56eb87a9052cbe4408a5` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local doc hierarchies
- preferred canonical-file patterns
- local review rules for doc changes
- repository-specific examples of authoritative surfaces
