---
name: ship
description: Commit, push, and create a PR for the current branch
user-invocable: true
disable-model-invocation: true
---
Ship the current worktree branch as a PR.

1. **Stage & commit** all changes with a descriptive commit message following repo conventions. Include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`.
2. **Push** the branch to origin with `-u`.
3. **Create PR** via `gh pr create`:
   - Short title (under 70 chars)
   - Body with `## Summary` (bullet points), `## Test plan` (checklist)
   - If a GitHub issue was created for this plan, add `Closes #N` to the body
   - End body with: `Generated with [Claude Code](https://claude.com/claude-code)`

Report the PR URL when done.
