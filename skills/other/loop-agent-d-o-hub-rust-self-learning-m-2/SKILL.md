---
name: loop-agent
description: Execute workflow agents iteratively for refinement and progressive improvement until quality criteria are met. Use when tasks require repetitive refinement, multi-iteration improvements, progressive optimization, or feedback loops until convergence.
---

# Loop Agent Skill

Execute workflow agents iteratively for refinement and progressive improvement until quality criteria are met.

## Quick Reference

- **[Modes](modes.md)** - Loop termination modes (fixed, criteria, convergence, hybrid)
- **[Patterns](patterns.md)** - Common loop patterns (refinement, test-fix, optimization)
- **[Configuration](configuration.md)** - Loop setup and templates
- **[Examples](examples.md)** - Complete loop examples

## When to Use

- Code needs iterative refinement until quality standards met
- Tests need repeated fix-validate cycles
- Performance requires progressive optimization
- Quality improvements need multiple passes
- Feedback loops necessary for convergence

## NOT Appropriate For

- Single-pass tasks (use specialized agent)
- Purely parallel work (use parallel-execution)
- Simple linear workflows (use sequential)
- One-time analysis

## Core Concepts

### Loop Termination Modes

| Mode | Description | Use When |
|------|-------------|----------|
| **Fixed** | Run exactly N iterations | Known number of passes needed |
| **Criteria** | Until success criteria met | Specific quality/performance targets |
| **Convergence** | Stop at diminishing returns | Optimal result unknown |
| **Hybrid** | Combine multiple conditions | Complex requirements |

See **[modes.md](modes.md)** for detailed mode documentation and **[patterns.md](patterns.md)** for common loop patterns.
