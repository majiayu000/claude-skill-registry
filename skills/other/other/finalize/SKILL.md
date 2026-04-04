---
name: finalize
description: "Run the post-implementation quality assurance workflow including tests, code polishing, review, and commit. Use when the user asks to \"finalize implementation\", \"finalize changes\", \"wrap up implementation\", \"finish up\", \"ready to commit\", or \"run QA workflow\"."
---

# Finalize Implementation

Post-implementation QA workflow: tests, code polishing, commit, and self-improvement.

## Task Tracking

At the start, use `TaskCreate` to create a task for each phase:

1. Run `/polish-code` skill
2. Run `/update-changelog` skill
3. Run `/self-improve` skill
4. Commit and PR

## Phase 1: Run `/polish-code` Skill

Run the `/polish-code` skill for the current changes.

## Phase 2: Run `/update-changelog` Skill

Run the `/update-changelog` skill.

## Phase 3: Run `/self-improve` Skill

Run the `/self-improve` skill for the current session. Always run this phase even if the session seemed routine.

## Phase 4: Commit and PR

### Step 1: Analyze Split Potential

Examine the staged changes and evaluate whether they should be split into multiple commits, branches, and PRs for reviewability.

Detect the repository's default branch via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`. Check the current branch name and whether a PR already exists for it using `gh pr view`. If a PR exists, read its title and description to understand the branch's purpose. This context informs which changes belong on the current branch and which should be split off.

Run `git diff --cached --stat` and `git diff --cached` to understand the scope. Categorize changes along three dimensions:

- **Concern type**: refactoring, bug fix, new feature, cleanup, dependency update
- **Layer/domain**: backend, frontend, database migrations, i18n, tests, configuration
- **Logical unit**: files that form a coherent, independently reviewable change

A split is warranted when the staged changes contain multiple reviewable units. Each unit should be independently understandable, testable, and revertable. When deciding group boundaries, consider whether a reviewer could evaluate each group without needing context from the others.

### Step 2: Present Analysis and Choose Path

Output the split analysis as text.

If changes form a single cohesive unit, note this and run the `/ship` skill.

If changes span multiple reviewable units, propose an ordered list of groups. For each group, specify:

- Name and one-line description
- File list (flag files with mixed-concern hunks)
- Branch topology: stacked on the previous group (when this group depends on it) or independent (when it can stand alone)

Use `AskUserQuestion` to let the user choose: ship as a single commit/PR, or split.

- **Ship** — run the `/ship` skill
- **Split** — run the `/split-and-ship` skill

## Rules

- Diff size, number of files changed, passing tests, perceived user urgency, or context window concerns are not reasons to skip a phase. Each phase does work beyond what those signals cover. "The session was long" or "a prior phase was thorough" are never valid reasons to skip a later phase.
- Never stage or commit files containing secrets (`.env`, credentials, API keys). Warn if detected.
- Do not present diffs to the user — the user reviews diffs in an external git client. Use `git diff` internally as needed.
- If a non-test step fails (polish, review), stop and report the failure. Do not skip ahead.
