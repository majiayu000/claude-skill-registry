---
name: github-comment-respond
description: Respond to a Github comment
---

First, find the comment ID by listing review comments:

```
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments
```

Then reply to a specific comment:

```
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments/{comment-id}/replies -f body="Thanks, fixed!"
```

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.
