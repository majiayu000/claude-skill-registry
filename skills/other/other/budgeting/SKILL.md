# Budgeting

name: budgeting
description: Annual and quarterly budgeting process and methodology

## When to Activate

- User needs to build or improve an annual or quarterly budgeting process
- Designing budget templates for revenue, cost centers, or capex
- Establishing a budget calendar and approval workflow
- Choosing between budgeting approaches (top-down, bottom-up, zero-based)
- Aligning headcount planning with financial budgets

## Core Concepts

### Budgeting Approaches

**Top-Down Budgeting:**
- Executive team sets high-level targets (revenue growth, margin targets, total opex envelope)
- Targets are allocated to business units and cost centers
- Pros: fast, aligned with strategic objectives, controls total spend
- Cons: may lack operational realism, limited buy-in from managers
- Best for: mature, stable businesses with centralized decision-making

**Bottom-Up Budgeting:**
- Individual departments build their budgets from granular assumptions
- Budgets are aggregated and reconciled at the corporate level
- Pros: operationally realistic, strong ownership from budget holders
- Cons: slow, prone to "padding," requires extensive review cycles
- Best for: decentralized organizations, businesses with diverse operating units

**Top-Down/Bottom-Up Hybrid (most common):**
- Executive team provides strategic guardrails (growth targets, margin floors)
- Departments build within those constraints
- Iterative negotiation resolves gaps between top-down targets and bottom-up reality
- Typically 2-3 iteration cycles

**Zero-Based Budgeting (ZBB):**
- Every expense must be justified from zero each period (no prior-year baseline)
- Decision packages ranked by priority; funded until budget envelope is exhausted
- Pros: eliminates legacy spending, forces prioritization
- Cons: extremely time-intensive, can impair morale if applied too aggressively
- Best for: cost transformation programs, PE-owned companies, organizations with significant cost bloat

### Budget Calendar

```
=== ANNUAL BUDGET CALENDAR (for January fiscal year-end) ===

Month         | Activity
July          | CFO issues budget guidelines, strategic priorities, macro assumptions
August        | Revenue planning: sales teams build pipeline-based forecasts
              | Headcount planning: HR and department heads draft hiring plans
September     | Department managers submit initial bottom-up budgets
              | FP&A consolidates, identifies gaps vs top-down targets
October       | Iteration 1: feedback to departments, request revisions
              | Capital committee reviews capex requests
November      | Iteration 2: final departmental submissions
              | FP&A produces consolidated P&L, balance sheet, cash flow
              | Executive review sessions (by BU/function)
December      | CFO/CEO finalize budget, present to Board for approval
              | Board approval
January       | Budget loaded into ERP/planning system
              | Communication to organization
              | Q1 operating against approved budget
```

### Revenue Budgeting

**By segment / product line:**
```
Revenue = Volume × Price × Mix

For SaaS:
ARR_beginning
+ New ARR (new logo bookings × average contract value)
+ Expansion ARR (upsell, cross-sell, price increases)
- Churned ARR (gross churn)
- Contraction ARR (downgrades)
= ARR_ending

Revenue ≈ (ARR_beginning + ARR_ending) / 2 + Professional Services + Other
```

**For each revenue stream, define:**
- Key driver (units, subscribers, seats, transactions, ASP)
- Growth assumptions with supporting evidence
- Seasonality pattern (allocate annual budget by month/quarter)
- Risk factors and upside scenarios

### Cost Center Budgeting

**Personnel costs (typically 60-80% of opex for knowledge businesses):**
```
Personnel Cost = Headcount × Avg Compensation × (1 + Benefits Load Factor)

Build from:
- Current headcount (filled positions)
- Planned hires (timing, role level, location)
- Expected attrition and backfills
- Merit increases (typically 3-5% annually)
- Bonus pool (% of base salary, linked to performance targets)
- Benefits load factor (15-30% of base, varies by country)
- Payroll taxes
- Stock-based compensation (vesting schedules)
```

**Non-personnel operating expenses:**
```
By category:
- Facilities (rent, utilities, maintenance) — typically fixed or contractual
- Technology (SaaS subscriptions, infrastructure, licenses) — semi-variable
- Professional services (consulting, legal, audit) — project-based
- Travel & entertainment — % of revenue or per-head
- Marketing (programs, events, digital) — % of revenue or campaign-based
- Depreciation & amortization — from capex schedule
```

### Capex Budgeting

**Maintenance capex:** Required to sustain current operations (asset replacement, IT refresh)
**Growth capex:** New capacity, new locations, product development

```
Capex Budget Line  | Category     | Amount  | Timing  | Useful Life | Approval
Server refresh     | Maintenance  | $___k   | Q2      | 5 years     | IT VP
New office buildout| Growth       | $___k   | Q1-Q2   | 10 years    | CFO
Product tooling    | Growth       | $___k   | Q3      | 7 years     | COO
```

### Headcount Planning

```
=== HEADCOUNT PLAN ===

Department   | Current HC | Attrition | Backfills | New Hires | Year-End HC | FTE Avg
Engineering  |    ___     |   ___     |    ___    |    ___    |     ___     |  ___
Sales        |    ___     |   ___     |    ___    |    ___    |     ___     |  ___
Marketing    |    ___     |   ___     |    ___    |    ___    |     ___     |  ___
G&A          |    ___     |   ___     |    ___    |    ___    |     ___     |  ___
Total        |    ___     |   ___     |    ___    |    ___    |     ___     |  ___

Average FTE = (BOY HC + EOY HC) / 2 (simplified)
or monthly FTE average for more precision
```

## Methodology

### Budget Build Process

1. **Set strategic context** — CFO communicates targets, macro assumptions, strategic priorities
2. **Distribute templates** — standardized templates to all budget holders
3. **Revenue build** — sales/commercial teams build revenue by segment, product, geography
4. **Headcount plan** — HR coordinates with department heads on hiring plan
5. **Opex build** — cost center managers populate expense budgets
6. **Capex requests** — capital expenditure proposals with business cases
7. **Consolidation** — FP&A aggregates all inputs into consolidated financials
8. **Gap analysis** — compare bottom-up total against top-down targets
9. **Iteration** — negotiate adjustments, typically 2-3 cycles
10. **Executive review** — CEO/CFO review by business unit and function
11. **Board approval** — final budget presented to board
12. **Communication** — approved budget distributed to organization
13. **System load** — budget entered into ERP/planning tool for tracking

### Common Macro Assumptions to Set Centrally

- FX rates (for multi-currency businesses)
- Inflation rate (feeds into cost escalation)
- Commodity prices (if relevant)
- Interest rates (for debt service budgeting)
- Tax rate (statutory, effective, cash tax rate)
- Merit increase pool percentage
- Benefits cost escalation rate

## Templates

### Budget Summary Template

```
=== ANNUAL BUDGET SUMMARY ===

Company: [Name]
Fiscal Year: [Year]
Currency: [CCY]
Prepared: [Date]

--- Consolidated P&L Budget ($ thousands) ---
                        | Prior Year | Budget  | YoY Growth | % Revenue
                        |  Actual    |  [Year] |            |
Revenue                 |   _____    |  _____  |    ___%    |  100.0%
Cost of Revenue         |  (_____) |  (_____) |    ___%    |   ___%
Gross Profit            |   _____    |  _____  |    ___%    |   ___%

Operating Expenses:
  Sales & Marketing     |  (_____) |  (_____) |    ___%    |   ___%
  Research & Dev        |  (_____) |  (_____) |    ___%    |   ___%
  General & Admin       |  (_____) |  (_____) |    ___%    |   ___%
Total Opex              |  (_____) |  (_____) |    ___%    |   ___%

EBITDA                  |   _____    |  _____  |    ___%    |   ___%
D&A                     |  (_____) |  (_____) |            |
EBIT                    |   _____    |  _____  |    ___%    |   ___%
Interest Expense        |  (_____) |  (_____) |            |
EBT                     |   _____    |  _____  |            |
Tax                     |  (_____) |  (_____) |            |
Net Income              |   _____    |  _____  |    ___%    |   ___%

--- Key Metrics ---
Headcount (year-end):       ____
Revenue per Employee:       $____k
Capex:                      $____k
Free Cash Flow:             $____k
```

### Department Budget Template

```
=== DEPARTMENT BUDGET ===

Department: [Name]
Budget Owner: [Name]
Cost Center: [Code]

--- Personnel Costs ---
Role / Level     | Headcount | Avg Comp | Benefits | Total Cost | Start Month
Senior Engineer  |    ___    | $____k   | $____k   |   $____k   |    ___
Junior Engineer  |    ___    | $____k   | $____k   |   $____k   |    ___
Manager          |    ___    | $____k   | $____k   |   $____k   |    ___
Subtotal         |    ___    |          |          |   $____k   |

--- Non-Personnel Costs ---
Category              | Monthly | Annual  | Notes
Software Licenses     | $____   | $____   | [Vendor, contract term]
Consulting            | $____   | $____   | [Project scope]
Travel                | $____   | $____   | [Per-head assumption]
Other                 | $____   | $____   |
Subtotal              | $____   | $____   |

--- Total Department Budget ---
Personnel:            $____k
Non-Personnel:        $____k
Total:                $____k
vs Prior Year:        ___% change
```

## Quality Gate

Before finalizing a budget, verify:

- [ ] Revenue assumptions are driver-based and traceable to operational inputs
- [ ] Headcount plan ties to personnel cost budget (no orphaned headcount)
- [ ] Hiring timing is realistic (account for recruiting lead time, typically 2-4 months)
- [ ] Benefits load factor reflects current rates and expected cost increases
- [ ] Capex is categorized as maintenance vs growth with appropriate useful lives
- [ ] Budget consolidation balances (intercompany eliminations handled)
- [ ] Seasonality is reflected in monthly/quarterly phasing (not straight-line unless appropriate)
- [ ] Currency assumptions are documented and applied consistently
- [ ] Budget implies achievable improvement vs prior year (not aspirational fantasy)
- [ ] Cash flow implications are modeled (working capital, capex, debt service)
- [ ] Contingency reserve is included (typically 2-5% of opex)
- [ ] Board-approved budget matches what is loaded into the planning system
- [ ] Budget holders have signed off on their respective budgets
