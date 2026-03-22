# DCF Valuation

name: dcf-valuation
description: DCF valuation methodology — WACC, terminal value, sensitivity

## When to Activate

- User asks to value a company using intrinsic/fundamental methods
- Building a discounted cash flow model from scratch or reviewing one
- Calculating WACC, terminal value, or equity value per share
- Performing sensitivity or scenario analysis on a valuation
- Preparing a valuation section for a pitch book or fairness opinion

## Core Concepts

### Unlevered Free Cash Flow (UFCF)

UFCF represents cash available to all capital providers before debt service.

**Formula:**
```
UFCF = EBIT × (1 - Tax Rate)
     + Depreciation & Amortization
     - Capital Expenditures
     - Change in Net Working Capital
```

**Key adjustments:**
- Exclude interest expense (already captured in WACC)
- Normalize one-time items (restructuring, litigation, asset sales)
- Stock-based compensation: deduct as real economic cost (do NOT add back)
- Capitalize operating leases if pre-IFRS 16 financials
- Deferred revenue changes flow through working capital

### Projection Period

- Typically 5-10 years; use 10 for high-growth or cyclical businesses
- Year 1-2: granular, driver-based (revenue by segment, gross margin, opex line items)
- Year 3-5: converge toward steady-state margins and growth
- Terminal year must reflect sustainable economics — no supernormal growth

### WACC Calculation

```
WACC = (E / V) × Ke + (D / V) × Kd × (1 - t)
```

**Cost of Equity (Ke) via CAPM:**
```
Ke = Rf + β × (Rm - Rf) + Size Premium + Country Risk Premium
```

| Component | Source / Guidance |
|-----------|-------------------|
| Risk-free rate (Rf) | 10-year government bond yield matching cash flow currency |
| Equity risk premium (Rm - Rf) | Damodaran annual update, typically 4.5-6.5% for developed markets |
| Beta (β) | Regression beta (2-5yr weekly), or unlevered sector beta re-levered to target structure |
| Size premium | Kroll/Duff & Phelps size study; 1-5% for micro/small cap |
| Country risk premium | Damodaran CRP spread for emerging markets |

**Cost of Debt (Kd):**
- Use yield-to-maturity on existing debt, not coupon rate
- If no public debt, use synthetic rating approach (interest coverage → rating → spread)
- Always use after-tax cost: Kd × (1 - t)

**Capital Structure Weights:**
- Use target or optimal capital structure, not current book values
- Market value of equity = share price × diluted shares outstanding
- Market value of debt = book value (unless distressed or materially mispriced)

### Terminal Value

**Gordon Growth Model (preferred for stable businesses):**
```
TV = UFCFn × (1 + g) / (WACC - g)
```
- Terminal growth rate (g): 1.5-3.0% for developed markets (should not exceed long-run GDP growth)
- Ensure terminal year capex ≈ depreciation (steady state)

**Exit Multiple Method (cross-check):**
```
TV = EBITDAn × Exit Multiple
```
- Exit multiple based on current trading comps (not peak-cycle)
- Common to use slightly lower multiple than current to reflect maturity

**Terminal value typically represents 60-80% of enterprise value — this is normal but warrants sensitivity testing.**

### Discount Factor and Present Value

```
Discount Factor = 1 / (1 + WACC)^n
```
- Use mid-year convention for businesses with evenly distributed cash flows
- Mid-year factor: 1 / (1 + WACC)^(n - 0.5)

### Equity Bridge

```
Enterprise Value (sum of PV of FCFs + PV of TV)
- Net Debt (total debt - cash & equivalents)
- Minority Interest (at market value)
- Preferred Stock
- Unfunded Pension Obligations
+ Equity Method Investments (at fair value)
= Equity Value
÷ Diluted Shares Outstanding (treasury stock method)
= Equity Value Per Share
```

## Methodology

### Step-by-Step DCF Process

1. **Gather historical financials** — minimum 3-5 years of income statement, balance sheet, cash flow statement
2. **Normalize historical performance** — strip out non-recurring items, adjust for acquisitions
3. **Build revenue model** — segment-level drivers (volume × price, same-store × new store, etc.)
4. **Project operating costs** — fixed vs variable cost structure, margin trajectory
5. **Calculate UFCF** — apply formula above for each projection year
6. **Determine WACC** — build up each component with sourced inputs
7. **Calculate terminal value** — both methods, cross-check for reasonableness
8. **Discount to present** — apply discount factors, sum PV of FCFs and TV
9. **Build equity bridge** — subtract non-equity claims to arrive at equity value per share
10. **Run sensitivity analysis** — WACC vs growth rate, WACC vs exit multiple

### Sensitivity / Scenario Analysis

Build two-dimensional sensitivity tables:

**Table 1: WACC vs Terminal Growth Rate**
```
             | g = 1.5% | g = 2.0% | g = 2.5% | g = 3.0%
WACC = 8.0%  |   $XX    |   $XX    |   $XX    |   $XX
WACC = 8.5%  |   $XX    |   $XX    |   $XX    |   $XX
WACC = 9.0%  |   $XX    |   $XX    |   $XX    |   $XX
WACC = 9.5%  |   $XX    |   $XX    |   $XX    |   $XX
```

**Table 2: WACC vs Exit Multiple**
```
             | 8.0x | 9.0x | 10.0x | 11.0x
WACC = 8.0%  | $XX  | $XX  |  $XX  |  $XX
WACC = 9.0%  | $XX  | $XX  |  $XX  |  $XX
```

### Football Field Chart

Present valuation ranges from multiple methodologies side by side:
- DCF (Gordon Growth) — low to high from sensitivity
- DCF (Exit Multiple) — low to high from sensitivity
- Trading Comps — 25th to 75th percentile
- Precedent Transactions — 25th to 75th percentile
- 52-Week Trading Range
- Analyst Price Targets

## Templates

### DCF Summary Output

```
=== DCF VALUATION SUMMARY ===

Company: [Name]
Valuation Date: [Date]
Currency: [CCY]

--- Unlevered Free Cash Flow Projections ($ millions) ---
                    Year 1   Year 2   Year 3   Year 4   Year 5   Terminal
Revenue              ____     ____     ____     ____     ____     ____
EBIT                 ____     ____     ____     ____     ____     ____
UFCF                 ____     ____     ____     ____     ____

--- WACC Build-Up ---
Risk-Free Rate:        ___%
Equity Risk Premium:   ___%
Beta (levered):        ___
Cost of Equity:        ___%
Pre-Tax Cost of Debt:  ___%
Tax Rate:              ___%
Debt / Total Capital:  ___%
WACC:                  ___%

--- Valuation ---
PV of FCFs:            $____m
PV of Terminal Value:  $____m  (___% of EV)
Enterprise Value:      $____m

--- Equity Bridge ---
Less: Net Debt         ($____m)
Less: Minority Int.    ($____m)
Equity Value:          $____m
Diluted Shares:        ____m
Equity Value/Share:    $____

--- Implied Multiples ---
EV / EBITDA (NTM):     ___x
P/E (NTM):             ___x
```

## Quality Gate

Before finalizing a DCF, verify:

- [ ] Terminal growth rate does not exceed long-run nominal GDP growth (1.5-3.0%)
- [ ] Terminal value is 60-80% of enterprise value — flag if outside this range
- [ ] WACC is within reasonable range for the sector and risk profile (6-12% typical)
- [ ] Implied multiples from DCF are cross-checked against trading comps
- [ ] Revenue growth rates converge to sustainable level by terminal year
- [ ] Capex ≈ depreciation in terminal year (steady state assumption)
- [ ] Working capital assumptions are consistent with historical days metrics
- [ ] Diluted share count uses treasury stock method for options/warrants
- [ ] Stock-based compensation is treated consistently (deducted from UFCF)
- [ ] Sensitivity tables span a meaningful range and the base case is centered
- [ ] All inputs are sourced and documented (Rf, ERP, beta source, tax rate basis)
- [ ] Mid-year convention is applied if cash flows are evenly distributed
- [ ] Currency of cash flows matches currency of discount rate components
