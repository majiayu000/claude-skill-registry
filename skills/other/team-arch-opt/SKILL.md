---
name: team-arch-opt
description: Architecture optimization team skill. Analyzes codebase architecture, designs refactoring plans, implements changes, validates improvements, and reviews code quality via CSV wave pipeline with interactive review-fix cycles.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"architecture optimization task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Architecture Optimization

## Usage

```bash
$team-arch-opt "Refactor the auth module to reduce coupling and eliminate circular dependencies"
$team-arch-opt -c 4 "Analyze and fix God Classes across the service layer"
$team-arch-opt -y "Remove dead code and clean up barrel exports in src/utils"
$team-arch-opt --continue "tao-refactor-auth-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Orchestrate multi-agent architecture optimization: analyze codebase structure, design refactoring plan, implement changes, validate improvements, review code quality. The pipeline has five domain roles (analyzer, designer, refactorer, validator, reviewer) mapped to CSV wave stages with an interactive review-fix cycle.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|           TEAM ARCHITECTURE OPTIMIZATION WORKFLOW                   |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse user task description                                  |
|     +- Detect scope: targeted module vs full architecture           |
|     +- Clarify ambiguous requirements (AskUserQuestion)             |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Identify architecture issues to target                       |
|     +- Build 5-stage pipeline (analyze->design->refactor->validate  |
|     |  +review)                                                     |
|     +- Classify tasks: csv-wave | interactive (exec_mode)           |
|     +- Compute dependency waves (topological sort)                  |
|     +- Generate tasks.csv with wave + exec_mode columns             |
|     +- User validates task breakdown (skip if -y)                   |
|                                                                     |
|  Phase 2: Wave Execution Engine (Extended)                          |
|     +- For each wave (1..N):                                        |
|     |   +- Execute pre-wave interactive tasks (if any)              |
|     |   +- Build wave CSV (filter csv-wave tasks for this wave)     |
|     |   +- Inject previous findings into prev_context column        |
|     |   +- spawn_agents_on_csv(wave CSV)                            |
|     |   +- Execute post-wave interactive tasks (if any)             |
|     |   +- Merge all results into master tasks.csv                  |
|     |   +- Check: any failed? -> skip dependents                    |
|     +- discoveries.ndjson shared across all modes (append-only)     |
|     +- Review-fix cycle: max 3 iterations per branch               |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion Action)                 |
|     +- Pipeline completion report with improvement metrics          |
|     +- Interactive completion choice (Archive/Keep/Export)           |
|     +- Final aggregation / report                                   |
|                                                                     |
|  Phase 4: Results Aggregation                                       |
|     +- Export final results.csv                                     |
|     +- Generate context.md with all findings                        |
|     +- Display summary: completed/failed/skipped per wave           |
|     +- Offer: view results | retry failed | done                    |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## Pipeline Definition

```
Stage 1           Stage 2           Stage 3           Stage 4
ANALYZE-001  -->  DESIGN-001  -->  REFACTOR-001 --> VALIDATE-001
[analyzer]        [designer]       [refactorer]     [validator]
                                       ^                |
                                       +<-- FIX-001 ----+
                                       |           REVIEW-001
                                       +<-------->  [reviewer]
                                              (max 3 iterations)
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, revision cycles, user checkpoints |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Architecture analysis (single-pass scan) | `csv-wave` |
| Refactoring plan design (single-pass) | `csv-wave` |
| Code refactoring implementation | `csv-wave` |
| Validation (build, test, metrics) | `csv-wave` |
| Code review (single-pass) | `csv-wave` |
| Review-fix cycle (iterative revision) | `interactive` |
| User checkpoint (plan approval) | `interactive` |
| Discussion round (DISCUSS-REFACTOR, DISCUSS-REVIEW) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,issue_type,priority,target_files,deps,context_from,exec_mode,wave,status,findings,verdict,artifacts_produced,error
"ANALYZE-001","Analyze architecture","Analyze codebase architecture to identify structural issues: cycles, coupling, cohesion, God Classes, dead code, API bloat. Produce baseline metrics and ranked report.","analyzer","","","","","","csv-wave","1","pending","","","",""
"DESIGN-001","Design refactoring plan","Analyze architecture report to design prioritized refactoring plan with strategies, expected improvements, and risk assessments.","designer","","","","ANALYZE-001","ANALYZE-001","csv-wave","2","pending","","","",""
"REFACTOR-001","Implement refactorings","Implement architecture refactoring changes following design plan in priority order (P0 first).","refactorer","","","","DESIGN-001","DESIGN-001","csv-wave","3","pending","","","",""
"VALIDATE-001","Validate changes","Validate refactoring: build checks, test suite, dependency metrics, API compatibility.","validator","","","","REFACTOR-001","REFACTOR-001","csv-wave","4","pending","","PASS","",""
"REVIEW-001","Review refactoring code","Review refactoring changes for correctness, patterns, completeness, migration safety, best practices.","reviewer","","","","REFACTOR-001","REFACTOR-001","csv-wave","4","pending","","APPROVE","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN format) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description (self-contained) |
| `role` | Input | Worker role: analyzer, designer, refactorer, validator, reviewer |
| `issue_type` | Input | Architecture issue category: CYCLE, COUPLING, COHESION, GOD_CLASS, DUPLICATION, LAYER_VIOLATION, DEAD_CODE, API_BLOAT |
| `priority` | Input | P0 (Critical), P1 (High), P2 (Medium), P3 (Low) |
| `target_files` | Input | Semicolon-separated file paths to focus on |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `verdict` | Output | Validation/review verdict: PASS, WARN, FAIL, APPROVE, REVISE, REJECT |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Plan Reviewer | agents/plan-reviewer.md | 2.3 (send_input cycle) | Review architecture report or refactoring plan at user checkpoint | pre-wave |
| Fix Cycle Handler | agents/fix-cycle-handler.md | 2.3 (send_input cycle) | Manage review-fix iteration cycle (max 3 rounds) | post-wave |
| Completion Handler | agents/completion-handler.md | 2.3 (send_input cycle) | Handle pipeline completion action (Archive/Keep/Export) | standalone |

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
| `task-analysis.json` | Phase 1 output: scope, issues, pipeline config | Created in Phase 1 |
| `artifacts/architecture-baseline.json` | Analyzer: pre-refactoring metrics | Created by analyzer |
| `artifacts/architecture-report.md` | Analyzer: ranked structural issue findings | Created by analyzer |
| `artifacts/refactoring-plan.md` | Designer: prioritized refactoring plan | Created by designer |
| `artifacts/validation-results.json` | Validator: post-refactoring validation | Created by validator |
| `artifacts/review-report.md` | Reviewer: code review findings | Created by reviewer |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state (all tasks, both modes)
+-- results.csv                # Final results export
+-- discoveries.ndjson         # Shared discovery board (all agents)
+-- context.md                 # Human-readable report
+-- task-analysis.json         # Phase 1 analysis output
+-- wave-{N}.csv               # Temporary per-wave input (csv-wave only)
+-- artifacts/
|   +-- architecture-baseline.json   # Analyzer output
|   +-- architecture-report.md       # Analyzer output
|   +-- refactoring-plan.md          # Designer output
|   +-- validation-results.json      # Validator output
|   +-- review-report.md             # Reviewer output
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json
+-- wisdom/
    +-- patterns.md            # Discovered patterns and conventions
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const continueMode = $ARGUMENTS.includes('--continue')
const concurrencyMatch = $ARGUMENTS.match(/(?:--concurrency|-c)\s+(\d+)/)
const maxConcurrency = concurrencyMatch ? parseInt(concurrencyMatch[1]) : 3

const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `tao-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')

// Initialize wisdom
Write(`${sessionFolder}/wisdom/patterns.md`, '# Patterns & Conventions\n')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse user task, detect architecture scope, clarify ambiguities, prepare for decomposition.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/tao-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **Identify architecture optimization target**:

| Signal | Target |
|--------|--------|
| Specific file/module mentioned | Scoped refactoring |
| "coupling", "dependency", "structure", generic | Full architecture analysis |
| Specific issue (cycles, God Class, duplication) | Targeted issue resolution |

4. **Clarify if ambiguous** (skip if AUTO_YES):
   ```javascript
   AskUserQuestion({
     questions: [{
       question: "Please confirm the architecture optimization scope:",
       header: "Architecture Scope",
       multiSelect: false,
       options: [
         { label: "Proceed as described", description: "Scope is clear" },
         { label: "Narrow scope", description: "Specify modules/files to focus on" },
         { label: "Add constraints", description: "Exclude areas, set priorities" }
       ]
     }]
   })
   ```

5. **Output**: Refined requirement string for Phase 1

**Success Criteria**:
- Refined requirements available for Phase 1 decomposition
- Existing session detected and handled if applicable

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Decompose architecture optimization task into the 5-stage pipeline tasks, assign waves, generate tasks.csv.

**Decomposition Rules**:

1. **Stage mapping** -- architecture optimization always follows this pipeline:

| Stage | Role | Task Prefix | Wave | Description |
|-------|------|-------------|------|-------------|
| 1 | analyzer | ANALYZE | 1 | Scan codebase, identify structural issues, produce baseline metrics |
| 2 | designer | DESIGN | 2 | Design refactoring plan from architecture report |
| 3 | refactorer | REFACTOR | 3 | Implement refactorings per plan priority |
| 4a | validator | VALIDATE | 4 | Validate build, tests, metrics, API compatibility |
| 4b | reviewer | REVIEW | 4 | Review refactoring code for correctness and patterns |

2. **Single-pipeline decomposition**: Generate one task per stage with sequential dependencies:
   - ANALYZE-001 (wave 1, no deps)
   - DESIGN-001 (wave 2, deps: ANALYZE-001)
   - REFACTOR-001 (wave 3, deps: DESIGN-001)
   - VALIDATE-001 (wave 4, deps: REFACTOR-001)
   - REVIEW-001 (wave 4, deps: REFACTOR-001)

3. **Description enrichment**: Each task description must be self-contained with:
   - Clear goal statement
   - Input artifacts to read
   - Output artifacts to produce
   - Success criteria
   - Session folder path

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| ANALYZE, DESIGN, REFACTOR, VALIDATE, REVIEW (initial pass) | `csv-wave` |
| FIX tasks (review-fix cycle) | `interactive` (handled by fix-cycle-handler agent) |

**Wave Computation**: Kahn's BFS topological sort with depth tracking (csv-wave tasks only).

**User Validation**: Display task breakdown with wave + exec_mode assignment (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with valid schema, wave, and exec_mode assignments
- task-analysis.json written with scope and pipeline config
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support and cross-wave context propagation.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
const maxWave = Math.max(...tasks.map(t => t.wave))

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\nWave ${wave}/${maxWave}`)

  // 1. Separate tasks by exec_mode
  const waveTasks = tasks.filter(t => t.wave === wave && t.status === 'pending')
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')

  // 2. Check dependencies -- skip tasks whose deps failed
  for (const task of waveTasks) {
    const depIds = (task.deps || '').split(';').filter(Boolean)
    const depStatuses = depIds.map(id => tasks.find(t => t.id === id)?.status)
    if (depStatuses.some(s => s === 'failed' || s === 'skipped')) {
      task.status = 'skipped'
      task.error = `Dependency failed: ${depIds.filter((id, i) =>
        ['failed','skipped'].includes(depStatuses[i])).join(', ')}`
    }
  }

  // 3. Execute pre-wave interactive tasks (if any)
  for (const task of interactiveTasks.filter(t => t.status === 'pending')) {
    // Determine agent file based on task type
    const agentFile = task.id.startsWith('FIX') ? 'agents/fix-cycle-handler.md' : 'agents/plan-reviewer.md'
    Read(agentFile)

    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: ${agentFile}\n2. Read: ${sessionFolder}/discoveries.ndjson\n3. Read: .workflow/project-tech.json (if exists)\n\n---\n\nGoal: ${task.description}\nScope: ${task.title}\nSession: ${sessionFolder}\n\n### Previous Context\n${buildPrevContext(task, tasks)}`
    })
    const result = wait({ ids: [agent], timeout_ms: 600000 })
    if (result.timed_out) {
      send_input({ id: agent, message: "Please finalize and output current findings." })
      wait({ ids: [agent], timeout_ms: 120000 })
    }
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed", findings: parseFindings(result),
      timestamp: getUtc8ISOString()
    }))
    close_agent({ id: agent })
    task.status = 'completed'
    task.findings = parseFindings(result)
  }

  // 4. Build prev_context for csv-wave tasks
  const pendingCsvTasks = csvTasks.filter(t => t.status === 'pending')
  for (const task of pendingCsvTasks) {
    task.prev_context = buildPrevContext(task, tasks)
  }

  if (pendingCsvTasks.length > 0) {
    // 5. Write wave CSV
    Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingCsvTasks))

    // 6. Determine instruction -- read from instructions/agent-instruction.md
    Read('instructions/agent-instruction.md')

    // 7. Execute wave via spawn_agents_on_csv
    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: archOptInstruction,  // from instructions/agent-instruction.md
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          verdict: { type: "string" },
          artifacts_produced: { type: "string" },
          error: { type: "string" }
        }
      }
    })

    // 8. Merge results into master CSV
    const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const r of results) {
      const t = tasks.find(t => t.id === r.id)
      if (t) Object.assign(t, r)
    }
  }

  // 9. Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 10. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // 11. Post-wave: check for review-fix cycle
  const validateTask = tasks.find(t => t.id.startsWith('VALIDATE') && t.wave === wave)
  const reviewTask = tasks.find(t => t.id.startsWith('REVIEW') && t.wave === wave)

  if ((validateTask?.verdict === 'FAIL' || reviewTask?.verdict === 'REVISE' || reviewTask?.verdict === 'REJECT')) {
    const fixCycleCount = tasks.filter(t => t.id.startsWith('FIX')).length
    if (fixCycleCount < 3) {
      // Create FIX task, add to tasks, re-run refactor -> validate+review cycle
      const fixId = `FIX-${String(fixCycleCount + 1).padStart(3, '0')}`
      const feedback = [validateTask?.error, reviewTask?.findings].filter(Boolean).join('\n')
      tasks.push({
        id: fixId, title: `Fix issues from review/validation cycle ${fixCycleCount + 1}`,
        description: `Fix issues found:\n${feedback}`,
        role: 'refactorer', issue_type: '', priority: 'P0', target_files: '',
        deps: '', context_from: '', exec_mode: 'interactive',
        wave: wave + 1, status: 'pending', findings: '', verdict: '',
        artifacts_produced: '', error: ''
      })
    }
  }

  // 12. Display wave summary
  const completed = waveTasks.filter(t => t.status === 'completed').length
  const failed = waveTasks.filter(t => t.status === 'failed').length
  const skipped = waveTasks.filter(t => t.status === 'skipped').length
  console.log(`Wave ${wave} Complete: ${completed} completed, ${failed} failed, ${skipped} skipped`)
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- Review-fix cycle handled with max 3 iterations
- discoveries.ndjson accumulated across all waves and mechanisms

---

### Phase 3: Post-Wave Interactive (Completion Action)

**Objective**: Pipeline completion report with architecture improvement metrics and interactive completion choice.

```javascript
// 1. Generate pipeline summary
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')

// 2. Load improvement metrics from validation results
let improvements = ''
try {
  const validation = JSON.parse(Read(`${sessionFolder}/artifacts/validation-results.json`))
  improvements = `Architecture Improvements:\n${validation.dimensions.map(d =>
    `  ${d.name}: ${d.baseline} -> ${d.current} (${d.improvement})`).join('\n')}`
} catch {}

console.log(`
============================================
ARCHITECTURE OPTIMIZATION COMPLETE

Deliverables:
  - Architecture Baseline: artifacts/architecture-baseline.json
  - Architecture Report: artifacts/architecture-report.md
  - Refactoring Plan: artifacts/refactoring-plan.md
  - Validation Results: artifacts/validation-results.json
  - Review Report: artifacts/review-report.md

${improvements}

Pipeline: ${completed.length}/${tasks.length} tasks
Session: ${sessionFolder}
============================================
`)

// 3. Completion action
if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "Architecture optimization complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, output final summary" },
        { label: "Keep Active", description: "Keep session for follow-up work" },
        { label: "Retry Failed", description: "Re-run failed tasks" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Post-wave interactive processing complete
- User informed of results and improvement metrics

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
// 1. Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// 2. Generate context.md
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
let contextMd = `# Architecture Optimization Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

contextMd += `## Deliverables\n\n`
contextMd += `| Artifact | Path |\n|----------|------|\n`
contextMd += `| Architecture Baseline | artifacts/architecture-baseline.json |\n`
contextMd += `| Architecture Report | artifacts/architecture-report.md |\n`
contextMd += `| Refactoring Plan | artifacts/refactoring-plan.md |\n`
contextMd += `| Validation Results | artifacts/validation-results.json |\n`
contextMd += `| Review Report | artifacts/review-report.md |\n\n`

const maxWave = Math.max(...tasks.map(t => t.wave))
contextMd += `## Wave Execution\n\n`
for (let w = 1; w <= maxWave; w++) {
  const waveTasks = tasks.filter(t => t.wave === w)
  contextMd += `### Wave ${w}\n\n`
  for (const t of waveTasks) {
    const icon = t.status === 'completed' ? '[DONE]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
    contextMd += `${icon} **${t.title}** [${t.role}] ${t.verdict ? `(${t.verdict})` : ''} ${t.findings || ''}\n\n`
  }
}

Write(`${sessionFolder}/context.md`, contextMd)

console.log(`Results exported to: ${sessionFolder}/results.csv`)
console.log(`Report generated at: ${sessionFolder}/context.md`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated with deliverables list
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"ANALYZE-001","type":"cycle_found","data":{"modules":["auth","user"],"depth":2,"description":"Circular dependency between auth and user modules"}}
{"ts":"2026-03-08T10:05:00Z","worker":"REFACTOR-001","type":"file_modified","data":{"file":"src/auth/index.ts","change":"Extracted interface to break cycle","lines_added":15}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `cycle_found` | `{modules, depth, description}` | Circular dependency detected |
| `god_class_found` | `{file, loc, methods, description}` | God Class/Module identified |
| `coupling_issue` | `{module, fan_in, fan_out, description}` | High coupling detected |
| `dead_code_found` | `{file, type, description}` | Dead code or dead export found |
| `file_modified` | `{file, change, lines_added}` | File change recorded |
| `pattern_found` | `{pattern_name, location, description}` | Code pattern identified |
| `metric_measured` | `{metric, value, unit, module}` | Architecture metric measured |
| `artifact_produced` | `{name, path, producer, type}` | Deliverable created |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file}` or `{type, data.modules}` key

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency in tasks | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| Interactive agent failed | Mark as failed, skip dependents |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| Review-fix cycle exceeds 3 iterations | Escalate to user with summary of remaining issues |
| Validation fails on build | Create FIX task with compilation error details |
| Architecture baseline unavailable | Fall back to static analysis estimates |
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
8. **Max 3 Fix Cycles**: Review-fix cycle capped at 3 iterations; escalate to user after
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
