---
name: financial-modeling
description: Build financial projections, P&L statements, DCF models, and valuation analyses from assumptions and historical data. Use when the user requests financial modeling or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Financial Modeling

Build structured financial projections including income statements, discounted cash flow (DCF) models, and valuation analyses. This skill takes a set of business assumptions and transforms them into multi-period financial forecasts with key metrics like NPV, IRR, EBITDA margins, and revenue growth rates. Suitable for startup fundraising, acquisition analysis, budgeting, and strategic planning.

## Workflow

1. **Define Core Assumptions**
   Gather all foundational inputs: revenue growth rates, pricing tiers, customer acquisition rates, churn, cost structures, tax rates, discount rates, and terminal growth rates. Validate that assumptions are internally consistent — for example, headcount growth should align with projected revenue capacity. Document each assumption with its source or rationale.

2. **Build the Revenue Model**
   Construct a bottoms-up or top-down revenue forecast depending on available data. For subscription businesses, model MRR by cohort with expansion and churn. For transactional businesses, model volume × average transaction value. Break revenue into segments if the business has multiple product lines or geographies.

3. **Project Operating Expenses**
   Forecast COGS, gross margin, and operating expenses by category: personnel, marketing, R&D, G&A, and infrastructure. Use a mix of fixed and variable cost assumptions. Tie headcount plans to compensation benchmarks. Model economies of scale where applicable — hosting costs per user should decline as volume grows.

4. **Calculate Free Cash Flows**
   Derive EBITDA from the projected P&L, then adjust for capital expenditures, changes in working capital, and taxes to arrive at unlevered free cash flow (UFCF) for each period. Clearly separate operating cash flow from investing and financing activities.

5. **Compute Valuation Metrics**
   Discount projected cash flows using WACC to compute enterprise value via DCF. Calculate terminal value using either a perpetuity growth model or an exit multiple approach. Derive NPV, IRR, and payback period. Run sensitivity tables across discount rate and growth rate ranges.

6. **Stress Test and Summarize**
   Run bear/base/bull scenarios by varying 2-3 key assumptions. Present results in a summary table showing the range of outcomes. Highlight which assumptions have the most impact on valuation.

## Usage

Provide your business assumptions, historical financials (if available), and the type of model you need. Specify the projection period and any specific metrics you want calculated.

**Example prompt:**
> Build a 3-year monthly P&L projection for a B2B SaaS startup. Starting MRR is $45K, growing 8% month-over-month for year 1, decelerating to 5% in year 2 and 3% in year 3. Gross margin is 78%. Opex starts at $60K/month and grows 4% monthly. Show EBITDA and cash position.

## Examples

### Example 1: SaaS Startup 3-Year P&L Projection

**Input:** B2B SaaS, $45K starting MRR, 8%/5%/3% MoM growth by year, 78% gross margin, $60K starting opex growing 4% monthly.

**Output (Year-End Summary):**

| Metric              | Year 1      | Year 2      | Year 3      |
|----------------------|-------------|-------------|-------------|
| Annual Revenue       | $853,971    | $1,753,589  | $2,754,401  |
| COGS (22%)           | $187,874    | $385,790    | $605,968    |
| Gross Profit         | $666,097    | $1,367,799  | $2,148,433  |
| Operating Expenses   | $901,548    | $1,443,408  | $2,310,943  |
| EBITDA               | ($235,451)  | ($75,609)   | ($162,510)  |
| EBITDA Margin        | -27.6%      | -4.3%       | -5.9%       |
| Cumulative EBITDA Deficit | ($235,451) | ($311,060) | ($473,570) |

This convention treats month 1 as the stated $45K MRR, applies 8% growth to months 2–12, 5% to months 13–24, and 3% to months 25–36. Monthly EBITDA remains negative because gross-profit dollars never overtake opex; the cumulative EBITDA deficit reaches about $474K. Actual cash position cannot be calculated without starting cash, working-capital, capex, tax, and financing assumptions. The plan therefore needs an explicit cash buffer and slower opex growth, and it does not support a conclusion about financing sufficiency on its own.

### Example 2: DCF Model for Small Business Acquisition

**Input:** Target business generates $500K annual UFCF, growing 6% per year for 5 years. WACC is 12%. Terminal growth rate 2.5%. Acquisition price $2.1M.

**Output:**

| Year | UFCF      | Discount Factor | PV of UFCF  |
|------|-----------|-----------------|-------------|
| 1    | $530,000  | 0.893           | $473,214    |
| 2    | $561,800  | 0.797           | $447,864    |
| 3    | $595,508  | 0.712           | $423,871    |
| 4    | $631,238  | 0.636           | $401,163    |
| 5    | $669,113  | 0.567           | $379,673    |

- **PV of Forecast Period:** $2,125,785
- **Terminal Value:** $669,113 × 1.025 / (0.12 − 0.025) = $7,219,377
- **PV of Terminal Value:** $7,219,377 / 1.12⁵ = $4,096,468
- **Enterprise Value:** $6,222,253
- **Enterprise value less stated purchase price:** $4,122,253 before debt, cash, transaction costs, taxes, and diligence adjustments

The modeled enterprise value exceeds the stated purchase price under these assumptions, but that is not enough to call the transaction accretive or a clear buy. Calculate equity value, financing cash flows, transaction costs, taxes, and an explicit exit or holding-period cash-flow schedule before reporting NPV or IRR. Stress-test WACC, terminal growth, operating performance, and downside cases.

## Best Practices

- Always separate assumptions from calculations so stakeholders can adjust inputs without modifying formulas.
- Use monthly granularity for the first 1-2 years and quarterly or annual thereafter to balance detail with readability.
- Anchor assumptions in comparable company data or historical performance wherever possible.
- Include a sensitivity analysis on at least two key variables (e.g., growth rate and discount rate).
- Label all units clearly — distinguish between monthly and annual figures, and between thousands and actuals.
- Cross-check the model: net income plus D&A should reconcile to operating cash flow before working capital changes.

## Safety Boundaries

- Treat the output as analytical support, not individualized financial, tax, investment, or accounting advice.
- Preserve source data and expose assumptions, formulas, units, and reconciliation checks so a reviewer can reproduce the result.
- Do not initiate payments, transactions, journal entries, filings, or account changes without explicit user authorization.
- Require a qualified professional to review material decisions, regulated filings, or conclusions based on incomplete data.

## Edge Cases

- **Pre-revenue startups:** Use a bottoms-up TAM/SAM/SOM approach with conversion funnels rather than historical growth rates. Flag that projections are highly speculative.
- **Negative free cash flow in all periods:** DCF still works but terminal value dominates. Note the sensitivity and consider using a revenue multiple as a sanity check.
- **Hyper-growth distortion:** When MoM growth exceeds 15%, compounding over 36 months produces unrealistic figures. Cap growth or switch to an S-curve model with a saturation point.
- **Currency mismatch:** If revenues and costs are in different currencies, model exchange rate assumptions explicitly and show impact of ±10% FX moves.
- **Seasonal businesses:** Monthly models must account for seasonality. Use historical monthly revenue distribution percentages rather than flat growth assumptions.
