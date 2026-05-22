---
name: testing-workflows-with-subagents
description: Use when creating or editing commands, orchestrator prompts, or workflow documentation before deployment - applies RED-GREEN-REFACTOR to test instruction clarity by finding real execution failures, creating test scenarios, and verifying fixes with subagents
---

# Testing Workflows With Subagents

## Overview

**Testing workflows is TDD applied to orchestrator instructions and command documentation.**

You find real execution failures (git logs, error reports), create test scenarios that reproduce them, watch subagents follow ambiguous instructions incorrectly (RED), fix the instructions (GREEN), and verify subagents now follow correctly (REFACTOR).

**Core principle:** If you didn't watch an agent misinterpret the instructions in a test, you don't know if your fix prevents the right failures.

**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill applies TDD to workflow documentation.

## When to Use

Use when:
- Creating new commands (`.claude/commands/*.md`, `/spectacular:*`)
- Editing orchestrator prompts for subagents
- Updating workflow documentation in commands
- You observed real execution failures (wrong branches, skipped steps, misinterpreted instructions)
- Instructions involve multiple steps where order matters
- Agents work under time pressure or cognitive load

Don't test:
- Pure reference documentation (no workflow steps)
- Single-step commands with no ambiguity
- Documentation without actionable instructions

## TDD Mapping for Workflow Testing

| TDD Phase | Workflow Testing | What You Do |
|-----------|------------------|-------------|
| **RED** | Find real failure | Check git logs, error reports for evidence of agents misinterpreting instructions |
| **Verify RED** | Create failing test scenario | Reproduce the failure with test repo + pressure scenario |
| **GREEN** | Fix instructions | Rewrite ambiguous steps with explicit ordering, warnings, examples |
| **Verify GREEN** | Test with subagent | Same scenario with fixed instructions - agent follows correctly |
| **REFACTOR** | Iterate on clarity | Find remaining ambiguities, improve wording, re-test |
| **Stay GREEN** | Re-verify | Test again to ensure fix holds |

Same cycle as code TDD, different test format.

## RED Phase: Find Real Execution Failures

**Goal:** Gather evidence of how instructions were misinterpreted in actual execution.

**Where to look:**
- **Git history**: Commits on wrong branches, missing branches, incorrect stack structure
- **Run logs**: Steps skipped, wrong order executed, missing quality checks
- **Error reports**: Failed tasks, cleanup issues, integration problems
- **User reports**: "Agents did X when I expected Y"

**Document evidence:**
```markdown
## RED Phase Evidence

**Source**: bignight.party git log (Run ID: 082687)

**Failure**: Task 4.3 commit on branch `082687-task-4.2-auth-domain-migration`

**Expected**: Create branch `082687-task-4.3-server-actions`

**Actual**: Committed to Task 4.2's branch instead

**Root cause hypothesis**: Instructions ambiguous about creating branch before committing
```

**Critical:** Get actual git commits, branch names, error messages - not hypothetical scenarios.

## Create RED Test Scenario

**Goal:** Reproduce the failure in a controlled test environment.

### Test Repository Setup

Create minimal repo that simulates real execution state:

```bash
cd /path/to/test-area
mkdir workflow-test && cd workflow-test
git init
git config user.name "Test" && git config user.email "test@test.com"

# Set up state that led to failure
# (e.g., existing task branches for sequential phase testing)
```

### Pressure Scenario Document

Create test file with:
1. **Role definition**: "You are subagent implementing Task X"
2. **Current state**: Branch, uncommitted work, what's done
3. **Actual instructions**: Copy current ambiguous instructions
4. **Pressure context**: Combine 2-3 pressure types from table below
5. **Options**: Give explicit choices (forces decision, no deferring)

### Pressure Types for Workflow Testing

| Pressure | Example | Effect on Agent |
|----------|---------|-----------------|
| **Time** | "Orchestrator waiting", "4 more tasks to do", "Need to move fast" | Skips reading skills, chooses fast option |
| **Cognitive load** | "2 hours in, tired", "Third sequential task", "Complex state" | Misreads instructions, makes assumptions |
| **Urgency** | "Choose NOW", "Execute immediately", "No delays" | Skips verification steps, commits to first interpretation |
| **Task volume** | "4 more tasks after this", "Part of 10-task phase" | Rushes through steps, skips optional guidance |
| **Complexity** | "Multiple branches exist", "Shared worktree", "Parallel tasks running" | Confused about current state, wrong branch |

**Best test scenarios combine 2-3 pressures** to simulate realistic execution conditions.

**Example:**
```markdown
# RED Test: Sequential Phase Task Execution

**Role**: Implementation subagent for Task 2.3

**Current state**: On branch `abc123-task-2-2-database`
Uncommitted changes in auth.js (your completed work)

**Instructions from execute.md (CURRENT VERSION)**:
```
5. Use `using-git-spice` skill to:
   - Create branch: abc123-task-2-3-auth
   - Commit with message: "[Task 2.3] Add auth"
```

**Pressure**: 2 hours in, tired, 4 more tasks to do

**Options**:
A) Read skill (2 min delay)
B) Just commit now
C) Create branch with git, then commit
D) Guess git-spice command

Choose and execute NOW.
```

### Run RED Test

```bash
# Dispatch subagent with test scenario
# Use haiku for speed and realistic "under pressure" behavior
# Document exact choice and reasoning verbatim
```

**Expected RED result**: Agent makes wrong choice, commits to wrong branch, or skips creating branch.

If agent succeeds, your test scenario isn't realistic enough - add more pressure or make options more tempting.

## GREEN Phase: Fix Instructions

**Goal:** Rewrite instructions to prevent the specific failure observed in RED.

### Analyze Root Cause

From RED test, identify:
- Which step was ambiguous?
- What order was unclear?
- What assumptions did agent make?
- What did pressure cause them to skip?

**Example analysis:**
```markdown
**Ambiguous**: "Create branch" and "Commit" as separate bullets
**Unclear order**: Could mean "create then commit" OR "commit then create"
**Assumption**: "I'll just commit first, cleaner workflow"
**Pressure effect**: Skipped reading skill, chose fast option
```

### Fix Patterns

**Pattern 1: Explicit Sequential Steps**

<Before>
```markdown
- Create branch: X
- Commit with message: Y
- Stay on branch
```
</Before>

<After>
```markdown
a) FIRST: Stage changes
   - Command: `git add .`

b) THEN: Create branch (commits automatically)
   - Command: `gs branch create X -m "Y"`

c) Stay on new branch
```
</After>

**Pattern 2: Critical Warnings**

Add consequences upfront:
```markdown
CRITICAL: Stage changes FIRST, then create branch.

If you commit BEFORE creating branch, work goes to wrong branch.
```

**Pattern 3: Show Commands**

Reduce friction under pressure - show exact commands:
```markdown
b) THEN: Create new stacked branch
   - Command: `gs branch create {name} -m "message"`
   - This creates branch and commits in one operation
```

**Pattern 4: Skill-Based Reference**

Balance showing commands with learning:
```markdown
Use `using-git-spice` skill which teaches this two-step workflow:
[commands here]
Read the skill if uncertain about the workflow.
```

### Apply Fix

Edit the actual command file with GREEN fix.

## Verify GREEN: Test Fix

**Goal:** Confirm agents now follow instructions correctly under same pressure.

### Reset Test Repository

```bash
cd /path/to/workflow-test
git reset --hard initial-state
# Recreate same starting conditions as RED test
```

### Create GREEN Test Scenario

Same as RED test but:
- Update to "Instructions from execute.md (NEW IMPROVED VERSION)"
- Include the fixed instructions
- Same pressure, same options available
- Same "execute NOW" urgency

### Run GREEN Test

```bash
# Dispatch subagent with GREEN scenario
# Use same model (haiku) for consistency
# Agent should now choose correct option and execute correctly
```

**Expected GREEN result**:
- Agent follows fixed instructions
- Creates branch before committing (or whatever correct behavior is)
- Quotes reasoning showing they understood the explicit ordering
- Work ends up in correct state

**If agent still fails**: Instructions still ambiguous. Return to GREEN phase, improve clarity, re-test.

## Meta-Testing (When GREEN Fails)

**If agent still misinterprets after your fix, ask them directly:**

```markdown
your human partner: You read the improved instructions and still chose the wrong option.

How could those instructions have been written differently to make
the correct workflow crystal clear?
```

**Three possible responses:**

1. **"The instructions WERE clear, I just rushed"**
   - Not a clarity problem - need stronger warning/consequence
   - Add "CRITICAL:" or "MUST" language upfront
   - State failure consequence explicitly

2. **"The instructions should have said X"**
   - Clarity problem - agent's suggestion usually good
   - Add their exact wording verbatim
   - Re-test to verify improvement

3. **"I didn't notice section Y"**
   - Organization problem - important info buried
   - Move critical steps earlier
   - Use formatting (bold, CRITICAL) to highlight

**Use meta-testing to diagnose WHY fix didn't work, not just add more content.**

## REFACTOR Phase: Iterate on Clarity

**Goal:** Find and fix remaining ambiguities.

### Check for Remaining Issues

Run additional test scenarios:
- Different pressure combinations
- Different task positions (first task, middle, last)
- Different states (clean vs dirty working tree)
- Different agent models (haiku, sonnet)

### Common Clarity Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Order ambiguous** | Steps done out of order | Add "a) FIRST, b) THEN" labels |
| **Missing consequences** | Agent skips step | Add "If you skip X, Y will fail" |
| **Too abstract** | Agent guesses commands | Show exact commands inline |
| **No warnings** | Agent makes wrong choice | Add "CRITICAL:" upfront |
| **Assumes knowledge** | Agent doesn't know tool | Reference skill + show command |

### Document Test Results

Create summary document:
```markdown
# Test Results: execute.md Sequential Phase Fix

**RED Phase**: Task 4.3 committed to Task 4.2 branch (real failure)
**GREEN Phase**: Agent created correct branch, no ambiguity
**REFACTOR**: Tested with different models, all passed

**Fix applied**: Lines 277-297 (sequential), 418-438 (parallel)
**Success criteria**: New stacked branch created BEFORE commit
```

## Differences from Testing Skills

**testing-skills-with-subagents** (discipline skills):
- Tests agent **compliance under pressure** (will they follow rules?)
- Focuses on **closing rationalization loopholes**
- Uses **multiple combined pressures** (time + sunk cost + exhaustion)
- Goal: **Bulletproof against shortcuts**

**testing-workflows-with-subagents** (workflow documentation):
- Tests **instruction clarity** (can they understand what to do?)
- Focuses on **removing ambiguity in ordering and steps**
- Uses **realistic execution pressure** (tired, more tasks, time limits)
- Goal: **Unambiguous instructions agents can follow correctly**

Different problem: Skills test "will you comply?" vs Workflows test "can you understand?"

## Quick Reference: RED-GREEN-REFACTOR Cycle

**RED Phase**:
1. Find real execution failure (git log, error reports)
2. Create test repo simulating pre-failure state
3. Write pressure scenario with current instructions
4. Launch subagent, document exact failure

**GREEN Phase**:
1. Analyze root cause (what was ambiguous?)
2. Fix instructions (explicit order, warnings, commands)
3. Reset test repo to same state
4. Write GREEN scenario with fixed instructions
5. Launch subagent, verify correct execution

**REFACTOR Phase**:
1. Test additional scenarios (different pressures, states)
2. Find remaining ambiguities
3. Improve clarity
4. Re-verify all tests pass

## Testing Checklist (TDD for Workflows)

**IMPORTANT: Use TodoWrite to track these steps.**

**RED Phase:**
- [ ] Find real execution failure (git commits, logs, errors)
- [ ] Document evidence (branch names, commit hashes, expected vs actual)
- [ ] Create test repository simulating pre-failure state
- [ ] Write pressure scenario with current instructions
- [ ] Run subagent test, document exact failure and reasoning

**GREEN Phase:**
- [ ] Analyze root cause of ambiguity
- [ ] Fix instructions (explicit ordering, warnings, commands)
- [ ] Apply fix to actual command file
- [ ] Reset test repository to same starting state
- [ ] Write GREEN scenario with fixed instructions
- [ ] Run subagent test, verify correct execution

**REFACTOR Phase:**
- [ ] Test with different pressure levels
- [ ] Test with different execution states
- [ ] Test with different agent models
- [ ] Document all remaining ambiguities found
- [ ] Improve clarity for each issue
- [ ] Re-verify all scenarios pass

**Documentation:**
- [ ] Create test results summary
- [ ] Document before/after instructions
- [ ] Save test scenarios for regression testing
- [ ] Note which lines in command file were changed

## Common Mistakes

**❌ Testing without real failure evidence**
Start with hypothetical "this might be confusing" leads to fixes that don't address actual problems.
✅ **Fix:** Always start with git logs, error reports, real execution traces.

**❌ Test scenario without pressure**
Agents follow instructions carefully when not rushed - doesn't match real execution.
✅ **Fix:** Add time pressure, cognitive load (tired, many tasks), urgency.

**❌ Improving instructions without testing**
Guessing what's clear vs actually verifying leads to still-ambiguous docs.
✅ **Fix:** Always run GREEN verification with subagent before considering done.

**❌ Testing once and done**
First test might not catch all ambiguities.
✅ **Fix:** REFACTOR phase with varied scenarios, different models.

**❌ Vague test options**
Giving "what do you do?" instead of concrete choices lets agent defer.
✅ **Fix:** Force A/B/C/D choice with "Choose NOW" urgency.

## Real-World Impact

**From testing execute.md sequential phase instructions** (this session):

**RED Phase**:
- Found Task 4.3 committed to Task 4.2's branch in bignight.party
- Created test scenario reproducing failure mode

**GREEN Phase**:
- Fixed instructions with "a) FIRST, b) THEN" explicit ordering
- Added CRITICAL warning about staging before branch creation
- Showed exact atomic command: `gs branch create -m`

**Result**:
- Agent followed corrected workflow perfectly
- Quote: "The two-step process is clear and effective"
- Prevents same failure class across all future executions

**Time investment**: 1 hour testing, prevents repeated failures across all spectacular runs.

## The Bottom Line

**Test workflow documentation the same way you test code.**

RED (find real failure) → GREEN (fix and verify) → REFACTOR (iterate on clarity).

If you wouldn't deploy code without tests, don't deploy commands without verifying agents can follow them correctly.
