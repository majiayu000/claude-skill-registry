---
name: skills-walkervvv-firstmile-deals-pipe
description: 'Purpose: Generate shipping profile analyses, rate comparisons, and FirstMile
  performance reports.'
---

# Analysis Agent Skill

**Purpose**: Generate shipping profile analyses, rate comparisons, and FirstMile performance reports.

## Core Reference
→ **See [rules.md](../../rules.md) → Agent-Specific Rules → Analysis Agent**
→ **See [~/.claude/FIRSTMILE.md](~/.claude/FIRSTMILE.md) → Complete FirstMile analysis framework**

## Execution Workflow

### Phase 1: Data Validation (First 5 minutes)
1. Load PLD (Parcel Level Detail) file from customer deal folder
2. Validate required columns: Carrier, Service, Weight, Zone, Destination State, Cost, Date
3. Check data quality: missing values, outliers, date ranges
4. Generate data quality report if issues found

### Phase 2: Comprehensive Analysis (10-15 minutes)
Execute in this order:
1. **Volume Profile**: Total shipments, daily average, marketplace mix
2. **Carrier Mix**: Volume/spend by carrier with percentages
3. **Service Level Distribution**: Services used with costs
4. **Expanded Weight Distribution**: Critical billable weight thresholds
5. **Dimensional Analysis**: Average dims, cubic volume (</>1 cu ft)
6. **Zone Distribution**: Individual zones 1-8, Regional vs Cross-Country
7. **Geographic Distribution**: Top 10 destination states
8. **Cost Analysis**: Total spend, avg/median costs per parcel
9. **Billable Weight Impact**: Actual vs billable weight comparison

### Phase 3: FirstMile Opportunity Identification (5-10 minutes)
1. Map volumes to Xparcel service levels (Ground, Expedited, Priority)
2. Identify National vs Select network allocation
3. Calculate potential savings by service level
4. Flag optimization opportunities (e.g., packages at billable weight thresholds)

### Phase 4: Report Generation (5-10 minutes)
**Choose format based on need**:
- **Quick Analysis**: Markdown summary with tables
- **Executive Summary**: One-page PDF with key metrics
- **Comprehensive Report**: 9-tab Excel with full analysis

## Analysis Components (Execute in Order)

### 1. Volume Profile
```python
import pandas as pd

def volume_profile(df):
    total_shipments = len(df)
    date_range = (df['Date'].min(), df['Date'].max())
    days_in_range = (date_range[1] - date_range[0]).days
    daily_average = total_shipments / days_in_range

    # Marketplace mix (if available)
    marketplace_dist = df['Marketplace'].value_counts(normalize=True) if 'Marketplace' in df.columns else None

    return {
        'total_shipments': total_shipments,
        'date_range': date_range,
        'daily_average': daily_average,
        'marketplace_distribution': marketplace_dist
    }
```

**Output Format**:
```markdown
## Volume Profile
- **Total Shipments**: {count:,} parcels
- **Date Range**: {start_date} to {end_date} ({days} days)
- **Daily Average**: {avg:,} parcels/day
- **Marketplace Mix**: Amazon ({pct}%), Shopify ({pct}%), Other ({pct}%)
```

### 2. Carrier Mix
```python
def carrier_mix(df):
    carrier_volume = df['Carrier'].value_counts()
    carrier_spend = df.groupby('Carrier')['Cost'].sum()
    carrier_summary = pd.DataFrame({
        'Volume': carrier_volume,
        'Volume %': (carrier_volume / len(df) * 100).round(1),
        'Spend': carrier_spend,
        'Spend %': (carrier_spend / carrier_spend.sum() * 100).round(1)
    })
    return carrier_summary.sort_values('Spend', ascending=False)
```

**Output Format**:
```markdown
## Carrier Mix
| Carrier | Volume | Volume % | Spend | Spend % |
|---------|--------|----------|-------|---------|
| [Name]  | X,XXX  | XX.X%    | $X,XXX| XX.X%   |
```

### 3. Expanded Weight Distribution
**CRITICAL**: This analysis identifies billable weight optimization opportunities.

```python
def expanded_weight_distribution(df):
    # Under 1 lb (critical thresholds)
    bins_under_1lb = [0, 0.25, 0.5, 0.75, 0.9375, 0.99, 1.0]  # 0-4oz, 5-8oz, 9-12oz, 13-15oz, 15.99oz, 16oz
    labels_under_1lb = ['0-4oz', '5-8oz', '9-12oz', '13-15oz', '15.99oz', '16oz (1lb)']

    # 1-5 lbs by billable pound
    bins_1_5lb = [1.0, 2.0, 3.0, 4.0, 5.0]
    labels_1_5lb = ['1-2lb', '2-3lb', '3-4lb', '4-5lb']

    # Over 5 lbs
    bins_over_5lb = [5.0, 10.0, 20.0, 50.0, float('inf')]
    labels_over_5lb = ['5-10lb', '10-20lb', '20-50lb', '50+lb']

    # Categorize and analyze
    under_1lb = df[df['Weight'] < 1.0]
    between_1_5lb = df[(df['Weight'] >= 1.0) & (df['Weight'] <= 5.0)]
    over_5lb = df[df['Weight'] > 5.0]

    return {
        'under_1lb_dist': pd.cut(under_1lb['Weight'], bins=bins_under_1lb, labels=labels_under_1lb).value_counts(),
        '1_5lb_dist': pd.cut(between_1_5lb['Weight'], bins=bins_1_5lb, labels=labels_1_5lb).value_counts(),
        'over_5lb_dist': pd.cut(over_5lb['Weight'], bins=bins_over_5lb, labels=labels_over_5lb).value_counts()
    }
```

**Key Thresholds to Flag**:
- **15.99 oz**: Maximum before jumping to 2 lbs billable (packages just over this are optimization targets)
- **32 oz**: Maximum before jumping to 3 lbs billable
- **48 oz**: Maximum before jumping to 4 lbs billable

**Output Format**:
```markdown
## Weight Distribution

### Under 1 lb (Critical Optimization Zone)
| Range | Count | % of Total | Spend | Avg Cost |
|-------|-------|------------|-------|----------|
| 0-4oz | X,XXX | XX.X% | $X,XXX | $X.XX |
| 15.99oz | XXX ⚠️ | X.X% | $XXX | $X.XX |

**Optimization Opportunity**: XXX packages at 15.99oz+ (consider packaging reduction to stay under 16oz threshold)
```

### 4. Zone Distribution
```python
def zone_distribution(df):
    zone_summary = df.groupby('Zone').agg({
        'Zone': 'count',  # Volume
        'Cost': ['sum', 'mean'],
        'Transit_Days': 'mean'  # If available
    }).round(2)

    # Regional (1-4) vs Cross-Country (5-8)
    regional = df[df['Zone'].isin([1, 2, 3, 4])]
    cross_country = df[df['Zone'].isin([5, 6, 7, 8])]

    return {
        'zone_detail': zone_summary,
        'regional_pct': len(regional) / len(df) * 100,
        'cross_country_pct': len(cross_country) / len(df) * 100
    }
```

**Output Format**:
```markdown
## Zone Distribution
| Zone | Volume | % | Avg Cost | Avg Transit |
|------|--------|---|----------|-------------|
| 1-2  | X,XXX  | XX%| $X.XX    | X.X days    |

**Regional (Zones 1-4)**: XX.X% | **Cross-Country (Zones 5-8)**: XX.X%

**FirstMile Recommendation**:
- Regional shipments → National Network + Xparcel Ground
- Cross-Country <1lb → Select Network + Xparcel Ground (zone-skipping)
```

### 5. Geographic Distribution with Hub Mapping
```python
# Hub mapping from rules.md
HUB_MAP = {
    "CA": "LAX - West Coast",
    "TX": "DFW - South Central",
    "FL": "MIA - Southeast",
    "NY": "JFK/EWR - Northeast",
    "IL": "ORD - Midwest",
    "GA": "ATL - Southeast",
    "WA": "SEA - Pacific Northwest",
    "PA": "PHL - Mid-Atlantic",
    "AZ": "PHX - Southwest",
    "CO": "DEN - Mountain West"
}

def geographic_distribution(df):
    state_summary = df.groupby('Destination_State').agg({
        'Destination_State': 'count',
        'Cost': 'sum'
    }).sort_values('Destination_State', ascending=False).head(15)

    # Map to FirstMile hubs
    state_summary['Hub'] = state_summary.index.map(lambda x: HUB_MAP.get(x, "National Network"))

    return state_summary
```

**Output Format**:
```markdown
## Top 15 Destination States
| State | Volume | % | Hub Assignment |
|-------|--------|---|----------------|
| CA    | X,XXX  | XX%| LAX - West Coast |
| TX    | X,XXX  | XX%| DFW - South Central |

**Select Network Coverage**: XX.X% (major metro hubs)
**National Network**: XX.X% (all other ZIPs)
```

## FirstMile Analysis Framework Compliance

**MANDATORY**: All reports MUST follow `~/.claude/FIRSTMILE.md` standards.

### ✅ REQUIRED Elements
1. **Lead with SLA Compliance** (if performance report)
2. **Use Xparcel service terminology** (Ground 3-8d, Expedited 2-5d, Priority 1-3d)
3. **Network terminology**: "National" or "Select" (NEVER name UPS, FedEx, USPS)
4. **Spell "eCommerce"** with camel-case 'C'
5. **FirstMile blue headers** in Excel (#366092)
6. **Hub mapping** for top destination states

### ❌ PROHIBITED
- Leading with daily delivery percentages
- Naming specific carriers in reports
- Presenting Xparcel as separate company (it's a ship-method under FirstMile)
- Skipping zone distribution analysis
- Missing geographic hub mapping

## Excel Report Generation (9-Tab Structure)

**When to generate**: Customer requests comprehensive report, executive summary, or QBR deck.

**Required Tabs** (in order):
1. **Executive Summary** - High-level KPIs in two-column table
2. **SLA Compliance** - Delivered-only metrics with color scale
3. **Transit Performance** - Daily distribution (0-7, 8+) with statistics
4. **Geographic Distribution** - Top 15 states with hub assignments
5. **Zone Analysis** - Zones 1-8 with Regional vs Cross-Country summary
6. **Operational Metrics** - Volume metrics and optimization opportunities
7. **In-Transit Detail** - Ships not delivered with SLA window status
8. **Notes & Assumptions** - Business rules and definitions
9. **Brand Style Guide** - Color swatches with HEX/RGB/CMYK values

**Styling Requirements**:
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# FirstMile brand colors
FIRSTMILE_BLUE = "366092"
LIGHT_GRAY = "DDDDDD"

# Header styling
header_fill = PatternFill(start_color=FIRSTMILE_BLUE, end_color=FIRSTMILE_BLUE, fill_type="solid")
header_font = Font(color="FFFFFF", bold=True, size=12)
header_alignment = Alignment(horizontal="center", vertical="center")

# Apply to all table headers
for cell in worksheet['A1:Z1']:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = header_alignment
```

**Filename Format**: `FirstMile_Xparcel_Performance_{Customer}_{YYYYMMDD_HHMM}.xlsx`

## Strict Compliance Rules

### ✅ MUST DO
- Follow FIRSTMILE.md analysis framework exactly
- Lead ALL reports with SLA compliance metrics (if performance data)
- Use billable weight rules (round up to next oz/lb)
- Apply FirstMile blue (#366092) to Excel headers
- Include geographic distribution with hub mapping
- Map volumes to Xparcel service levels
- Identify National vs Select network allocation
- Calculate optimization opportunities

### ❌ NEVER DO
- Present daily delivery % as primary metric
- Name specific carriers (UPS, FedEx, USPS) in reports
- Present Xparcel as separate company
- Skip zone distribution analysis
- Skip geographic hub mapping
- Use non-FirstMile terminology
- Violate brand color standards

## Quality Gates

Before marking analysis complete:
- [ ] All 9 analysis components executed in order
- [ ] FirstMile framework compliance validated
- [ ] SLA compliance metrics leading report (if applicable)
- [ ] Xparcel service terminology used correctly
- [ ] Network terminology (National/Select) applied
- [ ] Hub mapping included for top states
- [ ] Optimization opportunities identified
- [ ] Output saved in customer deal folder
- [ ] Excel styling meets brand standards (if Excel generated)

## Performance Metrics

**Target Benchmarks**:
- Analysis completion: <30 minutes for comprehensive report
- Data quality validation: <5 minutes
- Excel generation: <10 minutes
- Accuracy: >95% match with source data

**Monthly Review**:
- Report quality: Customer feedback on clarity and insights
- Accuracy: Corrections needed post-delivery
- Optimization impact: Savings realized from recommendations

## Error Handling

**Missing Data**:
- Document missing columns in data quality report
- Estimate missing values if possible (note assumptions)
- Flag incomplete analysis sections

**Data Quality Issues**:
- Outliers: Flag parcels with unusual weight/cost combinations
- Duplicates: Identify and handle duplicate tracking numbers
- Invalid values: Negative weights, zero costs, missing zones

**Excel Generation Failures**:
- Fall back to markdown summary if Excel library fails
- Save partial Excel with error notes
- Alert user to incomplete report

## Related Documentation

- [rules.md](../../rules.md) - Complete agent rules and Excel standards
- [~/.claude/FIRSTMILE.md](~/.claude/FIRSTMILE.md) - FirstMile brand framework
- [.claude/docs/templates/EXCEL_PROCESS_TEMPLATES.md](../docs/templates/EXCEL_PROCESS_TEMPLATES.md) - Excel templates
