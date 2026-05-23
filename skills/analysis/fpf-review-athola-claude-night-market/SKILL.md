---
name: fpf-review
description: |
  Triggers: architecture review, FPF, functional programming framework, systems architecture
  Architecture review using FPF (Functional Programming Framework) methodology.
  Evaluates codebases through functional, practical, and foundation perspectives.

  Use when: conducting architecture reviews, evaluating system design
  DO NOT use when: simple code reviews, bug fixes, documentation updates
category: review-methodology
tags: [architecture, review, FPF, functional, systems-design]
dependencies:
  - pensive:code-reviewer
  - imbue:review-core
tools:
  - Read
  - Grep
  - Glob
  - TodoWrite
usage_patterns:
  - architecture-analysis
  - design-evaluation
  - recommendation-generation
complexity: advanced
estimated_tokens: 3000
modules:
  - modules/functional-perspective.md
  - modules/practical-perspective.md
  - modules/foundation-perspective.md
version: 1.3.5
---
## Table of Contents

- [Philosophy](#philosophy)
- [Quick Start](#quick-start)
- [The Three Perspectives](#the-three-perspectives)
- [Workflow](#workflow)
- [Output Format](#output-format)
- [Configuration](#configuration)
- [Guardrails](#guardrails)
- [Integration Points](#integration-points)

# FPF Architecture Review

Conduct architecture reviews using the FPF (Functional Programming Framework) methodology, evaluating codebases through three complementary perspectives.

## Philosophy

Architecture reviews should be systematic and multi-dimensional. FPF provides three lenses:
- **Functional**: What the system does (capabilities, behaviors)
- **Practical**: How well it works (performance, usability)
- **Foundation**: What it's built on (principles, patterns)

This lighter skill-based approach replaces heavyweight tooling with focused analysis.

## Quick Start

```bash
# Full FPF review
/fpf-review

# Specific perspective
/fpf-review --perspective functional
/fpf-review --perspective practical
/fpf-review --perspective foundation

# Focused scope
/fpf-review --scope plugins/sanctum
```

## The Three Perspectives

### 1. Functional Perspective

**Question:** What does this system do?

**Evaluates:**
- Feature completeness
- Capability coverage
- Behavior correctness
- Integration points

**Outputs:**
- Feature inventory
- Capability gaps
- Behavior anomalies

### 2. Practical Perspective

**Question:** How well does this system work?

**Evaluates:**
- Performance characteristics
- Usability patterns
- Operational concerns
- Scalability considerations

**Outputs:**
- Performance assessment
- Usability issues
- Operational recommendations

### 3. Foundation Perspective

**Question:** What is this system built on?

**Evaluates:**
- Architectural patterns
- Design principles
- Code quality
- Technical debt

**Outputs:**
- Pattern analysis
- Principle adherence
- Debt inventory

## Workflow

### Phase 1: Discovery (`fpf-review:discovery-complete`)

1. **Scan codebase structure** - Identify components, modules, layers
2. **Map dependencies** - Internal and external relationships
3. **Identify entry points** - Public APIs, commands, interfaces

### Phase 2: Functional Analysis (`fpf-review:functional-complete`)

1. **Inventory features** - What capabilities exist
2. **Trace behaviors** - How features work end-to-end
3. **Identify gaps** - Missing or incomplete functionality

### Phase 3: Practical Analysis (`fpf-review:practical-complete`)

1. **Assess performance** - Latency, throughput, resource usage
2. **Evaluate usability** - Developer experience, API design
3. **Check operations** - Logging, monitoring, error handling

### Phase 4: Foundation Analysis (`fpf-review:foundation-complete`)

1. **Pattern recognition** - What patterns are used
2. **Principle check** - SOLID, DRY, KISS adherence
3. **Debt assessment** - Technical debt inventory

### Phase 5: Synthesis (`fpf-review:synthesis-complete`)

1. **Cross-reference findings** - Connect issues across perspectives
2. **Prioritize recommendations** - Based on impact and effort
3. **Generate report** - Structured findings and actions

## Output Format

### FPF Review Report

```markdown
# FPF Architecture Review: [Project/Component]

**Date:** [DATE]
**Scope:** [what was reviewed]
**Reviewer:** Claude Code with FPF skill

## Executive Summary

[2-3 sentence overview of findings]

## Functional Perspective

### Features Inventory

| Feature | Status | Notes |
|---------|--------|-------|
| [Feature 1] | Complete | - |
| [Feature 2] | Partial | Missing edge case handling |

### Capability Gaps

1. [Gap 1] - [Impact]
2. [Gap 2] - [Impact]

## Practical Perspective

### Performance Assessment

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| [Metric 1] | [value] | [target] | PASS/FAIL |

### Usability Issues

1. [Issue 1] - [Severity]
2. [Issue 2] - [Severity]

## Foundation Perspective

### Pattern Analysis

| Pattern | Usage | Assessment |
|---------|-------|------------|
| [Pattern 1] | [where used] | Appropriate/Problematic |

### Technical Debt

| Item | Severity | Effort | Priority |
|------|----------|--------|----------|
| [Debt 1] | High | Medium | P1 |

## Recommendations

### High Priority

1. **[Recommendation 1]**
   - Impact: [what improves]
   - Effort: [estimate]
   - Rationale: [why]

### Medium Priority

2. **[Recommendation 2]**
   ...

## Action Items

- [ ] [Action 1] - Owner: TBD
- [ ] [Action 2] - Owner: TBD
```

## Configuration

```yaml
# .fpf-review.yaml
scope:
  include:
    - src/
    - plugins/
  exclude:
    - tests/
    - docs/
    - node_modules/

perspectives:
  functional:
    enabled: true
    depth: "full"  # full, summary
  practical:
    enabled: true
    depth: "full"
  foundation:
    enabled: true
    depth: "full"

output:
  format: "markdown"
  create_issues: false  # Create GitHub issues for findings
  severity_threshold: "medium"  # Report medium+ severity
```

## Guardrails

1. **Scope boundaries** - Stay within configured scope
2. **Evidence-based** - Every finding needs supporting evidence
3. **Actionable output** - Recommendations must be actionable
4. **Balanced perspectives** - Don't over-index on one perspective

## Required TodoWrite Items

1. `fpf-review:discovery-complete`
2. `fpf-review:functional-complete`
3. `fpf-review:practical-complete`
4. `fpf-review:foundation-complete`
5. `fpf-review:synthesis-complete`

## Integration Points

- **`pensive:code-reviewer`**: Detailed code-level review
- **`imbue:review-core`**: Review methodology patterns
- **`imbue:feature-review`**: Feature-specific analysis

## References

- [FPF Framework](https://github.com/ailev/FPF) - Original methodology
- [quint-code](https://github.com/m0n0x41d/quint-code) - Heavy implementation (this skill is lighter)

---

**Status:** Skeleton implementation. Requires:
- Detailed analysis algorithms
- Pattern recognition logic
- Report generation templates
