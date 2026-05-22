---
name: develop
description: Unified development orchestrator with three modes — feature (TDD-first new capability), fix (reproduce-first bug resolution), refactor (test-first code quality). Each mode includes a built-in self-review gate before the shared quality stack and progressive review loop.
argument-hint: feature|fix|refactor|plan <goal>
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, TaskCreate, TaskUpdate
---

<objective>

Implement software changes with disciplined, test-driven workflows. The mode determines the entry contract:

- **feature**: TDD-first — validate demo → implement → review+fix loop (max 3 cycles) → doc → quality stack + review
- **fix**: reproduce-first — validate reproduction → apply minimal fix → review+fix loop (max 3 cycles) → quality stack + review
- **refactor**: test-first — validate coverage audit → characterization tests → refactor → review+fix loop (max 3 cycles) → quality stack + review
- **plan**: analysis-only — classify + scope → write structured plan to `tasks/todo.md` → exit (no code)

Each mode includes two layers of built-in review before the shared quality stack:

1. **Step 2 review** — validate the artifact (demo, regression test, or coverage audit) before writing any implementation
2. **Step 4/5 review+fix loop** — review the implementation, fix all gaps, loop (max 3 cycles) until only nits remain

Both layers are in-context (no agent spawn). They catch design mismatches, scope creep, and missing edge cases early so `/review` validates rather than discovers.

All modes share a quality stack, a mandatory Codex pre-pass, and a progressive review loop that narrows scope across cycles.

</objective>

<inputs>

- **$ARGUMENTS**: required
  - First token: `feature`, `fix`, `refactor`, or `plan`
  - Remaining tokens: mode-specific arguments (description, issue #, file path, etc.)
  - `--team` flag (anywhere in arguments): triggers team mode for the active mode

Examples:

- `/develop feature add batched predict() method to Classifier in src/classifier`
- `/develop fix 123`
- `/develop fix TypeError when passing None to transform()`
- `/develop refactor simplify error handling in src/transforms.py`
- `/develop feature --team add authentication flow`
- `/develop plan improve caching in the data loader`

</inputs>

<workflow>

**Task tracking**: immediately after Step 0 (mode is known), create TaskCreate entries for **all steps of the chosen mode's workflow** before doing any other work. This gives the user an instant view of the full plan. Mark each step in_progress when starting it, completed when done. On loop retry or scope change, create a new task or rename the existing one with TaskUpdate.

**`plan` mode shortcut**: if mode is `plan`, read `modes/plan.md` and execute its steps directly — skip Steps 1–2 below and all shared steps (quality stack, Codex pre-pass, review loop). Exit after the plan mode's final output.

## Step 0: Parse mode

Extract the first token from `$ARGUMENTS` as the mode. Valid values: `feature`, `fix`, `refactor`, `plan`.

If the first token is not a valid mode, stop and present the usage:

```
Usage: /develop <mode> <description>
Modes: feature, fix, refactor, plan
```

Strip the mode token from arguments — the remainder is passed to mode-specific steps.

Detect `--team` flag: if present anywhere in arguments, enable team mode (see ## Team Mode section).

## Step 1: Scope analysis

Read `.claude/skills/develop/modes/<mode>.md` and run its **## Step 1** instructions.

This step produces a scope analysis that is used by all subsequent steps.

**Gate**: if the mode file's Step 1 flags a complexity smell (feature: 8+ files / 2+ new classes; fix: root cause spans 3+ modules; refactor: directory-wide scope without explicit goal), present the scope concern to the user before proceeding.

## Step 2: Mode-specific steps

Read `.claude/skills/develop/modes/<mode>.md` and execute its steps in order (Step 2 onward).

The mode file defines all steps specific to that workflow (TDD loop, regression test, characterization tests, etc.).

## Shared Step: Quality stack

Run after all mode-specific steps complete:

```bash
# Linting and formatting
uv run ruff check <changed_files> --fix
uv run ruff format <changed_files>

# Type checking
uv run mypy <changed_files> --no-error-summary 2>&1 | head -30

# Full test suite
python -m pytest <test_dir> -v --tb=short -q

# Doctests (if applicable)
python -m pytest --doctest-modules <target_module> -v 2>&1 | tail -20
```

Spawn a **linting-expert** agent if mypy or ruff issues require non-trivial fixes.

## Shared Step: Codex pre-pass

Mandatory after the quality stack completes. Gracefully degrades if Codex is unavailable.

Read `.claude/skills/_shared/codex-prepass.md` and apply it to the current diff:

1. **Pre-flight**: `which codex` — if not installed, print `⚠ Codex not available — skipping pre-pass` and proceed
2. **Skip check**: if `git diff HEAD --stat` shows only formatting/comment/whitespace changes, skip
3. **Dispatch**: run the Codex pre-pass on the implementation diff:
   ```bash
   codex exec "Review the staged diff (git diff HEAD). Flag bugs, missed edge cases, incorrect logic, and inconsistencies with existing code patterns. Apply minimal targeted fixes — do not make architectural changes. Skip cosmetic nits." --sandbox workspace-write
   ```
   > **Sandbox note**: `--sandbox workspace-write` allows Codex to write source files in the workdir and `/tmp`, but blocks `.git/` paths (e.g. `.git/index.lock`) — so Codex can fix files but cannot stage or commit them; use `git diff HEAD` to capture what it changed.
4. **Validate**: if Codex made changes, re-run the quality stack on affected files only:
   ```bash
   CODEX_CHANGED=$(git diff HEAD --name-only | grep '\.py$' | tr '\n' ' ')
   [ -n "$CODEX_CHANGED" ] && uv run ruff check $CODEX_CHANGED --fix && uv run pytest <test_dir> -q 2>&1 | tail -10
   ```
   - Tests pass → accept Codex corrections
   - Tests fail → revert Codex changes (`git restore .`) and note in final report
5. **Collect findings**: build `CODEX_FINDINGS` — a bullet list of every applied fix and every flagged-but-not-fixed issue. If nothing was found or the step was skipped, set `CODEX_FINDINGS=""`.
6. **Co-authorship rule**: add `Co-Authored-By: OpenAI Codex <codex@openai.com>` to the commit when Codex made an intellectual contribution — correctly identifying a bug or issue and producing the right fix — regardless of whether its bytes landed in the file directly or were applied by Claude. The bar is the reasoning and the patch content, not file I/O mechanics. Do NOT add it when Codex found no issues or was skipped.

Include a `### Codex Pre-pass` section in the final report:

- Available + fixes applied: list what Codex fixed
- Available + no issues: "Codex pre-pass: no issues found"
- Skipped (unavailable): "Codex not installed — pre-pass skipped"
- Reverted (tests broke): "Codex corrections reverted — {reason}"

## Shared Step: Progressive review loop

Maximum 3 cycles. Applied after the quality stack.

**Cycle 1: Full review**

- Invoke `/review` for a full multi-agent code review. If `CODEX_FINDINGS` is non-empty, prepend it to the review brief: "Codex pre-pass found the following — verify these, do not rediscover: $CODEX_FINDINGS"
- Capture review state: `{agents_with_findings, unresolved_findings, files_reviewed}`
- If clean (no critical/high findings): skip to report

**Cycle 2: Targeted re-check**

- Fix critical/high findings from Cycle 1
- Re-run quality stack on modified files only
- Set up a run directory for file-based handoff: `RUN_DIR="/tmp/develop-review-$(date +%s)"; mkdir -p "$RUN_DIR"`
- For each agent type in `agents_with_findings`: spawn that agent directly (not `/review`) with a focused prompt scoped to modified files + prior findings. Each agent prompt must end with: "Write your full findings to `$RUN_DIR/<agent-name>.md` using the Write tool. Return ONLY a compact JSON envelope: `{\"status\":\"done\",\"findings\":N,\"severity\":{\"critical\":0,\"high\":0},\"file\":\"$RUN_DIR/<agent-name>.md\",\"confidence\":0.N}`"
- Skip agents that were clean in Cycle 1
- Collect envelopes to update review state (do not read the full finding files into context — check envelopes to determine if critical/high remain)

**Cycle 3: Minimal verification**

- Fix remaining critical/high findings
- Re-run quality stack only (no agents)
- If clean: proceed to report
- If still failing: stop and present findings to user — do not loop further

**Context optimization between cycles**:

- If context usage is high, write review state to `.claude/state/develop-review-state.md` before any compaction:
  ```
  # Develop Review State
  cycle: <N>
  resolved: [list]
  unresolved: [list]
  files_modified: [list]
  agents_with_issues: [list]
  ```
- After compaction, read it back to resume at the correct cycle
- Delete the file when the review loop completes

## Shared Step: Codex mechanical delegation (optional)

Read `.claude/skills/_shared/codex-delegation.md` and apply the delegation criteria. Delegate mechanical follow-up tasks to Codex when an accurate, specific brief can be written.

This step is distinct from the Codex pre-pass above — the pre-pass checks the implementation diff for correctness; mechanical delegation outsources low-level follow-up work (scaffolding, boilerplate, migration scripts, etc.) after the review loop closes.

Only include a `### Codex Delegation` section in the final report when tasks were actually delegated — omit entirely if nothing was delegated.

## Shared Step: Final report

The report format is defined in the mode file's `## Final Report` section. Use that template, then end with a `## Confidence` block per CLAUDE.md output standards.

## Team Mode (--team)

Detect `--team` flag in `$ARGUMENTS`. Each mode file defines its team assignments in a `## Team Assignments` section.

**Shared protocol:**

1. Lead performs Step 1 (scope analysis) in its own context
2. Lead reads the mode file's `## Team Assignments` to determine teammate roles and responsibilities
3. Spawn teammates per CLAUDE.md team rules:
   - Reasoning (sw-engineer, qa-specialist): model = `opus`
   - Execution (doc-scribe, linting-expert): model = `sonnet`
   - Max 3–5 teammates
4. Every spawn prompt includes:
   `Read .claude/TEAM_PROTOCOL.md — use AgentSpeak v2`
   - compact instructions (preserve: file paths, errors, test results, task IDs; discard: verbose tool output, handshakes)
   - Step 1 analysis broadcast to all teammates
5. Lead coordinates outputs, then runs shared quality stack + progressive review loop
6. Team shutdown via `SendMessage shutdown_request` after the final report

**When to trigger team mode (per mode):**

- feature: spans 3+ modules, OR changes public API, OR auth/payment/data scope
- fix: root cause unclear after Step 1, OR bug spans 3+ modules
- refactor: target is a directory OR cross-module scope

</workflow>

<notes>

- **Mode determines the entry contract** — use `feature` for net-new capability, `fix` for bugs, `refactor` for quality/structure improvements, `plan` for lightweight scope analysis before committing to implementation
- **Quality stack runs once** — it is shared across all modes; never skip it
- **Review loop is bounded** — after 3 cycles without a clean review, stop and re-scope with the user; do not retry indefinitely
- **`disable-model-invocation: true`** — you must type `/develop <mode> <description>` explicitly; once invoked, the parent model executes all workflow steps
- Related agents: `sw-engineer` (analysis + implementation), `qa-specialist` (tests + security), `doc-scribe` (documentation), `linting-expert` (type safety + style)
- Follow-up chains:
  - Feature changes public API → `/release` to prepare CHANGELOG + migration guide
  - Feature/fix is performance-sensitive → `/optimize` for baseline + bottleneck analysis
  - Any mode touches `.claude/` config files → spawn `self-mentor` on changed files, then `/sync` to propagate
  - Mechanical follow-up beyond Codex step → `/codex` to delegate additional tasks
  - External validation → `/review` if an independent multi-agent review is desired beyond the built-in self-review gates

</notes>
