---
name: team-perf-opt
description: Performance optimization team skill. Profiles application performance, identifies bottlenecks, designs optimization strategies, implements changes, benchmarks improvements, and reviews code quality via CSV wave pipeline with interactive review-fix cycles.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"performance optimization task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Performance Optimization

## Usage

```bash
$team-perf-opt "Optimize API response times for the user dashboard endpoints"
$team-perf-opt -c 4 "Profile and reduce memory usage in the data processing pipeline"
$team-perf-opt -y "Optimize bundle size and rendering performance for the frontend"
$team-perf-opt --continue "perf-optimize-api-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Orchestrate multi-agent performance optimization: profile application, identify bottlenecks, design optimization strategies, implement changes, benchmark improvements, review code quality. The pipeline has five domain roles (profiler, strategist, optimizer, benchmarker, reviewer) mapped to CSV wave stages with an interactive review-fix cycle.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|          TEAM PERFORMANCE OPTIMIZATION WORKFLOW                     |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse user task description                                  |
|     +- Detect scope: specific endpoint vs full app profiling        |
|     +- Clarify ambiguous requirements (AskUserQuestion)             |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Identify performance targets and metrics                     |
|     +- Build 5-stage pipeline (profile->strategize->optimize->      |
|     |  benchmark+review)                                            |
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
|     +- Pipeline completion report with benchmark comparisons        |
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
PROFILE-001  -->  STRATEGY-001 -->  IMPL-001   --> BENCH-001
[profiler]        [strategist]      [optimizer]    [benchmarker]
                                        ^               |
                                        +<-- FIX-001 ---+
                                        |          REVIEW-001
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
| Performance profiling (single-pass) | `csv-wave` |
| Optimization strategy design (single-pass) | `csv-wave` |
| Code optimization implementation | `csv-wave` |
| Benchmark execution (single-pass) | `csv-wave` |
| Code review (single-pass) | `csv-wave` |
| Review-fix cycle (iterative revision) | `interactive` |
| User checkpoint (plan approval) | `interactive` |
| Discussion round (DISCUSS-OPT, DISCUSS-REVIEW) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,bottleneck_type,priority,target_files,deps,context_from,exec_mode,wave,status,findings,verdict,artifacts_produced,error
"PROFILE-001","Profile performance","Profile application performance to identify CPU, memory, I/O, network, and rendering bottlenecks. Produce baseline metrics and ranked report.","profiler","","","","","","csv-wave","1","pending","","","",""
"STRATEGY-001","Design optimization plan","Analyze bottleneck report to design prioritized optimization plan with strategies and expected improvements.","strategist","","","","PROFILE-001","PROFILE-001","csv-wave","2","pending","","","",""
"IMPL-001","Implement optimizations","Implement performance optimization changes following strategy plan in priority order.","optimizer","","","","STRATEGY-001","STRATEGY-001","csv-wave","3","pending","","","",""
"BENCH-001","Benchmark improvements","Run benchmarks comparing before/after optimization metrics. Validate improvements meet plan criteria.","benchmarker","","","","IMPL-001","IMPL-001","csv-wave","4","pending","","PASS","",""
"REVIEW-001","Review optimization code","Review optimization changes for correctness, side effects, regression risks, and best practices.","reviewer","","","","IMPL-001","IMPL-001","csv-wave","4","pending","","APPROVE","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN format) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description (self-contained) |
| `role` | Input | Worker role: profiler, strategist, optimizer, benchmarker, reviewer |
| `bottleneck_type` | Input | Performance bottleneck category: CPU, MEMORY, IO, NETWORK, RENDERING, DATABASE |
| `priority` | Input | P0 (Critical), P1 (High), P2 (Medium), P3 (Low) |
| `target_files` | Input | Semicolon-separated file paths to focus on |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `verdict` | Output | Benchmark/review verdict: PASS, WARN, FAIL, APPROVE, REVISE, REJECT |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Plan Reviewer | agents/plan-reviewer.md | 2.3 (send_input cycle) | Review bottleneck report or optimization plan at user checkpoint | pre-wave |
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
| `task-analysis.json` | Phase 1 output: scope, bottleneck targets, pipeline config | Created in Phase 1 |
| `artifacts/baseline-metrics.json` | Profiler: before-optimization metrics | Created by profiler |
| `artifacts/bottleneck-report.md` | Profiler: ranked bottleneck findings | Created by profiler |
| `artifacts/optimization-plan.md` | Strategist: prioritized optimization plan | Created by strategist |
| `artifacts/benchmark-results.json` | Benchmarker: after-optimization metrics | Created by benchmarker |
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
|   +-- baseline-metrics.json        # Profiler output
|   +-- bottleneck-report.md         # Profiler output
|   +-- optimization-plan.md         # Strategist output
|   +-- benchmark-results.json       # Benchmarker output
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
const sessionId = `perf-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')

// Initialize wisdom
Write(`${sessionFolder}/wisdom/patterns.md`, '# Patterns & Conventions\n')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse user task, detect performance scope, clarify ambiguities, prepare for decomposition.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/perf-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **Identify performance optimization target**:

| Signal | Target |
|--------|--------|
| Specific endpoint/file mentioned | Scoped optimization |
| "slow", "performance", "speed", generic | Full application profiling |
| Specific metric (response time, memory, bundle size) | Targeted metric optimization |
| "frontend", "backend", "CLI" | Platform-specific profiling |

4. **Clarify if ambiguous** (skip if AUTO_YES):
   ```javascript
   AskUserQuestion({
     questions: [{
       question: "Please confirm the performance optimization scope:",
       header: "Performance Scope",
       multiSelect: false,
       options: [
         { label: "Proceed as described", description: "Scope is clear" },
         { label: "Narrow scope", description: "Specify endpoints/modules to focus on" },
         { label: "Add constraints", description: "Target metrics, acceptable trade-offs" }
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

**Objective**: Decompose performance optimization task into the 5-stage pipeline tasks, assign waves, generate tasks.csv.

**Decomposition Rules**:

1. **Stage mapping** -- performance optimization always follows this pipeline:

| Stage | Role | Task Prefix | Wave | Description |
|-------|------|-------------|------|-------------|
| 1 | profiler | PROFILE | 1 | Profile app, identify bottlenecks, produce baseline metrics |
| 2 | strategist | STRATEGY | 2 | Design optimization plan from bottleneck report |
| 3 | optimizer | IMPL | 3 | Implement optimizations per plan priority |
| 4a | benchmarker | BENCH | 4 | Benchmark before/after, validate improvements |
| 4b | reviewer | REVIEW | 4 | Review optimization code for correctness |

2. **Single-pipeline decomposition**: Generate one task per stage with sequential dependencies:
   - PROFILE-001 (wave 1, no deps)
   - STRATEGY-001 (wave 2, deps: PROFILE-001)
   - IMPL-001 (wave 3, deps: STRATEGY-001)
   - BENCH-001 (wave 4, deps: IMPL-001)
   - REVIEW-001 (wave 4, deps: IMPL-001)

3. **Description enrichment**: Each task description must be self-contained with:
   - Clear goal statement
   - Input artifacts to read
   - Output artifacts to produce
   - Success criteria
   - Session folder path

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| PROFILE, STRATEGY, IMPL, BENCH, REVIEW (initial pass) | `csv-wave` |
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
      instruction: perfOptInstruction,  // from instructions/agent-instruction.md
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
  const benchTask = tasks.find(t => t.id.startsWith('BENCH') && t.wave === wave)
  const reviewTask = tasks.find(t => t.id.startsWith('REVIEW') && t.wave === wave)

  if ((benchTask?.verdict === 'FAIL' || reviewTask?.verdict === 'REVISE' || reviewTask?.verdict === 'REJECT')) {
    const fixCycleCount = tasks.filter(t => t.id.startsWith('FIX')).length
    if (fixCycleCount < 3) {
      const fixId = `FIX-${String(fixCycleCount + 1).padStart(3, '0')}`
      const feedback = [benchTask?.error, reviewTask?.findings].filter(Boolean).join('\n')
      tasks.push({
        id: fixId, title: `Fix issues from review/benchmark cycle ${fixCycleCount + 1}`,
        description: `Fix issues found:\n${feedback}`,
        role: 'optimizer', bottleneck_type: '', priority: 'P0', target_files: '',
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

**Objective**: Pipeline completion report with performance improvement metrics and interactive completion choice.

```javascript
// 1. Generate pipeline summary
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')

// 2. Load improvement metrics from benchmark results
let improvements = ''
try {
  const benchmark = JSON.parse(Read(`${sessionFolder}/artifacts/benchmark-results.json`))
  improvements = `Performance Improvements:\n${benchmark.metrics.map(m =>
    `  ${m.name}: ${m.baseline} -> ${m.current} (${m.improvement})`).join('\n')}`
} catch {}

console.log(`
============================================
PERFORMANCE OPTIMIZATION COMPLETE

Deliverables:
  - Baseline Metrics: artifacts/baseline-metrics.json
  - Bottleneck Report: artifacts/bottleneck-report.md
  - Optimization Plan: artifacts/optimization-plan.md
  - Benchmark Results: artifacts/benchmark-results.json
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
      question: "Performance optimization complete. What would you like to do?",
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
let contextMd = `# Performance Optimization Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

contextMd += `## Deliverables\n\n`
contextMd += `| Artifact | Path |\n|----------|------|\n`
contextMd += `| Baseline Metrics | artifacts/baseline-metrics.json |\n`
contextMd += `| Bottleneck Report | artifacts/bottleneck-report.md |\n`
contextMd += `| Optimization Plan | artifacts/optimization-plan.md |\n`
contextMd += `| Benchmark Results | artifacts/benchmark-results.json |\n`
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
{"ts":"2026-03-08T10:00:00Z","worker":"PROFILE-001","type":"bottleneck_found","data":{"type":"CPU","location":"src/services/DataProcessor.ts:145","severity":"Critical","description":"O(n^2) nested loop in processRecords"}}
{"ts":"2026-03-08T10:05:00Z","worker":"IMPL-001","type":"file_modified","data":{"file":"src/services/DataProcessor.ts","change":"Replaced nested loop with Map lookup","lines_added":8}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `bottleneck_found` | `{type, location, severity, description}` | Performance bottleneck identified |
| `hotspot_found` | `{file, function, cpu_pct, description}` | CPU hotspot detected |
| `memory_issue` | `{file, type, size_mb, description}` | Memory leak or bloat found |
| `io_issue` | `{operation, latency_ms, description}` | I/O performance issue |
| `file_modified` | `{file, change, lines_added}` | File change recorded |
| `metric_measured` | `{metric, value, unit, context}` | Performance metric measured |
| `pattern_found` | `{pattern_name, location, description}` | Code pattern identified |
| `artifact_produced` | `{name, path, producer, type}` | Deliverable created |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.location}` or `{type, data.file}` key

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
| Benchmark regression detected | Create FIX task with regression details |
| Profiling tool not available | Fall back to static analysis methods |
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
