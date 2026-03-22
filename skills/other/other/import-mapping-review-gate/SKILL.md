---
name: "import-mapping-review-gate"
description: "How to gate import features that add column mapping and material remap or create flows"
domain: "testing"
confidence: "medium"
source: "hicks-import-mapping-gate"
---

## Context

Use this when an import workflow expands from fixed headers and exact material-name matches into a preview step where the user can map source columns, resolve unknown materials, and optionally create new library materials during import.

## Pattern

1. Separate the **obvious-default** path from the **rescue-mapping** path.
   - If headers and material names are already unambiguous, the reviewer should still be able to complete import quickly without mandatory remapping.

2. Require a **preview-before-commit** contract.
   - Every required target field must be auto-resolved or explicitly mapped before final import.
   - Duplicate target mappings, missing required targets, or ambiguous auto-matches must block commit visibly.

3. Treat material resolution as **canonicalization**, not guesswork.
   - Imported values may map to an existing library material, but the app must not silently fuzzy-match, silently case-fold, or silently remap behind the user.

4. Treat create-new-material as a **real library mutation**.
   - Reuse normal material validation and duplicate-name rules.
   - After creation, the new material should be immediately available to the current import and persist like any other library entry.

5. Keep **failure surfaces distinct**.
   - File errors, column-mapping gaps, unresolved materials, material-create failures, and row validation problems should remain separately actionable.
   - Final import must not succeed with unresolved required mappings.

## Anti-Patterns

- Approving because one messy spreadsheet can be rescued while the obvious happy path became slower or mandatory
- Silently auto-creating materials from unknown import values
- Letting unresolved field/material mappings degrade into dropped rows or generic import failures
- Keeping mapping decisions only in transient UI state so validation, save/open, or nesting sees different material names later
