---
name: team-issue
description: Hybrid team skill for issue resolution. CSV wave primary for exploration, planning, integration, and implementation. Interactive agents for review gates with fix cycles. Supports Quick, Full, and Batch pipelines.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] [--mode=quick|full|batch] \"issue-ids or --all-pending\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Issue Resolution

## Usage

```bash
$team-issue "ISS-20260308-120000 ISS-20260308-120001"
$team-issue -c 4 "ISS-20260308-120000 --mode=full"
$team-issue -y "--all-pending"
$team-issue --continue "issue-auth-fix-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session
- `--mode=quick|full|batch`: Force pipeline mode (default: auto-detect)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Orchestrate issue resolution pipeline: explore context, plan solution, review (optional), marshal queue, implement. Supports Quick, Full, and Batch pipelines with review-fix cycle.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+---------------------------------------------------------------------------+
|                    TEAM ISSUE RESOLUTION WORKFLOW                          |
+---------------------------------------------------------------------------+
|                                                                           |
|  Phase 1: Requirement Parsing + Pipeline Selection                        |
|     +-- Parse issue IDs (GH-\d+, ISS-\d{8}-\d{6}, --all-pending)         |
|     +-- Auto-detect pipeline mode (quick/full/batch)                      |
|     +-- Determine execution method (codex/gemini/auto)                    |
|     +-- Generate tasks.csv with wave + exec_mode columns                  |
|     +-- User validates task breakdown (skip if -y)                        |
|                                                                           |
|  Phase 2: Wave Execution Engine (Extended)                                |
|     +-- For each wave (1..N):                                             |
|     |   +-- Execute pre-wave interactive tasks (if any)                   |
|     |   +-- Build wave CSV (filter csv-wave tasks for this wave)          |
|     |   +-- Inject previous findings into prev_context column             |
|     |   +-- spawn_agents_on_csv(wave CSV)                                 |
|     |   +-- Execute post-wave interactive tasks (if any)                  |
|     |   +-- Merge all results into master tasks.csv                       |
|     |   +-- Check: any failed? -> skip dependents                         |
|     +-- discoveries.ndjson shared across all modes (append-only)          |
|                                                                           |
|  Phase 3: Post-Wave Interactive (Review Gate)                             |
|     +-- Reviewer agent: multi-dimensional review with verdict             |
|     +-- Fix cycle: rejected -> revise solution -> re-review (max 2)       |
|     +-- Final aggregation / report                                        |
|                                                                           |
|  Phase 4: Results Aggregation                                             |
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
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, clarification, review gates |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Codebase exploration (EXPLORE-*) | `csv-wave` |
| Solution planning (SOLVE-*) | `csv-wave` |
| Queue formation / integration (MARSHAL-*) | `csv-wave` |
| Code implementation (BUILD-*) | `csv-wave` |
| Technical review with verdict (AUDIT-*) | `interactive` |
| Solution revision after rejection (SOLVE-fix-*) | `csv-wave` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,issue_ids,exec_mode,execution_method,deps,context_from,wave,status,findings,artifact_path,error
"EXPLORE-001","Context analysis","Analyze issue context and map codebase impact for ISS-20260308-120000","explorer","ISS-20260308-120000","csv-wave","","","","1","pending","","","",""
"SOLVE-001","Solution design","Design solution and decompose into implementation tasks","planner","ISS-20260308-120000","csv-wave","","EXPLORE-001","EXPLORE-001","2","pending","","","",""
"AUDIT-001","Technical review","Review solution for feasibility, risk, and completeness","reviewer","ISS-20260308-120000","interactive","","SOLVE-001","SOLVE-001","3","pending","","","",""
"MARSHAL-001","Queue formation","Form execution queue with conflict detection","integrator","ISS-20260308-120000","csv-wave","","AUDIT-001","SOLVE-001","4","pending","","","",""
"BUILD-001","Implementation","Implement solution plan and verify with tests","implementer","ISS-20260308-120000","csv-wave","gemini","MARSHAL-001","EXPLORE-001;SOLVE-001","5","pending","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (EXPLORE-NNN, SOLVE-NNN, AUDIT-NNN, MARSHAL-NNN, BUILD-NNN) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `role` | Input | Worker role: explorer, planner, reviewer, integrator, implementer |
| `issue_ids` | Input | Semicolon-separated issue IDs this task covers |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `execution_method` | Input | codex, gemini, qwen, or empty (for non-BUILD tasks) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `artifact_path` | Output | Path to generated artifact (context report, solution, queue, etc.) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| reviewer | agents/reviewer.md | 2.3 (structured review) | Multi-dimensional solution review with verdict | post-wave (after SOLVE wave) |

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
| `explorations/context-{issueId}.json` | Explorer context reports | Created by explorer agents |
| `solutions/solution-{issueId}.json` | Planner solution plans | Created by planner agents |
| `audits/audit-report.json` | Reviewer audit report | Created by reviewer agent |
| `queue/execution-queue.json` | Integrator execution queue | Created by integrator agent |
| `builds/build-{issueId}.json` | Implementer build results | Created by implementer agents |
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
+-- explorations/              # Explorer output
|   +-- context-{issueId}.json
+-- solutions/                 # Planner output
|   +-- solution-{issueId}.json
+-- audits/                    # Reviewer output
|   +-- audit-report.json
+-- queue/                     # Integrator output
|   +-- execution-queue.json
+-- builds/                    # Implementer output
|   +-- build-{issueId}.json
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json
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

// Parse issue IDs
const issueIdPattern = /(?:GH-\d+|ISS-\d{8}-\d{6})/g
let issueIds = requirement.match(issueIdPattern) || []

// Parse mode override
const modeMatch = requirement.match(/--mode=(\w+)/)
let pipelineMode = modeMatch ? modeMatch[1] : null

// Handle --all-pending
if (requirement.includes('--all-pending')) {
  const result = Bash("ccw issue list --status registered,pending --json")
  issueIds = JSON.parse(result).map(i => i.id)
}

// If no issue IDs, ask user
if (issueIds.length === 0) {
  const answer = AskUserQuestion("No issue IDs found. Please provide issue IDs (e.g., ISS-20260308-120000):")
  issueIds = answer.match(issueIdPattern) || []
  if (issueIds.length === 0) return // abort
}

// Auto-detect pipeline mode
if (!pipelineMode) {
  // Load issue priorities
  const priorities = []
  for (const id of issueIds) {
    const info = JSON.parse(Bash(`ccw issue status ${id} --json`))
    priorities.push(info.priority || 0)
  }
  const hasHighPriority = priorities.some(p => p >= 4)

  if (issueIds.length <= 2 && !hasHighPriority) pipelineMode = 'quick'
  else if (issueIds.length <= 4) pipelineMode = 'full'
  else pipelineMode = 'batch'
}

// Execution method selection
let executionMethod = 'gemini' // default
const execMatch = requirement.match(/--exec=(\w+)/)
if (execMatch) executionMethod = execMatch[1]

const slug = issueIds[0].toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 30)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `issue-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/{explorations,solutions,audits,queue,builds,interactive,wisdom}`)

Write(`${sessionFolder}/discoveries.ndjson`, `# Discovery Board - ${sessionId}\n# Format: NDJSON\n`)

// Initialize wisdom files
Write(`${sessionFolder}/wisdom/learnings.md`, `# Learnings\n\nAccumulated during ${sessionId}\n`)
Write(`${sessionFolder}/wisdom/decisions.md`, `# Decisions\n\n`)
Write(`${sessionFolder}/wisdom/conventions.md`, `# Conventions\n\n`)
Write(`${sessionFolder}/wisdom/issues.md`, `# Issues\n\n`)

// Store session metadata
Write(`${sessionFolder}/session.json`, JSON.stringify({
  session_id: sessionId,
  pipeline_mode: pipelineMode,
  issue_ids: issueIds,
  execution_method: executionMethod,
  fix_cycles: 0,
  max_fix_cycles: 2,
  created_at: getUtc8ISOString()
}, null, 2))
```

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Parse issue IDs, determine pipeline mode, generate tasks.csv with wave and exec_mode assignments.

**Decomposition Rules**:

| Pipeline | Tasks Generated |
|----------|----------------|
| quick | EXPLORE-001, SOLVE-001, MARSHAL-001, BUILD-001 (4 tasks, waves 1-4) |
| full | EXPLORE-001, SOLVE-001, AUDIT-001, MARSHAL-001, BUILD-001 (5 tasks, waves 1-5) |
| batch | EXPLORE-001..N, SOLVE-001..N, AUDIT-001, MARSHAL-001, BUILD-001..M (N+N+1+1+M tasks) |

**Classification Rules**:

| Task Prefix | Role | exec_mode | Rationale |
|-------------|------|-----------|-----------|
| EXPLORE-* | explorer | csv-wave | One-shot codebase analysis |
| SOLVE-* | planner | csv-wave | One-shot solution design via CLI |
| SOLVE-fix-* | planner | csv-wave | One-shot revision addressing feedback |
| AUDIT-* | reviewer | interactive | Multi-round review with verdict routing |
| MARSHAL-* | integrator | csv-wave | One-shot queue formation |
| BUILD-* | implementer | csv-wave | One-shot implementation via CLI |

**Wave Computation**: Kahn's BFS topological sort with depth tracking (csv-wave tasks only).

**User Validation**: Display task breakdown with wave + exec_mode assignment (skip if AUTO_YES).

**Task Generation by Pipeline Mode**:

Quick pipeline:
```csv
id,title,description,role,issue_ids,exec_mode,execution_method,deps,context_from,wave,status,findings,artifact_path,error
"EXPLORE-001","Context analysis","Analyze issue context and map codebase impact","explorer","<issue-ids>","csv-wave","","","","1","pending","","",""
"SOLVE-001","Solution design","Design solution and decompose into implementation tasks","planner","<issue-ids>","csv-wave","","EXPLORE-001","EXPLORE-001","2","pending","","",""
"MARSHAL-001","Queue formation","Form execution queue with conflict detection and ordering","integrator","<issue-ids>","csv-wave","","SOLVE-001","SOLVE-001","3","pending","","",""
"BUILD-001","Implementation","Implement solution plan and verify with tests","implementer","<issue-ids>","csv-wave","<exec-method>","MARSHAL-001","EXPLORE-001;SOLVE-001","4","pending","","",""
```

Full pipeline (adds AUDIT-001 as interactive between SOLVE and MARSHAL):
```csv
"AUDIT-001","Technical review","Review solution for feasibility, risk, and completeness","reviewer","<issue-ids>","interactive","","SOLVE-001","SOLVE-001","3","pending","","",""
"MARSHAL-001","Queue formation","...","integrator","<issue-ids>","csv-wave","","AUDIT-001","SOLVE-001","4","pending","","",""
"BUILD-001","Implementation","...","implementer","<issue-ids>","csv-wave","<exec-method>","MARSHAL-001","EXPLORE-001;SOLVE-001","5","pending","","",""
```

Batch pipeline (parallel EXPLORE, sequential SOLVE, then AUDIT, MARSHAL, deferred BUILD):
- EXPLORE-001..N with wave=1, no deps
- SOLVE-001..N with wave=2, deps on all EXPLORE-*
- AUDIT-001 with wave=3, deps on all SOLVE-*, interactive
- MARSHAL-001 with wave=4, deps on AUDIT-001
- BUILD-001..M created after MARSHAL completes (deferred)

**Success Criteria**:
- tasks.csv created with valid schema, wave, and exec_mode assignments
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support and cross-wave context propagation.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
const maxWave = Math.max(...tasks.map(t => parseInt(t.wave)))
let fixCycles = 0

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\nWave ${wave}/${maxWave}`)

  // 1. Separate tasks by exec_mode
  const waveTasks = tasks.filter(t => parseInt(t.wave) === wave)
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave' && t.status === 'pending')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive' && t.status === 'pending')

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

  // 3. Execute csv-wave tasks
  const pendingCsv = csvTasks.filter(t => t.status === 'pending')
  if (pendingCsv.length > 0) {
    // Build prev_context for each task
    for (const task of pendingCsv) {
      const contextIds = (task.context_from || '').split(';').filter(Boolean)
      const prevFindings = contextIds.map(id => {
        const src = tasks.find(t => t.id === id)
        if (!src?.findings) return ''
        return `## [${src.id}] ${src.title}\n${src.findings}`
      }).filter(Boolean).join('\n\n')
      task.prev_context = prevFindings
    }

    // Write wave CSV
    Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingCsv))

    // Execute
    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: Read("~  or <project>/.codex/skills/team-issue/instructions/agent-instruction.md"),
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

    // Merge results
    const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const r of results) {
      const t = tasks.find(t => t.id === r.id)
      if (t) Object.assign(t, r)
    }

    // Cleanup temp files
    Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)
  }

  // 4. Execute interactive tasks (post-wave)
  const pendingInteractive = interactiveTasks.filter(t => t.status === 'pending')
  for (const task of pendingInteractive) {
    // Read agent definition
    const agentDef = Read(`~  or <project>/.codex/skills/team-issue/agents/reviewer.md`)

    // Build context from upstream tasks
    const contextIds = (task.context_from || '').split(';').filter(Boolean)
    const prevContext = contextIds.map(id => {
      const src = tasks.find(t => t.id === id)
      if (!src?.findings) return ''
      return `## [${src.id}] ${src.title}\n${src.findings}\nArtifact: ${src.artifact_path || 'N/A'}`
    }).filter(Boolean).join('\n\n')

    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-issue/agents/reviewer.md (MUST read first)
2. Read: ${sessionFolder}/discoveries.ndjson (shared discoveries)
3. Read: .workflow/project-tech.json (if exists)

---

Goal: ${task.description}
Issue IDs: ${task.issue_ids}
Session: ${sessionFolder}
Scope: Review all solutions in ${sessionFolder}/solutions/ for technical feasibility, risk, and completeness

Deliverables:
- Audit report at ${sessionFolder}/audits/audit-report.json
- Per-issue verdict: approved (>=80), concerns (60-79), rejected (<60)
- Overall verdict

### Previous Context
${prevContext}`
    })

    const result = wait({ ids: [agent], timeout_ms: 600000 })

    if (result.timed_out) {
      send_input({ id: agent, message: "Please finalize and output current findings immediately." })
      const retry = wait({ ids: [agent], timeout_ms: 120000 })
    }

    // Store interactive result
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id,
      status: "completed",
      findings: "Review completed",
      timestamp: getUtc8ISOString()
    }))

    close_agent({ id: agent })

    // Parse review verdict from audit report
    let verdict = 'approved'
    try {
      const auditReport = JSON.parse(Read(`${sessionFolder}/audits/audit-report.json`))
      verdict = auditReport.overall_verdict || 'approved'
    } catch (e) { /* default to approved */ }

    task.status = 'completed'
    task.findings = `Review verdict: ${verdict}`

    // Handle review-fix cycle
    if (verdict === 'rejected' && fixCycles < 2) {
      fixCycles++
      // Create SOLVE-fix and AUDIT re-review tasks
      const fixTask = {
        id: `SOLVE-fix-${String(fixCycles).padStart(3, '0')}`,
        title: `Revise solution (fix cycle ${fixCycles})`,
        description: `Revise solution addressing reviewer feedback. Read audit report for rejection reasons.`,
        role: 'planner',
        issue_ids: task.issue_ids,
        exec_mode: 'csv-wave',
        execution_method: '',
        deps: task.id,
        context_from: task.id,
        wave: String(parseInt(task.wave) + 1),
        status: 'pending',
        findings: '', artifact_path: '', error: ''
      }
      const reReviewTask = {
        id: `AUDIT-${String(fixCycles + 1).padStart(3, '0')}`,
        title: `Re-review revised solution (cycle ${fixCycles})`,
        description: `Re-review revised solution focusing on previously rejected dimensions.`,
        role: 'reviewer',
        issue_ids: task.issue_ids,
        exec_mode: 'interactive',
        execution_method: '',
        deps: fixTask.id,
        context_from: fixTask.id,
        wave: String(parseInt(task.wave) + 2),
        status: 'pending',
        findings: '', artifact_path: '', error: ''
      }
      tasks.push(fixTask, reReviewTask)
      // Adjust MARSHAL and BUILD waves
      for (const t of tasks) {
        if (t.id.startsWith('MARSHAL') || t.id.startsWith('BUILD')) {
          t.wave = String(parseInt(reReviewTask.wave) + (t.id.startsWith('MARSHAL') ? 1 : 2))
          if (t.id.startsWith('MARSHAL')) t.deps = reReviewTask.id
        }
      }
    } else if (verdict === 'rejected' && fixCycles >= 2) {
      // Force proceed with warning
      console.log(`WARNING: Fix cycle limit (${fixCycles}) reached. Forcing proceed to MARSHAL.`)
    }
  }

  // 5. Merge all results into master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 6. Handle deferred BUILD task creation (batch mode after MARSHAL)
  const completedMarshal = tasks.find(t => t.id === 'MARSHAL-001' && t.status === 'completed')
  if (completedMarshal && pipelineMode === 'batch') {
    try {
      const queue = JSON.parse(Read(`${sessionFolder}/queue/execution-queue.json`))
      const buildCount = queue.parallel_groups?.length || 1
      for (let b = 1; b <= Math.min(buildCount, 3); b++) {
        const buildIssues = queue.parallel_groups[b-1]?.issues || issueIds
        tasks.push({
          id: `BUILD-${String(b).padStart(3, '0')}`,
          title: `Implementation group ${b}`,
          description: `Implement solutions for issues in parallel group ${b}`,
          role: 'implementer',
          issue_ids: buildIssues.join(';'),
          exec_mode: 'csv-wave',
          execution_method: executionMethod,
          deps: 'MARSHAL-001',
          context_from: 'EXPLORE-001;SOLVE-001',
          wave: String(parseInt(completedMarshal.wave) + 1),
          status: 'pending',
          findings: '', artifact_path: '', error: ''
        })
      }
      Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))
    } catch (e) { /* single BUILD fallback */ }
  }
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms
- Review-fix cycles handled (max 2)
- Deferred BUILD tasks created after MARSHAL (batch mode)

---

### Phase 3: Post-Wave Interactive

**Objective**: Handle any remaining interactive tasks after all waves complete. In most cases, the review gate is handled inline during Phase 2 wave execution.

If any interactive tasks remain unprocessed (e.g., from dynamically added fix cycles), execute them using the same spawn_agent protocol as Phase 2.

**Success Criteria**:
- All interactive tasks completed or skipped
- Fix cycle limit respected

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')
const skipped = tasks.filter(t => t.status === 'skipped')

// Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// Generate context.md
let contextMd = `# Issue Resolution Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Pipeline**: ${pipelineMode}\n`
contextMd += `**Issues**: ${issueIds.join(', ')}\n`
contextMd += `**Fix Cycles**: ${fixCycles}/${2}\n\n`

contextMd += `## Summary\n\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${completed.length} |\n`
contextMd += `| Failed | ${failed.length} |\n`
contextMd += `| Skipped | ${skipped.length} |\n\n`

contextMd += `## Task Details\n\n`
for (const t of tasks) {
  const icon = t.status === 'completed' ? '[OK]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
  contextMd += `${icon} **${t.id}**: ${t.title} (${t.role})\n`
  if (t.findings) contextMd += `   Findings: ${t.findings.substring(0, 200)}\n`
  if (t.artifact_path) contextMd += `   Artifact: ${t.artifact_path}\n`
  if (t.error) contextMd += `   Error: ${t.error}\n`
  contextMd += `\n`
}

contextMd += `## Deliverables\n\n`
contextMd += `| Artifact | Path |\n|----------|------|\n`
contextMd += `| Context Reports | ${sessionFolder}/explorations/ |\n`
contextMd += `| Solution Plans | ${sessionFolder}/solutions/ |\n`
contextMd += `| Audit Report | ${sessionFolder}/audits/audit-report.json |\n`
contextMd += `| Execution Queue | ${sessionFolder}/queue/execution-queue.json |\n`
contextMd += `| Build Results | ${sessionFolder}/builds/ |\n`

Write(`${sessionFolder}/context.md`, contextMd)

// Display summary
console.log(`
Issue Resolution Complete
Pipeline: ${pipelineMode}
Completed: ${completed.length} | Failed: ${failed.length} | Skipped: ${skipped.length}
Fix Cycles Used: ${fixCycles}/2
Output: ${sessionFolder}
`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- Summary displayed to user

---

## Shared Discovery Board Protocol

Both csv-wave and interactive agents share the same discoveries.ndjson file:

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"EXPLORE-001","type":"file_found","data":{"path":"src/auth/handler.ts","relevance":"high","purpose":"Main auth handler"}}
{"ts":"2026-03-08T10:01:00Z","worker":"EXPLORE-001","type":"pattern_found","data":{"pattern":"middleware-chain","location":"src/middleware/","description":"Express middleware chain pattern"}}
{"ts":"2026-03-08T10:05:00Z","worker":"SOLVE-001","type":"solution_approach","data":{"issue_id":"ISS-20260308-120000","approach":"refactor","estimated_files":5}}
{"ts":"2026-03-08T10:10:00Z","worker":"BUILD-001","type":"impl_result","data":{"issue_id":"ISS-20260308-120000","files_changed":3,"tests_pass":true}}
```

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `file_found` | `path` | `{path, relevance, purpose}` | Relevant file discovered |
| `pattern_found` | `pattern+location` | `{pattern, location, description}` | Code pattern identified |
| `dependency_found` | `from+to` | `{from, to, type}` | Dependency relationship |
| `solution_approach` | `issue_id` | `{issue_id, approach, estimated_files}` | Solution strategy |
| `conflict_found` | `files` | `{issues, files, resolution}` | File conflict between issues |
| `impl_result` | `issue_id` | `{issue_id, files_changed, tests_pass}` | Implementation outcome |

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
| Review rejection exceeds 2 rounds | Force convergence to MARSHAL with warning |
| No issues found for given IDs | Report error, ask user for valid IDs |
| Deferred BUILD count unknown | Read execution-queue.json after MARSHAL completes |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 1
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
