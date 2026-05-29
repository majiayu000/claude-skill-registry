---
name: implementation-process
description: Implement a feature using the written implementation plan. Use when you have a fully-formed written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

## The Process

### Step 1: Load and Review Plan

1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Get the task from taskmaster
<!-- TODO: what's the purpose of this? 4. If no concerns: Create TodoWrite and proceed -->

### Step 2: Execute Sub-Task

1. Update status to in-progress
2. Follow the plan exactly
3. Run verifications as specified; use `testing-process` skill

### Step 3: Report

- Show what was implemented
- Show verification output
- Prompt user for code-review; if user responds 'yes' - run `zen` mcp code-review with gemini-3-pro
- Based on user and code-review feedback: apply changes if needed and finalize the sub-task
- When completed mark as done

### Step 4: Continue

- Execute next sub-task
- Repeat until all sub-tasks are completed

### Step 5: Complete Development

After all sub-tasks complete and verified:

- Use `testing-process` skill to verify and validate functionality
- Use `documentation-process` skill to create or update any relevant docs

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
