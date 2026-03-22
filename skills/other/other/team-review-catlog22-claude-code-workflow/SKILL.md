---
name: team-review
description: Multi-agent code review pipeline with scanner, reviewer, and fixer roles. Executes toolchain + LLM scan, deep analysis with root cause enrichment, and automated fixes with rollback-on-failure.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] [--full|--fix|-q] [--dimensions=sec,cor,prf,mnt] \"target path or pattern\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Review

## Usage

```bash
$team-review "src/auth/**/*.ts"
$team-review -c 2 --full "src/components"
$team-review -y --dimensions=sec,cor "src/api"
$team-review --continue "RV-auth-review-2026-03-08"
$team-review -q "src/utils"
$team-review --fix "src/auth/login.ts"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session
- `--full`: Enable scan + review + fix pipeline
- `--fix`: Fix-only mode (skip scan/review)
- `-q, --quick`: Quick scan only
- `--dimensions=sec,cor,prf,mnt`: Custom dimensions (security, correctness, performance, maintainability)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Orchestrate multi-agent code review with three specialized roles: scanner (toolchain + LLM semantic scan), reviewer (deep analysis with root cause enrichment), and fixer (automated fixes with rollback-on-failure). Supports 4-dimension analysis: security (SEC), correctness (COR), performance (PRF), maintainability (MNT).

**Execution Model**: Hybrid — CSV wave pipeline (primary) + individual agent spawn (secondary)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Team Review WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Pre-Wave Interactive                                           │
│     ├─ Parse arguments and detect pipeline mode                          │
│     ├─ Validate target path and resolve file patterns                    │
│     └─ Output: refined requirements for decomposition                    │
│                                                                          │
│  Phase 1: Requirement → CSV + Classification                             │
│     ├─ Generate task breakdown based on pipeline mode                    │
│     ├─ Create scan/review/fix tasks with dependencies                    │
│     ├─ Classify tasks: csv-wave (scanner, reviewer) | interactive (fixer)│
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
│  Phase 3: Post-Wave Interactive                                          │
│     ├─ Generate final review report and fix summary                      │
│     └─ Final aggregation / report                                        │
│                                                                          │
│  Phase 4: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Display summary: completed/failed/skipped per wave                │
│     └─ Offer: view results | retry failed | done                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, clarification, inline utility |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Scanner task (toolchain + LLM scan) | `csv-wave` |
| Reviewer task (deep analysis) | `csv-wave` |
| Fixer task (code modification with rollback) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,deps,context_from,exec_mode,dimension,target,wave,status,findings,error
1,Scan codebase,Run toolchain + LLM scan on target files,,,"csv-wave","sec,cor,prf,mnt","src/**/*.ts",1,pending,"",""
2,Review findings,Deep analysis with root cause enrichment,1,1,"csv-wave","sec,cor,prf,mnt","scan-results.json",2,pending,"",""
3,Fix issues,Apply fixes with rollback-on-failure,2,2,"interactive","","review-report.json",3,pending,"",""
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
| `dimension` | Input | Review dimensions (sec,cor,prf,mnt) |
| `target` | Input | Target path or pattern |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` → `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| fixer | agents/fixer.md | 2.3 | Apply fixes with rollback-on-failure | post-wave |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding agent.md** to reload.

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state — all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 4 |
| `discoveries.ndjson` | Shared exploration board (all agents, both modes) | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 4 |
| `interactive/fixer-result.json` | Results from fixer task | Created per interactive task |
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
│   ├── fixer-result.json      # Per-task results
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
const MODE = args.full ? 'full' : args.fix ? 'fix-only' : args.quick || args.q ? 'quick' : 'default'
const DIMENSIONS = args.dimensions || 'sec,cor,prf,mnt'
const TARGET = args._[0] || null

// Generate session ID
const sessionId = `RV-${slugify(TARGET || 'review')}-${formatDate(new Date(), 'yyyy-MM-dd')}`
const sessionDir = `.workflow/.csv-wave/${sessionId}`

// Create session structure
Bash({ command: `mkdir -p "${sessionDir}/interactive" "${sessionDir}/agents"` })
Write(`${sessionDir}/discoveries.ndjson`, '')
Write(`${sessionDir}/agents/registry.json`, JSON.stringify({ active: [], closed: [] }))
```

---

### Phase 0: Pre-Wave Interactive

**Objective**: Parse arguments, validate target, detect pipeline mode

**Execution**:

1. Parse command-line arguments for mode flags (--full, --fix, -q)
2. Extract target path/pattern from arguments
3. Validate target exists and resolve to file list
4. Detect pipeline mode based on flags
5. Store configuration in session metadata

**Success Criteria**:
- Refined requirements available for Phase 1 decomposition
- Interactive agents closed, results stored

---

### Phase 1: Requirement → CSV + Classification

**Objective**: Generate task breakdown based on pipeline mode and create master CSV

**Decomposition Rules**:

| Mode | Tasks Generated |
|------|----------------|
| quick | SCAN-001 (quick scan only) |
| default | SCAN-001 → REV-001 |
| full | SCAN-001 → REV-001 → FIX-001 |
| fix-only | FIX-001 (requires existing review report) |

**Classification Rules**:

- Scanner tasks: `exec_mode=csv-wave` (one-shot toolchain + LLM scan)
- Reviewer tasks: `exec_mode=csv-wave` (one-shot deep analysis)
- Fixer tasks: `exec_mode=interactive` (multi-round with rollback)

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
    const agent = spawn_agent({
      message: buildInteractivePrompt(task, sessionDir)
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
    const agent = spawn_agent({
      message: buildInteractivePrompt(task, sessionDir)
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

### Phase 3: Post-Wave Interactive

**Objective**: Generate final review report and fix summary

**Execution**:

1. Aggregate all findings from scan and review tasks
2. Generate comprehensive review report with metrics
3. If fixer ran, generate fix summary with success/failure rates
4. Write final reports to session directory

**Success Criteria**:
- Post-wave interactive processing complete
- Interactive agents closed, results stored

---

### Phase 4: Results Aggregation

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
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- All interactive agents closed (registry.json cleanup)
- Summary displayed to user

---

## Shared Discovery Board Protocol

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `finding` | `file+line+dimension` | `{dimension, file, line, severity, title}` | Code issue discovered by scanner |
| `root_cause` | `finding_id` | `{finding_id, description, related_findings[]}` | Root cause analysis from reviewer |
| `fix_applied` | `file+line` | `{file, line, fix_strategy, status}` | Fix application result from fixer |
| `pattern` | `pattern_name` | `{pattern, files[], occurrences}` | Code pattern identified across files |

**Discovery NDJSON Format**:

```jsonl
{"ts":"2026-03-08T14:30:22Z","worker":"1","type":"finding","data":{"dimension":"sec","file":"src/auth.ts","line":42,"severity":"high","title":"SQL injection vulnerability"}}
{"ts":"2026-03-08T14:35:10Z","worker":"2","type":"root_cause","data":{"finding_id":"SEC-001","description":"Unsanitized user input in query","related_findings":["SEC-002"]}}
{"ts":"2026-03-08T14:40:05Z","worker":"3","type":"fix_applied","data":{"file":"src/auth.ts","line":42,"fix_strategy":"minimal","status":"fixed"}}
```

> Both csv-wave and interactive agents read/write the same discoveries.ndjson file.

---

## Cross-Mechanism Context Bridging

### Interactive Result → CSV Task

When a pre-wave interactive task produces results needed by csv-wave tasks:

```javascript
// 1. Interactive result stored in file
const resultFile = `${sessionDir}/interactive/${taskId}-result.json`

// 2. Wave engine reads when building prev_context for csv-wave tasks
// If a csv-wave task has context_from referencing an interactive task:
//   Read the interactive result file and include in prev_context
```

### CSV Result → Interactive Task

When a post-wave interactive task needs CSV wave results:

```javascript
// Option A: Include in spawn message
const csvFindings = readMasterCSV().filter(t => t.wave === currentWave && t.exec_mode === 'csv-wave')
const context = csvFindings.map(t => `## Task ${t.id}: ${t.title}\n${t.findings}`).join('\n\n')

spawn_agent({
  message: `...\n### Wave ${currentWave} Results\n${context}\n...`
})

// Option B: Inject via send_input (if agent already running)
send_input({
  id: activeAgent,
  message: `## Wave ${currentWave} Results\n${context}\n\nProceed with analysis.`
})
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| Interactive agent failed | Mark as failed, skip dependents |
| Pre-wave interactive failed | Skip dependent csv-wave tasks in same wave |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| Lifecycle leak | Cleanup all active agents via registry.json at end |
| Continue mode: no session found | List available sessions, prompt user to select |
| Target path invalid | AskUserQuestion for corrected path |
| Scanner finds 0 findings | Report clean, skip review + fix stages |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when interaction pattern requires it
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
