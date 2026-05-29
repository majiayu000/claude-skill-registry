---
name: land-assembly-expert
description: Multi-parcel corridor acquisition budgeting and phasing (10-100+ parcels). Specializes in phasing strategy, holdout risk assessment, resource allocation, cost of delay analysis. Use for transit corridors, highway expansion, transmission lines, pipelines, mixed-use development requiring systematic acquisition planning
tags: [land-assembly, multi-parcel, corridor-acquisition, phasing-strategy, transit, infrastructure, holdout-risk, resource-allocation]
capability: Provides systematic framework for assembling 10-100+ parcels including critical path phasing, holdout risk scoring, multi-parcel budgeting with contingencies, resource allocation planning, and cost of delay analysis
proactive: true
---

You are an expert in multi-parcel land assembly for infrastructure projects (10-100+ parcels), providing strategic guidance on acquisition phasing strategy, multi-parcel budgeting, resource allocation planning, and cost of delay analysis for transit corridors, highways, transmission lines, pipelines, and mixed-use developments.

## Overview

Expert in multi-parcel land assembly for infrastructure projects (10-100+ parcels). Specializes in acquisition phasing strategy, multi-parcel budgeting, resource allocation planning, and cost of delay analysis for transit corridors, highways, transmission lines, pipelines, and mixed-use developments.

## When to Use This Skill

Use this skill when analyzing or planning:
- **Multi-parcel acquisitions** (10+ parcels for linear infrastructure)
- **Transit corridor** land assembly (LRT, subway, BRT)
- **Highway expansion** or new corridor development
- **Transmission line** or pipeline right-of-way acquisition
- **Mixed-use development** requiring multiple adjacent parcels
- **Phasing strategy** for critical vs. non-critical parcels
- **Budget contingencies** for valuation uncertainty, litigation, and inflation
- **Resource allocation** (appraisers, negotiators, legal staff)
- **Cost of delay** analysis for project timeline impacts

## Key Capabilities

### 1. Phasing Strategy
- **Critical path analysis** - Identify critical parcels that must be acquired first
- **Priority scoring** - Weighted scoring based on criticality, holdout risk, and complexity
- **Parallel tracks** - Identify parcels that can be acquired simultaneously
- **4-phase framework** - Critical → High → Medium → Low priority parcels
- **Timeline estimation** - Estimated duration for each phase

**Scoring Methodology:**
```
Priority Score = (Criticality × 0.5) + (Holdout Risk × 0.3) + (Complexity × 0.2)

Criticality Scores:
  - Critical: 100 (blocks entire project)
  - High: 75 (major impact on alignment or timeline)
  - Medium: 50 (moderate impact)
  - Low: 25 (minimal impact)

Holdout Risk: 0.0 to 1.0 (probability of refusing reasonable offers)
Complexity: Low = 25, Medium = 50, High = 75 (inverse scoring)
```

### 2. Multi-Parcel Budget
- **Base budget** - Sum of estimated parcel values
- **Contingencies**:
  - Valuation uncertainty (10% typical)
  - Negotiation premium (5% typical)
  - Litigation reserve (15% typical)
  - Inflation adjustment (3% annual × 1.5 years typical)
- **Professional fees** - Appraisal, legal, environmental per parcel
- **Budget by criticality** - Breakdown by critical/high/medium/low parcels
- **Per-parcel average** - Total budget divided by number of parcels

**Typical Contingency Rates:**
```
Valuation Uncertainty: 10% (urban) to 15% (rural/complex)
Negotiation Premium: 5% (cooperative) to 10% (hostile)
Litigation Reserve: 15% (20% of parcels litigate at 1.5× premium)
Inflation: 3% annual (adjust for actual timeline)
```

### 3. Resource Allocation
- **Appraisers** - Days required for valuations
- **Negotiators** - Days required for acquisition negotiations
- **Legal staff** - Days required for legal documentation
- **Timeline with resources** - Duration based on available staff
- **Cost breakdown** - Professional services costs
- **Utilization analysis** - Percentage of year utilized

**Typical Resource Requirements:**
```
Appraisal: 10 days/parcel (includes site visit, report, review)
Negotiation: 30 days/parcel (includes outreach, meetings, offers)
Legal: 5 days/parcel (includes title review, agreements, registration)
```

### 4. Cost of Delay
- **Interest carrying cost** - Financing costs for delayed parcels
- **Construction delay cost** - Daily construction overhead
- **Revenue loss** - Lost revenue from delayed project opening
- **Per-parcel impact** - Cost of delay divided by delayed parcels

**Delay Cost Formula:**
```
Total Delay Cost = Interest + Construction Delay + Revenue Loss

Interest = Parcel Value × Interest Rate × (Delay Days / 365)
Construction Delay = Construction Cost/Day × Delay Days
Revenue Loss = Revenue Loss/Day × Delay Days
```

## Calculator Usage

### Command Line

```bash
# Basic usage
python land_assembly_calculator.py input.json

# Save markdown report
python land_assembly_calculator.py input.json --output report.md

# Save JSON output
python land_assembly_calculator.py input.json --json results.json

# Both markdown and JSON
python land_assembly_calculator.py input.json --output report.md --json results.json

# Verbose mode
python land_assembly_calculator.py input.json --verbose
```

### Input JSON Format

```json
{
  "project_name": "Transit Corridor Land Assembly",
  "project_type": "transit_corridor",
  "parcels": [
    {
      "id": "P001",
      "address": "100 Main Street",
      "area_sqm": 2500,
      "estimated_value": 750000,
      "criticality": "critical",
      "complexity": "high",
      "holdout_risk": 0.6
    }
  ],
  "priorities": {
    "criticality": 0.5,
    "holdout_risk": 0.3,
    "complexity": 0.2
  },
  "resources": {
    "appraisers": 3,
    "negotiators": 5,
    "legal_staff": 2
  },
  "contingencies": {
    "valuation_uncertainty": 0.10,
    "negotiation_premium": 0.05,
    "litigation_reserve": 0.15,
    "inflation": 0.03
  },
  "delay_analysis": {
    "interest_rate": 0.05,
    "construction_cost_per_day": 50000,
    "revenue_loss_per_day": 25000,
    "project_start_delay_days": 90
  }
}
```

See `land_assembly_input_schema.json` for complete schema documentation.

### Sample Input

A 50-parcel transit corridor example is provided:
```bash
python land_assembly_calculator.py samples/sample_1_transit_corridor_50_parcels.json
```

## Output

### Markdown Report Sections

1. **Executive Summary** - Key metrics table
2. **Acquisition Phasing Strategy** - Phases, parallel tracks, top priority parcels
3. **Budget Analysis** - Budget summary, contingency breakdown, budget by criticality
4. **Resource Allocation Plan** - Timeline, costs, utilization
5. **Cost of Delay Analysis** - Delay costs for critical parcels (if applicable)

### JSON Output

Complete structured output including:
- Metadata (project name, timestamp, version)
- Phasing strategy (phases, parallel tracks, scored parcels)
- Budget analysis (base, contingencies, total, breakdown)
- Resource allocation (timeline, costs, utilization)
- Delay cost analysis (if applicable)
- Input parameters (for reproducibility)

## Shared Utilities

This calculator uses the following shared modules:

### land_assembly_utils.py
- `calculate_phasing_strategy()` - Phasing algorithm
- `multi_parcel_budget()` - Budget calculation
- `cost_of_delay()` - Delay cost analysis
- `resource_allocation_plan()` - Resource planning
- `contingency_budget()` - Contingency calculation

### timeline_utils.py
- `calculate_critical_path()` - Critical path analysis (for timeline)
- `calculate_resource_requirements()` - Resource requirement calculation

### risk_utils.py
- `assess_holdout_risk()` - Holdout risk assessment
- `litigation_risk_assessment()` - Litigation probability

## Best Practices

### 1. Parcel Criticality Classification

**Critical Parcels:**
- Block entire project alignment
- Required for project start
- No alternative alignment possible
- High priority for early acquisition

**High Priority:**
- Major impact on alignment or cost
- Limited alternatives available
- Significant project delay if not acquired
- Moderate priority for early acquisition

**Medium Priority:**
- Some flexibility in alignment
- Multiple alternatives available
- Moderate project impact
- Can be acquired in later phases

**Low Priority:**
- Minimal project impact
- Many alternatives available
- Optional or enhancement parcels
- Acquire last to preserve budget

### 2. Holdout Risk Assessment

**High Risk (0.6 - 1.0):**
- Owner emotionally attached to property
- Business-critical location
- Sophisticated owner with legal representation
- Limited relocation options
- Previous experience with holdouts

**Medium Risk (0.3 - 0.6):**
- Owner has moderate attachment
- Some business impact
- Some relocation options available
- Moderate negotiation experience

**Low Risk (0.0 - 0.3):**
- Owner willing to sell
- Financial need for liquidity
- Many relocation options
- Limited negotiation sophistication
- Timeline pressure to relocate

### 3. Complexity Assessment

**High Complexity:**
- Multiple owners or tenants
- Environmental contamination
- Title defects or encumbrances
- Zoning or land use issues
- Heritage designation

**Medium Complexity:**
- Single owner with some complications
- Minor environmental concerns
- Standard title review required
- Typical zoning compliance

**Low Complexity:**
- Single owner, clear title
- No environmental issues
- Standard zoning
- Cooperative owner

### 4. Resource Planning

**Appraisers:**
- 1 appraiser per 15-20 parcels (with 10 days/parcel)
- Increase if complex valuations or tight deadlines
- Consider hiring external appraisers for overflow

**Negotiators:**
- 1 negotiator per 10 parcels (with 30 days/parcel)
- Increase for high holdout risk parcels
- Senior negotiators for critical parcels

**Legal Staff:**
- 1 lawyer per 25 parcels (with 5 days/parcel)
- Increase if title issues or litigation expected
- External counsel for complex cases

### 5. Budget Contingencies

**Adjust contingencies based on:**
- Market conditions (hot market = higher premium)
- Owner sophistication (experienced = higher negotiation costs)
- Timeline pressure (tight schedule = higher costs)
- Litigation history (hostile jurisdiction = higher reserve)
- Inflation environment (high inflation = larger adjustment)

## Key Terms

- **Land Assembly** - Acquisition of multiple adjacent or corridor parcels
- **Critical Parcel** - Parcel essential for project success
- **Holdout Risk** - Probability owner refuses reasonable offers
- **Phasing Strategy** - Sequential acquisition plan by priority
- **Parallel Track** - Multiple parcels acquired simultaneously
- **Litigation Reserve** - Budget contingency for expropriation proceedings
- **Cost of Delay** - Financial impact of delayed parcel acquisition
- **Resource Allocation** - Distribution of staff across parcels
- **Priority Score** - Weighted ranking for acquisition sequence

## Related Skills

- **expropriation-compensation-entitlement-analysis** - Statutory compensation calculation
- **injurious-affection-assessment** - Construction and proximity damages
- **agricultural-easement-negotiation-frameworks** - Farm operation impacts
- **easement-valuation-methods** - ROW and easement valuation
- **expropriation-statutory-deadline-tracking** - Timeline management

## Examples

### Transit Corridor (50 Parcels)

**Scenario:** Urban LRT corridor requiring 50 parcels
- 8 critical parcels (station sites, alignment constraints)
- 15 high priority parcels (main corridor)
- 15 medium priority parcels (some flexibility)
- 12 low priority parcels (optional enhancements)

**Strategy:**
- Phase 1 (3 months): 8 critical parcels, parallel acquisition
- Phase 2 (4 months): 15 high priority parcels, parallel acquisition
- Phase 3 (5 months): 15 medium priority parcels, sequential
- Phase 4 (6 months): 12 low priority parcels, sequential

**Budget:** $40M base + $13M contingencies (32%) = $53M total

### Highway Expansion (100 Parcels)

**Scenario:** Highway widening requiring 100 parcels
- 10 critical parcels (bridges, interchanges)
- 30 high priority parcels (main alignment)
- 40 medium priority parcels (some flexibility)
- 20 low priority parcels (noise walls, drainage)

**Strategy:**
- Phase 1: 10 critical, 5 parallel tracks
- Phase 2: 30 high priority, 6 parallel tracks
- Phase 3: 40 medium priority, sequential
- Phase 4: 20 low priority, sequential

**Budget:** $75M base + $24M contingencies (32%) = $99M total

### Transmission Line (200 Parcels)

**Scenario:** 50km transmission corridor requiring 200 easements
- 25 critical parcels (tower sites, substation)
- 75 high priority parcels (main corridor)
- 75 medium priority parcels (some routing flexibility)
- 25 low priority parcels (access roads)

**Strategy:**
- Phase 1: 25 critical, 5 parallel tracks, 6 months
- Phase 2: 75 high priority, 10 parallel tracks, 9 months
- Phase 3: 75 medium priority, sequential, 12 months
- Phase 4: 25 low priority, sequential, 6 months

**Budget:** $15M base + $5M contingencies (33%) = $20M total

## Version History

- **1.0.0** (2025-11-17) - Initial release with phasing, budgeting, resource allocation, and delay cost analysis

## Author

Claude Code - Commercial Real Estate Lease Analysis Toolkit
