---
name: performance-review
description: 'Detect time and space complexity hotspots via AST scan.'
alwaysApply: false
category: code-quality
tags:
- performance
- complexity
- algorithms
- ast
- static-analysis
tools: []
usage_patterns:
- hotspot-detection
- complexity-review
- pre-merge-performance-check
complexity: advanced
model_hint: deep
estimated_tokens: 280
progressive_loading: true
dependencies:
- pensive:shared
modules:
- modules/time-complexity.md
- modules/space-complexity.md
- modules/gauntlet-integration.md
---

## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [When NOT to Use](#when-not-to-use)
- [Required TodoWrite Items](#required-todowrite-items)
- [Workflow](#workflow)
- [Tiered Analysis](#tiered-analysis)
- [Output Format](#output-format)
- [Cross-Plugin Dependencies](#cross-plugin-dependencies)
- [Supporting Modules](#supporting-modules)

# Performance Review

Static-analysis review of time and space complexity hotspots.

The skill runs in three escalating tiers. Tier 1 uses Python's
stdlib `ast` and always runs. Tier 2 uses gauntlet's tree-sitter
parser to extend detection across languages when gauntlet is
installed. Tier 3 uses the gauntlet code graph to upgrade
severity when hotspots reach other hotspots transitively. If
gauntlet is missing, Tiers 2 and 3 no-op and Tier 1 still
produces useful findings on Python source.

## Quick Start

```bash
/performance-review                  # scan changed files
/performance-review path/to/file.py  # scan one file
/performance-review --tier 1         # force Tier 1 only
```

Programmatic use:

```python
from pensive.skills.performance_review import PerformanceReviewSkill
skill = PerformanceReviewSkill()
result = skill.analyze(context, "src/module.py")
for f in result.issues:
    print(f"[{f.severity}] {f.file}:{f.line} {f.message}")
```

## When to Use

- Pre-merge review of code that runs on user-scaled inputs.
- Triage of a function that "feels slow" before reaching for a
  profiler.
- Audit a refactor for newly introduced O(n²) patterns.
- Guardrail for AI-generated code where nested-loop hot spots
  are common.

## When NOT to Use

- The target needs **runtime** measurement (memory profile, CPU
  time on real data). Use `Skill(parseltongue:python-performance)`
  instead: that skill drives `cProfile`, `py-spy`, and benchmarks.
- General refactoring guidance not focused on hotspots: use
  `Skill(pensive:code-refinement)` whose `algorithm-efficiency`
  module covers broader optimization patterns. This skill
  detects; that skill teaches.
- Architecture-level performance (sharding, caching layers,
  queue placement): use `Skill(pensive:architecture-review)`.

## Required TodoWrite Items

1. `perf-review:context-established`
2. `perf-review:scan-complete`
3. `perf-review:findings-categorized`
4. `perf-review:integration-checked`
5. `perf-review:report-generated`

## Workflow

### Step 1: Context (`perf-review:context-established`)

- Identify target files. If invoked with no argument, use
  `git diff --name-only`. If invoked with a path, scope to that.
- Note language(s) involved. Tier 1 covers Python; non-Python
  files need gauntlet for Tier 2 coverage.

### Step 2: Tier 1 AST scan (`perf-review:scan-complete`)

Load `modules/time-complexity.md` for the time-side patterns and
`modules/space-complexity.md` for space-side. Each module
documents the AST shape of every detector.

For each Python target file, call:

```python
from pensive.skills.performance_review import PerformanceReviewSkill
result = PerformanceReviewSkill().analyze(context, path)
```

The visitor walks the AST once and emits `ReviewFinding` records.

### Step 3: Categorize and rank (`perf-review:findings-categorized`)

Group findings by severity:

- **HIGH**: O(n²) or worse on input-sized iterables (T1, T2).
- **MEDIUM**: Unbounded allocation or per-iteration overhead
  (T3, T4, S1, S3).
- **LOW**: Style-level inefficiencies (T5, T6, S2).
- **CRITICAL**: Reserved for Tier-3 transitive upgrades.

Within a severity, sort by file then line. Suppress findings
the user has explicitly marked acceptable (TODO/comment
markers) at module-load time of the target.

### Step 4: Tier 2/3 enrichment (`perf-review:integration-checked`)

Load `modules/gauntlet-integration.md` for the contract.

If gauntlet is installed, run Tier 2 on non-Python files that
were skipped at Step 2. If a `.gauntlet/graph.db` exists in the
working tree, run Tier 3 to upgrade severities based on
transitive hotspot reachability.

If gauntlet is missing, this step is a no-op and the report
notes "Tier 2/3 not available: install gauntlet for
multi-language and call-chain coverage."

### Step 5: Report (`perf-review:report-generated`)

Emit a markdown report:

```
## Performance Review: <target>

### HIGH (<count>)
- src/foo.py:42: Nested loop over the same iterable 'items'.
  Suggestion: sort + two pointers, or hash-set membership.

### MEDIUM (<count>)
- ...

### LOW (<count>)
- ...

Tier coverage: 1 (always) | 2 (gauntlet ✓/✗) | 3 (graph ✓/✗)
```

The report is informational. Apply fixes via
`Skill(pensive:code-refinement)` or hand-merge.

## Tiered Analysis

| Tier | Source | When it runs | What it covers |
|------|--------|--------------|----------------|
| 1 | stdlib `ast` | Always (Python source only) | T1-T6, S1-S3 |
| 2 | `gauntlet.treesitter_parser` | When gauntlet importable | Same patterns adapted to JS/TS, Go, Rust, Java, C/C++ |
| 3 | `gauntlet.graph.GraphStore` | When `.gauntlet/graph.db` exists | Severity upgrade via transitive call chains |

## Output Format

Findings use the shared `ReviewFinding` dataclass from
`pensive.skills.base`:

```python
ReviewFinding(
    file="src/module.py",
    line=42,
    severity="HIGH",          # LOW | MEDIUM | HIGH | CRITICAL
    category="time",          # time | space
    message="Nested loop over the same iterable 'items'.",
    suggestion="Sort + two pointers, or hash-set membership.",
    code_snippet="",
)
```

This shape matches every other pensive review skill, so the
findings can flow into `Skill(pensive:unified-review)` without
translation.

## Cross-Plugin Dependencies

| Dependency | Required? | Effect when missing |
|------------|-----------|---------------------|
| `gauntlet.treesitter_parser` | Optional | Tier 2 returns []; Python coverage unchanged |
| `gauntlet.graph.GraphStore` | Optional | Tier 3 returns []; severities are not upgraded |

The optional-import contract follows the precedent in
`plugins/leyline/src/leyline/tokens.py:25-32` and
`plugins/gauntlet/hooks/pr_blast_radius.py:52-56`: try-import
to module-level sentinels, then early-return on `None` inside
each tier helper. See `modules/gauntlet-integration.md` for the
exact code shape.

## Supporting Modules

- `modules/time-complexity.md`: T1-T6 detector patterns and AST
  shapes.
- `modules/space-complexity.md`: S1-S3 detector patterns.
- `modules/gauntlet-integration.md`: Tier 2/3 contract,
  fallback semantics, examples.
