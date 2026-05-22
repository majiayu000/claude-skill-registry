---
name: model-evaluation-benchmark
version: 1.0.0
description: |
  Automated reproduction of comprehensive model evaluation benchmarks following the Benchmark Suite V3.
  Auto-activates for model benchmarking, comparison evaluation, or performance testing between AI models.
---

# Model Evaluation Benchmark Skill

**Purpose**: Automated reproduction of comprehensive model evaluation benchmarks following the Benchmark Suite V3 reference implementation.

**Auto-activates when**: User requests model benchmarking, comparison evaluation, or performance testing between AI models in agentic workflows.

## Skill Description

This skill orchestrates end-to-end model evaluation benchmarks that measure:

- **Efficiency**: Duration, turns, cost, tool calls
- **Quality**: Code quality scores via reviewer agents
- **Workflow Adherence**: Subagent calls, skills used, workflow step compliance
- **Artifacts**: GitHub issues, PRs, documentation generated

The skill automates the entire benchmark workflow from execution through cleanup, following the v3 reference implementation.

## When to Use

✅ **Use when**:

- Comparing AI models (Opus vs Sonnet, etc.)
- Measuring workflow adherence
- Generating comprehensive benchmark reports
- Need reproducible benchmarking

❌ **Don't use when**:

- Simple code reviews (use `reviewer`)
- Performance profiling (use `optimizer`)
- Architecture decisions (use `architect`)

## Execution Instructions

When this skill is invoked, follow these steps:

### Phase 1: Setup

1. Read `tests/benchmarks/benchmark_suite_v3/BENCHMARK_TASKS.md`
2. Identify models to benchmark (default: Opus 4.5, Sonnet 4.5)
3. Create TodoWrite list with all phases

### Phase 2: Execute Benchmarks

For each task × model:

```bash
cd tests/benchmarks/benchmark_suite_v3
python run_benchmarks.py --model {opus|sonnet} --tasks 1,2,3,4
```

### Phase 3: Analyze Results

1. Read all result files: `.claude/runtime/benchmarks/suite_v3/*/result.json`
2. Launch parallel Task tool calls with `subagent_type="reviewer"` to:
   - Analyze trace logs for tool/agent/skill usage
   - Score code quality (1-5 scale)
3. Synthesize findings

### Phase 4: Generate Report

1. Create markdown report following `BENCHMARK_REPORT_V3.md` structure
2. Create GitHub issue with report
3. Archive artifacts to GitHub release
4. Update issue with release link

### Phase 5: Cleanup (MANDATORY)

1. Close all benchmark PRs: `gh pr close {numbers}`
2. Close all benchmark issues: `gh issue close {numbers}`
3. Remove worktrees: `git worktree remove worktrees/bench-*`
4. Verify cleanup complete

See `tests/benchmarks/benchmark_suite_v3/CLEANUP_PROCESS.md` for detailed cleanup instructions.

## Example Usage

```
User: "Run model evaluation benchmark"Assistant: I'll run the complete benchmark suite following the v3 reference implementation.

[Executes phases 1-5 above]

Final Report: See GitHub Issue #XXXX
Artifacts: https://github.com/.../releases/tag/benchmark-suite-v3-artifacts
```

## References

- **Reference Report**: `tests/benchmarks/benchmark_suite_v3/BENCHMARK_REPORT_V3.md`
- **Task Definitions**: `tests/benchmarks/benchmark_suite_v3/BENCHMARK_TASKS.md`
- **Cleanup Guide**: `tests/benchmarks/benchmark_suite_v3/CLEANUP_PROCESS.md`
- **Runner Script**: `tests/benchmarks/benchmark_suite_v3/run_benchmarks.py`

---

**Last Updated**: 2025-11-26
**Reference Implementation**: Benchmark Suite V3
**GitHub Issue Example**: #1698
