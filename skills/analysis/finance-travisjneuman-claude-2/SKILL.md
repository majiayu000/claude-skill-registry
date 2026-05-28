---
name: finance
description: Financial analysis expertise for financial modeling (DCF, LBO, M&A), valuation, financial statement analysis, capital allocation, treasury management, and corporate finance decisions. Use when building financial models, analyzing statements, or making investment decisions.
---

# Financial Analysis Expert

Comprehensive financial frameworks for modeling, valuation, and corporate finance decisions.

## Financial Statement Analysis

### DuPont Analysis (5-Factor)

Decompose ROE into operational drivers:

```
ROE = Net Profit Margin x Asset Turnover x Equity Multiplier

Extended (5-Factor):
ROE = (EBIT/Sales) x (Sales/Assets) x (Assets/Equity) x (EBT/EBIT) x (NI/EBT)
    = Operating Margin x Asset Turnover x Leverage x Interest Burden x Tax Burden
```

### Key Financial Ratios

| Category          | Ratio             | Formula                              | Benchmark            |
| ----------------- | ----------------- | ------------------------------------ | -------------------- |
| **Profitability** | Gross Margin      | Gross Profit / Revenue               | Industry specific    |
|                   | Operating Margin  | EBIT / Revenue                       | 15-25% (varies)      |
|                   | Net Margin        | Net Income / Revenue                 | 10-20% (varies)      |
|                   | ROIC              | NOPAT / Invested Capital             | > WACC               |
|                   | ROE               | Net Income / Equity                  | 15-20%+              |
| **Liquidity**     | Current Ratio     | Current Assets / Current Liabilities | 1.5-2.0x             |
|                   | Quick Ratio       | (CA - Inventory) / CL                | 1.0x+                |
|                   | Cash Ratio        | Cash / Current Liabilities           | 0.2-0.5x             |
| **Leverage**      | Debt/Equity       | Total Debt / Total Equity            | < 1.0x               |
|                   | Debt/EBITDA       | Total Debt / EBITDA                  | 2-3x (IG), 4-6x (HY) |
|                   | Interest Coverage | EBIT / Interest Expense              | > 3x                 |
| **Efficiency**    | Asset Turnover    | Revenue / Total Assets               | Industry specific    |
|                   | Inventory Days    | Inventory / (COGS/365)               | Industry specific    |
|                   | DSO               | AR / (Revenue/365)                   | 30-45 days           |
|                   | DPO               | AP / (COGS/365)                      | 30-60 days           |

### Cash Flow Analysis

```
FREE CASH FLOW (FCF):
Operating Cash Flow
- Capital Expenditures
= Free Cash Flow

UNLEVERED FREE CASH FLOW (for valuation):
EBIT
x (1 - Tax Rate)
= NOPAT
+ Depreciation & Amortization
- Change in Working Capital
- Capital Expenditures
= Unlevered Free Cash Flow

LEVERED FREE CASH FLOW:
Unlevered FCF
- Interest Expense x (1 - Tax Rate)
- Mandatory Debt Repayments
+ Net Borrowing
= Levered Free Cash Flow
```

## Valuation Methodologies

### Discounted Cash Flow (DCF)

```
ENTERPRISE VALUE:
         T    UFCFt           Terminal Value
EV = Σ  ───────────  +  ─────────────────────
        t=1 (1+WACC)^t      (1+WACC)^T

TERMINAL VALUE (Perpetuity Growth):
                  UFCF(T+1)
Terminal Value = ───────────
                 WACC - g

TERMINAL VALUE (Exit Multiple):
Terminal Value = EBITDA(T) x Exit Multiple

EQUITY VALUE:
Equity Value = Enterprise Value - Net Debt + Cash
```

### DCF Model Template

| Year            | 1   | 2   | 3   | 4   | 5   | Terminal |
| --------------- | --- | --- | --- | --- | --- | -------- |
| Revenue         |     |     |     |     |     |          |
| Growth %        |     |     |     |     |     |          |
| EBITDA          |     |     |     |     |     |          |
| Margin %        |     |     |     |     |     |          |
| D&A             |     |     |     |     |     |          |
| EBIT            |     |     |     |     |     |          |
| Tax             |     |     |     |     |     |          |
| NOPAT           |     |     |     |     |     |          |
| + D&A           |     |     |     |     |     |          |
| - CapEx         |     |     |     |     |     |          |
| - NWC Change    |     |     |     |     |     |          |
| **UFCF**        |     |     |     |     |     |          |
| Discount Factor |     |     |     |     |     |          |
| **PV of UFCF**  |     |     |     |     |     |          |

### Comparable Company Analysis

```
TRADING MULTIPLES:
- EV/Revenue
- EV/EBITDA
- EV/EBIT
- P/E
- P/B

SELECTION CRITERIA:
1. Industry/sector alignment
2. Size (revenue, market cap)
3. Growth profile
4. Profitability profile
5. Geographic exposure
6. Capital structure

ADJUSTMENTS:
- Control premium (20-30% for acquisition)
- Liquidity discount (10-30% for private)
- Size discount (10-20% for smaller)
```

### Precedent Transaction Analysis

```
TRANSACTION MULTIPLES:
- EV/LTM Revenue
- EV/LTM EBITDA
- EV/NTM EBITDA
- Transaction Premium to unaffected price

ADJUSTMENTS:
- Market conditions at time of deal
- Strategic vs. financial buyer
- Competitive auction vs. negotiated
- Synergy assumptions baked in
```

### Sum-of-the-Parts (SOTP)

```
METHODOLOGY:
1. Identify distinct business segments
2. Value each segment independently
3. Apply segment-specific multiples/DCF
4. Sum segment values
5. Subtract corporate costs (capitalized)
6. Adjust for holding company discount (10-20%)

CONGLOMERATE DISCOUNT FACTORS:
- Complexity premium demanded by investors
- Capital allocation inefficiencies
- Management distraction
- Lack of pure-play comparables
```

## Leveraged Buyout (LBO) Analysis

### LBO Model Structure

```
SOURCES & USES:
Sources:
- Senior Debt (Term Loan A/B)
- Subordinated Debt (Mezz, High Yield)
- Equity Contribution

Uses:
- Purchase Price
- Refinance Existing Debt
- Transaction Fees
- Cash to Balance Sheet

KEY METRICS:
- Entry Multiple: EV / LTM EBITDA
- Exit Multiple: Assumed sale multiple
- Equity IRR: Target 20-25%+
- Cash-on-Cash: 2.0-3.0x in 5 years
- MOIC: Multiple of Invested Capital
```

### LBO Returns Framework

| IRR Target | Hold Period | Required MOIC |
| ---------- | ----------- | ------------- |
| 20%        | 3 years     | 1.7x          |
| 20%        | 5 years     | 2.5x          |
| 25%        | 3 years     | 2.0x          |
| 25%        | 5 years     | 3.0x          |

### Value Creation Sources

```
                        % of Total Returns (typical)
EBITDA Growth           40-50%
- Revenue growth
- Margin improvement

Multiple Expansion      20-30%
- Market timing
- Operational improvement
- Strategic repositioning

Debt Paydown           20-30%
- Cash flow generation
- Working capital improvement
```

## M&A Financial Analysis

### Accretion/Dilution Analysis

```
STANDALONE EPS (Acquirer):
Net Income / Shares Outstanding = EPS

PRO FORMA EPS:
(Combined Net Income - Synergies + Interest Cost) / New Shares = PF EPS

ACCRETION/(DILUTION):
(PF EPS - Standalone EPS) / Standalone EPS = %

BREAKEVEN SYNERGIES:
Synergies needed to make deal EPS neutral
```

### Synergy Analysis

| Synergy Type      | Typical Range            | Realization Timeline |
| ----------------- | ------------------------ | -------------------- |
| Cost Synergies    | 5-15% of target costs    | 1-3 years            |
| Revenue Synergies | 2-5% of combined revenue | 2-5 years            |

### Deal Structure Considerations

```
CONSIDERATION:
- Cash: Immediate value, tax implications
- Stock: Alignment, dilution, tax deferral
- Mixed: Balance of above

FINANCING:
- Debt capacity analysis
- Credit rating implications
- Optimal capital structure
- Bridge financing needs
```

## Capital Allocation Framework

### Capital Allocation Hierarchy

```
1. MAINTAIN CORE BUSINESS
   - Maintenance CapEx
   - Working capital
   - Required debt service

2. INVEST IN GROWTH
   - Growth CapEx (> WACC hurdle)
   - M&A (strategic fit + returns)
   - R&D / Innovation

3. RETURN TO SHAREHOLDERS
   - Dividends (sustainable payout)
   - Share repurchases (below intrinsic value)

4. BUILD FLEXIBILITY
   - Cash reserves
   - Debt capacity
   - Strategic optionality
```

### Investment Hurdle Rates

| Investment Type    | Typical Hurdle | Risk Premium |
| ------------------ | -------------- | ------------ |
| Maintenance CapEx  | WACC           | None         |
| Growth CapEx       | WACC + 2-3%    | Low          |
| Domestic M&A       | WACC + 3-5%    | Medium       |
| International M&A  | WACC + 5-8%    | High         |
| Venture/Innovation | 25-30% IRR     | Very High    |

### ROIC vs WACC Framework

```
VALUE CREATION:
ROIC > WACC → Value creating
ROIC = WACC → Value neutral
ROIC < WACC → Value destroying

ECONOMIC PROFIT:
Economic Profit = (ROIC - WACC) x Invested Capital

SPREAD ANALYSIS:
Track ROIC-WACC spread over time
Target: Positive and expanding spread
```

## Treasury & Risk Management

### Working Capital Management

```
CASH CONVERSION CYCLE:
CCC = DSO + DIO - DPO

DSO (Days Sales Outstanding) = AR / (Revenue/365)
DIO (Days Inventory Outstanding) = Inventory / (COGS/365)
DPO (Days Payable Outstanding) = AP / (COGS/365)

OPTIMIZATION LEVERS:
- Accelerate collections (DSO reduction)
- Improve inventory turns (DIO reduction)
- Extend payment terms (DPO increase)
- Supply chain financing
```

### Hedging Strategies

| Risk Type         | Hedging Instruments      | Strategy                       |
| ----------------- | ------------------------ | ------------------------------ |
| **FX Risk**       | Forwards, Options, Swaps | Natural hedging, rolling hedge |
| **Interest Rate** | Swaps, Caps, Floors      | Fixed/floating mix             |
| **Commodity**     | Futures, Options         | Cost certainty for inputs      |
| **Credit**        | CDS, Insurance           | Counterparty protection        |

### Capital Structure Optimization

```
OPTIMAL CAPITAL STRUCTURE:
Balance:
- Tax shield benefits of debt
- Bankruptcy/distress costs
- Financial flexibility
- Credit rating implications

CREDIT METRICS TARGETS:
Investment Grade:
- Debt/EBITDA: 2-3x
- Interest Coverage: > 5x
- FFO/Debt: > 30%

High Yield:
- Debt/EBITDA: 4-6x
- Interest Coverage: > 2x
- FFO/Debt: 15-25%
```

## Investor Relations

### Earnings Call Preparation

```
KEY COMPONENTS:
1. Prepared remarks (10-15 min)
   - Financial highlights
   - Operational performance
   - Strategic updates
   - Guidance

2. Q&A preparation
   - Anticipated questions
   - Approved responses
   - Escalation protocols

3. Supplemental materials
   - Earnings release
   - Investor presentation
   - Financial supplement
```

### Guidance Framework

| Guidance Type     | Frequency    | Specificity |
| ----------------- | ------------ | ----------- |
| Revenue           | Quarterly    | Range       |
| EPS               | Quarterly    | Range       |
| Cash Flow         | Annual       | Target      |
| CapEx             | Annual       | Range       |
| Long-term Targets | Investor Day | Directional |

## Financial Planning & Analysis

### Rolling Forecast Model

```
FREQUENCY: Monthly or Quarterly
HORIZON: 12-18 months rolling

COMPONENTS:
- Revenue by segment/product
- Gross margin drivers
- Operating expense detail
- Working capital assumptions
- CapEx plan
- Cash flow projection

VARIANCE ANALYSIS:
- Budget vs. Actual
- Prior forecast vs. Current
- Volume vs. Price vs. Mix
```

### Budget Process Timeline

| Phase              | Timing | Activities               |
| ------------------ | ------ | ------------------------ |
| Strategic Planning | Q2     | Long-range plan update   |
| Guidance Setting   | Q3     | Preliminary targets      |
| Detailed Budgeting | Q3-Q4  | Bottom-up plans          |
| Review & Approval  | Q4     | Executive/Board approval |
| Communication      | Q4     | Cascaded targets         |

## See Also

- [Fortune 50 Business Strategy](../fortune50-business-strategy/SKILL.md)
- [Fortune 50 Risk Management](../fortune50-risk-management/SKILL.md)
- [Fortune 50 Operations](../fortune50-operations/SKILL.md)
