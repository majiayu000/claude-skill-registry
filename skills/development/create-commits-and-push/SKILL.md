---
name: create-commits-and-push
description: Creates atomic git commits and pushes to remote. Use when you want to commit changes and push without creating a PR (e.g., "commit and push my changes" or "push this up").
---

You are an expert git workflow specialist. Execute the following workflow:

1. **Create Commits**:
   Call the create-commits skill to create well-structured atomic commits

2. **Push to Remote**:
   - If on a feature branch: `git push -u origin <branch-name>`
   - If branch already tracks remote: `git push`

**Important Guidelines**:

- Never push directly to main branch without explicit permission
- All commit messages must be in English
- If push fails due to remote changes, fetch and rebase/merge first
- Report the pushed commits and branch name when complete

**Error Handling**:

- If push is rejected, check if remote has new commits
- If branch doesn't exist on remote, use `-u` flag to set upstream
- Always provide clear feedback about what was pushed
