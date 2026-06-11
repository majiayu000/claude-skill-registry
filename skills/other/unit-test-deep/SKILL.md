---
description: Iterative test-coverage improvement loop — dispatches `/optimus:unit-test` (unit-test phase) and `/optimus:refactor` with testability focus (refactor phase) into fresh subagent contexts per cycle, applies tests, runs the test suite, bisects refactor failures, and continues until coverage plateaus or the cycle cap (default 5, hard cap 10). Use to drive coverage up on a codebase that has untestable barriers — the loop alternates between writing tests and unblocking testability so a single skill cannot stall.
disable-model-invocation: true
---

# Unit-Test Coverage Improvement (Deep)

Orchestrate paired cycles of test generation and testability refactoring. Each cycle is two subagent dispatches: first `/optimus:unit-test` (writes tests, measures coverage, flags untestable code), then `/optimus:refactor` with focus on testability (unblocks the flagged items so the next cycle can cover them). All state lives in `.claude/unit-test-deep-progress.json`.

## Step 1: Parse Arguments and Guard Against Re-entry

### Re-entry guard

If your invocation prompt body already contains `HARNESS_MODE_INLINE`, stop immediately with: *"Deep mode cannot run inside deep mode."*

### Parse invocation arguments

Extract from the user's arguments:
1. `--resume` flag (present/absent)
2. `--no-commit` flag (present/absent)
3. `--yes` flag (present/absent) — auto-confirm the Step 3 prompt; required when invoked under `claude -p` or any other non-interactive session that cannot answer `AskUserQuestion`.
4. `--max-cycles N` (optional, default 5, hard cap 10)
5. Everything else → scope text (optional path filter)

Examples:
- `/optimus:unit-test-deep` → 5 cycles, full project
- `/optimus:unit-test-deep --max-cycles 8` → 8 cycles
- `/optimus:unit-test-deep src/api` → scoped
- `/optimus:unit-test-deep --resume` → continue from existing progress file
- `/optimus:unit-test-deep --no-commit` → skip per-phase checkpoint commits
- `claude -p "/optimus:unit-test-deep --yes src/api"` → headless / CI usage; skips the Step 3 confirmation prompt

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

Read `.claude/CLAUDE.md` and capture the documented test command verbatim — store the exact string (e.g. `npm test`, `pytest`) as `test_command`. If none is documented, stop and recommend `/optimus:init` to set one up first (the auto-fix loop has no safety net without a test command). You pass this captured command to `init` in Step 4 via `--test-command`; `init` can also parse `.claude/CLAUDE.md` itself, but its parser is stricter than a human read, so passing the command you just read avoids a spurious "No test command found" failure on a command the CLI can't parse.

### Test infrastructure

The base `/optimus:unit-test` skill requires a test framework to be installed. If `/optimus:init` flagged the test framework as missing or "installed but no tests yet," warn the user but proceed — the unit-test phase will surface the gap.

### Git state

On a fresh (non-`--resume`) run, refuse to proceed if the working tree has uncommitted changes unless `--no-commit` is passed.

## Step 3: User Confirmation

Skip this step entirely when `--resume` is given, or when `--yes` is given (headless / CI: the caller has pre-approved the run).

Warn the user with:

> **Deep unit-test mode** runs up to [N] cycles. Each cycle is two subagent dispatches: a unit-test phase that writes tests + measures coverage, and a refactor phase (only when the first phase flags untestable code) that unblocks testability barriers. Credit and time consumption multiplies with cycle count. Tests and refactor fixes are applied automatically without per-change approval. Press Esc twice to interrupt — state is saved per-phase; resume with `/optimus:unit-test-deep --resume`.
>
> Test command: `[test command]`

Use `AskUserQuestion` — header "Deep unit-test", question "Proceed with deep unit-test?":
- **Proceed** — "Run the unit-test + refactor cycle loop (max [N] cycles)"
- **Cancel** — "Don't run deep mode"

If the user selects **Cancel**, stop.

## Step 4: Initialize or Resume Progress

### On `--resume`

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli resume \
    --progress-file ".claude/unit-test-deep-progress.json" \
    [--max-cycles N] \
    --project-dir "."
```

Pass `--max-cycles N` through when the user supplied a higher cap on `--resume` — `resume` raises the persisted cycle cap (and clears a prior `diminishing-returns` stop) so the loop continues past the previous limit. A run that finished cleanly is archived to `.done.json`; `--resume` only continues a still-on-disk run (interrupt or `diminishing-returns`).

### On fresh run

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli init \
    --skill unit-test \
    --max-cycles [N] \
    --test-command "<test_command>" \
    [--scope "<scope>"] \
    [--no-commit] \
    --progress-file ".claude/unit-test-deep-progress.json" \
    --project-dir "."
```

Pass `--no-commit` through to `init` when the user supplied it — the mode is persisted in the progress file, so `--resume` keeps it without re-passing the flag (and `commit-checkpoint` self-skips regardless).

If `init` reports *"progress file already exists"*, a prior un-archived run is on disk. Either run with `--resume` to continue it, or re-invoke `init` with `--force` to discard the prior progress.

### Establish a baseline (fresh runs only)

Skip on `--resume`. On a fresh run, after `init` succeeds, run the baseline once to calibrate the per-cycle test timeout:

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli baseline \
    --progress-file ".claude/unit-test-deep-progress.json" \
    --allow-red
```

`--allow-red` is passed unconditionally here: a coverage run legitimately starts with little or no passing test coverage, so a non-green baseline is not a reason to refuse. When the suite is green the command calibrates the per-cycle timeout from the measured duration (so a slow suite doesn't spuriously time out during bisection); when it isn't, it proceeds and leaves the timeout at its default.

## Step 5: Run the Cycle Loop

Read `$CLAUDE_PLUGIN_ROOT/references/orchestrator-loop-paired.md` and follow its 11-step per-cycle body, with these parameters:

- `<progress-path>` = `.claude/unit-test-deep-progress.json`
- `<max>` = the cycle cap from Step 1

The paired-loop template handles:
- Dispatching the unit-test subagent with `Phase: unit-test`
- Recording the unit-test phase outputs (tests, coverage history, untestable items)
- Checkpoint commit for the unit-test phase
- Conditionally dispatching the refactor subagent with `Phase: refactor` (only when pending untestable items exist)
- Recording the refactor phase outputs (with bisection on test failure)
- Checkpoint commit for the refactor phase
- Recording cycle history + advancing the cycle counter
- Termination check (`continue`, `convergence`, `cap`, `diminishing-returns`)

Brief per-phase status updates are appropriate (e.g., *"Cycle 2/5 unit-test: dispatching subagent…"*, *"Cycle 2/5 refactor: applied 3 fixes, tests pass."*). Do not narrate the subagent's findings in conversation prose — the report at Step 6 covers them.

## Step 6: Final Report

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli final-report \
    --progress-file ".claude/unit-test-deep-progress.json" \
    --archive
```

The report prints cycles completed, coverage baseline → final, total tests written (with file count), testability fixes applied, untestable items still pending, bugs discovered (if any), the termination reason, and git rollback guidance. The run is then archived — except on a `diminishing-returns` soft-exit, which the CLI leaves un-archived (prints `not-archived`) so it stays resumable via `--resume`.

## Important

User approval recorded at Step 3 stands for the entire loop — tests and refactor fixes are applied without per-change confirmation. Recommend `/optimus:commit` next, followed by `/optimus:pr` once the branch is ready. Tell the user: **Tip:** stay in this conversation when running `/optimus:commit` and `/optimus:pr` so the implementation context is captured. Other downstream skills (`/optimus:code-review`, `/optimus:unit-test`) should still run in fresh conversations.

## Tip

Unit-test-deep is the most expensive of the three orchestrator skills — each cycle is two subagent dispatches plus a full test-suite run after each. Default 5 cycles is appropriate for most codebases; raise it only when the project has substantial untestable code that takes multiple refactor rounds to unblock.
