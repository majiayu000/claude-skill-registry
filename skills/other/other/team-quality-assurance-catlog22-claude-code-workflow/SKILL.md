---
name: team-quality-assurance
description: Full closed-loop QA combining issue discovery and software testing. Scout -> Strategist -> Generator -> Executor -> Analyst with multi-perspective scanning, progressive test layers, GC loops, and quality scoring. Supports discovery, testing, and full QA modes.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] [--mode=discovery|testing|full] \"task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Quality Assurance

## Usage

```bash
$team-quality-assurance "Full QA for the authentication module"
$team-quality-assurance --mode=discovery "Scan codebase for security and bug issues"
$team-quality-assurance --mode=testing "Test recent changes with progressive coverage"
$team-quality-assurance -c 4 --mode=full "Complete QA cycle with regression scanning"
$team-quality-assurance -y "QA all changed files since last commit"
$team-quality-assurance --continue "qa-auth-module-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session
- `--mode=discovery|testing|full`: Force QA mode (default: auto-detect or full)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Orchestrate multi-agent QA pipeline: scout -> strategist -> generator -> executor -> analyst. Supports three modes: **discovery** (issue scanning), **testing** (progressive test coverage), and **full** (closed-loop QA with regression). Multi-perspective scanning from bug, security, test-coverage, code-quality, and UX viewpoints. Progressive layer coverage (L1/L2/L3) with Generator-Critic loops for coverage convergence.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|              TEAM QUALITY ASSURANCE WORKFLOW                        |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse task description, detect QA mode                       |
|     +- Mode selection (discovery/testing/full)                      |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Select pipeline based on QA mode                             |
|     +- Build dependency chain with appropriate roles                |
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
|     +- Pipeline completion report with quality score                |
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

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, needs iterative fix-verify cycles |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Multi-perspective code scanning (scout) | `csv-wave` |
| Strategy formulation (single-pass analysis) | `csv-wave` |
| Test generation (single-pass code creation) | `csv-wave` |
| Test execution with auto-fix cycle | `interactive` |
| Quality analysis (single-pass report) | `csv-wave` |
| GC loop fix-verify iteration | `interactive` |
| Regression scanning (post-fix) | `csv-wave` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,perspective,layer,coverage_target,deps,context_from,exec_mode,wave,status,findings,issues_found,pass_rate,coverage_achieved,test_files,quality_score,error
"SCOUT-001","Multi-perspective code scan","Scan codebase from bug, security, test-coverage, code-quality perspectives. Produce severity-ranked findings with file:line references.","scout","bug;security;test-coverage;code-quality","","","","","csv-wave","1","pending","","","","","","",""
"QASTRAT-001","Test strategy formulation","Analyze scout findings and code changes. Determine test layers, define coverage targets, generate test strategy document.","strategist","","","","SCOUT-001","SCOUT-001","csv-wave","2","pending","","","","","","",""
"QAGEN-L1-001","Generate L1 unit tests","Generate L1 unit tests based on strategy. Cover priority files, include happy path, edge cases, error handling.","generator","","L1","80","QASTRAT-001","QASTRAT-001","csv-wave","3","pending","","","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN format) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description (self-contained) |
| `role` | Input | Worker role: `scout`, `strategist`, `generator`, `executor`, `analyst` |
| `perspective` | Input | Scan perspectives (semicolon-separated, scout only) |
| `layer` | Input | Test layer: `L1`, `L2`, `L3`, or empty for non-layer tasks |
| `coverage_target` | Input | Target coverage percentage for this layer (empty if N/A) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `issues_found` | Output | Count of issues discovered (scout/analyst) |
| `pass_rate` | Output | Test pass rate as decimal (executor only) |
| `coverage_achieved` | Output | Actual coverage percentage achieved (executor only) |
| `test_files` | Output | Semicolon-separated paths of test files (generator only) |
| `quality_score` | Output | Quality score 0-100 (analyst only) |
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
| `scan/scan-results.json` | Scout output: multi-perspective scan results | Created in scout wave |
| `strategy/test-strategy.md` | Strategist output: test strategy document | Created in strategy wave |
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
+-- scan/                      # Scout output
|   +-- scan-results.json
+-- strategy/                  # Strategist output
|   +-- test-strategy.md
+-- tests/                     # Generator output
|   +-- L1-unit/
|   +-- L2-integration/
|   +-- L3-e2e/
+-- results/                   # Executor output
|   +-- run-L1.json
|   +-- run-L2.json
+-- analysis/                  # Analyst output
|   +-- quality-report.md
+-- wisdom/                    # Cross-task knowledge
|   +-- learnings.md
|   +-- conventions.md
|   +-- decisions.md
|   +-- issues.md
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

// Parse QA mode flag
const modeMatch = $ARGUMENTS.match(/--mode=(\w+)/)
const explicitMode = modeMatch ? modeMatch[1] : null

const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+|--mode=\w+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `qa-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/scan ${sessionFolder}/strategy ${sessionFolder}/tests/L1-unit ${sessionFolder}/tests/L2-integration ${sessionFolder}/tests/L3-e2e ${sessionFolder}/results ${sessionFolder}/analysis ${sessionFolder}/wisdom ${sessionFolder}/interactive`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')

// Initialize wisdom files
Write(`${sessionFolder}/wisdom/learnings.md`, '# Learnings\n')
Write(`${sessionFolder}/wisdom/conventions.md`, '# Conventions\n')
Write(`${sessionFolder}/wisdom/decisions.md`, '# Decisions\n')
Write(`${sessionFolder}/wisdom/issues.md`, '# Issues\n')

// Initialize GC state
Write(`${sessionFolder}/gc-state.json`, JSON.stringify({
  rounds: {}, coverage_history: [], max_rounds_per_layer: 3
}, null, 2))
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse task description, detect QA mode, prepare for decomposition.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/qa-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **QA Mode Selection**:

   | Condition | Mode | Description |
   |-----------|------|-------------|
   | Explicit `--mode=discovery` | discovery | Scout-first: issue discovery then testing |
   | Explicit `--mode=testing` | testing | Skip scout, direct test pipeline |
   | Explicit `--mode=full` | full | Complete QA closed loop + regression scan |
   | Keywords: discovery, scan, issue, audit | discovery | Auto-detected discovery mode |
   | Keywords: test, coverage, TDD, verify | testing | Auto-detected testing mode |
   | No explicit flag and no keyword match | full | Default to full QA |

4. **Clarify if ambiguous** (skip if AUTO_YES):
   ```javascript
   AskUserQuestion({
     questions: [{
       question: "Detected QA mode: '" + qaMode + "'. Confirm?",
       header: "QA Mode Selection",
       multiSelect: false,
       options: [
         { label: "Proceed with " + qaMode, description: "Detected mode is appropriate" },
         { label: "Use discovery", description: "Scout-first: scan for issues, then test" },
         { label: "Use testing", description: "Direct testing pipeline (skip scout)" },
         { label: "Use full", description: "Complete QA closed loop with regression" }
       ]
     }]
   })
   ```

5. **Output**: Refined requirement, QA mode, scope

**Success Criteria**:
- QA mode selected
- Refined requirements available for Phase 1 decomposition

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Decompose QA task into dependency-ordered CSV tasks based on selected mode.

**Decomposition Rules**:

1. **Select pipeline based on QA mode**:

   | Mode | Pipeline |
   |------|----------|
   | discovery | SCOUT-001 -> QASTRAT-001 -> QAGEN-001 -> QARUN-001 -> QAANA-001 |
   | testing | QASTRAT-001 -> QAGEN-L1-001 -> QARUN-L1-001 -> QAGEN-L2-001 -> QARUN-L2-001 -> QAANA-001 |
   | full | SCOUT-001 -> QASTRAT-001 -> [QAGEN-L1-001, QAGEN-L2-001] -> [QARUN-L1-001, QARUN-L2-001] -> QAANA-001 -> SCOUT-002 |

2. **Assign roles, layers, perspectives, and coverage targets** per task

3. **Assign exec_mode**:
   - Scout, Strategist, Generator, Analyst tasks: `csv-wave` (single-pass)
   - Executor tasks: `interactive` (iterative fix cycle)

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Multi-perspective scanning (single-pass) | `csv-wave` |
| Strategy analysis (single-pass read + write) | `csv-wave` |
| Test code generation (single-pass write) | `csv-wave` |
| Test execution with fix loop (multi-round) | `interactive` |
| Quality analysis (single-pass read + write) | `csv-wave` |
| Regression scanning (single-pass) | `csv-wave` |

**Wave Computation**: Kahn's BFS topological sort with depth tracking.

**User Validation**: Display task breakdown with wave + exec_mode + role assignment (skip if AUTO_YES).

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
    const instruction = buildQAInstruction(sessionFolder, wave)

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
          issues_found: { type: "string" },
          pass_rate: { type: "string" },
          coverage_achieved: { type: "string" },
          test_files: { type: "string" },
          quality_score: { type: "string" },
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
      gcState.rounds[layer] = rounds + 1
      Write(`${sessionFolder}/gc-state.json`, JSON.stringify(gcState, null, 2))

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

**Objective**: Pipeline completion report with quality score and interactive completion choice.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')

// Quality score from analyst
const analystTask = tasks.find(t => t.role === 'analyst' && t.status === 'completed')
const qualityScore = analystTask?.quality_score || 'N/A'

// Scout issues count
const scoutTasks = tasks.filter(t => t.role === 'scout' && t.status === 'completed')
const totalIssues = scoutTasks.reduce((sum, t) => sum + parseInt(t.issues_found || '0'), 0)

// Coverage summary per layer
const layerSummary = ['L1', 'L2', 'L3'].map(layer => {
  const execTask = tasks.find(t => t.role === 'executor' && t.layer === layer && t.status === 'completed')
  return execTask ? `  ${layer}: ${execTask.coverage_achieved}% coverage, ${execTask.pass_rate} pass rate` : null
}).filter(Boolean).join('\n')

console.log(`
============================================
QA PIPELINE COMPLETE

Quality Score: ${qualityScore}/100
Issues Discovered: ${totalIssues}

Deliverables:
${completed.map(t => `  - ${t.id}: ${t.title} (${t.role})`).join('\n')}

Coverage:
${layerSummary}

Pipeline: ${completed.length}/${tasks.length} tasks
Session: ${sessionFolder}
============================================
`)

if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "Quality Assurance pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, output final summary" },
        { label: "Keep Active", description: "Keep session for follow-up work" },
        { label: "Export Results", description: "Export deliverables to target directory" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Post-wave interactive processing complete
- Quality score and coverage metrics displayed
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
const analystTask = tasks.find(t => t.role === 'analyst' && t.status === 'completed')

let contextMd = `# Team Quality Assurance Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n`
contextMd += `**QA Mode**: ${explicitMode || 'full'}\n`
contextMd += `**Quality Score**: ${analystTask?.quality_score || 'N/A'}/100\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

// Scout findings
const scoutTasks = tasks.filter(t => t.role === 'scout' && t.status === 'completed')
if (scoutTasks.length > 0) {
  contextMd += `## Scout Findings\n\n`
  for (const t of scoutTasks) {
    contextMd += `**${t.title}**: ${t.issues_found || 0} issues found\n${t.findings || ''}\n\n`
  }
}

// Coverage results
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

// Wave execution details
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
- context.md generated with quality score, scout findings, and coverage breakdown
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"SCOUT-001","type":"issue_found","data":{"file":"src/auth.ts","line":42,"severity":"high","perspective":"security","description":"Hardcoded secret key in auth module"}}
{"ts":"2026-03-08T10:05:00Z","worker":"QASTRAT-001","type":"framework_detected","data":{"framework":"vitest","config_file":"vitest.config.ts","test_pattern":"**/*.test.ts"}}
{"ts":"2026-03-08T10:10:00Z","worker":"QAGEN-L1-001","type":"test_generated","data":{"file":"tests/L1-unit/auth.test.ts","source_file":"src/auth.ts","test_count":8}}
{"ts":"2026-03-08T10:15:00Z","worker":"QARUN-L1-001","type":"defect_found","data":{"file":"src/auth.ts","line":42,"pattern":"null_reference","description":"Missing null check on token payload"}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `issue_found` | `{file, line, severity, perspective, description}` | Issue discovered by scout |
| `framework_detected` | `{framework, config_file, test_pattern}` | Test framework identified |
| `test_generated` | `{file, source_file, test_count}` | Test file created |
| `defect_found` | `{file, line, pattern, description}` | Defect pattern discovered during testing |
| `coverage_gap` | `{file, current, target, gap}` | Coverage gap identified |
| `convention_found` | `{pattern, example_file, description}` | Test convention detected |
| `fix_applied` | `{test_file, fix_type, description}` | Test fix during GC loop |
| `quality_metric` | `{dimension, score, details}` | Quality dimension score |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file, data.line}` key (where applicable)

---

## Pipeline Definitions

### Discovery Mode (5 tasks, serial)

```
SCOUT-001 -> QASTRAT-001 -> QAGEN-001 -> QARUN-001 -> QAANA-001
```

| Task ID | Role | Layer | Wave | exec_mode |
|---------|------|-------|------|-----------|
| SCOUT-001 | scout | - | 1 | csv-wave |
| QASTRAT-001 | strategist | - | 2 | csv-wave |
| QAGEN-001 | generator | L1 | 3 | csv-wave |
| QARUN-001 | executor | L1 | 4 | interactive |
| QAANA-001 | analyst | - | 5 | csv-wave |

### Testing Mode (6 tasks, progressive layers)

```
QASTRAT-001 -> QAGEN-L1-001 -> QARUN-L1-001 -> QAGEN-L2-001 -> QARUN-L2-001 -> QAANA-001
```

| Task ID | Role | Layer | Wave | exec_mode |
|---------|------|-------|------|-----------|
| QASTRAT-001 | strategist | - | 1 | csv-wave |
| QAGEN-L1-001 | generator | L1 | 2 | csv-wave |
| QARUN-L1-001 | executor | L1 | 3 | interactive |
| QAGEN-L2-001 | generator | L2 | 4 | csv-wave |
| QARUN-L2-001 | executor | L2 | 5 | interactive |
| QAANA-001 | analyst | - | 6 | csv-wave |

### Full Mode (8 tasks, parallel windows + regression)

```
SCOUT-001 -> QASTRAT-001 -> [QAGEN-L1-001 // QAGEN-L2-001] -> [QARUN-L1-001 // QARUN-L2-001] -> QAANA-001 -> SCOUT-002
```

| Task ID | Role | Layer | Wave | exec_mode |
|---------|------|-------|------|-----------|
| SCOUT-001 | scout | - | 1 | csv-wave |
| QASTRAT-001 | strategist | - | 2 | csv-wave |
| QAGEN-L1-001 | generator | L1 | 3 | csv-wave |
| QAGEN-L2-001 | generator | L2 | 3 | csv-wave |
| QARUN-L1-001 | executor | L1 | 4 | interactive |
| QARUN-L2-001 | executor | L2 | 4 | interactive |
| QAANA-001 | analyst | - | 5 | csv-wave |
| SCOUT-002 | scout | - | 6 | csv-wave |

---

## GC Loop (Generator-Critic)

Generator and executor iterate per test layer until coverage converges:

```
QAGEN -> QARUN -> (if coverage < target) -> GC Loop Handler
                  (if coverage >= target) -> next wave
```

- Max iterations: 3 per layer
- After 3 iterations: accept current coverage with warning
- GC loop runs as interactive agent (gc-loop-handler.md) which internally generates fixes and re-runs tests

---

## Scan Perspectives (Scout)

| Perspective | Focus |
|-------------|-------|
| bug | Logic errors, crash paths, null references |
| security | Vulnerabilities, auth bypass, data exposure |
| test-coverage | Untested code paths, missing assertions |
| code-quality | Anti-patterns, complexity, maintainability |
| ux | User-facing issues, accessibility (optional, when task mentions UX/UI) |

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
| Scout finds no issues | Report clean scan, proceed to testing (skip discovery-specific tasks) |
| GC loop exceeded (3 rounds) | Accept current coverage with warning, proceed to next layer |
| Test framework not detected | Default to Jest patterns |
| Coverage tool unavailable | Degrade to pass rate judgment |
| quality_score < 60 | Report with WARNING, suggest re-run with deeper coverage |
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
9. **Scout Feeds Strategy**: Scout findings flow into strategist via prev_context and discoveries.ndjson
10. **Cleanup Temp Files**: Remove wave-{N}.csv after results are merged
11. **DO NOT STOP**: Continuous execution until all waves complete or all remaining tasks are skipped


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
