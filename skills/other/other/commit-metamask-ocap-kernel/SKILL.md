---
name: commit
description: Optionally checks, then commits code to the current or a new feature branch.
---

When asked to commit code, follow these steps:

## Arguments

- `check` (default): Run checks first to lint, build, and test the code. Stop if any checks fail.
- `force`: Skip the check step and commit directly.

## Steps

1. Run these bash commands in parallel to understand the current state:

   - `git status` to see all untracked files
   - `git diff HEAD` to see both staged and unstaged changes
   - `git log --oneline -10` to see recent commit messages for style consistency

2. If you are on the `main` branch, create a new feature branch using `git branch` and switch to it.

3. Analyze all changes and draft a commit message:

   - Summarize the nature of the changes (new feature, enhancement, bug fix, refactoring, test, docs, etc.)
   - Use the conventional commit format: `type(scope): description`
   - Keep the first line under 72 characters
   - Do not commit files that likely contain secrets (.env, credentials.json, etc.)

4. Stage and commit the changes:

   - Add relevant files using `git add`
   - Use a plain string for the commit message (do not use HEREDOCs).

5. Report the results including:
   - The commit hash
   - The commit message
