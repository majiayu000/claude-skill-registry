---
name: team-testing
description: Multi-agent test pipeline with progressive layer coverage (L1/L2/L3), Generator-Critic loops for coverage convergence, and shared defect memory. Strategist -> Generator -> Executor -> Analyst with dynamic pipeline selection.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"task description or scope\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Testing

## Usage

```bash
$team-testing "Generate tests for the authentication module"
$team-testing -c 4 "Progressive testing for recent changes with L1+L2 coverage"
$team-testing -y "Test all changed files since last commit"
$team-testing --continue "tst-auth-module-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Orchestrate multi-agent test pipeline: strategist -> generator -> executor -> analyst. Progressive layer coverage (L1 unit / L2 integration / L3 E2E) with Generator-Critic (GC) loops for coverage convergence. Dynamic pipeline selection based on change scope (targeted / standard / comprehensive).

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|                    TEAM TESTING WORKFLOW                            |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse task description, detect change scope                  |
|     +- Select pipeline (targeted/standard/comprehensive)            |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Analyze git diff for changed files                           |
|     +- Map files to test layers (L1/L2/L3)                         |
|     +- Build dependency chain with GC loop tasks                    |
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
|     |   +- GC Loop Check: coverage < target? -> spawn fix tasks     |
|     |   +- Check: any failed? -> skip dependents                    |
|     +- discoveries.ndjson shared across all modes (append-only)     |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion Action)                 |
|     +- Pipeline completion report with coverage metrics             |
|     +- Interactive completion choice (Archive/Keep/Deepen)          |
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

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, needs iterative fix-verify cycles |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Strategy formulation (single-pass analysis) | `csv-wave` |
| Test generation (single-pass code creation) | `csv-wave` |
| Test execution with auto-fix cycle | `interactive` |
| Quality analysis (single-pass report) | `csv-wave` |
| GC loop fix-verify iteration | `interactive` |
| Coverage gate decision (coordinator) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,layer,coverage_target,deps,context_from,exec_mode,wave,status,findings,pass_rate,coverage_achieved,test_files,error
"STRATEGY-001","Analyze changes and define test strategy","Analyze git diff, detect test framework, determine test layers, define coverage targets, formulate prioritized test strategy","strategist","","","","","csv-wave","1","pending","","","","",""
"TESTGEN-001","Generate L1 unit tests","Generate L1 unit tests for priority files based on test strategy. Follow project test conventions, include happy path, edge cases, error handling","generator","L1","80","STRATEGY-001","STRATEGY-001","csv-wave","2","pending","","","","",""
"TESTRUN-001","Execute L1 tests and collect coverage","Run L1 test suite, collect coverage data, auto-fix failures up to 3 iterations. Report pass rate and coverage percentage","executor","L1","80","TESTGEN-001","TESTGEN-001","interactive","3","pending","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN format) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description (self-contained) |
| `role` | Input | Worker role: `strategist`, `generator`, `executor`, `analyst` |
| `layer` | Input | Test layer: `L1`, `L2`, `L3`, or empty for non-layer tasks |
| `coverage_target` | Input | Target coverage percentage for this layer (empty if N/A) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `pass_rate` | Output | Test pass rate as decimal (e.g., "0.95") |
| `coverage_achieved` | Output | Actual coverage percentage achieved |
| `test_files` | Output | Semicolon-separated paths of test files produced |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Test Executor | agents/executor.md | 2.3 (send_input cycle) | Execute tests with iterative fix cycle, report pass rate and coverage | per-wave |
| GC Loop Handler | agents/gc-loop-handler.md | 2.3 (send_input cycle) | Manage Generator-Critic loop: evaluate coverage, trigger fix rounds | post-wave |

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
| `strategy/test-strategy.md` | Strategist output: test strategy document | Created in wave 1 |
| `tests/L1-unit/` | Generator output: L1 unit test files | Created in L1 wave |
| `tests/L2-integration/` | Generator output: L2 integration test files | Created in L2 wave |
| `tests/L3-e2e/` | Generator output: L3 E2E test files | Created in L3 wave |
| `results/run-{layer}.json` | Executor output: per-layer test results | Created per execution |
| `analysis/quality-report.md` | Analyst output: quality analysis report | Created in final wave |
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
+-- strategy/                  # Strategist output
|   +-- test-strategy.md
+-- tests/                     # Generator output
|   +-- L1-unit/
|   +-- L2-integration/
|   +-- L3-e2e/
+-- results/                   # Executor output
|   +-- run-L1.json
|   +-- run-L2.json
|   +-- run-L3.json
+-- analysis/                  # Analyst output
|   +-- quality-report.md
+-- wisdom/                    # Cross-task knowledge
|   +-- learnings.md
|   +-- conventions.md
|   +-- decisions.md
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json
+-- gc-state.json              # GC loop tracking state
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
const sessionId = `tst-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/strategy ${sessionFolder}/tests/L1-unit ${sessionFolder}/tests/L2-integration ${sessionFolder}/tests/L3-e2e ${sessionFolder}/results ${sessionFolder}/analysis ${sessionFolder}/wisdom ${sessionFolder}/interactive`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')

// Initialize wisdom files
Write(`${sessionFolder}/wisdom/learnings.md`, '# Learnings\n')
Write(`${sessionFolder}/wisdom/conventions.md`, '# Conventions\n')
Write(`${sessionFolder}/wisdom/decisions.md`, '# Decisions\n')

// Initialize GC state
Write(`${sessionFolder}/gc-state.json`, JSON.stringify({
  rounds: {}, coverage_history: [], max_rounds_per_layer: 3
}, null, 2))
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse task description, analyze change scope, select pipeline mode.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/tst-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **Analyze change scope**:
   ```bash
   git diff --name-only HEAD~1 2>/dev/null || git diff --name-only --cached
   ```

4. **Select pipeline**:

   | Condition | Pipeline | Stages |
   |-----------|----------|--------|
   | fileCount <= 3 AND moduleCount <= 1 | targeted | strategy -> gen-L1 -> run-L1 |
   | fileCount <= 10 AND moduleCount <= 3 | standard | strategy -> gen-L1 -> run-L1 -> gen-L2 -> run-L2 -> analysis |
   | Otherwise | comprehensive | strategy -> [gen-L1 // gen-L2] -> [run-L1 // run-L2] -> gen-L3 -> run-L3 -> analysis |

5. **Clarify if ambiguous** (skip if AUTO_YES):
   ```javascript
   AskUserQuestion({
     questions: [{
       question: "Detected scope suggests the '" + pipeline + "' pipeline. Confirm?",
       header: "Pipeline Selection",
       multiSelect: false,
       options: [
         { label: "Proceed with " + pipeline, description: "Detected pipeline is appropriate" },
         { label: "Use targeted", description: "Minimal: L1 only" },
         { label: "Use standard", description: "Progressive: L1 + L2 + analysis" },
         { label: "Use comprehensive", description: "Full: L1 + L2 + L3 + analysis" }
       ]
     }]
   })
   ```

6. **Output**: Refined requirement, pipeline mode, changed file list

**Success Criteria**:
- Pipeline mode selected
- Changed files identified
- Refined requirements available for Phase 1 decomposition

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Decompose testing task into dependency-ordered CSV tasks with wave assignments.

**Decomposition Rules**:

1. **Detect test framework** from project files:

   | Signal File | Framework |
   |-------------|-----------|
   | vitest.config.ts/js | Vitest |
   | jest.config.js/ts | Jest |
   | pytest.ini / pyproject.toml | Pytest |
   | No detection | Default to Jest |

2. **Build pipeline task chain** from selected pipeline:

   | Pipeline | Task Chain |
   |----------|------------|
   | targeted | STRATEGY-001 -> TESTGEN-001 -> TESTRUN-001 |
   | standard | STRATEGY-001 -> TESTGEN-001 -> TESTRUN-001 -> TESTGEN-002 -> TESTRUN-002 -> TESTANA-001 |
   | comprehensive | STRATEGY-001 -> [TESTGEN-001, TESTGEN-002] -> [TESTRUN-001, TESTRUN-002] -> TESTGEN-003 -> TESTRUN-003 -> TESTANA-001 |

3. **Assign roles, layers, and coverage targets** per task

4. **Assign exec_mode**:
   - Strategist, Generator, Analyst tasks: `csv-wave` (single-pass)
   - Executor tasks: `interactive` (iterative fix cycle)

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Strategy analysis (single-pass read + write) | `csv-wave` |
| Test code generation (single-pass write) | `csv-wave` |
| Test execution with fix loop (multi-round) | `interactive` |
| Quality analysis (single-pass read + write) | `csv-wave` |

**Wave Computation**: Kahn's BFS topological sort with depth tracking.

**User Validation**: Display task breakdown with wave + exec_mode + layer assignment (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with valid schema, wave, and exec_mode assignments
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support, GC loop handling, and cross-wave context propagation.

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

  // 3. Execute csv-wave tasks
  const pendingCsvTasks = csvTasks.filter(t => t.status === 'pending')
  if (pendingCsvTasks.length > 0) {
    for (const task of pendingCsvTasks) {
      task.prev_context = buildPrevContext(task, tasks)
    }

    Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingCsvTasks))

    // Read instruction template
    Read(`instructions/agent-instruction.md`)

    // Build instruction with session folder baked in
    const instruction = buildTestingInstruction(sessionFolder, wave)

    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: instruction,
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          pass_rate: { type: "string" },
          coverage_achieved: { type: "string" },
          test_files: { type: "string" },
          error: { type: "string" }
        }
      }
    })

    // Merge results
    const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const r of results) {
      const t = tasks.find(t => t.id === r.id)
      if (t) Object.assign(t, r)
    }
  }

  // 4. Execute interactive tasks (executor with fix cycle)
  const pendingInteractive = interactiveTasks.filter(t => t.status === 'pending')
  for (const task of pendingInteractive) {
    Read(`agents/executor.md`)

    const prevContext = buildPrevContext(task, tasks)
    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: agents/executor.md\n2. Read: ${sessionFolder}/discoveries.ndjson\n3. Read: .workflow/project-tech.json (if exists)\n\n---\n\nGoal: ${task.description}\nLayer: ${task.layer}\nCoverage Target: ${task.coverage_target}%\nSession: ${sessionFolder}\n\n### Previous Context\n${prevContext}`
    })
    const result = wait({ ids: [agent], timeout_ms: 900000 })
    if (result.timed_out) {
      send_input({ id: agent, message: "Please finalize current test results and report." })
      wait({ ids: [agent], timeout_ms: 120000 })
    }
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed", findings: parseFindings(result),
      timestamp: getUtc8ISOString()
    }))
    close_agent({ id: agent })
    task.status = result.success ? 'completed' : 'failed'
    task.findings = parseFindings(result)
  }

  // 5. GC Loop Check (after executor completes)
  for (const task of pendingInteractive.filter(t => t.role === 'executor')) {
    const gcState = JSON.parse(Read(`${sessionFolder}/gc-state.json`))
    const layer = task.layer
    const rounds = gcState.rounds[layer] || 0
    const coverageAchieved = parseFloat(task.coverage_achieved || '0')
    const coverageTarget = parseFloat(task.coverage_target || '80')
    const passRate = parseFloat(task.pass_rate || '0')

    if (coverageAchieved < coverageTarget && passRate < 0.95 && rounds < 3) {
      // Trigger GC fix round
      gcState.rounds[layer] = rounds + 1
      Write(`${sessionFolder}/gc-state.json`, JSON.stringify(gcState, null, 2))

      // Insert fix tasks into tasks array for a subsequent micro-wave
      // TESTGEN-fix task + TESTRUN-fix task
      // These are spawned inline, not added to CSV
      Read(`agents/gc-loop-handler.md`)
      const gcAgent = spawn_agent({
        message: `## GC LOOP ROUND ${rounds + 1}\n\n### MANDATORY FIRST STEPS\n1. Read: agents/gc-loop-handler.md\n2. Read: ${sessionFolder}/discoveries.ndjson\n\nLayer: ${layer}\nRound: ${rounds + 1}/3\nCurrent Coverage: ${coverageAchieved}%\nTarget: ${coverageTarget}%\nPass Rate: ${passRate}\nSession: ${sessionFolder}\nPrevious Results: ${sessionFolder}/results/run-${layer}.json\nTest Directory: ${sessionFolder}/tests/${layer === 'L1' ? 'L1-unit' : layer === 'L2' ? 'L2-integration' : 'L3-e2e'}/`
      })
      const gcResult = wait({ ids: [gcAgent], timeout_ms: 900000 })
      close_agent({ id: gcAgent })
    }
  }

  // 6. Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 7. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // 8. Display wave summary
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
- GC loops triggered when coverage below target (max 3 rounds per layer)
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms

---

### Phase 3: Post-Wave Interactive (Completion Action)

**Objective**: Pipeline completion report with coverage metrics and interactive completion choice.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')
const gcState = JSON.parse(Read(`${sessionFolder}/gc-state.json`))

// Coverage summary per layer
const layerSummary = ['L1', 'L2', 'L3'].map(layer => {
  const execTask = tasks.find(t => t.role === 'executor' && t.layer === layer && t.status === 'completed')
  return execTask ? `  ${layer}: ${execTask.coverage_achieved}% coverage, ${execTask.pass_rate} pass rate` : null
}).filter(Boolean).join('\n')

console.log(`
============================================
TESTING PIPELINE COMPLETE

Deliverables:
${completed.map(t => `  - ${t.id}: ${t.title} (${t.role})`).join('\n')}

Coverage:
${layerSummary}

GC Rounds: ${JSON.stringify(gcState.rounds)}
Pipeline: ${completed.length}/${tasks.length} tasks
Session: ${sessionFolder}
============================================
`)

if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "Testing pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, output final summary" },
        { label: "Keep Active", description: "Keep session for follow-up work" },
        { label: "Deepen Coverage", description: "Add more test layers or increase coverage targets" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Post-wave interactive processing complete
- Coverage metrics displayed
- User informed of results

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
// 1. Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// 2. Generate context.md
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const gcState = JSON.parse(Read(`${sessionFolder}/gc-state.json`))

let contextMd = `# Team Testing Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

contextMd += `## Coverage Results\n\n`
contextMd += `| Layer | Coverage | Target | Pass Rate | GC Rounds |\n`
contextMd += `|-------|----------|--------|-----------|----------|\n`
for (const layer of ['L1', 'L2', 'L3']) {
  const execTask = tasks.find(t => t.role === 'executor' && t.layer === layer)
  if (execTask) {
    contextMd += `| ${layer} | ${execTask.coverage_achieved || 'N/A'}% | ${execTask.coverage_target}% | ${execTask.pass_rate || 'N/A'} | ${gcState.rounds[layer] || 0} |\n`
  }
}
contextMd += '\n'

const maxWave = Math.max(...tasks.map(t => t.wave))
contextMd += `## Wave Execution\n\n`
for (let w = 1; w <= maxWave; w++) {
  const waveTasks = tasks.filter(t => t.wave === w)
  contextMd += `### Wave ${w}\n\n`
  for (const t of waveTasks) {
    const icon = t.status === 'completed' ? '[DONE]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
    contextMd += `${icon} **${t.title}** [${t.role}/${t.layer || '-'}] ${t.findings || ''}\n\n`
  }
}

Write(`${sessionFolder}/context.md`, contextMd)

console.log(`Results exported to: ${sessionFolder}/results.csv`)
console.log(`Report generated at: ${sessionFolder}/context.md`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated with coverage breakdown
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"STRATEGY-001","type":"framework_detected","data":{"framework":"vitest","config_file":"vitest.config.ts","test_pattern":"**/*.test.ts"}}
{"ts":"2026-03-08T10:05:00Z","worker":"TESTGEN-001","type":"test_generated","data":{"file":"tests/L1-unit/auth.test.ts","source_file":"src/auth.ts","test_count":8}}
{"ts":"2026-03-08T10:10:00Z","worker":"TESTRUN-001","type":"defect_found","data":{"file":"src/auth.ts","line":42,"pattern":"null_reference","description":"Missing null check on token payload"}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `framework_detected` | `{framework, config_file, test_pattern}` | Test framework identified |
| `test_generated` | `{file, source_file, test_count}` | Test file created |
| `defect_found` | `{file, line, pattern, description}` | Defect pattern discovered |
| `coverage_gap` | `{file, current, target, gap}` | Coverage gap identified |
| `convention_found` | `{pattern, example_file, description}` | Test convention detected |
| `fix_applied` | `{test_file, fix_type, description}` | Test fix during GC loop |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file}` key

---

## Pipeline Definitions

### Targeted Pipeline (3 tasks, serial)

```
STRATEGY-001 -> TESTGEN-001 -> TESTRUN-001
```

| Task ID | Role | Layer | Wave | exec_mode |
|---------|------|-------|------|-----------|
| STRATEGY-001 | strategist | - | 1 | csv-wave |
| TESTGEN-001 | generator | L1 | 2 | csv-wave |
| TESTRUN-001 | executor | L1 | 3 | interactive |

### Standard Pipeline (6 tasks, progressive layers)

```
STRATEGY-001 -> TESTGEN-001 -> TESTRUN-001 -> TESTGEN-002 -> TESTRUN-002 -> TESTANA-001
```

| Task ID | Role | Layer | Wave | exec_mode |
|---------|------|-------|------|-----------|
| STRATEGY-001 | strategist | - | 1 | csv-wave |
| TESTGEN-001 | generator | L1 | 2 | csv-wave |
| TESTRUN-001 | executor | L1 | 3 | interactive |
| TESTGEN-002 | generator | L2 | 4 | csv-wave |
| TESTRUN-002 | executor | L2 | 5 | interactive |
| TESTANA-001 | analyst | - | 6 | csv-wave |

### Comprehensive Pipeline (8 tasks, parallel windows)

```
STRATEGY-001 -> [TESTGEN-001 // TESTGEN-002] -> [TESTRUN-001 // TESTRUN-002] -> TESTGEN-003 -> TESTRUN-003 -> TESTANA-001
```

| Task ID | Role | Layer | Wave | exec_mode |
|---------|------|-------|------|-----------|
| STRATEGY-001 | strategist | - | 1 | csv-wave |
| TESTGEN-001 | generator | L1 | 2 | csv-wave |
| TESTGEN-002 | generator | L2 | 2 | csv-wave |
| TESTRUN-001 | executor | L1 | 3 | interactive |
| TESTRUN-002 | executor | L2 | 3 | interactive |
| TESTGEN-003 | generator | L3 | 4 | csv-wave |
| TESTRUN-003 | executor | L3 | 5 | interactive |
| TESTANA-001 | analyst | - | 6 | csv-wave |

---

## GC Loop (Generator-Critic)

Generator and executor iterate per test layer until coverage converges:

```
TESTGEN -> TESTRUN -> (if pass_rate < 0.95 OR coverage < target) -> GC Loop Handler
                      (if pass_rate >= 0.95 AND coverage >= target) -> next wave
```

- Max iterations: 3 per layer
- After 3 iterations: accept current coverage with warning
- GC loop runs as interactive agent (gc-loop-handler.md) which internally generates fixes and re-runs tests

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| Interactive agent failed | Mark as failed, skip dependents |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| GC loop exceeded (3 rounds) | Accept current coverage with warning, proceed to next layer |
| Test framework not detected | Default to Jest patterns |
| No changed files found | Use full project scan with user confirmation |
| Coverage tool unavailable | Degrade to pass rate judgment |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when multi-round interaction is required
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If a dependency failed, skip the dependent task
8. **GC Loop Discipline**: Max 3 rounds per layer; never infinite-loop on coverage
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
