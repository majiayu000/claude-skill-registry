---
name: workflow-lite-plan
description: Lightweight planning skill - task analysis, multi-angle exploration, clarification, adaptive planning, confirmation, and execution handoff
allowed-tools: Skill, Agent, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
---

<purpose>
Planning pipeline: explore → clarify → plan → confirm → handoff to lite-execute.
Produces exploration results, a structured plan (plan.json), independent task files (.task/TASK-*.json), and hands off to lite-execute for implementation.
</purpose>

<process>

## 1. Context Isolation

> **CRITICAL**: If invoked from analyze-with-file (via "执行任务"), the analyze-with-file session is **COMPLETE** and all its phase instructions are FINISHED and MUST NOT be referenced. Only follow LP-Phase 1-5 defined in THIS document. Phase numbers are INDEPENDENT of any prior workflow.

## 2. Input

```
<task-description>         Task description or path to .md file (required)
```

| Flag | Description |
|------|-------------|
| `-y`, `--yes` | Auto mode: Skip clarification, auto-confirm plan, auto-select execution, skip review (entire plan+execute workflow) |
| `--force-explore` | Force code exploration even when task has prior analysis |

**Note**: Workflow preferences (`autoYes`, `forceExplore`) must be initialized at skill start. If not provided by caller, skill will prompt user for workflow mode selection.

## 3. Output Artifacts

| Artifact | Description |
|----------|-------------|
| `exploration-{angle}.json` | Per-angle exploration results (1-4 files based on complexity) |
| `explorations-manifest.json` | Index of all exploration files |
| `planning-context.md` | Evidence paths + synthesized understanding |
| `plan.json` | Plan overview with task_ids[] (plan-overview-base-schema.json) |
| `.task/TASK-*.json` | Independent task files (one per task) |

**Output Directory**: `.workflow/.lite-plan/{task-slug}-{YYYY-MM-DD}/`

**Agent Usage**: Low → Direct Claude planning (no agent) | Medium/High → `cli-lite-planning-agent`

**Schema Reference**: `~/.ccw/workflows/cli-templates/schemas/plan-overview-base-schema.json`

## 4. Phase Summary

| Phase | Core Action | Output |
|-------|-------------|--------|
| LP-0 | Initialize workflowPreferences | autoYes, forceExplore |
| LP-1 | Complexity assessment → parallel cli-explore-agents (1-4) | exploration-*.json + manifest |
| LP-2 | Aggregate + dedup clarification_needs → multi-round AskUserQuestion | clarificationContext (in-memory) |
| LP-3 | Low: Direct Claude planning / Medium+High: cli-lite-planning-agent | plan.json + .task/TASK-*.json |
| LP-4 | Display plan → AskUserQuestion (Confirm + Execution + Review) | userSelection |
| LP-5 | Build executionContext → Skill("lite-execute") | handoff (Mode 1) |

## 5. LP-Phase 0: Workflow Preferences Initialization

```javascript
if (typeof workflowPreferences === 'undefined' || workflowPreferences === null) {
  workflowPreferences = {
    autoYes: false,      // false: show LP-Phase 2/4 prompts | true (-y): skip all prompts
    forceExplore: false
  }
}
```

## 6. LP-Phase 1: Intelligent Multi-Angle Exploration

**Session Setup** (MANDATORY):
```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()
const taskSlug = task_description.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10)
const sessionId = `${taskSlug}-${dateStr}`
const sessionFolder = `.workflow/.lite-plan/${sessionId}`
bash(`mkdir -p ${sessionFolder} && test -d ${sessionFolder} && echo "SUCCESS: ${sessionFolder}" || echo "FAILED: ${sessionFolder}"`)
```

**TodoWrite Template** (initial state — subsequent phases update status progressively):
```javascript
// Pattern: set phases[0..N-1].status="completed", phases[N].status="in_progress"
// Only full block shown here; subsequent updates follow same structure with status changes
TodoWrite({ todos: [
  { content: `LP-Phase 1: Exploration [${complexity}] ${selectedAngles.length} angles`, status: "in_progress", activeForm: `Exploring: ${selectedAngles.join(', ')}` },
  { content: "LP-Phase 2: Clarification", status: "pending" },
  { content: `LP-Phase 3: Planning [${planningStrategy}]`, status: "pending" },
  { content: "LP-Phase 4: Confirmation", status: "pending" },
  { content: "LP-Phase 5: Execution", status: "pending" }
]})
```

**Exploration Decision Logic**:
```javascript
const hasPriorAnalysis = /##\s*Prior Analysis/i.test(task_description)
const hasHandoffSpec = /```json:handoff-spec/i.test(task_description)

// Parse structured handoff from analyze-with-file (if present)
let handoffSpec = null
if (hasHandoffSpec) {
  const specMatch = task_description.match(/```json:handoff-spec\s*\n([\s\S]*?)\n```/)
  if (specMatch) {
    handoffSpec = JSON.parse(specMatch[1])
    // handoffSpec contains: { source, session_id, session_folder, summary,
    //   implementation_scope[], code_anchors[], key_files[], key_findings[], decision_context[] }
    // implementation_scope[]: { objective, rationale, priority, target_files[], acceptance_criteria[], change_summary }
    console.log(`[Handoff] From ${handoffSpec.source} session ${handoffSpec.session_id}`)
    console.log(`[Handoff] ${handoffSpec.implementation_scope.length} scoped items with acceptance criteria`)
  }
}

needsExploration = workflowPreferences.forceExplore ? true
  : (hasPriorAnalysis || hasHandoffSpec) ? false
  : (task.mentions_specific_files ||
     task.requires_codebase_context ||
     task.needs_architecture_understanding ||
     task.modifies_existing_code)

if (!needsExploration) {
  // manifest absent; LP-Phase 3 loads with safe fallback
  // If handoffSpec exists, it provides pre-scoped implementation context
  proceed_to_next_phase()
}
```

**Context Protection**: File reading >=50k chars → force `needsExploration=true` (delegate to cli-explore-agent)

**Complexity Assessment**:
```javascript
const complexity = analyzeTaskComplexity(task_description)
// 'Low': single file, single function, zero cross-module impact (fix typo, rename var, adjust constant)
// 'Medium': multiple files OR integration point OR new pattern (add endpoint, implement feature, refactor)
// 'High': cross-module, architectural, systemic (new subsystem, migration, security overhaul)
// Default bias: uncertain between Low/Medium → choose Medium

const ANGLE_PRESETS = {
  architecture: ['architecture', 'dependencies', 'modularity', 'integration-points'],
  security: ['security', 'auth-patterns', 'dataflow', 'validation'],
  performance: ['performance', 'bottlenecks', 'caching', 'data-access'],
  bugfix: ['error-handling', 'dataflow', 'state-management', 'edge-cases'],
  feature: ['patterns', 'integration-points', 'testing', 'dependencies']
}

function selectAngles(taskDescription, count) {
  const text = taskDescription.toLowerCase()
  let preset = 'feature'
  if (/refactor|architect|restructure|modular/.test(text)) preset = 'architecture'
  else if (/security|auth|permission|access/.test(text)) preset = 'security'
  else if (/performance|slow|optimi|cache/.test(text)) preset = 'performance'
  else if (/fix|bug|error|issue|broken/.test(text)) preset = 'bugfix'
  return ANGLE_PRESETS[preset].slice(0, count)
}

const selectedAngles = selectAngles(task_description, complexity === 'High' ? 4 : (complexity === 'Medium' ? 3 : 1))

// Direct Claude planning ONLY for: Low + no prior analysis + single angle
const planningStrategy = (
  complexity === 'Low' && !hasPriorAnalysis && selectedAngles.length <= 1
) ? 'Direct Claude Planning' : 'cli-lite-planning-agent'

console.log(`Exploration Plan: ${complexity} | ${selectedAngles.join(', ')} | ${planningStrategy}`)
```

**Launch Parallel Explorations**:

**CRITICAL**: MUST NOT use `run_in_background: true` — exploration results are REQUIRED before planning.

```javascript
const explorationTasks = selectedAngles.map((angle, index) =>
  Task(
    subagent_type="cli-explore-agent",
    run_in_background=false,
    description=`Explore: ${angle}`,
    prompt=`
## Task Objective
Execute **${angle}** exploration for task planning context.

## Output Location
**Session Folder**: ${sessionFolder}
**Output File**: ${sessionFolder}/exploration-${angle}.json

## Assigned Context
- **Exploration Angle**: ${angle}
- **Task Description**: ${task_description}
- **Exploration Index**: ${index + 1} of ${selectedAngles.length}

## Exploration Strategy (${angle} focus)

**Step 1: Structural Scan** (Bash)
- get_modules_by_depth.sh → identify modules related to ${angle}
- find/rg → locate files relevant to ${angle} aspect
- Analyze imports/dependencies from ${angle} perspective

**Step 2: Semantic Analysis** (Gemini CLI)
- How does existing code handle ${angle} concerns?
- What patterns are used for ${angle}?
- Where would new code integrate from ${angle} viewpoint?

**Step 3: Write Output**
- Consolidate ${angle} findings into JSON
- Identify ${angle}-specific clarification needs

## Expected Output
**Schema**: explore-json-schema.json (auto-loaded by agent)
- All fields scoped to ${angle} perspective
- Ensure rationale is specific and >10 chars (not generic)
- Include file:line locations in integration_points
- _metadata.exploration_angle: "${angle}"

## Success Criteria
- [ ] get_modules_by_depth.sh executed
- [ ] At least 3 relevant files with specific rationale (>10 chars) + role classification
- [ ] Patterns are actionable (code examples, not generic advice)
- [ ] Integration points include file:line locations
- [ ] Constraints are project-specific to ${angle}
- [ ] JSON follows schema; clarification_needs includes options + recommended
- [ ] Files with relevance >= 0.7 have key_code array + topic_relation

## Execution
**Write**: \`${sessionFolder}/exploration-${angle}.json\`
**Return**: 2-3 sentence summary of ${angle} findings
`
  )
)
// Execute all exploration tasks in parallel
```

**Auto-discover & Build Manifest**:
```javascript
const explorationFiles = bash(`find ${sessionFolder} -name "exploration-*.json" -type f`)
  .split('\n').filter(f => f.trim())

const explorationManifest = {
  session_id: sessionId,
  task_description: task_description,
  timestamp: getUtc8ISOString(),
  complexity: complexity,
  exploration_count: explorationFiles.length,
  explorations: explorationFiles.map(file => {
    const data = JSON.parse(Read(file))
    return {
      angle: data._metadata.exploration_angle,
      file: path.basename(file),
      path: file,
      index: data._metadata.exploration_index
    }
  })
}

Write(`${sessionFolder}/explorations-manifest.json`, JSON.stringify(explorationManifest, null, 2))
console.log(`Exploration complete: ${explorationManifest.explorations.map(e => e.angle).join(', ')}`)
```

// TodoWrite: Phase 1 → completed, Phase 2 → in_progress

**Output**: `exploration-{angle}.json` (1-4 files) + `explorations-manifest.json`

## 7. LP-Phase 2: Clarification (Optional, Multi-Round)

**Skip if**: No exploration or `clarification_needs` is empty across all explorations

**CRITICAL**: AskUserQuestion limits max 4 questions per call. **MUST execute multiple rounds** to exhaust all clarification needs.

```javascript
const manifest = file_exists(`${sessionFolder}/explorations-manifest.json`)
  ? JSON.parse(Read(`${sessionFolder}/explorations-manifest.json`))
  : { exploration_count: 0, explorations: [] }
const explorations = manifest.explorations.map(exp => ({
  angle: exp.angle,
  data: JSON.parse(Read(exp.path))
}))

// Aggregate from all explorations
const allClarifications = []
explorations.forEach(exp => {
  if (exp.data.clarification_needs?.length > 0) {
    exp.data.clarification_needs.forEach(need => {
      allClarifications.push({ ...need, source_angle: exp.angle })
    })
  }
})

// Intelligent dedup: merge similar intent across angles, combine options
const dedupedClarifications = intelligentMerge(allClarifications)

if (workflowPreferences.autoYes) {
  console.log(`[Auto] Skipping ${dedupedClarifications.length} clarification questions`)
} else if (dedupedClarifications.length > 0) {
  const BATCH_SIZE = 4
  const totalRounds = Math.ceil(dedupedClarifications.length / BATCH_SIZE)

  for (let i = 0; i < dedupedClarifications.length; i += BATCH_SIZE) {
    const batch = dedupedClarifications.slice(i, i + BATCH_SIZE)
    const currentRound = Math.floor(i / BATCH_SIZE) + 1
    console.log(`### Clarification Round ${currentRound}/${totalRounds}`)

    AskUserQuestion({
      questions: batch.map(need => ({
        question: `[${need.source_angle}] ${need.question}\n\nContext: ${need.context}`,
        header: need.source_angle.substring(0, 12),
        multiSelect: false,
        options: need.options.map((opt, index) => ({
          label: need.recommended === index ? `${opt} ★` : opt,
          description: need.recommended === index ? `Recommended` : `Use ${opt}`
        }))
      }))
    })
    // Store batch responses in clarificationContext before next round
  }
}
```

**Output**: `clarificationContext` (in-memory)

## 8. LP-Phase 3: Planning

**IMPORTANT**: LP-Phase 3 is **planning only** — NO code execution. All execution happens in LP-Phase 5 via lite-execute.

**Executor Assignment** (after plan generation):
```javascript
// Priority: 1. User explicit ("用 gemini 分析..." → gemini) | 2. Default → agent
const executorAssignments = {}  // { taskId: { executor: 'gemini'|'codex'|'agent', reason } }
const taskFiles = Glob(`${sessionFolder}/.task/TASK-*.json`)
taskFiles.forEach(taskPath => {
  const task = JSON.parse(Read(taskPath))
  executorAssignments[task.id] = { executor: '...', reason: '...' }
})
```

**Low Complexity** — Direct planning by Claude:
```javascript
const schema = Bash(`cat ~/.ccw/workflows/cli-templates/schemas/plan-overview-base-schema.json`)

const manifest = file_exists(`${sessionFolder}/explorations-manifest.json`)
  ? JSON.parse(Read(`${sessionFolder}/explorations-manifest.json`))
  : { explorations: [] }
manifest.explorations.forEach(exp => {
  console.log(`\n### Exploration: ${exp.angle}\n${Read(exp.path)}`)
})

// When handoffSpec exists, use it as primary planning input
// implementation_scope[].acceptance_criteria -> convergence.criteria
// implementation_scope[].target_files -> files[]
// implementation_scope[].objective -> task title/description
if (handoffSpec) {
  console.log(`\n### Handoff Spec from ${handoffSpec.source}`)
  console.log(`Scope items: ${handoffSpec.implementation_scope.length}`)
  handoffSpec.implementation_scope.forEach((item, i) => {
    console.log(`  ${i+1}. ${item.objective} [${item.priority}] — Done when: ${item.acceptance_criteria.join('; ')}`)
  })
}

// Generate tasks — MUST incorporate exploration insights OR handoff spec
// When handoffSpec: map implementation_scope[] → tasks[] (1:1 or group by context)
// Field names: convergence.criteria (not acceptance), files[].change (not modification_points), test (not verification)
const tasks = [
  {
    id: "TASK-001", title: "...", description: "...", depends_on: [],
    convergence: { criteria: ["..."] },  // From handoffSpec: item.acceptance_criteria
    files: [{ path: "...", change: "..." }],  // From handoffSpec: item.target_files + item.change_summary
    implementation: ["..."], test: "..."
  }
]

const taskDir = `${sessionFolder}/.task`
Bash(`mkdir -p "${taskDir}"`)
tasks.forEach(task => Write(`${taskDir}/${task.id}.json`, JSON.stringify(task, null, 2)))

const plan = {
  summary: "...", approach: "...",
  task_ids: tasks.map(t => t.id), task_count: tasks.length,
  complexity: "Low", estimated_time: "...", recommended_execution: "Agent",
  _metadata: { timestamp: getUtc8ISOString(), source: "direct-planning", planning_mode: "direct", plan_type: "feature" }
}
Write(`${sessionFolder}/plan.json`, JSON.stringify(plan, null, 2))
// MUST continue to LP-Phase 4 — DO NOT execute code here
```

**Medium/High Complexity** — Invoke cli-lite-planning-agent:

```javascript
Task(
  subagent_type="cli-lite-planning-agent",
  run_in_background=false,
  description="Generate detailed implementation plan",
  prompt=`
Generate implementation plan and write plan.json.

## Output Location
**Session Folder**: ${sessionFolder}
**Output Files**:
- ${sessionFolder}/planning-context.md (evidence + understanding)
- ${sessionFolder}/plan.json (plan overview — NO embedded tasks[])
- ${sessionFolder}/.task/TASK-*.json (independent task files, one per task)

## Schema Reference
Execute: cat ~/.ccw/workflows/cli-templates/schemas/plan-overview-base-schema.json

## Project Context (MANDATORY)
Execute: ccw spec load --category planning
**CRITICAL**: All generated tasks MUST comply with constraints in specs/*.md

## Task Description
${task_description}

## Multi-Angle Exploration Context

${manifest.explorations.length > 0
  ? manifest.explorations.map(exp => `### Exploration: ${exp.angle} (${exp.file})
Path: ${exp.path}
Read this file for detailed ${exp.angle} analysis.`).join('\n\n') + `

Total: ${manifest.exploration_count} | Angles: ${manifest.explorations.map(e => e.angle).join(', ')}
Manifest: ${sessionFolder}/explorations-manifest.json`
  : `No exploration files. Task Description contains "## Prior Analysis" — use as primary planning context.`}

## Structured Handoff Spec (from analyze-with-file)
${handoffSpec ? `
**Source**: ${handoffSpec.source} session ${handoffSpec.session_id}
**CRITICAL**: Use implementation_scope as PRIMARY input for task generation.
Each scope item maps to one or more tasks. Acceptance criteria become convergence.criteria.

${JSON.stringify(handoffSpec.implementation_scope, null, 2)}

**Code Anchors** (implementation targets):
${JSON.stringify(handoffSpec.code_anchors?.slice(0, 8), null, 2)}

**Key Findings** (context):
${JSON.stringify(handoffSpec.key_findings?.slice(0, 5), null, 2)}

**Task Generation Rules when handoffSpec present**:
1. Each implementation_scope item → 1 task (group only if tightly coupled)
2. scope.acceptance_criteria[] → task.convergence.criteria[]
3. scope.target_files[] → task.files[] with change from scope.change_summary
4. scope.objective → task.title, scope.rationale → task.description context
5. scope.priority → task ordering (high first)
` : 'No structured handoff spec — use task description and explorations as input.'}

## User Clarifications
${JSON.stringify(clarificationContext) || "None"}

## Complexity Level
${complexity}

## Requirements
- _metadata.exploration_angles: ${JSON.stringify(manifest.explorations.map(e => e.angle))}
- Two-layer output: plan.json (task_ids[], NO tasks[]) + .task/TASK-*.json
- Follow plan-overview-base-schema.json for plan.json, task-schema.json for .task/*.json
- Field names: files[].change (not modification_points), convergence.criteria (not acceptance)

## Task Grouping Rules
1. **Group by feature**: All changes for one feature = one task (even if 3-5 files)
2. **Group by context**: Related functional changes can be grouped together
3. **Minimize agent count**: Group simple unrelated tasks to reduce overhead
4. **Avoid file-per-task**: Do NOT create separate tasks for each file
5. **Substantial tasks**: Each task = 15-60 minutes of work
6. **True dependencies only**: depends_on only when Task B needs Task A's output
7. **Prefer parallel**: Most tasks should be independent

## Execution
1. Read schema → 2. ccw spec load → 3. Read ALL exploration files → 4. Synthesize + generate
5. Write: planning-context.md, .task/TASK-*.json, plan.json (task_ids[], NO tasks[])
6. Return brief completion summary
`
)
```

**Output**: `${sessionFolder}/plan.json`

// TodoWrite: Phase 3 → completed, Phase 4 → in_progress

## 9. LP-Phase 4: Task Confirmation & Execution Selection

**Display Plan**:
```javascript
const plan = JSON.parse(Read(`${sessionFolder}/plan.json`))
const tasks = (plan.task_ids || []).map(id => JSON.parse(Read(`${sessionFolder}/.task/${id}.json`)))

console.log(`
## Implementation Plan
**Summary**: ${plan.summary}
**Approach**: ${plan.approach}
**Tasks** (${tasks.length}):
${tasks.map((t, i) => `${i+1}. ${t.title} (${t.scope || t.files?.[0]?.path || ''})`).join('\n')}
**Complexity**: ${plan.complexity} | **Time**: ${plan.estimated_time} | **Recommended**: ${plan.recommended_execution}
`)
```

**Collect Confirmation**:
```javascript
let userSelection

if (workflowPreferences.autoYes) {
  console.log(`[Auto] Allow & Execute | Auto | Skip + Skip`)
  userSelection = { confirmation: "Allow", execution_method: "Auto", code_review_tool: "Skip", convergence_review_tool: "Skip" }
} else {
  // "Other" in Execution allows specifying CLI tools from ~/.claude/cli-tools.json
  userSelection = AskUserQuestion({
    questions: [
      {
        question: `Confirm plan and authorize execution? (${tasks.length} tasks, ${plan.complexity})`,
        header: "Confirm",
        multiSelect: false,
        options: [
          { label: "Allow & Execute", description: "Approve plan and begin execution immediately (no further prompts)" },
          { label: "Modify", description: "Adjust before execution" },
          { label: "Cancel", description: "Abort workflow" }
        ]
      },
      {
        question: "Execution method:",
        header: "Execution",
        multiSelect: false,
        options: [
          { label: "Agent", description: "@code-developer agent" },
          { label: "Codex", description: "codex CLI tool" },
          { label: "Auto", description: `Auto: ${plan.complexity === 'Low' ? 'Agent' : 'Codex'}` }
        ]
      },
      {
        question: "Code review after execution? (runs in lite-execute)",
        header: "Code Review",
        multiSelect: false,
        options: [
          { label: "Gemini Review", description: "Gemini CLI: git diff quality review" },
          { label: "Codex Review", description: "Codex CLI: git-aware code review (--mode review)" },
          { label: "Agent Review", description: "@code-reviewer agent" },
          { label: "Skip", description: "No code review" }
        ]
      },
      {
        question: "Convergence review in test-review phase?",
        header: "Convergence Review",
        multiSelect: false,
        options: [
          { label: "Agent", description: "Agent: verify convergence criteria against implementation" },
          { label: "Gemini", description: "Gemini CLI: convergence verification" },
          { label: "Codex", description: "Codex CLI: convergence verification" },
          { label: "Skip", description: "Skip convergence review, run tests only" }
        ]
      }
    ]
  })
}
```

// TodoWrite: Phase 4 → completed `[${userSelection.execution_method} | CR:${userSelection.code_review_tool} | CVR:${userSelection.convergence_review_tool}]`, Phase 5 → in_progress

## 10. LP-Phase 5: Handoff to Execution

**CRITICAL**: lite-plan NEVER executes code directly. ALL execution goes through lite-execute.

**Build executionContext**:
```javascript
const manifest = file_exists(`${sessionFolder}/explorations-manifest.json`)
  ? JSON.parse(Read(`${sessionFolder}/explorations-manifest.json`))
  : { exploration_count: 0, explorations: [] }
const explorations = {}
manifest.explorations.forEach(exp => {
  if (file_exists(exp.path)) explorations[exp.angle] = JSON.parse(Read(exp.path))
})

const plan = JSON.parse(Read(`${sessionFolder}/plan.json`))

executionContext = {
  planObject: plan,
  taskFiles: (plan.task_ids || []).map(id => ({ id, path: `${sessionFolder}/.task/${id}.json` })),
  explorationsContext: explorations,
  explorationAngles: manifest.explorations.map(e => e.angle),
  explorationManifest: manifest,
  clarificationContext: clarificationContext || null,
  executionMethod: userSelection.execution_method,
  codeReviewTool: userSelection.code_review_tool,
  convergenceReviewTool: userSelection.convergence_review_tool,
  originalUserInput: task_description,
  executorAssignments: executorAssignments,  // { taskId: { executor, reason } } — overrides executionMethod
  session: {
    id: sessionId,
    folder: sessionFolder,
    artifacts: {
      explorations: manifest.explorations.map(exp => ({ angle: exp.angle, path: exp.path })),
      explorations_manifest: `${sessionFolder}/explorations-manifest.json`,
      plan: `${sessionFolder}/plan.json`,
      task_dir: `${sessionFolder}/.task`
    }
  }
}
```

**Handoff**:
```javascript
if (!workflowPreferences.autoYes) {
  console.log(`Handing off to execution engine. No further prompts.`)
}

// TodoWrite: Phase 5 → completed, add LE-Phase 1 → in_progress
const taskCount = (plan.task_ids || []).length
TodoWrite({ todos: [
  { content: "LP-Phase 1: Exploration", status: "completed" },
  { content: "LP-Phase 2: Clarification", status: "completed" },
  { content: "LP-Phase 3: Planning", status: "completed" },
  { content: `LP-Phase 4: Confirmed [${userSelection.execution_method} | CR:${userSelection.code_review_tool} | CVR:${userSelection.convergence_review_tool}]`, status: "completed" },
  { content: `LP-Phase 5: Handoff → lite-execute`, status: "completed" },
  { content: `LE-Phase 1: Task Loading [${taskCount} tasks]`, status: "in_progress", activeForm: "Loading tasks" }
]})

Skill("lite-execute")
// executionContext passed as global variable (Mode 1: In-Memory Plan)
```

## 11. Session Folder Structure

```
.workflow/.lite-plan/{task-slug}-{YYYY-MM-DD}/
├── exploration-{angle}.json (1-4)   # Per-angle exploration
├── explorations-manifest.json        # Exploration index
├── planning-context.md               # Evidence paths + understanding
├── plan.json                         # Plan overview (task_ids[])
├── code-review.md                    # Generated by lite-execute Step 4
├── test-checklist.json               # Generated by lite-test-review
├── test-review.md                    # Generated by lite-test-review
└── .task/
    ├── TASK-001.json
    ├── TASK-002.json
    └── ...
```

## Chain: lite-plan → lite-execute → lite-test-review

```
lite-plan (LP-Phase 1-5)
  └─ Skill("lite-execute")     ← executionContext (global)
       ├─ Step 1-3: Task Execution
       ├─ Step 4: Code Review (quality/correctness/security)
       └─ Step 5: Skill("lite-test-review")  ← testReviewContext (global)
            ├─ TR-Phase 1: Detect test framework
            ├─ TR-Phase 2: Convergence verification (plan criteria)
            ├─ TR-Phase 3-4: Run tests + Auto-fix
            └─ TR-Phase 5: Report + Sync specs
```

## 12. Error Handling

| Error | Resolution |
|-------|------------|
| Exploration agent failure | Skip exploration, continue with task description only |
| Planning agent failure | Fallback to direct planning by Claude |
| Clarification timeout | Use exploration findings as-is |
| Confirmation timeout | Save context, display resume instructions |
| Modify loop > 3 times | Suggest breaking task or using /workflow-plan |

</process>

<auto_mode>
When `workflowPreferences.autoYes === true` (entire plan+execute workflow):
- **Clarification**: Skipped | **Plan Confirmation**: Allow & Execute | **Execution**: Auto | **Review**: Skip

Auto mode authorizes the complete plan-and-execute workflow with a single confirmation. No further prompts.
</auto_mode>

<success_criteria>
- [ ] Workflow preferences (autoYes, forceExplore) initialized at LP-Phase 0
- [ ] Complexity assessed and exploration angles selected appropriately
- [ ] Parallel exploration agents launched with run_in_background=false
- [ ] Explorations manifest built from auto-discovered files
- [ ] Clarification needs aggregated, deduped, and presented in batches of 4
- [ ] Plan generated via direct Claude (Low) or cli-lite-planning-agent (Medium/High)
- [ ] Plan output as two-layer: plan.json (task_ids[]) + .task/TASK-*.json
- [ ] User confirmation collected (or auto-approved in auto mode)
- [ ] executionContext fully built with all artifacts and session references
- [ ] Handoff to lite-execute via Skill("lite-execute") with executionContext
- [ ] No code execution in planning phases -- all execution deferred to lite-execute
</success_criteria>
