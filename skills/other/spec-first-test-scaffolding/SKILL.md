---
name: "spec-first-test-scaffolding"
description: "How to scaffold executable tests before the implementation seams land"
domain: "testing"
confidence: "high"
source: "hicks-phase0-1"
---

## Context

Use this when architecture or service seams are still being built, but the team needs concrete acceptance coverage now.

## Pattern

1. Create one test project per seam (`Desktop`, `Services`, `Domain`) under `tests/`.
2. Add one runnable smoke or contract test that can pass against what exists today.
3. Encode expected rules in tiny spec helpers so the acceptance behavior is executable, not just written down.
4. Add skipped tests with precise blocker text for the integration checks that cannot run yet.
5. Pair the tests with a written matrix that maps each case to a success criterion or failure mode.
6. Record contract gaps immediately so implementation teams know what must stabilize for the placeholders to turn live.

## Good signs

- The first `dotnet test` run passes immediately.
- Blocked tests say exactly what seam is missing.
- Reviewers can see which requirements are already guarded and which are waiting on implementation.

## Anti-patterns

- Creating only prose test notes with no executable checks
- Adding failing tests that block unrelated work before the seam exists
- Leaving placeholders without an explicit blocker or acceptance target
