---
name: team-iterdev
description: Iterative development team with Generator-Critic loop, dynamic pipeline selection (patch/sprint/multi-sprint), task ledger for progress tracking, and shared wisdom for cross-sprint learning.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team IterDev

## Usage

```bash
$team-iterdev "Implement user authentication with JWT"
$team-iterdev -c 4 "Refactor payment module to support multiple gateways"
$team-iterdev -y "Fix login button not responding on mobile"
$team-iterdev --continue "ids-auth-jwt-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Iterative development team skill with Generator-Critic (GC) loops between developer and reviewer roles (max 3 rounds). Automatically selects pipeline complexity (patch/sprint/multi-sprint) based on task signals. Tracks progress via task ledger. Accumulates cross-sprint wisdom in shared discovery board.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary for GC loop control and requirement analysis)

```
+-------------------------------------------------------------------------+
|                    TEAM ITERDEV WORKFLOW                                  |
+-------------------------------------------------------------------------+
|                                                                          |
|  Phase 0: Pre-Wave Interactive                                           |
|     +-- Analyze task complexity and select pipeline mode                 |
|     +-- Explore codebase for patterns and dependencies                   |
|     +-- Output: pipeline mode, task analysis, session artifacts          |
|                                                                          |
|  Phase 1: Requirement -> CSV + Classification                            |
|     +-- Parse task into pipeline-specific task chain                     |
|     +-- Assign roles: architect, developer, tester, reviewer             |
|     +-- Classify tasks: csv-wave | interactive (exec_mode)               |
|     +-- Compute dependency waves (topological sort -> depth grouping)    |
|     +-- Generate tasks.csv with wave + exec_mode columns                 |
|     +-- User validates task breakdown (skip if -y)                       |
|                                                                          |
|  Phase 2: Wave Execution Engine (Extended)                               |
|     +-- For each wave (1..N):                                            |
|     |   +-- Execute pre-wave interactive tasks (if any)                  |
|     |   +-- Build wave CSV (filter csv-wave tasks for this wave)         |
|     |   +-- Inject previous findings into prev_context column            |
|     |   +-- spawn_agents_on_csv(wave CSV)                                |
|     |   +-- Execute post-wave interactive tasks (if any)                 |
|     |   +-- Merge all results into master tasks.csv                      |
|     |   +-- Check: any failed? -> skip dependents                        |
|     +-- discoveries.ndjson shared across all modes (append-only)         |
|                                                                          |
|  Phase 3: Post-Wave Interactive                                          |
|     +-- Generator-Critic (GC) loop control                               |
|     +-- If review has critical issues: trigger DEV-fix -> re-REVIEW      |
|     +-- Max 3 GC rounds, then force convergence                         |
|                                                                          |
|  Phase 4: Results Aggregation                                            |
|     +-- Export final results.csv                                         |
|     +-- Generate context.md with all findings                            |
|     +-- Display summary: completed/failed/skipped per wave               |
|     +-- Offer: view results | retry failed | done                       |
|                                                                          |
+-------------------------------------------------------------------------+
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
| Architecture design (DESIGN-*) | `csv-wave` |
| Code implementation (DEV-*) | `csv-wave` |
| Test execution and fix cycle (VERIFY-*) | `csv-wave` |
| Code review (REVIEW-*) | `csv-wave` |
| Fix task from review feedback (DEV-fix-*) | `csv-wave` |
| GC loop control (decide revision vs convergence) | `interactive` |
| Task analysis and pipeline selection (Phase 0) | `interactive` |

---

## Pipeline Selection Logic

| Signal | Score |
|--------|-------|
| Changed files > 10 | +3 |
| Changed files 3-10 | +2 |
| Structural change (refactor, architect, restructure) | +3 |
| Cross-cutting concern (multiple, across, cross) | +2 |
| Simple fix (fix, bug, typo, patch) | -2 |

| Score | Pipeline |
|-------|----------|
| >= 5 | multi-sprint |
| 2-4 | sprint |
| 0-1 | patch |

### Pipeline Definitions

**Patch** (2 tasks, serial):
```
DEV-001 -> VERIFY-001
```

**Sprint** (4 tasks, with parallel window):
```
DESIGN-001 -> DEV-001 -> [VERIFY-001 + REVIEW-001] (parallel)
```

**Multi-Sprint** (5+ tasks, iterative with GC loop):
```
Sprint 1: DESIGN-001 -> DEV-001 -> [VERIFY-001 + REVIEW-001] -> DEV-fix (if needed) -> REVIEW-002
Sprint 2+ created dynamically
```

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,pipeline,sprint_num,gc_round,deps,context_from,exec_mode,wave,status,findings,review_score,gc_signal,error
"DESIGN-001","Technical design and task breakdown","Explore codebase, create component design, break into implementable tasks with acceptance criteria","architect","sprint","1","0","","","csv-wave","1","pending","","","",""
"DEV-001","Implement design","Load design and task breakdown, implement tasks in execution order, validate syntax","developer","sprint","1","0","DESIGN-001","DESIGN-001","csv-wave","2","pending","","","",""
"VERIFY-001","Verify implementation","Detect test framework, run targeted tests, run regression suite","tester","sprint","1","0","DEV-001","DEV-001","csv-wave","3","pending","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `role` | Input | Worker role: architect, developer, tester, reviewer |
| `pipeline` | Input | Pipeline mode: patch, sprint, multi-sprint |
| `sprint_num` | Input | Sprint number (1-based, for multi-sprint) |
| `gc_round` | Input | Generator-Critic round number (0 = initial, 1+ = fix round) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `review_score` | Output | Quality score 1-10 (reviewer only) |
| `gc_signal` | Output | `REVISION_NEEDED` or `CONVERGED` (reviewer only) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| task-analyzer | agents/task-analyzer.md | 2.3 (wait-respond) | Analyze task complexity, select pipeline mode, detect capabilities | standalone (Phase 0) |
| gc-controller | agents/gc-controller.md | 2.3 (wait-respond) | Evaluate review severity, decide DEV-fix vs convergence | post-wave (after REVIEW wave) |

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
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |
| `wisdom/` | Cross-sprint knowledge accumulation | Updated by agents via discoveries |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state (all tasks, both modes)
+-- results.csv                # Final results export
+-- discoveries.ndjson         # Shared discovery board (all agents)
+-- context.md                 # Human-readable report
+-- wave-{N}.csv               # Temporary per-wave input (csv-wave only)
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json       # Per-task results
+-- wisdom/                    # Cross-sprint knowledge
|   +-- learnings.md
|   +-- decisions.md
|   +-- conventions.md
|   +-- issues.md
+-- design/                    # Architect output
|   +-- design-001.md
|   +-- task-breakdown.json
+-- code/                      # Developer tracking
|   +-- dev-log.md
+-- verify/                    # Tester output
|   +-- verify-001.json
+-- review/                    # Reviewer output
    +-- review-001.md
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const continueMode = $ARGUMENTS.includes('--continue')
const concurrencyMatch = $ARGUMENTS.match(/(?:--concurrency|-c)\s+(\d+)/)
const maxConcurrency = concurrencyMatch ? parseInt(concurrencyMatch[1]) : 3

// Clean requirement text (remove flags)
const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
let sessionId = `ids-${slug}-${dateStr}`
let sessionFolder = `.workflow/.csv-wave/${sessionId}`

// Continue mode: find existing session
if (continueMode) {
  const existing = Bash(`ls -t .workflow/.csv-wave/ids-* 2>/dev/null | head -1`).trim()
  if (existing) {
    sessionId = existing.split('/').pop()
    sessionFolder = existing
    // Read existing tasks.csv, find incomplete waves, resume from Phase 2
  }
}

Bash(`mkdir -p ${sessionFolder}/{interactive,wisdom,design,code,verify,review}`)

// Initialize wisdom files
Write(`${sessionFolder}/wisdom/learnings.md`, `# Learnings\n\n`)
Write(`${sessionFolder}/wisdom/decisions.md`, `# Decisions\n\n`)
Write(`${sessionFolder}/wisdom/conventions.md`, `# Conventions\n\n`)
Write(`${sessionFolder}/wisdom/issues.md`, `# Issues\n\n`)
```

---

### Phase 0: Pre-Wave Interactive

**Objective**: Analyze task complexity, explore codebase, and select pipeline mode.

**Execution**:

```javascript
const analyzer = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-iterdev/agents/task-analyzer.md (MUST read first)
2. Read: .workflow/project-tech.json (if exists)

---

Goal: Analyze iterative development task and select pipeline mode
Requirement: ${requirement}

### Task
1. Detect capabilities from keywords:
   - design/architect/restructure -> architect role needed
   - implement/build/code/fix -> developer role needed
   - test/verify/validate -> tester role needed
   - review/audit/quality -> reviewer role needed
2. Score complexity for pipeline selection:
   - Changed files > 10: +3, 3-10: +2
   - Structural change: +3
   - Cross-cutting: +2
   - Simple fix: -2
3. Score >= 5 -> multi-sprint, 2-4 -> sprint, 0-1 -> patch
4. Return structured analysis result
`
})

const analyzerResult = wait({ ids: [analyzer], timeout_ms: 120000 })

if (analyzerResult.timed_out) {
  send_input({ id: analyzer, message: "Please finalize and output current findings." })
  const retry = wait({ ids: [analyzer], timeout_ms: 60000 })
}

close_agent({ id: analyzer })

// Store analysis result
Write(`${sessionFolder}/interactive/task-analyzer-result.json`, JSON.stringify({
  task_id: "task-analysis",
  status: "completed",
  pipeline_mode: parsedMode, // "patch" | "sprint" | "multi-sprint"
  capabilities: parsedCapabilities,
  complexity_score: parsedScore,
  roles_needed: parsedRoles,
  timestamp: getUtc8ISOString()
}))
```

If not AUTO_YES, present pipeline mode selection for confirmation:

```javascript
if (!AUTO_YES) {
  const answer = AskUserQuestion({
    questions: [{
      question: `Task: "${requirement}"\nRecommended pipeline: ${pipeline_mode} (complexity: ${complexity_score})\nRoles: ${roles_needed.join(', ')}\n\nApprove?`,
      header: "Pipeline Selection",
      multiSelect: false,
      options: [
        { label: "Approve", description: `Use ${pipeline_mode} pipeline` },
        { label: "Patch", description: "Simple fix: DEV -> VERIFY (2 tasks)" },
        { label: "Sprint", description: "Standard: DESIGN -> DEV -> VERIFY + REVIEW (4 tasks)" },
        { label: "Multi-Sprint", description: "Complex: Multiple sprint cycles with incremental delivery" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Pipeline mode selected and confirmed
- Task analysis stored in session
- Interactive agents closed, results stored

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Build tasks.csv from selected pipeline mode with proper wave assignments.

**Decomposition Rules**:

| Pipeline | Tasks | Wave Structure |
|----------|-------|---------------|
| patch | DEV-001 -> VERIFY-001 | 2 waves, serial |
| sprint | DESIGN-001 -> DEV-001 -> VERIFY-001 + REVIEW-001 | 3 waves (VERIFY and REVIEW parallel in wave 3) |
| multi-sprint | DESIGN-001 -> DEV-001 -> VERIFY-001 + REVIEW-001 -> DEV-fix + REVIEW-002 | 4+ waves, with GC loop |

**Pipeline Task Definitions**:

#### Patch Pipeline (2 csv-wave tasks)

| Task ID | Role | Wave | Deps | Description |
|---------|------|------|------|-------------|
| DEV-001 | developer | 1 | (none) | Implement fix: load target files, apply changes, validate syntax |
| VERIFY-001 | tester | 2 | DEV-001 | Verify fix: detect test framework, run targeted tests, check for regressions |

#### Sprint Pipeline (4 csv-wave tasks)

| Task ID | Role | Wave | Deps | Description |
|---------|------|------|------|-------------|
| DESIGN-001 | architect | 1 | (none) | Technical design: explore codebase, create component design, task breakdown |
| DEV-001 | developer | 2 | DESIGN-001 | Implement design: load design and task breakdown, implement in order, validate syntax |
| VERIFY-001 | tester | 3 | DEV-001 | Verify implementation: detect framework, run targeted tests, run regression suite |
| REVIEW-001 | reviewer | 3 | DEV-001 | Code review: load changes and design, review across correctness/completeness/maintainability/security, score quality |

#### Multi-Sprint Pipeline (5+ csv-wave tasks + GC control)

| Task ID | Role | Wave | Deps | Description |
|---------|------|------|------|-------------|
| DESIGN-001 | architect | 1 | (none) | Technical design and task breakdown for sprint 1 |
| DEV-001 | developer | 2 | DESIGN-001 | First implementation batch |
| VERIFY-001 | tester | 3 | DEV-001 | Test execution and fix cycle |
| REVIEW-001 | reviewer | 3 | DEV-001 | Code review with GC signal |
| GC-CHECK-001 | gc-controller | 4 | REVIEW-001 | GC decision: revision or convergence |

Additional DEV-fix and REVIEW tasks created dynamically when GC controller decides REVISION.

**Classification Rules**:

All work tasks (design, development, testing, review) are `csv-wave`. GC loop control between reviewer and next dev-fix is `interactive` (post-wave, spawned by orchestrator to decide the GC outcome).

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
const failedIds = new Set()
const skippedIds = new Set()
const MAX_GC_ROUNDS = 3
let gcRound = 0

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\n## Wave ${wave}/${maxWave}\n`)

  // 1. Read current master CSV
  const masterCsv = parseCsv(Read(`${sessionFolder}/tasks.csv`))

  // 2. Separate csv-wave and interactive tasks for this wave
  const waveTasks = masterCsv.filter(row => parseInt(row.wave) === wave)
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')

  // 3. Skip tasks whose deps failed
  const executableCsvTasks = []
  for (const task of csvTasks) {
    const deps = task.deps.split(';').filter(Boolean)
    if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
      skippedIds.add(task.id)
      updateMasterCsvRow(sessionFolder, task.id, {
        status: 'skipped',
        error: 'Dependency failed or skipped'
      })
      continue
    }
    executableCsvTasks.push(task)
  }

  // 4. Build prev_context for each csv-wave task
  for (const task of executableCsvTasks) {
    const contextIds = task.context_from.split(';').filter(Boolean)
    const prevFindings = contextIds
      .map(id => {
        const prevRow = masterCsv.find(r => r.id === id)
        if (prevRow && prevRow.status === 'completed' && prevRow.findings) {
          return `[Task ${id}: ${prevRow.title}] ${prevRow.findings}`
        }
        return null
      })
      .filter(Boolean)
      .join('\n')
    task.prev_context = prevFindings || 'No previous context available'
  }

  // 5. Write wave CSV and execute csv-wave tasks
  if (executableCsvTasks.length > 0) {
    const waveHeader = 'id,title,description,role,pipeline,sprint_num,gc_round,deps,context_from,exec_mode,wave,prev_context'
    const waveRows = executableCsvTasks.map(t =>
      [t.id, t.title, t.description, t.role, t.pipeline, t.sprint_num, t.gc_round, t.deps, t.context_from, t.exec_mode, t.wave, t.prev_context]
        .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
        .join(',')
    )
    Write(`${sessionFolder}/wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

    const waveResult = spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: Read(`~  or <project>/.codex/skills/team-iterdev/instructions/agent-instruction.md`),
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          review_score: { type: "string" },
          gc_signal: { type: "string" },
          error: { type: "string" }
        },
        required: ["id", "status", "findings"]
      }
    })

    // Merge results into master CSV
    const waveResults = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const result of waveResults) {
      updateMasterCsvRow(sessionFolder, result.id, {
        status: result.status,
        findings: result.findings || '',
        review_score: result.review_score || '',
        gc_signal: result.gc_signal || '',
        error: result.error || ''
      })
      if (result.status === 'failed') failedIds.add(result.id)
    }

    Bash(`rm -f "${sessionFolder}/wave-${wave}.csv"`)
  }

  // 6. Execute post-wave interactive tasks (GC controller)
  for (const task of interactiveTasks) {
    if (task.status !== 'pending') continue
    const deps = task.deps.split(';').filter(Boolean)
    if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
      skippedIds.add(task.id)
      continue
    }

    // Spawn GC controller agent
    const gcAgent = spawn_agent({
      message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-iterdev/agents/gc-controller.md (MUST read first)
2. Read: ${sessionFolder}/discoveries.ndjson (shared discoveries)

---

Goal: Evaluate review severity and decide DEV-fix vs convergence
Session: ${sessionFolder}
GC Round: ${gcRound}
Max GC Rounds: ${MAX_GC_ROUNDS}

### Context
Read the latest review file in ${sessionFolder}/review/ and check:
- review.critical_count > 0 OR review.score < 7 -> REVISION
- review.critical_count == 0 AND review.score >= 7 -> CONVERGE
If gcRound >= maxRounds -> CONVERGE (force convergence)
`
    })

    const gcResult = wait({ ids: [gcAgent], timeout_ms: 120000 })
    if (gcResult.timed_out) {
      send_input({ id: gcAgent, message: "Please finalize your decision now." })
      wait({ ids: [gcAgent], timeout_ms: 60000 })
    }
    close_agent({ id: gcAgent })

    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed",
      gc_decision: gcDecision, gc_round: gcRound,
      timestamp: getUtc8ISOString()
    }))

    if (gcDecision === "CONVERGE") {
      // Skip remaining GC tasks, mark fix tasks as skipped
    } else {
      gcRound++
      // Dynamically add DEV-fix and REVIEW tasks to master CSV for next waves
      const fixWave = wave + 1
      const reviewWave = wave + 2
      appendMasterCsvRow(sessionFolder, {
        id: `DEV-fix-${gcRound}`, title: `Fix review issues (round ${gcRound})`,
        description: `Fix critical/high issues from REVIEW. Focus on review feedback only.`,
        role: 'developer', pipeline: pipeline_mode, sprint_num: '1',
        gc_round: String(gcRound), deps: task.id, context_from: `REVIEW-001`,
        exec_mode: 'csv-wave', wave: String(fixWave),
        status: 'pending', findings: '', review_score: '', gc_signal: '', error: ''
      })
      appendMasterCsvRow(sessionFolder, {
        id: `REVIEW-${gcRound + 1}`, title: `Re-review (round ${gcRound})`,
        description: `Review fixes from DEV-fix-${gcRound}. Re-evaluate quality.`,
        role: 'reviewer', pipeline: pipeline_mode, sprint_num: '1',
        gc_round: String(gcRound), deps: `DEV-fix-${gcRound}`, context_from: `DEV-fix-${gcRound}`,
        exec_mode: 'csv-wave', wave: String(reviewWave),
        status: 'pending', findings: '', review_score: '', gc_signal: '', error: ''
      })
      maxWave = Math.max(maxWave, reviewWave)
    }

    updateMasterCsvRow(sessionFolder, task.id, { status: 'completed', findings: `GC decision: ${gcDecision}` })
  }
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms
- GC loop controlled with max 3 rounds

---

### Phase 3: Post-Wave Interactive

**Objective**: Handle any final GC loop convergence and multi-sprint transitions.

If the pipeline is multi-sprint and the current sprint completed successfully:
1. Evaluate sprint metrics (velocity, review scores)
2. If more sprints needed, dynamically create next sprint tasks in master CSV
3. If sprint metrics are strong (review avg >= 8), consider downgrading next sprint to simpler pipeline

If max GC rounds reached and issues remain, log to wisdom/issues.md and proceed.

**Success Criteria**:
- Post-wave interactive processing complete
- Interactive agents closed, results stored

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
Write(`${sessionFolder}/results.csv`, masterCsv)

const tasks = parseCsv(masterCsv)
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')
const skipped = tasks.filter(t => t.status === 'skipped')

const contextContent = `# Team IterDev Report

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Pipeline**: ${pipeline_mode}
**Completed**: ${getUtc8ISOString()}

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | ${tasks.length} |
| Completed | ${completed.length} |
| Failed | ${failed.length} |
| Skipped | ${skipped.length} |
| GC Rounds | ${gcRound} |

---

## Pipeline Execution

${waveDetails}

---

## Task Details

${taskDetails}

---

## Deliverables

| Artifact | Path |
|----------|------|
| Design Document | ${sessionFolder}/design/design-001.md |
| Task Breakdown | ${sessionFolder}/design/task-breakdown.json |
| Dev Log | ${sessionFolder}/code/dev-log.md |
| Verification | ${sessionFolder}/verify/verify-001.json |
| Review Report | ${sessionFolder}/review/review-001.md |
| Wisdom | ${sessionFolder}/wisdom/ |
`

Write(`${sessionFolder}/context.md`, contextContent)
```

If not AUTO_YES, offer completion actions:

```javascript
if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "IterDev pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, generate final report" },
        { label: "Keep Active", description: "Keep session for follow-up or inspection" },
        { label: "Retry Failed", description: "Re-run failed tasks" }
      ]
    }]
  })
}
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- All interactive agents closed
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents across all waves share `discoveries.ndjson`. This enables cross-role knowledge sharing.

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `design_decision` | `data.component` | `{component, approach, rationale, alternatives}` | Architecture decision |
| `implementation` | `data.file` | `{file, changes, pattern_used, notes}` | Code implementation detail |
| `test_result` | `data.test_suite` | `{test_suite, pass_rate, failures[], regressions}` | Test execution result |
| `review_finding` | `data.file_line` | `{file_line, severity, dimension, description, suggestion}` | Review finding |
| `convention` | `data.name` | `{name, description, example}` | Discovered project convention |
| `gc_decision` | `data.round` | `{round, signal, critical_count, score}` | GC loop decision |

**Format**: NDJSON, each line is self-contained JSON:

```jsonl
{"ts":"2026-03-08T10:00:00+08:00","worker":"DESIGN-001","type":"design_decision","data":{"component":"AuthModule","approach":"JWT with refresh tokens","rationale":"Stateless auth for microservices","alternatives":"Session-based, OAuth2"}}
{"ts":"2026-03-08T10:05:00+08:00","worker":"DEV-001","type":"implementation","data":{"file":"src/auth/jwt.ts","changes":"Added JWT middleware","pattern_used":"Express middleware pattern","notes":"Uses existing bcrypt dependency"}}
{"ts":"2026-03-08T10:10:00+08:00","worker":"REVIEW-001","type":"review_finding","data":{"file_line":"src/auth/jwt.ts:42","severity":"HIGH","dimension":"security","description":"Token expiry not validated","suggestion":"Add exp claim check"}}
```

**Protocol Rules**:
1. Read board before own work -- leverage existing context
2. Write discoveries immediately via `echo >>` -- don't batch
3. Deduplicate -- check existing entries by type + dedup key
4. Append-only -- never modify or delete existing lines

---

## Consensus Severity Routing

When the reviewer returns review results with severity-graded verdicts:

| Severity | Action |
|----------|--------|
| HIGH | Trigger DEV-fix round (GC loop), max 3 rounds total |
| MEDIUM | Log warning, continue pipeline |
| LOW | Treat as review passed |

**Constraints**: Max 3 GC rounds (fix cycles). If still HIGH after 3 rounds, force convergence and record in wisdom/issues.md.

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
| GC loop exceeds 3 rounds | Force convergence, record in wisdom/issues.md |
| Sprint velocity drops below 50% | Report to user, suggest scope reduction |
| Task ledger corrupted | Rebuild from tasks.csv state |
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
8. **Lifecycle Balance**: Every spawn_agent MUST have a matching close_agent
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
