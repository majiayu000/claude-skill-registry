---
name: optimization.quality_report
phase: optimization
roles:
  - QA Lead
  - Product Manager
description: Compile a recurring quality report that synthesizes defect trends, automation health, and recommendations.
variables:
  required:
    - name: period
      description: Reporting window (e.g., Week 32, August 2024).
    - name: focus_areas
      description: Product areas or squads covered.
  optional:
    - name: data_sources
      description: Tools or exports providing quality signals.
    - name: audience
      description: Stakeholder audience for the report.
outputs:
  - Quality highlights and summary.
  - Defect and automation metrics with commentary.
  - Recommended actions, owners, and follow-ups.
---

# Purpose
Increase transparency into product quality and drive prioritization of remediation work.

# Pre-run Checklist
- ✅ Collect defect stats, test automation results, and reliability metrics.
- ✅ Align on focus areas with product and engineering leadership.
- ✅ Verify data freshness and accuracy.

# Invocation Guidance
```bash
codex run --skill optimization.quality_report \
  --vars "period={{period}}" \
         "focus_areas={{focus_areas}}" \
         "data_sources={{data_sources}}" \
         "audience={{audience}}"
```

# Recommended Input Attachments
- Defect tracker export.
- Test automation dashboards or CI results.
- Incident or support ticket summaries.

# Claude Workflow Outline
1. Summarize reporting period, audience, and focus areas.
2. Highlight key wins, risks, and trends.
3. Provide metrics tables covering defects, automation, coverage, and customer impact.
4. Recommend remediation actions with owners and due dates.
5. Outline next review cadence and areas requiring deeper dives.

# Output Template
```
# Quality Report — {{period}}

## Highlights & Risks
- Highlight:
- Risk:

## Metrics Snapshot
| Metric | Current | Δ vs Prior | Target | Notes |
| --- | --- | --- | --- | --- |

## Defect & Automation Details
- Defect Backlog:
- Automation Pass Rate:
- Flaky Tests:

## Recommendations
| Action | Owner | Priority | Due Date |
| --- | --- | --- | --- |

## Next Steps
- Upcoming Reviews:
- Data Improvements Needed:
```

# Follow-up Actions
- Share the report with stakeholders via the agreed channel.
- Track recommendations in the quality improvement backlog.
- Plan deep dives on high-risk areas.
