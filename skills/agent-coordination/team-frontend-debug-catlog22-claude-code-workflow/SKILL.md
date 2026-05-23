---
name: team-frontend-debug
description: Frontend debugging team using Chrome DevTools MCP. Dual-mode -- feature-list testing or bug-report debugging. Covers reproduction, root cause analysis, code fixes, and verification. CSV wave pipeline with conditional skip and iteration loops.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"feature list or bug description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Frontend Debug Team

## Usage

```bash
$team-frontend-debug "Test features: login, dashboard, user profile at localhost:3000"
$team-frontend-debug "Bug: clicking save button on /settings causes white screen"
$team-frontend-debug -y "Test: 1. User registration 2. Email verification 3. Password reset"
$team-frontend-debug --continue "tfd-login-bug-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 2)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Dual-mode frontend debugging: feature-list testing or bug-report debugging, powered by Chrome DevTools MCP. Roles: tester (test-pipeline), reproducer (debug-pipeline), analyzer, fixer, verifier. Supports conditional skip (all tests pass -> no downstream tasks), iteration loops (analyzer requesting more evidence, verifier triggering re-fix), and Chrome DevTools-based browser interaction.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|              FRONTEND DEBUG WORKFLOW                                |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Input Analysis)                     |
|     +- Parse user input (feature list or bug report)                |
|     +- Detect mode: test-pipeline or debug-pipeline                 |
|     +- Extract: base URL, features/steps, evidence plan             |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Select pipeline (test or debug)                              |
|     +- Build dependency graph from pipeline definition              |
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
|     |   +- Conditional skip: TEST-001 with 0 issues -> done         |
|     |   +- Iteration: ANALYZE needs more evidence -> REPRODUCE-002  |
|     |   +- Re-fix: VERIFY fails -> FIX-002 -> VERIFY-002            |
|     +- discoveries.ndjson shared across all modes (append-only)     |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion Action)                 |
|     +- Pipeline completion report with debug summary                |
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

## Pipeline Modes

| Input Pattern | Pipeline | Flow |
|---------------|----------|------|
| Feature list / function checklist / test items | `test-pipeline` | TEST -> ANALYZE -> FIX -> VERIFY |
| Bug report / error description / crash report | `debug-pipeline` | REPRODUCE -> ANALYZE -> FIX -> VERIFY |

### Pipeline Selection Keywords

| Keywords | Pipeline |
|----------|----------|
| feature, test, list, check, verify functions, validate | `test-pipeline` |
| bug, error, crash, broken, white screen, not working | `debug-pipeline` |
| performance, slow, latency, memory leak | `debug-pipeline` (perf dimension) |
| Ambiguous / unclear | AskUserQuestion to clarify |

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, progress updates, inner loop |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Feature testing with inner loop (tester iterates over features) | `csv-wave` |
| Bug reproduction (single pass) | `csv-wave` |
| Root cause analysis (single pass) | `csv-wave` |
| Code fix implementation | `csv-wave` |
| Fix verification (single pass) | `csv-wave` |
| Conditional skip gate (evaluating TEST results) | `interactive` |
| Pipeline completion action | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,pipeline_mode,base_url,evidence_dimensions,deps,context_from,exec_mode,wave,status,findings,artifacts_produced,issues_count,verdict,error
"TEST-001","Feature testing","PURPOSE: Test all features from list | Success: All features tested with evidence","tester","test-pipeline","http://localhost:3000","screenshot;console;network","","","csv-wave","1","pending","","","","",""
"ANALYZE-001","Root cause analysis","PURPOSE: Analyze discovered issues | Success: RCA for each issue","analyzer","test-pipeline","","console;network","TEST-001","TEST-001","csv-wave","2","pending","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN: TEST, REPRODUCE, ANALYZE, FIX, VERIFY) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description with PURPOSE/TASK/CONTEXT/EXPECTED/CONSTRAINTS |
| `role` | Input | Role name: `tester`, `reproducer`, `analyzer`, `fixer`, `verifier` |
| `pipeline_mode` | Input | Pipeline: `test-pipeline` or `debug-pipeline` |
| `base_url` | Input | Target URL for browser-based tasks (empty for non-browser tasks) |
| `evidence_dimensions` | Input | Semicolon-separated evidence types: `screenshot`, `console`, `network`, `snapshot`, `performance` |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `issues_count` | Output | Number of issues found (tester/analyzer), empty for others |
| `verdict` | Output | Verification verdict: `pass`, `pass_with_warnings`, `fail` (verifier only) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Conditional Skip Gate | agents/conditional-skip-gate.md | 2.3 (send_input cycle) | Evaluate TEST results and skip downstream if no issues | post-wave |
| Iteration Handler | agents/iteration-handler.md | 2.3 (send_input cycle) | Handle analyzer's need_more_evidence request | post-wave |
| Completion Handler | agents/completion-handler.md | 2.3 (send_input cycle) | Handle pipeline completion action (Archive/Keep/Export) | standalone |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding agent.md** to reload.

---

## Chrome DevTools MCP Tools

All browser inspection operations use Chrome DevTools MCP. Tester, reproducer, and verifier are primary consumers. These tools are available to CSV wave agents.

| Tool | Purpose |
|------|---------|
| `mcp__chrome-devtools__navigate_page` | Navigate to target URL |
| `mcp__chrome-devtools__take_screenshot` | Capture visual state |
| `mcp__chrome-devtools__take_snapshot` | Capture DOM/a11y tree |
| `mcp__chrome-devtools__list_console_messages` | Read console logs |
| `mcp__chrome-devtools__get_console_message` | Get specific console message |
| `mcp__chrome-devtools__list_network_requests` | Monitor network activity |
| `mcp__chrome-devtools__get_network_request` | Inspect request/response detail |
| `mcp__chrome-devtools__performance_start_trace` | Start performance recording |
| `mcp__chrome-devtools__performance_stop_trace` | Stop and analyze trace |
| `mcp__chrome-devtools__click` | Simulate user click |
| `mcp__chrome-devtools__fill` | Fill form inputs |
| `mcp__chrome-devtools__hover` | Hover over elements |
| `mcp__chrome-devtools__evaluate_script` | Execute JavaScript in page |
| `mcp__chrome-devtools__wait_for` | Wait for element/text |
| `mcp__chrome-devtools__list_pages` | List open browser tabs |
| `mcp__chrome-devtools__select_page` | Switch active tab |
| `mcp__chrome-devtools__press_key` | Press keyboard keys |

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state -- all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 4 |
| `discoveries.ndjson` | Shared exploration board (all agents, both modes) | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 4 |
| `task-analysis.json` | Phase 0/1 output: mode, features/steps, dimensions | Created in Phase 1 |
| `role-instructions/` | Per-role instruction templates for CSV agents | Created in Phase 1 |
| `artifacts/` | All deliverables: test reports, RCA reports, fix changes, verification reports | Created by agents |
| `evidence/` | Screenshots, snapshots, network logs, performance traces | Created by tester/reproducer/verifier |
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
+-- role-instructions/         # Per-role instruction templates
|   +-- tester.md              # (test-pipeline)
|   +-- reproducer.md          # (debug-pipeline)
|   +-- analyzer.md
|   +-- fixer.md
|   +-- verifier.md
+-- artifacts/                 # All deliverables
|   +-- TEST-001-report.md
|   +-- TEST-001-issues.json
|   +-- ANALYZE-001-rca.md
|   +-- FIX-001-changes.md
|   +-- VERIFY-001-report.md
+-- evidence/                  # Browser evidence
|   +-- F-001-login-before.png
|   +-- F-001-login-after.png
|   +-- before-screenshot.png
|   +-- after-screenshot.png
|   +-- before-snapshot.txt
|   +-- after-snapshot.txt
|   +-- evidence-summary.json
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json
+-- wisdom/                    # Cross-task knowledge
    +-- learnings.md
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const continueMode = $ARGUMENTS.includes('--continue')
const concurrencyMatch = $ARGUMENTS.match(/(?:--concurrency|-c)\s+(\d+)/)
const maxConcurrency = concurrencyMatch ? parseInt(concurrencyMatch[1]) : 2

const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `tfd-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts ${sessionFolder}/evidence ${sessionFolder}/role-instructions ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

Write(`${sessionFolder}/discoveries.ndjson`, '')
Write(`${sessionFolder}/wisdom/learnings.md`, '# Debug Learnings\n')
```

---

### Phase 0: Pre-Wave Interactive (Input Analysis)

**Objective**: Parse user input, detect mode (test vs debug), extract parameters.

**Workflow**:

1. **Parse user input** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/tfd-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2

3. **Detect mode**:

   | Input Pattern | Mode |
   |---------------|------|
   | Contains: feature, test, list, check, verify | `test-pipeline` |
   | Contains: bug, error, crash, broken, not working | `debug-pipeline` |
   | Ambiguous | AskUserQuestion to clarify |

4. **Extract parameters by mode**:

   **Test Mode**:
   - `base_url`: URL in text or AskUserQuestion
   - `features`: Parse feature list (bullet points, numbered list, free text)
   - Generate structured feature items with id, name, url

   **Debug Mode**:
   - `bug_description`: Bug description text
   - `target_url`: URL in text or AskUserQuestion
   - `reproduction_steps`: Steps in text or AskUserQuestion
   - `evidence_plan`: Detect dimensions from keywords (UI, network, console, performance)

5. **Dimension Detection** (debug mode):

   | Keywords | Dimension |
   |----------|-----------|
   | render, style, display, layout, CSS | screenshot, snapshot |
   | request, API, network, timeout | network |
   | error, crash, exception | console |
   | slow, performance, lag, memory | performance |
   | interaction, click, input, form | screenshot, console |

**Success Criteria**:
- Mode determined (test-pipeline or debug-pipeline)
- Base URL and features/steps extracted
- Evidence dimensions identified

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Build task dependency graph, generate tasks.csv and per-role instruction templates.

**Decomposition Rules**:

1. **Pipeline Definition**:

   **Test Pipeline** (4 tasks, conditional):
   ```
   TEST-001 -> [issues?] -> ANALYZE-001 -> FIX-001 -> VERIFY-001
                  |
                  +-- no issues -> Pipeline Complete (skip downstream)
   ```

   **Debug Pipeline** (4 tasks, linear with iteration):
   ```
   REPRODUCE-001 -> ANALYZE-001 -> FIX-001 -> VERIFY-001
                         ^                        |
                         |    (if fail)            |
                         +--- REPRODUCE-002 <-----+
   ```

2. **Task Description Template**: Every task uses PURPOSE/TASK/CONTEXT/EXPECTED/CONSTRAINTS format with session path, base URL, and upstream artifact references

3. **Role Instruction Generation**: Write per-role instruction templates to `role-instructions/{role}.md` using the base instruction template customized for each role

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Feature testing (tester with inner loop) | `csv-wave` |
| Bug reproduction (single pass) | `csv-wave` |
| Root cause analysis (single pass) | `csv-wave` |
| Code fix (may need multiple passes) | `csv-wave` |
| Fix verification (single pass) | `csv-wave` |
| All standard pipeline tasks | `csv-wave` |

**Wave Computation**: Kahn's BFS topological sort with depth tracking.

```javascript
// Generate per-role instruction templates
const roles = pipelineMode === 'test-pipeline'
  ? ['tester', 'analyzer', 'fixer', 'verifier']
  : ['reproducer', 'analyzer', 'fixer', 'verifier']

for (const role of roles) {
  const instruction = generateRoleInstruction(role, sessionFolder, pipelineMode)
  Write(`${sessionFolder}/role-instructions/${role}.md`, instruction)
}

const tasks = buildTasksCsv(pipelineMode, requirement, sessionFolder, baseUrl, evidencePlan)
Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))
Write(`${sessionFolder}/task-analysis.json`, JSON.stringify(analysisResult, null, 2))
```

**User Validation**: Display task breakdown (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with valid schema and wave assignments
- Role instruction templates generated
- task-analysis.json written
- No circular dependencies

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with conditional skip, iteration loops, and re-fix cycles.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
let maxWave = Math.max(...tasks.map(t => t.wave))
let fixRound = 0
const MAX_FIX_ROUNDS = 3
const MAX_REPRODUCE_ROUNDS = 2

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\nWave ${wave}/${maxWave}`)

  const waveTasks = tasks.filter(t => t.wave === wave && t.status === 'pending')
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')

  // Check dependencies -- skip tasks whose deps failed
  for (const task of waveTasks) {
    const depIds = (task.deps || '').split(';').filter(Boolean)
    const depStatuses = depIds.map(id => tasks.find(t => t.id === id)?.status)
    if (depStatuses.some(s => s === 'failed' || s === 'skipped')) {
      task.status = 'skipped'
      task.error = `Dependency failed: ${depIds.filter((id, i) =>
        ['failed','skipped'].includes(depStatuses[i])).join(', ')}`
    }
  }

  // Execute pre-wave interactive tasks (if any)
  for (const task of interactiveTasks.filter(t => t.status === 'pending')) {
    // Determine agent file based on task type
    const agentFile = task.id.includes('skip') ? 'agents/conditional-skip-gate.md'
      : task.id.includes('iter') ? 'agents/iteration-handler.md'
      : 'agents/completion-handler.md'

    Read(agentFile)
    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: ${agentFile}\n2. Read: ${sessionFolder}/discoveries.ndjson\n\nGoal: ${task.description}\nSession: ${sessionFolder}\n\n### Previous Context\n${buildPrevContext(task, tasks)}`
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

  // Build prev_context for csv-wave tasks
  const pendingCsvTasks = csvTasks.filter(t => t.status === 'pending')
  for (const task of pendingCsvTasks) {
    task.prev_context = buildPrevContext(task, tasks)
  }

  if (pendingCsvTasks.length > 0) {
    Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingCsvTasks))

    const waveInstruction = buildWaveInstruction(pendingCsvTasks, sessionFolder, wave)

    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: waveInstruction,
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 1200,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          artifacts_produced: { type: "string" },
          issues_count: { type: "string" },
          verdict: { type: "string" },
          error: { type: "string" }
        }
      }
    })

    // Merge results into master CSV
    const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const r of results) {
      const t = tasks.find(t => t.id === r.id)
      if (t) Object.assign(t, r)
    }

    // Conditional Skip: TEST-001 with 0 issues
    const testResult = results.find(r => r.id === 'TEST-001')
    if (testResult && parseInt(testResult.issues_count || '0') === 0) {
      // Skip all downstream tasks
      tasks.filter(t => t.wave > wave && t.status === 'pending').forEach(t => {
        t.status = 'skipped'
        t.error = 'No issues found in testing -- skipped'
      })
      console.log('All features passed. No issues found. Pipeline complete.')
    }

    // Iteration: Analyzer needs more evidence
    const analyzerResult = results.find(r => r.id.startsWith('ANALYZE') && r.findings?.includes('need_more_evidence'))
    if (analyzerResult) {
      const reproduceRound = tasks.filter(t => t.id.startsWith('REPRODUCE')).length
      if (reproduceRound < MAX_REPRODUCE_ROUNDS) {
        const newRepId = `REPRODUCE-${String(reproduceRound + 1).padStart(3, '0')}`
        const newAnalyzeId = `ANALYZE-${String(tasks.filter(t => t.id.startsWith('ANALYZE')).length + 1).padStart(3, '0')}`
        tasks.push({
          id: newRepId, title: 'Supplemental evidence collection',
          description: `PURPOSE: Collect additional evidence per Analyzer request | Success: Targeted evidence collected`,
          role: 'reproducer', pipeline_mode: tasks[0].pipeline_mode,
          base_url: tasks[0].base_url, evidence_dimensions: tasks[0].evidence_dimensions,
          deps: '', context_from: analyzerResult.id,
          exec_mode: 'csv-wave', wave: wave + 1, status: 'pending',
          findings: '', artifacts_produced: '', issues_count: '', verdict: '', error: ''
        })
        tasks.push({
          id: newAnalyzeId, title: 'Re-analysis with supplemental evidence',
          description: `PURPOSE: Re-analyze with additional evidence | Success: Higher-confidence RCA`,
          role: 'analyzer', pipeline_mode: tasks[0].pipeline_mode,
          base_url: '', evidence_dimensions: '',
          deps: newRepId, context_from: `${analyzerResult.id};${newRepId}`,
          exec_mode: 'csv-wave', wave: wave + 2, status: 'pending',
          findings: '', artifacts_produced: '', issues_count: '', verdict: '', error: ''
        })
        // Update FIX task deps
        const fixTask = tasks.find(t => t.id === 'FIX-001' && t.status === 'pending')
        if (fixTask) fixTask.deps = newAnalyzeId
      }
    }

    // Re-fix: Verifier verdict = fail
    const verifyResult = results.find(r => r.id.startsWith('VERIFY') && r.verdict === 'fail')
    if (verifyResult && fixRound < MAX_FIX_ROUNDS) {
      fixRound++
      const newFixId = `FIX-${String(fixRound + 1).padStart(3, '0')}`
      const newVerifyId = `VERIFY-${String(fixRound + 1).padStart(3, '0')}`
      tasks.push({
        id: newFixId, title: `Re-fix (round ${fixRound + 1})`,
        description: `PURPOSE: Re-fix based on verification failure | Success: Issue resolved`,
        role: 'fixer', pipeline_mode: tasks[0].pipeline_mode,
        base_url: '', evidence_dimensions: '',
        deps: verifyResult.id, context_from: verifyResult.id,
        exec_mode: 'csv-wave', wave: wave + 1, status: 'pending',
        findings: '', artifacts_produced: '', issues_count: '', verdict: '', error: ''
      })
      tasks.push({
        id: newVerifyId, title: `Re-verify (round ${fixRound + 1})`,
        description: `PURPOSE: Re-verify after fix | Success: Bug resolved`,
        role: 'verifier', pipeline_mode: tasks[0].pipeline_mode,
        base_url: tasks[0].base_url, evidence_dimensions: tasks[0].evidence_dimensions,
        deps: newFixId, context_from: newFixId,
        exec_mode: 'csv-wave', wave: wave + 2, status: 'pending',
        findings: '', artifacts_produced: '', issues_count: '', verdict: '', error: ''
      })
    }
  }

  // Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // Recalculate maxWave (may have grown from iteration/re-fix)
  maxWave = Math.max(maxWave, ...tasks.map(t => t.wave))

  // Display wave summary
  const completed = waveTasks.filter(t => t.status === 'completed').length
  const failed = waveTasks.filter(t => t.status === 'failed').length
  const skipped = waveTasks.filter(t => t.status === 'skipped').length
  console.log(`Wave ${wave} Complete: ${completed} completed, ${failed} failed, ${skipped} skipped`)
}
```

**Success Criteria**:
- All waves executed in order
- Conditional skip handled (TEST with 0 issues)
- Iteration loops handled (analyzer need_more_evidence)
- Re-fix cycles handled (verifier fail verdict)
- discoveries.ndjson accumulated across all waves
- Max iteration/fix bounds respected

---

### Phase 3: Post-Wave Interactive (Completion Action)

**Objective**: Pipeline completion report with debug summary.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const pipelineMode = tasks[0]?.pipeline_mode

console.log(`
============================================
FRONTEND DEBUG COMPLETE

Pipeline: ${pipelineMode} | ${completed.length}/${tasks.length} tasks
Fix Rounds: ${fixRound}/${MAX_FIX_ROUNDS}
Session: ${sessionFolder}

Results:
${completed.map(t => `  [DONE] ${t.id} (${t.role}): ${t.findings?.substring(0, 80) || 'completed'}`).join('\n')}
============================================
`)

if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "Debug pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, output final summary" },
        { label: "Keep Active", description: "Keep session for follow-up debugging" },
        { label: "Export Results", description: "Export debug report and patches" }
      ]
    }]
  })
}
```

**Success Criteria**:
- User informed of debug pipeline results
- Completion action taken

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
let contextMd = `# Frontend Debug Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Pipeline**: ${tasks[0]?.pipeline_mode}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

const maxWave = Math.max(...tasks.map(t => t.wave))
contextMd += `## Wave Execution\n\n`
for (let w = 1; w <= maxWave; w++) {
  const waveTasks = tasks.filter(t => t.wave === w)
  contextMd += `### Wave ${w}\n\n`
  for (const t of waveTasks) {
    const icon = t.status === 'completed' ? '[DONE]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
    contextMd += `${icon} **${t.title}** [${t.role}]`
    if (t.verdict) contextMd += ` Verdict: ${t.verdict}`
    if (t.issues_count) contextMd += ` Issues: ${t.issues_count}`
    contextMd += ` ${t.findings || ''}\n\n`
  }
}

// Debug-specific sections
const verifyTasks = tasks.filter(t => t.role === 'verifier' && t.verdict)
if (verifyTasks.length > 0) {
  contextMd += `## Verification Results\n\n`
  for (const v of verifyTasks) {
    contextMd += `- **${v.id}**: ${v.verdict}\n`
  }
}

Write(`${sessionFolder}/context.md`, contextMd)
console.log(`Results exported to: ${sessionFolder}/results.csv`)
console.log(`Report generated at: ${sessionFolder}/context.md`)
```

**Success Criteria**:
- results.csv exported
- context.md generated with debug summary
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents share a single `discoveries.ndjson` file.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"TEST-001","type":"feature_tested","data":{"feature":"F-001","name":"Login","result":"fail","issues":2}}
{"ts":"2026-03-08T10:05:00Z","worker":"REPRODUCE-001","type":"bug_reproduced","data":{"url":"/settings","steps":3,"console_errors":2,"network_failures":1}}
{"ts":"2026-03-08T10:10:00Z","worker":"ANALYZE-001","type":"root_cause_found","data":{"category":"TypeError","file":"src/components/Settings.tsx","line":142,"confidence":"high"}}
{"ts":"2026-03-08T10:15:00Z","worker":"FIX-001","type":"file_modified","data":{"file":"src/components/Settings.tsx","change":"Added null check","lines_added":3}}
{"ts":"2026-03-08T10:20:00Z","worker":"VERIFY-001","type":"verification_result","data":{"verdict":"pass","original_error_resolved":true,"new_errors":0}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `feature_tested` | `{feature, name, result, issues}` | Feature test result |
| `bug_reproduced` | `{url, steps, console_errors, network_failures}` | Bug reproduction result |
| `evidence_collected` | `{dimension, file, description}` | Evidence artifact saved |
| `root_cause_found` | `{category, file, line, confidence}` | Root cause identified |
| `file_modified` | `{file, change, lines_added}` | Code fix applied |
| `verification_result` | `{verdict, original_error_resolved, new_errors}` | Fix verification result |
| `issue_found` | `{file, line, severity, description}` | Issue discovered |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file}` key

---

## Conditional Skip Logic

After TEST-001 completes, evaluate issues:

| Condition | Action |
|-----------|--------|
| `issues_count === 0` | Skip ANALYZE/FIX/VERIFY. Pipeline complete with all-pass. |
| Only low-severity warnings | AskUserQuestion: fix warnings or complete |
| High/medium severity issues | Proceed with ANALYZE -> FIX -> VERIFY |

---

## Iteration Rules

| Trigger | Condition | Action | Max |
|---------|-----------|--------|-----|
| Analyzer -> Reproducer | Confidence < 50% | Create REPRODUCE-002 -> ANALYZE-002 | 2 reproduction rounds |
| Verifier -> Fixer | Verdict = fail | Create FIX-002 -> VERIFY-002 | 3 fix rounds |
| Max iterations reached | Round >= max | Report to user for manual intervention | -- |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| All features pass test | Skip downstream tasks, report success |
| Bug not reproducible | Report failure, ask user for more details |
| Browser not available | Report error, suggest manual reproduction steps |
| Analysis inconclusive | Request more evidence via iteration loop |
| Fix introduces regression | Verifier reports fail, dispatch re-fix |
| Max iterations reached | Escalate to user for manual intervention |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when interaction pattern requires it
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If a dependency failed, skip the dependent task
8. **Conditional Skip**: If TEST finds 0 issues, skip all downstream tasks
9. **Iteration Bounds**: Max 2 reproduction rounds, max 3 fix rounds
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
