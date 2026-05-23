---
name: faion-writing-implementation-plan
user-invocable: false
description: "SDD Framework: Creates implementation-plan.md from design.md. Decomposes into tasks that fit 100k token context. Triggers on \"implementation plan\", \"impl plan\"."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion
---

# SDD: Writing Implementation Plans

**Communication: User's language. Docs: English.**

## Key Principle

**Each task MUST fit 100k token context** = atomic, single-agent executable.

## Workflow

```
LOAD CONTEXT → ANALYZE COMPLEXITY → DEFINE WORK UNITS → APPLY 100k RULE → DEPENDENCIES → DRAFT → REVIEW → SAVE
```

## Phase 1: Load Context

Read: `constitution.md`, `spec.md`, `design.md`

## Phase 2: Analyze Complexity

For each file in design.md:

| File | Action | Complexity | Est. Tokens |
|------|--------|------------|-------------|
| models.py | CREATE | High | 40k |
| services.py | CREATE | High | 50k |

**Factors:** LOC, dependencies, business logic, tests

## Phase 3: Define Work Units

Group related work:
```markdown
## Work Unit 1: Data Layer
- models.py (CREATE)
Est: 40k tokens
```

## Phase 4: Apply 100k Rule

```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

**If > 100k:** Split into smaller tasks.

## Phase 5: Dependencies

| Task | Depends On | Enables |
|------|------------|---------|
| TASK_001 | — | TASK_003 |
| TASK_002 | — | TASK_003 |
| TASK_003 | 001, 002 | — |

Rules: No cycles, maximize parallelization.

## Phase 6: Draft

Show section by section:
- Overview (total tasks, critical path, est. tokens)
- Tasks list (files, deps, FR/AD coverage, AC)
- Execution order (phases, parallel/sequential)

## Phase 7: Review

Call `faion-impl-plan-reviewer-agent` agent. Checks: 100k compliance, deps, coverage.

## Phase 8: Save

`aidocs/sdd/{project}/features/{feature}/implementation-plan.md`

## Token Estimation Guide

| Component | Tokens |
|-----------|--------|
| Django model simple | 5-10k |
| Django model complex | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Test file | 20-40k |

**Rule:** If uncertain, estimate higher and split.

## Output

`implementation-plan.md` → Next: `faion-make-tasks` skill (via `/faion-net` → create tasks)
