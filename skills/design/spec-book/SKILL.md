---
name: spec-book
description: "Build an ordered specification package with every selected product accounted for, using accepted templates and exact product identities. Use for grouped cut sheets or a combined book; not for implicit scope reduction or adoption."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# /as:spec-book — Assemble a Specification Package

Before acting, read the [host contract](../../docs/host-harness-contract.md) and this component's [declaration](host-contract.json) (`skill:spec-book`). Load only its referenced mode profiles from the [shared catalog](../../corpus/host-contracts.json). Compose modes required by the actual task; declarations are requirements, not proof of access or permission.

<!-- architecture-studio:harness-compatibility -->
> Host adapter: read [delivery-specific guidance](../../docs/host-adapters.md) for invocation, package paths, questions, file access and optional delegation.

Compose `/as:product-cut-sheet`; do not duplicate extraction, research or sheet layout logic. Input: explicit ordered scope, pinned schedule/item revisions or a one-off snapshot, accepted template, grouping and audience. Output: individual/combined artifacts as requested and a derived package preparation manifest and revision receipt owned by this skill. `/as:product-data-import` owns the accepted job input manifest; this skill only consumes it. Item/schedule records remain owned by `/as:master-schedule`; decisions and project facts remain owned by `/as:project`.

## Native preparation and publication

Read the complete [native output owner](../../tools/renderers/ffe-output-contract.md) and
[design resolver](../../tools/renderers/document-design-contract.md), including exact schemas,
identity/versioned filenames, hashes and retry boundaries. Use the actual host's native tooling;
operation names identify semantic work and do not dispatch an Arch Studio executable.

Follow [Inspect → Prepare → Verify preparation → Apply → Verify result → Complete](../../docs/workspace-model.md#native-mutation-sequence).
The whole affected preparation set is the new manifest, projected data and every image asset; guard
full source/template/design/current record pins. For verification, the whole set is the receipt,
its immutable companion evidence and actual artifacts. Finish durable saves and separately reopen
and validate **all full saved originals/prepared bytes and access metadata before the first publisher**.
Inspect pending state before preparing or allocating another revision. Publish complete file bytes
without clobbering prior jobs, then freshly read back every actual destination and dependency,
including access metadata, before completion. Real every-page visual/link/privacy inspection is
required; a hash or supplied flag does not substitute for an inspection.

## 1. Resolve and freeze the package

For project-bound work resolve the valid `PROJECT.md`, read instructions and preserve malformed/unindexed records. Select a registered project only when the requested durable work needs it; never create one implicitly. A one-off package uses the authorized task folder with no studio/project gate. Do not infer context from plugin installation. Preserve originals and use project/task-relative references. No issue/approval state is inferred from artifact generation.

Reuse authorization and supplied corrections. Ask once only if a material choice remains unresolved; combine exact target, scope, template, audience and effects in the single gate. For an adopted schedule, pin the full schedule ID/revision/hash and each selected item ID/revision using the native record owner’s complete current-read procedure. For one-off work, explicitly pin a source snapshot without adoption. Do not let an older workbook, cached scope or historic output package replace a corrected accepted source. Schedule updates, workbook reconciliation and recovery route to their owner.

Build an explicit ordered expected-tag list. Define product-versus-finish grouping through `outputs[].item_ids`; never assume one spreadsheet row equals one sheet. Omissions require recorded user authorization and a revised scope; a missing or failed item is not an authorized omission. Preserve exact tags and isolate filenames by unique `ffe/jobs/<job-id>/<revision>/` folder.

Follow the [shared identity and versioned filename contract](../../tools/renderers/ffe-output-contract.md#encoding-and-exact-identity).
Keep dotted tags unchanged. Use the current filename contract and exact item identifiers; never infer canonical retagging.

### Accepted input handoff and derived projection

Derive the expected denominator from the full accepted input scope, not just successfully parsed
products. Keep all requested categories, including lighting. Maintain one ledger entry per requested
item: verified artifact reference/hash, or unresolved with a precise reason. An unresolved row accounts
for the item but does not complete its sheet. Use `delivery_coverage.assess` from the
[native evidence contracts](../../tools/transformers/evidence-contracts.md) to screen the ledger;
it does not replace actual `ffe_outputs.check` or visual inspection. Report expected, accounted-for,
verified and unresolved counts separately. Never shrink scope to match the files produced. Before returning links, perform native `delivery_coverage.verify-links` with one expected entry per artifact containing current item/revision/source/template hashes, actual artifact and receipt paths, and immutable companion evidence path/raw hash. It reads the linked files and receipts and rejects stale identities, revisions or hashes; a supplied ledger alone does not establish that the returned links are current.

Consume `ffe/jobs/<job-id>/input-manifest.json` from `/as:product-data-import`, using [the intake schema](../../schema/ffe-intake.schema.json). If it is absent, hand off to that owner to record the supplied sources and scope under existing authorization; one-off mode records inputs without adopting a schedule. Verify its `input_hash`, source hashes/status, selected tags, accepted template and adopted `record_basis` when present. Reconcile explicit product/finish grouping with that selection. Corrections produce a superseding input job through the owner, never an output skill's rewrite of the accepted manifest.

Preserve the untouched joined record read (or one-off source extraction) separately. Create a **derived output snapshot**, retaining schedule ID/revision/hash and item ID/revision while selecting only the accepted scope. Put accepted `input_hash`, source references/status, selected tags and the original record source in the snapshot's `source` object; an empty record source is not invented evidence. Record the raw-read hash and explicit field mapping separately in the preparation evidence. The output snapshot is a rendering projection, not a newly signed canonical record.

Map structured values deliberately into the output contract’s scalar render fields. For a stored hyperlink `{label,url}`, retain separate display-label and true-URL fields and explicitly allowlist the intended fields; never replace the URL with its label. Preserve the raw structured value and mapping in private preparation evidence. Other nested values require an explicit lossless source-to-display mapping, not guessed flattening. The host must create and inspect actual PDF link annotations, not merely print URL-looking text. Never mutate adopted records to satisfy a renderer's input schema.

Before verification or resume, reread current canonical data and accepted input evidence, then rebuild the same derived projection and mapping. Compare it with the prepared inputs; changed source/scope/mapping/revisions invalidate affected outputs. Keep all raw evidence and preparation controls outside client delivery.

## 2. Prepare and compose sheets

Resolve the centrally owned [document design system](../../studio/standards/documents/design-system.md) and [cut-sheet template](../../studio/templates/documents/product-cut-sheet/template.md) plus [book template](../../studio/templates/documents/spec-book/template.md). Layout/type rules live there, not in this skill. Use `document_contracts.resolve` from the [native design owner](../../tools/renderers/document-design-contract.md): explicitly selected project/job assets first, configured studio assets next, bundled assets last. A supplied accepted reference takes precedence for its declared rules; record `reference_overrides` and its hash rather than silently replacing it. Missing assets or incompatible dependencies block the affected output.

Resolve the requested physical preset/custom dimensions, portrait/landscape and displayed measurement units separately. Pin design/template IDs, versions, asset hashes, page dimensions, margins, content area and layout version in `resolved-design.json`. Supply that exact parsed resolution to preparation and verification. Re-resolve current dependencies before verification; retain earlier resolved bytes. The host follows size-aware grid/type/overflow rules and inspects every actual page, image resolution and 100% print geometry. Do not scale a Letter layout to a board, substitute a nearby paper size, or imply product images have drawing scale. Unsupported combinations are explicit blockers.


Follow [native output contracts](../../tools/renderers/ffe-output-contract.md). Bind accepted template hash/layout, audience field allowlist, sourced images, expected page counts and whether a combined PDF was requested. Declare `front_matter_pages` when cover/index pages are requested, using the central book template; default is zero. The host verifies final index destinations and page numbering after assembly. Keep client rendering inputs free of internal fields. Private controls, excluded values and source files never enter `delivery/`.

Perform native `ffe_outputs.prepare` once for the exact package snapshot and contract. Invoke `/as:product-cut-sheet` logic for each output using the same pinned inputs and template, writing PDFs under their resolved filenames in the package delivery directory while preserving exact visible tags. Preserve all selected finish/image decisions and distinguish exact/representative/missing imagery. Missing renderer/source/image blocks the affected output unless the approved contract permits a labeled placeholder. Do not claim remote execution from MCP instruction retrieval.

Merge actual PDFs in the explicit expected order using host PDF tooling when combined output is requested. Preserve links and readable text. Reopen the merged output and inspect every page. Never rename HTML to PDF or return links as proof that a batch finished.

## 3. Resume and invalidate deliberately

On interruption, inspect retained pending state first and preserve manifests, failures and individual evidence. Finish the exact retained preparation only when its intent/pins still match. Otherwise prepare a new revision from current source/template/audience/image inputs and perform native `ffe_outputs.resume` using the complete output owner.

The read-only reuse procedure identifies previously verified individual files whose item data/revision, grouping, template, audience, layout and images still match, and whose actual file hash still verifies. Copy only those reusable files into the new job; regenerate invalidated items. A corrected AP-05 invalidates its sheet. A changed template/audience invalidates every affected sheet. Combined output is rebuilt and checked. No automatic background work, retries or overwrite of issued revisions is implied.

Re-read the current authoritative revision set immediately before completion. The verification procedure checks the input snapshot it is given; it cannot discover a newer record unless the host supplies the current read. A restored PDF is not authority to revert schedule data. Do not regenerate record identity while resuming.

## 4. Verify completeness and return

Record genuine host visual inspection against the accepted template, image outcomes, working links and audience safety for every individual/combined artifact; bind evidence to artifact and template hashes. Use native `ffe_outputs.check` with current input, contract, design, template and new receipt plus companion evidence paths. Require exact expected file set, page counts and tag order. Unknown renderer capabilities, inaccessible sources or one failed item mean an incomplete package; never mark the whole job complete from successful first items.

Return the requested usable artifact links plus a summary of expected/verified/failed items, omissions (if explicitly authorized), source/template/record revisions and stale outputs. Preserve previous receipts and issued artifacts. Sending, uploading and sharing remain separately authorized host actions. Internal receipts must not be bundled for clients. The native output procedure checks PDF structure/text and hash-bound host evidence; only actual host inspection establishes visual fidelity and hidden-content safety.

## Receipt, document placement and completion

The complete native owner defines schema-conforming receipts and a separately retained immutable
companion carrying raw receipt binding, source hash and actual source/visual/mechanical evidence.
Stage and verify both files as one set before either is published. Complete/true is allowed only
after every applicable requested workflow check and actual full-set byte/access readback passes;
incomplete/false retains precise failures. Keep legacy receipts unchanged and identified as historical.
Unknown facts allowed by the requested artifact scope remain explicit; output generation proves no
independent source truth, legal compliance or approval.

For requested durable project placement, use the [document owner](../../docs/workspace-model.md)
with explicit project, phase, stage, scope, originator, date and kind. Receive owns registration;
project library and schedule paths keep their owners. One-off files need no registration or project
setup. Return only intended delivery artifacts and explicitly requested private evidence; never
include the whole job in a client package. Follow [completion reporting](../../docs/completion-reporting.md).
