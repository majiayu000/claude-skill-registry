---
name: review-file-size
description: Find files approaching context limits and evaluate whether coupling-aware splits are worthwhile
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Identify source files approaching the context load limit and evaluate whether they can be meaningfully split. Use parallelism where possible.

## Why This Matters

Files over ~25k tokens cause problems: the Read tool must batch them, they bloat context for tasks that only need a small piece, and they're harder to reason about in a single pass. But splitting a file poorly — into two halves that share all the same globals and must always be loaded together — is worse than one large file. A split only helps if the pieces are **independently useful**.

## Step 1 — Measure file sizes

Scan all `.ahk` files in `src/` and `tests/` (excluding `src/lib/`). For each file, estimate the token count — don't rely on line counts alone. AHK files with long DllCall signatures, inline strings, or dense logic have significantly more tokens per line than sparse files with short functions.

**Approximate token estimation**: Read each file and estimate tokens. Characters ÷ 4 is a rough baseline, but AHK identifiers and camelCase inflate this. Aim for a reasonable estimate, not exact counts.

**Threshold**: Only flag files that are **approaching trouble** — roughly 20k+ tokens. Files well under this threshold are fine regardless of line count. Don't propose splitting a 500-line file that's 12k tokens just because it's "large by line count."

## Step 2 — Analyze internal coupling for flagged files

For each file above the threshold, use the tools to assess whether a split is viable:

| Tool | What It Tells You |
|------|------------------|
| `query_interface.ps1 <file>` | Public functions and globals — are there distinct groups serving different consumers? |
| `query_global_ownership.ps1 <globalName>` | For each global the file uses — who else writes/reads it? Would a split add manifest entries? |
| `query_function_visibility.ps1 <funcName>` | For key functions — who calls them? Would splitting require cross-file calls between the halves? |

**Look for natural seams:**
- Distinct functional sections (init vs runtime vs cleanup, or producer vs consumer)
- Function groups that reference different sets of globals
- Sections that different tasks/skills would load independently

**Look for coupling walls:**
- Most functions reading/writing the same globals (no seam exists)
- Circular call patterns between would-be halves
- A cohesive state machine or event handler where any piece requires the whole

## Step 3 — Evaluate each candidate split

For each file where a seam exists, evaluate the **net benefit**:

**Benefits of splitting:**
- Smaller context loads for tasks that only need one half
- Clearer separation of concerns
- Easier to test pieces in isolation

**Costs of splitting:**
- New ownership manifest entries if globals cross the boundary
- Additional `#Include` dependencies
- Two files that must always be loaded together (if coupling is too tight) = no actual benefit
- Risk of regressions from the refactor itself

**Only recommend a split when the net benefit is clearly positive.** A file at 22k tokens with no natural seam is better left alone than forcibly split into two 11k-token files that are joined at the hip.

## Plan Format

**Section 1 — File size inventory** (only files near/above threshold):

| File | Lines | Est. Tokens | Status |
|------|-------|-------------|--------|
| `gui_state.ahk` | 1400 | ~28k | Above threshold |
| `gui_paint.ahk` | 900 | ~19k | Approaching |
| `viewer.ahk` | 1100 | ~22k | Above threshold |

**Section 2 — Coupling analysis for candidates:**

| File | Natural Seam? | Shared Globals Across Seam | New Manifest Entries | Independently Useful? |
|------|--------------|---------------------------|--------------------|--------------------|
| `gui_state.ahk` | Yes — interceptor vs state transitions | 2 (`gGUI_State`, `gGUI_Sel`) | 0 (both already shared) | Yes — interceptor logic reads different than state logic |
| `viewer.ahk` | Weak — most functions share `gViewer_*` | 8 | 4 new entries | No — halves always loaded together |

**Section 3 — Recommended splits** (only where net-positive):

| File | Split Into | Seam | Tokens Each | Coupling Cost | Benefit |
|------|-----------|------|-------------|--------------|---------|
| `gui_state.ahk` | `gui_state.ahk` + `gui_interceptor.ahk` | Interceptor event handling vs state transitions | ~14k / ~14k | 0 new manifest entries | Tasks investigating input vs state can load one half |

**Section 4 — Files left alone** (above threshold but not worth splitting):

| File | Est. Tokens | Why Not Split |
|------|-------------|--------------|
| `viewer.ahk` | ~22k | All functions share 8+ `gViewer_*` globals — no seam |

Ignore any existing plans — create a fresh one.
