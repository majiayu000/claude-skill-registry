---
name: explore
description: Systematically explore a codebase area and find/fix obvious issues with fresh eyes.
argument-hint: [FOCUS=<focus>]
---

Explore the codebase **methodically**, not randomly. Goal: understand the relevant execution flow,
identify likely issues, and make the **smallest correct** improvements.

## How To Operate

1. **Clarify the target**
   - If `FOCUS` is provided, use it. If not, ask what area/bug/goal matters most.
   - Ask for repro steps, expected behavior, and constraints.
2. **Map the flow**
   - Identify entrypoints (CLI entry, API route, job, UI page, DB mutation, etc.).
   - Trace the call chain through imports and callers.
   - Note sources of truth (schema, config, shared types).
3. **Look for high-signal problems**
   - Obvious bugs, incorrect assumptions, dead code, mismatched types.
   - Inconsistencies with the repo’s conventions (SSOT, validation, config).
   - Missing error handling / logging around external boundaries.
4. **Fix surgically**
   - Prefer minimal diffs over refactors.
   - Don’t introduce new abstractions unless they delete more complexity than they add.
5. **Verify**
   - Run the smallest targeted test/build/lint available.
6. **Report**
   - What you inspected, what you found, what you changed, what remains.

## Output Format

- Summary (1–3 bullets)
- Findings (bugs / risks / debt)
- Fixes (what changed + why)
- Next steps (if any)
