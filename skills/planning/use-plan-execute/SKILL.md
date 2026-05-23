---
name: use-plan-execute
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for review.

**Announce at start:** "I'm using the use-plan-execute skill to implement this plan."

# The Process

## 1. Load and Review Plan

1. Read plan file
2. Review critically - identify any questions or concerns
3. If concerns: Raise them before starting
4. If no concerns: Create TodoWrite and proceed

## 2. Execute Batch

**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

## 3. Report

When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

## 4. Continue

Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

## 5. Complete Development

After all tasks complete and verified:
- Announce: "I'm using the use-branch-complete skill to complete this work."
- Use autonome:use-branch-complete
- Follow that skill to verify tests, present options, execute choice

# When to Stop

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, unclear instruction)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

# When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

# Key Rules

- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
