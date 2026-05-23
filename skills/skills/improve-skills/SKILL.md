---
name: improve-skills
description: Improve skill(s) by analyzing the current session.
disable-model-invocation: true
user-invocable: true
argument-hint: "extra commentary"
---

# Improve skills

Read and analyze the usage of skill(s) in the current session:

- read the conversation,
- focus on how the skill(s) were used,
- think of what worked, what did not work and new cases to cover,
- think of what was needs to be generalised,
- propose improvements.

The objective is to:

- keep skills simple,

Current session id: `${CLAUDE_SESSION_ID}`.

Read the session. Find interesting patterns. Ultrathink about if & what to improve.
Perform chain-of-thought reasoning. Consider pros & cons. Balance the tradeoffs.


## Conversation patterns to flag

When analyzing conversation, note all problems. This should include the following negative (-), positive (+) and (?) neutral signals:

- (-) User pointed out the implementation was incorrect.
- (-) User provided a very long list of improvements to implementation.
- (-) User mentioned that the changes broke CI/CD.
- (-) User asked repeatedly for the same thing.
- (-) Agent spent long time trying to figure out something (and guidance would help).
- (-) Agent got distracted from the main task and the objective was never reached.
- (-) User noted an agent diverged from the documented standards or existing code patterns without good reason.
- (-) Commands execution failed multiple times.
- (-) User had to fix the file after agent's changes.

- (?) User reflected on the implementation and asked for improvements by introducing new constraints.
- (?) New use-case or pattern emerged.

- (+) User accepted plan or code without comment.
- (+) User said "that's all".
- (+) User noted that new code pattern is brilliant.
- (+) User asked to commit the code produced by the agent and without modifications.
- (+) User asked an agent to proceed to the next objective.


## The balance: general & short vs detailed & long

You need to balance the impact of improvements versus the impact of not making changes:

- expanding a description may improve agent accuracy by addressing some use-case,
- but this will use more instruction tokens and consume context, which may lead to degraded performance.

Therefore:

- If a problem is rare and its improvement would cause context-engineering issues: not worth improving.
- If a problem is expected to reoccur often and improvement is short: worth implementing.

For other cases, think hard what to propose to the user.

Remember, the user will make the ultimate decision what to do with the findings.


## Example session

After a MR code-review session triggered by `/mr-review` skill,
when the user says "Improve the GitLab skill",
the agent will think hard about how the skill was used
and may respond with the following:

```
# Skills improvements

## 1. The `glab` command invocation

Observation:

- The agent invoked `glab` command incorrectly 6 times before figuring out how to do it properly.
- (CRITICAL) This will most likely reoccur on each skill usage.

Context of the situation / Analysis:

- An agent was trying to obtain MR details.

Remedy:

- Provide an agent with information about MR directly and/or examples how to obtain fruther MR details.
- Examples should include: `glab mr view ...`, `glab mr diff ...`, and `glab api /projects/:id/merge_requests/...`.

Implementation proposals:

a. (best) Update the `mr-review` skill: include MR details automatically by injecting dynamic context.

   Pros & cons:

   - ✅ GOOD: deterministic approach
   - ✅ GOOD: `glab` commands will be executed in parallel
   - ⚠️ BREAKING CHANGE: `mr-review` will require strict argument format - the IID of an MR

   Implementation:

   - At the top of `.claude/command/mr-review.md` inject dynamic context using bang + backtick syntax:

         ## MR request context

         - MR diff: ...
         - MR info: ...
         - MR extra: ...

   - Update frontmatter of a skill: set `argument-hint: "[mr-iid]"`.

b. (good) Update the `mr-review` skill - add a section with `glab` commands examples

   Pros & cons:

   - ✅ GOOD: Some benefits of proposal "A" without breaking changes
   - 🟡 TRADEOFF: `glab` commands will be executed sequentially

   Include example commands in the `.claude/skills/mr-review/`:

   - `glab mr view ...`
   - `glab mr diff ...`
   - `glab api /projects/:id/merge_requests/...`

   Update `CLAUDE.md` section `# References` with an entry:

       - `docs/glab-mr.md` - how to get MR details from GitLab

c. (comprehensive) Create a new `gitlab` skill that can be auto-loaded (`user-invocable: false`)
   and will guide an agent on how to query GitLab.

   This will require a dedicated SDD session to implement.

   Pros & cons:

   - ✅ GOOD: Some benefits of proposal "A" without breaking changes
   - 🟡 TRADEOFF: `glab` commands will be executed sequentially
   - 🔴 BAD: Lots of effort

   Note: the implementation must ensure that the `gitlab` skill is properly split
   into smaller files (progressive disclosure) or else the context will be polluted
   with lots of unrelated commands.

d. (comprehensive) Create a new `gitlab` skill that can be auto-loaded (`user-invocable: false`),
   will have its own context (`context: fork`), and will require specific instructions.

   Very similar to proposal "C", however this will run GitLab operations in isolated fresh context.
   This new skill will require description of what to do in the arguments passed
   and will return only results to main conversation.

   Pros & cons:

   - ✅ GOOD: Some benefits of proposal "A" without breaking changes
   - ✅ GOOD: Less information kept in main context
   - 🟡 TRADEOFF: `glab` commands will be executed sequentially
   - 🔴 BAD: Lots of effort


## 2. User did not want to fix the bug with REST API param processing.

Observation:

- The agent noted that the REST API params are parsed incorrectly and marked the problem as MAJOR.
- The user confirmed the problem as important.
- The user rejected the problem as MR-related noting that the problem existed before the MR. User said they will create a JIRA ticket.

Context of the situation / Analysis:

- The user appreciates to find bugs in MR.
- The user may opt to fix bugs at a later time.

Remedy:

- Nothing. Agent worked as expected.
```
