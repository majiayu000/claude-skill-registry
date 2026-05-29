---
name: manage-lifecycle
description: Manage plan lifecycle with status.toon and phase operations
allowed-tools: Read, Glob, Bash
---

# Manage Lifecycle Skill

Manage plan lifecycle with status.toon and phase operations. Replaces plan.md and absorbs phase-management skill functionality.

## What This Skill Provides

- Status.toon CRUD operations
- Phase management (transitions, progress)
- Plan discovery (list all plans)
- Phase routing (skill mapping)
- Delete operations (via manage-files)
- Archive operations

## When to Activate This Skill

Activate this skill when:
- Creating or updating plan status
- Transitioning between phases
- Discovering all plans
- Deleting plans (to replace or abandon)
- Archiving completed plans

---

## Storage Location

Status is stored in the plan directory:

```
.plan/plans/{plan_id}/status.toon
```

Archived plans:

```
.plan/archived-plans/{yyyy-mm-dd}-{plan-name}/
```

---

## File Format

TOON format with phases table:

```toon
title: Implement JWT Authentication
current_phase: execute

phases[5]{name,status}:
1-init,done
2-outline,done
3-plan,done
4-execute,in_progress
5-finalize,pending

created: 2025-12-02T10:00:00Z
updated: 2025-12-02T14:30:00Z
```

### Status Fields

| Field | Description |
|-------|-------------|
| `title` | Plan title |
| `current_phase` | Current active phase |
| `phases` | Table of phase names and statuses |
| `created` | ISO timestamp when created |
| `updated` | ISO timestamp of last update |

**Note**: Domain information is stored in `config.toon` (as a `domains` array), not in `status.toon`.

### Phase Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Not started |
| `in_progress` | Currently active |
| `done` | Completed |

---

## Status Operations

Script: `pm-workflow:manage-lifecycle:manage-lifecycle`

### read

Read plan status.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle read \
  --plan-id {plan_id}
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature

plan:
  title: Implement JWT Authentication
  current_phase: execute
  phases[5]{name,status}:
  init,done
  outline,done
  plan,done
  execute,in_progress
  finalize,pending
```

### create

Initialize status.toon for a new plan.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle create \
  --plan-id {plan_id} \
  --title "Feature Title" \
  --phases 1-init,2-outline,3-plan,4-execute,5-finalize \
  [--force]
```

**Parameters**:
- `--plan-id` (required): Plan identifier (kebab-case)
- `--title` (required): Plan title
- `--phases` (required): Comma-separated phase names
- `--force`: Overwrite existing status.toon

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: status.toon
created: true

plan:
  title: Feature Title
  current_phase: init
```

### set-phase

Set the current phase.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle set-phase \
  --plan-id {plan_id} \
  --phase execute
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
current_phase: execute
previous_phase: refine
```

### update-phase

Update a specific phase status.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle update-phase \
  --plan-id {plan_id} \
  --phase 1-init \
  --status done
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
phase: 1-init
phase_status: done
```

### progress

Calculate plan progress.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle progress \
  --plan-id {plan_id}
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature

progress:
  total_phases: 4
  completed_phases: 2
  current_phase: execute
  percent: 50
```

---

## Phase Management Operations

### list

Discover all plans.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle list \
  [--filter init,execute]
```

**Parameters**:
- `--filter`: Filter by phases (comma-separated)

**Output** (TOON):
```toon
status: success
total: 2
plans:
  - id: my-feature
    current_phase: execute
    status: in_progress
  - id: bug-fix-123
    current_phase: init
    status: in_progress
```

### transition

Transition to next phase.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle transition \
  --plan-id {plan_id} \
  --completed init
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
completed_phase: 1-init
next_phase: 2-outline
```

### archive

Archive a completed plan.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle archive \
  --plan-id {plan_id} \
  [--dry-run]
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
archived_to: .plan/archived-plans/2025-12-02-my-feature/
```

---

## Delete Operations

Delete operations use `pm-workflow:manage-files:manage-files` (not manage-lifecycle) because deletion involves removing plan directories, not just status management.

### delete-plan

Delete an entire plan directory. Use when:
- Replacing an existing plan with a fresh one
- Abandoning a plan that's no longer needed
- Cleaning up failed or corrupted plans

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files delete-plan \
  --plan-id {plan_id}
```

**Parameters**:
- `--plan-id` (required): Plan identifier to delete

**Output** (TOON):
```toon
status: success
plan_id: my-feature
action: deleted
path: .plan/plans/my-feature
files_removed: 7
```

**Error Output**:
```toon
status: error
plan_id: my-feature
error: plan_not_found
message: Plan directory does not exist
```

**Safety Notes**:
- Only deletes directories under `.plan/plans/`
- Validates plan_id format (kebab-case)
- Does NOT prompt for confirmation (caller handles user confirmation)
- Cannot be undone - ensure user confirms before calling

### Delete vs Archive

| Operation | Use Case | Recoverable |
|-----------|----------|-------------|
| `delete-plan` | Replace, abandon, cleanup | No |
| `archive` | Completed plans for reference | Yes (moved to archived-plans) |

---

### route

Get skill for a phase.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle route \
  --phase execute
```

**Parameters**:
- `--phase` (required): Phase name

**Output** (TOON):
```toon
status: success
phase: execute
skill: plan-execute
description: Execute implementation tasks
```

### get-routing-context

Get combined routing context (phase, skill, and progress) in one call.

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle get-routing-context \
  --plan-id {plan_id}
```

**Parameters**:
- `--plan-id` (required): Plan identifier

**Output** (TOON):
```toon
status: success
plan_id: my-feature
title: Implement JWT Authentication
current_phase: execute
skill: plan-execute
skill_description: Execute implementation tasks
total_phases: 5
completed_phases: 3
phases:
  - name: init
    status: done
  - name: outline
    status: done
  - name: plan
    status: done
  - name: execute
    status: in_progress
  - name: finalize
    status: pending
```

---

## Scripts

**Script**: `pm-workflow:manage-lifecycle:manage-lifecycle`

| Command | Parameters | Description |
|---------|------------|-------------|
| `read` | `--plan-id` | Read plan status |
| `create` | `--plan-id --title --phases [--force]` | Initialize status.toon |
| `set-phase` | `--plan-id --phase` | Set current phase |
| `update-phase` | `--plan-id --phase --status` | Update phase status |
| `progress` | `--plan-id` | Calculate plan progress |
| `list` | `[--filter]` | Discover all plans |
| `transition` | `--plan-id --completed` | Transition to next phase |
| `archive` | `--plan-id [--dry-run]` | Archive completed plan |
| `route` | `--phase` | Get skill for phase |
| `get-routing-context` | `--plan-id` | Get combined routing context |

**Script**: `pm-workflow:manage-files:manage-files` (delete operations)

| Command | Parameters | Description |
|---------|------------|-------------|
| `delete-plan` | `--plan-id` | Delete entire plan directory |

---

## Phase Routing

The `route` command returns skill names for each phase (from script `PHASE_ROUTING`):

| Phase | Skill | Description |
|-------|-------|-------------|
| init | `plan-init` | Initialize plan structure |
| outline | `solution-outline` | Create solution outline with deliverables |
| plan | `task-plan` | Create tasks from deliverables |
| execute | `plan-execute` | Execute implementation tasks |
| finalize | `plan-finalize` | Finalize with commit/PR |

**Note**: These are skill names, not full bundle:skill notation.

**Note**: Domain information is managed in `config.toon` (via `domains` array), not in `status.toon`. Domains are detected during the outline phase.

---

## Error Handling

```toon
status: error
plan_id: my-feature
error: invalid_transition
message: Cannot transition from 'init' to 'execute' - must complete phases in order
```
