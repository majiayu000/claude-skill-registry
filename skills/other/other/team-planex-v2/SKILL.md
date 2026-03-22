---
name: team-planex-v2
description: Hybrid team skill for plan-and-execute pipeline. CSV wave primary for planning and execution. Planner decomposes requirements into issues and solutions, then executor implements each via CLI tools. Supports issue IDs, text input, and plan file input.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] [--exec=codex|gemini] \"issue IDs or --text 'description' or --plan path\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team PlanEx

## Usage

```bash
$team-planex-v2 "ISS-20260308-120000 ISS-20260308-120001"
$team-planex-v2 -c 3 "--text 'Add rate limiting to all API endpoints'"
$team-planex-v2 -y "--plan .workflow/specs/roadmap.md --exec=codex"
$team-planex-v2 --continue "planex-rate-limit-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session
- `--exec=codex|gemini|qwen`: Force execution method for implementation

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Plan-and-execute pipeline for issue-based development. Planner decomposes requirements into individual issues with solution plans, then executors implement each issue independently.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+---------------------------------------------------------------------------+
|                        TEAM PLANEX WORKFLOW                                |
+---------------------------------------------------------------------------+
|                                                                           |
|  Phase 0: Pre-Wave Interactive (Input Analysis)                           |
|     +-- Parse input type (issue IDs / --text / --plan)                    |
|     +-- Determine execution method (codex/gemini/auto)                    |
|     +-- Create issues from text/plan if needed                            |
|     +-- Output: refined issue list for decomposition                      |
|                                                                           |
|  Phase 1: Requirement -> CSV + Classification                             |
|     +-- Planning wave: generate solutions for each issue                  |
|     +-- Execution wave: implement each issue independently                |
|     +-- Classify tasks: csv-wave (default) | interactive                  |
|     +-- Compute dependency waves (topological sort)                       |
|     +-- Generate tasks.csv with wave + exec_mode columns                  |
|     +-- User validates task breakdown (skip if -y)                        |
|                                                                           |
|  Phase 2: Wave Execution Engine (Extended)                                |
|     +-- For each wave (1..N):                                             |
|     |   +-- Build wave CSV (filter csv-wave tasks for this wave)          |
|     |   +-- Inject previous findings into prev_context column             |
|     |   +-- spawn_agents_on_csv(wave CSV)                                 |
|     |   +-- Merge all results into master tasks.csv                       |
|     |   +-- Check: any failed? -> skip dependents                         |
|     +-- discoveries.ndjson shared across all modes (append-only)          |
|                                                                           |
|  Phase 3: Results Aggregation                                             |
|     +-- Export final results.csv                                          |
|     +-- Generate context.md with all findings                             |
|     +-- Display summary: completed/failed/skipped per wave                |
|     +-- Offer: view results | retry failed | done                         |
|                                                                           |
+---------------------------------------------------------------------------+
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, clarification needed |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Solution planning per issue (PLAN-*) | `csv-wave` |
| Code implementation per issue (EXEC-*) | `csv-wave` |
| Complex multi-issue coordination (rare) | `interactive` |

> In the standard PlanEx pipeline, all tasks default to `csv-wave`. Interactive mode is reserved for edge cases requiring multi-round coordination.

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,issue_ids,input_type,raw_input,exec_mode,execution_method,deps,context_from,wave,status,findings,artifact_path,error
"PLAN-001","Plan issue-1","Generate solution for ISS-20260308-120000","planner","ISS-20260308-120000","issues","ISS-20260308-120000","csv-wave","","","","1","pending","","",""
"PLAN-002","Plan issue-2","Generate solution for ISS-20260308-120001","planner","ISS-20260308-120001","issues","ISS-20260308-120001","csv-wave","","","","1","pending","","",""
"EXEC-001","Implement issue-1","Implement solution for ISS-20260308-120000","executor","ISS-20260308-120000","","","csv-wave","gemini","PLAN-001","PLAN-001","2","pending","","",""
"EXEC-002","Implement issue-2","Implement solution for ISS-20260308-120001","executor","ISS-20260308-120001","","","csv-wave","gemini","PLAN-002","PLAN-002","2","pending","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PLAN-NNN, EXEC-NNN) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `role` | Input | Worker role: planner or executor |
| `issue_ids` | Input | Semicolon-separated issue IDs this task covers |
| `input_type` | Input | Input type: issues, text, or plan (planner tasks only) |
| `raw_input` | Input | Raw input text (planner tasks only) |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `execution_method` | Input | codex, gemini, qwen, or empty (executor tasks only) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `artifact_path` | Output | Path to generated artifact (solution file, build result) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state -- all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 3 |
| `discoveries.ndjson` | Shared exploration board (all agents) | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 3 |
| `artifacts/solutions/{issueId}.json` | Planner solution artifacts | Created by planner agents |
| `builds/{issueId}.json` | Executor build results | Created by executor agents |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state (all tasks)
+-- results.csv                # Final results export
+-- discoveries.ndjson         # Shared discovery board
+-- context.md                 # Human-readable report
+-- wave-{N}.csv               # Temporary per-wave input
+-- artifacts/
|   +-- solutions/             # Planner output
|       +-- {issueId}.json
+-- builds/                    # Executor output
|   +-- {issueId}.json
+-- wisdom/                    # Cross-task knowledge
    +-- learnings.md
    +-- decisions.md
    +-- conventions.md
    +-- issues.md
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

// Parse execution method
let executionMethod = 'gemini' // default
const execMatch = requirement.match(/--exec=(\w+)/)
if (execMatch) executionMethod = execMatch[1]

// Detect input type
const issueIdPattern = /ISS-\d{8}-\d{6}/g
const textMatch = requirement.match(/--text\s+'([^']+)'/)
const planMatch = requirement.match(/--plan\s+(\S+)/)

let inputType = 'issues'
let rawInput = requirement
let issueIds = requirement.match(issueIdPattern) || []

if (textMatch) {
  inputType = 'text'
  rawInput = textMatch[1]
  issueIds = [] // will be created by planner
} else if (planMatch) {
  inputType = 'plan'
  rawInput = planMatch[1]
  issueIds = [] // will be parsed from plan file
}

// If no input detected, ask user
if (issueIds.length === 0 && inputType === 'issues') {
  const answer = AskUserQuestion("No input detected. Provide issue IDs, or use --text 'description' or --plan <path>:")
  issueIds = answer.match(issueIdPattern) || []
  if (issueIds.length === 0 && !answer.includes('--text') && !answer.includes('--plan')) {
    inputType = 'text'
    rawInput = answer
  }
}

// Execution method selection (interactive if no flag)
if (!execMatch && !AUTO_YES) {
  const methodChoice = AskUserQuestion({
    questions: [{ question: "Select execution method for implementation:",
      options: [
        { label: "Gemini", description: "gemini-2.5-pro (recommended for <= 3 tasks)" },
        { label: "Codex", description: "gpt-5.2 (recommended for > 3 tasks)" },
        { label: "Auto", description: "Auto-select based on task count" }
      ]
    }]
  })
  if (methodChoice === 'Codex') executionMethod = 'codex'
  else if (methodChoice === 'Auto') executionMethod = 'auto'
}

const slug = (issueIds[0] || rawInput).toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 30)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `planex-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/{artifacts/solutions,builds,wisdom}`)

Write(`${sessionFolder}/discoveries.ndjson`, `# Discovery Board - ${sessionId}\n# Format: NDJSON\n`)

// Initialize wisdom files
Write(`${sessionFolder}/wisdom/learnings.md`, `# Learnings\n\nAccumulated during ${sessionId}\n`)
Write(`${sessionFolder}/wisdom/decisions.md`, `# Decisions\n\n`)
Write(`${sessionFolder}/wisdom/conventions.md`, `# Conventions\n\n`)
Write(`${sessionFolder}/wisdom/issues.md`, `# Issues\n\n`)

// Store session metadata
Write(`${sessionFolder}/session.json`, JSON.stringify({
  session_id: sessionId,
  pipeline_type: 'plan-execute',
  input_type: inputType,
  raw_input: rawInput,
  issue_ids: issueIds,
  execution_method: executionMethod,
  created_at: getUtc8ISOString()
}, null, 2))
```

---

### Phase 0: Pre-Wave Interactive (Input Analysis)

**Objective**: Parse and normalize input into a list of issue IDs ready for the planning wave.

**Input Type Handling**:

| Input Type | Processing |
|------------|-----------|
| `issues` (ISS-* IDs) | Use directly, verify exist via `ccw issue status` |
| `text` (--text flag) | Create issues via `ccw issue create --title ... --context ...` |
| `plan` (--plan flag) | Read plan file, parse phases/tasks, batch create issues |

For `text` input:
```bash
# Create issue from text description
ccw issue create --title "<derived-title>" --context "<raw_input>"
# Parse output for new issue ID
```

For `plan` input:
```bash
# Read plan file
planContent = Read("<plan-path>")
# Parse phases/sections into individual issues
# Create each as a separate issue via ccw issue create
```

After processing, update session.json with resolved issue_ids.

**Success Criteria**:
- All inputs resolved to valid issue IDs
- Session metadata updated with final issue list

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Generate tasks.csv with PLAN-* tasks (wave 1) and EXEC-* tasks (wave 2).

**Two-Wave Structure**:

Wave 1 (Planning): One PLAN-NNN task per issue, all independent (no deps), concurrent execution.
Wave 2 (Execution): One EXEC-NNN task per issue, each depends on its corresponding PLAN-NNN.

**Task Generation**:

```javascript
const tasks = []

// Wave 1: Planning tasks (one per issue)
for (let i = 0; i < issueIds.length; i++) {
  const n = String(i + 1).padStart(3, '0')
  tasks.push({
    id: `PLAN-${n}`,
    title: `Plan ${issueIds[i]}`,
    description: `Generate implementation solution for issue ${issueIds[i]}. Analyze requirements, design solution approach, break down into implementation tasks, identify files to modify/create.`,
    role: 'planner',
    issue_ids: issueIds[i],
    input_type: inputType,
    raw_input: inputType === 'issues' ? issueIds[i] : rawInput,
    exec_mode: 'csv-wave',
    execution_method: '',
    deps: '',
    context_from: '',
    wave: '1',
    status: 'pending',
    findings: '', artifact_path: '', error: ''
  })
}

// Wave 2: Execution tasks (one per issue, depends on corresponding PLAN)
for (let i = 0; i < issueIds.length; i++) {
  const n = String(i + 1).padStart(3, '0')
  // Resolve execution method
  let method = executionMethod
  if (method === 'auto') {
    method = issueIds.length <= 3 ? 'gemini' : 'codex'
  }
  tasks.push({
    id: `EXEC-${n}`,
    title: `Implement ${issueIds[i]}`,
    description: `Implement solution for issue ${issueIds[i]}. Load solution artifact, execute implementation via CLI, run tests, commit.`,
    role: 'executor',
    issue_ids: issueIds[i],
    input_type: '',
    raw_input: '',
    exec_mode: 'csv-wave',
    execution_method: method,
    deps: `PLAN-${n}`,
    context_from: `PLAN-${n}`,
    wave: '2',
    status: 'pending',
    findings: '', artifact_path: '', error: ''
  })
}

Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))
```

**User Validation**: Display task breakdown with wave assignment (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with valid schema and wave assignments
- PLAN-* tasks in wave 1, EXEC-* tasks in wave 2
- Each EXEC-* depends on its corresponding PLAN-*
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with context propagation between planning and execution waves.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
const maxWave = Math.max(...tasks.map(t => parseInt(t.wave)))

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\nWave ${wave}/${maxWave} (${wave === 1 ? 'Planning' : 'Execution'})`)

  // 1. Filter tasks for this wave
  const waveTasks = tasks.filter(t => parseInt(t.wave) === wave && t.status === 'pending')

  // 2. Check dependencies - skip if upstream failed
  for (const task of waveTasks) {
    const depIds = (task.deps || '').split(';').filter(Boolean)
    const depStatuses = depIds.map(id => tasks.find(t => t.id === id)?.status)
    if (depStatuses.some(s => s === 'failed' || s === 'skipped')) {
      task.status = 'skipped'
      task.error = `Dependency failed: ${depIds.filter((id, i) =>
        ['failed','skipped'].includes(depStatuses[i])).join(', ')}`
    }
  }

  const pendingTasks = waveTasks.filter(t => t.status === 'pending')
  if (pendingTasks.length === 0) {
    console.log(`Wave ${wave}: No pending tasks, skipping...`)
    continue
  }

  // 3. Build prev_context from completed upstream tasks
  for (const task of pendingTasks) {
    const contextIds = (task.context_from || '').split(';').filter(Boolean)
    const prevFindings = contextIds.map(id => {
      const src = tasks.find(t => t.id === id)
      if (!src?.findings) return ''
      return `## [${src.id}] ${src.title}\n${src.findings}\nArtifact: ${src.artifact_path || 'N/A'}`
    }).filter(Boolean).join('\n\n')
    task.prev_context = prevFindings
  }

  // 4. Write wave CSV
  Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingTasks))

  // 5. Execute wave
  spawn_agents_on_csv({
    csv_path: `${sessionFolder}/wave-${wave}.csv`,
    id_column: "id",
    instruction: Read("~  or <project>/.codex/skills/team-planex/instructions/agent-instruction.md"),
    max_concurrency: maxConcurrency,
    max_runtime_seconds: 1200,
    output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
    output_schema: {
      type: "object",
      properties: {
        id: { type: "string" },
        status: { type: "string", enum: ["completed", "failed"] },
        findings: { type: "string" },
        artifact_path: { type: "string" },
        error: { type: "string" }
      }
    }
  })

  // 6. Merge results into master CSV
  const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
  for (const r of results) {
    const t = tasks.find(t => t.id === r.id)
    if (t) Object.assign(t, r)
  }
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 7. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // 8. Display wave summary
  const completed = results.filter(r => r.status === 'completed').length
  const failed = results.filter(r => r.status === 'failed').length
  console.log(`Wave ${wave} Complete: ${completed} completed, ${failed} failed`)
}
```

**Success Criteria**:
- All waves executed in order
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves
- Planning wave completes before execution wave starts

---

### Phase 3: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')
const skipped = tasks.filter(t => t.status === 'skipped')

const planTasks = tasks.filter(t => t.role === 'planner')
const execTasks = tasks.filter(t => t.role === 'executor')

// Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// Generate context.md
let contextMd = `# PlanEx Pipeline Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Input Type**: ${inputType}\n`
contextMd += `**Execution Method**: ${executionMethod}\n`
contextMd += `**Issues**: ${issueIds.join(', ')}\n\n`

contextMd += `## Summary\n\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${completed.length} |\n`
contextMd += `| Failed | ${failed.length} |\n`
contextMd += `| Skipped | ${skipped.length} |\n\n`

contextMd += `## Planning Wave\n\n`
for (const t of planTasks) {
  const icon = t.status === 'completed' ? '[OK]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
  contextMd += `${icon} **${t.id}**: ${t.title}\n`
  if (t.findings) contextMd += `   ${t.findings.substring(0, 200)}\n`
  if (t.artifact_path) contextMd += `   Solution: ${t.artifact_path}\n`
  contextMd += `\n`
}

contextMd += `## Execution Wave\n\n`
for (const t of execTasks) {
  const icon = t.status === 'completed' ? '[OK]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
  contextMd += `${icon} **${t.id}**: ${t.title}\n`
  if (t.findings) contextMd += `   ${t.findings.substring(0, 200)}\n`
  if (t.error) contextMd += `   Error: ${t.error}\n`
  contextMd += `\n`
}

contextMd += `## Deliverables\n\n`
contextMd += `| Artifact | Path |\n|----------|------|\n`
contextMd += `| Solution Plans | ${sessionFolder}/artifacts/solutions/ |\n`
contextMd += `| Build Results | ${sessionFolder}/builds/ |\n`
contextMd += `| Discovery Board | ${sessionFolder}/discoveries.ndjson |\n`

Write(`${sessionFolder}/context.md`, contextMd)

// Display summary
console.log(`
PlanEx Pipeline Complete
Input: ${inputType} (${issueIds.length} issues)
Planning: ${planTasks.filter(t => t.status === 'completed').length}/${planTasks.length} completed
Execution: ${execTasks.filter(t => t.status === 'completed').length}/${execTasks.length} completed
Failed: ${failed.length} | Skipped: ${skipped.length}
Output: ${sessionFolder}
`)
```

**Success Criteria**:
- results.csv exported (all tasks)
- context.md generated
- Summary displayed to user

---

## Shared Discovery Board Protocol

Both planner and executor agents share the same discoveries.ndjson file:

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"PLAN-001","type":"solution_designed","data":{"issue_id":"ISS-20260308-120000","approach":"refactor","task_count":4,"estimated_files":6}}
{"ts":"2026-03-08T10:05:00Z","worker":"PLAN-002","type":"conflict_warning","data":{"issue_ids":["ISS-20260308-120000","ISS-20260308-120001"],"overlapping_files":["src/auth/handler.ts"]}}
{"ts":"2026-03-08T10:10:00Z","worker":"EXEC-001","type":"impl_result","data":{"issue_id":"ISS-20260308-120000","files_changed":3,"tests_pass":true,"commit":"abc123"}}
```

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `solution_designed` | `issue_id` | `{issue_id, approach, task_count, estimated_files}` | Planner: solution plan completed |
| `conflict_warning` | `issue_ids` | `{issue_ids, overlapping_files}` | Planner: file overlap detected between issues |
| `pattern_found` | `pattern+location` | `{pattern, location, description}` | Any: code pattern identified |
| `impl_result` | `issue_id` | `{issue_id, files_changed, tests_pass, commit}` | Executor: implementation outcome |
| `test_failure` | `issue_id` | `{issue_id, test_file, error_msg}` | Executor: test failure details |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent EXEC tasks |
| Planner fails to create solution | Mark PLAN task failed, skip corresponding EXEC task |
| Executor fails implementation | Mark as failed, report in context.md |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| No input provided | Ask user for input via AskUserQuestion |
| Issue creation fails (text/plan input) | Report error, suggest manual issue creation |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then input parsing
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state
4. **CSV First**: Default to csv-wave for all tasks; interactive only for edge cases
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If PLAN-N failed, skip EXEC-N automatically
8. **Cleanup Temp Files**: Remove wave-{N}.csv after results are merged
9. **Two-Wave Pipeline**: Wave 1 = Planning (PLAN-*), Wave 2 = Execution (EXEC-*)
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
