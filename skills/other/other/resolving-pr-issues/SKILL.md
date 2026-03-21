---
name: resolving-pr-issues
description: >
  Multi-agent review resolution with trust-but-verify methodology. Accepts a PR number/URL
  or a local code-review report file. Extracts review comments, verifies each with parallel
  agents using confidence scoring (0-100), filters false positives, presents a triage report
  for approval, then applies fixes and replies. Use when user runs /pr-issue-resolve, mentions
  "resolve PR comments", "address review feedback", "fix PR suggestions", "handle review
  comments", or "resolve review findings".
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr checkout:*), Bash(gh pr comment:*), Bash(gh pr review:*), Bash(gh api:*), Bash(gh issue create:*), Bash(git:*), Read, Write, Grep, Glob
argument-hint: "[PR-number | URL | file-path]"
---

# Multi-Agent PR Issue Resolver

Resolve review suggestions using parallel verification and confidence scoring.

**Core Principle**: Never assume a review comment is correct. Verify every suggestion against actual code before acting.

## Input Detection

Detect input mode from `$ARGUMENTS`:

- **PR mode**: argument is a number (`123`) or contains `github.com`/starts with `http` — use `gh` API
- **File mode**: argument contains `/` or `.md` or file exists on disk — parse findings from file
- **No argument**: show usage hint and stop

## Phase 1 — Context Gathering

**PR mode** — launch 2 parallel Haiku agents:

**Agent A — PR Metadata**: Run `gh pr view $ARGUMENTS --json number,title,body,baseRefName,headRefName,state,author,reviewRequests,statusCheckRollup` and `gh pr diff $ARGUMENTS`. Return: PR summary, base/head branches, CI status, files changed.

**Agent B — Comment Extraction**: Fetch all review comments using both endpoints:
- Inline review comments: `gh api repos/{owner}/{repo}/pulls/{pr}/comments`
- General issue comments: `gh api repos/{owner}/{repo}/issues/{pr}/comments`

Return structured list: comment ID, author, type (inline/general), file:line (if inline), body text, resolved status, whether it contains a `suggestion` code block.

**File mode** — launch 1 Haiku agent:

Parse the review report file. Extract each finding: description, file:line, category, suggested fix. Detect format from `review/skills/code-review/` report template or other common review formats.

**Skip conditions**: If no unresolved comments/findings exist, report "Nothing to resolve" and stop.

## Phase 2 — Parallel Verification

For each unresolved comment/finding, launch a **parallel Sonnet agent** (batched in groups of 5):

Each agent receives: the comment text, 50 lines of file context around the referenced line, the PR diff (or current branch diff in file mode), and the PR description.

Each agent returns:

```
Verdict: CONFIRMED | FALSE-POSITIVE | AMBIGUOUS
Category: Blocker | Bug | Code Quality | Style | Question
Confidence: 0-100
Evidence: {what was checked and found}
Suggested resolution: {specific code change or response text}
```

See [WORKFLOW.md](WORKFLOW.md) for agent prompt template and false positive filtering rules.

## Phase 3 — Triage Report

Filter findings scoring below **80**. Present a structured report:

```
## Review Issue Triage — {repo} PR #{number}
{N} comments analyzed, {M} actionable

### CONFIRMED ({count})
| # | Comment | File:Line | Category | Confidence | Action |
|---|---------|-----------|----------|------------|--------|
| 1 | {summary} | src/auth.ts:45 | Bug | 92 | Fix: add null check |

### FALSE POSITIVE ({count})
| # | Comment | File:Line | Confidence | Reason |
|---|---------|-----------|------------|--------|
| 2 | {summary} | src/api.ts:12 | 15 | Handled by framework |

### AMBIGUOUS ({count})
| # | Comment | File:Line | Options |
|---|---------|-----------|---------|
| 3 | {summary} | src/db.ts:78 | Option A: refactor / Option B: keep + comment |
```

**User approval gate**: Present the report and wait for the user to approve, modify, or reject the resolution plan before proceeding. For AMBIGUOUS items, let the user choose. For suggestions offering multiple options, present all and let the user decide.

## Phase 4 — Apply Changes

Execute the approved plan:

1. **PR mode**: `gh pr checkout $ARGUMENTS`; **File mode**: use current branch
2. For each approved fix (priority order: Blockers > Bugs > Code Quality > Style):
   - Edit the code as planned
   - Run targeted tests to verify the fix
   - Confirm no regressions in related functionality
   - Commit immediately: `fix(scope): description — addresses review comment on [topic]`
3. If tests fail, investigate root cause — do not skip or force-pass

See [WORKFLOW.md](WORKFLOW.md) for commit message format and priority ordering.

## Phase 5 — Update PR

**PR mode only** (skip entirely in file mode):

1. Push commits to the PR head branch
2. Reply to each comment using the correct mechanism:
   - **Inline review comments**: `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body="..."`
   - **General PR comments**: post a single consolidated response with anchor links: `### Re: [Finding title](#issuecomment-{id})`
3. Resolution status formats:
   - **Resolved**: "Addressed in commit `abc1234` — [brief description]"
   - **False positive**: evidence-based explanation (see [WORKFLOW.md](WORKFLOW.md) for template)
   - **Deferred**: "Created follow-up issue #xyz — [reason]"
4. Re-request reviews: `gh pr edit $ARGUMENTS --add-reviewer <username>`

## Confidence Scoring Rubric

| Score | Meaning |
|-------|---------|
| 0 | False positive — reviewer misread the code or concern doesn't apply |
| 25 | Plausible but likely misunderstanding, unable to verify |
| 50 | Valid observation but nitpick or style preference |
| 75 | Real issue, important, directly impacts functionality |
| 100 | Critical bug or security issue confirmed by evidence |

**Threshold**: Filter out findings below **80**.

## Resources

- [WORKFLOW.md](WORKFLOW.md) — Agent prompt templates, false positive rules, scoring details, reply formats
- [EXAMPLES.md](EXAMPLES.md) — End-to-end orchestration examples for PR and file modes
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues with gh CLI, comment API, and multi-agent pipeline
