---
name: scenario
description: 'Author and manage holdout behavioral validation scenarios.'
skill_api_version: 1
metadata:
  tier: execution
  stability: experimental
output_contract: "Scenario artifacts in .agents/holdout/*.json"
---
# Scenario Skill

Author and manage holdout scenarios for behavioral validation. Scenarios
define **what** the system should do in narrative form, with measurable
acceptance vectors and satisfaction scoring. They live in `.agents/holdout/`
so implementing agents cannot see them during development.

## Quick Start

```bash
# Initialize holdout directory
/scenario init

# Add a scenario from a description
/scenario add "user can authenticate with valid credentials"

# List all active scenarios
/scenario list

# Validate scenarios against the schema
/scenario validate
```

## Execution Steps

### Step 1: Initialize Holdout Directory

```bash
ao scenario init
```

Creates `.agents/holdout/` with a `README.md` explaining holdout isolation
rules. If the directory already exists, this is a no-op.

The README makes clear:
- Implementing agents MUST NOT read `.agents/holdout/`
- Only evaluator agents and humans should author scenarios
- Hook enforcement prevents implementing agents from accessing holdout files

### Step 2: Author Scenarios

Provide a narrative description and the skill generates a schema-compliant
JSON scenario file.

```bash
ao scenario add "user can authenticate with valid credentials"
```

The skill will:
1. Generate an ID (`s-YYYY-MM-DD-NNN`)
2. Prompt for or infer the narrative, expected outcome, and acceptance vectors
3. Set default satisfaction threshold (0.8)
4. Write to `.agents/holdout/s-YYYY-MM-DD-NNN.json`

You can also author scenarios manually by writing JSON that conforms to
`schemas/scenario.v1.schema.json`. See [Scenario Schema Reference](references/scenario-schema.md).

### Step 3: Validate Scenarios

```bash
ao scenario validate
```

Validates every `.json` file in `.agents/holdout/` against
`schemas/scenario.v1.schema.json`. Reports:
- Schema violations (missing fields, wrong types)
- Duplicate IDs
- Stale scenarios (status = "active" but date > 90 days old)
- Acceptance vectors with no check command

### Step 4: List Scenarios

```bash
ao scenario list
```

Displays all scenarios with:
- ID, goal, status, source, date
- Satisfaction threshold
- Count of acceptance vectors

Filter options:
```bash
ao scenario list --status active
ao scenario list --status draft
ao scenario list --status retired
```

### Step 5: Integration with Validation

Scenarios are consumed by **STEP 1.8** in the `/validation` skill. During
validation, the evaluator agent:
1. Loads all active scenarios from `.agents/holdout/`
2. Runs each acceptance vector's check command
3. Computes a satisfaction score per scenario (0.0-1.0)
4. Aggregates into an overall holdout score
5. Fails the validation gate if any scenario falls below its threshold

## Key Rules

### Holdout Isolation

Scenarios are **holdout data**. The implementing agent must never see them.
This prevents the agent from overfitting to specific test cases instead of
building correct general behavior.

- Scenarios live in `.agents/holdout/`, which is outside the codebase
- A hook enforces that implementing agents cannot read holdout files
- Only evaluator agents, humans, or the `/validation` skill access scenarios

### Satisfaction Scoring

Scenarios use continuous satisfaction scoring (0.0-1.0), not boolean
pass/fail. This enables:
- Partial credit for incomplete implementations
- Trend tracking across iterations
- Threshold tuning per scenario based on criticality

Each acceptance vector produces a score, and the scenario's overall score
is the weighted average across all vectors.

### Authorship Rules

- Scenarios should be written by **humans** or by **evaluator agents**
- The implementing agent MUST NOT author its own scenarios
- The `source` field tracks provenance: `human`, `agent`, or `prod-telemetry`
- When an evaluator agent writes scenarios, it should operate in a separate
  session with no access to implementation details

### Scenario Lifecycle

| Status | Meaning |
|--------|---------|
| `active` | Scenario is evaluated during validation |
| `retired` | Scenario passed consistently; kept for reference |
| `blocked` | Scenario cannot be evaluated (missing dependency) |
| `draft` | Scenario is incomplete; not yet evaluated |

## Reference Documents

- [Scenario Schema Reference](references/scenario-schema.md) -- full field
  documentation and example JSON for the scenario schema

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `validate` reports missing fields | Schema version mismatch | Check `version` field matches schema expectation |
| Scenario not picked up by validation | Status is not `active` | Set `"status": "active"` in the JSON |
| Implementing agent read holdout | Hook not installed | Run `ao scenario init` to verify hook setup |
| Duplicate ID error | Two scenarios share an ID | Rename one using `s-YYYY-MM-DD-NNN` format |
| Stale scenario warning | Active scenario older than 90 days | Review and retire or refresh the scenario |
| Score always 0.0 | Check command returns non-zero | Debug the check command independently |

## See Also

- `/validation` -- consumes scenarios at STEP 1.8 for holdout evaluation
- `/council` -- multi-model review can generate scenario suggestions
- `/vibe` -- code quality validation (complementary to behavioral scenarios)
