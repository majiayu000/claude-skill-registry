---
name: task-work
description: Work on a kspec task with proper lifecycle - verify, start, note, submit, PR, complete.
---

Base directory for this skill: /home/chapel/Projects/kynetic-spec/.claude/skills/task-work

# Task Work Session

Structured workflow for working on tasks. Full lifecycle from start through PR merge.

## Quick Start

```bash
# Start the workflow
kspec workflow start @task-work-session
kspec workflow next --input task_ref="@task-slug"
```

## When to Use

- Starting work on a ready task
- Ensuring consistent task lifecycle
- When you need to track progress with notes

## Inherit Existing Work First

**Before starting new work, check for existing in-progress or pending_review tasks.**

```bash
kspec session start  # Shows active work at the top
```

Priority order:
1. **pending_review** - PR awaiting merge, highest priority
2. **in_progress** - Work already started, continue it
3. **ready (pending)** - New work to start

**Always inherit existing work** unless user explicitly says otherwise. If there's an in_progress task, pick it up and continue. If there's a pending_review task, check the PR status and push it to completion.

Only start new work when:
- No in_progress or pending_review tasks exist
- User explicitly tells you to work on something else
- User says to ignore the existing work

This prevents orphaned work and ensures tasks get completed.

## Task States

```
pending → in_progress → pending_review → completed
```

- `task start` → in_progress (working on it)
- `task submit` → pending_review (code done, PR created, awaiting merge)
- `task complete` → completed (PR merged)

## Workflow Overview

10 steps for full task lifecycle:

1. **Check Existing Work** - Inherit in_progress or pending_review tasks first
2. **Choose Task** - Select from ready tasks (if no existing work)
3. **Verify Not Done** - Check git history, existing code
4. **Start Task** - Mark in_progress
5. **Work & Note** - Add notes during work
6. **Commit** - Ensure changes committed with trailers
7. **Submit Task** - Mark pending_review
8. **Create PR** - Use /pr skill
9. **PR Merged** - Wait for review and merge
10. **Complete Task** - Mark completed after merge

## Key Commands

```bash
# See available tasks
kspec tasks ready

# Get task details
kspec task get @task-slug

# Start working (in_progress)
kspec task start @task-slug

# Add notes as you work
kspec task note @task-slug "What you're doing..."

# Submit for review (pending_review) - code done, PR ready
kspec task submit @task-slug

# Complete after PR merged (completed)
kspec task complete @task-slug --reason "Summary of what was done"
```

## Verification Step

Before starting, check if work might already be done - but **always validate yourself**:

```bash
# Check git history for related work
git log --oneline --grep="feature-name"
git log --oneline -- path/to/relevant/files

# If code/tests exist, VERIFY they actually work:
npm test -- --grep "relevant-tests"
# Review code against acceptance criteria
# Check coverage is real, not just test.skip()
```

### Notes Are Context, Not Proof

Task notes provide historical context, but **never trust notes as proof of completion**. If a task is in the queue, there's a reason - validate independently:

- **"Already implemented"** → Run the tests yourself. Do they pass? Do they cover the ACs?
- **"Tests exist but skip in CI"** → That's a gap to fix, not a reason to mark complete
- **"Work done in PR #X"** → Verify the PR was merged AND the work is correct

Treat verification like a code review: check the actual code and tests against the acceptance criteria. Don't rubber-stamp based on notes.

### What "Already Implemented" Actually Requires

To mark a task complete as "Already implemented", you must:

1. **Run the tests** and see them pass (not skip)
2. **Verify AC coverage** - each acceptance criterion has a corresponding test
3. **Check the implementation** matches what the spec requires

If tests are skipped, broken, or missing coverage - the task is NOT done. Fix the gaps.

## Scope Expansion During Work

Tasks describe expected outcomes, not rigid boundaries. During work, you may discover:

- **Tests need implementation**: A "testing" task may reveal missing functionality. **Implementing that functionality is in scope** - the goal is verified behavior, not just test files.

- **Implementation needs tests**: An "implementation" task includes proving it works. Add tests.

- **DoD constraints are hard requirements**: If the task notes include Definition of Done criteria, those are not suggestions. Never produce deliverables that violate DoD.

### When to Expand vs Escalate

**Expand scope** (do it yourself) when:
- The additional work is clearly implied by the goal
- It's proportional to the original task (not 10x larger)
- You have the context to do it correctly

**Escalate** (ask user) when:
- Scope expansion is major (testing task becomes architecture redesign)
- You're uncertain about the right approach
- DoD is ambiguous and requires judgment calls

### Anti-patterns to Avoid

- **`test.skip()` as a deliverable**: Never use `test.skip()` to document missing functionality unless explicitly approved by user. Skipped tests give false coverage and fail the goal of verification.

- **Literal task title interpretation**: "Add tests for X" means "ensure X is verified." If X doesn't exist, implement it first.

- **Checkbox completion**: Completing *something* is not the goal. Completing the *right thing* is. If you can't achieve the actual goal, ask for guidance rather than delivering a hollow artifact.

- **Trusting notes without validation**: Notes saying "already done" or "tests exist" are not proof. Run the tests. Check the code. Verify against ACs. If a task is in the ready queue, assume there's unfinished work until you prove otherwise.

- **"Skipped in CI" as acceptable**: Tests that skip in CI are gaps, not completed work. Either fix the CI issue or document why it's acceptable (with user approval).

- **Automation mode shortcuts**: Automation mode means "make good decisions autonomously" - the same decisions a skilled human would make. It does NOT mean take shortcuts, skip hard problems, or produce placeholder deliverables.

## Notes Best Practices

Add notes **during** work, not just at the end:

- When you discover something unexpected
- When you make a design decision
- When you encounter a blocker
- When you complete a significant piece

Good notes help future sessions understand context:

```bash
# Good: explains decision
kspec task note @task "Using retry with exponential backoff. Chose 3 max retries based on API rate limits."

# Bad: no context
kspec task note @task "Done"
```

## Commit Format

Include task trailer in commits:

```
feat: add user authentication

Implemented JWT-based auth with refresh tokens.
Sessions expire after 24h.

Task: @task-add-auth
Spec: @auth-feature

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

This enables `kspec log @task` to find related commits.

## Submit vs Complete

**Submit** (`task submit`):
- Use when code is done and you're creating a PR
- Task moves to `pending_review`
- Indicates "ready for review, not yet merged"

**Complete** (`task complete`):
- Use only after PR is merged to main
- Task moves to `completed`
- Indicates "work is done and shipped"
- Use `--force` to complete from any state (for cleanup or stuck tasks)

**Why this matters:**
- Tracks tasks awaiting merge separately from done tasks
- `kspec tasks ready` won't show pending_review tasks as available
- Gives accurate picture of what's in progress vs awaiting review

## After Completion

After completing a task:

1. Check if other tasks were unblocked: `kspec tasks ready`
2. Consider starting the next task
3. If work revealed new tasks/issues, add to inbox

## Integration with Other Workflows

- **Before submit**: Consider `/local-review` for quality check
- **After submit**: Use `/pr` to create PR
- **For merge**: Use `@pr-review-merge` workflow
- **After merge**: Complete the task

## Loop Mode

You are running in autonomous loop mode. **Every action is logged and audited.** Work quality matters - automation mode means making the same decisions a skilled human would make, not taking shortcuts.

```bash
kspec workflow start @task-work-loop
```

### Accountability

Loop mode is NOT a free pass to:
- Skip hard problems because "they require human interaction"
- Mark tasks as needs_review without actually attempting the work
- Estimate time and bail before writing code
- Assume something won't work without trying it

**You are accountable for real progress.** All notes, commands, and decisions are recorded. A human will review this session. Do the work properly.

### Workflow Steps

1. **Get eligible tasks**
   ```bash
   kspec tasks ready --eligible
   ```

2. **Select task** (priority order):
   - First: any `in_progress` task (continue existing work)
   - Then: tasks that unblock others (high impact)
   - Finally: highest priority ready task (lowest number)

3. **Verify work is needed**
   - Check git history for related commits
   - Read existing implementation if files exist
   - If already done: `kspec task complete @task --reason "Already implemented"` and EXIT

4. **Start and implement**
   ```bash
   kspec task start @task
   # Do the work
   kspec task note @task "What you did..."
   ```

5. **Commit and submit**
   ```bash
   git add <files> && git commit -m "feat/fix: description

   Task: @task-slug"
   kspec task submit @task
   ```

6. **Create PR and stop responding**
   ```
   /pr
   ```
   After PR created, **stop responding** (do NOT call any more commands).
   Ralph automatically:
   1. Sends the reflection prompt to you
   2. Processes pending_review tasks via subagent
   3. Continues to the next iteration with remaining tasks

   **Do NOT call `end-loop`** - creating a PR completes ONE task, not the loop.

### Tasks Requiring Services

Many tasks require running services (daemons, servers, databases). **You can and must handle these.** See AGENTS.md for project-specific commands.

The pattern is always:
1. Start the service
2. Wait for it to be ready
3. Do the work
4. Clean up

**Do NOT mark tasks as needs_review just because they require a running service.** Start it. Run the tests. Fix failures. That's the job.

### When Tests Fail

Test failures are part of the work, not a reason to stop.

1. **Read the full error** - not just the assertion, the whole output
2. **Check logs** - server logs, daemon logs, build output
3. **Isolate** - run just the failing test to iterate faster
4. **Fix and retry** - make changes, run again
5. **Repeat** until tests pass

After 3 genuine attempts with different fixes, add a note documenting what you tried and what you learned. Then continue to the next task.

### Exit Conditions

**Normal exit: Stop responding.** After creating a PR (or blocking a task), simply stop responding. Ralph continues automatically — it checks for remaining eligible tasks at the start of each iteration and exits the loop itself when none remain. You do not need to manage loop termination.

**Important:** "No eligible tasks" means ALL eligible tasks are done or blocked, not just the one you're working on. If one task is blocked, check for others before stopping.

### Turn Completion vs Loop End

**Turn Completion (normal):** Stop responding. Ralph continues automatically.
Your turn ends when you stop sending tool calls. Ralph then:
- Sends the reflection prompt
- Processes pending_review tasks via subagent
- Continues to the next iteration

**Loop End (explicit signal):** `kspec ralph end-loop` - ends ALL remaining iterations.
Only use when `kspec tasks ready --eligible` returns empty AND you've verified
no more work is possible.

**Common Mistake:** Calling `end-loop` after creating a PR.
- Creating a PR = one task's code done
- Other ready tasks may still exist
- Ralph continues automatically to work on them

### Blocking vs Ending the Loop

When you hit a genuine blocker on a task, the correct pattern is:

1. **Attempt the work first** - actually try to solve the problem
2. **Block the specific task** - not the whole loop
3. **MUST run `kspec tasks ready --eligible`** - its output is authoritative
4. **If tasks remain: work on the next one.** If empty: stop responding — ralph exits automatically.

**Trust the YAML state.** If a task's `depends_on` is empty, it has no dependencies. If `kspec tasks ready --eligible` lists a task, it IS eligible and ready to work on. Do not invent blocking relationships based on perceived connections between tasks, PRs in CI, or other inferred state. The command output is the source of truth.

| Situation | Action | Correct Response |
|-----------|--------|------------------|
| Task needs external input | `kspec task block` | Block task, continue to next |
| Task has spec gap | `kspec task block` | Block task, continue to next |
| Task requires architectural decision | `kspec task block` | Block task, mark needs_review, continue |
| Task is complex/difficult | **DO THE WORK** | Complexity is not a blocker |
| Tests are failing | **FIX THEM** | Debug and resolve |
| Service needs to be running | **START IT** | See "Tasks Requiring Services" |
| No more eligible tasks exist | Stop responding | Ralph auto-exits when no tasks remain |

```bash
# Pattern: When you hit a genuine blocker mid-task
kspec task note @task "Attempted X, Y, Z. Blocked because: [external reason]"
kspec task block @task --reason "Requires architectural decision on X"
kspec task set @task --automation needs_review

# MUST check for other work — command output is authoritative
kspec tasks ready --eligible
# If tasks exist: pick one and continue
# If empty: stop responding — ralph exits the loop automatically
```

### Explicit Loop End Signal (Rare Escape Hatch)

Ralph automatically exits the loop when no eligible tasks remain — you do not need to signal this. In almost all cases, simply stop responding and let ralph manage loop termination.

`end-loop` exists only for situations where work is stalling across multiple iterations with no productive progress — something ralph's automatic task checks cannot detect. If you are uncertain whether to end, **default to stopping** rather than calling `end-loop`.

```bash
# Only if work is genuinely stalling across iterations
kspec ralph end-loop --reason "No progress across N iterations: [description]"
```

**Before calling `end-loop`, you MUST:**
1. Run `kspec tasks ready --eligible` and confirm it returns empty
2. Verify the stall is real, not just one difficult task

**Do NOT call `end-loop`:**
- After creating a PR → ralph continues automatically
- When one task is blocked → block it and check for others
- When a task is hard → do the work
- When `kspec tasks ready --eligible` still shows tasks → work on them

### What Is NOT an Exit Condition

These are NOT reasons to exit, block, or mark needs_review:
- "Task seems complex" - do it anyway
- "Might take multiple iterations" - that's fine, iterate
- "Requires daemon" - start the daemon
- "E2E tests need running" - run them
- "Estimated time exceeds iteration" - estimates are not work, do the work

**What to do instead:** Push through. Complexity and difficulty are expected. Block tasks only for genuine external blockers (human decision needed, spec gap, external dependency). If you can theoretically solve it with more effort, it's not blocked - keep working.

### Key Behaviors

- Only `automation: eligible` tasks are considered. Automation eligibility is determined solely by the `automation` field, not by task type, title, or description. If a task is marked `eligible`, work on it — do not re-triage based on whether it looks like a "design task" or any other category.
- Verification still performed (prevent duplicate work)
- Decisions auto-resolve without prompts
- PR review handled externally by ralph (not this workflow)
- **All actions are logged** - work as if being watched
