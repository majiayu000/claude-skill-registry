---
name: workflow-test-fix
description: Unified test-fix pipeline combining test generation (session, context, analysis, task gen) with iterative test-cycle execution (adaptive strategy, progressive testing, CLI fallback). Triggers on "workflow:test-fix-gen", "workflow:test-cycle-execute", "test fix workflow".
allowed-tools: Skill, Task, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow Test Fix

Unified test-fix orchestrator that combines **test planning generation** (Phase 1-4) with **iterative test-cycle execution** (Phase 5) into a single end-to-end pipeline. Creates test sessions with progressive L0-L3 test layers, generates test tasks, then executes them with adaptive fix cycles until pass rate >= 95% or max iterations reached.

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────────┐
│  Workflow Test Fix Orchestrator (SKILL.md)                                │
│  → Pure coordinator: Route entry point, track progress, pass context      │
│  → Five phases: Session → Context → Analysis → TaskGen → Execution       │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
  ┌────────────┬────────────┬──────┴──────┬────────────┬────────────┐
  ↓            ↓            ↓             ↓            ↓
┌──────────┐┌──────────┐┌──────────┐┌──────────┐    ┌──────────────┐
│ Phase 1  ││ Phase 2  ││ Phase 3  ││ Phase 4  │    │  Phase 5     │
│ Session  ││ Context  ││ Analysis ││ Task Gen │    │  Test Cycle  │
│ Start    ││ Gather   ││ Enhanced ││ Generate │    │  Execute     │
│          ││          ││          ││          │    │              │
│ Input    ││ Coverage ││ Gemini   ││ IMPL_PLAN│    │  1. Discovery│
│ Detect + ││ or Code  ││ L0-L3   ││ IMPL-*   │    │  2. Execute  │
│ Session  ││ Scan     ││ AI Issue ││ TODO_LIST│    │  3. Fix Loop │
│ Create   ││          ││          ││          │    │  4. Complete │
└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘    └──────────────┘
     │           │           │           │                  ↑
     │testSessionId          │           │                  │
     └──→────────┘contextPath│           │                  │
                  └──→───────┘AnalysisRes│                  │
                               └──→──────┘ testSessionId    │
                                          └──→──(Summary)──→┘

Task Pipeline (generated in Phase 4, executed in Phase 5):
┌──────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌──────────────┐
│  IMPL-001    │──→│  IMPL-001.3     │──→│  IMPL-001.5     │──→│  IMPL-002    │
│  Test Gen    │   │  Code Validate  │   │  Quality Gate   │   │  Test & Fix  │
│  L1-L3       │   │  L0 + AI Issues │   │  Coverage 80%+  │   │  Max N iter  │
│@code-developer│  │ @test-fix-agent │   │ @test-fix-agent │   │@test-fix-agent│
└──────────────┘   └─────────────────┘   └─────────────────┘   └──────────────┘
```

## Key Design Principles

1. **Unified Pipeline**: Generation and execution are one continuous workflow - no manual handoff
2. **Pure Orchestrator**: SKILL.md coordinates only - delegates all execution detail to phase files
3. **Auto-Continue**: Phase 1→2→3→4→(Summary)→5 automatically
4. **Task Attachment/Collapse**: Sub-tasks attached during phase execution, collapsed after completion
5. **Progressive Phase Loading**: Phase docs read **only** when that phase executes, not upfront
6. **Adaptive Strategy**: Fix loop auto-selects strategy (conservative/aggressive/surgical) based on iteration context
7. **Quality Gate**: Pass rate >= 95% (criticality-aware) terminates the fix loop
8. **Phase File Hygiene**: Phase files reference `workflowPreferences.*` for preferences, no CLI flag parsing

## Usage

Full pipeline and execute-only modes are triggered by skill name routing (see Mode Detection). Workflow preferences (auto mode) are collected interactively via AskUserQuestion before dispatching to phases.

**Full pipeline** (workflow:test-fix-gen): Task description or session ID as arguments → interactive preference collection → generate + execute pipeline
**Execute only** (workflow:test-cycle-execute): Auto-discovers active session → interactive preference collection → execution loop

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

## Execution Flow

```
Entry Point Detection:
   ├─ /workflow:test-fix-gen → Full Pipeline (Phase 1→2→3→4→Summary→5)
   └─ /workflow:test-cycle-execute → Execution Only (Phase 5)

Phase 1: Session Start (session-start)
   └─ Ref: phases/01-session-start.md
      ├─ Step 1.0: Detect input mode (session | prompt)
      ├─ Step 1.1: Create test session → testSessionId
      └─ Output: testSessionId, MODE

Phase 2: Test Context Gather (test-context-gather)
   └─ Ref: phases/02-test-context-gather.md
      ├─ Step 1.2: Gather test context → contextPath
      └─ Output: contextPath

Phase 3: Test Concept Enhanced (test-concept-enhanced)
   └─ Ref: phases/03-test-concept-enhanced.md
      ├─ Step 1.3: Test analysis (Gemini) → TEST_ANALYSIS_RESULTS.md
      └─ Output: TEST_ANALYSIS_RESULTS.md

Phase 4: Test Task Generate (test-task-generate)
   └─ Ref: phases/04-test-task-generate.md
      ├─ Step 1.4: Generate test tasks → IMPL_PLAN.md, IMPL-*.json, TODO_LIST.md
      └─ Output: testSessionId, 4+ task JSONs

Summary Output (inline after Phase 4):
   └─ Display summary, auto-continue to Phase 5

Phase 5: Test Cycle Execution (test-cycle-execute)
   └─ Ref: phases/05-test-cycle-execute.md
      ├─ Step 2.1: Discovery (load session, tasks, iteration state)
      ├─ Step 2.2: Execute initial tasks (IMPL-001 → 001.3 → 001.5 → 002)
      ├─ Step 2.3: Fix loop (if pass_rate < 95%)
      │   ├─ Select strategy: conservative/aggressive/surgical
      │   ├─ Generate fix task via @cli-planning-agent
      │   ├─ Execute fix via @test-fix-agent
      │   └─ Re-test → loop or exit
      └─ Step 2.4: Completion (summary, session archive)
         └─ Output: final pass_rate, summary
```

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Purpose |
|-------|----------|---------|
| 1 | [phases/01-session-start.md](phases/01-session-start.md) | Detect input mode, create test session |
| 2 | [phases/02-test-context-gather.md](phases/02-test-context-gather.md) | Gather test context (coverage/codebase) |
| 3 | [phases/03-test-concept-enhanced.md](phases/03-test-concept-enhanced.md) | Gemini analysis, L0-L3 test requirements |
| 4 | [phases/04-test-task-generate.md](phases/04-test-task-generate.md) | Generate task JSONs and IMPL_PLAN.md |
| 5 | [phases/05-test-cycle-execute.md](phases/05-test-cycle-execute.md) | Execute tasks, iterative fix cycles, completion |

## Core Rules

1. **Start Immediately**: First action is TaskCreate initialization, second action is Phase 1 (or Phase 5 for execute-only entry)
2. **No Preliminary Analysis**: Do not read files or gather context before starting the phase
3. **Parse Every Output**: Extract required data from each step output for next step
4. **Auto-Continue**: Phase 1→2→3→4→(Summary)→5 automatically (for full pipeline entry)
5. **Track Progress**: Update TaskCreate/TaskUpdate dynamically with task attachment/collapse pattern
6. **Task Attachment Model**: Sub-tasks **attached** during phase, **collapsed** after completion
7. **DO NOT STOP**: Continuous workflow until quality gate met or max iterations reached
8. **Progressive Loading**: Read phase doc ONLY when that phase is about to execute
9. **Entry Point Routing**: `workflow-test-fix` skill → Phase 1-5; `workflow-test-fix` skill → Phase 5 only

## Input Processing

### test-fix-gen Entry (Full Pipeline)
```
User input → Detect type:
  ├─ Starts with "WFS-" → MODE=session, sourceSessionId=input
  ├─ Ends with ".md"    → MODE=prompt, description=Read(input)
  └─ Otherwise          → MODE=prompt, description=input
```

### test-cycle-execute Entry (Phase 5 Only)
```
Arguments → Parse flags:
  ├─ --resume-session="WFS-xxx" → sessionId=WFS-xxx
  ├─ --max-iterations=N         → maxIterations=N (default: 10)
  └─ (no args)                  → auto-discover active test session
```

## Data Flow

```
User Input (session ID | description | file path)
    ↓
[Detect Mode: session | prompt]
    ↓
Phase 1: Session Start ─────────────────────────────────────────
    ↓ 1.0+1.1: session:start → testSessionId, MODE
    ↓
Phase 2: Test Context Gather ────────────────────────────────────
    ↓ 1.2: test-context-gather/context-gather → contextPath
    ↓
Phase 3: Test Concept Enhanced ──────────────────────────────────
    ↓ 1.3: test-concept-enhanced → TEST_ANALYSIS_RESULTS.md
    ↓
Phase 4: Test Task Generate ─────────────────────────────────────
    ↓ 1.4: test-task-generate → IMPL_PLAN.md, IMPL-*.json, TODO_LIST.md
    ↓
Summary Output (inline) ─────────────────────────────────────────
    ↓ Display summary with next step
    ↓
Phase 5: Test Cycle Execution ───────────────────────────────────
    ↓ 2.1: Load session + tasks + iteration state
    ↓ 2.2: Execute IMPL-001 → 001.3 → 001.5 → 002
    ↓ 2.3: Fix loop (analyze → fix → retest) until pass_rate >= 95%
    ↓ 2.4: Completion → summary → session archive
```

## Summary Output (after Phase 4)

After Phase 4 completes, display the following summary before auto-continuing to Phase 5:

```
Test-fix workflow created successfully!

Input: [original input]
Mode: [Session|Prompt]
Test Session: [testSessionId]

Tasks Created:
- IMPL-001: Test Understanding & Generation (@code-developer)
- IMPL-001.3: Code Validation Gate - AI Error Detection (@test-fix-agent)
- IMPL-001.5: Test Quality Gate - Static Analysis & Coverage (@test-fix-agent)
- IMPL-002: Test Execution & Fix Cycle (@test-fix-agent)

Quality Thresholds:
- Code Validation: Zero CRITICAL issues, zero compilation errors
- Minimum Coverage: 80% line, 70% branch
- Static Analysis: Zero critical anti-patterns
- Max Fix Iterations: 5

Review artifacts:
- Test plan: .workflow/[testSessionId]/IMPL_PLAN.md
- Task list: .workflow/[testSessionId]/TODO_LIST.md
- Analysis: .workflow/[testSessionId]/.process/TEST_ANALYSIS_RESULTS.md
```

**CRITICAL - Next Step**: Auto-continue to Phase 5: Test Cycle Execution.
Pass `testSessionId` to Phase 5 for test execution pipeline. Do NOT wait for user confirmation — the unified pipeline continues automatically.

## Test Strategy Overview

Progressive Test Layers (L0-L3):

| Layer | Name | Focus |
|-------|------|-------|
| **L0** | Static Analysis | Compilation, imports, types, AI code issues |
| **L1** | Unit Tests | Function/class behavior (happy/negative/edge cases) |
| **L2** | Integration Tests | Component interactions, API contracts, failure modes |
| **L3** | E2E Tests | User journeys, critical paths (optional) |

**Quality Thresholds**:
- Code Validation (IMPL-001.3): Zero CRITICAL issues, zero compilation errors
- Minimum Coverage: 80% line, 70% branch
- Static Analysis (IMPL-001.5): Zero critical anti-patterns
- Pass Rate Gate: >= 95% (criticality-aware) or 100%
- Max Fix Iterations: 10 (default, adjustable)

## Strategy Engine (Phase 5)

| Strategy | Trigger | Behavior |
|----------|---------|----------|
| **Conservative** | Iteration 1-2 (default) | Single targeted fix, full validation |
| **Aggressive** | Pass rate >80% + similar failures | Batch fix related issues |
| **Surgical** | Regression detected (pass rate drops >10%) | Minimal changes, rollback focus |

Selection logic and CLI fallback chain (Gemini → Qwen → Codex) are detailed in Phase 5.

## Agent Roles

| Agent | Used In | Responsibility |
|-------|---------|---------------|
| **Orchestrator** | All phases | Route entry, track progress, pass context |
| **@code-developer** | Phase 5 (IMPL-001) | Test generation (L1-L3) |
| **@test-fix-agent** | Phase 5 | Test execution, code fixes, criticality assignment |
| **@cli-planning-agent** | Phase 5 (fix loop) | CLI analysis, root cause extraction, fix task generation |

## TodoWrite Pattern

**Core Concept**: Dynamic task tracking with attachment/collapse for real-time visibility.

> **Implementation Note**: Phase files use `TodoWrite` syntax to describe the conceptual tracking pattern. At runtime, these are implemented via `TaskCreate/TaskUpdate/TaskList` tools from the allowed-tools list. Map `TodoWrite` examples as follows:
> - Initial list creation → `TaskCreate` for each item
> - Status changes → `TaskUpdate({ taskId, status })`
> - Sub-task attachment → `TaskCreate` + `TaskUpdate({ addBlockedBy })`
> - Sub-task collapse → `TaskUpdate({ status: "completed" })` + `TaskUpdate({ status: "deleted" })` for collapsed sub-items

### Full Pipeline (Phase 1-5)

```json
[
  {"content": "Phase 1: Session Start", "status": "in_progress"},
  {"content": "Phase 2: Test Context Gather", "status": "pending"},
  {"content": "Phase 3: Test Analysis (Gemini)", "status": "pending"},
  {"content": "Phase 4: Test Task Generate", "status": "pending"},
  {"content": "Phase 5: Test Cycle Execution", "status": "pending"}
]
```

### Phase 1-4 Collapsed → Phase 5 Active

```json
[
  {"content": "Phase 1: Session Start", "status": "completed"},
  {"content": "Phase 2: Test Context Gather", "status": "completed"},
  {"content": "Phase 3: Test Analysis (Gemini)", "status": "completed"},
  {"content": "Phase 4: Test Task Generate", "status": "completed"},
  {"content": "Phase 5: Test Cycle Execution", "status": "in_progress"},
  {"content": "  → Execute IMPL-001 [code-developer]", "status": "in_progress"},
  {"content": "  → Execute IMPL-001.3 [test-fix-agent]", "status": "pending"},
  {"content": "  → Execute IMPL-001.5 [test-fix-agent]", "status": "pending"},
  {"content": "  → Execute IMPL-002 [test-fix-agent]", "status": "pending"},
  {"content": "  → Fix Loop", "status": "pending"}
]
```

### Fix Loop Iterations

```json
[
  {"content": "Phase 1-4: Test Generation", "status": "completed"},
  {"content": "Phase 5: Test Cycle Execution", "status": "in_progress"},
  {"content": "  → Initial tasks", "status": "completed"},
  {"content": "  → Iteration 1: Initial test (pass: 70%, conservative)", "status": "completed"},
  {"content": "  → Iteration 2: Fix validation (pass: 82%, conservative)", "status": "completed"},
  {"content": "  → Iteration 3: Batch fix (pass: 89%, aggressive)", "status": "in_progress"}
]
```

## Session File Structure

```
.workflow/active/WFS-test-{session}/
├── workflow-session.json              # Session metadata
├── IMPL_PLAN.md                       # Test generation and execution strategy
├── TODO_LIST.md                       # Task checklist
├── .task/
│   ├── IMPL-001.json                  # Test understanding & generation
│   ├── IMPL-001.3-validation.json     # Code validation gate
│   ├── IMPL-001.5-review.json         # Test quality gate
│   ├── IMPL-002.json                  # Test execution & fix cycle
│   └── IMPL-fix-{N}.json             # Generated fix tasks (Phase 5 fix loop)
├── .process/
│   ├── [test-]context-package.json    # Context and coverage analysis
│   ├── TEST_ANALYSIS_RESULTS.md       # Test requirements (L0-L3)
│   ├── iteration-state.json           # Current iteration + strategy + stuck tests
│   ├── test-results.json              # Latest results (pass_rate, criticality)
│   ├── test-output.log                # Full test output
│   ├── fix-history.json               # All fix attempts
│   ├── iteration-{N}-analysis.md      # CLI analysis report
│   └── iteration-{N}-cli-output.txt
└── .summaries/
    └── iteration-summaries/
```

## Error Handling

### Phase 1-4 (Generation)

| Phase | Error Condition | Action |
|-------|----------------|--------|
| 1: Session Start | Source session not found (session mode) | Return error with session ID |
| 1: Session Start | No completed IMPL tasks (session mode) | Return error, source incomplete |
| 2: Context Gather | Context gathering failed | Return error, check source artifacts |
| 3: Analysis | Gemini analysis failed | Return error, check context package |
| 4: Task Gen | Task generation failed | Retry once, then return error |

### Phase 5 (Execution)

| Scenario | Action |
|----------|--------|
| Test execution error | Log, retry with error context |
| CLI analysis failure | Fallback: Gemini → Qwen → Codex → manual |
| Agent execution error | Save state, retry with simplified context |
| Max iterations reached | Generate failure report, mark blocked |
| Regression detected | Rollback last fix, switch to surgical strategy |
| Stuck tests detected | Continue with alternative strategy, document |

## Commit Strategy (Phase 5)

Automatic commits at key checkpoints:
1. **After successful iteration** (pass rate increased): `test-cycle: iteration N - strategy (pass: old% → new%)`
2. **Before rollback** (regression detected): `test-cycle: rollback iteration N - regression detected`

## Completion Conditions

| Condition | Pass Rate | Action |
|-----------|-----------|--------|
| **Full Success** | 100% | Auto-complete session |
| **Partial Success** | >= 95%, all failures low criticality | Auto-approve with review note |
| **Failure** | < 95% after max iterations | Failure report, mark blocked |

## Post-Completion Expansion

After completion, ask user if they want to expand into issues (test/enhance/refactor/doc). Selected items call `/issue:new "{summary} - {dimension}"`.

## Coordinator Checklist

### Phase 1 (session-start)
- [ ] Detect input type (session ID / description / file path)
- [ ] Initialize TaskCreate before any execution
- [ ] Read Phase 1 doc, execute Steps 1.0 + 1.1
- [ ] Parse testSessionId from step output, store in memory

### Phase 2 (test-context-gather)
- [ ] Read Phase 2 doc, execute Step 1.2
- [ ] Parse contextPath from step output, store in memory

### Phase 3 (test-concept-enhanced)
- [ ] Read Phase 3 doc, execute Step 1.3
- [ ] Verify TEST_ANALYSIS_RESULTS.md created

### Phase 4 (test-task-generate)
- [ ] Read Phase 4 doc, execute Step 1.4
- [ ] Verify all Phase 1-4 outputs (4 task JSONs, IMPL_PLAN.md, TODO_LIST.md)
- [ ] Display Summary output (inline)
- [ ] Collapse Phase 1-4 tasks, auto-continue to Phase 5

### Phase 5 (test-cycle-execute)
- [ ] Read Phase 5 doc
- [ ] Load session, tasks, iteration state
- [ ] Execute initial tasks sequentially
- [ ] Calculate pass rate from test-results.json
- [ ] If pass_rate < 95%: Enter fix loop
- [ ] Track iteration count, stuck tests, regression
- [ ] If pass_rate >= 95% or max iterations: Complete
- [ ] Generate completion summary
- [ ] Offer post-completion expansion

## Related Skills

**Prerequisite Skills**:
- `workflow-plan` skill or `workflow-execute` skill - Complete implementation (Session Mode source)
- None for Prompt Mode

**Follow-up Skills**:
- Display session status inline - Review workflow state
- `review-cycle` skill - Post-implementation review
- `/issue:new` - Create follow-up issues
