---
name: analyzing-cap-rates
description: Structures capitalization rate analysis with market comparison, risk premium decomposition, and trend assessment. Use when analyzing cap rates, comparing market yields, or assessing pricing trends.
tags:
  - analysis
  - real-estate-finance
  - risk
metadata:
  author: casemark
  practice_areas:
    - Real Estate Finance
    - REIT Analysis
    - Property Investment
  document_types:
    - Analysis Report
  skill_modes:
    - Analysis
---
# Analyzing Cap Rates

Structures capitalization rate analysis with market comparison, risk premium decomposition, and trend assessment.

## When To Use

- Evaluating acquisition pricing against market benchmarks for a specific property or portfolio
- Comparing yields across property types, geographies, or vintages
- Decomposing cap rate movements into risk-free rate, credit spread, and property risk premium components
- Assessing whether observed cap rate compression or expansion reflects fundamentals or market sentiment
- Supporting underwriting assumptions in investment committee memos or REIT portfolio reviews

## Inputs To Gather

- **Subject property NOI**: Trailing-12-month and forward-year stabilized NOI; confirm whether above-the-line or below-the-line capital reserves are deducted
- **Transaction price or appraised value**: Source and date; note whether price reflects gross or net of closing costs
- **Comparable transactions**: Minimum 3-5 comps with sale date, property type, location, size, occupancy, and confirmed cap rate
- **Risk-free rate benchmark**: Current 10-year Treasury yield as of analysis date [VERIFY current rate]
- **Market surveys**: CBRE, JLL, NCREIF, or RCA cap rate reports for the relevant property type and MSA [VERIFY data vintage]
- **Lease and occupancy profile**: WALT, credit quality of tenants, rollover schedule, and in-place vs. market rent spread
- **Property-specific risk factors**: Deferred capex, environmental issues, entitlement risk, single-tenant concentration

## Workflow

1. **Calculate the subject cap rate**
   - Going-in cap rate = Stabilized Year-1 NOI / Purchase Price
   - Terminal (exit/reversion) cap rate = Projected NOI at exit / Assumed sale price
   - If both are provided, confirm the implied spread between going-in and terminal rates (typically 25-75 bps expansion for standard hold periods)

2. **Build the comp set**
   - Select transactions closed within 12-18 months in the same MSA and property type
   - Adjust for material differences: occupancy (normalize to stabilized), lease structure (NNN vs. gross), and property quality (Class A/B/C)
   - Present comps in a table: address, sale date, price, SF/units, cap rate, occupancy, and key notes

3. **Decompose the cap rate into risk premium layers**
   - Risk-free rate (10Y Treasury)
   - General real estate risk premium (illiquidity, transaction cost, management burden — typically 150-300 bps over Treasuries for institutional-quality assets)
   - Property-type premium (e.g., office currently commands wider spreads than industrial) [VERIFY spread environment]
   - Location/market premium (primary vs. secondary vs. tertiary MSA)
   - Asset-specific premium (credit quality, lease term, physical condition, capex requirements)
   - Sum the build-up and compare to the observed cap rate; identify which component explains any divergence

4. **Assess cap rate trends**
   - Chart cap rate movement for the property type/MSA over 3-5 years using NCREIF, RCA, or survey data
   - Identify whether current pricing sits above, below, or at the historical mean
   - Separate rate-driven movement (changes in risk-free rate) from spread-driven movement (investor risk appetite)
   - Note supply pipeline and absorption trends that may pressure future cap rates [VERIFY local market data]

5. **Stress-test key assumptions**
   - Model cap rate sensitivity: show NOI value impact at +/- 25 bps and +/- 50 bps from base case
   - Test terminal cap rate assumptions against forward rate expectations
   - If vacancy or rent roll-down is material, show the impact on implied cap rate at stabilization vs. in-place

## Output

Structure the deliverable as follows:

- **Executive Summary**: Subject cap rate, position relative to comps and market averages, key risk factors, and pricing assessment (fairly priced / tight / wide)
- **Cap Rate Calculation**: Show NOI inputs, price, and resulting going-in and terminal cap rates with formulas
- **Comparable Transactions Table**: Minimum 3-5 comps with adjustment notes
- **Risk Premium Decomposition**: Build-up table from risk-free rate through asset-specific premium
- **Trend Analysis**: 3-5 year cap rate chart or table for property type/MSA with narrative on drivers
- **Sensitivity Matrix**: Value impact grid at varying cap rate and NOI scenarios
- **Limitations & Caveats**: Data gaps, stale comps, or assumption dependencies

## Quality Checks

- Confirm NOI definition is consistent across subject and comps (same treatment of reserves, TI/LC, management fees)
- Verify cap rate math: NOI / Price = stated cap rate (rounding errors are common in third-party reports)
- Ensure risk premium build-up sums to within 25 bps of the observed cap rate; if not, explain the residual
- Check that comp sale dates are disclosed and sufficiently recent; flag any comp older than 18 months
- Confirm risk-free rate and market survey data reflect the analysis date, not stale benchmarks
- Validate that terminal cap rate assumption is supportable — an exit cap tighter than going-in requires explicit justification
- Mark any jurisdiction-specific tax, zoning, or regulatory factors with [VERIFY] where they could materially affect value
