---
name: run-plan
description: "Execute a continuous plan deterministically by following the skill sequence. Use after continuous-planner creates a plan with skill sequences. Reads task_plan.md and executes each skill step by step."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Skill
---

# Run Plan - Deterministic Skill Execution

**Execute continuous plans by following the skill sequence step-by-step.**

## When To Use

After creating a continuous plan with `continuous-planner`, run this to execute the skill sequence deterministically.

## How It Works

1. **Read task_plan.md** to get the skill sequence
2. **For each skill in sequence:**
   - Check if status is "⏸️ Pending"
   - If pending, execute the skill
   - Update status in task_plan.md
   - Update progress.md with results
3. **Handle failures** with recovery protocols
4. **Mark plan complete** when all skills executed

## Skill Sequence Format

The task_plan.md should have a Skill Sequence table:

```markdown
| Step | Skill | Purpose | Input | Output | Status |
|------|-------|---------|-------|--------|--------|
| 1 | front-door | Interview/triage | User request | requirements | ⏸️ Pending |
| 2 | api-designer | Design API | requirements | api_spec | ⏸️ Pending |
| 3 | implement-plan | Execute | api_spec | Complete | ⏸️ Pending |
```

## Execution Flow

```
┌─────────────────────────────────────────┐
│  1. Read task_plan.md                   │
│  2. Parse Skill Sequence table          │
│  3. For each pending skill:             │
│     a. Invoke skill with input          │
│     b. Capture output                   │
│     c. Update findings.md               │
│     d. Update progress.md               │
│     e. Update skill status in plan      │
│  4. Update beads                       │
│  5. Report completion                   │
└─────────────────────────────────────────┘
```

## Error Handling

If a skill fails:
1. Log error to findings.md
2. Check failure-recovery skill for protocols
3. Update skill status to "❌ Failed"
4. Ask user for guidance

## Beads Integration

Each skill execution is tracked as a bead task:
- Plan epic: `continuous-[project-name]`
- Skill tasks: Created as subtasks
- Completion: Mark beads as complete

## Example Usage

```bash
# From project directory with continuous plan
/run-plan

# Or specify plan location
/run-plan .claude/continuous/task_plan.md
```

## Output

After execution:
- task_plan.md: All skills marked complete or failed
- findings.md: Research, errors, discoveries
- progress.md: Execution log with checkpoints
- beads: Tasks marked complete

## Keywords

run plan, execute plan, deterministic, skill sequence, continuous plan, task_plan.md