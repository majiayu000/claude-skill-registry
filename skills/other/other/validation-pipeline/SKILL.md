---
name: "Validation Pipeline"
description: "Structured step-by-step validation of requirements, code, and artifacts with gate enforcement, per-step scoring, and structured reports."
trust_tier: 3
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json
  eval_path: evals/validation-pipeline.yaml

---

# Validation Pipeline

## Purpose

Run structured validation pipelines that execute steps sequentially, enforce gates at blocking failures, and produce scored reports. Uses the `src/validation/pipeline.ts` framework with 13 requirements validation steps (BMAD-003).

## Activation

- When validating requirements documents
- When running structured quality gates
- When assessing document completeness, testability, or traceability
- When invoked via `/validation-pipeline`

## Quick Start

```bash
# Validate a requirements document (all 13 steps)
/validation-pipeline requirements docs/requirements.md

# Validate with specific steps only
/validation-pipeline requirements docs/requirements.md --steps format-check,completeness-check,invest-criteria

# Continue past blocking failures
/validation-pipeline requirements docs/requirements.md --continue-on-failure

# Output as JSON
/validation-pipeline requirements docs/requirements.md --json
```

## Workflow

### Step 1: Read the Target Document

Read the file specified by the user. If no file is provided, ask for one.

```
Read the target document using the Read tool.
Store the content for pipeline execution.
```

### Step 2: Select Pipeline

Choose the appropriate pipeline based on the user's request:

| Pipeline | Steps | Use Case |
|----------|-------|----------|
| `requirements` | 13 | Requirements documents, PRDs, user stories |

Additional pipelines can be created by defining new step sets in `src/validation/steps/`.

### Step 3: Execute Pipeline

The pipeline framework (`src/validation/pipeline.ts`) handles execution:

1. **Sequential execution** — steps run in order, each receiving results from prior steps
2. **Gate enforcement** — blocking steps that fail halt the pipeline (unless `--continue-on-failure`)
3. **Per-step scoring** — each step produces a 0-100 score with findings and evidence
4. **Weighted rollup** — overall score uses category weights (format=10%, content=30%, quality=25%, traceability=20%, compliance=15%)

#### Requirements Pipeline Steps (13 total)

| # | Step ID | Category | Severity | What It Checks |
|---|---------|----------|----------|----------------|
| 1 | `format-check` | format | blocking | Headings, required sections, document length |
| 2 | `completeness-check` | content | blocking | Required fields populated, acceptance criteria present |
| 3 | `invest-criteria` | quality | warning | Independent, Negotiable, Valuable, Estimable, Small, Testable |
| 4 | `smart-acceptance` | quality | warning | Specific, Measurable, Achievable, Relevant, Time-bound |
| 5 | `testability-score` | quality | warning | Can each requirement be tested? |
| 6 | `vague-term-detection` | content | info | Flags "should", "might", "various", "etc." |
| 7 | `information-density` | content | info | Every sentence carries weight, no filler |
| 8 | `traceability-check` | traceability | warning | Requirements-to-tests mapping exists |
| 9 | `implementation-leakage` | quality | warning | Requirements don't prescribe implementation |
| 10 | `domain-compliance` | compliance | info | Alignment with domain model |
| 11 | `dependency-analysis` | traceability | info | Cross-requirement dependencies identified |
| 12 | `bdd-scenario-generation` | quality | warning | Can generate Given/When/Then for each requirement |
| 13 | `holistic-quality` | compliance | blocking | Overall coherence, no contradictions |

### Step 4: Report Results

Format the pipeline result as a structured report:

```markdown
# Validation Report: Requirements Pipeline

**Overall**: PASS/FAIL/WARN | **Score**: 85/100 | **Duration**: 42ms

## Step Results
| # | Step | Status | Score | Findings | Duration |
|---|------|--------|-------|----------|----------|
| 1 | Format Check | PASS | 100 | 0 | 2ms |
| 2 | Completeness | WARN | 60 | 2 | 5ms |
...

## Blockers
- (blocking findings listed here)

## All Findings
- [HIGH] Missing acceptance criteria: Requirement US-104 has no AC
- [MEDIUM] Vague term: "should" used 5 times without specifics
...
```

### Step 5: Record Learning

After pipeline execution, record the outcome for learning:

```typescript
// Store validation pattern
memory store --namespace validation-pipeline --key "req-validation-{timestamp}" --value "{score, findings_count, halted}"
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pipeline` | string | `requirements` | Pipeline type to run |
| `file` | string | required | Path to document to validate |
| `--steps` | string[] | all | Specific step IDs to run |
| `--continue-on-failure` | boolean | false | Skip blocking gates |
| `--json` | boolean | false | Output as JSON instead of markdown |
| `--metadata` | object | {} | Additional context for steps |

## Integration Points

- **qe-requirements-validator agent** — delegates structured validation to this pipeline
- **qe-quality-gate agent** — uses pipeline for gate evaluation
- **YAML Pipelines** — can invoke validation steps as workflow actions
- **MCP** — accessible via `pipeline_validate` tool

## Output Schema

The pipeline produces a `PipelineResult` object (see `schemas/output.json`):

```typescript
{
  pipelineId: string;
  pipelineName: string;
  overall: 'pass' | 'fail' | 'warn';
  score: number;           // 0-100 weighted average
  steps: StepResult[];     // per-step details
  blockers: Finding[];     // blocking findings
  halted: boolean;
  haltedAt?: string;       // step ID where halted
  totalDuration: number;
  timestamp: string;
}
```

## Error Handling

- **Step throws exception** — captured as a FAIL with critical finding, pipeline continues or halts per severity
- **File not found** — report error, do not run pipeline
- **Empty document** — format-check step will catch this as a blocking failure
