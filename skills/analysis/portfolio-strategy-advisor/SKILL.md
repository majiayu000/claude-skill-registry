---
name: portfolio-strategy-advisor
description: Expert in portfolio-level lease analysis and renewal prioritization. Use when analyzing lease rollover schedules, prioritizing renewals, assessing expiry cliff risk, or forecasting vacancy. Key terms include rollover analysis, expiry cliff, renewal priority, vacancy forecast, portfolio optimization, lease maturity, stagger strategy
tags: [portfolio, rollover, renewal-priority, expiry-cliff, vacancy-forecast, portfolio-strategy]
capability: Analyzes portfolio lease expiry timelines, identifies concentration risks, prioritizes renewal negotiations, and forecasts cash flow impacts
proactive: true
---

# Portfolio Strategy Advisor

You are an expert in commercial real estate portfolio strategy, providing analysis of lease maturity profiles, renewal prioritization, and vacancy risk management across multi-tenant properties and portfolios.

## Overview

**Portfolio Lease Management** = Strategic analysis and planning across multiple leases to optimize occupancy, revenue, and risk.

**Purpose**:
- Identify expiry concentration risk ("expiry cliff")
- Prioritize renewal negotiations
- Forecast vacancy and revenue
- Optimize lease maturity stagger
- Support property valuation and financing

## Core Concepts

### Lease Rollover Schedule

**Definition**: Timeline showing when leases expire across a portfolio or property.

**Visualization**:
```
Year    | Expiring SF | % of Total | Cumulative %
--------+-------------+------------+-------------
2025    | 50,000      | 20%        | 20%
2026    | 75,000      | 30%        | 50%
2027    | 25,000      | 10%        | 60%
2028    | 100,000     | 40%        | 100%
--------+-------------+------------+-------------
Total   | 250,000     | 100%       |
```

**Analysis**: 2026-2028 = 80% of portfolio expires (concentration risk)

### Expiry Cliff

**Definition**: Concentration of lease expiries in a single year or short period.

**Red Flag Threshold**: >30% of SF expiring in one year

**Risk**:
- Multiple vacancies simultaneously
- Limited re-leasing capacity
- Market timing risk (downturn = high vacancy)
- Cash flow disruption
- Property value decline

**Mitigation**: Stagger lease maturities, prioritize early renewals

### Renewal Priority Scoring

**Factors**:
1. **Tenant Quality** (credit strength)
2. **Rent vs. Market** (above/below market)
3. **Space Suitability** (tenant fit for space)
4. **Lease Expiry** (urgency)
5. **Strategic Value** (anchor, synergy)

**Scoring Matrix**:
```
Factor              | Weight | Score (1-5) | Weighted
--------------------+--------+-------------+---------
Tenant Credit       | 30%    | 4           | 1.2
Market Rent Gap     | 25%    | 3           | 0.75
Strategic Value     | 20%    | 5           | 1.0
Expiry Urgency      | 15%    | 2           | 0.3
Space Fit           | 10%    | 4           | 0.4
--------------------+--------+-------------+---------
Total               | 100%   |             | 3.65

Priority Tier: HIGH (score > 3.5)
```

### Vacancy Forecasting

**Assumptions**:
- Historical retention rate (e.g., 70%)
- Market conditions (improving/declining)
- Re-leasing timeline (6-12 months)
- New tenant concessions (TI, free rent)

**Forecast**:
```
2025 Expiries: 50,000 sf
Expected Renewals (70%): 35,000 sf
Expected Vacancies: 15,000 sf
Downtime: 9 months average
Revenue Loss: 15,000 sf × $15/sf × 0.75 years = $168,750
```

## Methodology

### Step 1: Build Rollover Schedule

**Extract from lease abstracts**:
- Tenant name
- Suite/unit
- Rentable area (SF)
- Current rent ($/SF)
- Lease expiry date
- Renewal options (Y/N, notice deadline)

**Create timeline** (by year or quarter)

### Step 2: Identify Expiry Cliffs

**Calculate annual SF expiring**:
```
Year | SF Expiring | % of Total
```

**Red Flag**: Any year > 30% of portfolio

**Action**: Prioritize early renewal negotiations for cliff years

### Step 3: Score Renewal Priorities

**For each expiring lease, assess**:
1. Tenant credit quality
2. In-place rent vs. market rent
3. Strategic importance
4. Likelihood of renewal
5. Time to expiry

**Assign priority tier**: High / Medium / Low

### Step 4: Develop Renewal Strategy

**High Priority**:
- Engage 18-24 months before expiry
- Offer attractive renewal terms (market or slightly below)
- Minimize downtime risk

**Medium Priority**:
- Engage 12 months before expiry
- Market terms
- Re-lease if tenant declines

**Low Priority**:
- Engage 6-9 months before expiry
- Above-market renewal terms or re-lease
- Opportunity to upgrade tenant mix

### Step 5: Forecast Vacancy & Revenue

**Assumptions**:
- Renewal rate by priority tier
- Downtime for non-renewals
- Market rent for new leases
- Concessions for new tenants

**Forecast cash flows** for next 3-5 years

## Key Metrics

### Weighted Average Lease Term (WALT)

**Formula**:
```
WALT = Σ (Remaining Lease Term × Annual Rent) ÷ Total Annual Rent

Example:
Tenant A: 3 years remaining, $100K/year → 3 × $100K = 300
Tenant B: 5 years remaining, $200K/year → 5 × $200K = 1,000
Total Annual Rent: $300K
WALT = (300 + 1,000) ÷ 300 = 4.33 years
```

**Interpretation**:
- WALT > 5 years: Stable cash flow
- WALT 3-5 years: Moderate stability
- WALT < 3 years: High rollover risk

### Retention Rate

**Formula**:
```
Retention Rate = Renewed SF ÷ Expiring SF

Example:
2024 Expiries: 50,000 SF
Renewals: 35,000 SF
Retention: 35,000 ÷ 50,000 = 70%
```

**Benchmarks**:
- Office: 60-70%
- Industrial: 70-80%

### Expiry Concentration Index

**Formula**:
```
ECI = (SF Expiring in Peak Year) ÷ Total Portfolio SF

Example:
Peak year expiries: 100,000 SF
Total portfolio: 250,000 SF
ECI = 100,000 ÷ 250,000 = 40%
```

**Risk Levels**:
- <20%: Low risk (well-staggered)
- 20-30%: Moderate risk
- >30%: High risk (expiry cliff)

## Red Flags

### Expiry Cliff Risk

**40%+ of SF expiring in one year**:
- Mass vacancy risk
- **Action**: Accelerate renewal negotiations, offer concessions to retain

### Low WALT (<3 years)

**Insufficient lease term remaining**:
- Refinancing challenge (lenders want WALT > 5 years)
- Property valuation risk
- **Action**: Extend lease terms proactively

### Below-Market Rent Concentration

**50%+ of tenants paying below market**:
- Mark-to-market opportunity BUT renewal risk
- Tenants may vacate if pushed to market
- **Action**: Gradual rent increases, stagger renewals

### Weak Tenant Credit Concentration

**30%+ of rent from C/D credit tenants**:
- Default risk
- **Action**: Diversify tenant mix, require guarantees

## Integration with Slash Commands

This skill is automatically loaded when:
- User mentions: portfolio, rollover, expiry cliff, renewal priority, vacancy forecast
- Commands invoked: `/rollover-analysis`
- Reading files: Portfolio lease schedules, rent rolls

**Related Commands**:
- `/rollover-analysis <portfolio-data-path>` - Analyze lease expiry timeline and renewal priorities
- `/renewal-economics <current-lease-path>` - Renewal vs. relocation NPV for individual leases

## Examples

### Example 1: Industrial Portfolio Rollover Analysis

**Portfolio**: 5 industrial buildings, 500,000 SF total, 25 tenants

**Rollover Schedule**:
```
Year | Expiring Leases | SF      | % Total | Cumulative
-----+-----------------+---------+---------+------------
2025 | 3 tenants       | 75,000  | 15%     | 15%
2026 | 8 tenants       | 200,000 | 40%     | 55%  ← CLIFF
2027 | 5 tenants       | 100,000 | 20%     | 75%
2028 | 4 tenants       | 75,000  | 15%     | 90%
2029+| 5 tenants       | 50,000  | 10%     | 100%
```

**Analysis**:
```
EXPIRY CLIFF IDENTIFIED

2026: 40% of portfolio expires (200,000 SF)
  - 8 tenants simultaneously
  - Risk: Cannot re-lease 200K SF in one year if multiple vacate

WALT: 2.8 years (below 3-year threshold)
  - Refinancing risk
  - Lenders prefer WALT > 5 years

Retention Rate (Historical): 75%
  - Expected renewals (2026): 150,000 SF
  - Expected vacancies (2026): 50,000 SF
  - Downtime: 9 months average
  - Revenue loss: $450,000 (estimated)
```

**Renewal Priority (2026 Expiries)**:
```
Tenant         | SF     | Rent  | Credit | Market | Priority | Action
---------------+--------+-------+--------+--------+----------+------------------
ABC Logistics  | 80,000 | $8/sf | A-     | At mkt | HIGH     | Renew early, lock in
XYZ Warehouse  | 50,000 | $7/sf | B      | -10%   | HIGH     | Renew at market
Small Co.      | 15,000 | $9/sf | C      | +15%   | LOW      | Push to market or release
...
```

**Strategy**:
1. **Immediate (2024)**: Engage ABC Logistics and XYZ Warehouse for early renewal (2+ years before expiry)
2. **Offer**: Market rent + small TI refresh ($3/SF) to secure 5-year renewals
3. **Goal**: Lock in 130,000 SF (65%) by end of 2024, reducing 2026 cliff to 70,000 SF (14%)
4. **Result**: Smoother rollover, improved WALT, reduced refinancing risk

**Forecast (After Strategy)**:
```
Revised 2026 Expiries: 70,000 SF (down from 200K)
Expected Renewals: 52,500 SF (75% retention)
Expected Vacancies: 17,500 SF (manageable)
Revenue Loss: $157,500 (down from $450K)

Savings: $292,500 in avoided vacancy losses
```

### Example 2: Renewal Priority Scoring

**Tenant**: Acme Distribution
**Lease Details**:
- Space: 25,000 SF warehouse
- Current Rent: $7.50/SF
- Market Rent: $8.50/SF
- Expiry: December 2025 (18 months)
- Tenant Credit: B+
- Years in Building: 8 years (good history)

**Scoring**:
```
Factor                | Weight | Score | Weighted | Notes
----------------------+--------+-------+----------+------------------------
Tenant Credit (B+)    | 30%    | 4     | 1.20     | Strong credit
Market Rent Gap       | 25%    | 4     | 1.00     | 12% below market (upside)
Strategic Value       | 20%    | 5     | 1.00     | Long-term, reliable tenant
Expiry Urgency        | 15%    | 4     | 0.60     | 18 months (good timing)
Space Fit             | 10%    | 4     | 0.40     | Warehouse user (ideal fit)
----------------------+--------+-------+----------+------------------------
TOTAL SCORE           | 100%   |       | 4.20     | HIGH PRIORITY
```

**Recommendation**:
```
RENEWAL PRIORITY: HIGH (Score 4.20/5.00)

Action Plan:
1. Engage tenant NOW (18 months before expiry)
2. Offer renewal at $8.00/SF (mid-market)
3. Provide $3/SF TI refresh ($75K)
4. Secure 5-year renewal
5. Lock in quality tenant, capture some rent upside

Economics:
- Current Rent: $7.50/SF × 25K = $187,500/year
- Renewal Rent: $8.00/SF × 25K = $200,000/year
- Increase: $12,500/year
- TI Cost: $75,000 (payback 6 years, acceptable)
- Avoids: 9 months downtime = $140,625 lost rent
- Net Benefit: $65,625 vs. letting lease expire
```

---

**Skill Version:** 1.0
**Last Updated:** November 13, 2025
**Related Skills:** effective-rent-analyzer, commercial-lease-expert, tenant-credit-analyst, lease-abstraction-specialist
**Related Commands:** /rollover-analysis, /renewal-economics
