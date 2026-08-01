---
description: Runs an iterative auto-fix loop on a chosen target — review, refactor, or coverage — dispatching the base skill into fresh subagent contexts per iteration, applying fixes automatically without per-change approval, running tests with bisection on failure, and checkpoint-committing until convergence or the cap. Requires /optimus:init and a test command in .claude/CLAUDE.md.
disable-model-invocation: true
argument-hint: "<review|refactor|coverage> [testability|guidelines] [path] [--resume] [--yes] [--max-iterations N | --max-cycles N] [--no-commit] [--focus testability|guidelines] [--allow-red-baseline]"
---

# Deep Mode

Orchestrate a base skill in an iterative auto-fix loop. Each iteration runs in a fresh subagent context, so the loop is not bounded by single-conversation context decay. All state lives in the target's progress file; the `harness_common.cli` helper applies fixes, runs tests, bisects failures, and decides termination.

## Targets

| Target | Base skill (`--skill`) | Progress file | Cap flag (default/hard) | Loop reference | Focus |
|---|---|---|---|---|---|
| `review` | `code-review` | `.claude/code-review-deep-progress.json` | `--max-iterations` 8/20 | `references/orchestrator-loop-single.md` | no |
| `refactor` | `refactor` | `.claude/refactor-deep-progress.json` | `--max-iterations` 8/20 | `references/orchestrator-loop-single.md` | yes |
| `coverage` | `unit-test` | `.claude/unit-test-deep-progress.json` | `--max-cycles` 5/10 | `references/orchestrator-loop-paired.md` | no — pinned to `testability` for its refactor phase; a user-supplied focus is rejected |

The progress-file paths are load-bearing CLI defaults — never rename them. The `coverage` target counts **cycles**, not iterations: each cycle dispatches a unit-test phase (write tests, measure coverage, flag untestable code) and, when untestable items are pending, a refactor phase with testability focus.

## Step 1: Parse Arguments and Guard Against Re-entry

### Re-entry guard

If your invocation prompt body already contains `HARNESS_MODE_INLINE`, stop immediately with: *"Deep mode cannot run inside deep mode."* This prevents a misbehaving subagent from spawning a recursive deep run.

### Parse invocation arguments

1. Target — the first standalone token must be `review`, `refactor`, or `coverage`; otherwise stop and show the usage from the argument hint. All table lookups below use this target's row.
2. `--resume` and `--no-commit` flags (present/absent)
3. `--yes` flag — auto-confirm every confirmation prompt in this skill (the Step 3 prompt and Step 4's coverage red-baseline confirmation); required when invoked under `claude -p` or any other non-interactive session that cannot answer `AskUserQuestion`.
4. Cap — the target's cap flag from the table (`--max-iterations N` or `--max-cycles N`), default and hard cap per the table.
5. Focus — refactor target only; stop on any other value or any other target (the CLI rejects both). Accept **either** `--focus testability|guidelines` **or** a bare `testability`/`guidelines` token, applying the **Focus** detection rules in `$CLAUDE_PLUGIN_ROOT/skills/refactor/SKILL.md` — read that section when parsing this item; it is the single source for the rule (do not paraphrase it here). A token consumed as focus is removed from the scope text before item 7 — otherwise `deep refactor guidelines src` would lose the `src` path scope.
6. `--allow-red-baseline` — review/refactor only; coverage always tolerates a red baseline (see Step 4).
7. Everything else → scope text. An existing path scopes the run to that path; any other text is recorded as intent only — it does **not** filter. Default scope: `review` covers the branch diff; `refactor` covers the feature-branch diff when one exists, otherwise the full project, widening per iteration to files with active findings and newly modified files; `coverage` covers the full project.

Headless / CI example (skips the Step 3 confirmation): `claude -p "/optimus:deep review --yes src/auth"`.

## Step 2: Pre-flight Checks

### Plugin root

Resolve `plugin_root` (the absolute path to the installed plugin) and keep it for every CLI call and subagent dispatch below — the env var does not persist across separate Bash tool calls and reads empty on some platforms (notably Windows):

1. Run `echo $CLAUDE_PLUGIN_ROOT` via Bash. If it is non-empty **and** `<value>/scripts/harness_common` exists (`test -d`), use it.
2. Otherwise derive the root from the "Base directory for this skill:" line in your invocation context — strip the trailing `/skills/...` segment (this skill's own directory) — and use it if `<derived>/scripts/harness_common` exists.
3. If neither candidate contains `scripts/harness_common`, stop: *"Cannot resolve plugin root — ensure optimus-claude is installed via the Claude Code plugin system."*

Wherever the steps below (and `orchestrator-loop-*.md`) write `$CLAUDE_PLUGIN_ROOT`, use this resolved `plugin_root`; if `echo $CLAUDE_PLUGIN_ROOT` was empty, substitute the absolute path literally.

### Prerequisites

If `.claude/CLAUDE.md` is missing, stop: *"Deep mode requires `/optimus:init` to set up project context first."*

### Test command

Read `.claude/CLAUDE.md` and capture the documented test command verbatim (e.g. `npm test`, `pytest`) as `test_command` — the auto-fix loop has no safety net without one, so if none is documented, stop and recommend `/optimus:init`. Pass this captured command to `init` in Step 4 via `--test-command` (the CLI's own CLAUDE.md parser is stricter than a human read — passing the string you read avoids a spurious "No test command found" failure).

For `coverage`: if `/optimus:init` flagged the test framework as missing or "installed but no tests yet," warn the user but proceed — the unit-test phase will surface the gap.

### Git state

On a fresh (non-`--resume`) run, refuse to proceed if the working tree has uncommitted changes unless `--no-commit` is passed — uncommitted state would be ambiguous with the orchestrator's own checkpoint commits. On `--resume`, the existing progress file's `_snapshot.pre_head` is the recovery anchor; uncommitted state is preserved.

## Step 3: User Confirmation

Skip this step entirely when `--resume` is given, or when `--yes` is given (headless / CI: the caller has pre-approved the run).

Warn the user with:

> **Deep mode ([target])** runs up to [N] iterative fix passes (cycles for `coverage`, each up to two subagent dispatches). Every pass spawns fresh subagents — credit and time consumption multiplies with the count. Fixes are applied automatically without per-change approval. Low test coverage increases the chance of undetected breakage; consider running `/optimus:unit-test` first to strengthen the safety net. Press Esc twice to interrupt — state is saved per iteration; resume with `/optimus:deep [target] --resume`.
>
> Test command: `[test command]`
> Focus: `[focus or "balanced"]` *(refactor target only)*
>
> Mid-iteration interrupts may leave the working tree inconsistent; clean iterations are fully recoverable via `--resume`.

Use `AskUserQuestion` — header "Deep mode", question "Proceed with deep [target]?":
- **Proceed** — "Run the loop until clean (max [N] iterations/cycles)"
- **Cancel** — "Don't run deep mode"

If the user selects **Cancel**, stop.

## Step 4: Initialize or Resume Progress

Read `$CLAUDE_PLUGIN_ROOT/references/harness-init-resume.md` and apply its shared init/resume semantics — the `resume` invocation and cap raising, `init` error recovery (a prior run is discarded by re-invoking `init` with `--force`), `--no-commit` persistence, and `.done.json` archival — with `<progress-path>` and `<cap-flag>` from the Targets table.

### On fresh run

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli init \
    --skill <base-skill> \
    <cap-flag> [N] \
    --test-command "<test_command>" \
    [--focus testability | --focus guidelines] \
    [--scope "<scope>"] \
    [--no-commit] \
    --progress-file "<progress-path>" \
    --project-dir "."
```

Pass `--focus` only for the refactor target, and only with the value from Step 1.

### Baseline

Run `cli baseline` before entering the loop. Skip it on `--resume` only when the progress file's completed counter is greater than 0 — `iteration.completed` for the review and refactor targets, `cycle.completed` for the coverage target (a targeted read — do not load the `findings` array into context); if it is 0, the prior run never entered the loop and `resume` never re-checks the baseline — run it after `resume`.

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/scripts" python -m harness_common.cli baseline \
    --progress-file "<progress-path>" \
    [--allow-red]
```

`baseline` runs the test command once and calibrates the per-iteration timeout from its duration. Per target:

- **review / refactor** — green required. On `baseline-red`, stop and show the failing tests (a red starting tree makes bisection blame the iteration's fixes and revert good work); the user can fix them or re-run with `--allow-red-baseline`. Pass the CLI `--allow-red` only when the user supplied `--allow-red-baseline` — the CLI's own failure message names its internal flag, not the skill flag.
- **coverage** — always pass `--allow-red`: a coverage run legitimately starts with little or no passing coverage. If the CLI prints `baseline-red-allowed` and the project already has tests (or the baseline hit the test timeout), warn the user and confirm before entering the loop — under `--yes`, print the warning and proceed without confirming: a failing suite trips the unit-test phase's `blocked` stop gate at cycle 1, and a timing-out suite silently rolls every cycle's tests back.

## Step 5: Run the Loop

Read the target's loop reference — `$CLAUDE_PLUGIN_ROOT/references/orchestrator-loop-single.md` (review, refactor) or `$CLAUDE_PLUGIN_ROOT/references/orchestrator-loop-paired.md` (coverage) — and follow its per-iteration body exactly, with:

- `<base-skill>` = the table's base skill
- `<progress-path>` = the table's progress file
- `<max>` = the cap from Step 1

Refactor target: when a focus is set, add `Focus: <testability|guidelines>` to the dispatch prompt after the `Phase:` line (the base skill reads `config.focus` from the progress file; the echo makes the intent visible in the run trace).

Coverage target: the paired loop's blocked gate (a non-null `blocked` field from the unit-test phase) exits the loop instead of dispatching further cycles — record it with `mark-termination --reason blocked` as the loop reference specifies, then report the reason with matching recovery advice (`/optimus:init` for a missing framework or broken build; triage the failing tests for a red baseline). The run stays resumable: tell the user to re-run with `--resume` once the prerequisite is fixed.

Do not narrate subagent findings in conversation prose — the final report covers them.

## Step 6: Final Report

After the loop, follow the loop reference's "After the loop" section. For a fresh second-opinion pass after a clean finish, re-run `/optimus:deep <target>` without `--resume`.

## Important

Approval recorded at Step 3 stands for the entire loop — fixes are applied without per-change confirmation. The base skill's harness-mode protocol is the source of truth for which fixes get applied.

Recommend `/optimus:commit` next, then `/optimus:pr` once the branch is ready — the user should stay in this conversation for those so the implementation context is captured.
