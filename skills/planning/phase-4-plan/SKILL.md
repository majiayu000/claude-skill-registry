---
name: phase-4-plan
description: Domain-agnostic task planning from deliverables with skill resolution and optimization
user-invocable: false
allowed-tools: Read, Bash
---

# Phase Plan Skill

**Role**: Domain-agnostic workflow skill for transforming solution outline deliverables into optimized, executable tasks. Loaded by `pm-workflow:task-plan-agent`.

**Key Pattern**: Reads deliverables with metadata and profiles list from `solution_outline.md`, creates one task per profile (1:N mapping), resolves skills from architecture based on `module` + `profile`, applies aggregation/split analysis, creates tasks with explicit skill lists.

## Contract Compliance

**MANDATORY**: All tasks MUST follow the structure defined in the central contracts:

| Contract | Location | Purpose |
|----------|----------|---------|
| Task Contract | `pm-workflow:manage-tasks/standards/task-contract.md` | Required task structure and optimization workflow |

**CRITICAL - Steps Field**:
- The `steps` field MUST contain file paths from the deliverable's `Affected files` section
- Steps must NOT be descriptive text (e.g., "Update AuthController.java" is INVALID)
- Validation rejects tasks with non-file-path steps

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan identifier |

## Output

```toon
status: success | error
plan_id: {echo}
optimization_summary:
  deliverables_processed: N
  tasks_created: M
  aggregations: N
  splits: N
  parallelizable_groups: N
tasks_created[M]: {number, title, deliverables, depends_on}
execution_order: {parallel groups}
message: {error message if status=error}
```

## Workflow

### Step 1: Load All Deliverables

Read the solution document to get all deliverables with metadata:

```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline \
  list-deliverables \
  --plan-id {plan_id}
```

For each deliverable, extract:
- `metadata.change_type`, `metadata.execution_mode`
- `metadata.domain` (single value)
- `metadata.module` (module name from architecture)
- `metadata.depends`
- `profiles` (list: `implementation`, `testing`)
- `affected_files`
- `verification`

### Step 2: Build Dependency Graph

Parse `depends` field for each deliverable:
- Identify independent deliverables (`depends: none`)
- Identify dependency chains
- Detect cycles (INVALID - reject with error)

### Step 3: Analyze for Aggregation

For each pair of deliverables, check if they can be aggregated:
- Same `change_type`?
- Same `domain`?
- Same `profiles` list?
- Same `execution_mode` (must be `automated`)?
- Combined file count < 10?
- **NO dependency between them?** (CRITICAL - cannot aggregate if one depends on the other)

### Step 4: Analyze for Splits

For each deliverable, check for split requirements:
- `execution_mode: mixed` → MUST split
- File count > 15 → CONSIDER splitting

**Note**: Multiple profiles in `**Profiles:**` block naturally create multiple tasks (1:N) - no additional splitting needed for profile differences.

### Step 5: Create Tasks from Profiles (1:N Mapping)

For each deliverable, create one task per profile in its `profiles` list:

```
For each deliverable D:
  1. Query architecture: module --name {D.module}
  For each profile P in D.profiles:
    2. Extract skills: module.skills_by_profile.{P}
    3. Create task with profile P and resolved skills
    4. If P = testing, add depends on implementation task
```

**Query architecture**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  module --name {deliverable.module} \
  --trace-plan-id {plan_id}
```

**1:N Task Creation Flow**:

```
solution_outline.md                        TASK-*.toon (created by task-plan)
┌────────────────────────────┐             ┌────────────────────────────┐
│ **Metadata:**              │             │ TASK-001-IMPL              │
│ - domain: java             │             │ profile: implementation    │
│ - module: auth-service     │  ───────►   │ skills: [java-core,        │
│                            │  (1:N)      │          java-cdi]         │
│ **Profiles:**              │             ├────────────────────────────┤
│ - implementation           │  ───────►   │ TASK-002-TEST              │
│ - module_testing           │             │ profile: module_testing    │
│                            │             │ skills: [java-core,        │
└────────────────────────────┘             │          junit-core]       │
                                           │ depends: TASK-001-IMPL     │
                                           └────────────────────────────┘
```

**Log skill resolution** (for each task created):
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[SKILL] (pm-workflow:phase-4-plan) Resolved skills for TASK-{N} from {module}.{profile}: [{task.skills}]"
```

**Aggregation Rule**: When aggregating multiple deliverables, they must have same profiles list. Merge resolved skills arrays (union) per profile.

### Step 6: Create Optimized Tasks

For aggregated deliverables or single deliverables, create tasks using heredoc:

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id {plan_id} <<'EOF'
title: {aggregated title}
deliverables: [{n1}, {n2}, {n3}]
domain: {domain from deliverable}
profile: {profile from deliverable}
phase: 5-execute
description: |
  {combined description}

steps:
  - {file1}
  - {file2}
  - {file3}

depends_on: TASK-1, TASK-2

skills:
  - {skill1 from architecture}
  - {skill2 from architecture}

verification:
  commands:
    - {cmd1}
  criteria: {criteria}
EOF
```

**MANDATORY - Log each task creation**:
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[ARTIFACT] (pm-workflow:phase-4-plan) Created TASK-{N}: {title}"
```

**Key Fields**:
- `domain`: Single domain from deliverable
- `profile`: `implementation` or `testing` (determines workflow skill at execution)
- `skills`: Domain skills only (system skills loaded by agent)
- `steps`: File paths from `Affected files` (NOT descriptive text)

### Step 7: Determine Execution Order

Compute parallel execution groups:

```toon
execution_order:
  parallel_group_1: [TASK-1, TASK-3]    # No dependencies
  parallel_group_2: [TASK-2, TASK-4]    # Both depend on group 1
  parallel_group_3: [TASK-5]            # Depends on group 2
```

**Parallelism rules**:
- Tasks with no `depends_on` go in first group
- Tasks depending on same prior tasks can run in parallel
- Sequential dependencies remain sequential

### Step 8: Record Issues as Lessons

On ambiguous deliverable or planning issues:

```bash
python3 .plan/execute-script.py plan-marshall:manage-lessons:manage-lesson add \
  --component "pm-workflow:phase-4-plan" \
  --category improvement \
  --title "{issue summary}" \
  --detail "{context and resolution approach}"
```

**Valid categories**: `bug`, `improvement`, `anti-pattern`

### Step 9: Return Results

**Output**:
```toon
status: success
plan_id: {plan_id}

optimization_summary:
  deliverables_processed: {N}
  tasks_created: {M}
  aggregations: {count of deliverable groups}
  splits: {count of split deliverables}
  parallelizable_groups: {count of independent task groups}

tasks_created[M]{number,title,deliverables,depends_on}:
1,Implement UserService,[1],none
2,Implement UserRepository,[2],none
3,Add integration tests,[3],"TASK-1" "TASK-2"

execution_order:
  parallel_group_1: [TASK-1, TASK-2]
  parallel_group_2: [TASK-3]

lessons_recorded: {count}
```

## Optimization Decision Table

| Factor | Aggregate | Split | Keep |
|--------|-----------|-------|------|
| Same change_type | Yes | | |
| Same domain | Yes | | |
| Same profiles list | Yes | | |
| Combined files < 10 | Yes | | |
| Same execution_mode | Yes | | |
| Both depends: none | Yes | | |
| One depends on other | **Never** | | |
| execution_mode: mixed | | Yes | |
| File count > 15 | | Consider | |
| Large but coherent | | | Yes |
| Single file | | | Yes |

**Note**: Multiple profiles in one deliverable naturally create multiple tasks (1:N). This is not a "split" - it's the standard task creation pattern.

## Dependency Rules for Aggregation

| D1.depends | D2.depends | Can Aggregate? | Reason |
|------------|------------|----------------|--------|
| none | none | Yes | Both independent |
| none | D1 | **No** | D2 depends on D1 |
| D3 | D3 | Yes | Same dependency, can run together |
| D3 | D4 | Yes | Different deps, no conflict |
| D2 | D1 | **No** | Creates cycle if aggregated |

## Skill Resolution Guidelines

Skills are resolved from architecture based on `module` + `profile`:

| Scenario | Behavior |
|----------|----------|
| Single deliverable, single profile | Query `architecture.module --name {module}`, extract `skills_by_profile.{profile}` |
| Single deliverable, multiple profiles | Create one task per profile, each with its own resolved skills |
| Multiple deliverables (aggregation) | Union of resolved skills from all source modules (per profile) |
| Module not in architecture | Error - module must exist in project architecture |
| Profile not in module | Error - profile must exist in `module.skills_by_profile` |

## Error Handling

### Circular Dependencies

If deliverable dependencies form a cycle:
- Error: "Circular dependency detected: D1 -> D2 -> D1"
- Do NOT create tasks

### Module Not in Architecture

If `deliverable.module` is not found in architecture:
- Error: "Module '{module}' not found in architecture - run architecture discovery"
- Record as lesson learned

### Profile Not in Module

If a profile from `deliverable.profiles` is not in `module.skills_by_profile`:
- Error: "Profile '{profile}' not found in {module}.skills_by_profile"
- Record as lesson learned

### Ambiguous Deliverable

If deliverable metadata incomplete:
- Generate task with defaults
- Add lesson-learned for future reference
- Note ambiguity in task description

## Integration

**Invoked by**: `pm-workflow:task-plan-agent` (thin agent)

**Script Notations** (use EXACTLY as shown):
- `pm-workflow:manage-solution-outline:manage-solution-outline` - Read deliverables (list-deliverables, read)
- `plan-marshall:analyze-project-architecture:architecture` - Resolve skills (module --name {module})
- `pm-workflow:manage-tasks:manage-tasks` - Create tasks (add --plan-id X <<'EOF' ... EOF)
- `plan-marshall:manage-lessons:manage-lesson` - Record lessons on issues (add)

**Consumed By**:
- `pm-workflow:task-execute-agent` - Reads tasks and executes them
