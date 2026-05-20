---
name: team-tech-debt
description: Systematic tech debt governance with CSV wave pipeline. Scans codebase for tech debt across 5 dimensions, assesses severity with priority matrix, plans phased remediation, executes fixes in worktree, validates with 4-layer checks. Supports scan/remediate/targeted pipeline modes with fix-verify GC loop.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] [--mode=scan|remediate|targeted] \"scope or description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Tech Debt

## Usage

```bash
$team-tech-debt "Scan and fix tech debt in src/ module"
$team-tech-debt --mode=scan "Audit codebase for tech debt"
$team-tech-debt --mode=targeted "Fix known TODO/FIXME items in auth module"
$team-tech-debt -c 4 -y "Full remediation pipeline for entire project"
$team-tech-debt --continue "td-auth-debt-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session
- `--mode=scan`: Scan and assess only, no fixes
- `--mode=targeted`: Skip scan/assess, direct fix path for known debt
- `--mode=remediate`: Full pipeline (default)

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Systematic tech debt governance: scan -> assess -> plan -> fix -> validate. Five specialized worker roles execute as CSV wave agents, with interactive agents for plan approval checkpoints and fix-verify GC loops.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|              TEAM TECH DEBT WORKFLOW                                |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse mode (scan/remediate/targeted)                         |
|     +- Clarify scope and focus areas                                |
|     +- Output: pipeline mode + scope for decomposition              |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Select pipeline mode (scan/remediate/targeted)               |
|     +- Build task chain with fixed role assignments                 |
|     +- Classify tasks: csv-wave | interactive (exec_mode)           |
|     +- Compute dependency waves (linear chain)                      |
|     +- Generate tasks.csv with wave + exec_mode columns             |
|     +- User validates task breakdown (skip if -y)                   |
|                                                                     |
|  Phase 2: Wave Execution Engine (Extended)                          |
|     +- For each wave (1..N):                                        |
|     |   +- Execute pre-wave interactive tasks (plan approval)       |
|     |   +- Build wave CSV (filter csv-wave tasks for this wave)     |
|     |   +- Inject previous findings into prev_context column        |
|     |   +- spawn_agents_on_csv(wave CSV)                            |
|     |   +- Execute post-wave interactive tasks (if any)             |
|     |   +- Merge all results into master tasks.csv                  |
|     |   +- Check: any failed? -> skip dependents                    |
|     |   +- TDVAL checkpoint: GC loop check                          |
|     +- discoveries.ndjson shared across all modes (append-only)     |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion + PR)                   |
|     +- PR creation (if worktree mode, validation passed)            |
|     +- Debt reduction metrics report                                |
|     +- Interactive completion choice                                |
|                                                                     |
|  Phase 4: Results Aggregation                                       |
|     +- Export final results.csv                                     |
|     +- Generate context.md with debt metrics                        |
|     +- Display summary: debt scores, reduction rate                 |
|     +- Offer: new target | deep fix | close                        |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot scan, assessment, planning, execution, validation |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Plan approval checkpoint, fix-verify GC loop management |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Multi-dimension debt scan (TDSCAN) | `csv-wave` |
| Quantitative assessment (TDEVAL) | `csv-wave` |
| Remediation planning (TDPLAN) | `csv-wave` |
| Plan approval gate | `interactive` |
| Debt cleanup execution (TDFIX) | `csv-wave` |
| Cleanup validation (TDVAL) | `csv-wave` |
| Fix-verify GC loop management | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,debt_dimension,pipeline_mode,deps,context_from,exec_mode,wave,status,findings,debt_items_count,artifacts_produced,error
"TDSCAN-001","Multi-dimension debt scan","Scan codebase across 5 dimensions for tech debt items","scanner","all","remediate","","","csv-wave","1","pending","","0","",""
"TDEVAL-001","Severity assessment","Quantify impact and fix cost for each debt item","assessor","all","remediate","TDSCAN-001","TDSCAN-001","csv-wave","2","pending","","0","",""
"TDPLAN-001","Remediation planning","Create phased remediation plan from priority matrix","planner","all","remediate","TDEVAL-001","TDEVAL-001","csv-wave","3","pending","","0","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (TDPREFIX-NNN) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description with scope and context |
| `role` | Input | Worker role: scanner, assessor, planner, executor, validator |
| `debt_dimension` | Input | `all`, `code`, `architecture`, `testing`, `dependency`, `documentation` |
| `pipeline_mode` | Input | `scan`, `remediate`, `targeted` |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or execution notes (max 500 chars) |
| `debt_items_count` | Output | Number of debt items found/fixed/validated |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `error` | Output | Error message if failed |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Plan Approver | agents/plan-approver.md | 2.3 (send_input cycle) | Review remediation plan, approve/revise/abort | pre-wave (before TDFIX) |
| GC Loop Manager | agents/gc-loop-manager.md | 2.3 (send_input cycle) | Manage fix-verify loop, create retry tasks | post-wave (after TDVAL) |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding agent.md** to reload.

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state -- all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 4 |
| `discoveries.ndjson` | Shared exploration board (all agents) | Append-only, carries across waves |
| `context.md` | Human-readable report with debt metrics | Created in Phase 4 |
| `scan/debt-inventory.json` | Scanner output: structured debt inventory | Created by TDSCAN |
| `assessment/priority-matrix.json` | Assessor output: prioritized debt items | Created by TDEVAL |
| `plan/remediation-plan.md` | Planner output: phased fix plan | Created by TDPLAN |
| `plan/remediation-plan.json` | Planner output: machine-readable plan | Created by TDPLAN |
| `fixes/fix-log.json` | Executor output: fix results | Created by TDFIX |
| `validation/validation-report.json` | Validator output: validation results | Created by TDVAL |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state
+-- results.csv                # Final results
+-- discoveries.ndjson         # Shared discovery board
+-- context.md                 # Human-readable report
+-- wave-{N}.csv               # Temporary per-wave input
+-- scan/
|   +-- debt-inventory.json    # Scanner output
+-- assessment/
|   +-- priority-matrix.json   # Assessor output
+-- plan/
|   +-- remediation-plan.md    # Planner output (human)
|   +-- remediation-plan.json  # Planner output (machine)
+-- fixes/
|   +-- fix-log.json           # Executor output
+-- validation/
|   +-- validation-report.json # Validator output
+-- interactive/
|   +-- {id}-result.json       # Interactive task results
+-- wisdom/
    +-- learnings.md
    +-- decisions.md
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

// Detect pipeline mode
let pipelineMode = 'remediate'
if ($ARGUMENTS.includes('--mode=scan')) pipelineMode = 'scan'
else if ($ARGUMENTS.includes('--mode=targeted')) pipelineMode = 'targeted'

const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+|--mode=\w+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `td-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/scan ${sessionFolder}/assessment ${sessionFolder}/plan ${sessionFolder}/fixes ${sessionFolder}/validation ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')
Write(`${sessionFolder}/wisdom/learnings.md`, '# Learnings\n')
Write(`${sessionFolder}/wisdom/decisions.md`, '# Decisions\n')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse mode, clarify scope, prepare pipeline configuration.

**Workflow**:

1. **Detect mode from arguments** (--mode=scan/remediate/targeted) or from keywords:

| Keywords | Mode |
|----------|------|
| scan, audit, assess | scan |
| targeted, specific, fix known | targeted |
| Default | remediate |

2. **Clarify scope** (skip if AUTO_YES):
   ```javascript
   AskUserQuestion({
     questions: [{
       question: "Tech debt governance scope:",
       header: "Scope Selection",
       multiSelect: false,
       options: [
         { label: "Full project scan", description: "Scan entire codebase" },
         { label: "Specific module", description: "Target specific directory" },
         { label: "Custom scope", description: "Specify file patterns" }
       ]
     }]
   })
   ```

3. **Detect debt dimensions** from task description:

| Keywords | Dimension |
|----------|-----------|
| code quality, complexity, smell | code |
| architecture, coupling, structure | architecture |
| test, coverage, quality | testing |
| dependency, outdated, vulnerable | dependency |
| documentation, api doc, comments | documentation |
| Default | all |

4. **Output**: pipeline mode, scope, focus dimensions

**Success Criteria**:
- Pipeline mode determined
- Scope and dimensions clarified

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Build task chain based on pipeline mode, generate tasks.csv.

**Pipeline Definitions**:

| Mode | Task Chain |
|------|------------|
| scan | TDSCAN-001 -> TDEVAL-001 |
| remediate | TDSCAN-001 -> TDEVAL-001 -> TDPLAN-001 -> (plan-approval) -> TDFIX-001 -> TDVAL-001 |
| targeted | TDPLAN-001 -> (plan-approval) -> TDFIX-001 -> TDVAL-001 |

**Task Registry**:

| Task ID | Role | Prefix | exec_mode | Wave | Description |
|---------|------|--------|-----------|------|-------------|
| TDSCAN-001 | scanner | TDSCAN | csv-wave | 1 | Multi-dimension codebase scan |
| TDEVAL-001 | assessor | TDEVAL | csv-wave | 2 | Severity assessment with priority matrix |
| PLAN-APPROVE | - | - | interactive | 3 (pre-wave) | Plan approval checkpoint |
| TDPLAN-001 | planner | TDPLAN | csv-wave | 3 | Phased remediation plan |
| TDFIX-001 | executor | TDFIX | csv-wave | 4 | Worktree-based incremental fixes |
| TDVAL-001 | validator | TDVAL | csv-wave | 5 | 4-layer validation |

**Worktree Creation** (before TDFIX, remediate mode):
```bash
git worktree add .worktrees/td-<slug>-<date> -b tech-debt/td-<slug>-<date>
```

**Wave Computation**: Linear chain, waves assigned by position in pipeline.

**User Validation**: Display pipeline with mode and task chain (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with correct pipeline chain
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with checkpoints and GC loop support.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
const maxWave = Math.max(...tasks.map(t => t.wave))
let gcRounds = 0
const MAX_GC_ROUNDS = 3

for (let wave = 1; wave <= maxWave; wave++) {
  const waveTasks = tasks.filter(t => t.wave === wave && t.status === 'pending')
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')

  // Check dependencies
  for (const task of waveTasks) {
    const depIds = (task.deps || '').split(';').filter(Boolean)
    const depStatuses = depIds.map(id => tasks.find(t => t.id === id)?.status)
    if (depStatuses.some(s => s === 'failed' || s === 'skipped')) {
      task.status = 'skipped'
      task.error = `Dependency failed`
    }
  }

  // Pre-wave interactive: Plan Approval Gate (after TDPLAN completes)
  if (interactiveTasks.some(t => t.id === 'PLAN-APPROVE' && t.status === 'pending')) {
    Read('agents/plan-approver.md')
    const planTask = interactiveTasks.find(t => t.id === 'PLAN-APPROVE')

    const agent = spawn_agent({
      message: `## PLAN REVIEW\n\n### MANDATORY FIRST STEPS\n1. Read: ${sessionFolder}/plan/remediation-plan.md\n2. Read: ${sessionFolder}/discoveries.ndjson\n\nReview the remediation plan and decide: Approve / Revise / Abort\n\nSession: ${sessionFolder}`
    })
    const result = wait({ ids: [agent], timeout_ms: 600000 })

    // Parse decision
    if (result includes "Abort") {
      // Skip remaining pipeline
      for (const t of tasks.filter(t => t.status === 'pending')) t.status = 'skipped'
    } else if (result includes "Revise") {
      // Create revision task, re-run planner
      // ... create TDPLAN-revised task
    }
    // Approve: continue normally

    close_agent({ id: agent })
    planTask.status = 'completed'

    // Create worktree for fix execution
    if (pipelineMode === 'remediate' || pipelineMode === 'targeted') {
      Bash(`git worktree add .worktrees/${sessionId} -b tech-debt/${sessionId}`)
    }
  }

  // Execute csv-wave tasks
  const pendingCsvTasks = csvTasks.filter(t => t.status === 'pending')
  for (const task of pendingCsvTasks) {
    task.prev_context = buildPrevContext(task, tasks)
  }

  if (pendingCsvTasks.length > 0) {
    Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingCsvTasks))

    // Select instruction based on role
    const role = pendingCsvTasks[0].role
    const instruction = Read(`instructions/agent-instruction.md`)
    // Customize instruction for role (scanner/assessor/planner/executor/validator)

    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: buildRoleInstruction(role, sessionFolder, wave),
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          debt_items_count: { type: "string" },
          artifacts_produced: { type: "string" },
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

  // Post-wave: TDVAL GC Loop Check
  const completedVal = tasks.find(t => t.id.startsWith('TDVAL') && t.status === 'completed' && t.wave === wave)
  if (completedVal) {
    // Read validation results
    const valReport = JSON.parse(Read(`${sessionFolder}/validation/validation-report.json`))

    if (!valReport.passed && gcRounds < MAX_GC_ROUNDS) {
      gcRounds++
      // Create fix-verify retry tasks
      const fixId = `TDFIX-fix-${gcRounds}`
      const valId = `TDVAL-recheck-${gcRounds}`
      tasks.push({
        id: fixId, title: `Fix regressions (GC #${gcRounds})`, role: 'executor',
        description: `Fix regressions found in validation round ${gcRounds}`,
        debt_dimension: 'all', pipeline_mode: pipelineMode,
        deps: completedVal.id, context_from: completedVal.id,
        exec_mode: 'csv-wave', wave: wave + 1, status: 'pending',
        findings: '', debt_items_count: '0', artifacts_produced: '', error: ''
      })
      tasks.push({
        id: valId, title: `Revalidate (GC #${gcRounds})`, role: 'validator',
        description: `Revalidate after fix round ${gcRounds}`,
        debt_dimension: 'all', pipeline_mode: pipelineMode,
        deps: fixId, context_from: fixId,
        exec_mode: 'csv-wave', wave: wave + 2, status: 'pending',
        findings: '', debt_items_count: '0', artifacts_produced: '', error: ''
      })
      // Extend maxWave
    } else if (!valReport.passed && gcRounds >= MAX_GC_ROUNDS) {
      // Accept current state
      console.log(`Max GC rounds (${MAX_GC_ROUNDS}) reached. Accepting current state.`)
    }
  }

  // Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)
}
```

**Success Criteria**:
- All waves executed in order
- Plan approval checkpoint enforced before fix execution
- GC loop properly bounded (max 3 rounds)
- Worktree created for fix execution
- discoveries.ndjson accumulated across all waves

---

### Phase 3: Post-Wave Interactive (Completion + PR)

**Objective**: Create PR from worktree if validation passed, generate debt reduction report.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const allCompleted = tasks.every(t => t.status === 'completed' || t.status === 'skipped')

// PR Creation (if worktree exists and validation passed)
const worktreePath = `.worktrees/${sessionId}`
const valReport = JSON.parse(Read(`${sessionFolder}/validation/validation-report.json`) || '{}')
if (valReport.passed && fileExists(worktreePath)) {
  Bash(`cd ${worktreePath} && git add -A && git commit -m "tech-debt: remediate debt items (${sessionId})" && git push -u origin tech-debt/${sessionId}`)
  Bash(`gh pr create --title "Tech Debt Remediation: ${sessionId}" --body "Automated tech debt cleanup. See ${sessionFolder}/context.md for details."`)
  Bash(`git worktree remove ${worktreePath}`)
}

// Debt reduction metrics
const scanReport = JSON.parse(Read(`${sessionFolder}/scan/debt-inventory.json`) || '{}')
const debtBefore = scanReport.total_items || 0
const debtAfter = valReport.debt_score_after || 0
const reductionRate = debtBefore > 0 ? Math.round(((debtBefore - debtAfter) / debtBefore) * 100) : 0

console.log(`
============================================
TECH DEBT GOVERNANCE COMPLETE

Mode: ${pipelineMode}
Debt Items Found: ${debtBefore}
Debt Items Fixed: ${debtBefore - debtAfter}
Reduction Rate: ${reductionRate}%
GC Rounds: ${gcRounds}/${MAX_GC_ROUNDS}
Validation: ${valReport.passed ? 'PASSED' : 'FAILED'}

Session: ${sessionFolder}
============================================
`)

// Completion action
if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "What next?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "New target", description: "Run another scan/fix cycle" },
        { label: "Deep fix", description: "Continue fixing remaining items" },
        { label: "Close", description: "Archive session" }
      ]
    }]
  })
}
```

**Success Criteria**:
- PR created if applicable
- Debt metrics calculated and reported
- User informed of next steps

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

let contextMd = `# Tech Debt Governance Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Mode**: ${pipelineMode}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Debt Metrics\n`
contextMd += `| Metric | Value |\n|--------|-------|\n`
contextMd += `| Items Found | ${debtBefore} |\n`
contextMd += `| Items Fixed | ${debtBefore - debtAfter} |\n`
contextMd += `| Reduction Rate | ${reductionRate}% |\n`
contextMd += `| GC Rounds | ${gcRounds} |\n`
contextMd += `| Validation | ${valReport.passed ? 'PASSED' : 'FAILED'} |\n\n`

contextMd += `## Pipeline Execution\n\n`
for (const t of tasks) {
  const icon = t.status === 'completed' ? '[DONE]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
  contextMd += `${icon} **${t.title}** [${t.role}] ${t.findings || ''}\n\n`
}

Write(`${sessionFolder}/context.md`, contextMd)
```

**Success Criteria**:
- results.csv exported
- context.md generated with debt metrics
- Summary displayed to user

---

## Shared Discovery Board Protocol

**Format**: NDJSON (one JSON per line)

**Discovery Types**:

| Type | Dedup Key | Data Schema | Description |
|------|-----------|-------------|-------------|
| `debt_item_found` | `data.file+data.line` | `{id, dimension, severity, file, line, description, suggestion}` | Tech debt item identified |
| `pattern_found` | `data.pattern_name+data.location` | `{pattern_name, location, description}` | Code pattern (anti-pattern) found |
| `fix_applied` | `data.file+data.change` | `{file, change, lines_modified, debt_id}` | Fix applied to debt item |
| `regression_found` | `data.file+data.test` | `{file, test, description, severity}` | Regression found during validation |
| `dependency_issue` | `data.package+data.issue` | `{package, current, latest, issue, severity}` | Dependency problem |
| `metric_recorded` | `data.metric` | `{metric, value, dimension, file}` | Quality metric recorded |

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"TDSCAN-001","type":"debt_item_found","data":{"id":"TD-001","dimension":"code","severity":"high","file":"src/auth/jwt.ts","line":42,"description":"Complexity > 15","suggestion":"Extract helper functions"}}
{"ts":"2026-03-08T10:15:00Z","worker":"TDFIX-001","type":"fix_applied","data":{"file":"src/auth/jwt.ts","change":"Extracted 3 helper functions","lines_modified":25,"debt_id":"TD-001"}}
```

---

## Checkpoints

| Checkpoint | Trigger | Condition | Action |
|------------|---------|-----------|--------|
| Plan Approval Gate | TDPLAN-001 completes | Always (remediate/targeted mode) | Interactive: Approve / Revise / Abort |
| Worktree Creation | Plan approved | Before TDFIX | `git worktree add .worktrees/{session-id}` |
| Fix-Verify GC Loop | TDVAL-* completes | Regressions found | Create TDFIX-fix-N + TDVAL-recheck-N (max 3 rounds) |

---

## Pipeline Mode Details

### Scan Mode
```
Wave 1: TDSCAN-001 (scanner) -> Scan 5 dimensions
Wave 2: TDEVAL-001 (assessor) -> Priority matrix
```

### Remediate Mode (Full Pipeline)
```
Wave 1: TDSCAN-001 (scanner) -> Scan 5 dimensions
Wave 2: TDEVAL-001 (assessor) -> Priority matrix
Wave 3: TDPLAN-001 (planner) -> Remediation plan
         PLAN-APPROVE (interactive) -> User approval
Wave 4: TDFIX-001 (executor) -> Apply fixes in worktree
Wave 5: TDVAL-001 (validator) -> 4-layer validation
         [GC Loop: TDFIX-fix-N -> TDVAL-recheck-N, max 3]
```

### Targeted Mode
```
Wave 1: TDPLAN-001 (planner) -> Targeted fix plan
         PLAN-APPROVE (interactive) -> User approval
Wave 2: TDFIX-001 (executor) -> Apply fixes in worktree
Wave 3: TDVAL-001 (validator) -> 4-layer validation
         [GC Loop: TDFIX-fix-N -> TDVAL-recheck-N, max 3]
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| CSV agent timeout | Mark as failed in results, continue with wave |
| CSV agent failed | Mark as failed, skip dependent tasks in later waves |
| Interactive agent timeout | Urge convergence via send_input, then close if still timed out |
| Scanner finds no debt | Report clean codebase, skip to summary |
| Plan rejected by user | Abort pipeline or create revision task |
| Fix-verify loop stuck (>3 rounds) | Accept current state, continue to completion |
| Worktree creation fails | Fall back to direct changes with user confirmation |
| Validation tools not available | Skip unavailable checks, report partial validation |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive for approval checkpoints
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If a dependency failed, skip the dependent task
8. **GC Loop Bounded**: Maximum 3 fix-verify rounds before accepting current state
9. **Worktree Isolation**: All fix execution happens in git worktree, not main branch
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
