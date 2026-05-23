---
name: optimization.experiment_brief
phase: optimization
roles:
  - Product Designer
  - Product Manager
description: Prepare an experiment brief outlining hypothesis, design, success metrics, and operational plan.
variables:
  required:
    - name: hypothesis
      description: Hypothesis statement to validate.
    - name: primary_metric
      description: Primary metric measuring experiment success.
  optional:
    - name: secondary_metrics
      description: Supporting or guardrail metrics.
    - name: audience
      description: User segment or cohort being targeted.
outputs:
  - Experiment overview with hypothesis, rationale, and metrics.
  - Test design including variants, sample size, and timeline.
  - Operational checklist for launch, monitoring, and decision-making.
---

# Purpose
Ensure experiments are well-defined, measurable, and aligned with user experience considerations before launch.

# Pre-run Checklist
- ✅ Align with analytics on measurement feasibility and sample size.
- ✅ Confirm design assets and engineering bandwidth for variants.
- ✅ Review related research or previous experiments for context.

# Invocation Guidance
```bash
codex run --skill optimization.experiment_brief \
  --vars "hypothesis={{hypothesis}}" \
         "primary_metric={{primary_metric}}" \
         "secondary_metrics={{secondary_metrics}}" \
         "audience={{audience}}"
```

# Recommended Input Attachments
- Design mockups or copy variations.
- Experiment backlog or learning agenda.
- Prior experiment analyses.

# Claude Workflow Outline
1. Summarize hypothesis, audience, and metrics.
2. Detail the experiment design: variants, allocation, instrumentation, and run duration.
3. Provide sample size estimation guidance and data dependencies.
4. Outline monitoring plan, success criteria, and decision framework.
5. Document collaboration and approval workflow.

# Output Template
```
## Experiment Overview
- Hypothesis:
- Audience:
- Primary Metric:
- Secondary Metrics:

## Test Design
| Variant | Description | % Allocation | Key Changes |
| --- | --- | --- | --- |
- Expected Duration:
- Sample Size Estimate:

## Measurement & Monitoring
- Instrumentation Checklist:
- Data Quality Checks:
- Decision Cadence:

## Launch Plan
- Approvals:
- Launch Date:
- Responsibilities:
```

# Follow-up Actions
- Secure approvals from product, design, engineering, and analytics leads.
- Schedule mid-test reviews to monitor guardrails.
- Plan post-test readout session.
