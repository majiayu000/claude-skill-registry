---
name: delivery.tech_spec
phase: delivery
roles:
  - Engineering Lead
  - Feature Team Engineer
description: Produce an implementation-ready technical specification with architecture, sequencing, and validation details.
variables:
  required:
    - name: feature
      description: Feature or capability to be implemented.
    - name: objectives
      description: Desired business or customer outcomes for the work.
  optional:
    - name: constraints
      description: Technical, compliance, or timeline constraints.
    - name: integrations
      description: External systems or services impacted.
outputs:
  - Technical design overview with diagrams and data flow descriptions.
  - Implementation plan with milestones and task breakdown.
  - Validation strategy including testing, monitoring, and rollout considerations.
---

# Purpose
Accelerate engineering planning by generating a comprehensive spec template aligned with the squad's delivery standards.

# Pre-run Checklist
- ✅ Confirm definition artifacts (story map, spikes) are finalized.
- ✅ Align on target release milestone and success metrics.
- ✅ Gather existing system diagrams or API documentation.

# Invocation Guidance
```bash
codex skills run delivery.tech_spec \
  --vars "feature={{feature}}" \
         "objectives={{objectives}}" \
         "constraints={{constraints}}" \
         "integrations={{integrations}}"
```

# Recommended Input Attachments
- Architecture or sequence diagrams.
- API contracts or schema definitions.
- Relevant RFCs or ADRs.

# Claude Workflow Outline
1. Summarize feature objectives, constraints, and integration points.
2. Describe the target architecture, including components, data flows, and failure handling.
3. Outline implementation phases with tasks, owners, and dependencies.
4. Define validation strategy: testing, monitoring, observability, and rollout plan.
5. Provide documentation and review checklist.

# Output Template
```
# Technical Specification — {{feature}}

## 1. Summary & Objectives
- Objectives:
- Success Metrics:
- Constraints:

## 2. Architecture Overview
- Component Diagram Description
- Data Flow:
- Failure Modes & Mitigations:

## 3. Implementation Plan
| Milestone | Tasks | Owner | Dependencies | Target Date |
| --- | --- | --- | --- | --- |

## 4. Validation Strategy
- Testing:
- Monitoring & Alerts:
- Rollout Plan:

## 5. Open Questions & Risks
- Item — Owner — Due Date

## 6. Review Checklist
- [ ] Design review scheduled
- [ ] Security review required?
- [ ] Documentation updates planned
```

# Follow-up Actions
- Schedule a design review with relevant stakeholders.
- Break down milestone tasks into backlog tickets.
- Keep the spec updated as implementation progresses.
