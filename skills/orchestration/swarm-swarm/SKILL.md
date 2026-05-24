---
name: swarm-swarm
description: >-
  Self-claiming pool orchestration. Workers race to claim tasks from
  a shared pool, loop until the pool is empty.
---

# Swarm Orchestration (Self-Claiming Pool)

## Overview

> This skill is invoked by the `swarm` dispatcher. You should
> already have the goal, target, and selected roles from the
> dispatcher. If invoked directly, start from step 1.

Orchestrate a pool of interchangeable workers that self-assign from
a shared task list. Workers claim tasks, complete them, and loop
back for more until the pool is empty.

### How This Differs from Fan-Out

- **Fan-out**: one specialist per role, each gets a unique task
- **Swarm**: interchangeable workers share a task pool. Workers
  loop (claim multiple tasks). Task pool can be larger than worker
  count.

## When to Use

- Large workloads with many independent, similar-sized tasks
- Tasks that don't require specialized expertise per task
- The number of tasks exceeds the number of workers

## When NOT to Use

- Tasks require different specialist expertise (use fan-out)
- Sequential dependencies between tasks (use pipeline)
- Tasks need structured merging (use map-reduce)

## Checklist

You MUST complete these steps in order:

1. **Identify goal and target**
2. **Read config and determine worker role/count**
3. **Decompose target into work units**
4. **Check for existing team**
5. **Confirm with user**
6. **Create team and tasks**
7. **Spawn workers**
8. **Collect findings**
9. **Synthesize and present report**
10. **Await user instructions**
11. **Shutdown and cleanup**

## Step 1: Identify Goal and Target

Determine from the user's request (or dispatcher context):

- **Goal**: What is being done? (e.g., "audit all modules",
  "review all API endpoints")
- **Target**: Which files, directories, or scope?

If unclear, ask the user. Do not guess scope.

## Step 2: Read Config and Determine Workers

Read `$CLAUDE_PLUGIN_ROOT/config/swarm-roles.yaml` to get the
preset config.

From the preset, determine:

- **`worker_role`**: the role all workers share (default:
  `researcher`)
- **`worker_count`**: how many concurrent workers to spawn
  (default: 3)

### Validation

The dispatcher has already validated config shape (role existence,
required fields, `subagent_type` values, numeric ranges). The checks
below cover swarm-specific semantics.

- **Scale warning**: if `worker_count` > 7, warn the user that large
  swarms may hit context limits and recommend 3-5 workers.

## Step 3: Decompose Target into Work Units

Analyze the target to determine discrete work units. Each work unit
becomes one task in the pool:

- One task per module or directory
- One task per file group
- One task per endpoint or component

The number of tasks can (and often should) exceed the worker count.
Workers will loop through the pool.

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
I'll dispatch a swarm with these parameters:
- Worker role: {role name}
- Worker count: {N}
- Task pool: {M} tasks
- Target: {files/scope}

Tasks:
1. {work unit 1}
2. {work unit 2}
...

Proceed?
```

Do NOT spawn anything until the user confirms.

## Step 6: Create Team and Tasks

### Team Naming

Use format: `swarm-swarm-{goal-slug}-{timestamp}`

Generate the timestamp from the current date/time as a Unix epoch.

### Create Team

```text
TeamCreate with team_name: "swarm-swarm-{goal-slug}-{timestamp}"
```

### Create Tasks

One task per work unit via `TaskCreate`:

- `subject`: imperative title for the work unit
- `description`: detailed scope, specific files/modules, reporting
  expectations
- `activeForm`: present-continuous spinner label

All tasks are independent — no `blocks`/`blockedBy` dependencies.
No owner assigned — workers self-claim.

## Step 7: Spawn Workers

Spawn N worker agents via `Agent` with:

- `team_name`: the team name from step 6
- `name`: `worker-{n}` (e.g., `worker-1`, `worker-2`)
- `subagent_type`: from the worker role config
- `model`: from the worker role config (if specified)
- `run_in_background`: `true`
- `prompt`: composed from the parts below

### Isolation Handling

Before spawning, check the worker role's `isolation` field:

- If `isolation: worktree` is set:
  - Override `subagent_type` to `general-purpose`
  - Print a note: `Role {name}: using general-purpose (worktree
    isolation requires write access)`
  - Pass `isolation: "worktree"` to the `Agent` tool call
- If `isolation` is absent: use the role's `subagent_type` as-is

### Prompt Construction

#### Part 1: Identity and Loop Instructions

```markdown
Your name is {name}. You are part of team {team_name}.

You are a pool worker. Your workflow is a loop:

1. Check TaskList for unclaimed tasks (status: pending, no owner)
2. Claim one by setting yourself as owner and marking it in_progress
3. Verify the claim: call TaskGet on the task you claimed. If the
   owner is not your name, another worker claimed it first — go back
   to step 1
4. Complete the work described in the task
5. Send your findings to the team lead via SendMessage
   - Include a summary field (5-10 words)
   - Include the task subject in your message
6. Mark the task as completed
7. Go back to step 1

When no unclaimed tasks remain, go idle.
```

#### Part 2: Role Prompt

The `prompt` field from `swarm-roles.yaml` for the worker role.

#### Part 3: Goal and Target Context

```markdown
## Goal

{goal description from user}

## Target

{target scope — workers will self-select from the task pool}

{any additional context the user provided}
```

## Step 8: Collect Findings

Workers send findings via `SendMessage` after each task they
complete. Messages are delivered automatically.

**Normal flow:** Workers loop through multiple tasks, sending
findings after each. Workers go idle when the pool is empty.

**Error handling:**

- Idle worker without findings: send a message asking for status
- No response after nudge: note in report, mark tasks as blocked
- Stuck tasks: reassign by removing the owner if a worker stalls

## Step 9: Synthesize and Present Report

Once all tasks are completed (or you've noted stuck ones):

Synthesize findings into a unified report organized by theme or
severity, not by worker or task.

### Report Structure

```markdown
## Swarm Analysis Report

**Goal:** {goal}
**Target:** {target}
**Workers:** {N workers, M tasks completed}

### Critical Issues
{findings rated critical/high, with file:line references}

### Important Issues
{findings rated medium/important}

### Suggestions
{lower-priority findings and recommendations}

### Summary
{brief overall assessment — 2-3 sentences}
```

## Step 10: Await User Instructions

After presenting the report:

- Do NOT fix issues workers found
- Do NOT shut down the team automatically
- Do NOT proceed past reporting without user input

Wait for the user to decide next steps.

## Step 11: Shutdown and Cleanup

When the user indicates they're done:

1. Send `shutdown_request` to each worker via `SendMessage`
   (include the monitor agent if `watchdog: true` was active)
2. Wait for `shutdown_response` from each. If an agent does not
   respond after a reasonable wait, send one nudge message. If
   still unresponsive, proceed — the agent may have crashed or
   terminated.
3. Call `TeamDelete` to clean up. `TeamDelete` is the authoritative
   cleanup mechanism — it will fail if active agents remain. If
   it fails, retry after unresponsive agents have timed out.

## Design Constraints

- **Interchangeable workers**: all workers use the same role prompt
- **Self-claiming**: workers find and claim their own tasks
- **No dependencies**: all tasks in the pool are independent
- **One team per session**: check before creating
- **Lead synthesizes**: present a unified report, not raw worker
  output
- **User controls lifecycle**: never auto-shutdown
