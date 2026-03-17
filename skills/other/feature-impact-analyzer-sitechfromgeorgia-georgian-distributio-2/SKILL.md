---
name: feature-impact-analyzer
description: Product strategist for scoring and ranking feature ideas using RICE/ICE prioritization frameworks, connecting features to business KPIs (retention, growth, revenue), and identifying quick wins vs strategic bets. Use when evaluating product features, prioritizing roadmap items, analyzing feature requests, or making product investment decisions.
license: MIT
metadata:
  author: Product Strategy Team
  category: product-management
  version: 1.0.0
---

# Feature Impact Analyzer

## Overview

A comprehensive product prioritization system that applies proven frameworks (RICE, ICE, Impact/Effort) to evaluate and rank feature ideas based on their business impact. This skill helps product teams make data-driven decisions by connecting features to measurable KPIs and visualizing tradeoffs between effort and impact.

## Core Capabilities

1. **Multi-Framework Scoring**: Apply RICE, ICE, or Impact/Effort matrices
2. **KPI Alignment**: Connect features to retention, growth, and revenue metrics
3. **Tradeoff Visualization**: Generate 2x2 matrices showing impact vs effort
4. **Quick Win Identification**: Automatically flag high-impact, low-effort features
5. **Strategic Bet Analysis**: Identify long-term, high-investment opportunities
6. **Comparative Scoring**: Rank multiple features side-by-side

## When to Use This Skill

- Evaluating new feature requests or ideas
- Building or refining product roadmaps
- Prioritizing engineering resources
- Stakeholder discussions about feature priority
- Quarterly or annual planning sessions
- Responding to competitive pressure
- Analyzing user feedback themes

## Prioritization Workflows

### Workflow 1: Quick ICE Assessment

For fast decisions with limited data:

1. **Gather Feature Details**
   - Feature name and brief description
   - Target user segment
   - Problem being solved

2. **Score on 1-10 Scale**
   - **Impact**: How much will this improve the key metric?
   - **Confidence**: How certain are we about the estimates?
   - **Ease**: How simple is implementation?

3. **Calculate ICE Score**
   ```
   ICE Score = (Impact + Confidence + Ease) / 3
   ```

4. **Interpret Results**
   - Score 8-10: High priority, quick win candidate
   - Score 5-7: Medium priority, needs refinement
   - Score <5: Low priority or needs more research

### Workflow 2: Comprehensive RICE Analysis

For data-driven decisions with measurable reach:

1. **Define Success Metrics**
   - What metric are we trying to improve?
   - What timeframe? (per quarter, per month)

2. **Estimate Each Factor**
   
   - **Reach**: How many users/events affected per time period?
   - **Impact**: How much does it move the key metric? (0.25 - 3.0 scale)
     * 3.0 = Massive impact, 2.0 = High, 1.0 = Medium, 0.5 = Low
   - **Confidence**: How certain are we? (0-100%)
     * 100% = Strong data, 80% = Good data, 50% = Assumptions
   - **Effort**: How many person-months of work?

3. **Calculate RICE Score**
   ```
   RICE Score = (Reach × Impact × Confidence%) / Effort
   ```

4. **Rank and Prioritize**
   - Sort features by RICE score (highest first)
   - Identify top 3-5 features for next cycle

### Workflow 3: Impact/Effort Matrix

For visual stakeholder communication:

1. **Score Features**: Impact (1-10) and Effort (1-10)

2. **Plot on 2x2 Matrix**
   - **Quick Wins**: High Impact, Low Effort → Ship ASAP
   - **Strategic Bets**: High Impact, High Effort → Plan 2-3 quarters
   - **Fill-Ins**: Low Impact, Low Effort → Nice to have
   - **Time Sinks**: Low Impact, High Effort → Avoid

## Connecting Features to KPIs

### Retention KPIs
- Customer Retention Rate (CRR)
- Day 1/7/30 Retention Rates
- Churn Rate
- Net Revenue Retention (NRR)

**Example**:
```
Feature: Improved onboarding tutorial
Target KPI: Day 1 Retention (currently 35%)
Expected: +10pp (to 45%)
Reach: 5,000 new users/quarter
Impact: 2.0, Confidence: 80%, Effort: 2 PM
RICE: (5000 × 2.0 × 0.8) / 2 = 4,000
```

### Growth KPIs
- Monthly/Daily Active Users (MAU/DAU)
- User Acquisition Rate
- Activation Rate
- Viral Coefficient

**Example**:
```
Feature: Referral program
Target: Monthly signups (1,000/month)
Expected: +30% (to 1,300/month)
Reach: 10,000 active users
Impact: 2.5, Confidence: 70%, Effort: 3 PM
RICE: (10000 × 2.5 × 0.7) / 3 = 5,833
```

### Revenue KPIs
- Monthly Recurring Revenue (MRR)
- Average Revenue Per User (ARPU)
- Customer Lifetime Value (CLTV)
- Conversion Rate (Free to Paid)

## Output Formats

### Prioritized Backlog Table
```
| Rank | Feature | RICE | Impact | Effort | KPI Target |
|------|---------|------|--------|--------|------------|
| 1 | Referral | 5,833 | High | 3 PM | +30% signups |
| 2 | Onboarding | 4,000 | High | 2 PM | +10pp Day 1 |
```

### Impact/Effort Matrix
```
QUICK WINS (Ship Next Quarter)
- ✅ Feature A: Notifications
- ✅ Feature B: Search

STRATEGIC BETS (Plan Q2-Q3)
- 🎯 Feature C: AI recommendations
- 🎯 Feature D: Enterprise SSO
```

## Best Practices

1. **Use Real Metrics** - Pull actual data from analytics
2. **Document Assumptions** - Track confidence honestly
3. **Involve Stakeholders** - PMs, Engineering, Data, CS
4. **Avoid Pitfalls**:
   - ❌ Pet project bias
   - ❌ Loudest voice wins
   - ❌ Analysis paralysis
   - ❌ Ignoring strategic value

5. **Calibrate Quarterly** - Compare predicted vs actual results

## Decision Guidelines

### When to Override Scores
- Table stakes features (competitive parity)
- Technical debt (enables future velocity)
- Strategic positioning (long-term value)
- Regulatory requirements (compliance)

### Portfolio Balance
- 40-50%: Quick Wins
- 30-40%: Strategic Bets
- 10-20%: Technical Debt
- 5-10%: Experimental

## Integration with Tools

### Using Python Scripts

**Calculate RICE**:
```bash
python scripts/calculate_rice.py --reach 5000 --impact 2.0 --confidence 80 --effort 3
```

**Calculate ICE**:
```bash
python scripts/calculate_ice.py --impact 8 --confidence 7 --ease 6
```

**Batch Processing**:
```bash
python scripts/calculate_rice.py --csv features.csv --output results.csv
python scripts/calculate_ice.py --csv features.csv --output results.csv
```

### CSV Format Examples

See `assets/example_rice_features.csv` and `assets/example_ice_features.csv` for templates.

## Resources

For detailed information:
- **Framework Guide**: `references/FRAMEWORK_GUIDE.md`
- **KPI Mapping**: `references/KPI_MAPPING.md`
- **Evaluation Template**: `assets/prioritization_template.md`
- **Example Data**: `assets/example_*.csv`

---

**Remember**: Prioritization frameworks are tools to facilitate better discussions, not replacements for judgment. Use scores as inputs to thoughtful debate, not as final verdicts. Always consider strategic context, technical constraints, and business goals alongside numerical scores.