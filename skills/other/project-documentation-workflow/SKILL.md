---
name: project-documentation-workflow
description: Wave-based comprehensive project documentation generator with dynamic task decomposition. Analyzes project structure and generates appropriate documentation tasks, computes optimal execution waves via topological sort, produces complete documentation suite including architecture, methods, theory, features, usage, and design philosophy.
argument-hint: "[-y|--yes] [-c|--concurrency N] [--continue] \"project path or description\""
allowed-tools: spawn_agents_on_csv, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm task decomposition, skip interactive validation, use defaults.

# Project Documentation Workflow (Optimized)

## Usage

```bash
$project-documentation-workflow "Document the authentication module in src/auth/"
$project-documentation-workflow -c 4 "Generate full docs for the FEM solver project"
$project-documentation-workflow -y "Document entire codebase with architecture and API"
$project-documentation-workflow --continue "doc-auth-module-20260304"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --concurrency N`: Max concurrent agents within each wave (default: 3)
- `--continue`: Resume existing session

**Output Directory**: `.workflow/.csv-wave/{session-id}/`
**Core Output**: `tasks.csv` + `results.csv` + `discoveries.ndjson` + `wave-summaries/` + `docs/` (完整文档集)

---

## Overview

**优化版**：动态任务分解 + 拓扑排序波次计算 + 波次间综合步骤。

```
┌─────────────────────────────────────────────────────────────────────────┐
│         PROJECT DOCUMENTATION WORKFLOW (Dynamic & Optimized)            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 0: Dynamic Decomposition                                          │
│     ├─ Analyze project structure, complexity, domain                     │
│     ├─ Generate appropriate documentation tasks (动态数量)                │
│     ├─ Compute task dependencies (deps)                                  │
│     ├─ Compute execution waves (topological sort)                        │
│     └─ User validates task breakdown (skip if -y)                        │
│                                                                          │
│  Phase 1: Wave Execution (with Inter-Wave Synthesis)                     │
│     ├─ For each wave (1..N, dynamically computed):                       │
│     │   ├─ Load Wave Summary from previous wave                          │
│     │   ├─ Build wave CSV with prev_context injection                    │
│     │   ├─ spawn_agents_on_csv(wave CSV)                                 │
│     │   ├─ Collect results, merge into master tasks.csv                  │
│     │   ├─ Generate Wave Summary (波次综合)                               │
│     │   └─ Check: any failed? → skip dependents                          │
│     └─ discoveries.ndjson shared across all waves                        │
│                                                                          │
│  Phase 2: Results Aggregation                                            │
│     ├─ Export final results.csv                                          │
│     ├─ Generate context.md with all findings                             │
│     ├─ Generate docs/index.md navigation                                 │
│     └─ Display summary: completed/failed/skipped per wave                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## CSV Schema

### tasks.csv (Master State)

```csv
id,title,description,doc_type,target_scope,doc_sections,formula_support,priority,deps,context_from,wave,status,findings,doc_path,key_discoveries,error
"doc-001","项目概述","撰写项目的整体概述","overview","README.md,package.json","purpose,background,positioning,audience","false","high","","","1","pending","","","",""
```

**Columns**:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `id` | string | Yes | Task ID (doc-NNN, auto-generated) |
| `title` | string | Yes | Document title |
| `description` | string | Yes | Detailed task description |
| `doc_type` | enum | Yes | `overview|architecture|theory|implementation|feature|api|usage|synthesis` |
| `target_scope` | string | Yes | File scope (glob pattern) |
| `doc_sections` | string | Yes | Required sections (comma-separated) |
| `formula_support` | boolean | No | LaTeX formula support |
| `priority` | enum | No | `high|medium|low` (for task ordering) |
| `deps` | string | No | Dependency task IDs (semicolon-separated) |
| `context_from` | string | No | Context source task IDs |
| `wave` | integer | Computed | Wave number (computed by topological sort) |
| `status` | enum | Output | `pending→completed|failed|skipped` |
| `findings` | string | Output | Key findings summary |
| `doc_path` | string | Output | Generated document path |
| `key_discoveries` | string | Output | Key discoveries (JSON) |
| `error` | string | Output | Error message |

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
const sessionId = `doc-${slug}-${dateStr}`
const sessionFolder = `.workflow/.csv-wave/${sessionId}`

Bash(`mkdir -p ${sessionFolder}/docs ${sessionFolder}/wave-summaries`)

// Initialize discoveries.ndjson
Write(`${sessionFolder}/discoveries.ndjson`, `# Discovery Board - ${sessionId}\n# Format: NDJSON\n`)
```

---

### Phase 0: Dynamic Task Decomposition

**Objective**: Analyze the project and dynamically generate appropriate documentation tasks.

#### Step 1: Project Analysis

```javascript
Bash({
  command: `ccw cli -p "PURPOSE: Analyze the project and determine appropriate documentation tasks.
TASK:
  1. Scan project structure to identify:
     - Project type (library/application/service/CLI/tool)
     - Primary language(s) and frameworks
     - Project scale (small/medium/large based on file count and complexity)
     - Key modules and their purposes
     - Existing documentation (README, docs/, etc.)
  
  2. Determine documentation needs based on project characteristics:
     - For ALL projects: overview, tech-stack, directory-structure
     - For libraries: api-reference, usage-guide, best-practices
     - For applications: system-architecture, feature-list, usage-guide
     - For numerical/scientific projects: theoretical-foundations (with formula_support=true)
     - For services: api-reference, module-interactions, deployment
     - For complex projects (>50 files): add design-patterns, data-model
     - For simple projects (<10 files): reduce to essential docs only
  
  3. Generate task list with:
     - Unique task IDs (doc-001, doc-002, ...)
     - Appropriate doc_type for each task
     - Target scope (glob patterns) based on actual project structure
     - Required sections for each document type
     - Dependencies (deps) between related tasks
     - Context sources (context_from) for information flow
     - Priority (high for essential docs, medium for useful, low for optional)
  
  4. Task dependency rules:
     - overview tasks: no deps (Wave 1)
     - architecture tasks: depend on overview tasks
     - implementation tasks: depend on architecture tasks
     - feature/api tasks: depend on implementation
     - synthesis tasks: depend on most other tasks

MODE: analysis
CONTEXT: @**/*
EXPECTED: JSON with:
  - project_info: {type, scale, languages, frameworks, modules[]}
  - recommended_waves: number of waves suggested
  - tasks: [{id, title, description, doc_type, target_scope, doc_sections, formula_support, priority, deps[], context_from[]}]
  
CONSTRAINTS: 
  - Small projects: 5-8 tasks max
  - Medium projects: 10-15 tasks
  - Large projects: 15-25 tasks
  - Each doc_type should appear at most once unless justified
  - deps must form a valid DAG (no cycles)

PROJECT TO ANALYZE: ${requirement}" --tool gemini --mode analysis --rule planning-breakdown-task-steps`,
  run_in_background: true
})
```

#### Step 2: Topological Sort (Wave Computation)

```javascript
function computeWaves(tasks) {
  // Build adjacency list
  const graph = new Map()
  const inDegree = new Map()
  const taskMap = new Map()
  
  for (const task of tasks) {
    taskMap.set(task.id, task)
    graph.set(task.id, [])
    inDegree.set(task.id, 0)
  }
  
  // Fill edges based on deps
  for (const task of tasks) {
    const deps = task.deps.filter(d => taskMap.has(d))
    for (const dep of deps) {
      graph.get(dep).push(task.id)
      inDegree.set(task.id, inDegree.get(task.id) + 1)
    }
  }
  
  // Kahn's BFS algorithm
  const waves = []
  let currentWave = []
  
  // Start with tasks that have no dependencies
  for (const [id, degree] of inDegree) {
    if (degree === 0) currentWave.push(id)
  }
  
  while (currentWave.length > 0) {
    waves.push([...currentWave])
    const nextWave = []
    
    for (const id of currentWave) {
      for (const neighbor of graph.get(id)) {
        inDegree.set(neighbor, inDegree.get(neighbor) - 1)
        if (inDegree.get(neighbor) === 0) {
          nextWave.push(neighbor)
        }
      }
    }
    
    currentWave = nextWave
  }
  
  // Assign wave numbers
  for (let w = 0; w < waves.length; w++) {
    for (const id of waves[w]) {
      taskMap.get(id).wave = w + 1
    }
  }
  
  // Check for cycles
  const assignedCount = tasks.filter(t => t.wave > 0).length
  if (assignedCount < tasks.length) {
    throw new Error(`Circular dependency detected! Only ${assignedCount}/${tasks.length} tasks assigned.`)
  }
  
  return {
    tasks: tasks,
    waveCount: waves.length,
    waveDistribution: waves.map((w, i) => ({ wave: i + 1, tasks: w.length }))
  }
}
```

#### Step 3: User Validation

```javascript
// Parse decomposition result
const analysisResult = JSON.parse(decompositionOutput)
const { tasks, project_info, waveCount } = analysisResult

// Compute waves
const { tasks: tasksWithWaves, waveCount: computedWaves, waveDistribution } = computeWaves(tasks)

// Display to user (skip if AUTO_YES)
if (!AUTO_YES) {
  console.log(`
╔════════════════════════════════════════════════════════════════╗
║                  PROJECT ANALYSIS RESULT                        ║
╠════════════════════════════════════════════════════════════════╣
║ Type: ${project_info.type.padEnd(20)} Scale: ${project_info.scale.padEnd(10)}        ║
║ Languages: ${project_info.languages.join(', ').substring(0, 40).padEnd(40)} ║
║ Modules: ${project_info.modules.length} identified                                              ║
╠════════════════════════════════════════════════════════════════╣
║ WAVE DISTRIBUTION (${computedWaves} waves, ${tasksWithWaves.length} tasks)               ║
${waveDistribution.map(w => `║   Wave ${w.wave}: ${w.tasks} tasks${' '.repeat(50 - w.tasks.toString().length)}`).join('\n')}
╚════════════════════════════════════════════════════════════════╝
  `)
  
  // Show tasks by wave
  for (let w = 1; w <= computedWaves; w++) {
    const waveTasks = tasksWithWaves.filter(t => t.wave === w)
    console.log(`\nWave ${w}:`)
    for (const t of waveTasks) {
      console.log(`  ${t.id}: ${t.title} [${t.doc_type}]`)
    }
  }
  
  const confirm = AskUserQuestion("Proceed with this task breakdown?")
  if (!confirm) {
    console.log("Aborted. Use --continue to resume with modified tasks.")
    return
  }
}

// Generate tasks.csv
Write(`${sessionFolder}/tasks.csv`, toCsv(tasksWithWaves))
Write(`${sessionFolder}/project-info.json`, JSON.stringify(project_info, null, 2))
```

---

### Phase 1: Wave Execution (with Inter-Wave Synthesis)

**Key Optimization**: Add Wave Summary generation between waves for better context propagation.

```javascript
const masterCsv = Read(`${sessionFolder}/tasks.csv`)
let tasks = parseCsv(masterCsv)
const maxWave = Math.max(...tasks.map(t => t.wave))

for (let wave = 1; wave <= maxWave; wave++) {
  console.log(`\n{'='*60}`)
  console.log(`Wave ${wave}/${maxWave}`)
  console.log('='.repeat(60))
  
  // 1. Load Wave Summary from previous wave
  const waveSummaryPath = `${sessionFolder}/wave-summaries/wave-${wave-1}-summary.md`
  let prevWaveSummary = ''
  if (wave > 1 && fileExists(waveSummaryPath)) {
    prevWaveSummary = Read(waveSummaryPath)
    console.log(`Loaded Wave ${wave-1} Summary (${prevWaveSummary.length} chars)`)
  }
  
  // 2. Filter tasks for this wave
  const waveTasks = tasks.filter(t => t.wave === wave && t.status === 'pending')
  
  // 3. Check dependencies
  for (const task of waveTasks) {
    const depIds = (task.deps || '').split(';').filter(Boolean)
    const depStatuses = depIds.map(id => tasks.find(t => t.id === id)?.status)
    if (depStatuses.some(s => s === 'failed' || s === 'skipped')) {
      task.status = 'skipped'
      task.error = `Dependency failed: ${depIds.filter((id, i) => 
        ['failed','skipped'].includes(depStatuses[i])).join(', ')}`
    }
  }
  
  const pendingTasks = waveTasks.filter(t => t.status === 'pending')
  if (pendingTasks.length === 0) {
    console.log(`Wave ${wave}: No pending tasks, skipping...`)
    continue
  }
  
  // 4. Build enhanced prev_context
  for (const task of pendingTasks) {
    // a. From context_from tasks
    const contextIds = (task.context_from || '').split(';').filter(Boolean)
    const prevFindings = contextIds.map(id => {
      const src = tasks.find(t => t.id === id)
      if (!src?.findings) return ''
      return `## [${src.id}] ${src.title}\n${src.findings}`
    }).filter(Boolean).join('\n\n')
    
    // b. From previous wave summary (HIGH DENSITY CONTEXT)
    const waveContext = prevWaveSummary ? 
      `\n\n## Wave ${wave-1} Summary\n${prevWaveSummary}` : ''
    
    // c. From discoveries.ndjson (relevant entries)
    const discoveries = Read(`${sessionFolder}/discoveries.ndjson`)
    const relevantDiscoveries = discoveries
      .split('\n')
      .filter(line => line.startsWith('{'))
      .map(line => JSON.parse(line))
      .filter(d => isRelevantDiscovery(d, task))
      .slice(0, 10) // Limit to 10 most relevant
      .map(d => `- [${d.type}] ${JSON.stringify(d.data)}`)
      .join('\n')
    
    const discoveryContext = relevantDiscoveries ? 
      `\n\n## Relevant Discoveries\n${relevantDiscoveries}` : ''
    
    task.prev_context = prevFindings + waveContext + discoveryContext
  }
  
  // 5. Write wave CSV
  Write(`${sessionFolder}/wave-${wave}.csv`, toCsv(pendingTasks))
  
  // 6. Execute wave
  spawn_agents_on_csv({
    csv_path: `${sessionFolder}/wave-${wave}.csv`,
    id_column: "id",
    instruction: buildOptimizedInstruction(sessionFolder, wave),
    max_concurrency: maxConcurrency,
    max_runtime_seconds: 900,
    output_csv_path: `${sessionFolder}/wave-${wave}-results.csv`,
    output_schema: {
      type: "object",
      properties: {
        id: { type: "string" },
        status: { type: "string", enum: ["completed", "failed"] },
        findings: { type: "string" },
        doc_path: { type: "string" },
        key_discoveries: { type: "string" },
        error: { type: "string" }
      }
    }
  })
  
  // 7. Merge results
  const results = parseCsv(Read(`${sessionFolder}/wave-${wave}-results.csv`))
  for (const r of results) {
    const t = tasks.find(t => t.id === r.id)
    if (t) Object.assign(t, r)
  }
  Write(`${sessionFolder}/tasks.csv`, toCsv(tasks))
  
  // 8. Generate Wave Summary (NEW: Inter-Wave Synthesis)
  const completedThisWave = results.filter(r => r.status === 'completed')
  if (completedThisWave.length > 0) {
    const waveSummary = generateWaveSummary(wave, completedThisWave, tasks)
    Write(`${sessionFolder}/wave-summaries/wave-${wave}-summary.md`, waveSummary)
    console.log(`Generated Wave ${wave} Summary`)
  }
  
  // 9. Cleanup temp files
  Bash(`rm -f ${sessionFolder}/wave-${wave}.csv ${sessionFolder}/wave-${wave}-results.csv`)
  
  // 10. Display wave summary
  const completed = results.filter(r => r.status === 'completed').length
  const failed = results.filter(r => r.status === 'failed').length
  console.log(`Wave ${wave} Complete: ${completed} completed, ${failed} failed`)
}
```

---

### Wave Summary Generation (Inter-Wave Synthesis)

```javascript
function generateWaveSummary(waveNum, completedTasks, allTasks) {
  let summary = `# Wave ${waveNum} Summary\n\n`
  summary += `**Completed Tasks**: ${completedTasks.length}\n\n`
  
  // Group by doc_type
  const byType = {}
  for (const task of completedTasks) {
    const type = task.doc_type || 'unknown'
    if (!byType[type]) byType[type] = []
    byType[type].push(task)
  }
  
  for (const [type, tasks] of Object.entries(byType)) {
    summary += `## ${type.toUpperCase()}\n\n`
    for (const t of tasks) {
      summary += `### ${t.title}\n`
      if (t.findings) {
        summary += `${t.findings.substring(0, 300)}${t.findings.length > 300 ? '...' : ''}\n\n`
      }
      if (t.key_discoveries) {
        try {
          const discoveries = JSON.parse(t.key_discoveries)
          summary += `**Key Points**:\n`
          for (const d of discoveries.slice(0, 3)) {
            summary += `- ${d.name || d.type}: ${d.description || JSON.stringify(d).substring(0, 100)}\n`
          }
          summary += '\n'
        } catch (e) {}
      }
    }
  }
  
  // Add cross-references for next wave
  const nextWaveTasks = allTasks.filter(t => t.wave === waveNum + 1)
  if (nextWaveTasks.length > 0) {
    summary += `## Context for Wave ${waveNum + 1}\n\n`
    summary += `Next wave will focus on: ${nextWaveTasks.map(t => t.title).join(', ')}\n`
  }
  
  return summary
}

function isRelevantDiscovery(discovery, task) {
  // Check if discovery is relevant to the task
  const taskScope = task.target_scope || ''
  const taskType = task.doc_type || ''
  
  // Always include architecture discoveries for architecture tasks
  if (taskType === 'architecture' && discovery.type.includes('component')) return true
  if (taskType === 'implementation' && discovery.type.includes('algorithm')) return true
  if (taskType === 'api' && discovery.type.includes('api')) return true
  
  // Check file relevance
  if (discovery.data?.file) {
    return taskScope.includes(discovery.data.file.split('/')[0])
  }
  
  return false
}
```

---

### Optimized Instruction Template

```javascript
function buildOptimizedInstruction(sessionFolder, wave) {
  return `## DOCUMENTATION TASK — Wave ${wave}

### ⚠️ MANDATORY FIRST STEPS (DO NOT SKIP)

1. **CHECK DISCOVERIES FIRST** (避免重复工作):
   \`\`\`bash
   # Search for existing discoveries about your topic
   grep -i "{doc_type}" ${sessionFolder}/discoveries.ndjson
   grep -i "{target_keywords}" ${sessionFolder}/discoveries.ndjson
   \`\`\`
   
2. **Read Wave Summary** (高密度上下文):
   - Read: ${sessionFolder}/wave-summaries/wave-${wave-1}-summary.md (if exists)
   
3. **Read prev_context** (provided below)

---

## Your Task

**Task ID**: {id}
**Title**: {title}
**Document Type**: {doc_type}
**Target Scope**: {target_scope}
**Required Sections**: {doc_sections}
**LaTeX Support**: {formula_support}
**Priority**: {priority}

### Task Description
{description}

### Previous Context (USE THIS!)
{prev_context}

---

## Execution Protocol

### Step 1: Discovery Check (MANDATORY)
Before reading any source files:
- Search discoveries.ndjson for existing findings
- Note any pre-discovered components, patterns, algorithms
- Avoid re-documenting what's already found

### Step 2: Scope Analysis
- Read files matching \`{target_scope}\`
- Identify key structures, functions, classes
- Extract relevant code patterns

### Step 3: Context Integration
- Build on findings from prev_context
- Reference Wave Summary insights
- Connect to discoveries from other agents

### Step 4: Document Generation
**Output Path**: Determine based on doc_type:
- \`overview\` → \`docs/01-overview/\`
- \`architecture\` → \`docs/02-architecture/\`
- \`implementation\` → \`docs/03-implementation/\`
- \`feature\` → \`docs/04-features/\`
- \`api\` → \`docs/04-features/\`
- \`usage\` → \`docs/04-features/\`
- \`synthesis\` → \`docs/05-synthesis/\`

**Document Structure**:
\`\`\`markdown
# {Title}

## Overview
[Brief introduction]

## {Required Section 1}
[Content with code examples]

## {Required Section 2}
[Content with diagrams if applicable]

...

## Code Examples
\`\`\`{language}
// file:line references
\`\`\`

## Cross-References
- Related: [Doc](path)
- Depends: [Prereq](path)

## Summary
[Key takeaways]
\`\`\`

### Step 5: Share Discoveries (MANDATORY)
Append to discovery board:
\`\`\`bash
echo '{"ts":"${getUtc8ISOString()}","worker":"{id}","type":"<TYPE>","data":{...}}' >> ${sessionFolder}/discoveries.ndjson
\`\`\`

**Discovery Types**:
- \`component_found\`: {name, type, file, purpose}
- \`pattern_found\`: {pattern_name, location, description}
- \`algorithm_found\`: {name, file, complexity, purpose}
- \`formula_found\`: {name, latex, file, context}
- \`feature_found\`: {name, entry_point, description}
- \`api_found\`: {endpoint, file, parameters, returns}
- \`config_found\`: {name, file, type, default_value}

### Step 6: Report
\`\`\`json
{
  "id": "{id}",
  "status": "completed",
  "findings": "Key discoveries (max 500 chars, structured for context propagation)",
  "doc_path": "docs/XX-category/filename.md",
  "key_discoveries": "[{\"name\":\"...\",\"type\":\"...\",\"description\":\"...\",\"file\":\"...\"}]",
  "error": ""
}
\`\`\`

---

## Quality Requirements

| Requirement | Criteria |
|-------------|----------|
| Section Coverage | ALL sections in doc_sections present |
| Code References | Include file:line for code |
| Discovery Sharing | At least 2 discoveries shared |
| Context Usage | Reference prev_context findings |
| Cross-References | Link to related docs |
`
}
```

---

### Phase 2: Results Aggregation

```javascript
// 1. Generate docs/index.md
const tasks = parseCsv(Read(`${sessionFolder}/tasks.csv`))
const completed = tasks.filter(t => t.status === 'completed')

// Group by doc_type for navigation
const byType = {}
for (const t of completed) {
  const type = t.doc_type || 'other'
  if (!byType[type]) byType[type] = []
  byType[type].push(t)
}

let index = `# Project Documentation Index\n\n`
index += `**Generated**: ${getUtc8ISOString().substring(0, 10)}\n`
index += `**Total Documents**: ${completed.length}\n\n`

const typeLabels = {
  overview: '📋 概览',
  architecture: '🏗️ 架构',
  implementation: '⚙️ 实现',
  theory: '📐 理论',
  feature: '✨ 功能',
  api: '🔌 API',
  usage: '📖 使用',
  synthesis: '💡 综合'
}

for (const [type, typeTasks] of Object.entries(byType)) {
  const label = typeLabels[type] || type
  index += `## ${label}\n\n`
  for (const t of typeTasks) {
    index += `- [${t.title}](${t.doc_path})\n`
  }
  index += `\n`
}

// Add wave summaries reference
index += `## 📊 Execution Reports\n\n`
index += `- [Wave Summaries](wave-summaries/)\n`
index += `- [Full Context](../context.md)\n`

Write(`${sessionFolder}/docs/index.md`, index)

// 2. Export results.csv
Bash(`cp ${sessionFolder}/tasks.csv ${sessionFolder}/results.csv`)

// 3. Generate context.md
const projectInfo = JSON.parse(Read(`${sessionFolder}/project-info.json`))
let contextMd = `# Documentation Report\n\n`
contextMd += `**Session**: ${sessionId}\n`
contextMd += `**Date**: ${getUtc8ISOString().substring(0, 10)}\n\n`

contextMd += `## Project Info\n`
contextMd += `- **Type**: ${projectInfo.type}\n`
contextMd += `- **Scale**: ${projectInfo.scale}\n`
contextMd += `- **Languages**: ${projectInfo.languages?.join(', ') || 'N/A'}\n\n`

const statusCounts = {
  completed: tasks.filter(t => t.status === 'completed').length,
  failed: tasks.filter(t => t.status === 'failed').length,
  skipped: tasks.filter(t => t.status === 'skipped').length
}
contextMd += `## Summary\n`
contextMd += `| Status | Count |\n`
contextMd += `|--------|-------|\n`
contextMd += `| ✅ Completed | ${statusCounts.completed} |\n`
contextMd += `| ❌ Failed | ${statusCounts.failed} |\n`
contextMd += `| ⏭️ Skipped | ${statusCounts.skipped} |\n\n`

// Per-wave summary
const maxWave = Math.max(...tasks.map(t => t.wave))
contextMd += `## Wave Execution\n\n`
for (let w = 1; w <= maxWave; w++) {
  const waveTasks = tasks.filter(t => t.wave === w)
  contextMd += `### Wave ${w}\n\n`
  for (const t of waveTasks) {
    const icon = t.status === 'completed' ? '✅' : t.status === 'failed' ? '❌' : '⏭️'
    contextMd += `${icon} **${t.title}** [${t.doc_type}]\n`
    if (t.findings) {
      contextMd += `   ${t.findings.substring(0, 200)}${t.findings.length > 200 ? '...' : ''}\n`
    }
    if (t.doc_path) {
      contextMd += `   → [${t.doc_path}](${t.doc_path})\n`
    }
    contextMd += `\n`
  }
}

Write(`${sessionFolder}/context.md`, contextMd)

// 4. Display final summary
console.log(`
╔════════════════════════════════════════════════════════════════╗
║                  DOCUMENTATION COMPLETE                         ║
╠════════════════════════════════════════════════════════════════╣
║ ✅ Completed: ${statusCounts.completed.toString().padStart(2)} tasks                                    ║
║ ❌ Failed:    ${statusCounts.failed.toString().padStart(2)} tasks                                    ║
║ ⏭️ Skipped:   ${statusCounts.skipped.toString().padStart(2)} tasks                                    ║
╠════════════════════════════════════════════════════════════════╣
║ Output: ${sessionFolder.padEnd(50)} ║
╚════════════════════════════════════════════════════════════════╝
`)
```

---

## Optimized Output Structure

```
.workflow/.csv-wave/doc-{slug}-{date}/
├── project-info.json              # 项目分析结果
├── tasks.csv                      # Master CSV (动态生成的任务)
├── results.csv                    # 最终结果
├── discoveries.ndjson             # 发现板
├── context.md                     # 执行报告
│
├── wave-summaries/                # NEW: 波次摘要
│   ├── wave-1-summary.md
│   ├── wave-2-summary.md
│   └── ...
│
└── docs/
    ├── index.md                   # 文档导航
    ├── 01-overview/
    ├── 02-architecture/
    ├── 03-implementation/
    ├── 04-features/
    └── 05-synthesis/
```

---

## Optimization Summary

| 优化点 | 原版 | 优化版 |
|--------|------|--------|
| **任务数量** | 固定17任务 | 动态生成 (5-25基于项目规模) |
| **波次计算** | 硬编码5波 | 拓扑排序动态计算 |
| **上下文传播** | 仅 prev_context | prev_context + Wave Summary + Discoveries |
| **发现利用** | 依赖自觉 | 强制第一步检查 |
| **文档密度** | 原始 findings | 结构化 Wave Summary |

---

## Core Rules

1. **Dynamic First**: 任务列表动态生成，不预设
2. **Wave Order is Sacred**: 波次由拓扑排序决定
3. **Discovery Check Mandatory**: 必须先检查发现板
4. **Wave Summary**: 每波次结束生成摘要
5. **Context Compound**: 上下文累积传播
6. **Quality Gates**: 每文档必须覆盖所有 doc_sections
7. **DO NOT STOP**: 持续执行直到所有波次完成
