---
name: team-lifecycle-v4
description: Full lifecycle team skill — specification, planning, implementation, testing, and review. Supports spec-only, impl-only, full-lifecycle, and frontend pipelines with optional supervisor checkpoints.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Lifecycle v4

## Usage

```bash
$team-lifecycle-v4 "Design and implement a user authentication system"
$team-lifecycle-v4 -c 4 "Full lifecycle: build a REST API for order management"
$team-lifecycle-v4 -y "Implement dark mode toggle in settings page"
$team-lifecycle-v4 --continue "tlv4-auth-system-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session
- `--no-supervision`: Skip CHECKPOINT tasks (supervisor opt-out)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Full lifecycle software development orchestration: requirement analysis, specification writing (product brief, requirements, architecture, epics), quality gating, implementation planning, code implementation, testing, and code review. Supports multiple pipeline modes with optional supervisor checkpoints at phase transition points.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary for supervisor checkpoints and requirement clarification)

```
+-------------------------------------------------------------------------+
|                    TEAM LIFECYCLE v4 WORKFLOW                             |
+--------------------------------------------------------------------------+
|                                                                          |
|  Phase 0: Pre-Wave Interactive                                           |
|     +-- Requirement clarification + pipeline selection                   |
|     +-- Complexity scoring + signal detection                            |
|     +-- Output: refined requirements for decomposition                   |
|                                                                          |
|  Phase 1: Requirement -> CSV + Classification                            |
|     +-- Parse task into lifecycle tasks per selected pipeline             |
|     +-- Assign roles: analyst, writer, planner, executor, tester,        |
|     |   reviewer, supervisor                                             |
|     +-- Classify tasks: csv-wave | interactive (exec_mode)               |
|     +-- Compute dependency waves (topological sort -> depth grouping)    |
|     +-- Generate tasks.csv with wave + exec_mode columns                 |
|     +-- User validates task breakdown (skip if -y)                       |
|                                                                          |
|  Phase 2: Wave Execution Engine (Extended)                               |
|     +-- For each wave (1..N):                                            |
|     |   +-- Execute pre-wave interactive tasks (if any)                  |
|     |   +-- Build wave CSV (filter csv-wave tasks for this wave)         |
|     |   +-- Inject previous findings into prev_context column            |
|     |   +-- spawn_agents_on_csv(wave CSV)                                |
|     |   +-- Execute post-wave interactive tasks (if any)                 |
|     |   +-- Handle CHECKPOINT tasks via interactive supervisor           |
|     |   +-- Merge all results into master tasks.csv                      |
|     |   +-- Check: any failed? -> skip dependents                        |
|     +-- discoveries.ndjson shared across all modes (append-only)         |
|                                                                          |
|  Phase 3: Post-Wave Interactive                                          |
|     +-- Quality gate evaluation (QUALITY-001)                            |
|     +-- User approval checkpoint before implementation                   |
|     +-- Complexity-based implementation routing                          |
|                                                                          |
|  Phase 4: Results Aggregation                                            |
|     +-- Export final results.csv                                         |
|     +-- Generate context.md with all findings                            |
|     +-- Display summary: completed/failed/skipped per wave               |
|     +-- Offer: view results | retry failed | done                        |
|                                                                          |
+--------------------------------------------------------------------------+
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, clarification, checkpoint evaluation |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Research / analysis (RESEARCH-*) | `csv-wave` |
| Document generation (DRAFT-*) | `csv-wave` |
| Implementation planning (PLAN-*) | `csv-wave` |
| Code implementation (IMPL-*) | `csv-wave` |
| Test execution (TEST-*) | `csv-wave` |
| Code review (REVIEW-*) | `csv-wave` |
| Quality gate scoring (QUALITY-*) | `csv-wave` |
| Supervisor checkpoints (CHECKPOINT-*) | `interactive` |
| Requirement clarification (Phase 0) | `interactive` |
| Quality gate user approval | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,pipeline_phase,deps,context_from,exec_mode,wave,status,findings,quality_score,supervision_verdict,error
"RESEARCH-001","Domain research","Explore domain, extract structured context, identify constraints","analyst","research","","","csv-wave","1","pending","","","",""
"DRAFT-001","Product brief","Generate product brief from research context","writer","product-brief","RESEARCH-001","RESEARCH-001","csv-wave","2","pending","","","",""
"CHECKPOINT-001","Brief-PRD consistency","Verify terminology alignment and scope consistency between brief and PRD","supervisor","checkpoint","DRAFT-002","DRAFT-001;DRAFT-002","interactive","4","pending","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `role` | Input | Worker role: analyst, writer, planner, executor, tester, reviewer, supervisor |
| `pipeline_phase` | Input | Lifecycle phase: research, product-brief, requirements, architecture, epics, checkpoint, readiness, planning, implementation, validation, review |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `quality_score` | Output | Quality gate score (0-100) for QUALITY-* tasks |
| `supervision_verdict` | Output | `pass` / `warn` / `block` for CHECKPOINT-* tasks |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| requirement-clarifier | agents/requirement-clarifier.md | 2.3 (wait-respond) | Parse task, detect signals, select pipeline mode | standalone (Phase 0) |
| supervisor | agents/supervisor.md | 2.3 (wait-respond) | Verify cross-artifact consistency at phase transitions | post-wave (after checkpoint dependencies complete) |
| quality-gate | agents/quality-gate.md | 2.3 (wait-respond) | Evaluate quality and present user approval | post-wave (after QUALITY-001 completes) |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding agent.md** to reload.

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state -- all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 4 |
| `discoveries.ndjson` | Shared exploration board (all agents, both modes) | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 4 |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state (all tasks, both modes)
+-- results.csv                # Final results export
+-- discoveries.ndjson         # Shared discovery board (all agents)
+-- context.md                 # Human-readable report
+-- wave-{N}.csv               # Temporary per-wave input (csv-wave only)
+-- spec/                      # Specification artifacts
|   +-- spec-config.json
|   +-- discovery-context.json
|   +-- product-brief.md
|   +-- requirements/
|   +-- architecture.md
|   +-- epics.md
+-- plan/                      # Implementation plan
|   +-- plan.json
|   +-- .task/TASK-*.json
+-- artifacts/                 # Review and checkpoint reports
|   +-- CHECKPOINT-*-report.md
|   +-- review-report.md
+-- wisdom/                    # Cross-task knowledge
+-- explorations/              # Shared exploration cache
+-- interactive/               # Interactive task artifacts
    +-- {id}-result.json
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const continueMode = $ARGUMENTS.includes('--continue')
const noSupervision = $ARGUMENTS.includes('--no-supervision')
const concurrencyMatch = $ARGUMENTS.match(/(?:--concurrency|-c)\s+(\d+)/)
const maxConcurrency = concurrencyMatch ? parseInt(concurrencyMatch[1]) : 3

// Clean requirement text (remove flags)
const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--no-supervision|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
let sessionId = `tlv4-${slug}-${dateStr}`
let sessionFolder = `.workflow/.csv-wave/${sessionId}`

// Continue mode: find existing session
if (continueMode) {
  const existing = Bash(`ls -dt .workflow/.csv-wave/tlv4-* 2>/dev/null | head -1`).trim()
  if (existing) {
    sessionId = existing.split('/').pop()
    sessionFolder = existing
    // Read existing tasks.csv, find incomplete waves, resume from Phase 2
  }
}

Bash(`mkdir -p ${sessionFolder}/{spec,plan,plan/.task,artifacts,wisdom,explorations,interactive}`)
```

---

### Phase 0: Pre-Wave Interactive

**Objective**: Clarify requirement, detect capabilities, select pipeline mode.

**Execution**:

```javascript
const clarifier = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-lifecycle-v4/agents/requirement-clarifier.md (MUST read first)
2. Read: .workflow/project-tech.json (if exists)

---

Goal: Analyze task requirement and select appropriate pipeline
Requirement: ${requirement}

### Task
1. Parse task description for capability signals:
   - spec/design/document/requirements -> spec-only
   - implement/build/fix/code -> impl-only
   - full/lifecycle/end-to-end -> full-lifecycle
   - frontend/UI/react/vue -> fe-only or fullstack
2. Score complexity (per capability +1, cross-domain +2, parallel tracks +1, serial depth >3 +1)
3. Return structured result with pipeline_type, capabilities, complexity
`
})

const clarifierResult = wait({ ids: [clarifier], timeout_ms: 120000 })
if (clarifierResult.timed_out) {
  send_input({ id: clarifier, message: "Please finalize and output current findings." })
  wait({ ids: [clarifier], timeout_ms: 60000 })
}
close_agent({ id: clarifier })

Write(`${sessionFolder}/interactive/requirement-clarifier-result.json`, JSON.stringify({
  task_id: "requirement-clarification",
  status: "completed",
  pipeline_type: parsedPipelineType,
  capabilities: parsedCapabilities,
  complexity: parsedComplexity,
  timestamp: getUtc8ISOString()
}))
```

If not AUTO_YES, confirm pipeline selection:

```javascript
if (!AUTO_YES) {
  const answer = AskUserQuestion({
    questions: [{
      question: `Requirement: "${requirement}"\nDetected pipeline: ${pipeline_type} (complexity: ${complexity.level})\nRoles: ${capabilities.map(c => c.name).join(', ')}\n\nApprove?`,
      header: "Pipeline Selection",
      multiSelect: false,
      options: [
        { label: "Approve", description: `Use ${pipeline_type} pipeline` },
        { label: "Spec Only", description: "Research -> draft specs -> quality gate" },
        { label: "Impl Only", description: "Plan -> implement -> test + review" },
        { label: "Full Lifecycle", description: "Spec pipeline + implementation pipeline" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Refined requirements available for Phase 1 decomposition
- Interactive agents closed, results stored

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Build tasks.csv from selected pipeline mode with proper wave assignments.

**Decomposition Rules**:

| Pipeline | Tasks | Wave Structure |
|----------|-------|---------------|
| spec-only | RESEARCH-001 -> DRAFT-001 -> DRAFT-002 -> [CHECKPOINT-001] -> DRAFT-003 -> DRAFT-004 -> [CHECKPOINT-002] -> QUALITY-001 | 8 waves (6 csv + 2 interactive checkpoints) |
| impl-only | PLAN-001 -> [CHECKPOINT-003] -> IMPL-001 -> TEST-001 + REVIEW-001 | 4 waves (3 csv + 1 interactive) |
| full-lifecycle | spec-only pipeline + impl-only pipeline (PLAN blocked by QUALITY-001) | 12 waves |

**Pipeline Task Definitions**:

#### Spec-Only Pipeline

| Task ID | Role | Wave | Deps | exec_mode | Description |
|---------|------|------|------|-----------|-------------|
| RESEARCH-001 | analyst | 1 | (none) | csv-wave | Research domain, extract structured context |
| DRAFT-001 | writer | 2 | RESEARCH-001 | csv-wave | Generate product brief |
| DRAFT-002 | writer | 3 | DRAFT-001 | csv-wave | Generate requirements PRD |
| CHECKPOINT-001 | supervisor | 4 | DRAFT-002 | interactive | Brief-PRD consistency check |
| DRAFT-003 | writer | 5 | CHECKPOINT-001 | csv-wave | Generate architecture design |
| DRAFT-004 | writer | 6 | DRAFT-003 | csv-wave | Generate epics and stories |
| CHECKPOINT-002 | supervisor | 7 | DRAFT-004 | interactive | Full spec consistency check |
| QUALITY-001 | reviewer | 8 | CHECKPOINT-002 | csv-wave | Quality gate scoring |

#### Impl-Only Pipeline

| Task ID | Role | Wave | Deps | exec_mode | Description |
|---------|------|------|------|-----------|-------------|
| PLAN-001 | planner | 1 | (none) | csv-wave | Break down into implementation steps |
| CHECKPOINT-003 | supervisor | 2 | PLAN-001 | interactive | Plan-input alignment check |
| IMPL-001 | executor | 3 | CHECKPOINT-003 | csv-wave | Execute implementation plan |
| TEST-001 | tester | 4 | IMPL-001 | csv-wave | Run tests, fix failures |
| REVIEW-001 | reviewer | 4 | IMPL-001 | csv-wave | Code review |

When `--no-supervision` is set, skip all CHECKPOINT-* tasks entirely, adjust wave numbers and dependencies accordingly (e.g., DRAFT-003 depends directly on DRAFT-002).

**Classification Rules**:

All lifecycle work tasks (research, drafting, planning, implementation, testing, review, quality) are `csv-wave`. Supervisor checkpoints are `interactive` (post-wave, spawned by orchestrator to verify cross-artifact consistency). Quality gate user approval is `interactive`.

**Wave Computation**: Kahn's BFS topological sort with depth tracking (csv-wave tasks only).

**User Validation**: Display task breakdown with wave + exec_mode assignment (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with valid schema, wave, and exec_mode assignments
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support and cross-wave context propagation.

```javascript
const failedIds = new Set()
const skippedIds = new Set()

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\n## Wave ${wave}/${maxWave}\n`)

  // 1. Read current master CSV
  const masterCsv = parseCsv(Read(`${sessionFolder}/tasks.csv`))

  // 2. Separate csv-wave and interactive tasks for this wave
  const waveTasks = masterCsv.filter(row => parseInt(row.wave) === wave)
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')

  // 3. Skip tasks whose deps failed
  const executableCsvTasks = []
  for (const task of csvTasks) {
    const deps = task.deps.split(';').filter(Boolean)
    if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
      skippedIds.add(task.id)
      updateMasterCsvRow(sessionFolder, task.id, {
        status: 'skipped', error: 'Dependency failed or skipped'
      })
      continue
    }
    executableCsvTasks.push(task)
  }

  // 4. Build prev_context for each csv-wave task
  for (const task of executableCsvTasks) {
    const contextIds = task.context_from.split(';').filter(Boolean)
    const prevFindings = contextIds
      .map(id => {
        const prevRow = masterCsv.find(r => r.id === id)
        if (prevRow && prevRow.status === 'completed' && prevRow.findings) {
          return `[Task ${id}: ${prevRow.title}] ${prevRow.findings}`
        }
        // Check interactive results
        try {
          const interactiveResult = JSON.parse(Read(`${sessionFolder}/interactive/${id}-result.json`))
          return `[Task ${id}] ${JSON.stringify(interactiveResult.key_findings || interactiveResult.findings || '')}`
        } catch { return null }
      })
      .filter(Boolean)
      .join('\n')
    task.prev_context = prevFindings || 'No previous context available'
  }

  // 5. Write wave CSV and execute csv-wave tasks
  if (executableCsvTasks.length > 0) {
    const waveHeader = 'id,title,description,role,pipeline_phase,deps,context_from,exec_mode,wave,prev_context'
    const waveRows = executableCsvTasks.map(t =>
      [t.id, t.title, t.description, t.role, t.pipeline_phase, t.deps, t.context_from, t.exec_mode, t.wave, t.prev_context]
        .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
        .join(',')
    )
    Write(`${sessionFolder}/wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

    const waveResult = spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: Read(`~  or <project>/.codex/skills/team-lifecycle-v4/instructions/agent-instruction.md`)
        .replace(/{session-id}/g, sessionId),
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          quality_score: { type: "string" },
          supervision_verdict: { type: "string" },
          error: { type: "string" }
        },
        required: ["id", "status", "findings"]
      }
    })

    // Merge results into master CSV
    const waveResults = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const result of waveResults) {
      updateMasterCsvRow(sessionFolder, result.id, {
        status: result.status,
        findings: result.findings || '',
        quality_score: result.quality_score || '',
        supervision_verdict: result.supervision_verdict || '',
        error: result.error || ''
      })
      if (result.status === 'failed') failedIds.add(result.id)
    }

    Bash(`rm -f "${sessionFolder}/wave-${wave}.csv"`)
  }

  // 6. Execute post-wave interactive tasks (supervisor checkpoints)
  for (const task of interactiveTasks) {
    if (task.status !== 'pending') continue
    const deps = task.deps.split(';').filter(Boolean)
    if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
      skippedIds.add(task.id)
      continue
    }

    // Spawn supervisor agent for CHECKPOINT tasks
    const supervisorAgent = spawn_agent({
      message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-lifecycle-v4/agents/supervisor.md (MUST read first)
2. Read: ${sessionFolder}/discoveries.ndjson (shared discoveries)

---

Goal: Execute checkpoint verification
Session: ${sessionFolder}
Task ID: ${task.id}
Description: ${task.description}
Scope: ${task.deps}

### Context
Read upstream artifacts and verify cross-artifact consistency.
Produce verdict: pass (score >= 0.8), warn (0.5-0.79), block (< 0.5).
Write report to ${sessionFolder}/artifacts/${task.id}-report.md.
`
    })

    const checkpointResult = wait({ ids: [supervisorAgent], timeout_ms: 300000 })
    if (checkpointResult.timed_out) {
      send_input({ id: supervisorAgent, message: "Please finalize your checkpoint evaluation now." })
      wait({ ids: [supervisorAgent], timeout_ms: 120000 })
    }
    close_agent({ id: supervisorAgent })

    // Parse checkpoint verdict
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed",
      supervision_verdict: parsedVerdict,
      supervision_score: parsedScore,
      timestamp: getUtc8ISOString()
    }))

    // Handle verdict
    if (parsedVerdict === 'block') {
      if (!AUTO_YES) {
        const answer = AskUserQuestion({
          questions: [{
            question: `Checkpoint ${task.id} BLOCKED (score: ${parsedScore}). What to do?`,
            header: "Checkpoint Blocked",
            options: [
              { label: "Override", description: "Proceed despite block" },
              { label: "Revise upstream", description: "Go back and fix issues" },
              { label: "Abort", description: "Stop pipeline" }
            ]
          }]
        })
        // Handle user choice
      }
    }

    updateMasterCsvRow(sessionFolder, task.id, {
      status: 'completed',
      findings: `Checkpoint verdict: ${parsedVerdict} (score: ${parsedScore})`,
      supervision_verdict: parsedVerdict
    })
  }

  // 7. Handle special post-wave logic
  // After QUALITY-001: pause for user approval before implementation
  // After PLAN-001: read complexity for conditional routing
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms
- Supervisor checkpoints evaluated with proper verdict routing

---

### Phase 3: Post-Wave Interactive

**Objective**: Handle quality gate user approval and complexity-based implementation routing.

After QUALITY-001 completes (spec pipelines):
1. Read quality score from QUALITY-001 findings
2. If score >= 80%: present user approval for implementation (if full-lifecycle)
3. If score 60-79%: suggest revisions, offer retry
4. If score < 60%: return to writer for rework

After PLAN-001 completes (impl pipelines):
1. Read plan.json complexity assessment
2. Route by complexity:
   - Low (1-2 modules): direct IMPL-001
   - Medium (3-4 modules): parallel IMPL-{1..N}
   - High (5+ modules): detailed architecture first, then parallel IMPL

**Success Criteria**:
- Post-wave interactive processing complete
- Interactive agents closed, results stored

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
Write(`${sessionFolder}/results.csv`, masterCsv)

const tasks = parseCsv(masterCsv)
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')
const skipped = tasks.filter(t => t.status === 'skipped')

const contextContent = `# Team Lifecycle v4 Report

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Pipeline**: ${pipeline_type}
**Completed**: ${getUtc8ISOString()}

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | ${tasks.length} |
| Completed | ${completed.length} |
| Failed | ${failed.length} |
| Skipped | ${skipped.length} |
| Supervision | ${noSupervision ? 'Disabled' : 'Enabled'} |

---

## Pipeline Execution

${waveDetails}

---

## Deliverables

${deliverablesList}

---

## Quality Gates

${qualityGateResults}

---

## Checkpoint Reports

${checkpointResults}
`

Write(`${sessionFolder}/context.md`, contextContent)
```

If not AUTO_YES, offer completion action:

```javascript
if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "Pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session" },
        { label: "Keep Active", description: "Keep session for follow-up work" },
        { label: "Export Results", description: "Export deliverables to target directory" }
      ]
    }]
  })
}
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- All interactive agents closed
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents across all waves share `discoveries.ndjson`. This enables cross-role knowledge sharing.

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `research` | `data.dimension` | `{dimension, findings[], constraints[], integration_points[]}` | Research findings |
| `spec_artifact` | `data.doc_type` | `{doc_type, path, sections[], key_decisions[]}` | Specification document artifact |
| `exploration` | `data.angle` | `{angle, relevant_files[], patterns[], recommendations[]}` | Codebase exploration finding |
| `plan_task` | `data.task_id` | `{task_id, title, files[], complexity, convergence_criteria[]}` | Implementation task definition |
| `implementation` | `data.task_id` | `{task_id, files_modified[], approach, changes_summary}` | Implementation result |
| `test_result` | `data.framework` | `{framework, pass_rate, failures[], fix_iterations}` | Test execution result |
| `review_finding` | `data.file` | `{file, line, severity, dimension, description, suggested_fix}` | Code review finding |
| `checkpoint` | `data.checkpoint_id` | `{checkpoint_id, verdict, score, risks[], blocks[]}` | Supervisor checkpoint result |
| `quality_gate` | `data.gate_id` | `{gate_id, score, dimensions{}, verdict}` | Quality gate assessment |

**Format**: NDJSON, each line is self-contained JSON:

```jsonl
{"ts":"2026-03-08T10:00:00+08:00","worker":"RESEARCH-001","type":"research","data":{"dimension":"domain","findings":["Auth system needs OAuth2 + RBAC"],"constraints":["Must support SSO"],"integration_points":["User service API"]}}
{"ts":"2026-03-08T10:15:00+08:00","worker":"DRAFT-001","type":"spec_artifact","data":{"doc_type":"product-brief","path":"spec/product-brief.md","sections":["Vision","Problem","Users","Goals"],"key_decisions":["OAuth2 over custom auth"]}}
{"ts":"2026-03-08T11:00:00+08:00","worker":"CHECKPOINT-001","type":"checkpoint","data":{"checkpoint_id":"CHECKPOINT-001","verdict":"pass","score":0.90,"risks":[],"blocks":[]}}
```

**Protocol Rules**:
1. Read board before own work -> leverage existing context
2. Write discoveries immediately via `echo >>` -> don't batch
3. Deduplicate -- check existing entries by type + dedup key
4. Append-only -- never modify or delete existing lines

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| Interactive agent failed | Mark as failed, skip dependents |
| Supervisor checkpoint blocked | AskUserQuestion: Override / Revise / Abort |
| Quality gate failed (< 60%) | Return to writer for rework |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| CLI tool fails | Agent fallback to direct implementation |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when interaction pattern requires it
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson -- both mechanisms share it
7. **Skip on Failure**: If a dependency failed, skip the dependent task (regardless of mechanism)
8. **Lifecycle Balance**: Every spawn_agent MUST have a matching close_agent
9. **Cleanup Temp Files**: Remove wave-{N}.csv after results are merged
10. **DO NOT STOP**: Continuous execution until all waves complete or all remaining tasks are skipped


---

## Coordinator Role Constraints (Main Agent)

**CRITICAL**: The coordinator (main agent executing this skill) is responsible for **orchestration only**, NOT implementation.

15. **Coordinator Does NOT Execute Code**: The main agent MUST NOT write, modify, or implement any code directly. All implementation work is delegated to spawned team agents. The coordinator only:
    - Spawns agents with task assignments
    - Waits for agent callbacks
    - Merges results and coordinates workflow
    - Manages workflow transitions between phases

16. **Patient Waiting is Mandatory**: Agent execution takes significant time (typically 10-30 minutes per phase, sometimes longer). The coordinator MUST:
    - Wait patiently for `wait()` calls to complete
    - NOT skip workflow steps due to perceived delays
    - NOT assume agents have failed just because they're taking time
    - Trust the timeout mechanisms defined in the skill

17. **Use send_input for Clarification**: When agents need guidance or appear stuck, the coordinator MUST:
    - Use `send_input()` to ask questions or provide clarification
    - NOT skip the agent or move to next phase prematurely
    - Give agents opportunity to respond before escalating
    - Example: `send_input({ id: agent_id, message: "Please provide status update or clarify blockers" })`

18. **No Workflow Shortcuts**: The coordinator MUST NOT:
    - Skip phases or stages defined in the workflow
    - Bypass required approval or review steps
    - Execute dependent tasks before prerequisites complete
    - Assume task completion without explicit agent callback
    - Make up or fabricate agent results

19. **Respect Long-Running Processes**: This is a complex multi-agent workflow that requires patience:
    - Total execution time may range from 30-90 minutes or longer
    - Each phase may take 10-30 minutes depending on complexity
    - The coordinator must remain active and attentive throughout the entire process
    - Do not terminate or skip steps due to time concerns
