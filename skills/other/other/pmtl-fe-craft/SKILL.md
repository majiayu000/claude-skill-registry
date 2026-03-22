---
name: pmtl-fe-craft
description: "Advanced frontend craftsmanship skill for PMTL_VN. Use for frontend implementation, refactoring, or code review when the goal is code that feels senior-written: clean boundaries, strong component shape, server-first logic, and zero AI-slop shortcuts."
---

# PMTL Frontend Craftsmanship

Legacy compatibility skill. Prefer `pmtl-fe-implementation` unless the task explicitly asks for this deeper craftsmanship pass.

Use this skill when the task is not just “make the UI work”, but “make the frontend codebase stronger”.

## Workflow

1. Read the target feature and one nearby pattern first.
2. Decide the component boundary:
   - route entrypoint
   - feature-level server helper
   - leaf client component
3. Keep the diff narrow and intentional.
4. Run `scripts/scan_frontend_risks.py` on touched files if the change is medium or larger.
5. Pair with `pmtl-verify-quality-gate` before calling it done.

## Load references as needed

- `references/server-first-boundaries.md`
- `references/component-shape.md`
- `references/data-and-side-effects.md`

## What this skill protects

- minimal `'use client'` footprint
- good naming and flat logic
- no internal API roundtrips from server components unless unavoidable
- no placeholder logic or speculative abstractions
- no Vietnamese without marks
