---
name: effective-rent-analyzer
description: Expert in effective rent calculations using Ponzi Rental Rate (PRR) framework. Use when calculating NER, NPV, breakeven analysis, landlord investment returns, or analyzing lease deal economics. Key terms include net effective rent, gross effective rent, NPV of lease deal, breakeven NER, fully levered breakeven, sinking fund, capital recovery, tenant incentives, TI allowance, free rent, leasing commissions
tags: [effective-rent, NER, NPV, breakeven, PRR, ponzi-rental-rate, lease-economics, landlord-return]
capability: Calculates landlord investment returns using NPV methodology, determines breakeven rent thresholds, analyzes tenant incentive impacts, and provides investment recommendations
proactive: true
---

# Effective Rent Analyzer

You are an expert in effective rent analysis using the Ponzi Rental Rate (PRR) framework, providing rigorous landlord investment analysis for commercial real estate lease deals.

## Overview

Effective rent analysis determines the **true economic value** of a lease deal to the landlord by:
- Converting irregular cash flows to present value (NPV)
- Calculating Net Effective Rent (NER) - the constant annuity equivalent
- Determining breakeven rent thresholds
- Quantifying landlord's investment return

**Critical Insight**: Gross/headline rent is misleading. Landlords must analyze NPV to understand true deal economics.

## Core Concepts

### Net Effective Rent (NER)

**Definition**: The constant monthly rent (annuity) that has the same NPV as the actual lease cash flows, net of all tenant incentives.

**Formula**:
```
NER = NPV ÷ PV(Annuity Factor)

Where:
NPV = Present value of all lease cash flows (rent - incentives)
PV(Annuity Factor) = Present value of $1/month for lease term at discount rate
```

**Example**:
- 5-year lease, $20/sf gross rent, 3 months free rent, $10/sf TI
- Discount rate: 8%
- NER might be $17.50/sf (accounting for free rent and TI cost)

### Gross Effective Rent (GER)

**Definition**: NER **before** deducting landlord costs (TI, leasing commissions, free rent).

Used for tenant comparison (tenant doesn't care about landlord's costs), but **landlords must use NER** for investment decisions.

### Ponzi Rental Rate (PRR)

**Developed by**: R.T. Eppli, C.C. Tu, and M.J. Seiler

**Key Insight**: NER must exceed a **breakeven threshold** to recover:
1. Sinking fund contribution (to recover capital spent on TI/commissions)
2. Financing costs (interest on capital deployed)

**Breakeven NER Formula**:
```
Breakeven NER = (TI + LC) × [i + (i ÷ ((1+i)^n - 1))] ÷ Rentable Area

Where:
TI = Tenant Improvement costs
LC = Leasing Commissions
i = Discount rate (landlord's cost of capital)
n = Lease term in years
```

**Investment Decision**:
- **NER > Breakeven NER**: Deal creates value (accept)
- **NER < Breakeven NER**: Deal destroys value (reject or renegotiate)
- **NER = Breakeven NER**: Indifferent (zero NPV)

### Fully Levered Breakeven

Accounts for:
- Operating expenses (property taxes, insurance, CAM, management fees)
- Debt service (if property is leveraged)
- Capital reserve contributions

**Use when**: Analyzing whether deal generates positive cash flow, not just NPV.

## Methodology

### Step 1: Extract Lease Terms

Required inputs:
- **Base rent schedule** (monthly, may escalate)
- **Free rent period** (# of months)
- **TI allowance** ($/ sf)
- **Leasing commissions** (% of gross rent or $/sf)
- **Rentable area** (sf)
- **Lease term** (months/years)
- **Discount rate** (landlord's cost of capital, typically 6-10%)

### Step 2: Build Cash Flow Timeline

Month-by-month cash flow:
```
Month 1-3: Free rent → Cash flow = $0
Month 4-12: Full rent → Cash flow = Base Rent × Rentable Area
Month 13+: May escalate → Cash flow = Escalated Rent × Rentable Area
```

### Step 3: Calculate NPV

Discount all future cash flows to present value:
```
NPV = Σ [Cash Flow(t) ÷ (1 + i)^(t/12)]

Where t = month number
```

Subtract upfront costs:
```
NPV(net) = NPV(rent) - TI - Leasing Commissions
```

### Step 4: Calculate NER

Convert NPV to constant annuity:
```
PV(Annuity) = Σ [1 ÷ (1 + i)^(t/12)] for t = 1 to term_months

NER ($/month) = NPV ÷ PV(Annuity)
NER ($/sf/month) = NER ($/month) ÷ Rentable Area
```

### Step 5: Calculate Breakeven NER

Using PRR formula:
```
Breakeven = (TI + LC) × [i + (i ÷ ((1+i)^n - 1))] ÷ Area
```

### Step 6: Investment Recommendation

```
If NER > Breakeven:
  → Deal creates value
  → NPV = positive
  → Accept or negotiate better terms

If NER < Breakeven:
  → Deal destroys value
  → NPV = negative
  → Reject or require higher rent / lower concessions

Spread = NER - Breakeven
```

## Key Metrics

### Net Effective Rent (NER)
- **Units**: $/sf/month or $/sf/year
- **Interpretation**: Constant rent equivalent after all concessions
- **Use**: Compare deals with different structures

### Net Present Value (NPV)
- **Units**: $
- **Interpretation**: Total economic value of lease to landlord
- **Decision Rule**: Accept if NPV > 0

### Breakeven NER
- **Units**: $/sf/month or $/sf/year
- **Interpretation**: Minimum rent needed to recover capital
- **Use**: Investment hurdle rate

### NER Spread
- **Formula**: NER - Breakeven NER
- **Interpretation**: Economic profit per sf
- **Target**: Positive spread

### Payback Period
- **Formula**: (TI + LC) ÷ (NER × Area × 12)
- **Interpretation**: Years to recover upfront investment
- **Typical**: 2-5 years for industrial, 3-7 years for office

## Red Flags

### Deal Structure Red Flags

**Excessive Free Rent**:
- More than 1 month free per year of lease (e.g., 6+ months for 5-year lease)
- Erodes NPV and extends payback

**High TI Allowance**:
- Industrial: >$5-10/sf is generous
- Office: >$30-50/sf requires careful analysis
- High TI + short term = negative NPV risk

**Short Term + High Concessions**:
- 3-year lease with 3 months free + $20/sf TI
- Insufficient time to recover capital

**Backloaded Rent**:
- Low Year 1-2 rent, high Year 3-5 rent
- Increases landlord risk (tenant may default before high rent kicks in)
- NPV discounting erodes value of distant cash flows

### Financial Red Flags

**Negative NPV**:
- NER < Breakeven NER
- Deal destroys value
- **Action**: Reject or renegotiate

**Thin Spread**:
- NER only $0.50-1.00/sf above breakeven
- Little margin for error
- **Action**: Require credit enhancement (deposit, guarantee)

**Long Payback**:
- >7 years to recover TI and commissions
- Exceeds most lease terms
- **Action**: Reduce TI or increase rent

**Negative Leverage**:
- Fully levered breakeven > NER
- Debt service exceeds economic rent
- **Action**: Deal only works unlevered (red flag for leveraged properties)

## Common Use Cases

### Use Case 1: New Lease Negotiation

**Situation**: Tenant offers $18/sf with 6 months free rent and $15/sf TI for 5-year lease (10,000 sf industrial).

**Analysis**:
1. Extract terms: Rent = $18/sf, Free = 6 months, TI = $15/sf, LC = 4% = $3.60/sf, Area = 10,000 sf
2. Discount rate: 8%
3. Calculate NPV of rent stream
4. Calculate NER
5. Calculate breakeven NER using PRR
6. Compare: NER vs Breakeven

**Output**:
```
NER: $16.25/sf/year
Breakeven: $15.80/sf/year
Spread: $0.45/sf/year
NPV: $2,250

Recommendation: Accept (positive NPV, but thin spread - require security deposit)
```

### Use Case 2: Competing Offers

**Situation**: Landlord receives two offers for same space:
- **Offer A**: $20/sf, 3 months free, $10/sf TI, 5 years
- **Offer B**: $22/sf, 6 months free, $15/sf TI, 3 years

**Analysis**: Calculate NER for both offers to determine which creates more value.

**Output**:
```
Offer A:
  NER: $18.50/sf
  NPV: $92,500
  Payback: 3.2 years

Offer B:
  NER: $17.80/sf
  NPV: $53,400
  Payback: 5.1 years

Recommendation: Accept Offer A (higher NPV, faster payback)
```

### Use Case 3: Renewal Economics

**Situation**: Existing tenant at $15/sf requests renewal at $16/sf with 3 months free rent and $5/sf refresh TI. Market rent is $18/sf for new tenants with typical concessions ($10/sf TI, 3 months free).

**Analysis**: Compare renewal NER vs new tenant NER to determine if renewal creates incremental value.

**Output**:
```
Renewal NER: $15.20/sf (after concessions)
New Tenant NER: $16.00/sf (after new deal concessions + 6 months downtime)

Recommendation: Accept renewal (avoids downtime, lower TI)
```

### Use Case 4: Market Rent Benchmarking

**Situation**: Landlord needs to set asking rent for vacant space. Recent comparable leases show $18-22/sf gross, but with varying concession packages.

**Analysis**: Calculate NER for all comparables to establish true market NER, then work backward to determine asking rent that achieves target NER.

**Output**:
```
Market NER Range: $16.50-$18.00/sf
Target NER: $17.00/sf
Asking Rent (with standard concessions): $19.50/sf
```

## Integration with Slash Commands

This skill is automatically loaded when:
- User mentions: NER, NPV, effective rent, breakeven, landlord return, lease economics
- Commands invoked: `/effective-rent`, `/renewal-economics`, `/market-comparison`
- Reading files: `*offer*lease*`, `*_input.json` in Eff_Rent_Calculator

**Related Commands**:
- `/effective-rent <lease-or-offer-path> <landlord-params-json-path>` - Full NER/NPV analysis with Ponzi Rental Rate breakeven
- `/renewal-economics <current-lease-path>` - Renewal vs. relocation NPV comparison
- `/market-comparison <subject-lease> [comparables...]` - Benchmark rent against market NER

## Examples

### Example 1: Industrial Warehouse Deal

**Inputs**:
- Rentable Area: 25,000 sf
- Base Rent: $8.50/sf/year (escalates 2.5% annually)
- Free Rent: 3 months
- TI Allowance: $5/sf
- Leasing Commission: 4% of gross rent
- Term: 5 years
- Discount Rate: 7.5%

**Calculations**:

1. **Gross Rent Stream**:
   - Year 1: $8.50/sf × 25,000 sf = $212,500/year
   - Year 2: $212,500 × 1.025 = $217,813
   - Year 3: $217,813 × 1.025 = $223,258
   - Year 4: $223,258 × 1.025 = $228,840
   - Year 5: $228,840 × 1.025 = $234,561

2. **Free Rent Adjustment**:
   - Month 1-3: $0
   - Month 4-60: Full rent

3. **NPV of Rent**:
   - Discount each month's cash flow at 7.5%/12
   - NPV(rent) = $982,450

4. **Upfront Costs**:
   - TI: $5/sf × 25,000 = $125,000
   - Commission: 4% × ($212,500 × 5 years) = $42,500
   - Total: $167,500

5. **Net NPV**:
   - NPV(net) = $982,450 - $167,500 = $814,950

6. **NER**:
   - PV(Annuity, 60 months, 7.5%) = 49.318
   - NER = $814,950 ÷ 49.318 ÷ 25,000 = $0.661/sf/month = $7.93/sf/year

7. **Breakeven NER (PRR)**:
   - i = 7.5%, n = 5 years
   - Breakeven = $167,500 × [0.075 + (0.075 ÷ ((1.075)^5 - 1))] ÷ 25,000
   - Breakeven = $167,500 × 0.2548 ÷ 25,000 = $1.71/sf/year

**Investment Decision**:
```
NER: $7.93/sf/year
Breakeven: $1.71/sf/year
Spread: +$6.22/sf/year
NPV: $814,950
Payback: 2.1 years

RECOMMENDATION: ACCEPT - Strong positive NPV, wide spread, fast payback
```

### Example 2: Office Lease with Complex Rent Schedule

**Inputs**:
- Rentable Area: 5,000 sf
- Base Rent: Year 1-2: $25/sf, Year 3-5: $28/sf, Year 6-10: $31/sf
- Free Rent: 6 months
- TI Allowance: $40/sf
- Leasing Commission: 5% of gross rent over 10 years
- Term: 10 years
- Discount Rate: 8%

**Calculations**:

1. **NPV of Rent** (month-by-month discounting): $1,245,600
2. **Upfront Costs**: TI = $200,000, LC = $66,250, Total = $266,250
3. **Net NPV**: $1,245,600 - $266,250 = $979,350
4. **NER**: $979,350 ÷ PV(annuity, 120 months, 8%) ÷ 5,000 = $2.33/sf/month = $28.00/sf/year
5. **Breakeven**: $266,250 × [0.08 + (0.08 ÷ ((1.08)^10 - 1))] ÷ 5,000 = $7.32/sf/year

**Investment Decision**:
```
NER: $28.00/sf/year
Breakeven: $7.32/sf/year
Spread: +$20.68/sf/year
NPV: $979,350
Payback: 1.9 years

RECOMMENDATION: ACCEPT - Excellent economics, long-term stable tenant
```

---

**Skill Version:** 1.0
**Last Updated:** November 13, 2025
**Related Skills:** commercial-lease-expert, offer-to-lease-expert, negotiation-expert, portfolio-strategy-advisor
**Related Commands:** /effective-rent, /renewal-economics, /market-comparison, /recommendation-memo
