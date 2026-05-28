---
name: manage-tasks
description: Manage implementation tasks with sequential sub-steps within a plan
allowed-tools: Read, Glob, Bash
---

# Manage Tasks Skill

Manage implementation tasks with sequential sub-steps within a plan. Each task references deliverables from the solution document and contains ordered steps for execution.

> **Implementation Details**: See [design-for-manage-tasks.md](/.plan/task-management/design-for-manage-tasks.md) for the complete specification including file format, all commands, parameters, and validation rules.

## What This Skill Provides

- Individual TOON file storage for each task
- Sequential, immutable numbering (TASK-1, TASK-2, etc.)
- Deliverable references (M:N relationship to solution_outline.md)
- Delegation context (skill + workflow for execution)
- Verification commands and criteria
- Step management with status tracking
- Simple execution loop via `next` query

## When to Activate This Skill

Activate this skill when:
- Creating or managing implementation tasks for a plan
- Querying next actionable task/step
- Marking steps as started/completed/skipped
- Tracking implementation progress

---

## Storage Location

Tasks are stored in the plan directory:

```
{plan_dir}/tasks/
  TASK-001-IMPL.toon
  TASK-002-IMPL.toon
  TASK-003-FIX.toon
```

**Filename format**: `TASK-{NNN}-{TYPE}.toon` where TYPE is: IMPL, FIX, SONAR, PR, LINT, SEC, DOC

---

## File Format (Summary)

```toon
number: 1
title: Update misc agents to TOON output
status: pending
phase: execute
domain: plan-marshall-plugin-dev
profile: implementation
origin: plan
created: 2025-12-02T10:30:00Z
updated: 2025-12-02T10:30:00Z

skills:
  - pm-plugin-development:plugin-maintain
  - pm-plugin-development:plugin-architecture

deliverables[3]:
- 1
- 2
- 4

depends_on: TASK-1, TASK-2

description: |
  Migrate miscellaneous agents from JSON to TOON output format.

delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component
  domain: plan-marshall-plugin-dev
  context_skills:
  - pm-plugin-development:plugin-architecture

steps[3]{number,title,status}:
1,pm-plugin-development/agents/tool-coverage-agent.md,pending
2,pm-dev-builder/agents/gradle-builder.md,pending
3,pm-dev-frontend/commands/js-generate-coverage.md,pending

verification:
  commands[1]:
  - grep -L '```json' {files} | wc -l
  criteria: No JSON blocks remain
  manual: false

current_step: 1
```

**New Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `domain` | string | Task domain (arbitrary string, e.g., java, javascript, my-domain) |
| `profile` | string | Task profile (arbitrary string, e.g., `implementation`, `testing`) |
| `type` | string | Task type for filename: `IMPL`, `FIX`, `SONAR`, `PR`, `LINT`, `SEC`, `DOC` |
| `skills` | list | Pre-resolved skills for task execution |
| `origin` | string | Task origin: `plan` (from task-plan phase) or `fix` (from finalize) |
| `priority` | int | Optional priority for fix tasks (1=high, 2=medium, 3=low) |
| `finding` | object | Optional finding details for fix tasks |

---

## Operations

Script: `pm-workflow:manage-tasks:manage-tasks`

| Command | Parameters | Description |
|---------|------------|-------------|
| `add` | `--plan-id` + stdin | Add a new task (reads definition from stdin) |
| `update` | `--plan-id --number [--title] [--description] [--depends-on] [--status] [--domain] [--profile] [--skills] [--deliverables]` | Update task metadata |
| `remove` | `--plan-id --number` | Remove a task |
| `list` | `--plan-id [--status] [--phase] [--deliverable] [--ready]` | List all tasks |
| `get` | `--plan-id --number` | Get single task details |
| `next` | `--plan-id [--phase] [--include-context] [--ignore-deps]` | Get next pending task/step |
| `tasks-by-domain` | `--plan-id --domain` | List tasks filtered by domain |
| `tasks-by-profile` | `--plan-id --profile` | List tasks filtered by profile |
| `next-tasks` | `--plan-id` | Get all tasks ready for parallel execution |
| `step-start` | `--plan-id --task --step` | Mark step as in_progress |
| `step-done` | `--plan-id --task --step` | Mark step as done |
| `step-skip` | `--plan-id --task --step [--reason]` | Skip a step |
| `add-step` | `--plan-id --task --title [--after]` | Add step to task |
| `remove-step` | `--plan-id --task --step` | Remove step from task |

### Add Command (stdin-based API)

The `add` command reads the task definition from stdin in TOON format. Only `--plan-id` is passed as a CLI argument.

**Why stdin?** Complex task definitions with verification commands containing shell metacharacters (pipes, wildcards, quotes) caused permission issues when passed as CLI arguments. The stdin approach avoids shell interpretation of these characters.

**Stdin format**:

```toon
title: My Task Title
deliverables: [1, 2, 3]
domain: plan-marshall-plugin-dev
profile: implementation
type: IMPL
phase: execute
origin: plan
description: |
  Multi-line task description here.
  Can include any characters.

skills:
  - pm-plugin-development:plugin-maintain
  - pm-plugin-development:plugin-architecture

steps:
  - First step to execute
  - Second step to execute
  - Third step to execute

depends_on: none

delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component
  context_skills:
    - pm-plugin-development:plugin-architecture

verification:
  commands:
    - grep -l '```json' marketplace/bundles/*.md | wc -l
    - mvn verify
  criteria: All grep commands return 0 (no JSON blocks remain)
  manual: false
```

**Required fields**: `title`, `deliverables`, `domain`, `profile`, `skills`, `steps`

**Optional fields**: `phase` (default: execute), `description`, `depends_on`, `delegation`, `verification`, `origin` (default: plan), `priority`, `finding`

**Field values**:
- `deliverables`: Array of integers `[1, 2, 3]`
- `domain`: Domain from config.toon (e.g., `java`, `javascript`, `plan-marshall-plugin-dev`)
- `profile`: Arbitrary profile key from marshal.json (e.g., `implementation`, `testing`, `architecture`)
- `skills`: Array of `bundle:skill` format strings
- `phase`: One of `init`, `outline`, `plan`, `execute`, `finalize`
- `depends_on`: `none` or task references like `TASK-1, TASK-2`
- `origin`: `plan` (from task-plan phase) or `fix` (from finalize phase)

### List/Next Filters

| Parameter | Description |
|-----------|-------------|
| `--phase` | Filter by plan phase (init/outline/plan/execute/finalize) |
| `--deliverable` | Filter by deliverable number |
| `--ready` | Only tasks with satisfied dependencies |
| `--ignore-deps` | (next only) Ignore dependency constraints |

---

## Quick Examples

### Add a task

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id my-feature <<'EOF'
title: Update misc agents to TOON
deliverables: [1, 2, 4]
domain: java
description: |
  Migrate miscellaneous agents from JSON to TOON output format.

steps:
  - file1.md
  - file2.md
  - file3.md

delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component

verification:
  commands:
    - mvn verify
  criteria: Build passes
EOF
```

### Add a task with dependencies

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id my-feature <<'EOF'
title: Write integration tests
deliverables: [3]
domain: java-testing
description: Add integration tests for new endpoint

steps:
  - Create test class
  - Add test methods
  - Run tests

depends_on: TASK-1, TASK-2

verification:
  commands:
    - mvn verify -Pintegration
  criteria: All tests pass
EOF
```

### Add a task with complex verification commands (shell metacharacters)

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id migrate-json-to-toon <<'EOF'
title: Migrate agent outputs to TOON
deliverables: [1, 2, 3]
domain: plan-marshall-plugin-dev
description: |
  Update agents to use TOON format instead of JSON.

steps:
  - Update java-implement-agent.md
  - Update java-verify-agent.md
  - Update gradle-builder.md

delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component

verification:
  commands:
    - grep -l '```json' marketplace/bundles/pm-dev-java/agents/*.md | wc -l
    - grep -l '```json' marketplace/bundles/pm-dev-builder/agents/*.md | wc -l
  criteria: All grep commands return 0 (no JSON blocks remain)
EOF
```

### Get next task/step (respects dependencies)

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks next \
  --plan-id my-feature
```

### Get next task in specific phase

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks next \
  --plan-id my-feature \
  --phase execute
```

### List ready tasks only

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks list \
  --plan-id my-feature \
  --ready
```

### Mark step done

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks step-done \
  --plan-id my-feature \
  --task 2 \
  --step 3
```

---

## Integration Points

### With task-plan-agent

Task-plan agents create tasks during plan refinement using heredoc:
```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id {plan_id} <<'EOF'
title: {task_title}
deliverables: [{n1}, {n2}]
domain: {domain}
steps:
  - {step1}
  - {step2}
...
EOF
```

### With plan-execute

Plan-execute iterates through tasks:
```
LOOP:
  1. manage-tasks next --plan-id {plan_id}
  2. IF no next: DONE
  3. SPAWN implement agent
  4. CONTINUE
```

### With implement-agent

Implement agents execute steps:
```
1. manage-tasks get --plan-id {plan_id} --number {N}
2. FOR EACH step: step-start → execute → step-done
3. RUN verification
```

---

## Deliverable-to-Task Relationship

Tasks reference deliverables from `solution_outline.md` using the `deliverables` field in stdin.

| Pattern | Description | Example |
|---------|-------------|---------|
| 1:1 | One task per deliverable | `deliverables: [1]` - Task implements deliverable 1 |
| N:1 | Multiple deliverables in one task | `deliverables: [1, 2, 3]` - Task implements deliverables 1, 2, 3 |
| 1:N | One deliverable split across tasks | TASK-1 and TASK-2 both have `deliverables: [1]` |

**When to use N:1**: Group related deliverables that share implementation context.

**When to use 1:N**: Split large deliverables into phased implementation (e.g., init task, implement task, verify task).

---

## Dependency Management

Tasks can depend on other tasks using the `depends_on` field in stdin:

```yaml
# Task 3 waits for Task 1 and Task 2 to complete
depends_on: TASK-1, TASK-2

# No dependencies
depends_on: none
```

**Dependency enforcement**:
- `next` command only returns tasks with satisfied dependencies
- Use `--ignore-deps` to bypass dependency checking
- Use `--ready` filter to list only ready tasks

**Blocked output**: When tasks are blocked by dependencies, `next` returns:

```toon
next: null
blocked_tasks[2]{number,title,waiting_for}:
1,Write tests,TASK-3
2,Deploy,TASK-3, TASK-4
```

---

## Phase Filtering

Tasks belong to plan phases: `init`, `outline`, `plan`, `execute`, `finalize`

**Filter by phase**:
```bash
# List execute phase tasks only
--phase execute

# Get next task in finalize phase
next --phase finalize
```

**Phase purpose**:
- `init`: Setup tasks (create directories, configs)
- `outline`: Solution outline creation
- `plan`: Task planning and skill resolution
- `execute`: Implementation tasks (code changes)
- `finalize`: Cleanup tasks (docs, release)

---

## Status Model

**Task Status**: `pending` → `in_progress` → `done` (or `blocked`)

**Step Status**: `pending` → `in_progress` → `done` (or `skipped`)

---

## Related Documents

- [design-for-manage-tasks.md](/.plan/task-management/design-for-manage-tasks.md) - Complete implementation specification
- [design-for-task-planning.md](/.plan/task-management/design-for-task-planning.md) - Task-plan agent workflows
- [architecture.md](/.plan/task-management/architecture.md) - Core concepts
