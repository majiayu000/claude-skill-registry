---
name: codex
description: Delegate narrow, mechanical coding tasks to OpenAI Codex Command Line Interface (CLI) — Claude orchestrates and judges, Codex executes. Pre-flight checks ensure graceful degradation on machines without Codex.
argument-hint: '"<task description>" ["target file or directory"]'
allowed-tools: Read, Bash, Grep, Glob, TaskCreate, TaskUpdate
---

<objective>

Delegate mechanical, well-scoped coding tasks to Codex CLI while Claude retains orchestration, judgment, and validation. Use this skill when a task is repetitive or formulaic enough that Codex can execute it faster and cheaper — but the task still needs Claude to scope it precisely, verify the output, and decide whether to keep or revert the changes.

Good candidates for delegation: adding docstrings to undocumented functions, renaming symbols consistently, extracting constants, adding type annotations to a well-typed module, reformatting code to match a style, applying a mechanical refactor across many files, fixing ruff/mypy errors that require targeted code changes, or writing tests for well-specified functions.

Poor candidates: architectural decisions, novel logic, anything requiring deep codebase understanding, or tasks where the correct answer is ambiguous.

</objective>

<inputs>

- **$ARGUMENTS**: required
  - First token(s): task description in plain text (e.g., `"add docstrings to all public functions"`)
  - Optional second quoted token: target file or directory to scope the task (e.g., `"src/mypackage/transforms.py"`)
  - If no target given: Step 2 scope analysis identifies the right location

</inputs>

<workflow>

**Task tracking**: per CLAUDE.md, create tasks (TaskCreate) for each major phase. Mark in_progress/completed throughout. On loop retry or scope change, create a new task.

## Step 0: Initialise log path

Before any other step, initialise the log path:

```bash
CODEX_LOG=".codex/logs/delegations.jsonl"
mkdir -p .codex/logs
```

All subsequent log calls append a single JSON line to this file. The file grows monotonically — never edited, only appended.

## Step 1: Pre-flight check

Pre-flight results are cached per-check in `.claude/state/preflight/<key>.ok` (unix timestamp inside, TTL 4 hours). Checks are skipped individually when their cache is fresh — so `git` cached by another skill is reused here. See `_shared/preflight-helpers.md` for the full key registry and pattern.

```bash
# From _shared/preflight-helpers.md
preflight_ok()  { local f=".claude/state/preflight/$1.ok"; [ -f "$f" ] && [ $(( $(date +%s) - $(cat "$f") )) -lt 14400 ]; }
preflight_pass(){ mkdir -p .claude/state/preflight; date +%s > ".claude/state/preflight/$1.ok"; }
```

Run each check only when its cache is missing or stale. Stop at the first failure.

**1 — Git is initialised** (required for stash-based handover):

```bash
preflight_ok git || git rev-parse --git-dir
```

If this fails: log a `not_started` entry, then stop with the error message.

```bash
printf '{"ts":"%s","status":"not_started","reason":"not a git repository"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$CODEX_LOG"
```

`Pre-flight failed: not a git repository. Initialise git first — stash handover requires it.`

On success: `preflight_pass git`

**2 — Codex binary on PATH:**

```bash
preflight_ok codex || which codex
```

If this fails: log a `not_started` entry, then stop with the error message.

```bash
printf '{"ts":"%s","status":"not_started","reason":"codex not found on PATH"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$CODEX_LOG"
```

`Pre-flight failed: codex not found on PATH. Install and retry. npm install -g @openai/codex`

On success: `preflight_pass codex`

## Step 2: Scope and formulate the prompt

Read the target file or directory to understand what Codex will operate on:

```bash
# Count lines and check file structure
wc -l <target>
```

For a directory: use the Glob tool (pattern `**/*.py`, path `<target>`) to list Python files (up to 20 results with `head_limit: 20`).

Assess task complexity:

- **Simple** — mechanical, clearly bounded, affects ≤ 5 files: proceed to Step 3
- **Medium** — well-defined but touches more files or requires consistent judgment calls: proceed with a more explicit prompt
- **Too broad** — architectural, ambiguous, or touches > 20 files: log a `skipped` entry, do not delegate. Implement directly using the appropriate skill (`/develop feature`, `/develop refactor`, etc.) and report why delegation was skipped.

```bash
printf '{"ts":"%s","status":"skipped","reason":"task too broad for delegation","prompt":"%s","target":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$PROMPT" "$TARGET" >> "$CODEX_LOG"
```

Select the Codex agent based on task type. The "internal chain" column shows which agents Codex may spawn internally (per `.codex/AGENTS.md` spawn rules) — Claude receives the final working-tree result of the whole chain, not just the first agent:

| Task type                                               | Entry agent      | Internal chain                                 |
| ------------------------------------------------------- | ---------------- | ---------------------------------------------- |
| Docstrings, README, CHANGELOG                           | `doc-scribe`     | single agent                                   |
| Implementation, refactoring, renaming, type annotations | `sw-engineer`    | `sw-engineer` → `qa-specialist` + `doc-scribe` |
| Lint / type-check fixes                                 | `linting-expert` | single agent                                   |
| Test writing or improvements                            | `qa-specialist`  | single agent                                   |
| Continuous Integration (CI) config, GitHub Actions      | `ci-guardian`    | single agent                                   |
| Data pipeline changes                                   | `data-steward`   | single agent                                   |
| Release prep, deprecation notices                       | `oss-maintainer` | single agent                                   |

For chained tasks (e.g. `sw-engineer`), Codex may take longer and touch more files — factor this into the complexity assessment above.

Formulate a lean, unambiguous prompt: `use the <agent> to <exact task> in <target>`. Do NOT repeat Borda conventions, style rules, or language version — the agent already has all of this in its `developer_instructions`. Only add constraints specific to this invocation (e.g., "do not modify function signatures", "stop after the first file only").

Confirm the selected agent is registered before dispatching:

```bash
ls .codex/agents/
```

If the agent file (e.g., `.codex/agents/doc-scribe.toml`) is absent, stop with a message listing what is available and let the user select a different agent.

## Step 3: Dispatch to Codex

Capture the start time and log a `started` entry, then run `codex exec` non-interactively. Always address the agent by name — Codex routes the task to the right specialist based on the opening phrase:

```bash
CODEX_START=$(date +%s)
printf '{"ts":"%s","status":"started","agent":"%s","prompt":"%s","target":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$AGENT" "$PROMPT" "$TARGET" >> "$CODEX_LOG"

codex exec "use the <agent> to <exact task> in <target>" --sandbox workspace-write
```

Example prompts:

```bash
codex exec "use the doc-scribe to add Google-style docstrings to all undocumented public functions in src/mypackage/transforms.py" --sandbox workspace-write
codex exec "use the sw-engineer to rename BatchLoader to DataBatcher throughout src/mypackage/" --sandbox workspace-write
codex exec "use the linting-expert to fix all ruff errors in src/mypackage/utils.py — do not change logic" --sandbox workspace-write
```

The `--sandbox workspace-write` flag allows Codex to read and write files in the workspace but not execute arbitrary shell commands outside it.

**Boundary contract**: Codex agents chain internally via stash (per AGENTS.md Work Handover). The final agent in any chain must leave all changes in the working tree — not stashed — so Claude can pick them up with `git diff HEAD` in Step 5.

## Step 4: Monitor and handle responses

**First: check actual git state — do not rely on Codex's claimed outcome alone.**

```bash
DIFF_STAT=$(git diff HEAD --stat)
DIFF_CONTENT=$(git diff HEAD)
```

Route based on this ground truth:

- **`$DIFF_CONTENT` is non-empty**: Codex wrote changes to the working tree → proceed to Step 5
- **`$DIFF_CONTENT` is empty AND Codex output says "no changes needed" / task was already done**: report and stop (legitimate no-op)
- **`$DIFF_CONTENT` is empty AND Codex output claims changes were made**: this is a contradiction — Codex printed a patch or described changes but nothing reached the filesystem. Stop and report explicitly:
  > `! Codex claimed changes but git diff HEAD is empty — no files were modified. Sandbox may have blocked writes. Do not stage anything. Rerun interactively with codex "<task>" to diagnose.`
- **Codex output contains "permission denied", "Operation not permitted", "cannot write", or "sandbox denied"** alongside a claim that changes ARE in the working tree: treat this as a contradiction requiring manual verification — pause and surface the contradiction to the user before proceeding
- **Partial completion**: Codex stopped partway (token limit, ambiguity) → resume the session with a clarifying follow-up (max 2 additional attempts):
  ```bash
  codex exec resume --last "<specific clarification or continuation instruction>" --sandbox workspace-write  # Note: verify 'resume --last <prompt>' syntax with 'codex exec resume --help' — the --last flag may require a session ID rather than a prompt string
  ```
- **Error / timeout**: report the error, do not retry the same prompt; suggest running Codex interactively (`codex "<task>"`) for diagnostics
- **Rate limit**: report the limit hit, suggest waiting and retrying

**Hard stop after 3 attempts total** (1 initial + 2 resumes). If the task is not complete by then, revert all Codex changes and implement directly.

## Step 5: Validate and capture

`git diff HEAD` already ran in Step 4 — use it. Proceed with lint and tests against the same live working tree:

```bash
echo "$DIFF_STAT"           # already captured in Step 4 — print for the log
uv run ruff check <changed_files>
uv run mypy <changed_files> --no-error-summary 2>&1 | head -20
python -m pytest <test_dir> -v --tb=short -q 2>&1 | tail -20
```

Capture metrics for logging:

```bash
FILES=$(git diff HEAD --stat | tail -1 | grep -o '[0-9]* file' | grep -o '[0-9]*')
LINT=pass    # or fail
TYPES=pass   # or fail
TESTS=pass   # or fail
```

**If validation fails:**

1. Attempt one fix pass via `codex exec resume --last "<targeted correction>" --sandbox workspace-write` — counts toward the 3-attempt limit
2. Re-run validation
3. If still failing: discard and report — do not capture a patch:
   ```bash
   git restore .
   git clean -fd
   ```
   Log a `reverted` entry and report that delegation failed, then proceed with direct implementation:
   ```bash
   CODEX_END=$(date +%s)
   printf '{"ts":"%s","status":"reverted","agent":"%s","prompt":"%s","target":"%s","attempts":%d,"duration_s":%d,"files_changed":%d,"lint":"%s","types":"%s","tests":"%s","patch":""}\n' \
     "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$AGENT" "$PROMPT" "$TARGET" \
     "$ATTEMPTS" "$((CODEX_END - CODEX_START))" "$FILES" "$LINT" "$TYPES" "$TESTS" >> "$CODEX_LOG"
   ```

**If validation passes:** capture the diff as a named patch file, then restore the working tree:

```bash
mkdir -p .codex/handover
PATCH=".codex/handover/codex-<task-slug>-$(date +%s).patch"
git diff HEAD > "$PATCH"
git restore .
git clean -fd
```

Log a `success` (or `partial` if any validation check was marginal) entry:

```bash
CODEX_END=$(date +%s)
printf '{"ts":"%s","status":"%s","agent":"%s","prompt":"%s","target":"%s","attempts":%d,"duration_s":%d,"files_changed":%d,"lint":"%s","types":"%s","tests":"%s","patch":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$STATUS" "$AGENT" "$PROMPT" "$TARGET" \
  "$ATTEMPTS" "$((CODEX_END - CODEX_START))" "$FILES" "$LINT" "$TYPES" "$TESTS" "$PATCH" >> "$CODEX_LOG"
```

The patch is now the reviewed, validated artifact. Apply it to make the changes live:

```bash
git apply "$PATCH"
rm "$PATCH"
```

When running as a parallel subagent spawned by a parent Claude: stop after saving the patch — do not apply it. The parent Claude collects all subagent patches and applies them sequentially.

## Step 6: Report

Output a structured summary:

```
## Codex Report: <task summary>

### Delegation
- Tool: Codex CLI (`codex exec`)
- Agent: <agent-name>
- Attempts used: N / 3
- Patch: .codex/handover/<filename>.patch (applied / awaiting parent)

### Changes Made
| File | Change | Lines |
|------|--------|-------|
| path/to/file.py | description | -N/+M |

### Validation
- Lint: clean / N issues (fixed by retry)
- Types: clean / N issues
- Tests: PASS (N tests) / FAIL — reverted

### Cost Efficiency
- Delegation outcome: success / partial / reverted
- [If reverted: reason and fallback used]

### Follow-up
- [any deferred items or suggested next steps]

## Confidence
**Score**: [0.N]
**Gaps**: [e.g., Codex output not verified against tests, one or more checks skipped, partial completion]
**Refinements**: N passes. [Pass 1: <what improved>. Pass 2: <what improved>.] — omit if 0 passes
```

To review delegation history:

```bash
# Convenience for manual review; use Read tool for single-entry inspection when running as Claude
# Human-readable table (no dependencies)
cat .codex/logs/delegations.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    d = json.loads(line)
    print(f\"{d.get('ts',''):<22} {d.get('status',''):<12} {d.get('agent',''):<16} {d.get('prompt','')[:60]}\")
"

# With jq (if available)
jq -r '[.ts, .status, .agent, .prompt[:60]] | @tsv' .codex/logs/delegations.jsonl | column -t
```

</workflow>

<notes>

- **Log file**: `.codex/logs/delegations.jsonl` — append-only JSONL, one line per delegation event. Two lines per successful run: `started` when dispatch begins, final-status line when complete. A `started` with no matching completion signals a hang or crash.
- **Delegation criteria**: only delegate when the task is mechanical and clearly bounded — ambiguous tasks produce inconsistent Codex output that costs more to fix than to write
- **3-attempt hard limit**: prevents runaway CLI sessions; after 3 attempts (1 initial + 2 resumes) without a passing patch, discard and implement directly
- **Validate before capturing**: lint + tests run against the live working tree; only a passing result gets saved as a patch
- **Patch files are parallel-safe**: each subagent writes a uniquely named file — no shared git state, no stash index races
- **Parent applies patches**: when running as a subagent, stop after saving the patch; never apply it yourself — the parent serialises application
- **Invocation**: Claude can call this skill via the Skill tool; the user can also type `/codex <task>` directly. Once invoked, the parent model executes all workflow steps.
- **Codex install command**: the `npm install -g @openai/codex` suggestion in the pre-flight error message should be verified at use time — the package name or install method may change across Codex releases
- Related agents: `sw-engineer` (fallback for direct implementation), `linting-expert` (validation), `qa-specialist` (test validation)
- Follow-up chains:
  - Codex changes pass but need architectural review → `/review` for full multi-agent quality validation
  - Task was too broad for delegation → `/develop feature` or `/develop refactor` for full orchestrated workflow

</notes>
