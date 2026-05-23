---
name: team-ux-improve
description: Systematic UX improvement pipeline. Discovers and fixes UI/UX interaction issues including unresponsive buttons, missing feedback, and state refresh problems using scan->diagnose->design->implement->test workflow.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"<project-path> [--framework react|vue]\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# UX Improvement Pipeline

## Usage

```bash
$team-ux-improve "ccw/frontend --framework react"
$team-ux-improve -c 4 "src/components"
$team-ux-improve -y "app/ui --framework vue"
$team-ux-improve --continue "ux-improve-1709856000"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 4)
- `--continue`: Resume existing session
- `--framework react|vue`: Specify UI framework (auto-detected if omitted)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Systematic UX improvement workflow that discovers UI/UX interaction issues (unresponsive buttons, missing feedback, state refresh problems) and fixes them methodically. The pipeline scans for issues, diagnoses root causes, designs solutions, implements fixes, and validates with tests.

**Execution Model**: Hybrid — CSV wave pipeline (primary) + individual agent spawn (secondary)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UX IMPROVEMENT PIPELINE WORKFLOW                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Framework Detection & Exploration (Interactive)                │
│     ├─ Detect UI framework (React/Vue/etc.)                              │
│     ├─ Explore component patterns and conventions                        │
│     ├─ Build component inventory                                         │
│     └─ Output: exploration cache for downstream tasks                    │
│                                                                          │
│  Phase 1: Requirement → CSV + Classification                             │
│     ├─ Generate scan->diagnose->design->implement->test task chain       │
│     ├─ Classify tasks: csv-wave (scan/implement) | interactive (design)  │
│     ├─ Compute dependency waves (topological sort → depth grouping)      │
│     ├─ Generate tasks.csv with wave + exec_mode columns                  │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 2: Wave Execution Engine (Extended)                               │
│     ├─ For each wave (1..N):                                             │
│     │   ├─ Execute pre-wave interactive tasks (design)                   │
│     │   ├─ Build wave CSV (filter csv-wave tasks for this wave)          │
│     │   ├─ Inject previous findings into prev_context column             │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Execute post-wave interactive tasks (testing)                 │
│     │   ├─ Merge all results into master tasks.csv                       │
│     │   └─ Check: any failed? → skip dependents                         │
│     └─ discoveries.ndjson shared across all modes (append-only)          │
│                                                                          │
│  Phase 3: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Display summary: issues found/fixed, test pass rate               │
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
| Scanning tasks (pattern matching, issue detection) | `csv-wave` |
| Diagnosis tasks (root cause analysis) | `csv-wave` |
| Design tasks (solution design, user interaction) | `interactive` |
| Implementation tasks (code fixes) | `csv-wave` |
| Testing tasks (validation, iteration) | `interactive` |
| Exploration tasks (framework patterns, component inventory) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,deps,context_from,exec_mode,role,component,wave,status,findings,issues_found,issues_fixed,error
EXPLORE-001,Framework Exploration,Explore React component patterns and conventions,,,"interactive",explorer,,1,pending,"","","",""
SCAN-001,Scan for UX issues,Scan components for unresponsive buttons and missing feedback,EXPLORE-001,EXPLORE-001,"csv-wave",scanner,Button,2,pending,"","","",""
DIAG-001,Diagnose root causes,Analyze root causes of identified UX issues,SCAN-001,SCAN-001,"csv-wave",diagnoser,Button,3,pending,"","","",""
DESIGN-001,Design solutions,Design fix approach for UX issues,DIAG-001,DIAG-001,"interactive",designer,Button,4,pending,"","","",""
IMPL-001,Implement fixes,Apply fixes to Button component,DESIGN-001,DESIGN-001,"csv-wave",implementer,Button,5,pending,"","","",""
TEST-001,Test fixes,Validate fixes and run tests,IMPL-001,IMPL-001,"interactive",tester,Button,6,pending,"","","",""
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
| `role` | Input | Role name: explorer, scanner, diagnoser, designer, implementer, tester |
| `component` | Input | Component name being processed (empty for exploration) |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` → `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `issues_found` | Output | Number of issues found (scanner/diagnoser only) |
| `issues_fixed` | Output | Number of issues fixed (implementer only) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| explorer | ~/.codex/agents/ux-explorer.md | 2.3 | Explore codebase for UI component patterns | pre-wave (Phase 0) |
| designer | ~/.codex/agents/ux-designer.md | 2.4 | Design fix approach for UX issues | pre-wave (per component) |
| tester | ~/.codex/agents/ux-tester.md | 2.4 | Validate fixes and run tests | post-wave (per component) |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding agent.md** to reload.

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
| `artifacts/scan-report.md` | Scanner findings | Created by scanner |
| `artifacts/diagnosis.md` | Diagnoser analysis | Created by diagnoser |
| `artifacts/design-guide.md` | Designer solutions | Created by designer |
| `artifacts/fixes/` | Implementation files | Created by implementer |
| `artifacts/test-report.md` | Tester validation | Created by tester |

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
├── agents/
│   └── registry.json          # Active interactive agent tracking
└── artifacts/                 # Role deliverables
    ├── scan-report.md
    ├── diagnosis.md
    ├── design-guide.md
    ├── fixes/
    └── test-report.md
```

---

## Implementation

### Session Initialization

```javascript
// Parse arguments
const args = parseArguments($ARGUMENTS)
const autoYes = args.yes || args.y
const concurrency = args.concurrency || args.c || 4
const continueMode = args.continue
const projectPath = args._[0]
const framework = args.framework

// Validate project path
if (!projectPath) {
  throw new Error("Project path required")
}

// Generate session ID
const timestamp = Math.floor(Date.now() / 1000)
const sessionId = `ux-improve-${timestamp}`
const sessionDir = `.workflow/.csv-wave/${sessionId}`

// Create session structure
Bash(`mkdir -p "${sessionDir}/interactive" "${sessionDir}/agents" "${sessionDir}/artifacts/fixes"`)

// Initialize registry
Write(`${sessionDir}/agents/registry.json`, JSON.stringify({
  active: [],
  closed: [],
  created_at: new Date().toISOString()
}, null, 2))

// Initialize discoveries
Write(`${sessionDir}/discoveries.ndjson`, '')

// Store session config
Write(`${sessionDir}/config.json`, JSON.stringify({
  project_path: projectPath,
  framework: framework || "auto-detect",
  max_test_iterations: 5
}, null, 2))
```

---

### Phase 0: Framework Detection & Exploration (Interactive)

**Objective**: Detect UI framework and explore component patterns.

```javascript
// Spawn explorer
const explorer = spawn_agent({
  message: `### MANDATORY FIRST STEPS
1. Read: ~/.codex/agents/ux-explorer.md

---

## Task Assignment

**Goal**: Explore codebase for UI component patterns and framework conventions

**Project Path**: ${projectPath}

**Framework**: ${framework || "auto-detect"}

**Session Directory**: ${sessionDir}

**Deliverables**:
- Framework detection (if auto-detect)
- Component inventory with file paths
- Pattern analysis (state management, event handling, styling)
- Exploration cache for downstream tasks

**Instructions**:
1. Detect framework if not specified (check package.json, file extensions)
2. Scan for UI components (*.tsx, *.vue, etc.)
3. Analyze component patterns and conventions
4. Build component inventory
5. Cache findings in explorations/cache-index.json
6. Output result as JSON with framework and component list`
})

// Wait for completion
const result = wait({ ids: [explorer], timeout_ms: 600000 })

if (result.timed_out) {
  send_input({ id: explorer, message: "Please finalize exploration and output current findings." })
  const retry = wait({ ids: [explorer], timeout_ms: 120000 })
}

// Store result
const explorerOutput = JSON.parse(result.output)
Write(`${sessionDir}/interactive/EXPLORE-001-result.json`, JSON.stringify({
  task_id: "EXPLORE-001",
  status: "completed",
  findings: explorerOutput.summary,
  framework: explorerOutput.framework,
  component_count: explorerOutput.components.length,
  timestamp: new Date().toISOString()
}, null, 2))

close_agent({ id: explorer })

// Update config with detected framework
const config = JSON.parse(Read(`${sessionDir}/config.json`))
config.framework = explorerOutput.framework
Write(`${sessionDir}/config.json`, JSON.stringify(config, null, 2))
```

**Success Criteria**:
- Framework detected or confirmed
- Component inventory created
- Exploration cache available for downstream tasks

---

### Phase 1: Requirement → CSV + Classification

**Objective**: Generate task breakdown for UX improvement pipeline per component.

```javascript
// Load exploration results
const explorationResult = JSON.parse(Read(`${sessionDir}/interactive/EXPLORE-001-result.json`))
const components = explorationResult.components || []

// Generate tasks for each component
const allTasks = []
let taskCounter = 1

// Add exploration task (already completed)
allTasks.push({
  id: "EXPLORE-001",
  title: "Framework Exploration",
  description: "Explore component patterns and conventions",
  deps: "",
  context_from: "",
  exec_mode: "interactive",
  role: "explorer",
  component: "",
  wave: 1,
  status: "completed",
  findings: explorationResult.findings,
  issues_found: "",
  issues_fixed: "",
  error: ""
})

// For each component, create pipeline: scan -> diagnose -> design -> implement -> test
for (const component of components) {
  const compName = component.name
  const compPath = component.path

  // Scan task (csv-wave)
  const scanId = `SCAN-${String(taskCounter).padStart(3, '0')}`
  allTasks.push({
    id: scanId,
    title: `Scan ${compName}`,
    description: `Scan ${compName} component for UX issues: unresponsive buttons, missing feedback, state refresh problems\n\nFile: ${compPath}`,
    deps: "EXPLORE-001",
    context_from: "EXPLORE-001",
    exec_mode: "csv-wave",
    role: "scanner",
    component: compName,
    wave: 0, // Computed later
    status: "pending",
    findings: "",
    issues_found: "",
    issues_fixed: "",
    error: ""
  })

  // Diagnose task (csv-wave)
  const diagId = `DIAG-${String(taskCounter).padStart(3, '0')}`
  allTasks.push({
    id: diagId,
    title: `Diagnose ${compName}`,
    description: `Analyze root causes of UX issues in ${compName}\n\nFile: ${compPath}`,
    deps: scanId,
    context_from: scanId,
    exec_mode: "csv-wave",
    role: "diagnoser",
    component: compName,
    wave: 0,
    status: "pending",
    findings: "",
    issues_found: "",
    issues_fixed: "",
    error: ""
  })

  // Design task (interactive)
  const designId = `DESIGN-${String(taskCounter).padStart(3, '0')}`
  allTasks.push({
    id: designId,
    title: `Design fixes for ${compName}`,
    description: `Design fix approach for UX issues in ${compName}\n\nFile: ${compPath}`,
    deps: diagId,
    context_from: diagId,
    exec_mode: "interactive",
    role: "designer",
    component: compName,
    wave: 0,
    status: "pending",
    findings: "",
    issues_found: "",
    issues_fixed: "",
    error: ""
  })

  // Implement task (csv-wave)
  const implId = `IMPL-${String(taskCounter).padStart(3, '0')}`
  allTasks.push({
    id: implId,
    title: `Implement fixes for ${compName}`,
    description: `Apply fixes to ${compName} component\n\nFile: ${compPath}`,
    deps: designId,
    context_from: designId,
    exec_mode: "csv-wave",
    role: "implementer",
    component: compName,
    wave: 0,
    status: "pending",
    findings: "",
    issues_found: "",
    issues_fixed: "",
    error: ""
  })

  // Test task (interactive)
  const testId = `TEST-${String(taskCounter).padStart(3, '0')}`
  allTasks.push({
    id: testId,
    title: `Test fixes for ${compName}`,
    description: `Validate fixes and run tests for ${compName}\n\nFile: ${compPath}`,
    deps: implId,
    context_from: implId,
    exec_mode: "interactive",
    role: "tester",
    component: compName,
    wave: 0,
    status: "pending",
    findings: "",
    issues_found: "",
    issues_fixed: "",
    error: ""
  })

  taskCounter++
}

// Compute waves via topological sort
const tasksWithWaves = computeWaves(allTasks)

// Write master CSV
writeMasterCSV(`${sessionDir}/tasks.csv`, tasksWithWaves)

// User validation (skip if autoYes)
if (!autoYes) {
  const approval = AskUserQuestion({
    questions: [{
      question: `Generated ${tasksWithWaves.length} tasks for ${components.length} components. Proceed?`,
      header: "Task Breakdown Validation",
      multiSelect: false,
      options: [
        { label: "Proceed", description: "Start UX improvement pipeline" },
        { label: "Cancel", description: "Abort workflow" }
      ]
    }]
  })

  if (approval.answers[0] !== "Proceed") {
    throw new Error("User cancelled workflow")
  }
}
```

**Success Criteria**:
- tasks.csv created with valid schema, wave, and exec_mode assignments
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support.

(Implementation follows same pattern as team-roadmap-dev Phase 2, adapted for UX improvement roles)

---

### Phase 3: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
// Load final master CSV
const finalCSV = readMasterCSV(`${sessionDir}/tasks.csv`)

// Calculate metrics
const completed = finalCSV.filter(t => t.status === 'completed').length
const failed = finalCSV.filter(t => t.status === 'failed').length
const skipped = finalCSV.filter(t => t.status === 'skipped').length
const totalIssuesFound = finalCSV.reduce((sum, t) => sum + (parseInt(t.issues_found) || 0), 0)
const totalIssuesFixed = finalCSV.reduce((sum, t) => sum + (parseInt(t.issues_fixed) || 0), 0)

// Export results.csv
writeFinalResults(`${sessionDir}/results.csv`, finalCSV)

// Generate context.md
const contextMd = generateUXContextReport(finalCSV, sessionDir, {
  totalIssuesFound,
  totalIssuesFixed
})
Write(`${sessionDir}/context.md`, contextMd)

// Cleanup active agents
const registry = JSON.parse(Read(`${sessionDir}/agents/registry.json`))
for (const agent of registry.active) {
  close_agent({ id: agent.id })
}
registry.active = []
Write(`${sessionDir}/agents/registry.json`, JSON.stringify(registry, null, 2))

// Display summary
console.log(`\n=== UX Improvement Pipeline Complete ===`)
console.log(`Completed: ${completed}`)
console.log(`Failed: ${failed}`)
console.log(`Skipped: ${skipped}`)
console.log(`Issues Found: ${totalIssuesFound}`)
console.log(`Issues Fixed: ${totalIssuesFixed}`)
console.log(`Fix Rate: ${totalIssuesFound > 0 ? Math.round(totalIssuesFixed / totalIssuesFound * 100) : 0}%`)
console.log(`\nResults: ${sessionDir}/results.csv`)
console.log(`Report: ${sessionDir}/context.md`)

// Offer next steps
const nextStep = AskUserQuestion({
  questions: [{
    question: "UX Improvement pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean", description: "Archive session and clean up team resources" },
      { label: "Keep Active", description: "Keep session for follow-up work" },
      { label: "Export Results", description: "Export deliverables to specified location" }
    ]
  }]
})

if (nextStep.answers[0] === "Archive & Clean") {
  Bash(`tar -czf "${sessionDir}.tar.gz" "${sessionDir}" && rm -rf "${sessionDir}"`)
  console.log(`Session archived to ${sessionDir}.tar.gz`)
}
```

**Success Criteria**:
- results.csv exported with UX metrics
- context.md generated with issue summary
- All interactive agents closed
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents share `discoveries.ndjson` for UX findings.

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `ux_issue` | `component+type` | `{component, type, description, severity}` | UX issues discovered |
| `pattern` | `pattern` | `{pattern, files[], description}` | UI patterns identified |
| `fix_approach` | `component+issue` | `{component, issue, approach, rationale}` | Fix strategies |
| `test_result` | `component+test` | `{component, test, status, details}` | Test outcomes |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Framework detection fails | AskUserQuestion for framework selection |
| No components found | Complete with empty report, note in findings |
| Circular dependency | Detect in wave computation, abort with error |
| CSV agent timeout | Mark as failed, continue with wave |
| Interactive agent timeout | Urge convergence via send_input |
| Test iterations exceeded (5) | Accept current state, continue |
| All agents in wave failed | Log error, offer retry or abort |
| Project path invalid | Re-prompt user for valid path |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes
3. **CSV is Source of Truth**: Master tasks.csv holds all state
4. **CSV First**: Default to csv-wave; use interactive for design/testing
5. **Context Propagation**: prev_context built from master CSV
6. **Discovery Board is Append-Only**: Never clear discoveries.ndjson
7. **Skip on Failure**: If dependency failed, skip dependent task
8. **Lifecycle Balance**: Every spawn_agent has matching close_agent
9. **Cleanup Temp Files**: Remove wave-{N}.csv after merge
10. **DO NOT STOP**: Continuous execution until all waves complete


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
