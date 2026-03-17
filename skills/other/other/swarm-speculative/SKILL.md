---
name: swarm-speculative
description: >-
  Speculative orchestration. Competing implementations in isolated
  worktrees, evaluated by a judge who selects the winner.
---

# Speculative Orchestration

## Overview

> This skill is invoked by the `swarm` dispatcher. You should
> already have the goal, target, and selected roles from the
> dispatcher. If invoked directly, start from step 1.

Run competing approaches in parallel, each in an isolated worktree.
A judge teammate evaluates all approaches and selects the winner.

### Why the Judge Is a Teammate

Delegate mode prevents the lead from reading files, running code,
or checking out branches. The judge needs `general-purpose` access
with `isolation: worktree` to check out each approach branch, run
tests, and evaluate code quality.

## When to Use

- Risky or exploratory changes where the best approach is unclear
- Refactoring where multiple strategies are viable
- Best-of-N quality improvement
- Any task where comparing implementations side-by-side adds value

## When NOT to Use

- The best approach is already known (use pipeline or fan-out)
- Tasks are independent analyses (use fan-out or map-reduce)
- Sequential dependencies (use pipeline)

## Checklist

You MUST complete these steps in order:

1. **Identify goal and target**
2. **Read config**
3. **Define approaches**
4. **Check for existing team**
5. **Confirm with user**
6. **Create team and tasks**
7. **Spawn implementers and judge**
8. **Handle plan approval (if enabled)**
9. **Collect approach reports**
10. **Forward to judge**
11. **Present verdict**
12. **Await user instructions**
13. **Shutdown and cleanup**

## Step 1: Identify Goal and Target

Determine from the user's request (or dispatcher context):

- **Goal**: What is being implemented? The goal should describe
  the problem, not a single solution.
  (e.g., "refactor auth module", "optimize query layer")
- **Target**: Which files, modules, or scope?

If unclear, ask the user. Do not guess scope.

## Step 2: Read Config

Read `$CLAUDE_PLUGIN_ROOT/config/swarm-roles.yaml` to get the
preset config.

From the preset, determine:

- **`approach_role`**: the role for implementer agents
  (default: `implementer`)
- **`judge_role`**: the role for the judge agent
  (default: `judge`)
- **`approach_count`**: how many competing approaches (default: 3)
- **`plan_approval`**: whether implementers must submit plans
  before implementing (default: false)

### Validation

The dispatcher has already validated config shape (role existence,
required fields, `subagent_type` values, numeric ranges). The checks
below cover speculative-specific semantics.

- **Minimum approaches**: `approach_count` must be >= 2. A single
  approach has no comparison value — report the error and abort.

## Step 3: Define Approaches

Either:

- **User specifies approaches**: user provides N distinct approach
  descriptions
- **Lead generates approaches**: analyze the problem and generate
  N distinct approach descriptions, each taking a meaningfully
  different strategy

Each approach description should be specific enough that an
implementer can work independently without further guidance.

## Step 4: Check for Existing Team

Only one team can exist per session. Before creating a new team,
check if one already exists.

If a team exists:

- **Active swarm**: warn the user that a swarm is already running
  and offer to shut it down first (`TeamDelete`).
- **Orphaned team** (from a crashed session or `/resume`): agents
  from the previous session are gone but the team and task list
  persist. Offer the user two options:
  1. **Delete and restart**: `TeamDelete` the orphaned team, then
     proceed with a fresh swarm.
  2. **Salvage completed work**: check `TaskList` for completed
     tasks, synthesize any available findings from completed tasks,
     then `TeamDelete` and optionally re-run incomplete tasks.

## Step 5: Confirm with User

Present the dispatch plan using `AskUserQuestion`:

```text
I'll dispatch a speculative execution with these parameters:
- Approaches: {N}
- Approach role: {role name}
- Judge: {judge role name}
- Plan approval: {yes|no}
- Target: {target}

Approaches:
1. {approach 1 description}
2. {approach 2 description}
3. {approach 3 description}

Each approach runs in an isolated worktree. The judge evaluates
all approaches and selects the winner.

Proceed?
```

Do NOT spawn anything until the user confirms.

## Step 6: Create Team and Tasks

### Team Naming

Use format: `swarm-speculative-{goal-slug}-{timestamp}`

Generate the timestamp from the current date/time as a Unix epoch.

### Create Team

```text
TeamCreate with team_name: "swarm-speculative-{goal-slug}-{ts}"
```

### Create Tasks

**Approach tasks** — one per approach via `TaskCreate`:

- `subject`: imperative title including approach identifier
  (e.g., "Implement approach 1: extract middleware pattern")
- `description`: detailed approach description, target files,
  expectations (commit changes, report branch name)
- `activeForm`: present-continuous spinner label
- No dependencies — all approach tasks are independent

**Judge task** — one via `TaskCreate`:

- `subject`: "Evaluate competing approaches and select winner"
- `description`: evaluation criteria, expected input count,
  verdict format
- `activeForm`: "Evaluating competing approaches"
- `addBlockedBy`: all approach task IDs — judge auto-unblocks
  when all approaches complete

## Step 7: Spawn Implementers and Judge

### Spawn Implementers

For each approach, spawn one implementer agent via `Agent` with:

- `team_name`: the team name from step 6
- `name`: `approach-{n}` (e.g., `approach-1`, `approach-2`)
- `subagent_type`: `general-purpose` (worktree isolation requires
  write access)
- `isolation`: `worktree`
- `model`: from the approach role config (if specified)
- `mode`: `"plan"` if `plan_approval: true`, omit otherwise
  (this is the Agent tool's `mode` parameter — verify it exists
  before relying on it for plan-approval gating)
- `run_in_background`: `true`
- `prompt`: composed from the parts below

#### Implementer Prompt Construction

##### Part 1: Identity and Instructions

```markdown
Your name is {name}. You are part of team {team_name}.

You are implementing approach {n} of {N} in a speculative
execution. You are working in an isolated worktree.

Instructions:
- Claim your task from TaskList, mark it in_progress
- Implement your assigned approach
- Commit your changes with a clear commit message
- Send your report to the team lead via SendMessage:
  - Include a summary field (5-10 words)
  - Include the branch name of your worktree
  - Describe what you changed and why
- Mark the task as completed
```

##### Part 2: Role Prompt

The `prompt` field from `swarm-roles.yaml` for the approach role.

##### Part 3: Approach Assignment

```markdown
## Goal

{goal description from user}

## Your Approach

{specific approach description for this implementer}

## Target

{target files, modules, or scope}

{any additional context the user provided}
```

### Spawn Judge

Spawn one judge agent via `Agent` with:

- `team_name`: the team name from step 6
- `name`: `judge`
- `subagent_type`: `general-purpose`
- `isolation`: `worktree`
- `model`: from the judge role config (if specified)
- `run_in_background`: `true`
- `prompt`: composed from the parts below

#### Judge Prompt Construction

##### Part 1: Judge Identity and Instructions

```markdown
Your name is judge. You are part of team {team_name}.

You are the judge in a speculative execution with {N} competing
approaches.

Instructions:
- Your task is blocked until all approaches complete. It will
  unblock automatically when dependencies finish — the lead will
  forward approach summaries to you shortly after.
- Once you receive all approach reports, evaluate each one:
  - Check out each approach branch
  - Run tests and verify correctness
  - Evaluate code quality, maintainability, and completeness
- Select the best approach with clear justification
- Send your verdict to the team lead via SendMessage:
  - Include a summary field (5-10 words)
  - Include the winning branch name
  - Explain why you chose it and what the others lacked
- Mark the task as completed
```

##### Part 2: Judge Role Prompt

The `prompt` field from `swarm-roles.yaml` for the judge role.

##### Part 3: Judge Goal Context

```markdown
## Goal

{goal description from user}

## Approaches Being Evaluated

1. {approach 1 description}
2. {approach 2 description}
3. {approach 3 description}

## Expected Input

You will receive {N} approach reports via SendMessage from the
team lead after all implementers complete. Each report includes
the branch name to check out.

{any additional evaluation criteria from the user}
```

## Step 8: Handle Plan Approval (if enabled)

If `plan_approval: true` in the preset config:

Implementers are spawned with `mode: "plan"`. Each must submit a
plan before implementing.

When a `plan_approval_request` arrives:

1. Review the proposed plan
2. Check it aligns with the assigned approach
3. Approve via `plan_approval_response` with `approved: true`
   — or reject with `approved: false` and feedback explaining
   what to change

This gate ensures approaches stay distinct and on-track before
implementation begins.

## Step 9: Collect Approach Reports

Implementers send reports via `SendMessage` as they complete.
Each report should include:

- What they changed
- The branch name of their worktree
- Any issues encountered

Track which approaches have reported. All approach tasks must
complete before proceeding to the judge phase.

**Error handling:**

- Idle implementer without report: send a message asking for
  status
- Failed approach: note in report, proceed with available
  approaches (judge evaluates what's available)
- Minimum 2 approaches needed for meaningful comparison

## Step 10: Forward to Judge

When all approaches have completed:

1. Collect all approach reports
2. Send all approach summaries + branch names to the judge via
   `SendMessage`
3. Include approach identifiers so the judge knows which is which
4. End the message with: "You may now claim your task and begin
   evaluating."
5. Wait for the judge to acknowledge receipt before proceeding

The judge task auto-unblocks when all approach tasks are marked
complete. The judge checks out each branch, evaluates, and sends
the verdict back to the lead.

## Step 11: Present Verdict

Once the judge sends the verdict:

Present the result to the user with branch information.

### Report Structure

```markdown
## Speculative Execution Report

**Goal:** {goal}
**Target:** {target}
**Approaches:** {N} ({M} completed successfully)

### Winning Approach

**Branch:** {winning branch name}
**Approach:** {approach description}

{judge's justification for selecting this approach}

### Other Approaches

#### Approach {n}: {description}
**Branch:** {branch name}
{judge's evaluation — why it wasn't selected}

...

### Next Steps

To merge the winning approach:
`git merge {winning-branch-name}`

To inspect any approach:
`git diff main...{branch-name}`
```

## Step 12: Await User Instructions

After presenting the verdict:

- Do NOT merge any branch automatically
- Do NOT shut down the team automatically
- Do NOT proceed past reporting without user input

Wait for the user to decide whether to merge, inspect further,
or discard.

## Step 13: Shutdown and Cleanup

When the user indicates they're done:

1. Send `shutdown_request` to each agent via `SendMessage`
   (include the monitor agent if `watchdog: true` was active)
2. Wait for `shutdown_response` from each. If an agent does not
   respond after a reasonable wait, send one nudge message. If
   still unresponsive, proceed — the agent may have crashed or
   terminated.
3. Call `TeamDelete` to clean up. `TeamDelete` is the authoritative
   cleanup mechanism — it will fail if active agents remain. If
   it fails, retry after unresponsive agents have timed out.

Note: worktree branches persist after cleanup. The user can merge
or delete them independently.

## Design Constraints

- **Isolated worktrees**: each implementer works in its own
  worktree — no interference between approaches
- **Judge is a teammate**: delegate mode prevents lead from
  branch evaluation — the judge has `general-purpose` access
- **Approaches are independent**: no dependencies between them
- **Plan approval is optional**: controlled by preset config
- **One team per session**: check before creating
- **User controls lifecycle**: never auto-shutdown or auto-merge
