---
name: budget-planning
description: Create and manage budgets with variance analysis and departmental allocation. Use when the user requests budget planning or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Budget Planning

Create structured budgets by department, track actual spending against targets, and produce variance analyses that explain deviations. This skill supports top-down and bottom-up budgeting approaches, handles multi-department allocation, and generates actionable reports that highlight where spending is on track and where corrective action is needed.

## Workflow

1. **Gather Historical Data**
   Collect 6-12 months of actual spending data broken down by department and cost category. Identify trends, seasonal patterns, and one-time expenses that should be excluded from baseline calculations. Compute trailing averages and growth rates for each line item to establish a data-driven starting point.

2. **Set Budget Targets by Department**
   Define top-level budget envelopes for each department based on company revenue targets, strategic priorities, and historical run rates. Apply growth adjustments — departments investing in new initiatives may get 15-25% increases while mature cost centers target flat or declining budgets. Ensure the sum of department budgets aligns with the company-wide operating expense target.

3. **Allocate Line Items**
   Break each department budget into specific line items: personnel (salaries, benefits, contractors), software and tools, travel, marketing spend, office and facilities, professional services, and discretionary. Assign monthly phasing — some costs are evenly distributed while others are front-loaded (annual software renewals) or seasonal (Q4 marketing pushes).

4. **Track Actuals vs. Budget**
   As actual spending data comes in, map each transaction to the corresponding budget line item and period. Calculate period-to-date (MTD, QTD, YTD) actuals and compare against the phased budget. Compute both absolute dollar variance and percentage variance for each line item.

5. **Generate Variance Reports**
   Produce variance analysis showing over- and under-budget categories with explanations. Classify variances as timing (spending shifted between months but will normalize), volume (more/less activity than planned), rate (unit costs differ from plan), or permanent (structural change requiring budget revision). Project year-end estimates based on current run rates.

6. **Recommend Adjustments**
   Based on variance trends, recommend specific budget reallocations: pull forward unused budget from under-spending departments to cover overages elsewhere, or flag line items where a formal budget revision is warranted. Provide a revised forecast alongside the original budget for comparison.

## Usage

Provide historical spending data, department structure, and any top-level targets or constraints. Specify the budget period (monthly, quarterly, annual) and any known upcoming expenses.

**Example prompt:**
> Create a Q1 2025 budget for our Engineering, Marketing, and G&A departments. Engineering had $180K/month average spend last quarter, Marketing $95K, G&A $45K. We're targeting 10% overall expense reduction. Show the budget with monthly phasing and major line items.

## Examples

### Example 1: Quarterly Department Budget

**Input:** 3 departments, Q1 2025, 10% reduction target from Q4 2024 baseline of $320K/month.

**Output — Q1 2025 Budget:**

| Line Item                  | Department  | January   | February  | March     | Q1 Total   |
|----------------------------|-------------|-----------|-----------|-----------|------------|
| Salaries & Benefits        | Engineering | $112,000  | $112,000  | $112,000  | $336,000   |
| Contractors                | Engineering | $25,000   | $25,000   | $20,000   | $70,000    |
| Cloud Infrastructure       | Engineering | $18,500   | $19,000   | $19,500   | $57,000    |
| Software & Tools           | Engineering | $8,200    | $6,200    | $6,200    | $20,600    |
| **Engineering Subtotal**   |             | **$163,700** | **$162,200** | **$157,700** | **$483,600** |
| Salaries & Benefits        | Marketing   | $42,000   | $42,000   | $42,000   | $126,000   |
| Advertising & Paid Media   | Marketing   | $22,000   | $25,000   | $28,000   | $75,000    |
| Events & Sponsorships      | Marketing   | $5,000    | $2,000    | $12,000   | $19,000    |
| Content & Creative         | Marketing   | $8,000    | $8,000    | $8,000    | $24,000    |
| **Marketing Subtotal**     |             | **$77,000** | **$77,000** | **$90,000** | **$244,000** |
| Salaries & Benefits        | G&A         | $22,000   | $22,000   | $22,000   | $66,000    |
| Rent & Facilities          | G&A         | $12,000   | $12,000   | $12,000   | $36,000    |
| Insurance & Legal          | G&A         | $4,500    | $4,500    | $4,500    | $13,500    |
| Office & Miscellaneous     | G&A         | $2,500    | $2,500    | $2,500    | $7,500     |
| **G&A Subtotal**           |             | **$41,000** | **$41,000** | **$41,000** | **$123,000** |
| **Company Total**          |             | **$281,700** | **$280,200** | **$288,700** | **$850,600** |

**vs. Baseline:** Q4 2024 run rate was $320K/month ($960K/quarter). Q1 budget of $850.6K represents an 11.4% reduction, exceeding the 10% target by $9.4K.

### Example 2: Variance Analysis Report

**Input:** February actuals received, compare against Q1 budget from Example 1.

**Output — February Variance Report:**

| Line Item                | Budget    | Actual    | Variance $ | Variance % | Classification |
|--------------------------|-----------|-----------|------------|------------|----------------|
| Engineering — Salaries   | $112,000  | $112,000  | $0         | 0.0%       | On track       |
| Engineering — Contractors| $25,000   | $31,200   | +$6,200    | +24.8%     | Volume         |
| Engineering — Cloud      | $19,000   | $22,400   | +$3,400    | +17.9%     | Volume         |
| Engineering — Software   | $6,200    | $6,200    | $0         | 0.0%       | On track       |
| Marketing — Salaries     | $42,000   | $42,000   | $0         | 0.0%       | On track       |
| Marketing — Advertising  | $25,000   | $18,500   | -$6,500    | -26.0%     | Timing         |
| Marketing — Events       | $2,000    | $0        | -$2,000    | -100.0%    | Timing         |
| Marketing — Content      | $8,000    | $9,200    | +$1,200    | +15.0%     | Rate           |
| G&A — All Lines          | $41,000   | $40,100   | -$900      | -2.2%      | On track       |
| **Total**                | **$280,200** | **$281,600** | **+$1,400** | **+0.5%** |            |

**Analysis:**
- **Engineering Contractors (+$6,200):** Overage driven by an unplanned security audit requiring two additional contractors. Classified as volume variance. If audit completes in March, Q1 total may still land within 5% of budget.
- **Cloud Infrastructure (+$3,400):** Load testing for the v3.0 release drove higher-than-expected compute costs. Expected to normalize in March.
- **Marketing Advertising (-$6,500):** Campaign launch delayed to March. This is a timing variance — spending will shift to March, which is already budgeted higher. No action needed.
- **Year-end projection:** At current run rate, Q1 will land at $859K vs. $850.6K budget (+1.0%). Within acceptable tolerance.

## Best Practices

- Build budgets with 5-10% contingency reserves at the department level for unplanned but inevitable expenses.
- Phase budgets monthly rather than dividing annual totals by 12 — real spending is never evenly distributed.
- Review variances weekly for categories with high volatility (advertising, contractors) and monthly for stable costs (rent, salaries).
- Distinguish between controllable variances (spending decisions) and uncontrollable ones (vendor price increases, FX changes) in reporting.
- Lock budget baselines at the start of each period. Track changes through formal revision requests rather than silently editing the original budget.
- Tie budget targets to measurable outcomes — Marketing's $75K ad budget should be linked to a pipeline generation target, not just a spending ceiling.

## Safety Boundaries

- Treat the output as analytical support, not individualized financial, tax, investment, or accounting advice.
- Preserve source data and expose assumptions, formulas, units, and reconciliation checks so a reviewer can reproduce the result.
- Do not initiate payments, transactions, journal entries, filings, or account changes without explicit user authorization.
- Require a qualified professional to review material decisions, regulated filings, or conclusions based on incomplete data.

## Edge Cases

- **Mid-quarter headcount changes:** When a new hire starts mid-period, pro-rate their salary and benefits from their start date. Adjust the budget baseline going forward rather than showing a permanent favorable variance for the partial month.
- **One-time large purchases:** Capital expenditures (servers, office buildout) should be budgeted as one-time items in specific months, not spread evenly. Flag any unbudgeted purchase over $5K for CFO approval.
- **Departmental chargebacks:** Shared services (IT support, facilities) allocated across departments should use a consistent, pre-agreed allocation methodology. Don't change allocation percentages mid-year.
- **Budget for new departments:** When a new team spins up mid-year, create a separate budget with a ramp-up curve rather than trying to retrofit into existing department budgets.
- **Zero-based budgeting requests:** When management requests zero-based budgeting instead of incremental, start every line item at zero and require justification. This typically takes 3-4x longer but surfaces 10-15% in potential savings.
