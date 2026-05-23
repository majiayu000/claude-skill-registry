---
name: unified-review
description: |

Triggers: multi-domain, unified, code-quality, analysis, orchestration
  Orchestrate and run appropriate pensive review skills based on codebase
  analysis and context.

  Triggers: code review, unified review, full review, review orchestration,
  multi-domain review, intelligent review, auto-detect review

  Use when: general review needed without knowing which specific skill applies,
  full multi-domain review desired, integrated reporting needed

  DO NOT use when: specific review type known - use bug-review, test-review, etc.
  DO NOT use when: architecture-only focus - use architecture-review.

  Use this skill when orchestrating multiple review types.
category: orchestration
tags: [review, orchestration, code-quality, analysis, multi-domain]
tools: [skill-selector, context-analyzer, report-integrator]
usage_patterns:
  - auto-detect-review
  - full-review
  - focused-review
complexity: intermediate
estimated_tokens: 400
progressive_loading: true
dependencies:
  - pensive:shared
  - imbue:evidence-logging
  - imbue:structured-output
orchestrates:
  - pensive:rust-review
  - pensive:api-review
  - pensive:architecture-review
  - pensive:bug-review
  - pensive:test-review
  - pensive:makefile-review
  - pensive:math-review
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Review Skill Selection Matrix](#review-skill-selection-matrix)
- [Workflow](#workflow)
- [1. Analyze Repository Context](#1-analyze-repository-context)
- [2. Select Review Skills](#2-select-review-skills)
- [3. Execute Reviews](#3-execute-reviews)
- [4. Integrate Findings](#4-integrate-findings)
- [Review Modes](#review-modes)
- [Auto-Detect (default)](#auto-detect-(default))
- [Focused Mode](#focused-mode)
- [Full Review Mode](#full-review-mode)
- [Quality Gates](#quality-gates)
- [Deliverables](#deliverables)
- [Executive Summary](#executive-summary)
- [Domain-Specific Reports](#domain-specific-reports)
- [Integrated Action Plan](#integrated-action-plan)
- [Modular Architecture](#modular-architecture)
- [Exit Criteria](#exit-criteria)


# Unified Review Orchestration

Intelligently selects and executes appropriate review skills based on codebase analysis and context.

## Quick Start

```bash
# Auto-detect and run appropriate reviews
/full-review

# Focus on specific areas
/full-review api          # API surface review
/full-review architecture # Architecture review
/full-review bugs         # Bug hunting
/full-review tests        # Test suite review
/full-review all          # Run all applicable skills
```
**Verification:** Run `pytest -v` to verify tests pass.

## When to Use

- Starting a full code review
- Reviewing changes across multiple domains
- Need intelligent selection of review skills
- Want integrated reporting from multiple review types
- Before merging major feature branches

## Review Skill Selection Matrix

| Codebase Pattern | Review Skills | Triggers |
|-----------------|---------------|----------|
| Rust files (`*.rs`, `Cargo.toml`) | rust-review, bug-review, api-review | Rust project detected |
| API changes (`openapi.yaml`, `routes/`) | api-review, architecture-review | Public API surfaces |
| Test files (`test_*.py`, `*_test.go`) | test-review, bug-review | Test infrastructure |
| Makefile/build system | makefile-review, architecture-review | Build complexity |
| Mathematical algorithms | math-review, bug-review | Numerical computation |
| Architecture docs/ADRs | architecture-review, api-review | System design |
| General code quality | bug-review, test-review | Default review |

## Workflow

### 1. Analyze Repository Context
- Detect primary languages from extensions and manifests
- Analyze git status and diffs for change scope
- Identify project structure (monorepo, microservices, library)
- Detect build systems, testing frameworks, documentation

### 2. Select Review Skills
```python
# Detection logic
if has_rust_files():
    schedule_skill("rust-review")
if has_api_changes():
    schedule_skill("api-review")
if has_test_files():
    schedule_skill("test-review")
if has_makefiles():
    schedule_skill("makefile-review")
if has_math_code():
    schedule_skill("math-review")
if has_architecture_changes():
    schedule_skill("architecture-review")
# Default
schedule_skill("bug-review")
```
**Verification:** Run `pytest -v` to verify tests pass.

### 3. Execute Reviews
- Run selected skills concurrently
- Share context between reviews
- Maintain consistent evidence logging
- Track progress via TodoWrite

### 4. Integrate Findings
- Consolidate findings across domains
- Identify cross-domain patterns
- Prioritize by impact and effort
- Generate unified action plan

## Review Modes

### Auto-Detect (default)
Automatically selects skills based on codebase analysis.

### Focused Mode
Run specific review domains:
- `/full-review api` → api-review only
- `/full-review architecture` → architecture-review only
- `/full-review bugs` → bug-review only
- `/full-review tests` → test-review only

### Full Review Mode
Run all applicable review skills:
- `/full-review all` → Execute all detected skills

## Quality Gates

Each review must:
1. Establish proper context
2. Execute all selected skills successfully
3. Document findings with evidence
4. Prioritize recommendations by impact
5. Create action plan with owners

## Deliverables

### Executive Summary
- Overall codebase health assessment
- Critical issues requiring immediate attention
- Review frequency recommendations

### Domain-Specific Reports
- API surface analysis and consistency
- Architecture alignment with ADRs
- Test coverage gaps and improvements
- Bug analysis and security findings
- Performance and maintainability recommendations

### Integrated Action Plan
- Prioritized remediation tasks
- Cross-domain dependencies
- Assigned owners and target dates
- Follow-up review schedule

## Modular Architecture

All review skills use a hub-and-spoke architecture with progressive loading:

- **`pensive:shared`**: Common workflow, output templates, quality checklists
- **Each skill has `modules/`**: Domain-specific details loaded on demand
- **Cross-plugin deps**: `imbue:evidence-logging`, `imbue:diff-analysis/modules/risk-assessment-framework`

This reduces token usage by 50-70% for focused reviews while maintaining full capabilities.

## Exit Criteria

- All selected review skills executed
- Findings consolidated and prioritized
- Action plan created with ownership
- Evidence logged per `pensive:shared/modules/output-format-templates`
## Troubleshooting

### Common Issues

If the auto-detection fails to identify the correct review skills, explicitly specify the mode (e.g., `/full-review rust` instead of just `/full-review`). If integration fails, check that `TodoWrite` logs are accessible and that evidence files were correctly written by the individual skills.
