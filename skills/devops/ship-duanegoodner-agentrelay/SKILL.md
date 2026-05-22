---
name: ship
description: Commit, push, and create a PR for the current feature branch
disable-model-invocation: true
---

Ship the current feature branch: commit all changes, push, and open a PR.

Steps:

1. Run `git status` (no -uall flag), `git diff` (staged + unstaged), and
   `git log --oneline -5` to understand the current state.
2. Stage all relevant changed/new files (prefer naming files explicitly over
   `git add -A`). Do NOT stage files that likely contain secrets.
3. Write a concise commit message (1-2 sentences) focusing on the "why".
   End the message with:
   ```
   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   ```
   Use a HEREDOC to pass the commit message.
4. Push the branch to the remote with `-u`.
5. Create a PR with `gh pr create`. The PR body must include:
   - `## Summary` (1-3 bullet points)
   - `## Test plan` (bulleted checklist)
   - Footer: `Generated with [Claude Code](https://claude.com/claude-code)`
   Use a HEREDOC for the body.
6. Print the PR URL when done.

If $ARGUMENTS is provided, use it as additional context for the commit message.
