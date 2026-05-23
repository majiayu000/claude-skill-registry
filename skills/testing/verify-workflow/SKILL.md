---
name: verify-workflow
description: Verify workflow outputs using hybrid script + LLM assessment
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Verify Workflow Skill

Verifies plan-marshall workflow outputs using hybrid script + LLM-as-judge assessment.

## Supported Phases (6-Phase Model)

| Phase | Artifacts Verified | Checks |
|-------|-------------------|--------|
| `1-init` | config.toon, status.toon, request.md | Files exist, proper structure |
| `2-refine` | request.md, work.log | Clarifications present, [REFINE:*] log entries, domains in config |
| `3-outline` | solution_outline.md, deliverables, references.toon | Structure valid, deliverable count, affected files |
| `4-plan` | TASK-*.toon files | Tasks exist, match deliverables |
| `5-execute` | references.toon with modified files | Affected files tracked |
| `6-verify` | quality check results | (Not verified by script - use build commands) |
| `7-finalize` | git commit artifacts | (Not verified by script - use git commands) |

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `subcommand` | Yes | One of: `test`, `verify`, `create`, `list` |
| `--test-id` | verify/create | Test case identifier (kebab-case). Optional for `test` - auto-selects if only one exists |
| `--plan-id` | verify only | Existing plan to verify |

## Usage Examples

```bash
/verify-workflow test                                    # Auto-selects if only one test case
/verify-workflow test --test-id migrate-json-to-toon     # Explicit test case
/verify-workflow verify --test-id migrate-json-to-toon --plan-id my-plan
/verify-workflow create --test-id my-new-test
/verify-workflow list
```

## Critical Design Principle

**Use proper tool interfaces, NOT direct filesystem access.**

| DO | DON'T |
|----|-------|
| `manage-tasks list --plan-id X` | Read `.plan/plans/X/tasks/*.toon` directly |
| `manage-solution-outline list-deliverables` | Parse `solution_outline.md` directly |

## Subcommand Routing

**MANDATORY**: Based on subcommand, load and execute the corresponding workflow.

### test
Execute trigger from test-definition, then verify.
```
Read: workflows/test-and-verify.md
```
Execute the **test** workflow section.

### verify
Verify existing plan (requires `--plan-id`).
```
Read: workflows/test-and-verify.md
```
Execute the **verify** workflow section.

### create
Create new test case interactively.
```
Read: workflows/create-test-case.md
```

### list
List available test cases.
```
Read: workflows/list-test-cases.md
```

## Reference Documentation

Load only when needed:

- `standards/architecture.md` - Visual overview of verification engine
- `standards/scoring-guide.md` - Scoring rubric (0-100 scale)
- `standards/test-case-format.md` - Test case specification
- `standards/criteria-format.md` - Criteria authoring guide
- `standards/failure-categories.md` - Root cause taxonomy for structural failures

## Analysis Workflows

Loaded conditionally during verification:

- `workflows/trace-components.md` - Component tracing with sequential IDs (C1, C2, ...)
- `workflows/analyze-failures.md` - Structural failure analysis (runs when checks fail)
- `workflows/analyze-issues.md` - Issue attribution to components (runs when findings exist)

## Directory Structure

```
workflow-verification/test-cases/{test-id}/   # Version-controlled
├── test-definition.toon
├── expected-artifacts.toon
├── criteria/
└── golden/

.plan/temp/workflow-verification/             # Ephemeral results
└── {test-id}-{timestamp}/
    ├── assessment-results.toon
    ├── assessment-detail.md
    ├── component-trace.md
    ├── structural-checks.toon
    ├── structural-analysis.toon    # If failures exist
    ├── issue-analysis.md           # If findings exist
    └── artifacts/
```

## Scripts

Scripts are invoked via the executor using `local:` notation for automatic PYTHONPATH setup.

### verify-structure.py
Structural verification via manage-* tool interfaces.

**Input**: `--plan-id`, `--test-case`, `--output`, `--phases`
**Output**: TOON file with structural check results

```bash
python3 .plan/execute-script.py local:verify-workflow:verify-structure \
  --plan-id {plan_id} \
  --test-case workflow-verification/test-cases/{test-id} \
  --output {results_dir}/structural-checks.toon \
  --phases {workflow_phase}
```

### collect-artifacts.py
Artifact collection via manage-* tool interfaces.

**Input**: `--plan-id`, `--output`, `--phases`
**Output**: Directory with collected artifacts (solution_outline.md, config.toon, etc.)

```bash
python3 .plan/execute-script.py local:verify-workflow:collect-artifacts \
  --plan-id {plan_id} \
  --output {results_dir}/artifacts/ \
  --phases {workflow_phase}
```
