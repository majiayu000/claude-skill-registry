---
name: scope-management
description: Manage scope effectively - identify resources, prevent creep, optimise for token budget
category: Workflow Orchestration
---

# Skill: scope-management

## What I do

I help manage scope effectively by identifying required resources, preventing scope creep, and optimising scope to fit token budgets. I provide resource data to token-cost-estimation.

## When to use me

- Before starting work to define boundaries
- When scope is expanding unexpectedly
- When token budget is constrained
- When identifying what resources are needed
- When deciding what to defer or cut

## Core principles

1. **Define boundaries upfront** - What's in, what's out
2. **Identify resources early** - Files, tools, external dependencies
3. **Say no appropriately** - Protect scope from creep
4. **Optimise for constraints** - Fit scope to available tokens
5. **Defer explicitly** - Out-of-scope items get tracked, not forgotten

## Resource Identification

### Resource Categories

| Category | Token Impact | Identification |
|----------|--------------|----------------|
| **Files to read** | ~100-200 per file | List before starting |
| **Files to modify** | ~200-500 per file | Explicit list |
| **Tools required** | ~50-100 per call | Identify patterns |
| **External lookups** | ~200-500 each | Web fetches, docs |
| **Context needed** | Variable | Prior knowledge required |

### Resource Estimation Template
```
## Resource Requirements

Files to read: X files (~Y tokens)
Files to modify: X files (~Y tokens)
Tool calls expected: ~X calls (~Y tokens)
External lookups: X (~Y tokens)
Context rebuilding: ~Y tokens

Total resource overhead: ~Z tokens
```

## Scope Optimisation

### For Token Budget

When tokens are limited:
1. **Cut nice-to-haves** - Essential only
2. **Defer to next session** - Track explicitly
3. **Reduce file scope** - Fewer files = fewer tokens
4. **Skip verification shortcuts** - But document risk
5. **Use cached knowledge** - Check memory-keeper first

### Scope Reduction Strategies

| Strategy | Token Savings | Trade-off |
|----------|---------------|-----------|
| Defer docs | 10-20% | Technical debt |
| Minimal tests | 20-30% | Coverage risk |
| Single file focus | 30-50% | Scope reduction |
| Skip exploration | 20-40% | Miss context |

## Scope Creep Prevention

### Warning Signs
- "While we're here..." additions
- Discovering "one more thing"
- Requirements expanding mid-task
- Unclear original scope

### Response Pattern
```
SCOPE CREEP DETECTED:
  New request: [what]
  Original scope: [was]
  Options:
    1. Add to current (impact: +X tokens)
    2. Defer to next session (no impact)
    3. Replace existing item (swap)
  → Recommend: [choice with reasoning]
```

## Anti-patterns to avoid

- ❌ Starting without defined scope
- ❌ Saying yes to all additions
- ❌ Not identifying resources upfront
- ❌ Forgetting deferred items
- ❌ Ignoring token budget constraints

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Scope Management.md`

## Related skills

- `token-cost-estimation` - Uses resource data for estimates
- `estimation` - Scope affects estimates
- `task-tracker` - Tasks reflect scope
- `pre-action` - Clarify scope before starting
