---
name: review-function-visibility
description: Audit function visibility boundaries and rename misclassified public/private functions
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit function visibility boundaries for cleanup opportunities. Use parallelism where possible.

## Tools

**Primary** — run this first to get the candidate list:

| Command | Purpose |
|---------|---------|
| `query_visibility.ps1` | Public functions with 0 external callers (default) |
| `query_visibility.ps1 -MinCallers 1` | Also include functions with exactly 1 external caller |

**Verification** — for investigating specific functions:

| Command | Purpose |
|---------|---------|
| `query_function_visibility.ps1 <funcName>` | Where defined, public/private, all callers |
| `query_interface.ps1 <file>` | Public/private function ratios for a file |
| `query_impact.ps1 <funcName>` | Blast radius of making a function public (downstream callers/readers) |
| `query_includes.ps1` | Include tree — verify cross-file boundaries when assessing visibility |

## What to Look For

### 1. Public functions with 0 external callers (high signal, low risk)

These are private functions missing the `_` prefix. Rename them.

**Before renaming, verify:**
- Not a runtime callback target bound from a different file (`SetTimer`, `Hotkey`, `OnEvent`, `OnExit`, `OnError`, IPC function refs). Use `query_function_visibility.ps1` to check — it detects indirect references, not just direct calls.
- Runtime callbacks CAN be renamed if the binding site is in the **same file** as the definition. Only skip if bound from a different file.

### 2. Public functions with exactly 1 external caller (review, don't auto-rename)

Flag these but apply judgment. Only propose making private when:
- The single caller is in the same module/file
- The function isn't a hook/callback target
- The function isn't part of a coherent public API that happens to have one consumer today

**Skip** when the function is:
- A documented entry point or API function
- A callback registered by external code
- Part of a set of related public functions where making one private breaks the logical interface

## CRITICAL — Safe Renaming

**Never use `replace_all` when the function name is a substring of another function name.** For example, renaming `_Init` would corrupt `WL_Init`.

Before every rename:
1. Use `query_function_visibility.ps1 <funcName>` to get all call sites
2. Search for longer function names that contain the target as a suffix (e.g., before renaming `Foo`, check for `BarFoo`, `BazFoo`)
3. If substring collisions exist, rename each call site individually instead of using `replace_all`

## Plan Format

**Section 1 — Zero-caller renames** (high confidence):

| File | Function | Rename To | Verified No Callers | Substring Safe? |
|------|----------|----------|-------------------|-----------------|
| `gui_paint.ahk` | `BuildLayout()` | `_BuildLayout()` | `query_visibility.ps1` — 0 callers | Yes — no `XBuildLayout` exists |

**Section 2 — Single-caller candidates** (needs judgment):

| File | Function | Caller | Same File? | Recommendation | Reason |
|------|----------|--------|-----------|---------------|--------|
| `gui_data.ahk` | `FormatTitle()` | `gui_paint.ahk` | No | Keep public | Cross-file caller, legitimate API |

**Section 3 — Public/private ratio observations** (informational):

| File | Public | Private | Notes |
|------|--------|---------|-------|
| `gui_state.ahk` | 12 | 3 | High public ratio — may warrant review |

Order section 1 by file for efficient batch renaming. Run tests after all renames: `.\tests\test.ps1 --live`

Ignore any existing plans — create a fresh one.
