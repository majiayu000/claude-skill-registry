---
name: manage-plan-artifacts
description: Plan-scoped artifact storage for assessments and findings with JSONL persistence
user-invocable: false
allowed-tools: Bash
---

# Manage Plan Artifacts

Plan-level artifact storage providing structured JSONL persistence for assessments and findings.

## Scope Distinction

| Scope | Storage | Lifecycle |
|-------|---------|-----------|
| **Project-level** | `.plan/lessons-learned/` | Persists across plans |
| **Plan-level** | `.plan/plans/{plan_id}/artifacts/` | Temporary, promoted or discarded |

Plan artifacts are working data during plan execution. Notable findings are promoted to project-level at `7-finalize`.

## Storage Structure

```
.plan/plans/{plan_id}/artifacts/
├── assessments.jsonl  # Component assessments (certainty, confidence)
└── findings.jsonl     # Unified: lessons + bugs (optionally promotable)
```

## Artifact Types

### Assessments

Component evaluations from analysis agents with certainty gates and confidence scores.

**Certainty values**: `CERTAIN_INCLUDE`, `CERTAIN_EXCLUDE`, `UNCERTAIN`

### Findings

Unified storage for lessons and bugs. All types optionally promotable.

**Finding types**:

| Type | Origin | Default Promotion Target |
|------|--------|--------------------------|
| `bug` | Implementation errors | manage-lessons |
| `improvement` | Discovered patterns | manage-lessons |
| `anti-pattern` | Bad practices found | manage-lessons |
| `triage` | Triage decisions | manage-lessons |
| `tip` | Helpful hints | architecture (tips) |
| `insight` | Deeper understanding | architecture (insights) |
| `best-practice` | Recommended patterns | architecture (best_practices) |
| `build-error` | Compilation failures | (any, if pattern emerges) |
| `test-failure` | Test failures | (any, if pattern emerges) |
| `lint-issue` | Linter warnings | (any, if pattern emerges) |
| `sonar-issue` | Sonar findings | (any, if pattern emerges) |
| `pr-comment` | PR review comments | (any, if pattern emerges) |

**Resolution values**: `pending`, `fixed`, `suppressed`, `accepted`

## CLI Commands

### Assessment Commands

```bash
# Add assessment
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  assessment add {plan_id} {file_path} {certainty} {confidence} \
  [--agent AGENT] [--detail DETAIL] [--evidence EVIDENCE]

# Query assessments
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  assessment query {plan_id} [--certainty C] [--min-confidence N] \
  [--max-confidence N] [--file-pattern PATTERN]

# Get single assessment
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  assessment get {plan_id} {hash_id}
```

### Finding Commands

```bash
# Add finding
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  finding add {plan_id} {type} {title} --detail DETAIL \
  [--file-path PATH] [--line N] [--component C] \
  [--module M] [--rule R] [--severity S]

# Query findings
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  finding query {plan_id} [--type T] [--resolution R] \
  [--promoted BOOL] [--file-pattern PATTERN]

# Get single finding
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  finding get {plan_id} {hash_id}

# Resolve finding
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  finding resolve {plan_id} {hash_id} {resolution} [--detail DETAIL]

# Promote finding
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  finding promote {plan_id} {hash_id} {promoted_to}
```

## Output Format

All commands return TOON format.

**Add response**:
```toon
status: success
hash_id: a3f2c1
type: bug
```

**Query response**:
```toon
status: success
plan_id: my-plan
total_count: 30
filtered_count: 15

findings[15]{hash_id,type,title,resolution}:
a3f2c1,bug,Null check missing,pending
b4e3d2,sonar-issue,TODO comment,fixed
```

## Integration

### Producers

| Client | Artifact | Operation |
|--------|----------|-----------|
| Analysis agents | assessment | add |
| Sonar integration | finding (sonar-issue) | add, resolve |
| CI integration | finding (pr-comment) | add, resolve |
| phase-7-finalize | finding | add, promote |

### Consumers

| Client | Artifact | Operation |
|--------|----------|-----------|
| Q-Gate agent | assessment | query |
| phase-7-finalize | finding | query, resolve, promote |
| Workflow orchestration | assessment | query |

## Promotion Workflow

At `7-finalize`:

1. Query unpromoted findings: `finding query {plan_id} --promoted false`
2. For each finding to promote:
   - **To manage-lessons** (bug, improvement, anti-pattern, triage):
     ```bash
     manage-lessons add --component {component} --category {type} ...
     finding promote {plan_id} {hash_id} {promoted_id}
     ```
   - **To architecture** (tip, insight, best-practice):
     ```bash
     architecture enrich {type} --module {module} --{type} "{content}" --reasoning "From plan {plan_id}"
     finding promote {plan_id} {hash_id} architecture
     ```
