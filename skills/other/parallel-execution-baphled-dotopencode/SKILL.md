---
name: parallel-execution
description: Maximise efficiency by running independent tasks in parallel - reduce token overhead
category: Session Knowledge
---

# Skill: parallel-execution

## What I do

I am the **EXECUTE phase** — after `pre-action` PREFLIGHT planning, I batch all independent tool calls into a single message. This reduces token overhead by avoiding sequential context rebuilding.

**Workflow**: `pre-action` (PREFLIGHT) → `parallel-execution` (EXECUTE)

## When to use me

- **After PREFLIGHT** — batch calls marked as Parallel in the plan
- During investigation (read multiple files in one call)
- During verification (lint + test + arch-check in one call)

## Core principles

1. **Plan first** — Use `pre-action` PREFLIGHT to identify independent work
2. **Batch aggressively** — Single message, multiple tool calls
3. **Respect dependencies** — Dependent tasks MUST sequence
4. **Measure savings** — Track parallel vs sequential cost

## Parallelisation Patterns

### Fan-Out Investigation
```
ONE question → MANY parallel reads → COMBINE results
Example: "Where is X used?" → Read files A, B, C, D in parallel
Savings: ~40-60% vs sequential
```

### Parallel Verification
```
ONE change → MANY parallel checks → GATHER results
Example: After edit → lint + test + arch-check in parallel
Savings: ~50-70% vs sequential
```

### Scatter-Gather Research
```
ONE bug → MANY parallel investigations → IDENTIFY root cause
Example: Bug report → check logs + read code + search issues in parallel
Savings: ~30-50% vs sequential
```

## Token Savings Analysis

| Operation | Sequential | Parallel | Savings |
|-----------|------------|----------|---------|
| Read 4 files | 4 calls | 1 call (4 reads) | 75% overhead |
| 3 verification checks | 3 calls | 1 call (3 checks) | 66% overhead |
| Search 3 patterns | 3 calls | 1 call (3 searches) | 66% overhead |

**Overhead saved**: Each separate call adds ~50-100 tokens of overhead.

## Execution Rules

### MUST Parallel (Independent)
- Reading multiple files
- Running multiple tests/checks
- Searching multiple patterns
- Fetching multiple URLs
- Creating multiple entities

### MUST Sequence (Dependent)
- Write → Read (verify)
- Branch → Commit
- Build → Test
- Investigate → Fix → Verify
- Query → Process results

## Integration with pre-action

1. **PREFLIGHT** identifies which steps are independent
2. **EXECUTE** batches those steps into parallel tool calls
3. **Mid-chain reflection** (from pre-action) reassesses after results

## Anti-patterns to avoid

- ❌ Sequential calls for independent operations
- ❌ Parallelising dependent operations
- ❌ Not batching tool calls
- ❌ Ignoring parallelisation opportunities
- ❌ Not tracking efficiency gains

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Parallel Execution.md`

## Related skills

- `pre-action` — PREFLIGHT phase: plan before this skill executes
- `token-cost-estimation` — Benefits from parallel efficiency
- `token-efficiency` — Complementary efficiency techniques
