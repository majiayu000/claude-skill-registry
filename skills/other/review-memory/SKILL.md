---
name: review-memory
description: Audit CLAUDE.md and .claude/rules/ for stale references, outdated architecture claims, and rules now redundant with static analysis checks
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit the project's persistent AI context files for factual accuracy against the current codebase. The goal is to find landmines — stale knowledge that would actively mislead a future session.

## Philosophy

These files are terse by design. Every line costs context tokens every session. Brevity was hard-won. This skill does NOT:
- Suggest adding new rules or expanding existing ones
- Recommend rewording for "clarity" (clarity costs tokens)
- Question whether a rule is *needed* — the human knows the history of why each rule exists
- Suggest new patterns, conventions, or best practices

This skill ONLY checks: **is what's written here still true?**

## Scope

- `CLAUDE.md` — main project instructions
- `.claude/rules/*.md` — domain-specific knowledge files
- The table in `CLAUDE.md` that indexes the rules files

## Phase 1 — Identifier Verification (Mechanical, High Confidence)

For every concrete identifier referenced in these files, verify it exists in the current codebase.

### What to verify

- **File paths** — `src/gui/gui_data.ahk`, `src/shared/config_registry.ahk`, etc. Do they exist at those paths?
- **Function names** — `WL_UpsertWindow()`, `Blacklist_IsWindowEligible()`, `_WS_GetOpt()`, etc. Do they exist? Use `query_function_visibility.ps1`.
- **Global variable names** — `gGUI_DisplayItems`, `StorePipeName`, etc. Do they exist? Use `query_global_ownership.ps1`.
- **Config keys** — any setting name referenced. Does it exist in the config registry? Use `query_config.ps1`.
- **Tool/script names** — `check_globals.ps1`, `query_global_ownership.ps1`, `shader_bundle.ps1`, etc. Do they exist at the referenced location?
- **Check names** — specific check names referenced (e.g., `check_critical_leaks`). Do they exist as standalone scripts or sub-checks in batch bundles?
- **Command-line flags** — `--gui-only`, `--pump`, `--config`, etc. Are they still handled in the entry point?
- **IPC message types** — any `IPC_MSG_*` referenced. Do they exist?

### Classification

- **Broken** — identifier doesn't exist. An AI following this instruction will be confused.
- **Renamed** — old name gone, similar new name exists. Needs updating.
- **Moved** — exists but at a different path than documented.
- **Current** — verified correct. No action.

## Phase 2 — Architecture Claim Verification (Medium Confidence)

The rules files make factual claims about how the system works. Verify the significant ones against actual code.

### What to verify

- **Process model** — does the process model described in `architecture.md` match `alt_tabby.ahk`'s mode routing? Are all modes listed? Any new ones missing?
- **Key files table** — does the "Key Files" section list files that exist with accurate descriptions of what they contain?
- **Producer list** — are all producers listed? Any new ones not mentioned?
- **State machine** — does the state diagram match the actual states in the code?
- **Compositor stack** — does the layer ordering match `gui_effects.ahk` / `gui_paint.ahk`?
- **Config system description** — does it match how `config_registry.ahk` actually works? Are the registry entry fields (`s`, `k`, `g`, `t`, `default`, `d`, `min`, `max`, `fmt`) still accurate?
- **IPC architecture** — does the described pipe protocol match the actual implementation?
- **Keyboard hook defense stack** — are all the defense layers listed in `keyboard-hooks.md` still present in the code?

Don't verify every claim — focus on structural claims that, if wrong, would lead an AI to make incorrect architectural decisions.

### Classification

- **Contradicts code** — the code does Y, the rule says X. One of them changed and the other didn't keep up.
- **Incomplete** — a list or description is missing entries that now exist (e.g., new producer, new state, new compositor layer). The existing entries are correct.
- **Current** — verified correct.

## Phase 3 — Redundancy with Static Analysis (High Value)

Rules that are now mechanically enforced by static analysis checks are the best candidates for removal — the check does the job better and costs zero context.

For each rule in CLAUDE.md and the rules files that describes a coding pattern to follow or avoid:
1. Check if a corresponding `check_*.ps1` (or sub-check in a batch bundle) enforces this mechanically
2. If yes, flag it as **Redundant — enforced by [check name]**

The rule should still exist if it explains *why* (the AI needs to understand the principle to write correct code). But if the rule is purely "do X, don't do Y" with no judgment component, and a check enforces it, the rule can likely go.

Examples of what this catches:
- "Always declare globals inside functions" — if `check_globals` in `check_batch_functions.ps1` catches this, the rule is redundant as enforcement (though the explanation of AHK v2 scoping may still be needed)
- "Don't call `_Private()` functions cross-file" — if `query_function_visibility.ps1 -Check` enforces this, the rule is redundant

## Phase 4 — Rules Index Table

`CLAUDE.md` has a table mapping `.claude/rules/` files to their contents:

```
| File | Contents |
|------|----------|
| `ahk-patterns.md` | AHK v2 syntax, race conditions, ... |
```

Verify:
- Every file listed in the table exists
- Every `.md` file in `.claude/rules/` is listed in the table
- The one-line descriptions roughly match actual file content (don't nitpick — just catch "file was completely rewritten but description is from the old version")

## Phase 5 — File Size Check

Report the line count of each file:

| File | Lines |
|------|-------|
| `CLAUDE.md` | N |
| `.claude/rules/ahk-patterns.md` | N |
| ... | ... |

No threshold — just surface the numbers so the human can spot gradual bloat. Flag any file over 150 lines as worth a glance, since these load every session.

## Explore Strategy

Run in parallel by file — each rules file is independent:
- **Agent 1**: `CLAUDE.md` (identifiers, architecture claims, rules index table)
- **Agent 2**: `ahk-patterns.md` + `keyboard-hooks.md` (identifiers, patterns vs checks)
- **Agent 3**: `architecture.md` + `komorebi.md` (architecture claims, producer list, state machine)
- **Agent 4**: `testing.md` + `debugging.md` + `workflow.md` + `installation.md` (identifiers, tool references)

After agents report, do Phase 3 (redundancy check) yourself — it requires cross-referencing rules against check scripts.

## Output Format

### Mechanical Issues

Objectively wrong — identifiers, paths, names.

| File | Reference | Type | Status | Details |
|------|-----------|------|--------|---------|
| `architecture.md` | `src/gui/gui_store.ahk` | File path | Renamed | Now `src/gui/gui_data.ahk` |
| `CLAUDE.md` | `_WS_GetOpt()` | Function | Broken | Function no longer exists |
| `ahk-patterns.md` | `check_globals.ps1` | Script | Moved | Now a sub-check in `check_batch_functions.ps1` |

### Architecture Drift

Claims that contradict or lag behind the current code.

| File | Claim | Reality | Impact |
|------|-------|---------|--------|
| `architecture.md` | Compositor has 7 layers | Code shows 9 layers | AI will miss layers when reasoning about paint order |
| `architecture.md` | "EnrichmentPump" section missing stats flush | Stats flush now runs in pump | AI may put stats work in MainProcess |

### Redundancy Candidates

Rules now enforced by static analysis. Human decides whether the explanation is still worth the context cost.

| File | Rule | Enforced by | Recommendation |
|------|------|-------------|----------------|
| `CLAUDE.md` | Global declaration requirement | `check_globals` in `check_batch_functions.ps1` | Keep explanation of *why*, remove the "must do" directive |
| `ahk-patterns.md` | No cross-file `_Func()` calls | `query_function_visibility.ps1 -Check` | Rule is pure enforcement — check handles it |

### File Sizes

| File | Lines | Note |
|------|-------|------|
| `CLAUDE.md` | N | |
| `.claude/rules/ahk-patterns.md` | N | |
| ... | ... | |

### Index Table Discrepancies

Any mismatch between the rules index in `CLAUDE.md` and the actual `.claude/rules/` directory.

Order all tables by impact: broken references that cause wrong decisions first, cosmetic issues last.

Ignore any existing plans — create a fresh one.
