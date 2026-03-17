---
name: review-cycle
description: Unified multi-dimensional code review with automated fix orchestration. Supports session-based (git changes) and module-based (path patterns) review modes with 7-dimension parallel analysis, iterative deep-dive, and automated fix pipeline. Triggers on "workflow:review-cycle", "workflow:review-session-cycle", "workflow:review-module-cycle", "workflow:review-cycle-fix".
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# Review Cycle

Unified multi-dimensional code review orchestrator with dual-mode (session/module) file discovery, 7-dimension parallel analysis, iterative deep-dive on critical findings, and optional automated fix pipeline with intelligent batching and parallel planning.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│  Review Cycle Orchestrator (SKILL.md)                                │
│  → Pure coordinator: mode detection, phase dispatch, state tracking  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
  ┌─────────────────────────────┼─────────────────────────────────┐
  │           Review Pipeline (Phase 1-5)                          │
  │                                                                │
  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
  │  │ Phase 1 │→ │ Phase 2 │→ │ Phase 3 │→ │ Phase 4 │→ │ Phase 5 │
  │  │Discovery│  │Parallel │  │Aggregate│  │Deep-Dive│  │Complete │
  │  │  Init   │  │ Review  │  │         │  │(cond.)  │  │         │
  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
  │   session|      7 agents     severity     N agents     finalize
  │   module        ×cli-explore  calc        ×cli-explore  state
  │                                  ↕ loop
  └────────────────────────────────────────────────────────────────┘
                                │
                          (optional --fix)
                                │
  ┌─────────────────────────────┼─────────────────────────────────┐
  │           Fix Pipeline (Phase 6-9)                             │
  │                                                                │
  │  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐
  │  │ Phase 6 │→ │ Phase 7 │→ │Phase 7.5 │→ │ Phase 8 │→ │ Phase 9 │
  │  │Discovery│  │Parallel │  │Export to │  │Execution│  │Complete │
  │  │Batching │  │Planning │  │Task JSON │  │Orchestr.│  │         │
  │  └─────────┘  └─────────┘  └──────────┘  └─────────┘  └─────────┘
  │   grouping     N agents     fix-plan →    M agents     aggregate
  │   + batch      ×cli-plan    .task/FIX-*   ×cli-exec    + summary
  └────────────────────────────────────────────────────────────────────┘
```

## Key Design Principles

1. **Dual-Mode Review**: Session-based (git changes) and module-based (path patterns) share the same review pipeline (Phase 2-5), differing only in file discovery (Phase 1)
2. **Pure Orchestrator**: Execute phases in sequence, parse outputs, pass context between them
3. **Progressive Phase Loading**: Phase docs are read on-demand when that phase executes, not all at once
4. **Auto-Continue**: All phases run autonomously without user intervention between phases
5. **Subagent Lifecycle**: Explicit lifecycle management with spawn_agent → wait → close_agent
6. **Role Path Loading**: Subagent roles loaded via path reference in MANDATORY FIRST STEPS
7. **Optional Fix Pipeline**: Phase 6-9 triggered only by explicit `--fix` flag or user confirmation after Phase 5
8. **Content Preservation**: All agent prompts, code, schemas preserved verbatim from source commands

## Usage

```
# Review Pipeline (Phase 1-5)
review-cycle <path-pattern>                                    # Module mode
review-cycle [session-id]                                      # Session mode
review-cycle [session-id|path-pattern] [FLAGS]                 # With flags

# Fix Pipeline (Phase 6-9)
review-cycle --fix <review-dir|export-file>                    # Fix mode
review-cycle --fix <review-dir> [FLAGS]                        # Fix with flags

# Flags
--dimensions=dim1,dim2,...    Custom dimensions (default: all 7)
--max-iterations=N           Max deep-dive iterations (default: 3)
--fix                        Enter fix pipeline after review or standalone
--resume                     Resume interrupted fix session
--batch-size=N               Findings per planning batch (default: 5, fix mode only)
--export-tasks               Export fix-plan findings to .task/FIX-*.json (auto-enabled with --fix)

# Examples
review-cycle src/auth/**                                       # Module: review auth
review-cycle src/auth/**,src/payment/**                        # Module: multiple paths
review-cycle src/auth/** --dimensions=security,architecture    # Module: custom dims
review-cycle WFS-payment-integration                           # Session: specific
review-cycle                                                   # Session: auto-detect
review-cycle --fix ${projectRoot}/.workflow/active/WFS-123/.review/           # Fix: from review dir
review-cycle --fix --resume                                    # Fix: resume session
```

## Mode Detection

```javascript
// Input parsing logic (orchestrator responsibility)
function detectMode(args) {
  if (args.includes('--fix')) return 'fix';
  if (args.match(/\*|\.ts|\.js|\.py|src\/|lib\//)) return 'module';  // glob/path patterns
  if (args.match(/^WFS-/) || args.trim() === '') return 'session';   // session ID or empty
  return 'session';  // default
}
```

| Input Pattern | Detected Mode | Phase Entry |
|---------------|---------------|-------------|
| `src/auth/**` | `module` | Phase 1 (module branch) |
| `WFS-payment-integration` | `session` | Phase 1 (session branch) |
| _(empty)_ | `session` | Phase 1 (session branch, auto-detect) |
| `--fix .review/` | `fix` | Phase 6 |
| `--fix --resume` | `fix` | Phase 6 (resume) |

## Execution Flow

```
Input Parsing:
   └─ Detect mode (session|module|fix) → route to appropriate phase entry

Review Pipeline (session or module mode):

Phase 1: Discovery & Initialization
   └─ Ref: phases/01-discovery-initialization.md
      ├─ Session mode: session discovery → git changed files → resolve
      ├─ Module mode: path patterns → glob expand → resolve
      └─ Common: create session, output dirs, review-state.json, review-progress.json

Phase 2: Parallel Review Coordination
   └─ Ref: phases/02-parallel-review.md
      ├─ Spawn 7 cli-explore-agent instances (Deep Scan mode)
      ├─ Each produces dimensions/{dimension}.json + reports/{dimension}-analysis.md
      ├─ Lifecycle: spawn_agent → batch wait → close_agent
      └─ CLI fallback: Gemini → Qwen → Codex

Phase 3: Aggregation
   └─ Ref: phases/03-aggregation.md
      ├─ Load dimension JSONs, calculate severity distribution
      ├─ Identify cross-cutting concerns (files in 3+ dimensions)
      └─ Decision: critical > 0 OR high > 5 OR critical files → Phase 4
                   Else → Phase 5

Phase 4: Iterative Deep-Dive (conditional)
   └─ Ref: phases/04-iterative-deep-dive.md
      ├─ Select critical findings (max 5 per iteration)
      ├─ Spawn deep-dive agents for root cause analysis
      ├─ Re-assess severity → loop back to Phase 3 aggregation
      └─ Exit when: no critical findings OR max iterations reached

Phase 5: Review Completion
   └─ Ref: phases/05-review-completion.md
      ├─ Finalize review-state.json + review-progress.json
      ├─ Prompt user: "Run automated fixes? [Y/n]"
      └─ If yes → Continue to Phase 6

Fix Pipeline (--fix mode or after Phase 5):

Phase 6: Fix Discovery & Batching
   └─ Ref: phases/06-fix-discovery-batching.md
      ├─ Validate export file, create fix session
      └─ Intelligent grouping by file+dimension similarity → batches

Phase 7: Fix Parallel Planning
   └─ Ref: phases/07-fix-parallel-planning.md
      ├─ Spawn N cli-planning-agent instances (≤10 parallel)
      ├─ Each outputs partial-plan-{batch-id}.json
      ├─ Lifecycle: spawn_agent → batch wait → close_agent
      └─ Orchestrator aggregates → fix-plan.json

Phase 7.5: Export to Task JSON (auto with --fix, or explicit --export-tasks)
   └─ Convert fix-plan.json findings → .task/FIX-{seq}.json
      ├─ For each finding in fix-plan.json:
      │   ├─ finding.file          → files[].path (action: "modify")
      │   ├─ finding.severity      → priority (critical|high|medium|low)
      │   ├─ finding.fix_description → description
      │   ├─ finding.dimension     → scope
      │   ├─ finding.verification  → convergence.verification
      │   ├─ finding.changes[]     → convergence.criteria[]
      │   └─ finding.fix_steps[]   → implementation[]
      ├─ Output path: {projectRoot}/.workflow/active/WFS-{id}/.review/.task/FIX-{seq}.json
      ├─ Each file follows task-schema.json (IDENTITY + CONVERGENCE + FILES required)
      └─ source.tool = "review-cycle", source.session_id = WFS-{id}
      │
      ├─ Generate plan.json (plan-overview-fix-schema) after FIX task export:
      │   ```javascript
      │   const fixTaskFiles = Glob(`${reviewDir}/.task/FIX-*.json`)
      │   const taskIds = fixTaskFiles.map(f => JSON.parse(Read(f)).id).sort()
      │
      │   // Guard: skip plan.json if no fix tasks generated
      │   if (taskIds.length === 0) {
      │     console.warn('No fix tasks generated; skipping plan.json')
      │   } else {
      │
      │   const planOverview = {
      │     summary: `Fix plan from review cycle: ${reviewSummary}`,
      │     approach: "Review-driven fix pipeline",
      │     task_ids: taskIds,
      │     task_count: taskIds.length,
      │     complexity: taskIds.length > 5 ? "High" : taskIds.length > 2 ? "Medium" : "Low",
      │     fix_context: {
      │       root_cause: "Multiple review findings",
      │       strategy: "comprehensive_fix",
      │       severity: aggregatedFindings.maxSeverity || "Medium",  // Derived from max finding severity
      │       risk_level: aggregatedFindings.overallRisk || "medium" // Derived from combined risk assessment
      │     },
      │     test_strategy: {
      │       scope: "unit",
      │       specific_tests: [],
      │       manual_verification: ["Verify all review findings addressed"]
      │     },
      │     _metadata: {
      │       timestamp: getUtc8ISOString(),
      │       source: "review-cycle-agent",
      │       planning_mode: "agent-based",
      │       plan_type: "fix",
      │       schema_version: "2.0"
      │     }
      │   }
      │   Write(`${reviewDir}/plan.json`, JSON.stringify(planOverview, null, 2))
      │
      │   } // end guard
      │   ```
      └─ Output path: {reviewDir}/plan.json

Phase 8: Fix Execution
   └─ Ref: phases/08-fix-execution.md
      ├─ Stage-based execution per aggregated timeline
      ├─ Each group: analyze → fix → test → commit/rollback
      ├─ Lifecycle: spawn_agent → wait → close_agent per group
      └─ 100% test pass rate required

Phase 9: Fix Completion
   └─ Ref: phases/09-fix-completion.md
      ├─ Aggregate results → fix-summary.md
      └─ Optional: complete workflow session if all fixes successful

Complete: Review reports + optional fix results
```

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Load When | Source |
|-------|----------|-----------|--------|
| 1 | [phases/01-discovery-initialization.md](phases/01-discovery-initialization.md) | Review/Fix start | review-session-cycle + review-module-cycle Phase 1 (fused) |
| 2 | [phases/02-parallel-review.md](phases/02-parallel-review.md) | Phase 1 complete | Shared from both review commands Phase 2 |
| 3 | [phases/03-aggregation.md](phases/03-aggregation.md) | Phase 2 complete | Shared from both review commands Phase 3 |
| 4 | [phases/04-iterative-deep-dive.md](phases/04-iterative-deep-dive.md) | Aggregation triggers iteration | Shared from both review commands Phase 4 |
| 5 | [phases/05-review-completion.md](phases/05-review-completion.md) | No more iterations needed | Shared from both review commands Phase 5 |
| 6 | [phases/06-fix-discovery-batching.md](phases/06-fix-discovery-batching.md) | Fix mode entry | review-cycle-fix Phase 1 + 1.5 |
| 7 | [phases/07-fix-parallel-planning.md](phases/07-fix-parallel-planning.md) | Phase 6 complete | review-cycle-fix Phase 2 |
| 7.5 | _(inline in SKILL.md)_ | Phase 7 complete | Export fix-plan findings to .task/FIX-*.json |
| 8 | [phases/08-fix-execution.md](phases/08-fix-execution.md) | Phase 7.5 complete | review-cycle-fix Phase 3 |
| 9 | [phases/09-fix-completion.md](phases/09-fix-completion.md) | Phase 8 complete | review-cycle-fix Phase 4 + 5 |

## Core Rules

1. **Start Immediately**: First action is progress tracking initialization, second action is Phase 1 execution
2. **Mode Detection First**: Parse input to determine session/module/fix mode before Phase 1
3. **Parse Every Output**: Extract required data from each phase for next phase
4. **Auto-Continue**: Check progress status to execute next pending phase automatically
5. **Progressive Phase Loading**: Read phase docs ONLY when that phase is about to execute
6. **DO NOT STOP**: Continuous multi-phase workflow until all applicable phases complete
7. **Conditional Phase 4**: Only execute if aggregation triggers iteration (critical > 0 OR high > 5 OR critical files)
8. **Fix Pipeline Optional**: Phase 6-9 only execute with explicit --fix flag or user confirmation
9. **Explicit Lifecycle**: Always close_agent after wait completes to free resources

## Data Flow

```
User Input (path-pattern | session-id | --fix export-file)
    ↓
[Mode Detection: session | module | fix]
    ↓
Phase 1: Discovery & Initialization
    ↓ Output: sessionId, reviewId, resolvedFiles, reviewMode, outputDir
    ↓         review-state.json, review-progress.json
Phase 2: Parallel Review Coordination
    ↓ Output: dimensions/*.json, reports/*-analysis.md
Phase 3: Aggregation
    ↓ Output: severityDistribution, criticalFiles, deepDiveFindings
    ↓ Decision: iterate? → Phase 4 : Phase 5
Phase 4: Iterative Deep-Dive (conditional, loops with Phase 3)
    ↓ Output: iterations/*.json, reports/deep-dive-*.md
    ↓ Loop: re-aggregate → check criteria → iterate or exit
Phase 5: Review Completion
    ↓ Output: final review-state.json, review-progress.json
    ↓ Decision: fix? → Phase 6 : END
Phase 6: Fix Discovery & Batching
    ↓ Output: finding batches (in-memory)
Phase 7: Fix Parallel Planning
    ↓ Output: partial-plan-*.json → fix-plan.json (aggregated)
Phase 7.5: Export to Task JSON
    ↓ Output: .task/FIX-{seq}.json (per finding, follows task-schema.json)
Phase 8: Fix Execution
    ↓ Output: fix-progress-*.json, git commits
Phase 9: Fix Completion
    ↓ Output: fix-summary.md, fix-history.json
```

## Subagent API Reference

### spawn_agent

Create a new subagent with task assignment.

```javascript
const agentId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/{agent-type}.md (MUST read first)
2. Read: ${projectRoot}/.workflow/project-tech.json
3. Read: ${projectRoot}/.workflow/project-guidelines.json

---

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
  // Handle timeout - can continue waiting or send_input to prompt completion
}

// Check completion status
if (result.status[agentId].completed) {
  const output = result.status[agentId].completed;
}
```

### send_input

Continue interaction with active subagent (for clarification or follow-up).

```javascript
send_input({
  id: agentId,
  message: `
## CLARIFICATION ANSWERS
${answers}

## NEXT STEP
Continue with analysis generation.
`
})
```

### close_agent

Clean up subagent resources (irreversible).

```javascript
close_agent({ id: agentId })
```

## Progress Tracking Pattern

**Review Pipeline Initialization**:
```
Phase 1: Discovery & Initialization     → pending
Phase 2: Parallel Reviews (7 dimensions) → pending
Phase 3: Aggregation                     → pending
Phase 4: Deep-dive (conditional)         → pending
Phase 5: Review Completion               → pending
```

**During Phase 2 (sub-tasks for each dimension)**:
```
  → Security review       → in_progress / completed
  → Architecture review   → in_progress / completed
  → Quality review        → in_progress / completed
  ... other dimensions
```

**Fix Pipeline (added after Phase 5 if triggered)**:
```
Phase 6: Fix Discovery & Batching   → pending
Phase 7: Parallel Planning          → pending
Phase 7.5: Export to Task JSON      → pending
Phase 8: Execution                  → pending
Phase 9: Fix Completion             → pending
```

## Error Handling

### Review Pipeline Errors

| Phase | Error | Blocking? | Action |
|-------|-------|-----------|--------|
| Phase 1 | Session not found (session mode) | Yes | Error and exit |
| Phase 1 | No changed files (session mode) | Yes | Error and exit |
| Phase 1 | Invalid path pattern (module mode) | Yes | Error and exit |
| Phase 1 | No files matched (module mode) | Yes | Error and exit |
| Phase 2 | Single dimension fails | No | Log warning, continue other dimensions |
| Phase 2 | All dimensions fail | Yes | Error and exit |
| Phase 3 | Missing dimension JSON | No | Skip in aggregation, log warning |
| Phase 4 | Deep-dive agent fails | No | Skip finding, continue others |
| Phase 4 | Max iterations reached | No | Generate partial report |

### Fix Pipeline Errors

| Phase | Error | Blocking? | Action |
|-------|-------|-----------|--------|
| Phase 6 | Invalid export file | Yes | Abort with error |
| Phase 6 | Empty batches | No | Warn and skip empty |
| Phase 7 | Planning agent timeout | No | Mark batch failed, continue others |
| Phase 7 | All agents fail | Yes | Abort fix session |
| Phase 8 | Test failure after fix | No | Rollback, retry up to max_iterations |
| Phase 8 | Git operations fail | Yes | Abort, preserve state |
| Phase 9 | Aggregation error | No | Generate partial summary |

### CLI Fallback Chain

Gemini → Qwen → Codex → degraded mode

**Fallback Triggers**: HTTP 429/5xx, connection timeout, invalid JSON output, low confidence < 0.4, analysis too brief (< 100 words)

## Output File Structure

```
{projectRoot}/.workflow/active/WFS-{session-id}/.review/
├── review-state.json                    # Orchestrator state machine
├── review-progress.json                 # Real-time progress
├── dimensions/                          # Per-dimension results (Phase 2)
│   ├── security.json
│   ├── architecture.json
│   ├── quality.json
│   ├── action-items.json
│   ├── performance.json
│   ├── maintainability.json
│   └── best-practices.json
├── iterations/                          # Deep-dive results (Phase 4)
│   ├── iteration-1-finding-{uuid}.json
│   └── iteration-2-finding-{uuid}.json
├── reports/                             # Human-readable reports
│   ├── security-analysis.md
│   ├── security-cli-output.txt
│   ├── deep-dive-1-{uuid}.md
│   └── ...
├── .task/                              # Task JSON exports (Phase 7.5)
│   ├── FIX-001.json                    # Per-finding task (task-schema.json)
│   ├── FIX-002.json
│   └── ...
├── plan.json                           # Plan overview (plan-overview-fix-schema, Phase 7.5)
└── fixes/{fix-session-id}/             # Fix results (Phase 6-9)
    ├── partial-plan-*.json
    ├── fix-plan.json
    ├── fix-progress-*.json
    ├── fix-summary.md
    ├── active-fix-session.json
    └── fix-history.json
```

## Related Commands

### View Progress
```bash
ccw view
```

### Workflow Pipeline
```bash
# Step 1: Review (this skill)
review-cycle src/auth/**

# Step 2: Fix (continue or standalone)
review-cycle --fix ${projectRoot}/.workflow/active/WFS-{session-id}/.review/
```
