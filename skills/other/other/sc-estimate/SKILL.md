---
name: sc-estimate
description: Provide development estimates for tasks, features, or projects with intelligent analysis. Use when planning timelines, assessing complexity, or scoping resources.
---

# Development Estimation Skill

Systematic estimation with confidence intervals and risk assessment.

## Quick Start

```bash
# Time estimate with breakdown
/sc:estimate "auth system" --type time --unit days --breakdown

# Complexity assessment
/sc:estimate "microservices migration" --type complexity

# Effort analysis
/sc:estimate "performance optimization" --type effort --unit hours
```

## Behavioral Flow

1. **Analyze** - Examine scope, complexity, and dependencies
2. **Calculate** - Apply estimation methodology with benchmarks
3. **Validate** - Cross-reference with domain expertise
4. **Present** - Provide breakdown with confidence intervals
5. **Track** - Document for accuracy improvement

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | time | time, effort, complexity |
| `--unit` | string | days | hours, days, weeks |
| `--breakdown` | bool | false | Show detailed breakdown |

## Personas Activated

- **architect** - Design complexity assessment
- **performance** - Optimization effort analysis
- **project-manager** - Timeline and resource planning

## MCP Integration

- **PAL MCP** - Multi-perspective estimate validation

## Evidence Requirements

This skill does NOT require hard evidence. Deliverables are:
- Estimates with confidence intervals
- Risk factor identification
- Breakdown documentation

## Estimation Types

### Time (`--type time`)
- Calendar duration estimates
- Milestone planning
- Deadline assessment

### Effort (`--type effort`)
- Person-hours/days required
- Resource allocation guidance
- Team capacity planning

### Complexity (`--type complexity`)
- Technical complexity scoring
- Risk factor identification
- Dependency mapping

## Confidence Levels

Estimates include confidence intervals:
- **High (85-95%)** - Well-understood scope
- **Medium (70-84%)** - Some unknowns
- **Low (50-69%)** - Significant uncertainty

## Examples

### Feature Estimation
```
/sc:estimate "user authentication" --type time --unit days --breakdown
# Breakdown: DB design (2d) + API (3d) + UI (2d) + Tests (1d)
# Total: 8 days @ 85% confidence
```

### Complexity Assessment
```
/sc:estimate "monolith to microservices" --type complexity --breakdown
# Architecture complexity with risk factors
# Dependency mapping and migration phases
```

### Effort Analysis
```
/sc:estimate "API performance optimization" --type effort --unit hours
# Profiling (4h) + Analysis (6h) + Implementation (16h) + Testing (8h)
# Total: 34 hours @ 75% confidence
```

## Tool Coordination

- **Read/Grep/Glob** - Codebase complexity analysis
- **TodoWrite** - Estimation breakdown tracking
- **Task** - Multi-domain estimation delegation
- **Bash** - Dependency and project analysis
