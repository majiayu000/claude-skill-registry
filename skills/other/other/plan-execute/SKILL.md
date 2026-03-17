---
name: plan-execute
description: This skill should be used for any non-trivial request — features, bugs, stories, epics, spikes, or multi-step tasks. It accepts a ticket URL (Jira, Linear, GitHub), a file path containing a spec, or a plain-text prompt. It assembles an agent team, breaks the work into structured tasks, and manages the full lifecycle from research through implementation, code review, deploy, and empirical verification.
---


$ARGUMENTS is either a url to a ticket containing the request, a pointer to a file containing the request or the request in text format.

If it's a ticket, use either the Jira CLI (if it's a jira ticket), the Linear CLI (if it's a linear ticket) or the Github CLI (if it's a github ticket) to read and fully understand the request, including any comments or meta data associated with the ticket.

If it's a file, read the entire file without offset or limit to understand the request.

Is this a simple request? Just execute it as usual and ignore the rest...

Otherwise:


Review all available agent types listed in the Task tool's `subagent_type` options. This includes built-in agents (like `Explore`, `general-purpose`), custom agents (from `.claude/agents/`), and plugin agents (from `.claude/settings.json` `enabledPlugins`). For each agent, explain in one sentence why it IS or IS NOT relevant to this task. Then select all agents that are relevant. You MUST justify excluding an agent — inclusion is the default.

When deciding the agents to use, consider:
* Before any task is implemented, the agent team must explore the codebase for relevant research (documentation, code, git history, etc) and update each task's `metadata.relevant_documentation` with the findings.
* Each task must be reviewed by the team to make sure their verification passes.
* Each task must have their learnings reviewed by the learner subagent.

NOTE: Every team must include the Explore agent

Create an agent team composed of the selected agents. Spawn every agent with `mode: "plan"` so they must submit their plan for team lead approval before making any file changes.

Use the TeamCreate tool to create the team before doing anything else.

Using the general-purpose agent in Team Lead session, Determine the name of this plan

Using the general-purpose agent in Team Lead session, Determine what branch to use:
1. Are we already on a feature branch with an open pull request? Use that and set the target branch to the existing target of the pull request
2. Are we on a feature branch without an open pull request? Use the branch, but ask the human what branch to target for the PR
3. Are we on an environment branch (dev, staging, main, prod, production)? Check out a feature branch named for this plan and set the target branch of the PR to the environment branch

Using the general-purpose agent in Team Lead session, Determine what type of request this is for:
1. Informational/Spike
2. Task
3. Bug
4. Feature/Story
5. Epic

IF it's a bug, Using the general-purpose agent in Team Lead session, determine how you will replicate the bug empirically:
1. Examples:
   1. Write a simple API client and call the offending API
   2. Start the server on localhost and Use the Playwright CLI or Chrome DevTools

Using the general-purpose agent in Team Lead session, determine how you will know that the task is fully complete
1. Examples
   1. Direct deploy the changes to dev and then Write a simple API client and call the offending API
   2. Start the server on localhost and then Use the Playwright CLI or Chrome DevTools

Using the general-purpose agent in Team Lead session, create tasks needed to complete the request.

Every task MUST include this JSON metadata block. Do NOT omit `skills` (use `[]` if none), `learnings` (use `[]` if none) or `verification`.

```json
{
  "plan": "<plan-name>",
  "type": "spike|bug|task|epic|story",
  "acceptance_criteria": ["..."],
  "relevant_documentation": "",
  "testing_requirements": ["..."],
  "skills": ["..."],
  "learnings": ["..."],
  "verification": {
    "type": "test|ui-recording|test-coverage|api-test|manual-check|documentation",
    "command": "the proof command",
    "expected": "what success looks like"
  }
}
```

Before any task is implemented, the agent team must explore the codebase for relevant research (documentation, code, git history, etc) and update each task's `metadata.relevant_documentation` with the findings.

Each task must be reviewed by the team to make sure their verification passes.
Each task must have their learnings reviewed by the learner subagent.

Before shutting down the team:

1. Commit ALL outstanding changes in logical batches on the branch (minus sensitive data/information) — not just changes made by the agent team. This includes pre-existing uncommitted changes that were on the branch before the plan started. Do NOT filter commits to only "task-related" files. If it shows up in git status, it gets committed (unless it contains secrets).
2. Push the changes - if any pre-push hook blocks you, create a task for the agent team to fix the error/problem whether it was pre-existing or not
3. Open a pull request with auto-merge on
4. Monitor the PR. Create a task for the agent team to resolve any code review comments by either implementing the suggestions or commenting why they should not be implemented and close the comment. Fix any failing checks and repush. Continue all checks pass
5. Monitor the deploy action that triggers automatically from the successful merge
6. If it fails, create a task for the agent team to fix the failure, open a new PR and then go back to step 4
7. Execute empirical verification. If empirical verification succeeds, you're finished, otherwise, create a task for the agent team to find out why it failed, fix it and return to step 1 (repeat this until you get all the way through)
