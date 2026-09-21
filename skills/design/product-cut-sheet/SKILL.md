---
name: product-cut-sheet
description: "Produce one specification sheet from selected FF&E inputs using an accepted template, exact identity and inspected source imagery. Use for one product or explicit group; use spec-book for a complete package."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# /as:product-cut-sheet — Produce a Product Sheet

Before acting, read the [host contract](../../docs/host-harness-contract.md) and this component's [declaration](host-contract.json) (`skill:product-cut-sheet`). Load only its referenced mode profiles from the [shared catalog](../../corpus/host-contracts.json). Compose modes required by the actual task; declarations are requirements, not proof of access or permission.

<!-- architecture-studio:harness-compatibility -->
> Host adapter: read [delivery-specific guidance](../../docs/host-adapters.md) for invocation, package paths, questions, file access and optional delegation.

Produce one selected product sheet, or an explicitly agreed product/finish grouping. Input: pinned item revision(s) or a one-off source snapshot, accepted template, exact tag, audience and image evidence. Output: an actual requested-format artifact and hash-bound receipt. This skill owns derived individual-sheet preparation manifests and artifact receipts; `/as:product-data-import` owns the accepted job input manifest; `/as:spec-book` owns package receipts. Neither owns item specifications or project decisions.

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

## 1. Resolve context and inputs

For project or adopted-schedule work, resolve the nearest valid `PROJECT.md` using `/as:project` context resolution and read its instructions. If that project is unresolved, select it through `/as:studio`; never create one implicitly or write into the plugin. Discover canonical records independently of indexes; preserve malformed records and report their path/problem. Project facts and decisions stay owned by `/as:project`; schedule adoption and revisions stay owned by `/as:master-schedule`.

For samples, random products or demonstrations without a named project, default to standalone one-off work and state that assumption without a project-selection gate. Use an authorized task output folder, not a studio registry or project library. Ask only if an output destination or permission is actually missing. Research real products when selection was delegated, retain sourced facts and label the sheets as samples; never invent product evidence. An existing studio does not change this default. Explicit project/schedule instructions take precedence.

For standalone work, the [native intake owner](../../tools/transformers/ffe-intake-contract.md) uses the explicitly authorized task output root as the one-off boundary. Keep the same `ffe/jobs/<job-id>/` relative structure, evidence, templates and verification below within that task folder. No PROJECT.md or studio registration is required or created.

Use existing task authorization. Ask once only for an unresolved material choice, covering exact target, audience and side effects in one gate; do not re-ask accepted scope/template choices. Read the supplied source before writing. Do not infer approval, price, availability or configuration from a generated sheet.

For **adopted** schedules, read the exact schedule snapshot through `ffe_records.read`. Pin schedule ID/revision/hash and item ID/revision. Select the requested item(s) without changing their identity. For **one-off** work, preserve a source-identified input snapshot with stable local item IDs and positive snapshot revisions; explicitly record that no schedule adoption occurred. Never convert a workbook into authoritative records implicitly. Workbook editing/reconciliation belongs to the host and `/as:master-schedule`, not this output skill.

### Accepted input handoff and derived projection

Consume `ffe/jobs/<job-id>/input-manifest.json` from `/as:product-data-import`, using [the intake schema](../../schema/ffe-intake.schema.json). If it is absent, hand off to that owner to record the supplied sources and scope under existing authorization; one-off mode records inputs without adopting a schedule. Verify its `input_hash`, source hashes/status, selected tags, accepted template and adopted `record_basis` when present. Reconcile explicit product/finish grouping with that selection. Corrections produce a superseding input job through the owner, never an output skill's rewrite of the accepted manifest.

Preserve the untouched joined record read (or one-off source extraction) separately. Create a **derived output snapshot**, retaining schedule ID/revision/hash and item ID/revision while selecting only the accepted scope. Put accepted `input_hash`, source references/status, selected tags and the original record source in the snapshot's `source` object; an empty record source is not invented evidence. Record the raw-read hash and explicit field mapping separately in the preparation evidence. The output snapshot is a rendering projection, not a newly signed canonical record.

Map structured values deliberately into the output contract’s scalar render fields. For a stored hyperlink `{label,url}`, retain separate display-label and true-URL fields and explicitly allowlist the intended fields; never replace the URL with its label. Preserve the raw structured value and mapping in private preparation evidence. Other nested values require an explicit lossless source-to-display mapping, not guessed flattening. The host must create and inspect actual PDF link annotations, not merely print URL-looking text. Never mutate adopted records to satisfy a renderer's input schema.

Before verification or resume, reread current canonical data and accepted input evidence, then rebuild the same derived projection and mapping. Compare it with the prepared inputs; changed source/scope/mapping/revisions invalidate affected outputs. Keep all raw evidence and preparation controls outside client delivery.

## 2. Bind template, audience and images

Resolve the centrally owned [document design system](../../studio/standards/documents/design-system.md) and [cut-sheet template](../../studio/templates/documents/product-cut-sheet/template.md). Layout/type rules live there, not in this skill. Use `document_contracts.resolve` from the [native design owner](../../tools/renderers/document-design-contract.md): explicitly selected project/job assets first, configured studio assets next, bundled assets last. A supplied accepted reference takes precedence for its declared rules; record `reference_overrides` and its hash rather than silently replacing it. Missing assets or incompatible dependencies block the affected output.

Resolve the requested physical preset/custom dimensions, portrait/landscape and displayed measurement units separately. Pin design/template IDs, versions, asset hashes, page dimensions, margins, content area and layout version in `resolved-design.json`. Supply that exact parsed resolution to preparation and verification. Re-resolve current dependencies before verification; retain earlier resolved bytes. The host follows size-aware grid/type/overflow rules and inspects every actual page, image resolution and 100% print geometry. Do not scale a Letter layout to a board, substitute a nearby paper size, or imply product images have drawing scale. Unsupported combinations are explicit blockers.


Inspect the supplied template using the host's PDF/document capability. Record its hash and concrete page size, field order, typography, spacing, image placement and footer requirements. Preserve the accepted design; use a default only if no template was supplied and the task permits it. A template with an image placeholder is layout evidence, not proof of image completion.

Use [native output contracts](../../tools/renderers/ffe-output-contract.md) and [template contract](../../schema/ffe-output-template.schema.json). Set an explicit audience field allowlist; never feed excluded net prices, internal notes or full source records to a client renderer. Client output also requires inspection of metadata, attachments, hidden text, links and embedded images. An allowlist of fields alone cannot make an unsafe template safe.

Retain selected image/finish choices. `/as:product-image-processor` handles image preparation. Exact images, representative family imagery and missing images must remain distinct and sourced. A missing image blocks completion unless the user already authorized a labeled placeholder. Never substitute a generated image as product evidence. Image processing does not change the selection record.

Preserve exact requested tags. Unsafe filenames require a resolved naming choice, never silent normalization. Use a unique project-local `ffe/jobs/<job-id>/<revision>/` directory so `AP-05.pdf` does not overwrite another job or issued revision. Persist project-relative references. No cloud credentials or connector setup is part of this procedure.

Use the [shared identity and versioned filename contract](../../tools/renderers/ffe-output-contract.md#encoding-and-exact-identity).
Ordinary dotted tags remain exact. Keep `tag` for sheet identity and pin the current separate `filename` mapping. Validate the shared identity schema and complete native filename rules before preparing any output. Place images within the snapshot bundle; retain traversal and symlink checks.

## 3. Prepare and render

Create the explicit single-output contract and input snapshot, then perform native `ffe_outputs.prepare` using the complete output owner.

Preparation writes private controls under `internal/`, allowlisted data under `render/`, and an empty `delivery/`. It does not generate a PDF. Keep controls outside deliverables; use only projected data in the host renderer. Never copy the whole job folder into an external package.

Use the host's document/PDF skill and renderer to create the manifest's exact delivery filename (`<exact-tag>.pdf` for version 1; recorded `filename` for version 2), or the explicitly requested format. Show the exact bare tag on the sheet; filename text alone is insufficient identity evidence. Open and inspect every rendered page against the accepted reference after the last change. A saved HTML intermediate remains HTML; a download link or successful tool invocation is not a completed PDF. If rendering or source access is missing, retain the prepared work and state the exact missing capability. Hosted MCP context retrieval does not provide local filesystem or rendering access.

## 4. Verify and return

Trace each rendered product link back to its exact source document hash, physical page and annotation
identity, or the explicit URL observation. Compare the actual PDF annotation target with that binding;
correct inventory links do not prove downstream sheet links are correct. A filename suffix or matching
page number cannot establish product ownership. Keep raw dimensions and their source-backed axis/unit
mapping in preparation evidence; do not treat populated prose as normalized schedule fields.

Read back current item/source, template, audience and image revisions; changes require a new prepared revision. Write the hash-bound host inspection evidence described in the output contract, including actual layout/image/link/audience, physical page size, clipping/overflow and image-resolution inspection. Perform native `ffe_outputs.check` with the freshly current input, contract, design and template. It checks actual PDF bytes, parseability, page counts, tags, denied-field leakage, hashes and evidence references. It cannot independently judge layout or hidden objects; the host must actually inspect those.

Before returning the artifact link, perform native `delivery_coverage.verify-links` with the current item, revision, source/template hashes, actual artifact/receipt paths and the immutable companion evidence path/raw hash. Require verification of the linked bytes against the current expected entry.

Preserve failed outputs and earlier receipts. Report `complete` only if the requested artifact exists, has been reopened/inspected, and all required checks pass. Otherwise report the affected item and precise blocker. Return a usable local artifact link, source/template/item revision references, image status and receipt; no external sending/upload without authorization. Corrections route to `/as:product-audit` or record owner, then produce a new output revision. A restored artifact never rolls back authoritative records.

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
