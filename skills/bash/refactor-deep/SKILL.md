---
description: Iterative project-wide refactoring — runs `/optimus:refactor` in a fresh subagent context per iteration, applies fixes, runs tests, bisects failures, and continues until convergence or the iteration cap (default 8, hard cap 20). Supports `testability` or `guidelines` focus to prioritize finding categories. Each iteration runs in an isolated subagent so context does not accumulate. Requires a test command in .claude/CLAUDE.md. Use for thorough guideline alignment or testability cleanup before /optimus:unit-test.
disable-model-invocation: true
---

# Project Refactor (Deep)

Orchestrate `/optimus:refactor` in an iterative cleanup loop. Each iteration runs in a fresh subagent context. All state lives in `.claude/refactor-deep-progress.json`. The orchestrator dispatches subagents, parses their structured output, and uses the `harness_common.cli` helper to apply fixes, run tests, bisect failures, and decide termination.

## Step 1: Parse Arguments and Guard Against Re-entry

### Re-entry guard

If your invocation prompt body already contains `HARNESS_MODE_INLINE`, stop immediately with: *"Deep mode cannot run inside deep mode."*

### Parse invocation arguments

Extract from the user's arguments:
1. `--resume` flag (present/absent)
2. `--no-commit` flag (present/absent)
3. `--yes` flag (present/absent) — auto-confirm the Step 3 prompt; required when invoked under `claude -p` or any other non-interactive session that cannot answer `AskUserQuestion`.
4. `--max-iterations N` (optional, default 8, hard cap 20)
5. Focus keyword (standalone unquoted token): `testability` or `guidelines` (the same detection rules as `/optimus:refactor` — see `skills/refactor/SKILL.md` Step 1)
6. `--allow-red-baseline` flag (present/absent) — proceed even if the Step 4 pre-loop baseline finds the suite already failing
7. Everything else → scope text (an existing path scopes the refactor to that path; other text is recorded as intent only and does **not** filter — the full branch diff is still processed)

Examples:
- `/optimus:refactor-deep` → full project, 8 iterations, balanced focus
- `/optimus:refactor-deep testability` → focus on testability barriers
- `/optimus:refactor-deep guidelines src/backend` → guidelines focus, scoped to an existing path
- `/optimus:refactor-deep --max-iterations 12` → 12 iterations
- `/optimus:refactor-deep --resume` → continue from existing progress file
- `/optimus:refactor-deep --no-commit` → skip per-iteration checkpoint commits
- `claude -p "/optimus:refactor-deep --yes testability"` → headless / CI usage; skips the Step 3 confirmation prompt

## Step 2: Pre-flight Checks

### Plugin root

Resolve `plugin_root` (the absolute path to the installed plugin) and keep it for every CLI call and subagent dispatch below — the env var does not persist across separate Bash tool calls and reads empty on some platforms (notably Windows):

1. Run `echo $CLAUDE_PLUGIN_ROOT` via Bash. If it is non-empty **and** `<value>/scripts/harness_common` exists (`test -d`), use it.
2. Otherwise derive the root from the "Base directory for this skill:" line in your invocation context — strip the trailing `/skills/...` segment (this skill's own directory) — and use it if `<derived>/scripts/harness_common` exists.
3. If neither candidate contains `scripts/harness_common`, stop: *"Cannot resolve plugin root — ensure optimus-claude is installed via the Claude Code plugin system."*

Wherever the steps below (and `orchestrator-loop-*.md`) write `$CLAUDE_PLUGIN_ROOT`, use this resolved `plugin_root`; if `echo $CLAUDE_PLUGIN_ROOT` was empty, substitute the absolute path literally.

### Documentation prerequisites

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/prerequisite-check.md` and apply the prerequisite check. If `.claude/CLAUDE.md` is missing, stop: *"Deep mode requires `/optimus:init` to set up project context first."*

### Test command

Read `.claude/CLAUDE.md` and capture the documented test command verbatim — store the exact string (e.g. `npm test`, `pytest`) as `test_command`. If none is documented, stop and recommend `/optimus:init` to set one up first. You pass this captured command to `init` in Step 4 via `--test-command`; `init` can also parse `.claude/CLAUDE.md` itself, but its parser is stricter than a human read, so passing the command you just read avoids a spurious "No test command found" failure on a command the CLI can't parse.

### Git state

On a fresh (non-`--resume`) run, refuse to proceed if the working tree has uncommitted changes unless `--no-commit` is passed. On `--resume`, the existing progress file's `_snapshot.pre_head` is the recovery anchor.

## Step 3: User Confirmation

Skip this step entirely when `--resume` is given, or when `--yes` is given (headless / CI: the caller has pre-approved the run).

Warn the user with:

> **Deep refactor** runs up to [N] iterative refactor passes. Each iteration spawns a fresh subagent — credit and time consumption multiplies with iteration count. Fixes are applied automatically at each iteration without per-change approval. Low test coverage increases the chance of undetected breakage; consider running `/optimus:unit-test` first to strengthen the safety net. Press Esc twice to interrupt — state is saved per-iteration; resume with `/optimus:refactor-deep --resume`.
>
> Test command: `[test command]`
> Focus: `[focus or "balanced"]`

Use `AskUserQuestion` — header "Deep refactor", question "Proceed with deep refactor?":
- **Proceed** — "Run iterative refactor until clean (max [N] iterations)"
- **Cancel** — "Don't run deep mode"

If the user selects **Cancel**, stop.

## Step 4: Initialize or Resume Progress

### On `--resume`

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli resume \
    --progress-file ".claude/refactor-deep-progress.json" \
    [--max-iterations N] \
    --project-dir "."
```

Pass `--max-iterations N` through when the user supplied a higher cap on `--resume` — `resume` raises the persisted iteration cap (and clears a prior `diminishing-returns` stop) so the loop continues past the previous limit. A run that finished cleanly is archived to `.done.json`; `--resume` only continues a still-on-disk run (interrupt or `diminishing-returns`).

### On fresh run

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli init \
    --skill refactor \
    --max-iterations [N] \
    --test-command "<test_command>" \
    [--focus testability | --focus guidelines] \
    [--scope "<scope>"] \
    [--no-commit] \
    --progress-file ".claude/refactor-deep-progress.json" \
    --project-dir "."
```

Pass `--no-commit` through to `init` when the user supplied it — the mode is persisted in the progress file, so `--resume` keeps it without re-passing the flag (and `commit-checkpoint` self-skips regardless).

If `--focus` is supplied with anything other than `testability` or `guidelines`, the CLI rejects it.

If `init` reports *"progress file already exists"*, a prior un-archived run is on disk. Either run with `--resume` to continue it, or re-invoke `init` with `--force` to discard the prior progress.

### Establish a green baseline (fresh runs only)

Skip on `--resume` — the baseline already ran and the calibrated timeout is persisted. On a fresh run, after `init` succeeds, verify the suite is green before the loop:

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli baseline \
    --progress-file ".claude/refactor-deep-progress.json" \
    [--allow-red]
```

`baseline` runs the test command once and calibrates the per-iteration timeout from how long it takes (so a slow suite, re-run repeatedly during bisection, doesn't spuriously time out). It prints `baseline-green` (continue) or, on a failing suite, `baseline-red` with a non-zero exit. On `baseline-red`, stop and show the user the failing tests — a red starting tree makes bisection blame the iteration's fixes and revert good work. Pass `--allow-red` only when the user supplied `--allow-red-baseline` (proceed without a green safety net; the timeout is left at its default).

## Step 5: Run the Iteration Loop

Read `$CLAUDE_PLUGIN_ROOT/references/orchestrator-loop-single.md` and follow its 8-step per-iteration body, with these parameters:

- `<base-skill>` = `refactor`
- `<progress-path>` = `.claude/refactor-deep-progress.json`
- `<max>` = the iteration cap from Step 1

When dispatching the refactor subagent, include the focus keyword in the prompt body if one was set:

```
... Phase: refactor
    Focus: <testability|guidelines>
...
```

The base skill reads `config.focus` from the progress file (the CLI's `init` recorded it there) and applies the finding-cap weighting accordingly — but echoing the focus into the dispatch prompt makes the intent visible to anyone reading the run trace.

## Step 6: Final Report

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli final-report \
    --progress-file ".claude/refactor-deep-progress.json" \
    --archive
```

This prints the cumulative report and archives the run — except on a `diminishing-returns` soft-exit, which the CLI leaves un-archived (prints `not-archived`) so it stays resumable via `--resume`.

## Important

User approval recorded at Step 3 stands for the entire loop — fixes are applied without per-change confirmation. Recommend `/optimus:commit` next, followed by `/optimus:pr` once the branch is ready. Tell the user: **Tip:** stay in this conversation when running `/optimus:commit` and `/optimus:pr` so the implementation context is captured. Other downstream skills (`/optimus:code-review`, `/optimus:unit-test`) should still run in fresh conversations.

## Tip

If the project has low test coverage and you suspect testability barriers are blocking better coverage, run with `testability` focus first; then re-run with `guidelines` focus (in a fresh conversation) to align style and convention violations once tests are in place.
