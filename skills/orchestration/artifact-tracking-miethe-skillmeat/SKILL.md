---
name: artifact-tracking
description: "Token-efficient tracking for AI orchestration. CLI-first for status updates (~50 tokens), agent fallback for complex ops (~1KB). Use when: updating task status, querying blockers, creating progress files, validating phases."
---

# Artifact Tracking Skill

Token-efficient tracking artifacts for AI agent orchestration.

## Quick Operations (CLI First)

| Operation | Command | Tokens |
|-----------|---------|--------|
| Mark complete | `python scripts/update-status.py -f FILE -t TASK-X -s completed` | ~50 |
| Batch update | `python scripts/update-batch.py -f FILE --updates "T1:completed,T2:completed"` | ~100 |
| Query pending | `python scripts/query_artifacts.py --status pending` | ~50 |
| Validate | `python scripts/validate_artifact.py -f FILE` | ~50 |

**Scripts location**: `.claude/skills/artifact-tracking/scripts/`

## Agent Operations (When Needed)

For complex operations requiring judgment:

| Operation | Agent | When to Use |
|-----------|-------|-------------|
| CREATE file | artifact-tracker | New phase, need template |
| UPDATE complex | artifact-tracker | Blockers with context, decisions |
| QUERY synthesis | artifact-query | Cross-phase analysis, handoffs |
| VALIDATE quality | artifact-validator | Pre-completion checks |

**Agent invocation**:
```
Task("artifact-tracker", "Create Phase 2 progress for auth-overhaul PRD")
Task("artifact-query", "Show all blocked tasks in auth-overhaul phases 1-3")
```

## File Locations

| Type | Location | Limit |
|------|----------|-------|
| Progress | `.claude/progress/[prd]/phase-N-progress.md` | ONE per phase |
| Context | `.claude/worknotes/[prd]/context.md` | ONE per PRD |
| Bug fixes | `.claude/worknotes/fixes/bug-fixes-YYYY-MM.md` | ONE per month |
| Observations | `.claude/worknotes/observations/observation-log-MM-YY.md` | ONE per month |

**Policy**: `.claude/specs/doc-policy-spec.md`

## YAML Format (Source of Truth)

```yaml
---
type: progress
prd: "prd-name"
phase: 2
status: in_progress
progress: 40

tasks:
  - id: "TASK-2.1"
    status: "pending"           # pending|in_progress|completed|blocked
    assigned_to: ["agent-name"] # REQUIRED for orchestration
    dependencies: []            # REQUIRED for orchestration
    model: "opus"               # Optional: opus|sonnet|haiku

parallelization:
  batch_1: ["TASK-2.1", "TASK-2.2"]  # Run parallel
  batch_2: ["TASK-2.3"]              # After batch_1
---
```

## Token Efficiency

| Operation | Traditional | Optimized | Savings |
|-----------|-------------|-----------|---------|
| Task list | 25KB | 2KB | 92% |
| Query blockers | 75KB | 3KB | 96% |
| Status update | 25KB | 50 bytes | 99.8% |

## Detailed References

- **Creating files**: `./creating-artifacts.md`
- **Updating tasks**: `./updating-artifacts.md`
- **Querying data**: `./querying-artifacts.md`
- **Validating**: `./validating-artifacts.md`
- **Orchestration**: `./orchestration-reference.md`
- **Best practices**: `./best-practices.md`
- **Common patterns**: `./common-patterns.md`
- **Format spec**: `./format-specification.md`
- **Templates**: `./templates/`
- **Schemas**: `./schemas/`
