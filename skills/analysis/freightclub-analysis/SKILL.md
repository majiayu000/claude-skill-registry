---
name: freightclub-analysis
description: |
  FreightClub/ShipStation Shipping Data Analysis v3.0 - Enhanced with Revenue Architect rubrics.
  Triggers on: "freightclub analysis", "shipping data analysis", "PLD analysis", "shipstation export"
  Use when: Customer provides shipping data export for rate analysis or FirstMile opportunity assessment.
---

# FreightClub Shipping Data Analysis v3.0

> Enhanced with Revenue Architect Practice Gym rubrics for Customer Shipping Analysis

## What Changed from v2.0

| v2.0 | v3.0 Enhancement |
|------|------------------|
| Data tables only | + "So what?" insights after each section |
| No savings estimate | + FirstMile opportunity with $/annual projection |
| No confidence levels | + Data quality flags (Confirmed/Inferred/Missing) |
| Generic distributions | + Network fit analysis (Select vs National) |
| No next steps | + Actionable recommendations with timeline |
| 7 sheets | + 2 sheets: FirstMile Opportunity, Recommendations |

---

## Rubric Alignment (Score Target: 4.5+/5)

| Dimension | How v3.0 Addresses |
|-----------|-------------------|
| **Data Accuracy** | Confidence levels on every metric; data quality audit section |
| **Insight Clarity** | "Key Insight" box after every distribution table |
| **Savings Credibility** | Conservative/moderate/aggressive scenarios with math shown |
| **Visual Communication** | Executive dashboard with traffic lights; highlighted findings |
| **Geographic Intelligence** | Hub mapping; zone-skip quantification; Select eligibility % |
| **Actionable Next Steps** | Recommendations sheet with pilot plan and timeline |

---

## Enhanced Column Mapping

### Required Fields
```yaml
order_date: "Date column (Ship Date, Order Date, Label Created)"
weight_total: "TOTAL shipment weight (not per-item)"
  - CRITICAL: Verify this is total, not item weight
  - Check by comparing to item count
carrier: "Carrier column (or infer from tracking)"
service_level: "Service Selected column"
destination_state: "Ship To State"
destination_zip: "Ship To Postal Code (for zone calculation)"
zone: "Zone column (if available)"
shipping_cost: "Amount paid for shipping"
```

### Data Quality Checks (NEW)
```python
# Run these BEFORE analysis
quality_checks = {
    "weight_validation": "Compare Weight vs TotalOz columns",
    "date_range": "Verify date range matches expected period",
    "null_audit": "Count nulls per column, flag if >5%",
    "outlier_detection": "Flag weights >150 lbs, costs >$100",
    "zone_validation": "Verify zones 1-8 only, no blanks"
}
```

---

## Enhanced Output Structure (9 Sheets)

### Sheet 1: Executive Dashboard (NEW FORMAT)

```markdown
## SHIPPING PROFILE: [Company Name]

**Analysis Date**: [Date]
**Data Period**: [Start] to [End] ([X] days)
**Data Quality Score**: [A/B/C] - [Notes on any issues]

---

### Traffic Light Summary

| Metric | Value | Status | Insight |
|--------|-------|--------|---------|
| Daily Volume | 197 | GREEN | Meets FirstMile 100+/day threshold |
| Avg Weight | 1.28 lbs | GREEN | Sweet spot for Xparcel Ground |
| Cross-Country % | 56.4% | YELLOW | Zone-skip opportunity via Select |
| Carrier Diversity | 3 carriers | GREEN | Not locked into single carrier |

---

### Key Findings (Top 3)

1. **Volume Fit**: 6,000/month exceeds FirstMile minimum; qualifies for volume pricing
2. **Weight Profile**: 99% under 5 lbs = Xparcel Ground/Expedited candidate
3. **Zone Opportunity**: 56% zones 5-8 = significant zone-skip savings potential

---

### Data Confidence Levels

| Field | Status | Notes |
|-------|--------|-------|
| Volume | CONFIRMED | Full 31-day sample |
| Weight | CONFIRMED | Used TotalOz (verified vs WeightOz) |
| Carrier | CONFIRMED | Explicit in data |
| Zone | CONFIRMED | Populated for 100% of records |
| Cost | CONFIRMED | Shipping cost column present |
| Origin | INFERRED | Store name used as proxy |
```

### Sheet 2-7: (Same as v2.0 but with Key Insight boxes)

Each distribution sheet adds:
```markdown
### KEY INSIGHT
[One sentence explaining what this data means for FirstMile fit]
[One sentence on action implication]
```

### Sheet 8: FirstMile Opportunity Assessment (NEW)

```markdown
## FIRSTMILE OPPORTUNITY: [Company Name]

### Network Allocation

| Network | Eligibility | Volume | % | Notes |
|---------|-------------|--------|---|-------|
| Select (Metro Hubs) | Zones 1-4 + major metros | X,XXX | XX% | Zone-skip advantage |
| National (All ZIPs) | Remaining volume | X,XXX | XX% | Full coverage |

### Xparcel Service Mapping

| Current Service | Volume | Recommended Xparcel | Rationale |
|-----------------|--------|---------------------|-----------|
| USPS First Class | 2,636 | Xparcel Ground | Sub-1lb, 3-8 day acceptable |
| UPS Ground Saver | 1,638 | Xparcel Expedited | 1-5 lb, faster transit needed |
| USPS Priority | 991 | Xparcel Ground | Cost optimization |

### Savings Estimate

| Scenario | Assumption | Annual Savings | % Reduction |
|----------|------------|----------------|-------------|
| Conservative | 10% rate improvement | $XX,XXX | 10% |
| Moderate | 15% rate improvement | $XX,XXX | 15% |
| Aggressive | 20% + zone-skip | $XX,XXX | 20% |

**Methodology**: Current avg cost ($6.86) × volume × rate improvement %

### Optimization Flags

| Flag | Count | % | Opportunity |
|------|-------|---|-------------|
| 15.99oz threshold | XXX | XX% | Move to 1-lb rate |
| Zone 8 premium | XXX | XX% | Consider regional fulfillment |
| Residential surcharge | XXX | XX% | Already priced; no change |
```

### Sheet 9: Recommendations & Next Steps (NEW)

```markdown
## RECOMMENDATIONS: [Company Name]

### Recommended Actions

| Priority | Action | Owner | Timeline | Expected Impact |
|----------|--------|-------|----------|-----------------|
| 1 | Run 500-shipment pilot on Xparcel Ground | FirstMile + Customer | Week 1-2 | Validate transit times |
| 2 | Compare pilot costs to current USPS | Customer | Week 3 | Confirm savings |
| 3 | Phase 1 rollout: Sub-1lb volume | Both | Week 4+ | Capture quick wins |
| 4 | Phase 2: Evaluate Xparcel Expedited for UPS volume | Both | Month 2 | Additional savings |

### Pilot Plan

**Scope**: 500 shipments over 2 weeks
**Service**: Xparcel Ground
**Target Volume**: Sub-1lb, Zones 5-8 (highest savings potential)
**Success Criteria**:
- Transit ≤8 days for 90%+
- Cost ≤$5.50 avg (vs current $6.86)
- Claims rate <1%

### Questions to Resolve

- [ ] Contract status with current carriers (penalties?)
- [ ] Peak season volume expectations
- [ ] Integration requirements (API vs manual)
- [ ] Decision-maker for carrier changes
```

---

## Process Improvements

### Pre-Analysis Checklist
- [ ] Identify correct weight column (Total vs Item weight)
- [ ] Verify date column and format
- [ ] Check for tracking numbers (carrier inference)
- [ ] Confirm origin vs destination fields
- [ ] Note any data quality issues

### Post-Analysis Checklist
- [ ] All confidence levels documented
- [ ] Key Insight added to each section
- [ ] Savings calculated with methodology shown
- [ ] Recommendations include timeline
- [ ] Pilot plan is specific and actionable

---

## Tool Selection Guide

| Data Source | Best Tool | Notes |
|-------------|-----------|-------|
| ShipStation export | Python + pandas | Handle large files |
| FreightClub export | Python + pandas | Similar structure |
| Small sample (<1000) | Excel formulas | Quick analysis |
| Customer PLD | Python | May need column mapping |

### MCP Tools Used
- **BrightData**: Web scraping for carrier rate benchmarks
- **Perplexity**: Current carrier pricing research
- **Context7**: pandas/openpyxl documentation

---

## Anti-Patterns

```
NEVER:
- Present weight without verifying Total vs Item
- Skip data quality audit
- Show distributions without "so what?" insight
- Omit savings estimate (even rough)
- End without recommendations
- Use generic FirstMile pitch (customize to data)

ALWAYS:
- Verify weight column is total shipment weight
- Flag data quality issues upfront
- Connect every metric to FirstMile opportunity
- Show savings methodology (not just number)
- Include specific pilot plan
- Document confidence levels
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v3.0 | Dec 2025 | Rubric integration, FirstMile opportunity sheet, recommendations |
| v2.0 | Dec 2025 | Carrier inference, enhanced service level sheet |
| v1.0 | Dec 2025 | Initial 7-sheet structure |

---

*Skill Version: 3.0*
*Framework: Revenue Architect Practice Gym Rubric 1*
*Last Updated: December 2025*
