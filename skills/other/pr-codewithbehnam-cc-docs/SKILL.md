---
name: pr
description: >
  Create a pull request. Summarizes changes since the base branch, generates
  a PR title and description, pushes the branch, and opens a PR via the gh CLI.
  Use when opening a PR, submitting work for review, or when the user says
  "open a PR", "create a pull request", or "submit for review".
disable-model-invocation: true
allowed-tools: Bash, Read, Glob
argument-hint: "[base-branch]"
---

Create a pull request for the current branch:

1. Determine the base branch:
   - If $ARGUMENTS is provided, use it as the base branch
   - Otherwise, detect the default branch: `git remote show origin | grep 'HEAD branch'`
2. Check the current branch name: `git branch --show-current`
   - If already on the default branch, stop and ask the user to switch to a feature branch
3. Summarize changes compared to the base:
   - `git log origin/<base>..HEAD --oneline` for commit history
   - `git diff origin/<base>..HEAD --stat` for changed files
4. Push the current branch to origin: `git push -u origin HEAD`
   - If the push fails due to no upstream, use `git push --set-upstream origin <branch>`
5. Generate a PR title and description:
   - Title: concise, imperative mood, max 72 chars (e.g., "Add user authentication via OAuth2")
   - Description sections:
     - **Summary**: what this PR does and why (2-4 sentences)
     - **Changes**: bullet list of key changes
     - **Testing**: how to verify the changes
     - **Related issues**: mention any linked issue numbers if inferable from branch name or commits
6. Create the PR: `gh pr create --base <base> --title "<title>" --body "<description>"`
7. Print the PR URL

## Requirements

- `gh` CLI must be installed and authenticated (`gh auth status`)
- Must be on a feature branch (not the default branch)
- At least one commit must exist ahead of the base branch

## Error Handling

- If `gh` is not installed: provide the PR URL to create manually via the web
- If push is rejected (non-fast-forward): suggest `git pull --rebase` first
- If PR already exists for this branch: show the existing PR URL with `gh pr view`
- If no commits ahead of base: report and stop
