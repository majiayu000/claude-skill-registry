---
description: Commit and push changes with auto-generated summary
allowed-tools: Bash(git:*)
---

# Commit and Push Changes

## Current State

- Git status: !`git status`
- Staged changes: !`git diff --cached`
- Unstaged changes: !`git diff`

## Your Task

1. Review all changes (both staged and unstaged)
2. **Update documentation if appropriate:**
   - `agents.md` - Update if pipeline, findings, or project status changed
   - `README.md` - Update if user-facing docs need to reflect changes
3. Stage all relevant changes with `git add`
4. Create a clear, concise commit message that summarizes what was changed and why
5. Commit the changes
6. Push to the remote repository

Follow these commit message guidelines:
- Use imperative mood ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Focus on the "what" and "why", not the "how"

**Important:** Do not commit files that contain secrets (.env, credentials, etc.)
