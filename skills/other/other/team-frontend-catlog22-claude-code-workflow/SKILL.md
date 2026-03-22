---
name: team-frontend
description: Frontend development team with built-in ui-ux-pro-max design intelligence. Covers requirement analysis, design system generation, frontend implementation, and quality assurance. CSV wave pipeline with interactive QA gates.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"frontend task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults for scope/industry/constraints.

# Team Frontend Development

## Usage

```bash
$team-frontend "Build a SaaS dashboard with user management and analytics"
$team-frontend -c 3 "Create a healthcare patient portal with WCAG AA compliance"
$team-frontend -y "Implement e-commerce product listing page with dark mode"
$team-frontend --continue "fe-saas-dashboard-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Unified frontend development team: analyze requirements, retrieve design intelligence (ui-ux-pro-max), generate design token system, architect components, implement code, and run 5-dimension quality audit. Roles: analyst, architect, developer, qa -- dynamically assigned as CSV wave tasks with dependency ordering. Supports page (4-task), feature (5-task), and system (7-task) pipeline modes.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|              TEAM FRONTEND WORKFLOW                                 |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse frontend task description                              |
|     +- Select scope (page/feature/system), industry, constraints    |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Signal detection: keyword scan -> capability inference       |
|     +- Pipeline selection (page: 4-task, feature: 5-task, system)   |
|     +- Dependency graph from pipeline definition                    |
|     +- Classify tasks: csv-wave | interactive (exec_mode)           |
|     +- Compute dependency waves (topological sort)                  |
|     +- Generate tasks.csv with wave + exec_mode columns             |
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
|     |   +- GC Loop: if QA fails, create DEV-fix + QA-recheck        |
|     +- discoveries.ndjson shared across all modes (append-only)     |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion Action)                 |
|     +- Pipeline completion report with deliverables listing         |
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
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, revision cycles, user approval |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Requirement analysis (analyst) | `csv-wave` |
| Architecture design (architect) | `csv-wave` |
| Code implementation (developer) | `csv-wave` |
| QA audit (qa) | `csv-wave` |
| Architecture review gate (qa approving architecture before dev starts) | `interactive` |
| GC loop revision (developer fixing QA issues) | `csv-wave` |
| Pipeline completion action | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,pipeline_mode,scope,review_type,deps,context_from,exec_mode,wave,status,findings,artifacts_produced,qa_score,qa_verdict,error
"ANALYZE-001","Requirement analysis + design intelligence","PURPOSE: Analyze frontend requirements and retrieve design intelligence | Success: design-intelligence.json produced","analyst","feature","full","","","","csv-wave","1","pending","","","","",""
"ARCH-001","Design token system + component architecture","PURPOSE: Define design token system and component specs | Success: design-tokens.json + component specs produced","architect","feature","full","","ANALYZE-001","ANALYZE-001","csv-wave","2","pending","","","","",""
"QA-001","Architecture review","PURPOSE: Review architecture artifacts before development | Success: Architecture approved","qa","feature","full","architecture-review","ARCH-001","ARCH-001","csv-wave","3","pending","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN format: ANALYZE, ARCH, DEV, QA) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description with PURPOSE/TASK/CONTEXT/EXPECTED/CONSTRAINTS |
| `role` | Input | Role name: `analyst`, `architect`, `developer`, `qa` |
| `pipeline_mode` | Input | Pipeline: `page`, `feature`, `system` |
| `scope` | Input | Task scope: `full`, `tokens`, `components` |
| `review_type` | Input | QA review type: `architecture-review`, `code-review`, `final` (empty for non-QA) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `qa_score` | Output | QA weighted score (0-10, empty for non-QA tasks) |
| `qa_verdict` | Output | QA verdict: `PASSED`, `PASSED_WITH_WARNINGS`, `FIX_REQUIRED` (empty for non-QA) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| QA Gate Reviewer | agents/qa-gate-reviewer.md | 2.3 (send_input cycle) | Review QA verdict and handle GC loop decisions | post-wave |
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
| `task-analysis.json` | Phase 0/1 output: capabilities, pipeline, roles | Created in Phase 1 |
| `role-instructions/` | Per-role instruction templates for CSV agents | Created in Phase 1 |
| `artifacts/` | All deliverables: design-intelligence.json, design-tokens.json, component-specs/, QA audits | Created by agents |
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
+-- role-instructions/         # Per-role instruction templates
|   +-- analyst.md
|   +-- architect.md
|   +-- developer.md
|   +-- qa.md
+-- artifacts/                 # All deliverables
|   +-- analysis/
|   |   +-- design-intelligence.json
|   |   +-- requirements.md
|   +-- architecture/
|   |   +-- design-tokens.json
|   |   +-- component-specs/
|   |   +-- project-structure.md
|   +-- qa/
|   |   +-- audit-001.md
|   +-- build/
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
const sessionId = `fe-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts/analysis ${sessionFolder}/artifacts/architecture/component-specs ${sessionFolder}/artifacts/qa ${sessionFolder}/artifacts/build ${sessionFolder}/role-instructions ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

Write(`${sessionFolder}/discoveries.ndjson`, '')
Write(`${sessionFolder}/wisdom/learnings.md`, '# Learnings\n')
Write(`${sessionFolder}/wisdom/decisions.md`, '# Decisions\n')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse frontend task, clarify scope/industry/constraints, prepare for decomposition.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/fe-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **Clarify scope and industry** (skip if AUTO_YES):

   **Scope Selection**:

   | Option | Pipeline | Task Count |
   |--------|----------|------------|
   | Single page | page | 4 tasks (linear) |
   | Multi-component feature | feature | 5 tasks (with arch review gate) |
   | Full frontend system | system | 7 tasks (dual-track parallel) |

   **Industry Selection**:

   | Option | Strictness |
   |--------|------------|
   | SaaS/Tech | standard |
   | E-commerce/Retail | standard |
   | Healthcare/Finance | strict (extra accessibility) |
   | Other | standard |

   **Design Constraints** (multi-select): Existing design system, WCAG AA, Responsive, Dark mode

4. **Record requirements**: mode, scope, industry, constraints

5. **Signal Detection** for pipeline selection:

   | Signal | Keywords | Capability |
   |--------|----------|------------|
   | Analysis | analyze, requirements, design intelligence | analyst |
   | Architecture | design tokens, component architecture, design system | architect |
   | Implementation | implement, build, code, develop, page, component | developer |
   | Quality | review, audit, quality, test, accessibility | qa |

6. **Complexity Scoring**:

   | Factor | Points |
   |--------|--------|
   | ui-ux-pro-max integration needed | +1 |
   | Existing design system detected | +1 |
   | Accessibility strict mode (healthcare/finance) | +2 |
   | Multiple tech stacks | +2 |
   | Dark mode required | +1 |

   Results: 1-2 page, 3-4 feature, 5+ system. Default: feature.

**Success Criteria**:
- Scope, industry, constraints determined
- Pipeline mode selected (page/feature/system)

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Build task dependency graph, generate tasks.csv and per-role instruction templates.

**Decomposition Rules**:

1. **Pipeline Selection** based on scope:

   | Scope | Pipeline | Tasks |
   |-------|----------|-------|
   | page | ANALYZE-001 -> ARCH-001 -> DEV-001 -> QA-001 | 4 |
   | feature | ANALYZE-001 -> ARCH-001 -> QA-001(arch) -> DEV-001 -> QA-002(code) | 5 |
   | system | ANALYZE-001 -> ARCH-001 -> QA-001(arch) -> [ARCH-002 + DEV-001] -> QA-002 -> DEV-002 -> QA-003(final) | 7 |

2. **Task Description Template**: Every task description uses PURPOSE/TASK/CONTEXT/EXPECTED/CONSTRAINTS format (see dispatch.md for full templates)

3. **Role Instruction Generation**: Write per-role instruction templates to `role-instructions/{role}.md` using the base instruction template customized for each role (analyst, architect, developer, qa)

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Analyst analysis pass | `csv-wave` |
| Architect design pass | `csv-wave` |
| Developer implementation pass | `csv-wave` |
| QA audit pass | `csv-wave` |
| All standard pipeline tasks | `csv-wave` |

**Wave Computation**: Kahn's BFS topological sort with depth tracking.

```javascript
// Generate per-role instruction templates
for (const role of ['analyst', 'architect', 'developer', 'qa']) {
  const instruction = generateRoleInstruction(role, sessionFolder)
  Write(`${sessionFolder}/role-instructions/${role}.md`, instruction)
}

// Generate tasks.csv from pipeline definition
const tasks = buildTasksCsv(pipelineMode, requirement, sessionFolder, industry, constraints)
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
let gcRound = 0
const MAX_GC_ROUNDS = 2

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

  // 3. Execute pre-wave interactive tasks (if any)
  const preWaveInteractive = interactiveTasks.filter(t => t.status === 'pending')
  for (const task of preWaveInteractive) {
    Read(`agents/qa-gate-reviewer.md`)
    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: agents/qa-gate-reviewer.md\n2. Read: ${sessionFolder}/discoveries.ndjson\n\nGoal: ${task.description}\nScope: ${task.title}\nSession: ${sessionFolder}\n\n### Previous Context\n${buildPrevContext(task, tasks)}`
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

    // 6. Build instruction per role group
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
          qa_score: { type: "string" },
          qa_verdict: { type: "string" },
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

    // 9. GC Loop Check: if a QA task returned FIX_REQUIRED
    const qaResults = results.filter(r => r.id.startsWith('QA') && r.qa_verdict === 'FIX_REQUIRED')
    for (const qr of qaResults) {
      if (gcRound < MAX_GC_ROUNDS) {
        gcRound++
        // Create DEV-fix and QA-recheck tasks, append to tasks array
        const fixId = `DEV-fix-${gcRound}`
        const recheckId = `QA-recheck-${gcRound}`
        tasks.push({
          id: fixId, title: `Fix QA issues (round ${gcRound})`,
          description: `PURPOSE: Fix issues from ${qr.id} audit | Success: All critical/high resolved\nTASK:\n- Load QA audit report\n- Fix critical/high issues\n- Re-validate\nCONTEXT:\n- Session: ${sessionFolder}\n- Upstream: ${sessionFolder}/artifacts/qa/\nEXPECTED: Fixed source files\nCONSTRAINTS: Targeted fixes only`,
          role: 'developer', pipeline_mode: tasks[0].pipeline_mode, scope: 'full',
          review_type: '', deps: qr.id, context_from: qr.id,
          exec_mode: 'csv-wave', wave: wave + 1, status: 'pending',
          findings: '', artifacts_produced: '', qa_score: '', qa_verdict: '', error: ''
        })
        tasks.push({
          id: recheckId, title: `QA recheck (round ${gcRound})`,
          description: `PURPOSE: Re-audit after fixes | Success: Score >= 8, critical == 0\nTASK:\n- Execute 5-dimension audit on fixed code\n- Focus on previously flagged issues\nCONTEXT:\n- Session: ${sessionFolder}\n- Review type: code-review\nEXPECTED: ${sessionFolder}/artifacts/qa/audit-recheck-${gcRound}.md`,
          role: 'qa', pipeline_mode: tasks[0].pipeline_mode, scope: 'full',
          review_type: 'code-review', deps: fixId, context_from: fixId,
          exec_mode: 'csv-wave', wave: wave + 2, status: 'pending',
          findings: '', artifacts_produced: '', qa_score: '', qa_verdict: '', error: ''
        })
        // Extend maxWave
      }
    }
  }

  // 10. Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 11. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // 12. Display wave summary
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
- GC loop (developer <-> qa) handled with max 2 rounds
- discoveries.ndjson accumulated across all waves and mechanisms

---

### Phase 3: Post-Wave Interactive (Completion Action)

**Objective**: Pipeline completion report with deliverables listing and interactive completion choice.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')

// List deliverables
const deliverables = [
  { name: "Design Intelligence", path: `${sessionFolder}/artifacts/analysis/design-intelligence.json` },
  { name: "Requirements", path: `${sessionFolder}/artifacts/analysis/requirements.md` },
  { name: "Design Tokens", path: `${sessionFolder}/artifacts/architecture/design-tokens.json` },
  { name: "Component Specs", path: `${sessionFolder}/artifacts/architecture/component-specs/` },
  { name: "Project Structure", path: `${sessionFolder}/artifacts/architecture/project-structure.md` },
  { name: "QA Audits", path: `${sessionFolder}/artifacts/qa/` }
]

console.log(`
============================================
FRONTEND TEAM COMPLETE

Pipeline: ${completed.length}/${tasks.length} tasks (${tasks[0]?.pipeline_mode} mode)
GC Rounds: ${gcRound}/${MAX_GC_ROUNDS}
Session: ${sessionFolder}

Deliverables:
${deliverables.map(d => `  - ${d.name}: ${d.path}`).join('\n')}
============================================
`)

if (!AUTO_YES) {
  AskUserQuestion({
    questions: [{
      question: "Frontend pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session, output final summary" },
        { label: "Keep Active", description: "Keep session for follow-up work" },
        { label: "Export Results", description: "Export design tokens and component specs" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Post-wave interactive processing complete
- User informed of deliverables and pipeline status

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
let contextMd = `# Frontend Development Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Pipeline**: ${tasks[0]?.pipeline_mode} mode\n`
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
    contextMd += `${icon} **${t.title}** [${t.role}]`
    if (t.qa_score) contextMd += ` Score: ${t.qa_score}/10 (${t.qa_verdict})`
    contextMd += ` ${t.findings || ''}\n\n`
  }
}

contextMd += `## QA Summary\n\n`
const qaResults = tasks.filter(t => t.role === 'qa' && t.qa_score)
for (const q of qaResults) {
  contextMd += `- **${q.id}**: Score ${q.qa_score}/10 - ${q.qa_verdict}\n`
}

Write(`${sessionFolder}/context.md`, contextMd)
console.log(`Results exported to: ${sessionFolder}/results.csv`)
console.log(`Report generated at: ${sessionFolder}/context.md`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated with QA summary
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"ANALYZE-001","type":"tech_stack_detected","data":{"stack":"react","framework":"nextjs","ui_lib":"shadcn"}}
{"ts":"2026-03-08T10:05:00Z","worker":"ARCH-001","type":"token_generated","data":{"category":"color","count":24,"supports_dark_mode":true}}
{"ts":"2026-03-08T10:10:00Z","worker":"DEV-001","type":"file_modified","data":{"file":"src/styles/tokens.css","change":"Generated CSS custom properties","lines_added":85}}
{"ts":"2026-03-08T10:15:00Z","worker":"QA-001","type":"issue_found","data":{"file":"src/components/Button.tsx","line":42,"severity":"high","description":"Missing cursor-pointer on button"}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `tech_stack_detected` | `{stack, framework, ui_lib}` | Tech stack identified by analyst |
| `design_pattern_found` | `{pattern_name, location, description}` | Existing design pattern in codebase |
| `token_generated` | `{category, count, supports_dark_mode}` | Design token category created |
| `file_modified` | `{file, change, lines_added}` | File change recorded |
| `issue_found` | `{file, line, severity, description}` | QA issue discovered |
| `anti_pattern_violation` | `{pattern, file, line, description}` | Industry anti-pattern detected |
| `artifact_produced` | `{name, path, producer, type}` | Deliverable created |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file}` key

---

## Pipeline Definitions

### Page Mode (4 tasks, linear)

```
ANALYZE-001 --> ARCH-001 --> DEV-001 --> QA-001
[analyst]       [architect]  [developer]  [qa:code-review]
   wave 1         wave 2       wave 3       wave 4
```

### Feature Mode (5 tasks, with architecture review gate)

```
ANALYZE-001 --> ARCH-001 --> QA-001 --> DEV-001 --> QA-002
[analyst]       [architect]  [qa:arch]   [developer]  [qa:code-review]
   wave 1         wave 2       wave 3       wave 4       wave 5
```

### System Mode (7 tasks, dual-track parallel)

```
ANALYZE-001 --> ARCH-001 --> QA-001 --> ARCH-002 --+
[analyst]       [architect]  [qa:arch]  [architect] |
                                        DEV-001   --+--> QA-002 --> DEV-002 --> QA-003
                                        [dev:tokens]     [qa]      [dev:comp]  [qa:final]
   wave 1         wave 2       wave 3     wave 4          wave 5     wave 6     wave 7
```

### Generator-Critic Loop (developer <-> qa)

```
developer (Generator) -> QA artifact -> qa (Critic)
                      <- QA feedback <-
                         (max 2 rounds)

Convergence: qa.score >= 8 && qa.critical_count === 0
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
| All agents in wave failed | Log error, offer retry or abort |
| CSV parse error | Validate CSV format before execution, show line number |
| discoveries.ndjson corrupt | Ignore malformed lines, continue with valid entries |
| QA score < 6 over 2 GC rounds | Escalate to user for manual intervention |
| ui-ux-pro-max unavailable | Degrade to LLM general design knowledge |
| Task description too vague | AskUserQuestion for clarification in Phase 0 |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when interaction pattern requires it
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson
7. **Skip on Failure**: If a dependency failed, skip the dependent task
8. **GC Loop Cap**: Max 2 generator-critic rounds between developer and qa
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
