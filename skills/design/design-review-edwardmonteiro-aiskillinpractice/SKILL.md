---
name: delivery.design_review
phase: delivery
roles:
  - Product Designer
  - Design Lead
description: Facilitate a cross-functional design review capturing decisions, feedback, and implementation guidance.
variables:
  required:
    - name: feature
      description: Feature or experience under review.
    - name: design_principles
      description: Principles or heuristics guiding evaluation.
  optional:
    - name: personas
      description: Personas impacted by the design changes.
    - name: artifacts
      description: Links to prototypes, screenshots, or specs.
outputs:
  - Review agenda with goals and focus areas.
  - Consolidated feedback by theme and severity.
  - Action items and decisions log for the design and engineering team.
---

# Purpose
Standardize design review preparation and documentation to speed up alignment with engineering and product partners.

# Pre-run Checklist
- ✅ Ensure prototypes or artifacts are ready and accessible.
- ✅ Align with product and engineering on review goals and decision points.
- ✅ Collect previous feedback or usability findings.

# Invocation Guidance
```bash
codex run --skill delivery.design_review \
  --vars "feature={{feature}}" \
         "design_principles={{design_principles}}" \
         "personas={{personas}}" \
         "artifacts={{artifacts}}"
```

# Recommended Input Attachments
- Screenshots or prototype links.
- Accessibility or brand guidelines.
- Usability research summaries.

# Claude Workflow Outline
1. Summarize review context, goals, and design principles.
2. Prepare an agenda with timings, focus areas, and attendees.
3. Capture feedback items grouped by principle or theme with severity and owners.
4. Document decisions, follow-ups, and implementation guidance.
5. Provide communication plan for sharing outcomes and updates.

# Output Template
```
## Design Review Agenda
- Objective:
- Attendees:
- Artifacts:
| Section | Duration | Focus |
| --- | --- | --- |

## Feedback Log
| Theme | Feedback | Severity | Owner | Due Date |
| --- | --- | --- | --- | --- |

## Decisions & Actions
- Decision:
  - Rationale:
  - Owner:

## Communication Plan
- Channel:
- Update cadence:
```

# Follow-up Actions
- Share the review document in the design and engineering channels.
- Track action items in the design backlog or issue tracker.
- Schedule follow-up reviews or async sign-offs as needed.
