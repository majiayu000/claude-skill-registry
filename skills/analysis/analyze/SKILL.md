---
name: analyze
description: Invoke IMMEDIATELY via python script when user requests codebase analysis, architecture review, security assessment, or quality evaluation. Do NOT explore first - the script orchestrates exploration.
license: MIT
metadata:
---

# Analyze Skill

When this skill activates, IMMEDIATELY invoke the script. The script IS the workflow.

## Invocation

```bash
python3 scripts/analyze.py \
  --step-number 1 \
  --total-steps 6 \
  --thoughts "Starting analysis. User request: <describe what user asked to analyze>"
```

| Argument        | Required | Description                               |
| --------------- | -------- | ----------------------------------------- |
| `--step-number` | Yes      | Current step (starts at 1)                |
| `--total-steps` | Yes      | Minimum 6; adjust as script instructs     |
| `--thoughts`    | Yes      | Accumulated state from all previous steps |

## Workflow

The script outputs REQUIRED ACTIONS at each step. Follow them exactly.

```
Step 1: EXPLORATION         - Script tells you to delegate to Explore agent
Step 2: FOCUS SELECTION     - Classify areas, assign priorities
Step 3: INVESTIGATION PLAN  - Commit to specific files and questions
Step 4+: DEEP ANALYSIS      - Progressive investigation with evidence
Step N-1: VERIFICATION      - Validate completeness
Step N: SYNTHESIS           - Consolidate findings
```

Do NOT try to follow this workflow manually. Run the script and follow its output.

## Example Sequence

```bash
# Step 1: Start - script will instruct you to explore first
python3 scripts/analyze.py --step-number 1 --total-steps 6 \
  --thoughts "Starting analysis of auth system"

# [Follow REQUIRED ACTIONS from output - delegate to Explore agent]

# Step 1 again with explore results
python3 scripts/analyze.py --step-number 1 --total-steps 6 \
  --thoughts "Explore found: Flask app, SQLAlchemy, auth/ dir..."

# Step 2+: Continue following script output
python3 scripts/analyze.py --step-number 2 --total-steps 7 \
  --thoughts "[accumulated state from step 1] Focus: security P1, quality P2"
```
