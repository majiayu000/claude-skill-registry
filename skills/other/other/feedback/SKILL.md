---
name: impl-feedback
description: Process feedback on an implementation
---

Synthesize feedback on a specific step of an implementation plan from the given
Github pull request. Feedback is provided as pull request comments.

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.

# Rule: Commit Work

Use the `git-branch` skill to work from the existing branch for the pull request.  
Use the `git-commit` skill to commit your work after proving it works.

# Rule: Update Proof

Use the `prove` skill to capture proof that the feedback has been incorporated.

# Rule: Update Comments

Respond to each comment with proof that the comment was addressed, or requesting
more information if needed. Use the `github-comment-respond` skill to respond.

# Rule: Request Review

If all feedback has been addressed fully (e.g. you aren't waiting on a reply) then
re-request review from the reviewer. Use the `github-pr-update` skill.
