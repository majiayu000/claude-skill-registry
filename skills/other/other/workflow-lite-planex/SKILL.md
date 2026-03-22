---
name: workflow-lite-plan
description: Explore-first wave pipeline. Decomposes requirement into exploration angles, runs wave exploration via spawn_agents_on_csv, synthesizes findings into execution tasks with cross-phase context linking (E*→T*), then wave-executes via spawn_agents_on_csv.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"requirement description\""
allowed-tools: spawn_agents_on_csv, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm decomposition, skip interactive validation, use defaults.

# Workflow Lite Planex

## Usage

```bash
$workflow-lite-plan "Implement user authentication with OAuth, JWT, and 2FA"
$workflow-lite-plan -c 4 "Refactor payment module with Stripe and PayPal"
$workflow-lite-plan -y "Build notification system with email and SMS"
$workflow-lite-plan --continue "auth-20260228"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 4)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.lite-plan/{session-id}/`

---

## Overview

Explore-first wave-based pipeline using `spawn_agents_on_csv`. Two-stage CSV execution: **explore.csv** (codebase discovery) → **tasks.csv** (implementation), with cross-phase context propagation via `context_from` linking (`E*` → `T*`).

**Core workflow**: Decompose → Wave Explore → Synthesize & Plan → Wave Execute → Aggregate

```
┌──────────────────────────────────────────────────────────────────────┐
│                    WORKFLOW LITE PLANEX                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1: Requirement → explore.csv                                  │
│     ├─ Analyze complexity → select exploration angles (1-4)          │
│     ├─ Generate explore.csv (1 row per angle)                        │
│     └─ User validates (skip if -y)                                   │
│                                                                      │
│  Phase 2: Wave Explore (spawn_agents_on_csv)                         │
│     ├─ For each explore wave:                                        │
│     │   ├─ Build wave CSV from explore.csv                           │
│     │   ├─ spawn_agents_on_csv(explore instruction template)         │
│     │   └─ Merge findings/key_files into explore.csv                 │
│     └─ discoveries.ndjson shared across agents                       │
│                                                                      │
│  Phase 3: Synthesize & Plan → tasks.csv                              │
│     ├─ Read all explore findings → cross-reference                   │
│     ├─ Resolve conflicts between angles                              │
│     ├─ Decompose into execution tasks with context_from: E*;T*       │
│     ├─ Compute dependency waves (topological sort)                   │
│     └─ User validates (skip if -y)                                   │
│                                                                      │
│  Phase 4: Wave Execute (spawn_agents_on_csv)                         │
│     ├─ For each task wave:                                           │
│     │   ├─ Build prev_context from explore.csv + tasks.csv           │
│     │   ├─ Build wave CSV with prev_context column                   │
│     │   ├─ spawn_agents_on_csv(execute instruction template)         │
│     │   └─ Merge results into tasks.csv                              │
│     └─ discoveries.ndjson carries across all waves                   │
│                                                                      │
│  Phase 5: Aggregate                                                  │
│     ├─ Export results.csv                                            │
│     ├─ Generate context.md with all findings                         │
│     └─ Display summary                                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Context Flow

```
explore.csv             tasks.csv
┌──────────┐           ┌──────────┐
│ E1: arch │──────────→│ T1: setup│ context_from: E1;E2
│ findings │           │ prev_ctx │← E1+E2 findings
├──────────┤           ├──────────┤
│ E2: deps │──────────→│ T2: impl │ context_from: E1;T1
│ findings │           │ prev_ctx │← E1+T1 findings
├──────────┤           ├──────────┤
│ E3: test │──┐   ┌───→│ T3: test │ context_from: E3;T2
│ findings │  └───┘    │ prev_ctx │← E3+T2 findings
└──────────┘           └──────────┘

Two context channels:
1. Directed: context_from → prev_context (CSV findings lookup)
2. Broadcast: discoveries.ndjson (append-only shared board)

context_from prefix: E* → explore.csv lookup, T* → tasks.csv lookup
```

---

## CSV Schemas

### explore.csv

```csv
id,angle,description,focus,deps,wave,status,findings,key_files,error
"E1","architecture","Explore codebase architecture for: auth system","architecture","","1","pending","","",""
"E2","dependencies","Explore dependency landscape for: auth system","dependencies","","1","pending","","",""
"E3","testing","Explore test infrastructure for: auth system","testing","","1","pending","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Exploration ID: E1, E2, ... |
| `angle` | Input | Exploration angle name |
| `description` | Input | What to explore from this angle |
| `focus` | Input | Keywords and focus areas |
| `deps` | Input | Semicolon-separated dep IDs (usually empty — all wave 1) |
| `wave` | Computed | Wave number (usually 1 for all explorations) |
| `status` | Output | `pending` → `completed` / `failed` |
| `findings` | Output | Discoveries (max 800 chars) |
| `key_files` | Output | Relevant files (semicolon-separated) |
| `error` | Output | Error message if failed |

### tasks.csv

```csv
id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,status,findings,files_modified,tests_passed,acceptance_met,error
"T1","Setup types","Create type definitions","Verify types compile with tsc","All interfaces exported","src/types/**","Follow existing patterns || src/types/index.ts","tsc --noEmit","","E1;E2","1","pending","","","","",""
"T2","Implement core","Implement core auth logic","Unit test: login returns token","Login flow works end-to-end","src/auth/**","Reuse BaseService || src/services/Base.ts","npm test -- --grep auth","T1","E1;E2;T1","2","pending","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Task ID: T1, T2, ... |
| `title` | Input | Short task title |
| `description` | Input | Self-contained task description — what to implement |
| `test` | Input | Test cases: what tests to write and how to verify (unit/integration/edge) |
| `acceptance_criteria` | Input | Measurable conditions that define "done" |
| `scope` | Input | Target file/directory glob — constrains agent write area, prevents cross-task file conflicts |
| `hints` | Input | Implementation tips + reference files. Format: `tips text \|\| file1;file2`. Either part is optional |
| `execution_directives` | Input | Execution constraints: commands to run for verification, tool restrictions |
| `deps` | Input | Dependency task IDs: T1;T2 (semicolon-separated) |
| `context_from` | Input | Context source IDs: **E1;E2;T1** — `E*` lookups in explore.csv, `T*` in tasks.csv |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` → `completed` / `failed` / `skipped` |
| `findings` | Output | Execution findings (max 500 chars) |
| `files_modified` | Output | Semicolon-separated file paths |
| `tests_passed` | Output | Whether all defined test cases passed (true/false) |
| `acceptance_met` | Output | Summary of which acceptance criteria were met/unmet |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary CSV with an extra `prev_context` column.

**Explore wave**: `explore-wave-{N}.csv` — same columns as explore.csv (no prev_context, explorations are independent).

**Execute wave**: `task-wave-{N}.csv` — all task columns + `prev_context`:

```csv
id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,prev_context
"T2","Implement core","Implement core auth logic","Unit test: login returns token","Login flow works end-to-end","src/auth/**","Reuse BaseService || src/services/Base.ts","npm test -- --grep auth","T1","E1;E2;T1","2","[Explore architecture] Found BaseService pattern in src/services/\n[Task T1] Created types at src/types/auth.ts"
```

The `prev_context` column is built from `context_from` by looking up completed rows' `findings` in both explore.csv (`E*`) and tasks.csv (`T*`).

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `explore.csv` | Exploration state — angles with findings/key_files | Updated after Phase 2 |
| `tasks.csv` | Execution state — tasks with results | Updated after each wave in Phase 4 |
| `explore-wave-{N}.csv` | Per-wave explore input (temporary) | Created before wave, deleted after |
| `task-wave-{N}.csv` | Per-wave execute input (temporary) | Created before wave, deleted after |
| `results.csv` | Final results export | Created in Phase 5 |
| `discoveries.ndjson` | Shared discovery board (all agents, all phases) | Append-only |
| `context.md` | Human-readable execution report | Created in Phase 5 |

---

## Session Structure

```
.workflow/.lite-plan/{session-id}/
├── explore.csv              # Exploration state
├── tasks.csv                # Execution state
├── results.csv              # Final results export
├── discoveries.ndjson       # Shared discovery board
├── context.md               # Full context summary
├── explore-wave-{N}.csv     # Temporary per-wave explore input (cleaned up)
└── task-wave-{N}.csv        # Temporary per-wave execute input (cleaned up)
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
const maxConcurrency = concurrencyMatch ? parseInt(concurrencyMatch[1]) : 4

const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `wpp-${slug}-${dateStr}`
const sessionFolder = `.workflow/.lite-plan/${sessionId}`

// Continue mode: find existing session
if (continueMode) {
  const existing = Bash(`ls -t .workflow/.lite-plan/ 2>/dev/null | head -1`).trim()
  if (existing) {
    sessionId = existing
    sessionFolder = `.workflow/.lite-plan/${sessionId}`
    // Check which phase to resume: if tasks.csv exists → Phase 4, else → Phase 2
  }
}

Bash(`mkdir -p ${sessionFolder}`)
```

---

### Phase 1: Requirement → explore.csv

**Objective**: Analyze requirement complexity, select exploration angles, generate explore.csv.

**Steps**:

1. **Analyze & Decompose**

   ```javascript
   Bash({
     command: `ccw cli -p "PURPOSE: Analyze requirement complexity and select 1-4 exploration angles for codebase discovery before implementation.
TASK:
  • Classify requirement type (feature/bugfix/refactor/security/performance)
  • Assess complexity (Low: 1 angle, Medium: 2-3, High: 3-4)
  • Select exploration angles from: architecture, dependencies, integration-points, testing, patterns, security, performance, state-management, error-handling, edge-cases
  • For each angle, define focus keywords and what to discover
MODE: analysis
CONTEXT: @**/*
EXPECTED: JSON object: {type: string, complexity: string, angles: [{id: string, angle: string, description: string, focus: string}]}. Each angle id = E1, E2, etc.
CONSTRAINTS: 1-4 angles | Angles must be distinct | Each angle must have clear focus

REQUIREMENT: ${requirement}" --tool gemini --mode analysis --rule planning-breakdown-task-steps`,
     run_in_background: true
   })
   // Wait for CLI completion via hook callback
   // Parse JSON from CLI output → { type, complexity, angles[] }
   ```

2. **Generate explore.csv**

   ```javascript
   const header = 'id,angle,description,focus,deps,wave,status,findings,key_files,error'
   const rows = angles.map(a =>
     [a.id, a.angle, a.description, a.focus, '', '1', 'pending', '', '', '']
       .map(v => `"${String(v).replace(/"/g, '""')}"`)
       .join(',')
   )

   Write(`${sessionFolder}/explore.csv`, [header, ...rows].join('\n'))
   ```

3. **User Validation** (skip if AUTO_YES)

   ```javascript
   if (!AUTO_YES) {
     console.log(`\n## Exploration Plan (${angles.length} angles)\n`)
     angles.forEach(a => console.log(`  - [${a.id}] ${a.angle}: ${a.focus}`))

     const answer = AskUserQuestion({
       questions: [{
         question: "Approve exploration angles?",
         header: "Validation",
         multiSelect: false,
         options: [
           { label: "Approve", description: "Proceed with wave exploration" },
           { label: "Modify", description: `Edit ${sessionFolder}/explore.csv manually, then --continue` },
           { label: "Cancel", description: "Abort" }
         ]
       }]
     })

     if (answer.Validation === "Modify") {
       console.log(`Edit: ${sessionFolder}/explore.csv\nResume: $workflow-lite-plan --continue`)
       return
     } else if (answer.Validation === "Cancel") {
       return
     }
   }
   ```

**Success Criteria**:
- explore.csv created with 1-4 exploration angles
- User approved (or AUTO_YES)

---

### Phase 2: Wave Explore (spawn_agents_on_csv)

**Objective**: Execute exploration via `spawn_agents_on_csv`. Each angle produces findings and key_files.

**Steps**:

1. **Explore Wave Loop**

   ```javascript
   const exploreCSV = parseCsv(Read(`${sessionFolder}/explore.csv`))
   const maxExploreWave = Math.max(...exploreCSV.map(r => parseInt(r.wave)))

   for (let wave = 1; wave <= maxExploreWave; wave++) {
     const waveTasks = exploreCSV.filter(r =>
       parseInt(r.wave) === wave && r.status === 'pending'
     )
     if (waveTasks.length === 0) continue

     // Skip rows with failed dependencies
     const executableTasks = []
     for (const task of waveTasks) {
       const deps = (task.deps || '').split(';').filter(Boolean)
       if (deps.some(d => {
         const dep = exploreCSV.find(r => r.id === d)
         return !dep || dep.status !== 'completed'
       })) {
         task.status = 'skipped'
         task.error = 'Dependency failed/skipped'
         continue
       }
       executableTasks.push(task)
     }

     if (executableTasks.length === 0) continue

     // Write explore wave CSV
     const waveHeader = 'id,angle,description,focus,deps,wave'
     const waveRows = executableTasks.map(t =>
       [t.id, t.angle, t.description, t.focus, t.deps, t.wave]
         .map(v => `"${String(v).replace(/"/g, '""')}"`)
         .join(',')
     )
     Write(`${sessionFolder}/explore-wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

     // Execute explore wave
     console.log(`  Exploring ${executableTasks.length} angles (wave ${wave})...`)

     spawn_agents_on_csv({
       csv_path: `${sessionFolder}/explore-wave-${wave}.csv`,
       id_column: "id",
       instruction: buildExploreInstruction(sessionFolder),
       max_concurrency: maxConcurrency,
       max_runtime_seconds: 300,
       output_csv_path: `${sessionFolder}/explore-wave-${wave}-results.csv`,
       output_schema: {
         type: "object",
         properties: {
           id: { type: "string" },
           status: { type: "string", enum: ["completed", "failed"] },
           findings: { type: "string" },
           key_files: { type: "array", items: { type: "string" } },
           error: { type: "string" }
         },
         required: ["id", "status", "findings"]
       }
     })

     // Merge results into explore.csv
     const waveResults = parseCsv(Read(`${sessionFolder}/explore-wave-${wave}-results.csv`))
     for (const result of waveResults) {
       updateMasterCsvRow(`${sessionFolder}/explore.csv`, result.id, {
         status: result.status,
         findings: result.findings || '',
         key_files: Array.isArray(result.key_files) ? result.key_files.join(';') : (result.key_files || ''),
         error: result.error || ''
       })
     }

     // Cleanup temporary wave CSV
     Bash(`rm -f "${sessionFolder}/explore-wave-${wave}.csv" "${sessionFolder}/explore-wave-${wave}-results.csv"`)
   }
   ```

2. **Explore Instruction Template**

   ```javascript
   function buildExploreInstruction(sessionFolder) {
     return `
## EXPLORATION ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read shared discoveries: ${sessionFolder}/discoveries.ndjson (if exists, skip if not)
2. Read project context: .workflow/project-tech.json (if exists)

---

## Your Exploration

**Exploration ID**: {id}
**Angle**: {angle}
**Description**: {description}
**Focus**: {focus}

---

## Exploration Protocol

1. **Read discoveries**: Load ${sessionFolder}/discoveries.ndjson for shared findings
2. **Explore**: Search the codebase from the {angle} perspective
3. **Discover**: Find relevant files, patterns, integration points, constraints
4. **Share discoveries**: Append findings to shared board:
   \`\`\`bash
   echo '{"ts":"<ISO8601>","worker":"{id}","type":"<type>","data":{...}}' >> ${sessionFolder}/discoveries.ndjson
   \`\`\`
5. **Report result**: Return JSON via report_agent_job_result

### What to Look For
- Existing patterns and conventions to follow
- Integration points and module boundaries
- Dependencies and constraints
- Test infrastructure and coverage
- Risks and potential blockers

### Discovery Types to Share
- \`code_pattern\`: {name, file, description} — reusable patterns found
- \`integration_point\`: {file, description, exports[]} — module connection points
- \`convention\`: {naming, imports, formatting} — code style conventions
- \`tech_stack\`: {framework, version, config} — technology stack details

---

## Output (report_agent_job_result)

Return JSON:
{
  "id": "{id}",
  "status": "completed" | "failed",
  "findings": "Concise summary of ${'{'}angle{'}'} discoveries (max 800 chars)",
  "key_files": ["relevant/file1.ts", "relevant/file2.ts"],
  "error": ""
}
`
   }
   ```

**Success Criteria**:
- All explore angles executed
- explore.csv updated with findings and key_files
- discoveries.ndjson accumulated

---

### Phase 3: Synthesize & Plan → tasks.csv

**Objective**: Read exploration findings, cross-reference, resolve conflicts, generate tasks.csv with context_from linking to E* rows.

**Steps**:

1. **Synthesize Exploration Findings**

   ```javascript
   const exploreCSV = parseCsv(Read(`${sessionFolder}/explore.csv`))
   const completed = exploreCSV.filter(r => r.status === 'completed')

   // Cross-reference: find shared files across angles
   const fileRefs = {}
   completed.forEach(r => {
     (r.key_files || '').split(';').filter(Boolean).forEach(f => {
       if (!fileRefs[f]) fileRefs[f] = []
       fileRefs[f].push({ angle: r.angle, id: r.id })
     })
   })
   const sharedFiles = Object.entries(fileRefs).filter(([_, refs]) => refs.length > 1)

   // Build synthesis context for task decomposition
   const synthesisContext = completed.map(r =>
     `[${r.id}: ${r.angle}] ${r.findings}\n  Key files: ${r.key_files || 'none'}`
   ).join('\n\n')

   const sharedFilesContext = sharedFiles.length > 0
     ? `\nShared files (referenced by multiple angles):\n${sharedFiles.map(([f, refs]) =>
         `  ${f} ← ${refs.map(r => r.id).join(', ')}`
       ).join('\n')}`
     : ''
   ```

2. **Decompose into Tasks**

   ```javascript
   Bash({
     command: `ccw cli -p "PURPOSE: Based on exploration findings, decompose requirement into 3-10 atomic execution tasks. Each task must include test cases, acceptance criteria, and link to relevant exploration findings.
TASK:
  • Use exploration findings to inform task decomposition
  • Each task must be self-contained with specific implementation instructions
  • Link tasks to exploration rows via context_from (E1, E2, etc.)
  • Define dependencies between tasks (T1 must finish before T2, etc.)
  • For each task: define test cases, acceptance criteria, scope, hints, and execution directives
  • Ensure same-wave tasks have non-overlapping scopes
MODE: analysis
CONTEXT: @**/*
EXPECTED: JSON object with tasks array. Each task: {id: string, title: string, description: string, test: string, acceptance_criteria: string, scope: string, hints: string, execution_directives: string, deps: string[], context_from: string[]}.
  - id: T1, T2, etc.
  - description: what to implement (specific enough for an agent)
  - test: what tests to write (e.g. 'Unit test: X returns Y')
  - acceptance_criteria: what defines done (e.g. 'API returns 200')
  - scope: target glob (e.g. 'src/auth/**') — non-overlapping within same wave
  - hints: tips + ref files (format: 'tips || file1;file2')
  - execution_directives: verification commands (e.g. 'npm test --bail')
  - deps: task IDs that must complete first (T*)
  - context_from: explore (E*) and task (T*) IDs whose findings are needed
CONSTRAINTS: 3-10 tasks | Atomic | No circular deps | Concrete test/acceptance_criteria | Non-overlapping scopes per wave

EXPLORATION FINDINGS:
${synthesisContext}
${sharedFilesContext}

REQUIREMENT: ${requirement}" --tool gemini --mode analysis --rule planning-breakdown-task-steps`,
     run_in_background: true
   })
   // Wait for CLI completion → decomposedTasks[]
   ```

3. **Compute Waves & Write tasks.csv**

   ```javascript
   const { waveAssignment, maxWave } = computeWaves(decomposedTasks)

   const header = 'id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,status,findings,files_modified,tests_passed,acceptance_met,error'
   const rows = decomposedTasks.map(task => {
     const wave = waveAssignment.get(task.id)
     return [
       task.id,
       csvEscape(task.title),
       csvEscape(task.description),
       csvEscape(task.test),
       csvEscape(task.acceptance_criteria),
       csvEscape(task.scope),
       csvEscape(task.hints),
       csvEscape(task.execution_directives),
       task.deps.join(';'),
       task.context_from.join(';'),
       wave,
       'pending', '', '', '', '', ''
     ].map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
   })

   Write(`${sessionFolder}/tasks.csv`, [header, ...rows].join('\n'))
   ```

4. **User Validation** (skip if AUTO_YES)

   ```javascript
   if (!AUTO_YES) {
     console.log(`
## Execution Plan

Explore: ${completed.length} angles completed
Shared files: ${sharedFiles.length}
Tasks: ${decomposedTasks.length} across ${maxWave} waves

${Array.from({length: maxWave}, (_, i) => i + 1).map(w => {
  const wt = decomposedTasks.filter(t => waveAssignment.get(t.id) === w)
  return `### Wave ${w} (${wt.length} tasks, concurrent)
${wt.map(t => `  - [${t.id}] ${t.title} (scope: ${t.scope}, from: ${t.context_from.join(';')})`).join('\n')}`
}).join('\n')}
     `)

     const answer = AskUserQuestion({
       questions: [{
         question: `Proceed with ${decomposedTasks.length} tasks across ${maxWave} waves?`,
         header: "Confirm",
         multiSelect: false,
         options: [
           { label: "Execute", description: "Proceed with wave execution" },
           { label: "Modify", description: `Edit ${sessionFolder}/tasks.csv then --continue` },
           { label: "Cancel", description: "Abort" }
         ]
       }]
     })

     if (answer.Confirm === "Modify") {
       console.log(`Edit: ${sessionFolder}/tasks.csv\nResume: $workflow-lite-plan --continue`)
       return
     } else if (answer.Confirm === "Cancel") {
       return
     }
   }
   ```

**Success Criteria**:
- tasks.csv created with context_from linking to E* rows
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 4: Wave Execute (spawn_agents_on_csv)

**Objective**: Execute tasks wave-by-wave via `spawn_agents_on_csv`. Each wave's prev_context is built from both explore.csv and tasks.csv.

**Steps**:

1. **Wave Loop**

   ```javascript
   const exploreCSV = parseCsv(Read(`${sessionFolder}/explore.csv`))
   const failedIds = new Set()
   const skippedIds = new Set()

   for (let wave = 1; wave <= maxWave; wave++) {
     console.log(`\n## Wave ${wave}/${maxWave}\n`)

     // Re-read master CSV
     const masterCsv = parseCsv(Read(`${sessionFolder}/tasks.csv`))
     const waveTasks = masterCsv.filter(row => parseInt(row.wave) === wave)

     // Skip tasks whose deps failed
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

     // Build prev_context for each task (cross-phase: E* + T*)
     for (const task of executableTasks) {
       task.prev_context = buildPrevContext(task.context_from, exploreCSV, masterCsv)
     }

     // Write wave CSV
     const waveHeader = 'id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,prev_context'
     const waveRows = executableTasks.map(t =>
       [t.id, t.title, t.description, t.test, t.acceptance_criteria, t.scope, t.hints, t.execution_directives, t.deps, t.context_from, t.wave, t.prev_context]
         .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
         .join(',')
     )
     Write(`${sessionFolder}/task-wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

     // Execute wave
     console.log(`  Executing ${executableTasks.length} tasks (concurrency: ${maxConcurrency})...`)

     spawn_agents_on_csv({
       csv_path: `${sessionFolder}/task-wave-${wave}.csv`,
       id_column: "id",
       instruction: buildExecuteInstruction(sessionFolder, wave),
       max_concurrency: maxConcurrency,
       max_runtime_seconds: 600,
       output_csv_path: `${sessionFolder}/task-wave-${wave}-results.csv`,
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

     // Merge results into master CSV
     const waveResults = parseCsv(Read(`${sessionFolder}/task-wave-${wave}-results.csv`))
     for (const result of waveResults) {
       updateMasterCsvRow(`${sessionFolder}/tasks.csv`, result.id, {
         status: result.status,
         findings: result.findings || '',
         files_modified: Array.isArray(result.files_modified) ? result.files_modified.join(';') : (result.files_modified || ''),
         tests_passed: String(result.tests_passed ?? ''),
         acceptance_met: result.acceptance_met || '',
         error: result.error || ''
       })

       if (result.status === 'failed') {
         failedIds.add(result.id)
         console.log(`  [${result.id}] → FAILED: ${result.error}`)
       } else {
         console.log(`  [${result.id}] → COMPLETED${result.tests_passed ? ' ✓tests' : ''}`)
       }
     }

     // Cleanup
     Bash(`rm -f "${sessionFolder}/task-wave-${wave}.csv" "${sessionFolder}/task-wave-${wave}-results.csv"`)

     console.log(`  Wave ${wave} done: ${waveResults.filter(r => r.status === 'completed').length} completed, ${waveResults.filter(r => r.status === 'failed').length} failed`)
   }
   ```

2. **prev_context Builder (Cross-Phase)**

   The key function linking exploration context to execution:

   ```javascript
   function buildPrevContext(contextFrom, exploreCSV, tasksCSV) {
     if (!contextFrom) return 'No previous context available'

     const ids = contextFrom.split(';').filter(Boolean)
     const entries = []

     ids.forEach(id => {
       if (id.startsWith('E')) {
         // ← Look up in explore.csv (cross-phase link)
         const row = exploreCSV.find(r => r.id === id)
         if (row && row.status === 'completed' && row.findings) {
           entries.push(`[Explore ${row.angle}] ${row.findings}`)
           if (row.key_files) entries.push(`  Key files: ${row.key_files}`)
         }
       } else if (id.startsWith('T')) {
         // ← Look up in tasks.csv (same-phase link)
         const row = tasksCSV.find(r => r.id === id)
         if (row && row.status === 'completed' && row.findings) {
           entries.push(`[Task ${row.id}: ${row.title}] ${row.findings}`)
           if (row.files_modified) entries.push(`  Modified: ${row.files_modified}`)
         }
       }
     })

     return entries.length > 0 ? entries.join('\n') : 'No previous context available'
   }
   ```

3. **Execute Instruction Template**

   ```javascript
   function buildExecuteInstruction(sessionFolder, wave) {
     return `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read shared discoveries: ${sessionFolder}/discoveries.ndjson (if exists, skip if not)
2. Read project context: .workflow/project-tech.json (if exists)

---

## Your Task

**Task ID**: {id}
**Title**: {title}
**Description**: {description}
**Scope**: {scope}

### Implementation Hints & Reference Files
{hints}

> Format: \`tips text || file1;file2\`. Read ALL reference files (after ||) before starting. Apply tips (before ||) as guidance.

### Execution Directives
{execution_directives}

> Commands to run for verification, tool restrictions, or environment requirements.

### Test Cases
{test}

### Acceptance Criteria
{acceptance_criteria}

### Previous Context (from exploration and predecessor tasks)
{prev_context}

---

## Execution Protocol

1. **Read references**: Parse {hints} — read all files listed after \`||\` to understand existing patterns
2. **Read discoveries**: Load ${sessionFolder}/discoveries.ndjson for shared exploration findings
3. **Use context**: Apply previous tasks' findings from prev_context above
4. **Stay in scope**: ONLY create/modify files within {scope} — do NOT touch files outside this boundary
5. **Apply hints**: Follow implementation tips from {hints} (before \`||\`)
6. **Execute**: Implement the task as described
7. **Write tests**: Implement the test cases defined above
8. **Run directives**: Execute commands from {execution_directives} to verify your work
9. **Verify acceptance**: Ensure all acceptance criteria are met before reporting completion
10. **Share discoveries**: Append exploration findings to shared board:
   \`\`\`bash
   echo '{"ts":"<ISO8601>","worker":"{id}","type":"<type>","data":{...}}' >> ${sessionFolder}/discoveries.ndjson
   \`\`\`
11. **Report result**: Return JSON via report_agent_job_result

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
- All test cases pass
- All acceptance criteria are met
Otherwise set status to "failed" with details in error field.
`
   }
   ```

4. **Master CSV Update Helper**

   ```javascript
   function updateMasterCsvRow(csvPath, taskId, updates) {
     const content = Read(csvPath)
     const lines = content.split('\n')
     const header = lines[0].split(',')

     for (let i = 1; i < lines.length; i++) {
       const cells = parseCsvLine(lines[i])
       if (cells[0] === taskId || cells[0] === `"${taskId}"`) {
         for (const [col, val] of Object.entries(updates)) {
           const colIdx = header.indexOf(col)
           if (colIdx >= 0) {
             cells[colIdx] = `"${String(val).replace(/"/g, '""')}"`
           }
         }
         lines[i] = cells.join(',')
         break
       }
     }

     Write(csvPath, lines.join('\n'))
   }
   ```

**Success Criteria**:
- All waves executed in order
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all phases

---

### Phase 5: Results Aggregation

**Objective**: Generate final results and human-readable report.

**Steps**:

1. **Export results.csv**

   ```javascript
   const masterCsv = Read(`${sessionFolder}/tasks.csv`)
   Write(`${sessionFolder}/results.csv`, masterCsv)
   ```

2. **Generate context.md**

   ```javascript
   const finalTasks = parseCsv(masterCsv)
   const exploreCSV = parseCsv(Read(`${sessionFolder}/explore.csv`))
   const completed = finalTasks.filter(t => t.status === 'completed')
   const failed = finalTasks.filter(t => t.status === 'failed')
   const skipped = finalTasks.filter(t => t.status === 'skipped')

   const contextContent = `# Lite Planex Execution Report

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Completed**: ${getUtc8ISOString()}
**Waves**: ${maxWave} | **Concurrency**: ${maxConcurrency}

---

## Summary

| Metric | Count |
|--------|-------|
| Explore Angles | ${exploreCSV.length} |
| Total Tasks | ${finalTasks.length} |
| Completed | ${completed.length} |
| Failed | ${failed.length} |
| Skipped | ${skipped.length} |
| Waves | ${maxWave} |

---

## Exploration Results

${exploreCSV.map(e => `### ${e.id}: ${e.angle} (${e.status})
${e.findings || 'N/A'}
Key files: ${e.key_files || 'none'}`).join('\n\n')}

---

## Task Results

${finalTasks.map(t => `### ${t.id}: ${t.title} (${t.status})

| Field | Value |
|-------|-------|
| Wave | ${t.wave} |
| Scope | ${t.scope || 'none'} |
| Dependencies | ${t.deps || 'none'} |
| Context From | ${t.context_from || 'none'} |
| Tests Passed | ${t.tests_passed || 'N/A'} |
| Acceptance Met | ${t.acceptance_met || 'N/A'} |
| Error | ${t.error || 'none'} |

**Description**: ${t.description}

**Test Cases**: ${t.test || 'N/A'}

**Acceptance Criteria**: ${t.acceptance_criteria || 'N/A'}

**Hints**: ${t.hints || 'N/A'}

**Execution Directives**: ${t.execution_directives || 'N/A'}

**Findings**: ${t.findings || 'N/A'}

**Files Modified**: ${t.files_modified || 'none'}`).join('\n\n---\n\n')}

---

## All Modified Files

${[...new Set(finalTasks.flatMap(t => (t.files_modified || '').split(';')).filter(Boolean))].map(f => '- ' + f).join('\n') || 'None'}
`

   Write(`${sessionFolder}/context.md`, contextContent)
   ```

3. **Display Summary**

   ```javascript
   console.log(`
## Lite Planex Complete

- **Session**: ${sessionId}
- **Explore**: ${exploreCSV.filter(r => r.status === 'completed').length}/${exploreCSV.length} angles
- **Tasks**: ${completed.length}/${finalTasks.length} completed, ${failed.length} failed, ${skipped.length} skipped
- **Waves**: ${maxWave}

**Results**: ${sessionFolder}/results.csv
**Report**: ${sessionFolder}/context.md
**Discoveries**: ${sessionFolder}/discoveries.ndjson
   `)
   ```

4. **Offer Next Steps** (skip if AUTO_YES)

   ```javascript
   if (!AUTO_YES && failed.length > 0) {
     const answer = AskUserQuestion({
       questions: [{
         question: `${failed.length} tasks failed. Next action?`,
         header: "Next Step",
         multiSelect: false,
         options: [
           { label: "Retry Failed", description: `Re-execute ${failed.length} failed tasks with updated context` },
           { label: "View Report", description: "Display context.md" },
           { label: "Done", description: "Complete session" }
         ]
       }]
     })

     if (answer['Next Step'] === "Retry Failed") {
       for (const task of failed) {
         updateMasterCsvRow(`${sessionFolder}/tasks.csv`, task.id, { status: 'pending', error: '' })
       }
       for (const task of skipped) {
         updateMasterCsvRow(`${sessionFolder}/tasks.csv`, task.id, { status: 'pending', error: '' })
       }
       // Re-execute Phase 4
     } else if (answer['Next Step'] === "View Report") {
       console.log(Read(`${sessionFolder}/context.md`))
     }
   }
   ```

**Success Criteria**:
- results.csv exported
- context.md generated with full field coverage
- Summary displayed to user

---

## Wave Computation (Kahn's BFS)

```javascript
function computeWaves(tasks) {
  const taskMap = new Map(tasks.map(t => [t.id, t]))
  const inDegree = new Map(tasks.map(t => [t.id, 0]))
  const adjList = new Map(tasks.map(t => [t.id, []]))

  for (const task of tasks) {
    for (const dep of task.deps) {
      if (taskMap.has(dep)) {
        adjList.get(dep).push(task.id)
        inDegree.set(task.id, inDegree.get(task.id) + 1)
      }
    }
  }

  const queue = []
  const waveAssignment = new Map()

  for (const [id, deg] of inDegree) {
    if (deg === 0) {
      queue.push([id, 1])
      waveAssignment.set(id, 1)
    }
  }

  let maxWave = 1
  let idx = 0
  while (idx < queue.length) {
    const [current, depth] = queue[idx++]
    for (const next of adjList.get(current)) {
      const newDeg = inDegree.get(next) - 1
      inDegree.set(next, newDeg)
      const nextDepth = Math.max(waveAssignment.get(next) || 0, depth + 1)
      waveAssignment.set(next, nextDepth)
      if (newDeg === 0) {
        queue.push([next, nextDepth])
        maxWave = Math.max(maxWave, nextDepth)
      }
    }
  }

  for (const task of tasks) {
    if (!waveAssignment.has(task.id)) {
      throw new Error(`Circular dependency detected involving task ${task.id}`)
    }
  }

  return { waveAssignment, maxWave }
}
```

---

## Shared Discovery Board Protocol

All agents across all phases share `discoveries.ndjson`. This eliminates redundant codebase exploration.

```jsonl
{"ts":"2026-02-28T10:00:00+08:00","worker":"E1","type":"code_pattern","data":{"name":"repository-pattern","file":"src/repos/Base.ts","description":"Abstract CRUD repository"}}
{"ts":"2026-02-28T10:01:00+08:00","worker":"T2","type":"integration_point","data":{"file":"src/auth/index.ts","description":"Auth module entry","exports":["authenticate","authorize"]}}
```

**Types**: `code_pattern`, `integration_point`, `convention`, `blocker`, `tech_stack`, `test_command`
**Rules**: Read first → write immediately → deduplicate → append-only

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Explore agent failure | Mark as failed in explore.csv, exclude from planning |
| All explores failed | Fallback: plan directly from requirement without exploration |
| Circular dependency | Abort wave computation, report cycle |
| Execute agent timeout | Mark as failed in results, continue with wave |
| Execute agent failed | Mark as failed, skip dependent tasks in later waves |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| Continue mode: no session | List available sessions, prompt user to select |

---

## Core Rules

1. **Explore Before Execute**: Phase 2 completes before Phase 4 starts
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master CSVs hold all state — always read before wave, always write after
4. **Cross-Phase Context**: prev_context built from both explore.csv (E*) and tasks.csv (T*), not from memory
5. **E* ↔ T* Linking**: tasks.csv `context_from` references explore.csv rows for cross-phase context
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If a dependency failed, skip the dependent task (cascade)
8. **Cleanup Temp Files**: Remove wave CSVs after results are merged
9. **DO NOT STOP**: Continuous execution until all waves complete or all remaining tasks are skipped

---

## Best Practices

1. **Exploration Angles**: 1 for simple, 3-4 for complex; avoid redundant angles
2. **Context Linking**: Link every task to at least one explore row (E*) — exploration was done for a reason
3. **Task Granularity**: 3-10 tasks optimal; too many = overhead, too few = no parallelism
4. **Minimize Cross-Wave Deps**: More tasks in wave 1 = more parallelism
5. **Specific Descriptions**: Agent sees only its CSV row + prev_context — make description self-contained
6. **Non-Overlapping Scopes**: Same-wave tasks must not write to the same files
7. **Concurrency Tuning**: `-c 1` for serial (max context sharing); `-c 8` for I/O-bound tasks

---

## Usage Recommendations

| Scenario | Recommended Approach |
|----------|---------------------|
| Complex feature (unclear architecture) | `$workflow-lite-plan` — explore first, then plan |
| Simple known-pattern task | `$workflow-lite-plan` — skip exploration, direct execution |
| Independent parallel tasks | `$workflow-lite-plan -c 8` — single wave, max parallelism |
| Diamond dependency (A→B,C→D) | `$workflow-lite-plan` — 3 waves with context propagation |
| Unknown codebase | `$workflow-lite-plan` — exploration phase is essential |
