---
name: team-coordinate
description: Universal team coordination skill with dynamic role generation. Analyzes task, generates worker roles at runtime, decomposes into CSV tasks with dependency waves, dispatches parallel CSV agents per wave. Coordinator is orchestrator; all workers are CSV or interactive agents with dynamically generated instructions.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Coordinate

## Usage

```bash
$team-coordinate "Implement user authentication with JWT tokens"
$team-coordinate -c 4 "Refactor payment module and write API documentation"
$team-coordinate -y "Analyze codebase security and fix vulnerabilities"
$team-coordinate --continue "tc-auth-jwt-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Universal team coordination: analyze task -> detect capabilities -> generate dynamic role instructions -> decompose into dependency-ordered CSV tasks -> execute wave-by-wave -> deliver results. Only the **coordinator** (this orchestrator) is built-in. All worker roles are **dynamically generated** as CSV agent instructions at runtime.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|              TEAM COORDINATE WORKFLOW                               |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse user task description                                  |
|     +- Clarify ambiguous requirements (AskUserQuestion)             |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Signal detection: keyword scan -> capability inference       |
|     +- Dependency graph construction (DAG)                          |
|     +- Role minimization (cap at 5 roles)                           |
|     +- Classify tasks: csv-wave | interactive (exec_mode)           |
|     +- Compute dependency waves (topological sort)                  |
|     +- Generate tasks.csv with wave + exec_mode columns             |
|     +- Generate per-role agent instructions dynamically             |
|     +- User validates task breakdown (skip if -y)                   |
|                                                                     |
|  Phase 2: Wave Execution Engine (Extended)                          |
|     +- For each wave (1..N):                                        |
|     |   +- Execute pre-wave interactive tasks (if any)              |
|     |   +- Build wave CSV (filter csv-wave tasks for this wave)     |
|     |   +- Inject previous findings into prev_context column        |
|     |   +- spawn_agents_on_csv(wave CSV)                            |
|     |   +- Execute post-wave interactive tasks (if any)             |
|     |   +- Merge all results into master tasks.csv                  |
|     |   +- Check: any failed? -> skip dependents                    |
|     +- discoveries.ndjson shared across all modes (append-only)     |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion Action)                 |
|     +- Pipeline completion report                                   |
|     +- Interactive completion choice (Archive/Keep/Export)           |
|     +- Final aggregation / report                                   |
|                                                                     |
|  Phase 4: Results Aggregation                                       |
|     +- Export final results.csv                                     |
|     +- Generate context.md with all findings                        |
|     +- Display summary: completed/failed/skipped per wave           |
|     +- Offer: view results | retry failed | done                    |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, needs clarification, revision cycles |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Single-pass code implementation | `csv-wave` |
| Single-pass analysis or documentation | `csv-wave` |
| Research with defined scope | `csv-wave` |
| Testing with known targets | `csv-wave` |
| Design requiring iterative refinement | `interactive` |
| Plan requiring user approval checkpoint | `interactive` |
| Revision cycle (fix-verify loop) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,responsibility_type,output_type,deps,context_from,exec_mode,wave,status,findings,artifacts_produced,error
"RESEARCH-001","Investigate auth patterns","Research JWT authentication patterns and best practices","researcher","orchestration","artifact","","","csv-wave","1","pending","","",""
"IMPL-001","Implement auth module","Build JWT authentication middleware","developer","code-gen","codebase","RESEARCH-001","RESEARCH-001","csv-wave","2","pending","","",""
"TEST-001","Validate auth implementation","Write and run tests for auth module","tester","validation","artifact","IMPL-001","IMPL-001","csv-wave","3","pending","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN format) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description with goal, steps, success criteria |
| `role` | Input | Dynamic role name (researcher, developer, analyst, etc.) |
| `responsibility_type` | Input | `orchestration`, `read-only`, `code-gen`, `code-gen-docs`, `validation` |
| `output_type` | Input | `artifact` (session files), `codebase` (project files), `mixed` |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Plan Reviewer | agents/plan-reviewer.md | 2.3 (send_input cycle) | Review and approve plans before execution waves | pre-wave |
| Completion Handler | agents/completion-handler.md | 2.3 (send_input cycle) | Handle pipeline completion action (Archive/Keep/Export) | standalone |

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
| `task-analysis.json` | Phase 0/1 output: capabilities, dependency graph, roles | Created in Phase 1 |
| `role-instructions/` | Dynamically generated per-role instruction templates | Created in Phase 1 |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state (all tasks, both modes)
+-- results.csv                # Final results export
+-- discoveries.ndjson         # Shared discovery board (all agents)
+-- context.md                 # Human-readable report
+-- task-analysis.json         # Phase 1 analysis output
+-- wave-{N}.csv               # Temporary per-wave input (csv-wave only)
+-- role-instructions/         # Dynamically generated instruction templates
|   +-- researcher.md
|   +-- developer.md
|   +-- ...
+-- artifacts/                 # All deliverables from workers
|   +-- research-findings.md
|   +-- implementation-summary.md
|   +-- ...
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json
+-- wisdom/                    # Cross-task knowledge
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

const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
const sessionId = `tc-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts ${sessionFolder}/role-instructions ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')

// Initialize wisdom files
Write(`${sessionFolder}/wisdom/learnings.md`, '# Learnings\n')
Write(`${sessionFolder}/wisdom/decisions.md`, '# Decisions\n')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse user task, clarify ambiguities, prepare for decomposition.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/tc-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **Clarify if ambiguous** (skip if AUTO_YES):
   ```javascript
   AskUserQuestion({
     questions: [{
       question: "Please confirm the task scope and deliverables:",
       header: "Task Clarification",
       multiSelect: false,
       options: [
         { label: "Proceed as described", description: "Task is clear enough" },
         { label: "Narrow scope", description: "Specify files/modules/areas" },
         { label: "Add constraints", description: "Timeline, tech stack, style" }
       ]
     }]
   })
   ```

4. **Output**: Refined requirement string for Phase 1

**Success Criteria**:
- Refined requirements available for Phase 1 decomposition
- Existing session detected and handled if applicable

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Analyze task, detect capabilities, build dependency graph, generate tasks.csv and role instructions.

**Decomposition Rules**:

1. **Signal Detection** -- scan task description for capability keywords:

| Signal | Keywords | Capability | Prefix | Responsibility Type |
|--------|----------|------------|--------|---------------------|
| Research | investigate, explore, compare, survey, find, research, discover | researcher | RESEARCH | orchestration |
| Writing | write, draft, document, article, report, summarize | writer | DRAFT | code-gen-docs |
| Coding | implement, build, code, fix, refactor, develop, create, migrate | developer | IMPL | code-gen |
| Design | design, architect, plan, structure, blueprint, schema | designer | DESIGN | orchestration |
| Analysis | analyze, review, audit, assess, evaluate, inspect, diagnose | analyst | ANALYSIS | read-only |
| Testing | test, verify, validate, QA, quality, check, coverage | tester | TEST | validation |
| Planning | plan, breakdown, organize, schedule, decompose, roadmap | planner | PLAN | orchestration |

2. **Dependency Graph** -- build DAG using natural ordering tiers:

| Tier | Capabilities | Description |
|------|-------------|-------------|
| 0 | researcher, planner | Knowledge gathering / planning |
| 1 | designer | Design (requires tier 0 if present) |
| 2 | writer, developer | Creation (requires design/plan if present) |
| 3 | analyst, tester | Validation (requires artifacts to validate) |

3. **Role Minimization** -- merge overlapping capabilities, cap at 5 roles

4. **Key File Inference** -- extract nouns from task description, map to likely file paths

5. **output_type derivation**:

| Task Signal | output_type |
|-------------|-------------|
| "write report", "analyze", "research" | `artifact` |
| "update code", "modify", "fix bug" | `codebase` |
| "implement feature + write summary" | `mixed` |

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Single-pass implementation/analysis/documentation | `csv-wave` |
| Needs iterative user approval | `interactive` |
| Fix-verify revision cycle | `interactive` |
| Standard research, coding, testing | `csv-wave` |

**Wave Computation**: Kahn's BFS topological sort with depth tracking.

```javascript
// After task analysis, generate dynamic role instruction templates
for (const role of analysisResult.roles) {
  const instruction = generateRoleInstruction(role, sessionFolder)
  Write(`${sessionFolder}/role-instructions/${role.name}.md`, instruction)
}

// Generate tasks.csv from dependency graph
const tasks = buildTasksCsv(analysisResult)
Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))
Write(`${sessionFolder}/task-analysis.json`, JSON.stringify(analysisResult, null, 2))
```

**User Validation**: Display task breakdown with wave + exec_mode assignment (skip if AUTO_YES).

**Success Criteria**:
- tasks.csv created with valid schema, wave, and exec_mode assignments
- Role instruction templates generated in role-instructions/
- task-analysis.json written
- No circular dependencies
- User approved (or AUTO_YES)

---

### Phase 2: Wave Execution Engine (Extended)

**Objective**: Execute tasks wave-by-wave with hybrid mechanism support and cross-wave context propagation.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
const maxWave = Math.max(...tasks.map(t => t.wave))

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\nWave ${wave}/${maxWave}`)

  // 1. Separate tasks by exec_mode
  const waveTasks = tasks.filter(t => t.wave === wave && t.status === 'pending')
  const csvTasks = waveTasks.filter(t => t.exec_mode === 'csv-wave')
  const interactiveTasks = waveTasks.filter(t => t.exec_mode === 'interactive')

  // 2. Check dependencies -- skip tasks whose deps failed
  for (const task of waveTasks) {
    const depIds = (task.deps || '').split(';').filter(Boolean)
    const depStatuses = depIds.map(id => tasks.find(t => t.id === id)?.status)
    if (depStatuses.some(s => s === 'failed' || s === 'skipped')) {
      task.status = 'skipped'
      task.error = `Dependency failed: ${depIds.filter((id, i) =>
        ['failed','skipped'].includes(depStatuses[i])).join(', ')}`
    }
  }

  // 3. Execute pre-wave interactive tasks (e.g., plan approval)
  const preWaveInteractive = interactiveTasks.filter(t => t.status === 'pending')
  for (const task of preWaveInteractive) {
    // Read agent definition
    Read(`agents/plan-reviewer.md`)

    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: ${sessionFolder}/discoveries.ndjson\n\nGoal: ${task.description}\nScope: ${task.title}\nSession: ${sessionFolder}\n\n### Previous Context\n${buildPrevContext(task, tasks)}`
    })
    const result = wait({ ids: [agent], timeout_ms: 600000 })
    if (result.timed_out) {
      send_input({ id: agent, message: "Please finalize and output current findings." })
      wait({ ids: [agent], timeout_ms: 120000 })
    }
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed", findings: parseFindings(result),
      timestamp: getUtc8ISOString()
    }))
    close_agent({ id: agent })
    task.status = 'completed'
    task.findings = parseFindings(result)
  }

  // 4. Build prev_context for csv-wave tasks
  const pendingCsvTasks = csvTasks.filter(t => t.status === 'pending')
  for (const task of pendingCsvTasks) {
    task.prev_context = buildPrevContext(task, tasks)
  }

  if (pendingCsvTasks.length > 0) {
    // 5. Write wave CSV
    Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingCsvTasks))

    // 6. Determine instruction for this wave (use role-specific instruction)
    // Group tasks by role, build combined instruction
    const waveInstruction = buildWaveInstruction(pendingCsvTasks, sessionFolder, wave)

    // 7. Execute wave via spawn_agents_on_csv
    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: waveInstruction,
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          artifacts_produced: { type: "string" },
          error: { type: "string" }
        }
      }
    })

    // 8. Merge results into master CSV
    const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const r of results) {
      const t = tasks.find(t => t.id === r.id)
      if (t) Object.assign(t, r)
    }
  }

  // 9. Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 10. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // 11. Display wave summary
  const completed = waveTasks.filter(t => t.status === 'completed').length
  const failed = waveTasks.filter(t => t.status === 'failed').length
  const skipped = waveTasks.filter(t => t.status === 'skipped').length
  console.log(`Wave ${wave} Complete: ${completed} completed, ${failed} failed, ${skipped} skipped`)
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms

---

### Phase 3: Post-Wave Interactive (Completion Action)

**Objective**: Pipeline completion report and interactive completion choice.

```javascript
// 1. Generate pipeline summary
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')

console.log(`
============================================
TASK COMPLETE

Deliverables:
${completed.map(t => `  - ${t.id}: ${t.title} (${t.role})`).join('\n')}

Pipeline: ${completed.length}/${tasks.length} tasks
Duration: <elapsed>
Session: ${sessionFolder}
============================================
`)

// 2. Completion action
if (!AUTO_YES) {
  const choice = AskUserQuestion({
    questions: [{
      question: "Team pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, output final summary" },
        { label: "Keep Active", description: "Keep session for follow-up work" },
        { label: "Retry Failed", description: "Re-run failed tasks" }
      ]
    }]
  })
  // Handle choice accordingly
}
```

**Success Criteria**:
- Post-wave interactive processing complete
- User informed of results

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
// 1. Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// 2. Generate context.md
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
let contextMd = `# Team Coordinate Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

const maxWave = Math.max(...tasks.map(t => t.wave))
contextMd += `## Wave Execution\n\n`
for (let w = 1; w <= maxWave; w++) {
  const waveTasks = tasks.filter(t => t.wave === w)
  contextMd += `### Wave ${w}\n\n`
  for (const t of waveTasks) {
    const icon = t.status === 'completed' ? '[DONE]' : t.status === 'failed' ? '[FAIL]' : '[SKIP]'
    contextMd += `${icon} **${t.title}** [${t.role}] ${t.findings || ''}\n\n`
  }
}

Write(`${sessionFolder}/context.md`, contextMd)

// 3. Display final summary
console.log(`Results exported to: ${sessionFolder}/results.csv`)
console.log(`Report generated at: ${sessionFolder}/context.md`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"RESEARCH-001","type":"pattern_found","data":{"pattern_name":"Repository Pattern","location":"src/repos/","description":"Data access layer uses repository pattern"}}
{"ts":"2026-03-08T10:05:00Z","worker":"IMPL-001","type":"file_modified","data":{"file":"src/auth/jwt.ts","change":"Added JWT middleware","lines_added":45}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `pattern_found` | `{pattern_name, location, description}` | Design pattern identified |
| `file_modified` | `{file, change, lines_added}` | File change recorded |
| `dependency_found` | `{from, to, type}` | Dependency relationship discovered |
| `issue_found` | `{file, line, severity, description}` | Issue or bug discovered |
| `decision_made` | `{decision, rationale, impact}` | Design decision recorded |
| `artifact_produced` | `{name, path, producer, type}` | Deliverable created |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file, data.pattern_name}` key

---

## Dynamic Role Instruction Generation

The coordinator generates role-specific instruction templates during Phase 1. Each template is written to `role-instructions/{role-name}.md` and used as the `instruction` parameter for `spawn_agents_on_csv`.

**Generation Rules**:
1. Each instruction must be self-contained (agent has no access to master CSV)
2. Use `{column_name}` placeholders for CSV column substitution
3. Include session folder path as literal (not placeholder)
4. Include mandatory discovery board read/write steps
5. Include role-specific execution guidance based on responsibility_type
6. Include output schema matching tasks.csv output columns

See `instructions/agent-instruction.md` for the base instruction template that is customized per role.

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
| No capabilities detected | Default to single `general` role with TASK prefix |
| All capabilities merge to one | Valid: single-role execution, reduced overhead |
| Task description too vague | AskUserQuestion for clarification in Phase 0 |
| Continue mode: no session found | List available sessions, prompt user to select |
| Role instruction generation fails | Fall back to generic instruction template |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when interaction pattern requires it
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If a dependency failed, skip the dependent task
8. **Dynamic Roles**: All worker roles are generated at runtime from task analysis -- no static role registry
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
