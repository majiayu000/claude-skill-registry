---
name: team-roadmap-dev
description: Roadmap-driven development with phased execution pipeline. Coordinator discusses roadmap with user, then executes plan->execute->verify cycles per phase using CSV wave execution.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"<task-description>\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Roadmap-Driven Development

## Usage

```bash
$team-roadmap-dev "Build authentication module with JWT tokens"
$team-roadmap-dev -c 4 "Refactor payment processing to support multiple gateways"
$team-roadmap-dev -y "Add real-time notifications feature"
$team-roadmap-dev --continue "RD-auth-module-2026-03-08"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Roadmap-driven development workflow that breaks down complex development tasks into phases, with each phase following a plan->execute->verify cycle. The coordinator discusses the roadmap with the user to establish phases and requirements, then executes each phase systematically using CSV wave execution for parallel task processing.

**Execution Model**: Hybrid — CSV wave pipeline (primary) + individual agent spawn (secondary)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ROADMAP-DRIVEN DEVELOPMENT WORKFLOW                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Roadmap Discussion (Interactive)                               │
│     ├─ Discuss requirements and scope with user                          │
│     ├─ Break down into logical phases                                    │
│     ├─ Define success criteria per phase                                 │
│     └─ Output: roadmap.md with phase definitions                         │
│                                                                          │
│  Phase 1: Requirement → CSV + Classification                             │
│     ├─ For each roadmap phase: generate plan->execute->verify tasks      │
│     ├─ Classify tasks: csv-wave (execution) | interactive (planning)     │
│     ├─ Compute dependency waves (topological sort → depth grouping)      │
│     ├─ Generate tasks.csv with wave + exec_mode columns                  │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 2: Wave Execution Engine (Extended)                               │
│     ├─ For each wave (1..N):                                             │
│     │   ├─ Execute pre-wave interactive tasks (planning)                 │
│     │   ├─ Build wave CSV (filter csv-wave tasks for this wave)          │
│     │   ├─ Inject previous findings into prev_context column             │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Execute post-wave interactive tasks (verification)            │
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

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, clarification, inline utility |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Planning tasks (research, exploration, plan generation) | `interactive` |
| Execution tasks (code implementation, file modifications) | `csv-wave` |
| Verification tasks (testing, validation, gap detection) | `interactive` |
| Gap closure tasks (re-planning based on verification) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,deps,context_from,exec_mode,phase,role,wave,status,findings,error
PLAN-101,Phase 1 Planning,Research and plan for authentication module,,,"interactive",1,planner,1,pending,"",""
EXEC-101,Implement auth routes,Create Express routes for login/logout/register,PLAN-101,PLAN-101,"csv-wave",1,executor,2,pending,"",""
EXEC-102,Implement JWT middleware,Create JWT token generation and validation,PLAN-101,PLAN-101,"csv-wave",1,executor,2,pending,"",""
VERIFY-101,Verify Phase 1,Test and validate phase 1 implementation,"EXEC-101;EXEC-102","EXEC-101;EXEC-102","interactive",1,verifier,3,pending,"",""
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
| `phase` | Input | Phase number (1-based) |
| `role` | Input | Role name: planner, executor, verifier |
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
| roadmap-discusser | ~/.codex/agents/roadmap-discusser.md | 2.3 | Discuss roadmap with user, generate phase plan | pre-wave (Phase 0) |
| planner | ~/.codex/agents/roadmap-planner.md | 2.4 | Research and plan creation per phase | pre-wave (per phase) |
| verifier | ~/.codex/agents/roadmap-verifier.md | 2.4 | Test and validate phase implementation | post-wave (per phase) |

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
| `roadmap.md` | Phase definitions and requirements | Created in Phase 0 |
| `phase-{N}/IMPL_PLAN.md` | Implementation plan per phase | Created by planner |
| `phase-{N}/verification.md` | Verification results per phase | Created by verifier |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
├── tasks.csv                  # Master state (all tasks, both modes)
├── results.csv                # Final results export
├── discoveries.ndjson         # Shared discovery board (all agents)
├── context.md                 # Human-readable report
├── roadmap.md                 # Phase definitions
├── wave-{N}.csv               # Temporary per-wave input (csv-wave only)
├── interactive/               # Interactive task artifacts
│   ├── {id}-result.json       # Per-task results
│   └── cache-index.json       # Shared exploration cache
├── agents/
│   └── registry.json          # Active interactive agent tracking
└── phase-{N}/                 # Per-phase artifacts
    ├── IMPL_PLAN.md
    ├── TODO_LIST.md
    ├── .task/IMPL-*.json
    └── verification.md
```

---

## Implementation

### Session Initialization

```javascript
// Parse arguments
const args = parseArguments($ARGUMENTS)
const autoYes = args.yes || args.y
const concurrency = args.concurrency || args.c || 3
const continueMode = args.continue
const taskDescription = args._[0]

// Generate session ID
const slug = taskDescription.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 30)
const date = new Date().toISOString().split('T')[0]
const sessionId = `RD-${slug}-${date}`
const sessionDir = `.workflow/.csv-wave/${sessionId}`

// Create session structure
Bash(`mkdir -p "${sessionDir}/interactive" "${sessionDir}/agents" "${sessionDir}/phase-1"`)

// Initialize registry
Write(`${sessionDir}/agents/registry.json`, JSON.stringify({
  active: [],
  closed: [],
  created_at: new Date().toISOString()
}, null, 2))

// Initialize discoveries
Write(`${sessionDir}/discoveries.ndjson`, '')
```

---

### Phase 0: Roadmap Discussion (Interactive)

**Objective**: Discuss roadmap with user and generate phase plan with requirements and success criteria.

```javascript
// Spawn roadmap discusser
const discusser = spawn_agent({
  message: `### MANDATORY FIRST STEPS
1. Read: ~/.codex/agents/roadmap-discusser.md

---

## Task Assignment

**Goal**: Discuss roadmap with user and generate phase plan

**Task Description**: ${taskDescription}

**Session Directory**: ${sessionDir}

**Deliverables**:
- roadmap.md with phase definitions, requirements, and success criteria
- Each phase should have: phase number, goal, requirements (REQ-IDs), success criteria

**Instructions**:
1. Analyze task description to understand scope
2. Propose phase breakdown to user via AskUserQuestion
3. For each phase, clarify requirements and success criteria
4. Generate roadmap.md with structured phase definitions
5. Output result as JSON with roadmap_path and phase_count`
})

// Wait for completion
const result = wait({ ids: [discusser], timeout_ms: 600000 })

if (result.timed_out) {
  send_input({ id: discusser, message: "Please finalize roadmap and output current plan." })
  const retry = wait({ ids: [discusser], timeout_ms: 120000 })
}

// Store result
const discusserOutput = JSON.parse(result.output)
Write(`${sessionDir}/interactive/DISCUSS-001-result.json`, JSON.stringify({
  task_id: "DISCUSS-001",
  status: "completed",
  findings: discusserOutput.summary,
  roadmap_path: discusserOutput.roadmap_path,
  phase_count: discusserOutput.phase_count,
  timestamp: new Date().toISOString()
}, null, 2))

close_agent({ id: discusser })

// Load roadmap
const roadmap = Read(discusserOutput.roadmap_path)
const phases = parsePhases(roadmap)
```

**Success Criteria**:
- roadmap.md created with phase definitions
- Each phase has clear requirements and success criteria
- User approved phase breakdown

---

### Phase 1: Requirement → CSV + Classification

**Objective**: Generate task breakdown from roadmap phases, classify by exec_mode, compute waves.

```javascript
// Read roadmap
const roadmapContent = Read(`${sessionDir}/roadmap.md`)
const phases = parseRoadmapPhases(roadmapContent)

// Generate tasks for all phases
const allTasks = []
let taskCounter = 1

for (const phase of phases) {
  const phaseNum = phase.number

  // Planning task (interactive, pre-wave)
  allTasks.push({
    id: `PLAN-${phaseNum}01`,
    title: `Phase ${phaseNum} Planning`,
    description: `Research and plan for: ${phase.goal}\n\nRequirements:\n${phase.requirements.join('\n')}\n\nSuccess Criteria:\n${phase.success_criteria.join('\n')}`,
    deps: phaseNum > 1 ? `VERIFY-${phaseNum-1}01` : "",
    context_from: phaseNum > 1 ? `VERIFY-${phaseNum-1}01` : "",
    exec_mode: "interactive",
    phase: phaseNum,
    role: "planner",
    wave: 0, // Computed later
    status: "pending",
    findings: "",
    error: ""
  })

  // Execution tasks (csv-wave) - will be generated by planner
  // Placeholder: planner will create EXEC-{phaseNum}01, EXEC-{phaseNum}02, etc.

  // Verification task (interactive, post-wave)
  allTasks.push({
    id: `VERIFY-${phaseNum}01`,
    title: `Phase ${phaseNum} Verification`,
    description: `Test and validate phase ${phaseNum} implementation against success criteria:\n${phase.success_criteria.join('\n')}`,
    deps: `PLAN-${phaseNum}01`, // Will be updated after execution tasks created
    context_from: `PLAN-${phaseNum}01`, // Will be updated
    exec_mode: "interactive",
    phase: phaseNum,
    role: "verifier",
    wave: 0, // Computed later
    status: "pending",
    findings: "",
    error: ""
  })
}

// Compute waves via topological sort
const tasksWithWaves = computeWaves(allTasks)

// Write master CSV
writeMasterCSV(`${sessionDir}/tasks.csv`, tasksWithWaves)

// User validation (skip if autoYes)
if (!autoYes) {
  const approval = AskUserQuestion({
    questions: [{
      question: `Generated ${tasksWithWaves.length} tasks across ${phases.length} phases. Proceed?`,
      header: "Task Breakdown Validation",
      multiSelect: false,
      options: [
        { label: "Proceed", description: "Start execution" },
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

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support and cross-wave context propagation.

```javascript
// Load master CSV
const masterCSV = readMasterCSV(`${sessionDir}/tasks.csv`)
const maxWave = Math.max(...masterCSV.map(t => t.wave))

for (let waveNum = 1; waveNum <= maxWave; waveNum++) {
  console.log(`\n=== Executing Wave ${waveNum} ===\n`)

  // Get tasks for this wave
  const waveTasks = masterCSV.filter(t => t.wave === waveNum && t.status === 'pending')

  // Separate by exec_mode
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')

  // Execute pre-wave interactive tasks (planners)
  for (const task of interactiveTasks.filter(t => t.role === 'planner')) {
    const agent = spawn_agent({
      message: buildPlannerPrompt(task, sessionDir)
    })

    const result = wait({ ids: [agent], timeout_ms: 600000 })

    if (result.timed_out) {
      send_input({ id: agent, message: "Please finalize plan and output current results." })
      const retry = wait({ ids: [agent], timeout_ms: 120000 })
    }

    // Store result
    Write(`${sessionDir}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id,
      status: "completed",
      findings: parseFindings(result),
      timestamp: new Date().toISOString()
    }, null, 2))

    close_agent({ id: agent })

    // Update master CSV
    updateTaskStatus(masterCSV, task.id, "completed", parseFindings(result))

    // Planner generates execution tasks - read and add to master CSV
    const planTasks = readPlanTasks(`${sessionDir}/phase-${task.phase}/.task/`)
    for (const planTask of planTasks) {
      masterCSV.push({
        id: planTask.id,
        title: planTask.title,
        description: planTask.description,
        deps: task.id,
        context_from: task.id,
        exec_mode: "csv-wave",
        phase: task.phase,
        role: "executor",
        wave: waveNum + 1, // Next wave
        status: "pending",
        findings: "",
        error: ""
      })
    }
  }

  // Build wave CSV for csv-wave tasks
  if (csvTasks.length > 0) {
    const waveCSV = buildWaveCSV(csvTasks, masterCSV, sessionDir)
    const waveCSVPath = `${sessionDir}/wave-${waveNum}.csv`
    writeWaveCSV(waveCSVPath, waveCSV)

    // Execute CSV wave
    spawn_agents_on_csv({
      csv_file_path: waveCSVPath,
      instruction_file_path: `${sessionDir}/../instructions/executor-instruction.md`,
      concurrency: concurrency
    })

    // Merge results back to master CSV
    const waveResults = readWaveCSV(waveCSVPath)
    for (const result of waveResults) {
      updateTaskStatus(masterCSV, result.id, result.status, result.findings, result.error)
    }

    // Cleanup temp wave CSV
    Bash(`rm "${waveCSVPath}"`)
  }

  // Execute post-wave interactive tasks (verifiers)
  for (const task of interactiveTasks.filter(t => t.role === 'verifier')) {
    const agent = spawn_agent({
      message: buildVerifierPrompt(task, sessionDir, masterCSV)
    })

    const result = wait({ ids: [agent], timeout_ms: 600000 })

    if (result.timed_out) {
      send_input({ id: agent, message: "Please finalize verification and output current results." })
      const retry = wait({ ids: [agent], timeout_ms: 120000 })
    }

    // Store result
    const verificationResult = JSON.parse(result.output)
    Write(`${sessionDir}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id,
      status: "completed",
      findings: verificationResult.summary,
      gaps_found: verificationResult.gaps || [],
      timestamp: new Date().toISOString()
    }, null, 2))

    close_agent({ id: agent })

    // Update master CSV
    updateTaskStatus(masterCSV, task.id, "completed", verificationResult.summary)

    // Handle gaps (max 3 iterations)
    if (verificationResult.gaps && verificationResult.gaps.length > 0) {
      const gapIteration = countGapIterations(masterCSV, task.phase)
      if (gapIteration < 3) {
        // Create gap closure tasks
        const gapTasks = createGapClosureTasks(verificationResult.gaps, task.phase, gapIteration)
        masterCSV.push(...gapTasks)
      } else {
        console.log(`[WARNING] Max gap iterations (3) reached for phase ${task.phase}`)
      }
    }
  }

  // Write updated master CSV
  writeMasterCSV(`${sessionDir}/tasks.csv`, masterCSV)

  // Check for failures and skip dependents
  const failedTasks = waveTasks.filter(t => t.status === 'failed')
  if (failedTasks.length > 0) {
    skipDependentTasks(masterCSV, failedTasks.map(t => t.id))
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
// Load final master CSV
const finalCSV = readMasterCSV(`${sessionDir}/tasks.csv`)

// Export results.csv
writeFinalResults(`${sessionDir}/results.csv`, finalCSV)

// Generate context.md
const contextMd = generateContextReport(finalCSV, sessionDir)
Write(`${sessionDir}/context.md`, contextMd)

// Cleanup active agents
const registry = JSON.parse(Read(`${sessionDir}/agents/registry.json`))
for (const agent of registry.active) {
  close_agent({ id: agent.id })
}
registry.active = []
Write(`${sessionDir}/agents/registry.json`, JSON.stringify(registry, null, 2))

// Display summary
const completed = finalCSV.filter(t => t.status === 'completed').length
const failed = finalCSV.filter(t => t.status === 'failed').length
const skipped = finalCSV.filter(t => t.status === 'skipped').length

console.log(`\n=== Roadmap Development Complete ===`)
console.log(`Completed: ${completed}`)
console.log(`Failed: ${failed}`)
console.log(`Skipped: ${skipped}`)
console.log(`\nResults: ${sessionDir}/results.csv`)
console.log(`Report: ${sessionDir}/context.md`)

// Offer next steps
const nextStep = AskUserQuestion({
  questions: [{
    question: "Roadmap Dev pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean (Recommended)", description: "Archive session, clean up tasks and team resources" },
      { label: "Keep Active", description: "Keep session active for follow-up work or inspection" },
      { label: "Export Results", description: "Export deliverables to a specified location, then clean" }
    ]
  }]
})

if (nextStep.answers[0] === "Archive & Clean (Recommended)") {
  Bash(`tar -czf "${sessionDir}.tar.gz" "${sessionDir}" && rm -rf "${sessionDir}"`)
  console.log(`Session archived to ${sessionDir}.tar.gz`)
}
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- All interactive agents closed (registry.json cleanup)
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (both csv-wave and interactive) share a single `discoveries.ndjson` file for exploration findings.

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `file_pattern` | `pattern` | `{pattern, files[], description}` | Code patterns discovered |
| `dependency` | `from+to` | `{from, to, type}` | Module dependencies |
| `risk` | `description` | `{description, severity, mitigation}` | Implementation risks |
| `test_gap` | `area` | `{area, description, priority}` | Testing gaps |

**Write Protocol**:

```bash
echo '{"ts":"2026-03-08T14:30:22Z","worker":"EXEC-101","type":"file_pattern","data":{"pattern":"auth middleware","files":["src/middleware/auth.ts"],"description":"JWT validation pattern"}}' >> ${sessionDir}/discoveries.ndjson
```

**Read Protocol**:

```javascript
const discoveries = Read(`${sessionDir}/discoveries.ndjson`)
  .split('\n')
  .filter(line => line.trim())
  .map(line => JSON.parse(line))
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
| project-tech.json missing | Invoke workflow:init skill |
| Verifier gaps persist (>3 iterations) | Report to user, ask for manual intervention |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0
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
