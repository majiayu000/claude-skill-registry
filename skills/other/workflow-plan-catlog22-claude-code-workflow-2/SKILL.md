---
name: workflow-plan
description: |
  Planning pipeline with multi-mode routing (plan/verify/replan). Session discovery →
  context gathering (spawn_agent) → conditional conflict resolution → task generation
  (spawn_agent or N+1 parallel agents) → plan verification → interactive replan.
  Produces IMPL_PLAN.md, task JSONs, TODO_LIST.md.
argument-hint: "[-y|--yes] [--session ID] \"task description\" | verify [--session ID] | replan [--session ID] [IMPL-N] \"changes\""
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

## Auto Mode

When `--yes` or `-y`: Skip all confirmations, use defaults, auto-verify, auto-continue to execute if PROCEED.

# Workflow Plan

## Usage

```bash
# Plan mode (default)
$workflow-plan "Build authentication system with JWT and OAuth"
$workflow-plan -y "Add rate limiting to API endpoints"
$workflow-plan --session WFS-auth "Extend with 2FA support"

# Verify mode
$workflow-plan verify --session WFS-auth
$workflow-plan verify

# Replan mode
$workflow-plan replan --session WFS-auth "Change from JWT to session-based auth"
$workflow-plan replan --session WFS-auth IMPL-3 "Split into two smaller tasks"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `--session ID`: Use specific session

---

## Overview

Multi-mode planning pipeline using subagent coordination. Plan mode runs 4 sequential phases with conditional branching; verify and replan modes operate on existing plans.

```
┌──────────────────────────────────────────────────────────────────┐
│                    WORKFLOW PLAN PIPELINE                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Mode Detection: plan | verify | replan                           │
│                                                                    │
│  ═══ Plan Mode (default) ═══                                      │
│                                                                    │
│  Phase 1: Session Discovery                                       │
│     ├─ Create or find workflow session                            │
│     └─ Initialize planning-notes.md                               │
│                                                                    │
│  Phase 2: Context Gathering (spawn_agent: context-search-agent)  │
│     ├─ Codebase analysis → context-package.json                  │
│     └─ Conflict risk assessment                                   │
│                                                                    │
│  Phase 3: Conflict Resolution (conditional: risk ≥ medium)       │
│     ├─ CLI-driven conflict analysis                               │
│     └─ User-selected resolution strategies                        │
│                                                                    │
│  Phase 4: Task Generation (spawn_agent: action-planning-agent)   │
│     ├─ Single module → 1 agent                                    │
│     ├─ Multi-module → N+1 parallel agents                        │
│     └─ Output: IMPL_PLAN.md + task JSONs + TODO_LIST.md          │
│                                                                    │
│  Plan Confirmation Gate                                           │
│     ├─ "Verify Plan" → Phase 5                                   │
│     ├─ "Start Execution" → workflow-execute                      │
│     └─ "Review Status" → Display inline                          │
│                                                                    │
│  ═══ Verify Mode ═══                                              │
│  Phase 5: Plan Verification (spawn_agent: cli-explore-agent)     │
│     └─ 10-dimension analysis → PLAN_VERIFICATION.md              │
│                                                                    │
│  ═══ Replan Mode ═══                                              │
│  Phase 6: Interactive Replan                                      │
│     └─ Clarification → Impact → Backup → Apply → Verify          │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
User Input (task description)
    │
    ↓ [Convert to GOAL/SCOPE/CONTEXT]
    │
Phase 1 ──→ sessionId, planning-notes.md
    │
Phase 2 ──→ context-package.json, conflictRisk
    │
    ├── conflictRisk ≥ medium ──→ Phase 3 ──→ modified artifacts
    └── conflictRisk < medium ──→ skip Phase 3
    │
Phase 4 ──→ IMPL_PLAN.md, plan.json, task JSONs, TODO_LIST.md
    │
    ├── Verify → Phase 5 → PLAN_VERIFICATION.md
    ├── Execute → workflow-execute skill
    └── Review → inline display
```

---

## Session Structure

```
.workflow/active/WFS-{session}/
├── workflow-session.json              # Session metadata
├── planning-notes.md                  # Accumulated context across phases
├── IMPL_PLAN.md                       # Implementation plan (human-readable)
├── plan.json                          # Structured plan overview (machine-readable)
├── TODO_LIST.md                       # Task checklist
├── .task/                             # Task definitions
│   ├── IMPL-1.json
│   └── IMPL-N.json
└── .process/
    ├── context-package.json           # Phase 2 output
    ├── conflict-resolution.json       # Phase 3 output (conditional)
    ├── PLAN_VERIFICATION.md           # Phase 5 output
    └── backup/                        # Phase 6 backups
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
else if (cleanArgs.startsWith('replan')) mode = 'replan'

const taskDescription = cleanArgs
  .replace(/^(verify|replan)\s*/, '')
  .replace(/^["']|["']$/g, '')
  .trim()

// Extract replan task ID if present
const replanTaskMatch = taskDescription.match(/^(IMPL-\d+(?:\.\d+)?)\s+(.+)/)
const replanTaskId = replanTaskMatch ? replanTaskMatch[1] : null
const replanDescription = replanTaskMatch ? replanTaskMatch[2] : taskDescription
```

---

### Phase 1: Session Discovery (Plan Mode)

**Objective**: Create or find workflow session, initialize planning notes.

```javascript
if (mode !== 'plan') {
  // verify/replan: locate existing session
  // → Jump to Phase 5 or Phase 6
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
    Bash(`mkdir -p "${sessionFolder}/.task" "${sessionFolder}/.process" "${sessionFolder}/.summaries"`)

    Write(`${sessionFolder}/workflow-session.json`, JSON.stringify({
      session_id: sessionId,
      status: 'planning',
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

// Initialize planning-notes.md
const structuredDesc = `GOAL: ${taskDescription}\nSCOPE: Core implementation\nCONTEXT: New development`
Write(`${sessionFolder}/planning-notes.md`, `# Planning Notes\n\n## User Intent\n${structuredDesc}\n`)

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
Gather implementation context for planning.

**Session**: ${sessionFolder}
**Task**: ${taskDescription}
**Mode**: PLAN

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
const contextPath = `${sessionFolder}/.process/context-package.json`

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

### Phase 3: Conflict Resolution (Conditional)

**Objective**: Detect and resolve conflicts when risk ≥ medium.

```javascript
if (['medium', 'high'].includes(conflictRisk)) {
  console.log(`\n## Phase 3: Conflict Resolution (risk: ${conflictRisk})\n`)

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

  // Update planning-notes
  // Append conflict decisions to planning-notes.md
} else {
  console.log(`  Conflict risk: ${conflictRisk} — skipping Phase 3`)
}
```

---

### Phase 4: Task Generation (spawn_agent)

**Objective**: Generate IMPL_PLAN.md, task JSONs, TODO_LIST.md.

**Steps**:

1. **Determine Planning Strategy**

   ```javascript
   console.log(`\n## Phase 4: Task Generation\n`)

   // Detect module count from context
   const modules = contextPkg.integration_points?.map(p => p.module).filter(Boolean) || []
   const uniqueModules = [...new Set(modules)]
   const isMultiModule = uniqueModules.length >= 2
   ```

2. **Single Module → One Agent**

   ```javascript
   if (!isMultiModule) {
     const planAgent = spawn_agent({
       agent: `~/.codex/agents/action-planning-agent.md`,
       instruction: `
Generate implementation plan and task JSONs.

**Session**: ${sessionFolder}
**Task**: ${taskDescription}
**Context**: ${contextPath}
**Planning Notes**: ${sessionFolder}/planning-notes.md
${contextPkg.conflict_risk === 'medium' || contextPkg.conflict_risk === 'high'
  ? `**Conflict Resolution**: ${sessionFolder}/.process/conflict-resolution.json` : ''}

### Output Requirements
1. **IMPL_PLAN.md** at ${sessionFolder}/IMPL_PLAN.md
   - Section 1: Requirements Summary
   - Section 2: Architecture Decisions
   - Section 3: Task Breakdown (with dependencies)
   - Section 4: Implementation Strategy (Sequential/Parallel/Phased)
   - Section 5: Risk Assessment
2. **plan.json** at ${sessionFolder}/plan.json
   - {task_ids[], recommended_execution, complexity, shared_context}
3. **Task JSONs** at ${sessionFolder}/.task/IMPL-{N}.json
   - {id, title, description, depends_on[], convergence, meta: {type, agent}}
4. **TODO_LIST.md** at ${sessionFolder}/TODO_LIST.md
   - Checkbox format: - [ ] IMPL-{N}: {title}
`
     })

     wait({ id: planAgent })
     close_agent({ id: planAgent })
   }
   ```

3. **Multi-Module → N+1 Parallel Agents**

   ```javascript
   if (isMultiModule) {
     const prefixes = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
     const moduleAgents = []

     // Spawn N module planners in parallel
     for (let i = 0; i < uniqueModules.length; i++) {
       const prefix = prefixes[i]
       const mod = uniqueModules[i]

       const agentId = spawn_agent({
         agent: `~/.codex/agents/action-planning-agent.md`,
         instruction: `
Plan module: ${mod} (prefix: ${prefix})

**Session**: ${sessionFolder}
**Module**: ${mod}
**Context**: ${contextPath}
**Task ID prefix**: ${prefix} (e.g., ${prefix}1, ${prefix}2, ...)

Generate task JSONs for this module only.
Output to: ${sessionFolder}/.task/${prefix}{N}.json
Mark cross-module dependencies as CROSS::${'{module}'}::${'{task}'}
`
       })
       moduleAgents.push({ id: agentId, module: mod, prefix })
     }

     // Wait for all module planners
     wait({ ids: moduleAgents.map(a => a.id) })
     moduleAgents.forEach(a => close_agent({ id: a.id }))

     // +1 Coordinator: integrate all modules
     const coordAgent = spawn_agent({
       agent: `~/.codex/agents/action-planning-agent.md`,
       instruction: `
Integrate ${uniqueModules.length} module plans into unified IMPL_PLAN.md.

**Session**: ${sessionFolder}
**Modules**: ${uniqueModules.join(', ')}
**Task Directory**: ${sessionFolder}/.task/

### Steps
1. Read all module task JSONs from .task/
2. Resolve CROSS:: dependencies (replace with actual task IDs)
3. Generate unified IMPL_PLAN.md, plan.json, TODO_LIST.md
4. Renumber task IDs to sequential IMPL-1, IMPL-2, ...
`
     })

     wait({ id: coordAgent })
     close_agent({ id: coordAgent })
   }
   ```

4. **Plan Confirmation Gate**

   ```javascript
   // Validate outputs exist
   const planExists = Bash(`test -f "${sessionFolder}/IMPL_PLAN.md" && echo yes`).trim() === 'yes'
   const taskCount = parseInt(Bash(`ls ${sessionFolder}/.task/IMPL-*.json 2>/dev/null | wc -l`).trim()) || 0

   console.log(`\n## Plan Generated\n`)
   console.log(`  Tasks: ${taskCount}`)
   console.log(`  Plan: ${sessionFolder}/IMPL_PLAN.md`)

   if (AUTO_YES) {
     // Auto-verify then auto-execute if PROCEED
     console.log(`  [--yes] Auto-verifying plan...`)
     // → Fall through to Phase 5, then Phase 5 result determines next step
   } else {
     const nextStep = AskUserQuestion({
       questions: [{
         question: "Plan generated. What's next?",
         header: "Next Step",
         multiSelect: false,
         options: [
           { label: "Verify Plan (Recommended)", description: "Run quality verification before execution" },
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
     // Verify → continue to Phase 5
   }
   ```

---

### Phase 5: Plan Verification (Verify Mode)

**Objective**: Read-only multi-dimensional plan analysis.

```javascript
if (mode === 'verify' || /* auto-verify from Phase 4 */) {
  console.log(`\n## Phase 5: Plan Verification\n`)

  // Find session if in verify mode entry
  if (mode === 'verify' && !sessionFolder) {
    // Session discovery (same logic as Phase 1)
  }

  Bash({
    command: `ccw cli -p "PURPOSE: Verify implementation plan quality across 10 dimensions. Read-only analysis. Success = actionable quality gate recommendation.
TASK:
  • A: User Intent Alignment — does plan match original goal?
  • B: Requirements Coverage — are all requirements addressed?
  • C: Consistency Validation — internal consistency of plan
  • D: Dependency Integrity — valid dependency chain
  • E: Synthesis Alignment — matches brainstorm artifacts (if exist)
  • F: Task Specification Quality — clear, actionable, testable
  • G: Duplication Detection — no overlapping tasks
  • H: Feasibility Assessment — realistic scope and effort
  • I: Constraints Compliance — respects stated constraints
  • J: Context Validation — planning-notes consistent with plan
MODE: analysis
CONTEXT: @${sessionFolder}/IMPL_PLAN.md @${sessionFolder}/.task/**/*.json @${sessionFolder}/planning-notes.md @${sessionFolder}/TODO_LIST.md
EXPECTED: Structured report with: per-dimension score (PASS/WARN/FAIL), issues list, quality gate (BLOCK_EXECUTION/PROCEED_WITH_FIXES/PROCEED_WITH_CAUTION/PROCEED)
CONSTRAINTS: Read-only | No file modifications | Be specific about issues" --tool gemini --mode analysis --rule analysis-review-architecture --cd "${sessionFolder}"`,
    run_in_background: true
  })
  // Wait for CLI → verification report

  Write(`${sessionFolder}/.process/PLAN_VERIFICATION.md`, verificationReport)

  console.log(`  Quality gate: ${qualityGate}`)
  console.log(`  Report: ${sessionFolder}/.process/PLAN_VERIFICATION.md`)

  if (AUTO_YES && qualityGate === 'PROCEED') {
    console.log(`  [--yes] Plan verified. Ready for execution.`)
    console.log(`  Run: $workflow-execute --session ${sessionId}`)
  }
}
```

---

### Phase 6: Interactive Replan (Replan Mode)

**Objective**: Modify existing plan based on new requirements.

```javascript
if (mode === 'replan') {
  console.log(`\n## Phase 6: Interactive Replan\n`)

  // Find session
  if (!sessionFolder) {
    // Session discovery logic
  }

  const scope = replanTaskId ? 'task' : 'session'
  console.log(`  Scope: ${scope}${replanTaskId ? ` (${replanTaskId})` : ''}`)
  console.log(`  Changes: ${replanDescription}`)

  // 1. Backup current plan
  Bash(`mkdir -p "${sessionFolder}/.process/backup" && cp "${sessionFolder}/IMPL_PLAN.md" "${sessionFolder}/.process/backup/IMPL_PLAN-$(date +%Y%m%d%H%M%S).md"`)

  // 2. Replan via agent
  const replanAgent = spawn_agent({
    agent: `~/.codex/agents/action-planning-agent.md`,
    instruction: `
Replan ${scope === 'task' ? `task ${replanTaskId}` : 'entire session'}.

**Session**: ${sessionFolder}
**Current Plan**: ${sessionFolder}/IMPL_PLAN.md
**Current Tasks**: ${sessionFolder}/.task/
**Changes Requested**: ${replanDescription}
${replanTaskId ? `**Target Task**: ${sessionFolder}/.task/${replanTaskId}.json` : ''}

### Steps
1. Read current plan and task JSONs
2. Analyze impact of requested changes
3. Modify affected tasks (update/add/remove)
4. Update IMPL_PLAN.md with change annotations
5. Update TODO_LIST.md
6. Generate change summary

### Constraints
- Preserve completed tasks
- Minimize changes to unaffected tasks
- Maintain dependency integrity
`
  })

  wait({ id: replanAgent })
  close_agent({ id: replanAgent })

  console.log(`  Replan complete. Review: ${sessionFolder}/IMPL_PLAN.md`)
}
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No active session | Guide: run `$workflow-plan "description"` first |
| Context gathering timeout | Retry with reduced scope |
| Conflict analysis failure | Skip Phase 3, proceed with warning |
| Task generation failure | Retry agent with simplified context |
| Plan verification failure | Display partial results |
| Session not found (verify/replan) | List available sessions |

---

## Compact Protection

> **COMPACT DIRECTIVE**: If context compression occurs:
> - Re-read `planning-notes.md` for accumulated context
> - Re-read `workflow-session.json` for session state
> - Phase 4 is the most token-intensive — if compressed, re-read task JSONs on demand
