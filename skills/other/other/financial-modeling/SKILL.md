---
name: financial-modeling
description: Financial modeling patterns, valuation methodologies, and quantitative analysis for investment decisions. Includes DCF, LBO, and scenario modeling techniques.
---

# Financial Modeling Skill

Comprehensive financial modeling patterns for investment analysis and valuation.

## Valuation Methodologies

### Discounted Cash Flow (DCF)

The fundamental intrinsic valuation approach based on future cash flows.

```
Enterprise Value = Sum of PV(FCF) + PV(Terminal Value)

Where:
- FCF = Free Cash Flow for each projection year
- Terminal Value = Perpetuity or exit multiple value
- Discount Rate = WACC or required return
```

#### Key Assumptions to Document
1. Revenue growth rates and drivers
2. Margin assumptions (gross, EBITDA, net)
3. Working capital requirements
4. Capital expenditure needs
5. Terminal growth rate (typically 2-3%)
6. Discount rate components

### Comparable Company Analysis

Relative valuation using public company multiples.

| Metric | Formula | When to Use |
|--------|---------|-------------|
| EV/Revenue | For high-growth, unprofitable companies |
| EV/EBITDA | Standard for mature companies |
| P/E | For stable, profitable businesses |
| P/B | For asset-intensive businesses |

#### Cannabis Industry Multiples (2024-2025)
- MSOs (Multi-State Operators): 3-6x EV/Revenue
- Cultivation: 1-3x EV/Revenue
- Retail: 4-8x EV/EBITDA (adjusted)
- Manufacturing: 2-4x EV/Revenue

### Precedent Transactions

Analyze historical M&A transactions for valuation benchmarks.

- Control premium typically 20-40%
- Synergy assumptions affect deal multiples
- Market conditions at time of deal matter

## Cash Flow Modeling

### Unlevered Free Cash Flow

```python
def calculate_ufcf(
    revenue: float,
    ebitda_margin: float,
    da_pct: float,
    capex_pct: float,
    nwc_change: float,
    tax_rate: float
) -> float:
    """Calculate Unlevered Free Cash Flow."""
    ebitda = revenue * ebitda_margin
    da = revenue * da_pct
    ebit = ebitda - da
    nopat = ebit * (1 - tax_rate)
    ufcf = nopat + da - (revenue * capex_pct) - nwc_change
    return ufcf
```

### Levered Free Cash Flow

```
UFCF
- Interest Expense * (1 - Tax Rate)
- Mandatory Debt Repayment
+ Net Debt Proceeds
= Levered Free Cash Flow (to Equity)
```

## LBO Modeling

### Equity Returns Framework

```
IRR = (Exit Equity / Entry Equity)^(1/Years) - 1

Multiple = Exit Equity / Entry Equity

Components of Value Creation:
1. EBITDA Growth (organic + acquisitions)
2. Multiple Expansion (entry vs exit multiple)
3. Debt Paydown (deleveraging)
4. Cash Generation (dividends)
```

### Debt Capacity Analysis

```
Maximum Debt = Min of:
- EBITDA * Target Leverage (e.g., 4.0x)
- Free Cash Flow / Minimum DSCR
- Collateral Value * Advance Rate
```

### Cash Sweep Mechanics

```python
def calculate_cash_sweep(
    excess_cash: float,
    sweep_percentage: float,
    minimum_cash: float,
    available_cash: float
) -> float:
    """Calculate mandatory debt prepayment from excess cash."""
    sweepable = max(0, available_cash - minimum_cash)
    sweep_amount = sweepable * sweep_percentage
    return min(sweep_amount, excess_cash)
```

## Scenario Analysis Framework

### Three Scenario Model

| Scenario | Assumptions | Probability |
|----------|-------------|-------------|
| Base | Management case with haircut | 50% |
| Downside | Revenue -20%, margins -5% | 30% |
| Upside | Outperformance on key metrics | 20% |

### Sensitivity Analysis

Two-way sensitivity tables for key value drivers:

```
          Revenue Growth (%)
          5%    8%    10%   12%   15%
EBITDA
Margin
20%      X%    X%    X%    X%    X%
25%      X%    X%    X%    X%    X%  <- Base Case
30%      X%    X%    X%    X%    X%
35%      X%    X%    X%    X%    X%
```

### Monte Carlo Simulation

For more sophisticated analysis, simulate thousands of scenarios:

```python
import numpy as np

def monte_carlo_irr(
    base_case: dict,
    assumptions: dict,
    n_simulations: int = 10000
) -> dict:
    """
    Run Monte Carlo simulation on IRR.

    Returns distribution of outcomes.
    """
    results = []
    for _ in range(n_simulations):
        # Randomize assumptions within ranges
        scenario = {
            k: np.random.triangular(v['min'], v['mode'], v['max'])
            for k, v in assumptions.items()
        }
        irr = calculate_irr(base_case, scenario)
        results.append(irr)

    return {
        'mean': np.mean(results),
        'median': np.median(results),
        'std': np.std(results),
        'p10': np.percentile(results, 10),
        'p90': np.percentile(results, 90)
    }
```

## Working Capital Modeling

### Net Working Capital Definition

```
NWC = Current Operating Assets - Current Operating Liabilities

Typical Components:
+ Accounts Receivable
+ Inventory
+ Prepaid Expenses
- Accounts Payable
- Accrued Expenses
= Net Working Capital
```

### Days Calculation

```
DSO (Days Sales Outstanding) = AR / Revenue * 365
DIO (Days Inventory Outstanding) = Inventory / COGS * 365
DPO (Days Payables Outstanding) = AP / COGS * 365

Cash Conversion Cycle = DSO + DIO - DPO
```

## Model Quality Checklist

### Structure
- [ ] Inputs separated from calculations
- [ ] Consistent formatting throughout
- [ ] Clear navigation and flow
- [ ] Summary dashboard

### Accuracy
- [ ] Balance sheet balances
- [ ] Cash flow ties to balance sheet
- [ ] Debt schedule ties to financials
- [ ] Circular references resolved

### Flexibility
- [ ] Easy to change assumptions
- [ ] Scenario switches work
- [ ] Date handling is robust
- [ ] Handles edge cases

### Documentation
- [ ] All assumptions documented
- [ ] Sources cited
- [ ] Version control in place
- [ ] User guide included

## Output Standards

### Investment Memo Format
1. Executive Summary with recommendation
2. Key metrics summary table
3. Valuation range with methodology
4. Risk factors and mitigants
5. Sensitivity analysis results

### Presentation Deck Format
1. Investment highlights (1 slide)
2. Company overview (1-2 slides)
3. Financial summary (2-3 slides)
4. Valuation analysis (2 slides)
5. Returns analysis (1-2 slides)
6. Risk factors (1 slide)
7. Appendix with detailed schedules
