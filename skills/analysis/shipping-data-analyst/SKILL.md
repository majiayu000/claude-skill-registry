---
name: shipping-data-analyst
description: |
  Shipping Data Analyst Expert - Rate Preparation Intelligence v5.0
  Purpose: Analyze prospect shipping data to UNDERSTAND their operations BEFORE creating Xparcel rates.
  Mental Model: This is DISCOVERY, not selling. Learn their world before proposing solutions.
  Triggers on: "shipping analysis", "PLD analysis", "rate prep", "shipping data", "freightclub",
               "shipstation export", "analyze shipping", "weight distribution", "zone analysis"
  Use when: Customer provides shipping data export and you need to understand their profile for rate creation.
---

# Shipping Data Analyst Expert

> *"Understand their world before proposing solutions."*

## Quick Reference

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| Rate Prep Intelligence | Data extraction for rate team | Every new prospect with shipping data |
| Column Mapping | Identify data fields | Before any analysis |
| Data Quality Audit | Validate data reliability | First step of every analysis |
| Weight Band Analysis | Rate card tier pricing | Core deliverable |
| Zone Analysis | Zone-based pricing | Core deliverable |
| DIM Exposure | Billable weight adjustments | When dimensions available |

## Core Philosophy

**"Discovery Before Solutions"** - This analysis happens BEFORE rates exist. No savings estimates, no recommendations, no sales pitch. Just clean data for the rate team.

**"Red Pill Mode"** - Internal analysis, not customer-facing. Organized for rate team consumption.

## Decision Rules Summary

### Data Source Selection
```
IF file extension = .csv AND columns match ShipStation → Use ShipStation mapping
IF file extension = .xlsx AND "FreightClub" in filename → Use FreightClub mapping
IF columns unclear → Ask user for column mapping before proceeding
```

### Weight Column Selection (CRITICAL)
```
IF "TotalOz" column exists → USE THIS (total shipment weight)
IF only "WeightOz" exists → VERIFY with user (may be per-item weight)
IF 100% under 1lb → STOP - likely using wrong weight column
```

### Analysis Depth Selection
```
IF Zone column populated >95% → Include full zone analysis
IF Zone column <50% populated → Note "Zone data incomplete" in quality sheet
IF L/W/H all present → Include DIM exposure analysis
IF L/W/H missing or <10% → Skip DIM exposure sheet
```

### Output Selection
```
ALWAYS: Profile Summary, Weight Distribution, Current Carrier Mix, Data Quality
IF Zone data: Zone Distribution sheet
IF Destination data: Destination Footprint sheet
IF Dimension data: DIM Exposure sheet
IF >2 weeks data: Operational Patterns sheet
```

## Reference Files

| File | Load When | Contents |
|------|-----------|----------|
| `00-decision-rules.md` | Always | IF-THEN rules for analysis decisions |
| `01-column-mappings.md` | Data loading | ShipStation, FreightClub, PLD mappings |
| `02-weight-bands.md` | Weight analysis | Xparcel rate card tier structure |
| `03-data-quality-checks.md` | Validation | Quality audit procedures |
| `04-python-template.py` | Execution | Analysis script template |

## Workflow

### Step 1: Identify Data Source
```
1. Check file type (CSV, XLSX, XLS)
2. Scan column headers
3. Match to known export format (ShipStation, FreightClub, custom)
4. If unknown → Ask user for column mapping
```

### Step 2: Validate Weight Column
```
1. Find weight column (TotalOz preferred over WeightOz)
2. Check distribution - if 100% under 1lb, STOP and verify
3. Compare TotalOz vs WeightOz if both exist
4. Document which column used in Data Quality sheet
```

### Step 3: Run Analysis
```
1. Load data with proper column mapping
2. Apply address normalization
3. Calculate derived fields (bill weight, DIM weight)
4. Generate all applicable sheets
5. Create console summary for rate team
```

### Step 4: Handoff to Rate Team
```
Rate Prep Summary:
- Volume profile (shipments/month, daily avg)
- Weight profile (under 1lb %, 1-5lb %, over 5lb %)
- Zone profile (regional vs cross-country split)
- DIM exposure (if applicable)
- Data quality confidence level
```

## Column Mappings

### ShipStation Exports
```yaml
order_date: "Date - Shipped Date"
weight_oz: "Weight - TotalOz"      # CRITICAL: NOT "Weight - WeightOz"
origin: "Market - Store Name"
service_level: "Carrier - Service Selected"
carrier: "Carrier - Carrier Selected"
dest_state: "Ship To - State"
dest_zip: "Ship To - Postal Code"
zone: "Ship To - Zone"
length: "Dimensions - Length"
width: "Dimensions - Width"
height: "Dimensions - Height"
```

### FreightClub Exports
```yaml
order_date: "Ship Date" or "Label Created"
weight: varies - check if oz or lbs
origin: "Ship From" or "Warehouse"
service_level: "Service Selected"
carrier: "Carrier" or infer from tracking
```

## Weight Bands (Xparcel Rate Card Alignment)

```
1-4 oz      → First tier
5-8 oz      → Second tier
9-12 oz     → Third tier
13-15.99 oz → Fourth tier (just under 1lb threshold)
1 lb        → One pound tier
1-2 lbs     → Pound tiers begin
2-3 lbs
3-4 lbs
4-5 lbs
5-10 lbs    → Heavier tiers
10-15 lbs
15-20 lbs
20+ lbs     → Heavy parcel
```

## Key Thresholds for Rate Team

| Threshold | Why It Matters |
|-----------|---------------|
| Under 1 lb | Xparcel Ground sweet spot |
| 1-5 lbs | Core Xparcel Ground/Expedited range |
| Over 5 lbs | May need service level mix |
| Regional (Z1-4) | Select network eligibility |
| Cross-Country (Z5-8) | National network |
| DIM Exposed % | Affects billable weight pricing |

## Data Quality Standards

| Field | High (>95%) | Medium (80-95%) | Low (<80%) |
|-------|-------------|-----------------|------------|
| Weight | Required | Review source | Cannot analyze |
| Zone | Full analysis | Note limitation | Skip zone sheet |
| Dimensions | DIM analysis | Partial DIM | Skip DIM sheet |
| Destination | Full footprint | Top states only | Limited value |

## Integration Points

### Source Skills (Reference, don't duplicate)
- `.claude/skills/excel-analysis/` - Excel file handling
- `.claude/skills/freightclub-analysis/` - Legacy v3.0 (sales-focused)

### Commands That Trigger This Expert
- `shipping analysis [file]` - Full rate prep analysis
- `PLD analysis` - Parcel Level Detail analysis
- `rate prep [company]` - Rate preparation workflow

### Downstream Skills (After Rates Created)
- `.claude/skills/discovery-sales-expert/` - For customer conversations
- `.claude/skills/cvm-white-glove-sales-process/` - For pipeline execution

## Anti-Patterns

```
NEVER (in Rate Prep phase):
- Estimate savings (no rates to compare yet)
- Make recommendations (premature)
- Use traffic lights (sales enablement tool)
- Add "Key Insight" editorial commentary
- Present directly to customer (internal use only)
- Use WeightOz without verifying it's total weight

ALWAYS:
- Verify weight column before analysis
- Note data quality issues prominently
- Organize output for rate team consumption
- Include data source documentation
- Keep output factual and clean
```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Weight Column Accuracy | 100% | Never use wrong weight column |
| Data Quality Documentation | 100% | Every analysis notes data issues |
| Rate Team Usability | High | Rate team can build rates without questions |
| Handoff Completeness | 100% | All required fields for rate card |

## Output Sheets (8 sheets)

1. **Profile Summary** - Volume, weight stats, origins, carriers
2. **Weight Distribution** - Bands aligned to Xparcel rate card
3. **Zone Distribution** - Zone breakdown, regional vs cross-country
4. **Destination Footprint** - Top states, ZIP3s, lanes
5. **DIM Exposure** - DIM weight analysis (if dims available)
6. **Current Carrier Mix** - What they use today (context)
7. **Operational Patterns** - Day-of-week, monthly trends
8. **Data Quality** - Confidence levels, data source notes

---

*Expert Version: 5.0*
*Mental Model: Discovery before solutions*
*Last Updated: December 2025*
