---
name: workflow-req-plan
description: Requirement-level progressive roadmap planning with issue creation. Decomposes requirements into convergent layers or task sequences, creates issues via ccw issue create, and generates roadmap.md for human review. Issues stored in .workflow/issues/issues.jsonl (single source of truth).
argument-hint: "[-y|--yes] [-c|--continue] [-m|--mode progressive|direct|auto] \"requirement description\""
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow Req-Plan

## Usage

```bash
$workflow-req-plan "Implement user authentication system with OAuth and 2FA"

# With mode selection
$workflow-req-plan -m progressive "Build real-time notification system"   # Layered MVP→iterations
$workflow-req-plan -m direct "Refactor payment module"                   # Topologically-sorted task sequence
$workflow-req-plan -m auto "Add data export feature"                     # Auto-select strategy

# Continue existing session
$workflow-req-plan --continue "user authentication system"

# Auto mode (skip all confirmations)
$workflow-req-plan -y "Implement caching layer"

# Flags
-y, --yes                              Skip all confirmations (auto mode)
-c, --continue                         Continue existing session
-m, --mode <progressive|direct|auto>   Decomposition strategy (default: auto)
```

**Context Source**: cli-explore-agent (optional) + requirement analysis
**Output Directory**: `.workflow/.req-plan/{session-id}/`
**Core Innovation**: Requirement decomposition → issue creation via `ccw issue create`. Issues stored in `.workflow/issues/issues.jsonl` (single source of truth); wave and dependency info embedded in issue tags and `extended_context.notes`. team-planex consumes issues directly by ID or tag query.

## Overview

Requirement-level layered roadmap planning. Decomposes a requirement into **convergent layers or task sequences**, creates issues via `ccw issue create`. Issues are the single source of truth in `.workflow/issues/issues.jsonl`; wave and dependency info is embedded in issue tags and `extended_context.notes`.

**Dual Modes**:
- **Progressive**: Layered MVP→iterations, suitable for high-uncertainty requirements (validate first, then refine)
- **Direct**: Topologically-sorted task sequence, suitable for low-uncertainty requirements (clear tasks, directly ordered)
- **Auto**: Automatically selects based on uncertainty level

**Core Workflow**: Requirement Understanding → Strategy Selection → Context Collection (optional) → Decomposition + Issue Creation → Validation → team-planex Handoff

## Execution Process

```
Phase 0: Initialization
   ├─ Parse arguments (--yes, --continue, --mode)
   ├─ Generate session ID (RPLAN-{slug}-{date})
   └─ Create session folder

Phase 1: Requirement Understanding & Strategy Selection
   ├─ Parse requirement: goal / constraints / stakeholders
   ├─ Assess uncertainty level
   │   ├─ High uncertainty → recommend progressive
   │   └─ Low uncertainty  → recommend direct
   ├─ ASK_USER: Confirm strategy (-m skips, -y auto-selects)
   └─ Write strategy-assessment.json + roadmap.md skeleton

Phase 2: Context Collection (Optional, Subagent)
   ├─ Detect codebase: package.json / go.mod / src / ...
   ├─ Has codebase → spawn_agent cli-explore-agent
   │   ├─ Explore relevant modules and patterns
   │   ├─ wait for completion
   │   └─ close_agent
   └─ No codebase → skip, pure requirement decomposition

Phase 3: Decomposition & Issue Creation (Inlined Agent)
   ├─ Step 3.1: CLI-Assisted Decomposition
   │   ├─ Construct CLI prompt with requirement + context + mode
   │   ├─ Execute Gemini (fallback: Qwen → manual decomposition)
   │   └─ Parse CLI output into structured records
   ├─ Step 3.2: Record Enhancement & Validation
   │   ├─ Validate each record against schema
   │   ├─ Enhance convergence criteria quality
   │   ├─ Validate dependency graph (no cycles)
   │   └─ Progressive: verify scope; Direct: verify inputs/outputs
   ├─ Step 3.3: Issue Creation & Output Generation
   │   ├─ Internal records → issue data mapping
   │   ├─ ccw issue create for each item (get ISS-xxx IDs)
   │   └─ Generate roadmap.md with issue ID references
   └─ Step 3.4: Decomposition Quality Check (MANDATORY)
       ├─ Execute CLI quality check (Gemini, Qwen fallback)
       └─ Decision: PASS / AUTO_FIX / NEEDS_REVIEW

Phase 4: Validation & team-planex Handoff
   ├─ Display decomposition results (tabular + convergence criteria)
   ├─ ASK_USER: Feedback loop (up to 5 rounds)
   └─ ASK_USER: Next steps (team-planex / wave-by-wave / view / done)
```

## Output

```
.workflow/.req-plan/RPLAN-{slug}-{YYYY-MM-DD}/
├── roadmap.md                    # Human-readable roadmap with issue ID references
├── strategy-assessment.json      # Strategy assessment result
└── exploration-codebase.json     # Codebase context (optional)
```

| File | Phase | Description |
|------|-------|-------------|
| `strategy-assessment.json` | 1 | Uncertainty analysis + mode recommendation + extracted goal/constraints/stakeholders |
| `roadmap.md` (skeleton) | 1 | Initial skeleton with placeholders, finalized in Phase 3 |
| `exploration-codebase.json` | 2 | Codebase context: relevant modules, patterns, integration points (only when codebase exists) |
| `roadmap.md` (final) | 3 | Human-readable roadmap with issue ID references, convergence details, team-planex execution guide |

## Subagent API Reference

### spawn_agent
Create a new subagent with task assignment.

```javascript
const agentId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/{agent-type}.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

## TASK CONTEXT
${taskContext}

## DELIVERABLES
${deliverables}
`
})
```

### wait
Get results from subagent (only way to retrieve results).

```javascript
const result = wait({
  ids: [agentId],
  timeout_ms: 600000  // 10 minutes
})

if (result.timed_out) {
  // Handle timeout - can send_input to prompt completion
}
```

### close_agent
Clean up subagent resources (irreversible).

```javascript
close_agent({ id: agentId })
```

---

## Implementation

### Phase 0: Initialization

##### Step 0: Determine Project Root

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse arguments
const args = "$ARGUMENTS"
const AUTO_YES = args.includes('--yes') || args.includes('-y')
const continueMode = args.includes('--continue') || args.includes('-c')
const modeMatch = args.match(/(?:--mode|-m)\s+(progressive|direct|auto)/)
const requestedMode = modeMatch ? modeMatch[1] : 'auto'

// Clean requirement text (remove flags)
const requirement = args
  .replace(/--yes|-y|--continue|-c|--mode\s+\w+|-m\s+\w+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10)
const sessionId = `RPLAN-${slug}-${dateStr}`
const sessionFolder = `${projectRoot}/.workflow/.req-plan/${sessionId}`

bash(`mkdir -p ${sessionFolder}`)

// Utility functions
function fileExists(p) {
  try { return bash(`test -f "${p}" && echo "yes"`).includes('yes') } catch { return false }
}
```

---

### Phase 1: Requirement Understanding & Strategy Selection

**Objective**: Parse requirement, assess uncertainty, select decomposition strategy.

```javascript
// 1. Parse Requirement
// - Extract core goal (what to achieve)
// - Identify constraints (tech stack, timeline, compatibility, etc.)
// - Identify stakeholders (users, admins, developers, etc.)
// - Identify keywords to determine domain

// 2. Assess Uncertainty Level
const uncertaintyFactors = {
  scope_clarity: 'low|medium|high',
  technical_risk: 'low|medium|high',
  dependency_unknown: 'low|medium|high',
  domain_familiarity: 'low|medium|high',
  requirement_stability: 'low|medium|high'
}
// high uncertainty (>=3 high) → progressive
// low uncertainty (>=3 low)  → direct
// otherwise → ask user preference

// 3. Strategy Selection
let selectedMode
if (requestedMode !== 'auto') {
  selectedMode = requestedMode
} else if (AUTO_YES) {
  selectedMode = recommendedMode  // use defaults
} else {
  const strategyAnswer = ASK_USER([
    {
      id: "strategy", type: "select",
      prompt: `Decomposition strategy selection:\n\nUncertainty: ${uncertaintyLevel}\nRecommended: ${recommendedMode}\n\nSelect:`,
      options: [
        { label: recommendedMode === 'progressive' ? "Progressive (Recommended)" : "Progressive",
          description: "Layered MVP→iterations, validate core first" },
        { label: recommendedMode === 'direct' ? "Direct (Recommended)" : "Direct",
          description: "Topologically-sorted task sequence" }
      ]
    }
  ])  // BLOCKS (wait for user response)
  selectedMode = strategyAnswer.strategy.toLowerCase().includes('progressive') ? 'progressive' : 'direct'
}

// 4. Generate strategy-assessment.json
const strategyAssessment = {
  session_id: sessionId,
  requirement: requirement,
  timestamp: getUtc8ISOString(),
  uncertainty_factors: uncertaintyFactors,
  uncertainty_level: uncertaintyLevel,
  recommended_mode: recommendedMode,
  selected_mode: selectedMode,
  goal: extractedGoal,
  constraints: extractedConstraints,
  stakeholders: extractedStakeholders,
  domain_keywords: extractedKeywords
}
Write(`${sessionFolder}/strategy-assessment.json`, JSON.stringify(strategyAssessment, null, 2))

// 5. Initialize roadmap.md skeleton
const roadmapMdSkeleton = `# Requirement Roadmap

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Strategy**: ${selectedMode}
**Status**: Planning
**Created**: ${getUtc8ISOString()}

## Strategy Assessment
- Uncertainty level: ${uncertaintyLevel}
- Decomposition mode: ${selectedMode}

## Roadmap
> To be populated after Phase 3 decomposition

## Convergence Criteria Details
> To be populated after Phase 3 decomposition

## Risk Items
> To be populated after Phase 3 decomposition

## Next Steps
> To be populated after Phase 4 validation
`
Write(`${sessionFolder}/roadmap.md`, roadmapMdSkeleton)
```

**Success Criteria**:
- Requirement goal, constraints, stakeholders identified
- Uncertainty level assessed
- Strategy selected (progressive or direct)
- strategy-assessment.json generated
- roadmap.md skeleton initialized

---

### Phase 2: Context Collection (Optional, Subagent)

**Objective**: If a codebase exists, collect relevant context to enhance decomposition quality.

```javascript
// 1. Detect Codebase
const hasCodebase = bash(`
  test -f package.json && echo "nodejs" ||
  test -f go.mod && echo "golang" ||
  test -f Cargo.toml && echo "rust" ||
  test -f pyproject.toml && echo "python" ||
  test -f pom.xml && echo "java" ||
  test -d src && echo "generic" ||
  echo "none"
`).trim()

// 2. Codebase Exploration (only when hasCodebase !== 'none')
let exploreAgent = null

if (hasCodebase !== 'none') {
  try {
    exploreAgent = spawn_agent({
      message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: ${projectRoot}/.workflow/project-tech.json (if exists)
3. Read: ${projectRoot}/.workflow/project-guidelines.json (if exists)

---

## Task Objective
Explore codebase for requirement decomposition context.

## Exploration Context
Requirement: ${requirement}
Strategy: ${selectedMode}
Project Type: ${hasCodebase}
Session: ${sessionFolder}

## MANDATORY FIRST STEPS
1. Run: ccw tool exec get_modules_by_depth '{}'
2. Execute relevant searches based on requirement keywords

## Exploration Focus
- Identify modules/components related to the requirement
- Find existing patterns that should be followed
- Locate integration points for new functionality
- Assess current architecture constraints

## Output
Write findings to: ${sessionFolder}/exploration-codebase.json

Schema: {
  project_type: "${hasCodebase}",
  relevant_modules: [{name, path, relevance}],
  existing_patterns: [{pattern, files, description}],
  integration_points: [{location, description, risk}],
  architecture_constraints: [string],
  tech_stack: {languages, frameworks, tools},
  _metadata: {timestamp, exploration_scope}
}
`
    })

    // Wait with timeout handling
    let result = wait({ ids: [exploreAgent], timeout_ms: 600000 })

    if (result.timed_out) {
      send_input({ id: exploreAgent, message: 'Complete now and write exploration-codebase.json.' })
      result = wait({ ids: [exploreAgent], timeout_ms: 300000 })
      if (result.timed_out) throw new Error('Agent timeout')
    }

  } finally {
    if (exploreAgent) close_agent({ id: exploreAgent })
  }
}
// No codebase → skip, proceed directly to Phase 3
```

---

### Phase 3: Decomposition & Issue Creation (Inlined Agent)

**Objective**: Execute requirement decomposition, create issues, generate execution-plan.json + issues.jsonl + roadmap.md.

**CRITICAL**: After creating issues, MUST execute **Decomposition Quality Check** (Step 3.4) using CLI analysis before proceeding to Phase 4.

#### Prepare Context

```javascript
const strategy = JSON.parse(Read(`${sessionFolder}/strategy-assessment.json`))
let explorationContext = null
if (fileExists(`${sessionFolder}/exploration-codebase.json`)) {
  explorationContext = JSON.parse(Read(`${sessionFolder}/exploration-codebase.json`))
}
```

#### Internal Record Schemas (CLI Parsing)

These schemas are used internally for parsing CLI decomposition output. They are converted to issues in Step 3.3.

**Progressive Mode - Layer Record**:
```javascript
{
  id: "L{n}",               // L0, L1, L2, L3
  name: string,              // Layer name: MVP / 可用 / 完善 / 优化
  goal: string,              // Layer goal (one sentence)
  scope: [string],           // Features included
  excludes: [string],        // Features explicitly excluded
  convergence: {
    criteria: [string],         // Testable conditions
    verification: string,       // How to verify
    definition_of_done: string  // Business-language completion definition
  },
  risks: [{description, probability, impact, mitigation}],
  effort: "small" | "medium" | "large",
  depends_on: ["L{n}"]
}
```

**Direct Mode - Task Record**:
```javascript
{
  id: "T{n}",                // T1, T2, T3, ...
  title: string,
  type: "infrastructure" | "feature" | "enhancement" | "testing",
  scope: string,
  inputs: [string],
  outputs: [string],
  convergence: { criteria, verification, definition_of_done },
  depends_on: ["T{n}"],
  parallel_group: number      // Same group = parallelizable
}
```

#### Convergence Quality Requirements

| Field | Requirement | Bad Example | Good Example |
|-------|-------------|-------------|--------------|
| `criteria[]` | **Testable** | `"系统工作正常"` | `"API 返回 200 且响应体包含 user_id 字段"` |
| `verification` | **Executable** | `"检查一下"` | `"jest --testPathPattern=auth && curl -s localhost:3000/health"` |
| `definition_of_done` | **Business language** | `"代码通过编译"` | `"新用户可完成注册→登录→执行核心操作的完整流程"` |

---

#### Step 3.1: CLI-Assisted Decomposition

##### Progressive Mode CLI Template

```bash
ccw cli -p "
PURPOSE: Decompose requirement into progressive layers (MVP→iterations) with convergence criteria
Success: 2-4 self-contained layers, each with testable convergence, no scope overlap

REQUIREMENT:
${requirement}

STRATEGY CONTEXT:
- Uncertainty: ${strategy.uncertainty_level}
- Goal: ${strategy.goal}
- Constraints: ${strategy.constraints.join(', ')}
- Stakeholders: ${strategy.stakeholders.join(', ')}

${explorationContext ? `CODEBASE CONTEXT:
- Relevant modules: ${explorationContext.relevant_modules.map(m => m.name).join(', ')}
- Existing patterns: ${explorationContext.existing_patterns.map(p => p.pattern).join(', ')}
- Architecture constraints: ${explorationContext.architecture_constraints.join(', ')}
- Tech stack: ${JSON.stringify(explorationContext.tech_stack)}` : 'NO CODEBASE (pure requirement decomposition)'}

TASK:
• Define 2-4 progressive layers from MVP to full implementation
• L0 (MVP): Minimum viable closed loop - core path works end-to-end
• L1 (Usable): Critical user paths, basic error handling
• L2 (Complete): Edge cases, performance, security hardening
• L3 (Optimized): Advanced features, observability, operations support
• Each layer: explicit scope (included) and excludes (not included)
• Each layer: convergence with testable criteria, executable verification, business-language DoD
• Risk items per layer

MODE: analysis
CONTEXT: @**/*
EXPECTED:
For each layer output:
## L{n}: {Name}
**Goal**: {one sentence}
**Scope**: {comma-separated features}
**Excludes**: {comma-separated excluded features}
**Convergence**:
- Criteria: {bullet list of testable conditions}
- Verification: {executable command or steps}
- Definition of Done: {business language sentence}
**Risk Items**: {bullet list}
**Effort**: {small|medium|large}
**Depends On**: {layer IDs or none}

CONSTRAINTS:
- Each feature belongs to exactly ONE layer (no overlap)
- Criteria must be testable (can write assertions)
- Verification must be executable (commands or explicit steps)
- Definition of Done must be understandable by non-technical stakeholders
- L0 must be a complete closed loop (end-to-end path works)
" --tool gemini --mode analysis
```

##### Direct Mode CLI Template

```bash
ccw cli -p "
PURPOSE: Decompose requirement into topologically-sorted task sequence with convergence criteria
Success: Self-contained tasks with clear inputs/outputs, testable convergence, correct dependency order

REQUIREMENT:
${requirement}

STRATEGY CONTEXT:
- Goal: ${strategy.goal}
- Constraints: ${strategy.constraints.join(', ')}

${explorationContext ? `CODEBASE CONTEXT:
- Relevant modules: ${explorationContext.relevant_modules.map(m => m.name).join(', ')}
- Existing patterns: ${explorationContext.existing_patterns.map(p => p.pattern).join(', ')}
- Tech stack: ${JSON.stringify(explorationContext.tech_stack)}` : 'NO CODEBASE (pure requirement decomposition)'}

TASK:
• Decompose into vertical slices with clear boundaries
• Each task: type (infrastructure|feature|enhancement|testing)
• Each task: explicit inputs (what it needs) and outputs (what it produces)
• Each task: convergence with testable criteria, executable verification, business-language DoD
• Topological sort: respect dependency order
• Assign parallel_group numbers (same group = can run in parallel)

MODE: analysis
CONTEXT: @**/*
EXPECTED:
For each task output:
## T{n}: {Title}
**Type**: {infrastructure|feature|enhancement|testing}
**Scope**: {description}
**Inputs**: {comma-separated files/modules or 'none'}
**Outputs**: {comma-separated files/modules}
**Convergence**:
- Criteria: {bullet list of testable conditions}
- Verification: {executable command or steps}
- Definition of Done: {business language sentence}
**Depends On**: {task IDs or none}
**Parallel Group**: {number}

CONSTRAINTS:
- Inputs must come from preceding task outputs or existing resources
- No circular dependencies
- Criteria must be testable
- Verification must be executable
- Tasks in same parallel_group must be truly independent
" --tool gemini --mode analysis
```

##### CLI Fallback Chain

```javascript
// Fallback chain: Gemini → Qwen → manual decomposition
try {
  cliOutput = executeCLI('gemini', prompt)
} catch (error) {
  try {
    cliOutput = executeCLI('qwen', prompt)
  } catch {
    // Manual fallback (see Fallback Decomposition below)
    records = selectedMode === 'progressive'
      ? manualProgressiveDecomposition(requirement, explorationContext)
      : manualDirectDecomposition(requirement, explorationContext)
  }
}
```

##### CLI Output Parsing

```javascript
// Parse progressive layers from CLI output
function parseProgressiveLayers(cliOutput) {
  const layers = []
  const layerBlocks = cliOutput.split(/## L(\d+):/).slice(1)

  for (let i = 0; i < layerBlocks.length; i += 2) {
    const layerId = `L${layerBlocks[i].trim()}`
    const text = layerBlocks[i + 1]

    const nameMatch = /^(.+?)(?=\n)/.exec(text)
    const goalMatch = /\*\*Goal\*\*:\s*(.+?)(?=\n)/.exec(text)
    const scopeMatch = /\*\*Scope\*\*:\s*(.+?)(?=\n)/.exec(text)
    const excludesMatch = /\*\*Excludes\*\*:\s*(.+?)(?=\n)/.exec(text)
    const effortMatch = /\*\*Effort\*\*:\s*(.+?)(?=\n)/.exec(text)
    const dependsMatch = /\*\*Depends On\*\*:\s*(.+?)(?=\n|$)/.exec(text)
    const riskMatch = /\*\*Risk Items\*\*:\n((?:- .+?\n)*)/.exec(text)

    const convergence = parseConvergence(text)

    layers.push({
      id: layerId,
      name: nameMatch?.[1].trim() || `Layer ${layerId}`,
      goal: goalMatch?.[1].trim() || "",
      scope: scopeMatch?.[1].split(/[,，]/).map(s => s.trim()).filter(Boolean) || [],
      excludes: excludesMatch?.[1].split(/[,，]/).map(s => s.trim()).filter(Boolean) || [],
      convergence,
      risks: riskMatch
        ? riskMatch[1].split('\n').map(s => s.replace(/^- /, '').trim()).filter(Boolean)
            .map(desc => ({description: desc, probability: "Medium", impact: "Medium", mitigation: "N/A"}))
        : [],
      effort: normalizeEffort(effortMatch?.[1].trim()),
      depends_on: parseDependsOn(dependsMatch?.[1], 'L')
    })
  }

  return layers
}

// Parse direct tasks from CLI output
function parseDirectTasks(cliOutput) {
  const tasks = []
  const taskBlocks = cliOutput.split(/## T(\d+):/).slice(1)

  for (let i = 0; i < taskBlocks.length; i += 2) {
    const taskId = `T${taskBlocks[i].trim()}`
    const text = taskBlocks[i + 1]

    const titleMatch = /^(.+?)(?=\n)/.exec(text)
    const typeMatch = /\*\*Type\*\*:\s*(.+?)(?=\n)/.exec(text)
    const scopeMatch = /\*\*Scope\*\*:\s*(.+?)(?=\n)/.exec(text)
    const inputsMatch = /\*\*Inputs\*\*:\s*(.+?)(?=\n)/.exec(text)
    const outputsMatch = /\*\*Outputs\*\*:\s*(.+?)(?=\n)/.exec(text)
    const dependsMatch = /\*\*Depends On\*\*:\s*(.+?)(?=\n|$)/.exec(text)
    const groupMatch = /\*\*Parallel Group\*\*:\s*(\d+)/.exec(text)

    const convergence = parseConvergence(text)

    tasks.push({
      id: taskId,
      title: titleMatch?.[1].trim() || `Task ${taskId}`,
      type: normalizeType(typeMatch?.[1].trim()),
      scope: scopeMatch?.[1].trim() || "",
      inputs: parseList(inputsMatch?.[1]),
      outputs: parseList(outputsMatch?.[1]),
      convergence,
      depends_on: parseDependsOn(dependsMatch?.[1], 'T'),
      parallel_group: parseInt(groupMatch?.[1]) || 1
    })
  }

  return tasks
}

// Parse convergence section from a record block
function parseConvergence(text) {
  const criteriaMatch = /- Criteria:\s*((?:.+\n?)+?)(?=- Verification:)/.exec(text)
  const verificationMatch = /- Verification:\s*(.+?)(?=\n- Definition)/.exec(text)
  const dodMatch = /- Definition of Done:\s*(.+?)(?=\n\*\*|$)/.exec(text)

  const criteria = criteriaMatch
    ? criteriaMatch[1].split('\n')
        .map(s => s.replace(/^\s*[-•]\s*/, '').trim())
        .filter(s => s && !s.startsWith('Verification') && !s.startsWith('Definition'))
    : []

  return {
    criteria: criteria.length > 0 ? criteria : ["Task completed successfully"],
    verification: verificationMatch?.[1].trim() || "Manual verification",
    definition_of_done: dodMatch?.[1].trim() || "Feature works as expected"
  }
}

// Helpers
function normalizeEffort(effort) {
  if (!effort) return "medium"
  const lower = effort.toLowerCase()
  if (lower.includes('small') || lower.includes('low')) return "small"
  if (lower.includes('large') || lower.includes('high')) return "large"
  return "medium"
}

function normalizeType(type) {
  if (!type) return "feature"
  const lower = type.toLowerCase()
  if (lower.includes('infra')) return "infrastructure"
  if (lower.includes('enhance')) return "enhancement"
  if (lower.includes('test')) return "testing"
  return "feature"
}

function parseList(text) {
  if (!text || text.toLowerCase() === 'none') return []
  return text.split(/[,，]/).map(s => s.trim()).filter(Boolean)
}

function parseDependsOn(text, prefix) {
  if (!text || text.toLowerCase() === 'none' || text === '[]') return []
  const pattern = new RegExp(`${prefix}\\d+`, 'g')
  return (text.match(pattern) || [])
}
```

##### Fallback Decomposition

```javascript
// Manual decomposition when CLI fails
function manualProgressiveDecomposition(requirement, context) {
  return [
    {
      id: "L0", name: "MVP", goal: "最小可用闭环",
      scope: ["核心功能"], excludes: ["高级功能", "优化"],
      convergence: {
        criteria: ["核心路径端到端可跑通"],
        verification: "手动测试核心流程",
        definition_of_done: "用户可完成一次核心操作的完整流程"
      },
      risks: [{description: "技术选型待验证", probability: "Medium", impact: "Medium", mitigation: "待评估"}],
      effort: "medium", depends_on: []
    },
    {
      id: "L1", name: "可用", goal: "关键用户路径完善",
      scope: ["错误处理", "输入校验"], excludes: ["性能优化", "监控"],
      convergence: {
        criteria: ["所有用户输入有校验", "错误场景有提示"],
        verification: "单元测试 + 手动测试错误场景",
        definition_of_done: "用户遇到问题时有清晰的引导和恢复路径"
      },
      risks: [], effort: "medium", depends_on: ["L0"]
    }
  ]
}

function manualDirectDecomposition(requirement, context) {
  return [
    {
      id: "T1", title: "基础设施搭建", type: "infrastructure",
      scope: "项目骨架和基础配置",
      inputs: [], outputs: ["project-structure"],
      convergence: {
        criteria: ["项目可构建无报错", "基础配置完成"],
        verification: "npm run build (或对应构建命令)",
        definition_of_done: "项目基础框架就绪，可开始功能开发"
      },
      depends_on: [], parallel_group: 1
    },
    {
      id: "T2", title: "核心功能实现", type: "feature",
      scope: "核心业务逻辑",
      inputs: ["project-structure"], outputs: ["core-module"],
      convergence: {
        criteria: ["核心 API/功能可调用", "返回预期结果"],
        verification: "运行核心功能测试",
        definition_of_done: "核心业务功能可正常使用"
      },
      depends_on: ["T1"], parallel_group: 2
    }
  ]
}
```

---

#### Step 3.2: Record Enhancement & Validation

```javascript
// Validate progressive layers
function validateProgressiveLayers(layers) {
  const errors = []

  // Check scope overlap
  const allScopes = new Map()
  layers.forEach(layer => {
    layer.scope.forEach(feature => {
      if (allScopes.has(feature)) {
        errors.push(`Scope overlap: "${feature}" in both ${allScopes.get(feature)} and ${layer.id}`)
      }
      allScopes.set(feature, layer.id)
    })
  })

  // Check circular dependencies
  const cycleErrors = detectCycles(layers, 'L')
  errors.push(...cycleErrors)

  // Check convergence quality
  layers.forEach(layer => {
    errors.push(...validateConvergence(layer.id, layer.convergence))
  })

  // Check L0 is self-contained (no depends_on)
  const l0 = layers.find(l => l.id === 'L0')
  if (l0 && l0.depends_on.length > 0) {
    errors.push("L0 (MVP) should not have dependencies")
  }

  return errors
}

// Validate direct tasks
function validateDirectTasks(tasks) {
  const errors = []

  // Check inputs/outputs chain
  const availableOutputs = new Set()
  const sortedTasks = topologicalSort(tasks)

  sortedTasks.forEach(task => {
    task.inputs.forEach(input => {
      if (!availableOutputs.has(input)) {
        // Existing files are valid inputs - only warn
      }
    })
    task.outputs.forEach(output => availableOutputs.add(output))
  })

  // Check circular dependencies
  errors.push(...detectCycles(tasks, 'T'))

  // Check convergence quality
  tasks.forEach(task => {
    errors.push(...validateConvergence(task.id, task.convergence))
  })

  // Check parallel_group consistency
  const groups = new Map()
  tasks.forEach(task => {
    if (!groups.has(task.parallel_group)) groups.set(task.parallel_group, [])
    groups.get(task.parallel_group).push(task)
  })
  groups.forEach((groupTasks, groupId) => {
    if (groupTasks.length > 1) {
      const ids = new Set(groupTasks.map(t => t.id))
      groupTasks.forEach(task => {
        task.depends_on.forEach(dep => {
          if (ids.has(dep)) {
            errors.push(`Parallel group ${groupId}: ${task.id} depends on ${dep} but both in same group`)
          }
        })
      })
    }
  })

  return errors
}

// Validate convergence quality
function validateConvergence(recordId, convergence) {
  const errors = []

  const vaguePatterns = /正常|正确|好|可以|没问题|works|fine|good|correct/i
  convergence.criteria.forEach((criterion, i) => {
    if (vaguePatterns.test(criterion) && criterion.length < 15) {
      errors.push(`${recordId} criteria[${i}]: Too vague - "${criterion}"`)
    }
  })

  if (convergence.verification.length < 10) {
    errors.push(`${recordId} verification: Too short, needs executable steps`)
  }

  const technicalPatterns = /compile|build|lint|npm|npx|jest|tsc|eslint/i
  if (technicalPatterns.test(convergence.definition_of_done)) {
    errors.push(`${recordId} definition_of_done: Should be business language, not technical commands`)
  }

  return errors
}

// Detect circular dependencies
function detectCycles(records, prefix) {
  const errors = []
  const graph = new Map(records.map(r => [r.id, r.depends_on]))
  const visited = new Set()
  const inStack = new Set()

  function dfs(node, path) {
    if (inStack.has(node)) {
      errors.push(`Circular dependency detected: ${[...path, node].join(' → ')}`)
      return
    }
    if (visited.has(node)) return

    visited.add(node)
    inStack.add(node)
    ;(graph.get(node) || []).forEach(dep => dfs(dep, [...path, node]))
    inStack.delete(node)
  }

  records.forEach(r => {
    if (!visited.has(r.id)) dfs(r.id, [])
  })

  return errors
}

// Topological sort
function topologicalSort(tasks) {
  const result = []
  const visited = new Set()
  const taskMap = new Map(tasks.map(t => [t.id, t]))

  function visit(taskId) {
    if (visited.has(taskId)) return
    visited.add(taskId)
    const task = taskMap.get(taskId)
    if (task) {
      task.depends_on.forEach(dep => visit(dep))
      result.push(task)
    }
  }

  tasks.forEach(t => visit(t.id))
  return result
}
```

---

#### Step 3.3: Issue Creation & Output Generation

##### 3.3a: Internal Records → Issue Data Mapping

```javascript
// Progressive mode: layer → issue data (issues-jsonl-schema)
function layerToIssue(layer, sessionId, timestamp) {
  const context = `## Goal\n${layer.goal}\n\n` +
    `## Scope\n${layer.scope.map(s => `- ${s}`).join('\n')}\n\n` +
    `## Excludes\n${layer.excludes.map(s => `- ${s}`).join('\n') || 'None'}\n\n` +
    `## Convergence Criteria\n${layer.convergence.criteria.map(c => `- ${c}`).join('\n')}\n\n` +
    `## Verification\n${layer.convergence.verification}\n\n` +
    `## Definition of Done\n${layer.convergence.definition_of_done}\n\n` +
    (layer.risks.length ? `## Risks\n${layer.risks.map(r => `- ${r.description} (P:${r.probability} I:${r.impact})`).join('\n')}` : '')

  const effortToPriority = { small: 4, medium: 3, large: 2 }

  return {
    title: `[${layer.name}] ${layer.goal}`,
    context: context,
    priority: effortToPriority[layer.effort] || 3,
    source: "text",
    tags: ["req-plan", "progressive", layer.name.toLowerCase(), `wave-${getWaveNum(layer)}`],
    affected_components: [],
    extended_context: {
      notes: JSON.stringify({
        session: sessionId,
        strategy: "progressive",
        layer: layer.id,
        wave: getWaveNum(layer),
        effort: layer.effort,
        depends_on_issues: [],    // Backfilled after all issues created
        original_id: layer.id
      })
    },
    lifecycle_requirements: {
      test_strategy: "integration",
      regression_scope: "affected",
      acceptance_type: "automated",
      commit_strategy: "per-task"
    }
  }
}

function getWaveNum(layer) {
  const match = layer.id.match(/L(\d+)/)
  return match ? parseInt(match[1]) + 1 : 1
}

// Direct mode: task → issue data (issues-jsonl-schema)
function taskToIssue(task, sessionId, timestamp) {
  const context = `## Scope\n${task.scope}\n\n` +
    `## Inputs\n${task.inputs.length ? task.inputs.map(i => `- ${i}`).join('\n') : 'None (starting task)'}\n\n` +
    `## Outputs\n${task.outputs.map(o => `- ${o}`).join('\n')}\n\n` +
    `## Convergence Criteria\n${task.convergence.criteria.map(c => `- ${c}`).join('\n')}\n\n` +
    `## Verification\n${task.convergence.verification}\n\n` +
    `## Definition of Done\n${task.convergence.definition_of_done}`

  return {
    title: `[${task.type}] ${task.title}`,
    context: context,
    priority: 3,
    source: "text",
    tags: ["req-plan", "direct", task.type, `wave-${task.parallel_group}`],
    affected_components: task.outputs,
    extended_context: {
      notes: JSON.stringify({
        session: sessionId,
        strategy: "direct",
        task_id: task.id,
        wave: task.parallel_group,
        parallel_group: task.parallel_group,
        depends_on_issues: [],    // Backfilled after all issues created
        original_id: task.id
      })
    },
    lifecycle_requirements: {
      test_strategy: task.type === 'testing' ? 'unit' : 'integration',
      regression_scope: "affected",
      acceptance_type: "automated",
      commit_strategy: "per-task"
    }
  }
}
```

##### 3.3b: Create Issues via ccw issue create

```javascript
// Create issues sequentially (get formal ISS-xxx IDs)
const issueIdMap = {}  // originalId → ISS-xxx

for (const record of records) {
  const issueData = selectedMode === 'progressive'
    ? layerToIssue(record, sessionId, getUtc8ISOString())
    : taskToIssue(record, sessionId, getUtc8ISOString())

  // Create issue via ccw issue create
  try {
    const createResult = bash(`ccw issue create --data '${JSON.stringify(issueData)}' --json`)
    const created = JSON.parse(createResult.trim())
    issueIdMap[record.id] = created.id
  } catch (error) {
    // Retry once
    try {
      const retryResult = bash(`ccw issue create --data '${JSON.stringify(issueData)}' --json`)
      const created = JSON.parse(retryResult.trim())
      issueIdMap[record.id] = created.id
    } catch {
      // Log error, skip this record, continue with remaining
      console.error(`Failed to create issue for ${record.id}`)
    }
  }
}

// Backfill depends_on_issues into extended_context.notes
for (const record of records) {
  const issueId = issueIdMap[record.id]
  if (!issueId) continue
  const deps = record.depends_on.map(d => issueIdMap[d]).filter(Boolean)
  if (deps.length > 0) {
    const currentNotes = JSON.parse(issueData.extended_context.notes)
    currentNotes.depends_on_issues = deps
    bash(`ccw issue update ${issueId} --notes '${JSON.stringify(currentNotes)}'`)
  }
}
```

##### 3.3c: Generate execution-plan.json

```javascript
function generateExecutionPlan(records, issueIdMap, sessionId, requirement, selectedMode) {
  const issueIds = records.map(r => issueIdMap[r.id]).filter(Boolean)

  let waves
  if (selectedMode === 'progressive') {
    waves = records.filter(r => issueIdMap[r.id]).map((r, i) => ({
      wave: i + 1,
      label: r.name,
      issue_ids: [issueIdMap[r.id]],
      depends_on_waves: r.depends_on.length > 0
        ? [...new Set(r.depends_on.map(d => records.findIndex(x => x.id === d) + 1))]
        : []
    }))
  } else {
    const groups = new Map()
    records.filter(r => issueIdMap[r.id]).forEach(r => {
      const g = r.parallel_group
      if (!groups.has(g)) groups.set(g, [])
      groups.get(g).push(r)
    })

    waves = [...groups.entries()]
      .sort(([a], [b]) => a - b)
      .map(([groupNum, groupRecords]) => ({
        wave: groupNum,
        label: `Group ${groupNum}`,
        issue_ids: groupRecords.map(r => issueIdMap[r.id]),
        depends_on_waves: groupNum > 1 ? [groupNum - 1] : []
      }))
  }

  const issueDependencies = {}
  records.forEach(r => {
    if (!issueIdMap[r.id]) return
    const deps = r.depends_on.map(d => issueIdMap[d]).filter(Boolean)
    if (deps.length > 0) {
      issueDependencies[issueIdMap[r.id]] = deps
    }
  })

  return {
    session_id: sessionId,
    requirement: requirement,
    strategy: selectedMode,
    created_at: new Date().toISOString(),
    issue_ids: issueIds,
    waves: waves,
    issue_dependencies: issueDependencies
  }
}

const executionPlan = generateExecutionPlan(records, issueIdMap, sessionId, requirement, selectedMode)
Write(`${sessionFolder}/execution-plan.json`, JSON.stringify(executionPlan, null, 2))
```

##### 3.3d: Generate issues.jsonl Session Copy

```javascript
const sessionIssues = []
for (const originalId of Object.keys(issueIdMap)) {
  const issueId = issueIdMap[originalId]
  if (!issueId) continue
  const issueJson = bash(`ccw issue status ${issueId} --json`).trim()
  sessionIssues.push(issueJson)
}
Write(`${sessionFolder}/issues.jsonl`, sessionIssues.join('\n') + '\n')
```

##### 3.3e: Generate roadmap.md (with Issue ID References)

```javascript
// Progressive mode roadmap
function generateProgressiveRoadmapMd(layers, issueIdMap, input) {
  return `# 需求路线图

**Session**: ${input.sessionId}
**需求**: ${input.requirement}
**策略**: progressive
**不确定性**: ${input.strategy.uncertainty_level}
**生成时间**: ${new Date().toISOString()}

## 策略评估

- 目标: ${input.strategy.goal}
- 约束: ${input.strategy.constraints.join(', ') || '无'}
- 利益方: ${input.strategy.stakeholders.join(', ') || '无'}

## 路线图概览

| 层级 | 名称 | 目标 | 工作量 | 依赖 | Issue ID |
|------|------|------|--------|------|----------|
${layers.map(l => `| ${l.id} | ${l.name} | ${l.goal} | ${l.effort} | ${l.depends_on.length ? l.depends_on.join(', ') : '-'} | ${issueIdMap[l.id]} |`).join('\n')}

## Issue Mapping

| Wave | Issue ID | Title | Priority |
|------|----------|-------|----------|
${layers.map(l => `| ${getWaveNum(l)} | ${issueIdMap[l.id]} | [${l.name}] ${l.goal} | ${({small: 4, medium: 3, large: 2})[l.effort] || 3} |`).join('\n')}

## 各层详情

${layers.map(l => `### ${l.id}: ${l.name} (${issueIdMap[l.id]})

**目标**: ${l.goal}

**范围**: ${l.scope.join('、')}

**排除**: ${l.excludes.join('、') || '无'}

**收敛标准**:
${l.convergence.criteria.map(c => `- ${c}`).join('\n')}
- **验证方法**: ${l.convergence.verification}
- **完成定义**: ${l.convergence.definition_of_done}

**风险项**: ${l.risks.length ? l.risks.map(r => `\n- ${r.description} (概率: ${r.probability}, 影响: ${r.impact}, 缓解: ${r.mitigation})`).join('') : '无'}

**工作量**: ${l.effort}
`).join('\n---\n\n')}

## 风险汇总

${layers.flatMap(l => l.risks.map(r => `- **${l.id}** (${issueIdMap[l.id]}): ${r.description} (概率: ${r.probability}, 影响: ${r.impact})`)).join('\n') || '无已识别风险'}

## Next Steps

### 使用 team-planex 执行全部波次
\`\`\`
$team-planex --plan ${input.sessionFolder}/execution-plan.json
\`\`\`

### 按波次逐步执行
\`\`\`
${layers.map(l => `# Wave ${getWaveNum(l)}: ${l.name}\n$team-planex ${issueIdMap[l.id]}`).join('\n')}
\`\`\`

路线图文件: \`${input.sessionFolder}/\`
- issues.jsonl (标准 issue 格式)
- execution-plan.json (波次编排)
`
}

// Direct mode roadmap
function generateDirectRoadmapMd(tasks, issueIdMap, input) {
  const groups = new Map()
  tasks.forEach(t => {
    const g = t.parallel_group
    if (!groups.has(g)) groups.set(g, [])
    groups.get(g).push(t)
  })

  return `# 需求路线图

**Session**: ${input.sessionId}
**需求**: ${input.requirement}
**策略**: direct
**生成时间**: ${new Date().toISOString()}

## 策略评估

- 目标: ${input.strategy.goal}
- 约束: ${input.strategy.constraints.join(', ') || '无'}

## 任务序列

| 组 | ID | 标题 | 类型 | 依赖 | Issue ID |
|----|-----|------|------|------|----------|
${tasks.map(t => `| ${t.parallel_group} | ${t.id} | ${t.title} | ${t.type} | ${t.depends_on.length ? t.depends_on.join(', ') : '-'} | ${issueIdMap[t.id]} |`).join('\n')}

## Issue Mapping

| Wave | Issue ID | Title | Priority |
|------|----------|-------|----------|
${tasks.map(t => `| ${t.parallel_group} | ${issueIdMap[t.id]} | [${t.type}] ${t.title} | 3 |`).join('\n')}

## 各任务详情

${tasks.map(t => `### ${t.id}: ${t.title} (${issueIdMap[t.id]})

**类型**: ${t.type} | **并行组**: ${t.parallel_group}

**范围**: ${t.scope}

**输入**: ${t.inputs.length ? t.inputs.join(', ') : '无（起始任务）'}
**输出**: ${t.outputs.join(', ')}

**收敛标准**:
${t.convergence.criteria.map(c => `- ${c}`).join('\n')}
- **验证方法**: ${t.convergence.verification}
- **完成定义**: ${t.convergence.definition_of_done}
`).join('\n---\n\n')}

## Next Steps

### 使用 team-planex 执行全部波次
\`\`\`
$team-planex --plan ${input.sessionFolder}/execution-plan.json
\`\`\`

### 按波次逐步执行
\`\`\`
${[...groups.entries()].sort(([a], [b]) => a - b).map(([g, ts]) =>
  `# Wave ${g}: Group ${g}\n$team-planex ${ts.map(t => issueIdMap[t.id]).join(' ')}`
).join('\n')}
\`\`\`

路线图文件: \`${input.sessionFolder}/\`
- issues.jsonl (标准 issue 格式)
- execution-plan.json (波次编排)
`
}

// Write roadmap.md
const roadmapInput = {
  sessionId, requirement, sessionFolder,
  strategy: { ...strategy }
}
const roadmapMd = selectedMode === 'progressive'
  ? generateProgressiveRoadmapMd(records, issueIdMap, roadmapInput)
  : generateDirectRoadmapMd(records, issueIdMap, roadmapInput)
Write(`${sessionFolder}/roadmap.md`, roadmapMd)
```

---

#### Step 3.4: Decomposition Quality Check (MANDATORY)

After creating issues and generating output files, **MUST** execute CLI quality check before proceeding.

##### Quality Dimensions

| Dimension | Check Criteria | Critical? |
|-----------|---------------|-----------|
| **Requirement Coverage** | All aspects of original requirement addressed in issues | Yes |
| **Convergence Quality** | criteria testable, verification executable, DoD business-readable | Yes |
| **Scope Integrity** | Progressive: no overlap/gaps; Direct: inputs/outputs chain valid | Yes |
| **Dependency Correctness** | No circular deps, proper ordering, issue dependencies match | Yes |
| **Effort Balance** | No single issue disproportionately large | No |

##### CLI Quality Check

```bash
ccw cli -p "
PURPOSE: Validate roadmap decomposition quality
Success: All quality dimensions pass

ORIGINAL REQUIREMENT:
${requirement}

ISSUES CREATED (${selectedMode} mode):
${issuesJsonlContent}

EXECUTION PLAN:
${JSON.stringify(executionPlan, null, 2)}

TASK:
• Requirement Coverage: Does the decomposition address ALL aspects of the requirement?
• Convergence Quality: Are criteria testable? Is verification executable? Is DoD business-readable?
• Scope Integrity: ${selectedMode === 'progressive' ? 'No scope overlap between layers, no feature gaps' : 'Inputs/outputs chain is valid, parallel groups are correct'}
• Dependency Correctness: No circular dependencies, wave ordering correct
• Effort Balance: No disproportionately large items

MODE: analysis
EXPECTED:
## Quality Check Results
### Requirement Coverage: PASS|FAIL
[details]
### Convergence Quality: PASS|FAIL
[details and specific issues per record]
### Scope Integrity: PASS|FAIL
[details]
### Dependency Correctness: PASS|FAIL
[details]
### Effort Balance: PASS|FAIL
[details]

## Recommendation: PASS|AUTO_FIX|NEEDS_REVIEW
## Fixes (if AUTO_FIX):
[specific fixes as JSON patches]

CONSTRAINTS: Read-only validation, do not modify files
" --tool gemini --mode analysis
```

##### Auto-Fix Strategy

| Issue Type | Auto-Fix Action |
|-----------|----------------|
| Vague criteria | Replace with specific, testable conditions |
| Technical DoD | Rewrite in business language |
| Missing scope items | Add to appropriate issue context |
| Effort imbalance | Suggest split (report to user) |

After fixes, update issues via `ccw issue update` and regenerate `issues.jsonl` + `roadmap.md`.

---

### Phase 4: Validation & team-planex Handoff

**Objective**: Display decomposition results, collect user feedback, provide team-planex execution options.

```javascript
// 1. Display Decomposition Results
const executionPlan = JSON.parse(Read(`${sessionFolder}/execution-plan.json`))
const issueIds = executionPlan.issue_ids
const waves = executionPlan.waves
```

**Progressive Mode** display:
```markdown
## Roadmap Overview

| Wave | Issue ID | Name | Goal | Priority |
|------|----------|------|------|----------|
| 1 | ISS-xxx | MVP | ... | 2 |
| 2 | ISS-yyy | Usable | ... | 3 |

### Convergence Criteria
**Wave 1 - MVP (ISS-xxx)**:
- Criteria: [criteria list]
- Verification: [verification]
- Definition of Done: [definition_of_done]
```

**Direct Mode** display:
```markdown
## Task Sequence

| Wave | Issue ID | Title | Type | Dependencies |
|------|----------|-------|------|--------------|
| 1 | ISS-xxx | ... | infrastructure | - |
| 2 | ISS-yyy | ... | feature | ISS-xxx |
```

#### User Feedback Loop (up to 5 rounds, skipped when AUTO_YES)

```javascript
if (!AUTO_YES) {
  let round = 0
  let continueLoop = true

  while (continueLoop && round < 5) {
    round++
    const feedback = ASK_USER([
      {
        id: "feedback", type: "select",
        prompt: `Roadmap validation (round ${round}):\nAny feedback on the current decomposition?`,
        options: [
          { label: "Approve", description: "Decomposition is reasonable, proceed to next steps" },
          { label: "Adjust Scope", description: "Some issue scopes need adjustment" },
          { label: "Modify Convergence", description: "Convergence criteria are not specific or testable enough" },
          { label: "Re-decompose", description: "Overall strategy or layering approach needs change" }
        ]
      }
    ])  // BLOCKS (wait for user response)

    if (feedback.feedback === 'Approve') {
      continueLoop = false
    } else {
      // Handle adjustment based on feedback type
      // After adjustment, re-display and return to loop top
    }
  }
}
```

#### Post-Completion Options

```javascript
if (AUTO_YES) {
  // Auto mode: display summary and end
  console.log(`路线图已生成，${issueIds.length} 个 issues 已创建。`)
  console.log(`Session: ${sessionFolder}`)
} else {
  const nextStep = ASK_USER([
    {
      id: "next", type: "select",
      prompt: `路线图已生成，${issueIds.length} 个 issues 已创建。下一步：`,
      options: [
        { label: "Execute with team-planex",
          description: `启动 team-planex 执行全部 ${issueIds.length} 个 issues（${waves.length} 个波次）` },
        { label: "Execute first wave",
          description: `仅执行 Wave 1: ${waves[0].label}` },
        { label: "View issues",
          description: "查看已创建的 issue 详情" },
        { label: "Done",
          description: "保存路线图，稍后执行" }
      ]
    }
  ])  // BLOCKS (wait for user response)
}
```

| Selection | Action |
|-----------|--------|
| Execute with team-planex | `$team-planex --plan ${sessionFolder}/execution-plan.json` |
| Execute first wave | `$team-planex ${waves[0].issue_ids.join(' ')}` |
| View issues | Display issues summary table from issues.jsonl |
| Done | Display file paths, end |

> **Implementation sketch**: 编排器内部使用 `Skill(skill="team-planex", args="--plan ...")` 接口调用，
> 此为伪代码示意，非命令行语法。

---

## JSONL Schema Design

### Issue Format (issues.jsonl)

Each line follows the standard `issues-jsonl-schema.json` (see `.ccw/workflows/cli-templates/schemas/issues-jsonl-schema.json`).

| Field | Source | Description |
|-------|--------|-------------|
| `id` | `ccw issue create` | Formal ISS-YYYYMMDD-NNN ID |
| `title` | Layer/task mapping | `[LayerName] goal` or `[TaskType] title` |
| `context` | Convergence fields | Markdown with goal, scope, convergence criteria, verification, DoD |
| `priority` | Effort mapping | small→4, medium→3, large→2 |
| `source` | Fixed | `"text"` |
| `tags` | Auto-generated | `["req-plan", mode, name/type, "wave-N"]` |
| `extended_context.notes` | Metadata JSON | session, strategy, original_id, wave, depends_on_issues |
| `lifecycle_requirements` | Fixed | test_strategy, regression_scope, acceptance_type, commit_strategy |

### Execution Plan Format (execution-plan.json)

```json
{
  "session_id": "RPLAN-{slug}-{date}",
  "requirement": "Original requirement description",
  "strategy": "progressive|direct",
  "created_at": "ISO 8601",
  "issue_ids": ["ISS-xxx", "ISS-yyy"],
  "waves": [
    {
      "wave": 1,
      "label": "MVP",
      "issue_ids": ["ISS-xxx"],
      "depends_on_waves": []
    },
    {
      "wave": 2,
      "label": "Usable",
      "issue_ids": ["ISS-yyy"],
      "depends_on_waves": [1]
    }
  ],
  "issue_dependencies": {
    "ISS-yyy": ["ISS-xxx"]
  }
}
```

**Wave mapping**:
- Progressive mode: each layer → one wave (L0→Wave 1, L1→Wave 2, ...)
- Direct mode: each parallel_group → one wave (group 1→Wave 1, group 2→Wave 2, ...)

---

## Session Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `-y, --yes` | false | Auto-confirm all decisions |
| `-c, --continue` | false | Continue existing session |
| `-m, --mode` | auto | Decomposition strategy: progressive / direct / auto |

**Session ID format**: `RPLAN-{slug}-{YYYY-MM-DD}`
- slug: lowercase, alphanumeric + CJK characters, max 40 chars
- date: YYYY-MM-DD (UTC+8)

---

## Error Handling

| Error | Resolution |
|-------|------------|
| cli-explore-agent timeout | Retry once with send_input prompt, then skip exploration |
| cli-explore-agent failure | Skip code exploration, proceed with pure requirement decomposition |
| No codebase | Normal flow, skip Phase 2 |
| CLI decomposition failure (Gemini) | Fallback to Qwen, then manual decomposition |
| Issue creation failure | Retry once, then skip and continue with remaining |
| Circular dependency detected | Prompt user to adjust dependencies, re-decompose |
| User feedback timeout | Save current state, display `--continue` recovery command |
| Max feedback rounds reached | Use current version to generate final artifacts |
| Session folder conflict | Append timestamp suffix |
| Quality check NEEDS_REVIEW | Report critical issues to user for manual resolution |

## Core Rules

1. **Explicit Lifecycle**: Always close_agent after wait completes to free resources
2. **DO NOT STOP**: Continuous multi-phase workflow. After completing each phase, immediately proceed to next
3. **NEVER output vague convergence**: criteria must be testable, verification executable, DoD in business language
4. **NEVER skip quality check**: Step 3.4 is MANDATORY before proceeding to Phase 4
5. **ALWAYS write all three output files**: issues.jsonl, execution-plan.json, roadmap.md

## Best Practices

1. **Clear requirement description**: Detailed description → more accurate uncertainty assessment and decomposition
2. **Validate MVP first**: In progressive mode, L0 should be the minimum verifiable closed loop
3. **Testable convergence**: criteria must be writable as assertions or manual steps; definition_of_done should be judgeable by non-technical stakeholders
4. **Incremental validation**: Use `--continue` to iterate on existing roadmaps
5. **team-planex integration**: Issues created follow standard issues-jsonl-schema, directly consumable by `$team-planex` via execution-plan.json

## Usage Recommendations

**Use `$workflow-req-plan` when:**
- You need to decompose a large requirement into a progressively executable roadmap
- Unsure where to start, need an MVP strategy
- Need to generate a trackable task sequence
- Requirement involves multiple stages or iterations
- Want automatic issue creation + team-planex execution pipeline

**Use `$workflow-lite-plan` when:**
- You have a clear single task to execute
- The requirement is already a layer/task from the roadmap
- No layered planning needed

**Use `$team-planex` directly when:**
- Issues already exist (created manually or from other workflows)
- Have an execution-plan.json ready from a previous req-plan session

---

**Now execute req-plan workflow for**: $ARGUMENTS
