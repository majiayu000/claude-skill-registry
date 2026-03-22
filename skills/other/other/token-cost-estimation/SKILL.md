---
name: token-cost-estimation
description: Estimate and track token costs before work sessions - complexity, duration, resources
category: Core Universal
---

# Skill: token-cost-estimation

## What I do

I estimate token costs BEFORE work sessions begin, enabling informed decisions about workflow optimisation. I provide structured cost breakdowns, identify savings opportunities, and track actual vs estimated usage via memory-keeper for continuous improvement.

## When to use me

- **Always-active**: Load with every session automatically
- At the START of any work session before executing tasks
- When planning complex multi-step tasks
- When token budget is constrained
- During retrospectives to compare estimates vs actuals

## Core principles

1. **Estimate upfront** - Never start work without understanding expected cost
2. **Break down costs** - Show components: investigation, implementation, verification
3. **Identify savings** - Recommend optimisations before starting
4. **Track accuracy** - Store estimates and actuals to improve over time
5. **Integrate with workflow** - Use parallel-execution, scope-management to reduce costs

## Estimation Framework

### Task Complexity Tiers

| Tier | Description | Token Range | Examples |
|------|-------------|-------------|----------|
| **Simple** | Single-file, well-defined task | 100-500 | Fix typo, add config, simple refactor |
| **Moderate** | Multi-file, clear scope | 500-2000 | Add feature, fix bug, update tests |
| **Complex** | Cross-cutting, investigation needed | 2000-5000 | Architecture change, new system |
| **Major** | Large scope, uncertain requirements | 5000+ | Full feature, migration, major refactor |

### Duration Multipliers

| Duration | Multiplier | Impact |
|----------|------------|--------|
| Short (<30min) | 1.0x | Focused, minimal context switching |
| Medium (30-90min) | 1.5x | Some iteration, context rebuilding |
| Long (90min+) | 2.0x | Multiple iterations, fatigue overhead |

### Resource Factors

- **Files involved**: +100 tokens per file read/modified
- **Codebase familiarity**: New (2x), Familiar (1x), Expert (0.7x)
- **Tool usage**: Each tool call ~50-100 tokens overhead
- **Verification**: Tests add 30-50% to implementation cost

## Cost Breakdown Template

```
## Token Cost Estimate

**Session Goal**: [state objective]
**Complexity Tier**: [Simple/Moderate/Complex/Major]
**Estimated Duration**: [time]

### Breakdown
| Phase | Estimated Tokens | Notes |
|-------|------------------|-------|
| Investigation | X | File reads, search, context |
| Implementation | Y | Edits, writes, iterations |
| Verification | Z | Tests, checks, validation |
| **Total** | **X+Y+Z** | |

### Optimisation Opportunities
- [ ] Parallel investigation (save ~X tokens)
- [ ] Scope reduction (save ~Y tokens)
- [ ] Efficient prompting (save ~Z tokens)

### Estimated vs Budget
- Estimate: X tokens
- Budget: Y tokens (if applicable)
- Difference: +/- Z
```

## Savings Strategies

### From parallel-execution
- Fan-out investigation: Read multiple files simultaneously
- Parallel verification: Run lint/test/check in parallel
- Estimated savings: 20-40% on investigation phase

### From scope-management
- Reduce scope to essential deliverables
- Defer nice-to-haves to separate sessions
- Estimated savings: Variable (scope-dependent)

### From token-efficiency
- Structure prompts clearly
- Provide focused context
- Use examples over descriptions
- Estimated savings: 10-30%

## Post-Session Tracking

After session completion:
1. Record actual token usage
2. Compare to estimate
3. Store in memory-keeper:
   ```
   ESTIMATE: [prediction]
   ACTUAL: [result]
   VARIANCE: [difference]
   FACTORS: [what caused variance]
   → Update estimation heuristics
   ```

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Token Cost Estimation.md`

## Related skills

- `pre-action` - Clarify scope before estimating
- `memory-keeper` - Store estimates and actuals
- `estimation` - Task complexity evaluation
- `time-management` - Duration estimation
- `task-tracker` - Progress and complexity tracking
- `scope-management` - Resource identification
- `token-efficiency` - Cost reduction techniques
- `parallel-execution` - Efficiency through parallelism
