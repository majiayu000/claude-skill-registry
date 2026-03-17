---
name: plugin-plan-implement
description: Implement plugin tasks from plan with step iteration and progress tracking
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
---

# Plugin Plan Implement Skill

**Role**: Implement plugin-domain tasks by iterating through steps (file paths) and applying changes.

**Execution Pattern**: Load task → Load skills → Iterate steps → Apply changes → Verify → Return result

## Scripts

| Script | Purpose |
|--------|---------|
| `pm-workflow:manage-tasks:manage-tasks` | Task retrieval and progress tracking |
| `plan-marshall:manage-logging:manage-log` | Work log entries |
| `plan-marshall:manage-plan-marshall-config:plan-marshall-config` | Domain skill retrieval |

## Standards (Load On-Demand)

### Step Execution
```
Read standards/step-execution.md
```
Contains: How to execute each step type (modify, create, etc.)

---

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan identifier |
| `task_number` | number | Yes | Task to execute |

## Workflow

### Step 1: Load Task Details

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks get \
  --plan-id {plan_id} \
  --number {task_number}
```

Extract from response:
- `title`: Task title for logging
- `description`: What changes to apply
- `delegation.domain`: For loading default skills
- `delegation.context_skills`: Additional skills
- `steps[]`: File paths to process
- `verification`: Commands and criteria

### Step 2: Load Domain Skills

#### 2a. Get Domain Defaults

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  skill-domains get-defaults \
  --domain {delegation.domain}
```

#### 2b. Load Default Skills

```
Skill: {default_skill_1}
Skill: {default_skill_2}
```

#### 2c. Load Context Skills

From task delegation block:

```
Skill: {delegation.context_skills[0]}
Skill: {delegation.context_skills[1]}
```

### Step 3: Log Task Start

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[TASK] (pm-plugin-development:plugin-plan-implement) Starting task {task_number}: {title}"
```

### Step 4: Execute Steps

For each step WHERE `status == pending`:

#### 4a. Execute Step

The step `title` is a file path. Apply changes based on:
1. Task `description` - overall change guidance
2. Loaded skills - implementation patterns
3. File type - markdown with YAML frontmatter for plugins

**For plugin files** (agents, commands, skills):
- Read the file
- Identify sections to update
- Apply changes per task description
- Write updated content

Load step execution patterns if needed:
```
Read standards/step-execution.md
```

#### 4b. Log Step Progress

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STEP] (pm-plugin-development:plugin-plan-implement) Completed step {step_number}: {file_path}"
```

#### 4c. Finalize Step

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks finalize-step \
  --plan-id {plan_id} \
  --task {task_number} \
  --step {step_number} \
  --outcome done
```

### Step 5: Run Verification

After all steps complete:

```bash
# Execute each verification command
{verification.commands[0]}
{verification.commands[1]}
```

Log result:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[VERIFY] (pm-plugin-development:plugin-plan-implement) Verification {passed|failed}: {criteria}"
```

### Step 6: Return Result

**Success Output**:

```toon
status: success
plan_id: {plan_id}
task_number: {task_number}

execution_summary:
  steps_completed: {N}
  steps_total: {M}
  files_modified[N]:
    - {path1}
    - {path2}

verification:
  passed: true
  command: "{verification command}"

next_action: task_complete
```

**Error Output**:

```toon
status: error
plan_id: {plan_id}
task_number: {task_number}

execution_summary:
  steps_completed: {N}
  steps_failed: {M}

failure:
  step: {step_number}
  file: "{file path}"
  error: "{error message}"
  recoverable: true

next_action: requires_attention
```

---

## Error Handling

### Step Failure

If a step fails:
1. Log error to work-log
2. Do NOT mark step as done
3. Continue to next step OR stop (based on severity)
4. Include failure in result

### Verification Failure

If verification fails:
1. Log what failed
2. Return error status with `recoverable: true`
3. Task remains in_progress for retry

---

## Constraints

### File Access
- **`.plan/` files**: ONLY via execute-script.py
- **Marketplace files**: Use Read/Write/Edit as needed

### Progress Tracking
- Execute step
- Mark finalize-step AFTER success (outcome: done or skipped)
- Log progress at each step

---

## Integration

### Called By
- `pm-plugin-development:plugin-plan-implement-agent` - Thin wrapper agent

### Uses
- `pm-plugin-development:plugin-architecture` - Architecture principles
- `pm-workflow:manage-tasks` - Task and step management
- `plan-marshall:manage-logging:manage-log` - Work logging
- Context skills from task delegation (loaded dynamically)

### Related Skills
- `pm-workflow:phase-5-execute` - Generic plan execution orchestrator
- `pm-plugin-development:plugin-maintain` - Plugin maintenance operations
