---
name: resubmission-deadline-tracker
description: Track manuscript resubmission deadlines and automatically generate phase-appropriate task breakdowns for academic researchers based on remaining time.
license: MIT
skill-author: AIPOCH
---
# Resubmission Deadline Tracker

Track manuscript resubmission deadlines and generate actionable task schedules based on remaining time.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Use this skill when tracking one or more manuscript resubmission deadlines and generating a task breakdown.
- Use this skill when assessing urgency level and creating a phase-appropriate revision schedule.
- Do not use this skill to sync with journal submission systems, send automated reminders, or manage grant deadlines.

## Workflow

1. Confirm the manuscript title, journal, deadline date, and reviewer issue counts.
2. **Timezone validation:** If `--timezone` is not provided, default to `Asia/Shanghai` and emit a note: "Deadline calculated using Asia/Shanghai timezone. Use `--timezone` to specify your local timezone (e.g., `America/New_York`, `Europe/London`)."
3. Calculate remaining time and assign urgency level (standard / urgent / emergency).
4. Generate a phase-appropriate task schedule based on the urgency level.
5. Return the deadline summary, task breakdown, and risk notes.
6. If inputs are incomplete, state exactly which fields are missing and request only the minimum additional information.

## Usage

```text
# Add new deadline
python scripts/main.py --add --title "Cancer Research Paper" \
  --journal "Nature Medicine" --deadline "2024-03-15" \
  --major-issues 2 --minor-issues 8

# List all tracked deadlines
python scripts/main.py --list

# Show details for specific paper
python scripts/main.py --show "Cancer Research Paper"

# Generate task breakdown
python scripts/main.py --tasks "Cancer Research Paper"

# Update progress
python scripts/main.py --update "Cancer Research Paper" --progress 60
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--deadline` | date | Yes | — | Target submission date (YYYY-MM-DD) |
| `--title` | string | No | — | Manuscript title |
| `--journal` | string | No | — | Target journal name |
| `--major-issues` | integer | No | 0 | Count of major reviewer concerns |
| `--minor-issues` | integer | No | 0 | Count of minor reviewer concerns |
| `--timezone` | string | No | Asia/Shanghai | User timezone |

## Urgency Levels

| Remaining Time | Level | Mode |
|----------------|-------|------|
| > 14 days | Standard | Full 4-phase schedule |
| 3–14 days | Urgent | Triage and P0-only execution |
| < 3 days | Emergency | Minimum viable changes + extension request |

**Note:** The 3–7 day range was previously labeled "Urgent" but the boundary is 3–14 days. Any remaining time between 3 and 14 days triggers Urgent mode.

## Output

- Deadline summary with urgency status
- Phase-by-phase task schedule
- Daily targets and checkbox list
- Risk notes (timezone, submission type, buffer time)

## Stress-Case Rules

For complex multi-constraint requests, always include these explicit blocks:

1. Assumptions
2. Deadline and Urgency Assessment
3. Task Schedule
4. Risks and Caveats
5. Next Checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate deadline dates, journal policies, or task estimates.

## Input Validation

This skill accepts: a manuscript resubmission deadline with optional reviewer issue counts and journal details.

If the request does not involve manuscript resubmission deadline tracking — for example, asking to manage grant deadlines, sync with journal systems, or send automated email reminders — do not proceed with the workflow. Instead respond:
> "resubmission-deadline-tracker is designed to track manuscript resubmission deadlines and generate task schedules. Your request appears to be outside this scope. Please provide a deadline date and manuscript details, or use a more appropriate tool."

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
