---
name: dev-buddy-feature-implement
description: Full feature development pipeline — chains requirements, planning, plan review, implementation, and code review stage skills. Uses single plan file and TaskManagement for progress tracking.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, TaskGet
---

# Feature Pipeline Orchestrator

Run the full feature development pipeline end-to-end. All phases append to a single plan file. Uses TaskManagement for progress tracking across context compactions.

---

## Step 1: Initialize

1. Load the pipeline config:

```bash
bun -e "
import { loadDevBuddyConfig, expandPipelineToEntries } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stages = expandPipelineToEntries(config, 'feature_pipeline');
console.log(JSON.stringify({
  pipeline: config.feature_pipeline,
  stages,
  max_iterations: config.max_iterations
}));
"
```

2. Display the pipeline stages to the user:
```
Feature Pipeline: requirements → planning → plan-review → implementation → code-review
Executors: {count} total across {stage_count} stages
```

3. **Create pipeline phase tasks with TaskManagement:**

```
T_req = TaskCreate(subject='Phase: Requirements + TDD Test Plan', description='Gather requirements, create TDD tests, identify risks', activeForm='Gathering requirements...')
T_plan = TaskCreate(subject='Phase: Implementation Planning', description='Create granular implementation steps mapped to ACs and tests', activeForm='Planning...')
TaskUpdate(T_plan, addBlockedBy: [T_req])
T_review_plan = TaskCreate(subject='Phase: Plan Review', description='Review plan for coverage, granularity, and risk acknowledgment', activeForm='Reviewing plan...')
TaskUpdate(T_review_plan, addBlockedBy: [T_plan])
T_impl = TaskCreate(subject='Phase: Implementation', description='Implement plan with TDD loop', activeForm='Implementing...')
TaskUpdate(T_impl, addBlockedBy: [T_review_plan])
T_review_code = TaskCreate(subject='Phase: Code Review', description='Review implementation against ACs with evidence', activeForm='Reviewing code...')
TaskUpdate(T_review_code, addBlockedBy: [T_impl])
```

---

## Step 2: Execute Stages in Order

For each stage type in `feature_pipeline`:

### Stage-to-Skill Mapping

| Stage Type | Skill | Plan File Section Produced |
|---|---|---|
| `requirements` | `Skill(skill: "dev-buddy-requirements")` | Requirements + TDD Test Plan + Risk Registry |
| `planning` | `Skill(skill: "dev-buddy-plan")` | Implementation Steps |
| `plan-review` | `Skill(skill: "dev-buddy-review", args: "--plan")` | Plan Review Record |
| `implementation` | `Skill(skill: "dev-buddy-implement")` | Step status updates |
| `code-review` | `Skill(skill: "dev-buddy-review", args: "--code")` | Code Review Record + Sign-off |

### Execution Flow

For each stage:
1. `TaskUpdate(phase_task_id, status: 'in_progress')`
2. Announce: `**Stage: {stage_type}** — dispatching...`
3. Invoke the corresponding skill (see mapping above)
4. After skill completes, verify the expected plan file section exists (Read the plan file, check for the section header)
5. `TaskUpdate(phase_task_id, status: 'completed')`
6. If a review stage status is `rejected` (check the fenced JSON in the review record section) → **STOP the pipeline**, `TaskUpdate(phase_task_id, status: 'blocked')`, report to user

**IMPORTANT:** Review stages handle their own repair loops internally. The orchestrator just invokes once and waits.

---

## Step 3: Resume Support

If context is compacted mid-pipeline:
1. `TaskList()` — find which phase tasks are completed vs pending
2. Read the plan file — check which sections exist
3. Skip completed phases, continue from the next pending one

---

## Step 4: Report

After all stages complete:
1. Present per-stage status summary
2. `TaskList()` to show final task statuses
3. If all stages passed → "Feature pipeline complete!"
4. If any stage was rejected → report which stage and remaining findings
