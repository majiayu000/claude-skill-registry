---
name: implementation-process
description: Implement a feature using the written implementation plan. Use when you have a fully-formed written implementation plan to execute in a separate session with review checkpoints. TRIGGER when: the user asks to work on, implement, or continue a task from a docs/wip feature (e.g., "work on task 1", "let's do the next task", "implement the first task for X feature", "continue with the auth system tasks").
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

## The Process

### Step 1: Load and Review Plan

1. Read the feature's `tasks.md` file to get the task list and current progress
2. Read the linked `design.md` and `implementation.md` for full context
3. Identify the next pending task (one whose dependencies are all done)
4. Review critically — identify any questions or concerns about the plan
5. If concerns: Raise them with your human partner before starting

### Step 2: Execute Sub-Task

1. Update `tasks.md`: set the task's status to `in-progress`
2. Follow the plan exactly
3. Check off subtasks (`- [x]`) in `tasks.md` as you complete them
4. Run verifications as specified; use `testing-process` skill

### Step 3: Report

- Show what was implemented
- Show verification output
- Prompt user for code-review; if user responds 'yes' - run `zen` mcp code-review with gemini-3-pro
- Based on user and code-review feedback: apply changes if needed and finalize the sub-task
- When completed, update `tasks.md`: set the task's status to `done`

### Step 4: Continue

- Move to the next pending task in `tasks.md`
- Repeat until all tasks are completed

### Step 5: Complete Development

After all tasks complete and verified:

- Use `testing-process` skill to verify and validate functionality
- Use `documentation-process` skill to create or update any relevant docs
- Update the feature status in `tasks.md` header to `done`

## When to Stop and Ask for Help

**STOP executing immediately when:**

- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**IMPORTANT! Always ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**

- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**IMPORTANT! Don't force through blockers** - stop and ask.

## Remember

- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Use skills when the plan says to do so
- Between batches: just report and wait
- Stop when blocked, don't guess
