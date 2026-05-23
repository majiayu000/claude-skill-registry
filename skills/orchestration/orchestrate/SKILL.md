---
name: orchestrate
description: |
  Task Decomposition Engine - Breaks down complex tasks into phases,
  creates Native Tasks with dependencies, and generates worker prompts.

  Pipeline Position: After /planning, Before /assign
  Handoff: /assign --workload {slug}
user-invocable: true
model: opus
version: "4.0.0"
argument-hint: "--plan-slug <slug> | <task-description>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/parallel-agent.sh"
      timeout: 5000
  PreToolUse:
    - type: command
      command: "/home/palantir/.claude/hooks/orchestrate-validate.sh"
      timeout: 30000
      matcher: "TaskCreate"

# =============================================================================
# EFL Pattern Configuration (P1-P6)
# =============================================================================
agent_delegation:
  enabled: true
  default_mode: true
  max_sub_agents: 5
  delegation_strategy: "complexity-based"

parallel_agent_config:
  enabled: true
  agent_count_by_complexity:
    simple: 1
    moderate: 2
    complex: 3
    very_complex: 4

synthesis_config:
  phase_3a_l2_horizontal:
    enabled: true
    validation_criteria:
      - cross_phase_consistency
      - dependency_acyclicity
      - target_file_coverage
  phase_3b_l3_vertical:
    enabled: true
    validation_criteria:
      - plan_alignment
      - file_existence_verification
      - criteria_measurability

selective_feedback:
  enabled: true
  severity_filter: "warning"
  feedback_targets:
    - gate: "ORCHESTRATE"
      action: "block_on_error"

agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  validation_criteria:
    - "Each phase has clear completion criteria"
    - "Dependencies form DAG (no cycles)"
    - "Target files are specified for each phase"
    - "Phase count is reasonable (3-10)"
---

# /orchestrate - Task Decomposition Engine

> **Version:** 4.0.0 | **Model:** opus
> **Pipeline:** /planning -> [/orchestrate] -> /assign
> **EFL:** P1-P6 Complete

---

## 1. Purpose

Task Decomposition Engine that:
1. Breaks down complex tasks into phases
2. Creates Native Tasks via `TaskCreate`
3. Sets up dependencies via `TaskUpdate(addBlockedBy)`
4. Generates worker prompt files (`.agent/prompts/{slug}/pending/`)
5. Initializes workload-specific context and progress tracking

**Does NOT:**
- Assign tasks to terminals (use `/assign`)
- Execute tasks (handled by `/worker`)
- Set `owner` field (remains null until `/assign`)

---

## 2. Task API Integration

### Task Creation Pattern
```javascript
// Create tasks in dependency order
for (phase of analysis.phases) {
  task = TaskCreate({
    subject: phase.name,
    description: phase.description,
    activeForm: `Working on ${phase.name}`,
    metadata: {
      phaseId: phase.id,
      priority: phase.priority || "P1",
      promptFile: `${workloadPromptDir}/pending/${filename}`
    }
  })
  taskMap[phase.id] = task.id
}

// Set up dependencies
for (phase of analysis.phases) {
  if (phase.dependencies.length > 0) {
    TaskUpdate({
      taskId: taskMap[phase.id],
      addBlockedBy: phase.dependencies.map(d => taskMap[d])
    })
  }
}
```

### Output Files
| File | Purpose |
|------|---------|
| `_context.yaml` | Project context and phase definitions |
| `_progress.yaml` | Progress tracking per terminal |
| `pending/*.yaml` | Worker task prompts |

---

## 3. Invocation

```bash
# With plan slug (from /planning)
/orchestrate --plan-slug user-auth-20260128

# Standalone (auto-generates workload)
/orchestrate "Implement user authentication system"
```

---

## 4. Execution Protocol

### Phase 1: Requirements Analysis
```javascript
// Parse input and generate workload ID
const workloadId = generateWorkloadId(projectSlug)
const workloadSlug = generateSlugFromWorkload(workloadId)

// Analyze task for decomposition
const analysis = analyzeTask(input)
// Returns: { project, objectives, phases[], estimatedWorkers }
```

### Phase 2: Gate 4 Validation (Shift-Left)
```javascript
// Validate phase dependencies BEFORE creating tasks
const gate4Result = await validatePhaseDependencies(phases)

if (gate4Result.hasErrors) {
  return { status: "gate4_failed", errors: gate4Result.errors }
}
// Log warnings but continue
if (gate4Result.hasWarnings) {
  logValidationWarnings("ORCHESTRATE", gate4Result.warnings)
}
```

### Phase 3: Initialize Workload Directory
```javascript
// Create workload structure
Bash(`source .claude/skills/shared/workload-tracker.sh && init_workload_directories "${workloadId}"`)
Bash(`source .claude/skills/shared/workload-files.sh && set_active_workload "${workloadId}"`)
```

### Phase 4: Native Task Creation
```javascript
// Create tasks with TaskCreate
for (phase of phases) {
  const task = TaskCreate({
    subject: phase.name,
    description: phase.description,
    activeForm: `Working on ${phase.name}`
  })
  taskMap[phase.id] = task.id
}
```

### Phase 5: Dependency Setup
```javascript
// Set blockers with TaskUpdate
for (phase of phases) {
  if (phase.dependencies.length > 0) {
    TaskUpdate({
      taskId: taskMap[phase.id],
      addBlockedBy: phase.dependencies.map(d => taskMap[d])
    })
  }
}
```

### Phase 6: Generate Context Files
- `_context.yaml`: Project metadata, phases, dependency graph
- `_progress.yaml`: Terminal status, phase progress

### Phase 7: Generate Worker Prompts
- Create `pending/worker-phase-{n}-{slug}-task.yaml` for each phase
- Include scope, target files, completion criteria, validation

### Phase 8: Summary Output
```
=== Orchestration Complete ===
Project: {project}
Tasks: {count}
Next: /assign auto
```

---

## 5. Error Handling

| Error | Recovery |
|-------|----------|
| Invalid input | Prompt for clarification |
| Too many phases (>10) | Suggest sub-orchestration |
| Circular dependency | Reject, show cycle |
| Gate 4 failed | Show errors, abort |

---

## 6. Handoff Contract

```yaml
# On completion, output:
handoff:
  skill: "orchestrate"
  workload_slug: "{slug}"
  status: "completed"
  next_action:
    skill: "/assign"
    arguments: "--workload {slug}"
```

---

## 7. Version History

| Version | Changes |
|---------|---------|
| 4.0.0 | Deduplicated, V2.1.19 frontmatter, Task API patterns |
| 3.0.0 | Full EFL P1-P6 implementation |
| 2.1.0 | V2.1.19 Spec compatibility |
| 1.0.0 | Initial task orchestration |

**End of Skill Documentation**
