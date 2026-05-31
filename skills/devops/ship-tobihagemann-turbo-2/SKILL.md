---
name: ship
description: "Commit, push, and optionally create or update a PR for the current staged changes. Use when the user asks to \"ship\", \"ship it\", \"ship changes\", \"commit push and PR\", or \"ship this\"."
---

# Ship

Commit, push, and optionally create or update a PR for the current staged changes.

## Task Tracking

At the start, use `update_plan` to track each phase:

1. Determine intent
2. Branch (if needed)
3. Stage unstaged changes
4. Run `$commit-rules` skill
5. Commit
6. Push (if requested)
7. Create or update PR (if requested)

## Step 1: Determine Intent

Detect the repository state:

- Default branch: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
- Current branch name, and whether it tracks an upstream
- Whether a PR already exists for the current branch (`gh pr view`)

Sample the prevailing workflow from recent default-branch history (`git log --first-parent origin/<default-branch> -n 30 --pretty=%s`): judge whether changes mostly land through pull requests (merge-PR commits or `(#N)`-suffixed squash commits) or are committed directly to the default branch.

Output a one-line summary of the detected state as text. Then use `request_user_input` to choose how to proceed, offering these options:

- **Commit, push, and create/update the PR** — say "create a PR" when no PR exists for the current branch and "update the PR" when one does; on the default branch, Step 2 creates a feature branch first
- **Commit and push** — commit, then push to the current branch's remote
- **Commit only** — commit the staged changes, do not push

Recommend the option that fits this repo by listing it first and labeling it `(Recommended)`: when the current branch already has a PR, recommend updating it; otherwise follow the prevailing workflow — recommend the PR path for a PR-based history, or commit and push for a direct-commit history.

If the user declines (chooses the free-form "Other" option or asks to abort), leave the changes staged and do not commit.

## Step 2: Branch (if Needed)

If the chosen option creates a PR and the current branch is the default branch:

1. Suggest a branch name based on the changes and use `request_user_input` to confirm or adjust
2. Create and switch to the new branch: `git checkout -b <branch-name>`

## Step 3: Check for Unstaged Changes

Run `git status` to check for unstaged changes. If any exist, stage them. This catches files modified by auto-formatters that were not re-staged.

## Step 4: Run `$commit-rules` Skill

Run the `$commit-rules` skill to load commit message rules and technical constraints.

## Step 5: Commit

Commit the already-staged changes (do not stage additional files) with a message following the loaded rules.

If the commit fails due to a pre-commit hook (formatter, linter), fix the issues — or run the project's format/lint script to auto-fix — then **re-stage all modified files** before retrying. Pre-commit hooks may modify files in the working tree without updating the staging area.

## Step 6: Push (if Requested)

If the chosen option includes pushing, push to the current branch's remote:

```bash
git push
```

## Step 7: Create or Update PR (if Requested)

- **Create PR** — run the `$create-pr` skill
- **Update PR** — run the `$update-pr` skill

Then update or check the active plan and proceed to any remaining task.

## Rules

- Run the `$commit-rules` skill before every commit; do not commit without loading it first.
- Never stage or commit files containing secrets (`.env`, credentials, API keys). Warn if detected.
- Don't reference `.turbo/` content (filenames, IDs, headings) in branch names. `.turbo/` is gitignored, so these references would be opaque to anyone reading without local copies.
