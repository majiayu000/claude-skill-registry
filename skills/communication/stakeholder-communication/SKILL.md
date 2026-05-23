---
name: stakeholder-communication
version: "2.0.0"
description: Stakeholder management, executive communication, and organizational alignment for product leaders.
sasmp_version: "1.3.0"
bonded_agent: 07-leadership-stakeholder
bond_type: PRIMARY_BOND
parameters:
  - name: audience_type
    type: string
    enum: [executive, board, cross_functional, team, external]
    required: true
  - name: communication_format
    type: string
    enum: [presentation, document, meeting, email]
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Stakeholder Communication Skill

Effectively communicate with stakeholders and manage expectations across the organization. Master executive communication and alignment.

## Executive Communication

### BLUF Format (Bottom Line Up Front)

```
BOTTOM LINE: [1 sentence - decision/news]

SITUATION: [2-3 sentences - context]

IMPLICATIONS: [2-3 sentences - why it matters]

NEXT STEPS: [Actions needed]
```

### Executive Summary Template

```
TITLE: [Topic]
DATE: [Date]
OWNER: [Name]

SUMMARY:
[2-3 sentence overview]

KEY METRICS:
- Metric 1: [Current vs Target]
- Metric 2: [Current vs Target]

DECISION NEEDED:
[What you need from reader]

TIMELINE:
[Key dates]
```

## Stakeholder Management

### Stakeholder Matrix

```
           HIGH INFLUENCE
                 │
    MANAGE       │      ENGAGE
    CLOSELY      │      ACTIVELY
    (Weekly)     │      (Weekly)
                 │
LOW ─────────────┼───────────── HIGH
INTEREST         │              INTEREST
                 │
    MONITOR      │      KEEP
    ONLY         │      INFORMED
    (Quarterly)  │      (Bi-weekly)
                 │
           LOW INFLUENCE
```

### RACI Matrix

| Task | Responsible | Accountable | Consulted | Informed |
|------|-------------|-------------|-----------|----------|
| Task 1 | Dev Lead | PM | Design | Eng Team |
| Task 2 | PM | CEO | Sales | All |

## Presentation Skills

### Presentation Structure (15 min)

```
1. Hook (1 min) - Why should they care?
2. Context (2 min) - Background
3. Problem (2 min) - What's wrong
4. Solution (5 min) - What you propose
5. Impact (3 min) - Benefits & metrics
6. Ask (2 min) - What you need
```

### Data Visualization Rules

- One point per chart
- Labels on chart, not legend
- Highlight key data
- Remove chart junk
- Use consistent colors

## Written Communication

### Status Update Template

```
PROJECT: [Name]
STATUS: On Track / At Risk / Off Track

PROGRESS THIS WEEK:
- [Completed item]
- [Completed item]

NEXT WEEK:
- [Planned item]
- [Planned item]

BLOCKERS:
- [Blocker + mitigation]

METRICS:
- [KPI]: [Value vs Target]
```

### Decision Document

```
DECISION: [What we decided]
DATE: [Date]
PARTICIPANTS: [Who was involved]

CONTEXT:
[Why this decision was needed]

OPTIONS CONSIDERED:
1. [Option A] - Pros/Cons
2. [Option B] - Pros/Cons

DECISION RATIONALE:
[Why we chose this option]

NEXT STEPS:
- [Action] - Owner - Date
```

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Stakeholder surprise | No early warning | Increase frequency |
| Misalignment | Unclear communication | BLUF, document |
| No decision | Too many stakeholders | RACI, single decider |
| Resistance | Not included early | Early involvement |

### Debug Checklist

```
[ ] RACI defined mi?
[ ] Communication cadence set mi?
[ ] Key stakeholders informed mi?
[ ] Decisions documented mi?
[ ] Follow-up scheduled mi?
```

### Recovery Procedures

1. **Stakeholder Surprise** → 1:1 meeting, rebuild trust
2. **Misalignment** → Alignment meeting, document
3. **Decision Deadlock** → Escalate with recommendation

## Learning Outcomes

- Present effectively to executives
- Manage stakeholder expectations
- Write clear status updates
- Build organizational alignment
- Handle difficult conversations
