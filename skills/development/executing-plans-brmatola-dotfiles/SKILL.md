---
name: executing-plans
description: Use when you have a written implementation plan to execute - runs autonomously by default, or in batched mode with checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks until complete or blocked.

**Core principle:** Autonomous execution with stops only for blockers.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Plan location:** `plans/active/{plan-name}/implementation/`

## Execution Modes

| Mode | Invocation | Behavior |
|------|------------|----------|
| **Autonomous** | `/executing-plans` (default) | Run full plan, stop only for blockers |
| **Batched** | `/executing-plans --batched` | Execute 3 tasks → checkpoint → repeat |

**Invocation syntax:**
- Default: `/executing-plans {plan-name}` - runs autonomous
- Batched: `/executing-plans {plan-name} --batched` - runs with checkpoints
- The `--batched` flag can appear anywhere in args

**When to use batched mode:**
- Large plans where you want incremental review
- Plans with uncertain requirements
- When explicitly requested by user

**Autonomous is default** because:
- Reduces back-and-forth for well-defined plans
- Faster end-to-end execution
- Blockers still trigger stops

**Note:** This is a default behavior change. Previous behavior was batched. Users expecting checkpoints should add `--batched`.

## The Process

### Step 1: Load and Review Plan

1. Read plan files from `plans/active/{plan-name}/implementation/`
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

**Autonomous Mode (default):**

For each task in sequence:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed
5. **Continue to next task** (don't stop)

Stop ONLY when:
- All tasks complete
- Hit a blocker (test failure, missing dependency, unclear instruction)
- Verification fails repeatedly

**Batched Mode (`--batched`):**

Execute in batches of 3 tasks:
1. Complete 3 tasks following steps above
2. Stop and report progress
3. Wait for feedback
4. Continue with next batch

### Step 3: Handle Blockers

When hitting a blocker in either mode:
1. Stop immediately
2. Report what blocked you
3. Report what was completed so far
4. Wait for guidance

**Don't guess past blockers** - ask for help.

### Step 4: Report Completion

**Autonomous mode completion report:**

```
## Execution Complete: {plan-name}

### Tasks Completed: {X}/{Y}

### Summary
| Task | Status | Commit |
|------|--------|--------|
| Task 1 description | ✓ Done | abc123 |
| Task 2 description | ✓ Done | def456 |

### Test Results
- Final suite: {X}/{Y} passing

### Blockers Encountered
- [None / List any and how resolved]

### Ready for: implementation-review
```

**Batched mode report:** Same as above but for current batch, with "Ready for feedback."

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use gremlins:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember

- Review plan critically first
- **Autonomous is default** - run to completion unless blocked
- **Batched mode** - stop every 3 tasks for checkpoint
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
