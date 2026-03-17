---
name: code-review
description: "Use when reviewing code changes before committing or merging — staged diffs, branch diffs, or PR readiness checks. Triggers: 'review my code', 'check these changes', 'review this branch', 'give feedback on my diff', 'is this PR ready?'. Not for implementing features, running test suites, or formatting-only passes."
---

# Code Review

## Overview

Structured, actionable code review focused on correctness, bugs, style, and maintainability.
Act as a senior engineer: thorough, pragmatic, impact-first.

## Constraints

- Do NOT modify code unless explicitly asked.
- Do NOT guess missing code or behavior; ask for missing context.
- Do NOT suggest adding suppressions (e.g., `#pragma warning disable`).
- Stay focused on review quality; avoid unrelated commentary.
- Work strictly from the provided diff or code context.

## When to Use

- Reviewing staged changes before committing.
- Reviewing branch changes before merging or opening a PR.
- Checking a diff for correctness, bugs, style, or structure.
- Final review of all changes on a feature branch.
- Quick sanity-check of a small changeset before pushing.

**When NOT to use:**

- Implementing new features from scratch.
- Running test suites (see `python-testing` or equivalent).
- Refactoring without a prior review (review first, then refactor on request).
- Linting or formatting only — use a linter or formatter directly.

## Quick Reference

| Area                        | Look for                                            |
| --------------------------- | --------------------------------------------------- |
| Correctness & Logic         | Wrong behavior, broken contracts, off-by-one        |
| Bugs & Edge Cases           | Nil/null paths, boundary values, error propagation  |
| Code Quality & Style        | Naming, readability, idiomatic usage                |
| Structure & Maintainability | Coupling, duplication, separation of concerns       |
| Best Practices              | Language/framework conventions, SOLID, DRY          |
| Test Adequacy               | Missing tests for behavior changes, regression gaps |
| Security & Risk             | Input validation, auth, secrets, dependency risk    |
| Documentation               | Misleading comments, missing doc for public API     |

## Common Mistakes

- **Reviewing without full context** — jumping to conclusions without reading the complete diff or understanding intent.
- **Mixing review and edits** — modifying code during the review phase instead of separating feedback from implementation.
- **Nitpick overload** — burying critical issues under dozens of style nitpicks.
- **Ignoring intent** — critiquing design choices without understanding the constraints or goals behind them.
- **Incomplete scope** — reviewing only one file when the change spans multiple files or modules.

## Workflow

### Step 0 — Set Review Strategy

Before collecting findings:

- For medium/large or cross-module changes, write a short review plan focused on risk hotspots.
- Optionally split analysis by module and use subagents/parallel review passes when available.
- Consolidate findings into one prioritized report after parallel passes.

### Step 1 — Identify Changes

Determine the review scope based on what the user is reviewing.

**Pre-commit (staged changes):**

```sh
# List staged files
git diff --cached --name-status

# View staged diff
git --no-pager diff --cached

# View staged diff for a specific file
git --no-pager diff --cached -- path/to/file.ext
```

**Pre-merge (branch vs. target):**

```sh
# Resolve target base branch from origin/HEAD when available
BASE_BRANCH=$(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null)
BASE_BRANCH=${BASE_BRANCH#origin/}
BASE_BRANCH=${BASE_BRANCH:-main}
MERGE_BASE=$(git merge-base "$BASE_BRANCH" HEAD)

# List changed files on this branch relative to the target base
git diff --name-status "$MERGE_BASE"...HEAD

# View full branch diff
git --no-pager diff "$MERGE_BASE"...HEAD

# View diff for a specific file or directory
git --no-pager diff "$MERGE_BASE"...HEAD -- path/to/file.ext
```

If the user does not specify scope, infer from context:

- On a feature branch with commits ahead of the target base branch → pre-merge review.
- Staged changes present → pre-commit review.
- Ask if ambiguous, especially when default branch detection fails.

### Step 2 — Structured Review (No Edits)

For each changed file or module, summarize what changed and why.
Evaluate each area in the Quick Reference table above.

Rules:

- If intent is unclear, ask clarifying questions before judging.
- If an area has no issues, state that explicitly.
- Reference specific code locations (line numbers or quoted snippets).
- Keep feedback actionable and concise.
- Review all changed lines before final judgment; open surrounding context where needed.
- Address runtime errors, validation, error handling, concurrency risks, resource usage, and obvious performance pitfalls.
- Behavior changes without tests → raise an issue (at least Medium).
- Style comments are non-blocking unless they map to project conventions.
- Dependency manifest or lockfile changes → assess supply-chain risk and compatibility.
- Call out TODO comments and their implications.

Compile findings into issues using the template in `assets/issue-template.md`.
Sort issues by priority: critical > high > medium > low.
For each issue, include blocking status, confidence, and evidence.

### Step 3 — Apply Changes (Only on Explicit Request)

Proceed only when the user asks to "apply changes", "fix issues", "implement suggestions", or similar.

1. Apply only changes discussed in Step 2.
2. Make minimal, targeted edits.
3. Do not introduce additional refactors without user approval.
4. After editing, summarize what changed and why, mapping back to the original review items.

## Scope Note

Treat these recommendations as preferred defaults.
When a default conflicts with project constraints, suggest a better-fit alternative, call out tradeoffs, and note compensating controls.

## References

- `assets/issue-template.md` — issue type/priority legends and suggestion format.
- `references/review-best-practices-links.md` — external review best-practice links used by this skill.
