---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session using subagents
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

- Have an implementation plan (spool change with tasks.md)
- Tasks are mostly independent
- Want to stay in this session (vs. parallel session with `spool-apply-change-proposal`)

**vs. spool-apply-change-proposal:**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task
- Faster iteration (no human-in-loop between tasks)

## The Process

1. **Setup**: Read plan, extract all tasks, set up tracking
2. **Per Task**:
   - Dispatch implementer subagent
   - Answer any questions
   - Implementer implements, tests, commits, self-reviews
   - Dispatch spec reviewer subagent
   - If issues: implementer fixes, re-review
   - Dispatch code quality reviewer subagent
   - If issues: implementer fixes, re-review
   - Mark task complete: `spool tasks complete <change-id> <task-id>`
3. **Completion**: Dispatch final code reviewer, then use `spool-finishing-a-development-branch`

## Setup

```bash
# Get the change context
spool agent instruction apply --change <change-id>

# Read tasks.md
cat .spool/changes/<change-id>/tasks.md

# Extract all tasks with full text and context upfront
```

## Per Task Workflow

### 1. Mark Task Started

```bash
spool tasks start <change-id> <task-id>
```

### 2. Dispatch Implementer Subagent

Provide:
- Full task text (not just reference)
- Context: what came before, what comes after
- Relevant file paths
- Expected outcome

Subagent implements using TDD:
1. Write failing test
2. Run to confirm failure
3. Implement
4. Run to confirm pass
5. Commit

### 3. Spec Compliance Review

Dispatch spec reviewer subagent with:
- The task specification
- Git diff of changes

Reviewer checks:
- All spec requirements met?
- No extra functionality added?
- Correct files modified?

If issues: implementer subagent fixes, re-review until ✅

### 4. Code Quality Review

Dispatch code quality reviewer subagent with:
- Git SHAs for review
- Code review template

Reviewer checks:
- Code quality
- Test coverage
- Style/conventions

If issues: implementer subagent fixes, re-review until ✅

### 5. Mark Task Complete

```bash
spool tasks complete <change-id> <task-id>
```

### 6. Next Task or Finish

If more tasks: repeat from step 1
If done: dispatch final reviewer, then use `spool-finishing-a-development-branch`

## Prompt Templates

- `./implementer-prompt.md` - Dispatch implementer subagent
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer subagent
- `./code-quality-reviewer-prompt.md` - Dispatch code quality reviewer subagent

## Red Flags

**Never:**
- Start implementation on main/master without explicit user consent
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context
- Accept "close enough" on spec compliance
- Start code quality review before spec compliance is ✅
- Move to next task while either review has open issues

**If subagent asks questions:**
- Answer clearly and completely
- Provide additional context if needed

**If reviewer finds issues:**
- Implementer fixes them
- Reviewer reviews again
- Repeat until approved

## Integration

**Required workflow skills:**
- `spool-using-git-worktrees` - Set up isolated workspace before starting
- `spool-write-change-proposal` - Creates the plan this skill executes
- `spool-requesting-code-review` - Code review template for reviewer subagents
- `spool-finishing-a-development-branch` - Complete development after all tasks

**Subagents should use:**
- `spool-test-driven-development` - Subagents follow TDD for each task

**Alternative workflow:**
- `spool-apply-change-proposal` - Use for human-in-loop execution with batch checkpoints
