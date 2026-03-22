---
name: csv-wave-pipeline
description: Requirement planning to wave-based CSV execution pipeline. Decomposes requirement into dependency-sorted CSV tasks, computes execution waves, runs wave-by-wave via spawn_agents_on_csv with cross-wave context propagation.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"requirement description\""
allowed-tools: spawn_agents_on_csv, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# CSV Wave Pipeline

## Usage

```bash
$csv-wave-pipeline "Implement user authentication with OAuth, JWT, and 2FA"
$csv-wave-pipeline -c 4 "Refactor payment module with Stripe and PayPal"
$csv-wave-pipeline -y "Build notification system with email and SMS"
$csv-wave-pipeline --continue "auth-20260228"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 4)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Wave-based batch execution using `spawn_agents_on_csv` with **cross-wave context propagation**. Tasks are grouped into dependency waves; each wave executes concurrently, and its results feed into the next wave.

**Core workflow**: Decompose → Compute Waves → Execute Wave-by-Wave → Aggregate

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CSV BATCH EXECUTION WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 1: Requirement → CSV                                              │
│     ├─ Parse requirement into subtasks (3-10 tasks)                      │
│     ├─ Identify dependencies (deps column)                               │
│     ├─ Compute dependency waves (topological sort → depth grouping)      │
│     ├─ Generate tasks.csv with wave column                               │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 2: Wave Execution Engine                                          │
│     ├─ For each wave (1..N):                                             │
│     │   ├─ Build wave CSV (filter rows for this wave)                    │
│     │   ├─ Inject previous wave findings into prev_context column        │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Collect results, merge into master tasks.csv                  │
│     │   └─ Check: any failed? → skip dependents or retry                 │
│     └─ discoveries.ndjson shared across all waves (append-only)          │
│                                                                          │
│  Phase 3: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Display summary: completed/failed/skipped per wave                │
│     └─ Offer: view results | retry failed | done                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,status,findings,files_modified,tests_passed,acceptance_met,error
"1","Setup auth module","Create auth directory structure and base files","Verify directory exists and base files export expected interfaces","auth/ dir created; index.ts and types.ts export AuthProvider interface","src/auth/**","Follow monorepo module pattern || package.json;src/shared/types.ts","","","","1","","","","","",""
"2","Implement OAuth","Add OAuth provider integration with Google and GitHub","Unit test: mock OAuth callback returns valid token; Integration test: verify redirect URL generation","OAuth login redirects to provider; callback returns JWT; supports Google and GitHub","src/auth/oauth/**","Use passport.js strategy pattern || src/auth/index.ts;docs/oauth-flow.md","Run npm test -- --grep oauth before completion","1","1","2","","","","","",""
"3","Add JWT tokens","Implement JWT generation and validation","Unit test: sign/verify round-trip; Edge test: expired token returns 401","generateToken() returns valid JWT; verifyToken() rejects expired/tampered tokens","src/auth/jwt/**","Use jsonwebtoken library; Set default expiry 1h || src/config/auth.ts","Ensure tsc --noEmit passes","1","1","2","","","","","",""
"4","Setup 2FA","Add TOTP-based 2FA with QR code generation","Unit test: TOTP verify with correct code; Test: QR data URL is valid","QR code generates scannable image; TOTP verification succeeds within time window","src/auth/2fa/**","Use speakeasy + qrcode libraries || src/auth/oauth/strategy.ts;src/auth/jwt/token.ts","Run full test suite: npm test","2;3","1;2;3","3","","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description — what to implement |
| `test` | Input | Test cases: what tests to write and how to verify (unit/integration/edge) |
| `acceptance_criteria` | Input | Acceptance criteria: measurable conditions that define "done" |
| `scope` | Input | Target file/directory glob — constrains agent work area, prevents cross-task file conflicts |
| `hints` | Input | Implementation tips + reference files. Format: `tips text \|\| file1;file2`. Before `\|\|` = how to implement; after `\|\|` = existing files to read before starting. Either part is optional |
| `execution_directives` | Input | Execution constraints: commands to run for verification, tool restrictions, environment requirements |
| `deps` | Input | Semicolon-separated dependency task IDs (empty = no deps) |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` → `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `files_modified` | Output | Semicolon-separated file paths |
| `tests_passed` | Output | Whether all defined test cases passed (true/false) |
| `acceptance_met` | Output | Summary of which acceptance criteria were met/unmet |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with an extra `prev_context` column:

```csv
id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,prev_context
"2","Implement OAuth","Add OAuth integration","Unit test: mock OAuth callback returns valid token","OAuth login redirects to provider; callback returns JWT","src/auth/oauth/**","Use passport.js strategy pattern || src/auth/index.ts;docs/oauth-flow.md","Run npm test -- --grep oauth","1","1","2","[Task 1] Created auth/ with index.ts and types.ts"
"3","Add JWT tokens","Implement JWT","Unit test: sign/verify round-trip; Edge test: expired token returns 401","generateToken() returns valid JWT; verifyToken() rejects expired/tampered tokens","src/auth/jwt/**","Use jsonwebtoken library; Set default expiry 1h || src/config/auth.ts","Ensure tsc --noEmit passes","1","1","2","[Task 1] Created auth/ with index.ts and types.ts"
```

The `prev_context` column is built from `context_from` by looking up completed tasks' `findings` in the master CSV.

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state — all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 3 |
| `discoveries.ndjson` | Shared exploration board across all agents | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 3 |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
├── tasks.csv                  # Master state (updated per wave)
├── results.csv                # Final results export
├── discoveries.ndjson         # Shared discovery board (all agents)
├── context.md                 # Human-readable report
└── wave-{N}.csv               # Temporary per-wave input (cleaned up)
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

// Clean requirement text (remove flags)
const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `cwp-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

// Continue mode: find existing session
if (continueMode) {
  const existing = Bash(`ls -t .workflow/.csv-wave/ 2>/dev/null | head -1`).trim()
  if (existing) {
    sessionId = existing
    sessionFolder = `.workflow/.csv-wave/${sessionId}`
    // Read existing tasks.csv, find incomplete waves, resume from there
    const existingCsv = Read(`${sessionFolder}/tasks.csv`)
    // → jump to Phase 2 with remaining waves
  }
}

Bash(`mkdir -p ${sessionFolder}`)
```

---

### Phase 1: Requirement → CSV

**Objective**: Decompose requirement into tasks, compute dependency waves, generate tasks.csv.

**Steps**:

1. **Decompose Requirement**

   ```javascript
   // Use ccw cli to decompose requirement into subtasks
   Bash({
     command: `ccw cli -p "PURPOSE: Decompose requirement into 3-10 atomic tasks for batch agent execution. Each task must include implementation description, test cases, and acceptance criteria.
TASK:
  • Parse requirement into independent subtasks
  • Identify dependencies between tasks (which must complete before others)
  • Identify context flow (which tasks need previous tasks' findings)
  • For each task, define concrete test cases (unit/integration/edge)
  • For each task, define measurable acceptance criteria (what defines 'done')
  • Each task must be executable by a single agent with file read/write access
MODE: analysis
CONTEXT: @**/*
EXPECTED: JSON object with tasks array. Each task: {id: string, title: string, description: string, test: string, acceptance_criteria: string, scope: string, hints: string, execution_directives: string, deps: string[], context_from: string[]}.
  - description: what to implement (specific enough for an agent to execute independently)
  - test: what tests to write and how to verify (e.g. 'Unit test: X returns Y; Edge test: handles Z')
  - acceptance_criteria: measurable conditions that define done (e.g. 'API returns 200; token expires after 1h')
  - scope: target file/directory glob (e.g. 'src/auth/**') — tasks in same wave MUST have non-overlapping scopes
  - hints: implementation tips + reference files, format '<tips> || <ref_file1>;<ref_file2>' (e.g. 'Use strategy pattern || src/base/Strategy.ts;docs/design.md')
  - execution_directives: commands to run for verification or tool constraints (e.g. 'Run npm test --bail; Ensure tsc passes')
  - deps: task IDs that must complete first
  - context_from: task IDs whose findings are needed
CONSTRAINTS: 3-10 tasks | Each task is atomic | No circular deps | test and acceptance_criteria must be concrete and verifiable | Same-wave tasks must have non-overlapping scopes

REQUIREMENT: ${requirement}" --tool gemini --mode analysis --rule planning-breakdown-task-steps`,
     run_in_background: true
   })
   // Wait for CLI completion via hook callback
   // Parse JSON from CLI output → decomposedTasks[]
   ```

2. **Compute Waves** (Topological Sort → Depth Grouping)

   ```javascript
   function computeWaves(tasks) {
     // Build adjacency: task.deps → predecessors
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

     // BFS-based topological sort with depth tracking
     const queue = []  // [taskId, depth]
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

     // Detect cycles: any task without wave assignment
     for (const task of tasks) {
       if (!waveAssignment.has(task.id)) {
         throw new Error(`Circular dependency detected involving task ${task.id}`)
       }
     }

     return { waveAssignment, maxWave }
   }

   const { waveAssignment, maxWave } = computeWaves(decomposedTasks)
   ```

3. **Generate tasks.csv**

   ```javascript
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
       'pending',  // status
       '',         // findings
       '',         // files_modified
       '',         // tests_passed
       '',         // acceptance_met
       ''          // error
     ].map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
   })

   Write(`${sessionFolder}/tasks.csv`, [header, ...rows].join('\n'))
   ```

4. **User Validation** (skip if AUTO_YES)

   ```javascript
   if (!AUTO_YES) {
     // Display task breakdown with wave assignment
     console.log(`\n## Task Breakdown (${decomposedTasks.length} tasks, ${maxWave} waves)\n`)
     for (let w = 1; w <= maxWave; w++) {
       const waveTasks = decomposedTasks.filter(t => waveAssignment.get(t.id) === w)
       console.log(`### Wave ${w} (${waveTasks.length} tasks, concurrent)`)
       waveTasks.forEach(t => console.log(`  - [${t.id}] ${t.title}`))
     }

     const answer = AskUserQuestion({
       questions: [{
         question: "Approve task breakdown?",
         header: "Validation",
         multiSelect: false,
         options: [
           { label: "Approve", description: "Proceed with wave execution" },
           { label: "Modify", description: `Edit ${sessionFolder}/tasks.csv manually, then --continue` },
           { label: "Cancel", description: "Abort" }
         ]
       }]
     })  // BLOCKS

     if (answer.Validation === "Modify") {
       console.log(`Edit: ${sessionFolder}/tasks.csv\nResume: $csv-wave-pipeline --continue`)
       return
     } else if (answer.Validation === "Cancel") {
       return
     }
   }
   ```

**Success Criteria**:
- tasks.csv created with valid schema and wave assignments
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine

**Objective**: Execute tasks wave-by-wave via `spawn_agents_on_csv`. Each wave sees previous waves' results.

**Steps**:

1. **Wave Loop**

   ```javascript
   const failedIds = new Set()
   const skippedIds = new Set()

   for (let wave = 1; wave <= maxWave; wave++) {
     console.log(`\n## Wave ${wave}/${maxWave}\n`)

     // 1. Read current master CSV
     const masterCsv = parseCsv(Read(`${sessionFolder}/tasks.csv`))

     // 2. Filter tasks for this wave
     const waveTasks = masterCsv.filter(row => parseInt(row.wave) === wave)

     // 3. Skip tasks whose deps failed
     const executableTasks = []
     for (const task of waveTasks) {
       const deps = task.deps.split(';').filter(Boolean)
       if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
         skippedIds.add(task.id)
         // Update master CSV: mark as skipped
         updateMasterCsvRow(sessionFolder, task.id, {
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

     // 4. Build prev_context for each task
     for (const task of executableTasks) {
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

     // 5. Write wave CSV
     const waveHeader = 'id,title,description,test,acceptance_criteria,scope,hints,execution_directives,deps,context_from,wave,prev_context'
     const waveRows = executableTasks.map(t =>
       [t.id, t.title, t.description, t.test, t.acceptance_criteria, t.scope, t.hints, t.execution_directives, t.deps, t.context_from, t.wave, t.prev_context]
         .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
         .join(',')
     )
     Write(`${sessionFolder}/wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

     // 6. Execute wave
     console.log(`  Executing ${executableTasks.length} tasks (concurrency: ${maxConcurrency})...`)

     const waveResult = spawn_agents_on_csv({
       csv_path: `${sessionFolder}/wave-${wave}.csv`,
       id_column: "id",
       instruction: buildInstructionTemplate(sessionFolder, wave),
       max_concurrency: maxConcurrency,
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
     // ↑ Blocks until all agents in this wave complete

     // 7. Merge results into master CSV
     const waveResults = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
     for (const result of waveResults) {
       updateMasterCsvRow(sessionFolder, result.id, {
         status: result.status,
         findings: result.findings || '',
         files_modified: (result.files_modified || []).join(';'),
         tests_passed: String(result.tests_passed ?? ''),
         acceptance_met: result.acceptance_met || '',
         error: result.error || ''
       })

       if (result.status === 'failed') {
         failedIds.add(result.id)
         console.log(`  [${result.id}] ${result.title} → FAILED: ${result.error}`)
       } else {
         console.log(`  [${result.id}] ${result.title} → COMPLETED`)
       }
     }

     // 8. Cleanup temporary wave CSV
     Bash(`rm -f "${sessionFolder}/wave-${wave}.csv"`)

     console.log(`  Wave ${wave} done: ${waveResults.filter(r => r.status === 'completed').length} completed, ${waveResults.filter(r => r.status === 'failed').length} failed`)
   }
   ```

2. **Instruction Template Builder**

   ```javascript
   function buildInstructionTemplate(sessionFolder, wave) {
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

> Format: \`<tips> || <ref_file1>;<ref_file2>\`. Read ALL reference files (after ||) before starting implementation. Apply tips (before ||) as implementation guidance.

### Execution Directives
{execution_directives}

> Commands to run for verification, tool restrictions, or environment requirements. Follow these constraints during and after implementation.

### Test Cases
{test}

### Acceptance Criteria
{acceptance_criteria}

### Previous Tasks' Findings (Context)
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

3. **Master CSV Update Helper**

   ```javascript
   function updateMasterCsvRow(sessionFolder, taskId, updates) {
     const csvPath = `${sessionFolder}/tasks.csv`
     const content = Read(csvPath)
     const lines = content.split('\n')
     const header = lines[0].split(',')

     for (let i = 1; i < lines.length; i++) {
       const cells = parseCsvLine(lines[i])
       if (cells[0] === taskId || cells[0] === `"${taskId}"`) {
         // Update specified columns
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
- discoveries.ndjson accumulated across all waves

---

### Phase 3: Results Aggregation

**Objective**: Generate final results and human-readable report.

**Steps**:

1. **Export results.csv**

   ```javascript
   const masterCsv = Read(`${sessionFolder}/tasks.csv`)
   // results.csv = master CSV (already has all results populated)
   Write(`${sessionFolder}/results.csv`, masterCsv)
   ```

2. **Generate context.md**

   ```javascript
   const tasks = parseCsv(masterCsv)
   const completed = tasks.filter(t => t.status === 'completed')
   const failed = tasks.filter(t => t.status === 'failed')
   const skipped = tasks.filter(t => t.status === 'skipped')

   const contextContent = `# CSV Batch Execution Report

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Completed**: ${getUtc8ISOString()}
**Waves**: ${maxWave} | **Concurrency**: ${maxConcurrency}

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | ${tasks.length} |
| Completed | ${completed.length} |
| Failed | ${failed.length} |
| Skipped | ${skipped.length} |
| Waves | ${maxWave} |

---

## Wave Execution

${Array.from({ length: maxWave }, (_, i) => i + 1).map(w => {
  const waveTasks = tasks.filter(t => parseInt(t.wave) === w)
  return `### Wave ${w}
${waveTasks.map(t => `- **[${t.id}] ${t.title}**: ${t.status}${t.tests_passed ? ' ✓tests' : ''}${t.error ? ' — ' + t.error : ''}
  ${t.findings ? 'Findings: ' + t.findings : ''}`).join('\n')}`
}).join('\n\n')}

---

## Task Details

${tasks.map(t => `### ${t.id}: ${t.title}

| Field | Value |
|-------|-------|
| Status | ${t.status} |
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

**Files Modified**: ${t.files_modified || 'none'}
`).join('\n---\n')}

---

## All Modified Files

${[...new Set(tasks.flatMap(t => (t.files_modified || '').split(';')).filter(Boolean))].map(f => '- ' + f).join('\n') || 'None'}
`

   Write(`${sessionFolder}/context.md`, contextContent)
   ```

3. **Display Summary**

   ```javascript
   console.log(`
## Execution Complete

- **Session**: ${sessionId}
- **Waves**: ${maxWave}
- **Completed**: ${completed.length}/${tasks.length}
- **Failed**: ${failed.length}
- **Skipped**: ${skipped.length}

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
     })  // BLOCKS

     if (answer['Next Step'] === "Retry Failed") {
       // Reset failed tasks to pending, re-run Phase 2 for their waves
       for (const task of failed) {
         updateMasterCsvRow(sessionFolder, task.id, { status: 'pending', error: '' })
       }
       // Also reset skipped tasks whose deps are now retrying
       for (const task of skipped) {
         updateMasterCsvRow(sessionFolder, task.id, { status: 'pending', error: '' })
       }
       // Re-execute Phase 2 (loop will skip already-completed tasks)
       // → goto Phase 2
     } else if (answer['Next Step'] === "View Report") {
       console.log(Read(`${sessionFolder}/context.md`))
     }
   }
   ```

**Success Criteria**:
- results.csv exported
- context.md generated
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents across all waves share `discoveries.ndjson`. This eliminates redundant codebase exploration.

**Lifecycle**:
- Created by the first agent to write a discovery
- Carries over across waves — never cleared
- Agents append via `echo '...' >> discoveries.ndjson`

**Format**: NDJSON, each line is a self-contained JSON:

```jsonl
{"ts":"2026-02-28T10:00:00+08:00","worker":"1","type":"code_pattern","data":{"name":"repository-pattern","file":"src/repos/Base.ts","description":"Abstract CRUD repository"}}
{"ts":"2026-02-28T10:01:00+08:00","worker":"2","type":"integration_point","data":{"file":"src/auth/index.ts","description":"Auth module entry","exports":["authenticate","authorize"]}}
```

**Discovery Types**:

| type | Dedup Key | Description |
|------|-----------|-------------|
| `code_pattern` | `data.name` | Reusable code pattern found |
| `integration_point` | `data.file` | Module connection point |
| `convention` | singleton | Code style conventions |
| `blocker` | `data.issue` | Blocking issue encountered |
| `tech_stack` | singleton | Project technology stack |
| `test_command` | singleton | Test commands discovered |

**Protocol Rules**:
1. Read board before own exploration → skip covered areas
2. Write discoveries immediately via `echo >>` → don't batch
3. Deduplicate — check existing entries; skip if same type + dedup key exists
4. Append-only — never modify or delete existing lines

---

## Wave Computation Details

### Algorithm

Kahn's BFS topological sort with depth tracking:

```
Input:  tasks[] with deps[]
Output: waveAssignment (taskId → wave number)

1. Build in-degree map and adjacency list from deps
2. Enqueue all tasks with in-degree 0 at wave 1
3. BFS: for each dequeued task at wave W:
   - For each dependent task D:
     - Decrement D's in-degree
     - D.wave = max(D.wave, W + 1)
     - If D's in-degree reaches 0, enqueue D
4. Any task without wave assignment → circular dependency error
```

### Wave Properties

- **Wave 1**: No dependencies — all tasks in wave 1 are fully independent
- **Wave N**: All dependencies are in waves 1..(N-1) — guaranteed completed before wave N starts
- **Within a wave**: Tasks are independent of each other → safe for concurrent execution

### Example

```
Task A (no deps)      → Wave 1
Task B (no deps)      → Wave 1
Task C (deps: A)      → Wave 2
Task D (deps: A, B)   → Wave 2
Task E (deps: C, D)   → Wave 3

Execution:
  Wave 1: [A, B]  ← concurrent
  Wave 2: [C, D]  ← concurrent, sees A+B findings
  Wave 3: [E]     ← sees A+B+C+D findings
```

---

## Context Propagation Flow

```
Wave 1 agents:
  ├─ Execute tasks (no prev_context)
  ├─ Write findings to report_agent_job_result
  └─ Append discoveries to discoveries.ndjson

        ↓ merge results into master CSV

Wave 2 agents:
  ├─ Read discoveries.ndjson (exploration sharing)
  ├─ Read prev_context column (wave 1 findings from context_from)
  ├─ Execute tasks with full upstream context
  ├─ Write findings to report_agent_job_result
  └─ Append new discoveries to discoveries.ndjson

        ↓ merge results into master CSV

Wave 3 agents:
  ├─ Read discoveries.ndjson (accumulated from waves 1+2)
  ├─ Read prev_context column (wave 1+2 findings from context_from)
  ├─ Execute tasks
  └─ ...
```

**Two context channels**:
1. **CSV findings** (structured): `context_from` column → `prev_context` injection — task-specific directed context
2. **NDJSON discoveries** (broadcast): `discoveries.ndjson` — general exploration findings available to all

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Circular dependency | Detect in wave computation, abort with error message |
| Agent timeout | Mark as failed in results, continue with wave |
| Agent failed | Mark as failed, skip dependent tasks in later waves |
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state — always read before wave, always write after
4. **Context Propagation**: prev_context built from master CSV, not from memory
5. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
6. **Skip on Failure**: If a dependency failed, skip the dependent task (don't attempt)
7. **Cleanup Temp Files**: Remove wave-{N}.csv after results are merged
8. **DO NOT STOP**: Continuous execution until all waves complete or all remaining tasks are skipped

---

## Best Practices

1. **Task Granularity**: 3-10 tasks optimal; too many = overhead, too few = no parallelism benefit
2. **Minimize Cross-Wave Deps**: More tasks in wave 1 = more parallelism
3. **Specific Descriptions**: Agent sees only its CSV row + prev_context — make description self-contained
4. **Context From ≠ Deps**: `deps` = execution order constraint; `context_from` = information flow. A task can have `context_from` without `deps` (it just reads previous findings but doesn't require them to be done first in its wave)
5. **Concurrency Tuning**: `-c 1` for serial execution (maximum context sharing); `-c 8` for I/O-bound tasks

---

## Usage Recommendations

| Scenario | Recommended Approach |
|----------|---------------------|
| Independent parallel tasks (no deps) | `$csv-wave-pipeline -c 8` — single wave, max parallelism |
| Linear pipeline (A→B→C) | `$csv-wave-pipeline -c 1` — 3 waves, serial, full context |
| Diamond dependency (A→B,C→D) | `$csv-wave-pipeline` — 3 waves, B+C concurrent in wave 2 |
| Complex requirement, unclear tasks | Use `$roadmap-with-file` first for planning, then feed issues here |
| Single complex task | Use `$workflow-lite-plan` instead |
