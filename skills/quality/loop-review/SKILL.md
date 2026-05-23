---
name: loop-review
description: >
  Use when a plan needs quality assurance before execution, especially
  after writing-plans completes. Catches intent gaps (missing user
  requirements) and quality gaps (vague, inconsistent, or unexecutable tasks).
allowed-tools: Read, Glob, Grep, Edit, Task, AskUserQuestion
user-invocable: true
argument-hint: <plan-file-path>
---

> **Spelling:** It's `saurun:` (with U), not "sauron"

# Loop Review

Iterative plan quality assurance. Spawns dual parallel reviewer subagents — one checking intent coverage against user's original ask, one checking standalone quality — and loops until the plan passes both or hits max iterations.

## When to Use

- After `saurun:writing-plans` (or any planning skill) completes
- When you want automated QA before executing a plan
- When plan quality matters (complex features, multi-task plans)
- `/loop-review` with optional plan file path

## When NOT to Use

- Plan is a simple 1-2 task change (overhead not worth it)
- You just need coverage verification against a spec (use `saurun:verify-plan-coverage`)
- Plan is already being executed (review first, execute after)

## Phase 0: Context Detection

### Resolve Plan Path

1. If `$ARGUMENTS` contains a file path → use it
2. Otherwise → find most recent `.md` in `_docs/plans/` by modification time (use Glob)
3. If no plan found → AskUserQuestion: "Which plan file should I review?"

Read the plan file. Store contents as `PLAN_CONTENT`.

### Extract User's Original Ask

Search conversation history for the user's original request that led to plan creation. Look for:
- The first substantive user message before planning began
- Messages containing requirements, feature requests, or problem descriptions
- Ignore meta-messages like "use writing-plans" or "create a plan"

Store verbatim as `USER_ORIGINAL_ASK`.

**Fallback:** If no clear original ask found in conversation history → AskUserQuestion: "What was the original request or goal this plan should fulfill? (paste verbatim or summarize)"

## Reviewer Dispatch

Both reviewers are dispatched via `Task(subagent_type="general-purpose")`. Each gets a prompt template with placeholders replaced before dispatch.

| Placeholder | Source | Used By |
|-------------|--------|---------|
| `{{PLAN_CONTENT}}` | Full plan file contents | Both |
| `{{PLAN_PATH}}` | Path to plan file | Both |
| `{{USER_ORIGINAL_ASK}}` | Verbatim user request | Intent ONLY |
| `{{ITERATION}}` | Current iteration number (1-based) | Both |
| `{{MAX_ITERATIONS}}` | Always `3` | Both |

**Prompt templates:**
- **Intent reviewer:** Read `intent-reviewer-prompt.md` from this skill directory, replace all placeholders
- **Quality reviewer:** Read `quality-reviewer-prompt.md` from this skill directory, replace all placeholders

**Dispatch rules:**
- All active reviewers spawned in a **single message** (parallel Task calls)
- `subagent_type: "general-purpose"`
- No model override (inherits session model)

## Main Loop

```
intent_passed = false
quality_passed = false
iteration = 1
MAX_ITERATIONS = 3

WHILE iteration <= MAX_ITERATIONS AND (NOT intent_passed OR NOT quality_passed):

  # 1. Build reviewer list (skip already-passed reviewers)
  reviewers = []
  IF NOT intent_passed: reviewers.add(INTENT)
  IF NOT quality_passed: reviewers.add(QUALITY)

  # 2. Read prompt templates, replace placeholders
  For each reviewer:
    Read template file from this skill directory
    Replace {{PLAN_CONTENT}}, {{PLAN_PATH}}, {{ITERATION}}, {{MAX_ITERATIONS}}
    For intent reviewer only: replace {{USER_ORIGINAL_ASK}}

  # 3. Spawn reviewers in parallel (ALL Task calls in single message)
  Dispatch all reviewers as Task(subagent_type="general-purpose")

  # 4. Parse results
  For each reviewer result:
    Parse VERDICT line: ACCEPT, REVISE, or ABORT
    IF ACCEPT → mark that reviewer as passed
    IF ABORT → stop loop immediately, report to user, ask for guidance

  # 5. Collect issues
  Merge all ISSUES from non-passed reviewers into single list
  IF no issues remain → ACCEPT. Report success to user. Done.

  # 6. Apply fixes (priority order)
  Sort issues: HIGH intent → HIGH quality → MEDIUM intent → MEDIUM quality
  For each HIGH and MEDIUM issue:
    Apply fix to plan file using Edit tool
    Skip LOW issues (informational only)

  # 7. Re-read plan after edits
  PLAN_CONTENT = Read(plan_path)
  iteration++

# Loop exit
IF iteration > MAX_ITERATIONS AND NOT (intent_passed AND quality_passed):
  Show remaining issues to user
  AskUserQuestion: "Max iterations reached. How would you like to proceed?"
    Options:
    - "Accept plan as-is with known issues"
    - "Fix remaining issues manually and re-run"
    - "Continue for N more iterations"
ELSE:
  Report: "Plan accepted after {iteration} iteration(s). Both reviewers passed."
```

## Shared Output Format

Both reviewer prompts include this core format (intent reviewer adds additional sections before DIMENSION_SCORES):

```
VERDICT: ACCEPT | REVISE | ABORT
OVERALL_SCORE: N/10
ITERATION: N/M

DIMENSION_SCORES:
| Dimension | Score | Weight | Notes |
|-----------|-------|--------|-------|
| ... | N/10 | Nx | ... |

ISSUES:
| # | Severity | Dimension | Location | Issue | Suggested Fix |
|---|----------|-----------|----------|-------|---------------|
| 1 | HIGH | ... | Task N / Section X | ... | ... |

SUMMARY:
[2-3 sentence narrative of findings]
```

**Parsing rules:**
- `VERDICT` line determines pass/fail/abort
- `ISSUES` table provides fix instructions for Edit tool
- `OVERALL_SCORE` is informational (verdict is authoritative)
- If output doesn't match format, treat as REVISE with a note about unparseable output

## Accept Criteria

A reviewer returns `ACCEPT` when:
- `OVERALL_SCORE >= 9`, **OR**
- Zero HIGH or MEDIUM issues found

**Both reviewers must ACCEPT** for the plan to pass the loop.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Sequential reviewer dispatch | ALL active reviewers in a single message (parallel Task calls) |
| Giving quality reviewer the user's ask | Quality reviewer gets plan ONLY — its lack of context IS the test |
| Fixing LOW issues | LOW = informational. Only fix HIGH and MEDIUM. |
| Re-running passed reviewers | Once a reviewer ACCEPTs, skip it in future iterations |
| Applying fixes without re-reading plan | Always re-read plan file after edits before next iteration |
| Continuing after ABORT | ABORT means stop. Report to user and ask for guidance. |
| Editing plan between dispatch and parse | Don't modify plan while reviewers are running |
| Downgrading severity to avoid fixes | If you're reclassifying MEDIUM as LOW to skip it, it's probably MEDIUM |

## Red Flags — Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "The intent is clearly covered by Task N" | Did the reviewer cite specific text? Vague claims = not covered. |
| "Quality is fine, the reviewer is being pedantic" | Pedantic = catching real ambiguity. Fix it. |
| "3 iterations is enough, accept with issues" | If HIGH issues remain, don't accept. Ask user. |
| "I can fix this during execution" | Plans with known gaps produce worse implementations. Fix now. |
| "The reviewer misunderstood the plan" | If a reviewer misunderstands, a developer will too. Improve clarity. |
| "This issue is LOW, basically" | If you're downgrading severity to avoid fixing, it's probably MEDIUM. |
| "Score is 8.5, close enough to 9" | < 9 is < 9. Fix issues or get explicit user approval. |
| "The quality reviewer doesn't have context" | That's the point. A good plan IS the context. |
