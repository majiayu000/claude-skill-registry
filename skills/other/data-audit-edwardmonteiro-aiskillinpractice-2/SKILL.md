---
name: discovery.data_audit
phase: discovery
roles:
  - Data Analyst
  - Analytics Engineer
description: Inventory available datasets, instrumentation gaps, and data quality considerations for the initiative.
variables:
  required:
    - name: domain
      description: Product area or journey requiring data assessment.
    - name: decision_goals
      description: Business or product decisions the data should support.
  optional:
    - name: current_sources
      description: Known data sources or dashboards already leveraged.
    - name: compliance_flags
      description: Privacy or governance issues to consider.
outputs:
  - Data catalog listing sources, owners, freshness, and accessibility.
  - Gap analysis with recommended instrumentation or ETL changes.
  - Alignment summary on how data will support upcoming decisions.
---

# Purpose
Give analytics partners a reusable way to surface the state of data readiness and highlight what is needed to support discovery.

# Pre-run Checklist
- ✅ Access existing schema documentation or data dictionaries.
- ✅ Review outstanding data governance tickets or debt.
- ✅ Align with product on the decision timeline and required fidelity.

# Invocation Guidance
```bash
codex skills run discovery.data_audit \
  --vars "domain={{domain}}" \
         "decision_goals={{decision_goals}}" \
         "current_sources={{current_sources}}" \
         "compliance_flags={{compliance_flags}}"
```

# Recommended Input Attachments
- Links to Looker/Mode dashboards or warehouse tables.
- Screenshots of tracking plans or event schemas.

# Claude Workflow Outline
1. Summarize the decision goals and domain context.
2. Produce a data catalog table with source details, owners, freshness, and trust level.
3. Identify instrumentation or modeling gaps blocking the decision goals.
4. Recommend implementation steps, owners, and sequencing.
5. Outline interim proxies or experiments while data gaps are addressed.

# Output Template
```
## Data Inventory
| Source | Owner | Freshness | Accessibility | Trust Level | Notes |
| --- | --- | --- | --- | --- | --- |

## Gaps & Recommendations
1. Gap — Impact — Suggested Fix — Owner — Timeline

## Decision Support Plan
- Immediate next step:
- Interim proxy:
- Long-term instrumentation:
```

# Follow-up Actions
- File tracking or warehouse work items with clear acceptance criteria.
- Communicate data readiness to product and engineering leadership.
- Schedule follow-up audits post-implementation.
