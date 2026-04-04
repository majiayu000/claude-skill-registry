---
name: ship
description: "Commit, push, and optionally create or update a PR for the current staged changes. Use when the user asks to \"ship\", \"ship it\", \"ship changes\", \"commit push and PR\", or \"ship this\"."
---

# Ship

Commit, push, and optionally create or update a PR for the current staged changes.

## Step 1: Determine Intent

Detect the repository's default branch via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`. Check the current branch name and whether a PR already exists for it using `gh pr view`.

Use `AskUserQuestion` to ask the user how to proceed. Present the options based on the current state:

- **On a feature branch with an existing PR** — commit, push, and update the PR; or commit and push
- **On a feature branch without a PR** — commit, push, and create a PR; or commit and push
- **On the default branch** — create a feature branch, commit, push, and create a PR; or commit and push
- **Abort** — leave changes staged, do not commit

## Step 2: Branch (if Needed)

If the user wants a PR and the current branch is the default branch:

1. Suggest a branch name based on the changes and use `AskUserQuestion` to confirm or adjust
2. Create and switch to the new branch: `git checkout -b <branch-name>`

## Step 3: Check for Unstaged Changes

Run `git status` to check for unstaged changes. If any exist, stage them. This catches files modified by auto-formatters that were not re-staged.

## Step 4: Run `/commit-staged-push` Skill

Run the `/commit-staged-push` skill.

If the commit fails due to a pre-commit hook (formatter, linter), fix the issues — or run the project's format/lint script to auto-fix — then **re-stage all modified files** before retrying. Pre-commit hooks may modify files in the working tree without updating the staging area.

## Step 5: Create or Update PR (if Requested)

- **Create PR** — run the `/create-pr` skill
- **Update PR** — run the `/update-pr` skill

## Rules

- Never stage or commit files containing secrets (`.env`, credentials, API keys). Warn if detected.
