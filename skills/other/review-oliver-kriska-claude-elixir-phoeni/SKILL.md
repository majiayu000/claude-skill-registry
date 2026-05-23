---
name: phx:review
description: Review code with parallel agents — tests, security, Ecto, LiveView, Oban. Use after implementation to catch bugs and anti-patterns before committing.
effort: high
argument-hint: [test|security|oban|deploy|iron-laws|all]
---

# Review Elixir/Phoenix Code

Review code by spawning parallel specialist agents. Find and
explain issues — do NOT create tasks or fix anything.

## Usage

```
/phx:review                          # Auto-detects task ID from branch/commits
/phx:review test                     # Review test files only
/phx:review security                 # Run security audit only
/phx:review oban                     # Review Oban workers only
/phx:review deploy                   # Validate deployment config
/phx:review iron-laws                # Check Iron Law violations only
/phx:review ENA-8931                 # Force Linear issue
/phx:review #42                      # Force GitHub issue
/phx:review .claude/plans/auth/plan.md    # Force plan / spec file
/phx:review --no-requirements        # Skip requirements coverage check
```

## Arguments

`$ARGUMENTS` = Focus area, task ID, or path to plan/spec file.

When no requirements argument is passed, the skill auto-detects a task ID
from the current git branch name and recent commits (see
`${CLAUDE_SKILL_DIR}/references/requirements-detection.md`).

## Workflow

### Step 1: Identify Changed Files and Prepare Directories

**CRITICAL**: Create output dirs BEFORE spawning agents — agents cannot
create directories and writes will fail.

1. Determine SLUG via Glob on `.claude/plans/*/` (default: `"review"`)
2. Run `mkdir -p ".claude/plans/${SLUG}/reviews" ".claude/plans/${SLUG}/summaries" .claude/reviews`
3. Run `git diff --name-only HEAD~5` and `git diff --name-only main`
4. Save the diff base for pre-existing detection in Step 3b

### Step 1b: Load Plan Context and Prior Reviews

- Read `.claude/plans/${SLUG}/scratchpad.md` for planning decisions and rationale
- Pass relevant decisions to agents as WHY-context (eliminates session archaeology)
- Check `.claude/plans/${SLUG}/reviews/` for prior output; if present, include a
  consolidated summary as "PRIOR FINDINGS" with: "Focus on NEW issues. Mark
  still-present issues as PERSISTENT."

### Step 1c: Detect Requirements Source (skip on `--no-requirements`)

Find a task/spec whose requirements should be cross-checked against the diff.
Priority order (stop at first match): explicit arg → conversation context →
branch regex → commit subjects → latest plan → none. Full table, regexes,
and fetch mapping in `${CLAUDE_SKILL_DIR}/references/requirements-detection.md`.

Fetch the detected source into `.claude/plans/${SLUG}/reviews/.requirements-input.md`
(Linear via `mcp__linear__get_issue`, GitHub via `gh issue view`, file via Read).
Record `REQ_SOURCE` label (e.g. `"Linear ENA-8931"`) for the verifier heading.
On fetch failure, set `SOURCE_STATUS=FETCH_FAILED` and continue — verifier
will emit `NOT AVAILABLE` rather than block the review.

### Step 2: Spawn Review Agents (MANDATORY)

**NEVER** spawn the same agent role twice per review. One pass per role.
**NEVER** analyze code yourself — use the Agent tool only. Zero agents = failure.

1. Create a Claude Code task per agent via `TaskCreate` and `TaskUpdate` to `in_progress`
2. For `/phx:review` or `/phx:review all`: select agents dynamically per the
   selection table in `${CLAUDE_SKILL_DIR}/references/agent-spawning.md`
3. For focused reviews (`test|security|oban|deploy|iron-laws`): spawn only the
   matching specialist from the focused mode table in the same reference
4. **If Step 1c succeeded** (REQ_SOURCE non-empty and `--no-requirements`
   not passed): add `elixir-phoenix:requirements-verifier` to the same
   parallel batch. Pass these prompt inputs: `REQUIREMENTS_TEXT` (content
   of `.requirements-input.md`), `REQUIREMENTS_SOURCE` (REQ_SOURCE label),
   `DIFF_FILES` (git diff --name-only output), `SOURCE_STATUS` (only if
   FETCH_FAILED), `output_file: .claude/plans/{slug}/reviews/requirements.md`
5. Spawn in ONE message with `mode: "bypassPermissions"` and `run_in_background: true`
6. **MANDATORY**: pass explicit `output_file` per-agent (mapping in the reference)
7. Include the CRITICAL prompt block: write by turn ~12, chat body ≤300 words
8. Scope every agent to the diff: pass `git diff --name-only` output with
   "Focus on NEW code. Pre-existing: one-line `{file}:{line} — {brief}`. Do
   NOT deep-analyze unchanged files."

### Step 3: Collect and Compress Findings

Wait for ALL agents to complete. **Do NOT report status until every agent
completes.** Mark each task `completed` via `TaskUpdate` as it finishes.

**Missing file fallback** — after each agent finishes, verify its expected
`output_file` exists. If missing (turn exhaustion, error):

1. Append to `.claude/plans/{slug}/scratchpad.md`:
   `[HH:MM] WARN: {agent} did not write {expected_path} — extracting from message`
2. Parse findings from the agent's return message as fallback
3. Mark the section in the final review with
   `⚠️ EXTRACTED FROM AGENT MESSAGE (see scratchpad)` — never silent

**Verification-runner fallback** — if it times out, run directly:
`mix compile --warnings-as-errors && mix format --check-formatted $(git diff --name-only HEAD~5 | grep '\.exs\?$' | tr '\n' ' ') && mix credo --strict && mix test`

**Context supervision** — for 4+ agents, spawn `elixir-phoenix:context-supervisor`:

```
Prompt: "Compress review agent output.
  input_dir: .claude/plans/{slug}/reviews
  output_dir: .claude/plans/{slug}/summaries
  output_file: review-consolidated.md
  priority_instructions: BLOCKERs and WARNINGs: KEEP ALL.
    SUGGESTIONs: COMPRESS similar ones into groups.
    Deconfliction: when iron-law-judge and elixir-reviewer
    flag same code, keep iron-law-judge finding."
```

Skip the supervisor for focused (1-agent) reviews — read output directly.

### Step 3b: Filter Findings (Anti-Noise)

Before writing the review, apply these overriding filters to each finding:

1. Would a senior Elixir dev dismiss this as noise?
2. Does the finding add complexity exceeding the problem's complexity?
3. Are any findings duplicates reworded by different agents?
4. Does the finding affect code actually changed in this diff?
5. Is the finding on unchanged code (not in diff)? → Mark PRE-EXISTING

Demote or remove findings that fail filters 1-4. Mark pre-existing per filter 5.

### Step 4: Generate Review Summary

Read consolidated/agent output. Write to `.claude/plans/{slug}/reviews/{feature}-review.md`
with verdict: PASS | PASS WITH WARNINGS | REQUIRES CHANGES | BLOCKED.

**Requirements Coverage in verdict**: if the verifier ran, read its
summary line and fold into the verdict:

- Any `UNMET` → escalate to `REQUIRES CHANGES` (even if code-quality PASS)
- Any `PARTIAL` (no UNMET) → downgrade PASS → `PASS WITH WARNINGS`
- `NOT AVAILABLE` / all `MET` / `UNCLEAR` only → no verdict change

Insert the verifier's `## Requirements Coverage` block into the
review document **before** the per-agent findings so it's the first
thing the user sees.

### Step 5: Present Findings and Ask User

**STOP and present the review.** Do NOT create tasks or fix
anything.

**On BLOCKED or REQUIRES CHANGES**: Show finding count by severity,
then offer via `AskUserQuestion`: `/phx:triage` (recommended), `/phx:plan`,
fix directly, or "I'll handle it myself".

**On PASS / PASS WITH WARNINGS**: Suggest `/phx:compound`, `/phx:learn-from-fix`.

**Convention extraction**: After presenting findings, offer: "Any findings
to suppress or enforce as conventions?" See `${CLAUDE_SKILL_DIR}/references/conventions.md`.

## Iron Laws

1. **Review is READ-ONLY** — Find and explain, never fix
2. **NEVER auto-fix after review** — Always ask the user first
3. **Always offer both paths**: `/phx:plan` and `/phx:work`
4. **Research before claiming** — Agents MUST research before
   making claims about CI/CD or external services

## Integration

`/phx:plan` → `/phx:work` → `/phx:review` (YOU ARE HERE) → Blocked? `/phx:triage` or `/phx:plan` | Pass? `/phx:compound`

See: `${CLAUDE_SKILL_DIR}/references/review-template.md`, `${CLAUDE_SKILL_DIR}/references/example-review.md`, `${CLAUDE_SKILL_DIR}/references/blocker-handling.md`, `${CLAUDE_SKILL_DIR}/references/requirements-detection.md`
