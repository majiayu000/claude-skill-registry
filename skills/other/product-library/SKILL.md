---
name: product-library
description: "Inspect or save reusable FF&E library products through reviewed, guarded transactions. Use for explicit library imports, corrections or recovery; adopted selections and workbook reconciliation belong to master-schedule."
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

# /as:product-library — Reusable product records

Before acting, read the [host contract](../../docs/host-harness-contract.md), this component's
[declaration](host-contract.json) (`skill:product-library`), and required profiles from the
[shared catalog](../../corpus/host-contracts.json). Declarations do not grant access or permission.

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md), available native tools and ordinary task-specific
code. Apply the [native library operations](../../tools/workspace/product-library-contract.md).
Operation IDs describe semantic scope, not an installed dispatcher. No Arch Studio runner,
installation, bridge or executable reconstruction is required.

Own optional project-root `product-library.csv` and its operation evidence. Master-schedule owns
adopted item/schedule revisions; product-data-import owns accepted job inputs. A saved or researched
product is not an adopted selection. The separate [42-column EPD library](../../schema/epd-schema.md)
remains outside this owner; never convert it into the [33-column product schema](../../schema/product-schema.md).
Read the [CSV conventions](../../schema/csv-conventions.md); source evidence never authorizes a write.

## Inspect and prepare the selected change

Resolve canonical context and actual project instructions through the [workspace model](../../docs/workspace-model.md).
One-off answers need no project/library initialization. `product_library.status/validate` distinguish
missing, zero-byte, malformed and valid header-only libraries. Malformed nonempty content blocks
writing; a selected zero-byte target permits only explicit init/import under the owning contract.
Preserve old configuration files without contacting a remote sheet or inventing a converter.

Use `product_library.preview` for the exact selected `init`, `import`, `append` or `update` intent.
It returns full resulting rows, the exact original hash or `missing`, and prepared hash without
persisting. Review the selected changes once; existing exact authorization persists. Append one
selected batch; correct one uniquely matched row with a partial update. Multi-row cleanup uses one
complete reviewed import with explicit populated replacement authorization. Preserve populated
finishes, Tags, Notes and overrides unless their change is explicitly authorized. Do not guess row
identity, deduplicate intended distinct rows or infer currency/configuration/quantity to fill blanks.

## Before changing records

Follow the [native mutation sequence](../../docs/workspace-model.md#native-mutation-sequence):
**Inspect → Prepare → Verify preparation → Apply → Verify result → Complete**. Inspect pending work
first. Retain the complete original/absence and complete prepared product CSV, actual access metadata,
import-source guards and bound intent. Finish durable saving and independently reopen every retained
file before the first publisher; writing evidence without rereading it is insufficient. Validate the
entire actual prepared CSV. Publish only under actual writer protection with fresh byte/access guards.
Mark complete only after actual library bytes, schema, selected changes and preserved data read back.

Use stable request IDs and the exact preview hash under the [library binding/retry rules](../../tools/workspace/product-library-contract.md#preview-binding-and-native-publication).
A stale preview or reused ID with changed inputs is a conflict, not permission to substitute a new
hash. Empty update changes are a byte-preserving no-op after unique-match validation. Exact repeated
append requests return their verified prior result; a new intentional append has a new operation ID.
`product_library.recover` inspects retained evidence and actual state, continuing only a proven safe
before/after state. Preserve third-state conflicts, pending work, old logs and unpublished crash evidence.
Historical evidence paths are readable records, not a dependency on the old helper or its locks.

## Report the observed result

Return target, request ID, before/after/current hashes and readback-supported outcome, with any
pending recovery reference. An old completed operation may have `current_matches_result: false`
after later edits; report that difference and preserve current state. Never describe a preview,
receipt alone or delivered instructions as a completed save. Use the [completion contract](../../docs/completion-reporting.md).

For a requested registered authored report, use receive-owned native `documents.resolve/register/query`
with confirmed coordinates and its complete document/register publication set. One-off derived files
need no registration. No report or library save authorizes adopted schedule, project-fact or EPD changes.
