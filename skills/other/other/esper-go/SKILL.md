---
name: esper:go
description: Advance the current work stage. If in spec mode, derives an increment plan. If in increment mode, begins implementation.
---

You are advancing the current work stage. The behavior depends on the active context.

## Step 1: Read context

Run `esperkit context get` to determine the current state.

Check:
- Is there an active increment? (`active_increment` field)
- What is the workflow mode?
- Is there an active run? (`active_run` field)
- What is the execution mode? (`active_execution_mode` field)

## Step 2: Detect work stage and branch

### Branch A: No active increment — derive from specs

If there is no active increment but the user has been working on specs (via `esper:spec`):
1. Read the spec files that were being edited
2. Identify what implementation work is needed based on the specs
3. Ask the user: "What would you like to implement from these specs?"
4. Based on the answer:
   - **Single task**: Create one increment via `esperkit increment create --title "..." --lane atomic --spec <file>`
   - **Multiple tasks**: Suggest using `esper:batch` instead
5. Activate the increment: `esperkit increment activate <filename>`
6. Present the increment plan for review
7. Stop here — do NOT begin implementation until the user confirms or runs `esper:go` again

### Branch B: Active increment in plan stage

If there is an active increment and its `## Progress` section is empty or says "[Updated during implementation]":
1. Read the full increment file from `.esper/increments/active/<filename>`
2. Read the referenced spec files (from `spec:` frontmatter field)
3. Check the `execution_mode` frontmatter field
4. Confirm the plan is approved with the user

**If `execution_mode` is `interactive` (default):**
5. Begin implementation:
   - Follow the `## Scope` section
   - Create/modify files as listed in `## Files Affected`
   - Run verification commands from `## Verification`
   - Update the `## Progress` section as work is completed
   - Proactively update spec files if implementation reveals spec gaps
   - Commit according to `workflow_defaults.commits`

**If `execution_mode` is `autonomous`:**
5. Begin autonomous execution:
   - Freeze the approved spec snapshot (record the spec file and its current state)
   - Create a run: `esperkit run create <increment-filename>`
   - Read the run ID from the output
   - Decompose the increment scope into bounded task packets
   - For each task, create a task packet: `esperkit run add-task <run-id> '<task-json>'`
   - Task JSON must include: `spec`, `spec_section`, `files_allowed`, `verification`, `acceptance_criteria`, `assigned_role`
   - Dispatch tasks to the appropriate worker role as defined in `.esper/esper.json` `agent_roles`
   - After all tasks complete, trigger a review pass
   - Create a review record: `esperkit run add-review <run-id> '<review-json>'`
   - If review passes: update run status and proceed to completion
   - If review fails: convert findings into repair tasks and repeat
   - Stop and escalate to the user if:
     - Max review rounds exceeded (from `autonomous_run_policy.max_review_rounds`)
     - Runtime limit exceeded (from `autonomous_run_policy.max_runtime_minutes`)
     - The reviewer finds spec ambiguity, requirement conflicts, or missing approvals
   - To stop a run: `esperkit run stop <run-id> '<reason>'`

### Branch C: Active increment in progress

If there is an active increment with progress recorded:
1. Read the increment and assess remaining work
2. Continue implementation from where it left off
3. When all scope items are complete and verification passes:
   - Ask the user if they want to finish the increment
   - If yes: run `esperkit increment finish <filename>`
   - Suggest running `esper:sync` to update specs if needed
   - Then check for batch continuation (see Step 4)

### Branch D: Active run in progress

If there is an active run (`active_run` is not null):
1. Run `esperkit run get <run-id>` to read the run state
2. Run `esperkit run list-tasks <run-id>` to check task status
3. If tasks are pending: continue dispatching
4. If all tasks complete: trigger review
5. If review passed: proceed to completion
6. If review failed: create repair tasks and continue the loop
7. If the run is cancelled or escalated: report to the user

## Step 3: Refuse if blocked

Before advancing, check:
- If the increment file has unresolved comments (lines starting with `> TODO:` or `> FIXME:`), refuse to advance
- Tell the user to resolve the comments first
- List the unresolved items

## Step 4: Batch auto-loop

After finishing a child increment, check if it belongs to a batch (has a `parent:` field in its frontmatter).

If yes:
1. Run `esperkit context get` to check if a new `active_increment` was auto-activated
2. If a new child is active, loop back to **Step 2** — read the new increment and continue implementation
3. Repeat until no more children remain (i.e. `active_increment` is null or points to the parent)
4. When the batch is fully complete, finish the parent increment if still active

This loop runs automatically — do NOT ask the user to run `esper:go` again between children. The user already approved the full queue during `esper:batch`.

## Available CLI commands

- `esperkit context get` — read current context
- `esperkit increment create --title "..." [--lane atomic|systematic] [--type feature|fix|chore] [--spec <file>]` — create increment
- `esperkit increment activate <file>` — activate an increment
- `esperkit increment finish <file>` — finish an increment
- `esperkit increment list` — list all increments
- `esperkit spec get <file>` — read a spec file
- `esperkit run create <increment>` — create a new autonomous run
- `esperkit run get <id>` — read run state
- `esperkit run list` — list all runs
- `esperkit run stop <id> [reason]` — stop a run
- `esperkit run add-task <run-id> '<task-json>'` — add a task packet
- `esperkit run get-task <run-id> <task-id>` — read a task
- `esperkit run list-tasks <run-id>` — list tasks in a run
- `esperkit run add-review <run-id> '<review-json>'` — add a review record
- `esperkit run list-reviews <run-id>` — list reviews in a run
