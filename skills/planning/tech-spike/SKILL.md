---
name: definition.tech_spike
phase: definition
roles:
  - Engineering Lead
  - Staff Engineer
description: Scope and prioritize technical spikes that de-risk architecture or implementation questions.
variables:
  required:
    - name: topic
      description: Technology, component, or uncertainty to investigate.
    - name: desired_outcome
      description: Decision or learning goal that the spike must achieve.
  optional:
    - name: constraints
      description: Constraints such as timebox, compliance, or tooling.
    - name: collaborators
      description: Roles or teams partnering on the spike.
outputs:
  - Spike charter including background, questions, and deliverables.
  - Evaluation criteria and success definition.
  - Work plan with tasks, owners, and timebox.
---

# Purpose
Help engineering leaders quickly define spikes that reduce uncertainty and feed confidently into planning conversations.

# Pre-run Checklist
- ✅ Clarify what decision will be unlocked by the spike.
- ✅ Align on timebox and resourcing availability.
- ✅ Gather related research or prior explorations.

# Invocation Guidance
```bash
codex skills run definition.tech_spike \
  --vars "topic={{topic}}" \
         "desired_outcome={{desired_outcome}}" \
         "constraints={{constraints}}" \
         "collaborators={{collaborators}}"
```

# Recommended Input Attachments
- Architecture diagrams or RFCs.
- Known issues or bugs impacting the area.

# Claude Workflow Outline
1. Summarize context, desired outcome, and constraints.
2. Define success criteria and explicit questions to answer.
3. Outline the spike plan with tasks, owners, and deliverables.
4. Recommend instrumentation or benchmarks to capture results.
5. Provide guidance for sharing outcomes and converting to stories.

# Output Template
```
## Spike Charter — {{topic}}
### Background
...

### Questions to Answer
1. ...

### Success Criteria
- Criterion:

### Plan & Timebox
| Task | Owner | Duration | Notes |
| --- | --- | --- | --- |

### Reporting Plan
- Artifact:
- Audience:
- Next Steps:
```

# Follow-up Actions
- Create spike tickets in the engineering tracker with links to this output.
- Schedule readout with the product trio to review learnings.
- Convert recommendations into backlog work with acceptance criteria.
