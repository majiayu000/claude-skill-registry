---
name: Perf Reviewer
description: Review code for performance issues and run benchmarks. Use when user asks to analyze performance, compare AILANG vs Python vs Go, run benchmarks, or review code for optimization opportunities.
---

# Performance Reviewer

Review code for performance issues and run cross-language benchmarks.

## Quick Start

**Run benchmarks comparing AILANG vs Python vs compiled Go:**
```bash
# Run all standard benchmarks
.claude/skills/perf-reviewer/scripts/benchmark.sh

# Run specific benchmark
.claude/skills/perf-reviewer/scripts/benchmark.sh fibonacci

# Review code for performance issues
# Just ask: "review this code for performance"
```

## When to Use This Skill

Invoke this skill when:
- User asks to "benchmark" or "compare performance"
- User wants to compare AILANG vs Python vs Go
- User asks to "review for performance" or "optimize"
- User mentions "slow", "performance", "bottleneck"
- After implementing compute-intensive code
- Before releases to verify no performance regressions

## Available Scripts

### `scripts/benchmark.sh [benchmark_name]`
Run cross-language benchmarks comparing AILANG interpreted, Python, and AILANG compiled to Go.

**Available benchmarks:** `fibonacci`, `sort`, `transform`, `all`

**Output:** Timing comparisons, speedup ratios, and recommendations.

### `scripts/profile_ailang.sh <file.ail>`
Profile an AILANG file with timing breakdown by compilation phase.

## Workflow

### 1. Performance Review (Code Analysis)

When reviewing code, check against these principles (see [resources/principles.md](resources/principles.md)):

**Critical checks:**
1. **Algorithmic complexity** - Is there an O(n log n) solution for O(n²) code?
2. **Batch operations** - Can multiple operations be combined?
3. **Memory allocation** - Are allocations inside hot loops?
4. **Data layout** - Are frequently-accessed fields colocated?

**Quick checklist:**
```
[ ] No O(n²) where O(n log n) exists
[ ] Batch APIs for repeated operations
[ ] Allocations hoisted outside loops
[ ] Hot paths optimized, edge cases separate
[ ] No unnecessary string formatting in loops
```

### 2. Benchmarking (Cross-Language Comparison)

**Run benchmarks:**
```bash
# Full benchmark suite
.claude/skills/perf-reviewer/scripts/benchmark.sh all

# Single benchmark
.claude/skills/perf-reviewer/scripts/benchmark.sh fibonacci
```

**Interpret results:**
| Ratio | Interpretation |
|-------|----------------|
| Go/AILANG < 0.1x | Compiled Go is 10x+ faster (expected) |
| Python/AILANG ~ 1x | Similar interpreted performance |
| AILANG/Go > 10x | Consider compilation for this workload |

### 3. Profiling (Phase Breakdown)

```bash
.claude/skills/perf-reviewer/scripts/profile_ailang.sh examples/compute_heavy.ail
```

**Phase timing helps identify:**
- Slow parsing -> complex syntax
- Slow type checking -> deep type inference
- Slow evaluation -> algorithmic issues

## Performance Principles Summary

From [resources/principles.md](resources/principles.md):

| Principle | Action |
|-----------|--------|
| Profile First | Measure before optimizing |
| Algorithms > Micro-opts | O(n) beats optimized O(n^2) |
| Batch Operations | Amortize overhead |
| Memory Layout | Cache-friendly structures |
| Fast Path | Optimize common case |
| Defer Work | Lazy evaluation |
| Right-size Data | Appropriate containers |

## Resources

- [resources/principles.md](resources/principles.md) - Full performance principles (Abseil-inspired)
- [resources/go_patterns.md](resources/go_patterns.md) - Go-specific optimization patterns

## Notes

- Compiled AILANG (Go) should be 10-100x faster than interpreted
- Python comparison provides baseline for interpreted languages
- Always profile real workloads, not just microbenchmarks
