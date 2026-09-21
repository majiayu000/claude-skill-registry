---
name: drawing-quantity-extract
description: "Extract countable FF&E or luminaire instances from supplied drawings with position-level evidence. Use for plan quantities or symbol counts; not area takeoffs, product specs or cross-source reconciliation."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# /as:drawing-quantity-extract — Count drawing instances

Before acting, read the [host contract](../../docs/host-harness-contract.md) and
[declaration](host-contract.json) (`skill:drawing-quantity-extract`), using only referenced profiles
from the [catalog](../../corpus/host-contracts.json). Requirements do not grant access.

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and available native tools or ordinary task-specific code. Operation names identify semantic procedures, not installed functions. No Arch Studio runner, package installation or executable reconstruction is required. Existing exact authorization persists; ask only for material missing information or permission.

Input: exact supplied drawing files/revisions, building/floor/phase scope and requested tags/types.
Output: unadopted instance ledger, scoped counts and coverage/exclusion evidence. No record owner is
changed. Read owning instructions for project work; one-off files do not require initialization.

1. Verify actual source access. Freeze document hashes and physical page list; record printed sheet
   IDs separately. Keep drawing types/revisions distinct. Missing access calls a real host grant or
   produces a precise handoff; never substitute another workspace.
2. Read [native evidence procedures](../../tools/transformers/evidence-contracts.md). Extract text and
   coordinates using the native `pdf_evidence.extract` procedure; use host OCR/visual inspection for image-only
   labels. Save page-sized checkpoints. A legend index is local to its drawing, not a global type ID.
3. Build one ledger row per candidate label/symbol at its document/page/bounding box. Classify each as
   instance, legend, note or unresolved. Count repeated identical tags at distinct positions; inspect
   duplicate text/OCR layers and overlapping boxes before excluding any. Preserve exclusions and reasons.
   Associate rooms only using visible boundaries or explicit schedule evidence, not nearest-label proximity.
4. Inspect each scoped page against the ledger. Reconcile revision callouts and same-page schedules;
   never count note text as furniture or silently relabel instances because a revision note proposes it.
   Keep observed label counts and any evidenced revised allocation distinct. If methods disagree,
   report unresolved counts and the source regions; an approximate number is not verified quantity.
5. Apply `drawing_quantities.summarize` with native computation under the complete evidence procedure.
   It counts supplied classified instances only. Retain the actual result plus the host's per-page
   coverage and visual evidence; neither a successful command nor unique-tag count proves full extraction.
6. Return counts by exact tag and scope, source locators, excluded/unresolved instances and pages not
   inspected. Save only requested derived outputs, fresh-read them and preserve originals. Route
   comparison with inventories or other drawings to `/as:schedule-quantity-reconcile`; route adopted
   record changes to `/as:master-schedule`, under its authorization. Never certify procurement totals.

## Current document placement

Save only authorized derived outputs and verify their actual content, source hashes and complete requested scope. Inline answers and one-off files need no project setup or adoption. For a requested registered project report, resolve confirmed coordinates using the receive-owned native `documents.resolve/register` semantics in the [workspace model](../../docs/workspace-model.md), including its complete document/register mutation sequence. Find existing records with `documents.query`; never guess a folder. This conditional handoff does not authorize schedule or library changes.
