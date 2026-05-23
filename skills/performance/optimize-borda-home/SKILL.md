---
name: optimize
description: Performance deep-dive orchestrator. Establishes a baseline, spawns perf-optimizer agent to identify the real bottleneck, and produces a before/after report. Covers CPU, memory, Input/Output (I/O), concurrency, and Machine Learning (ML) / Graphics Processing Unit (GPU) workloads.
argument-hint: <file, module, or directory>
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Grep, Glob, Agent, TaskCreate, TaskUpdate
---

<objective>

Orchestrate a performance investigation using the perf-optimizer agent. This skill handles the measurement bookends (baseline → change → verify) while the agent handles the actual analysis and implementation.

</objective>

<inputs>

- **$ARGUMENTS**: file, module, or directory to optimize.

</inputs>

<workflow>

**Task tracking**: per CLAUDE.md, create tasks (TaskCreate) for each major phase. Mark in_progress/completed throughout. On loop retry or scope change, create a new task.

**Scope heuristic**: Single file or function → use this default workflow. Directory or system-wide scope → consider team mode: spawn 2 **perf-optimizer** teammates each profiling different subsystems, then converge findings in the Step 5 report. Each teammate follows the same baseline → bottleneck → profile loop independently and uses AgentSpeak v2 (see `.claude/TEAM_PROTOCOL.md`) for coordination.

## Step 1: Establish baseline

Before touching any code, measure current performance:

```bash
# Python script / module
python -m cProfile -s cumtime "$ARGUMENTS" 2>&1 | head -30

# Quick wall-clock timing
time python "$ARGUMENTS"

# Memory snapshot — use memray (safer and more accurate than exec-based approaches):
# python -m memray run --output /tmp/memray.bin "$ARGUMENTS" && python -m memray stats /tmp/memray.bin
```

Record the baseline numbers — they are the benchmark for all improvements.

## Step 2: Spawn perf-optimizer agent

Task the `perf-optimizer` agent with:

1. Read all relevant code files in and around `$ARGUMENTS`
2. Apply the optimization hierarchy (algorithm → data structure → I/O → memory → concurrency → vectorization → compute → caching)
3. Identify the **single biggest bottleneck** — not a laundry list
4. Implement a targeted fix for that bottleneck
5. Identify 2 additional bottlenecks to address next
6. Write your full analysis (bottleneck identification, optimization reasoning, Confidence block) to `tasks/optimize-analysis-$(date +%Y-%m-%d).md` using the Write tool
7. Return ONLY a compact JSON envelope on your final line — nothing else after it: `{"status":"done","bottleneck":"<description>","files_modified":[],"confidence":0.N,"file":"tasks/optimize-analysis-<date>.md"}`

## Step 3: Codex correctness check

Read `.claude/skills/_shared/codex-prepass.md` and run the Codex pre-pass on the optimization changes from Step 2.

Codex focus: verify functional equivalence — same outputs for same inputs, same error paths, same boundary behavior. Resolve any correctness findings before re-measurement in Step 4.

## Step 4: Verify improvement

After each change from the perf-optimizer:

```bash
# Re-run the same baseline measurement
python -m cProfile -s cumtime "$ARGUMENTS" 2>&1 | head -30
time python "$ARGUMENTS"
```

**Accept** if improvement > 10% (adjust threshold for your workload — GPU benchmarks may need 20%+ to clear noise; hot-path latency may justify 2%). **Revert** if not measurable or < noise floor.

**Safety break**: max 3 optimization-verification cycles. After 3 perf-optimizer changes, proceed to Step 5 (report). Ask the user whether to run another round.

## Step 5: Report

```
## Performance Optimization: [target]

### Baseline
- [metric]: [value]

### Changes Applied
1. **[bottleneck]**: [what changed] → [measured improvement]
2. **[bottleneck]**: [what changed] → [measured improvement]

### After
- [metric]: [new value] ([X]x improvement)

### Remaining Opportunities
- [next bottleneck to address]
```

## Step 6: Delegate follow-up (optional)

After confirming improvements, inspect the applied changes (`git diff HEAD --stat`) and identify tasks Codex can complete from the categories below.

**Delegate to Codex when:**

- Optimized code uses non-obvious techniques (pre-allocation, vectorized ops, batched I/O) that need inline explanation — read the code first, then describe the technique and why it is faster
- A function signature changed due to optimization (e.g., added `batch_size` or `device` parameter) and the docstring no longer matches the actual contract
- Tests for the optimized path where coverage is thin — describe the input ranges and expected output behaviour precisely
- ruff or mypy errors introduced by the optimization — read each error, use Codex to delegate to `linting-expert` with a precise description of what to fix

**Do not delegate:**

- Generic "add comments" requests — only delegate when you can describe the specific technique and its rationale

Read `.claude/skills/_shared/codex-delegation.md` and apply the delegation criteria defined there.

Example prompt: `"use the doc-scribe to add an inline comment to the inner loop in src/batch_processor.py:87 explaining that the result tensor is pre-allocated before the loop to avoid repeated GPU memory allocation — the old version called torch.zeros() inside the loop"`

Only print a `### Codex Delegation` section after the Step 4 terminal output when tasks were actually delegated — omit entirely if nothing was delegated.

End your complete response with a `## Confidence` block per CLAUDE.md output standards.

</workflow>

<notes>

- The perf-optimizer agent has the full optimization knowledge base — this skill only orchestrates the measure-change-measure loop
- Never skip the baseline measurement — unmeasured optimization is guessing
- For ML-specific optimization (DataLoader, mixed precision, torch.compile), the perf-optimizer agent has dedicated sections
- Follow-up chains:
  - Bottleneck is architectural (not just a hot loop) → `/develop refactor` for structural changes with test safety net
  - Optimization changes non-trivial code paths → `/review` for quality validation
  - Optimized code needs documentation updates → Step 5 auto-delegates to Codex

</notes>
