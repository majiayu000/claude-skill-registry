---
name: aoa-adr-write
scope: core
status: evaluated
summary: Record a meaningful architectural or workflow decision so future changes can understand the rationale rather than only the outcome.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-PENDING-ADR-WRITE
---

# aoa-adr-write

## Intent

Use this skill to capture an architectural, structural, or workflow decision in a concise reviewable note that preserves rationale and tradeoffs.

## Trigger boundary

Use this skill when:
- a decision changes structure, boundaries, tooling, or workflow expectations
- future contributors will need to know why a path was chosen
- several plausible options existed and the reasoning matters
- the team or project risks repeating the same debate later

Do not use this skill when:
- the change is tiny and self-evident
- the note would only restate an obvious diff with no real decision content
- the main problem is unclear authoritative documentation rather than decision rationale; use `aoa-source-of-truth-check` first
- the main problem is deciding whether logic belongs in the core or at the edge; use `aoa-core-logic-boundary` first

## Inputs

- decision to record
- context and problem statement
- relevant options or alternatives
- chosen path and rationale
- known consequences or tradeoffs

## Outputs

- concise decision note or ADR draft
- statement of rationale
- consequence notes
- verification that the note matches the actual change

## Procedure

1. state the context and the problem the decision addresses
2. list the main options if they meaningfully shaped the choice
3. record the chosen decision in clear language
4. note why it was chosen and what tradeoffs it introduces
5. connect the note to the actual change surface when relevant
6. verify that the note explains the decision rather than narrating the diff only

## Contracts

- the note should explain why, not just what changed
- the decision should be bounded and understandable
- tradeoffs should not be hidden behind certainty theater
- the note should help future reviewers, not merely satisfy process

## Risks and anti-patterns

- writing an ADR for a trivial edit with no real decision
- using inflated language to mask weak reasoning
- recording the chosen path without naming consequences
- letting the ADR drift away from the actual change

## Verification

- confirm the decision was meaningful enough to record
- confirm the rationale is explicit
- confirm consequences or tradeoffs are named
- confirm the note aligns with the real change surface

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-ADR-WRITE from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local ADR templates
- local placement rules
- architecture review expectations
- repository-specific examples
