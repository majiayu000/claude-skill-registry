---
name: review
description: Use when reviewing code changes (PRs, diffs, or files) with parallel specialized agents. 8-agent review with self-challenge protocol and cross-agent corroboration.
effort: max
argument-hint: "review|find|learn [PR number or file paths]"
---



# Review

## Purpose

Parallel specialized code review. Dispatches 8 review agents, each analyzing the same code from a different angle. Every agent argues AGAINST its own findings (self-challenge). Cross-agent corroboration filters noise from signal.

## When to Use

- Before merging a PR
- After completing a feature (pre-commit review)
- When reviewing someone else's code
- Periodic architecture review

## Process

1. **Explore first** -- run `/ai-explore` on the changed files to build architectural context
2. **Dispatch reviewers** -- follow `handlers/review.md` (8 parallel specialized agents)
3. **Aggregate findings** -- correlate, deduplicate, confidence-score
4. **Self-challenge** -- each finding is argued against by its own agent
5. **Filter** -- drop solo findings below 40% confidence
6. **Report** -- produce review summary with actionable findings

See `handlers/review.md` for the full review workflow, `handlers/find.md` for finding existing reviews, and `handlers/learn.md` for the continuous improvement loop.

## Quick Reference

| Mode | What it does |
|------|-------------|
| `review` | Full parallel review (default) |
| `find` | Find and summarize existing review comments on a PR |
| `learn` | Extract lessons from past reviews for future improvement |

## The 8 Review Agents

| Agent | Focus | Looks for |
|-------|-------|-----------|
| Security | OWASP, injection, auth | SQL injection, XSS, auth bypass, secret exposure |
| Performance | Speed, memory, I/O | N+1 queries, O(n^2), memory leaks, blocking I/O |
| Correctness | Logic, edge cases | Off-by-one, null handling, race conditions, missing cases |
| Maintainability | Readability, complexity | God functions, deep nesting, unclear naming, magic numbers |
| Testing | Coverage, quality | Missing tests, weak assertions, testing implementation |
| Compatibility | Breaking changes, API | Public API changes, backward compat, deprecation |
| Architecture | Boundaries, patterns | Layer violations, circular deps, pattern inconsistency |
| Frontend | UX, a11y, rendering | Missing aria labels, layout shifts, unhandled states |

## Confidence Scoring

Each finding gets a confidence score (20-100%):

| Score | Meaning | Action |
|-------|---------|--------|
| 80-100% | High confidence, clear evidence | Must address |
| 60-79% | Moderate confidence | Should address |
| 40-59% | Low confidence, single agent | Consider |
| 20-39% | Solo finding, uncertain | Dropped unless critical severity |

**Corroboration bonus**: when 2+ agents flag the same issue, confidence increases by 20%.
**Solo penalty**: single-agent findings below 40% are dropped from the report.

## Self-Challenge Protocol

For each finding, the reviewing agent must:

1. **State the finding** (what is wrong)
2. **Argue against it** (why this might be acceptable)
3. **Resolve** (finding stands, confidence adjusted, or finding withdrawn)

Example:
```
Finding: Function handles 5 different concerns (god function)
Counter: This is a CLI command handler -- some breadth is expected in the entry point
Resolution: Finding stands but severity reduced to minor. The handler delegates
  to helpers for the complex logic. Confidence: 55%
```

## Common Mistakes

- Reviewing without architectural context (always explore first)
- Treating all findings equally (use confidence scoring)
- Not self-challenging (every finding must be argued against)
- Reviewing only the diff without understanding the surrounding code
- Flagging style preferences as bugs

## Integration

- **Called by**: user directly, `/ai-pr` (pre-merge review)
- **Calls**: `/ai-explore` (context), `handlers/review.md`, `handlers/find.md`, `handlers/learn.md`
- **Read-only**: never modifies code -- produces review findings

$ARGUMENTS
