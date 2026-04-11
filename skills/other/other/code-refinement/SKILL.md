---
name: code-refinement
description: 'Improve code quality: duplication, efficiency, clean code, architectural fit, and error handling'
version: 1.7.1
alwaysApply: false
category: code-quality
tags:
- refactoring
- clean-code
- algorithms
- duplication
- anti-slop
- craft
tools:
- Read
- Grep
- Glob
- Bash
usage_patterns:
- code-quality-improvement
- duplication-reduction
- algorithm-optimization
- clean-code-enforcement
complexity: advanced
model_hint: deep
estimated_tokens: 350
progressive_loading: true
dependencies:
- pensive:shared
- pensive:safety-critical-patterns
- imbue:proof-of-work
- imbue:justify
modules:
- modules/duplication-analysis.md
- modules/algorithm-efficiency.md
- modules/clean-code-checks.md
- modules/architectural-fit.md
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Analysis Dimensions](#analysis-dimensions)
- [Progressive Loading](#progressive-loading)
- [Required TodoWrite Items](#required-todowrite-items)
- [Workflow](#workflow)
- [Tiered Analysis](#tiered-analysis)
- [Cross-Plugin Dependencies](#cross-plugin-dependencies)

# Code Refinement Workflow

Analyze and improve living code quality across six dimensions.

## Quick Start

```bash
/refine-code
/refine-code --level 2 --focus duplication
/refine-code --level 3 --report refinement-plan.md
```

## When To Use

- After rapid AI-assisted development sprints
- Before major releases (quality gate)
- When code "works but smells"
- Refactoring existing modules for clarity
- Reducing technical debt in living code

## When NOT To Use

- Removing
  dead/unused code (use conserve:bloat-detector)

## Analysis Dimensions

| # | Dimension | Module | What It Catches |
|---|-----------|--------|----------------|
| 1 | Duplication & Redundancy | `duplication-analysis` | Near-identical blocks, similar functions, copy-paste |
| 2 | Algorithmic Efficiency | `algorithm-efficiency` | O(n^2) where O(n) works, unnecessary iterations |
| 3 | Clean Code Violations | `clean-code-checks` | Long methods, deep nesting, poor naming, magic values |
| 4 | Architectural Fit | `architectural-fit` | Paradigm mismatches, coupling violations, leaky abstractions |
| 5 | Anti-Slop Patterns | `clean-code-checks` | Premature abstraction, enterprise cosplay, hollow patterns |
| 6 | Error Handling | `clean-code-checks` | Bare excepts, swallowed errors, happy-path-only |
| 7 | Additive Bias | `imbue:justify` | Workarounds over root fixes, test tampering, unnecessary additions |

## Plugin-Specific Patterns

Detection patterns for plugin and skill codebases where
standard code quality heuristics miss structural issues.

### Delegation Stub Bodies

A skill that declares "delegates to X" but still carries the
full template body is doing double duty. The delegating skill
should be a thin wrapper (under 30 lines) that routes to the
target. Flag any delegating skill whose body exceeds 50 lines.

### Module Explosion

Flag skills with 10+ module files where 40% or more of content
overlaps. Signal: two modules covering the same API surface
from different angles (e.g., both describing the same config
options or the same CLI flags).

### Oversized Single Modules

Flag individual module files exceeding 500 lines as candidates
for splitting or trimming. Large modules defeat progressive
loading by forcing full-file reads for partial information.

### Dead Python References

Skills referencing Python commands (`python -m module.name` or
`python -c "from module import ..."`) where the referenced
module does not exist in the plugin's `src/` directory. These
are stale references to renamed or removed code.

## Progressive Loading

Load modules based on refinement focus:

- **`modules/duplication-analysis.md`** (~400 tokens): Duplication detection and consolidation
- **`modules/algorithm-efficiency.md`** (~400 tokens): Complexity analysis and optimization
- **`modules/clean-code-checks.md`** (~450 tokens): Clean code, anti-slop, error handling
- **`modules/architectural-fit.md`** (~400 tokens): Paradigm alignment and coupling

Load all for comprehensive refinement. For focused work, load only relevant modules.

## Required TodoWrite Items

1. `refine:context-established` — Scope, language, framework detection
2. `refine:scan-complete` — Findings across all dimensions
3. `refine:prioritized` — Findings ranked by impact and effort
4. `refine:plan-generated` — Concrete refactoring plan with before/after
5. `refine:evidence-captured` — Evidence appendix per `imbue:proof-of-work`

## Workflow

### Step 1: Establish Context (`refine:context-established`)

Detect project characteristics:
```bash
# Language detection
find . -not -path "*/.venv/*" -not -path "*/__pycache__/*" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  \( -name "*.py" -o -name "*.ts" -o -name "*.rs" -o -name "*.go" \) \
  | head -20

# Framework detection
ls package.json pyproject.toml Cargo.toml go.mod 2>/dev/null

# Size assessment
find . -not -path "*/.venv/*" -not -path "*/__pycache__/*" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  \( -name "*.py" -o -name "*.ts" -o -name "*.rs" \) \
  | xargs wc -l 2>/dev/null | tail -1
```

### Step 2: Dimensional Scan (`refine:scan-complete`)

Load relevant modules and execute analysis per tier level.
For dimension 7 (Additive Bias), run `Skill(imbue:justify)`
to compute the bias score, check Iron Law compliance,
and flag unnecessary additions or workarounds.

### Step 3: Prioritize (`refine:prioritized`)

Rank findings by:
- **Impact**: How much quality improves (HIGH/MEDIUM/LOW)
- **Effort**: Lines changed, files touched (SMALL/MEDIUM/LARGE)
- **Risk**: Likelihood of introducing bugs (LOW/MEDIUM/HIGH)

Priority = HIGH impact + SMALL effort + LOW risk first.

### Step 4: Generate Plan (`refine:plan-generated`)

For each finding, produce:
- File path and line range
- Current code snippet
- Proposed improvement
- Rationale (which principle/dimension)
- Estimated effort

### Step 5: Evidence Capture (`refine:evidence-captured`)

Document with `imbue:proof-of-work` (if available):
- `[E1]`, `[E2]` references for each finding
- Metrics before/after where measurable
- Principle violations cited

**Fallback**: If `imbue` is not installed, capture evidence inline in the report using the same `[E1]` reference format without TodoWrite integration.

## Tiered Analysis

| Tier | Time | Scope |
|------|------|-------|
| **1: Quick** (default) | 2-5 min | Complexity hotspots, obvious duplication, naming, magic values |
| **2: Targeted** | 10-20 min | Algorithm analysis, full duplication scan, architectural alignment |
| **3: Deep** | 30-60 min | All above + cross-module coupling, paradigm fitness, comprehensive plan |

## Cross-Plugin Dependencies

| Dependency | Required? | Fallback |
|------------|-----------|----------|
| `pensive:shared` | Yes | Core review patterns |
| `imbue:proof-of-work` | Optional | Inline evidence in report |
| `conserve:code-quality-principles` | Optional | Built-in KISS/YAGNI/SOLID checks |
| `archetypes:architecture-paradigms` | Optional | Principle-based checks only (no paradigm detection) |

## Supporting Modules

- [Code quality analysis](modules/code-quality-analysis.md) - duplication detection commands and consolidation strategies

When optional plugins are not installed, the skill degrades gracefully:
- Without `imbue`: Evidence captured inline, no TodoWrite proof-of-work
- Without `conserve`: Uses built-in clean code checks (subset)
- Without `archetypes`: Skips paradigm-specific alignment, uses coupling/cohesion principles only
