---
name: team-uidesign
description: UI design team pipeline. Research existing design system, generate design tokens (W3C format), audit quality, and implement code. CSV wave pipeline with GC loop (designer <-> reviewer) and dual-track parallel support.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"UI design task description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults for scope/industry/constraints.

# Team UI Design

## Usage

```bash
$team-uidesign "Design a button component with tokens and accessibility"
$team-uidesign -c 3 "Create a complete design system for our SaaS dashboard"
$team-uidesign -y "Full design system redesign for healthcare portal"
$team-uidesign --continue "uds-saas-dashboard-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Systematic UI design pipeline: research existing design system, generate design tokens (W3C Design Tokens Format), audit for quality/accessibility, and implement production code. Roles: researcher, designer, reviewer, implementer -- dynamically assigned as CSV wave tasks with dependency ordering. Supports component (4-task), system (7-task), and full-system (8-task) pipeline modes. Designer <-> Reviewer Generator-Critic loop with max 2 rounds.

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|                    TEAM UI DESIGN WORKFLOW                          |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse UI design task description                             |
|     +- Select scope (component/system/full-system), industry        |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Signal detection: keyword scan -> pipeline inference          |
|     +- Pipeline selection (component/system/full-system)             |
|     +- Dependency graph from pipeline definition                     |
|     +- Classify tasks: csv-wave | interactive (exec_mode)            |
|     +- Compute dependency waves (topological sort)                   |
|     +- Generate tasks.csv with wave + exec_mode columns              |
|     +- User validates task breakdown (skip if -y)                    |
|                                                                     |
|  Phase 2: Wave Execution Engine (Extended)                          |
|     +- For each wave (1..N):                                        |
|     |   +- Execute pre-wave interactive tasks (if any)               |
|     |   +- Build wave CSV (filter csv-wave tasks for this wave)      |
|     |   +- Inject previous findings into prev_context column         |
|     |   +- spawn_agents_on_csv(wave CSV)                             |
|     |   +- Execute post-wave interactive tasks (if any)              |
|     |   +- Merge all results into master tasks.csv                   |
|     |   +- Check: any failed? -> skip dependents                     |
|     |   +- GC Loop: if audit fails, create DESIGN-fix + AUDIT-re     |
|     +- discoveries.ndjson shared across all modes (append-only)      |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Completion Action)                 |
|     +- Pipeline completion report with deliverables listing          |
|     +- Interactive completion choice (Archive/Keep/Export)            |
|     +- Final aggregation / report                                    |
|                                                                     |
|  Phase 4: Results Aggregation                                       |
|     +- Export final results.csv                                      |
|     +- Generate context.md with all findings                         |
|     +- Display summary: completed/failed/skipped per wave            |
|     +- Offer: view results | retry failed | done                     |
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
| Design system research (researcher) | `csv-wave` |
| Token system design (designer) | `csv-wave` |
| Component specification (designer) | `csv-wave` |
| 5-dimension audit (reviewer) | `csv-wave` |
| Token/component implementation (implementer) | `csv-wave` |
| GC loop fix revision (designer) | `csv-wave` |
| GC loop escalation (user decision on audit failure) | `interactive` |
| Pipeline completion action | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,pipeline_mode,scope,audit_type,deps,context_from,exec_mode,wave,status,findings,artifacts_produced,audit_score,audit_signal,error
"RESEARCH-001","Design system analysis","PURPOSE: Analyze existing design system...","researcher","component","full","","","","csv-wave","1","pending","","","","",""
"DESIGN-001","Design tokens + component spec","PURPOSE: Define design tokens...","designer","component","tokens","","RESEARCH-001","RESEARCH-001","csv-wave","2","pending","","","","",""
"AUDIT-001","Design audit","PURPOSE: 5-dimension quality audit...","reviewer","component","full","token-audit","DESIGN-001","DESIGN-001","csv-wave","3","pending","","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (PREFIX-NNN: RESEARCH, DESIGN, AUDIT, BUILD) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description with PURPOSE/TASK/CONTEXT/EXPECTED/CONSTRAINTS |
| `role` | Input | Role name: `researcher`, `designer`, `reviewer`, `implementer` |
| `pipeline_mode` | Input | Pipeline: `component`, `system`, `full-system` |
| `scope` | Input | Task scope: `full`, `tokens`, `components` |
| `audit_type` | Input | Audit type: `token-audit`, `component-audit`, `final-audit` (empty for non-reviewer) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `artifacts_produced` | Output | Semicolon-separated paths of produced artifacts |
| `audit_score` | Output | Audit weighted score (0-10, empty for non-reviewer tasks) |
| `audit_signal` | Output | Audit signal: `audit_passed`, `audit_result`, `fix_required` (empty for non-reviewer) |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| GC Loop Handler | agents/gc-loop-handler.md | 2.3 (send_input cycle) | Handle audit GC loop escalation decisions | post-wave |
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
| `task-analysis.json` | Phase 0/1 output: scope, pipeline, industry | Created in Phase 1 |
| `role-instructions/` | Per-role instruction templates for CSV agents | Created in Phase 1 |
| `artifacts/` | All deliverables: research, design, audit, build artifacts | Created by agents |
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
|   +-- researcher.md
|   +-- designer.md
|   +-- reviewer.md
|   +-- implementer.md
+-- artifacts/                 # All deliverables
|   +-- research/
|   |   +-- design-system-analysis.json
|   |   +-- component-inventory.json
|   |   +-- accessibility-audit.json
|   |   +-- design-intelligence.json
|   +-- design/
|   |   +-- design-tokens.json
|   |   +-- component-specs/
|   |   +-- layout-specs/
|   +-- audit/
|   |   +-- audit-001.md
|   +-- build/
|       +-- token-files/
|       +-- component-files/
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
const sessionId = `uds-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts/research ${sessionFolder}/artifacts/design/component-specs ${sessionFolder}/artifacts/design/layout-specs ${sessionFolder}/artifacts/audit ${sessionFolder}/artifacts/build/token-files ${sessionFolder}/artifacts/build/component-files ${sessionFolder}/role-instructions ${sessionFolder}/interactive ${sessionFolder}/wisdom`)

Write(`${sessionFolder}/discoveries.ndjson`, '')
Write(`${sessionFolder}/wisdom/learnings.md`, '# Learnings\n')
Write(`${sessionFolder}/wisdom/decisions.md`, '# Decisions\n')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse UI design task, clarify scope/industry/constraints, prepare for decomposition.

**Workflow**:

1. **Parse user task description** from $ARGUMENTS

2. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/uds-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2
   - If active session found: ask user whether to resume or start new

3. **Clarify scope and industry** (skip if AUTO_YES):

   **Scope Selection**:

   | Option | Pipeline | Task Count |
   |--------|----------|------------|
   | Single component | component | 4 tasks (linear) |
   | Component system | system | 7 tasks (dual-track parallel) |
   | Full design system | full-system | 8 tasks (dual-track + final audit) |

   **Industry Selection**:

   | Option | Strictness |
   |--------|------------|
   | SaaS/Tech | standard |
   | E-commerce/Retail | standard |
   | Healthcare/Finance | strict (extra accessibility) |
   | Education/Content | standard |
   | Other | standard |

4. **Signal Detection** for pipeline selection:

   | Signal | Keywords | Pipeline Hint |
   |--------|----------|---------------|
   | Component | component, button, card, input, modal | component |
   | System | design system, token, theme, multiple components | system |
   | Full | complete, full, all components, redesign | full-system |
   | Accessibility | accessibility, a11y, wcag | component or system |

5. **Complexity Scoring**:

   | Factor | Points |
   |--------|--------|
   | Single component | +1 |
   | Component system | +2 |
   | Full design system | +3 |
   | Accessibility required | +1 |
   | Multiple industries/constraints | +1 |

   Results: 1-2 component, 3-4 system, 5+ full-system.

6. **Industry Detection**:

   | Keywords | Industry |
   |----------|----------|
   | saas, dashboard, analytics | SaaS/Tech |
   | shop, cart, checkout | E-commerce |
   | medical, patient, healthcare | Healthcare |
   | bank, finance, payment | Finance |
   | edu, course, learning | Education/Content |
   | Default | SaaS/Tech |

7. Record: pipeline_mode, industry, complexity

**Success Criteria**:
- Scope, industry, constraints determined
- Pipeline mode selected (component/system/full-system)

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Build task dependency graph, generate tasks.csv and per-role instruction templates.

**Decomposition Rules**:

1. **Pipeline Selection** based on scope:

   | Scope | Pipeline | Tasks |
   |-------|----------|-------|
   | component | RESEARCH-001 -> DESIGN-001 -> AUDIT-001 -> BUILD-001 | 4 |
   | system | RESEARCH-001 -> DESIGN-001 -> AUDIT-001 -> [DESIGN-002 + BUILD-001] -> AUDIT-002 -> BUILD-002 | 7 |
   | full-system | system chain + AUDIT-003 after BUILD-002 | 8 |

2. **Task Description Template**: Every task description uses PURPOSE/TASK/CONTEXT/EXPECTED/CONSTRAINTS format

3. **Role Instruction Generation**: Write per-role instruction templates to `role-instructions/{role}.md` using the base instruction template customized for each role (researcher, designer, reviewer, implementer)

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Research analysis pass (researcher) | `csv-wave` |
| Token design pass (designer) | `csv-wave` |
| Component spec pass (designer) | `csv-wave` |
| Audit pass (reviewer) | `csv-wave` |
| Implementation pass (implementer) | `csv-wave` |
| GC fix revision (designer) | `csv-wave` |
| All standard pipeline tasks | `csv-wave` |

**Wave Computation**: Kahn's BFS topological sort with depth tracking.

```javascript
// Generate per-role instruction templates
for (const role of ['researcher', 'designer', 'reviewer', 'implementer']) {
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
    Read(`agents/gc-loop-handler.md`)
    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: agents/gc-loop-handler.md\n2. Read: ${sessionFolder}/discoveries.ndjson\n\nGoal: ${task.description}\nScope: ${task.title}\nSession: ${sessionFolder}\n\n### Previous Context\n${buildPrevContext(task, tasks)}`
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
          audit_score: { type: "string" },
          audit_signal: { type: "string" },
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

    // 9. GC Loop Check: if a reviewer task returned fix_required
    const auditResults = results.filter(r => r.id.startsWith('AUDIT') && r.audit_signal === 'fix_required')
    for (const ar of auditResults) {
      if (gcRound < MAX_GC_ROUNDS) {
        gcRound++
        const fixId = `DESIGN-fix-${gcRound}`
        const recheckId = `AUDIT-recheck-${gcRound}`
        tasks.push({
          id: fixId, title: `Fix audit issues (round ${gcRound})`,
          description: `PURPOSE: Address audit feedback from ${ar.id} | Success: All critical/high issues resolved\nTASK:\n- Parse audit feedback for specific issues\n- Apply targeted fixes to design tokens/specs\n- Re-validate affected artifacts\nCONTEXT:\n- Session: ${sessionFolder}\n- Upstream: artifacts/audit/\nEXPECTED: Fixed design artifacts\nCONSTRAINTS: Targeted fixes only`,
          role: 'designer', pipeline_mode: tasks[0].pipeline_mode, scope: 'full',
          audit_type: '', deps: ar.id, context_from: ar.id,
          exec_mode: 'csv-wave', wave: wave + 1, status: 'pending',
          findings: '', artifacts_produced: '', audit_score: '', audit_signal: '', error: ''
        })
        tasks.push({
          id: recheckId, title: `Audit recheck (round ${gcRound})`,
          description: `PURPOSE: Re-audit after fixes | Success: Score >= 8, critical == 0\nTASK:\n- Execute 5-dimension audit on fixed artifacts\n- Focus on previously flagged issues\nCONTEXT:\n- Session: ${sessionFolder}\n- Audit type: token-audit\nEXPECTED: artifacts/audit/audit-recheck-${gcRound}.md`,
          role: 'reviewer', pipeline_mode: tasks[0].pipeline_mode, scope: 'full',
          audit_type: 'token-audit', deps: fixId, context_from: fixId,
          exec_mode: 'csv-wave', wave: wave + 2, status: 'pending',
          findings: '', artifacts_produced: '', audit_score: '', audit_signal: '', error: ''
        })
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
- GC loop (designer <-> reviewer) handled with max 2 rounds
- discoveries.ndjson accumulated across all waves and mechanisms

---

### Phase 3: Post-Wave Interactive (Completion Action)

**Objective**: Pipeline completion report with deliverables listing and interactive completion choice.

```javascript
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')
const failed = tasks.filter(t => t.status === 'failed')

const deliverables = [
  { name: "Design System Analysis", path: `${sessionFolder}/artifacts/research/design-system-analysis.json` },
  { name: "Component Inventory", path: `${sessionFolder}/artifacts/research/component-inventory.json` },
  { name: "Accessibility Audit", path: `${sessionFolder}/artifacts/research/accessibility-audit.json` },
  { name: "Design Intelligence", path: `${sessionFolder}/artifacts/research/design-intelligence.json` },
  { name: "Design Tokens", path: `${sessionFolder}/artifacts/design/design-tokens.json` },
  { name: "Component Specs", path: `${sessionFolder}/artifacts/design/component-specs/` },
  { name: "Audit Reports", path: `${sessionFolder}/artifacts/audit/` },
  { name: "Token Files", path: `${sessionFolder}/artifacts/build/token-files/` },
  { name: "Component Files", path: `${sessionFolder}/artifacts/build/component-files/` }
]

console.log(`
============================================
UI DESIGN TEAM COMPLETE

Pipeline: ${completed.length}/${tasks.length} tasks (${tasks[0]?.pipeline_mode} mode)
GC Rounds: ${gcRound}/${MAX_GC_ROUNDS}
Session: ${sessionFolder}

Deliverables:
${deliverables.map(d => `  - ${d.name}: ${d.path}`).join('\n')}
============================================
`)

if (!AUTO_YES) {
  // Spawn completion handler interactive agent
  Read(`agents/completion-handler.md`)
  const agent = spawn_agent({
    message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: agents/completion-handler.md\n2. Read: ${sessionFolder}/tasks.csv\n\nGoal: Handle pipeline completion action\nSession: ${sessionFolder}\nDeliverables: ${JSON.stringify(deliverables)}`
  })
  const result = wait({ ids: [agent], timeout_ms: 300000 })
  close_agent({ id: agent })
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
let contextMd = `# UI Design Report\n\n`
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
    if (t.audit_score) contextMd += ` Score: ${t.audit_score}/10 (${t.audit_signal})`
    contextMd += ` ${t.findings || ''}\n\n`
  }
}

contextMd += `## Audit Summary\n\n`
const auditResults = tasks.filter(t => t.role === 'reviewer' && t.audit_score)
for (const a of auditResults) {
  contextMd += `- **${a.id}**: Score ${a.audit_score}/10 - ${a.audit_signal}\n`
}

contextMd += `\n## GC Loop Summary\n`
contextMd += `- Rounds used: ${gcRound}/${MAX_GC_ROUNDS}\n`

Write(`${sessionFolder}/context.md`, contextMd)
console.log(`Results exported to: ${sessionFolder}/results.csv`)
console.log(`Report generated at: ${sessionFolder}/context.md`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated with audit summary
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"RESEARCH-001","type":"tech_stack_detected","data":{"stack":"react","framework":"nextjs","ui_lib":"shadcn"}}
{"ts":"2026-03-08T10:05:00Z","worker":"DESIGN-001","type":"token_generated","data":{"category":"color","count":24,"supports_dark_mode":true}}
{"ts":"2026-03-08T10:10:00Z","worker":"BUILD-001","type":"file_modified","data":{"file":"tokens.css","change":"Generated CSS custom properties","lines_added":85}}
{"ts":"2026-03-08T10:15:00Z","worker":"AUDIT-001","type":"issue_found","data":{"file":"design-tokens.json","line":0,"severity":"high","description":"Missing dark mode variant for semantic color tokens"}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `tech_stack_detected` | `{stack, framework, ui_lib}` | Tech stack identified by researcher |
| `design_pattern_found` | `{pattern_name, location, description}` | Existing design pattern in codebase |
| `token_generated` | `{category, count, supports_dark_mode}` | Design token category created |
| `file_modified` | `{file, change, lines_added}` | File change recorded |
| `issue_found` | `{file, line, severity, description}` | Audit issue discovered |
| `anti_pattern_violation` | `{pattern, file, line, description}` | Design anti-pattern detected |
| `artifact_produced` | `{name, path, producer, type}` | Deliverable created |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file}` key

---

## Pipeline Definitions

### Component Mode (4 tasks, linear)

```
RESEARCH-001 --> DESIGN-001 --> AUDIT-001 --> BUILD-001
[researcher]     [designer]     [reviewer]    [implementer]
   wave 1          wave 2         wave 3        wave 4
```

### System Mode (7 tasks, dual-track parallel)

```
RESEARCH-001 --> DESIGN-001 --> AUDIT-001 --> DESIGN-002 --+
[researcher]     [designer]     [reviewer]    [designer]    |
                                              BUILD-001   --+--> AUDIT-002 --> BUILD-002
                                              [implementer]      [reviewer]    [implementer]
   wave 1          wave 2         wave 3        wave 4            wave 5        wave 6
```

### Full-System Mode (8 tasks, dual-track + final audit)

```
Same as System + AUDIT-003 after BUILD-002

BUILD-002 --> AUDIT-003
              [reviewer: final-audit]
   wave 6      wave 7
```

### Generator-Critic Loop (designer <-> reviewer)

```
designer (Generator) -> design artifacts -> reviewer (Critic)
                      <- audit feedback  <-
                         (max 2 rounds)

Convergence: audit.score >= 8 AND audit.critical_count === 0
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
| Audit score < 6 over 2 GC rounds | Escalate to user for manual intervention |
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
8. **GC Loop Cap**: Max 2 generator-critic rounds between designer and reviewer
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
