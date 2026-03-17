---
name: unified-execute-with-file
description: Universal execution engine consuming .task/*.json directory format. Serial task execution with convergence verification, progress tracking via execution.md + execution-events.md.
argument-hint: "PLAN=\"<path/to/.task/>\" [--auto-commit] [--dry-run]"
---

# Unified-Execute-With-File Workflow

## Quick Start

Universal execution engine consuming **`.task/*.json`** directory and executing tasks serially with convergence verification and progress tracking.

```bash
# Execute from lite-plan output
/codex:unified-execute-with-file PLAN=".workflow/.lite-plan/LPLAN-auth-2025-01-21/.task/"

# Execute from workflow session output
/codex:unified-execute-with-file PLAN=".workflow/active/WFS-xxx/.task/" --auto-commit

# Execute a single task JSON file
/codex:unified-execute-with-file PLAN=".workflow/active/WFS-xxx/.task/IMPL-001.json" --dry-run

# Auto-detect from .workflow/ directories
/codex:unified-execute-with-file
```

**Core workflow**: Scan .task/*.json → Validate → Pre-Execution Analysis → Execute → Verify Convergence → Track Progress

**Key features**:
- **Directory-based**: Consumes `.task/` directory containing individual task JSON files
- **Convergence-driven**: Verifies each task's convergence criteria after execution
- **Serial execution**: Process tasks in topological order with dependency tracking
- **Dual progress tracking**: `execution.md` (overview) + `execution-events.md` (event stream)
- **Auto-commit**: Optional conventional commits per task
- **Dry-run mode**: Simulate execution without changes
- **Flexible input**: Accepts `.task/` directory path or a single `.json` file path

**Input format**: Each task is a standalone JSON file in `.task/` directory (e.g., `IMPL-001.json`). Use `plan-converter` to convert other formats to `.task/*.json` first.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   UNIFIED EXECUTE WORKFLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Phase 1: Load & Validate                                     │
│     ├─ Scan .task/*.json (one task per file)                   │
│     ├─ Validate schema (id, title, depends_on, convergence)   │
│     ├─ Detect cycles, build topological order                 │
│     └─ Initialize execution.md + execution-events.md          │
│                                                               │
│  Phase 2: Pre-Execution Analysis                              │
│     ├─ Check file conflicts (multiple tasks → same file)      │
│     ├─ Verify file existence                                  │
│     ├─ Generate feasibility report                            │
│     └─ User confirmation (unless dry-run)                     │
│                                                               │
│  Phase 3: Serial Execution + Convergence Verification         │
│     For each task in topological order:                        │
│     ├─ Check dependencies satisfied                           │
│     ├─ Record START event                                     │
│     ├─ Execute directly (Read/Edit/Write/Grep/Glob/Bash)      │
│     ├─ Verify convergence.criteria[]                          │
│     ├─ Run convergence.verification command                   │
│     ├─ Record COMPLETE/FAIL event with verification results   │
│     ├─ Update _execution state in task JSON file               │
│     └─ Auto-commit if enabled                                 │
│                                                               │
│  Phase 4: Completion                                          │
│     ├─ Finalize execution.md with summary statistics          │
│     ├─ Finalize execution-events.md with session footer       │
│     ├─ Write back .task/*.json with _execution states          │
│     └─ Offer follow-up actions                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Output Structure

```
${projectRoot}/.workflow/.execution/EXEC-{slug}-{date}-{random}/
├── execution.md              # Plan overview + task table + summary
└── execution-events.md       # ⭐ Unified event log (single source of truth)
```

Additionally, each source `.task/*.json` file is updated in-place with `_execution` states.

---

## Implementation Details

### Session Initialization

##### Step 0: Initialize Session

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()
const projectRoot = Bash(`git rev-parse --show-toplevel 2>/dev/null || pwd`).trim()

// Parse arguments
const autoCommit = $ARGUMENTS.includes('--auto-commit')
const dryRun = $ARGUMENTS.includes('--dry-run')
const planMatch = $ARGUMENTS.match(/PLAN="([^"]+)"/) || $ARGUMENTS.match(/PLAN=(\S+)/)
let planPath = planMatch ? planMatch[1] : null

// Auto-detect if no PLAN specified
if (!planPath) {
  // Search in order (most recent first):
  //   .workflow/active/*/.task/
  //   .workflow/.lite-plan/*/.task/
  //   .workflow/.req-plan/*/.task/
  //   .workflow/.planning/*/.task/
  // Use most recently modified directory containing *.json files
}

// Resolve path
planPath = path.isAbsolute(planPath) ? planPath : `${projectRoot}/${planPath}`

// Generate session ID
const slug = path.basename(path.dirname(planPath)).toLowerCase().substring(0, 30)
const dateStr = getUtc8ISOString().substring(0, 10)
const random = Math.random().toString(36).substring(2, 9)
const sessionId = `EXEC-${slug}-${dateStr}-${random}`
const sessionFolder = `${projectRoot}/.workflow/.execution/${sessionId}`

Bash(`mkdir -p ${sessionFolder}`)
```

---

## Phase 1: Load & Validate

**Objective**: Scan `.task/` directory, parse individual task JSON files, validate schema and dependencies, build execution order.

### Step 1.1: Scan .task/ Directory and Parse Task Files

```javascript
// Determine if planPath is a directory or single file
const isDirectory = planPath.endsWith('/') || Bash(`test -d "${planPath}" && echo dir || echo file`).trim() === 'dir'

let taskFiles, tasks

if (isDirectory) {
  // Directory mode: scan for all *.json files
  taskFiles = Glob('*.json', planPath)
  if (taskFiles.length === 0) throw new Error(`No .json files found in ${planPath}`)

  tasks = taskFiles.map(filePath => {
    try {
      const content = Read(filePath)
      const task = JSON.parse(content)
      task._source_file = filePath  // Track source file for write-back
      return task
    } catch (e) {
      throw new Error(`${path.basename(filePath)}: Invalid JSON - ${e.message}`)
    }
  })
} else {
  // Single file mode: parse one task JSON
  try {
    const content = Read(planPath)
    const task = JSON.parse(content)
    task._source_file = planPath
    tasks = [task]
  } catch (e) {
    throw new Error(`${path.basename(planPath)}: Invalid JSON - ${e.message}`)
  }
}

if (tasks.length === 0) throw new Error('No tasks found')
```

### Step 1.2: Validate Schema

Validate against unified task schema: `~/.ccw/workflows/cli-templates/schemas/task-schema.json`

```javascript
const errors = []
tasks.forEach((task, i) => {
  const src = task._source_file ? path.basename(task._source_file) : `Task ${i + 1}`

  // Required fields (per task-schema.json)
  if (!task.id) errors.push(`${src}: missing 'id'`)
  if (!task.title) errors.push(`${src}: missing 'title'`)
  if (!task.description) errors.push(`${src}: missing 'description'`)
  if (!Array.isArray(task.depends_on)) errors.push(`${task.id || src}: missing 'depends_on' array`)

  // Context block (optional but validated if present)
  if (task.context) {
    if (task.context.requirements && !Array.isArray(task.context.requirements))
      errors.push(`${task.id}: context.requirements must be array`)
    if (task.context.acceptance && !Array.isArray(task.context.acceptance))
      errors.push(`${task.id}: context.acceptance must be array`)
    if (task.context.focus_paths && !Array.isArray(task.context.focus_paths))
      errors.push(`${task.id}: context.focus_paths must be array`)
  }

  // Convergence (required for execution verification)
  if (!task.convergence) {
    errors.push(`${task.id || src}: missing 'convergence'`)
  } else {
    if (!task.convergence.criteria?.length) errors.push(`${task.id}: empty convergence.criteria`)
    if (!task.convergence.verification) errors.push(`${task.id}: missing convergence.verification`)
    if (!task.convergence.definition_of_done) errors.push(`${task.id}: missing convergence.definition_of_done`)
  }

  // Flow control (optional but validated if present)
  if (task.flow_control) {
    if (task.flow_control.target_files && !Array.isArray(task.flow_control.target_files))
      errors.push(`${task.id}: flow_control.target_files must be array`)
  }

  // New unified schema fields (backward compatible addition)
  if (task.focus_paths && !Array.isArray(task.focus_paths))
    errors.push(`${task.id}: focus_paths must be array`)
  if (task.implementation && !Array.isArray(task.implementation))
    errors.push(`${task.id}: implementation must be array`)
  if (task.files && !Array.isArray(task.files))
    errors.push(`${task.id}: files must be array`)
})

if (errors.length) {
  // Report errors, stop execution
}
```

### Step 1.3: Build Execution Order

```javascript
// 1. Validate dependency references
const taskIds = new Set(tasks.map(t => t.id))
tasks.forEach(task => {
  task.depends_on.forEach(dep => {
    if (!taskIds.has(dep)) errors.push(`${task.id}: depends on unknown task '${dep}'`)
  })
})

// 2. Detect cycles (DFS)
function detectCycles(tasks) {
  const graph = new Map(tasks.map(t => [t.id, t.depends_on || []]))
  const visited = new Set(), inStack = new Set(), cycles = []
  function dfs(node, path) {
    if (inStack.has(node)) { cycles.push([...path, node].join(' → ')); return }
    if (visited.has(node)) return
    visited.add(node); inStack.add(node)
    ;(graph.get(node) || []).forEach(dep => dfs(dep, [...path, node]))
    inStack.delete(node)
  }
  tasks.forEach(t => { if (!visited.has(t.id)) dfs(t.id, []) })
  return cycles
}
const cycles = detectCycles(tasks)
if (cycles.length) errors.push(`Circular dependencies: ${cycles.join('; ')}`)

// 3. Topological sort
function topoSort(tasks) {
  const inDegree = new Map(tasks.map(t => [t.id, 0]))
  tasks.forEach(t => t.depends_on.forEach(dep => {
    inDegree.set(t.id, (inDegree.get(t.id) || 0) + 1)
  }))
  const queue = tasks.filter(t => inDegree.get(t.id) === 0).map(t => t.id)
  const order = []
  while (queue.length) {
    const id = queue.shift()
    order.push(id)
    tasks.forEach(t => {
      if (t.depends_on.includes(id)) {
        inDegree.set(t.id, inDegree.get(t.id) - 1)
        if (inDegree.get(t.id) === 0) queue.push(t.id)
      }
    })
  }
  return order
}
const executionOrder = topoSort(tasks)
```

### Step 1.4: Initialize Execution Artifacts

```javascript
// execution.md
const executionMd = `# Execution Overview

## Session Info
- **Session ID**: ${sessionId}
- **Plan Source**: ${planPath}
- **Started**: ${getUtc8ISOString()}
- **Total Tasks**: ${tasks.length}
- **Mode**: ${dryRun ? 'Dry-run (no changes)' : 'Direct inline execution'}
- **Auto-Commit**: ${autoCommit ? 'Enabled' : 'Disabled'}

## Task Overview

| # | ID | Title | Type | Priority | Effort | Dependencies | Status |
|---|-----|-------|------|----------|--------|--------------|--------|
${tasks.map((t, i) => `| ${i+1} | ${t.id} | ${t.title} | ${t.type || '-'} | ${t.priority || '-'} | ${t.effort || '-'} | ${t.depends_on.join(', ') || '-'} | pending |`).join('\n')}

## Pre-Execution Analysis
> Populated in Phase 2

## Execution Timeline
> Updated as tasks complete

## Execution Summary
> Updated after all tasks complete
`
Write(`${sessionFolder}/execution.md`, executionMd)

// execution-events.md
Write(`${sessionFolder}/execution-events.md`, `# Execution Events

**Session**: ${sessionId}
**Started**: ${getUtc8ISOString()}
**Source**: ${planPath}

---

`)
```

---

## Phase 2: Pre-Execution Analysis

**Objective**: Validate feasibility and identify issues before execution.

### Step 2.1: Analyze File Conflicts

```javascript
const fileTaskMap = new Map()  // file → [taskIds]
tasks.forEach(task => {
  (task.files || []).forEach(f => {
    const key = f.path
    if (!fileTaskMap.has(key)) fileTaskMap.set(key, [])
    fileTaskMap.get(key).push(task.id)
  })
})

const conflicts = []
fileTaskMap.forEach((taskIds, file) => {
  if (taskIds.length > 1) {
    conflicts.push({ file, tasks: taskIds, resolution: 'Execute in dependency order' })
  }
})

// Check file existence
const missingFiles = []
tasks.forEach(task => {
  (task.files || []).forEach(f => {
    if (f.action !== 'create' && !file_exists(f.path)) {
      missingFiles.push({ file: f.path, task: task.id })
    }
  })
})
```

### Step 2.2: Append to execution.md

```javascript
// Replace "Pre-Execution Analysis" section with:
// - File Conflicts (list or "No conflicts")
// - Missing Files (list or "All files exist")
// - Dependency Validation (errors or "No issues")
// - Execution Order (numbered list)
```

### Step 2.3: User Confirmation

```javascript
if (!dryRun) {
  AskUserQuestion({
    questions: [{
      question: `Execute ${tasks.length} tasks?\n\n${conflicts.length ? `⚠ ${conflicts.length} file conflicts\n` : ''}Execution order:\n${executionOrder.map((id, i) => `  ${i+1}. ${id}: ${tasks.find(t => t.id === id).title}`).join('\n')}`,
      header: "Confirm",
      multiSelect: false,
      options: [
        { label: "Execute", description: "Start serial execution" },
        { label: "Dry Run", description: "Simulate without changes" },
        { label: "Cancel", description: "Abort execution" }
      ]
    }]
  })
}
```

---

## Phase 3: Serial Execution + Convergence Verification

**Objective**: Execute tasks sequentially, verify convergence after each task, track all state.

**Execution Model**: Direct inline execution — main process reads, edits, writes files directly. No CLI delegation.

### Step 3.1: Execution Loop

```javascript
const completedTasks = new Set()
const failedTasks = new Set()
const skippedTasks = new Set()

for (const taskId of executionOrder) {
  const task = tasks.find(t => t.id === taskId)
  const startTime = getUtc8ISOString()

  // 1. Check dependencies
  const unmetDeps = task.depends_on.filter(dep => !completedTasks.has(dep))
  if (unmetDeps.length) {
    appendToEvents(task, 'BLOCKED', `Unmet dependencies: ${unmetDeps.join(', ')}`)
    skippedTasks.add(task.id)
    task._execution = { status: 'skipped', executed_at: startTime,
      result: { success: false, error: `Blocked by: ${unmetDeps.join(', ')}` } }
    continue
  }

  // 2. Record START event
  appendToEvents(`## ${getUtc8ISOString()} — ${task.id}: ${task.title}

**Type**: ${task.type || '-'} | **Priority**: ${task.priority || '-'} | **Effort**: ${task.effort || '-'}
**Status**: ⏳ IN PROGRESS
**Files**: ${(task.files || []).map(f => f.path).join(', ') || 'To be determined'}
**Description**: ${task.description}
**Convergence Criteria**:
${task.convergence.criteria.map(c => `- [ ] ${c}`).join('\n')}

### Execution Log
`)

  if (dryRun) {
    // Simulate: mark as completed without changes
    appendToEvents(`\n**Status**: ⏭ DRY RUN (no changes)\n\n---\n`)
    task._execution = { status: 'completed', executed_at: startTime,
      result: { success: true, summary: 'Dry run — no changes made' } }
    completedTasks.add(task.id)
    continue
  }

  // 3. Execute task directly
  //    - Read each file in task.files (if specified)
  //    - Analyze what changes satisfy task.description + task.convergence.criteria
  //    - If task.files has detailed changes, use them as guidance
  //    - Apply changes using Edit (preferred) or Write (for new files)
  //    - Use Grep/Glob/mcp__ace-tool for discovery if needed
  //    - Use Bash for build/test commands

  // Dual-path field access (supports both unified and legacy 6-field schema)
  // const targetFiles = task.files?.map(f => f.path) || task.flow_control?.target_files || []
  // const acceptanceCriteria = task.convergence?.criteria || task.context?.acceptance || []
  // const requirements = task.implementation || task.context?.requirements || []
  // const focusPaths = task.focus_paths || task.context?.focus_paths || []

  // 4. Verify convergence
  const convergenceResults = verifyConvergence(task)

  const endTime = getUtc8ISOString()
  const filesModified = getModifiedFiles()

  if (convergenceResults.allPassed) {
    // 5a. Record SUCCESS
    appendToEvents(`
**Status**: ✅ COMPLETED
**Duration**: ${calculateDuration(startTime, endTime)}
**Files Modified**: ${filesModified.join(', ')}

#### Changes Summary
${changeSummary}

#### Convergence Verification
${task.convergence.criteria.map((c, i) => `- [${convergenceResults.verified[i] ? 'x' : ' '}] ${c}`).join('\n')}
- **Verification**: ${convergenceResults.verificationOutput}
- **Definition of Done**: ${task.convergence.definition_of_done}

---
`)
    task._execution = {
      status: 'completed', executed_at: endTime,
      result: {
        success: true,
        files_modified: filesModified,
        summary: changeSummary,
        convergence_verified: convergenceResults.verified
      }
    }
    completedTasks.add(task.id)
  } else {
    // 5b. Record FAILURE
    handleTaskFailure(task, convergenceResults, startTime, endTime)
  }

  // 6. Auto-commit if enabled
  if (autoCommit && task._execution.status === 'completed') {
    autoCommitTask(task, filesModified)
  }
}
```

### Step 3.2: Convergence Verification

```javascript
function verifyConvergence(task) {
  const results = {
    verified: [],           // boolean[] per criterion
    verificationOutput: '', // output of verification command
    allPassed: true
  }

  // 1. Check each criterion
  //    For each criterion in task.convergence.criteria:
  //      - If it references a testable condition, check it
  //      - If it's manual, mark as verified based on changes made
  //      - Record true/false per criterion
  task.convergence.criteria.forEach(criterion => {
    const passed = evaluateCriterion(criterion, task)
    results.verified.push(passed)
    if (!passed) results.allPassed = false
  })

  // 2. Run verification command (if executable)
  const verification = task.convergence.verification
  if (isExecutableCommand(verification)) {
    try {
      const output = Bash(verification, { timeout: 120000 })
      results.verificationOutput = `${verification} → PASS`
    } catch (e) {
      results.verificationOutput = `${verification} → FAIL: ${e.message}`
      results.allPassed = false
    }
  } else {
    results.verificationOutput = `Manual: ${verification}`
  }

  return results
}

function isExecutableCommand(verification) {
  // Detect executable patterns: npm, npx, jest, tsc, curl, pytest, go test, etc.
  return /^(npm|npx|jest|tsc|eslint|pytest|go\s+test|cargo\s+test|curl|make)/.test(verification.trim())
}
```

### Step 3.3: Failure Handling

```javascript
function handleTaskFailure(task, convergenceResults, startTime, endTime) {
  appendToEvents(`
**Status**: ❌ FAILED
**Duration**: ${calculateDuration(startTime, endTime)}
**Error**: Convergence verification failed

#### Failed Criteria
${task.convergence.criteria.map((c, i) => `- [${convergenceResults.verified[i] ? 'x' : ' '}] ${c}`).join('\n')}
- **Verification**: ${convergenceResults.verificationOutput}

---
`)

  task._execution = {
    status: 'failed', executed_at: endTime,
    result: {
      success: false,
      error: 'Convergence verification failed',
      convergence_verified: convergenceResults.verified
    }
  }
  failedTasks.add(task.id)

  // Ask user
  AskUserQuestion({
    questions: [{
      question: `Task ${task.id} failed convergence verification. How to proceed?`,
      header: "Failure",
      multiSelect: false,
      options: [
        { label: "Skip & Continue", description: "Skip this task, continue with next" },
        { label: "Retry", description: "Retry this task" },
        { label: "Accept", description: "Mark as completed despite failure" },
        { label: "Abort", description: "Stop execution, keep progress" }
      ]
    }]
  })
}
```

### Step 3.4: Auto-Commit

```javascript
function autoCommitTask(task, filesModified) {
  Bash(`git add ${filesModified.join(' ')}`)

  const commitType = {
    fix: 'fix', refactor: 'refactor', feature: 'feat',
    enhancement: 'feat', testing: 'test', infrastructure: 'chore'
  }[task.type] || 'chore'

  const scope = inferScope(filesModified)

  Bash(`git commit -m "$(cat <<'EOF'
${commitType}(${scope}): ${task.title}

Task: ${task.id}
Source: ${path.basename(planPath)}
EOF
)"`)

  appendToEvents(`**Commit**: \`${commitType}(${scope}): ${task.title}\`\n`)
}
```

---

## Phase 4: Completion

**Objective**: Finalize all artifacts, write back execution state, offer follow-up actions.

### Step 4.1: Finalize execution.md

Append summary statistics to execution.md:

```javascript
const summary = `
## Execution Summary

- **Completed**: ${getUtc8ISOString()}
- **Total Tasks**: ${tasks.length}
- **Succeeded**: ${completedTasks.size}
- **Failed**: ${failedTasks.size}
- **Skipped**: ${skippedTasks.size}
- **Success Rate**: ${Math.round(completedTasks.size / tasks.length * 100)}%

### Task Results

| ID | Title | Status | Convergence | Files Modified |
|----|-------|--------|-------------|----------------|
${tasks.map(t => {
  const ex = t._execution || {}
  const convergenceStatus = ex.result?.convergence_verified
    ? `${ex.result.convergence_verified.filter(v => v).length}/${ex.result.convergence_verified.length}`
    : '-'
  return `| ${t.id} | ${t.title} | ${ex.status || 'pending'} | ${convergenceStatus} | ${(ex.result?.files_modified || []).join(', ') || '-'} |`
}).join('\n')}

${failedTasks.size > 0 ? `### Failed Tasks

${[...failedTasks].map(id => {
  const t = tasks.find(t => t.id === id)
  return `- **${t.id}**: ${t.title} — ${t._execution?.result?.error || 'Unknown'}`
}).join('\n')}
` : ''}
### Artifacts
- **Plan Source**: ${planPath}
- **Execution Overview**: ${sessionFolder}/execution.md
- **Execution Events**: ${sessionFolder}/execution-events.md
`
// Append to execution.md
```

### Step 4.2: Finalize execution-events.md

```javascript
appendToEvents(`
---

# Session Summary

- **Session**: ${sessionId}
- **Completed**: ${getUtc8ISOString()}
- **Tasks**: ${completedTasks.size} completed, ${failedTasks.size} failed, ${skippedTasks.size} skipped
- **Total Events**: ${completedTasks.size + failedTasks.size + skippedTasks.size}
`)
```

### Step 4.3: Write Back .task/*.json with _execution

Update each source task JSON file with execution states:

```javascript
tasks.forEach(task => {
  const filePath = task._source_file
  if (!filePath) return

  // Read current file to preserve formatting and non-execution fields
  const current = JSON.parse(Read(filePath))

  // Update _execution status and result
  current._execution = {
    status: task._execution?.status || 'pending',
    executed_at: task._execution?.executed_at || null,
    result: task._execution?.result || null
  }

  // Write back individual task file
  Write(filePath, JSON.stringify(current, null, 2))
})
// Each task JSON file now has _execution: { status, executed_at, result }
```

### Step 4.4: Post-Completion Options

```javascript
AskUserQuestion({
  questions: [{
    question: `Execution complete: ${completedTasks.size}/${tasks.length} succeeded (${Math.round(completedTasks.size / tasks.length * 100)}%).\nNext step:`,
    header: "Post-Execute",
    multiSelect: false,
    options: [
      { label: "Retry Failed", description: `Re-execute ${failedTasks.size} failed tasks` },
      { label: "View Events", description: "Display execution-events.md" },
      { label: "Create Issue", description: "Create issue from failed tasks" },
      { label: "Done", description: "End workflow" }
    ]
  }]
})
```

| Selection | Action |
|-----------|--------|
| Retry Failed | Filter tasks with `_execution.status === 'failed'`, re-execute, append `[RETRY]` events |
| View Events | Display execution-events.md content |
| Create Issue | `Skill(skill="issue:new", args="...")` from failed task details |
| Done | Display artifact paths, end workflow |

---

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `PLAN="..."` | auto-detect | Path to `.task/` directory or single task `.json` file |
| `--auto-commit` | false | Commit changes after each successful task |
| `--dry-run` | false | Simulate execution without making changes |

### Plan Auto-Detection Order

When no `PLAN` specified, search for `.task/` directories in order (most recent first):

1. `.workflow/active/*/.task/`
2. `.workflow/.lite-plan/*/.task/`
3. `.workflow/.req-plan/*/.task/`
4. `.workflow/.planning/*/.task/`

**If source is not `.task/*.json`**: Run `plan-converter` first to generate `.task/` directory.

---

## Error Handling & Recovery

| Situation | Action | Recovery |
|-----------|--------|----------|
| .task/ directory not found | Report error with path | Check path, run plan-converter |
| Invalid JSON in task file | Report filename and error | Fix task JSON file manually |
| Missing convergence | Report validation error | Run plan-converter to add convergence |
| Circular dependency | Stop, report cycle path | Fix dependencies in task JSON |
| Task execution fails | Record in events, ask user | Retry, skip, accept, or abort |
| Convergence verification fails | Mark task failed, ask user | Fix code and retry, or accept |
| Verification command timeout | Mark as unverified | Manual verification needed |
| File conflict during execution | Document in events | Resolve in dependency order |
| All tasks fail | Report, suggest plan review | Re-analyze or manual intervention |

---

## Best Practices

### Before Execution

1. **Validate Plan**: Use `--dry-run` first to check plan feasibility
2. **Check Convergence**: Ensure all tasks have meaningful convergence criteria
3. **Review Dependencies**: Verify execution order makes sense
4. **Backup**: Commit pending changes before starting
5. **Convert First**: Use `plan-converter` for non-.task/ sources

### During Execution

1. **Monitor Events**: Check execution-events.md for real-time progress
2. **Handle Failures**: Review convergence failures carefully before deciding
3. **Check Commits**: Verify auto-commits are correct if enabled

### After Execution

1. **Review Summary**: Check execution.md statistics and failed tasks
2. **Verify Changes**: Inspect modified files match expectations
3. **Check Task Files**: Review `_execution` states in `.task/*.json` files
4. **Next Steps**: Use completion options for follow-up

---

**Now execute unified-execute-with-file for**: $PLAN
