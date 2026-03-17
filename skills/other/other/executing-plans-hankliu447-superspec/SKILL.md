---
name: executing-plans
description: |
  Use when you have a written implementation plan to execute in a separate session with review checkpoints.
  Alternative to subagent-driven development for batch execution.
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for user review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## When to Use

```
Have implementation plan?
    ↓ yes
Want batch execution with checkpoints?
    ↓ yes
Separate session (not subagent-driven)?
    ↓ yes
→ Use executing-plans
```

**vs. Subagent-Driven Development:**
- Batch execution (multiple tasks at once)
- User review between batches
- Better for sequential tasks with dependencies
- User stays in loop at checkpoints

## The Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Executing Plans Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   Step 1: Load and Review Plan                                   │
│   └─→ Read plan, identify questions, raise concerns              │
│                                                                   │
│   Step 2: Execute Batch (default: 3 tasks)                       │
│   └─→ Follow TDD for each task                                   │
│   └─→ Mark as in_progress → completed                            │
│                                                                   │
│   Step 3: Report                                                  │
│   └─→ Show what was implemented                                  │
│   └─→ Show verification output                                   │
│   └─→ "Ready for feedback"                                       │
│                                                                   │
│   Step 4: Continue                                                │
│   └─→ Apply feedback if needed                                   │
│   └─→ Execute next batch                                         │
│                                                                   │
│   Step 5: Complete Development                                    │
│   └─→ Use superspec:finish-branch                                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Step 1: Load and Review Plan

```markdown
1. Read plan file: superspec/changes/[id]/plan.md
2. Review critically - identify any questions or concerns
3. If concerns: Raise them with user before starting
4. If no concerns: Create TodoWrite and proceed
```

**Questions to ask yourself:**
- Do I understand all tasks?
- Are there any ambiguous requirements?
- Do I have all the context I need?
- Are there any risks or concerns?

## Step 2: Execute Batch

**Default: First 3 tasks**

For each task:

1. **Mark as in_progress** in TodoWrite
2. **Follow TDD strictly:**
   - Write failing test
   - Run test, verify fails
   - Implement minimal code
   - Run test, verify passes
   - Commit with Spec reference
3. **Mark as completed**
4. **Update tasks.md** with completion

**TDD is mandatory for each task.** No exceptions.

## Step 3: Report

When batch complete, report:

```markdown
## Batch 1 Complete (Tasks 1-3)

### Task 1: [Name]
- Implemented: [what]
- Tests: [X/Y pass]
- Commit: [sha]

### Task 2: [Name]
- Implemented: [what]
- Tests: [X/Y pass]
- Commit: [sha]

### Task 3: [Name]
- Implemented: [what]
- Tests: [X/Y pass]
- Commit: [sha]

### Verification
```
$ npm test
All tests pass (X/Y)
```

Ready for feedback.
```

**Wait for user feedback before continuing.**

## Step 4: Continue

Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

## Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finish-branch skill to complete this work."
- **REQUIRED:** Use `superspec:finish-branch`
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly
- TDD cycle isn't working (test won't fail/pass as expected)

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- User updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Batch Size Guidelines

| Situation | Batch Size |
|-----------|------------|
| Normal tasks | 3 tasks |
| Complex tasks | 1-2 tasks |
| Simple tasks | 4-5 tasks |
| User requests | As specified |

**Adjust based on:**
- Task complexity
- User preference
- How closely user wants to monitor

## SuperSpec Integration

### TDD for Each Task

Every task in the batch must follow TDD:

```
For each task:
  1. Write test based on Scenario
  2. Run test → MUST FAIL
  3. Implement minimal code
  4. Run test → MUST PASS
  5. Commit with Spec reference
```

### Update Documents

After each batch:
- Update `tasks.md` with completed tasks
- Update status counts (top section)
- **Update Completion Tracking table (bottom section)**
- Mark phases complete when done

**Completion Tracking table example:**
```markdown
## Completion Tracking

| Phase | Tasks | Completed | Status |
|-------|-------|-----------|--------|
| Phase 1 | 3 | 2 | IN_PROGRESS |
| Phase 2 | 6 | 0 | PENDING |
| **Total** | **9** | **2** | **22%** |
```

### Spec References in Commits

```bash
git commit -m "feat([capability]): [description]

Refs: superspec/changes/[id]/specs/[cap]/spec.md
Requirement: [Name]
Scenario: [Name]"
```

## Red Flags

**Never:**
- Skip TDD for "simple" tasks
- Continue without user feedback at checkpoints
- Ignore blockers and push through
- Skip verification before reporting
- Guess when unsure
- **Skip Completion Tracking table updates**

**Always:**
- Review plan critically first
- Follow TDD for every task
- Report at batch completion
- **Update Completion Tracking table after each batch**
- Wait for feedback
- Stop when blocked

## Quick Reference

| Step | Action | Output |
|------|--------|--------|
| 1. Load | Read plan, raise concerns | Questions or proceed |
| 2. Execute | TDD for each task in batch | Implemented code |
| 3. Report | Show results, verification | Batch summary |
| 4. Continue | Apply feedback, next batch | Continue or adjust |
| 5. Complete | Use finish-branch skill | Merge/PR/Keep |

## Integration

**Called by:**
- Plan header directive
- User choosing "Parallel Session" execution

**Pairs with:**
- `superspec:plan` - Creates the plan this executes
- `superspec:finish-branch` - Completes development
- `tdd` - Implementation method for each task
- `verification-before-completion` - Before claiming batch complete

## Remember

- Review plan critically first
- Follow plan steps exactly
- Follow TDD for EVERY task
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
