---
name: lighting-report-extract
description: "Check reported lighting quantities and results in supplied simulation PDFs without adding repeated calculation surfaces. Use for scoped luminaire inventories and illuminance results; not simulation or compliance."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# /as:lighting-report-extract — Extract reported lighting results

Before acting, read the [host contract](../../docs/host-harness-contract.md) and
[declaration](host-contract.json) (`skill:lighting-report-extract`), using its profiles from the
[catalog](../../corpus/host-contracts.json). Host access must be demonstrated, not inferred.

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and available native tools or ordinary task-specific code. Operation names identify semantic procedures, not installed functions. No Arch Studio runner, package installation or executable reconstruction is required. Existing exact authorization persists; ask only for material missing information or permission.

Input: supplied report PDF(s), requested rooms/surfaces, metrics and inventory scope. Output: separately
sourced inventory observations and calculation results with a coverage ledger. No simulation, design adequacy determination or regulatory target is
produced. One-off extraction requires no studio initialization or schedule adoption.

1. Read exact source bytes through the host; retain hash/revision. Read owning project instructions
   when applicable. If access is missing, request an exposed native grant or give the precise handoff.
2. Read [PDF evidence contracts](../../tools/transformers/evidence-contracts.md). Inventory every
   physical page separately from printed labels. Search actual text and inspect table images using
   host PDF/OCR capabilities. A TOC referring beyond the physical page count can reflect an excerpt
   with original pagination; it does not prove that results are absent. Check summary and individual
   calculation-surface tables before marking a requested metric unavailable.
3. Extract exact room/surface name, metric label, value, unit, calculation condition/height where
   reported, document hash, physical page, printed page and table/region locator. Keep average,
   minimum, uniformity, glare and daylight metrics distinct. Preserve reported decimal notation and
   unknown units; no target values or compliance conclusions may be supplied from memory.
4. Keep the report's room/surface labels. A mezzanine is not a named laboratory without explicit
   mapping evidence. Separate multiple surfaces and scenarios; never select the most favorable value
   or merge them silently. Inspect requested values against rendered tables and retain conflicts.
5. When quantities are requested, read the [lighting observation contract](../../tools/transformers/evidence-contracts.md#lighting-inventory-and-calculation-results)
   and [schema](../../schema/lighting-report.schema.json). A room's luminaire inventory repeated under
   two calculation surfaces is one inventory, not two additive counts. Establish inventory identity
   from the report's room/list/scope evidence; matching quantities or labels alone cannot establish it.
   Keep room, scene, variant and source version separate; unknown identity remains unresolved. A report
   without a scene label uses `not-reported`, never an invented scenario. Apply `lighting_report.build`
   to the explicitly prepared observations using native computation and the complete grouping rules.
   The normalized result describes supplied identities; it does not establish source verification.
6. Return extracted metrics plus per-request status: observed, unresolved association, unparsed or
   not located after inspection. Preserve inspected page coverage and OCR limitations. Only claim
   absence within the supplied and inspected pages, not the full originating report. Save requested
   derived outputs and read them back; do not edit simulation files or adopted schedules. Luminaire
   product specifications belong to `/as:product-spec-pdf-parser`; plan counts to
   `/as:drawing-quantity-extract`. Compliance assessment is outside this skill's scope.
   Requested quantity comparison goes to `/as:schedule-quantity-reconcile` with all locators and
   unresolved/conflicting groups retained; extraction does not authorize schedule adoption.

## Current document placement

Save only authorized derived outputs and verify their actual content, source hashes and complete requested scope. Inline answers and one-off files need no project setup or adoption. For a requested registered project report, resolve confirmed coordinates using the receive-owned native `documents.resolve/register` semantics in the [workspace model](../../docs/workspace-model.md), including its complete document/register mutation sequence. Find existing records with `documents.query`; never guess a folder. This conditional handoff does not authorize schedule or library changes.
