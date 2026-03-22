# Cash Flow Forecasting

name: cash-flow-forecasting
description: Cash flow forecasting — direct and indirect method, 13-week

## When to Activate

- User needs to build a short-term (13-week) or long-term cash flow forecast
- Modeling working capital dynamics and their cash impact
- Calculating liquidity runway or debt service coverage
- Choosing between direct and indirect cash flow forecasting methods
- Managing cash in a distressed, high-growth, or seasonal business

## Core Concepts

### Direct vs Indirect Method

**Direct method (receipts and disbursements):**
- Forecasts actual cash inflows (customer receipts) and outflows (vendor payments, payroll)
- Built from operational data: invoices, payment terms, payroll calendars
- More accurate for short-term forecasting (1-13 weeks)
- Harder to reconcile to P&L; requires granular data

```
Cash Receipts:
  Collections from customers
  Interest received
  Other receipts
- Cash Disbursements:
  Vendor payments
  Payroll and benefits
  Rent and facilities
  Tax payments
  Interest payments
  Debt principal repayments
  Capital expenditures
= Net Cash Flow
+ Opening Cash Balance
= Closing Cash Balance
```

**Indirect method (starts from net income):**
- Adjusts net income for non-cash items and working capital changes
- Aligns with P&L forecast; easier to produce from a financial model
- Better for long-term forecasting (monthly/quarterly, 12-24 months)
- Less precise on timing of individual cash flows

```
Net Income
+ Depreciation & Amortization
+ Stock-Based Compensation
+/- Changes in Working Capital
  - Increase in Accounts Receivable
  + Decrease in Accounts Receivable
  + Increase in Accounts Payable
  - Decrease in Accounts Payable
  +/- Change in Inventory
  +/- Change in Deferred Revenue
  +/- Other Working Capital
= Cash from Operations
- Capital Expenditures
= Free Cash Flow
+/- Financing Activities (debt draws/repayments, equity)
= Net Cash Flow
```

### 13-Week Cash Flow Forecast

The 13-week forecast is the gold standard for short-term liquidity management. It covers one full quarter with weekly granularity.

**Why 13 weeks:**
- Provides enough visibility to avoid liquidity surprises
- Weekly granularity captures payment timing (biweekly payroll, monthly rent, quarterly tax)
- Standard requirement for revolving credit facilities and distressed situations
- Rolling — each week, drop the completed week and add a new week at the end

**Structure:**
```
=== 13-WEEK CASH FLOW FORECAST ===

                    | Wk 1  | Wk 2  | Wk 3  | ... | Wk 13 | Total
RECEIPTS
Customer collections| ____  | ____  | ____  |     | ____  | ____
  - Current AR      | ____  | ____  | ____  |     | ____  | ____
  - Aged AR         | ____  | ____  | ____  |     | ____  | ____
  - New billings    | ____  | ____  | ____  |     | ____  | ____
Other receipts      | ____  | ____  | ____  |     | ____  | ____
Total Receipts      | ____  | ____  | ____  |     | ____  | ____

DISBURSEMENTS
Payroll & benefits  | ____  | ____  | ____  |     | ____  | ____
Vendor payments     | ____  | ____  | ____  |     | ____  | ____
Rent / facilities   | ____  | ____  | ____  |     | ____  | ____
Insurance           | ____  | ____  | ____  |     | ____  | ____
Tax payments        | ____  | ____  | ____  |     | ____  | ____
Interest payments   | ____  | ____  | ____  |     | ____  | ____
Debt repayments     | ____  | ____  | ____  |     | ____  | ____
Capex               | ____  | ____  | ____  |     | ____  | ____
Other disbursements | ____  | ____  | ____  |     | ____  | ____
Total Disbursements | ____  | ____  | ____  |     | ____  | ____

NET CASH FLOW       | ____  | ____  | ____  |     | ____  | ____
Opening Balance     | ____  | ____  | ____  |     | ____  |
Closing Balance     | ____  | ____  | ____  |     | ____  |
Revolver Draw/(Paydown)| __ | ____  | ____  |     | ____  |
Available Liquidity | ____  | ____  | ____  |     | ____  |
```

### Working Capital Modeling

Working capital changes are the primary source of cash flow timing differences vs the P&L.

**Days-based approach:**
```
Accounts Receivable = Revenue × (DSO / 365)
Inventory = COGS × (DIO / 365)
Accounts Payable = COGS × (DPO / 365)

Net Working Capital = AR + Inventory + Prepaid Expenses
                    - AP - Accrued Expenses - Deferred Revenue

Cash Impact = ΔWorking Capital = NWC_prior - NWC_current
(Increase in NWC = cash outflow; Decrease in NWC = cash inflow)
```

**Key metrics to track:**
| Metric | Formula | Typical Range |
|--------|---------|---------------|
| DSO (Days Sales Outstanding) | AR / Revenue × 365 | 30-60 days |
| DIO (Days Inventory Outstanding) | Inventory / COGS × 365 | 30-90 days |
| DPO (Days Payable Outstanding) | AP / COGS × 365 | 30-60 days |
| Cash Conversion Cycle | DSO + DIO - DPO | 0-90 days |

**Seasonal working capital:** For businesses with seasonality, model working capital monthly using seasonal patterns from historical data, not annual averages.

### Debt Service Coverage

```
Debt Service Coverage Ratio (DSCR) = Cash Available for Debt Service / Debt Service

Where:
Cash Available = EBITDA - Taxes - Maintenance Capex - Working Capital Changes
Debt Service = Interest Payments + Mandatory Principal Repayments

Minimum DSCR:
- Investment grade: > 2.0x
- Non-investment grade: > 1.5x
- Distressed / covenant minimum: > 1.1x
```

### Liquidity Runway Calculation

```
Liquidity Runway = Available Liquidity / Monthly Net Cash Burn

Available Liquidity = Cash & Equivalents
                    + Undrawn Revolver Capacity
                    - Minimum Operating Cash (typically 2-4 weeks of disbursements)

Monthly Net Cash Burn = Average monthly cash outflows - Average monthly cash inflows
(Use trailing 3-month average, adjusted for known one-time items)
```

**For startups and pre-profit companies:**
```
Runway (months) = (Cash + Undrawn Committed Facilities) / Monthly Burn Rate

Example:
Cash: $15M
Undrawn facility: $5M
Monthly burn: $1.2M
Runway: $20M / $1.2M = 16.7 months
```

**Action thresholds:**
- > 18 months runway: comfortable, focus on growth
- 12-18 months: begin fundraising planning
- 6-12 months: actively raise or cut costs
- < 6 months: crisis mode, immediate action required

## Methodology

### Building a 13-Week Cash Flow Forecast

1. **Map cash inflow sources:**
   - Aged AR schedule: when will existing invoices be collected? Apply historical collection patterns.
   - New billings: forecast billings from the revenue model, apply payment terms to estimate collection timing.
   - Other receipts: interest, tax refunds, asset sales (known timing).

2. **Map cash outflow sources:**
   - Payroll calendar: exact dates and amounts from HR system
   - AP aging: when are vendor invoices due? What is the actual payment pattern?
   - Recurring fixed payments: rent (1st of month), insurance (quarterly), loan payments (specific dates)
   - Tax payments: estimated tax dates, VAT/GST filing calendar
   - Capex: committed purchase orders with delivery/payment milestones

3. **Week 1-4: high confidence** — based on known invoices, committed payments, payroll calendar
4. **Week 5-8: moderate confidence** — blend of known items and forecast assumptions
5. **Week 9-13: lower confidence** — primarily forecast-driven, flag assumptions

6. **Reconcile to indirect method:** Cross-check 13-week total against the monthly/quarterly cash flow derived from the P&L model. Significant discrepancies indicate a modeling error or missing items.

### Long-Term Cash Flow Projection (12-24 months)

Use the indirect method, built from the P&L and balance sheet forecast:

```
                        | Q1 Fcst | Q2 Fcst | Q3 Fcst | Q4 Fcst | FY Total
Net Income              |  ____   |  ____   |  ____   |  ____   |  ____
+ D&A                   |  ____   |  ____   |  ____   |  ____   |  ____
+ SBC                   |  ____   |  ____   |  ____   |  ____   |  ____
+/- Working Capital     |  ____   |  ____   |  ____   |  ____   |  ____
Cash from Operations    |  ____   |  ____   |  ____   |  ____   |  ____
- Capex                 | (____) | (____) | (____) | (____) | (____)
Free Cash Flow          |  ____   |  ____   |  ____   |  ____   |  ____
+/- Financing           |  ____   |  ____   |  ____   |  ____   |  ____
Net Cash Flow           |  ____   |  ____   |  ____   |  ____   |  ____
Opening Cash            |  ____   |  ____   |  ____   |  ____   |  ____
Closing Cash            |  ____   |  ____   |  ____   |  ____   |  ____
```

### Collection Pattern Analysis

Build a collection curve from historical data:

```
Invoice Month   | Month 0 | Month 1 | Month 2 | Month 3+ | Bad Debt
Collection %    |   10%   |   55%   |   25%   |    8%    |   2%

Apply to forecast billings:
Jan Billings $1,000k:
  Jan collection: $100k
  Feb collection: $550k
  Mar collection: $250k
  Apr+ collection: $80k
  Write-off: $20k
```

## Templates

### Cash Flow Forecast Summary

```
=== CASH FLOW FORECAST SUMMARY ===

Company: [Name]
Forecast Date: [Date]
Method: [Direct / Indirect / Both]

--- Liquidity Position ---
Current Cash Balance:        $____
Undrawn Revolver:            $____
Total Available Liquidity:   $____
Monthly Burn Rate:           $____
Runway:                      ___ months

--- Key Metrics ---
DSO (current / target):     ___ / ___ days
DPO (current / target):     ___ / ___ days
Cash Conversion Cycle:      ___ days
DSCR (LTM):                 ___x
Free Cash Flow Yield:        ___%

--- Working Capital Drivers ---
                    | Current | Forecast | Δ Cash Impact
Accounts Receivable | $____   | $____    | $____
Inventory           | $____   | $____    | $____
Accounts Payable    | $____   | $____    | $____
Deferred Revenue    | $____   | $____    | $____
Net Working Capital | $____   | $____    | $____
```

## Quality Gate

Before finalizing a cash flow forecast, verify:

- [ ] 13-week forecast is built from actual invoices and payment calendars (Weeks 1-4)
- [ ] Payroll timing matches actual pay dates (biweekly, semi-monthly)
- [ ] Tax payment dates are correct (estimated taxes, VAT/GST, payroll taxes)
- [ ] Collection assumptions are supported by historical DSO and aging analysis
- [ ] Working capital seasonality is reflected (not straight-line annual assumptions)
- [ ] Capex timing reflects actual PO commitments and delivery schedules
- [ ] Debt service payments match loan agreement terms exactly
- [ ] Revolver draws/repayments are modeled to maintain minimum cash balance
- [ ] 13-week total reconciles to the monthly indirect method forecast (within 5%)
- [ ] Liquidity runway is calculated conservatively (minimum cash buffer included)
- [ ] DSCR is above covenant minimum throughout the forecast period
- [ ] Forecast is updated weekly (13-week) or monthly (long-term) with actuals
- [ ] Confidence levels are differentiated (high for near-term, lower for outer weeks)
