---
name: review-code-quality-open
description: Open Review of code quality
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-review the codebase for code quality and maintainability issues. Use maximum parallelism — spawn explore agents for independent areas.

This is an open ended check (aside from mega-function guidelines below), you determine what you think is code smell or code quality opportunities / issues. 

## CRITICAL — Mega-Function Guidelines

Do **NOT** flag functions for refactoring based on line count alone. Length is not a quality issue.

**SKIP refactoring when the function has:**
- **Single responsibility** — does one coherent thing with many steps (e.g., "process full state", "render overlay", "apply update")
- **Linear/sequential logic** — steps must happen in order, error handling spans multiple steps (update installers, init sequences, transaction-like operations)
- **Performance-critical path** — rendering loops, tick functions, hot paths. Function call overhead matters.
- **Switch/case event handler** — a 150-line switch handling 10 event types is clearer than 10 handler functions with dispatch logic
- **Mirrors external structure** — code structure mirrors an API, protocol, or data format
- **Well-commented sections** — clear section comments within a long function often beat extraction
- **Tested and stable** — working code with passing tests. Refactoring introduces regression risk for no functional gain.

**RECOMMEND refactoring only when:**
- **Multiple unrelated responsibilities** in one function
- **Repeated logic** — same 20+ lines in multiple places with slight variations
- **Deep nesting** — 4+ levels of indentation making flow hard to follow
- **Difficult to test** — can't unit test pieces in isolation when you need to
- **Hard to extend** — adding functionality requires understanding the entire function

**Risk/reward check** before recommending any refactor:
- What bugs or maintenance problems has this function *actually caused*?
- Will extracted functions be reused, or just called from one place?
- Does splitting add indirection that hurts readability?
- If the answer to "what problem does this solve?" is just "it's long" — skip it.

## Explore Strategy

Split by area for parallel scanning:

- `src/gui/` — GUI rendering, state machine, overlay, input
- `src/core/` — Producers (WinEventHook, Komorebi, pumps)
- `src/shared/` — Window list, config, IPC, blacklist, theme, stats
- `src/editors/` — Config/blacklist editors
- `src/pump/` — EnrichmentPump subprocess
- Root `src/` files — Entry points, launcher, installation, update

Exclude `src/lib/` (third-party code).

Use `query_interface.ps1` to compare module public surfaces — similar API shapes across files can reveal DRY violations or misplaced responsibilities. Use `query_function.ps1 <funcName>` to read function bodies when evaluating DRY violations without loading full files. Use `query_callchain.ps1 <funcName> -Reverse` to trace callers when checking whether misplaced logic is called from the expected module or from elsewhere.

## Validation

After explore agents report back, **validate every finding yourself**. Code quality is subjective — what looks like a concern violation may be an intentional design choice for performance or simplicity.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted.
2. **Trace downstream impact**: For DRY violations, show both copies and where they've drifted. For magic numbers, show what would change if the value needed updating.
3. **Counter-argument**: "What would make this fix unnecessary or counterproductive?" — Is the "duplication" actually simpler than the abstraction? Is the magic number only used once and obvious in context?
4. **Observed vs inferred**: Did you find the pattern by reading the code, or infer it from file/function names?

## Plan Format

Group by category:

| Category | File | Lines | Issue | Fix | Counter-argument |
|----------|------|-------|-------|-----|-----------------|
| Magic number | `foo.ahk` | 42 | `Sleep(150)` — grace period, no named constant | Extract to `cfg.GracePeriodMs` or named constant | Only used once, comment explains it |
| DRY | `bar.ahk:30`, `baz.ahk:55` | Duplicate pipe cleanup logic | Extract shared helper | Both are 5 lines, abstraction may not be worth it |

Order by maintenance impact: issues that make future changes error-prone first, purely cosmetic issues last.

Ignore any existing plans — create a fresh one.
