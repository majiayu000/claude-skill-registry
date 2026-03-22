---
name: team-designer
description: Meta-skill for generating team skills. Analyzes requirements, scaffolds directory structure, generates role definitions and specs, validates completeness. Produces complete Codex team skill packages with SKILL.md orchestrator, CSV schemas, agent instructions, and interactive agents.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"skill description with roles and domain\""
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Team Skill Designer

## Usage

```bash
$team-designer "Design a code review team with analyst, reviewer, security-expert roles"
$team-designer -c 4 "Create a documentation team with researcher, writer, editor"
$team-designer -y "Generate a test automation team with planner, executor, tester"
$team-designer --continue "td-code-review-20260308"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` (master state) + `results.csv` (final) + `discoveries.ndjson` (shared exploration) + `context.md` (human-readable report)

---

## Overview

Meta-skill for generating complete team skill packages. Takes a skill description with roles and domain, then: analyzes requirements -> scaffolds directory structure -> generates all role files, specs, templates -> validates the package. The generated skill follows the Codex hybrid team architecture (CSV wave primary + interactive secondary).

**Execution Model**: Hybrid -- CSV wave pipeline (primary) + individual agent spawn (secondary)

```
+-------------------------------------------------------------------+
|              TEAM SKILL DESIGNER WORKFLOW                           |
+-------------------------------------------------------------------+
|                                                                     |
|  Phase 0: Pre-Wave Interactive (Requirement Clarification)          |
|     +- Parse user skill description                                 |
|     +- Detect input source (reference, structured, natural)         |
|     +- Gather core identity (skill name, prefix, domain)            |
|     +- Output: refined requirements for decomposition               |
|                                                                     |
|  Phase 1: Requirement -> CSV + Classification                       |
|     +- Discover roles from domain keywords                          |
|     +- Define pipelines from role combinations                      |
|     +- Determine commands distribution (inline vs commands/)        |
|     +- Build teamConfig data structure                              |
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
|     +- discoveries.ndjson shared across all modes (append-only)     |
|                                                                     |
|  Phase 3: Post-Wave Interactive (Validation)                        |
|     +- Structural validation (files exist, sections present)        |
|     +- Reference integrity (role registry matches files)            |
|     +- Pipeline consistency (no circular deps, roles exist)         |
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
| Single-pass file generation (role.md, spec.md) | `csv-wave` |
| Directory scaffold creation | `csv-wave` |
| SKILL.md generation (complex, multi-section) | `csv-wave` |
| Coordinator role generation (multi-file) | `csv-wave` |
| Worker role generation (single file) | `csv-wave` |
| Pipeline spec generation | `csv-wave` |
| Template generation | `csv-wave` |
| User requirement clarification | `interactive` |
| Validation requiring user approval | `interactive` |
| Error recovery (auto-fix vs regenerate choice) | `interactive` |

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,role,file_target,gen_type,deps,context_from,exec_mode,wave,status,findings,files_produced,error
"SCAFFOLD-001","Create directory structure","Create the complete directory structure for the team skill including roles/, specs/, templates/ subdirectories","scaffolder","skill-dir","directory","","","csv-wave","1","pending","","",""
"SPEC-001","Generate pipelines spec","Generate specs/pipelines.md with pipeline definitions, task registry, conditional routing","spec-writer","specs/pipelines.md","spec","SCAFFOLD-001","","csv-wave","2","pending","","",""
"ROLE-001","Generate coordinator role","Generate roles/coordinator/role.md with entry router, command execution protocol, phase logic","role-writer","roles/coordinator/","role-bundle","SCAFFOLD-001;SPEC-001","SPEC-001","csv-wave","2","pending","","",""
"ROLE-002","Generate analyst worker role","Generate roles/analyst/role.md with domain-specific Phase 2-4 logic","role-writer","roles/analyst/role.md","role-inline","SCAFFOLD-001;SPEC-001","SPEC-001","csv-wave","2","pending","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Unique task identifier (string) |
| `title` | Input | Short task title |
| `description` | Input | Detailed task description with generation instructions |
| `role` | Input | Generator role: `scaffolder`, `spec-writer`, `role-writer`, `router-writer`, `validator` |
| `file_target` | Input | Target file or directory path relative to skill root |
| `gen_type` | Input | Generation type: `directory`, `router`, `role-bundle`, `role-inline`, `spec`, `template` |
| `deps` | Input | Semicolon-separated dependency task IDs |
| `context_from` | Input | Semicolon-separated task IDs whose findings this task needs |
| `exec_mode` | Input | `csv-wave` or `interactive` |
| `wave` | Computed | Wave number (computed by topological sort, 1-based) |
| `status` | Output | `pending` -> `completed` / `failed` / `skipped` |
| `findings` | Output | Key discoveries or implementation notes (max 500 chars) |
| `files_produced` | Output | Semicolon-separated paths of produced files |
| `error` | Output | Error message if failed (empty if success) |

### Per-Wave CSV (Temporary)

Each wave generates a temporary `wave-{N}.csv` with extra `prev_context` column (csv-wave tasks only).

---

## Agent Registry (Interactive Agents)

| Agent | Role File | Pattern | Responsibility | Position |
|-------|-----------|---------|----------------|----------|
| Requirement Clarifier | agents/requirement-clarifier.md | 2.3 (send_input cycle) | Gather and refine skill requirements interactively | standalone (Phase 0) |
| Validation Reporter | agents/validation-reporter.md | 2.3 (send_input cycle) | Validate generated skill package and report results | standalone (Phase 3) |

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
| `teamConfig.json` | Phase 0/1 output: skill config, roles, pipelines | Created in Phase 1 |
| `interactive/{id}-result.json` | Results from interactive tasks | Created per interactive task |

---

## Session Structure

```
.workflow/.csv-wave/{session-id}/
+-- tasks.csv                  # Master state (all tasks, both modes)
+-- results.csv                # Final results export
+-- discoveries.ndjson         # Shared discovery board (all agents)
+-- context.md                 # Human-readable report
+-- teamConfig.json            # Skill configuration from Phase 1
+-- wave-{N}.csv               # Temporary per-wave input (csv-wave only)
+-- artifacts/                 # Generated skill files (intermediate)
+-- interactive/               # Interactive task artifacts
|   +-- {id}-result.json
+-- validation/                # Validation reports
    +-- structural.json
    +-- references.json
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
const sessionId = `td-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/artifacts ${sessionFolder}/interactive ${sessionFolder}/validation`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, '')
```

---

### Phase 0: Pre-Wave Interactive (Requirement Clarification)

**Objective**: Parse user skill description, clarify ambiguities, build teamConfig.

**Workflow**:

1. **Parse user skill description** from $ARGUMENTS

2. **Detect input source**:

| Source Type | Detection | Action |
|-------------|-----------|--------|
| Reference | Contains "based on", "like", or existing skill path | Read referenced skill, extract structure |
| Structured | Contains ROLES:, PIPELINES:, or DOMAIN: | Parse structured input directly |
| Natural language | Default | Analyze keywords, discover roles |

3. **Check for existing sessions** (continue mode):
   - Scan `.workflow/.csv-wave/td-*/tasks.csv` for sessions with pending tasks
   - If `--continue`: resume the specified or most recent session, skip to Phase 2

4. **Gather core identity** (skip if AUTO_YES or already clear):

Read `agents/requirement-clarifier.md`, then:

```javascript
const clarifier = spawn_agent({
  message: `## TASK ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read: agents/requirement-clarifier.md
2. Read: ${sessionFolder}/discoveries.ndjson (if exists)

---

Goal: Gather team skill requirements from the user
Input: "${requirement}"
Session: ${sessionFolder}

Determine: skill name (kebab-case), session prefix (3-4 chars), domain description, roles, pipelines, commands distribution.`
})
const clarifyResult = wait({ ids: [clarifier], timeout_ms: 600000 })
if (clarifyResult.timed_out) {
  send_input({ id: clarifier, message: "Please finalize requirements with current information." })
  wait({ ids: [clarifier], timeout_ms: 120000 })
}
Write(`${sessionFolder}/interactive/clarify-result.json`, JSON.stringify({
  task_id: "CLARIFY-001", status: "completed", findings: parseFindings(clarifyResult),
  timestamp: getUtc8ISOString()
}))
close_agent({ id: clarifier })
```

5. **Build teamConfig** from gathered requirements:

```javascript
const teamConfig = {
  skillName: "<kebab-case-name>",
  sessionPrefix: "<3-4 char prefix>",
  domain: "<domain description>",
  title: "<Human Readable Title>",
  roles: [
    { name: "coordinator", prefix: "—", inner_loop: false, hasCommands: true, commands: ["analyze", "dispatch", "monitor"], path: "roles/coordinator/role.md" },
    // ... discovered worker roles
  ],
  pipelines: [{ name: "<pipeline-name>", tasks: [/* task definitions */] }],
  specs: ["pipelines"],
  templates: [],
  conditionalRouting: false,
  targetDir: `.codex/skills/<skill-name>`
}

Write(`${sessionFolder}/teamConfig.json`, JSON.stringify(teamConfig, null, 2))
```

6. **Decompose into tasks** -- generate tasks.csv from teamConfig:

| Task Pattern | gen_type | Wave | Description |
|--------------|----------|------|-------------|
| Directory scaffold | `directory` | 1 | Create skill directory structure |
| SKILL.md router | `router` | 2 | Generate main SKILL.md orchestrator |
| Pipeline spec | `spec` | 2 | Generate specs/pipelines.md |
| Domain specs | `spec` | 2 | Generate additional specs files |
| Coordinator role | `role-bundle` | 3 | Generate coordinator role.md + commands/ |
| Worker roles (each) | `role-inline` or `role-bundle` | 3 | Generate each worker role.md |
| Templates (each) | `template` | 3 | Generate template files |
| Validation | `validation` | 4 | Validate the complete package |

**Success Criteria**:
- teamConfig.json written with complete configuration
- Refined requirements available for Phase 1 decomposition
- Interactive agents closed, results stored

---

### Phase 1: Requirement -> CSV + Classification

**Objective**: Generate tasks.csv from teamConfig with dependency-ordered waves.

**Decomposition Rules**:

1. **Role Discovery** -- scan domain description for keywords:

| Signal | Keywords | Role Name | Prefix |
|--------|----------|-----------|--------|
| Analysis | analyze, research, investigate, explore | analyst | RESEARCH |
| Planning | plan, design, architect, decompose | planner | PLAN |
| Writing | write, document, draft, spec, report | writer | DRAFT |
| Implementation | implement, build, code, develop | executor | IMPL |
| Testing | test, verify, validate, qa | tester | TEST |
| Review | review, audit, check, inspect | reviewer | REVIEW |
| Security | security, vulnerability, penetration | security-expert | SECURITY |

2. **Commands Distribution** -- determine inline vs commands/:

| Condition | Commands Structure |
|-----------|-------------------|
| 1 distinct action for role | Inline in role.md |
| 2+ distinct actions | commands/ folder |
| Coordinator (always) | commands/: analyze, dispatch, monitor |

3. **Pipeline Construction** -- build from role ordering:

| Role Combination | Pipeline Type |
|------------------|---------------|
| analyst + writer + executor | full-lifecycle |
| analyst + writer (no executor) | spec-only |
| planner + executor (no analyst) | impl-only |
| Other | custom |

**Classification Rules**:

| Task Property | exec_mode |
|---------------|-----------|
| Directory creation | `csv-wave` |
| Single file generation (role.md, spec.md) | `csv-wave` |
| Multi-file bundle generation (coordinator) | `csv-wave` |
| SKILL.md router generation | `csv-wave` |
| User requirement clarification | `interactive` |
| Validation with error recovery | `interactive` |

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

  // 3. Execute pre-wave interactive tasks
  const preWaveInteractive = interactiveTasks.filter(t => t.status === 'pending')
  for (const task of preWaveInteractive) {
    // Use appropriate interactive agent
    const agentFile = task.gen_type === 'validation'
      ? 'agents/validation-reporter.md'
      : 'agents/requirement-clarifier.md'
    Read(agentFile)

    const agent = spawn_agent({
      message: `## TASK ASSIGNMENT\n\n### MANDATORY FIRST STEPS\n1. Read: ${agentFile}\n2. Read: ${sessionFolder}/discoveries.ndjson\n\nGoal: ${task.description}\nScope: ${task.title}\nSession: ${sessionFolder}\nteamConfig: ${sessionFolder}/teamConfig.json\n\n### Previous Context\n${buildPrevContext(task, tasks)}`
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

    // 6. Execute wave via spawn_agents_on_csv
    spawn_agents_on_csv({
      csv_path: `${sessionFolder}/wave-${wave}.csv`,
      id_column: "id",
      instruction: Read(`instructions/agent-instruction.md`)
        .replace(/<session-folder>/g, sessionFolder),
      max_concurrency: maxConcurrency,
      max_runtime_seconds: 900,
      output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
      output_schema: {
        type: "object",
        properties: {
          id: { type: "string" },
          status: { type: "string", enum: ["completed", "failed"] },
          findings: { type: "string" },
          files_produced: { type: "string" },
          error: { type: "string" }
        }
      }
    })

    // 7. Merge results into master CSV
    const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
    for (const r of results) {
      const t = tasks.find(t => t.id === r.id)
      if (t) Object.assign(t, r)
    }
  }

  // 8. Update master CSV
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))

  // 9. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)

  // 10. Display wave summary
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

### Phase 3: Post-Wave Interactive (Validation)

**Objective**: Validate the generated team skill package and present results.

Read `agents/validation-reporter.md`, then:

```javascript
const validator = spawn_agent({
  message: `## TASK ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read: agents/validation-reporter.md
2. Read: ${sessionFolder}/discoveries.ndjson
3. Read: ${sessionFolder}/teamConfig.json

---

Goal: Validate the generated team skill package at ${teamConfig.targetDir}
Session: ${sessionFolder}

### Validation Checks
1. Structural: All files exist per teamConfig
2. SKILL.md: Required sections present, role registry correct
3. Role frontmatter: YAML frontmatter valid for each worker role
4. Pipeline consistency: No circular deps, roles referenced exist
5. Commands distribution: commands/ matches hasCommands flag

### Previous Context
${buildCompletePrevContext(tasks)}`
})
const validResult = wait({ ids: [validator], timeout_ms: 600000 })
if (validResult.timed_out) {
  send_input({ id: validator, message: "Please finalize validation with current findings." })
  wait({ ids: [validator], timeout_ms: 120000 })
}
Write(`${sessionFolder}/interactive/validation-result.json`, JSON.stringify({
  task_id: "VALIDATE-001", status: "completed", findings: parseFindings(validResult),
  timestamp: getUtc8ISOString()
}))
close_agent({ id: validator })
```

**Success Criteria**:
- Post-wave interactive processing complete
- Validation report generated
- Interactive agents closed, results stored

---

### Phase 4: Results Aggregation

**Objective**: Generate final results and human-readable report.

```javascript
// 1. Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// 2. Generate context.md
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
let contextMd = `# Team Skill Designer Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Skill**: ${teamConfig.skillName}\n`
contextMd += `**Target**: ${teamConfig.targetDir}\n\n`

contextMd += `## Summary\n`
contextMd += `| Status | Count |\n|--------|-------|\n`
contextMd += `| Completed | ${tasks.filter(t => t.status === 'completed').length} |\n`
contextMd += `| Failed | ${tasks.filter(t => t.status === 'failed').length} |\n`
contextMd += `| Skipped | ${tasks.filter(t => t.status === 'skipped').length} |\n\n`

contextMd += `## Generated Skill Structure\n\n`
contextMd += `\`\`\`\n${teamConfig.targetDir}/\n`
contextMd += `+-- SKILL.md\n+-- schemas/\n|   +-- tasks-schema.md\n+-- instructions/\n|   +-- agent-instruction.md\n`
// ... roles, specs, templates
contextMd += `\`\`\`\n\n`

contextMd += `## Validation\n`
// ... validation results

Write(`${sessionFolder}/context.md`, contextMd)

// 3. Display final summary
console.log(`\nTeam Skill Designer Complete`)
console.log(`Generated skill: ${teamConfig.targetDir}`)
console.log(`Results: ${sessionFolder}/results.csv`)
console.log(`Report: ${sessionFolder}/context.md`)
console.log(`\nUsage: $${teamConfig.skillName} "task description"`)
```

**Success Criteria**:
- results.csv exported (all tasks, both modes)
- context.md generated
- All interactive agents closed
- Summary displayed to user

---

## Shared Discovery Board Protocol

All agents (csv-wave and interactive) share a single `discoveries.ndjson` file for cross-task knowledge exchange.

**Format**: One JSON object per line (NDJSON):

```jsonl
{"ts":"2026-03-08T10:00:00Z","worker":"SCAFFOLD-001","type":"dir_created","data":{"path":"~  or <project>/.codex/skills/team-code-review/","description":"Created skill directory structure"}}
{"ts":"2026-03-08T10:05:00Z","worker":"ROLE-001","type":"file_generated","data":{"file":"roles/coordinator/role.md","gen_type":"role-bundle","sections":["entry-router","commands"]}}
{"ts":"2026-03-08T10:10:00Z","worker":"SPEC-001","type":"pattern_found","data":{"pattern_name":"full-lifecycle","description":"Pipeline with analyst -> writer -> executor -> tester"}}
```

**Discovery Types**:

| Type | Data Schema | Description |
|------|-------------|-------------|
| `dir_created` | `{path, description}` | Directory structure created |
| `file_generated` | `{file, gen_type, sections}` | File generated with specific sections |
| `pattern_found` | `{pattern_name, description}` | Design pattern identified in golden sample |
| `config_decision` | `{decision, rationale, impact}` | Configuration decision made |
| `validation_result` | `{check, passed, message}` | Validation check result |
| `reference_found` | `{source, target, type}` | Cross-reference between generated files |

**Protocol**:
1. Agents MUST read discoveries.ndjson at start of execution
2. Agents MUST append relevant discoveries during execution
3. Agents MUST NOT modify or delete existing entries
4. Deduplication by `{type, data.file, data.path}` key

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
| Invalid role name | Must be lowercase alphanumeric with hyphens, max 20 chars |
| Directory conflict | Warn if skill directory already exists, ask user to confirm overwrite |
| Golden sample not found | Fall back to embedded templates in instructions |
| Validation FAIL | Offer auto-fix, regenerate, or accept as-is |
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
8. **Golden Sample Fidelity**: Generated files must match existing team skill patterns
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
