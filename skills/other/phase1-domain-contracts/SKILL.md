---
name: "phase1-domain-contracts"
description: "How to keep PanelNester's first import-to-nest seam deterministic and UI-independent"
domain: "domain-modeling"
confidence: "high"
source: "earned"
---

## Context

Use this when standing up or extending the backend seam between bridge handlers and the nesting/import logic. The goal is to let early vertical slices move without dragging WPF, persistence, or material CRUD into pure domain code.

## Patterns

### Stable bridge-facing records in the domain project

- Keep request/response/data shapes in `src/PanelNester.Domain/Models/`.
- Keep only service interfaces in `src/PanelNester.Domain/Contracts/`.
- Use serializer-friendly property shapes (`success`, `parts`, `sheets`, etc. via standard .NET property names) and avoid UI-specific types.

### Compact import, expanded nesting

- Import returns compact `PartRow` records with `Quantity`.
- Nesting is the only place that expands quantity into instance-level part IDs (`PartA#1`, `PartA#2`, ...).
- This keeps validation/editing row-based while still producing deterministic placement/unplaced outputs.

### Decimal geometry, explicit clearance

- Use `decimal` for sheet sizes, coordinates, kerf, spacing, and margins.
- Apply kerf as additional spacing/clearance between placements.
- Do not resize part geometry to account for kerf; rendered dimensions should stay true to the imported part.

### Hardcoded demo material for the first slice

- Default Phase 1 import/nesting to a single known `Demo Material`.
- Inject known materials into the import service, but fall back to the demo catalog by default.
- This keeps the first path working before material CRUD and persistence exist.

## Examples

- `CsvImportService` validates rows against the demo material catalog and returns row-level validation status/messages.
- `ShelfNestingService` sorts expanded parts deterministically by area/dimensions/ID, then applies a shelf heuristic with spacing + kerf clearance.

## Anti-Patterns

- Expanding quantity during import and forcing the UI to edit thousands of duplicated rows.
- Using `double` for fit checks where small rounding differences can change placement decisions.
- Letting domain/service contracts depend on WPF, WebView2, or storage concerns.
- Treating kerf as magic geometry shrinkage that makes placements hard to explain to users.
