---
name: agent-comparison
description: "A/B test agent variants for quality and token cost."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
routing:
  triggers:
    - "compare agents"
    - "A/B test agents"
    - "benchmark agents"
    - "optimize skill"
    - "optimize description"
    - "run autoresearch"
  category: meta-tooling
  pairs_with:
    - agent-evaluation
    - skill-eval
---

# Agent Comparison Skill

Compare agent variants through controlled A/B benchmarks. Runs identical tasks on both agents, grades output quality with domain-specific checklists, and reports total session token cost to a working solution. This skill is exclusively for agent variant comparison — use `agent-evaluation` for single-agent assessment, and `skill-eval` for skill testing.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| selecting benchmark tasks and directory layout (Phase 1) | `benchmark-tasks.md` | Loads detailed guidance from `benchmark-tasks.md`. |
| example-driven tasks, errors | `examples-and-errors.md` | Loads detailed guidance from `examples-and-errors.md`. |
| scoring solutions: 5-criteria rubric and effective cost calculation | `grading-rubric.md` | Loads detailed guidance from `grading-rubric.md`. |
| deciding when to run comparisons; December 2024 baseline data | `methodology.md` | Loads detailed guidance from `methodology.md`. |
| configuring autoresearch: targets, task formats, eval isolation modes | `optimization-guide.md` | Loads detailed guidance from `optimization-guide.md`. |
| executing Phase 5 OPTIMIZE step by step | `optimize-phase.md` | Loads detailed guidance from `optimize-phase.md`. |
| writing the Phase 4 comparison report | `report-template.md` | Loads detailed guidance from `report-template.md`. |

## Instructions

> See `references/examples-and-errors.md` for error handling. See `references/optimize-phase.md` for Phase 5 OPTIMIZE full procedure. See `references/methodology.md` for December 2024 benchmark data.

### Phase 1: PREPARE

**Goal**: Create benchmark environment and validate both agent variants exist.

Read and follow the repository CLAUDE.md before starting any execution.

**Step 1: Analyze original agent**

```bash
wc -l agents/{original-agent}.md
grep "^## " agents/{original-agent}.md
grep -c '```' agents/{original-agent}.md
```

**Step 2: Create or validate compact variant**

If creating a compact variant, preserve:
- YAML frontmatter (name, description, routing)
- Core patterns and principles
- Error handling philosophy

Remove or condense:
- Lengthy code examples (keep 1-2 representative per pattern)
- Verbose explanations (condense to bullet points)
- Redundant instructions and changelogs

Target 10-15% of original size while keeping essential knowledge. Remove redundancy, not capability — stripping error handling patterns or concurrency guidance creates an unfair comparison because the compact agent is missing essential knowledge rather than expressing it concisely.

**Step 3: Validate compact variant structure**

```bash
head -20 agents/{compact-agent}.md | grep -E "^(name|description):"
echo "Original: $(wc -l < agents/{original-agent}.md) lines"
echo "Compact:  $(wc -l < agents/{compact-agent}.md) lines"
```

**Step 4: Create benchmark directory and prepare prompts**

```bash
mkdir -p benchmark/{task-name}/{full,compact}
```

Write the task prompt ONCE, then copy it for both agents. Both agents must receive the exact same task description, character-for-character, because different requirements produce different solutions and invalidate all measurements.

Keep benchmark scripts simple — no speculative features or configurable frameworks that were not requested.

**Gate**: Both agent variants exist with valid YAML frontmatter. Benchmark directories created. Identical task prompts written. Proceed only when gate passes.

### Phase 2: BENCHMARK

**Goal**: Run identical tasks on both agents, capturing all metrics.

**Step 1: Run simple task benchmark (2-3 tasks)**

Use algorithmic problems with clear specifications (e.g., Advent of Code Day 1-6). Simple tasks establish a baseline — if an agent fails here, it has fundamental issues. Running multiple simple tasks is necessary because a single data point is sensitive to task selection bias and cannot distinguish luck from systematic quality.

Spawn both agents in parallel using Task tool:

```
Task(
  prompt="[exact task prompt]\nSave to: benchmark/{task}/full/",
  subagent_type="{full-agent}"
)

Task(
  prompt="[exact task prompt]\nSave to: benchmark/{task}/compact/",
  subagent_type="{compact-agent}"
)
```

Run in parallel to avoid caching effects or system load variance skewing results.

**Step 2: Run complex task benchmark (1-2 tasks)**

Use production-style problems that require concurrency, error handling, edge case anticipation — these are where quality differences emerge because simple tasks mask differences in edge case handling. See `references/benchmark-tasks.md` for standard tasks.

Recommended complex tasks:
- **Worker Pool**: Rate limiting, graceful shutdown, panic recovery
- **LRU Cache with TTL**: Generics, background goroutines, zero-value semantics
- **HTTP Service**: Middleware chains, structured errors, health checks

**Step 3: Capture metrics for each run**

Record immediately after each agent completes — delayed recording loses precision. Track input/output token counts per turn where visible, since total session cost (not just prompt size) is what matters.

| Metric | Full Agent | Compact Agent |
|--------|------------|---------------|
| Tests pass | X/X | X/X |
| Race conditions | X | X |
| Code lines (main) | X | X |
| Test lines | X | X |
| Session tokens | X | X |
| Wall-clock time | Xm Xs | Xm Xs |
| Retry cycles | X | X |

**Step 4: Run tests with race detector**

```bash
cd benchmark/{task-name}/full && go test -race -v -count=1
cd benchmark/{task-name}/compact && go test -race -v -count=1
```

Use `-count=1` to disable test caching. All generated code must pass the same test suite with the `-race` flag because race conditions are automatic quality failures.

**Gate**: Both agents completed all tasks. Metrics captured for every run. Test output saved. Proceed only when gate passes.

### Phase 3: GRADE

**Goal**: Score code quality beyond pass/fail using domain-specific checklists.

**Step 1: Create quality checklist BEFORE reviewing code**

Define criteria before seeing results to prevent bias — inventing criteria after seeing one agent's output skews the comparison. See `references/grading-rubric.md` for standard rubrics.

| Criterion | 5/5 | 3/5 | 1/5 |
|-----------|-----|-----|-----|
| Correctness | All tests pass, no race conditions | Some failures | Broken |
| Error Handling | Comprehensive, production-ready | Adequate | None |
| Idioms | Exemplary for the language | Acceptable | Failure modes |
| Documentation | Thorough | Adequate | None |
| Testing | Comprehensive coverage | Basic | Minimal |

**Step 2: Score each solution independently**

Grade each agent's code on all five criteria. Score one agent completely before starting the other. Report facts and show command output rather than describing it — every claim must be backed by measurable data (tokens, test counts, quality scores).

```markdown
## {Agent} Solution - {Task}

| Criterion | Score | Notes |
|-----------|-------|-------|
| Correctness | X/5 | |
| Error Handling | X/5 | |
| Idioms | X/5 | |
| Documentation | X/5 | |
| Testing | X/5 | |
| **Total** | **X/25** | |
```

**Step 3: Document specific bugs with production impact**

For each bug found, record:

```markdown
### Bug: {description}
- Agent: {which agent}
- What happened: {behavior}
- Correct behavior: {expected}
- Production impact: {consequence}
- Test coverage: {did tests catch it? why not?}
```

"Tests pass" is necessary but not sufficient — production bugs often pass tests. Apply the domain-specific quality checklist rather than relying only on test pass rates, because tests can miss goroutine leaks, wrong semantics, and other production issues.

**Step 4: Calculate effective cost**

```
effective_cost = total_tokens * (1 + bug_count * 0.25)
```

An agent using 194k tokens with 0 bugs has better economics than one using 119k tokens with 5 bugs requiring fixes. The metric that matters is total cost to working, production-quality solution — not prompt size, because prompt is a one-time cost while reasoning tokens dominate sessions. Check quality scores before claiming token savings, since savings that come from cutting corners are not real savings.

**Gate**: Both solutions graded with evidence. Specific bugs documented with production impact. Effective cost calculated. Proceed only when gate passes.

### Phase 4: REPORT

**Goal**: Generate comparison report with evidence-backed verdict.

**Step 1: Generate comparison report**

Use the report template from `references/report-template.md`. Include:
- Executive summary with clear winner per metric
- Per-task results with metrics tables
- Token economics analysis (one-time prompt cost vs session cost)
- Specific bugs found and their production impact
- Verdict based on total evidence

**Step 2: Run comparison analysis**

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/compare.py benchmark/{task-name}/
```

**Step 3: Analyze token economics**

The key economic insight: agent prompts are a one-time cost per session. Everything after — reasoning, code generation, debugging, retries — costs tokens on every turn. When a micro agent produces correct code, it uses approximately the same total tokens. The savings appear only when it cuts corners.

| Pattern | Description |
|---------|-------------|
| Large agent, low churn | High initial cost, fewer retries, less debugging |
| Small agent, high churn | Low initial cost, more retries, more debugging |

Our data showed a 57-line agent used 69.5k tokens vs 69.6k for a 3,529-line agent on the same correct solution — prompt size alone does not determine cost.

**Step 4: State verdict with evidence**

The verdict must be backed by data. Include:
- Which agent won on simple tasks (expected: equivalent)
- Which agent won on complex tasks (expected: full agent)
- Total session cost comparison
- Effective cost comparison (with bug penalty)
- Clear recommendation for when to use each variant

See `references/methodology.md` for the complete testing methodology with December 2024 data.

**Step 5: Clean up**

Remove temporary benchmark files and debug outputs. Keep only the comparison report and generated code.

**Gate**: Report generated with all metrics. Verdict stated with evidence. Report saved to benchmark directory.

### Phase 5: OPTIMIZE (optional — invoked explicitly)

**Goal**: Run an automated optimization loop that improves a markdown target's frontmatter `description` using trigger-rate eval tasks, then selects the best measured variants through beam search or single-path search.

Invoke when the user says "optimize this skill", "optimize the description", or "run autoresearch". The existing manual A/B comparison (Phases 1-4) remains the path for full agent benchmarking.

> See `references/optimize-phase.md` for the full 9-step procedure, all CLI flags, recommended modes, live eval defaults, current reality check, and optional extensions.

**Gate**: Optimization complete. Results reviewed. Cherry-picked improvements applied and verified against full task set. Results recorded.

---

## References

- `${CLAUDE_SKILL_DIR}/references/methodology.md`: Complete testing methodology with December 2024 data
- `${CLAUDE_SKILL_DIR}/references/grading-rubric.md`: Detailed grading criteria and quality checklists
- `${CLAUDE_SKILL_DIR}/references/benchmark-tasks.md`: Standard benchmark task descriptions and prompts
- `${CLAUDE_SKILL_DIR}/references/report-template.md`: Comparison report template with all required sections
- `${CLAUDE_SKILL_DIR}/references/optimize-phase.md`: Full Phase 5 OPTIMIZE procedure (autoresearch loop, CLI flags, beam search, reality check)
- `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md`: Error handling for common benchmark failures
