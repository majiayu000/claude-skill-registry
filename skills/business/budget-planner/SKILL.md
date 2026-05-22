---
name: Budget Planner
slug: budget-planner
description: Create, manage, and optimize budgets for projects, departments, and organizations with variance tracking and scenario planning
category: finance
complexity: moderate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create budget"
  - "budget planning"
  - "budget template"
  - "budget vs actual"
  - "annual budget"
  - "project budget"
tags:
  - budgeting
  - financial-planning
  - variance-analysis
  - cost-management
  - forecasting
---

# Budget Planner

Expert budget creation and management agent that builds comprehensive budgets, tracks spending against plans, analyzes variances, and optimizes resource allocation. Specializes in zero-based budgeting, rolling forecasts, and multi-scenario planning.

This skill applies structured budgeting methodologies to help organizations plan spending, control costs, and make data-driven allocation decisions. Perfect for annual planning, project budgets, departmental spending, and startup runway management.

## Core Workflows

### Workflow 1: Annual Budget Creation

**Objective:** Build a comprehensive annual operating budget from scratch

**Steps:**
1. **Gather Historical Data**
   - Prior year actuals (P&L by month)
   - Prior year budget vs actual variances
   - Headcount and compensation data
   - Vendor contracts and commitments
   - Capital expenditure history
   - Revenue trends and projections

2. **Define Budget Parameters**
   - Fiscal year start/end dates
   - Budget cycle (calendar vs fiscal)
   - Currency and exchange assumptions
   - Inflation assumptions (2-4% typical)
   - Headcount growth assumptions
   - Revenue growth targets

3. **Revenue Budget**
   - Product/service revenue projections
   - Pricing assumptions
   - Volume/unit assumptions
   - Seasonal patterns
   - New product launches
   - Customer retention assumptions
   - Geographic mix

4. **Cost of Goods Sold (COGS) Budget**
   - Direct materials costs
   - Direct labor costs
   - Manufacturing overhead
   - Gross margin targets
   - Unit economics assumptions

5. **Operating Expense Budget**
   - **Personnel Costs:**
     - Salaries and wages (by department)
     - Benefits (typically 20-30% of salary)
     - Payroll taxes (7.65% FICA + state)
     - Bonuses and commissions
     - Stock-based compensation
     - Contractor costs

   - **Facilities Costs:**
     - Rent and lease payments
     - Utilities
     - Insurance
     - Maintenance and repairs
     - Property taxes

   - **Technology Costs:**
     - Software subscriptions (SaaS)
     - Hardware and equipment
     - Cloud infrastructure
     - IT support and services

   - **Marketing Costs:**
     - Advertising and media
     - Events and conferences
     - Content and creative
     - Marketing technology
     - Agency fees

   - **General & Administrative:**
     - Legal and professional services
     - Accounting and audit
     - Office supplies
     - Travel and entertainment
     - Training and development

6. **Capital Expenditure Budget**
   - Equipment purchases
   - Facility improvements
   - Technology infrastructure
   - Depreciation schedules

7. **Cash Flow Implications**
   - Working capital needs
   - CapEx timing
   - Seasonal cash requirements
   - Financing needs

8. **Budget Consolidation**
   - Roll up departmental budgets
   - Eliminate intercompany items
   - Create consolidated P&L budget
   - Balance sheet projections
   - Cash flow projections

9. **Scenario Development**
   - Base case (most likely)
   - Upside case (+10-20% revenue)
   - Downside case (-10-20% revenue)
   - Cost reduction scenarios

**Deliverable:** Complete annual budget package with P&L, departmental details, and scenarios

### Workflow 2: Project Budget Development

**Objective:** Create a detailed budget for a specific project or initiative

**Steps:**
1. **Project Scope Definition**
   - Project objectives and deliverables
   - Timeline and milestones
   - Resource requirements
   - Success criteria
   - Constraints and dependencies

2. **Work Breakdown Structure**
   - Decompose project into phases
   - Identify major work packages
   - List activities within each package
   - Estimate effort for each activity

3. **Resource Cost Estimation**
   - **Internal Labor:**
     - Identify required roles
     - Estimate hours per role
     - Apply fully-loaded labor rates
     - Account for utilization rates

   - **External Resources:**
     - Contractor/consultant rates
     - Agency or vendor costs
     - Outsourced services

4. **Non-Labor Costs**
   - Materials and supplies
   - Software and tools
   - Equipment and hardware
   - Travel and expenses
   - Training and certifications
   - Contingency reserve (10-20%)

5. **Cost Phasing**
   - Spread costs across timeline
   - Account for payment terms
   - Identify upfront vs. ongoing costs
   - Create monthly cost forecast

6. **Budget Controls**
   - Approval thresholds
   - Change request process
   - Variance reporting triggers
   - Contingency release criteria

7. **Risk-Adjusted Budget**
   - Identify cost risks
   - Probability-weighted contingency
   - Management reserve (if applicable)
   - Total project budget with reserves

**Deliverable:** Project budget with timeline, resource plan, and risk contingencies

### Workflow 3: Zero-Based Budgeting

**Objective:** Build budget from scratch justifying every expense

**Steps:**
1. **Identify Decision Units**
   - Define budget owners
   - Establish decision units (departments, functions)
   - Clarify accountability

2. **Define Service Levels**
   - Minimum level (survival)
   - Current level (maintain status quo)
   - Improvement level (enhanced performance)
   - Each level must be costed

3. **Cost Justification**
   - For each expense, answer:
     - Why is this needed?
     - What happens without it?
     - What are alternatives?
     - What's the ROI?

4. **Decision Package Creation**
   - Package 1: Minimum viable operations
   - Package 2: Core operations
   - Package 3: Growth investments
   - Package 4: Strategic initiatives

5. **Ranking and Prioritization**
   - Stack rank all packages
   - Apply funding constraints
   - Make trade-off decisions
   - Document rationale

6. **Final Budget Assembly**
   - Fund packages within constraints
   - Document unfunded priorities
   - Create implementation plan

**Deliverable:** Zero-based budget with prioritized decision packages

### Workflow 4: Rolling Forecast Update

**Objective:** Continuously update budget with latest actuals and projections

**Steps:**
1. **Close Period**
   - Gather actual results for completed period
   - Ensure data completeness
   - Reconcile to GL/accounting

2. **Variance Analysis**
   - Calculate budget vs actual variances
   - Identify significant variances (>5% or material)
   - Categorize as:
     - Timing differences (will normalize)
     - Run-rate changes (permanent)
     - One-time items (non-recurring)

3. **Forecast Adjustment**
   - Update remaining periods based on:
     - Run-rate from actuals
     - Known commitments
     - Revised assumptions
     - New information

4. **Full-Year Outlook**
   - Combine YTD actuals + forecast
   - Compare to original budget
   - Calculate expected year-end variance
   - Identify risks to forecast

5. **Action Planning**
   - If tracking above budget: investment opportunities
   - If tracking below budget: corrective actions
   - Document assumptions and risks
   - Assign owners to actions

6. **Reporting Package**
   - Executive summary
   - Variance commentary
   - Updated forecast
   - Risks and opportunities
   - Recommended actions

**Deliverable:** Updated rolling forecast with variance analysis and action plan

### Workflow 5: Startup Runway Planning

**Objective:** Model cash runway and funding needs for startups

**Steps:**
1. **Current Cash Position**
   - Cash on hand
   - Outstanding receivables
   - Available credit lines
   - Expected fundraise timing

2. **Monthly Burn Rate Analysis**
   - Current monthly expenses
   - Committed future expenses
   - Planned hiring costs
   - Growth investments

3. **Revenue Assumptions**
   - Current MRR/ARR
   - Growth rate assumptions
   - Churn assumptions
   - Cash collection timing

4. **Runway Calculation**
   - Gross burn = Total monthly expenses
   - Net burn = Gross burn - Revenue
   - Runway = Cash / Net Burn
   - Zero cash date projection

5. **Scenario Modeling**
   - Current trajectory
   - Aggressive growth scenario
   - Conservative/survival scenario
   - Path to profitability scenario

6. **Milestone Mapping**
   - Key milestones for next funding round
   - Costs to achieve milestones
   - Timeline requirements
   - Funding amount needed

7. **Cash Management Actions**
   - Expense reduction opportunities
   - Revenue acceleration options
   - Timing optimization
   - Bridge financing options

**Deliverable:** Runway model with scenarios and funding recommendations

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create annual budget | "Build annual budget for [year/org]" |
| Project budget | "Create budget for [project]" |
| Variance analysis | "Analyze budget vs actual for [period]" |
| Update forecast | "Update rolling forecast with [month] actuals" |
| Runway analysis | "Calculate runway with current burn" |
| Zero-based budget | "Build ZBB for [department]" |

## Budget Templates

### Monthly P&L Budget Template

```markdown
| Line Item | Jan | Feb | Mar | Q1 | Apr | May | Jun | Q2 | ... | FY Total |
|-----------|-----|-----|-----|----|----|-----|-----|----|----|----------|
| **Revenue** |
| Product Revenue | | | | | | | | | | |
| Service Revenue | | | | | | | | | | |
| **Total Revenue** | | | | | | | | | | |
| |
| **COGS** |
| Direct Costs | | | | | | | | | | |
| **Gross Profit** | | | | | | | | | | |
| Gross Margin % | | | | | | | | | | |
| |
| **Operating Expenses** |
| Personnel | | | | | | | | | | |
| Marketing | | | | | | | | | | |
| Technology | | | | | | | | | | |
| Facilities | | | | | | | | | | |
| G&A | | | | | | | | | | |
| **Total OpEx** | | | | | | | | | | |
| |
| **Operating Income** | | | | | | | | | | |
| Operating Margin % | | | | | | | | | | |
```

### Variance Report Template

```markdown
# Budget Variance Report: [Period]

## Executive Summary
- Total Revenue: $XXX vs Budget $XXX (X% variance)
- Total Expenses: $XXX vs Budget $XXX (X% variance)
- Net Income: $XXX vs Budget $XXX (X% variance)

## Significant Variances (>5%)

### Favorable Variances
| Line Item | Actual | Budget | Variance | Explanation |
|-----------|--------|--------|----------|-------------|
| | | | | |

### Unfavorable Variances
| Line Item | Actual | Budget | Variance | Explanation |
|-----------|--------|--------|----------|-------------|
| | | | | |

## Full-Year Impact
- Current trajectory vs annual budget
- Risks to achieving budget
- Recommended actions

## Forecast Update
- Revised full-year forecast
- Key assumption changes
```

## Budgeting Best Practices

### Planning Phase
- Start with strategic priorities
- Get executive alignment on key assumptions
- Involve budget owners early
- Build in realistic timelines
- Document all assumptions

### Execution Phase
- Distribute budgets to owners
- Establish spending approval processes
- Set up variance monitoring
- Create regular reporting cadence
- Enable budget vs actual tracking

### Monitoring Phase
- Monthly variance reviews
- Rolling forecast updates
- Action plans for significant variances
- Re-forecast when major changes occur
- Year-end projections

### Common Budget Categories

| Category | Typical % of OpEx | Notes |
|----------|-------------------|-------|
| Personnel | 60-70% | Largest expense for most companies |
| Technology | 10-15% | Growing rapidly with SaaS adoption |
| Marketing | 10-20% | Varies by stage and industry |
| Facilities | 5-10% | Often fixed costs |
| G&A | 5-10% | Legal, accounting, insurance |

## Integration with Other Skills

- **Use with `cash-flow-forecaster`:** Convert budget to cash projections
- **Use with `revenue-modeler`:** Develop revenue assumptions
- **Use with `unit-economics-calculator`:** Validate profitability assumptions
- **Use with `cost-optimizer`:** Identify budget reduction opportunities
- **Use with `financial-reporter`:** Create budget reporting packages

## Common Pitfalls to Avoid

- **Hockey stick projections:** Be realistic about growth rates
- **Ignoring seasonality:** Build monthly fluctuations into budget
- **Underestimating personnel costs:** Include benefits, taxes, raises
- **Forgetting one-time costs:** License renewals, annual fees
- **No contingency:** Include 5-10% buffer for unknowns
- **Static budgets:** Update forecasts as reality changes
- **Sandbbagging:** Budgets should be achievable but ambitious
- **No accountability:** Assign clear owners to every line item
