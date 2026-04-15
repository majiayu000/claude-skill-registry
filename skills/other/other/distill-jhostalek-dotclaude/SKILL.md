---
name: distill
description: Use when the goal is to reduce code size, remove unnecessary complexity, or simplify a module without removing user-facing behavior.
---

target_module = $ARGUMENTS

If no target module path is provided, ask for one.

**Optional flags** (parse from $ARGUMENTS if present):
- `--tiers 1-3` — run only specified tier range
- `--files foo.py bar.py` — scope to specific files instead of full module

You are the team lead for a distillation. You don't write production code — you orchestrate file-distiller specialists who do. Your job: establish safety, distribute work, handle structural changes (Tier 6), resolve cross-file conflicts, and enforce quality gates.

## Mission

Maximize net LOC reduction while improving or maintaining readability.

**Primary metric:** `git diff --stat` net line delta (negative = good).
**Hard constraint:** Tests pass. External behavior unchanged for auto-applied changes.

## Two Modes

- **Auto-fix** — everything preserving user-facing capabilities. File merges, abstraction collapses, test rewrites, internal API changes — if behavior is preserved and tests pass, just do it.
- **Propose** — user-facing capability removal only (endpoints, tools, CLI commands, features). You can't verify usage patterns, so these need sign-off.

## File-Distiller Teammate

The teammate prompt lives at `${CLAUDE_SKILL_DIR}/agents/file-distiller.md`. Read the prompt file and spawn a teammate with the full content as their prompt. Prepend the file assignment and any dead code scanner findings:

```
You own `{file_path}` (and `{test_file_path}` if applicable).
Dead code scanner findings for this file: {findings or "none available"}
Tier restriction: {tier range or "all tiers"}

<full content of agents/file-distiller.md>
```

Spawn with `isolation: worktree` — prevents mid-flight collisions when teammates edit files that import from each other. Merge each teammate's worktree branch after verifying their changes pass tests.

Why teammates instead of serial analysis: a single context doing file-by-file analysis loses steam after easy wins. It skims Tiers 2-5 and declares "code is tight." Teammates can't — each one has exactly one file and must justify their results.

## Setup

Run tests first. If they fail, stop — distillation requires a passing baseline.

Branch: `git checkout -b distill/$(date +%s)`. Record baseline LOC for the target module. Run dead code scanner (`{dead_code}`) if available — distribute findings to relevant teammates.

Small modules (<500 LOC, <5 files): handle directly without spawning teammates.

## Tier 6 — Structural Simplification (Lead Only)

After all teammates finish, handle cross-file structural work they can't do in isolation:

- **File merges** — single-function files into consumer. Thin `types.py`/`schemas.py`/`exceptions.py` into adjacent modules. Any file under ~30 lines that isn't `__init__.py` — question whether it needs to exist.
- **Abstraction collapse** — ABC/Protocol with one impl: delete ABC. Factory constructing one type: inline. Service class of static methods: module functions.
- **Solution simplification** — complex library when stdlib suffices. Class with state when a function would do.
- **Config knob removal** — knobs always set to the same value in every environment.

**Do not hesitate on structural work.** Moving functions between files feels "risky" because humans fear breaking imports. You grep every reference and fix them all in one pass. The cost of a scattered codebase compounds forever; the cost of a file merge is one edit session.

Fix all import references in one pass. Run full lint + test suite after Tier 6.

## Report

Report `git diff --stat` and reduction percentage against baseline.

If no user-facing features were flagged, just report the stats. Otherwise:

```
## Auto-fix complete: -XX lines (tests pass)

Feature removal — needs your call:

1. **Remove submit_test_feedback tool** — only used during testing phase, never
   called in production. ~-40 lines. Risk: feature removal.

Which should I remove? (e.g., "1" or "all" or "none")
```
