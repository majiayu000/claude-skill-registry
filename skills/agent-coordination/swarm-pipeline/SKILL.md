---
name: swarm-pipeline
description: >-
  Pipeline and task-graph orchestration. Sequential stages with
  dependency edges — linear chain or arbitrary DAG.
---

# Pipeline / Task Graph Orchestration

## Overview

> This skill is invoked by the `swarm` dispatcher. You should
> already have the goal, target, and selected roles from the
> dispatcher. If invoked directly, start from step 1.

Orchestrate sequential stages with dependency edges. Handles two
config shapes:

- **`pattern: pipeline`** with `stages` array — linear chain where
  each stage blocks the next. Stages support multiple `roles`.
- **`pattern: task-graph`** with `nodes` map — arbitrary DAG with
  `depends_on` edges supporting fan-in and fan-out. Each node has
  a single `role` (not a list).

Pipeline is a degenerate task-graph (linear topology). Both use the
same `blocks`/`blockedBy` primitives for automatic stage
transitions.

## When to Use

- Multi-stage workflows where output feeds the next stage
- Implementation + review chains
- Database migrations with dependent steps
- Any workflow with sequential dependencies

## When NOT to Use

- All tasks are independent (use fan-out or swarm)
- Tasks need structured merging with a dedicated reducer
  (use map-reduce)
- Competing approaches (use speculative)

## Checklist

You MUST complete these steps in order:

1. **Identify goal and target**
2. **Read config and determine topology**
3. **Build dependency graph**
4. **Check for existing team**
5. **Confirm with user**
6. **Create team and tasks**
7. **Spawn agents**
8. **Relay context between stages**
9. **Collect findings**
10. **Synthesize and present report**
11. **Await user instructions**
12. **Shutdown and cleanup**

## Step 1: Identify Goal and Target

Determine from the user's request (or dispatcher context):

- **Goal**: What is being done?
- **Target**: Which files, directories, or scope?

If unclear, ask the user. Do not guess scope.

## Step 2: Read Config and Determine Topology

Read `$CLAUDE_PLUGIN_ROOT/config/swarm-roles.yaml` to get the
preset config.

Determine the topology:

- If preset has `stages` array → **pipeline** (linear chain)
- If preset has `nodes` map → **task-graph** (arbitrary DAG)

### Validation

The dispatcher has already validated config shape (role existence,
required fields, `subagent_type` values). The checks below cover
pipeline/task-graph-specific semantics.

- **Non-empty topology**: pipeline must have at least 1 stage; task
  graph must have at least 1 node. If empty, report the error and
  abort.
- **Non-empty stage roles**: each `stages[].roles` list must contain
  at least 1 entry. A stage with no roles would block the relay
  indefinitely. If empty, report the error and abort.
- **Single-stage warning**: if a pipeline has exactly 1 stage, warn
  the user that this degenerates to fan-out but uses pipeline hook
  semantics (requiring commit or SendMessage instead of just
  SendMessage). Offer to switch to fan-out for simpler gating.
- **No cycles** (task-graph): validate that `depends_on` references
  do not create cycles. If cycles found, report the error and abort.
- **Valid depends_on** (task-graph): all `depends_on` entries must
  reference existing node names.

## Step 3: Build Dependency Graph

### For Pipeline (`stages`)

Convert the linear `stages` array into a dependency chain:

```text
stage[0] → stage[1] → stage[2] → ...
```

Each stage blocks the next. Stages with multiple roles create
parallel tasks within the stage (fan-out within a stage, sequential
between stages).

### For Task Graph (`nodes`)

Read each node's `depends_on` list to build the DAG:

```text
analyze → migrate-users ──→ validate
       → migrate-orders ──↗
```

All graph validation (cycles, dangling references) was completed in
step 2. This step is construction only — do not re-validate here.

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
I'll dispatch a {pipeline|task-graph} with these stages:

Stage 1: {name} — {roles}
  ↓
Stage 2: {name} — {roles} (blocked by: stage 1)
  ↓
Stage 3: {name} — {roles} (blocked by: stage 2)

Target: {files/scope}

Proceed?
```

For task-graph, show the DAG structure with dependency arrows.

Do NOT spawn anything until the user confirms.

## Step 6: Create Team and Tasks

### Team Naming

- Pipeline: `swarm-pipeline-{goal-slug}-{timestamp}`
- Task Graph: `swarm-task-graph-{goal-slug}-{timestamp}`

Generate the timestamp from the current date/time as a Unix epoch.

### Create Team

```text
TeamCreate with team_name: "swarm-{topology}-{goal-slug}-{ts}"
```

### Create Tasks

One task per role per stage/node via `TaskCreate`:

- `subject`: imperative title including stage name
- `description`: detailed scope, target, stage context, reporting
  expectations
- `activeForm`: present-continuous spinner label

Set dependencies via `TaskUpdate`:

- For pipeline: each stage's tasks have `addBlockedBy` pointing to
  the previous stage's tasks
- For task-graph: each node's tasks have `addBlockedBy` matching
  the node's `depends_on` references

First stage / root nodes have no blockers — they start immediately.

**Relay tasks** — one per stage transition via `TaskCreate`:

- `subject`: "Relay stage {N} findings to stage {N+1}"
- `description`: "Collect findings from stage {N} agents, forward
  to stage {N+1} agents via SendMessage, wait for acknowledgment"
- `activeForm`: "Relaying stage {N} findings"
- `addBlockedBy`: all task IDs from stage N — relay auto-unblocks
  when the source stage completes
- Relay tasks for stage N+1 should be added to the `addBlockedBy`
  list of stage N+1's agent tasks (in addition to stage N's tasks)

This makes relay a visible, trackable step in the task list. The
lead claims and completes relay tasks as part of step 8.

## Step 7: Spawn Agents

For each role in each stage/node, spawn one agent via `Agent` with:

- `team_name`: the team name from step 6
- `name`: `{stage-name}-{role-name}` (e.g., `implement-implementer`)
- `subagent_type`: from the role config
- `model`: from the role config (if specified)
- `isolation`: from the role config (if specified — see isolation
  handling below)
- `run_in_background`: `true`
- `prompt`: composed from the parts below

### Isolation Handling

Before spawning, check each role's `isolation` field:

- If `isolation: worktree` is set:
  - Override `subagent_type` to `general-purpose`
  - Print a note: `Role {name}: using general-purpose (worktree
    isolation requires write access)`
  - Pass `isolation: "worktree"` to the `Agent` tool call
- If `isolation` is absent: use the role's `subagent_type` as-is

### Prompt Construction

#### Part 1: Identity and Stage Instructions

```markdown
Your name is {name}. You are part of team {team_name}.

You are working on stage "{stage-name}" of a {pipeline|task-graph}.

Instructions:
- Claim your task from TaskList, mark it in_progress, then
  completed when done.
- Send your findings to the team lead via SendMessage when
  complete.
- Include a summary field in your message (5-10 words).

Your task may be blocked by earlier stages. When it unblocks, do
NOT claim it immediately. Wait for the team lead to send you a
"start" message via SendMessage containing upstream findings.
Only claim your task and begin work AFTER receiving the lead's
start message.

First-stage agents (no blockers): claim your task immediately.
```

#### Part 2: Role Prompt

The `prompt` field from `swarm-roles.yaml` for this role.

#### Part 3: Goal, Target, and Upstream Context

```markdown
## Goal

{goal description from user}

## Target

{target files, scope, or context}

## Upstream Context

{forwarded findings from completed predecessor stages — empty for
first stage, populated by lead relay in step 8}

{any additional context the user provided}
```

## Step 8: Relay Context Between Stages

This is the lead's core responsibility in pipeline orchestration.

When a stage completes (all its tasks are done and agents have
sent findings):

1. Collect all findings from that stage's agents
2. Create a relay task via `TaskCreate`:
   - `subject`: "Relay stage {N} findings to stage {N+1}"
   - `description`: summary of what to forward
   - `activeForm`: "Relaying stage findings"
   - `addBlockedBy`: all task IDs from the completed stage
3. Forward the findings to the next stage's agents via
   `SendMessage` — include the stage name and a summary of what
   was done. End the message with: "You may now claim your task
   and begin work."
4. Wait for each downstream agent to acknowledge receipt via
   `SendMessage` before marking the relay task completed
5. Mark the relay task as completed

Do NOT proceed to the next relay until downstream agents have
acknowledged. If an agent does not acknowledge, nudge it.

### Context Passing Mechanisms

- **SendMessage relay** (default): lead forwards findings between
  stages as messages
- **Worktree chain** (when roles have `isolation: worktree`): each
  stage works on the branch from the previous stage. The lead
  includes the branch name in the forwarded context so the next
  stage can check it out.

## Step 9: Collect Findings

As each stage completes, its agents send findings via
`SendMessage`. The lead accumulates findings across all stages.

**Normal flow:** stages complete sequentially (or per the DAG).
Each stage's agents go idle after sending.

**Error handling:**

- Stage agent idle without findings: send a message asking for
  status
- Blocked task not unblocking: check if predecessor is truly
  complete, intervene if stuck
- Stage failure: notify user, ask whether to continue with
  remaining stages or abort

## Step 10: Synthesize and Present Report

Once all stages are complete:

Synthesize findings into a unified report that shows the
progression through stages.

### Report Structure

```markdown
## Pipeline Analysis Report

**Goal:** {goal}
**Target:** {target}
**Topology:** {pipeline|task-graph}

### Stage: {stage-1-name}
{findings from stage 1}

### Stage: {stage-2-name}
{findings from stage 2, including how they built on stage 1}

...

### Summary
{brief overall assessment — how the pipeline progressed and
final outcome}
```

## Step 11: Await User Instructions

After presenting the report:

- Do NOT fix issues agents found
- Do NOT shut down the team automatically
- Do NOT proceed past reporting without user input

Wait for the user to decide next steps.

## Step 12: Shutdown and Cleanup

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

## Design Constraints

- **Sequential execution**: stages run in dependency order
- **Parallel within stages**: multiple roles in one stage run
  concurrently
- **Lead relays context**: the lead is responsible for forwarding
  findings between stages
- **One team per session**: check before creating
- **User controls lifecycle**: never auto-shutdown
