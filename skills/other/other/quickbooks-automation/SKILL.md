---
name: QuickBooks Automation
description: Automate QuickBooks accounting workflows including invoicing, expenses, reporting, and bank reconciliation
version: 1.0.0
author: Claude Office Skills
category: accounting
tags:
  - quickbooks
  - accounting
  - invoicing
  - bookkeeping
  - finance
department: finance
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: accounting-mcp
  tools:
    - qb_invoice
    - qb_expense
    - qb_customer
    - qb_reports
capabilities:
  - Invoice management
  - Expense tracking
  - Financial reporting
  - Bank reconciliation
input:
  - Transaction data
  - Customer information
  - Expense receipts
  - Bank statements
output:
  - Invoices
  - Financial reports
  - Reconciliation status
  - Tax summaries
languages:
  - en
related_skills:
  - invoice-automation
  - expense-tracker
  - financial-modeling
---

# QuickBooks Automation

Comprehensive skill for automating QuickBooks accounting and bookkeeping workflows.

## Core Workflows

### 1. Accounting Pipeline

```
QUICKBOOKS AUTOMATION FLOW:
┌─────────────────────────────────────────────────────────┐
│                    DATA ENTRY                            │
│  Invoices │ Expenses │ Payments │ Bank Feeds            │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   CATEGORIZATION                         │
│  Chart of Accounts │ Classes │ Locations                │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   RECONCILIATION                         │
│  Bank Matching │ Credit Card │ Clearing                 │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    REPORTING                             │
│  P&L │ Balance Sheet │ Cash Flow │ Tax Reports          │
└─────────────────────────────────────────────────────────┘
```

### 2. Automation Rules

```yaml
automation_rules:
  - name: auto_categorize_amazon
    trigger:
      vendor: "Amazon"
    action:
      account: "Office Supplies"
      class: "Operations"
      
  - name: auto_categorize_payroll
    trigger:
      vendor: "Gusto"
    action:
      account: "Payroll Expenses"
      split:
        - account: "Salaries"
          percentage: 85
        - account: "Payroll Taxes"
          percentage: 15
          
  - name: invoice_reminder
    trigger:
      invoice_days_overdue: 7
    action:
      send_reminder_email: true
      add_late_fee: false
```

## Invoice Management

### Invoice Creation

```yaml
invoice_template:
  customer:
    name: "{{customer_name}}"
    email: "{{customer_email}}"
    billing_address: "{{billing_address}}"
    
  header:
    invoice_number: "INV-{{auto_increment}}"
    invoice_date: "{{today}}"
    due_date: "{{today + 30}}"
    terms: "Net 30"
    
  line_items:
    - description: "{{service_description}}"
      quantity: "{{quantity}}"
      rate: "{{unit_price}}"
      amount: "{{quantity * unit_price}}"
      account: "Services Revenue"
      
  footer:
    subtotal: "{{sum_line_items}}"
    tax_rate: "{{tax_percent}}"
    tax_amount: "{{subtotal * tax_rate}}"
    total: "{{subtotal + tax_amount}}"
    
  delivery:
    send_email: true
    cc_accountant: false
    attach_pdf: true
```

### Recurring Invoices

```yaml
recurring_invoices:
  - name: Monthly Retainer
    customer: "Acme Corp"
    frequency: monthly
    day_of_month: 1
    amount: 5000
    description: "Monthly consulting retainer"
    auto_send: true
    
  - name: Quarterly Subscription
    customer: "TechStart Inc"
    frequency: quarterly
    start_date: "2024-01-01"
    amount: 2500
    description: "Q{{quarter}} Software Subscription"
    auto_send: true
```

## Expense Tracking

### Expense Categories

```yaml
expense_categories:
  operating_expenses:
    - Advertising
    - Bank Charges
    - Insurance
    - Legal & Professional
    - Office Supplies
    - Rent
    - Utilities
    
  cost_of_goods:
    - Materials
    - Shipping
    - Direct Labor
    
  payroll:
    - Salaries & Wages
    - Payroll Taxes
    - Employee Benefits
```

### Receipt Processing

```yaml
receipt_automation:
  capture:
    sources:
      - email_forward
      - mobile_app
      - bank_feed
      
  extraction:
    fields:
      - vendor
      - date
      - amount
      - payment_method
      
  matching:
    auto_match:
      threshold: 0.95
      rules:
        - amount_exact
        - date_within_3_days
        - vendor_fuzzy_match
        
  categorization:
    use_history: true
    default_category: "Ask Accountant"
```

## Bank Reconciliation

### Bank Feed Rules

```yaml
bank_rules:
  - name: Stripe Deposits
    conditions:
      description_contains: "STRIPE"
    action:
      category: "Sales Revenue"
      class: "Online Sales"
      auto_match_invoices: true
      
  - name: Payroll
    conditions:
      description_contains: "GUSTO"
      amount_range: [-50000, -1000]
    action:
      category: "Payroll"
      split_by_historical: true
      
  - name: AWS Charges
    conditions:
      description_contains: "AMAZON WEB SERVICES"
    action:
      category: "Cloud Hosting"
      class: "Technology"
```

### Reconciliation Dashboard

```
BANK RECONCILIATION STATUS
═══════════════════════════════════════

Account: Business Checking ****4567

Bank Balance:       $125,450.23
QuickBooks Balance: $124,890.45
Difference:         $559.78

UNMATCHED TRANSACTIONS:
┌────────────┬────────────────────┬──────────┐
│ Date       │ Description        │ Amount   │
├────────────┼────────────────────┼──────────┤
│ 01/15      │ CHECK #1234        │ $450.00  │
│ 01/16      │ WIRE TRANSFER      │ $109.78  │
└────────────┴────────────────────┴──────────┘

PENDING ITEMS:
Outstanding Checks:  $1,234.50
Deposits in Transit: $674.72

LAST RECONCILED: January 10, 2024
```

## Financial Reports

### Standard Reports

```yaml
reports:
  profit_loss:
    type: standard
    period: this_month
    comparison: previous_period
    columns:
      - actual
      - budget
      - variance
      - percent_change
      
  balance_sheet:
    type: standard
    as_of_date: period_end
    show_totals: true
    
  cash_flow:
    type: standard
    method: indirect
    period: this_quarter
    
  ar_aging:
    type: aging
    aging_buckets: [30, 60, 90, 120]
    
  ap_aging:
    type: aging
    aging_buckets: [30, 60, 90]
```

### Report Dashboard

```
FINANCIAL DASHBOARD - JANUARY 2024
═══════════════════════════════════════

PROFIT & LOSS:
Revenue:          $185,450
COGS:             $45,230
Gross Profit:     $140,220 (75.6%)
Operating Exp:    $82,340
Net Income:       $57,880 (31.2%)

vs. Budget:
Revenue     ████████████████░░ +8%
Expenses    ██████████████░░░░ -3%
Profit      ██████████████████ +15%

BALANCE SHEET:
Assets:           $456,780
Liabilities:      $123,450
Equity:           $333,330

CASH POSITION:
Operating Cash:   $125,450
Receivables:      $89,230
Payables:         $34,560
Net Cash:         $180,120

AR AGING:
Current     ████████████████ $45,230
1-30 days   ████████░░░░░░░░ $23,450
31-60 days  ████░░░░░░░░░░░░ $12,340
61-90 days  ██░░░░░░░░░░░░░░ $5,670
90+ days    █░░░░░░░░░░░░░░░ $2,540
```

## Integration Workflows

### E-commerce Sync

```yaml
shopify_sync:
  frequency: daily
  
  orders:
    create_invoice: true
    match_customer: true
    create_customer_if_new: true
    
  products:
    sync_inventory: true
    update_cogs: true
    
  payments:
    record_deposits: true
    account: "Undeposited Funds"
    
  refunds:
    create_credit_memo: true
    link_to_original: true
```

### Payroll Integration

```yaml
gusto_sync:
  frequency: per_payroll
  
  mapping:
    gross_pay: "Salaries & Wages"
    employer_taxes: "Payroll Taxes"
    benefits: "Employee Benefits"
    
  journal_entry:
    debit:
      - account: "Payroll Expenses"
        amount: total_gross
    credit:
      - account: "Payroll Liabilities"
        amount: withholdings
      - account: "Cash"
        amount: net_pay
```

## API Examples

### Create Invoice

```javascript
// QuickBooks API - Create Invoice
const invoice = {
  CustomerRef: {
    value: "123"
  },
  Line: [
    {
      DetailType: "SalesItemLineDetail",
      Amount: 1000,
      SalesItemLineDetail: {
        ItemRef: { value: "1" },
        Qty: 10,
        UnitPrice: 100
      }
    }
  ],
  DueDate: "2024-02-15"
};

const response = await qbo.createInvoice(invoice);
```

### Query Transactions

```javascript
// Query recent expenses
const expenses = await qbo.findPurchases({
  TxnDate: { $gt: '2024-01-01' },
  AccountRef: { value: '50' } // Operating Expenses
});

// Query unpaid invoices
const unpaid = await qbo.findInvoices({
  Balance: { $gt: 0 },
  DueDate: { $lt: new Date().toISOString() }
});
```

## Best Practices

1. **Daily Bank Feed Review**: Match transactions promptly
2. **Consistent Categorization**: Use standard chart of accounts
3. **Monthly Reconciliation**: Close books monthly
4. **Document Attachment**: Attach receipts to transactions
5. **Class Tracking**: Use for department/project tracking
6. **Regular Backups**: Export data periodically
7. **Access Controls**: Limit user permissions
8. **Audit Trail**: Review changes regularly
