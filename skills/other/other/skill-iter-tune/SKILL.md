---
name: skill-iter-tune
description: Iterative skill tuning via execute-evaluate-improve feedback loop. Uses ccw cli Claude to execute skill, Gemini to evaluate quality, and Agent to apply improvements. Iterates until quality threshold or max iterations. Triggers on "skill iter tune", "iterative skill tuning", "tune skill".
allowed-tools: Skill, Agent, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash, Glob, Grep
---

# Skill Iter Tune

Iterative skill refinement through execute-evaluate-improve feedback loops. Each iteration runs the skill via Claude, evaluates output via Gemini, and applies improvements via Agent.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Skill Iter Tune Orchestrator (SKILL.md)                                 │
│  → Parse input → Setup workspace → Iteration Loop → Final Report         │
└────────────────────────────┬─────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────────────────────┐
         ↓                   ↓                                   ↓
    ┌──────────┐      ┌─────────────────────────────┐     ┌──────────┐
    │ Phase 1  │      │  Iteration Loop (2→3→4)     │     │ Phase 5  │
    │ Setup    │      │  ┌─────┐  ┌─────┐  ┌─────┐ │     │ Report   │
    │          │─────→│  │ P2  │→ │ P3  │→ │ P4  │ │────→│          │
    │ Backup + │      │  │Exec │  │Eval │  │Impr │ │     │ History  │
    │ Init     │      │  └─────┘  └─────┘  └─────┘ │     │ Summary  │
    └──────────┘      │       ↑               │     │     └──────────┘
                      │       └───────────────┘     │
                      │    (if score < threshold    │
                      │     AND iter < max)         │
                      └─────────────────────────────┘
```

### Chain Mode Extension

```
Chain Mode (execution_mode === "chain"):

Phase 2 runs per-skill in chain_order:
  Skill A → ccw cli → artifacts/skill-A/
       ↓ (artifacts as input)
  Skill B → ccw cli → artifacts/skill-B/
       ↓ (artifacts as input)
  Skill C → ccw cli → artifacts/skill-C/

Phase 3 evaluates entire chain output + per-skill scores
Phase 4 improves weakest skill(s) in chain
```

## Key Design Principles

1. **Iteration Loop**: Phases 2-3-4 repeat until quality threshold, max iterations, or convergence
2. **Two-Tool Pipeline**: Claude (write/execute) + Gemini (analyze/evaluate) = complementary perspectives
3. **Pure Orchestrator**: SKILL.md coordinates only — execution detail lives in phase files
4. **Progressive Phase Loading**: Phase docs read only when that phase executes
5. **Skill Versioning**: Each iteration snapshots skill state before execution
6. **Convergence Detection**: Stop early if score stalls (no improvement in 2 consecutive iterations)

## Interactive Preference Collection

```javascript
// ★ Auto mode detection
const autoYes = /\b(-y|--yes)\b/.test($ARGUMENTS)

if (autoYes) {
  workflowPreferences = {
    autoYes: true,
    maxIterations: 5,
    qualityThreshold: 80,
    executionMode: 'single'
  }
} else {
  const prefResponse = AskUserQuestion({
    questions: [
      {
        question: "选择迭代调优配置：",
        header: "Tune Config",
        multiSelect: false,
        options: [
          { label: "Quick (3 iter, 70)", description: "快速迭代，适合小幅改进" },
          { label: "Standard (5 iter, 80) (Recommended)", description: "平衡方案，适合多数场景" },
          { label: "Thorough (8 iter, 90)", description: "深度优化，适合生产级 skill" }
        ]
      }
    ]
  })

  const configMap = {
    "Quick": { maxIterations: 3, qualityThreshold: 70 },
    "Standard": { maxIterations: 5, qualityThreshold: 80 },
    "Thorough": { maxIterations: 8, qualityThreshold: 90 }
  }
  const selected = Object.keys(configMap).find(k =>
    prefResponse["Tune Config"].startsWith(k)
  ) || "Standard"
  workflowPreferences = { autoYes: false, ...configMap[selected] }

  // ★ Mode selection: chain vs single
  const modeResponse = AskUserQuestion({
    questions: [{
      question: "选择调优模式：",
      header: "Tune Mode",
      multiSelect: false,
      options: [
        { label: "Single Skill (Recommended)", description: "独立调优每个 skill，适合单一 skill 优化" },
        { label: "Skill Chain", description: "按链序执行，前一个 skill 的产出作为后一个的输入" }
      ]
    }]
  });
  workflowPreferences.executionMode = modeResponse["Tune Mode"].startsWith("Skill Chain")
    ? "chain" : "single";
}
```

## Input Processing

```
$ARGUMENTS → Parse:
  ├─ Skill path(s): first arg, comma-separated for multiple
  │   e.g., ".claude/skills/my-skill" or "my-skill" (auto-prefixed)
  │   Chain mode: order preserved as chain_order
  ├─ Test scenario: --scenario "description" or remaining text
  └─ Flags: --max-iterations=N, --threshold=N, -y/--yes
```

## Execution Flow

> **⚠️ COMPACT DIRECTIVE**: Context compression MUST check TodoWrite phase status.
> The phase currently marked `in_progress` is the active execution phase — preserve its FULL content.
> Only compress phases marked `completed` or `pending`.

### Phase 1: Setup (one-time)

Read and execute: `Ref: phases/01-setup.md`

- Parse skill paths, validate existence
- Create workspace at `.workflow/.scratchpad/skill-iter-tune-{ts}/`
- Backup original skill files
- Initialize iteration-state.json

Output: `workDir`, `targetSkills[]`, `testScenario`, initialized state

### Iteration Loop

```javascript
// Orchestrator iteration loop
while (true) {
  // Increment iteration
  state.current_iteration++;
  state.iterations.push({
    round: state.current_iteration,
    status: 'pending',
    execution: null,
    evaluation: null,
    improvement: null
  });

  // Update TodoWrite
  TaskUpdate(iterationTask, {
    subject: `Iteration ${state.current_iteration}/${state.max_iterations}`,
    status: 'in_progress',
    activeForm: `Running iteration ${state.current_iteration}`
  });

  // === Phase 2: Execute ===
  // Read: phases/02-execute.md
  // Single mode: one ccw cli call for all skills
  // Chain mode: sequential ccw cli per skill in chain_order, passing artifacts
  // Snapshot skill → construct prompt → ccw cli --tool claude --mode write
  // Collect artifacts

  // === Phase 3: Evaluate ===
  // Read: phases/03-evaluate.md
  // Construct eval prompt → ccw cli --tool gemini --mode analysis
  // Parse score → write iteration-N-eval.md → check termination

  // Check termination
  if (shouldTerminate(state)) {
    break;  // → Phase 5
  }

  // === Phase 4: Improve ===
  // Read: phases/04-improve.md
  // Agent applies suggestions → write iteration-N-changes.md

  // Update TodoWrite with score
  // Continue loop
}
```

### Phase 2: Execute Skill (per iteration)

Read and execute: `Ref: phases/02-execute.md`

- Snapshot skill → `iteration-{N}/skill-snapshot/`
- Build execution prompt from skill content + test scenario
- Execute: `ccw cli -p "..." --tool claude --mode write --cd "${iterDir}/artifacts"`
- Collect artifacts

### Phase 3: Evaluate Quality (per iteration)

Read and execute: `Ref: phases/03-evaluate.md`

- Build evaluation prompt with skill + artifacts + criteria + history
- Execute: `ccw cli -p "..." --tool gemini --mode analysis`
- Parse 5-dimension score (Clarity, Completeness, Correctness, Effectiveness, Efficiency)
- Write `iteration-{N}-eval.md`
- Check termination: score >= threshold | iter >= max | convergence | error limit

### Phase 4: Apply Improvements (per iteration, skipped on termination)

Read and execute: `Ref: phases/04-improve.md`

- Read evaluation suggestions
- Launch general-purpose Agent to apply changes
- Write `iteration-{N}-changes.md`
- Update state

### Phase 5: Final Report (one-time)

Read and execute: `Ref: phases/05-report.md`

- Generate comprehensive report with score progression table
- Write `final-report.md`
- Display summary to user

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Purpose | Compact |
|-------|----------|---------|---------|
| 1 | [phases/01-setup.md](phases/01-setup.md) | Initialize workspace and state | TodoWrite 驱动 |
| 2 | [phases/02-execute.md](phases/02-execute.md) | Execute skill via ccw cli Claude | TodoWrite 驱动 + 🔄 sentinel |
| 3 | [phases/03-evaluate.md](phases/03-evaluate.md) | Evaluate via ccw cli Gemini | TodoWrite 驱动 + 🔄 sentinel |
| 4 | [phases/04-improve.md](phases/04-improve.md) | Apply improvements via Agent | TodoWrite 驱动 + 🔄 sentinel |
| 5 | [phases/05-report.md](phases/05-report.md) | Generate final report | TodoWrite 驱动 |

**Compact Rules**:
1. **TodoWrite `in_progress`** → 保留完整内容，禁止压缩
2. **TodoWrite `completed`** → 可压缩为摘要
3. **🔄 sentinel fallback** → 若 compact 后仅存 sentinel 而无完整 Step 协议，立即 `Read()` 恢复

## Core Rules

1. **Start Immediately**: First action is preference collection → Phase 1 setup
2. **Progressive Loading**: Read phase doc ONLY when that phase is about to execute
3. **Snapshot Before Execute**: Always snapshot skill state before each iteration
4. **Background CLI**: ccw cli runs in background, wait for hook callback before proceeding
5. **Parse Every Output**: Extract structured JSON from CLI outputs for state updates
6. **DO NOT STOP**: Continuous iteration until termination condition met
7. **Single State Source**: `iteration-state.json` is the only source of truth

## Data Flow

```
User Input (skill paths + test scenario)
    ↓ (+ execution_mode + chain_order if chain mode)
    ↓
Phase 1: Setup
    ↓ workDir, targetSkills[], testScenario, iteration-state.json
    ↓
┌─→ Phase 2: Execute (ccw cli claude)
│   ↓ artifacts/ (skill execution output)
│   ↓
│   Phase 3: Evaluate (ccw cli gemini)
│   ↓ score, dimensions[], suggestions[], iteration-N-eval.md
│   ↓
│   [Terminate?]─── YES ──→ Phase 5: Report → final-report.md
│   ↓ NO
│   ↓
│   Phase 4: Improve (Agent)
│   ↓ modified skill files, iteration-N-changes.md
│   ↓
└───┘ next iteration
```

## TodoWrite Pattern

```javascript
// Initial state
TaskCreate({ subject: "Phase 1: Setup workspace", activeForm: "Setting up workspace" })
TaskCreate({ subject: "Iteration Loop", activeForm: "Running iterations" })
TaskCreate({ subject: "Phase 5: Final Report", activeForm: "Generating report" })

// Chain mode: create per-skill tracking tasks
if (state.execution_mode === 'chain') {
  for (const skillName of state.chain_order) {
    TaskCreate({
      subject: `Chain: ${skillName}`,
      activeForm: `Tracking ${skillName}`,
      description: `Skill chain member position ${state.chain_order.indexOf(skillName) + 1}`
    })
  }
}

// During iteration N
// Single mode: one score per iteration (existing behavior)
// Chain mode: per-skill status updates
if (state.execution_mode === 'chain') {
  // After each skill executes in Phase 2:
  TaskUpdate(chainSkillTask, {
    subject: `Chain: ${skillName} — Iter ${N} executed`,
    activeForm: `${skillName} iteration ${N}`
  })
  // After Phase 3 evaluates:
  TaskUpdate(chainSkillTask, {
    subject: `Chain: ${skillName} — Score ${chainScores[skillName]}/100`,
    activeForm: `${skillName} scored`
  })
} else {
  // Single mode (existing)
  TaskCreate({
    subject: `Iteration ${N}: Score ${score}/100`,
    activeForm: `Iteration ${N} complete`,
    description: `Strengths: ... | Weaknesses: ... | Suggestions: ${count}`
  })
}

// Completed — collapse
TaskUpdate(iterLoop, {
  subject: `Iteration Loop (${totalIters} iters, final: ${finalScore})`,
  status: 'completed'
})
```

## Termination Logic

```javascript
function shouldTerminate(state) {
  // 1. Quality threshold met
  if (state.latest_score >= state.quality_threshold) {
    return { terminate: true, reason: 'quality_threshold_met' };
  }
  // 2. Max iterations reached
  if (state.current_iteration >= state.max_iterations) {
    return { terminate: true, reason: 'max_iterations_reached' };
  }
  // 3. Convergence: ≤2 points improvement over last 2 iterations
  if (state.score_trend.length >= 3) {
    const last3 = state.score_trend.slice(-3);
    if (last3[2] - last3[0] <= 2) {
      state.converged = true;
      return { terminate: true, reason: 'convergence_detected' };
    }
  }
  // 4. Error limit
  if (state.error_count >= state.max_errors) {
    return { terminate: true, reason: 'error_limit_reached' };
  }
  return { terminate: false };
}
```

## Error Handling

| Phase | Error | Recovery |
|-------|-------|----------|
| 2: Execute | CLI timeout/crash | Retry once with simplified prompt, then skip |
| 3: Evaluate | CLI fails | Retry once, then use score 50 with warning |
| 3: Evaluate | JSON parse fails | Extract score heuristically, save raw output |
| 4: Improve | Agent fails | Rollback from `iteration-{N}/skill-snapshot/` |
| Any | 3+ consecutive errors | Terminate with error report |

**Error Budget**: Each phase gets 1 retry. 3 consecutive failed iterations triggers termination.

## Coordinator Checklist

### Pre-Phase Actions
- [ ] Read iteration-state.json for current state
- [ ] Verify workspace directory exists
- [ ] Check error count hasn't exceeded limit

### Per-Iteration Actions
- [ ] Increment current_iteration in state
- [ ] Create iteration-{N} subdirectory
- [ ] Update TodoWrite with iteration status
- [ ] After Phase 3: check termination before Phase 4
- [ ] After Phase 4: write state, proceed to next iteration

### Post-Workflow Actions
- [ ] Execute Phase 5 (Report)
- [ ] Display final summary to user
- [ ] Update all TodoWrite tasks to completed
