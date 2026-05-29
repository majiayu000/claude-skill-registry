---
name: stakeholder-docs
description: Executive documentation from technical living docs - business summaries, progress dashboards, feature status reports. Use for stakeholder communication.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
context: fork
model: sonnet
---

# Stakeholder Documentation Skill

Expert in translating technical living documentation into business-friendly views for stakeholders, executives, and non-technical team members.

## When This Skill Activates

- Creating executive summaries or board reports
- Generating progress dashboards for management
- Writing business impact statements
- Creating feature status overviews
- Preparing quarterly/monthly reports
- Translating technical docs for sales/customer-facing use

## What I Generate

### 1. Executive Summary

One-page overview of project/feature status:

```markdown
# [Project Name] Executive Summary
*Generated: [Date] | Period: [Sprint/Quarter]*

## Quick Stats

| Metric | Value | Trend |
|--------|-------|-------|
| Features Delivered | 12 | +3 vs last quarter |
| Active Work Items | 8 | On track |
| Test Coverage | 87% | +5% |
| Documentation Currency | 94% | Stable |

## Key Achievements

1. **[Feature A]** - Reduced checkout time by 40%
2. **[Feature B]** - Enabled 3 new enterprise customers
3. **[Feature C]** - Improved system reliability to 99.9%

## Current Focus

- [Active Initiative 1] - ETA: 2 weeks
- [Active Initiative 2] - ETA: 4 weeks

## Risks & Blockers

| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk 1] | Medium | Mitigation plan in place |
| [Blocker 1] | High | Escalated, awaiting decision |

## Next Quarter Priorities

1. [Priority 1] - Business Value: [description]
2. [Priority 2] - Business Value: [description]
```

### 2. Feature Status Dashboard

Visual progress tracking for all features:

```markdown
# Feature Status Dashboard
*Last Updated: [Date]*

## Overall Progress

**Total Features**: 25 | **Completed**: 18 | **In Progress**: 5 | **Blocked**: 2

## Feature Breakdown

### Completed This Quarter

| Feature | Business Impact | Delivered |
|---------|-----------------|-----------|
| User Authentication | Security compliance | Q1 2025 |
| Payment Integration | Revenue enablement | Q1 2025 |

### In Progress

| Feature | Progress | ETA | Owner |
|---------|----------|-----|-------|
| Analytics Dashboard | 75% | Feb 2025 | Team A |
| API v2 | 40% | Mar 2025 | Team B |

### Blocked

| Feature | Blocker | Action Required |
|---------|---------|-----------------|
| Mobile App | Vendor delay | Escalate to CTO |
```

### 3. Business Impact Statement

For each feature, translate technical details into business value:

```markdown
# Business Impact: [Feature Name]

## Summary

**What**: [One sentence describing the feature]
**Why**: [Business problem solved]
**Who Benefits**: [Target users/customers]

## Business Value

| Metric | Before | After | Impact |
|--------|--------|-------|--------|
| Process Time | 5 min | 30 sec | 90% reduction |
| Error Rate | 5% | 0.1% | 98% reduction |
| Customer Satisfaction | 3.2 | 4.5 | +40% |

## ROI Calculation

- **Investment**: [Development cost]
- **Annual Savings**: [Cost reduction]
- **Revenue Impact**: [Revenue increase]
- **Payback Period**: [Months]

## Success Metrics

1. [Metric 1]: Target [X], Current [Y]
2. [Metric 2]: Target [X], Current [Y]
```

### 4. Release Summary

Non-technical release notes for stakeholders:

```markdown
# Release [Version] Summary
*Release Date: [Date]*

## Highlights

This release delivers [X] improvements that [business benefit].

## What's New

### For Customers
- **[Feature 1]**: [Customer benefit in plain language]
- **[Feature 2]**: [Customer benefit in plain language]

### For Operations
- **[Improvement 1]**: [Operational benefit]
- **[Improvement 2]**: [Operational benefit]

## Known Limitations

- [Limitation 1] - Workaround: [description]

## Next Release Preview

Coming in [timeframe]: [brief preview of upcoming features]
```

## How to Use

### From Technical Living Docs

I read from `.specweave/docs/internal/` and transform:

| Source | Output |
|--------|--------|
| `specs/` feature specs | Feature Status Dashboard |
| `strategy/` docs | Executive Summary |
| Increment metadata | Progress Reports |
| ADRs | Risk/Decision summaries |

### Generation Commands

```bash
# Generate executive summary
"Create an executive summary of our current project status"

# Generate feature dashboard
"Generate a feature status dashboard for Q1"

# Create business impact statement
"Write a business impact statement for the authentication feature"

# Prepare release summary
"Create a stakeholder-friendly release summary for v2.0"
```

## Best Practices

### DO

1. **Use plain language** - Avoid jargon, explain acronyms
2. **Focus on outcomes** - "Reduced wait time by 40%" not "Optimized database queries"
3. **Include metrics** - Numbers make impact tangible
4. **Highlight risks early** - Stakeholders need to know blockers
5. **Show progress visually** - Tables, percentages, trends

### DON'T

1. **Don't include technical details** - No code, no architecture diagrams
2. **Don't use developer terminology** - "API" → "integration", "deploy" → "release"
3. **Don't bury bad news** - Lead with blockers if they exist
4. **Don't overload with data** - Curate, don't dump

## Output Locations

Generated stakeholder docs are saved to:

```
.specweave/docs/internal/strategy/
├── executive-summary.md      # Overall project summary
├── feature-dashboard.md      # Feature status tracking
├── quarterly-report-Q1.md    # Quarterly summaries
└── business-impact/
    └── [feature-name].md     # Per-feature impact statements
```

## Integration with Living Docs

This skill works best when combined with:

- **living-docs-navigator**: Navigate source technical docs
- **docs-writer**: Generate detailed documentation
- **image-generation**: Add charts and visualizations via `/sw:image-generation`

## Activation Keywords

This skill activates automatically when you mention:
- "executive summary", "board report", "investor update"
- "stakeholder", "non-technical", "business view"
- "progress dashboard", "feature status"
- "quarterly report", "monthly update"
- "business impact", "ROI", "business value"
- "release summary", "customer-facing docs"
