---
name: product-manager
description: Product management: PRDs, RICE prioritization, metrics
allowed-tools: Read, Write, Grep
---

# Product Manager

Assists with core product management workflows including research synthesis, requirement documentation, feature prioritization, and strategic communication.

## When to Use
- Analyzing user interviews, surveys, or feedback
- Writing or reviewing PRDs and product requirements
- Prioritizing features or roadmap items
- Preparing stakeholder updates or presentations
- Interpreting product metrics and analytics
- Conducting competitive analysis

## Instructions

### User Research Analysis
When analyzing user research:
1. Read the provided transcripts, feedback, or survey data
2. Identify the top 3-5 pain points with supporting quotes
3. Group insights by themes (not by individual users)
4. Prioritize by frequency AND impact
5. Suggest 2-3 actionable opportunity areas
6. Include specific quotes to support each finding

### Feature Prioritization
When prioritizing features, use the RICE framework:
- **Reach**: How many users impacted per time period?
- **Impact**: Confidence score (0.25=minimal, 0.5=low, 1=medium, 2=high, 3=massive)
- **Confidence**: Data quality (0-100%)
- **Effort**: Person-months required
- **RICE Score** = (Reach × Impact × Confidence) / Effort

Present results in a table with reasoning for each score.

### PRD Writing
When creating or reviewing PRDs, ensure these sections:
1. **Problem Statement**: Clear user problem with evidence
2. **Success Metrics**: Quantifiable measures (not "improve UX")
3. **User Stories**: Format: "As a [user], I want [action] so that [benefit]"
4. **Acceptance Criteria**: Testable, specific conditions
5. **Edge Cases**: Error states, boundary conditions, empty states
6. **Out of Scope**: What we're explicitly NOT building

Flag any missing or unclear sections.

### Stakeholder Communication
When drafting communications:
1. Lead with impact/outcome, not features
2. Match tone to audience (C-level: business impact; Eng: technical details)
3. Use specific metrics, not vague terms like "better" or "improved"
4. Include next steps with owners and timelines
5. Be transparent about blockers/challenges

### Metrics Analysis
When analyzing metrics:
1. Calculate key ratios (DAU/MAU, retention cohorts, conversion rates)
2. Identify trends (week-over-week, month-over-month)
3. Flag anomalies requiring investigation
4. Distinguish between correlation and causation
5. Provide 2-3 actionable recommendations

## Quick Reference

**Problem Validation Checklist**:
- [ ] Problem clearly articulated?
- [ ] Validated with real users (not assumptions)?
- [ ] Frequent/painful enough to solve?
- [ ] Users will pay/engage more if solved?
- [ ] Technically feasible within constraints?

**Go/No-Go Decision Criteria**:
- Strategic alignment with company vision?
- Solves a validated user problem?
- Moves key metrics meaningfully?
- Team can build and maintain it?
- Strengthens competitive differentiation?

## Guidelines
- Focus on outcomes (metrics moved) over outputs (features shipped)
- Validate assumptions with data before building
- Write testable, specific requirements (avoid "intuitive" or "easy to use")
- Consider edge cases: errors, empty states, loading states
- Question vanity metrics (prioritize engagement over page views)
- Be explicit about trade-offs in prioritization decisions

**Automatic Triggers**:
- User pastes interview transcripts or feedback
- User asks to prioritize features or compare options
- User mentions "PRD", "product requirements", or "user stories"
- User shares metrics data or analytics
- User requests stakeholder updates or presentations