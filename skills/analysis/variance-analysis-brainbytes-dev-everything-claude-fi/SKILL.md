---
name: variance-analysis
description: 'name: variance-analysis'
---

# Variance Analysis

name: variance-analysis
description: Variance analysis — price, volume, mix, efficiency variances

## When to Activate

- User needs to decompose budget vs actual variances into root causes
- Performing price, volume, and mix analysis on revenue or cost variances
- Building variance reporting for management or board presentations
- Setting materiality thresholds and action triggers
- Creating waterfall/bridge charts to visualize variance drivers

## Core Concepts

### Variance Decomposition Framework

Every financial variance can be decomposed into underlying drivers. The goal is to move beyond "we missed by $2M" to "we missed because volume was 5% below plan partially offset by 2% higher pricing."

### Revenue Variance Decomposition

**Price × Volume framework:**
```
Total Revenue Variance = Actual Revenue - Budget Revenue

Price Variance  = (Actual Price - Budget Price) × Actual Volume
Volume Variance = (Actual Volume - Budget Volume) × Budget Price
Mix Variance    = Σ [(Actual Mix_i - Budget Mix_i) × Budget Margin_i × Actual Total Volume]
```

**Three-way decomposition (price, volume, mix):**
```
Example:
Budget:  1,000 units × $100 avg price = $100,000
Actual:  1,050 units × $97 avg price  = $101,850

Volume Variance:  (1,050 - 1,000) × $100 = +$5,000 (F)
Price Variance:   ($97 - $100) × 1,050   = -$3,150 (U)
Total Variance:   $101,850 - $100,000     = +$1,850 (F)
```

**Revenue variance with mix effect (multi-product):**
When the product mix shifts toward higher or lower-margin products, the mix variance captures this impact separately from pure volume and price effects.

### Cost Variance Decomposition

**Direct materials:**
```
Material Price Variance    = (Actual Price - Standard Price) × Actual Quantity
Material Quantity Variance = (Actual Quantity - Standard Quantity) × Standard Price
```

**Direct labor:**
```
Labor Rate Variance       = (Actual Rate - Standard Rate) × Actual Hours
Labor Efficiency Variance = (Actual Hours - Standard Hours) × Standard Rate
```

**Overhead:**
```
Spending Variance   = Actual Overhead - Budgeted Overhead (at actual activity level)
Volume Variance     = Budgeted OH (at actual activity) - Applied OH (standard rate × actual units)
Efficiency Variance = (Actual Hours - Standard Hours) × Standard OH Rate
```

### Favorable vs Unfavorable

| Variance Type | Favorable (F) | Unfavorable (U) |
|---------------|--------------|-----------------|
| Revenue | Actual > Budget | Actual < Budget |
| Cost / Expense | Actual < Budget | Actual > Budget |
| Margin | Actual > Budget | Actual < Budget |

**Always label variances as (F) or (U) — never rely on sign convention alone.**

### Materiality Thresholds

Define thresholds that trigger deeper investigation and management action:

```
=== MATERIALITY THRESHOLDS ===

Level 1 — Informational (no action required):
Revenue:   < 2% or < $100k
Opex:      < 3% or < $50k

Level 2 — Investigation required (root cause analysis):
Revenue:   2-5% or $100k-$500k
Opex:      3-8% or $50k-$200k

Level 3 — Escalation to management (corrective action plan):
Revenue:   > 5% or > $500k
Opex:      > 8% or > $200k

Level 4 — Board notification:
Any variance impacting full-year EBITDA by > 10% or > $1M
```

Thresholds should be calibrated to the company's size and risk tolerance.

### Root Cause Analysis

For every material variance, document:
1. **What happened** — quantified variance with decomposition
2. **Why it happened** — operational root cause (not "we spent more")
3. **Is it recurring** — one-time or systemic issue
4. **Timing impact** — pulled forward / pushed back, or permanent change
5. **Full-year impact** — update forecast based on root cause
6. **Corrective action** — specific steps, owner, and timeline

**Common root causes by category:**
```
Revenue shortfall:
- Delayed deal closings (timing — may recover next quarter)
- Lower win rate (competitive pressure — systemic)
- Customer churn above forecast (product/service issue)
- Pricing pressure (market dynamics)
- FX impact (external)

Cost overrun:
- Unplanned hiring / consulting (scope creep)
- Higher input costs (inflation, supply chain)
- Project delays (cost escalation)
- Technology/infrastructure costs (usage-based overrun)
- Legal/regulatory costs (unforeseeable)
```

## Methodology

### Step-by-Step Variance Analysis Process

1. **Extract actuals** from ERP/accounting system for the closed period
2. **Align to budget** — ensure chart of accounts mapping is correct
3. **Calculate total variances** — actual minus budget for every line item
4. **Apply materiality filter** — focus analysis effort on material variances
5. **Decompose material variances** — into price, volume, mix, timing, FX, one-time
6. **Conduct root cause analysis** — interview budget owners, review operational data
7. **Assess full-year impact** — does the variance persist, reverse, or amplify?
8. **Update forecast** — incorporate learnings into the rolling forecast
9. **Prepare variance report** — executive summary with bridge chart
10. **Present to management** — focus on actions, not just explanations

### Bridge Chart (Waterfall) Construction

A bridge chart visually walks from budget to actual, showing each variance driver.

```
Budget Revenue: $10,000k
  + Volume:      +$500k  ←  green bar (favorable)
  + Pricing:     -$200k  ←  red bar (unfavorable)
  + Mix:         +$150k  ←  green bar
  + FX:          -$100k  ←  red bar
  + One-time:    -$50k   ←  gray bar
= Actual Revenue: $10,300k
```

**Rules for effective bridge charts:**
- Start with budget, end with actual
- Order drivers by magnitude (largest impact first) or logical flow
- Use consistent colors (green = favorable, red = unfavorable, gray = neutral/FX)
- Include both the dollar amount and percentage impact
- Maximum 6-8 bars between budget and actual (combine small items into "other")

### Management Action Triggers

```
Variance Situation            | Required Action
Revenue > 5% below budget     | Sales pipeline deep dive, revised go-to-market, forecast update
Gross margin > 200bp below    | Pricing review, supplier renegotiation, product cost analysis
Opex > 10% above budget       | Spending freeze assessment, hiring pause evaluation
Cash flow > 15% below budget  | Working capital initiative, capex reprioritization
Customer churn > 2x plan      | Executive escalation, retention program, product review
```

## Templates

### Variance Report Template

```
=== VARIANCE ANALYSIS REPORT ===

Period: [Month/Quarter] [Year]
Prepared by: [Name]
Date: [Date]

--- Executive Summary ---
[2-3 sentence narrative: key takeaways, largest variances, full-year implications]

--- P&L Variance Summary ($ thousands) ---
                   | Budget | Actual | Variance | Var %  | Status
Revenue            | _____  | _____  |  _____   | ____%  | F/U
COGS               | _____  | _____  |  _____   | ____%  | F/U
Gross Profit       | _____  | _____  |  _____   | ____%  | F/U
  Gross Margin %   | ____%  | ____%  |  ___ bp  |        |
Sales & Marketing  | _____  | _____  |  _____   | ____%  | F/U
R&D                | _____  | _____  |  _____   | ____%  | F/U
G&A                | _____  | _____  |  _____   | ____%  | F/U
EBITDA             | _____  | _____  |  _____   | ____%  | F/U
  EBITDA Margin %  | ____%  | ____%  |  ___ bp  |        |

--- Material Variance Detail ---

Variance #1: [Description] — $___k [F/U]
  Decomposition: Volume $___k + Price $___k + Mix $___k + Other $___k
  Root Cause: [Explanation]
  Recurring: [Yes/No]
  Full-Year Impact: $___k
  Action: [Corrective action, owner, deadline]

Variance #2: [Description] — $___k [F/U]
  [Same structure]

--- Revenue Bridge ---
Budget → [+Volume] → [+/-Price] → [+/-Mix] → [+/-FX] → [+/-Other] → Actual

--- EBITDA Bridge ---
Budget → [+/-Revenue impact] → [+/-COGS] → [+/-Opex] → [+/-Other] → Actual

--- Forecast Update ---
Prior FY Forecast:    $____k EBITDA
Variance Impact:      $____k
Updated FY Forecast:  $____k EBITDA
vs Budget:            ____%
```

### Departmental Variance Template

```
=== DEPARTMENT VARIANCE REPORT ===

Department: [Name]
Budget Owner: [Name]
Period: [Month/Quarter]

Line Item          | Budget | Actual | Variance | Explanation          | Action Required
Salaries           | _____  | _____  |  _____   | [2 hires ahead of plan] | [None — in plan]
Consulting         | _____  | _____  |  _____   | [Unplanned project]  | [CFO approval needed]
Travel             | _____  | _____  |  _____   | [Conference pulled fwd]| [Will reverse Q3]
Software           | _____  | _____  |  _____   | [New tool added]     | [Review Q3]
Total              | _____  | _____  |  _____   |                      |
```

## Quality Gate

Before finalizing variance analysis, verify:

- [ ] Actuals are final (month/quarter is closed, no pending adjustments)
- [ ] Budget baseline is correct (approved budget, not a prior forecast)
- [ ] Variance decomposition is complete (price + volume + mix + other = total)
- [ ] Favorable/unfavorable labels are correct and consistent
- [ ] Materiality thresholds are applied consistently
- [ ] Root causes are operational, not circular (not "we spent more because we spent more")
- [ ] Timing variances are identified (will reverse in future periods)
- [ ] Full-year impact is assessed for each material variance
- [ ] Corrective actions have specific owners and deadlines
- [ ] Bridge chart mathematically reconciles from budget to actual
- [ ] FX impact is isolated if the business operates in multiple currencies
- [ ] Variance report is reviewed with budget owners before executive presentation
- [ ] Forecast is updated to reflect variance learnings
