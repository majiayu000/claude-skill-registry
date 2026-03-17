---
name: swarm-map-reduce
description: >-
  Map-reduce orchestration. Parallel mappers process input chunks
  independently, then a dedicated reducer merges all outputs.
---

# Map-Reduce Orchestration

## Overview

> This skill is invoked by the `swarm` dispatcher. You should
> already have the goal, target, and selected roles from the
> dispatcher. If invoked directly, start from step 1.

Fan-out with structured input splitting and a dedicated reduce
phase. Mappers process independent chunks in parallel; a reducer
teammate merges all mapper outputs into a unified result.

### Why the Reducer Is a Teammate

Delegate mode prevents the lead from reading files, running code,
or writing output. The reducer needs `general-purpose` access to
produce structured merged artifacts. It is spawned as a teammate,
not handled by the lead.

## When to Use

- Large-scale analysis where input can be partitioned
- Codebase audits across many directories or modules
- Document processing at scale
- Any task where results need structured merging

## When NOT to Use

- Tasks don't partition cleanly (use fan-out with specialists)
- Sequential dependencies between chunks (use pipeline)
- Competing approaches (use speculative)

## Checklist

You MUST complete these steps in order:

1. **Identify goal and target**
2. **Read config**
3. **Determine the split**
4. **Check for existing team**
5. **Confirm with user**
6. **Create team and tasks**
7. **Spawn mappers and reducer**
8. **Collect mapper findings**
9. **Forward to reducer**
10. **Present final result**
11. **Await user instructions**
12. **Shutdown and cleanup**

## Step 1: Identify Goal and Target

Determine from the user's request (or dispatcher context):

- **Goal**: What is being analyzed? (e.g., "audit codebase",
  "review all modules")
- **Target**: Which directory, repo, or scope to split?

If unclear, ask the user. Do not guess scope.

## Step 2: Read Config

Read `$CLAUDE_PLUGIN_ROOT/config/swarm-roles.yaml` to get the
preset config.

From the preset, determine:

- **`map_role`**: the role for mapper agents (default: `mapper`)
- **`reduce_role`**: the role for the reducer agent (default:
  `reducer`)
- **`split_strategy`**: how to partition the target

### Validation

The dispatcher has already validated config shape (role existence,
required fields, `subagent_type` values). The checks below cover
map-reduce-specific semantics.

- **Reducer capability**: the `reduce_role` must have
  `subagent_type: general-purpose`. A reducer with `Explore` cannot
  write merged output. If the reducer role uses `Explore`, **warn**
  and recommend changing it — or note that `isolation: worktree`
  will override it to `general-purpose` at spawn time.
- **Split strategy required**: `split_strategy` must be present and
  one of `by-directory`, `by-file-count`, or `manual`. If absent or
  unrecognized, report the error and abort.

## Step 3: Determine the Split

Partition the target into chunks based on `split_strategy`:

### `by-directory`

List top-level directories in the target path. One mapper per
directory.

### `by-file-count`

Count files in the target. Split into roughly equal groups
(default: ceil(total / 5) files per group, minimum 3 mappers).

### `manual`

Ask the user to specify the split. Present the target structure
and let them define chunk boundaries.

The number of chunks determines the number of mappers.

### Split Validation

- **Minimum chunks**: the split must produce at least 1 chunk. If the
  target is empty or the split yields 0 chunks, report the error and
  abort.
- **Single chunk bypass**: if the split yields exactly 1 chunk, warn
  the user that map-reduce overhead is unnecessary and offer two
  options:
  1. Switch to fan-out (recommended — no reducer needed)
  2. Proceed without a reducer — spawn one mapper, skip the reducer
     entirely, and present the mapper's output directly as the final
     result (skip steps 7b, 9)
- **Maximum mappers**: if the split yields more than 7 chunks, warn
  the user that large swarms may hit context limits. Offer to batch
  directories into groups to reduce mapper count.

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
I'll dispatch a map-reduce with these parameters:
- Mappers: {N} (one per chunk)
- Reducer: 1 ({reduce_role})
- Split strategy: {strategy}
- Target: {target}

Chunks:
1. {chunk description / directory / file group}
2. {chunk description}
...

The reducer will merge all mapper outputs after they complete.

Proceed?
```

Do NOT spawn anything until the user confirms.

## Step 6: Create Team and Tasks

### Team Naming

Use format: `swarm-map-reduce-{goal-slug}-{timestamp}`

Generate the timestamp from the current date/time as a Unix epoch.

### Create Team

```text
TeamCreate with team_name: "swarm-map-reduce-{goal-slug}-{ts}"
```

### Create Tasks

**Mapper tasks** — one per chunk via `TaskCreate`:

- `subject`: imperative title including chunk identifier
  (e.g., "Audit src/auth/ directory")
- `description`: detailed scope, specific files in this chunk,
  reporting format expectations
- `activeForm`: present-continuous spinner label
- No dependencies — all mapper tasks are independent

**Reducer task** — one via `TaskCreate`:

- `subject`: "Merge mapper outputs into unified report"
- `description`: merge instructions, expected input count,
  output format
- `activeForm`: "Merging mapper outputs"
- `addBlockedBy`: all mapper task IDs — reducer auto-unblocks
  when all mappers complete

## Step 7: Spawn Mappers and Reducer

### Spawn Mappers

For each chunk, spawn one mapper agent via `Agent` with:

- `team_name`: the team name from step 6
- `name`: `mapper-{n}` (e.g., `mapper-1`, `mapper-2`)
- `subagent_type`: from the map role config
- `model`: from the map role config (if specified)
- `run_in_background`: `true`
- `prompt`: composed from the parts below

#### Isolation Handling

Before spawning, check the map role's `isolation` field:

- If `isolation: worktree` is set:
  - Override `subagent_type` to `general-purpose`
  - Print a note: `Role {name}: using general-purpose (worktree
    isolation requires write access)`
  - Pass `isolation: "worktree"` to the `Agent` tool call
- If `isolation` is absent: use the role's `subagent_type` as-is

#### Mapper Prompt Construction

##### Part 1: Identity and Instructions

```markdown
Your name is {name}. You are part of team {team_name}.

You are mapper {n} of {N} in a map-reduce operation.

Instructions:
- Claim your task from TaskList, mark it in_progress, then
  completed when done.
- Send your findings to the team lead via SendMessage when
  complete.
- Include a summary field in your message (5-10 words).
- Use consistent output format so the reducer can merge easily.
```

##### Part 2: Role Prompt

The `prompt` field from `swarm-roles.yaml` for the map role.

##### Part 3: Chunk Assignment

```markdown
## Goal

{goal description from user}

## Your Chunk

{specific chunk assignment — directories, files, or scope}

{any additional context the user provided}
```

### Spawn Reducer

Spawn one reducer agent via `Agent` with:

- `team_name`: the team name from step 6
- `name`: `reducer`
- `subagent_type`: from the reduce role config
  (typically `general-purpose`)
- `model`: from the reduce role config (if specified)
- `run_in_background`: `true`
- `prompt`: composed from the parts below

#### Reducer Prompt Construction

##### Part 1: Reducer Identity and Instructions

```markdown
Your name is reducer. You are part of team {team_name}.

You are the reducer in a map-reduce operation with {N} mappers.

Instructions:
- Your task is blocked until all mappers complete. It will unblock
  automatically when dependencies finish — the lead will forward
  mapper outputs to you shortly after.
- Once you receive all mapper outputs, merge them into a unified
  result.
- Claim your task from TaskList, mark it in_progress, then
  completed when done.
- Send your merged result to the team lead via SendMessage.
- Include a summary field in your message (5-10 words).
- Mark the task as completed.
```

##### Part 2: Reducer Role Prompt

The `prompt` field from `swarm-roles.yaml` for the reduce role.

##### Part 3: Reducer Goal Context

```markdown
## Goal

{goal description from user}

## Expected Input

You will receive {N} mapper outputs via SendMessage from the team
lead after all mappers complete.

{any additional context about desired output format}
```

## Step 8: Collect Mapper Findings

Mappers send findings via `SendMessage` as they complete. Messages
are delivered automatically.

Track which mappers have reported. All mapper tasks must complete
before proceeding to the reduce phase.

**Error handling:**

- Idle mapper without findings: send a message asking for status
- No response after nudge: note in report, proceed with available
  findings
- Unresponsive mapper blocking reducer: manually mark the failed
  mapper's task as completed (or deleted) to unblock the reducer.
  Note the missing chunk in the forwarded data.
- All mappers must complete (or be noted as failed) before
  forwarding to reducer

## Step 9: Forward to Reducer

When all mappers have completed:

1. Collect all mapper findings
2. Send all mapper outputs to the reducer via `SendMessage` in a
   single message (or sequentially if too large)
3. Include mapper identifiers so the reducer knows which chunk
   each output covers
4. End the message with: "You may now claim your task and begin
   reducing."
5. Wait for the reducer to acknowledge receipt before proceeding

The reducer task auto-unblocks when all mapper tasks are marked
complete. The reducer claims its task, merges the outputs, and
sends the unified result back to the lead.

## Step 10: Present Final Result

Once the reducer sends its merged result:

Present the unified report to the user. Include both the merged
result and a note about how many mappers contributed.

### Report Structure

```markdown
## Map-Reduce Analysis Report

**Goal:** {goal}
**Target:** {target}
**Mappers:** {N} ({M} reported successfully)
**Reducer:** {reducer role name}

### Merged Findings

{reducer's unified output}

### Summary
{brief overall assessment — coverage, key themes, confidence}
```

## Step 11: Await User Instructions

After presenting the report:

- Do NOT fix issues found
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

- **Reducer is a teammate**: delegate mode prevents lead from
  doing the merge — the reducer has `general-purpose` access
- **Mappers are independent**: no dependencies between mapper tasks
- **Structured output**: mappers must use consistent format for
  clean merging
- **One team per session**: check before creating
- **User controls lifecycle**: never auto-shutdown
