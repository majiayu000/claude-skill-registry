---
name: collect
description: |
  Result Aggregation Agent - Aggregates worker results, verifies completion,
  detects blockers, and generates collection report.

  Pipeline Position: After /worker, Before /synthesis
  Handoff: /synthesis for traceability validation
user-invocable: true
model: opus
version: "4.0.0"
argument-hint: "[--all | --phase <phase-id> | --from-session | --from-git]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - TaskList
  - TaskGet
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000

# =============================================================================
# EFL Pattern Configuration (P1-P6)
# =============================================================================
agent_delegation:
  enabled: true
  default_mode: true
  max_sub_agents: 3
  delegation_strategy: "source-based"

parallel_agent_config:
  enabled: true
  agent_count_by_complexity:
    simple: 1
    moderate: 2
    complex: 3

synthesis_config:
  phase_3a_l2_horizontal:
    enabled: true
    validation_criteria:
      - cross_worker_consistency
      - deliverable_completeness
      - gap_detection
  phase_3b_l3_vertical:
    enabled: true
    validation_criteria:
      - code_reality_check
      - reference_accuracy
      - output_verification

selective_feedback:
  enabled: true
  severity_filter: "warning"
  feedback_targets:
    - gate: "COLLECT"
      action: "block_on_error"

agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  validation_criteria:
    - "All worker outputs collected"
    - "Completion manifests verified"
    - "No missing deliverables"
---

# /collect - Result Aggregation Agent

> **Version:** 4.0.0 | **Model:** opus
> **Pipeline:** /worker -> [/collect] -> /synthesis
> **EFL:** P1-P6 Complete

---

## 1. Purpose

Result Aggregation Agent that:
1. Aggregates worker outputs from all terminals
2. Verifies task completion status via TaskList
3. Validates completion manifests (SHA256 integrity)
4. Detects blockers and incomplete work
5. Generates collection report for /synthesis

---

## 2. Task API Integration

### Collection Pattern
```javascript
// Get all tasks for workload
const allTasks = TaskList()

// Categorize by status
const completed = allTasks.filter(t => t.status === "completed")
const inProgress = allTasks.filter(t => t.status === "in_progress")
const pending = allTasks.filter(t => t.status === "pending")
const blocked = allTasks.filter(t => t.blockedBy?.length > 0)

// Verify each completed task has outputs
for (const task of completed) {
  const outputs = await collectTaskOutputs(task)
  verifyIntegrity(outputs)
}
```

### Multi-Source Collection
```javascript
// Source 1: Task System
const taskResults = collectFromTasks()

// Source 2: Output Files
const fileResults = collectFromFiles(workloadSlug)

// Source 3: Git Commits (optional)
const gitResults = collectFromGit()

// Source 4: Session State
const sessionResults = collectFromSession()

// Merge and deduplicate
const allResults = mergeResults([taskResults, fileResults, gitResults, sessionResults])
```

---

## 3. Invocation

```bash
# Collect all results
/collect

# Collect specific phase
/collect --phase phase1

# Collect from specific sources
/collect --from-session
/collect --from-git

# Full collection with all sources
/collect --all
```

---

## 4. Execution Protocol

### Phase 1: Source Discovery
```javascript
// Determine collection sources
const sources = {
  tasks: true,           // Always check TaskList
  files: true,           // Always check output files
  git: args.includes('--from-git'),
  session: args.includes('--from-session')
}

// Get active workload
const workloadSlug = getActiveWorkloadSlug()
const outputDir = `.agent/prompts/${workloadSlug}/outputs`
```

### Phase 2: Task Collection
```javascript
// Collect from Native Task System
const tasks = TaskList()

for (const task of tasks) {
  const detail = TaskGet({taskId: task.id})

  taskResults.push({
    taskId: task.id,
    subject: task.subject,
    status: task.status,
    owner: task.owner,
    completedAt: detail.metadata?.completedAt,
    outputs: detail.metadata?.outputs || []
  })
}
```

### Phase 3: File Collection
```javascript
// Collect from output directories
const terminals = ['terminal-b', 'terminal-c', 'terminal-d']

for (const terminal of terminals) {
  const terminalDir = `${outputDir}/${terminal}`
  const files = Glob(`${terminalDir}/*.md`)

  for (const file of files) {
    const content = Read(file)
    fileResults.push({
      terminal: terminal,
      file: file,
      type: detectOutputType(file), // l1, l2, l3, manifest
      content: extractSummary(content)
    })
  }
}
```

### Phase 4: Integrity Verification
```javascript
// Verify completion manifests
for (const result of completedResults) {
  const manifestPath = `${outputDir}/${result.terminal}/task-${result.taskId}-manifest.yaml`

  if (fileExists(manifestPath)) {
    const manifest = parseYAML(Read(manifestPath))

    // Verify SHA256 hashes
    for (const output of manifest.outputs) {
      const actualHash = computeSHA256(Read(output.path))
      if (actualHash !== output.hash) {
        integrityErrors.push({
          task: result.taskId,
          file: output.path,
          expected: output.hash,
          actual: actualHash
        })
      }
    }
  }
}
```

### Phase 5: Gap Detection
```javascript
// Detect missing deliverables
const gaps = []

for (const task of tasks) {
  if (task.status === "completed") {
    // Check for expected outputs
    const expectedOutputs = getExpectedOutputs(task)
    const actualOutputs = getActualOutputs(task)

    const missing = expectedOutputs.filter(e =>
      !actualOutputs.some(a => a.type === e.type)
    )

    if (missing.length > 0) {
      gaps.push({ taskId: task.id, missing })
    }
  }
}
```

### Phase 6: Report Generation
```javascript
// Generate collection report
const report = `
# Collection Report

## Summary
- Total Tasks: ${tasks.length}
- Completed: ${completed.length}
- In Progress: ${inProgress.length}
- Pending: ${pending.length}

## Completion Status
${completed.map(t => `- [x] Task #${t.id}: ${t.subject}`).join('\n')}
${inProgress.map(t => `- [ ] Task #${t.id}: ${t.subject} (in progress)`).join('\n')}
${pending.map(t => `- [ ] Task #${t.id}: ${t.subject} (pending)`).join('\n')}

## Deliverables
${deliverables.map(d => `- ${d.file}: ${d.type}`).join('\n')}

## Integrity Check
${integrityErrors.length === 0
  ? '- All manifests verified'
  : integrityErrors.map(e => `- ERROR: ${e.file} hash mismatch`).join('\n')
}

## Gaps Detected
${gaps.length === 0
  ? '- No gaps detected'
  : gaps.map(g => `- Task #${g.taskId}: Missing ${g.missing.join(', ')}`).join('\n')
}

## Next Steps
${getNextSteps(completed, pending, gaps)}
`

Write({
  file_path: `.agent/prompts/${workloadSlug}/collection_report.md`,
  content: report
})
```

---

## 5. Output Files

| Output | Path |
|--------|------|
| Collection Report | `.agent/prompts/{slug}/collection_report.md` |
| L1 Summary | Inline in report |
| L2 Details | Per-task summaries in report |
| L3 References | Links to worker output files |

---

## 6. Collection Sources

| Source | Flag | Description |
|--------|------|-------------|
| Tasks | (default) | Native Task System via TaskList |
| Files | (default) | Output files in workload directory |
| Git | `--from-git` | Recent commits in current branch |
| Session | `--from-session` | Session state and context |

---

## 7. Error Handling

| Error | Recovery |
|-------|----------|
| No completed tasks | Show pending tasks, suggest wait |
| Missing outputs | Flag as gap, continue collection |
| Integrity error | Log error, flag in report |
| Workload not found | Use active workload or prompt |

---

## 8. Handoff Contract

```yaml
handoff:
  skill: "collect"
  workload_slug: "{slug}"
  status: "completed"
  report_path: ".agent/prompts/{slug}/collection_report.md"
  next_action:
    skill: "/synthesis"
    arguments: "--workload {slug}"
    required: true
    reason: "Results collected, ready for traceability validation"
```

---

## 9. Version History

| Version | Changes |
|---------|---------|
| 4.0.0 | Deduplicated, V2.1.19 frontmatter, Task API patterns |
| 3.0.0 | Multi-source collection, fallback strategies |
| 2.0.0 | EFL Pattern P1-P6 implementation |
| 1.0.0 | Initial result aggregation |

**End of Skill Documentation**
