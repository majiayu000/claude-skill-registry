---
name: planner
description: Interactive planning and execution for complex tasks. Use when breaking down multi-step projects (planning) or executing approved plans through delegation (execution). Planning creates milestones with specifications; execution delegates to specialized agents.
license: MIT
metadata:
version: 1.0.0
model: claude-opus-4-5
---

# Planner Skill

## Purpose

Two workflows for complex tasks:

1. **Planning workflow** (planner.py): Create and review implementation plans
2. **Execution workflow** (executor.py): Execute approved plans through delegation

## Invocation Routing

**Invoke planner.py** when user asks to:

- "plan", "design", "architect" a feature
- "review" an existing plan
- Break down a complex task into milestones

**Invoke executor.py** when user asks to:

- "execute", "implement", "run" a plan
- "resume" or "continue" execution
- Provides a plan file path for implementation

---

## When to Use

Use the planner skill when the task has:

- Multiple milestones with dependencies
- Architectural decisions requiring documentation
- Migration steps that need coordination
- Complexity that benefits from forced reflection pauses

## When to Skip

Skip the planner skill when the task is:

- Single-step with obvious implementation
- A quick fix or minor change
- Already well-specified by the user

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/planner.py` | Planning and review workflow with step-based state management |
| `scripts/executor.py` | Execution workflow for approved plans with milestone delegation |

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `plan this feature` | planner.py (planning phase) |
| `create implementation plan` | planner.py (planning phase) |
| `review the plan and pick up next item` | executor.py (execution phase) |
| `execute the plan at plans/X.md` | executor.py (execution phase) |
| `resume execution` | executor.py (continue from last step) |

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping review phase after planning | Misses quality/temporal issues | Always run review steps 1-2 before execution |
| Starting execution without /clear | Context pollution from planning | User should /clear before execution workflow |
| Manually following workflow steps | Script manages state and transitions | Run the script and follow its output |
| Planning single-step tasks | Overhead exceeds benefit | Implement directly without planner |
| Editing plan during execution | Creates drift between plan and actions | Return to planning phase for changes |

---

## Verification

After planning:

- [ ] Plan file written to specified path
- [ ] Review phase completed (both TW and QR steps)
- [ ] Review verdict is PASS or PASS_WITH_CONCERNS

After execution:

- [ ] All milestones marked complete
- [ ] Post-implementation QR passed
- [ ] Documentation step completed
- [ ] Retrospective generated

---

## Process

### Planning Overview

```text
PLANNING PHASE (steps 1-N)
    |
    v
Write plan to file
    |
    v
REVIEW PHASE (steps 1-2)
    |-- Step 1: @agent-technical-writer (plan-annotation)
    |-- Step 2: @agent-quality-reviewer (plan-review)
    v
APPROVED --> Execution workflow
```

### Planning Preconditions

Before invoking step 1, you MUST have:

1. **Plan file path** - If user did not specify, ASK before proceeding
2. **Clear problem statement** - What needs to be accomplished

### Planning Invocation

```bash
python3 scripts/planner.py \
  --step-number 1 \
  --total-steps <estimated_steps> \
  --thoughts "<your thinking about the problem>"
```

### Planning Arguments

| Argument        | Description                                      |
| --------------- | ------------------------------------------------ |
| `--phase`       | Workflow phase: `planning` (default) or `review` |
| `--step-number` | Current step (starts at 1)                       |
| `--total-steps` | Estimated total steps for this phase             |
| `--thoughts`    | Your thinking, findings, and progress            |

### Planning Steps

1. Confirm preconditions (plan file path, problem statement)
2. Invoke step 1 immediately
3. Complete REQUIRED ACTIONS from output
4. Invoke next step with your thoughts
5. Repeat until `STATUS: phase_complete`
6. Write plan to file using format below

## Phase Transition: Planning to Review

When planning phase completes, the script outputs an explicit `ACTION REQUIRED`
marker:

```text
============================================
>>> ACTION REQUIRED: INVOKE REVIEW PHASE <<<
============================================
```

**You MUST invoke the review phase before proceeding to execution.**

The review phase ensures:

- Temporally contaminated comments are fixed (via @agent-technical-writer)
- Code snippets have WHY comments (via @agent-technical-writer)
- Plan is validated for production risks (via @agent-quality-reviewer)
- Documentation needs are identified

## Review Phase

After writing the plan file, transition to review phase:

```bash
python3 scripts/planner.py \
  --phase review \
  --step-number 1 \
  --total-steps 2 \
  --thoughts "Plan written to [path/to/plan.md]"
```

### Review Step 1: Technical Writer

Delegate to @agent-technical-writer with mode: `plan-annotation`

### Review Step 2: Quality Reviewer

Delegate to @agent-quality-reviewer with mode: `plan-review`

### After Review

- **PASS / PASS_WITH_CONCERNS**: Ready for execution workflow
- **NEEDS_CHANGES**: Return to planning phase to address issues

---

## Execution Workflow (executor.py)

### Execution Overview

```text
Step 1: Execution Planning
    |
    v
Step 2: Reconciliation (conditional, if prior work signaled)
    |
    v
Step 3: Milestone Execution (repeat until all complete)
    |
    v
Step 4: Post-Implementation QR
    |
    v
QR issues? --YES--> Step 5: Issue Resolution --> delegate fixes --> Step 4
    |
    NO
    v
Step 6: Documentation
    |
    v
Step 7: Retrospective
```

### Execution Preconditions

Before invoking step 1, you MUST have:

1. **Approved plan file** - Plan that passed review phase
2. **Clear context window** - User should /clear before execution

### Execution Invocation

```bash
python3 scripts/executor.py \
  --plan-file PATH \
  --step-number 1 \
  --total-steps 7 \
  --thoughts "<user's request and context>"
```

### Execution Arguments

| Argument        | Description                      |
| --------------- | -------------------------------- |
| `--plan-file`   | Path to the approved plan file   |
| `--step-number` | Current step (1-7)               |
| `--total-steps` | Always 7 for executor            |
| `--thoughts`    | Your current thinking and status |

## Execution Steps

| Step | Name                   | Purpose                                       |
| ---- | ---------------------- | --------------------------------------------- |
| 1    | Execution Planning     | Analyze plan, detect reconciliation, strategy |
| 2    | Reconciliation         | (conditional) Validate existing code vs plan  |
| 3    | Milestone Execution    | Delegate to agents, run tests (repeat)        |
| 4    | Post-Implementation QR | Quality review of implemented code            |
| 5    | Issue Resolution       | (conditional) Present issues, collect fixes   |
| 6    | Documentation          | TW pass for CLAUDE.md, README.md              |
| 7    | Retrospective          | Present execution summary                     |

Note: Step 3 may be re-invoked multiple times until all milestones complete.
Step 4 may loop back through step 5 until QR passes.

---

## Resources

| Resource                              | Purpose                                            |
| ------------------------------------- | -------------------------------------------------- |
| `resources/plan-format.md`            | Plan template (injected at planning completion)    |
| `resources/diff-format.md`            | Authoritative specification for code change format |
| `resources/temporal-contamination.md` | Detecting/fixing temporally contaminated comments  |
| `resources/default-conventions.md`    | Default conventions when project docs are silent   |

Note: Execution guidance is embedded directly in `scripts/executor.py` (not in
separate resource files) since it's only used by that script.

---

## Quick Reference

```bash
# === PLANNING WORKFLOW ===

# Start planning
python3 scripts/planner.py --step-number 1 --total-steps 4 --thoughts "..."

# Continue planning
python3 scripts/planner.py --step-number 2 --total-steps 4 --thoughts "..."

# Start review (after plan written)
python3 scripts/planner.py --phase review --step-number 1 --total-steps 2 \
  --thoughts "Plan at plans/feature.md"

# Continue review
python3 scripts/planner.py --phase review --step-number 2 --total-steps 2 \
  --thoughts "TW done, ready for QR"

# === EXECUTION WORKFLOW ===

# Start execution
python3 scripts/executor.py --plan-file plans/feature.md --step-number 1 \
  --total-steps 7 --thoughts "Execute the feature plan"

# Continue milestone execution
python3 scripts/executor.py --plan-file plans/feature.md --step-number 3 \
  --total-steps 7 --thoughts "Completed M1, M2. Executing M3..."

# After QR passes
python3 scripts/executor.py --plan-file plans/feature.md --step-number 6 \
  --total-steps 7 --thoughts "QR passed. Running documentation."

# Generate retrospective
python3 scripts/executor.py --plan-file plans/feature.md --step-number 7 \
  --total-steps 7 --thoughts "Execution complete. Generating retrospective."
```
