# LBO Modeling

name: lbo-modeling
description: LBO model construction — sources & uses, debt schedules, returns

## When to Activate

- User needs to build or review a leveraged buyout model
- Evaluating a PE acquisition with debt financing
- Constructing debt schedules with multiple tranches
- Calculating IRR/MOIC under various exit and leverage scenarios
- Assessing maximum purchase price a financial sponsor can pay

## Core Concepts

### LBO Value Creation Levers

An LBO generates returns through three mechanisms:
1. **Debt paydown** — free cash flow services and reduces debt, equity value grows
2. **EBITDA growth** — revenue growth and margin expansion increase enterprise value
3. **Multiple expansion** — exit at a higher multiple than entry (least reliable)

### Sources & Uses

**Sources (how the deal is funded):**
```
Revolving Credit Facility (drawn at close, if any)
Term Loan A
Term Loan B
Senior Secured Notes
Mezzanine / Subordinated Debt
Sponsor Equity
Management Rollover Equity
-----------------------------
Total Sources
```

**Uses (where the money goes):**
```
Equity Purchase Price (share price × diluted shares, or EV - net debt)
Refinance Existing Debt
Transaction Fees (advisory, financing, legal — typically 2-4% of EV)
Financing Fees (OID, arrangement fees — amortized over debt life)
Cash to Balance Sheet (minimum operating cash)
-----------------------------
Total Uses
```

**Sources must equal Uses. This is the fundamental balancing equation.**

### Debt Tranches

| Tranche | Typical Terms | Characteristics |
|---------|---------------|-----------------|
| Revolving Credit Facility | L+150-250bps, 5yr maturity | Undrawn at close; working capital buffer |
| Term Loan A | L+175-275bps, 5-6yr, amortizing | 5-10% annual mandatory amortization |
| Term Loan B | L+250-400bps, 6-7yr, bullet | 1% annual amortization, bullet at maturity |
| Senior Secured Notes | 4-8% fixed, 7-8yr | Call protection (NC2-3, then par+half coupon) |
| Senior Unsecured Notes | 6-10% fixed, 8-10yr | Subordinated to secured debt |
| Mezzanine / 2nd Lien | 10-14% (cash + PIK), 8-10yr | PIK toggle common, equity kickers |
| Seller Note | Negotiated, 5-7yr | Subordinated, often below market rate |

### Leverage Metrics

```
Total Leverage = Total Debt / LTM EBITDA (typically 4.0-6.5x for PE deals)
Senior Leverage = Senior Debt / LTM EBITDA (typically 3.0-4.5x)
Interest Coverage = EBITDA / Total Interest Expense (minimum 2.0x)
Fixed Charge Coverage = (EBITDA - Capex) / (Interest + Mandatory Amort) (minimum 1.2x)
```

### Debt Schedule Mechanics

**Mandatory amortization:**
- Scheduled principal payments (e.g., 1% per year for TLB, 5-10% for TLA)
- Contractual obligation regardless of cash flow

**Optional prepayment (voluntary):**
- Available free cash flow after mandatory payments
- Prepay highest-cost debt first (waterfall)
- Subject to prepayment penalties on some instruments

**Cash sweep:**
- Percentage (typically 50-75%) of excess cash flow directed to debt repayment
- Excess cash flow = EBITDA - interest - taxes - capex - mandatory amort - working capital changes
- Steps down as leverage ratio improves (e.g., 75% above 4.0x, 50% at 3.0-4.0x, 25% below 3.0x)

### Free Cash Flow to Equity

```
EBITDA
- Cash Interest Expense
- Cash Taxes
- Capital Expenditures
- Change in Net Working Capital
- Mandatory Debt Amortization
= Free Cash Flow Available for Optional Prepayment / Cash Sweep
```

## Methodology

### Step-by-Step LBO Build

1. **Set entry assumptions** — purchase price, entry multiple, transaction fees
2. **Build sources & uses** — balance debt capacity against equity check
3. **Construct operating model** — revenue, EBITDA, capex, working capital (5-7 year projection)
4. **Build debt schedules** — for each tranche: opening balance, interest, mandatory amort, optional prepay, closing balance
5. **Calculate free cash flow** — determine cash available for debt service and paydown
6. **Model cash sweep** — apply excess cash flow percentage to debt reduction
7. **Set exit assumptions** — exit year (typically Year 3-5), exit multiple
8. **Calculate exit enterprise value** — exit EBITDA × exit multiple
9. **Compute equity value at exit** — exit EV minus remaining net debt
10. **Calculate returns** — IRR, MOIC, cash-on-cash

### Return Calculations

**MOIC (Multiple of Invested Capital):**
```
MOIC = Exit Equity Value / Initial Equity Investment

Example:
Sponsor equity invested: $500m
Exit equity value: $1,250m
MOIC: 2.5x
```

**IRR (Internal Rate of Return):**
```
IRR solves for r in: -Equity₀ + Σ(Dividends_t / (1+r)^t) + Exit Equity / (1+r)^n = 0

Typical PE targets:
- 20-25% gross IRR (before fees)
- 2.0-3.0x MOIC over 4-5 year hold
```

**Include interim dividends/recapitalizations in IRR calculation if applicable.**

### Sensitivity Analysis

**Two-way tables to construct:**

**Table 1: Entry Multiple vs Exit Multiple**
```
IRR           | Exit 8.0x | Exit 9.0x | Exit 10.0x | Exit 11.0x
Entry 8.0x    |   ___%    |   ___%    |    ___%    |    ___%
Entry 9.0x    |   ___%    |   ___%    |    ___%    |    ___%
Entry 10.0x   |   ___%    |   ___%    |    ___%    |    ___%
```

**Table 2: EBITDA Growth vs Leverage**
```
IRR              | 4.0x Lev | 4.5x Lev | 5.0x Lev | 5.5x Lev
EBITDA CAGR 3%   |   ___%   |   ___%   |   ___%   |   ___%
EBITDA CAGR 5%   |   ___%   |   ___%   |   ___%   |   ___%
EBITDA CAGR 8%   |   ___%   |   ___%   |   ___%   |   ___%
```

**Table 3: MOIC by Exit Year**
```
           | Year 3 | Year 4 | Year 5 | Year 6 | Year 7
MOIC       |  ___x  |  ___x  |  ___x  |  ___x  |  ___x
IRR        |  ___%  |  ___%  |  ___%  |  ___%  |  ___%
```

### Maximum Purchase Price (Ability to Pay)

Work backwards from target IRR:
1. Set target IRR (e.g., 20%) and hold period (e.g., 5 years)
2. Assume exit multiple and projected exit EBITDA
3. Calculate required exit equity value
4. Back into maximum entry equity = exit equity / (1 + IRR)^n
5. Add debt capacity to get maximum enterprise value
6. Implied maximum entry multiple = max EV / entry EBITDA

## Templates

### LBO Summary Output

```
=== LBO MODEL SUMMARY ===

Target: [Company Name]
Sponsor: [Fund Name]
Transaction Date: [Date]

--- Transaction Summary ---
Entry EV:              $____m
Entry Multiple:        ___x LTM EBITDA
Equity Contribution:   $____m (___% of total sources)
Total Debt:            $____m (___x EBITDA)

--- Sources & Uses ---
Sources                          Uses
Term Loan B:    $____m           Equity Purchase:  $____m
Senior Notes:   $____m           Refinance Debt:   $____m
Sponsor Equity: $____m           Transaction Fees: $____m
Mgmt Rollover:  $____m           Financing Fees:   $____m
Total:          $____m           Total:            $____m

--- Projected Returns ---
                  | Year 3  | Year 4  | Year 5
Exit EBITDA       | $____m  | $____m  | $____m
Exit EV (at __x)  | $____m  | $____m  | $____m
Net Debt at Exit  | $____m  | $____m  | $____m
Equity Value      | $____m  | $____m  | $____m
MOIC              |  ___x   |  ___x   |  ___x
IRR               |  ___%   |  ___%   |  ___%

--- Value Creation Bridge ---
Entry equity:                $____m
+ EBITDA growth              $____m
+ Debt paydown               $____m
+ Multiple expansion         $____m
= Exit equity:               $____m
```

## Quality Gate

Before finalizing an LBO model, verify:

- [ ] Sources equal uses exactly
- [ ] Debt capacity is realistic for the sector (check leverage vs comparable LBOs)
- [ ] Interest coverage ratio stays above 2.0x throughout the projection
- [ ] Cash balance never goes negative (model a revolver as liquidity backstop)
- [ ] Debt paydown waterfall follows seniority (senior before subordinated)
- [ ] Cash sweep mechanics step down with leverage improvement
- [ ] Exit multiple assumption is justified (typically assume no expansion)
- [ ] IRR includes management fees and carry structure if modeling net returns
- [ ] Sensitivity tables cover meaningful range of entry/exit multiples and growth rates
- [ ] Circular reference from cash interest on revolver is resolved (iterate or break)
- [ ] PIK interest compounds correctly (adds to principal, does not consume cash)
- [ ] Working capital and capex assumptions are consistent with operating model
- [ ] Transaction and financing fees are realistic (2-4% of EV for transaction, 2-3% of debt for financing)
