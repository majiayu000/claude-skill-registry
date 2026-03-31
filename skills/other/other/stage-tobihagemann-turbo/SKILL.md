---
name: stage
description: "Stage implementation changes for commit with precise file selection. Use when the user asks to \"stage changes\", \"stage files\", \"add files to staging\", or \"prepare changes for commit\"."
---

# Stage Changes

Stage implementation changes with precise file selection.

## Step 1: Identify Changes

Run `git status` to see all modified, added, and deleted files.

## Step 2: Stage Files

Stage only the files relevant to the current task:

```bash
git add <file1> <file2> ...
```

- Do not use `git add -A` or `git add .`
- If a file contains both relevant and unrelated changes, use `git add -p <file>` to stage only the relevant hunks
- Never stage files containing secrets (`.env`, credentials, API keys). Warn if detected.

## Step 3: Verify

Run `git status` and `git diff --cached` to verify the staging area contains exactly the intended changes.
