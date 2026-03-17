---
name: impl-implement
description: Implement a step of an implementation plan
---

Implement a specific step of an implementation plan from the given Linear issue.

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.

# Rule: Find Plan

You might be given the top-level plan or a specific step. You can differentiate by
checking if the issue is an epic (contains sub-issues) or is standlone. Step issues
are standalone, while top-level plans are epics.

When the next step to implement is ambiguous, scan all steps in the plan and
pick the very next unimplemented step. If you still aren't sure what to do, ask
the user for clarification.

Get information about the plan step issue using the `linear-issue-view` skill.

# Rule: Issue Status

Change the issue status to "In Progress" when starting work on the issue. Ensure the
parent issue also has a status of "In Progress".

Once the work is committed, change the status to "In Review". Assign yourself when starting.
If this is the last step of the plan, update the parent issue to "In Review".

Use the `linear-issue-update` skill to make changes to the issue.

# Rule: Commit Work

Use the `git-branch` skill to work from a new branch. Name the branch with the Linear 
issue id. Use the `git-commit` skill to commit your work after proving it works. 

# Rule: Show Proof

Use the `prove` skill to capture proof that the plan step is correct.

# Rule: Request Feedback

Once verified, use the `github-pr-open` skill to open a new pull request. The body
of the pull request should contain the proof you generated above.
