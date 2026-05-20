---
name: workflow-tdd-plan
description: |
  TDD planning pipeline with multi-mode routing (plan/verify). Session discovery →
  context gathering (spawn_agent) → test coverage analysis (spawn_agent) → conditional
  conflict resolution → TDD task generation (spawn_agent) → structure validation →
  interactive verification. Produces IMPL_PLAN.md with Red-Green-Refactor cycles,
  task JSONs, TODO_LIST.md.
argument-hint: "[-y|--yes] [--session ID] \"task description\" | verify [--session ID]"
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

## Auto Mode

When `--yes` or `-y`: Skip all confirmations, use defaults, auto-verify, auto-continue to execute if PROCEED.

# Workflow TDD Plan

## Usage

```bash
# Plan mode (default)
$workflow-tdd-plan "Build authentication system with JWT and OAuth"
$workflow-tdd-plan -y "Add rate limiting to API endpoints"
$workflow-tdd-plan --session WFS-auth "Extend with 2FA support"

# Verify mode
$workflow-tdd-plan verify --session WFS-auth
$workflow-tdd-plan verify
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `--session ID`: Use specific session

---

## Overview

Multi-mode TDD planning pipeline using subagent coordination. Plan mode runs 6 sequential phases with conditional branching; verify mode operates on existing plans with TDD compliance validation.

**Core Principle**: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

```
┌──────────────────────────────────────────────────────────────────┐
│                    WORKFLOW TDD PLAN PIPELINE                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Mode Detection: plan | verify                                    │
│                                                                    │
│  ═══ Plan Mode (default) ═══                                      │
│                                                                    │
│  Phase 1: Session Discovery                                       │
│     ├─ Create or find workflow session                            │
│     └─ Initialize planning-notes.md with TDD context              │
│                                                                    │
│  Phase 2: Context Gathering (spawn_agent: context-search-agent)  │
│     ├─ Codebase analysis → context-package.json                  │
│     └─ Conflict risk assessment                                   │
│                                                                    │
│  Phase 3: Test Coverage Analysis (spawn_agent: cli-explore-agent)│
│     ├─ Detect test framework and conventions                      │
│     ├─ Analyze existing test coverage                             │
│     └─ Output: test-context-package.json                          │
│                                                                    │
│  Phase 4: Conflict Resolution (conditional: risk ≥ medium)       │
│     ├─ CLI-driven conflict analysis                               │
│     └─ User-selected resolution strategies                        │
│                                                                    │
│  Phase 5: TDD Task Generation (spawn_agent: action-planning-agent)│
│     ├─ Generate tasks with Red-Green-Refactor cycles              │
│     └─ Output: IMPL_PLAN.md + task JSONs + TODO_LIST.md          │
│                                                                    │
│  Phase 6: TDD Structure Validation                                │
│     ├─ Validate Red-Green-Refactor structure                      │
│     └─ Present Plan Confirmation Gate                             │
│                                                                    │
│  Plan Confirmation Gate                                           │
│     ├─ "Verify TDD Compliance" → Phase 7                         │
│     ├─ "Start Execution" → workflow-execute                      │
│     └─ "Review Status" → Display inline                          │
│                                                                    │
│  ═══ Verify Mode ═══                                              │
│  Phase 7: TDD Verification (spawn_agent: cli-explore-agent)      │
│     └─ 4-dimension TDD compliance → TDD_COMPLIANCE_REPORT.md     │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
User Input (task description)
    │
    ↓ [Convert to TDD Structured Format]
    │   TDD: [Feature Name]
    │   GOAL: [objective]
    │   SCOPE: [boundaries]
    │   CONTEXT: [background]
    │   TEST_FOCUS: [test scenarios]
    │
Phase 1 ──→ sessionId, planning-notes.md
    │
Phase 2 ──→ context-package.json, conflictRisk
    │
Phase 3 ──→ test-context-package.json
    │
    ├── conflictRisk ≥ medium ──→ Phase 4 ──→ conflict-resolution.json
    └── conflictRisk < medium ──→ skip Phase 4
    │
Phase 5 ──→ IMPL_PLAN.md (with Red-Green-Refactor), task JSONs, TODO_LIST.md
    │
Phase 6 ──→ TDD structure validation
    │
    ├── Verify → Phase 7 → TDD_COMPLIANCE_REPORT.md
    ├── Execute → workflow-execute skill
    └── Review → inline display
```

---

## Session Structure

```
.workflow/active/WFS-{session}/
├── workflow-session.json              # Session metadata
├── planning-notes.md                  # Accumulated context across phases
├── IMPL_PLAN.md                       # Implementation plan with TDD cycles
├── plan.json                          # Structured plan overview
├── TODO_LIST.md                       # Task checklist
├── .task/                             # Task definitions with TDD phases
│   ├── IMPL-1.json                    # Each task has Red-Green-Refactor steps
│   └── IMPL-N.json
└── .process/
    ├── context-package.json           # Phase 2 output
    ├── test-context-package.json      # Phase 3 output
    ├── conflict-resolution.json       # Phase 4 output (conditional)
    └── TDD_COMPLIANCE_REPORT.md       # Phase 7 output
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const sessionMatch = $ARGUMENTS.match(/--session\s+(\S+)/)
const existingSessionId = sessionMatch ? sessionMatch[1] : null

// Mode detection
const cleanArgs = $ARGUMENTS
  .replace(/--yes|-y|--session\s+\S+/g, '').trim()

let mode = 'plan'
if (cleanArgs.startsWith('verify')) mode = 'verify'

const taskDescription = cleanArgs
  .replace(/^verify\s*/, '')
  .replace(/^["']|["']$/g, '')
  .trim()

// Convert to TDD structured format
function toTddStructured(desc) {
  const featureName = desc.split(/\s+/).slice(0, 3).join(' ')
  return `TDD: ${featureName}
GOAL: ${desc}
SCOPE: Core implementation
CONTEXT: New development
TEST_FOCUS: Unit tests, integration tests, edge cases`
}

const structuredDesc = toTddStructured(taskDescription)
```

---

### Phase 1: Session Discovery (Plan Mode)

**Objective**: Create or find workflow session, initialize planning notes with TDD context.

```javascript
if (mode !== 'plan') {
  // verify: locate existing session
  // → Jump to Phase 7
}

let sessionId, sessionFolder

if (existingSessionId) {
  sessionId = existingSessionId
  sessionFolder = `.workflow/active/${sessionId}`
  if (!Bash(`test -d "${sessionFolder}" && echo yes`).trim()) {
    console.log(`ERROR: Session ${sessionId} not found`)
    return
  }
} else {
  // Auto-detect from .workflow/active/ or create new
  const sessions = Bash(`ls -d .workflow/active/WFS-* 2>/dev/null`).trim().split('\n').filter(Boolean)

  if (sessions.length === 0 || taskDescription) {
    // Create new session
    const slug = taskDescription.toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-').substring(0, 40)
    sessionId = `WFS-${slug}`
    sessionFolder = `.workflow/active/${sessionId}`
    Bash(`mkdir -p "${sessionFolder}/.task" "${sessionFolder}/.process"`)

    Write(`${sessionFolder}/workflow-session.json`, JSON.stringify({
      session_id: sessionId,
      status: 'planning',
      workflow_type: 'tdd',
      created_at: getUtc8ISOString(),
      task_description: taskDescription
    }, null, 2))
  } else if (sessions.length === 1) {
    sessionId = sessions[0].split('/').pop()
    sessionFolder = sessions[0]
  } else {
    // Multiple sessions — ask user
    if (AUTO_YES) {
      sessionFolder = sessions[0]
      sessionId = sessions[0].split('/').pop()
    } else {
      const answer = AskUserQuestion({
        questions: [{
          question: "Multiple sessions found. Select one:",
          header: "Session",
          multiSelect: false,
          options: sessions.slice(0, 4).map(s => ({
            label: s.split('/').pop(),
            description: s
          }))
        }]
      })
      sessionId = answer.Session
      sessionFolder = `.workflow/active/${sessionId}`
    }
  }
}

// Initialize planning-notes.md with TDD context
Write(`${sessionFolder}/planning-notes.md`, `# TDD Planning Notes

## User Intent
${structuredDesc}

## TDD Principles
- NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
- Red-Green-Refactor cycle for all tasks
- Test-first forces edge case discovery before implementation
`)

console.log(`Session: ${sessionId}`)
```

---

### Phase 2: Context Gathering (spawn_agent)

**Objective**: Gather project context, assess conflict risk.

```javascript
console.log(`\n## Phase 2: Context Gathering\n`)

const ctxAgent = spawn_agent({
  agent: `~/.codex/agents/context-search-agent.md`,
  instruction: `
Gather implementation context for TDD planning.

**Session**: ${sessionFolder}
**Task**: ${taskDescription}
**Mode**: TDD_PLAN

### Steps
1. Analyze project structure (package.json, tsconfig, etc.)
2. Search for existing similar implementations
3. Identify integration points and dependencies
4. Assess conflict risk with existing code
5. Generate context package

### Output
Write context package to: ${sessionFolder}/.process/context-package.json
Format: {
  "critical_files": [...],
  "patterns": [...],
  "dependencies": [...],
  "integration_points": [...],
  "conflict_risk": "none" | "low" | "medium" | "high",
  "conflict_areas": [...],
  "constraints": [...]
}
`
})

wait({ id: ctxAgent })
close_agent({ id: ctxAgent })

// Parse outputs
const contextPkg = JSON.parse(Read(`${sessionFolder}/.process/context-package.json`) || '{}')
const conflictRisk = contextPkg.conflict_risk || 'none'

// Update planning-notes.md
Edit(`${sessionFolder}/planning-notes.md`, {
  oldText: '## User Intent',
  newText: `## Context Findings
- Critical files: ${(contextPkg.critical_files || []).join(', ')}
- Conflict risk: ${conflictRisk}
- Constraints: ${(contextPkg.constraints || []).join('; ')}

## User Intent`
})

console.log(`  Context gathered. Conflict risk: ${conflictRisk}`)
```

---

### Phase 3: Test Coverage Analysis (spawn_agent)

**Objective**: Analyze existing test patterns and coverage.

```javascript
console.log(`\n## Phase 3: Test Coverage Analysis\n`)

const testAgent = spawn_agent({
  agent: `~/.codex/agents/cli-explore-agent.md`,
  instruction: `
Analyze test coverage and framework for TDD planning.

**Session**: ${sessionFolder}
**Context**: ${sessionFolder}/.process/context-package.json

### Steps
1. Detect test framework (Jest, Vitest, Mocha, etc.)
2. Identify test file patterns and conventions
3. Analyze existing test coverage
4. Identify coverage gaps
5. Extract test utilities and helpers

### Output
Write test context to: ${sessionFolder}/.process/test-context-package.json
Format: {
  "test_framework": "jest" | "vitest" | "mocha" | "other",
  "test_patterns": {
    "unit": "**/*.test.ts",
    "integration": "**/*.integration.test.ts"
  },
  "coverage_summary": {
    "lines": 75.5,
    "branches": 68.2,
    "functions": 80.1
  },
  "coverage_gaps": [...],
  "test_utilities": [...],
  "conventions": {
    "naming": "describe/it",
    "mocking": "jest.mock",
    "assertions": "expect"
  }
}
`
})

wait({ id: testAgent })
close_agent({ id: testAgent })

const testContext = JSON.parse(Read(`${sessionFolder}/.process/test-context-package.json`) || '{}')

// Update planning-notes
Edit(`${sessionFolder}/planning-notes.md`, {
  oldText: '## TDD Principles',
  newText: `## Test Context
- Framework: ${testContext.test_framework || 'unknown'}
- Coverage: ${testContext.coverage_summary?.lines || 'N/A'}% lines
- Gaps: ${(testContext.coverage_gaps || []).join(', ')}

## TDD Principles`
})

console.log(`  Test framework: ${testContext.test_framework}`)
```

---

### Phase 4: Conflict Resolution (Conditional)

**Objective**: Detect and resolve conflicts when risk ≥ medium.

```javascript
if (['medium', 'high'].includes(conflictRisk)) {
  console.log(`\n## Phase 4: Conflict Resolution (risk: ${conflictRisk})\n`)

  Bash({
    command: `ccw cli -p "PURPOSE: Analyze and resolve conflicts between planned changes and existing codebase.
TASK:
  • Read context package for conflict areas
  • Analyze each conflict area in detail
  • Propose resolution strategies (refactor, adapt, isolate, defer)
  • For each conflict: assess impact and recommend approach
MODE: analysis
CONTEXT: @**/*
EXPECTED: JSON: {conflicts: [{area, severity, description, strategy, impact}], summary: string}
CONSTRAINTS: Focus on ${(contextPkg.conflict_areas || []).join(', ')}

TASK DESCRIPTION: ${taskDescription}" --tool gemini --mode analysis --rule analysis-diagnose-bug-root-cause`,
    run_in_background: true
  })
  // Wait for CLI → conflicts[]

  if (!AUTO_YES && conflicts.length > 0) {
    // Present conflicts and let user select strategies
    console.log(`\n### Conflicts Found: ${conflicts.length}\n`)
    conflicts.forEach((c, i) => {
      console.log(`${i + 1}. [${c.severity}] ${c.area}: ${c.description}`)
      console.log(`   Strategy: ${c.strategy} | Impact: ${c.impact}`)
    })

    const answer = AskUserQuestion({
      questions: [{
        question: "Accept conflict resolution strategies?",
        header: "Conflicts",
        multiSelect: false,
        options: [
          { label: "Accept All", description: "Apply all recommended strategies" },
          { label: "Review Each", description: "Approve strategies individually" },
          { label: "Skip", description: "Proceed without resolving" }
        ]
      }]
    })
  }

  // Write resolution
  Write(`${sessionFolder}/.process/conflict-resolution.json`,
    JSON.stringify({ conflicts, resolved_at: getUtc8ISOString() }, null, 2))
} else {
  console.log(`  Conflict risk: ${conflictRisk} — skipping Phase 4`)
}
```

---

### Phase 5: TDD Task Generation (spawn_agent)

**Objective**: Generate IMPL_PLAN.md with Red-Green-Refactor cycles, task JSONs, TODO_LIST.md.

```javascript
console.log(`\n## Phase 5: TDD Task Generation\n`)

const planAgent = spawn_agent({
  agent: `~/.codex/agents/action-planning-agent.md`,
  instruction: `
Generate TDD implementation plan with Red-Green-Refactor cycles.

**Session**: ${sessionFolder}
**Task**: ${taskDescription}
**Context**: ${sessionFolder}/.process/context-package.json
**Test Context**: ${sessionFolder}/.process/test-context-package.json
**Planning Notes**: ${sessionFolder}/planning-notes.md
${conflictRisk === 'medium' || conflictRisk === 'high'
  ? `**Conflict Resolution**: ${sessionFolder}/.process/conflict-resolution.json` : ''}

### TDD Requirements
Each task MUST include Red-Green-Refactor cycle:
1. **Red Phase**: Write failing test first
   - Define test cases
   - Verify test fails (proves test is valid)
   - Document expected failure
2. **Green Phase**: Implement minimal code to pass
   - Write simplest implementation
   - Run tests until passing
   - Max 3 test-fix iterations (auto-revert if exceeded)
3. **Refactor Phase**: Improve code quality
   - Refactor with tests as safety net
   - Maintain passing tests
   - Document improvements

### Output Requirements
1. **IMPL_PLAN.md** at ${sessionFolder}/IMPL_PLAN.md
   - Section 1: Requirements Summary
   - Section 2: Test Strategy (framework, patterns, coverage goals)
   - Section 3: Task Breakdown with TDD cycles
   - Section 4: Implementation Strategy
   - Section 5: Risk Assessment
2. **plan.json** at ${sessionFolder}/plan.json
   - {task_ids[], recommended_execution, complexity, tdd_compliance: true}
3. **Task JSONs** at ${sessionFolder}/.task/IMPL-{N}.json
   - Each task has "implementation" array with 3 steps:
     [
       {step: 1, tdd_phase: "red", description: "Write failing test", ...},
       {step: 2, tdd_phase: "green", description: "Implement code", test_fix_cycle: {max_iterations: 3, auto_revert: true}},
       {step: 3, tdd_phase: "refactor", description: "Refactor code", ...}
     ]
4. **TODO_LIST.md** at ${sessionFolder}/TODO_LIST.md
   - Checkbox format: - [ ] IMPL-{N}: {title} (TDD)
`
})

wait({ id: planAgent })
close_agent({ id: planAgent })

console.log(`  TDD tasks generated`)
```

---

### Phase 6: TDD Structure Validation

**Objective**: Validate Red-Green-Refactor structure in all tasks.

```javascript
console.log(`\n## Phase 6: TDD Structure Validation\n`)

// Read all task JSONs
const taskFiles = Bash(`ls ${sessionFolder}/.task/IMPL-*.json 2>/dev/null`).trim().split('\n').filter(Boolean)
const tasks = taskFiles.map(f => JSON.parse(Read(f)))

// Validate TDD structure
const validationErrors = []
for (const task of tasks) {
  const impl = task.implementation || []

  // Check 3-step structure
  if (impl.length !== 3) {
    validationErrors.push(`${task.id}: Expected 3 steps, found ${impl.length}`)
    continue
  }

  // Check Red phase
  if (impl[0].tdd_phase !== 'red') {
    validationErrors.push(`${task.id}: Step 1 must be Red phase`)
  }

  // Check Green phase with test-fix-cycle
  if (impl[1].tdd_phase !== 'green') {
    validationErrors.push(`${task.id}: Step 2 must be Green phase`)
  }
  if (!impl[1].test_fix_cycle || !impl[1].test_fix_cycle.max_iterations) {
    validationErrors.push(`${task.id}: Green phase missing test-fix-cycle config`)
  }

  // Check Refactor phase
  if (impl[2].tdd_phase !== 'refactor') {
    validationErrors.push(`${task.id}: Step 3 must be Refactor phase`)
  }
}

if (validationErrors.length > 0) {
  console.log(`\n### TDD Structure Validation Errors:\n`)
  validationErrors.forEach(e => console.log(`  - ${e}`))

  if (!AUTO_YES) {
    const answer = AskUserQuestion({
      questions: [{
        question: "TDD structure validation failed. Continue anyway?",
        header: "Validation",
        multiSelect: false,
        options: [
          { label: "Fix and Retry", description: "Regenerate tasks with correct structure" },
          { label: "Continue", description: "Proceed despite errors" },
          { label: "Abort", description: "Stop planning" }
        ]
      }]
    })

    if (answer.Validation === "Fix and Retry") {
      // Re-run Phase 5
      // → goto Phase 5
    } else if (answer.Validation === "Abort") {
      return
    }
  }
} else {
  console.log(`  ✓ All tasks have valid Red-Green-Refactor structure`)
}

// Plan Confirmation Gate
const taskCount = tasks.length
console.log(`\n## Plan Generated\n`)
console.log(`  Tasks: ${taskCount}`)
console.log(`  Plan: ${sessionFolder}/IMPL_PLAN.md`)

if (AUTO_YES) {
  console.log(`  [--yes] Auto-verifying TDD compliance...`)
  // → Fall through to Phase 7
} else {
  const nextStep = AskUserQuestion({
    questions: [{
      question: "TDD plan generated. What's next?",
      header: "Next Step",
      multiSelect: false,
      options: [
        { label: "Verify TDD Compliance (Recommended)", description: "Run full TDD compliance verification" },
        { label: "Start Execution", description: "Proceed to workflow-execute" },
        { label: "Review Status", description: "Display plan summary inline" }
      ]
    }]
  })

  if (nextStep['Next Step'] === 'Start Execution') {
    console.log(`\nReady to execute. Run: $workflow-execute --session ${sessionId}`)
    return
  }
  if (nextStep['Next Step'] === 'Review Status') {
    const plan = Read(`${sessionFolder}/IMPL_PLAN.md`)
    console.log(plan)
    return
  }
  // Verify → continue to Phase 7
}
```

---

### Phase 7: TDD Verification (Verify Mode)

**Objective**: Full TDD compliance verification with quality gate.

```javascript
if (mode === 'verify' || /* auto-verify from Phase 6 */) {
  console.log(`\n## Phase 7: TDD Verification\n`)

  // Find session if in verify mode entry
  if (mode === 'verify' && !sessionFolder) {
    // Session discovery (same logic as Phase 1)
  }

  const verifyAgent = spawn_agent({
    agent: `~/.codex/agents/cli-explore-agent.md`,
    instruction: `
Verify TDD compliance across 4 dimensions.

**Session**: ${sessionFolder}

### Verification Dimensions

**A. Test-First Structure**
- Every task has Red-Green-Refactor cycle
- Red phase defines failing tests
- Green phase implements code
- Refactor phase improves quality

**B. Test Coverage**
- All critical paths have tests
- Edge cases covered
- Integration points tested
- Coverage meets project standards

**C. Cycle Integrity**
- Red phase: test fails before implementation
- Green phase: minimal code to pass
- Refactor phase: maintains passing tests
- No production code without failing test first

**D. Quality Gates**
- Test-fix-cycle configured (max 3 iterations)
- Auto-revert on iteration limit
- Clear acceptance criteria
- Testable convergence conditions

### Output
Write report to: ${sessionFolder}/.process/TDD_COMPLIANCE_REPORT.md

Format:
# TDD Compliance Report

## Summary
- Quality Gate: APPROVED | CONDITIONAL | BLOCKED
- Tasks Analyzed: N
- Compliance Score: X%

## Dimension Scores
- A. Test-First Structure: PASS/WARN/FAIL
- B. Test Coverage: PASS/WARN/FAIL
- C. Cycle Integrity: PASS/WARN/FAIL
- D. Quality Gates: PASS/WARN/FAIL

## Issues Found
[List specific issues with task IDs]

## Recommendations
[Actionable recommendations]

## Quality Gate Decision
APPROVED: All dimensions PASS, ready for execution
CONDITIONAL: Minor warnings, can proceed with caution
BLOCKED: Critical failures, must fix before execution
`
  })

  wait({ id: verifyAgent })
  close_agent({ id: verifyAgent })

  const report = Read(`${sessionFolder}/.process/TDD_COMPLIANCE_REPORT.md`)
  const qualityGate = report.match(/Quality Gate: (\w+)/)?.[1] || 'UNKNOWN'

  console.log(`  Quality gate: ${qualityGate}`)
  console.log(`  Report: ${sessionFolder}/.process/TDD_COMPLIANCE_REPORT.md`)

  if (AUTO_YES && qualityGate === 'APPROVED') {
    console.log(`  [--yes] TDD compliance verified. Ready for execution.`)
    console.log(`  Run: $workflow-execute --session ${sessionId}`)
  }
}
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No active session | Guide: run `$workflow-tdd-plan "description"` first |
| Context gathering timeout | Retry with reduced scope |
| Test framework detection failed | Manual specification in test-context-package.json |
| TDD structure validation failed | Regenerate tasks or fix manually |
| Conflict analysis failure | Skip Phase 4, proceed with warning |
| Task generation failure | Retry agent with simplified context |
| Verification failure | Display partial results |
| Session not found (verify) | List available sessions |

---

## TDD Compliance Requirements

### The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

### Red-Green-Refactor Cycle

Every task must have:
1. **Red**: Write failing test (proves test is valid)
2. **Green**: Implement minimal code to pass (with test-fix-cycle)
3. **Refactor**: Improve code quality (maintain passing tests)

### Quality Gates

- Test-fix-cycle: max 3 iterations
- Auto-revert: triggered when max iterations reached
- Coverage goals: defined per project
- Acceptance criteria: testable and measurable

---

## Compact Protection

> **COMPACT DIRECTIVE**: If context compression occurs:
> - Re-read `planning-notes.md` for accumulated context
> - Re-read `workflow-session.json` for session state
> - Phase 5 is the most token-intensive — if compressed, re-read task JSONs on demand
