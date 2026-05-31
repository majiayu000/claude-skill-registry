---
name: univer-plan
description: "Use when planning complex SaC workbook behavior, Facade Migration Packs, workbook range roles, migration boundaries, or assertion gates before implementation."
---

# univer-plan

Plan complex SaC workbook behavior before editing migration source. The plan is a source-first authoring artifact, not chat-only notes.

## Output Location

Write or update a plan file under the SaC workspace:

```text
<workspace>/plans/<topic>.md
```

Use an existing project naming convention if one exists. Keep the plan close to `migrations/` and `assertions.ts` so future agents can understand the workbook behavior from source.

## Required Plan Shape

```md
## Workbook Intent

- User-visible outcome:
- Explicit non-goals:

## Baseline Evidence

- Source already read:
- Readonly probes:
- Unknowns:

## Range Roles

- Source data:
- Target output:
- Helper/control input:
- Lookup/reference:
- Example/demo:
- Existing output:
- Preserve-only:

## Workbook Behavior Contract

- Visible target/state:
- Source/input dependency:
- Shape/layout boundary:
- Ordering/grouping/mapping policy:
- Value/formula semantics:
- Formatting/presentation semantics:
- Interaction/validation/protection behavior:
- Preservation and negative constraints:
- Example/demo/answer-range handling:

## Contract Decision Evidence

| Decision | Candidate interpretations | Evidence read | Evidence strength | Chosen rule | Assertions/probes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Migration Packs

1. `<pack-id>`: durable workbook intent
   - reads:
   - writes:
   - must preserve:
   - rollback/verify boundary:
   - assertion gate:

## TDD Gates

- Assertions to write or update first:
- Allowed bootstrap/probe:
- Completion verify command:
```

## Range Role Rules

For every relevant range role, say whether the migration may read it, write it, replace it, or must preserve it.

Range roles include source data, target output, helper/control input, lookup/reference, example/demo, existing output, and preserve-only areas.

Source data, helper/control input, lookup/reference, example/demo, existing output, and preserve-only ranges are not target output unless the user explicitly says to change them. If an example/demo range is used to infer a formula, layout, or behavior, capture that reasoning in the plan and add assertion gates that distinguish the real target output from the example.

Answer ranges and output ranges are constraints and evidence windows. They do not prove that the top-left cell is the output start or that the range contains the full contract.

## Workbook Behavior Contract Rules

For complex workbook behavior, fill the relevant Workbook Behavior Contract fields before editing migration source. The contract should turn ambiguous workbook-visible behavior into explicit plan choices that assertions can verify.

Output-heavy transformations should capture shape, mapping, ordering, and value/formula semantics. Formatting, validation, protection, chart, comment, layout, or sheet-structure changes should capture visible state, presentation or interaction semantics, preservation rules, and negative constraints.

## Contract Decision Evidence Rules

For every high-risk or non-obvious workbook behavior decision, record evidence before editing migration source.

High-risk decisions include ordering precedence, grouping and truncation order, source-to-target mapping, sign-to-column mapping, blank-versus-zero policy, text casing or whitespace preservation, header or section-boundary handling, formula-versus-static-value strategy, and any behavior where the instruction can reasonably be read in more than one way.

- Do not write `Unknowns: none` when a decision depends on domain intuition, ambiguous wording, partial preview data, or an unverified sample/reference pattern.
- If multiple interpretations are plausible, list the rejected interpretations and why they lost.
- If the chosen rule is based on workbook-visible evidence, name the source range or cells.
- If the chosen rule is based only on instruction wording, quote the deciding phrase in the plan.
- If no decisive evidence exists, mark the decision as an assumption and choose the rule that best satisfies the final target/output wording.
- Each high-risk decision must have at least one assertion or readonly probe that would fail if the opposite interpretation were used.

## Evidence Sufficiency Rules

High-risk decisions need discriminating evidence, not only compatible evidence.

Evidence is discriminating only when it makes at least one plausible interpretation unlikely. Evidence that can fit both the chosen rule and a rejected rule is compatible evidence, not proof.

Separate observed workbook facts from semantic labels. A source value changing a balance can prove source sign behavior, but it does not by itself prove which target label should receive that sign. A section boundary can prove where data changes shape, but it does not by itself prove whether headers should be copied, skipped, or rewritten.

Do not treat domain intuition, adjacent-row arithmetic, source-side patterns, or conventional business meanings as decisive target-mapping evidence unless they directly connect to workbook-visible target labels, examples, instruction wording, or existing output.

Use the `Evidence strength` field to mark each high-risk decision as one of:

- `explicit`: directly specified by the instruction or an existing workbook-visible target/example
- `inferred`: supported by discriminating workbook-visible evidence
- `underdetermined assumption`: no available evidence rules out another plausible interpretation

For an underdetermined decision:

- In an interactive task, ask the user before editing.
- In a non-interactive task, proceed only when required, choose the best-effort rule that most closely follows the instruction and target layout, and keep the uncertainty visible in the plan and handoff.
- Do not present the assumption as workbook-proven evidence.

## Pack Decomposition

Split by durable workbook intent:

- create or reshape a sheet
- load or normalize a data model
- add a formula family
- generate review or summary output
- add presentation or validation behavior

Do not split by individual cells, individual Facade calls, or incidental implementation steps. A pack is well-sized when it has one clear workbook intent, a reasonable rollback boundary, and its own assertion gate.

## Completion Gate

Do not edit migration source for a complex SaC behavior until the plan identifies:

- workbook-visible intent and non-goals
- range roles and preservation rules
- workbook behavior contract choices for complex behavior
- ordered Migration Packs
- assertion gate for each non-trivial changed pack

If `univer-tdd` verification changes the expected behavior, update the plan in `plans/` before or alongside source/assertion repairs.
