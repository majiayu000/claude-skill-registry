---
name: review-ahk2
description: Scan for AHK v1 patterns that slipped into the v2 codebase
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-scan all source files for AHK v1 patterns that don't belong in a v2 codebase. Use maximum parallelism — spawn explore agents for independent areas.

## Context

LLMs are trained on far more AHK v1 code than v2. This means v1 patterns can slip in during AI-assisted development — they often compile and even run, but with subtly wrong behavior. This review catches those.

## Step 1 — Build the checklist

Before scanning, gather the full v1→v2 migration surface:

1. Read `.claude/rules/ahk-patterns.md` for known project-specific v2 rules and past mistakes
2. Do a **web search** for "AutoHotkey v1 vs v2 syntax changes" to get the comprehensive migration list
3. Combine into a checklist of patterns to scan for

## Common v1→v2 Mistakes

These are the most frequent offenders (not exhaustive — the web search in Step 1 may surface more):

### Syntax changes
- `Func("Name")` instead of direct function reference `FuncName` (v1 pattern for callbacks/timers)
- `%variable%` dereferencing instead of just `variable` (v1 legacy syntax)
- `:=` vs `=` confusion — v2 uses `:=` for all assignments; `=` is comparison only
- `If var =` instead of `If (var =)` or `If var ==` — v1's loose comparison syntax
- String concatenation with `.` instead of space or explicit `.` (context-dependent)
- `Return value` instead of `return value` (cosmetic but signals v1 habits)

### Function/command changes
- `MsgBox, text` (v1 command) instead of `MsgBox(text)` (v2 function)
- `SetTimer, Label` (v1 label) instead of `SetTimer(FuncRef)` (v2 function ref)
- `Gui, Add` (v1 command) instead of `myGui.Add()` (v2 object)
- `IfWinExist` (v1 command) instead of `WinExist()` (v2 function)
- `StringReplace` / `StringSplit` (v1) instead of `StrReplace()` / `StrSplit()` (v2)
- `SubStr(str, 1, 1)` is fine in both, but `StringLeft` / `StringMid` are v1-only

### Variable/scope changes
- `local` keyword used unnecessarily — v2 functions default to local
- Assuming globals are accessible inside functions without `global` declaration
- `#Warn` differences between v1 and v2

### Object model changes
- `Object.Insert()` (v1) instead of `Object.Push()` / `Map.Set()` (v2)
- `Object.Remove()` (v1) instead of `Array.RemoveAt()` / `Map.Delete()` (v2)
- `Array[0]` — v2 arrays are 1-based by default
- `new ClassName()` (v1) instead of `ClassName()` (v2 — `new` was removed)
- Legacy `__New` / `__Delete` patterns that don't match v2 class syntax

### Comparison operators
- `<` / `>` for string comparison — v2 should use `StrCompare()` (project rule)
- `==` is case-sensitive in v2 (was case-insensitive in v1)
- `!= ` vs `!==` awareness

## Explore Strategy

Split the codebase for parallel scanning:

- `src/gui/` — GUI rendering, state machine, overlay, input
- `src/core/` — Producers (WinEventHook, Komorebi, pumps)
- `src/shared/` — Window list, config, IPC, blacklist, theme, stats
- `src/editors/` — Config/blacklist editors
- `src/pump/` — EnrichmentPump subprocess
- Root `src/` files — Entry points, launcher, installation, update

Exclude `src/lib/` (third-party code).

Each explore agent should scan for ALL checklist patterns within its zone, not just one pattern at a time.

Use `query_function_visibility.ps1 <funcName>` to validate whether flagged function call patterns are v1 or v2 — it shows all callers and the definition site, confirming whether indirect references (timers, callbacks) use v1 string syntax or v2 direct refs.

## Validation

Many v1-looking patterns may actually be correct v2 code. AHK v2 kept some syntax from v1. **Validate every finding yourself** before including it in the plan.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with the actual code quoted.
2. **Confirm it's v1**: Is this actually a v1 pattern, or valid v2 syntax? Some constructs look like v1 but are legal in v2 (e.g., `return` without parens is fine in v2).
3. **Counter-argument**: "What would make this a false positive?" — Is this an intentional choice? Does the v1-style syntax actually work identically in v2 for this specific use case?
4. **Observed vs inferred**: Did you see the v1 pattern directly, or infer it from naming conventions?
5. **Impact**: Does this cause wrong behavior, or is it just stylistic? Wrong behavior is a bug fix; stylistic is lower priority.

## Plan Format

Group by impact (wrong behavior > silent difference > purely stylistic):

| File | Lines | v1 Pattern | Correct v2 | Impact | Evidence |
|------|-------|-----------|------------|--------|---------|
| `file.ahk` | 42 | `Func("MyHandler")` | `MyHandler` (direct ref) | Wrong — creates string, not func ref | Verified lines 40–45 |

Note which findings are also candidates for a new static analysis check (if a v1 pattern can be caught by regex, it could become a `check_batch_*.ps1` sub-check to prevent recurrence).

Ignore any existing plans — create a fresh one.
