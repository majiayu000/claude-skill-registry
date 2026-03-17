---
name: collaborative-plan-with-file
description: Serial collaborative planning with Plan Note - Multi-domain serial task generation, unified plan-note.md, conflict detection. No agent delegation.
argument-hint: "[-y|--yes] <task description> [--max-domains=5]"
---

# Collaborative-Plan-With-File Workflow

## Quick Start

Serial collaborative planning workflow using **Plan Note** architecture. Analyzes requirements, identifies sub-domains, generates detailed plans per domain serially, and detects conflicts across domains.

```bash
# Basic usage
/codex:collaborative-plan-with-file "Implement real-time notification system"

# With options
/codex:collaborative-plan-with-file "Refactor authentication module" --max-domains=4
/codex:collaborative-plan-with-file "Add payment gateway support" -y
```

**Core workflow**: Understand → Template → Serial Domain Planning → Conflict Detection → Completion

**Key features**:
- **plan-note.md**: Shared collaborative document with pre-allocated sections per domain
- **Serial domain planning**: Each sub-domain planned sequentially with full codebase context
- **Conflict detection**: Automatic file, dependency, and strategy conflict scanning
- **No merge needed**: Pre-allocated sections eliminate merge conflicts

## Auto Mode

When `--yes` or `-y`: Auto-approve splits, skip confirmations.

## Overview

This workflow enables structured planning through sequential phases:

1. **Understanding & Template** — Analyze requirements, identify sub-domains, create plan-note.md template
2. **Serial Domain Planning** — Plan each sub-domain sequentially using direct search and analysis
3. **Conflict Detection** — Scan plan-note.md for conflicts across all domains
4. **Completion** — Generate human-readable plan.md summary

The key innovation is the **Plan Note** architecture — a shared collaborative document with pre-allocated sections per sub-domain, eliminating merge conflicts even in serial execution.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PLAN NOTE COLLABORATIVE PLANNING                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 1: Understanding & Template Creation                              │
│     ├─ Analyze requirements (inline search & analysis)                   │
│     ├─ Identify 2-5 sub-domains (focus areas)                            │
│     ├─ Create plan-note.md with pre-allocated sections                   │
│     └─ Assign TASK ID ranges (no conflicts)                              │
│                                                                          │
│  Phase 2: Serial Domain Planning                                         │
│     ┌──────────────┐                                                     │
│     │   Domain 1   │→ Explore codebase → Generate .task/TASK-*.json      │
│     │   Section 1  │→ Fill task pool + evidence in plan-note.md          │
│     └──────┬───────┘                                                     │
│     ┌──────▼───────┐                                                     │
│     │   Domain 2   │→ Explore codebase → Generate .task/TASK-*.json      │
│     │   Section 2  │→ Fill task pool + evidence in plan-note.md          │
│     └──────┬───────┘                                                     │
│     ┌──────▼───────┐                                                     │
│     │   Domain N   │→ ...                                                │
│     └──────────────┘                                                     │
│                                                                          │
│  Phase 3: Conflict Detection (Single Source)                             │
│     ├─ Parse plan-note.md (all sections)                                 │
│     ├─ Detect file/dependency/strategy conflicts                         │
│     └─ Update plan-note.md conflict section                              │
│                                                                          │
│  Phase 4: Completion (No Merge)                                          │
│     ├─ Collect domain .task/*.json → session .task/*.json                │
│     ├─ Generate plan.md (human-readable)                                 │
│     └─ Ready for execution                                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Output Structure

> **Schema**: `cat ~/.ccw/workflows/cli-templates/schemas/task-schema.json`

```
{projectRoot}/.workflow/.planning/CPLAN-{slug}-{date}/
├── plan-note.md                  # ⭐ Core: Requirements + Tasks + Conflicts
├── requirement-analysis.json     # Phase 1: Sub-domain assignments
├── domains/                      # Phase 2: Per-domain plans
│   ├── {domain-1}/
│   │   └── .task/                # Per-domain task JSON files
│   │       ├── TASK-001.json
│   │       └── ...
│   ├── {domain-2}/
│   │   └── .task/
│   │       ├── TASK-101.json
│   │       └── ...
│   └── ...
├── plan.json                     # Plan overview (plan-overview-base-schema.json)
├── .task/                        # ⭐ Merged task JSON files (all domains)
│   ├── TASK-001.json
│   ├── TASK-101.json
│   └── ...
├── conflicts.json                # Phase 3: Conflict report
└── plan.md                       # Phase 4: Human-readable summary
```

## Output Artifacts

### Phase 1: Understanding & Template

| Artifact | Purpose |
|----------|---------|
| `plan-note.md` | Collaborative template with pre-allocated task pool and evidence sections per domain |
| `requirement-analysis.json` | Sub-domain assignments, TASK ID ranges, complexity assessment |

### Phase 2: Serial Domain Planning

| Artifact | Purpose |
|----------|---------|
| `domains/{domain}/.task/TASK-*.json` | Task JSON files per domain (one file per task with convergence) |
| Updated `plan-note.md` | Task pool and evidence sections filled for each domain |

### Phase 3: Conflict Detection

| Artifact | Purpose |
|----------|---------|
| `conflicts.json` | Detected conflicts with types, severity, and resolutions |
| Updated `plan-note.md` | Conflict markers section populated |

### Phase 4: Completion

| Artifact | Purpose |
|----------|---------|
| `.task/TASK-*.json` | Merged task JSON files from all domains (consumable by unified-execute) |
| `plan.json` | Plan overview following plan-overview-base-schema.json |
| `plan.md` | Human-readable summary with requirements, tasks, and conflicts |

---

## Implementation Details

### Session Initialization

##### Step 0: Initialize Session

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Detect project root
const projectRoot = Bash(`git rev-parse --show-toplevel 2>/dev/null || pwd`).trim()

// Parse arguments
const autoMode = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const maxDomainsMatch = $ARGUMENTS.match(/--max-domains=(\d+)/)
const maxDomains = maxDomainsMatch ? parseInt(maxDomainsMatch[1]) : 5

// Clean task description
const taskDescription = $ARGUMENTS
  .replace(/--yes|-y|--max-domains=\d+/g, '')
  .trim()

const slug = taskDescription.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 30)
const dateStr = getUtc8ISOString().substring(0, 10)
const sessionId = `CPLAN-${slug}-${dateStr}`
const sessionFolder = `${projectRoot}/.workflow/.planning/${sessionId}`

// Auto-detect continue: session folder + plan-note.md exists → continue mode
// If continue → load existing state and resume from incomplete phase
Bash(`mkdir -p ${sessionFolder}/domains`)
```

**Session Variables**:
- `sessionId`: Unique session identifier
- `sessionFolder`: Base directory for all artifacts
- `maxDomains`: Maximum number of sub-domains (default: 5)
- `autoMode`: Boolean for auto-confirmation

**Auto-Detection**: If session folder exists with plan-note.md, automatically enters continue mode.

---

## Phase 1: Understanding & Template Creation

**Objective**: Analyze task requirements, identify parallelizable sub-domains, and create the plan-note.md template with pre-allocated sections.

### Step 1.1: Analyze Task Description

Use built-in tools directly to understand the task scope and identify sub-domains.

**Analysis Activities**:
1. **Search for references** — Find related documentation, README files, and architecture guides
   - Use: `mcp__ace-tool__search_context`, Grep, Glob, Read
   - Read: `.workflow/project-tech.json`, `.workflow/project-guidelines.json` (if exists)
2. **Extract task keywords** — Identify key terms and concepts from the task description
3. **Identify ambiguities** — List any unclear points or multiple possible interpretations
4. **Clarify with user** — If ambiguities found, use AskUserQuestion for clarification
5. **Identify sub-domains** — Split into 2-{maxDomains} parallelizable focus areas based on task complexity
6. **Assess complexity** — Evaluate overall task complexity (Low/Medium/High)

**Sub-Domain Identification Patterns**:

| Pattern | Keywords |
|---------|----------|
| Backend API | 服务, 后端, API, 接口 |
| Frontend | 界面, 前端, UI, 视图 |
| Database | 数据, 存储, 数据库, 持久化 |
| Testing | 测试, 验证, QA |
| Infrastructure | 部署, 基础, 运维, 配置 |

**Guideline**: Prioritize identifying latest documentation (README, design docs, architecture guides). When ambiguities exist, ask user for clarification instead of assuming interpretations.

### Step 1.2: Create plan-note.md Template

Generate a structured template with pre-allocated sections for each sub-domain.

**plan-note.md Structure**:

```yaml
---
session_id: CPLAN-{slug}-{date}
original_requirement: "{task description}"
created_at: "{ISO timestamp}"
complexity: Low | Medium | High
sub_domains: ["{domain-1}", "{domain-2}", ...]
domain_task_id_ranges:
  "{domain-1}": [1, 100]
  "{domain-2}": [101, 200]
status: planning
---
```

**Sections**:
- `## 需求理解` — Core objectives, key points, constraints, split strategy
- `## 任务池 - {Domain N}` — Pre-allocated task section per domain (TASK-{range})
- `## 依赖关系` — Auto-generated after all domains complete
- `## 冲突标记` — Populated in Phase 3
- `## 上下文证据 - {Domain N}` — Evidence section per domain

**TASK ID Range Allocation**: Each domain receives a non-overlapping range of 100 IDs (e.g., Domain 1: TASK-001~100, Domain 2: TASK-101~200).

### Step 1.3: Generate requirement-analysis.json

```javascript
Write(`${sessionFolder}/requirement-analysis.json`, JSON.stringify({
  session_id: sessionId,
  original_requirement: taskDescription,
  complexity: complexity,  // Low | Medium | High
  sub_domains: subDomains.map(sub => ({
    focus_area: sub.focus_area,
    description: sub.description,
    task_id_range: sub.task_id_range,
    estimated_effort: sub.estimated_effort,
    dependencies: sub.dependencies  // cross-domain dependencies
  })),
  total_domains: subDomains.length
}, null, 2))
```

**Success Criteria**:
- Latest documentation identified and referenced (if available)
- Ambiguities resolved via user clarification (if any found)
- 2-{maxDomains} clear sub-domains identified
- Each sub-domain can be planned independently
- Plan Note template includes all pre-allocated sections
- TASK ID ranges have no overlap (100 IDs per domain)
- Requirements understanding is comprehensive

---

## Phase 2: Serial Sub-Domain Planning

**Objective**: Plan each sub-domain sequentially, generating detailed plans and updating plan-note.md.

**Execution Model**: Serial inline execution — each domain explored and planned directly using search tools, one at a time.

### Step 2.1: User Confirmation (unless autoMode)

Display identified sub-domains and confirm before starting.

```javascript
if (!autoMode) {
  AskUserQuestion({
    questions: [{
      question: `已识别 ${subDomains.length} 个子领域:\n${subDomains.map((s, i) =>
        `${i+1}. ${s.focus_area}: ${s.description}`).join('\n')}\n\n确认开始规划?`,
      header: "Confirm",
      multiSelect: false,
      options: [
        { label: "开始规划", description: "逐域进行规划" },
        { label: "调整拆分", description: "修改子领域划分" },
        { label: "取消", description: "退出规划" }
      ]
    }]
  })
}
```

### Step 2.2: Serial Domain Planning

For each sub-domain, execute the full planning cycle inline:

```javascript
for (const sub of subDomains) {
  // 1. Create domain directory with .task/ subfolder
  Bash(`mkdir -p ${sessionFolder}/domains/${sub.focus_area}/.task`)

  // 2. Explore codebase for domain-relevant context
  //    Use: mcp__ace-tool__search_context, Grep, Glob, Read
  //    Focus on:
  //      - Modules/components related to this domain
  //      - Existing patterns to follow
  //      - Integration points with other domains
  //      - Architecture constraints

  // 3. Generate task JSON records (following task-schema.json)
  const domainTasks = [
    // For each task within the assigned ID range:
    {
      id: `TASK-${String(sub.task_id_range[0]).padStart(3, '0')}`,
      title: "...",
      description: "...",                 // scope/goal of this task
      type: "feature",                    // infrastructure|feature|enhancement|fix|refactor|testing
      priority: "medium",                 // high|medium|low
      effort: "medium",                   // small|medium|large
      scope: "...",                       // Brief scope description
      depends_on: [],                     // TASK-xxx references
      convergence: {
        criteria: ["... (testable)"],     // Testable conditions
        verification: "... (executable)", // Command or steps
        definition_of_done: "... (business language)"
      },
      files: [                            // Files to modify
        {
          path: "...",
          action: "modify",              // modify|create|delete
          changes: ["..."],               // Change descriptions
          conflict_risk: "low"            // low|medium|high
        }
      ],
      source: {
        tool: "collaborative-plan-with-file",
        session_id: sessionId,
        original_id: `TASK-${String(sub.task_id_range[0]).padStart(3, '0')}`
      }
    }
    // ... more tasks
  ]

  // 4. Write individual task JSON files (one per task)
  domainTasks.forEach(task => {
    Write(`${sessionFolder}/domains/${sub.focus_area}/.task/${task.id}.json`,
      JSON.stringify(task, null, 2))
  })

  // 5. Sync summary to plan-note.md
  //    Read current plan-note.md
  //    Locate pre-allocated sections:
  //      - Task Pool:  "## 任务池 - ${toTitleCase(sub.focus_area)}"
  //      - Evidence:   "## 上下文证据 - ${toTitleCase(sub.focus_area)}"
  //    Fill with task summaries and evidence
  //    Write back plan-note.md
}
```

**Task Summary Format** (for plan-note.md task pool sections):

```markdown
### TASK-{ID}: {Title} [{focus-area}]
- **状态**: pending
- **类型**: feature/fix/refactor/enhancement/testing/infrastructure
- **优先级**: high/medium/low
- **工作量**: small/medium/large
- **依赖**: TASK-xxx (if any)
- **范围**: Brief scope description
- **修改文件**: `file-path` (action): change summary
- **收敛标准**:
  - criteria 1
  - criteria 2
- **验证方式**: executable command or steps
- **完成定义**: business language definition
```

**Evidence Format** (for plan-note.md evidence sections):

```markdown
- **相关文件**: file list with relevance
- **现有模式**: patterns identified
- **约束**: constraints discovered
```

**Domain Planning Rules**:
- Each domain modifies ONLY its pre-allocated sections in plan-note.md
- Use assigned TASK ID range exclusively
- Include convergence criteria for each task (criteria + verification + definition_of_done)
- Include `files[]` with conflict_risk assessment per file
- Reference cross-domain dependencies explicitly
- Each task record must be self-contained (can be independently consumed by unified-execute)

### Step 2.3: Verify plan-note.md Consistency

After all domains are planned, verify the shared document.

**Verification Activities**:
1. Read final plan-note.md
2. Verify all task pool sections are populated
3. Verify all evidence sections are populated
4. Validate TASK ID uniqueness across all domains
5. Check for any section format inconsistencies

**Success Criteria**:
- `domains/{domain}/.task/TASK-*.json` created for each domain (one file per task)
- Each task has convergence (criteria + verification + definition_of_done)
- `plan-note.md` updated with all task pools and evidence sections
- Task summaries follow consistent format
- No TASK ID overlaps across domains

---

## Phase 3: Conflict Detection

**Objective**: Analyze plan-note.md for conflicts across all domain contributions.

### Step 3.1: Parse plan-note.md

Extract all tasks from all "任务池" sections and domain .task/*.json files.

```javascript
// parsePlanNote(markdown)
//   - Extract YAML frontmatter between `---` markers
//   - Scan for heading patterns: /^(#{2,})\s+(.+)$/
//   - Build sections array: { level, heading, start, content }
//   - Return: { frontmatter, sections }

// Also load all domain .task/*.json for detailed data
// loadDomainTasks(sessionFolder, subDomains):
//   const allTasks = []
//   for (const sub of subDomains) {
//     const taskDir = `${sessionFolder}/domains/${sub.focus_area}/.task`
//     const taskFiles = Glob(`${taskDir}/TASK-*.json`)
//     taskFiles.forEach(file => {
//       allTasks.push(JSON.parse(Read(file)))
//     })
//   }
//   return allTasks

// extractTasksFromSection(content, sectionHeading)
//   - Match: /### (TASK-\d+):\s+(.+?)\s+\[(.+?)\]/
//   - For each: extract taskId, title, author
//   - Parse details: status, type, priority, effort, depends_on, files, convergence
//   - Return: array of task objects

// parseTaskDetails(content)
//   - Extract via regex:
//     - /\*\*状态\*\*:\s*(.+)/ → status
//     - /\*\*类型\*\*:\s*(.+)/ → type
//     - /\*\*优先级\*\*:\s*(.+)/ → priority
//     - /\*\*工作量\*\*:\s*(.+)/ → effort
//     - /\*\*依赖\*\*:\s*(.+)/ → depends_on (extract TASK-\d+ references)
//   - Extract files: /- `([^`]+)` \((\w+)\):\s*(.+)/ → path, action, change
//   - Return: { status, type, priority, effort, depends_on[], files[], convergence }
```

### Step 3.2: Detect Conflicts

Scan all tasks for three categories of conflicts.

**Conflict Types**:

| Type | Severity | Detection Logic | Resolution |
|------|----------|-----------------|------------|
| file_conflict | high | Same file:location modified by multiple domains | Coordinate modification order or merge changes |
| dependency_cycle | critical | Circular dependencies in task graph (DFS detection) | Remove or reorganize dependencies |
| strategy_conflict | medium | Multiple high-risk tasks in same file from different domains | Review approaches and align on single strategy |

**Detection Functions**:

```javascript
// detectFileConflicts(tasks)
//   Build fileMap: { "file-path": [{ task_id, task_title, source_domain, changes }] }
//   For each file with modifications from multiple domains:
//     → conflict: type='file_conflict', severity='high'
//     → include: file, tasks_involved, domains_involved, changes
//     → resolution: 'Coordinate modification order or merge changes'

// detectDependencyCycles(tasks)
//   Build dependency graph: { taskId: [dependsOn_taskIds] }
//   DFS with recursion stack to detect cycles:
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

// detectStrategyConflicts(tasks)
//   Group tasks by files they modify (from task.files[].path)
//   For each file with tasks from multiple domains:
//     Filter for tasks with files[].conflict_risk === 'high' or 'medium'
//     If >1 high-risk from different domains:
//       → conflict: type='strategy_conflict', severity='medium'
//       → resolution: 'Review approaches and align on single strategy'
```

### Step 3.3: Generate Conflict Artifacts

Write conflict results and update plan-note.md.

```javascript
// 1. Write conflicts.json
Write(`${sessionFolder}/conflicts.json`, JSON.stringify({
  detected_at: getUtc8ISOString(),
  total_tasks: allTasks.length,
  total_domains: subDomains.length,
  total_conflicts: allConflicts.length,
  conflicts: allConflicts  // { type, severity, tasks_involved, description, suggested_resolution }
}, null, 2))

// 2. Update plan-note.md "## 冲突标记" section
// generateConflictMarkdown(conflicts):
//   If empty: return '✅ 无冲突检测到'
//   For each conflict:
//     ### CONFLICT-{padded_index}: {description}
//     - **严重程度**: critical | high | medium
//     - **涉及任务**: TASK-xxx, TASK-yyy
//     - **涉及领域**: domain-a, domain-b
//     - **问题详情**: (based on conflict type)
//     - **建议解决方案**: ...
//     - **决策状态**: [ ] 待解决

// replaceSectionContent(markdown, sectionHeading, newContent):
//   Find section heading position via regex
//   Find next heading of same or higher level
//   Replace content between heading and next section
//   If section not found: append at end
```

**Success Criteria**:
- All tasks extracted and analyzed
- `conflicts.json` written with detection results
- `plan-note.md` updated with conflict markers
- All conflict types checked (file, dependency, strategy)

---

## Phase 4: Completion

**Objective**: Generate human-readable plan summary and finalize workflow.

### Step 4.1: Collect Domain .task/*.json to Session .task/

Copy all per-domain task JSON files into a single session-level `.task/` directory.

```javascript
// Create session-level .task/ directory
Bash(`mkdir -p ${sessionFolder}/.task`)

// Collect all domain task files
for (const sub of subDomains) {
  const taskDir = `${sessionFolder}/domains/${sub.focus_area}/.task`
  const taskFiles = Glob(`${taskDir}/TASK-*.json`)
  taskFiles.forEach(file => {
    const filename = path.basename(file)
    // Copy domain task file to session .task/ directory
    Bash(`cp ${file} ${sessionFolder}/.task/${filename}`)
  })
}
```

### Step 4.2: Generate plan.json

Generate a plan overview following the plan-overview-base-schema.

```javascript
// Generate plan.json (plan-overview-base-schema)
const allTaskFiles = Glob(`${sessionFolder}/.task/TASK-*.json`)
const taskIds = allTaskFiles.map(f => JSON.parse(Read(f)).id).sort()

// Guard: skip plan.json if no tasks generated
if (taskIds.length === 0) {
  console.warn('No tasks generated; skipping plan.json')
} else {

const planOverview = {
  summary: `Collaborative plan for: ${taskDescription}`,
  approach: `Multi-domain planning across ${subDomains.length} sub-domains: ${subDomains.map(s => s.focus_area).join(', ')}`,
  task_ids: taskIds,
  task_count: taskIds.length,
  complexity: complexity,
  recommended_execution: "Agent",
  _metadata: {
    timestamp: getUtc8ISOString(),
    source: "direct-planning",
    planning_mode: "direct",
    plan_type: "collaborative",
    schema_version: "2.0"
  }
}
Write(`${sessionFolder}/plan.json`, JSON.stringify(planOverview, null, 2))

} // end guard
```

### Step 4.3: Generate plan.md

Create a human-readable summary from plan-note.md content.

**plan.md Structure**:

| Section | Content |
|---------|---------|
| Header | Session ID, task description, creation time |
| 需求 (Requirements) | Copied from plan-note.md "需求理解" section |
| 子领域拆分 (Sub-Domains) | Each domain with description, task range, estimated effort |
| 任务概览 (Task Overview) | All tasks with complexity, dependencies, and target files |
| 冲突报告 (Conflict Report) | Summary of detected conflicts or "无冲突" |
| 执行指令 (Execution) | Command to execute the plan |

```javascript
const planMd = `# Collaborative Plan

**Session**: ${sessionId}
**Requirement**: ${taskDescription}
**Created**: ${getUtc8ISOString()}
**Complexity**: ${complexity}
**Domains**: ${subDomains.length}

## 需求理解

${requirementSection}

## 子领域拆分

| # | Focus Area | Description | TASK Range | Effort |
|---|-----------|-------------|------------|--------|
${subDomains.map((s, i) => `| ${i+1} | ${s.focus_area} | ${s.description} | ${s.task_id_range[0]}-${s.task_id_range[1]} | ${s.estimated_effort} |`).join('\n')}

## 任务概览

${subDomains.map(sub => {
  const domainTasks = allTasks.filter(t => t.source?.original_id?.startsWith('TASK') && t.source?.session_id === sessionId)
  return `### ${sub.focus_area}\n\n` +
    domainTasks.map(t => `- **${t.id}**: ${t.title} (${t.type}, ${t.effort}) ${t.depends_on.length ? '← ' + t.depends_on.join(', ') : ''}`).join('\n')
}).join('\n\n')}

## 冲突报告

${allConflicts.length === 0
  ? '✅ 无冲突检测到'
  : allConflicts.map(c => `- **${c.type}** (${c.severity}): ${c.description}`).join('\n')}

## 执行

\`\`\`bash
/workflow:unified-execute-with-file PLAN="${sessionFolder}/.task/"
\`\`\`

**Session artifacts**: \`${sessionFolder}/\`
`
Write(`${sessionFolder}/plan.md`, planMd)
```

### Step 4.4: Display Completion Summary

Present session statistics and next steps.

```javascript
// Display:
// - Session ID and directory path
// - Total domains planned
// - Total tasks generated
// - Conflict status (count and severity)
// - Execution command for next step

if (!autoMode) {
  AskUserQuestion({
    questions: [{
      question: `规划完成:\n- ${subDomains.length} 个子领域\n- ${allTasks.length} 个任务\n- ${allConflicts.length} 个冲突\n\n下一步:`,
      header: "Next Step",
      multiSelect: false,
      options: [
        { label: "Execute Plan", description: "使用 unified-execute 执行计划" },
        { label: "Review Conflicts", description: "查看并解决冲突" },
        { label: "Export", description: "导出 plan.md" },
        { label: "Done", description: "保存产物，稍后执行" }
      ]
    }]
  })
}
```

| Selection | Action |
|-----------|--------|
| Execute Plan | `Skill(skill="workflow:unified-execute-with-file", args="PLAN=\"${sessionFolder}/.task/\"")` |
| Review Conflicts | Display conflicts.json content for manual resolution |
| Export | Copy plan.md + plan-note.md to user-specified location |
| Done | Display artifact paths, end workflow |

**Success Criteria**:
- `plan.md` generated with complete summary
- `.task/TASK-*.json` collected at session root (consumable by unified-execute)
- All artifacts present in session directory
- User informed of completion and next steps

---

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--max-domains` | 5 | Maximum sub-domains to identify |
| `-y, --yes` | false | Auto-confirm all decisions |

## Iteration Patterns

### New Planning Session

```
User initiates: TASK="task description"
   ├─ No session exists → New session mode
   ├─ Analyze task with inline search tools
   ├─ Identify sub-domains
   ├─ Create plan-note.md template
   ├─ Generate requirement-analysis.json
   │
   ├─ Serial domain planning:
   │   ├─ Domain 1: explore → .task/TASK-*.json → fill plan-note.md
   │   ├─ Domain 2: explore → .task/TASK-*.json → fill plan-note.md
   │   └─ Domain N: ...
   │
   ├─ Collect domain .task/*.json → session .task/
   │
   ├─ Verify plan-note.md consistency
   ├─ Detect conflicts
   ├─ Generate plan.md summary
   └─ Report completion
```

### Continue Existing Session

```
User resumes: TASK="same task"
   ├─ Session exists → Continue mode
   ├─ Load plan-note.md and requirement-analysis.json
   ├─ Identify incomplete domains (empty task pool sections)
   ├─ Plan remaining domains serially
   └─ Continue with conflict detection
```

---

## Error Handling & Recovery

| Situation | Action | Recovery |
|-----------|--------|----------|
| No codebase detected | Normal flow, pure requirement planning | Proceed without codebase context |
| Codebase search fails | Continue with available context | Note limitation in plan-note.md |
| Domain planning fails | Record error, continue with next domain | Retry failed domain or plan manually |
| Section not found in plan-note | Create section defensively | Continue with new section |
| No tasks generated for a domain | Review domain description | Refine scope and retry |
| Conflict detection fails | Continue with empty conflicts | Note in completion summary |
| Session folder conflict | Append timestamp suffix | Create unique folder |
| plan-note.md format inconsistency | Validate and fix format after each domain | Re-read and normalize |

---

## Best Practices

### Before Starting Planning

1. **Clear Task Description**: Detailed requirements lead to better sub-domain splitting
2. **Reference Documentation**: Ensure latest README and design docs are identified during Phase 1
3. **Clarify Ambiguities**: Resolve unclear requirements before committing to sub-domains

### During Planning

1. **Review Plan Note**: Check plan-note.md between domains to verify progress
2. **Verify Independence**: Ensure sub-domains are truly independent and have minimal overlap
3. **Check Dependencies**: Cross-domain dependencies should be documented explicitly
4. **Inspect Details**: Review `domains/{domain}/.task/TASK-*.json` for specifics when needed
5. **Consistent Format**: Follow task summary format strictly across all domains
6. **TASK ID Isolation**: Use pre-assigned non-overlapping ranges to prevent ID conflicts

### After Planning

1. **Resolve Conflicts**: Address high/critical conflicts before execution
2. **Review Summary**: Check plan.md for completeness and accuracy
3. **Validate Tasks**: Ensure all tasks have clear scope and modification targets

## When to Use

**Use collaborative-plan-with-file when:**
- A complex task spans multiple sub-domains (backend + frontend + database, etc.)
- Need structured multi-domain task breakdown with conflict detection
- Planning a feature that touches many parts of the codebase
- Want pre-allocated section organization for clear domain separation

**Use lite-plan when:**
- Single domain, clear task with no sub-domain splitting needed
- Quick planning without conflict detection

**Use req-plan-with-file when:**
- Requirement-level progressive roadmap needed (MVP → iterations)
- Higher-level decomposition before detailed planning

**Use analyze-with-file when:**
- Need in-depth analysis before planning
- Understanding and discussion, not task generation

---

**Now execute collaborative-plan-with-file for**: $ARGUMENTS
