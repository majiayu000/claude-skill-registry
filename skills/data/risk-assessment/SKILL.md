---
name: discovery.risk_assessment
phase: discovery
roles:
  - QA Lead
  - Reliability Engineer
description: Identify potential quality, security, and delivery risks early in discovery to inform mitigation planning.
variables:
  required:
    - name: feature
      description: Feature or initiative being evaluated.
    - name: scope
      description: Intended platforms, channels, or user journeys in scope.
  optional:
    - name: known_gaps
      description: Known technical or process gaps already identified.
    - name: compliance_requirements
      description: Regulatory or policy obligations that introduce risk.
outputs:
  - Risk taxonomy grouped by functional, non-functional, and process risks.
  - Impact/probability matrix with mitigation suggestions.
  - Questions to resolve during definition and delivery phases.
---

# Purpose
Enable QA and reliability partners to bring risk thinking into discovery conversations and influence scope decisions early.

# Pre-run Checklist
- ✅ Confirm initial feature concept or brief is available.
- ✅ Collect historical incidents or bug trends for similar areas.
- ✅ Align on acceptable risk tolerance with product and engineering.

# Invocation Guidance
```bash
codex skills run discovery.risk_assessment \
  --vars "feature={{feature}}" \
         "scope={{scope}}" \
         "known_gaps={{known_gaps}}" \
         "compliance_requirements={{compliance_requirements}}"
```

# Recommended Input Attachments
- Post-incident reports or retrospective documents.
- Quality dashboards highlighting defect rates or test coverage.

# Claude Workflow Outline
1. Restate the feature scope and critical user journeys.
2. Categorize risks into functional, non-functional, data, and process buckets.
3. For each risk, assign impact, probability, detection difficulty, and owner.
4. Recommend mitigations, including tests, instrumentation, or process changes.
5. Surface questions or dependencies that need resolution before definition completes.

# Output Template
```
## Risk Overview
...

## Risk Matrix
| Risk | Category | Impact | Probability | Detection | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- | --- |

## Follow-up Questions
1. ...
2. ...
```

# Follow-up Actions
- Log high risks in the squad RAID register.
- Schedule risk reviews with security or compliance as needed.
- Ensure mitigation actions are reflected in planning artifacts.
