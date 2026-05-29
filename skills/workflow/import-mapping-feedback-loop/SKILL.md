---
name: "import-mapping-feedback-loop"
description: "How to add explicit import-time column/material mapping without weakening deterministic defaults"
domain: "import-pipeline"
confidence: "high"
source: "earned"
---

## Context

Use this when a file import flow must keep its exact-match happy path, but still let users recover from mismatched headers or unknown material names inside the app.

## Pattern

1. **Keep the default strict.** Exact header/material matches should continue to work with zero extra input.
2. **Return mapping metadata on every import response.** Include detected source columns, required field mapping status, and unique imported material resolutions so the UI can react without inventing its own parser.
3. **Suggest, don’t auto-apply.** Deterministic header aliases (`Part Id` → `Id`, `Qty` → `Quantity`) are useful as suggestions, but require an explicit user mapping before import succeeds.
4. **Separate pure import from side effects.** Let the service layer consume explicit mappings; let the bridge/app layer create missing library entities first, then rerun import with the created ids.
5. **Rewrite imported material values to the resolved library name before validation.** That keeps downstream project/nesting flows working with canonical material names.
6. **Keep the UI two-speed.** Let exact header/material files stay on the fast import path, but hold mismatched files in a review session that tracks pending mapping edits, requires an explicit preview refresh after operator changes, and only creates new materials on final commit.

## Good signs

- The same `import-file` route can support first-pass analysis and final import.
- Unknown materials are listed once per source value with a stable status (`resolved`, `unresolved`, `created`).
- Row validation codes stay actionable instead of disappearing behind bridge-only errors.

## Anti-patterns

- Auto-mapping fuzzy headers without telling the user.
- Creating materials inside the pure parser/validator service.
- Returning only row errors and forcing the UI to re-open the file itself to learn what headers existed.

