---
name: product-audit
description: "Audit a product, selection or FF&E schedule against sourced evidence and flag discrepancies, unknowns and stale specifications. Use to check product data; not to repair records, certify compliance or generate cut sheets."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebFetch
  - WebSearch
---

# /as:product-audit — Audit a product selection

Before acting, read the [host contract](../../docs/host-harness-contract.md) and this component's [declaration](host-contract.json) (`skill:product-audit`). Load only its referenced mode profiles from the [shared catalog](../../corpus/host-contracts.json). Compose modes required by the actual task; declarations are requirements, not proof of access or permission.

<!-- architecture-studio:harness-compatibility -->
> Host adapter: read [delivery-specific guidance](../../docs/host-adapters.md) for invocation, questions, target access and optional delegation.

## Input and authority

For source-independent captured evidence, use the [shared product-observation adapter](../../schema/product-observations.md) with explicit item/revision bindings. Include its conflicts and notices alongside the legacy audit projection; never discard identity, variant, unit, currency, or price-basis uncertainty when reporting findings.

Accept one item, selected tags, or a complete schedule. For project records, resolve exact native [project context](../project/references/context-resolution.md) and read its instructions. A missing/ambiguous boundary is not permission to create a project. One-off comparison uses an explicitly supplied snapshot without adoption. Read the complete [native audit owner](../../tools/validators/ffe-audit-contract.md) and [input schema](../../schema/ffe-audit.schema.json).

For adopted schedules, use `/as:master-schedule` to read the pinned item/schedule revisions. Item IDs are immutable; tags and workbook rows are only locators. An old workbook or optional `product-library.csv` does not override current records. One-off library comparisons retain the exact header and [CSV conventions](../../schema/csv-conventions.md).

## Steps

1. Establish the requested scope, revision, source basis and **live** versus **snapshot** mode. Default a request to check current product facts to live retrieval. No routine second confirmation is needed for a read-only comparison.
2. **Live audit always retrieves/re-parses the relevant sources in this invocation.** Use the host browser/PDF capabilities; do not present cached catalog data as freshly verified. Record source/page or field locator and observed-at time. If access fails, keep `unavailable`; do not downgrade to snapshot comparison silently. Snapshot mode explicitly compares saved observations and cannot establish current facts.
3. Separate manufacturer/dealer, selected versus available configuration, actual model/accessory and installed/cutout dimensions. Preserve unknown prices/currency, evidence conflicts and user overrides. A variant combination is not a manufacturer-confirmed SKU without source evidence.
4. Build the complete typed input and apply `ffe_audit.assess` through available native capabilities under its owning semantics. It compares supplied observations only, performs no retrieval and cannot authenticate the host's evidence. Preserve strict number kinds, ASCII-escaped logical input hash, full findings order and exact comparison counts. Missing validation capability is a limitation, not a successful check.
5. Present discrepancies, missing evidence, stale observations and conflicting sources, tied to immutable item/revision and field. Exact value comparisons do not convert units: resolve dimensional meaning and units before constructing comparable observations. Missing evidence is unknown, not proof that the specification is wrong.
6. When a durable report is requested/authorized, preview the exact collision-safe target under `ffe/jobs/<job-id>/audits/`, then save the report and source references. Use one confirmation gate only if required and not already authorized. Refuse overwrite; preserve previous reports. Do not persist machine-absolute paths in records. Report the actual file created.

## Output and handoff

The schema/result includes input hash, item IDs/revisions, source locators, findings and comparison mode. `matches-supplied-observations` means only that the supplied values match; it is not product certification or legal compliance.

Audit does not mutate item/schedule specifications, decisions, recovery snapshots or the optional library. Propose corrections to `/as:master-schedule`; sourcing goes to `/as:product-research`, PDF/URL extraction to their existing skills. Selection rationale and approval go through `/as:project`; never infer them from an artifact or audit result. After resolved findings, `/as:product-cut-sheet` and `/as:spec-book` consume the exact selected revisions. Cross-skill handoff does not require a subagent or separate Norma runtime.

## Native report publication and handoff

Apply the [native mutation sequence](../../docs/workspace-model.md#native-mutation-sequence) to the complete report set: original snapshot/source evidence and identity/revision guards, output absence, full prepared report and recoverable pending intent. Finish durable saves and independently reopen **all** actual original/prepared bytes and access metadata before first publication. Use no-clobber publication, preserve older reports and all source records, and reopen every actual output's full bytes and mode/applicable ownership/ACLs before completion. A correct hash or creation-mode argument alone is not readback. Exact retry verifies the prior result without duplicate allocation; changed or uncertain state needs reconciliation.

A registered deliverable goes through receive's native document owner for exact placement/query/registration; do not compose document folders from labels. One-off reports use only the authorized task destination. Keep source data separate from execution authority and preserve user-selected scope. Existing exact authorization persists, so request only missing material scope or host permission. Any unavailable protection or failed result verification remains explicitly blocked/pending with recovery evidence.

Operation IDs are semantic responsibilities, not a dispatch API to recreate. No Arch Studio runtime, installer or source handoff is required. Separate actual host retrieval, assessment, report publication and owner handoffs in the final evidence; instructions delivered or a validator receipt alone cannot establish completion.

## Native workbook preservation comparison

When an explicitly selected before/after native `.xlsx` or `.xlsm` pair and permitted cell edits are
available, load the complete [workbook comparison owner](../../tools/validators/workbook-preservation-contract.md)
and perform native `workbook_preservation.compare` with actual ZIP/XML inspection. Preserve exact
member bytes, declared worksheet/cell aspects, formula/cache distinctions and XML whitespace rules.
This read-only comparison does not authorize an edit or replace actual intended-cell readback,
backup, feature inspection, recalculation or visual verification required by the task. Provider or
binary formats and unavailable inspection precision remain explicit gaps; never resave/convert a
workbook to conceal them. No Arch Studio helper or process runtime is mandatory.
