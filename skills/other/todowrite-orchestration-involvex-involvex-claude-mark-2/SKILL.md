---
name: todowrite-orchestration
description: Track progress in multi-phase workflows with TodoWrite. Use when orchestrating 5+ phase commands, managing iteration loops, tracking parallel tasks, or providing real-time progress visibility. Trigger keywords - "phase tracking", "progress", "workflow", "multi-step", "multi-phase", "todo", "tracking", "status".
version: 0.1.0
tags: [orchestration, todowrite, progress, tracking, workflow, multi-phase]
keywords: [phase-tracking, progress, workflow, multi-step, multi-phase, todo, tracking, status, visibility]
---

# TodoWrite Orchestration

**Version:** 1.0.0
**Purpose:** Patterns for using TodoWrite in complex multi-phase workflows
**Status:** Production Ready

## Overview

TodoWrite orchestration is the practice of using the TodoWrite tool to provide **real-time progress visibility** in complex multi-phase workflows. It transforms opaque "black box" workflows into transparent, trackable processes where users can see:

- What phase is currently executing
- How many phases remain
- Which tasks are pending, in-progress, or completed
- Overall progress percentage
- Iteration counts in loops

This skill provides battle-tested patterns for:
- **Phase initialization** (create complete task list before starting)
- **Task granularity** (how to break phases into trackable tasks)
- **Status transitions** (pending → in_progress → completed)
- **Real-time updates** (mark complete immediately, not batched)
- **Iteration tracking** (progress through loops)
- **Parallel task tracking** (multiple agents executing simultaneously)

TodoWrite orchestration is especially valuable for workflows with >5 phases or >10 minutes duration, where users need progress feedback.

## Core Patterns

### Pattern 1: Phase Initialization

**Create TodoWrite List BEFORE Starting:**

Initialize TodoWrite as **step 0** of your workflow, before any actual work begins:

```
✅ CORRECT - Initialize First:

Step 0: Initialize TodoWrite
  TodoWrite: Create task list
    - PHASE 1: Gather user inputs
    - PHASE 1: Validate inputs
    - PHASE 2: Select AI models
    - PHASE 2: Estimate costs
    - PHASE 2: Get user approval
    - PHASE 3: Launch parallel reviews
    - PHASE 3: Wait for all reviews
    - PHASE 4: Consolidate reviews
    - PHASE 5: Present results

Step 1: Start actual work (PHASE 1)
  Mark "PHASE 1: Gather user inputs" as in_progress
  ... do work ...
  Mark "PHASE 1: Gather user inputs" as completed
  Mark "PHASE 1: Validate inputs" as in_progress
  ... do work ...

❌ WRONG - Create During Workflow:

Step 1: Do some work
  ... work happens ...
  TodoWrite: Create task "Did some work" (completed)

Step 2: Do more work
  ... work happens ...
  TodoWrite: Create task "Did more work" (completed)

Problem: User has no visibility into upcoming phases
```

**List All Phases Upfront:**

When initializing, include **all phases** in the task list, not just the current phase:

```
✅ CORRECT - Complete Visibility:

TodoWrite Initial State:
  [ ] PHASE 1: Gather user inputs
  [ ] PHASE 1: Validate inputs
  [ ] PHASE 2: Architecture planning
  [ ] PHASE 3: Implementation
  [ ] PHASE 3: Run quality checks
  [ ] PHASE 4: Code review
  [ ] PHASE 5: User acceptance
  [ ] PHASE 6: Generate report

User sees: "8 tasks total, 0 complete, Phase 1 starting"

❌ WRONG - Incremental Discovery:

TodoWrite Initial State:
  [ ] PHASE 1: Gather user inputs
  [ ] PHASE 1: Validate inputs

(User thinks workflow is 2 tasks, then surprised by 6 more phases)
```

**Why Initialize First:**

1. **User expectation setting:** User knows workflow scope (8 phases, ~20 minutes)
2. **Progress visibility:** User can see % complete (3/8 = 37.5%)
3. **Time estimation:** User can estimate remaining time based on progress
4. **Transparency:** No hidden phases or surprises

---

### Pattern 2: Task Granularity Guidelines

**One Task Per Significant Operation:**

Each task should represent a **significant operation** (1-5 minutes of work):

```
✅ CORRECT - Significant Operations:

Tasks:
  - PHASE 1: Ask user for inputs (30s)
  - PHASE 2: Generate architecture plan (2 min)
  - PHASE 3: Implement feature (5 min)
  - PHASE 4: Run tests (1 min)
  - PHASE 5: Code review (3 min)

Each task = meaningful unit of work

❌ WRONG - Too Granular:

Tasks:
  - PHASE 1: Ask user question 1
  - PHASE 1: Ask user question 2
  - PHASE 1: Ask user question 3
  - PHASE 2: Read file A
  - PHASE 2: Read file B
  - PHASE 2: Write file C
  - ... (50 micro-tasks)

Problem: Too many updates, clutters user interface
```

**Multi-Step Phases: Break Into 2-3 Sub-Tasks:**

For complex phases (>5 minutes), break into 2-3 sub-tasks:

```
✅ CORRECT - Sub-Task Breakdown:

PHASE 3: Implementation (15 min total)
  → Sub-tasks:
    - PHASE 3: Implement core logic (5 min)
    - PHASE 3: Add error handling (3 min)
    - PHASE 3: Write tests (7 min)

User sees progress within phase: "PHASE 3: 2/3 complete"

❌ WRONG - Single Monolithic Task:

PHASE 3: Implementation (15 min)
  → No sub-tasks

Problem: User sees "in_progress" for 15 min with no updates
```

**Avoid Too Many Tasks:**

Limit to **max 15-20 tasks** for readability:

```
✅ CORRECT - 12 Tasks (readable):

10-phase workflow:
  - PHASE 1: Ask user
  - PHASE 2: Plan (2 sub-tasks)
  - PHASE 3: Implement (3 sub-tasks)
  - PHASE 4: Test
  - PHASE 5: Review (2 sub-tasks)
  - PHASE 6: Fix issues
  - PHASE 7: Re-review
  - PHASE 8: Accept

Total: 12 tasks (clean, trackable)

❌ WRONG - 50 Tasks (overwhelming):

Every single action as separate task:
  - Read file 1
  - Read file 2
  - Write file 3
  - Run command 1
  - ... (50 tasks)

Problem: User overwhelmed, can't see forest for trees
```

**Guideline by Workflow Duration:**

```
Workflow Duration → Task Count:

< 5 minutes:    3-5 tasks
5-15 minutes:   8-12 tasks
15-30 minutes:  12-18 tasks
> 30 minutes:   15-20 tasks (if more, group into phases)

Example:
  5-minute workflow (3 phases):
    - PHASE 1: Prepare
    - PHASE 2: Execute
    - PHASE 3: Present
  Total: 3 tasks ✓

  20-minute workflow (6 phases):
    - PHASE 1: Ask user
    - PHASE 2: Plan (2 sub-tasks)
    - PHASE 3: Implement (3 sub-tasks)
    - PHASE 4: Test
    - PHASE 5: Review (2 sub-tasks)
    - PHASE 6: Accept
  Total: 11 tasks ✓
```

---

### Pattern 3: Status Transitions

**Exactly ONE Task In Progress at a Time:**

Maintain the invariant: **exactly one task in_progress** at any moment:

```
✅ CORRECT - One In-Progress:

State at time T1:
  [✓] PHASE 1: Ask user (completed)
  [✓] PHASE 2: Plan (completed)
  [→] PHASE 3: Implement (in_progress)  ← Only one
  [ ] PHASE 4: Test (pending)
  [ ] PHASE 5: Review (pending)

State at time T2 (after PHASE 3 completes):
  [✓] PHASE 1: Ask user (completed)
  [✓] PHASE 2: Plan (completed)
  [✓] PHASE 3: Implement (completed)
  [→] PHASE 4: Test (in_progress)  ← Only one
  [ ] PHASE 5: Review (pending)

❌ WRONG - Multiple In-Progress:

State:
  [✓] PHASE 1: Ask user (completed)
  [→] PHASE 2: Plan (in_progress)  ← Two in-progress?
  [→] PHASE 3: Implement (in_progress)  ← Confusing!
  [ ] PHASE 4: Test (pending)

Problem: User confused about current phase
```

**Status Transition Sequence:**

```
Lifecycle of a Task:

1. Created: pending
   (Task exists, not started yet)

2. Started: pending → in_progress
   (Mark as in_progress when starting work)

3. Completed: in_progress → completed
   (Mark as completed immediately after finishing)

4. Next task: Mark next task as in_progress
   (Continue to next task)

Example Timeline:

T=0s:  [→] Task 1 (in_progress), [ ] Task 2 (pending)
T=30s: [✓] Task 1 (completed),   [→] Task 2 (in_progress)
T=60s: [✓] Task 1 (completed),   [✓] Task 2 (completed)
```

**NEVER Batch Completions:**

Mark tasks completed **immediately** after finishing, not at end of phase:

```
✅ CORRECT - Immediate Updates:

Mark "PHASE 1: Ask user" as in_progress
... do work (30s) ...
Mark "PHASE 1: Ask user" as completed  ← Immediate

Mark "PHASE 1: Validate inputs" as in_progress
... do work (20s) ...
Mark "PHASE 1: Validate inputs" as completed  ← Immediate

User sees real-time progress

❌ WRONG - Batched Updates:

Mark "PHASE 1: Ask user" as in_progress
... do work (30s) ...

Mark "PHASE 1: Validate inputs" as in_progress
... do work (20s) ...

(At end of PHASE 1, batch update both to completed)

Problem: User doesn't see progress for 50s, thinks workflow is stuck
```

---

### Pattern 4: Real-Time Progress Tracking

**Update TodoWrite As Work Progresses:**

TodoWrite should reflect **current state**, not past state:

```
✅ CORRECT - Real-Time Updates:

T=0s:  Initialize TodoWrite (8 tasks, all pending)
T=5s:  Mark "PHASE 1" as in_progress
T=35s: Mark "PHASE 1" as completed, "PHASE 2" as in_progress
T=90s: Mark "PHASE 2" as completed, "PHASE 3" as in_progress
...

User always sees accurate current state

❌ WRONG - Delayed Updates:

T=0s:   Initialize TodoWrite
T=300s: Workflow completes
T=301s: Update all tasks to completed

Problem: No progress visibility for 5 minutes
```

**Add New Tasks If Discovered During Execution:**

If you discover additional work during execution, add new tasks:

```
Scenario: During implementation, realize refactoring needed

Initial TodoWrite:
  [✓] PHASE 1: Plan
  [→] PHASE 2: Implement
  [ ] PHASE 3: Test
  [ ] PHASE 4: Review

During PHASE 2, discover:
  "Implementation requires refactoring legacy code"

Updated TodoWrite:
  [✓] PHASE 1: Plan
  [✓] PHASE 2: Implement core logic (completed)
  [→] PHASE 2: Refactor legacy code (in_progress)  ← New task added
  [ ] PHASE 3: Test
  [ ] PHASE 4: Review

User sees: "Additional work discovered: refactoring. Total now 5 tasks."
```

**User Can See Current Progress at Any Time:**

With real-time updates, user can check progress:

```
User checks at T=120s:

TodoWrite State:
  [✓] PHASE 1: Ask user
  [✓] PHASE 2: Plan architecture
  [→] PHASE 3: Implement core logic (in_progress)
  [ ] PHASE 3: Add error handling
  [ ] PHASE 3: Write tests
  [ ] PHASE 4: Code review
  [ ] PHASE 5: Accept

User sees: "3/8 tasks complete (37.5%), currently implementing core logic"
```

---

### Pattern 5: Iteration Loop Tracking

**Create Task Per Iteration:**

For iteration loops, create a task for each iteration:

```
✅ CORRECT - Iteration Tasks:

Design Validation Loop (max 10 iterations):

Initial TodoWrite:
  [ ] Iteration 1/10: Designer validation
  [ ] Iteration 2/10: Designer validation
  [ ] Iteration 3/10: Designer validation
  ... (create all 10 upfront)

Progress:
  [✓] Iteration 1/10: Designer validation (NEEDS IMPROVEMENT)
  [✓] Iteration 2/10: Designer validation (NEEDS IMPROVEMENT)
  [→] Iteration 3/10: Designer validation (in_progress)
  [ ] Iteration 4/10: Designer validation
  ...

User sees: "Iteration 3/10 in progress, 2 complete"

❌ WRONG - Single Loop Task:

TodoWrite:
  [→] Design validation loop (in_progress)

Problem: User sees "in_progress" for 10 minutes, no iteration visibility
```

**Mark Iteration Complete When Done:**

```
Iteration Lifecycle:

Iteration 1:
  Mark "Iteration 1/10" as in_progress
  Run designer validation
  If NEEDS IMPROVEMENT: Run developer fixes
  Mark "Iteration 1/10" as completed

Iteration 2:
  Mark "Iteration 2/10" as in_progress
  Run designer validation
  If PASS: Exit loop early
  Mark "Iteration 2/10" as completed

Result: Loop exited after 2 iterations
  [✓] Iteration 1/10 (completed)
  [✓] Iteration 2/10 (completed)
  [ ] Iteration 3/10 (not needed, loop exited)
  ...

User sees: "Loop completed in 2/10 iterations"
```

**Track Total Iterations vs Max Limit:**

```
Iteration Progress:

Max: 10 iterations
Current: 5

TodoWrite State:
  [✓] Iteration 1/10
  [✓] Iteration 2/10
  [✓] Iteration 3/10
  [✓] Iteration 4/10
  [→] Iteration 5/10
  [ ] Iteration 6/10
  ...

User sees: "Iteration 5/10 (50% through max)"

Warning at Iteration 8:
  "Iteration 8/10 - approaching max, may escalate to user if not PASS"
```

**Clear Progress Visibility:**

```
Iteration Loop with TodoWrite:

User Request: "Validate UI design"

TodoWrite:
  [✓] PHASE 1: Gather design reference
  [✓] Iteration 1/10: Designer validation (5 issues found)
  [✓] Iteration 2/10: Designer validation (3 issues found)
  [✓] Iteration 3/10: Designer validation (1 issue found)
  [→] Iteration 4/10: Designer validation (in_progress)
  [ ] Iteration 5/10: Designer validation
  ...
  [ ] PHASE 3: User validation gate

User sees:
  - 4 iterations completed (40% through max)
  - Issues reducing each iteration (5 → 3 → 1)
  - Progress toward PASS
```

---

### Pattern 6: Parallel Task Tracking

**Multiple Agents Executing Simultaneously:**

When running agents in parallel, track each separately:

```
✅ CORRECT - Separate Tasks for Parallel Agents:

Multi-Model Review (3 models in parallel):

TodoWrite:
  [✓] PHASE 1: Prepare review context
  [→] PHASE 2: Claude review (in_progress)
  [→] PHASE 2: Grok review (in_progress)
  [→] PHASE 2: Gemini review (in_progress)
  [ ] PHASE 3: Consolidate reviews

Note: 3 tasks "in_progress" is OK for parallel execution
      (Exception to "one in_progress" rule)

As models complete:
  [✓] PHASE 1: Prepare review context
  [✓] PHASE 2: Claude review (completed)  ← First to finish
  [→] PHASE 2: Grok review (in_progress)
  [→] PHASE 2: Gemini review (in_progress)
  [ ] PHASE 3: Consolidate reviews

User sees: "1/3 reviews complete, 2 in progress"

❌ WRONG - Single Task for Parallel Work:

TodoWrite:
  [✓] PHASE 1: Prepare
  [→] PHASE 2: Run 3 reviews (in_progress)
  [ ] PHASE 3: Consolidate

Problem: No visibility into which reviews are complete
```

**Update As Each Agent Completes:**

```
Parallel Execution Timeline:

T=0s:  Launch 3 reviews in parallel
  [→] Claude review (in_progress)
  [→] Grok review (in_progress)
  [→] Gemini review (in_progress)

T=60s: Claude completes first
  [✓] Claude review (completed)
  [→] Grok review (in_progress)
  [→] Gemini review (in_progress)

T=120s: Gemini completes
  [✓] Claude review (completed)
  [→] Grok review (in_progress)
  [✓] Gemini review (completed)

T=180s: Grok completes
  [✓] Claude review (completed)
  [✓] Grok review (completed)
  [✓] Gemini review (completed)

User sees real-time completion updates
```

**Progress Indicators During Long Parallel Tasks:**

```
For long-running parallel tasks (>2 minutes), show progress:

T=0s:   "Launching 5 AI model reviews (estimated 5 minutes)..."
T=60s:  "1/5 reviews complete..."
T=120s: "2/5 reviews complete..."
T=180s: "4/5 reviews complete, 1 in progress..."
T=240s: "All reviews complete! Consolidating results..."

TodoWrite mirrors this:
  [✓] Claude review (1/5 complete)
  [✓] Grok review (2/5 complete)
  [→] Gemini review (in_progress)
  [→] GPT-5 review (in_progress)
  [→] DeepSeek review (in_progress)
```

---

## Integration with Other Skills

**todowrite-orchestration + multi-agent-coordination:**

```
Use Case: Multi-phase implementation workflow

Step 1: Initialize TodoWrite (todowrite-orchestration)
  Create task list for all 8 phases

Step 2: Sequential Agent Delegation (multi-agent-coordination)
  Phase 1: api-architect
    Mark PHASE 1 as in_progress
    Delegate to api-architect
    Mark PHASE 1 as completed

  Phase 2: backend-developer
    Mark PHASE 2 as in_progress
    Delegate to backend-developer
    Mark PHASE 2 as completed

  ... continue for all phases
```

**todowrite-orchestration + multi-model-validation:**

```
Use Case: Multi-model review with progress tracking

Step 1: Initialize TodoWrite (todowrite-orchestration)
  [ ] PHASE 1: Prepare context
  [ ] PHASE 2: Launch reviews (5 models)
  [ ] PHASE 3: Consolidate results

Step 2: Parallel Execution (multi-model-validation)
  Mark "PHASE 2: Launch reviews" as in_progress
  Launch all 5 models simultaneously
  As each completes: Update progress (1/5, 2/5, ...)
  Mark "PHASE 2: Launch reviews" as completed

Step 3: Real-Time Visibility (todowrite-orchestration)
  User sees: "PHASE 2: 3/5 reviews complete..."
```

**todowrite-orchestration + quality-gates:**

```
Use Case: Iteration loop with TodoWrite tracking

Step 1: Initialize TodoWrite (todowrite-orchestration)
  [ ] Iteration 1/10
  [ ] Iteration 2/10
  ...

Step 2: Iteration Loop (quality-gates)
  For i = 1 to 10:
    Mark "Iteration i/10" as in_progress
    Run designer validation
    If PASS: Exit loop
    Mark "Iteration i/10" as completed

Step 3: Progress Visibility
  User sees: "Iteration 5/10 complete, 5 remaining"
```

---

## Best Practices

**Do:**
- ✅ Initialize TodoWrite BEFORE starting work (step 0)
- ✅ List ALL phases upfront (user sees complete scope)
- ✅ Use 8-15 tasks for typical workflows (readable)
- ✅ Mark completed IMMEDIATELY after finishing (real-time)
- ✅ Keep exactly ONE task in_progress (except parallel tasks)
- ✅ Track iterations separately (Iteration 1/10, 2/10, ...)
- ✅ Update as work progresses (not batched at end)
- ✅ Add new tasks if discovered during execution

**Don't:**
- ❌ Create TodoWrite during workflow (initialize first)
- ❌ Hide phases from user (list all upfront)
- ❌ Create too many tasks (>20 overwhelms user)
- ❌ Batch completions at end of phase (update real-time)
- ❌ Leave multiple tasks in_progress (pick one)
- ❌ Use single task for loop (track iterations separately)
- ❌ Update only at start/end (update during execution)

**Performance:**
- TodoWrite overhead: <1s per update (negligible)
- User visibility benefit: Reduces perceived wait time 30-50%
- Workflow confidence: User knows progress, less likely to cancel

---

## Examples

### Example 1: 8-Phase Implementation Workflow

**Scenario:** Full-cycle implementation with TodoWrite tracking

**Execution:**

```
Step 0: Initialize TodoWrite
  TodoWrite: Create task list
    [ ] PHASE 1: Ask user for requirements
    [ ] PHASE 2: Generate architecture plan
    [ ] PHASE 3: Implement core logic
    [ ] PHASE 3: Add error handling
    [ ] PHASE 3: Write tests
    [ ] PHASE 4: Run test suite
    [ ] PHASE 5: Code review
    [ ] PHASE 6: Fix review issues
    [ ] PHASE 7: User acceptance
    [ ] PHASE 8: Generate report

  User sees: "10 tasks, 0 complete, Phase 1 starting..."

Step 1: PHASE 1
  Mark "PHASE 1: Ask user" as in_progress
  ... gather requirements (30s) ...
  Mark "PHASE 1: Ask user" as completed
  User sees: "1/10 tasks complete (10%)"

Step 2: PHASE 2
  Mark "PHASE 2: Architecture plan" as in_progress
  ... generate plan (2 min) ...
  Mark "PHASE 2: Architecture plan" as completed
  User sees: "2/10 tasks complete (20%)"

Step 3: PHASE 3 (3 sub-tasks)
  Mark "PHASE 3: Implement core" as in_progress
  ... implement (3 min) ...
  Mark "PHASE 3: Implement core" as completed
  User sees: "3/10 tasks complete (30%)"

  Mark "PHASE 3: Add error handling" as in_progress
  ... add error handling (2 min) ...
  Mark "PHASE 3: Add error handling" as completed
  User sees: "4/10 tasks complete (40%)"

  Mark "PHASE 3: Write tests" as in_progress
  ... write tests (3 min) ...
  Mark "PHASE 3: Write tests" as completed
  User sees: "5/10 tasks complete (50%)"

... continue through all phases ...

Final State:
  [✓] All 10 tasks completed
  User sees: "10/10 tasks complete (100%). Workflow finished!"

Total Duration: ~15 minutes
User Experience: Continuous progress updates every 1-3 minutes
```

---

### Example 2: Iteration Loop with Progress Tracking

**Scenario:** Design validation with 10 max iterations

**Execution:**

```
Step 0: Initialize TodoWrite
  TodoWrite: Create task list
    [ ] PHASE 1: Gather design reference
    [ ] Iteration 1/10: Designer validation
    [ ] Iteration 2/10: Designer validation
    [ ] Iteration 3/10: Designer validation
    [ ] Iteration 4/10: Designer validation
    [ ] Iteration 5/10: Designer validation
    ... (10 iterations total)
    [ ] PHASE 3: User validation gate

Step 1: PHASE 1
  Mark "PHASE 1: Gather design" as in_progress
  ... gather design (20s) ...
  Mark "PHASE 1: Gather design" as completed

Step 2: Iteration Loop
  Iteration 1:
    Mark "Iteration 1/10" as in_progress
    Designer: "NEEDS IMPROVEMENT - 5 issues"
    Developer: Fix 5 issues
    Mark "Iteration 1/10" as completed
    User sees: "Iteration 1/10 complete, 5 issues fixed"

  Iteration 2:
    Mark "Iteration 2/10" as in_progress
    Designer: "NEEDS IMPROVEMENT - 3 issues"
    Developer: Fix 3 issues
    Mark "Iteration 2/10" as completed
    User sees: "Iteration 2/10 complete, 3 issues fixed"

  Iteration 3:
    Mark "Iteration 3/10" as in_progress
    Designer: "NEEDS IMPROVEMENT - 1 issue"
    Developer: Fix 1 issue
    Mark "Iteration 3/10" as completed
    User sees: "Iteration 3/10 complete, 1 issue fixed"

  Iteration 4:
    Mark "Iteration 4/10" as in_progress
    Designer: "PASS ✓"
    Mark "Iteration 4/10" as completed
    Exit loop (early exit)
    User sees: "Loop completed in 4/10 iterations"

Step 3: PHASE 3
  Mark "PHASE 3: User validation" as in_progress
  ... user validates ...
  Mark "PHASE 3: User validation" as completed

Final State:
  [✓] PHASE 1: Gather design
  [✓] Iteration 1/10 (5 issues fixed)
  [✓] Iteration 2/10 (3 issues fixed)
  [✓] Iteration 3/10 (1 issue fixed)
  [✓] Iteration 4/10 (PASS)
  [ ] Iteration 5/10 (not needed)
  ...
  [✓] PHASE 3: User validation

User Experience: Clear iteration progress, early exit visible
```

---

### Example 3: Parallel Multi-Model Review

**Scenario:** 5 AI models reviewing code in parallel

**Execution:**

```
Step 0: Initialize TodoWrite
  TodoWrite: Create task list
    [ ] PHASE 1: Prepare review context
    [ ] PHASE 2: Claude review
    [ ] PHASE 2: Grok review
    [ ] PHASE 2: Gemini review
    [ ] PHASE 2: GPT-5 review
    [ ] PHASE 2: DeepSeek review
    [ ] PHASE 3: Consolidate reviews
    [ ] PHASE 4: Present results

Step 1: PHASE 1
  Mark "PHASE 1: Prepare context" as in_progress
  ... prepare (30s) ...
  Mark "PHASE 1: Prepare context" as completed

Step 2: PHASE 2 (Parallel Execution)
  Mark all 5 reviews as in_progress:
    [→] Claude review
    [→] Grok review
    [→] Gemini review
    [→] GPT-5 review
    [→] DeepSeek review

  Launch all 5 in parallel (4-Message Pattern)

  As each completes:
    T=60s:  Claude completes
      [✓] Claude review
      User sees: "1/5 reviews complete"

    T=90s:  Gemini completes
      [✓] Gemini review
      User sees: "2/5 reviews complete"

    T=120s: GPT-5 completes
      [✓] GPT-5 review
      User sees: "3/5 reviews complete"

    T=150s: Grok completes
      [✓] Grok review
      User sees: "4/5 reviews complete"

    T=180s: DeepSeek completes
      [✓] DeepSeek review
      User sees: "5/5 reviews complete!"

Step 3: PHASE 3
  Mark "PHASE 3: Consolidate" as in_progress
  ... consolidate (30s) ...
  Mark "PHASE 3: Consolidate" as completed

Step 4: PHASE 4
  Mark "PHASE 4: Present results" as in_progress
  ... present (10s) ...
  Mark "PHASE 4: Present results" as completed

Final State:
  [✓] All 8 tasks completed
  User sees: "Multi-model review complete in 3 minutes"

User Experience:
  - Real-time progress as each model completes
  - Clear visibility: "3/5 reviews complete"
  - Reduces perceived wait time (user knows progress)
```

---

## Troubleshooting

**Problem: User thinks workflow is stuck**

Cause: No TodoWrite updates for >1 minute

Solution: Update TodoWrite more frequently, or add sub-tasks

```
❌ Wrong:
  [→] PHASE 3: Implementation (in_progress for 10 minutes)

✅ Correct:
  [✓] PHASE 3: Implement core logic (2 min)
  [✓] PHASE 3: Add error handling (3 min)
  [→] PHASE 3: Write tests (in_progress, 2 min so far)

User sees progress every 2-3 minutes
```

---

**Problem: Too many tasks (>20), overwhelming**

Cause: Too granular task breakdown

Solution: Group micro-tasks into larger operations

```
❌ Wrong (25 tasks):
  [ ] Read file 1
  [ ] Read file 2
  [ ] Write file 3
  ... (25 micro-tasks)

✅ Correct (8 tasks):
  [ ] PHASE 1: Gather inputs (includes reading files)
  [ ] PHASE 2: Process data
  ... (8 significant operations)
```

---

**Problem: Multiple tasks "in_progress" (not parallel execution)**

Cause: Forgot to mark previous task as completed

Solution: Always mark completed before starting next

```
❌ Wrong:
  [→] PHASE 1: Ask user (in_progress)
  [→] PHASE 2: Plan (in_progress)  ← Both in_progress?

✅ Correct:
  [✓] PHASE 1: Ask user (completed)
  [→] PHASE 2: Plan (in_progress)  ← Only one
```

---

## Summary

TodoWrite orchestration provides real-time progress visibility through:

- **Phase initialization** (create task list before starting)
- **Appropriate granularity** (8-15 tasks, significant operations)
- **Real-time updates** (mark completed immediately)
- **Exactly one in_progress** (except parallel execution)
- **Iteration tracking** (separate task per iteration)
- **Parallel task tracking** (update as each completes)

Master these patterns and users will always know:
- What's happening now
- What's coming next
- How much progress has been made
- How much remains

This transforms "black box" workflows into transparent, trackable processes.

---

**Extracted From:**
- `/review` command (10-task initialization, phase-based tracking)
- `/implement` command (8-phase workflow with sub-tasks)
- `/validate-ui` command (iteration tracking, user feedback rounds)
- All multi-phase orchestration workflows
