---
name: team-ultra-analyze
description: Deep collaborative analysis pipeline. Multi-perspective exploration, deep analysis, user-driven discussion loops, and cross-perspective synthesis. Supports Quick, Standard, and Deep pipeline modes.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] [--mode quick|standard|deep] \"analysis topic\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Ultra Analyze

## Usage

```bash
$team-ultra-analyze "Analyze authentication module architecture and security"
$team-ultra-analyze -c 4 --mode deep "Deep analysis of payment processing pipeline"
$team-ultra-analyze -y --mode quick "Quick overview of API endpoint structure"
$team-ultra-analyze --continue "uan-auth-analysis-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--mode`: Pipeline mode override (quick|standard|deep)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Deep collaborative analysis with multi-perspective exploration, deep analysis, user-driven discussion loops, and cross-perspective synthesis. Each perspective gets its own explorer and analyst, working in parallel. Discussion rounds allow the user to steer analysis depth and direction.

**Execution Model**: Hybrid — CSV wave pipeline (primary) + individual agent spawn (secondary for discussion feedback loop)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TEAM ULTRA ANALYZE WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Pre-Wave Interactive                                           │
│     ├─ Topic parsing + dimension detection                               │
│     ├─ Pipeline mode selection (quick/standard/deep)                     │
│     ├─ Perspective assignment                                            │
│     └─ Output: refined requirements for decomposition                    │
│                                                                          │
│  Phase 1: Requirement → CSV + Classification                             │
│     ├─ Parse topic into exploration + analysis + discussion + synthesis  │
│     ├─ Assign roles: explorer, analyst, discussant, synthesizer          │
│     ├─ Classify tasks: csv-wave | interactive (exec_mode)                │
│     ├─ Compute dependency waves (topological sort → depth grouping)      │
│     ├─ Generate tasks.csv with wave + exec_mode columns                  │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 2: Wave Execution Engine (Extended)                               │
│     ├─ For each wave (1..N):                                             │
│     │   ├─ Build wave CSV (filter csv-wave tasks for this wave)          │
│     │   ├─ Inject previous findings into prev_context column             │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Execute post-wave interactive tasks (if any)                  │
│     │   ├─ Merge all results into master tasks.csv                       │
│     │   └─ Check: any failed? → skip dependents                         │
│     └─ discoveries.ndjson shared across all modes (append-only)          │
│                                                                          │
│  Phase 3: Post-Wave Interactive (Discussion Loop)                        │
│     ├─ After discussant completes: user feedback gate                    │
│     ├─ User chooses: continue deeper | adjust direction | done           │
│     ├─ Creates dynamic tasks (DISCUSS-N, ANALYZE-fix-N) as needed        │
│     └─ Max discussion rounds: quick=0, standard=1, deep=5               │
│                                                                          │
│  Phase 4: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Display summary: completed/failed/skipped per wave                │
│     └─ Offer: view results | export | archive                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Task Classification Rules

Each task is classified by `exec_mode`:

| exec_mode | Mechanism | Criteria |
|-----------|-----------|----------|
| `csv-wave` | `spawn_agents_on_csv` | One-shot, structured I/O, no multi-round interaction |
| `interactive` | `spawn_agent`/`wait`/`send_input`/`close_agent` | Multi-round, user feedback, direction control |

**Classification Decision**:

| Task Property | Classification |
|---------------|---------------|
| Codebase exploration (single perspective) | `csv-wave` |
| Parallel exploration (multiple perspectives) | `csv-wave` (parallel in same wave) |
| Deep analysis (single perspective) | `csv-wave` |
| Parallel analysis (multiple perspectives) | `csv-wave` (parallel in same wave) |
| Direction-fix analysis (adjusted focus) | `csv-wave` |
| Discussion processing (aggregate results) | `csv-wave` |
| Final synthesis (cross-perspective integration) | `csv-wave` |
| Discussion feedback gate (user interaction) | `interactive` |
| Topic clarification (Phase 0) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,perspective,dimensions,discussion_round,discussion_type,deps,context_from,exec_mode,wave,status,findings,error
"EXPLORE-001","Explore from technical perspective","Search codebase from technical perspective. Collect files, patterns, findings.","explorer","technical","architecture;implementation","0","","","","csv-wave","1","pending","",""
"ANALYZE-001","Deep analysis from technical perspective","Analyze exploration results from technical perspective. Generate insights with confidence levels.","analyst","technical","architecture;implementation","0","","EXPLORE-001","EXPLORE-001","csv-wave","2","pending","",""
"DISCUSS-001","Initial discussion round","Aggregate all analysis results. Identify convergent themes, conflicts, top discussion points.","discussant","","","1","initial","ANALYZE-001;ANALYZE-002","ANALYZE-001;ANALYZE-002","csv-wave","3","pending","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `role` | Input | Worker role: explorer, analyst, discussant, synthesizer |
| `perspective` | Input | Analysis perspective: technical, architectural, business, domain_expert |
| `dimensions` | Input | Analysis dimensions (semicolon-separated): architecture, implementation, performance, security, concept, comparison, decision |
| `discussion_round` | Input | Discussion round number (0 = N/A, 1+ = round number) |
| `discussion_type` | Input | Discussion type: initial, deepen, direction-adjusted, specific-questions |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
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
| discussion-feedback | agents/discussion-feedback.md | 2.3 (wait-respond) | Collect user feedback after discussion round, create dynamic tasks | post-wave (after discussant wave) |
| topic-analyzer | agents/topic-analyzer.md | 2.3 (wait-respond) | Parse topic, detect dimensions, select pipeline mode and perspectives | standalone (Phase 0) |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs, **you MUST immediately `Read` the corresponding agent.md** to reload.

---

## Output Artifacts

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `tasks.csv` | Master state — all tasks with status/findings | Updated after each wave |
| `wave-{N}.csv` | Per-wave input (temporary, csv-wave tasks only) | Created before wave, deleted after |
| `results.csv` | Final export of all task results | Created in Phase 4 |
| `discoveries.ndjson` | Shared exploration board (all agents, both modes) | Append-only, carries across waves |
| `context.md` | Human-readable execution report | Created in Phase 4 |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
├── tasks.csv                  # Master state (all tasks, both modes)
├── results.csv                # Final results export
├── discoveries.ndjson         # Shared discovery board (all agents)
├── context.md                 # Human-readable report
├── wave-{N}.csv               # Temporary per-wave input (csv-wave only)
└── interactive/               # Interactive task artifacts
    └── {id}-result.json       # Per-task results
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
const modeMatch = $ARGUMENTS.match(/--mode\s+(quick|standard|deep)/)
const explicitMode = modeMatch ? modeMatch[1] : null

// Clean requirement text (remove flags)
const topic = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+|--mode\s+\w+/g, '')
  .trim()

const slug = topic.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
let sessionId = `uan-${slug}-${dateStr}`
let sessionFolder = `.workflow/.csv-wave/${sessionId}`

// Continue mode: find existing session
if (continueMode) {
  const existing = Bash(`ls -t .workflow/.csv-wave/uan-* 2>/dev/null | head -1`).trim()
  if (existing) {
    sessionId = existing.split('/').pop()
    sessionFolder = existing
  }
}

Bash(`mkdir -p ${sessionFolder}/interactive`)
```

---

### Phase 0: Pre-Wave Interactive

**Objective**: Parse topic, detect analysis dimensions, select pipeline mode, and assign perspectives.

**Execution**:

```javascript
const analyzer = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-ultra-analyze/agents/topic-analyzer.md (MUST read first)
2. Read: .workflow/project-tech.json (if exists)

---

Goal: Analyze topic and recommend pipeline configuration
Topic: ${topic}
Explicit Mode: ${explicitMode || 'auto-detect'}

### Task
1. Detect analysis dimensions from topic keywords:
   - architecture, implementation, performance, security, concept, comparison, decision
2. Select perspectives based on dimensions:
   - technical, architectural, business, domain_expert
3. Determine pipeline mode (if not explicitly set):
   - Complexity 1-3 → quick, 4-6 → standard, 7+ → deep
4. Return structured configuration
`
})

const analyzerResult = wait({ ids: [analyzer], timeout_ms: 120000 })

if (analyzerResult.timed_out) {
  send_input({ id: analyzer, message: "Please finalize and output current findings." })
  wait({ ids: [analyzer], timeout_ms: 60000 })
}

close_agent({ id: analyzer })

// Parse result: pipeline_mode, perspectives[], dimensions[], depth
Write(`${sessionFolder}/interactive/topic-analyzer-result.json`, JSON.stringify({
  task_id: "topic-analysis",
  status: "completed",
  pipeline_mode: parsedMode,
  perspectives: parsedPerspectives,
  dimensions: parsedDimensions,
  depth: parsedDepth,
  timestamp: getUtc8ISOString()
}))
```

If not AUTO_YES, present user with configuration for confirmation:

```javascript
if (!AUTO_YES) {
  const answer = AskUserQuestion({
    questions: [{
      question: `Topic: "${topic}"\nPipeline: ${pipeline_mode}\nPerspectives: ${perspectives.join(', ')}\nDimensions: ${dimensions.join(', ')}\n\nApprove?`,
      header: "Analysis Configuration",
      multiSelect: false,
      options: [
        { label: "Approve", description: `Use ${pipeline_mode} mode with ${perspectives.length} perspectives` },
        { label: "Quick", description: "1 explorer → 1 analyst → synthesizer (fast)" },
        { label: "Standard", description: "N explorers → N analysts → discussion → synthesizer" },
        { label: "Deep", description: "N explorers → N analysts → discussion loop (up to 5 rounds) → synthesizer" }
      ]
    }]
  })
}
```

**Success Criteria**:
- Refined requirements available for Phase 1 decomposition
- Interactive agents closed, results stored

---

### Phase 1: Requirement → CSV + Classification

**Objective**: Build tasks.csv from selected pipeline mode and perspectives.

**Decomposition Rules**:

| Pipeline | Tasks | Wave Structure |
|----------|-------|---------------|
| quick | EXPLORE-001 → ANALYZE-001 → SYNTH-001 | 3 waves, serial, depth=1 |
| standard | EXPLORE-001..N → ANALYZE-001..N → DISCUSS-001 → SYNTH-001 | 4 wave groups, parallel explore+analyze |
| deep | EXPLORE-001..N → ANALYZE-001..N → DISCUSS-001 (→ dynamic tasks) → SYNTH-001 | 3+ waves, SYNTH created after discussion loop |

Where N = number of selected perspectives.

**Classification Rules**:

All work tasks (exploration, analysis, discussion processing, synthesis) are `csv-wave`. The discussion feedback gate (user interaction after discussant completes) is `interactive`.

**Pipeline Task Definitions**:

#### Quick Pipeline (3 csv-wave tasks)

| Task ID | Role | Wave | Deps | Perspective | Description |
|---------|------|------|------|-------------|-------------|
| EXPLORE-001 | explorer | 1 | (none) | general | Explore codebase structure for analysis topic |
| ANALYZE-001 | analyst | 2 | EXPLORE-001 | technical | Deep analysis from technical perspective |
| SYNTH-001 | synthesizer | 3 | ANALYZE-001 | (all) | Integrate analysis into final conclusions |

#### Standard Pipeline (2N+2 tasks, parallel windows)

| Task ID | Role | Wave | Deps | Perspective | Description |
|---------|------|------|------|-------------|-------------|
| EXPLORE-001..N | explorer | 1 | (none) | per-perspective | Parallel codebase exploration, one per perspective |
| ANALYZE-001..N | analyst | 2 | EXPLORE-N | per-perspective | Parallel deep analysis, one per perspective |
| DISCUSS-001 | discussant | 3 | all ANALYZE-* | (all) | Aggregate analyses, identify themes and conflicts |
| FEEDBACK-001 | (interactive) | 4 | DISCUSS-001 | - | User feedback: done → create SYNTH, continue → more discussion |
| SYNTH-001 | synthesizer | 5 | FEEDBACK-001 | (all) | Cross-perspective integration and conclusions |

#### Deep Pipeline (2N+1 initial tasks + dynamic)

Same as Standard, but SYNTH-001 is omitted initially. Created dynamically after the discussion loop (up to 5 rounds) completes. Additional dynamic tasks:
- `DISCUSS-N` — subsequent discussion round
- `ANALYZE-fix-N` — supplementary analysis with adjusted focus
- `SYNTH-001` — created after final discussion round

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
let discussionRound = 0
const MAX_DISCUSSION_ROUNDS = pipeline_mode === 'deep' ? 5 : pipeline_mode === 'standard' ? 1 : 0

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
        status: 'skipped', error: 'Dependency failed or skipped'
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
    const waveHeader = 'id,title,description,role,perspective,dimensions,discussion_round,discussion_type,deps,context_from,exec_mode,wave,prev_context'
    const waveRows = executableCsvTasks.map(t =>
      [t.id, t.title, t.description, t.role, t.perspective, t.dimensions,
       t.discussion_round, t.discussion_type, t.deps, t.context_from, t.exec_mode, t.wave, t.prev_context]
        .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
        .join(',')
    )
    Write(`${sessionFolder}/wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

    const waveResult = spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: buildAnalysisInstruction(sessionFolder, wave),
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 600,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
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
        error: result.error || ''
      })
      if (result.status === 'failed') failedIds.add(result.id)
    }

    Bash(`rm -f "${sessionFolder}/wave-${wave}.csv"`)
  }

  // 6. Execute post-wave interactive tasks (Discussion Feedback)
  for (const task of interactiveTasks) {
    if (task.status !== 'pending') continue
    const deps = task.deps.split(';').filter(Boolean)
    if (deps.some(d => failedIds.has(d) || skippedIds.has(d))) {
      skippedIds.add(task.id)
      continue
    }

    discussionRound++

    // Discussion Feedback Gate
    if (pipeline_mode === 'quick' || discussionRound > MAX_DISCUSSION_ROUNDS) {
      // No discussion or max rounds reached — proceed to synthesis
      if (!masterCsv.find(t => t.id === 'SYNTH-001')) {
        // Create SYNTH-001 dynamically
        const lastDiscuss = masterCsv.filter(t => t.id.startsWith('DISCUSS'))
          .sort((a, b) => b.id.localeCompare(a.id))[0]
        addTaskToMasterCsv(sessionFolder, {
          id: 'SYNTH-001', title: 'Final synthesis',
          description: 'Integrate all analysis into final conclusions',
          role: 'synthesizer', perspective: '', dimensions: '',
          discussion_round: '0', discussion_type: '',
          deps: lastDiscuss ? lastDiscuss.id : '', context_from: 'all',
          exec_mode: 'csv-wave', wave: String(wave + 1),
          status: 'pending', findings: '', error: ''
        })
        maxWave = wave + 1
      }
      updateMasterCsvRow(sessionFolder, task.id, {
        status: 'completed',
        findings: `Discussion round ${discussionRound}: proceeding to synthesis`
      })
      continue
    }

    // Spawn discussion feedback agent
    const feedbackAgent = spawn_agent({
      message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-ultra-analyze/agents/discussion-feedback.md (MUST read first)
2. Read: ${sessionFolder}/discoveries.ndjson (shared discoveries)

---

Goal: Collect user feedback on discussion round ${discussionRound}
Session: ${sessionFolder}
Discussion Round: ${discussionRound}/${MAX_DISCUSSION_ROUNDS}
Pipeline Mode: ${pipeline_mode}

### Context
The discussant has completed round ${discussionRound}. Present the user with discussion results and collect feedback on next direction.
`
    })

    const feedbackResult = wait({ ids: [feedbackAgent], timeout_ms: 300000 })
    if (feedbackResult.timed_out) {
      send_input({ id: feedbackAgent, message: "Please finalize: user did not respond, default to 'Done'." })
      wait({ ids: [feedbackAgent], timeout_ms: 60000 })
    }
    close_agent({ id: feedbackAgent })

    // Parse feedback decision: "continue_deeper" | "adjust_direction" | "done"
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed",
      discussion_round: discussionRound,
      feedback: feedbackDecision,
      timestamp: getUtc8ISOString()
    }))

    // Handle feedback
    if (feedbackDecision === 'done') {
      // Create SYNTH-001 blocked by last DISCUSS task
      addTaskToMasterCsv(sessionFolder, {
        id: 'SYNTH-001', deps: task.id.replace('FEEDBACK', 'DISCUSS'),
        role: 'synthesizer', exec_mode: 'csv-wave', wave: String(wave + 1)
      })
      maxWave = wave + 1
    } else if (feedbackDecision === 'adjust_direction') {
      // Create ANALYZE-fix-N and DISCUSS-N+1
      const fixId = `ANALYZE-fix-${discussionRound}`
      const nextDiscussId = `DISCUSS-${String(discussionRound + 1).padStart(3, '0')}`
      addTaskToMasterCsv(sessionFolder, {
        id: fixId, role: 'analyst', exec_mode: 'csv-wave', wave: String(wave + 1)
      })
      addTaskToMasterCsv(sessionFolder, {
        id: nextDiscussId, role: 'discussant', deps: fixId,
        exec_mode: 'csv-wave', wave: String(wave + 2)
      })
      addTaskToMasterCsv(sessionFolder, {
        id: `FEEDBACK-${String(discussionRound + 1).padStart(3, '0')}`,
        exec_mode: 'interactive', deps: nextDiscussId, wave: String(wave + 3)
      })
      maxWave = wave + 3
    } else {
      // continue_deeper: Create DISCUSS-N+1
      const nextDiscussId = `DISCUSS-${String(discussionRound + 1).padStart(3, '0')}`
      addTaskToMasterCsv(sessionFolder, {
        id: nextDiscussId, role: 'discussant', exec_mode: 'csv-wave', wave: String(wave + 1)
      })
      addTaskToMasterCsv(sessionFolder, {
        id: `FEEDBACK-${String(discussionRound + 1).padStart(3, '0')}`,
        exec_mode: 'interactive', deps: nextDiscussId, wave: String(wave + 2)
      })
      maxWave = wave + 2
    }

    updateMasterCsvRow(sessionFolder, task.id, {
      status: 'completed',
      findings: `Discussion feedback: ${feedbackDecision}, round ${discussionRound}`
    })
  }
}
```

**Success Criteria**:
- All waves executed in order
- Both csv-wave and interactive tasks handled per wave
- Each wave's results merged into master CSV before next wave starts
- Dependent tasks skipped when predecessor failed
- discoveries.ndjson accumulated across all waves and mechanisms
- Discussion loop controlled with proper round tracking
- Dynamic tasks created correctly based on user feedback

---

### Phase 3: Post-Wave Interactive

**Objective**: Handle discussion loop completion and ensure synthesis is triggered.

After all discussion rounds are exhausted or user chooses "done":
1. Ensure SYNTH-001 exists in master CSV
2. Ensure SYNTH-001 is unblocked (blocked by last completed discussion task)
3. Execute remaining waves (synthesis)

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

const contextContent = `# Ultra Analyze Report

**Session**: ${sessionId}
**Topic**: ${topic}
**Pipeline**: ${pipeline_mode}
**Perspectives**: ${perspectives.join(', ')}
**Discussion Rounds**: ${discussionRound}
**Completed**: ${getUtc8ISOString()}

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | ${tasks.length} |
| Completed | ${completed.length} |
| Failed | ${failed.length} |
| Skipped | ${skipped.length} |
| Discussion Rounds | ${discussionRound} |

---

## Wave Execution

${waveDetails}

---

## Analysis Artifacts

- Explorations: discoveries with type "exploration" in discoveries.ndjson
- Analyses: discoveries with type "analysis" in discoveries.ndjson
- Discussion: discoveries with type "discussion" in discoveries.ndjson
- Conclusions: discoveries with type "conclusion" in discoveries.ndjson

---

## Conclusions

${synthesisFindings}
`

Write(`${sessionFolder}/context.md`, contextContent)
```

If not AUTO_YES, offer completion options:

```javascript
if (!AUTO_YES) {
  const answer = AskUserQuestion({
    questions: [{
      question: "Ultra-Analyze pipeline complete. What would you like to do?",
      header: "Completion",
      multiSelect: false,
      options: [
        { label: "Archive & Clean (Recommended)", description: "Archive session" },
        { label: "Keep Active", description: "Keep session for follow-up" },
        { label: "Export Results", description: "Export deliverables to specified location" }
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
| `exploration` | `data.perspective+data.file` | `{perspective, file, relevance, summary, patterns[]}` | Explored file/module |
| `analysis` | `data.perspective+data.insight` | `{perspective, insight, confidence, evidence, file_ref}` | Analysis insight |
| `pattern` | `data.name` | `{name, file, description, type}` | Code/architecture pattern |
| `discussion_point` | `data.topic` | `{topic, perspectives[], convergence, open_questions[]}` | Discussion point |
| `recommendation` | `data.action` | `{action, rationale, priority, confidence}` | Recommendation |
| `conclusion` | `data.point` | `{point, evidence, confidence, perspectives_supporting[]}` | Final conclusion |

**Format**: NDJSON, each line is self-contained JSON:

```jsonl
{"ts":"2026-03-08T10:00:00+08:00","worker":"EXPLORE-001","type":"exploration","data":{"perspective":"technical","file":"src/auth/index.ts","relevance":"high","summary":"Auth module entry point with OAuth and JWT exports","patterns":["module-pattern","strategy-pattern"]}}
{"ts":"2026-03-08T10:05:00+08:00","worker":"ANALYZE-001","type":"analysis","data":{"perspective":"technical","insight":"Auth module uses strategy pattern for provider switching","confidence":"high","evidence":"src/auth/strategies/*.ts","file_ref":"src/auth/index.ts:15"}}
{"ts":"2026-03-08T10:10:00+08:00","worker":"DISCUSS-001","type":"discussion_point","data":{"topic":"Authentication scalability","perspectives":["technical","architectural"],"convergence":"Both perspectives agree on stateless JWT approach","open_questions":["Token refresh strategy for long sessions"]}}
```

**Protocol Rules**:
1. Read board before own exploration → skip covered areas
2. Write discoveries immediately via `echo >>` → don't batch
3. Deduplicate — check existing entries by type + dedup key
4. Append-only — never modify or delete existing lines

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
| Discussion loop exceeds 5 rounds | Force synthesis, offer continuation |
| Explorer finds nothing | Continue with limited context, note limitation |
| CLI tool unavailable | Fallback chain: gemini → codex → direct analysis |
| User timeout in discussion | Save state, default to "done", proceed to synthesis |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when user interaction is needed
5. **Context Propagation**: prev_context built from master CSV, not from memory
6. **Discovery Board is Append-Only**: Never clear, modify, or recreate discoveries.ndjson — both mechanisms share it
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
