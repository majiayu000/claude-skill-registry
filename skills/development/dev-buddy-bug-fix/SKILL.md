---
name: dev-buddy-bug-fix
description: Bug fix pipeline — chains root cause analysis, requirements, planning, plan review, implementation, and code review. Uses single plan file and TaskManagement for progress tracking.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, TaskGet
---

# Bug Fix Pipeline Orchestrator

Run the full bug fix pipeline end-to-end. Chains individual stage skills in the order defined by `bugfix_pipeline` in `~/.vcp/dev-buddy.json`. All phases append to a single plan file.

---

## Step 1: Initialize

1. Load the pipeline config:

```bash
bun -e "
import { loadDevBuddyConfig, expandPipelineToEntries } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stages = expandPipelineToEntries(config, 'bugfix_pipeline');
console.log(JSON.stringify({
  pipeline: config.bugfix_pipeline,
  stages,
  max_iterations: config.max_iterations
}));
"
```

2. Display the pipeline stages to the user:
```
Bug Fix Pipeline: rca → requirements → planning → plan-review → implementation → code-review
Executors: {count} total across {stage_count} stages
```

3. **Initialize plan file** — the plan file must exist before any stage appends to it. Create it now via the Write tool or by entering plan mode. Write the header:
```markdown
# Plan: Bug Fix — {user's bug description (short title)}
**Status:** rca
**Pipeline:** bug-fix
**Created:** {date}

---
```

4. **Create pipeline phase tasks with TaskManagement:**

```
T_rca = TaskCreate(subject='Phase: Root Cause Analysis', description='Diagnose the bug — find root cause with evidence', activeForm='Diagnosing...')
T_req = TaskCreate(subject='Phase: Requirements + TDD Test Plan', description='Define fix requirements, create TDD tests, identify risks', activeForm='Gathering requirements...')
TaskUpdate(T_req, addBlockedBy: [T_rca])
T_plan = TaskCreate(subject='Phase: Implementation Planning', description='Create granular fix steps mapped to ACs and tests', activeForm='Planning...')
TaskUpdate(T_plan, addBlockedBy: [T_req])
T_review_plan = TaskCreate(subject='Phase: Plan Review', description='Review fix plan for coverage and granularity', activeForm='Reviewing plan...')
TaskUpdate(T_review_plan, addBlockedBy: [T_plan])
T_impl = TaskCreate(subject='Phase: Implementation', description='Implement fix with TDD loop', activeForm='Implementing...')
TaskUpdate(T_impl, addBlockedBy: [T_review_plan])
T_review_code = TaskCreate(subject='Phase: Code Review', description='Review fix against ACs with evidence', activeForm='Reviewing code...')
TaskUpdate(T_review_code, addBlockedBy: [T_impl])
```

---

## Step 2: Execute Stages in Order

For each stage type in `bugfix_pipeline`:

### Stage-to-Skill Mapping

| Stage Type | Skill | Plan File Section Produced |
|---|---|---|
| `rca` | `Skill(skill: "dev-buddy-rca")` | RCA Diagnosis |
| `requirements` | `Skill(skill: "dev-buddy-requirements")` | Requirements + TDD Test Plan + Risk Registry |
| `planning` | `Skill(skill: "dev-buddy-plan")` | Implementation Steps |
| `plan-review` | `Skill(skill: "dev-buddy-review", args: "--plan")` | Plan Review Record |
| `implementation` | `Skill(skill: "dev-buddy-implement")` | Step status updates |
| `code-review` | `Skill(skill: "dev-buddy-review", args: "--code")` | Code Review Record + Sign-off |

### Execution Flow

Same as feature pipeline:
1. `TaskUpdate(phase_task_id, status: 'in_progress')`
2. Announce each stage
3. Invoke the corresponding skill
4. Verify expected plan file section exists
5. `TaskUpdate(phase_task_id, status: 'completed')`
6. If review returns `rejected` → **STOP**, mark blocked, report

---

## Step 3: Resume Support

Same as feature pipeline:
1. `TaskList()` to find completed vs pending phases
2. Read plan file to check which sections exist
3. Skip completed phases, continue from next pending

---

## Step 4: Report

After all stages complete:
1. Present per-stage status summary
2. `TaskList()` for final task statuses
3. If all passed → "Bug fix pipeline complete!"
4. If any rejected → report which stage and remaining findings
