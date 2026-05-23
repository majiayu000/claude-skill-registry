---
name: pr-summary
description: Create a PR with dev as base using the pull request template. Use when opening a new PR.
user-invocable: true
disable-model-invocation: true
---

Summarize the latest changes in this branch to create a pull request on GitHub.

<workflow-steps>

1. Compare the current branch against default branch to see what changes need to be described in the pull request. Make sure to only focus on the finalized implementation details. Since pull requests tend to have work-in-progress commits at the beginning, you should be extra mindful on whether these are still relevant in the finalized snapshot.
2. Use the [pull request template](assets/pull-request-template.md) to generate a `.claude/scratchpad/PR.md`.
3. Pause here and prompt the user to check the `.claude/scratchpad/PR.md` before proceeding.
4. Once edited and approved by the user, fill in the missing details in the following script and then run it:
   ```bash
   gh pr create --base dev --head "$(git rev-parse --abbrev-ref HEAD)" --title '[TICKET-123] category: short title' --body-file .claude/scratchpad/PR.md
   ```
5. Delete `.claude/scratchpad/PR.md` once successfully submitted.

</workflow-steps>
