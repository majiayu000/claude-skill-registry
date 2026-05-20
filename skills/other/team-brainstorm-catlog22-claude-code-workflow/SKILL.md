---
name: team-brainstorm
description: Multi-agent brainstorming pipeline with Generator-Critic loop. Generates ideas, challenges assumptions, synthesizes themes, and evaluates proposals. Supports Quick, Deep, and Full pipeline modes.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"topic description\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Brainstorm

## Usage

```bash
$team-brainstorm "How should we approach microservices migration?"
$team-brainstorm -c 4 "Innovation strategies for AI-powered developer tools"
$team-brainstorm -y "Quick brainstorm on naming conventions"
$team-brainstorm --continue "brs-microservices-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Multi-agent brainstorming with Generator-Critic loop: generate ideas across multiple angles, challenge assumptions, synthesize themes, and evaluate proposals. Supports three pipeline modes (Quick/Deep/Full) with configurable depth and parallel ideation.

**Execution Model**: Hybrid — CSV wave pipeline (primary) + individual agent spawn (secondary for Generator-Critic control)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TEAM BRAINSTORM WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Pre-Wave Interactive                                           │
│     ├─ Topic clarification + complexity scoring                          │
│     ├─ Pipeline mode selection (quick/deep/full)                         │
│     └─ Output: refined requirements for decomposition                    │
│                                                                          │
│  Phase 1: Requirement → CSV + Classification                             │
│     ├─ Parse topic into brainstorm tasks per selected pipeline            │
│     ├─ Assign roles: ideator, challenger, synthesizer, evaluator         │
│     ├─ Classify tasks: csv-wave | interactive (exec_mode)                │
│     ├─ Compute dependency waves (topological sort → depth grouping)      │
│     ├─ Generate tasks.csv with wave + exec_mode columns                  │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 2: Wave Execution Engine (Extended)                               │
│     ├─ For each wave (1..N):                                             │
│     │   ├─ Execute pre-wave interactive tasks (if any)                   │
│     │   ├─ Build wave CSV (filter csv-wave tasks for this wave)          │
│     │   ├─ Inject previous findings into prev_context column             │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Execute post-wave interactive tasks (if any)                  │
│     │   ├─ Merge all results into master tasks.csv                       │
│     │   └─ Check: any failed? → skip dependents                         │
│     └─ discoveries.ndjson shared across all modes (append-only)          │
│                                                                          │
│  Phase 3: Post-Wave Interactive                                          │
│     ├─ Generator-Critic (GC) loop control                                │
│     ├─ If critique severity >= HIGH: trigger revision wave               │
│     └─ Max 2 GC rounds, then force convergence                          │
│                                                                          │
│  Phase 4: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Display summary: completed/failed/skipped per wave                │
│     └─ Offer: view results | retry failed | done                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
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
| Idea generation (single angle) | `csv-wave` |
| Parallel ideation (Full pipeline, multiple angles) | `csv-wave` (parallel in same wave) |
| Idea revision (GC loop) | `csv-wave` |
| Critique / challenge | `csv-wave` |
| Synthesis (theme extraction) | `csv-wave` |
| Evaluation (scoring / ranking) | `csv-wave` |
| GC loop control (severity check → decide revision or convergence) | `interactive` |
| Topic clarification (Phase 0) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,angle,gc_round,deps,context_from,exec_mode,wave,status,findings,gc_signal,severity_summary,error
"IDEA-001","Multi-angle idea generation","Generate 3+ ideas per angle with title, description, assumption, impact","ideator","Technical;Product;Innovation","0","","","csv-wave","1","pending","","","",""
"CHALLENGE-001","Critique generated ideas","Challenge each idea across assumption, feasibility, risk, competition dimensions","challenger","","0","IDEA-001","IDEA-001","csv-wave","2","pending","","","",""
"GC-CHECK-001","GC loop decision","Evaluate critique severity and decide: revision or convergence","gc-controller","","1","CHALLENGE-001","CHALLENGE-001","interactive","3","pending","","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description |
| `role` | Input | Worker role: ideator, challenger, synthesizer, evaluator |
| `angle` | Input | Brainstorming angle(s) for ideator tasks (semicolon-separated) |
| `gc_round` | Input | Generator-Critic round number (0 = initial, 1+ = revision) |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` → `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `gc_signal` | Output | Generator-Critic signal: `REVISION_NEEDED` or `CONVERGED` (challenger only) |
| `severity_summary` | Output | Severity count: e.g. "CRITICAL:1 HIGH:2 MEDIUM:3 LOW:1" |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| gc-controller | agents/gc-controller.md | 2.3 (wait-respond) | Evaluate critique severity, decide revision vs convergence | post-wave (after challenger wave) |
| topic-clarifier | agents/topic-clarifier.md | 2.3 (wait-respond) | Clarify topic, assess complexity, select pipeline mode | standalone (Phase 0) |

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

// Clean requirement text (remove flags)
const topic = $ARGUMENTS
  .replace(/--yes|-y|--continue|--concurrency\s+\d+|-c\s+\d+/g, '')
  .trim()

const slug = topic.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10).replace(/-/g, '')
let sessionId = `brs-${slug}-${dateStr}`
let sessionFolder = `.workflow/.csv-wave/${sessionId}`

// Continue mode: find existing session
if (continueMode) {
  const existing = Bash(`ls -t .workflow/.csv-wave/brs-* 2>/dev/null | head -1`).trim()
  if (existing) {
    sessionId = existing.split('/').pop()
    sessionFolder = existing
    // Read existing tasks.csv, find incomplete waves, resume from Phase 2
  }
}

Bash(`mkdir -p ${sessionFolder}/interactive`)
```

---

### Phase 0: Pre-Wave Interactive

**Objective**: Clarify topic, assess complexity, and select pipeline mode.

**Execution**:

```javascript
const clarifier = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~  or <project>/.codex/skills/team-brainstorm/agents/topic-clarifier.md (MUST read first)
2. Read: .workflow/project-tech.json (if exists)

---

Goal: Clarify brainstorming topic and select pipeline mode
Topic: ${topic}

### Task
1. Assess topic complexity using signal detection:
   - Strategic/systemic keywords (+3): strategy, architecture, system, framework, paradigm
   - Multi-dimensional keywords (+2): multiple, compare, tradeoff, versus, alternative
   - Innovation-focused keywords (+2): innovative, creative, novel, breakthrough
   - Simple/basic keywords (-2): simple, quick, straightforward, basic
2. Score >= 4 → full, 2-3 → deep, 0-1 → quick
3. Suggest divergence angles (e.g., Technical, Product, Innovation, Risk)
4. Return structured result
`
})

const clarifierResult = wait({ ids: [clarifier], timeout_ms: 120000 })

if (clarifierResult.timed_out) {
  send_input({ id: clarifier, message: "Please finalize and output current findings." })
  const retry = wait({ ids: [clarifier], timeout_ms: 60000 })
}

// Parse result for pipeline_mode, angles
close_agent({ id: clarifier })

// Store result
Write(`${sessionFolder}/interactive/topic-clarifier-result.json`, JSON.stringify({
  task_id: "topic-clarification",
  status: "completed",
  pipeline_mode: parsedMode, // "quick" | "deep" | "full"
  angles: parsedAngles,      // ["Technical", "Product", "Innovation", "Risk"]
  complexity_score: parsedScore,
  timestamp: getUtc8ISOString()
}))
```

If not AUTO_YES, present user with pipeline mode selection for confirmation:

```javascript
if (!AUTO_YES) {
  const answer = AskUserQuestion({
    questions: [{
      question: `Topic: "${topic}"\nRecommended pipeline: ${pipeline_mode} (complexity: ${complexity_score})\nAngles: ${angles.join(', ')}\n\nApprove?`,
      header: "Pipeline Selection",
      multiSelect: false,
      options: [
        { label: "Approve", description: `Use ${pipeline_mode} pipeline` },
        { label: "Quick", description: "3 tasks: generate → challenge → synthesize" },
        { label: "Deep", description: "6 tasks: generate → challenge → revise → re-challenge → synthesize → evaluate" },
        { label: "Full", description: "7 tasks: 3x parallel generation → challenge → revise → synthesize → evaluate" }
      ]
    }]
  })
  // Update pipeline_mode based on user choice
}
```

**Success Criteria**:
- Refined requirements available for Phase 1 decomposition
- Interactive agents closed, results stored

---

### Phase 1: Requirement → CSV + Classification

**Objective**: Build tasks.csv from selected pipeline mode with proper wave assignments.

**Decomposition Rules**:

| Pipeline | Tasks | Wave Structure |
|----------|-------|---------------|
| quick | IDEA-001 → CHALLENGE-001 → SYNTH-001 | 3 waves, serial |
| deep | IDEA-001 → CHALLENGE-001 → IDEA-002 → CHALLENGE-002 → SYNTH-001 → EVAL-001 | 6 waves, serial with GC loop |
| full | IDEA-001,002,003 (parallel) → CHALLENGE-001 → IDEA-004 → SYNTH-001 → EVAL-001 | 5 waves, fan-out + GC |

**Classification Rules**:

All brainstorm work tasks (ideation, challenging, synthesis, evaluation) are `csv-wave`. The GC loop controller between challenger and next ideation revision is `interactive` (post-wave, spawned by orchestrator to decide the GC outcome).

**Wave Computation**: Kahn's BFS topological sort with depth tracking (csv-wave tasks only).

**User Validation**: Display task breakdown with wave + exec_mode assignment (skip if AUTO_YES).

**Pipeline Task Definitions**:

#### Quick Pipeline (3 csv-wave tasks)

| Task ID | Role | Wave | Deps | Description |
|---------|------|------|------|-------------|
| IDEA-001 | ideator | 1 | (none) | Generate multi-angle ideas: 3+ ideas per angle with title, description, assumption, impact |
| CHALLENGE-001 | challenger | 2 | IDEA-001 | Challenge each idea across 4 dimensions (assumption, feasibility, risk, competition). Assign severity per idea. Output GC signal |
| SYNTH-001 | synthesizer | 3 | CHALLENGE-001 | Synthesize ideas and critiques into 1-3 integrated proposals with feasibility and innovation scores |

#### Deep Pipeline (6 csv-wave tasks + 1 interactive GC check)

Same as Quick plus:

| Task ID | Role | Wave | Deps | Description |
|---------|------|------|------|-------------|
| IDEA-002 | ideator | 4 | CHALLENGE-001 | Revise ideas based on critique feedback (GC Round 1). Address HIGH/CRITICAL challenges |
| CHALLENGE-002 | challenger | 5 | IDEA-002 | Validate revised ideas (GC Round 2). Re-evaluate previously challenged ideas |
| SYNTH-001 | synthesizer | 6 | CHALLENGE-002 | Synthesize all ideas and critiques |
| EVAL-001 | evaluator | 7 | SYNTH-001 | Score and rank proposals: Feasibility 30%, Innovation 25%, Impact 25%, Cost 20% |

GC-CHECK-001 (interactive) runs post-wave after CHALLENGE-001 to decide whether to proceed with revision or skip to synthesis.

#### Full Pipeline (7 csv-wave tasks + GC control)

| Task ID | Role | Wave | Deps | Description |
|---------|------|------|------|-------------|
| IDEA-001 | ideator | 1 | (none) | Generate ideas from angle 1 |
| IDEA-002 | ideator | 1 | (none) | Generate ideas from angle 2 |
| IDEA-003 | ideator | 1 | (none) | Generate ideas from angle 3 |
| CHALLENGE-001 | challenger | 2 | IDEA-001;IDEA-002;IDEA-003 | Critique all generated ideas |
| IDEA-004 | ideator | 3 | CHALLENGE-001 | Revise ideas based on critique |
| SYNTH-001 | synthesizer | 4 | IDEA-004 | Synthesize all ideas and critiques |
| EVAL-001 | evaluator | 5 | SYNTH-001 | Score and rank proposals |

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
const MAX_GC_ROUNDS = 2
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
    const waveHeader = 'id,title,description,role,angle,gc_round,deps,context_from,exec_mode,wave,prev_context'
    const waveRows = executableCsvTasks.map(t =>
      [t.id, t.title, t.description, t.role, t.angle, t.gc_round, t.deps, t.context_from, t.exec_mode, t.wave, t.prev_context]
        .map(cell => `"${String(cell).replace(/"/g, '""')}"`)
        .join(',')
    )
    Write(`${sessionFolder}/wave-${wave}.csv`, [waveHeader, ...waveRows].join('\n'))

    const waveResult = spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: buildBrainstormInstruction(sessionFolder, wave),
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 600,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          gc_signal: { type: "string" },
          severity_summary: { type: "string" },
          error: { type: "string" }
        },
        required: ["id", "status", "findings"]
      }
    })
    // Blocks until wave completes

    // Merge results into master CSV
    const waveResults = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const result of waveResults) {
      updateMasterCsvRow(sessionFolder, result.id, {
        status: result.status,
        findings: result.findings || '',
        gc_signal: result.gc_signal || '',
        severity_summary: result.severity_summary || '',
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
1. **Read role definition**: ~  or <project>/.codex/skills/team-brainstorm/agents/gc-controller.md (MUST read first)
2. Read: ${sessionFolder}/discoveries.ndjson (shared discoveries)

---

Goal: Evaluate critique severity and decide revision vs convergence
Session: ${sessionFolder}
GC Round: ${gcRound}
Max GC Rounds: ${MAX_GC_ROUNDS}

### Context
Read the latest critique file and determine the GC signal.
If REVISION_NEEDED and gcRound < maxRounds: output "REVISION"
If CONVERGED or gcRound >= maxRounds: output "CONVERGE"
`
    })

    const gcResult = wait({ ids: [gcAgent], timeout_ms: 120000 })
    if (gcResult.timed_out) {
      send_input({ id: gcAgent, message: "Please finalize your decision now." })
      wait({ ids: [gcAgent], timeout_ms: 60000 })
    }
    close_agent({ id: gcAgent })

    // Parse GC decision and potentially create/skip revision tasks
    Write(`${sessionFolder}/interactive/${task.id}-result.json`, JSON.stringify({
      task_id: task.id, status: "completed",
      gc_decision: gcDecision, gc_round: gcRound,
      timestamp: getUtc8ISOString()
    }))

    if (gcDecision === "CONVERGE") {
      // Skip remaining GC tasks, mark revision tasks as skipped
      // Unblock SYNTH directly
    } else {
      gcRound++
      // Let the revision wave proceed naturally
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
- GC loop controlled with max 2 rounds

---

### Phase 3: Post-Wave Interactive

**Objective**: Handle any final GC loop convergence and prepare for synthesis.

If the pipeline used GC loops and the final GC decision was CONVERGE or max rounds reached, ensure SYNTH-001 is unblocked and all remaining GC-related tasks are properly marked.

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

const contextContent = `# Team Brainstorm Report

**Session**: ${sessionId}
**Topic**: ${topic}
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

## Wave Execution

${waveDetails}

---

## Task Details

${taskDetails}

---

## Brainstorm Artifacts

- Ideas: discoveries with type "idea" in discoveries.ndjson
- Critiques: discoveries with type "critique" in discoveries.ndjson
- Synthesis: discoveries with type "synthesis" in discoveries.ndjson
- Evaluation: discoveries with type "evaluation" in discoveries.ndjson
`

Write(`${sessionFolder}/context.md`, contextContent)
```

If not AUTO_YES and there are failed tasks, offer retry or view report.

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
| `idea` | `data.title` | `{title, angle, description, assumption, impact}` | Generated idea |
| `critique` | `data.idea_title` | `{idea_title, dimension, severity, challenge, rationale}` | Critique of an idea |
| `theme` | `data.name` | `{name, strength, supporting_ideas[]}` | Extracted theme from synthesis |
| `proposal` | `data.title` | `{title, source_ideas[], feasibility, innovation, description}` | Integrated proposal |
| `evaluation` | `data.proposal_title` | `{proposal_title, weighted_score, rank, recommendation}` | Proposal evaluation |
| `gc_decision` | `data.round` | `{round, signal, severity_counts}` | GC loop decision |

**Format**: NDJSON, each line is self-contained JSON:

```jsonl
{"ts":"2026-03-08T10:00:00+08:00","worker":"IDEA-001","type":"idea","data":{"title":"API Gateway Pattern","angle":"Technical","description":"Centralized API gateway for microservice routing","assumption":"Services need unified entry point","impact":"Simplifies client integration"}}
{"ts":"2026-03-08T10:05:00+08:00","worker":"CHALLENGE-001","type":"critique","data":{"idea_title":"API Gateway Pattern","dimension":"feasibility","severity":"MEDIUM","challenge":"Single point of failure","rationale":"Requires high availability design"}}
```

**Protocol Rules**:
1. Read board before own work → leverage existing context
2. Write discoveries immediately via `echo >>` → don't batch
3. Deduplicate — check existing entries by type + dedup key
4. Append-only — never modify or delete existing lines

---

## Consensus Severity Routing

When the challenger returns critique results with severity-graded verdicts:

| Severity | Action |
|----------|--------|
| HIGH | Trigger revision round (GC loop), max 2 rounds total |
| MEDIUM | Log warning, continue pipeline |
| LOW | Treat as consensus reached |

**Constraints**: Max 2 GC rounds (revision cycles). If still HIGH after 2 rounds, force convergence to synthesizer.

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
| GC loop exceeds 2 rounds | Force convergence to synthesizer |
| No ideas generated | Report failure, suggest refining topic |
| Continue mode: no session found | List available sessions, prompt user to select |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 0/1
2. **Wave Order is Sacred**: Never execute wave N before wave N-1 completes and results are merged
3. **CSV is Source of Truth**: Master tasks.csv holds all state (both csv-wave and interactive)
4. **CSV First**: Default to csv-wave for tasks; only use interactive when interaction pattern requires it
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
