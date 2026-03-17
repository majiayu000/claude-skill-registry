---
name: impl-plan
description: Document an implementation plan based on given context
---

Write a concise yet precise and detailed implementation plan for the feature,
bug fix, etc that is described in the Linear issue provided in context.

Get information about the issue using the `linear-issue-view` skill.

# Rule: Identity

First use the `identity` skill to assume the identity of the agent.

# Rule: Content Style

Write the plan clearly, concisely, and with as much detail as necessary. Keep it
as short as possible without losing context. The plan should contain as much
detail as needed for a human or future agent to pick it up and build and deliver
a working pull-request that meets the specification of the user.

# Rule: Break It Down

Plans should be broken into steps. Represent each step of the plan as a sub issue
of the given Linear issue, turning the given issue into an epic. Each step of the
plan should map to the amount of work done in a single commit.

Create new issues using the `linear-issue-create` skill with the same status and
project as the parent issue. It should not be assigned to an owner or have a deadline.
