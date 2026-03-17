---
name: aget-generate-report
description: Generate reports with metrics, findings, and visualizations
archetype: analyst
allowed-tools:
  - Read
  - Glob
  - Write
---

# aget-generate-report

Generate structured reports presenting analysis results, metrics, and insights. Tailored to audience needs.

## Instructions

When this skill is invoked:

1. **Determine Report Parameters**
   - Report type: Status, Analysis, Summary, Executive
   - Target audience: Executive, Technical, Operational
   - Scope and time period

2. **Structure the Report**
   - Executive Summary (always first)
   - Key Metrics with definitions
   - Findings and Analysis
   - Recommendations
   - Appendix (if needed)

3. **Populate Content**
   - Lead with most important findings
   - Include visualizations where data supports
   - Use appropriate detail level for audience

4. **Quality Check**
   - Verify all metrics have context
   - Ensure recommendations are actionable
   - Check navigation for long reports

## Output Format

```markdown
# [Report Title]

**Date**: [YYYY-MM-DD]
**Author**: [Agent Name]
**Audience**: [Executive/Technical/Operational]
**Period**: [Time range covered]

---

## Executive Summary

[2-3 sentences capturing key takeaways]

**Key Findings**:
- [Finding 1]
- [Finding 2]

---

## Metrics

| Metric | Value | Definition | Trend |
|--------|-------|------------|-------|
| [Metric 1] | [Value] | [What it measures] | [↑/↓/→] |

---

## Findings

### [Finding Category 1]

[Detailed analysis with supporting data]

---

## Recommendations

1. **[Action]**: [Rationale]

---

## Appendix

[Supporting data, methodology, raw tables]
```

## Constraints

- **C1**: NEVER include raw data dumps without context — reports must interpret data
- **C2**: NEVER bury critical findings in appendices — key findings must be prominent
- **C3**: NEVER generate reports exceeding 10 pages without sectioned navigation

## Related

- SKILL-017: aget-generate-report specification
- ONTOLOGY_analyst.yaml: Report, Metric, Visualization concepts
- CAP-ANL-002: Report Generation capability
