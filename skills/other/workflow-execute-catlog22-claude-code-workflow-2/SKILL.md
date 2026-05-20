---
name: workflow-execute
description: |
  Autonomous workflow execution pipeline with CSV wave engine.
  Session discovery → plan validation → IMPL-*.json → CSV conversion →
  wave execution via spawn_agents_on_csv → results sync.
  Task JSONs remain the rich data source; CSV is brief + execution state.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--resume-session=ID] [--with-commit]"
allowed-tools: spawn_agents_on_csv, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

## Auto Mode

When `--yes` or `-y`: Auto-select first session, auto-complete session after all tasks, skip all confirmations.

# Workflow Execute

## Usage

```bash
$workflow-execute
$workflow-execute --yes
$workflow-execute --resume-session=WFS-auth
$workflow-execute -y --with-commit
$workflow-execute -y -c 4 --with-commit
$workflow-execute -y --with-commit --resume-session=WFS-auth
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents per wave (default: 4)
- `--resume-session=ID`: Resume specific session (skip Phase 1-2)
- `--with-commit`: Auto-commit after each task completion

---

## Overview

Autonomous execution pipeline using `spawn_agents_on_csv` wave engine. Converts planning artifacts (IMPL-*.json + plan.json) into CSV for wave-based parallel execution, with full task JSON available via `task_json_path` column.

```
┌──────────────────────────────────────────────────────────────────┐
│                    WORKFLOW EXECUTE PIPELINE                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Phase 1: Session Discovery                                       │
│     ├─ Find active sessions                                       │
│     ├─ Auto-select (1 session) or prompt (multiple)              │
│     └─ Load session metadata                                      │
│                                                                    │
│  Phase 2: Planning Document Validation                            │
│     ├─ Verify IMPL_PLAN.md exists                                 │
│     ├─ Verify TODO_LIST.md exists                                 │
│     └─ Verify .task/ contains IMPL-*.json                        │
│                                                                    │
│  Phase 3: JSON → CSV Conversion                                   │
│     ├─ Read all IMPL-*.json + plan.json                          │
│     ├─ Skip already-completed tasks (resume support)             │
│     ├─ Compute waves via Kahn's BFS (deps + plan hints)          │
│     ├─ Generate tasks.csv (21 cols) + context.csv                │
│     └─ Initialize discoveries.ndjson                              │
│                                                                    │
│  Phase 4: Wave Execute (spawn_agents_on_csv)                      │
│     ├─ Per wave: build prev_context → wave-{N}.csv               │
│     ├─ spawn_agents_on_csv with execute instruction               │
│     ├─ Merge results → tasks.csv + task JSON status              │
│     ├─ Auto-commit per task (if --with-commit)                   │
│     └─ Cleanup temp wave CSVs                                     │
│                                                                    │
│  Phase 5: Results Sync                                            │
│     ├─ Export results.csv                                         │
│     ├─ Reconcile TODO_LIST.md with tasks.csv status              │
│     └─ User choice: Review | Complete Session                    │
│                                                                    │
│  Phase 6: Post-Implementation Review (Optional)                  │
│     ├─ Select review type (quality/security/architecture)        │
│     ├─ CLI-assisted analysis                                      │
│     └─ Generate REVIEW-{type}.md                                 │
│                                                                    │
│  Resume Mode (--resume-session):                                  │
│     └─ Skip Phase 1-2 → enter Phase 3 (skip completed tasks)    │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## CSV Schemas

### tasks.csv (21 columns)

```csv
id,title,description,agent,scope,deps,execution_group,context_from,wave,task_json_path,hints,execution_directives,acceptance_criteria,prev_context,status,findings,files_modified,tests_passed,acceptance_met,summary_path,error
```

| Column | Phase | Source | Description |
|--------|-------|--------|-------------|
| `id` | Input | task.id | IMPL-001 etc |
| `title` | Input | task.title | Short title |
| `description` | Input | task.description | Full description |
| `agent` | Input | meta.agent or inferred | @code-developer etc |
| `scope` | Input | task.scope / focus_paths | File scope glob |
| `deps` | Input | depends_on.join(';') | Dependency IDs (semicolon-separated) |
| `execution_group` | Input | meta.execution_group | Parallel group identifier |
| `context_from` | Computed | deps + completed predecessors | Context source IDs |
| `wave` | Computed | Kahn's BFS | Wave number (1-based) |
| `task_json_path` | Input | relative path | `.task/IMPL-001.json` (agent reads full JSON) |
| `hints` | Input | artifacts + pre_analysis refs | `tips \|\| file1;file2` |
| `execution_directives` | Input | convergence.verification | Verification commands |
| `acceptance_criteria` | Input | convergence.criteria.join | Acceptance conditions |
| `prev_context` | Computed(per-wave) | context_from findings lookup | Predecessor task findings |
| `status` | Output | agent result | pending→completed/failed/skipped |
| `findings` | Output | agent result | Key findings (max 500 chars) |
| `files_modified` | Output | agent result | Modified files (semicolon-separated) |
| `tests_passed` | Output | agent result | true/false |
| `acceptance_met` | Output | agent result | Acceptance status |
| `summary_path` | Output | generated | .summaries/IMPL-X-summary.md |
| `error` | Output | agent result | Error message |

**Key design**: `task_json_path` lets agents read the full task JSON (with pre_analysis, flow_control, convergence etc). CSV is "brief + execution state".

### context.csv (4 columns)

```csv
key,type,value,source
"tech_stack","array","TypeScript;React 18;Zustand","plan.json"
"conventions","array","Use useIntl;Barrel exports","plan.json"
"context_package_path","path",".process/context-package.json","session"
"discoveries_path","path","discoveries.ndjson","session"
```

Injected into instruction template as static context — avoids each agent rediscovering project basics.

---

## Session Structure

```
.workflow/active/WFS-{session}/
├── workflow-session.json        # Session state
├── plan.json                    # Structured plan (machine-readable)
├── IMPL_PLAN.md                 # Implementation plan (human-readable)
├── TODO_LIST.md                 # Progress tracking (Phase 5 sync)
├── tasks.csv                    # Phase 3 generated, Phase 4 updated
├── context.csv                  # Phase 3 generated
├── results.csv                  # Phase 5 exported
├── discoveries.ndjson           # Phase 3 initialized, Phase 4 agents append
├── .task/                       # Task definitions (unchanged)
│   ├── IMPL-1.json
│   └── IMPL-N.json
├── .summaries/                  # Agent-generated summaries
│   ├── IMPL-1-summary.md
│   └── IMPL-N-summary.md
├── .process/context-package.json# Unchanged
└── wave-{N}.csv                 # Phase 4 temporary (cleaned after each wave)
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const withCommit = $ARGUMENTS.includes('--with-commit')
const resumeMatch = $ARGUMENTS.match(/--resume-session[=\s]+(\S+)/)
const resumeSessionId = resumeMatch ? resumeMatch[1] : null
const isResumeMode = !!resumeSessionId
const concurrencyMatch = $ARGUMENTS.match(/(?:--concurrency|-c)\s+(\d+)/)
const maxConcurrency = concurrencyMatch ? parseInt(concurrencyMatch[1]) : 4
```

---

### Phase 1: Session Discovery

**Applies to**: Normal mode only (skipped if `--resume-session`).

```javascript
let sessionId, sessionFolder

if (isResumeMode) {
  sessionId = resumeSessionId
  sessionFolder = `.workflow/active/${sessionId}`
  // Skip to Phase 3
} else {
  const sessions = Bash(`ls -d .workflow/active/WFS-* 2>/dev/null`).trim().split('\n').filter(Boolean)

  if (sessions.length === 0) {
    console.log('ERROR: No active workflow sessions found.')
    console.log('Run $workflow-plan "task description" to create a session.')
    return
  }

  if (sessions.length === 1) {
    sessionFolder = sessions[0]
    sessionId = sessionFolder.split('/').pop()
    console.log(`Auto-selected session: ${sessionId}`)
  } else {
    if (AUTO_YES) {
      sessionFolder = sessions[0]
      sessionId = sessionFolder.split('/').pop()
      console.log(`[--yes] Auto-selected: ${sessionId}`)
    } else {
      const sessionInfos = sessions.slice(0, 4).map(s => {
        const id = s.split('/').pop()
        const total = parseInt(Bash(`grep -c '^- \\[' "${s}/TODO_LIST.md" 2>/dev/null || echo 0`).trim()) || 0
        const done = parseInt(Bash(`grep -c '^- \\[x\\]' "${s}/TODO_LIST.md" 2>/dev/null || echo 0`).trim()) || 0
        return { id, path: s, progress: `${done}/${total} tasks` }
      })

      const answer = AskUserQuestion({
        questions: [{
          question: "Select session to execute:",
          header: "Session",
          multiSelect: false,
          options: sessionInfos.map(s => ({
            label: s.id,
            description: s.progress
          }))
        }]
      })
      sessionId = answer.Session
      sessionFolder = `.workflow/active/${sessionId}`
    }
  }
}
```

---

### Phase 2: Planning Document Validation

**Applies to**: Normal mode only.

```javascript
if (!isResumeMode) {
  const checks = {
    'IMPL_PLAN.md': Bash(`test -f "${sessionFolder}/IMPL_PLAN.md" && echo yes`).trim() === 'yes',
    'TODO_LIST.md': Bash(`test -f "${sessionFolder}/TODO_LIST.md" && echo yes`).trim() === 'yes',
    '.task/ has files': parseInt(Bash(`ls ${sessionFolder}/.task/IMPL-*.json 2>/dev/null | wc -l`).trim()) > 0
  }

  const missing = Object.entries(checks).filter(([_, ok]) => !ok).map(([name]) => name)
  if (missing.length > 0) {
    console.log(`ERROR: Missing planning documents: ${missing.join(', ')}`)
    console.log(`Run $workflow-plan --session ${sessionId} to generate plan.`)
    return
  }

  console.log(`Planning documents validated.`)
}
```

---

### Phase 3: JSON → CSV Conversion

**Applies to**: Both normal and resume modes (resume entry point).

**Objective**: Convert IMPL-*.json + plan.json into tasks.csv + context.csv with computed waves.

```javascript
console.log(`\n## Phase 3: JSON → CSV Conversion\n`)

// Update session status to active
Bash(`cd "${sessionFolder}" && jq '.status = "active" | .execution_started_at = (.execution_started_at // "'"$(date -Iseconds)"'")' workflow-session.json > tmp.json && mv tmp.json workflow-session.json 2>/dev/null || true`)
Bash(`mkdir -p "${sessionFolder}/.summaries"`)

// 3.1: Read all IMPL-*.json
const taskFiles = Bash(`ls ${sessionFolder}/.task/IMPL-*.json 2>/dev/null`).trim().split('\n').filter(Boolean)
if (taskFiles.length === 0) {
  console.log('ERROR: No task JSONs found in .task/')
  return
}

const taskJsons = taskFiles.map(f => {
  const content = Read(f)
  const json = JSON.parse(content)
  json._filePath = f
  // Fallback: derive id from filename if missing
  if (!json.id) {
    json.id = f.split('/').pop().replace('.json', '')
  }
  return json
})

// 3.2: Skip completed tasks (resume support)
const todoContent = Read(`${sessionFolder}/TODO_LIST.md`)
const completedIds = new Set()
const todoLines = todoContent.match(/^- \[x\] (IMPL-\d+(?:\.\d+)?)/gm) || []
todoLines.forEach(line => {
  const match = line.match(/IMPL-\d+(?:\.\d+)?/)
  if (match) completedIds.add(match[0])
})

// Also check task JSON status field
taskJsons.forEach(tj => {
  if (tj.status === 'completed') completedIds.add(tj.id)
})

const pendingJsons = taskJsons.filter(tj => !completedIds.has(tj.id))

console.log(`  Total tasks: ${taskJsons.length}`)
console.log(`  Already completed: ${completedIds.size}`)
console.log(`  Pending: ${pendingJsons.length}`)

if (pendingJsons.length === 0) {
  console.log(`\nAll tasks already completed. Proceeding to Phase 5.`)
  // → Jump to Phase 5
}

// 3.3: Read plan.json for execution hints
const planJsonPath = `${sessionFolder}/plan.json`
const planJsonExists = Bash(`test -f "${planJsonPath}" && echo yes`).trim() === 'yes'
const planJson = planJsonExists ? JSON.parse(Read(planJsonPath) || '{}') : {}

// 3.4: Extract fields from task JSONs (handles two schema variants)
function resolveAgent(tj) {
  if (tj.meta?.agent) return tj.meta.agent
  const typeMap = {
    'feature': 'code-developer',
    'test-gen': 'code-developer',
    'test-fix': 'test-fix-agent',
    'review': 'universal-executor',
    'docs': 'doc-generator'
  }
  return typeMap[tj.meta?.type] || 'code-developer'
}

function extractDeps(tj) {
  return tj.depends_on || tj.context?.depends_on || []
}

function buildHints(tj) {
  const tips = []
  const files = []
  // Gather artifact references
  if (tj.artifacts) {
    tj.artifacts.forEach(a => { if (a.path) files.push(a.path) })
  }
  // Gather pre_analysis Read references
  if (tj.pre_analysis) {
    tj.pre_analysis.forEach(step => {
      if (step.tool === 'Read' && step.path) files.push(step.path)
    })
  }
  // Gather tips from meta or context
  if (tj.meta?.hints) tips.push(tj.meta.hints)
  if (tj.context?.tips) tips.push(tj.context.tips)

  const tipsStr = tips.join('; ')
  const filesStr = files.join(';')
  if (tipsStr && filesStr) return `${tipsStr} || ${filesStr}`
  if (tipsStr) return tipsStr
  if (filesStr) return `|| ${filesStr}`
  return ''
}

function extractDirectives(tj) {
  if (tj.convergence?.verification) {
    return Array.isArray(tj.convergence.verification)
      ? tj.convergence.verification.join('; ')
      : tj.convergence.verification
  }
  if (tj.execution_config?.verification_command) return tj.execution_config.verification_command
  return ''
}

function extractAcceptance(tj) {
  if (tj.convergence?.criteria) {
    return Array.isArray(tj.convergence.criteria)
      ? tj.convergence.criteria.join('; ')
      : tj.convergence.criteria
  }
  if (tj.context?.acceptance) {
    return Array.isArray(tj.context.acceptance)
      ? tj.context.acceptance.join('; ')
      : tj.context.acceptance
  }
  return ''
}

function extractScope(tj) {
  if (tj.scope) return tj.scope
  if (tj.focus_paths) {
    return Array.isArray(tj.focus_paths) ? tj.focus_paths.join(';') : tj.focus_paths
  }
  return ''
}

// Build task rows (all tasks — completed ones carry status forward)
const taskRows = taskJsons.map(tj => ({
  id: tj.id,
  title: tj.title || '',
  description: tj.description || '',
  agent: resolveAgent(tj),
  scope: extractScope(tj),
  deps: extractDeps(tj).join(';'),
  execution_group: tj.meta?.execution_group || '',
  context_from: '',  // computed after wave assignment
  task_json_path: `.task/${tj.id}.json`,
  hints: buildHints(tj),
  execution_directives: extractDirectives(tj),
  acceptance_criteria: extractAcceptance(tj),
  prev_context: '',  // computed per-wave in Phase 4
  status: completedIds.has(tj.id) ? 'completed' : 'pending',
  findings: '',
  files_modified: '',
  tests_passed: '',
  acceptance_met: '',
  summary_path: `.summaries/${tj.id}-summary.md`,
  error: ''
}))

// 3.5: Compute waves via Kahn's BFS with plan.json hints
function computeWaves(rows, planJson) {
  const taskMap = new Map(rows.map(r => [r.id, r]))
  const inDegree = new Map(rows.map(r => [r.id, 0]))
  const adjList = new Map(rows.map(r => [r.id, []]))

  for (const row of rows) {
    const deps = row.deps.split(';').filter(Boolean)
    for (const dep of deps) {
      if (taskMap.has(dep)) {
        adjList.get(dep).push(row.id)
        inDegree.set(row.id, inDegree.get(row.id) + 1)
      }
    }
  }

  // BFS
  const queue = []
  const waveMap = new Map()

  for (const [id, deg] of inDegree) {
    if (deg === 0) {
      queue.push([id, 1])
      waveMap.set(id, 1)
    }
  }

  let maxWave = 1
  let idx = 0
  while (idx < queue.length) {
    const [current, depth] = queue[idx++]
    for (const next of adjList.get(current)) {
      const newDeg = inDegree.get(next) - 1
      inDegree.set(next, newDeg)
      const nextDepth = Math.max(waveMap.get(next) || 0, depth + 1)
      waveMap.set(next, nextDepth)
      if (newDeg === 0) {
        queue.push([next, nextDepth])
        maxWave = Math.max(maxWave, nextDepth)
      }
    }
  }

  // Check for unassigned (circular deps)
  for (const row of rows) {
    if (!waveMap.has(row.id)) {
      console.log(`WARNING: Circular dependency involving ${row.id}, assigning to wave ${maxWave + 1}`)
      waveMap.set(row.id, maxWave + 1)
      maxWave = maxWave + 1
    }
  }

  // Apply plan.json execution_graph hints if available
  if (planJson.execution_graph?.phases) {
    planJson.execution_graph.phases.forEach((phase, idx) => {
      const phaseWave = idx + 1
      const taskIds = phase.tasks || phase.task_ids || []
      taskIds.forEach(id => {
        if (waveMap.has(id)) {
          // Only shift to later wave (never earlier — respect deps)
          if (phaseWave > waveMap.get(id)) {
            waveMap.set(id, phaseWave)
          }
        }
      })
    })
    maxWave = Math.max(maxWave, ...waveMap.values())
  }

  return { waveMap, maxWave }
}

const { waveMap, maxWave } = computeWaves(taskRows, planJson)

// Assign wave + context_from
taskRows.forEach(row => {
  row.wave = waveMap.get(row.id) || 1
  // context_from = deps + already-completed IDs for resume context
  const depIds = row.deps.split(';').filter(Boolean)
  const contextIds = [...new Set([...depIds, ...[...completedIds].filter(id => id !== row.id)])]
  row.context_from = contextIds.join(';')
})

// 3.6: Write tasks.csv
function csvEscape(val) {
  return `"${String(val).replace(/"/g, '""')}"`
}

const tasksCsvHeader = 'id,title,description,agent,scope,deps,execution_group,context_from,wave,task_json_path,hints,execution_directives,acceptance_criteria,prev_context,status,findings,files_modified,tests_passed,acceptance_met,summary_path,error'
const tasksCsvRows = taskRows.map(r =>
  [r.id, r.title, r.description, r.agent, r.scope, r.deps, r.execution_group,
   r.context_from, r.wave, r.task_json_path, r.hints, r.execution_directives,
   r.acceptance_criteria, r.prev_context, r.status, r.findings, r.files_modified,
   r.tests_passed, r.acceptance_met, r.summary_path, r.error]
    .map(csvEscape).join(',')
)
Write(`${sessionFolder}/tasks.csv`, [tasksCsvHeader, ...tasksCsvRows].join('\n'))

// 3.7: Write context.csv
const contextRows = ['key,type,value,source']
if (planJson.tech_stack) {
  const stack = Array.isArray(planJson.tech_stack) ? planJson.tech_stack.join(';') : planJson.tech_stack
  contextRows.push(`"tech_stack","array","${stack}","plan.json"`)
}
if (planJson.conventions) {
  const conv = Array.isArray(planJson.conventions) ? planJson.conventions.join(';') : planJson.conventions
  contextRows.push(`"conventions","array","${conv}","plan.json"`)
}
const ctxPkgExists = Bash(`test -f "${sessionFolder}/.process/context-package.json" && echo yes`).trim() === 'yes'
if (ctxPkgExists) {
  contextRows.push(`"context_package_path","path",".process/context-package.json","session"`)
}
contextRows.push(`"discoveries_path","path","discoveries.ndjson","session"`)
Write(`${sessionFolder}/context.csv`, contextRows.join('\n'))

// 3.8: Initialize discoveries.ndjson
Bash(`touch "${sessionFolder}/discoveries.ndjson"`)

// 3.9: User validation (skip if AUTO_YES)
if (!AUTO_YES) {
  const pendingRows = taskRows.filter(r => r.status === 'pending')
  console.log(`\n## Wave Execution Plan\n`)
  console.log(`  Tasks: ${pendingRows.length} pending across ${maxWave} waves\n`)
  for (let w = 1; w <= maxWave; w++) {
    const waveTasks = pendingRows.filter(r => r.wave === w)
    if (waveTasks.length === 0) continue
    console.log(`  Wave ${w}: ${waveTasks.map(t => `${t.id}(${t.agent})`).join(', ')}`)
  }

  const answer = AskUserQuestion({
    questions: [{
      question: `Proceed with ${pendingRows.length} tasks across ${maxWave} waves?`,
      header: "Confirm",
      multiSelect: false,
      options: [
        { label: "Execute", description: "Proceed with wave execution" },
        { label: "Modify", description: `Edit ${sessionFolder}/tasks.csv then --resume-session` },
        { label: "Cancel", description: "Abort" }
      ]
    }]
  })

  if (answer.Confirm === "Modify") {
    console.log(`Edit: ${sessionFolder}/tasks.csv\nResume: $workflow-execute --resume-session=${sessionId}`)
    return
  } else if (answer.Confirm === "Cancel") {
    return
  }
}

console.log(`\n  tasks.csv: ${taskRows.length} rows (${pendingJsons.length} pending)`)
console.log(`  context.csv: ${contextRows.length - 1} entries`)
console.log(`  Wave plan: ${maxWave} waves`)
```

---

### Phase 4: Wave Execute (spawn_agents_on_csv)

**Objective**: Execute tasks wave-by-wave via `spawn_agents_on_csv`. Each wave builds `prev_context` from completed predecessors.

```javascript
console.log(`\n## Phase 4: Wave Execute\n`)

// Determine concurrency from plan.json or flag
let effectiveConcurrency = maxConcurrency
if (planJson.recommended_execution === 'Sequential') {
  effectiveConcurrency = 1
  console.log(`  Sequential mode (from plan.json), concurrency: 1`)
} else {
  console.log(`  Parallel mode, concurrency: ${effectiveConcurrency}`)
}

// Read context.csv for instruction injection
const contextCsvContent = Read(`${sessionFolder}/context.csv`)
const contextEntries = parseCsv(contextCsvContent)
const contextBlock = contextEntries.map(e => `- **${e.key}** (${e.type}): ${e.value}`).join('\n')

const failedIds = new Set()
const skippedIds = new Set()

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\n### Wave ${wave}/${maxWave}\n`)

  // Re-read master CSV for current state
  const masterCsv = parseCsv(Read(`${sessionFolder}/tasks.csv`))
  const waveTasks = masterCsv.filter(row =>
    parseInt(row.wave) === wave && row.status === 'pending'
  )

  if (waveTasks.length === 0) {
    console.log(`  No pending tasks in wave ${wave}`)
    continue
  }

  // Skip tasks whose deps failed/skipped
  const executableTasks = []
  for (const task of waveTasks) {
    const deps = (task.deps || '').split(';').filter(Boolean)
    if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
      skippedIds.add(task.id)
      updateMasterCsvRow(`${sessionFolder}/tasks.csv`, task.id, {
        status: 'skipped',
        error: 'Dependency failed or skipped'
      })
      console.log(`  [${task.id}] ${task.title} → SKIPPED (dependency failed)`)
      continue
    }
    executableTasks.push(task)
  }

  if (executableTasks.length === 0) {
    console.log(`  No executable tasks in wave ${wave}`)
    continue
  }

  // Build prev_context for each task
  for (const task of executableTasks) {
    task.prev_context = buildPrevContext(task.context_from, masterCsv)
  }

  // Write wave CSV (input columns + prev_context)
  const waveHeader = 'id,title,description,agent,scope,deps,execution_group,context_from,wave,task_json_path,hints,execution_directives,acceptance_criteria,prev_context'
  const waveRows = executableTasks.map(t =>
    [t.id, t.title, t.description, t.agent, t.scope, t.deps, t.execution_group,
     t.context_from, t.wave, t.task_json_path, t.hints, t.execution_directives,
     t.acceptance_criteria, t.prev_context]
      .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
      .join(',')
  )
  Write(`${sessionFolder}/wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

  // Execute wave
  console.log(`  Executing ${executableTasks.length} tasks (concurrency: ${effectiveConcurrency})...`)

  spawn_agents_on_csv({
    csv_path: `${sessionFolder}/wave-${wave}.csv`,
    id_column: "id",
    instruction: buildExecuteInstruction(sessionFolder, contextBlock),
    max_concurrency: effectiveConcurrency,
    max_runtime_seconds: 600,
    output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
    output_schema: {
      type: "object",
      properties: {
        id: { type: "string" },
        status: { type: "string", enum: ["completed", "failed"] },
        findings: { type: "string" },
        files_modified: { type: "array", items: { type: "string" } },
        tests_passed: { type: "boolean" },
        acceptance_met: { type: "string" },
        error: { type: "string" }
      },
      required: ["id", "status", "findings", "tests_passed"]
    }
  })

  // Merge results into master CSV + update task JSONs
  const waveResults = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
  for (const result of waveResults) {
    const filesModified = Array.isArray(result.files_modified)
      ? result.files_modified.join(';')
      : (result.files_modified || '')

    updateMasterCsvRow(`${sessionFolder}/tasks.csv`, result.id, {
      status: result.status,
      findings: result.findings || '',
      files_modified: filesModified,
      tests_passed: String(result.tests_passed ?? ''),
      acceptance_met: result.acceptance_met || '',
      error: result.error || ''
    })

    // Update task JSON status
    if (result.status === 'completed' || result.status === 'failed') {
      Bash(`cd "${sessionFolder}/.task" && jq '.status="${result.status}" | .status_history=(.status_history // [])+[{"from":"in_progress","to":"${result.status}","changed_at":"'"$(date -Iseconds)"'"}]' "${result.id}.json" > tmp.json && mv tmp.json "${result.id}.json" 2>/dev/null || true`)
    }

    if (result.status === 'failed') {
      failedIds.add(result.id)
      console.log(`  [${result.id}] → FAILED: ${result.error}`)
    } else {
      console.log(`  [${result.id}] → COMPLETED${result.tests_passed ? ' (tests passed)' : ''}`)
    }

    // Auto-commit per completed task
    if (withCommit && result.status === 'completed' && filesModified) {
      const files = filesModified.split(';').filter(Boolean)
      if (files.length > 0) {
        const taskJson = JSON.parse(Read(`${sessionFolder}/.task/${result.id}.json`) || '{}')
        const typeMap = { feature: 'feat', bugfix: 'fix', refactor: 'refactor', 'test-gen': 'test', docs: 'docs' }
        const type = typeMap[taskJson.meta?.type] || 'chore'
        const title = taskJson.title || result.id
        const msg = `${type}: ${title}`
        Bash(`git add ${files.map(f => '"' + f + '"').join(' ')} && git commit -m "${msg}" 2>/dev/null || true`)
        console.log(`  Committed: ${msg}`)
      }
    }
  }

  // Cleanup temp wave CSVs
  Bash(`rm -f "${sessionFolder}/wave-${wave}.csv" "${sessionFolder}/wave-${wave}-results.csv"`)

  const completedCount = waveResults.filter(r => r.status === 'completed').length
  const failedCount = waveResults.filter(r => r.status === 'failed').length
  console.log(`  Wave ${wave} done: ${completedCount} completed, ${failedCount} failed`)
}
```

**prev_context Builder**

```javascript
function buildPrevContext(contextFrom, masterCsv) {
  if (!contextFrom) return 'No previous context available'

  const ids = contextFrom.split(';').filter(Boolean)
  const entries = []

  ids.forEach(id => {
    const row = masterCsv.find(r => r.id === id)
    if (row && row.status === 'completed' && row.findings) {
      entries.push(`[${row.id}: ${row.title}] ${row.findings}`)
      if (row.files_modified) entries.push(`  Modified: ${row.files_modified}`)
    }
  })

  return entries.length > 0 ? entries.join('\n') : 'No previous context available'
}
```

**Execute Instruction Template**

```javascript
function buildExecuteInstruction(sessionFolder, contextBlock) {
  return `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read your FULL task JSON: ${sessionFolder}/{task_json_path}
   - CSV row is a brief — task JSON has pre_analysis, flow_control, convergence, and full context
2. Read shared discoveries: ${sessionFolder}/discoveries.ndjson (if exists)
3. Read project context: .workflow/project-tech.json (if exists)

---

## Your Task

**Task ID**: {id}
**Title**: {title}
**Description**: {description}
**Agent Type**: {agent}
**Scope**: {scope}

### Task JSON (full details)
Read: ${sessionFolder}/{task_json_path}

### Implementation Hints & Reference Files
{hints}

> Format: \`tips text || file1;file2\`. Read ALL reference files (after ||) before starting. Apply tips (before ||) as guidance.

### Execution Directives
{execution_directives}

> Commands to run for verification, tool restrictions, or environment requirements.

### Acceptance Criteria
{acceptance_criteria}

### Previous Context (from predecessor tasks)
{prev_context}

### Project Context
${contextBlock}

---

## Execution Protocol

1. **Read task JSON**: Load ${sessionFolder}/{task_json_path} for full task details including pre_analysis steps and flow_control
2. **Check execution method**: If task JSON has \`execution_config.method\`, follow it (agent vs cli mode)
3. **Execute pre_analysis**: If task JSON has \`pre_analysis\` steps, run them first to gather context
4. **Read references**: Parse {hints} — read all files listed after \`||\` to understand existing patterns
5. **Read discoveries**: Load ${sessionFolder}/discoveries.ndjson for shared findings
6. **Use context**: Apply predecessor tasks' findings from prev_context above
7. **Stay in scope**: ONLY create/modify files within {scope} — do NOT touch files outside this boundary
8. **Apply hints**: Follow implementation tips from {hints} (before \`||\`)
9. **Execute**: Implement the task as described in the task JSON
10. **Generate summary**: Write execution summary to ${sessionFolder}/.summaries/{id}-summary.md with sections:
    ## Summary, ## Files Modified (as \`- \\\`path\\\`\` list), ## Key Decisions, ## Tests
11. **Run directives**: Execute commands from {execution_directives} to verify your work
12. **Update TODO**: In ${sessionFolder}/TODO_LIST.md, change \`- [ ] {id}\` to \`- [x] {id}\`
13. **Share discoveries**: Append findings to shared board:
    \`\`\`bash
    echo '{"ts":"<ISO8601>","worker":"{id}","type":"<type>","data":{...}}' >> ${sessionFolder}/discoveries.ndjson
    \`\`\`
14. **Report result**: Return JSON via report_agent_job_result

### Discovery Types to Share
- \`code_pattern\`: {name, file, description} — reusable patterns found
- \`integration_point\`: {file, description, exports[]} — module connection points
- \`convention\`: {naming, imports, formatting} — code style conventions
- \`blocker\`: {issue, severity, impact} — blocking issues encountered

---

## Output (report_agent_job_result)

Return JSON:
{
  "id": "{id}",
  "status": "completed" | "failed",
  "findings": "Key discoveries and implementation notes (max 500 chars)",
  "files_modified": ["path1", "path2"],
  "tests_passed": true | false,
  "acceptance_met": "Summary of which acceptance criteria were met/unmet",
  "error": ""
}

**IMPORTANT**: Set status to "completed" ONLY if:
- All acceptance criteria are met
- Verification directives pass (if any)
Otherwise set status to "failed" with details in error field.
`
}
```

---

### Phase 5: Results Sync

**Objective**: Export results, reconcile TODO_LIST.md, update session status.

```javascript
console.log(`\n## Phase 5: Results Sync\n`)

// 5.1: Export results.csv (final copy of tasks.csv)
const finalCsvContent = Read(`${sessionFolder}/tasks.csv`)
Write(`${sessionFolder}/results.csv`, finalCsvContent)

// 5.2: Reconcile TODO_LIST.md with tasks.csv status
const finalTasks = parseCsv(finalCsvContent)
let todoMd = Read(`${sessionFolder}/TODO_LIST.md`)

for (const task of finalTasks) {
  if (task.status === 'completed') {
    // Ensure marked as [x] in TODO_LIST.md
    const uncheckedPattern = new RegExp(`^(- \\[ \\] ${task.id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(:.*)?)$`, 'm')
    todoMd = todoMd.replace(uncheckedPattern, (match, line) => line.replace('- [ ]', '- [x]'))
  }
}
Write(`${sessionFolder}/TODO_LIST.md`, todoMd)

// 5.3: Summary
const completed = finalTasks.filter(t => t.status === 'completed')
const failed = finalTasks.filter(t => t.status === 'failed')
const skipped = finalTasks.filter(t => t.status === 'skipped')
const pending = finalTasks.filter(t => t.status === 'pending')

console.log(`  Results:`)
console.log(`    Completed: ${completed.length}`)
console.log(`    Failed: ${failed.length}`)
console.log(`    Skipped: ${skipped.length}`)
console.log(`    Pending: ${pending.length}`)

// 5.4: Update session status
const allDone = failed.length === 0 && skipped.length === 0 && pending.length === 0
const sessionStatus = allDone ? 'completed' : 'partial'
Bash(`cd "${sessionFolder}" && jq '.status = "${sessionStatus}" | .completed_at = "'"$(date -Iseconds)"'"' workflow-session.json > tmp.json && mv tmp.json workflow-session.json 2>/dev/null || true`)

// 5.5: User next step
if (AUTO_YES) {
  console.log(`  [--yes] Session ${sessionId} ${sessionStatus}.`)
} else {
  const nextStep = AskUserQuestion({
    questions: [{
      question: "Execution complete. What's next?",
      header: "Next Step",
      multiSelect: false,
      options: [
        { label: "Enter Review", description: "Run post-implementation review (security/quality/architecture)" },
        { label: "Complete Session", description: "Archive session and finalize" }
      ]
    }]
  })

  if (nextStep['Next Step'] === 'Enter Review') {
    // → Phase 6
  } else {
    console.log(`  Session ${sessionId} ${sessionStatus}.`)
  }
}
```

---

### Phase 6: Post-Implementation Review (Optional)

**Objective**: CLI-assisted specialized review of implemented code.

```javascript
// Phase 6 entry (from Phase 5 "Enter Review" or direct invocation)
console.log(`\n## Phase 6: Post-Implementation Review\n`)

const reviewType = AUTO_YES ? 'quality' : (() => {
  const answer = AskUserQuestion({
    questions: [{
      question: "Select review type:",
      header: "Review",
      multiSelect: false,
      options: [
        { label: "Quality", description: "Code quality, best practices, maintainability" },
        { label: "Security", description: "Security vulnerabilities, OWASP Top 10" },
        { label: "Architecture", description: "Architecture decisions, scalability, patterns" },
        { label: "Action Items", description: "TODO items, tech debt, follow-ups" }
      ]
    }]
  })
  return answer.Review.toLowerCase()
})()

// Get list of modified files from tasks.csv
const reviewTasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const allModifiedFiles = new Set()
reviewTasks.forEach(t => {
  (t.files_modified || '').split(';').filter(Boolean).forEach(f => allModifiedFiles.add(f))
})

const fileList = [...allModifiedFiles].join(', ')

Bash({
  command: `ccw cli -p "PURPOSE: Post-implementation ${reviewType} review of modified files. Identify issues and generate actionable report.
TASK:
  • Review all modified files for ${reviewType} concerns
  • Assess overall ${reviewType} posture
  • Generate prioritized issue list with severity
  • Provide remediation recommendations
MODE: analysis
CONTEXT: @${[...allModifiedFiles].map(f => f).join(' @')}
EXPECTED: Structured ${reviewType} review report with: summary, issue list (severity, file, line, description, fix), overall score
CONSTRAINTS: Focus on ${reviewType} | Review only modified files: ${fileList}" --tool gemini --mode analysis --rule analysis-review-code-quality`,
  run_in_background: true
})
// Wait for CLI → review report

Write(`${sessionFolder}/REVIEW-${reviewType}.md`, reviewReport)
console.log(`  Review complete: ${sessionFolder}/REVIEW-${reviewType}.md`)

// Post-review options
if (!AUTO_YES) {
  const postReview = AskUserQuestion({
    questions: [{
      question: "Review complete. What's next?",
      header: "Post-Review",
      multiSelect: false,
      options: [
        { label: "Another Review", description: "Run a different review type" },
        { label: "Complete Session", description: "Archive and finalize" }
      ]
    }]
  })

  if (postReview['Post-Review'] === 'Another Review') {
    // Loop back to Phase 6 review type selection
  }
}

console.log(`\nSession ${sessionId} execution complete.`)
```

---

## CSV Helpers

```javascript
function parseCsv(content) {
  const lines = content.trim().split('\n')
  if (lines.length < 2) return []
  const header = parseCsvLine(lines[0])
  return lines.slice(1).map(line => {
    const cells = parseCsvLine(line)
    const obj = {}
    header.forEach((col, i) => { obj[col] = cells[i] || '' })
    return obj
  })
}

function parseCsvLine(line) {
  const cells = []
  let current = ''
  let inQuotes = false
  for (let i = 0; i < line.length; i++) {
    const ch = line[i]
    if (inQuotes) {
      if (ch === '"' && line[i + 1] === '"') {
        current += '"'
        i++
      } else if (ch === '"') {
        inQuotes = false
      } else {
        current += ch
      }
    } else {
      if (ch === '"') {
        inQuotes = true
      } else if (ch === ',') {
        cells.push(current)
        current = ''
      } else {
        current += ch
      }
    }
  }
  cells.push(current)
  return cells
}

function updateMasterCsvRow(csvPath, taskId, updates) {
  const content = Read(csvPath)
  const lines = content.split('\n')
  const header = parseCsvLine(lines[0])

  for (let i = 1; i < lines.length; i++) {
    const cells = parseCsvLine(lines[i])
    if (cells[0] === taskId) {
      for (const [col, val] of Object.entries(updates)) {
        const colIdx = header.indexOf(col)
        if (colIdx >= 0) {
          cells[colIdx] = String(val).replace(/"/g, '""')
        }
      }
      lines[i] = cells.map(c => `"${c}"`).join(',')
      break
    }
  }

  Write(csvPath, lines.join('\n'))
}

function csvEscape(val) {
  return `"${String(val).replace(/"/g, '""')}"`
}
```

---

## Agent Assignment Rules

```
meta.agent specified → Use specified agent file
meta.agent missing → Infer from meta.type:
  feature    → code-developer
  test-gen   → code-developer
  test-fix   → test-fix-agent
  review     → universal-executor
  docs       → doc-generator
  default    → code-developer
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No active sessions | Guide: run `$workflow-plan "description"` first |
| Missing planning docs | Guide: run `$workflow-plan --session ID` |
| Agent failure | Mark failed in tasks.csv, skip dependents, continue wave |
| Dependency cascade | Skip dependent tasks, report at Phase 5 |
| CSV parse error | Validate CSV format, report line number |
| Task JSON corruption | Skip task, mark failed in CSV |
| Commit failure | Log error, continue execution (non-blocking) |
| Circular dependency | Warn and assign to last wave |
| All wave tasks skipped | Log and continue to next wave |

---

## Core Rules

1. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results merge
2. **CSV is Execution State**: tasks.csv holds all execution state — always re-read before each wave
3. **Task JSON is Rich Data**: agents read full task JSON via `task_json_path` — CSV is brief
4. **Skip on Failure**: If a dependency failed, skip the dependent task (cascade)
5. **Cleanup Temp Files**: Remove wave CSVs after results are merged
6. **TODO_LIST.md Sync**: Phase 5 reconciles TODO_LIST.md with tasks.csv final state
7. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
8. **DO NOT STOP**: Continuous execution until all waves complete or all remaining tasks are skipped
9. **Planning Artifacts Unchanged**: IMPL-*.json, plan.json, IMPL_PLAN.md formats are preserved

---

## Compact Protection

> **COMPACT DIRECTIVE**: If context compression occurs during execution:
> - Re-read `tasks.csv` for current execution state (source of truth)
> - Re-read `TODO_LIST.md` for progress display
> - Re-read `plan.json` for execution hints (concurrency, phases)
> - Task JSONs are read per-wave via `task_json_path`, compression has minimal impact
> - Wave loop state (`failedIds`, `skippedIds`, `wave`) can be reconstructed from tasks.csv status column
