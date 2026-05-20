---
name: workflow-lite-execute
description: Lightweight execution engine - multi-mode input, task grouping, batch execution, chain to test-review
allowed-tools: Skill, Agent, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow-Lite-Execute

Execution engine for workflow-lite-plan handoff and standalone task execution.

---

## Usage

```
<input>                    Task description string, or path to file (required)
```

| Flag | Description |
|------|-------------|
| `--in-memory` | Mode 1: Use executionContext from workflow-lite-plan handoff (via Skill({ skill: "workflow-lite-execute", args: "--in-memory" }) |

## Input Modes

### Mode 1: In-Memory Plan

**Trigger**: `--in-memory` flag or `executionContext` global variable available

**Input Source**: `executionContext` global variable set by workflow-lite-plan

**Behavior**: Skip execution method/code review selection (already chosen in LP-Phase 4), directly proceed with full context (exploration, clarifications, plan artifacts all available)

> **Note**: LP-Phase 4 is the single confirmation gate. Mode 1 invocation means user already approved — no further prompts.

### Mode 2: Prompt Description

**Trigger**: User calls with task description string (e.g., "Add unit tests for auth module")

**Behavior**: Store prompt as `originalUserInput` → create simple execution plan → run `selectExecutionOptions()` → proceed

### Mode 3: File Content

**Trigger**: User calls with file path (ends with .md/.json/.txt)

```javascript
fileContent = Read(filePath)
try {
  jsonData = JSON.parse(fileContent)
  // plan.json detection: two-layer format with task_ids[]
  if (jsonData.summary && jsonData.approach && jsonData.task_ids) {
    planObject = jsonData
    originalUserInput = jsonData.summary
    isPlanJson = true
    const planDir = filePath.replace(/[/\\][^/\\]+$/, '')
    planObject._loadedTasks = loadTaskFiles(planDir, jsonData.task_ids)
  } else {
    originalUserInput = fileContent
    isPlanJson = false
  }
} catch {
  originalUserInput = fileContent
  isPlanJson = false
}
```

- `isPlanJson === true`: Use `planObject` directly → run `selectExecutionOptions()`
- `isPlanJson === false`: Treat as prompt (same as Mode 2)

### User Selection (Mode 2/3 shared)

```javascript
function selectExecutionOptions() {
  // autoYes: set by -y flag (standalone only; Mode 1 never reaches here)
  const autoYes = workflowPreferences?.autoYes ?? false

  if (autoYes) {
    return { execution_method: "Auto", code_review_tool: "Skip", convergence_review_tool: "Skip" }
  }

  return AskUserQuestion({
    questions: [
      {
        question: "Select execution method:",
        header: "Execution",
        multiSelect: false,
        options: [
          { label: "Agent", description: "@code-developer agent" },
          { label: "Codex", description: "codex CLI tool" },
          { label: "Auto", description: "Auto-select based on complexity" }
        ]
      },
      {
        question: "Code review after execution? (runs here in lite-execute)",
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
          { label: "Agent", description: "Agent: verify convergence criteria" },
          { label: "Gemini", description: "Gemini CLI: convergence verification" },
          { label: "Codex", description: "Codex CLI: convergence verification" },
          { label: "Skip", description: "Skip convergence review, run tests only" }
        ]
      }
    ]
  })
}
```

## Execution Steps

### Step 1: Initialize & Echo Strategy

```javascript
previousExecutionResults = []

// Mode 1: echo strategy for transparency
if (executionContext) {
  console.log(`
  Execution Strategy (from lite-plan):
   Method: ${executionContext.executionMethod}
   Code Review: ${executionContext.codeReviewTool}
   Convergence Review: ${executionContext.convergenceReviewTool}
   Tasks: ${getTasks(executionContext.planObject).length}
   Complexity: ${executionContext.planObject.complexity}
${executionContext.executorAssignments ? `   Assignments: ${JSON.stringify(executionContext.executorAssignments)}` : ''}
  `)
}

// Helper: load .task/*.json files (two-layer format)
function loadTaskFiles(planDir, taskIds) {
  return taskIds.map(id => JSON.parse(Read(`${planDir}/.task/${id}.json`)))
}
function getTasks(planObject) {
  return planObject._loadedTasks || []
}
```

### Step 2: Task Grouping & Batch Creation

```javascript
// Dependency extraction: explicit depends_on only (no file/keyword inference)
function extractDependencies(tasks) {
  const taskIdToIndex = {}
  tasks.forEach((t, i) => { taskIdToIndex[t.id] = i })
  return tasks.map((task, i) => {
    const deps = (task.depends_on || [])
      .map(depId => taskIdToIndex[depId])
      .filter(idx => idx !== undefined && idx < i)
    return { ...task, taskIndex: i, dependencies: deps }
  })
}

// Executor resolution: executorAssignments[taskId] > executionMethod > Auto fallback
function getTaskExecutor(task) {
  const assignments = executionContext?.executorAssignments || {}
  if (assignments[task.id]) return assignments[task.id].executor  // 'gemini' | 'codex' | 'agent'
  const method = executionContext?.executionMethod || 'Auto'
  if (method === 'Agent') return 'agent'
  if (method === 'Codex') return 'codex'
  return planObject.complexity === 'Low' ? 'agent' : 'codex'  // Auto fallback
}

function groupTasksByExecutor(tasks) {
  const groups = { gemini: [], codex: [], agent: [] }
  tasks.forEach(task => { groups[getTaskExecutor(task)].push(task) })
  return groups
}

// Batch creation: independent → per-executor parallel, dependent → sequential phases
function createExecutionCalls(tasks, executionMethod) {
  const tasksWithDeps = extractDependencies(tasks)
  const processed = new Set()
  const calls = []

  // Phase 1: Independent tasks → per-executor parallel batches
  const independentTasks = tasksWithDeps.filter(t => t.dependencies.length === 0)
  if (independentTasks.length > 0) {
    const executorGroups = groupTasksByExecutor(independentTasks)
    let parallelIndex = 1
    for (const [executor, tasks] of Object.entries(executorGroups)) {
      if (tasks.length === 0) continue
      tasks.forEach(t => processed.add(t.taskIndex))
      calls.push({
        method: executionMethod, executor, executionType: "parallel",
        groupId: `P${parallelIndex++}`,
        taskSummary: tasks.map(t => t.title).join(' | '), tasks
      })
    }
  }

  // Phase 2+: Dependent tasks → respect dependency order
  let sequentialIndex = 1
  let remaining = tasksWithDeps.filter(t => !processed.has(t.taskIndex))
  while (remaining.length > 0) {
    let ready = remaining.filter(t => t.dependencies.every(d => processed.has(d)))
    if (ready.length === 0) { console.warn('Circular dependency detected, forcing remaining'); ready = [...remaining] }

    if (ready.length > 1) {
      const executorGroups = groupTasksByExecutor(ready)
      for (const [executor, tasks] of Object.entries(executorGroups)) {
        if (tasks.length === 0) continue
        tasks.forEach(t => processed.add(t.taskIndex))
        calls.push({
          method: executionMethod, executor, executionType: "parallel",
          groupId: `P${calls.length + 1}`,
          taskSummary: tasks.map(t => t.title).join(' | '), tasks
        })
      }
    } else {
      ready.forEach(t => processed.add(t.taskIndex))
      calls.push({
        method: executionMethod, executor: getTaskExecutor(ready[0]),
        executionType: "sequential", groupId: `S${sequentialIndex++}`,
        taskSummary: ready[0].title, tasks: ready
      })
    }
    remaining = remaining.filter(t => !processed.has(t.taskIndex))
  }
  return calls
}

executionCalls = createExecutionCalls(getTasks(planObject), executionMethod).map(c => ({ ...c, id: `[${c.groupId}]` }))

TodoWrite({
  todos: executionCalls.map((c, i) => ({
    content: `${c.executionType === "parallel" ? "⚡" : `→ [${i+1}/${executionCalls.filter(x=>x.executionType==="sequential").length}]`} ${c.id} [${c.executor}] ${c.tasks.map(t=>t.id).join(', ')}`,
    status: "pending",
    activeForm: `Waiting: ${c.tasks.length} task(s) via ${c.executor}`
  }))
})
```

### Step 3: Launch Execution & Track Progress

> **CHECKPOINT**: Verify Phase 2 execution protocol (Step 3-5) is in active memory. If only a summary remains, re-read `phases/02-lite-execute.md` now.

**Batch Routing** (by `batch.executor` field):
```javascript
function executeBatch(batch) {
  const executor = batch.executor || getTaskExecutor(batch.tasks[0])
  const sessionId = executionContext?.session?.id || 'standalone'
  const fixedId = `${sessionId}-${batch.groupId}`

  if (executor === 'agent') {
    return Agent({ subagent_type: "code-developer", run_in_background: false,
      description: batch.taskSummary, prompt: buildExecutionPrompt(batch) })
  } else {
    // CLI execution (codex/gemini): background with fixed ID
    const tool = executor  // 'codex' | 'gemini'
    const mode = executor === 'gemini' ? 'analysis' : 'write'
    const previousCliId = batch.resumeFromCliId || null
    const cmd = previousCliId
      ? `ccw cli -p "${buildExecutionPrompt(batch)}" --tool ${tool} --mode ${mode} --id ${fixedId} --resume ${previousCliId}`
      : `ccw cli -p "${buildExecutionPrompt(batch)}" --tool ${tool} --mode ${mode} --id ${fixedId}`
    return Bash(cmd, { run_in_background: true })
    // STOP - wait for task hook callback
  }
}
```

**Parallel execution rules**:
- Each batch = one independent CLI instance or Agent call
- Parallel = multiple Bash(run_in_background=true) or multiple Agent() in single message
- Never merge independent tasks into one CLI prompt
- Agent: run_in_background=false, but multiple Agent() calls can be concurrent in single message

**Execution Flow**: Parallel batches concurrently → Sequential batches in order
```javascript
const parallel = executionCalls.filter(c => c.executionType === "parallel")
const sequential = executionCalls.filter(c => c.executionType === "sequential")

// Phase 1: All parallel batches (single message, multiple tool calls)
if (parallel.length > 0) {
  TodoWrite({ todos: executionCalls.map(c => ({
    status: c.executionType === "parallel" ? "in_progress" : "pending",
    activeForm: c.executionType === "parallel" ? `Running [${c.executor}]: ${c.tasks.map(t=>t.id).join(', ')}` : `Blocked by parallel phase`
  })) })
  parallelResults = await Promise.all(parallel.map(c => executeBatch(c)))
  previousExecutionResults.push(...parallelResults)
  TodoWrite({ todos: executionCalls.map(c => ({
    status: parallel.includes(c) ? "completed" : "pending",
    activeForm: parallel.includes(c) ? `Done [${c.executor}]` : `Ready`
  })) })
}

// Phase 2: Sequential batches one by one
for (const call of sequential) {
  TodoWrite({ todos: executionCalls.map(c => ({
    status: c === call ? "in_progress" : (c.status === "completed" ? "completed" : "pending"),
    activeForm: c === call ? `Running [${c.executor}]: ${c.tasks.map(t=>t.id).join(', ')}` : undefined
  })) })
  result = await executeBatch(call)
  previousExecutionResults.push(result)
  TodoWrite({ todos: executionCalls.map(c => ({
    status: sequential.indexOf(c) <= sequential.indexOf(call) ? "completed" : "pending"
  })) })
}
```

**Resume on Failure**:
```javascript
if (bash_result.status === 'failed' || bash_result.status === 'timeout') {
  // fixedId = `${sessionId}-${groupId}` (predictable, no auto-generated timestamps)
  console.log(`Execution incomplete. Resume: ccw cli -p "Continue" --resume ${fixedId} --tool codex --mode write --id ${fixedId}-retry`)
  batch.resumeFromCliId = fixedId
}
```

Progress tracked at batch level. Icons: ⚡ parallel (concurrent), → sequential (one-by-one).

### Unified Task Prompt Builder

Each task is a self-contained checklist. Same template for Agent and CLI.

```javascript
function buildExecutionPrompt(batch) {
  const formatTask = (t) => `
## ${t.title}

**Scope**: \`${t.scope}\`  |  **Action**: ${t.action}

### Files
${(t.files || []).map(f => `- **${f.path}** → \`${f.target || ''}\`: ${f.change || (f.changes || []).join(', ') || ''}`).join('\n')}

${t.rationale ? `### Why this approach (Medium/High)
${t.rationale.chosen_approach}
${t.rationale.decision_factors?.length > 0 ? `Key factors: ${t.rationale.decision_factors.join(', ')}` : ''}
${t.rationale.tradeoffs ? `Tradeoffs: ${t.rationale.tradeoffs}` : ''}` : ''}

### How to do it
${t.description}
${t.implementation.map(step => `- ${step}`).join('\n')}

${t.code_skeleton ? `### Code skeleton (High)
${t.code_skeleton.interfaces?.length > 0 ? `**Interfaces**: ${t.code_skeleton.interfaces.map(i => `\`${i.name}\` - ${i.purpose}`).join(', ')}` : ''}
${t.code_skeleton.key_functions?.length > 0 ? `**Functions**: ${t.code_skeleton.key_functions.map(f => `\`${f.signature}\` - ${f.purpose}`).join(', ')}` : ''}
${t.code_skeleton.classes?.length > 0 ? `**Classes**: ${t.code_skeleton.classes.map(c => `\`${c.name}\` - ${c.purpose}`).join(', ')}` : ''}` : ''}

### Reference
- Pattern: ${t.reference?.pattern || 'N/A'}
- Files: ${t.reference?.files?.join(', ') || 'N/A'}
${t.reference?.examples ? `- Notes: ${t.reference.examples}` : ''}

${t.risks?.length > 0 ? `### Risk mitigations (High)
${t.risks.map(r => `- ${r.description} → **${r.mitigation}**`).join('\n')}` : ''}

### Done when
${(t.convergence?.criteria || []).map(c => `- [ ] ${c}`).join('\n')}
${(t.test?.success_metrics || []).length > 0 ? `**Success metrics**: ${t.test.success_metrics.join(', ')}` : ''}`

  const sections = []
  if (originalUserInput) sections.push(`## Goal\n${originalUserInput}`)
  sections.push(`## Tasks\n${batch.tasks.map(formatTask).join('\n\n---\n')}`)

  const context = []
  if (previousExecutionResults.length > 0)
    context.push(`### Previous Work\n${previousExecutionResults.map(r => `- ${r.tasksSummary}: ${r.status}`).join('\n')}`)
  if (clarificationContext)
    context.push(`### Clarifications\n${Object.entries(clarificationContext).map(([q, a]) => `- ${q}: ${a}`).join('\n')}`)
  if (executionContext?.planObject?.data_flow?.diagram)
    context.push(`### Data Flow\n${executionContext.planObject.data_flow.diagram}`)
  if (executionContext?.session?.artifacts?.plan)
    context.push(`### Artifacts\nPlan: ${executionContext.session.artifacts.plan}`)
  context.push(`### Project Guidelines\n(Loaded via ccw spec load --category planning)`)
  if (context.length > 0) sections.push(`## Context\n${context.join('\n\n')}`)

  sections.push(`Complete each task according to its "Done when" checklist.`)
  return sections.join('\n\n')
}
```

### Step 4: Code Review

**Skip if**: `codeReviewTool === 'Skip'`

**Resolve review tool**: From `executionContext.codeReviewTool` (Mode 1) or `userSelection.code_review_tool` (Mode 2/3).

```javascript
const codeReviewTool = executionContext?.codeReviewTool || userSelection?.code_review_tool || 'Skip'
const resolvedTool = (() => {
  if (!codeReviewTool || codeReviewTool === 'Skip') return 'skip'
  if (/gemini/i.test(codeReviewTool)) return 'gemini'
  if (/codex/i.test(codeReviewTool)) return 'codex'
  return 'agent'
})()

if (resolvedTool === 'skip') {
  console.log('[Code Review] Skipped')
} else {
  // proceed with review
}
```

**Agent Code Review** (resolvedTool === 'agent'):

```javascript
Agent({
  subagent_type: "code-reviewer",
  run_in_background: false,
  description: `Code review: ${planObject.summary}`,
  prompt: `## Code Review — Post-Execution Quality Check

**Goal**: ${originalUserInput}
**Plan Summary**: ${planObject.summary}

### Changed Files
Run \`git diff --name-only HEAD~${getTasks(planObject).length}..HEAD\` to identify changes.

### Review Focus
1. **Code quality**: Readability, naming, structure, dead code
2. **Correctness**: Logic errors, off-by-one, null handling, edge cases
3. **Patterns**: Consistency with existing codebase conventions
4. **Security**: Injection, XSS, auth bypass, secrets exposure
5. **Performance**: Unnecessary loops, N+1 queries, missing indexes

### Instructions
1. Run git diff to see actual changes
2. Read changed files for full context
3. For each issue found: severity (Critical/High/Medium/Low) + file:line + description + fix suggestion
4. Return structured review: issues[], summary, overall verdict (PASS/WARN/FAIL)`
})
```

**CLI Code Review — Codex** (resolvedTool === 'codex'):

```javascript
const reviewId = `${sessionId}-code-review`
Bash(`ccw cli -p "Review code changes for quality, correctness, security, and pattern compliance. Focus: ${planObject.summary}" --tool codex --mode review --id ${reviewId}`, { run_in_background: true })
// STOP - wait for hook callback
```

**CLI Code Review — Gemini** (resolvedTool === 'gemini'):

```javascript
const reviewId = `${sessionId}-code-review`
Bash(`ccw cli -p "PURPOSE: Post-execution code quality review for: ${planObject.summary}
TASK: • Run git diff to identify all changes • Review each changed file for quality, correctness, security • Check pattern compliance with existing codebase • Identify potential bugs, edge cases, performance issues
MODE: analysis
CONTEXT: @**/* | Memory: lite-execute completed, reviewing code quality
EXPECTED: Per-file review with severity levels (Critical/High/Medium/Low), file:line references, fix suggestions, overall verdict
CONSTRAINTS: Read-only | Focus on code quality not convergence" --tool gemini --mode analysis --rule analysis-review-code-quality --id ${reviewId}`, { run_in_background: true })
// STOP - wait for hook callback
```

**Write review artifact** (if session folder exists):
```javascript
if (executionContext?.session?.folder) {
  Write(`${executionContext.session.folder}/code-review.md`, codeReviewOutput)
}
```

### Step 5: Chain to Test Review & Post-Completion

**Resolve convergence review tool**: From `executionContext.convergenceReviewTool` (Mode 1) or `userSelection.convergence_review_tool` (Mode 2/3).

```javascript
function resolveConvergenceTool(ctx, selection) {
  const raw = ctx?.convergenceReviewTool || selection?.convergence_review_tool || 'skip'
  if (!raw || raw === 'Skip') return 'skip'
  if (/gemini/i.test(raw)) return 'gemini'
  if (/codex/i.test(raw)) return 'codex'
  return 'agent'
}
```

**Build testReviewContext and handoff**:

```javascript
testReviewContext = {
  planObject: planObject,
  taskFiles: executionContext?.taskFiles
    || getTasks(planObject).map(t => ({ id: t.id, path: `${executionContext?.session?.folder}/.task/${t.id}.json` })),
  convergenceReviewTool: resolveConvergenceTool(executionContext, userSelection),
  executionResults: previousExecutionResults,
  originalUserInput: originalUserInput,
  session: executionContext?.session || {
    id: 'standalone',
    folder: executionContext?.session?.folder || '.',
    artifacts: { plan: null, task_dir: null }
  }
}

// Chain to lite-test-review (Mode 1: In-Memory)
Skill("lite-test-review")
// testReviewContext passed as global variable
```

**After test-review returns**: Ask user whether to expand into issues (enhance/refactor/doc). Selected items call `/issue:new "{summary} - {dimension}"`.

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing executionContext | "No execution context found. Only available when called by lite-plan." |
| File not found | "File not found: {path}. Check file path." |
| Empty file | "File is empty: {path}. Provide task description." |
| Invalid plan JSON | Warning: "Missing required fields. Treating as plain text." |
| Malformed JSON | Treat as plain text (expected for non-JSON files) |
| Execution failure | Use fixed ID `${sessionId}-${groupId}` for resume |
| Execution timeout | Use fixed ID for resume with extended timeout |
| Codex unavailable | Show installation instructions, offer Agent execution |
| Fixed ID not found | Check `ccw cli history`, verify date directories |

## Data Structures

### executionContext (Input - Mode 1)

```javascript
{
  planObject: {
    summary: string,
    approach: string,
    task_ids: string[],
    task_count: number,
    _loadedTasks: [...],        // populated at runtime from .task/*.json
    estimated_time: string,
    recommended_execution: string,
    complexity: string
  },
  taskFiles: [{id: string, path: string}] | null,
  explorationsContext: {...} | null,
  explorationAngles: string[],
  explorationManifest: {...} | null,
  clarificationContext: {...} | null,
  executionMethod: "Agent" | "Codex" | "Auto",
  codeReviewTool: "Skip" | "Gemini Review" | "Codex Review" | "Agent Review",
  convergenceReviewTool: "Skip" | "Agent" | "Gemini" | "Codex",
  originalUserInput: string,
  executorAssignments: {            // per-task override, priority over executionMethod
    [taskId]: { executor: "gemini" | "codex" | "agent", reason: string }
  },
  session: {
    id: string,                     // {taskSlug}-{shortTimestamp}
    folder: string,                 // .workflow/.lite-plan/{session-id}
    artifacts: {
      explorations: [{angle, path}],
      explorations_manifest: string,
      plan: string                  // always present
    }
  }
}
```

### executionResult (Output)

```javascript
{
  executionId: string,              // e.g., "[Agent-1]", "[Codex-1]"
  status: "completed" | "partial" | "failed",
  tasksSummary: string,
  completionSummary: string,
  keyOutputs: string,
  notes: string,
  fixedCliId: string | null         // for resume: ccw cli detail ${fixedCliId}
}
// Appended to previousExecutionResults[] for context continuity
```
