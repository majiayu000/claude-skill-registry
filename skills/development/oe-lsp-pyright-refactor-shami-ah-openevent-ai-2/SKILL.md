---
name: oe-lsp-pyright-refactor
description: Refactor planning and execution discipline using LSP/Pyright. Use when making non-trivial refactors (splitting files, renaming symbols, moving modules) and you want compiler-accurate references/definitions, plus a Pyright-driven contract baseline to avoid regressions.
---

# oe-lsp-pyright-refactor

## Workflow (shim-first, LSP-first)

1. Before changes:
   - Use LSP to find the definition, outgoing calls, and references for the symbols you will move/rename.
   - Inventory importers before moving modules (including dynamic imports).

2. During refactor:
   - Keep public surfaces stable with re-exports/thin wrappers first.
   - Prefer moving pure helpers/constants before orchestration.

3. After each PR-sized step:
   - Use Pyright/LSP diagnostics to catch Optional leaks, wrong return types, and missing attributes.
   - Fix the contract at the boundary (Protocol/TypedDict) rather than sprinkling `Any`.

## Canonical plans

- Use `docs/internal/BACKEND_REFACTORING_PLAN_DEC_2025.md` for step-file ladders and preserve sets.
- Use `docs/internal/BACKEND_REFACTORING_PLAN_DEC_2025_ADDENDUM.md` for production hardening + PH5 typing work.

## Common refactor targets (Pyright tends to catch first)

- Adapter interfaces: define `Protocol`s for optional capabilities instead of `hasattr`-only contracts.
- API boundary models: ensure required fields never receive `None` (or model them as Optional intentionally).
- “stringly typed” payloads: introduce TypedDicts for `event_entry`, `draft_messages`, `process_msg` output.

