---
name: review-static-coverage
description: Find gaps in static analysis where new checks could prevent classes of bugs
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-review production code patterns to find gaps where static analysis checks (`tests/check_*.ps1`) could prevent whole classes of bugs. Use maximum parallelism — spawn explore agents for independent areas.

**Scope**: Static analysis pre-gate checks only. NOT AHK test coverage (see `review-test-coverage`), NOT query tools, NOT check speed (see `review-static-speed`).

## The Bar for a New Check

A proposed check must clear ALL of these:

1. **Prevents a class, not an instance** — catches a pattern that can recur, not a one-off bug
2. **Statically detectable** — regex/parsing on source files is sufficient. If it needs runtime info, skip it.
3. **Low false positive rate** — a check that fires on 50 lines but only 2 are real problems creates noise that erodes trust in the pre-gate
4. **Worth the maintenance** — a check that fires once a year isn't worth maintaining. Focus on patterns that are easy to introduce accidentally during normal development.

## Current Check Inventory

**Standalone checks** (complex enough to warrant their own process):
- `check_warn.ps1` — warn directive enforcement

**Batch checks** (grouped to share file cache and reduce PowerShell overhead):
- `check_batch_simple.ps1` — lightweight pattern checks (switch globals, IPC constants, DllCall types, IsSet patterns, cfg properties, duplicate functions, dead code detection, config registry integrity, etc.)
- `check_batch_functions.ps1` — function-level checks
- `check_batch_directives.ps1` — directive-level checks
- `check_batch_guards.ps1` — guard pattern checks
- `check_batch_patterns.ps1` — code pattern checks
- `check_batch_tests.ps1` — test file checks

**Enforcement tools** (in `tools/`, run as pre-gate checks):
- `query_global_ownership.ps1 -Check` — ownership manifest enforcement
- `query_function_visibility.ps1 -Check` — private function boundary enforcement

## Where to Look for Gaps

Explore the production code for patterns that are:
- **Error-prone by nature** — easy to get wrong during normal development
- **Silent when broken** — no runtime error, just wrong behavior
- **Repetitive** — the same pattern appears in many files, so a check amortizes well

Categories to investigate:
- **Resource management** — GDI+ create without delete, DllCall handle leaks, unclosed file handles
- **Concurrency** — `Critical "On"` without matching `Critical "Off"` on all exit paths
- **AHK v2 gotchas** — patterns that are valid syntax but wrong semantics (e.g., v1 patterns that compile but misbehave in v2)
- **API contracts** — functions called with wrong argument counts or types, especially DllCall
- **Data flow** — globals read before initialization, config keys used but not in registry

## Placement Guidance

When proposing a new check, specify where it fits:

- **Add to existing batch** — if the check is short (<50 lines of logic), benefits from the shared file cache, and fits the batch's theme. This is the default for simple pattern checks.
- **New standalone** — if the check is complex (>100 lines), needs its own specialized parsing, or has significantly different performance characteristics than batch siblings.
- **New batch** — only if there are 3+ related sub-checks that share a specialized cache or parsing step not needed by existing batches.

## Validation

For each proposed check:

1. **Cite the pattern**: "I found this pattern in `file.ahk` lines X–Y" — show real code that the check would flag (or correctly skip).
2. **False positive analysis**: Run the proposed regex/logic mentally against the codebase. How many hits? How many are true positives? A >80% true positive rate is the minimum.
3. **Counter-argument**: "What would make this check unnecessary?" — Is the pattern already prevented by coding conventions? Is it rare enough that code review catches it?
4. **Observed vs inferred**: Did you find actual instances of this bug pattern, or infer it could happen from code structure?

## Plan Format

| Pattern | Detection Method | False Positive Est. | Placement | Justification |
|---------|-----------------|--------------------|-----------|--------------|
| Missing `Critical "Off"` on early return | Regex: `Critical "On"` then `return` without intervening `Critical "Off"` | Low — pattern is structural | `check_batch_guards.ps1` | Easy to miss during edits, silent corruption |

For each proposed check, include:
- A sketch of the detection logic (regex pattern or parsing approach)
- Example true positive and true negative from actual codebase
- Which existing batch it belongs in (or why standalone)

Order by value: high-frequency silent bugs first, rare edge cases last.

Ignore any existing plans — create a fresh one.
