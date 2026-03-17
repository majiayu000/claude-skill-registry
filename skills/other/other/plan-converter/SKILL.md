---
name: plan-converter
description: Convert any planning/analysis/brainstorm output to .task/*.json multi-file format. Supports roadmap.jsonl, plan.json, plan-note.md, conclusions.json, synthesis.json.
argument-hint: "<input-file> [-o <output-file>]"
---

# Plan Converter

## Overview

Converts any planning artifact to **`.task/*.json` multi-file format** — the single standard consumed by `unified-execute-with-file`.

> **Schema**: `cat ~/.ccw/workflows/cli-templates/schemas/task-schema.json`

```bash
# Auto-detect format, output to same directory .task/
/codex:plan-converter ".workflow/.req-plan/RPLAN-auth-2025-01-21/roadmap.jsonl"

# Specify output directory
/codex:plan-converter ".workflow/.planning/CPLAN-xxx/plan-note.md" -o .task/

# Convert brainstorm synthesis
/codex:plan-converter ".workflow/.brainstorm/BS-xxx/synthesis.json"
```

**Supported inputs**: roadmap.jsonl, .task/*.json (per-domain), plan-note.md, conclusions.json, synthesis.json

**Output**: `.task/*.json` (one file per task, in same directory's `.task/` subfolder, or specified `-o` path)

## Task JSON Schema

每个任务一个独立 JSON 文件 (`.task/TASK-{id}.json`)，遵循统一 schema：

> **Schema 定义**: `cat ~/.ccw/workflows/cli-templates/schemas/task-schema.json`

**Producer 使用的字段集** (plan-converter 输出):

```
IDENTITY (必填):        id, title, description
CLASSIFICATION (可选):   type, priority, effort, action
SCOPE (可选):            scope, excludes, focus_paths
DEPENDENCIES (必填):     depends_on, parallel_group, inputs, outputs
CONVERGENCE (必填):      convergence.criteria, convergence.verification, convergence.definition_of_done
FILES (可选):            files[].path, files[].action, files[].changes, files[].change, files[].target, files[].conflict_risk
IMPLEMENTATION (可选):   implementation[], test.manual_checks, test.success_metrics
PLANNING (可选):         reference, rationale, risks
CONTEXT (可选):          source.tool, source.session_id, source.original_id, evidence, risk_items
RUNTIME (执行时填充):    status, executed_at, result
```

**文件命名**: `TASK-{id}.json` (保留原有 ID 前缀: L0-, T1-, IDEA- 等)

## Target Input

**$ARGUMENTS**

## Execution Process

```
Step 0: Parse arguments, resolve input path
Step 1: Detect input format
Step 2: Parse input → extract raw records
Step 3: Transform → unified task records
Step 4: Validate convergence quality
Step 5: Write .task/*.json output + display summary
```

## Implementation

### Step 0: Parse Arguments

```javascript
const args = $ARGUMENTS
const outputMatch = args.match(/-o\s+(\S+)/)
const outputPath = outputMatch ? outputMatch[1] : null
const inputPath = args.replace(/-o\s+\S+/, '').trim()

// Resolve absolute path
const projectRoot = Bash(`git rev-parse --show-toplevel 2>/dev/null || pwd`).trim()
const resolvedInput = path.isAbsolute(inputPath) ? inputPath : `${projectRoot}/${inputPath}`
```

### Step 1: Detect Format

```javascript
const filename = path.basename(resolvedInput)
const content = Read(resolvedInput)

function detectFormat(filename, content) {
  if (filename === 'roadmap.jsonl')     return 'roadmap-jsonl'
  if (filename === 'tasks.jsonl')       return 'tasks-jsonl'    // legacy JSONL or per-domain
  if (filename === 'plan-note.md')      return 'plan-note-md'
  if (filename === 'conclusions.json')  return 'conclusions-json'
  if (filename === 'synthesis.json')    return 'synthesis-json'
  if (filename.endsWith('.jsonl'))      return 'generic-jsonl'
  if (filename.endsWith('.json')) {
    const parsed = JSON.parse(content)
    if (parsed.top_ideas)               return 'synthesis-json'
    if (parsed.recommendations && parsed.key_conclusions) return 'conclusions-json'
    if (parsed.tasks && parsed.focus_area) return 'domain-plan-json'
    return 'unknown-json'
  }
  if (filename.endsWith('.md'))         return 'plan-note-md'
  return 'unknown'
}
```

**Format Detection Table**:

| Filename | Format ID | Source Tool |
|----------|-----------|------------|
| `roadmap.jsonl` | roadmap-jsonl | req-plan-with-file |
| `tasks.jsonl` (legacy) / `.task/*.json` | tasks-jsonl / task-json | collaborative-plan-with-file |
| `plan-note.md` | plan-note-md | collaborative-plan-with-file |
| `conclusions.json` | conclusions-json | analyze-with-file |
| `synthesis.json` | synthesis-json | brainstorm-with-file |

### Step 2: Parse Input

#### roadmap-jsonl (req-plan-with-file)

```javascript
function parseRoadmapJsonl(content) {
  return content.split('\n')
    .filter(line => line.trim())
    .map(line => JSON.parse(line))
}
// Records have: id (L0/T1), name/title, goal/scope, convergence, depends_on, etc.
```

#### plan-note-md (collaborative-plan-with-file)

```javascript
function parsePlanNoteMd(content) {
  const tasks = []
  // 1. Extract YAML frontmatter for session metadata
  const frontmatter = extractYamlFrontmatter(content)

  // 2. Find all "## 任务池 - {Domain}" sections
  const taskPoolSections = content.match(/## 任务池 - .+/g) || []

  // 3. For each section, extract tasks matching:
  //    ### TASK-{ID}: {Title} [{domain}]
  //    - **状态**: pending
  //    - **复杂度**: Medium
  //    - **依赖**: TASK-xxx
  //    - **范围**: ...
  //    - **修改点**: `file:location`: change summary
  //    - **冲突风险**: Low
  taskPoolSections.forEach(section => {
    const sectionContent = extractSectionContent(content, section)
    const taskPattern = /### (TASK-\d+):\s+(.+?)\s+\[(.+?)\]/g
    let match
    while ((match = taskPattern.exec(sectionContent)) !== null) {
      const [_, id, title, domain] = match
      const taskBlock = extractTaskBlock(sectionContent, match.index)
      tasks.push({
        id, title, domain,
        ...parseTaskDetails(taskBlock)
      })
    }
  })
  return { tasks, frontmatter }
}
```

#### conclusions-json (analyze-with-file)

```javascript
function parseConclusionsJson(content) {
  const conclusions = JSON.parse(content)
  // Extract from: conclusions.recommendations[]
  //   { action, rationale, priority }
  // Also available: conclusions.key_conclusions[]
  return conclusions
}
```

#### synthesis-json (brainstorm-with-file)

```javascript
function parseSynthesisJson(content) {
  const synthesis = JSON.parse(content)
  // Extract from: synthesis.top_ideas[]
  //   { title, description, score, feasibility, next_steps, key_strengths, main_challenges }
  // Also available: synthesis.recommendations
  return synthesis
}
```

### Step 3: Transform to Unified Records

#### roadmap-jsonl → unified

```javascript
function transformRoadmap(records, sessionId) {
  return records.map(rec => {
    // roadmap.jsonl now uses unified field names (title, description, source)
    // Passthrough is mostly direct
    return {
      id: rec.id,
      title: rec.title,
      description: rec.description,
      type: rec.type || 'feature',
      effort: rec.effort,
      scope: rec.scope,
      excludes: rec.excludes,
      depends_on: rec.depends_on || [],
      parallel_group: rec.parallel_group,
      inputs: rec.inputs,
      outputs: rec.outputs,
      convergence: rec.convergence,  // already unified format
      risk_items: rec.risk_items,
      source: rec.source || {
        tool: 'req-plan-with-file',
        session_id: sessionId,
        original_id: rec.id
      }
    }
  })
}
```

#### plan-note-md → unified

```javascript
function transformPlanNote(parsed) {
  const { tasks, frontmatter } = parsed
  return tasks.map(task => ({
    id: task.id,
    title: task.title,
    description: task.scope || task.title,
    type: task.type || inferTypeFromTitle(task.title),
    priority: task.priority || inferPriorityFromEffort(task.effort),
    effort: task.effort || 'medium',
    scope: task.scope,
    depends_on: task.depends_on || [],
    convergence: task.convergence || generateConvergence(task),  // plan-note now has convergence
    files: task.files?.map(f => ({
      path: f.path || f.file,
      action: f.action || 'modify',
      changes: f.changes || (f.change ? [f.change] : undefined),
      change: f.change,
      target: f.target,
      conflict_risk: f.conflict_risk
    })),
    source: {
      tool: 'collaborative-plan-with-file',
      session_id: frontmatter.session_id,
      original_id: task.id
    }
  }))
}

// Generate convergence from task details when source lacks it (legacy fallback)
function generateConvergence(task) {
  return {
    criteria: [
      // Derive testable conditions from scope and files
      // e.g., "Modified files compile without errors"
      // e.g., scope-derived: "API endpoint returns expected response"
    ],
    verification: '// Derive from files — e.g., test commands',
    definition_of_done: '// Derive from scope — business language summary'
  }
}
```

#### conclusions-json → unified

```javascript
function transformConclusions(conclusions) {
  return conclusions.recommendations.map((rec, index) => ({
    id: `TASK-${String(index + 1).padStart(3, '0')}`,
    title: rec.action,
    description: rec.rationale,
    type: inferTypeFromAction(rec.action),
    priority: rec.priority,
    depends_on: [],
    convergence: {
      criteria: generateCriteriaFromAction(rec),
      verification: generateVerificationFromAction(rec),
      definition_of_done: generateDoDFromRationale(rec)
    },
    evidence: conclusions.key_conclusions.map(c => c.point),
    source: {
      tool: 'analyze-with-file',
      session_id: conclusions.session_id
    }
  }))
}

function inferTypeFromAction(action) {
  const lower = action.toLowerCase()
  if (/fix|resolve|repair|修复/.test(lower)) return 'fix'
  if (/refactor|restructure|extract|重构/.test(lower)) return 'refactor'
  if (/add|implement|create|新增|实现/.test(lower)) return 'feature'
  if (/improve|optimize|enhance|优化/.test(lower)) return 'enhancement'
  if (/test|coverage|validate|测试/.test(lower)) return 'testing'
  return 'feature'
}
```

#### synthesis-json → unified

```javascript
function transformSynthesis(synthesis) {
  return synthesis.top_ideas
    .filter(idea => idea.score >= 6)  // Only viable ideas (score ≥ 6)
    .map((idea, index) => ({
      id: `IDEA-${String(index + 1).padStart(3, '0')}`,
      title: idea.title,
      description: idea.description,
      type: 'feature',
      priority: idea.score >= 8 ? 'high' : idea.score >= 6 ? 'medium' : 'low',
      effort: idea.feasibility >= 4 ? 'small' : idea.feasibility >= 2 ? 'medium' : 'large',
      depends_on: [],
      convergence: {
        criteria: idea.next_steps || [`${idea.title} implemented and functional`],
        verification: 'Manual validation of feature functionality',
        definition_of_done: idea.description
      },
      risk_items: idea.main_challenges || [],
      source: {
        tool: 'brainstorm-with-file',
        session_id: synthesis.session_id,
        original_id: `idea-${index + 1}`
      }
    }))
}
```

### Step 4: Validate Convergence Quality

All records must pass convergence quality checks before output.

```javascript
function validateConvergence(records) {
  const vaguePatterns = /正常|正确|好|可以|没问题|works|fine|good|correct/i
  const technicalPatterns = /compile|build|lint|npm|npx|jest|tsc|eslint/i
  const issues = []

  records.forEach(record => {
    const c = record.convergence
    if (!c) {
      issues.push({ id: record.id, field: 'convergence', issue: 'Missing entirely' })
      return
    }
    if (!c.criteria?.length) {
      issues.push({ id: record.id, field: 'criteria', issue: 'Empty criteria array' })
    }
    c.criteria?.forEach((criterion, i) => {
      if (vaguePatterns.test(criterion) && criterion.length < 15) {
        issues.push({ id: record.id, field: `criteria[${i}]`, issue: `Too vague: "${criterion}"` })
      }
    })
    if (!c.verification || c.verification.length < 10) {
      issues.push({ id: record.id, field: 'verification', issue: 'Too short or missing' })
    }
    if (technicalPatterns.test(c.definition_of_done)) {
      issues.push({ id: record.id, field: 'definition_of_done', issue: 'Should be business language' })
    }
  })

  return issues
}

// Auto-fix strategy:
// | Issue                | Fix                                          |
// |----------------------|----------------------------------------------|
// | Missing convergence  | Generate from title + description + files     |
// | Vague criteria       | Replace with specific condition from context  |
// | Short verification   | Expand with file-based test suggestion        |
// | Technical DoD        | Rewrite in business language                  |
```

### Step 5: Write .task/*.json Output & Summary

```javascript
// Determine output directory
const outputDir = outputPath
  || `${path.dirname(resolvedInput)}/.task`

// Create output directory
Bash(`mkdir -p ${outputDir}`)

// Clean records: remove undefined/null optional fields
const cleanedRecords = records.map(rec => {
  const clean = { ...rec }
  Object.keys(clean).forEach(key => {
    if (clean[key] === undefined || clean[key] === null) delete clean[key]
    if (Array.isArray(clean[key]) && clean[key].length === 0 && key !== 'depends_on') delete clean[key]
  })
  return clean
})

// Write individual task JSON files
cleanedRecords.forEach(record => {
  const filename = `${record.id}.json`
  Write(`${outputDir}/${filename}`, JSON.stringify(record, null, 2))
})

// Display summary
// | Source          | Format            | Records | Issues |
// |-----------------|-------------------|---------|--------|
// | roadmap.jsonl   | roadmap-jsonl     | 4       | 0      |
//
// Output: .workflow/.req-plan/RPLAN-xxx/.task/ (4 files)
// Records: 4 tasks with convergence criteria
// Quality: All convergence checks passed
```

---

## Conversion Matrix

| Source | Source Tool | ID Pattern | Has Convergence | Has Files | Has Priority | Has Source |
|--------|-----------|------------|-----------------|-----------|--------------|-----------|
| roadmap.jsonl (progressive) | req-plan | L0-L3 | **Yes** | No | No | **Yes** |
| roadmap.jsonl (direct) | req-plan | T1-TN | **Yes** | No | No | **Yes** |
| .task/TASK-*.json (per-domain) | collaborative-plan | TASK-NNN | **Yes** | **Yes** (detailed) | Optional | **Yes** |
| plan-note.md | collaborative-plan | TASK-NNN | **Generate** | **Yes** (from 修改文件) | From effort | No |
| conclusions.json | analyze | TASK-NNN | **Generate** | No | **Yes** | No |
| synthesis.json | brainstorm | IDEA-NNN | **Generate** | No | From score | No |

**Legend**: Yes = source already has it, Generate = converter produces it, No = not available

## Error Handling

| Situation | Action |
|-----------|--------|
| Input file not found | Report error, suggest checking path |
| Unknown format | Report error, list supported formats |
| Empty input | Report error, no output file created |
| Convergence validation fails | Auto-fix where possible, report remaining issues |
| Partial parse failure | Convert valid records, report skipped items |
| Output file exists | Overwrite with warning message |
| plan-note.md has empty sections | Skip empty domains, report in summary |

---

**Now execute plan-converter for**: $ARGUMENTS
