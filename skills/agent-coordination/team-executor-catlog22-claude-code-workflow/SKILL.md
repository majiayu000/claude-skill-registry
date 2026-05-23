---
name: team-executor
description: Lightweight session execution skill. Resumes existing team-coordinate sessions for pure execution via worker agents. No analysis, no role generation -- only loads and executes. Session path required.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"--session=<path>\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Executor

## Usage

```bash
$team-executor "--session=.workflow/.team/TC-project-2026-03-08"
$team-executor -c 4 "--session=.workflow/.team/TC-auth-2026-03-07"
$team-executor -y "--session=.workflow/.team/TC-api-2026-03-06"
$team-executor --continue "EX-project-2026-03-08"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing executor session
- `--session=<path>`: Path to team-coordinate session folder (REQUIRED)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Lightweight session execution skill: load team-coordinate session → reconcile state → spawn worker agents → execute → deliver. No analysis, no role generation -- only executes existing sessions.

**Execution Model**: Hybrid — CSV wave pipeline (primary) + individual agent spawn (secondary)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Team Executor WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Session Validation + State Reconciliation                      │
│     ├─ Validate session structure (team-session.json, task-analysis.json)│
│     ├─ Load session state and role specifications                        │
│     ├─ Reconcile with TaskList (bidirectional sync)                      │
│     ├─ Reset interrupted tasks (in_progress → pending)                   │
│     ├─ Detect fast-advance orphans and reset                             │
│     └─ Output: validated session, reconciled state                       │
│                                                                          │
│  Phase 1: Requirement → CSV + Classification                             │
│     ├─ Load task-analysis.json from session                              │
│     ├─ Create tasks from analysis with role assignments                  │
│     ├─ Classify tasks: csv-wave | interactive (from role specs)          │
│     ├─ Compute dependency waves (topological sort → depth grouping)      │
│     ├─ Generate tasks.csv with wave + exec_mode columns                  │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 2: Wave Execution Engine (Extended)                               │
│     ├─ For each wave (1..N):                                             │
│     │   ├─ Execute pre-wave interactive tasks (if any)                   │
│     │   ├─ Build wave CSV (filter csv-wave tasks for this wave)          │
│     │   ├─ Inject previous findings into prev_context column             │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Execute post-wave interactive tasks (if any)                  │
│     │   ├─ Merge all results into master tasks.csv                       │
│     │   └─ Check: any failed? → skip dependents                         │
│     └─ discoveries.ndjson shared across all modes (append-only)          │
│                                                                          │
│  Phase 3: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Display summary: completed/failed/skipped per wave                │
│     └─ Offer: view results | retry failed | done                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Task Classification Rules

Each task is classified by `exec_mode` based on role specification:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | Role has inner_loop=false |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Role has inner_loop=true |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Role inner_loop=false | `csv-wave` |
| Role inner_loop=true | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,deps,context_from,exec_mode,role,wave,status,findings,error
1,Implement auth module,Create authentication module with JWT,,,"csv-wave","implementer",1,pending,"",""
2,Write tests,Write unit tests for auth module,1,1,"csv-wave","tester",2,pending,"",""
3,Review code,Review implementation and tests,2,2,"interactive","reviewer",3,pending,"",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `role` | Input | Role name from session role-specs |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` → `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

Interactive agents are loaded dynamically from session role-specs where `inner_loop=true`.

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding role-spec.md** to reload.

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state — all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 3 |
| `discoveries.ndjson` | Shared exploration board (all agents, both modes) | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 3 |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |
| `agents/registry.json` | Active interactive agent tracking | Updated on spawn/close |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
├── tasks.csv                  # Master state (all tasks, both modes)
├── results.csv                # Final results export
├── discoveries.ndjson         # Shared discovery board (all agents)
├── context.md                 # Human-readable report
├── wave-{N}.csv               # Temporary per-wave input (csv-wave only)
├── interactive/               # Interactive task artifacts
│   ├── {id}-result.json       # Per-task results
│   └── cache-index.json       # Shared exploration cache
└── agents/
    └── registry.json          # Active interactive agent tracking
```

---

## Implementation

### Session Initialization

```javascript
// Parse arguments
const args = parseArguments($ARGUMENTS)
const AUTO_YES = args.yes || args.y || false
const CONCURRENCY = args.concurrency || args.c || 3
const CONTINUE_SESSION = args.continue || null
const SESSION_PATH = args.session || null

// Validate session path
if (!SESSION_PATH) {
  throw new Error("Session required. Usage: --session=<path-to-TC-folder>")
}

// Generate executor session ID
const sessionId = `EX-${extractSessionName(SESSION_PATH)}-${formatDate(new Date(), 'yyyy-MM-dd')}`
const sessionDir = `.workflow/.csv-wave/${sessionId}`

// Create session structure
Bash({ command: `mkdir -p "${sessionDir}/interactive" "${sessionDir}/agents"` })
Write(`${sessionDir}/discoveries.ndjson`, '')
Write(`${sessionDir}/agents/registry.json`, JSON.stringify({ active: [], closed: [] }))
```

---

### Phase 0: Session Validation + State Reconciliation

**Objective**: Validate session structure and reconcile session state with actual task status

**Validation Steps**:

1. Check `--session` provided
2. Validate session structure:
   - Directory exists at path
   - `team-session.json` exists and valid JSON
   - `task-analysis.json` exists and valid JSON
   - `role-specs/` directory has at least one `.md` file
   - Each role in `team-session.json#roles` has corresponding `.md` file in `role-specs/`
3. If validation fails → ERROR with specific reason → STOP

**Reconciliation Steps**:

1. Load team-session.json and task-analysis.json
2. Compare TaskList() with session.completed_tasks, bidirectional sync
3. Reset any in_progress tasks to pending
4. Detect fast-advance orphans (in_progress tasks without matching active_worker + created > 5 minutes) → reset to pending
5. Create missing tasks (if needed) from task-analysis
6. Update session file with reconciled state
7. TeamCreate if team does not exist

**Success Criteria**:
- Session validated, state reconciled, team ready
- All role-specs loaded and validated

---

### Phase 1: Requirement → CSV + Classification

**Objective**: Generate task breakdown from session task-analysis and create master CSV

**Decomposition Rules**:

Load task-analysis.json from session and create tasks with:
- Task ID, title, description from analysis
- Dependencies from analysis
- Role assignment from analysis
- exec_mode classification based on role inner_loop flag

**Classification Rules**:

Read each role-spec file to determine inner_loop flag:
- inner_loop=false → `exec_mode=csv-wave`
- inner_loop=true → `exec_mode=interactive`

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
// Load master CSV
const masterCSV = readCSV(`${sessionDir}/tasks.csv`)
const maxWave = Math.max(...masterCSV.map(t => t.wave))

for (let wave = 1; wave <= maxWave; wave++) {
  // Execute pre-wave interactive tasks
  const preWaveTasks = masterCSV.filter(t =>
    t.wave === wave && t.exec_mode === 'interactive' && t.position === 'pre-wave'
  )
  for (const task of preWaveTasks) {
    const roleSpec = Read(`${SESSION_PATH}/role-specs/${task.role}.md`)
    const agent = spawn_agent({
      message: buildWorkerPrompt(task, roleSpec, sessionDir)
    })
    const result = wait({ ids: [agent], timeout_ms: 600000 })
    close_agent({ id: agent })
    updateTaskStatus(task.id, result)
  }

  // Build wave CSV (csv-wave tasks only)
  const waveTasks = masterCSV.filter(t => t.wave === wave && t.exec_mode === 'csv-wave')
  if (waveTasks.length > 0) {
    // Inject prev_context from context_from tasks
    for (const task of waveTasks) {
      if (task.context_from) {
        const contextIds = task.context_from.split(';')
        const contextFindings = masterCSV
          .filter(t => contextIds.includes(t.id))
          .map(t => `[Task ${t.id}] ${t.findings}`)
          .join('\n\n')
        task.prev_context = contextFindings
      }
    }

    // Write wave CSV
    writeCSV(`${sessionDir}/wave-${wave}.csv`, waveTasks)

    // Execute wave
    spawn_agents_on_csv({
      csv_path: `${sessionDir}/wave-${wave}.csv`,
      instruction_path: `${sessionDir}/instructions/agent-instruction.md`,
      concurrency: CONCURRENCY
    })

    // Merge results back to master
    const waveResults = readCSV(`${sessionDir}/wave-${wave}.csv`)
    for (const result of waveResults) {
      const masterTask = masterCSV.find(t => t.id === result.id)
      Object.assign(masterTask, result)
    }
    writeCSV(`${sessionDir}/tasks.csv`, masterCSV)

    // Cleanup wave CSV
    Bash({ command: `rm "${sessionDir}/wave-${wave}.csv"` })
  }

  // Execute post-wave interactive tasks
  const postWaveTasks = masterCSV.filter(t =>
    t.wave === wave && t.exec_mode === 'interactive' && t.position === 'post-wave'
  )
  for (const task of postWaveTasks) {
    const roleSpec = Read(`${SESSION_PATH}/role-specs/${task.role}.md`)
    const agent = spawn_agent({
      message: buildWorkerPrompt(task, roleSpec, sessionDir)
    })
    const result = wait({ ids: [agent], timeout_ms: 600000 })
    close_agent({ id: agent })
    updateTaskStatus(task.id, result)
  }

  // Check for failures and skip dependents
  const failedTasks = masterCSV.filter(t => t.wave === wave && t.status === 'failed')
  if (failedTasks.length > 0) {
    skipDependents(masterCSV, failedTasks)
  }
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms
- Interactive agent lifecycle tracked in registry.json

---

### Phase 3: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
// Export results.csv
const masterCSV = readCSV(`${sessionDir}/tasks.csv`)
writeCSV(`${sessionDir}/results.csv`, masterCSV)

// Generate context.md
const contextMd = generateContextReport(masterCSV, sessionDir)
Write(`${sessionDir}/context.md`, contextMd)

// Cleanup interactive agents
const registry = JSON.parse(Read(`${sessionDir}/agents/registry.json`))
for (const agent of registry.active) {
  close_agent({ id: agent.id })
}
Write(`${sessionDir}/agents/registry.json`, JSON.stringify({ active: [], closed: registry.closed }))

// Display summary
const summary = {
  total: masterCSV.length,
  completed: masterCSV.filter(t => t.status === 'completed').length,
  failed: masterCSV.filter(t => t.status === 'failed').length,
  skipped: masterCSV.filter(t => t.status === 'skipped').length
}
console.log(`Pipeline complete: ${summary.completed}/${summary.total} tasks completed`)

// Completion action
const action = await AskUserQuestion({
  questions: [{
    question: "Team pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean (Recommended)", description: "Archive session, clean up team" },
      { label: "Keep Active", description: "Keep session for follow-up work" },
      { label: "Export Results", description: "Export deliverables to target directory, then clean" }
    ]
  }]
})

// Handle completion action
if (action === "Archive & Clean") {
  // Update session status, cleanup team
} else if (action === "Keep Active") {
  // Update session status to paused
} else if (action === "Export Results") {
  // Ask for target path, copy artifacts, then archive
}
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- All interactive agents closed (registry.json cleanup)
- Summary displayed to user
- Completion action executed

---

## Shared Discovery Board Protocol

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `implementation` | `file+function` | `{file, function, approach, notes}` | Implementation approach taken |
| `test_result` | `test_name` | `{test_name, status, duration}` | Test execution result |
| `review_comment` | `file+line` | `{file, line, severity, comment}` | Code review comment |
| `pattern` | `pattern_name` | `{pattern, files[], occurrences}` | Code pattern identified |

**Discovery NDJSON Format**:

```jsonl
{"ts":"2026-03-08T14:30:22Z","worker":"1","type":"implementation","data":{"file":"src/auth.ts","function":"login","approach":"JWT-based","notes":"Used bcrypt for password hashing"}}
{"ts":"2026-03-08T14:35:10Z","worker":"2","type":"test_result","data":{"test_name":"auth.login.success","status":"pass","duration":125}}
{"ts":"2026-03-08T14:40:05Z","worker":"3","type":"review_comment","data":{"file":"src/auth.ts","line":42,"severity":"medium","comment":"Consider adding rate limiting"}}
```

> Both csv-wave and interactive agents read/write the same discoveries.ndjson file.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No --session provided | ERROR immediately with usage message |
| Session directory not found | ERROR with path, suggest checking path |
| team-session.json missing | ERROR, session incomplete, suggest re-run team-coordinate |
| task-analysis.json missing | ERROR, session incomplete, suggest re-run team-coordinate |
| No role-specs in session | ERROR, session incomplete, suggest re-run team-coordinate |
| Role-spec file not found | ERROR with expected path |
| capability_gap reported | Warn only, cannot generate new role-specs |
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| Interactive agent failed | Mark as failed, skip dependents |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| Lifecycle leak | Cleanup all active agents via registry.json at end |
| Continue mode: no session found | List available sessions, prompt user to select |
| Completion action fails | Default to Keep Active, log warning |

---

## Core Rules

1. **Start Immediately**: First action is session validation, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when role inner_loop=true
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson — both mechanisms share it
7. **Skip on Failure**: If a dependency failed, skip the dependent task (regardless of mechanism)
8. **Lifecycle Balance**: Every spawn_agent MUST have a matching close_agent (tracked in registry.json)
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
