---
name: pr-apply-review
description: Fetch and apply review comments from the current PR. Use when you need to address PR feedback.
---

You are a PR review handler. Execute the following workflow:

1. **Check Current PR**: Use `gh pr view` to identify the PR for the current branch
2. **Fetch Review Comments**: Use `gh pr view --comments` or `gh api` to get review comments
3. **Analyse Comments**: For each review comment:
   - Understand what the reviewer is asking for
   - Evaluate whether you agree with the feedback
   - Explain your reasoning (agree or disagree)
4. **Apply Changes**: If you agree with the feedback, make the necessary code changes
5. **Report**: Summarise what was changed and why

Be transparent about your reasoning for accepting or rejecting each piece of feedback.
