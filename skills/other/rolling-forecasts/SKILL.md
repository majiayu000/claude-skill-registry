# Rolling Forecasts

name: rolling-forecasts
description: Rolling forecast methodology and implementation

## When to Activate

- User wants to implement or improve a rolling forecast process
- Transitioning from static annual budgets to continuous forecasting
- Building driver-based forecast models
- Tracking forecast accuracy and reducing bias
- Designing forecast cadence and governance

## Core Concepts

### Rolling Forecast vs Static Budget

| Dimension | Static Budget | Rolling Forecast |
|-----------|--------------|------------------|
| Horizon | Fixed fiscal year | Continuous 12-18 months |
| Update frequency | Once per year | Monthly or quarterly |
| Granularity | Detailed line items | Driver-based, higher level |
| Purpose | Target-setting, accountability | Decision support, agility |
| Effort | Heavy annual process | Lighter, continuous updates |
| Relevance | Decays as year progresses | Always current |

**A rolling forecast does not replace the budget.** The budget remains the accountability benchmark. The forecast provides the latest view of where the business is actually heading.

### Forecast Horizon

**12-month rolling:** Always see 12 months ahead regardless of where you are in the fiscal year. When January actuals close, add the next January to the forecast.

**18-month rolling:** Provides visibility beyond the fiscal year boundary. Useful for businesses with long lead times, capex planning, or seasonal dynamics.

**Quarterly cadence with monthly granularity:** Most common approach. Full re-forecast quarterly; interim months updated only for material changes.

### Driver-Based Forecasting

Instead of forecasting every line item, identify the 15-25 key drivers that determine 80%+ of financial outcomes.

**Revenue drivers by business model:**
```
SaaS:        Customers × ARPU × Retention Rate
E-commerce:  Traffic × Conversion Rate × AOV
Manufacturing: Units × Price × Utilization Rate
Professional Services: Headcount × Utilization × Bill Rate × Realization
Subscription Media: Subscribers × ARPU + Ad Impressions × CPM
```

**Cost drivers:**
```
Personnel:   Headcount × Avg Cost (driven by hiring plan)
COGS:        Revenue × (1 - Gross Margin %) or Unit Volume × Unit Cost
Marketing:   Revenue × Marketing Spend Ratio or Campaign-level build
Facilities:  Fixed (lease) + Variable (utilities per sqft)
```

**Advantages of driver-based approach:**
- Faster to update (change the driver, formulas recalculate)
- More intuitive for business owners (they think in drivers, not GL codes)
- Enables scenario modeling (what if conversion rate drops 2%?)
- Facilitates accountability (driver owners vs line item owners)

### Re-Forecast Cadence

```
=== ROLLING FORECAST CALENDAR ===

Frequency: Quarterly full re-forecast, monthly actuals comparison

Day      | Activity
Day 1-3  | Month-end close (actuals finalized)
Day 4-5  | FP&A distributes driver templates to forecast owners
Day 6-8  | Business units update driver assumptions
Day 9-10 | FP&A consolidates, identifies key changes vs prior forecast
Day 11   | FP&A review meeting (challenge assumptions, resolve issues)
Day 12   | Forecast finalized, loaded into system
Day 13-15| Executive review: forecast vs budget, forecast vs prior forecast
```

### Forecast Accuracy Measurement

**MAPE (Mean Absolute Percentage Error):**
```
MAPE = (1/n) × Σ |Actual - Forecast| / |Actual| × 100%
```

**Tracking accuracy over time:**
- Measure MAPE at different lead times (1-month ahead, 3-month ahead, 12-month ahead)
- Revenue forecast accuracy target: MAPE < 5% at 1-quarter lead
- EBITDA forecast accuracy target: MAPE < 10% at 1-quarter lead
- Track bias (systematic over- or under-forecasting) separately from accuracy

**Forecast accuracy scorecard:**
```
Metric     | 1Q Ahead | 2Q Ahead | 3Q Ahead | 4Q Ahead | Target
Revenue    |   ___%   |   ___%   |   ___%   |   ___%   | < 5%
Gross Profit|  ___%   |   ___%   |   ___%   |   ___%   | < 8%
EBITDA     |   ___%   |   ___%   |   ___%   |   ___%   | < 10%
Cash Flow  |   ___%   |   ___%   |   ___%   |   ___%   | < 15%
```

### Forecast vs Actual (FvA) Analysis

Every forecast cycle should include a disciplined FvA review:

1. **Compare latest actuals to prior forecast** — what changed and why?
2. **Categorize variances:**
   - Timing (shifted between periods, self-correcting)
   - Volume/mix (demand different from forecast)
   - Rate/price (pricing, FX, inflation different from assumption)
   - One-time (unforeseeable events)
3. **Update drivers** — incorporate learnings into forward forecast
4. **Document assumptions** — every material change should be traceable

### Scenario Overlays

Layer scenarios on top of the base rolling forecast:

```
Base Forecast (most likely outcome)
± Upside Scenario (favorable market, accelerated wins)
± Downside Scenario (demand slowdown, cost inflation)
± Stress Scenario (recession, key customer loss)
```

Scenarios should modify specific drivers, not arbitrary percentage adjustments.

## Methodology

### Implementation Roadmap

**Phase 1: Foundation (Month 1-2)**
- Define forecast horizon and cadence
- Identify key drivers (15-25 for the business)
- Assign driver owners (who is accountable for each assumption)
- Build driver-based model in planning tool or spreadsheet

**Phase 2: First Cycle (Month 3-4)**
- Run parallel with existing budget process
- Collect driver inputs from business owners
- Consolidate and review
- Identify gaps in process and data

**Phase 3: Refinement (Month 5-8)**
- Iterate on driver selection (add/remove based on explanatory power)
- Improve data collection workflow (reduce manual effort)
- Begin tracking forecast accuracy
- Train business partners on driver-based thinking

**Phase 4: Maturity (Month 9+)**
- Forecast becomes primary management tool for forward-looking decisions
- Accuracy improves as institutional memory develops
- Scenario planning integrated into regular cadence
- Consider technology upgrade (Anaplan, Adaptive, Pigment, etc.)

### Best Practices

- **Limit detail:** Forecast at a higher level than the budget. Not every GL line needs a separate forecast.
- **Separate known from unknown:** Committed items (signed contracts, fixed costs) vs assumptions
- **Time-bound assumptions:** Every driver assumption should have an expiration/review date
- **No gaming:** Forecast should reflect the most likely outcome, not a sandbagged or stretched number
- **Speed over precision:** A roughly right forecast delivered quickly beats a precise one delivered late
- **Close the loop:** Every forecast cycle should begin with reviewing the accuracy of the prior forecast

## Templates

### Rolling Forecast Summary

```
=== ROLLING FORECAST SUMMARY ===

Company: [Name]
Forecast Date: [Date]
Horizon: [Next 12/18 months]

--- P&L Forecast ($ thousands) ---
              | Q1 Act | Q2 Fcst | Q3 Fcst | Q4 Fcst | FY Fcst | FY Budget | Δ to Budget
Revenue       | _____  | _____   | _____   | _____   | _____   |  _____    |  ____
Gross Profit  | _____  | _____   | _____   | _____   | _____   |  _____    |  ____
EBITDA        | _____  | _____   | _____   | _____   | _____   |  _____    |  ____
Net Income    | _____  | _____   | _____   | _____   | _____   |  _____    |  ____

--- Key Driver Assumptions ---
Driver                    | Prior Fcst | Current Fcst | Change  | Owner
Revenue growth rate       |    ___%    |     ___%     |  ___ bp | [Name]
Gross margin              |    ___%    |     ___%     |  ___ bp | [Name]
Headcount (year-end)      |    ___     |     ___      |  ± ___  | [Name]
Customer churn rate       |    ___%    |     ___%     |  ___ bp | [Name]

--- Forecast Change Bridge ---
Prior Forecast EBITDA:    $____k
+ Revenue volume impact:  $____k
+ Pricing impact:         $____k
- Cost increase:          ($____k)
± Timing / phasing:       $____k
± Other:                  $____k
= Current Forecast EBITDA: $____k
```

### Driver Input Template

```
=== DRIVER INPUT FORM ===

Department: [Name]
Forecast Owner: [Name]
Submission Date: [Date]

Driver              | Current Value | Forecast Value | Assumption Basis
New logos per month  |     ___      |      ___       | [Pipeline, win rate]
Avg deal size       |    $___k     |     $___k      | [Mix shift, pricing]
Churn rate (monthly)|    ___%      |     ___%       | [Cohort analysis]
Hiring plan (FTEs)  |     ___      |      ___       | [Approved reqs]
Unit COGS           |    $___      |     $___       | [Supplier contract]

Comments / risks:
[Free text for qualitative context]
```

## Quality Gate

Before finalizing a rolling forecast, verify:

- [ ] Forecast horizon extends at least 12 months from current date
- [ ] Key drivers are identified, owned, and documented with assumption basis
- [ ] Actuals are incorporated for closed periods (not still showing forecast)
- [ ] Forecast vs prior forecast changes are explained with a variance bridge
- [ ] Forecast vs budget delta is quantified and communicated to management
- [ ] Seasonality is reflected in monthly/quarterly phasing
- [ ] Known items (signed contracts, committed costs) are reflected at actual amounts
- [ ] Headcount forecast ties to personnel cost forecast
- [ ] Cash flow implications are included (not just P&L)
- [ ] Forecast accuracy is tracked over time (MAPE by metric and lead time)
- [ ] Bias is measured separately from accuracy (systematic over/under-forecasting)
- [ ] Scenario overlays are driver-based, not arbitrary percentage adjustments
