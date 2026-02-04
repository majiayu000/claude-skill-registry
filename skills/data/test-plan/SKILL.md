---
name: delivery.test_plan
phase: delivery
roles:
  - QA Lead
  - Test Engineer
description: Generate a detailed test plan covering scenarios, environments, data, and reporting for the release.
variables:
  required:
    - name: feature
      description: Release or feature to validate.
    - name: scope
      description: Platforms, locales, or customer segments included.
  optional:
    - name: regression_focus
      description: Critical regression areas that require emphasis.
    - name: external_dependencies
      description: Services or teams whose readiness impacts testing.
outputs:
  - Test scenario matrix with priority, type, and ownership.
  - Environment, data, and tooling checklist.
  - Reporting cadence and exit criteria.
---

# Purpose
Transform the high-level test strategy into an actionable plan that QA can execute throughout the delivery lifecycle.

# Pre-run Checklist
- ✅ Finalize scope, requirements, and acceptance criteria with product and engineering.
- ✅ Align on test environment availability and cutover timelines.
- ✅ Gather data requirements and staging credentials.

# Invocation Guidance
```bash
codex run --skill delivery.test_plan \
  --vars "feature={{feature}}" \
         "scope={{scope}}" \
         "regression_focus={{regression_focus}}" \
         "external_dependencies={{external_dependencies}}"
```

# Recommended Input Attachments
- User stories with acceptance criteria.
- Integration contracts or mock data samples.
- Past regression suites or automation scripts.

# Claude Workflow Outline
1. Restate feature scope, critical flows, and constraints.
2. Enumerate test scenarios covering functional, integration, and non-functional needs.
3. Map scenarios to owners, environments, data sets, and automation status.
4. Outline environment prep, tooling setup, and data seeding steps.
5. Provide reporting cadence, defect triage plan, and exit criteria.

# Output Template
```
## Test Scenario Matrix
| Scenario | Type | Priority | Owner | Environment | Data Needs | Automation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Environment & Data Checklist
- Environment:
- Access/Credentials:
- Data Setup Tasks:

## Reporting & Exit Criteria
- Daily reporting cadence:
- Defect SLA:
- Exit Criteria:
```

# Follow-up Actions
- Import scenarios into the test management tool.
- Schedule daily stand-ups or async updates for the test window.
- Coordinate with release management on exit criteria sign-off.
