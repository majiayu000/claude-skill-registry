---
name: esper:batch
description: Decompose a feature set into a queue of increments. Creates a batch parent with child increments. Stays in plan mode until `esper:go`.
---

You are working in batch mode — decomposing a larger feature into a queue of increments.

## Step 1: Read context

Run `esperkit context get` to understand the current state.
Read `.esper/CONSTITUTION.md` for project constraints.
Run `esperkit spec index` to see the spec tree.

## Step 2: Gather the feature set

Ask the user what they want to build. This should be a larger feature or set of related changes that will require multiple increments.

If the user provides a spec file, read it: `esperkit spec get <file>`

## Step 3: Decompose into increments

Break the feature set into a queue of increments:
1. Each increment should be independently shippable
2. Order them by dependency (what must come first)
3. Each increment should be small enough for a single implementation session
4. Identify which spec files each increment touches
5. Consider the `increment_policy.max_files_per_atomic_increment` limit from config

For each increment, define:
- **Title**: concise, imperative
- **Type**: feature, fix, or chore
- **Lane**: atomic (usually, unless it's a cross-cutting refactor)
- **Spec**: which spec file is relevant
- **Priority**: execution order (1 = first)
- **Execution mode**: `interactive` (default) or `autonomous`

## Step 4: Present the queue

Show the user the proposed queue:
```
Queue: [Batch Title]
  1. [Increment title] — [type] — [spec reference]
  2. [Increment title] — [type] — [spec reference]
  3. ...
```

Include for each:
- Scope summary
- Key files affected
- Verification approach
- PR behavior (per workflow_defaults)

**If any increment uses `autonomous` execution mode**, also show:
- Planned agent roles for orchestration, implementation, and review (from `agent_roles` config)
- Stop conditions (from `autonomous_run_policy` config)
- The frozen spec inputs that will be used during the run

## Step 5: Create the batch

Once the user approves the queue, create it:

Build the children JSON array and run:
`esperkit increment group --title "<batch title>" --children '<json array>'`

This creates:
- A parent batch increment in `active/` (systematic lane)
- Child increments in `pending/` (one per queue item)

If any child uses autonomous execution, set the execution_mode:
`esperkit increment set <filename> execution_mode autonomous`

## Step 6: Stay in plan mode

Present the created batch and children.
Tell the user: "Run `esper:go` to begin implementing the first increment in the queue."

Do NOT begin implementation. Batch mode is for planning the queue.

## Available CLI commands

- `esperkit context get` — read current context
- `esperkit increment list` — list all increments
- `esperkit increment group --title "..." --children '<json>'` — create batch
- `esperkit increment activate <file>` — activate first child
- `esperkit increment set <file> <field> <value>` — update increment field
- `esperkit spec index` — show spec tree
- `esperkit spec get <file>` — read a spec
- `esperkit config get agent_roles` — read agent role mappings
- `esperkit config get autonomous_run_policy` — read run policy
