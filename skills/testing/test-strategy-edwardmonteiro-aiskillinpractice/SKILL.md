---
name: definition.test_strategy
phase: definition
roles:
  - QA Lead
  - Test Engineer
description: Define the holistic testing approach across functional, non-functional, and automation layers for the initiative.
variables:
  required:
    - name: feature
      description: Feature, release, or program under test.
    - name: scope
      description: Platforms, devices, or channels included in coverage.
  optional:
    - name: non_functional
      description: Critical non-functional requirements such as performance or accessibility.
    - name: constraints
      description: Time, tooling, or staffing constraints to consider.
outputs:
  - Testing goals and risk-based prioritization.
  - Coverage matrix across test types and environments.
  - Milestones, entry/exit criteria, and reporting cadence.
---

# Purpose
Equip QA teams with a thorough test strategy document ready to align with engineering and product before delivery begins.

# Pre-run Checklist
- ✅ Review discovery risk assessment outcomes.
- ✅ Gather architectural diagrams and integration dependencies.
- ✅ Confirm available automation frameworks and environment readiness.

# Invocation Guidance
```bash
codex run --skill definition.test_strategy \
  --vars "feature={{feature}}" \
         "scope={{scope}}" \
         "non_functional={{non_functional}}" \
         "constraints={{constraints}}"
```

# Recommended Input Attachments
- Historical defect data or production incident summaries.
- Existing test plans or automation coverage reports.

# Claude Workflow Outline
1. Summarize feature scope, risks, and constraints.
2. Define testing objectives tied to quality risks and success metrics.
3. Produce a coverage matrix mapping test types to owners, environments, and tooling.
4. Outline milestones with entry/exit criteria and reporting cadence.
5. Highlight dependencies, data needs, and automation investments.

# Output Template
```
## Test Strategy Overview
Feature: {{feature}}
Scope: {{scope}}

## Testing Objectives
- Objective — Risk addressed — Metric

## Coverage Matrix
| Test Type | Owner | Environment | Tooling | Automation | Notes |
| --- | --- | --- | --- | --- | --- |

## Milestones & Criteria
| Milestone | Entry Criteria | Exit Criteria | Target Date | Owner |
| --- | --- | --- | --- | --- |

## Dependencies & Data Needs
- Dependency:
- Mitigation:
```

# Follow-up Actions
- Review strategy with engineering and product leadership for sign-off.
- Translate coverage needs into executable test cases in the test management tool.
- Track progress and update strategy as scope evolves.
