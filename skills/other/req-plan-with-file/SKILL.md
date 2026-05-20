---
name: req-plan-with-file
description: Requirement-level progressive roadmap planning with JSONL output. Decomposes requirements into convergent layers (MVP→iterations) or topologically-sorted task sequences, each with testable completion criteria.
argument-hint: "[-y|--yes] [-c|--continue] [-m|--mode progressive|direct|auto] \"requirement description\""
---

# Codex Req-Plan-With-File Prompt

## Overview

Requirement-level roadmap planning with **JSONL output and convergence criteria**. Decomposes a requirement into self-contained layers or tasks, each with testable completion criteria, independently executable via `lite-plan`.

**Core workflow**: Requirement Understanding → Strategy Selection → Context Collection (optional) → Decomposition → Validation → Quality Check → Output

**Dual modes**:
- **Progressive**: Layered MVP→iterations, suitable for high-uncertainty requirements (validate first, then refine)
- **Direct**: Topologically-sorted task sequence, suitable for low-uncertainty requirements (clear tasks, directly ordered)
- **Auto**: Automatically selects based on uncertainty assessment

## Auto Mode

When `--yes` or `-y`: Auto-confirm strategy selection, use recommended mode, skip interactive validation rounds.

## Quick Start

```bash
# Basic usage
/codex:req-plan-with-file "Implement user authentication system with OAuth and 2FA"

# With mode selection
/codex:req-plan-with-file -m progressive "Build real-time notification system"
/codex:req-plan-with-file -m direct "Refactor payment module"
/codex:req-plan-with-file -m auto "Add data export feature"

# Continue existing session
/codex:req-plan-with-file --continue "user authentication system"

# Auto mode (skip all confirmations)
/codex:req-plan-with-file -y "Implement caching layer"
```

## Target Requirement

**$ARGUMENTS**

## Execution Process

```
Step 0: Session Setup
   ├─ Parse flags (-y, -c, -m) and requirement text
   ├─ Generate session ID: RPLAN-{slug}-{date}
   └─ Create session folder (or detect existing → continue mode)

Step 1: Parse Requirement & Select Strategy
   ├─ Extract goal, constraints, stakeholders, domain keywords
   ├─ Assess uncertainty (5 dimensions)
   ├─ Select mode: progressive / direct
   ├─ Write strategy-assessment.json
   └─ Initialize roadmap.md skeleton

Step 2: Explore Codebase (Optional)
   ├─ Detect project markers (package.json, go.mod, etc.)
   ├─ Has codebase → search relevant modules, patterns, integration points
   │   ├─ Read project-tech.json / project-guidelines.json (if exists)
   │   ├─ Search modules/components related to the requirement
   │   └─ Write exploration-codebase.json
   └─ No codebase → skip

Step 3: Decompose Requirement → roadmap.jsonl
   ├─ Step 3.1: Build decomposition (requirement + strategy + context)
   │   ├─ Generate JSONL records with convergence criteria
   │   └─ Apply convergence quality requirements
   ├─ Step 3.2: Validate records
   │   ├─ Schema compliance, scope integrity
   │   ├─ No circular dependencies (topological sort)
   │   ├─ Convergence quality (testable criteria, executable verification, business DoD)
   │   └─ Write roadmap.jsonl
   └─ Step 3.3: Quality check (MANDATORY)
       ├─ Requirement coverage, convergence quality, scope integrity
       ├─ Dependency correctness, effort balance
       └─ Auto-fix or report issues

Step 4: Validate & Finalize → roadmap.md
   ├─ Display decomposition (tabular + convergence details)
   ├─ User feedback loop (up to 5 rounds, skip if -y)
   ├─ Write final roadmap.md
   └─ Next step options: lite-plan / issue / export / done
```

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `-y, --yes` | false | Auto-confirm all decisions |
| `-c, --continue` | false | Continue existing session |
| `-m, --mode` | auto | Decomposition strategy: progressive / direct / auto |

**Session ID format**: `RPLAN-{slug}-{YYYY-MM-DD}`
- slug: lowercase, alphanumeric + CJK characters, max 40 chars
- date: YYYY-MM-DD (UTC+8)
- Auto-detect continue: session folder + roadmap.jsonl exists → continue mode

## Implementation Details

### Session Setup

##### Step 0: Initialize Session

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const continueMode = $ARGUMENTS.includes('--continue') || $ARGUMENTS.includes('-c')
const modeMatch = $ARGUMENTS.match(/(?:--mode|-m)\s+(progressive|direct|auto)/)
const requestedMode = modeMatch ? modeMatch[1] : 'auto'

// Clean requirement text
const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|-c|--mode\s+\w+|-m\s+\w+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10)
const sessionId = `RPLAN-${slug}-${dateStr}`
const sessionFolder = `.workflow/.req-plan/${sessionId}`

// Auto-detect continue: session folder + roadmap.jsonl exists → continue mode
// If continue → skip to Step 4 (load existing roadmap.jsonl, display, collect feedback)
Bash(`mkdir -p ${sessionFolder}`)
```

### Phase 1: Parse Requirement & Select Strategy

**Objective**: Parse requirement, assess uncertainty, select decomposition strategy.

##### Step 1.1: Analyze Requirement & Select Strategy

Parse the requirement, evaluate uncertainty across 5 dimensions, and select decomposition strategy in one step:

```javascript
// 1. Extract from requirement text
const goal = extractCoreGoal(requirement)       // What to achieve
const constraints = extractConstraints(requirement) // Tech stack, timeline, compatibility
const stakeholders = extractStakeholders(requirement) // Users, admins, developers
const domainKeywords = extractDomainKeywords(requirement) // Domain-specific terms

// 2. Assess uncertainty (each: low | medium | high)
const uncertaintyFactors = {
  scope_clarity: '...',       // Is scope well-defined?
  technical_risk: '...',      // Known tech vs experimental?
  dependency_unknown: '...',  // Are dependencies clear?
  domain_familiarity: '...',  // Team knows this domain?
  requirement_stability: '...' // Will requirements change?
}
// >=3 high → progressive, >=3 low → direct, otherwise → ask

// 3. Select strategy
let selectedMode
if (requestedMode !== 'auto') {
  selectedMode = requestedMode
} else if (autoYes) {
  selectedMode = recommendedMode
} else {
  AskUserQuestion({
    questions: [{
      question: `Decomposition strategy selection:\n\nUncertainty assessment: ${uncertaintyLevel}\nRecommended strategy: ${recommendedMode}\n\nSelect decomposition strategy:`,
      header: "Strategy",
      multiSelect: false,
      options: [
        {
          label: recommendedMode === 'progressive' ? "Progressive (Recommended)" : "Progressive",
          description: "Layered MVP→iterations, validate core first then refine progressively. Suitable for high-uncertainty requirements needing quick validation"
        },
        {
          label: recommendedMode === 'direct' ? "Direct (Recommended)" : "Direct",
          description: "Topologically-sorted task sequence with explicit dependencies. Suitable for clear requirements with confirmed technical approach"
        }
      ]
    }]
  })
}

// 4. Write strategy assessment
Write(`${sessionFolder}/strategy-assessment.json`, JSON.stringify({
  session_id: sessionId,
  requirement, timestamp: getUtc8ISOString(),
  uncertainty_factors: uncertaintyFactors,
  uncertainty_level: uncertaintyLevel,
  recommended_mode: recommendedMode,
  selected_mode: selectedMode,
  goal, constraints, stakeholders,
  domain_keywords: domainKeywords
}, null, 2))

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
- Assessment basis: ${Object.entries(uncertaintyFactors).map(([k,v]) => `${k}=${v}`).join(', ')}

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
- Requirement goal, constraints, stakeholders, domain keywords identified
- Uncertainty level assessed across 5 dimensions
- Strategy selected (progressive or direct)
- strategy-assessment.json generated
- roadmap.md skeleton initialized

### Phase 2: Explore Codebase (Optional)

**Objective**: If a codebase exists, collect relevant context to enhance decomposition quality.

##### Step 2.1: Detect & Explore

If a codebase exists, directly search for relevant context. No agent delegation — use search tools inline.

```javascript
const hasCodebase = Bash(`
  test -f package.json && echo "nodejs" ||
  test -f go.mod && echo "golang" ||
  test -f Cargo.toml && echo "rust" ||
  test -f pyproject.toml && echo "python" ||
  test -f pom.xml && echo "java" ||
  test -d src && echo "generic" ||
  echo "none"
`).trim()

if (hasCodebase !== 'none') {
  // 1. Read project metadata (if exists)
  //    - .workflow/project-tech.json (tech stack info)
  //    - .workflow/project-guidelines.json (project conventions)

  // 2. Search codebase for modules related to the requirement
  //    Use: Grep, Glob, Read, or mcp__ace-tool__search_context
  //    Focus on:
  //      - Modules/components related to the requirement
  //      - Existing patterns to follow
  //      - Integration points for new functionality
  //      - Architecture constraints

  // 3. Write findings to exploration-codebase.json:
  Write(`${sessionFolder}/exploration-codebase.json`, JSON.stringify({
    project_type: hasCodebase,
    relevant_modules: [...],      // [{name, path, relevance}]
    existing_patterns: [...],     // [{pattern, files, description}]
    integration_points: [...],    // [{location, description, risk}]
    architecture_constraints: [...],
    tech_stack: {languages, frameworks, tools},
    _metadata: {timestamp: getUtc8ISOString(), exploration_scope: '...'}
  }, null, 2))
}
// No codebase → skip, proceed to Phase 3
```

**Success Criteria**:
- Codebase detection complete
- When codebase exists, exploration-codebase.json generated with relevant modules, patterns, integration points
- When no codebase, skipped and proceed to Phase 3

### Phase 3: Decompose Requirement

**Objective**: Execute requirement decomposition, generating validated roadmap.jsonl.

##### Step 3.1: Generate JSONL Records

Directly decompose the requirement into JSONL records based on the selected mode. Analyze the requirement yourself and produce the records, referencing strategy assessment and codebase context (if available).

```javascript
// Load context
const strategy = JSON.parse(Read(`${sessionFolder}/strategy-assessment.json`))
let explorationContext = null
if (file_exists(`${sessionFolder}/exploration-codebase.json`)) {
  explorationContext = JSON.parse(Read(`${sessionFolder}/exploration-codebase.json`))
}
```

**Progressive mode** — generate 2-4 layers:

```javascript
// Each layer must have:
// - id: L0, L1, L2, L3
// - title: "MVP" / "Usable" / "Refined" / "Optimized"
// - description: what this layer achieves (goal)
// - type: feature (default for layers)
// - priority: high (L0) | medium (L1) | low (L2-L3)
// - scope[]: features included
// - excludes[]: features explicitly deferred
// - convergence: { criteria[], verification, definition_of_done }
// - risk_items[], effort (small|medium|large), depends_on[]
// - source: { tool, session_id, original_id }
//
// Rules:
// - L0 (MVP) = self-contained closed loop, no dependencies
// - Each feature in exactly ONE layer (no overlap)
// - 2-4 layers total
// - Convergence MUST satisfy quality requirements (see below)

const layers = [
  {
    id: "L0", title: "MVP",
    description: "...",
    type: "feature", priority: "high",
    scope: ["..."], excludes: ["..."],
    convergence: {
      criteria: ["... (testable)"],
      verification: "... (executable command or steps)",
      definition_of_done: "... (business language)"
    },
    risk_items: [], effort: "medium", depends_on: [],
    source: { tool: "req-plan-with-file", session_id: sessionId, original_id: "L0" }
  },
  // L1, L2, ...
]
```

**Direct mode** — generate topologically-sorted tasks:

```javascript
// Each task must have:
// - id: T1, T2, ...
// - title, description, type (infrastructure|feature|enhancement|testing)
// - priority (high|medium|low)
// - scope, inputs[], outputs[]
// - convergence: { criteria[], verification, definition_of_done }
// - depends_on[], parallel_group
// - source: { tool, session_id, original_id }
//
// Rules:
// - Inputs must come from preceding task outputs or existing resources
// - Same parallel_group = truly independent
// - No circular dependencies
// - Convergence MUST satisfy quality requirements (see below)

const tasks = [
  {
    id: "T1", title: "...", description: "...", type: "infrastructure",
    priority: "high",
    scope: "...", inputs: [], outputs: ["..."],
    convergence: {
      criteria: ["... (testable)"],
      verification: "... (executable)",
      definition_of_done: "... (business language)"
    },
    depends_on: [], parallel_group: 1,
    source: { tool: "req-plan-with-file", session_id: sessionId, original_id: "T1" }
  },
  // T2, T3, ...
]
```

##### Step 3.2: Validate Records

Validate all records before writing JSONL. Fix any issues found.

```javascript
const items = selectedMode === 'progressive' ? layers : tasks
const errors = []

// 1. Schema validation: each record has convergence with all 3 fields
items.forEach(item => {
  if (!item.convergence?.criteria?.length) errors.push(`${item.id}: missing convergence.criteria`)
  if (!item.convergence?.verification) errors.push(`${item.id}: missing convergence.verification`)
  if (!item.convergence?.definition_of_done) errors.push(`${item.id}: missing convergence.definition_of_done`)
})

// 2. Convergence quality check
const vaguePatterns = /正常|正确|好|可以|没问题|works|fine|good|correct/i
items.forEach(item => {
  item.convergence.criteria.forEach((criterion, i) => {
    if (vaguePatterns.test(criterion) && criterion.length < 15) {
      errors.push(`${item.id} criteria[${i}]: Too vague - "${criterion}"`)
    }
  })
  if (item.convergence.verification.length < 10) {
    errors.push(`${item.id} verification: Too short, needs executable steps`)
  }
  const technicalPatterns = /compile|build|lint|npm|npx|jest|tsc|eslint/i
  if (technicalPatterns.test(item.convergence.definition_of_done)) {
    errors.push(`${item.id} definition_of_done: Should be business language, not technical commands`)
  }
})

// 3. Circular dependency detection
function detectCycles(records, prefix) {
  const graph = new Map(records.map(r => [r.id, r.depends_on]))
  const visited = new Set(), inStack = new Set(), cycleErrors = []
  function dfs(node, path) {
    if (inStack.has(node)) { cycleErrors.push(`Circular: ${[...path, node].join(' → ')}`); return }
    if (visited.has(node)) return
    visited.add(node); inStack.add(node)
    ;(graph.get(node) || []).forEach(dep => dfs(dep, [...path, node]))
    inStack.delete(node)
  }
  records.forEach(r => { if (!visited.has(r.id)) dfs(r.id, []) })
  return cycleErrors
}
errors.push(...detectCycles(items, selectedMode === 'progressive' ? 'L' : 'T'))

// 4. Mode-specific validation
if (selectedMode === 'progressive') {
  // Check 2-4 layers
  if (items.length < 2 || items.length > 4) errors.push(`Expected 2-4 layers, got ${items.length}`)

  // Check L0 is self-contained (no depends_on)
  const l0 = items.find(l => l.id === 'L0')
  if (l0 && l0.depends_on.length > 0) errors.push("L0 (MVP) should not have dependencies")

  // Check scope overlap
  const allScopes = new Map()
  items.forEach(layer => {
    layer.scope.forEach(feature => {
      if (allScopes.has(feature)) {
        errors.push(`Scope overlap: "${feature}" in both ${allScopes.get(feature)} and ${layer.id}`)
      }
      allScopes.set(feature, layer.id)
    })
  })
} else {
  // Check inputs/outputs chain
  const availableOutputs = new Set()
  items.forEach(task => {
    task.inputs.forEach(input => {
      if (!availableOutputs.has(input)) {
        // Only warn for non-existing resources - existing files are valid inputs
      }
    })
    task.outputs.forEach(output => availableOutputs.add(output))
  })

  // Check parallel_group consistency (same group tasks should not depend on each other)
  const groups = new Map()
  items.forEach(task => {
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
}

// 5. Fix errors if any, then write
// If errors found → fix records and re-validate
// Write roadmap.jsonl (one JSON record per line)
const jsonlContent = items.map(item => JSON.stringify(item)).join('\n')
Write(`${sessionFolder}/roadmap.jsonl`, jsonlContent)
```

##### Step 3.3: Quality Check (MANDATORY)

After generating roadmap.jsonl, execute a self-check across 5 quality dimensions before proceeding.

```javascript
const roadmapJsonlContent = Read(`${sessionFolder}/roadmap.jsonl`)

// Quality dimensions to verify:
//
// | Dimension              | Check Criteria                                              | Critical? |
// |------------------------|-------------------------------------------------------------|-----------|
// | Requirement Coverage   | All aspects of original requirement addressed in layers/tasks | Yes       |
// | Convergence Quality    | criteria testable, verification executable, DoD business-readable | Yes   |
// | Scope Integrity        | Progressive: no overlap/gaps; Direct: inputs/outputs chain valid | Yes    |
// | Dependency Correctness | No circular deps, proper ordering                           | Yes       |
// | Effort Balance         | No single layer/task disproportionately large               | No        |
//
// Decision after check:
// - PASS → proceed to Phase 4
// - AUTO_FIX → fix convergence wording, rebalance scope, update roadmap.jsonl
// - NEEDS_REVIEW → report issues to user in Phase 4 feedback

// Auto-fix strategy:
// | Issue Type      | Auto-Fix Action                              |
// |-----------------|----------------------------------------------|
// | Vague criteria  | Replace with specific, testable conditions    |
// | Technical DoD   | Rewrite in business language                  |
// | Missing scope   | Add to appropriate layer/task                 |
// | Effort imbalance| Split oversized layer/task                    |

// After auto-fixes, update roadmap.jsonl
```

**Success Criteria**:
- roadmap.jsonl generated, each line independently JSON.parse-able
- Each record contains convergence (criteria + verification + definition_of_done)
- Quality check passed (all critical dimensions)
- No circular dependencies
- Progressive: 2-4 layers, no scope overlap, L0 self-contained
- Direct: tasks have explicit inputs/outputs, parallel_group assigned correctly

### Phase 4: Validate & Finalize

**Objective**: Display decomposition results, collect user feedback, generate final artifacts.

##### Step 4.1: Display Results & Collect Feedback

Display the decomposition as a table with convergence criteria, then run feedback loop.

**Progressive Mode display format**:

```markdown
## Roadmap Overview

| Layer | Title | Description | Effort | Dependencies |
|-------|-------|-------------|--------|--------------|
| L0 | MVP | ... | medium | - |
| L1 | Usable | ... | medium | L0 |

### Convergence Criteria
**L0 - MVP**:
- Criteria: [criteria list]
- Verification: [verification]
- Definition of Done: [definition_of_done]
```

**Direct Mode display format**:

```markdown
## Task Sequence

| Group | ID | Title | Type | Description | Dependencies |
|-------|----|-------|------|-------------|--------------|
| 1 | T1 | ... | infrastructure | ... | - |
| 2 | T2 | ... | feature | ... | T1 |

### Convergence Criteria
**T1 - Establish Data Model**:
- Criteria: [criteria list]
- Verification: [verification]
- Definition of Done: [definition_of_done]
```

**Feedback loop**:

```javascript
const items = Read(`${sessionFolder}/roadmap.jsonl`)
  .split('\n').filter(l => l.trim()).map(l => JSON.parse(l))

// Display tabular results + convergence for each item (using format above)

if (!autoYes) {
  let round = 0, continueLoop = true
  while (continueLoop && round < 5) {
    round++
    const feedback = AskUserQuestion({
      questions: [{
        question: `Roadmap validation (round ${round}):\nAny feedback on the current decomposition?`,
        header: "Feedback",
        multiSelect: false,
        options: [
          { label: "Approve", description: "Decomposition is reasonable, generate final artifacts" },
          { label: "Adjust Scope", description: "Some layer/task scopes need adjustment" },
          { label: "Modify Convergence", description: "Convergence criteria not specific enough" },
          { label: "Re-decompose", description: "Overall strategy or layering needs change" }
        ]
      }]
    })
    if (feedback === 'Approve') continueLoop = false
    // else: apply adjustment, re-write roadmap.jsonl, re-display, loop
  }
}
```

##### Step 4.2: Write roadmap.md & Next Steps

Generate final roadmap.md using the generation templates below, then provide post-completion options.

**Progressive mode roadmap.md generation**:

```javascript
const roadmapMd = `# Requirement Roadmap

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Strategy**: progressive
**Uncertainty**: ${strategy.uncertainty_level}
**Generated**: ${getUtc8ISOString()}

## Strategy Assessment
- Uncertainty level: ${strategy.uncertainty_level}
- Decomposition mode: progressive
- Assessment basis: ${Object.entries(strategy.uncertainty_factors).map(([k,v]) => `${k}=${v}`).join(', ')}
- Goal: ${strategy.goal}
- Constraints: ${strategy.constraints.join(', ') || 'None'}
- Stakeholders: ${strategy.stakeholders.join(', ') || 'None'}

## Roadmap Overview

| Layer | Title | Description | Effort | Dependencies |
|-------|-------|-------------|--------|--------------|
${items.map(l => `| ${l.id} | ${l.title} | ${l.description} | ${l.effort} | ${l.depends_on.length ? l.depends_on.join(', ') : '-'} |`).join('\n')}

## Layer Details

${items.map(l => `### ${l.id}: ${l.title}

**Description**: ${l.description}

**Scope**: ${l.scope.join(', ')}

**Excludes**: ${l.excludes.join(', ') || 'None'}

**Convergence Criteria**:
${l.convergence.criteria.map(c => \`- ${c}\`).join('\n')}
- **Verification**: ${l.convergence.verification}
- **Definition of Done**: ${l.convergence.definition_of_done}

**Risk Items**: ${l.risk_items.length ? l.risk_items.map(r => \`\n- ${r}\`).join('') : 'None'}

**Effort**: ${l.effort}
`).join('\n---\n\n')}

## Risk Summary

${items.flatMap(l => l.risk_items.map(r => \`- **${l.id}**: ${r}\`)).join('\n') || 'No identified risks'}

## Next Steps

Each layer can be executed independently:
\\\`\\\`\\\`bash
/workflow:lite-plan "${items[0]?.title}: ${items[0]?.scope.join(', ')}"
\\\`\\\`\\\`

Roadmap JSONL file: \\\`${sessionFolder}/roadmap.jsonl\\\`
`
```

**Direct mode roadmap.md generation**:

```javascript
const roadmapMd = `# Requirement Roadmap

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Strategy**: direct
**Generated**: ${getUtc8ISOString()}

## Strategy Assessment
- Goal: ${strategy.goal}
- Constraints: ${strategy.constraints.join(', ') || 'None'}
- Assessment basis: ${Object.entries(strategy.uncertainty_factors).map(([k,v]) => `${k}=${v}`).join(', ')}

## Task Sequence

| Group | ID | Title | Type | Description | Dependencies |
|-------|----|-------|------|-------------|--------------|
${items.map(t => `| ${t.parallel_group} | ${t.id} | ${t.title} | ${t.type} | ${t.description} | ${t.depends_on.length ? t.depends_on.join(', ') : '-'} |`).join('\n')}

## Task Details

${items.map(t => `### ${t.id}: ${t.title}

**Type**: ${t.type} | **Parallel Group**: ${t.parallel_group}

**Description**: ${t.description}

**Scope**: ${t.scope}

**Inputs**: ${t.inputs.length ? t.inputs.join(', ') : 'None (starting task)'}
**Outputs**: ${t.outputs.join(', ')}

**Convergence Criteria**:
${t.convergence.criteria.map(c => \`- ${c}\`).join('\n')}
- **Verification**: ${t.convergence.verification}
- **Definition of Done**: ${t.convergence.definition_of_done}
`).join('\n---\n\n')}

## Next Steps

Each task can be executed independently:
\\\`\\\`\\\`bash
/workflow:lite-plan "${items[0]?.title}: ${items[0]?.scope}"
\\\`\\\`\\\`

Roadmap JSONL file: \\\`${sessionFolder}/roadmap.jsonl\\\`
`
```

**Write and provide post-completion options**:

```javascript
Write(`${sessionFolder}/roadmap.md`, roadmapMd)

// Post-completion options
if (!autoYes) {
  AskUserQuestion({
    questions: [{
      question: "Roadmap generated. Next step:",
      header: "Next Step",
      multiSelect: false,
      options: [
        { label: "Execute First Layer", description: `Launch lite-plan to execute ${items[0].id}` },
        { label: "Create Issue", description: "Create GitHub Issue based on roadmap" },
        { label: "Export Report", description: "Generate standalone shareable roadmap report" },
        { label: "Done", description: "Save roadmap only, execute later" }
      ]
    }]
  })
}
```

| Selection | Action |
|-----------|--------|
| Execute First Layer | `Skill(skill="workflow:lite-plan", args="${firstItem.scope}")` |
| Create Issue | `Skill(skill="issue:new", args="...")` |
| Export Report | Copy roadmap.md + roadmap.jsonl to user-specified location |
| Done | Display roadmap file paths, end |

**Success Criteria**:
- User feedback processed (or skipped via autoYes)
- roadmap.md finalized with full tables and convergence details
- roadmap.jsonl final version updated
- Post-completion options provided

## Session Folder Structure

```
.workflow/.req-plan/RPLAN-{slug}-{YYYY-MM-DD}/
├── roadmap.md                    # Human-readable roadmap
├── roadmap.jsonl                 # Machine-readable, one self-contained record per line
├── strategy-assessment.json      # Strategy assessment result
└── exploration-codebase.json     # Codebase context (optional)
```

| File | Phase | Description |
|------|-------|-------------|
| `strategy-assessment.json` | 1 | Uncertainty analysis + mode recommendation + extracted goal/constraints/stakeholders/domain_keywords |
| `roadmap.md` (skeleton) | 1 | Initial skeleton with placeholders, finalized in Phase 4 |
| `exploration-codebase.json` | 2 | Codebase context: relevant modules, patterns, integration points (only when codebase exists) |
| `roadmap.jsonl` | 3 | One self-contained JSON record per line with convergence criteria and source provenance |
| `roadmap.md` (final) | 4 | Human-readable roadmap with tabular display + convergence details, revised per user feedback |

## JSONL Schema

### Convergence Criteria

Each record's `convergence` object:

| Field | Purpose | Requirement |
|-------|---------|-------------|
| `criteria[]` | List of checkable specific conditions | **Testable** - can be written as assertions or manual steps |
| `verification` | How to verify these conditions | **Executable** - command, script, or explicit steps |
| `definition_of_done` | One-sentence completion definition | **Business language** - non-technical person can judge |

### Progressive Mode (one layer per line)

| Layer | Title | Typical Description |
|-------|-------|---------------------|
| L0 | MVP | Minimum viable closed loop, core path end-to-end |
| L1 | Usable | Key user paths refined, basic error handling |
| L2 | Refined | Edge cases, performance, security hardening |
| L3 | Optimized | Advanced features, observability, operations |

**Schema**: `id, title, description, type, priority, scope[], excludes[], convergence{}, risk_items[], effort, depends_on[], source{}`

```jsonl
{"id":"L0","title":"MVP","description":"Minimum viable closed loop","type":"feature","priority":"high","scope":["User registration and login","Basic CRUD"],"excludes":["OAuth","2FA"],"convergence":{"criteria":["End-to-end register→login→operate flow works","Core API returns correct responses"],"verification":"curl/Postman manual testing or smoke test script","definition_of_done":"New user can complete register→login→perform one core operation"},"risk_items":["JWT library selection needs validation"],"effort":"medium","depends_on":[],"source":{"tool":"req-plan-with-file","session_id":"RPLAN-xxx","original_id":"L0"}}
{"id":"L1","title":"Usable","description":"Complete key user paths","type":"feature","priority":"medium","scope":["Password reset","Input validation","Error messages"],"excludes":["Audit logs","Rate limiting"],"convergence":{"criteria":["All form fields have frontend+backend validation","Password reset email can be sent and reset completed","Error scenarios show user-friendly messages"],"verification":"Unit tests cover validation logic + manual test of reset flow","definition_of_done":"Users have a clear recovery path when encountering input errors or forgotten passwords"},"risk_items":[],"effort":"medium","depends_on":["L0"],"source":{"tool":"req-plan-with-file","session_id":"RPLAN-xxx","original_id":"L1"}}
```

**Constraints**: 2-4 layers, L0 must be a self-contained closed loop with no dependencies, each feature belongs to exactly ONE layer (no scope overlap).

### Direct Mode (one task per line)

| Type | Use Case |
|------|----------|
| infrastructure | Data models, configuration, scaffolding |
| feature | API, UI, business logic implementation |
| enhancement | Validation, error handling, edge cases |
| testing | Unit tests, integration tests, E2E |

**Schema**: `id, title, description, type, scope, inputs[], outputs[], convergence{}, depends_on[], parallel_group, source{}`

```jsonl
{"id":"T1","title":"Establish data model","description":"Create database schema and TypeScript type definitions for all business entities","type":"infrastructure","scope":"DB schema + TypeScript types","inputs":[],"outputs":["schema.prisma","types/user.ts"],"convergence":{"criteria":["Migration executes without errors","TypeScript types compile successfully","Fields cover all business entities"],"verification":"npx prisma migrate dev && npx tsc --noEmit","definition_of_done":"Database schema migrates correctly, type definitions can be referenced by other modules"},"depends_on":[],"parallel_group":1,"source":{"tool":"req-plan-with-file","session_id":"RPLAN-xxx","original_id":"T1"}}
{"id":"T2","title":"Implement core API","description":"Build CRUD endpoints for User entity with proper validation and error handling","type":"feature","scope":"CRUD endpoints for User","inputs":["schema.prisma","types/user.ts"],"outputs":["routes/user.ts","controllers/user.ts"],"convergence":{"criteria":["GET/POST/PUT/DELETE return correct status codes","Request/response conforms to schema","No N+1 queries"],"verification":"jest --testPathPattern=user.test.ts","definition_of_done":"All User CRUD endpoints pass integration tests"},"depends_on":["T1"],"parallel_group":2,"source":{"tool":"req-plan-with-file","session_id":"RPLAN-xxx","original_id":"T2"}}
```

**Constraints**: Inputs must come from preceding task outputs or existing resources, tasks in same parallel_group must be truly independent, no circular dependencies.

## Convergence Quality Requirements

Every `convergence` field MUST satisfy these quality standards:

| Field | Requirement | Bad Example | Good Example |
|-------|-------------|-------------|--------------|
| `criteria[]` | **Testable** - can write assertions or manual steps | `"System works correctly"` | `"API returns 200 and response body contains user_id field"` |
| `verification` | **Executable** - command, script, or clear steps | `"Check it"` | `"jest --testPathPattern=auth && curl -s localhost:3000/health"` |
| `definition_of_done` | **Business language** - non-technical person can judge | `"Code compiles"` | `"New user can complete register→login→perform core operation flow"` |

**NEVER** output vague convergence criteria ("works correctly", "system is normal"). **ALWAYS** ensure:
- criteria are testable (can be written as assertions or manual verification steps)
- verification is executable (commands or explicit steps)
- definition_of_done uses business language (non-technical stakeholders can judge)

## Fallback Decomposition

When normal decomposition fails or produces empty results, use fallback templates:

**Progressive fallback**:
```javascript
[
  {
    id: "L0", title: "MVP", description: "Minimum viable closed loop",
    type: "feature", priority: "high",
    scope: ["Core functionality"], excludes: ["Advanced features", "Optimization"],
    convergence: {
      criteria: ["Core path works end-to-end"],
      verification: "Manual test of core flow",
      definition_of_done: "User can complete one full core operation"
    },
    risk_items: ["Tech selection needs validation"], effort: "medium", depends_on: [],
    source: { tool: "req-plan-with-file", session_id: sessionId, original_id: "L0" }
  },
  {
    id: "L1", title: "Usable", description: "Refine key user paths",
    type: "feature", priority: "medium",
    scope: ["Error handling", "Input validation"], excludes: ["Performance optimization", "Monitoring"],
    convergence: {
      criteria: ["All user inputs validated", "Error scenarios show messages"],
      verification: "Unit tests + manual error scenario testing",
      definition_of_done: "Users have clear guidance and recovery paths when encountering problems"
    },
    risk_items: [], effort: "medium", depends_on: ["L0"],
    source: { tool: "req-plan-with-file", session_id: sessionId, original_id: "L1" }
  }
]
```

**Direct fallback**:
```javascript
[
  {
    id: "T1", title: "Infrastructure setup", description: "Project scaffolding and base configuration",
    type: "infrastructure", priority: "high",
    scope: "Project scaffolding and base configuration",
    inputs: [], outputs: ["project-structure"],
    convergence: {
      criteria: ["Project builds without errors", "Base configuration complete"],
      verification: "npm run build (or equivalent build command)",
      definition_of_done: "Project foundation ready for feature development"
    },
    depends_on: [], parallel_group: 1,
    source: { tool: "req-plan-with-file", session_id: sessionId, original_id: "T1" }
  },
  {
    id: "T2", title: "Core feature implementation", description: "Implement core business logic",
    type: "feature", priority: "high",
    scope: "Core business logic",
    inputs: ["project-structure"], outputs: ["core-module"],
    convergence: {
      criteria: ["Core API/functionality callable", "Returns expected results"],
      verification: "Run core feature tests",
      definition_of_done: "Core business functionality works as expected"
    },
    depends_on: ["T1"], parallel_group: 2,
    source: { tool: "req-plan-with-file", session_id: sessionId, original_id: "T2" }
  }
]
```

## Error Handling

| Situation | Action |
|-----------|--------|
| No codebase detected | Normal flow, skip Phase 2 |
| Codebase search fails | Proceed with pure requirement decomposition |
| Circular dependency in records | Fix dependency graph before writing JSONL |
| User feedback timeout | Save current state, display `--continue` recovery command |
| Max feedback rounds (5) | Use current version to generate final artifacts |
| Session folder conflict | Append timestamp suffix |
| JSONL format error | Validate line by line, report problematic lines and fix |
| Quality check fails | Auto-fix if possible, otherwise report to user in feedback loop |
| Decomposition produces empty results | Use fallback decomposition templates |

## Best Practices

1. **Clear requirement description**: Detailed description leads to more accurate uncertainty assessment and decomposition
2. **Validate MVP first**: In progressive mode, L0 should be the minimum verifiable closed loop
3. **Testable convergence**: criteria must be writable as assertions or manual steps; definition_of_done should be judgeable by non-technical stakeholders
4. **Incremental validation**: Use `--continue` to iterate on existing roadmaps
5. **Independently executable**: Each JSONL record should be independently passable to lite-plan for execution

## When to Use

**Use req-plan-with-file when:**
- You need to decompose a large requirement into a progressively executable roadmap
- Unsure where to start, need an MVP strategy
- Need to generate a trackable task sequence for the team
- Requirement involves multiple stages or iterations

**Use lite-plan when:**
- You have a clear single task to execute
- The requirement is already a layer/task from the roadmap
- No layered planning needed

**Use collaborative-plan-with-file when:**
- A single complex task needs multi-agent parallel planning
- Need to analyze the same task from multiple domain perspectives

**Use analyze-with-file when:**
- Need in-depth analysis of a technical problem
- Not about planning execution, but understanding and discussion

---

**Now execute the req-plan-with-file workflow for**: $ARGUMENTS
