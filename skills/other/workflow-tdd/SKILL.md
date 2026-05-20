---
name: workflow-tdd
description: Unified TDD workflow skill combining 6-phase TDD planning with Red-Green-Refactor task chain generation, and 4-phase TDD verification with compliance reporting. Triggers on "workflow:tdd-plan", "workflow:tdd-verify".
allowed-tools: Skill, Task, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow TDD

Unified TDD workflow skill combining TDD planning (Red-Green-Refactor task chain generation with test-first development structure) and TDD verification (compliance validation with quality gate reporting). Produces IMPL_PLAN.md, task JSONs with internal TDD cycles, and TDD_COMPLIANCE_REPORT.md.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  Workflow TDD Orchestrator (SKILL.md)                            │
│  → Route by mode: plan | verify                                  │
│  → Pure coordinator: Execute phases, parse outputs, pass context │
└──────────────────────────────┬───────────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ↓                                               ↓
  ┌─────────────┐                                ┌───────────┐
  │  Plan Mode  │                                │  Verify   │
  │  (default)  │                                │   Mode    │
  │ Phase 1-6   │                                │  Phase 7  │
  └──────┬──────┘                                └───────────┘
         │
   ┌─────┼─────┬─────┬─────┬─────┐
   ↓     ↓     ↓     ↓     ↓     ↓
 ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
 │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │
 │Ses│ │Ctx│ │Tst│ │Con│ │Gen│ │Val│
 └───┘ └───┘ └───┘ └───┘ └─┬─┘ └───┘
                             ↓
                       ┌───────────┐
                       │ Confirm   │─── Verify ──→ Phase 7
                       │ (choice)  │─── Execute ─→ Skill("workflow-execute")
                       └───────────┘─── Review ──→ Display session status inline
```

## Key Design Principles

1. **Pure Orchestrator**: SKILL.md routes and coordinates only; execution detail lives in phase files
2. **Progressive Phase Loading**: Read phase docs ONLY when that phase is about to execute
3. **Multi-Mode Routing**: Single skill handles plan/verify via mode detection
4. **Task Attachment Model**: Sub-command tasks are ATTACHED, executed sequentially, then COLLAPSED
5. **Auto-Continue**: After each phase completes, automatically execute next pending phase
6. **TDD Iron Law**: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST - enforced in task structure

## Interactive Preference Collection

Before dispatching to phase execution, collect workflow preferences via AskUserQuestion:

```javascript
// ★ 统一 auto mode 检测：-y/--yes 从 $ARGUMENTS 或 ccw 传播
const autoYes = /\b(-y|--yes)\b/.test($ARGUMENTS)

if (autoYes) {
  // 自动模式：跳过所有询问，使用默认值
  workflowPreferences = { autoYes: true }
} else {
  const prefResponse = AskUserQuestion({
    questions: [
      {
        question: "是否跳过所有确认步骤（自动模式）？",
        header: "Auto Mode",
        multiSelect: false,
        options: [
          { label: "Interactive (Recommended)", description: "交互模式，包含确认步骤" },
          { label: "Auto", description: "跳过所有确认，自动执行" }
        ]
      }
    ]
  })

  workflowPreferences = {
    autoYes: prefResponse.autoMode === 'Auto'
  }
}
```

**workflowPreferences** is passed to phase execution as context variable, referenced as `workflowPreferences.autoYes` within phases.

## Mode Detection

```javascript
const args = $ARGUMENTS
const mode = detectMode(args)

function detectMode(args) {
  // Skill trigger determines mode
  if (skillName === 'workflow:tdd-verify') return 'verify'
  return 'plan'  // default: workflow:tdd-plan
}
```

## Execution Flow

### Plan Mode (default)

```
Input Parsing:
   └─ Convert user input to TDD structured format (GOAL/SCOPE/CONTEXT/TEST_FOCUS)

Phase 1: Session Discovery
   └─ Ref: phases/01-session-discovery.md
      └─ Output: sessionId (WFS-xxx)

Phase 2: Context Gathering
   └─ Ref: phases/02-context-gathering.md
      ├─ Tasks attached: Analyze structure → Identify integration → Generate package
      └─ Output: contextPath + conflictRisk

Phase 3: Test Coverage Analysis
   └─ Ref: phases/03-test-coverage-analysis.md
      ├─ Tasks attached: Detect framework → Analyze coverage → Identify gaps
      └─ Output: testContextPath

Phase 4: Conflict Resolution (conditional: conflictRisk ≥ medium)
   └─ Decision (conflictRisk check):
      ├─ conflictRisk ≥ medium → Ref: phases/04-conflict-resolution.md
      │   ├─ Tasks attached: Detect conflicts → Log analysis → Apply strategies
      │   └─ Output: conflict-resolution.json
      └─ conflictRisk < medium → Skip to Phase 5

Phase 5: TDD Task Generation
   └─ Ref: phases/05-tdd-task-generation.md
      ├─ Tasks attached: Discovery → Planning → Output
      └─ Output: IMPL_PLAN.md, IMPL-*.json, TODO_LIST.md

Phase 6: TDD Structure Validation
   └─ Ref: phases/06-tdd-structure-validation.md
      └─ Output: Validation report + Plan Confirmation Gate

Plan Confirmation (User Decision Gate):
   └─ Decision (user choice):
      ├─ "Verify TDD Compliance" (Recommended) → Route to Phase 7 (tdd-verify)
      ├─ "Start Execution" → Skill(skill="workflow-execute")
      └─ "Review Status Only" → Display session status inline
```

### Verify Mode

```
Phase 7: TDD Verification
   └─ Ref: phases/07-tdd-verify.md
      └─ Output: TDD_COMPLIANCE_REPORT.md with quality gate recommendation
```

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Purpose | Mode |
|-------|----------|---------|------|
| 1 | [phases/01-session-discovery.md](phases/01-session-discovery.md) | Create or discover TDD workflow session | plan |
| 2 | [phases/02-context-gathering.md](phases/02-context-gathering.md) | Gather project context and analyze codebase | plan |
| 3 | [phases/03-test-coverage-analysis.md](phases/03-test-coverage-analysis.md) | Analyze test coverage and framework detection | plan |
| 4 | [phases/04-conflict-resolution.md](phases/04-conflict-resolution.md) | Detect and resolve conflicts (conditional) | plan |
| 5 | [phases/05-tdd-task-generation.md](phases/05-tdd-task-generation.md) | Generate TDD tasks with Red-Green-Refactor cycles | plan |
| 6 | [phases/06-tdd-structure-validation.md](phases/06-tdd-structure-validation.md) | Validate TDD structure and present confirmation gate | plan |
| 7 | [phases/07-tdd-verify.md](phases/07-tdd-verify.md) | Full TDD compliance verification with quality gate | verify |

## Core Rules

1. **Start Immediately**: First action is mode detection + TaskCreate initialization, second action is phase execution
2. **No Preliminary Analysis**: Do not read files, analyze structure, or gather context before Phase 1
3. **Parse Every Output**: Extract required data from each phase output for next phase
4. **Auto-Continue via TaskList**: Check TaskList status to execute next pending phase automatically
5. **Track Progress**: Update TaskCreate/TaskUpdate dynamically with task attachment/collapse pattern
6. **Task Attachment Model**: Skill execute **attaches** sub-tasks to current workflow. Orchestrator **executes** these attached tasks itself, then **collapses** them after completion
7. **Progressive Phase Loading**: Read phase docs ONLY when that phase is about to execute
8. **DO NOT STOP**: Continuous multi-phase workflow. After executing all attached tasks, immediately collapse them and execute next phase
9. **TDD Context**: All descriptions include "TDD:" prefix

## TDD Compliance Requirements

### The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Enforcement Method**:
- Phase 5: `implementation` includes test-first steps (Red → Green → Refactor)
- Green phase: Includes test-fix-cycle configuration (max 3 iterations)
- Auto-revert: Triggered when max iterations reached without passing tests

**Verification**: Phase 6 validates Red-Green-Refactor structure in all generated tasks

### TDD Compliance Checkpoint

| Checkpoint | Validation Phase | Evidence Required |
|------------|------------------|-------------------|
| Test-first structure | Phase 5 | `implementation` has 3 steps |
| Red phase exists | Phase 6 | Step 1: `tdd_phase: "red"` |
| Green phase with test-fix | Phase 6 | Step 2: `tdd_phase: "green"` + test-fix-cycle |
| Refactor phase exists | Phase 6 | Step 3: `tdd_phase: "refactor"` |

### Core TDD Principles

**Red Flags - STOP and Reassess**:
- Code written before test
- Test passes immediately (no Red phase witnessed)
- Cannot explain why test should fail
- "Just this once" rationalization
- "Tests after achieve same goals" thinking

**Why Order Matters**:
- Tests written after code pass immediately → proves nothing
- Test-first forces edge case discovery before implementation
- Tests-after verify what was built, not what's required

## Input Processing

**Convert User Input to TDD Structured Format**:

1. **Simple text** → Add TDD context:
   ```
   User: "Build authentication system"

   Structured:
   TDD: Authentication System
   GOAL: Build authentication system
   SCOPE: Core authentication features
   CONTEXT: New implementation
   TEST_FOCUS: Authentication scenarios
   ```

2. **Detailed text** → Extract components with TEST_FOCUS:
   ```
   User: "Add JWT authentication with email/password login and token refresh"

   Structured:
   TDD: JWT Authentication
   GOAL: Implement JWT-based authentication
   SCOPE: Email/password login, token generation, token refresh endpoints
   CONTEXT: JWT token-based security, refresh token rotation
   TEST_FOCUS: Login flow, token validation, refresh rotation, error cases
   ```

3. **File/Issue** → Read and structure with TDD

## Data Flow

### Plan Mode

```
User Input (task description)
    ↓
[Convert to TDD Structured Format]
    ↓ Structured Description:
    ↓   TDD: [Feature Name]
    ↓   GOAL: [objective]
    ↓   SCOPE: [boundaries]
    ↓   CONTEXT: [background]
    ↓   TEST_FOCUS: [test scenarios]
    ↓
Phase 1: session:start --auto "TDD: structured-description"
    ↓ Output: sessionId
    ↓
Phase 2: context-gather --session sessionId "structured-description"
    ↓ Input: sessionId + structured description
    ↓ Output: contextPath (context-package.json) + conflictRisk
    ↓
Phase 3: test-context-gather --session sessionId
    ↓ Input: sessionId
    ↓ Output: testContextPath (test-context-package.json)
    ↓
Phase 4: conflict-resolution [conditional: conflictRisk ≥ medium]
    ↓ Input: sessionId + contextPath + conflictRisk
    ↓ Output: conflict-resolution.json
    ↓ Skip if conflictRisk is none/low → proceed directly to Phase 5
    ↓
Phase 5: task-generate-tdd --session sessionId
    ↓ Input: sessionId + all accumulated context
    ↓ Output: IMPL_PLAN.md, IMPL-*.json, TODO_LIST.md
    ↓
Phase 6: TDD Structure Validation (internal)
    ↓ Validate Red-Green-Refactor structure
    ↓ Present Plan Confirmation Gate
    ↓
Plan Confirmation (User Decision Gate):
    ├─ "Verify TDD Compliance" (Recommended) → Route to Phase 7
    ├─ "Start Execution" → Skill(skill="workflow-execute")
    └─ "Review Status Only" → Display session status inline
```

### Verify Mode

```
Input: --session sessionId (or auto-detect)
    ↓
Phase 7: Session discovery → Chain validation → Coverage analysis → Report
    ↓ Output: TDD_COMPLIANCE_REPORT.md with quality gate
```

**Session Memory Flow**: Each phase receives session ID, which provides access to:
- Previous task summaries
- Existing context and analysis
- Session-specific configuration

## TodoWrite Pattern

**Core Concept**: Dynamic task attachment and collapse for real-time visibility into TDD workflow execution.

> **Implementation Note**: Phase files use `TodoWrite` syntax to describe the conceptual tracking pattern. At runtime, these are implemented via `TaskCreate/TaskUpdate/TaskList` tools. Map as follows:
> - Initial list creation → `TaskCreate` for each item
> - Status changes → `TaskUpdate({ taskId, status })`
> - Sub-task attachment → `TaskCreate` + `TaskUpdate({ addBlockedBy })`
> - Sub-task collapse → `TaskUpdate({ status: "completed" })` + `TaskUpdate({ status: "deleted" })` for collapsed sub-items

### Key Principles

1. **Task Attachment** (when phase executed):
   - Sub-tasks are **attached** to orchestrator's TodoWrite
   - **Phase 3, 4, 5**: Multiple sub-tasks attached
   - **Phase 1, 2, 6**: Single task (atomic)
   - First attached task marked as `in_progress`, others as `pending`
   - Orchestrator **executes** these attached tasks sequentially

2. **Task Collapse** (after sub-tasks complete):
   - **Applies to Phase 3, 4, 5**: Remove detailed sub-tasks from TodoWrite
   - **Collapse** to high-level phase summary
   - **Phase 1, 2, 6**: No collapse needed (single task, just mark completed)
   - Maintains clean orchestrator-level view

3. **Continuous Execution**: After completion, automatically proceed to next pending phase

**Lifecycle**: Initial pending → Phase executed (tasks ATTACHED) → Sub-tasks executed sequentially → Phase completed (tasks COLLAPSED for 3/4/5, marked completed for 1/2/6) → Next phase → Repeat

### Initial State (Plan Mode):
```json
[
  {"content": "Phase 1: Session Discovery", "status": "in_progress", "activeForm": "Executing session discovery"},
  {"content": "Phase 2: Context Gathering", "status": "pending", "activeForm": "Executing context gathering"},
  {"content": "Phase 3: Test Coverage Analysis", "status": "pending", "activeForm": "Executing test coverage analysis"},
  {"content": "Phase 5: TDD Task Generation", "status": "pending", "activeForm": "Executing TDD task generation"},
  {"content": "Phase 6: TDD Structure Validation", "status": "pending", "activeForm": "Validating TDD structure"}
]
```

**Note**: Phase 4 (Conflict Resolution) is added dynamically after Phase 2 if conflictRisk ≥ medium.

### Phase 3 (Tasks Attached):
```json
[
  {"content": "Phase 1: Session Discovery", "status": "completed"},
  {"content": "Phase 2: Context Gathering", "status": "completed"},
  {"content": "Phase 3: Test Coverage Analysis", "status": "in_progress"},
  {"content": "  → Detect test framework and conventions", "status": "in_progress"},
  {"content": "  → Analyze existing test coverage", "status": "pending"},
  {"content": "  → Identify coverage gaps", "status": "pending"},
  {"content": "Phase 5: TDD Task Generation", "status": "pending"},
  {"content": "Phase 6: TDD Structure Validation", "status": "pending"}
]
```

### Phase 3 (Collapsed):
```json
[
  {"content": "Phase 1: Session Discovery", "status": "completed"},
  {"content": "Phase 2: Context Gathering", "status": "completed"},
  {"content": "Phase 3: Test Coverage Analysis", "status": "completed"},
  {"content": "Phase 5: TDD Task Generation", "status": "pending"},
  {"content": "Phase 6: TDD Structure Validation", "status": "pending"}
]
```

### Phase 5 (Tasks Attached):
```json
[
  {"content": "Phase 1: Session Discovery", "status": "completed"},
  {"content": "Phase 2: Context Gathering", "status": "completed"},
  {"content": "Phase 3: Test Coverage Analysis", "status": "completed"},
  {"content": "Phase 5: TDD Task Generation", "status": "in_progress"},
  {"content": "  → Discovery - analyze TDD requirements", "status": "in_progress"},
  {"content": "  → Planning - design Red-Green-Refactor cycles", "status": "pending"},
  {"content": "  → Output - generate IMPL tasks with internal TDD phases", "status": "pending"},
  {"content": "Phase 6: TDD Structure Validation", "status": "pending"}
]
```

**Note**: See individual Phase descriptions for detailed TodoWrite Update examples.

## Post-Phase Updates

### Memory State Check

After heavy phases (Phase 2-3), evaluate context window usage:
- If memory usage is high (>110K tokens or approaching context limits):
  ```javascript
  Skill(skill="memory-capture")
  ```
- Memory compaction is particularly important after analysis phases

### Planning Notes (Optional)

Similar to workflow-plan, a `planning-notes.md` can accumulate context across phases if needed. See Phase 1 for initialization.

## Error Handling

- **Parsing Failure**: If output parsing fails, retry command once, then report error
- **Validation Failure**: Report which file/data is missing or invalid
- **Command Failure**: Keep phase `in_progress`, report error to user, do not proceed
- **TDD Validation Failure**: Report incomplete chains or wrong dependencies
- **Session Not Found** (verify mode): Report error with available sessions list

### Error Handling Quick Reference

| Error Type | Detection | Recovery Action |
|------------|-----------|-----------------|
| Parsing failure | Empty/malformed output | Retry once, then report |
| Missing context-package | File read error | Re-run Phase 2 (context-gathering) |
| Invalid task JSON | jq parse error | Report malformed file path |
| Task count exceeds 18 | Count validation ≥19 | Request re-scope, split into multiple sessions |
| Missing cli_execution.id | All tasks lack ID | Regenerate tasks with phase 0 user config |
| Test-context missing | File not found | Re-run Phase 3 (test-coverage-analysis) |
| Phase timeout | No response | Retry phase, check CLI connectivity |
| CLI tool not available | Tool not in cli-tools.json | Fall back to alternative preferred tool |

### TDD Warning Patterns

| Pattern | Warning Message | Recommended Action |
|---------|----------------|-------------------|
| Task count >10 | High task count detected | Consider splitting into multiple sessions |
| Missing test-fix-cycle | Green phase lacks auto-revert | Add `max_iterations: 3` to task config |
| Red phase missing test path | Test file path not specified | Add explicit test file paths |
| Generic task names | Vague names like "Add feature" | Use specific behavior descriptions |
| No refactor criteria | Refactor phase lacks completion criteria | Define clear refactor scope |

### Non-Blocking Warning Policy

**All warnings are advisory** - they do not halt execution:
1. Warnings logged to `.process/tdd-warnings.log`
2. Summary displayed in Phase 6 output
3. User decides whether to address before `workflow-execute` skill

## Coordinator Checklist

### Plan Mode
- **Pre-Phase**: Convert user input to TDD structured format (TDD/GOAL/SCOPE/CONTEXT/TEST_FOCUS)
- Initialize TaskCreate before any command (Phase 4 added dynamically after Phase 2)
- Execute Phase 1 immediately with structured description
- Parse session ID from Phase 1 output, store in memory
- Pass session ID and structured description to Phase 2 command
- Parse context path from Phase 2 output, store in memory
- **Extract conflictRisk from context-package.json**: Determine Phase 4 execution
- Execute Phase 3 (test coverage analysis) with sessionId
- Parse testContextPath from Phase 3 output, store in memory
- **If conflictRisk ≥ medium**: Launch Phase 4 conflict-resolution with sessionId and contextPath
- Wait for Phase 4 to finish executing (if executed), verify conflict-resolution.json created
- **If conflictRisk is none/low**: Skip Phase 4, proceed directly to Phase 5
- Pass session ID to Phase 5 command (TDD task generation)
- Verify all Phase 5 outputs (IMPL_PLAN.md, IMPL-*.json, TODO_LIST.md)
- Execute Phase 6 (internal TDD structure validation)
- **Plan Confirmation Gate**: Present user with choice (Verify → Phase 7 / Execute / Review Status)
- **If user selects Verify**: Read phases/07-tdd-verify.md, execute Phase 7 in-process
- **If user selects Execute**: Skill(skill="workflow-execute")
- **If user selects Review**: Display session status inline
- **Auto mode (workflowPreferences.autoYes)**: Auto-select "Verify TDD Compliance", then auto-continue to execute if APPROVED
- Update TaskCreate/TaskUpdate after each phase
- After each phase, automatically continue to next phase based on TaskList status

### Verify Mode
- Detect/validate session (from --session flag or auto-detect)
- Initialize TaskCreate with verification tasks
- Execute Phase 7 through all sub-phases (session validation → chain validation → coverage analysis → report generation)
- Present quality gate result and next step options

## Related Skills

**Prerequisite Skills**:
- None - TDD planning is self-contained (can optionally run brainstorm commands before)

**Called by Plan Mode** (6 phases):
- `/workflow:session:start` - Phase 1: Create or discover TDD workflow session
- `phases/02-context-gathering.md` - Phase 2: Gather project context and analyze codebase (inline)
- `phases/03-test-coverage-analysis.md` - Phase 3: Analyze existing test patterns and coverage (inline)
- `phases/04-conflict-resolution.md` - Phase 4: Detect and resolve conflicts (inline, conditional)
- `memory-capture` skill - Phase 4: Memory optimization (if context approaching limits)
- `phases/05-tdd-task-generation.md` - Phase 5: Generate TDD tasks with Red-Green-Refactor cycles (inline)

**Called by Verify Mode**:
- `phases/07-tdd-verify.md` - Phase 7: Test coverage and cycle analysis (inline)

**Follow-up Skills**:
- `workflow-tdd` skill (tdd-verify phase) - Verify TDD compliance (can also invoke via verify mode)
- `workflow-plan` skill (plan-verify phase) - Verify plan quality and dependencies
- Display session status inline - Review TDD task breakdown
- `Skill(skill="workflow-execute")` - Begin TDD implementation
