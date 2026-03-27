---
name: phx:review
description: Review code with parallel specialist agents covering tests, security, Ecto, LiveView, and Oban patterns. Use after any implementation to catch bugs, security vulnerabilities, and anti-patterns before committing. Even quick changes benefit from at least a targeted review track.
effort: high
argument-hint: [test|security|oban|deploy|iron-laws|all]
disable-model-invocation: true
---

# Review Elixir/Phoenix Code

Review code by spawning parallel specialist agents. Find and
explain issues — do NOT create tasks or fix anything.

## Usage

```
/phx:review                          # Review all changed files
/phx:review test                     # Review test files only
/phx:review security                 # Run security audit only
/phx:review oban                     # Review Oban workers only
/phx:review deploy                   # Validate deployment config
/phx:review iron-laws                # Check Iron Law violations only
/phx:review .claude/plans/auth/plan.md    # Review implementation of plan
```

## Arguments

`$ARGUMENTS` = Focus area or path to plan file.

## Workflow

### Step 1: Identify Changed Files and Prepare Directories

```bash
# CRITICAL: Create output dirs BEFORE spawning agents — agents
# cannot create directories and will fail repeatedly on writes
SLUG="$(basename "$(ls -td .claude/plans/*/ 2>/dev/null | head -1)" 2>/dev/null || echo "review")"
mkdir -p ".claude/plans/${SLUG}/reviews" ".claude/plans/${SLUG}/summaries"

# If no plan context, use fallback directory
mkdir -p .claude/reviews

git diff --name-only HEAD~5   # Recent changes (also save as DIFF_BASE)
git diff --name-only main     # Or changes from main
# Save diff base for pre-existing detection in Step 3b
```

### Step 1b: Load Plan Context (Scratchpad)

If reviewing a plan, read `.claude/plans/${SLUG}/scratchpad.md` for
planning decisions, rationale, and handoff notes. Include relevant
decisions in each agent's prompt so they have context about WHY
code was written a certain way. This eliminates session archaeology.

### Step 1c: Check Prior Reviews

If `.claude/plans/${SLUG}/reviews/` has prior output, include consolidated
summary in each agent's prompt as "PRIOR FINDINGS" with instruction:
"Focus on NEW issues. Mark still-present issues as PERSISTENT."

### Step 2: Create Task List and Spawn Review Agents (MANDATORY)

**NEVER spawn the same agent role twice in one review.** If reviewing
a plan, scope ALL agents to the plan's changed files in a single pass.
Do NOT run a scoped review followed by a broader review — one pass per role.

**Create Claude Code tasks** for each review agent BEFORE spawning.
This gives real-time progress visibility:

```
For each agent to spawn:
  TaskCreate({
    subject: "{Agent Name} review",
    description: "Review changed files for {focus area}",
    activeForm: "Running {Agent Name}..."
  })
  TaskUpdate({taskId, status: "in_progress"})
```

Then spawn agents using the Agent tool. Do NOT analyze code
yourself — delegate to agents.

**For `/phx:review` or `/phx:review all` — select agents dynamically
based on the diff, then spawn selected agents in ONE message (parallel):**

| Agent | subagent_type | When to spawn |
|-------|---------------|---------------|
| Elixir Reviewer | `elixir-phoenix:elixir-reviewer` | **Always** |
| Iron Law Judge | `elixir-phoenix:iron-law-judge` | Only if >200 lines changed AND auth/LiveView/Oban files in diff. **Skip** if PostToolUse hooks already verified all files (hooks check Iron Laws on every Edit/Write) |
| Verification Runner | `elixir-phoenix:verification-runner` | Only if `mix test` has NOT been run in this session. **Skip** if `/phx:work` just passed all verification tiers |
| Security Analyzer | `elixir-phoenix:security-analyzer` | Auth/session/password/token files changed |
| Testing Reviewer | `elixir-phoenix:testing-reviewer` | Test files changed OR new public functions |
| Oban Specialist | `elixir-phoenix:oban-specialist` | Worker files changed (*_worker.ex) |
| Deploy Validator | `elixir-phoenix:deployment-validator` | Dockerfile/fly.toml/runtime.exs changed |

**Agent count**: Min 1, max 5. For <200 lines changed: spawn only
elixir-reviewer + security-analyzer (if auth files). Log selection
rationale in review output.
Spawn with `mode: "bypassPermissions"` and `run_in_background: true`.

**For focused reviews — spawn the specified agent only:**

| Argument | subagent_type |
|----------|---------------|
| `test` | `elixir-phoenix:testing-reviewer` |
| `security` | `elixir-phoenix:security-analyzer` |
| `oban` | `elixir-phoenix:oban-specialist` |
| `deploy` | `elixir-phoenix:deployment-validator` |
| `iron-laws` | `elixir-phoenix:iron-law-judge` |

Zero agents spawned = skill failure.

### Step 2b: Scope Agents to the Diff (MANDATORY)

Include `git diff --name-only` in each agent's prompt. Add instruction:
"Focus on NEW code from the diff. Pre-existing issues get one line:
'Pre-existing: {file}:{line} — {brief}'. Do NOT deep-analyze unchanged files."

### Step 3: Collect and Compress Findings

Wait for ALL agents to FULLY complete. **Do NOT report status
until every agent completes.** Mark each agent's Claude Code task
as `completed` via `TaskUpdate` as it finishes.

**Verification-runner fallback**: If it fails/times out, run directly:
`mix compile --warnings-as-errors && mix format --check-formatted $(git diff --name-only HEAD~5 | grep '\.exs\?$' | tr '\n' ' ') && mix credo --strict && mix test`

**For 4+ agents:** Spawn `elixir-phoenix:context-supervisor` to compress output:

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

**For focused reviews (1 agent):** Skip supervisor, read
agent output directly.

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

### Step 5: Present Findings and Ask User

**STOP and present the review.** Do NOT create tasks or fix
anything.

**On BLOCKED or REQUIRES CHANGES**: Show finding count by severity,
then offer via `AskUserQuestion`: `/phx:triage` (recommended), `/phx:plan`,
fix directly, or "I'll handle it myself".

**On PASS / PASS WITH WARNINGS**: Suggest `/phx:compound`, `/phx:learn`.

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

See: `${CLAUDE_SKILL_DIR}/references/review-template.md`, `${CLAUDE_SKILL_DIR}/references/example-review.md`, `${CLAUDE_SKILL_DIR}/references/blocker-handling.md`
