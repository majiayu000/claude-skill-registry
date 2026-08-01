---
name: scenario-planning
description: 'name: scenario-planning'
---

# Scenario Planning

name: scenario-planning
description: Financial scenario planning — base, upside, downside, stress

## When to Activate

- User needs to build financial scenarios for strategic decision-making
- Presenting management or board with a range of financial outcomes
- Evaluating the impact of specific risks or opportunities on the P&L and cash flow
- Building probability-weighted expected outcomes
- Defining management action triggers tied to scenario thresholds

## Core Concepts

### Scenario Definitions

**Base Case (most likely outcome, 50-60% probability):**
- Reflects management's best estimate of future performance
- Anchored to current run-rate, pipeline, and known commitments
- Incorporates consensus macro assumptions
- This is typically the rolling forecast or budget case

**Upside Case (favorable outcome, 15-25% probability):**
- Key opportunities materialize (large deal wins, market tailwinds)
- Revenue growth at the upper end of the reasonable range
- Operating leverage kicks in (margin expansion)
- Does NOT assume everything goes right simultaneously — that is fantasy, not a scenario

**Downside Case (adverse but plausible outcome, 15-25% probability):**
- Demand softens, customer decisions delay, competitive pressure increases
- Revenue growth slows or declines moderately
- Cost inflation exceeds assumptions
- Represents a "soft landing" — things go wrong but the business adapts

**Stress Case (severe but possible outcome, 5-10% probability):**
- Recession, key customer loss, regulatory shock, or market disruption
- Revenue declines materially (10-30% depending on industry)
- Tests liquidity and solvency under extreme conditions
- Purpose: ensure the business survives, not that it thrives
- Informs liquidity reserves, covenant headroom, and contingency plans

### Key Driver Identification

Scenarios should be built by modifying specific operational drivers, not by applying blanket percentage adjustments to the P&L.

**Step 1: Identify the 10-15 drivers that most impact financial outcomes**
```
Revenue Drivers:
- New customer acquisition rate
- Customer retention / churn rate
- Average revenue per customer (ARPU)
- Pricing power / ASP changes
- Market growth rate
- Win rate on pipeline

Cost Drivers:
- Headcount growth / hiring pace
- Wage inflation / merit increases
- Input cost inflation (materials, energy)
- Discretionary spend levels (marketing, T&E, consulting)
- FX rates (for multi-currency businesses)
```

**Step 2: Define driver values for each scenario**
```
Driver                | Base    | Upside  | Downside | Stress
New logos/quarter     | 15      | 20      | 10       | 5
Monthly churn rate    | 1.5%    | 1.0%    | 2.0%     | 3.5%
ARPU                  | $500    | $550    | $475     | $450
Hiring (net adds)     | 25      | 35      | 15       | -10
COGS inflation        | 3%      | 2%      | 5%       | 8%
```

**Step 3: Run each driver set through the financial model to generate scenario P&L, balance sheet, and cash flow.**

### Probability Weighting

Calculate an expected (probability-weighted) outcome for key metrics:

```
Expected EBITDA = P(Base) × EBITDA_Base
               + P(Upside) × EBITDA_Upside
               + P(Downside) × EBITDA_Downside
               + P(Stress) × EBITDA_Stress

Example:
= 0.55 × $50M + 0.20 × $65M + 0.20 × $35M + 0.05 × $15M
= $27.5M + $13.0M + $7.0M + $0.75M
= $48.25M
```

**Use probability-weighted outcomes for:**
- Valuation (expected cash flows in a DCF)
- Debt capacity assessment (what can we comfortably service?)
- Capital allocation decisions (invest only if NPV positive across weighted scenarios)
- Investor communications (sensitivity ranges around guidance)

### Sensitivity Tables

Two-dimensional tables isolating the impact of two key drivers:

```
=== EBITDA SENSITIVITY: Revenue Growth × Gross Margin ===

EBITDA ($M)      | GM = 58% | GM = 60% | GM = 62% | GM = 64%
Rev Growth = 0%  |   $__    |   $__    |   $__    |   $__
Rev Growth = 5%  |   $__    |   $__    |   $__    |   $__
Rev Growth = 10% |   $__    |   $__    |   $__    |   $__
Rev Growth = 15% |   $__    |   $__    |   $__    |   $__
```

Build sensitivity tables for the most critical driver pairs:
- Revenue growth × gross margin
- Volume × pricing
- Churn rate × new customer acquisition
- FX rate × revenue growth
- Interest rate × leverage level

### Scenario Comparison Dashboard

```
=== SCENARIO COMPARISON ===

Metric              | Stress  | Downside | Base    | Upside
Revenue ($M)        |  ____   |   ____   |  ____   |  ____
Revenue Growth      |  ____%  |   ____%  |  ____%  |  ____%
Gross Margin        |  ____%  |   ____%  |  ____%  |  ____%
EBITDA ($M)         |  ____   |   ____   |  ____   |  ____
EBITDA Margin       |  ____%  |   ____%  |  ____%  |  ____%
Net Income ($M)     |  ____   |   ____   |  ____   |  ____
Free Cash Flow ($M) |  ____   |   ____   |  ____   |  ____
Net Debt / EBITDA   |  ___x   |   ___x   |  ___x   |  ___x
Cash Runway (months)|  ___    |   ___    |  ___    |  ___
Covenant Headroom   |  ____%  |   ____%  |  ____%  |  ____%
Probability         |  5-10%  |  15-25%  |  50-60% |  15-25%
```

## Methodology

### Scenario Construction Process

1. **Define purpose** — what decision does this scenario analysis support?
2. **Identify key drivers** — 10-15 drivers that explain 80%+ of variance
3. **Define scenario narratives** — coherent story for each scenario (not random combinations)
4. **Set driver values** — specific, justified assumptions for each driver in each scenario
5. **Run financial model** — generate full P&L, balance sheet, and cash flow for each
6. **Analyze outputs** — compare key metrics across scenarios
7. **Probability weight** — assign probabilities, calculate expected values
8. **Identify action triggers** — what metric levels trigger which management actions
9. **Build contingency plans** — pre-approved actions for downside/stress scenarios
10. **Present to management** — decision-focused, not analysis-focused

### Scenario Narratives

Each scenario needs a coherent narrative — the drivers should tell a consistent story.

**Example narratives:**
```
Upside: "Accelerated digital transformation drives demand pull-forward.
Enterprise segment grows 25% as large deals close faster.
Gross margins expand 200bp from favorable mix shift toward high-margin products.
Headcount scales efficiently due to productivity improvements."

Downside: "Economic uncertainty causes enterprise customers to delay purchasing decisions.
SMB churn increases as smaller customers cut discretionary spend.
Wage inflation persists at 5%, compressing margins.
Two planned product launches slip by one quarter."

Stress: "Recession triggers a 20% decline in new business.
Largest customer (8% of revenue) announces vendor consolidation.
Credit markets tighten, refinancing costs increase 200bp.
Workforce reduction of 15% required to preserve cash."
```

### Management Decision Triggers

```
=== DECISION TRIGGER FRAMEWORK ===

Metric                   | Green          | Yellow         | Red            | Action
Quarterly revenue        | > 95% of plan  | 90-95% of plan | < 90% of plan  | [Hiring pause]
Monthly cash burn        | < $__M         | $__M - $__M    | > $__M         | [Cost reduction]
Net retention rate       | > 110%         | 100-110%       | < 100%         | [CS intervention]
Pipeline coverage ratio  | > 3.0x         | 2.0-3.0x       | < 2.0x         | [Lead gen surge]
Covenant ratio           | > 30% headroom | 15-30% headroom| < 15% headroom | [Lender dialogue]
Cash runway              | > 18 months    | 12-18 months   | < 12 months    | [Fundraise/cut]
```

**Pre-approved contingency actions:**
- Yellow zone: management-level response, enhanced monitoring frequency
- Red zone: executive team activation, board notification, specific pre-approved actions

## Templates

### Scenario Planning Summary

```
=== SCENARIO PLANNING SUMMARY ===

Company: [Name]
Purpose: [Decision being supported]
Date: [Date]

--- Scenario Definitions ---
Base Case:     [2-sentence narrative]
Upside Case:   [2-sentence narrative]
Downside Case: [2-sentence narrative]
Stress Case:   [2-sentence narrative]

--- Key Driver Assumptions ---
[Driver table as shown above]

--- Financial Outcomes ---
[Scenario comparison dashboard as shown above]

--- Probability-Weighted Expected Outcome ---
Expected Revenue:      $____M
Expected EBITDA:       $____M
Expected Free Cash Flow: $____M

--- Decision Triggers and Contingency Plans ---
[Decision trigger framework as shown above]

--- Recommendation ---
[Specific recommendation based on scenario analysis]
[Actions to take now regardless of scenario]
[Contingency actions to prepare but not yet execute]
```

## Quality Gate

Before finalizing scenario analysis, verify:

- [ ] Each scenario has a coherent narrative (drivers tell a consistent story)
- [ ] Scenarios span a meaningful range of outcomes (not clustered around base case)
- [ ] Driver values are justified with supporting evidence or precedent
- [ ] Base case aligns with the current rolling forecast or budget
- [ ] Stress case tests liquidity and covenant compliance, not just profitability
- [ ] Probabilities assigned to scenarios sum to approximately 100%
- [ ] Probability-weighted outcome is calculated for key decision metrics
- [ ] Full financial statements are modeled (not just P&L — include cash flow and balance sheet)
- [ ] Decision triggers are specific, measurable, and tied to pre-approved actions
- [ ] Scenarios are not stale — refresh when material new information emerges
- [ ] Management has reviewed and validated scenario assumptions
- [ ] Presentation focuses on decisions and actions, not just analysis
