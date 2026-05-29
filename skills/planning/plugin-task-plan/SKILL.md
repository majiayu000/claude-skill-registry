---
name: plugin-task-plan
description: Create implementation tasks from deliverables using skill delegation
allowed-tools: Read, Bash
---

# Plugin Task Plan Skill

**Role**: Domain planning skill for plugin development tasks. Transforms solution outline deliverables into optimized, executable tasks that delegate to existing skills for implementation.

**Key Pattern**: Skill delegation with optimization - reads deliverables with metadata from `solution_outline.md`, applies aggregation/split analysis, creates tasks with delegation blocks and dependencies.

## Contract Compliance

**MANDATORY**: All tasks MUST follow the structure defined in the central contracts:

| Contract | Location | Purpose |
|----------|----------|---------|
| Task Contract | `pm-workflow:manage-tasks/standards/task-contract.md` | Task structure and optimization workflow |

**Non-compliant tasks will be rejected by validation.**

**CRITICAL**: The `steps` field MUST contain file paths from the deliverable's `Affected files` section:

```yaml
# CORRECT - file paths from deliverable
steps:
  - marketplace/bundles/pm-workflow/agents/plan-init-agent.md
  - marketplace/bundles/pm-workflow/agents/solution-outline-agent.md

# WRONG - descriptive text (violates contract)
steps[2]{number,title,status}:
1,Convert plan-init-agent outputs,pending
2,Convert solution-outline-agent outputs,pending
```

The `steps` field lists FILES TO MODIFY, not progress tracking entries.

## Operation: plan

**Input**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan identifier |
| `deliverable_number` | number | No | Single deliverable number (omit to process all deliverables) |

**Process**:

### Step 1: Load All Deliverables

Read the solution document to get all deliverables with metadata:

```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline \
  list-deliverables \
  --plan-id {plan_id}
```

For each deliverable, extract:
- `metadata.change_type`, `metadata.execution_mode`, `metadata.domain`
- `metadata.suggested_skill`, `metadata.suggested_workflow`
- `metadata.context_skills`, `metadata.depends`
- `affected_files`, `verification`

### Step 2: Build Dependency Graph

Parse `depends` field for each deliverable:
- Identify independent deliverables (`depends: none`)
- Identify dependency chains
- Detect cycles (INVALID - reject)

### Step 3: Analyze for Aggregation

For each pair of deliverables, check if they can be aggregated:
- Same `change_type`?
- Same `suggested_skill`?
- Same `execution_mode` (must be `automated`)?
- Combined file count < 10?
- **NO dependency between them?** (CRITICAL - cannot aggregate if one depends on other)

### Step 4: Analyze for Splits

For each deliverable, check for split requirements:
- `execution_mode: mixed` → MUST split
- Different concerns within → SHOULD split
- File count > 15 → CONSIDER splitting

### Step 4b: Log Optimization Decisions (REQUIRED)

After analyzing each deliverable or deliverable pair, log the decision:

```bash
# If aggregating deliverables
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} INFO "[OPTIMIZATION] (pm-plugin-development:plugin-task-plan) Aggregating D{N}+D{M}: same skill ({skill}), no inter-dependency"

# If keeping deliverable separate
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} INFO "[OPTIMIZATION] (pm-plugin-development:plugin-task-plan) Keeping D{N} separate: {reason}"

# If splitting deliverable
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} INFO "[OPTIMIZATION] (pm-plugin-development:plugin-task-plan) Splitting D{N}: execution_mode=mixed"
```

This logging is REQUIRED for audit trail and debugging.

### Step 5: Create Optimized Tasks

For aggregated deliverables or single deliverables, create tasks using heredoc.

**CRITICAL**: The `steps` field MUST contain file paths copied from the deliverable's `Affected files` section.

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id {plan_id} <<'EOF'
title: {Action Verb} {Target}: {Scope}
deliverables: [{n1}, {n2}, {n3}]
domain: plan-marshall-plugin-dev
phase: execute
description: |
  {combined description from deliverables}

steps:
  - marketplace/bundles/{bundle}/agents/{file1}.md
  - marketplace/bundles/{bundle}/agents/{file2}.md
  - marketplace/bundles/{bundle}/commands/{file3}.md

depends_on: {TASK-N | none}

delegation:
  skill: {suggested_skill from deliverable metadata}
  workflow: {suggested_workflow from deliverable metadata}
  context_skills: {context_skills from deliverable metadata - MUST include even if empty []}

verification:
  commands:
    - {verification.command from deliverable}
  criteria: {verification.criteria from deliverable}
EOF
```

**Field mapping from deliverable to task**:

| Deliverable Field | Task Field | Required |
|-------------------|------------|----------|
| `Affected files:` list | `steps:` list (copy file paths directly) | Yes |
| `metadata.suggested_skill` | `delegation.skill` | Yes |
| `metadata.suggested_workflow` | `delegation.workflow` | Yes |
| `metadata.context_skills` | `delegation.context_skills` | **Yes (even if empty `[]`)** |
| `metadata.depends` | Used to compute `depends_on` | Yes |
| `Verification.Command` | `verification.commands` | Yes |
| `Verification.Criteria` | `verification.criteria` | Yes |

**CRITICAL**: The `context_skills` field MUST always be included in the delegation block, even when empty. Tasks without this field violate the task-contract and will fail validation.

**Example with real paths**:

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks add \
  --plan-id migrate-json-to-toon <<'EOF'
title: Migrate pm-workflow Agents to TOON Format
deliverables: [2]
domain: plan-marshall-plugin-dev
phase: execute
description: |
  Convert all JSON output blocks to TOON format in pm-workflow agents.

steps:
  - marketplace/bundles/pm-workflow/agents/plan-init-agent.md
  - marketplace/bundles/pm-workflow/agents/solution-outline-agent.md
  - marketplace/bundles/pm-workflow/agents/task-plan-agent.md
  - marketplace/bundles/pm-workflow/agents/task-execute-agent.md

depends_on: TASK-1

delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component
  context_skills: []

verification:
  commands:
    - grep -r '```json' marketplace/bundles/pm-workflow/agents/
  criteria: Returns no matches (exit code 1)
EOF
```

### Step 6: Record Issues as Lessons

On ambiguous deliverable or planning issues:

```bash
python3 .plan/execute-script.py plan-marshall:lessons-learned:manage-lesson add \
  --component-type skill \
  --component-name plugin-task-plan \
  --category observation \
  --title "{issue summary}" \
  --detail "{context and resolution approach}"
```

### Step 7: Return Results

**Output**:
```toon
status: success
plan_id: {plan_id}

optimization_summary:
  deliverables_processed: {N}
  tasks_created: {M}
  aggregations: {count of deliverable groups}
  splits: {count of split deliverables}

tasks_created[M]{number,title,deliverables,depends_on}:
1,Create skill: java-logging-patterns,[1],none
2,Update plugin-maintain,[2 3],TASK-1
3,Refactor bundle structure,[4],none

lessons_recorded: {count}
```

---

## Delegation Mapping

When creating tasks, map from deliverable metadata to stdin TOON fields:

| Deliverable Metadata | TOON Field |
|---------------------|------------|
| `domain` | `domain:` |
| `suggested_skill` | `delegation: skill:` |
| `suggested_workflow` | `delegation: workflow:` |
| `context_skills` | `delegation: context_skills:` (merged from all aggregated deliverables) |
| `affected_files` | `steps:` (one per file) |
| `verification.command` | `verification: commands:` (may consolidate) |
| `verification.criteria` | `verification: criteria:` |

### Plugin-Specific Skill Mapping

| Change Type | Component Type | Skill | Workflow |
|-------------|----------------|-------|----------|
| create | skill | pm-plugin-development:plugin-create | create-skill |
| create | command | pm-plugin-development:plugin-create | create-command |
| create | agent | pm-plugin-development:plugin-create | create-agent |
| create | bundle | pm-plugin-development:plugin-create | create-bundle |
| modify | any | pm-plugin-development:plugin-maintain | update-component |
| refactor | any | pm-plugin-development:plugin-maintain | refactor-structure |
| migrate | format | pm-plugin-development:plugin-maintain | update-component |
| delete | any | pm-plugin-development:plugin-maintain | remove-component |

---

## Task Generation Patterns

These patterns show how to create tasks for different operation types. Note that `steps` always contains FILE PATHS.

### Create Component Task

**Deliverable**: "Create new {skill|command|agent} for {purpose}"

The `steps` field lists files that WILL BE CREATED:

```yaml
title: Create skill: java-logging-patterns
steps:
  - marketplace/bundles/pm-dev-java/skills/java-logging-patterns/SKILL.md
delegation:
  skill: pm-plugin-development:plugin-create
  workflow: create-skill
```

### Modify Component Task

**Deliverable**: "Update {component} to {change description}"

The `steps` field lists existing files to MODIFY:

```yaml
title: Update plugin-maintain Skill
steps:
  - marketplace/bundles/pm-plugin-development/skills/plugin-maintain/SKILL.md
delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component
```

### Migrate Task (Multiple Files)

**Deliverable**: "Migrate {components} to {new format}"

The `steps` field lists ALL files to migrate (copied from `Affected files`):

```yaml
title: Migrate pm-workflow Agents to TOON Format
steps:
  - marketplace/bundles/pm-workflow/agents/plan-init-agent.md
  - marketplace/bundles/pm-workflow/agents/solution-outline-agent.md
  - marketplace/bundles/pm-workflow/agents/task-plan-agent.md
  - marketplace/bundles/pm-workflow/agents/task-execute-agent.md
delegation:
  skill: pm-plugin-development:plugin-maintain
  workflow: update-component
```

### Script Task (Special Case)

Scripts are created within skills. The `steps` lists the script file AND its test:

```yaml
title: Create script: manage-config
steps:
  - marketplace/bundles/pm-workflow/skills/manage-config/scripts/manage-config.py
  - test/pm-workflow/manage-config/test_manage_config.py
delegation:
  skill: pm-plugin-development:plugin-create
  workflow: create-skill
```

---

## Parameter Extraction

When analyzing deliverables, extract these parameters:

### For Create Operations

| Parameter | Source |
|-----------|--------|
| `bundle` | Explicit in deliverable OR inferred from context |
| `name` | Explicit in deliverable OR derived from purpose |
| `description` | Extracted from deliverable body |
| `type` | Component-specific (agent type, skill type, etc.) |

### For Modify Operations

| Parameter | Source |
|-----------|--------|
| `component_path` | Explicit path OR resolve from component name |
| `improvements` | Description from deliverable body |

---

## Multi-Task Deliverables

Some deliverables require multiple tasks in sequence:

### Skill with Scripts
```
TASK-1: Create skill structure
  - Delegate to: plugin-create → create-skill

TASK-2: Create script(s)
  - Create Python script in skill/scripts/
  - Add test file
  - Update SKILL.md
```

### Command with New Skill
```
TASK-1: Create supporting skill
  - Delegate to: plugin-create → create-skill

TASK-2: Create command
  - Delegate to: plugin-create → create-command
  - Reference skill from TASK-1
```

---

## Task Dependencies

When creating multiple tasks:

| Dependency | Ordering |
|------------|----------|
| Scripts within skill | Create skill first, then scripts |
| Command referencing skill | Create skill first |
| Agent referencing skill | Create skill first |
| Refactor before create | Complete refactor first |

---

## Error Handling

### Ambiguous Deliverable

If deliverable doesn't specify:
- **Target bundle** → Ask for clarification
- **Component type** → Infer from keywords or ask
- **Operation type** → Default to create unless "update/modify/fix" present

### Missing Information

If deliverable lacks required parameters:
- Generate task with available info
- Note missing parameters in task description
- Record lesson for future reference

---

## Integration

**Caller**: `pm-plugin-development:plugin-task-plan-agent`

**Script Notations** (use EXACTLY as shown):
- `pm-workflow:manage-solution-outline:manage-solution-outline` - Read solution and list deliverables (list-deliverables, read)
- `pm-workflow:manage-tasks:manage-tasks` - Create tasks (add --plan-id X <<'EOF' ... EOF)
- `plan-marshall:lessons-learned:manage-lesson` - Record lessons on issues (add)
- `plan-marshall:logging:manage-log` - Log progress (work)

**Skills Delegated To**:
- `pm-plugin-development:plugin-create` - Component creation (handles validation and verification internally)
- `pm-plugin-development:plugin-maintain` - Component updates and refactoring (handles verification internally)

**Contract Reference**:
- [manage-tasks/standards/task-contract.md](../../pm-workflow/skills/manage-tasks/standards/task-contract.md) - Optimization workflow and decision tables
