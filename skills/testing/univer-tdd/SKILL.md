---
name: univer-tdd
description: "Use when implementing SaC workbook behavior with assertions.ts, Facade Migration Packs, univer sac apply, univer sac verify, or verify-report repair loops."
---

# univer-tdd

`univer-tdd` is SaC adapted TDD: workbook behavior is complete only when assertion contracts prove the changed packs through `univer sac verify`.

It is not generic code TDD. It is source-first workbook behavior development with `plans/`, `migrations/`, `assertions.ts`, and `.sac/runs/<run-id>/verify-report.json`.

## Operating Contract

- Use `univer-plan` first for complex workbook behavior.
- Treat `assertions.ts` as the workbook-visible contract for each non-trivial changed pack.
- Allow bounded bootstrap or readonly probes when needed, but never use them as final completion evidence.
- Do not claim completion from `univer sac apply` success.
- Do not claim completion from a zero-assertion, all-skipped, or unchecked changed pack verify run.

## Assertion Coverage

Derive assertions from user intent, baseline evidence, range roles, and final-layout reasoning. Do not derive them from whatever the migration happened to write.

Assertions should cover:

- workbook-visible final state: sheets, used ranges, headers, representative values, formulas, and computed values
- range role preservation: source data, helper/control input, lookup/reference, example/demo, existing output, and preserve-only ranges
- boundary and negative constraints: no extra headings, no helper sheets, cleared tails, no unintended overwrite, no unwanted formatting changes
- workbook-behavior contract decisions: one assertion for each non-obvious output shape, sort/group/mapping, value/formula semantic, formatting/presentation, interaction/validation/protection, preservation, or negative constraint decision
- formula behavior: representative calculated values in addition to formula strings
- meaningful cases: first, middle, last, blank, zero, date-boundary, text-boundary, and grouping-boundary rows when relevant
- exact value semantics: casing, whitespace, abbreviations, blank-versus-zero, text-versus-number, and display-critical stored values

Keep assertions small and deterministic. Prefer representative ranges over broad workbook snapshots.

Assertions must verify behavior decisions, not just the values the migration happened to write.

For each high-risk decision recorded in the plan's Contract Decision Evidence table, add at least one assertion or readonly probe that distinguishes the chosen rule from a plausible wrong rule. Examples include:

- sort/group/truncation decisions: verify first, middle, last, and the first excluded candidate when output capacity is limited
- mapping decisions: verify representative source-to-target coordinates, including one row for each side of a category, sign, blank/zero, or boundary mapping when relevant
- text decisions: verify exact casing, whitespace, abbreviations, and stored value type
- structural decisions: verify section headers, segment boundaries, and first/last row after the final layout is determined

A passed assertion that only mirrors the migration output is not enough when the underlying semantic decision was ambiguous.

Assertions cannot turn an underdetermined assumption into workbook-proven truth. When the plan marks a decision as `underdetermined assumption`, assertions should verify that the implementation consistently applies the declared assumption, and the final handoff should preserve that uncertainty instead of presenting it as decisive workbook evidence.

## Feedback Loop

After editing source or assertions:

1. Run `univer sac apply <workspace>` when the relevant migration is not yet applied.
2. Run `univer sac verify <workspace> --json`.
3. Read the JSON summary and `.sac/runs/<run-id>/verify-report.json`.
4. If status is `failed`, inspect pack id, assertion kind, target, expected value, actual value, and first difference when present.
5. Decide whether the migration source or assertion expectation is wrong before changing either.
6. Run apply or verify again after the repair.
7. If status is `error`, fix setup, config, missing target, source validation, bundling, or runtime setup before judging workbook behavior.

Readonly probes such as inspect, pipe out, or readonly runtime commands may help debug failures. Convert useful probe findings back into the plan, migration source, or assertions, then return to `univer sac verify`.

## Passing Gate

For non-trivial SaC TDD handoff:

- the latest relevant `univer sac verify <workspace> --json` status must be `passed`
- every pack created or modified for the task must be checked unless explicitly assertion-free
- each changed pack must have at least one passed assertion
- skipped packs must be mentioned when relevant
- zero-assertion and all-skipped runs are not completion signals

## Final Handoff

The final handoff must include:

- migration plan outcome and pack sequence
- verification command
- final status
- `verify-report.json` path
- changed pack assertion evidence
- skipped packs, if relevant
- auxiliary probes used, if any, and why they were not completion evidence
