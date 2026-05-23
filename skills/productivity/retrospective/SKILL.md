---
name: optimization.retrospective
phase: optimization
roles:
  - Product Manager
  - Engineering Lead
  - Scrum Master
description: Facilitate a sprint or release retrospective focusing on insights, actions, and ownership.
variables:
  required:
    - name: period
      description: Sprint, release, or project window being reviewed.
    - name: goals
      description: Goals or commitments set for the period.
  optional:
    - name: participants
      description: Roles attending the retrospective.
    - name: data_points
      description: Supporting metrics or signals to consider.
outputs:
  - Retrospective agenda and prompts.
  - Themed insights categorized as Keep/Stop/Start or equivalent.
  - Action plan with owners, due dates, and follow-up cadence.
---

# Purpose
Ensure retrospectives are structured, psychologically safe, and result in actionable improvements.

# Pre-run Checklist
- ✅ Collect metrics, incidents, and feedback for the reviewed period.
- ✅ Confirm participants and logistical details.
- ✅ Align on facilitation approach and tools.

# Invocation Guidance
```bash
codex run --skill optimization.retrospective \
  --vars "period={{period}}" \
         "goals={{goals}}" \
         "participants={{participants}}" \
         "data_points={{data_points}}"
```

# Recommended Input Attachments
- Sprint reports, burndown charts, or throughput metrics.
- Incident summaries or customer feedback.

# Claude Workflow Outline
1. Summarize period context, goals, and participants.
2. Propose an agenda with timings and facilitation tips.
3. Capture insights under themes (Keep, Stop, Start) or squad-specific categories.
4. Translate insights into actionable improvements with owners and deadlines.
5. Provide follow-up rituals for accountability.

# Output Template
```
## Retrospective Agenda — {{period}}
| Segment | Time | Purpose | Facilitation Tips |
| --- | --- | --- | --- |

## Insights
### Keep Doing
- ...

### Stop Doing
- ...

### Start Doing
- ...

## Action Plan
| Action | Owner | Due Date | Success Measure |
| --- | --- | --- | --- |

## Follow-up
- Next Check-in:
- Accountability Mechanism:
```

# Follow-up Actions
- Share retro notes with the squad and stakeholders.
- Track action items in the team workspace and revisit each retro.
- Celebrate improvements and adjust format as needed.
