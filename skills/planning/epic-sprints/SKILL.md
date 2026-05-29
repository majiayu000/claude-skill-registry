# Epic Sprints Skill

Generate sprint breakdown with dependency graph and execution layers for epic workflows.

## Purpose

Break down epic plans into parallelizable sprints with dependency analysis, API contract locking, and execution layer optimization.

## When to Invoke

- During `/epic` Step 4 (Sprint Breakdown phase)
- After plan.md is complete and reviewed
- Invokes `/tasks` command with epic context

## Sprint Breakdown Process

**Invoke /tasks with epic context:**

```bash
/tasks
```

**The /tasks phase will:**

1. Read plan.md to understand phases
2. Analyze complexity and identify sprint boundaries
3. Build dependency graph between sprints
4. Lock API contracts (OpenAPI schemas) for parallel work
5. Generate sprint-plan.md with execution layers

## Sprint Plan Structure

```xml
<sprint_plan>
  <sprints>
    <sprint id="S01" name="auth-backend">
      <dependencies></dependencies>
      <estimated_hours>16</estimated_hours>
      <subsystems>backend, database</subsystems>
      <contracts_locked>
        <api_contract>contracts/api/auth-v1.yaml</api_contract>
      </contracts_locked>
    </sprint>

    <sprint id="S02" name="auth-frontend">
      <dependencies>S01</dependencies>
      <estimated_hours>20</estimated_hours>
      <subsystems>frontend</subsystems>
    </sprint>

    <sprint id="S03" name="auth-integration">
      <dependencies>S01, S02</dependencies>
      <estimated_hours>12</estimated_hours>
      <subsystems>backend, frontend</subsystems>
    </sprint>
  </sprints>

  <execution_layers>
    <layer num="1">
      <sprint_ids>S01</sprint_ids>
      <parallelizable>true</parallelizable>
    </layer>
    <layer num="2">
      <sprint_ids>S02</sprint_ids>
      <parallelizable>false</parallelizable>
      <depends_on_layer>1</depends_on_layer>
    </layer>
    <layer num="3">
      <sprint_ids>S03</sprint_ids>
      <parallelizable>false</parallelizable>
      <depends_on_layer>2</depends_on_layer>
    </layer>
  </execution_layers>
</sprint_plan>
```

## Tasks Generation

**Also generates tasks.xml:**

- All tasks across all sprints
- Task-level dependencies
- Sprint assignments
- Acceptance criteria per task

## API Contract Locking

For parallel sprint execution, API contracts must be locked:

1. Extract API boundaries from plan.md
2. Generate OpenAPI schemas in `contracts/api/`
3. Mark contracts as locked in sprint-plan.md
4. Sprints reference locked contracts for implementation

## Commit Sprint Breakdown

```bash
# Extract metadata for commit message
SPRINT_COUNT=$(xmllint --xpath 'count(//sprint)' epics/${EPIC_SLUG}/sprint-plan.md)
LAYER_COUNT=$(xmllint --xpath 'count(//layer)' epics/${EPIC_SLUG}/sprint-plan.md)
CONTRACT_COUNT=$(find epics/${EPIC_SLUG}/contracts -name '*.yaml' | wc -l)
TASK_COUNT=$(xmllint --xpath 'count(//task)' epics/${EPIC_SLUG}/tasks.md)

# Commit sprint breakdown and contracts
git add epics/${EPIC_SLUG}/sprint-plan.md
git add epics/${EPIC_SLUG}/tasks.md
git add epics/${EPIC_SLUG}/contracts/
git commit -m "docs(epic-tasks): create sprint breakdown for ${EPIC_SLUG} (${SPRINT_COUNT} sprints)

Sprints: ${SPRINT_COUNT}
Layers: ${LAYER_COUNT}
Contracts locked: ${CONTRACT_COUNT}
Total tasks: ${TASK_COUNT}

Next: /implement-epic (parallel sprint execution)"
```

**Alternative:** `/meta:enforce-git-commits --phase "epic-sprint-breakdown"`

## Dependency Graph Rules

1. **No circular dependencies**: Sprints cannot depend on each other cyclically
2. **Layer assignment**: Sprints in the same layer can run in parallel
3. **Contract boundaries**: Sprints in different layers communicating via API must have locked contracts
4. **Resource constraints**: Consider subsystem conflicts when parallelizing

## Execution Layer Optimization

**Goal**: Maximize parallelization while respecting dependencies

**Algorithm**:

1. Start with sprints that have no dependencies (Layer 1)
2. Sprints depending only on Layer 1 → Layer 2
3. Continue until all sprints assigned
4. Mark layers as parallelizable if multiple sprints share the same layer

**Example optimization**:

```
Before: S01 → S02 → S03 → S04 (sequential, 4 layers)
After:  L1[S01, S03] → L2[S02, S04] (parallel, 2 layers, 2x speedup)
```

## State Updates

After sprint breakdown:

```yaml
phases:
  tasks:
    status: completed
    completed_at: { ISO_TIMESTAMP }

sprints:
  total: { SPRINT_COUNT }
  completed: 0
  failed: 0

layers:
  total: { LAYER_COUNT }
  completed: 0
```

## Next Step

After sprint breakdown, proceed to `/implement-epic` for parallel sprint execution.
