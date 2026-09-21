---
name: schedule-quantity-reconcile
description: "Compare scoped quantity snapshots and explain matches, missing rows and conflicts. Use to reconcile drawing, report or schedule counts; not to extract source documents or update adopted records."
allowed-tools:
  - Read
  - Write
  - Bash
---

# /as:schedule-quantity-reconcile — Reconcile sourced quantities

Before acting, read the [host contract](../../docs/host-harness-contract.md) and
[declaration](host-contract.json) (`skill:schedule-quantity-reconcile`), using its profiles from the
[catalog](../../corpus/host-contracts.json). No source or write access is implied.

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and available native tools or ordinary task-specific code. Operation names identify semantic procedures, not installed functions. No Arch Studio runner, package installation or executable reconstruction is required. Existing exact authorization persists; ask only for material missing information or permission.

Input: two source-identified quantity snapshots and explicit building/floor/phase/revision scope.
Output: a read-only comparison, not an authoritative merged schedule. Project instructions apply
when bound to a project; one-off comparison does not initialize or adopt records.

1. Read both actual inputs and preserve hashes/locators. Drawing extraction belongs to
   `/as:drawing-quantity-extract`. Do not compare a whole-campus inventory against one floor as though
   their denominators match. Missing scope or unit evidence remains unresolved.
2. Read [native evidence procedures](../../tools/transformers/evidence-contracts.md). Prepare exact tag/scope/unit
   keys and preserve every contributing source row. Explicitly resolve aliases or unit conversions
   using source evidence before comparison; no fuzzy match or automatic phase/room synonym.
3. Apply `schedule_reconcile.compare` with native computation under its evidence procedure. Duplicate
   keys require explicit aggregation or conflict resolution first. Unknown is null, not zero; absent
   rows are not zero. Matching supplied values proves agreement, not correctness or completeness.
   Lighting reports first use `/as:lighting-report-extract` to distinguish inventory from calculation
   surfaces. Never sum repeated room inventory to remove duplicate keys. Before projecting normalized
   groups to tag/scope/unit, explicitly select matching source revisions, rooms, scenes and variants
   on both sides, or preserve those distinctions in the agreed comparison scope. Keep every contributing
   locator; do not flatten unresolved/conflicting identity into an authoritative quantity. The comparison
   rejects duplicate comparison keys; it does not choose or merge lighting inventories.
4. Explain each discrepancy with locators on both sides and source coverage. A revision note can
   explain a split but does not authorize changing labels or records. Preserve competing values;
   distinguish a proposed correction from an approved one. Product identity/spec discrepancies route
   to `/as:product-audit`; do not enlarge this skill into a general product audit.
5. Return matched, conflicting, missing and unknown groups. Save only an authorized derived report
   and read it back; do not change original files. Adopted changes go to `/as:master-schedule` with
   explicit selected changes and expected revisions. Missing host capability yields a bounded handoff,
   not a fabricated match or silent fallback. On retry, reread input hashes before reusing results.

## Current document placement

Save only authorized derived outputs and verify their actual content, source hashes and complete requested scope. Inline answers and one-off files need no project setup or adoption. For a requested registered project report, resolve confirmed coordinates using the receive-owned native `documents.resolve/register` semantics in the [workspace model](../../docs/workspace-model.md), including its complete document/register mutation sequence. Find existing records with `documents.query`; never guess a folder. This conditional handoff does not authorize schedule or library changes.
