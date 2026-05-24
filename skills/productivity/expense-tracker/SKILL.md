---
name: Expense Tracker
slug: expense-tracker
description: Track business expenses, categorize spending, manage budgets, and generate financial reports
category: business
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "expense tracking"
  - "track expenses"
  - "business spending"
  - "expense report"
  - "budget tracking"
  - "financial reporting"
tags:
  - expenses
  - finance
  - budgeting
  - accounting
  - business-operations
---

# Expense Tracker

Expert expense tracking and management system that helps you capture, categorize, and analyze business spending, manage budgets, and generate financial reports. This skill provides structured workflows for expense management, budget control, and financial visibility based on accounting best practices.

Smart expense tracking is the foundation of financial control. This skill helps you understand where money is going, identify cost savings opportunities, stay compliant with tax requirements, and make informed budgeting decisions. Whether you're a solopreneur or managing team expenses, this provides the discipline needed for financial health.

Built on accounting principles and expense management best practices, this skill combines proper categorization, budget monitoring, and reporting workflows to give you complete visibility into your business spending.

## Core Workflows

### Workflow 1: Expense Capture & Recording
**Document expenses accurately and consistently**

1. **Required Information**
   - **Date**: When the expense occurred (transaction date)
   - **Amount**: Total amount spent (including tax)
   - **Vendor/Payee**: Who was paid
   - **Category**: Type of expense (see categorization below)
   - **Payment Method**: Cash, credit card, check, ACH
   - **Description**: What was purchased and business purpose
   - **Receipt**: Photo or PDF attachment

2. **Capture Methods**
   - **Manual Entry**: Key in details from receipt
   - **Receipt Scanning**: Photo → auto-extract data
   - **Credit Card Import**: Connect accounts for auto-sync
   - **Email Forwarding**: Forward receipts to expense email
   - **Mobile App**: Capture on-the-go

3. **Best Practices**
   - Record expenses within 24-48 hours (while fresh)
   - Always save receipts (digital or physical)
   - Note business purpose for tax deductibility
   - Flag personal expenses mixed in business accounts
   - Batch similar expenses (e.g., weekly mileage)

### Workflow 2: Expense Categorization
**Organize spending into meaningful categories**

1. **Standard Categories**
   - **Cost of Goods Sold (COGS)**: Direct costs of products/services sold
     - Materials, inventory purchases
     - Manufacturing costs
     - Shipping/fulfillment

   - **Operating Expenses**:
     - **Salaries & Wages**: Employee compensation, contractors
     - **Rent**: Office, warehouse, retail space
     - **Utilities**: Electric, water, internet, phone
     - **Marketing & Advertising**: Ads, campaigns, events
     - **Software & Subscriptions**: SaaS tools, licenses
     - **Office Supplies**: Stationery, equipment, furniture
     - **Travel & Entertainment**: Business travel, client meals
     - **Professional Services**: Legal, accounting, consulting
     - **Insurance**: Liability, property, health
     - **Taxes & Licenses**: Business taxes, permits, fees
     - **Depreciation**: Asset depreciation (non-cash)
     - **Miscellaneous**: Other operating costs

2. **Categorization Rules**
   - Use consistent categories across all periods
   - Create sub-categories for detailed tracking (e.g., Marketing > Facebook Ads)
   - Map credit card descriptions to categories automatically
   - Review and recategorize monthly for accuracy
   - Document category definitions for team clarity

3. **Tax Deductibility Flags**
   - Mark expenses as deductible, non-deductible, or partial
   - Track personal vs. business use percentage
   - Document business purpose for audit defense
   - Separate capital expenses (assets) from operating expenses

### Workflow 3: Budget Management
**Set spending limits and monitor against budget**

1. **Budget Creation**
   - Set budgets by category and time period (monthly, quarterly, annual)
   - Base on historical spending + growth plans
   - Align with revenue projections and cash flow
   - Build in contingency buffer (5-10%)

2. **Budget Tracking**
   - Compare actual vs. budget by category
   - Calculate variance: (Actual - Budget) / Budget
   - Identify over-budget categories early
   - Forecast end-of-period spending based on run rate

3. **Budget Alerts**
   - Set thresholds for alerts (e.g., 80% of budget spent)
   - Notify stakeholders of overages
   - Require approval for over-budget purchases
   - Review and adjust budgets quarterly

4. **Flexible Budgeting**
   - Adjust budgets for variable costs tied to revenue
   - Example: Marketing budget = 20% of revenue
   - Automatically scale up/down with business performance

### Workflow 4: Expense Reporting & Analysis
**Generate reports for decision-making and compliance**

1. **Standard Reports**
   - **Expense by Category**: Total and % of total for each category
   - **Expense Trends**: Month-over-month, year-over-year comparisons
   - **Budget Variance**: Actual vs. budget by category
   - **Vendor Spending**: Total spend by vendor (find savings opportunities)
   - **Expense by Project/Department**: Track cost centers
   - **Tax Deduction Summary**: Total deductible expenses for tax prep

2. **Time-Based Analysis**
   - **Daily**: Track daily burn rate
   - **Weekly**: Review team expenses, flag anomalies
   - **Monthly**: Close books, reconcile accounts, analyze trends
   - **Quarterly**: Budget reviews, forecast adjustments
   - **Annual**: Tax preparation, year-end reporting

3. **Cost Optimization**
   - Identify top expense categories (80/20 rule)
   - Find duplicate subscriptions or unused services
   - Negotiate vendor contracts for high-spend categories
   - Benchmark spending vs. industry standards
   - Track cost per customer/revenue metrics

### Workflow 5: Reimbursement & Approval
**Manage employee expense reimbursements**

1. **Expense Submission**
   - Employee submits expense report with receipts
   - Categorizes expenses per company policy
   - Notes business purpose and attendees (for meals)
   - Submits for manager approval

2. **Approval Workflow**
   - Manager reviews for policy compliance
   - Checks receipt accuracy and business purpose
   - Approves, rejects, or requests clarification
   - Finance validates and processes payment

3. **Reimbursement Processing**
   - Set payment schedule (weekly, bi-weekly)
   - Pay via payroll, direct deposit, or check
   - Track reimbursement status (submitted → approved → paid)
   - Provide payment confirmation to employee

4. **Expense Policy Enforcement**
   - Define spending limits by category and role
   - Require pre-approval for large expenses
   - Specify allowed expense types
   - Set receipt requirements ($25+ threshold common)
   - Establish timely submission rules (within 30 days)

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Add expense | "Log expense: [Amount] at [Vendor] for [Category]" |
| Categorize | "Categorize [Expense] as [Category]" |
| Monthly report | "Show expenses for [Month]" |
| Budget check | "Compare spending to budget" |
| Top expenses | "Show top 10 expenses this month" |
| Vendor analysis | "Total spending at [Vendor]" |
| Tax deductions | "Show deductible expenses [Year]" |
| Category breakdown | "Expense breakdown by category" |
| Pending reimbursements | "Show unpaid expense reports" |
| Receipt upload | "Attach receipt for [Expense]" |

## Best Practices

### Expense Recording
- Capture expenses immediately (don't let receipts pile up)
- Always attach receipt/proof of purchase
- Write detailed descriptions for audit trail
- Separate personal and business expenses
- Use dedicated business accounts (easier tracking)

### Categorization Consistency
- Define category taxonomy upfront
- Train team on category usage
- Review and recategorize monthly
- Use automation rules for recurring expenses
- Keep categories aligned with P&L structure

### Receipt Management
- **Keep receipts for**: All expenses (digital or physical)
- **Retention period**: 7 years (IRS requirement)
- **Critical details**: Date, vendor, amount, items purchased
- **Digital storage**: Cloud backup, searchable, organized by year/month
- **Credit card statements**: Not sufficient for IRS (need itemized receipts)

### Reconciliation
- Reconcile credit cards and bank accounts monthly
- Match expenses to bank transactions
- Identify and investigate discrepancies
- Mark expenses as reconciled
- Close books at month-end before reporting

### Tax Readiness
- Track deductible vs. non-deductible expenses
- Document business purpose (especially travel, meals, entertainment)
- Maintain mileage logs for vehicle expenses
- Separate home office expenses
- Consult CPA on deductibility questions

### Cost Control
- Review largest expense categories monthly
- Question recurring charges (cancel unused subscriptions)
- Negotiate with top vendors annually
- Implement approval workflows for large purchases
- Track cost per unit metrics (per customer, per employee)

## Key Metrics to Track

**Spending Metrics:**
- Total expenses (monthly, quarterly, annual)
- Expense growth rate (month-over-month, year-over-year)
- Expenses by category (absolute and % of total)
- Burn rate (monthly cash out)
- Runway (months of cash at current burn rate)

**Budget Metrics:**
- Budget variance by category (actual vs. budget)
- Budget utilization rate (% of budget spent)
- Forecast vs. actual variance

**Efficiency Metrics:**
- Expense ratio (expenses / revenue)
- Cost per customer acquisition
- Cost per employee
- Operating margin (revenue - expenses) / revenue

**Vendor Metrics:**
- Top 10 vendors by spend
- Vendor concentration (% of spend with top vendor)
- Average payment terms

## Common Pitfalls to Avoid

- **Delayed recording**: Letting expenses pile up (leads to forgotten items)
- **Lost receipts**: No proof for tax deductions or reimbursements
- **Inconsistent categories**: Making period-over-period comparisons impossible
- **Personal/business mixing**: Complicating accounting and audit risk
- **No budget discipline**: Spending without awareness of constraints
- **Missing business purpose**: Can't defend deductions in audit
- **Poor reconciliation**: Bank balance doesn't match books
- **Ignored small expenses**: Death by a thousand cuts

## Integration Points

- **Accounting Software**: QuickBooks, Xero, FreshBooks
- **Banking**: Auto-import transactions from connected accounts
- **Credit Cards**: Sync corporate cards, personal cards used for business
- **Receipt Scanning**: OCR to extract data from receipts
- **Mileage Tracking**: GPS-based mileage logs
- **Payroll**: Sync reimbursements to payroll system
- **Project Management**: Allocate expenses to projects/clients
- **Tax Software**: Export deductions for tax filing

## Expense Policy Template

**Allowable Expenses:**
- Business travel (flights, hotels, ground transportation)
- Client meals and entertainment (with business purpose documented)
- Office supplies and equipment
- Software and subscriptions (approved by IT)
- Professional development (courses, books, conferences)
- Marketing and advertising

**Spending Limits:**
- Meals: $50/day domestic, $75/day international (without approval)
- Hotels: Reasonable rate for business district
- Flights: Economy class (business class for 5+ hour flights with approval)
- Equipment: Under $500 no approval, over $500 requires manager approval

**Requirements:**
- Submit expense reports within 30 days
- Attach itemized receipts for all expenses over $25
- Document business purpose and attendees for meals
- Use corporate card when available
- Pre-approve travel over $1,000
