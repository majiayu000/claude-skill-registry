---
name: definition.metric_catalog
phase: definition
roles:
  - Data Analyst
  - Product Manager
description: Document key metrics, definitions, and segmentation required to track product success.
variables:
  required:
    - name: theme
      description: Product or business theme (e.g., Activation, Retention).
    - name: required_segments
      description: Segmentation dimensions needed for reporting.
  optional:
    - name: measurement_tools
      description: Analytics tools or warehouses where metrics live.
    - name: stakeholders
      description: Stakeholders who rely on the metrics.
outputs:
  - Metric catalog with definitions, formulas, and owners.
  - Segmentation guidance and data availability notes.
  - Instrumentation or governance checklist.
---

# Purpose
Ensure product and analytics teams align on the metrics that matter, how they are defined, and how they will be reported.

# Pre-run Checklist
- ✅ Review existing dashboards and metric definitions.
- ✅ Confirm segmentation requirements with stakeholders.
- ✅ Verify data availability or instrumentation plans for new metrics.

# Invocation Guidance
```bash
codex run --skill definition.metric_catalog \
  --vars "theme={{theme}}" \
         "required_segments={{required_segments}}" \
         "measurement_tools={{measurement_tools}}" \
         "stakeholders={{stakeholders}}"
```

# Recommended Input Attachments
- Current metric definitions or SQL queries.
- Business reviews or KPI scorecards.

# Claude Workflow Outline
1. Summarize the theme and stakeholders.
2. Build a catalog table with metric names, definitions, formulas, owners, and tools.
3. Detail segmentation requirements, data sources, and known gaps.
4. Provide governance and instrumentation checklist for each metric.
5. Suggest review cadence and communication plan.

# Output Template
```
## Metric Catalog — {{theme}}
| Metric | Definition | Formula / Source | Owner | Tool | Segments |
| --- | --- | --- | --- | --- | --- |

## Segmentation Guidance
- Required Segments:
- Data Availability:
- Known Gaps:

## Governance & Instrumentation
| Metric | Quality Checks | Instrumentation Actions | Review Cadence |
| --- | --- | --- | --- |
```

# Follow-up Actions
- Publish the catalog in the analytics knowledge base.
- Align with engineering on instrumentation stories.
- Schedule periodic metric reviews to ensure definitions stay current.
