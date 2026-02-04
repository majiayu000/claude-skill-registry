---
name: delivery.roadmap
phase: delivery
roles:
  - Product Manager
  - Program Manager
description: Create a delivery roadmap that translates strategy into sequenced releases with milestones and dependencies.
variables:
  required:
    - name: product
      description: Product or program to roadmap.
    - name: horizon
      description: Time horizon (e.g., next 2 quarters).
  optional:
    - name: themes
      description: Strategic themes or pillars to organize work.
    - name: dependencies
      description: Known cross-team or platform dependencies.
outputs:
  - Timeline view of releases or increments with objectives and success metrics.
  - Dependency and risk register with mitigation steps.
  - Communication plan for stakeholders.
---

# Purpose
Provide a roadmap artifact that balances ambition with delivery realism and gives stakeholders visibility into upcoming milestones.

# Pre-run Checklist
- ✅ Align on strategic themes and investment mix with leadership.
- ✅ Confirm engineering capacity and velocity assumptions.
- ✅ Collect known dependencies, risks, and sequencing constraints.

# Invocation Guidance
```bash
codex run --skill delivery.roadmap \
  --vars "product={{product}}" \
         "horizon={{horizon}}" \
         "themes={{themes}}" \
         "dependencies={{dependencies}}"
```

# Recommended Input Attachments
- OKR drafts or strategic plans.
- Engineering capacity plans.
- Dependency tracker or RAID log.

# Claude Workflow Outline
1. Summarize product vision, horizon, and strategic themes.
2. Map releases or increments across the horizon with objectives, metrics, and target dates.
3. Identify dependencies, risks, and mitigation strategies per increment.
4. Provide stakeholder communication plan and review cadence.
5. Suggest visualization tips for slides or shared docs.

# Output Template
```
## Roadmap Overview — {{product}} ({{horizon}})
| Increment | Target Date | Theme | Objective | Success Metric | Key Dependencies |
| --- | --- | --- | --- | --- | --- |

## Risks & Mitigations
| Risk | Impact | Likelihood | Mitigation | Owner | Review Date |
| --- | --- | --- | --- | --- | --- |

## Stakeholder Communication Plan
- Audience:
- Channel:
- Cadence:
```

# Follow-up Actions
- Socialize roadmap with core stakeholders for feedback and sign-off.
- Integrate roadmap milestones into project tracking tools.
- Review and update monthly based on delivery progress and learnings.
