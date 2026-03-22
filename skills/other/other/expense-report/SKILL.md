---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: expense-report
description: ">"
version: "1.0.0"
author: Claude Office Skills Contributors
license: MIT

# Categorization
category: finance
tags:
  - expense
  - report
  - reimbursement
department: Finance

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - read_xlsx
    - create_xlsx
    - analyze_spreadsheet

# Skill Capabilities
capabilities:
  - expense_tracking
  - categorization
  - summarization

# Language Support
languages:
  - en
  - zh
---

# Expense Report

## Overview

This skill helps you organize business expenses into clear, categorized reports suitable for reimbursement requests, accounting, and tax preparation.

**Use Cases:**
- Creating expense reimbursement reports
- Organizing receipts for tax preparation
- Categorizing business expenses
- Summarizing travel expenses
- Preparing monthly/quarterly expense summaries

## How to Use

1. Provide your expense information (receipts, transactions, or descriptions)
2. Specify the purpose (reimbursement, tax prep, budget tracking)
3. Tell me your expense categories or policies
4. I'll create a structured expense report

**Example prompts:**
- "Create an expense report from these receipts for my business trip"
- "Categorize and summarize my expenses for the month"
- "Format these expenses for reimbursement"
- "Help me organize my freelance business expenses for taxes"

## Expense Report Templates

### Standard Reimbursement Report

```markdown
# Expense Report

**Employee:** [Name]
**Department:** [Department]
**Report Period:** [Start Date] - [End Date]
**Purpose:** [Business trip / Project / General]
**Submission Date:** [Date]

## Summary
| Category | Amount |
|----------|--------|
| Transportation | $XXX.XX |
| Lodging | $XXX.XX |
| Meals | $XXX.XX |
| Other | $XXX.XX |
| **Total** | **$XXX.XX** |

## Expense Details

### Transportation
| Date | Description | Vendor | Amount | Receipt |
|------|-------------|--------|--------|---------|
| [Date] | [Description] | [Vendor] | $XX.XX | ✓ |

### Lodging
| Date | Description | Vendor | Amount | Receipt |
|------|-------------|--------|--------|---------|
| [Date] | [Hotel name] | [Vendor] | $XX.XX | ✓ |

### Meals & Entertainment
| Date | Description | Attendees | Business Purpose | Amount | Receipt |
|------|-------------|-----------|------------------|--------|---------|
| [Date] | [Restaurant] | [Names] | [Purpose] | $XX.XX | ✓ |

### Other Expenses
| Date | Description | Category | Amount | Receipt |
|------|-------------|----------|--------|---------|
| [Date] | [Description] | [Category] | $XX.XX | ✓ |

## Approvals
- [ ] Employee Signature: _____________ Date: _______
- [ ] Manager Approval: _____________ Date: _______
- [ ] Finance Approval: _____________ Date: _______

## Notes
[Any additional context or explanations]
```

### Travel Expense Report

```markdown
# Travel Expense Report

**Traveler:** [Name]
**Trip Dates:** [Start] - [End]
**Destination:** [City, Country]
**Business Purpose:** [Reason for travel]

## Trip Summary
- **Duration:** [X] days
- **Total Expenses:** $X,XXX.XX
- **Per Diem Allowance:** $XXX.XX
- **Variance:** +/- $XX.XX

## Pre-Trip Expenses
| Item | Vendor | Amount | Date Paid |
|------|--------|--------|-----------|
| Flight | [Airline] | $XXX.XX | [Date] |
| Hotel Booking | [Hotel] | $XXX.XX | [Date] |
| Conference Registration | [Event] | $XXX.XX | [Date] |

## Daily Expenses

### Day 1 - [Date]
| Category | Description | Amount |
|----------|-------------|--------|
| Transport | Airport taxi | $XX.XX |
| Meals | Dinner | $XX.XX |
| **Day Total** | | **$XX.XX** |

### Day 2 - [Date]
| Category | Description | Amount |
|----------|-------------|--------|
| Meals | Breakfast/Lunch/Dinner | $XX.XX |
| Transport | Uber to meeting | $XX.XX |
| **Day Total** | | **$XX.XX** |

## Expense by Category
| Category | Amount | % of Total |
|----------|--------|------------|
| Airfare | $XXX.XX | XX% |
| Lodging | $XXX.XX | XX% |
| Ground Transport | $XXX.XX | XX% |
| Meals | $XXX.XX | XX% |
| Other | $XXX.XX | XX% |
| **Total** | **$X,XXX.XX** | 100% |

## Receipt Checklist
- [ ] Flight confirmation/receipt
- [ ] Hotel invoice
- [ ] Ground transportation receipts
- [ ] Meal receipts over $[threshold]
- [ ] Other expense receipts
```

### Monthly Expense Summary

```markdown
# Monthly Expense Summary

**Period:** [Month Year]
**Prepared by:** [Name]
**Business:** [Business Name]

## Overview
| Metric | Amount |
|--------|--------|
| Total Expenses | $X,XXX.XX |
| vs Last Month | +/-XX% |
| vs Budget | +/-XX% |

## Expenses by Category

### Operating Expenses
| Category | Amount | Budget | Variance |
|----------|--------|--------|----------|
| Rent/Utilities | $XXX.XX | $XXX.XX | $XX.XX |
| Software/Subscriptions | $XXX.XX | $XXX.XX | $XX.XX |
| Office Supplies | $XXX.XX | $XXX.XX | $XX.XX |

### Professional Services
| Category | Amount | Budget | Variance |
|----------|--------|--------|----------|
| Legal | $XXX.XX | $XXX.XX | $XX.XX |
| Accounting | $XXX.XX | $XXX.XX | $XX.XX |
| Consulting | $XXX.XX | $XXX.XX | $XX.XX |

### Marketing & Sales
| Category | Amount | Budget | Variance |
|----------|--------|--------|----------|
| Advertising | $XXX.XX | $XXX.XX | $XX.XX |
| Events | $XXX.XX | $XXX.XX | $XX.XX |
| Travel | $XXX.XX | $XXX.XX | $XX.XX |

## Top 10 Expenses
| Rank | Date | Description | Category | Amount |
|------|------|-------------|----------|--------|
| 1 | [Date] | [Description] | [Category] | $XXX.XX |
| 2 | [Date] | [Description] | [Category] | $XXX.XX |

## Notes & Anomalies
- [Explanation for any unusual expenses]
- [Budget variance explanations]
```

## Expense Categories

### Common Business Categories

| Category | Examples | Tax Deductible |
|----------|----------|----------------|
| **Travel** | Flights, hotels, car rentals | Usually yes |
| **Meals & Entertainment** | Client dinners, team lunches | 50-100% |
| **Transportation** | Taxi, Uber, parking, mileage | Yes |
| **Office Supplies** | Paper, pens, printer ink | Yes |
| **Software & Subscriptions** | SaaS tools, apps | Yes |
| **Professional Development** | Courses, books, conferences | Usually yes |
| **Communication** | Phone, internet | Partial |
| **Professional Services** | Legal, accounting | Yes |
| **Marketing** | Ads, promotional materials | Yes |
| **Equipment** | Computer, office furniture | Depreciated |

### IRS Category Alignment (US)

| IRS Category | Description |
|--------------|-------------|
| Advertising | Marketing and promotional |
| Car and Truck | Vehicle expenses |
| Commissions | Payments to contractors |
| Contract Labor | Freelancer payments |
| Depreciation | Asset depreciation |
| Insurance | Business insurance |
| Interest | Business loan interest |
| Legal and Professional | Attorney, CPA fees |
| Office Expense | General office |
| Rent | Workspace rental |
| Repairs | Equipment maintenance |
| Supplies | Business supplies |
| Taxes and Licenses | Business taxes |
| Travel | Business travel |
| Meals | Business meals (50%) |
| Utilities | Business utilities |

## Processing Guidelines

### Receipt Requirements
- **Keep receipts for:** All expenses over $25 (US) or local threshold
- **Required info:** Date, vendor, amount, payment method
- **Meals:** Include attendees and business purpose
- **Missing receipts:** Note explanation in report

### Currency Conversion
- Use exchange rate from date of expense
- Document rate source (bank, XE.com, etc.)
- Keep in original currency + converted amount

### Mileage Calculation
- Current IRS rate (2024): $0.67/mile (verify current rate)
- Document: Date, destination, purpose, miles
- Use odometer readings or mapping app

## Output Format

```markdown
# Expense Report

**Period:** [Dates]
**Total:** $X,XXX.XX

## Summary by Category
[Category breakdown table]

## Detailed Expenses
[Line items with all required info]

## Missing/Notes
[Any issues to address]
```

## Limitations

- Cannot scan or read receipt images directly
- Tax advice should be verified with a professional
- Exchange rates should be verified for accuracy
- Company policies may have specific requirements
- Cannot submit reports to your expense system

## Examples

### Example: Quick Expense Organization

**Input:**
```
uber to airport $45
flight to NYC $380
hotel 2 nights $420
dinner with client john from acme $125
coffee and breakfast $35
uber to meetings $28
lunch meeting $65
return flight $395
uber home $42
```

**Output:**

# Travel Expense Report

**Trip:** NYC Client Visit
**Dates:** [Dates based on context]
**Purpose:** Client meeting with Acme Corp

## Summary
| Category | Amount |
|----------|--------|
| Airfare | $775.00 |
| Lodging | $420.00 |
| Ground Transportation | $115.00 |
| Meals & Entertainment | $225.00 |
| **Total** | **$1,535.00** |

## Detailed Expenses

### Airfare
| Date | Description | Amount | Receipt |
|------|-------------|--------|---------|
| [Day 1] | Flight to NYC | $380.00 | Needed |
| [Day 3] | Return flight | $395.00 | Needed |
| **Subtotal** | | **$775.00** | |

### Lodging
| Date | Description | Amount | Receipt |
|------|-------------|--------|---------|
| [Day 1-2] | Hotel (2 nights) | $420.00 | Needed |

### Ground Transportation
| Date | Description | Amount | Receipt |
|------|-------------|--------|---------|
| [Day 1] | Uber to airport | $45.00 | ✓ App |
| [Day 2] | Uber to meetings | $28.00 | ✓ App |
| [Day 3] | Uber to home | $42.00 | ✓ App |
| **Subtotal** | | **$115.00** | |

### Meals & Entertainment
| Date | Description | Attendees | Purpose | Amount | Receipt |
|------|-------------|-----------|---------|--------|---------|
| [Day 1] | Client dinner | John (Acme) | Account review | $125.00 | Needed |
| [Day 2] | Breakfast/coffee | Self | Working meal | $35.00 | Optional |
| [Day 2] | Lunch meeting | [TBD] | [Purpose] | $65.00 | Needed |
| **Subtotal** | | | | **$225.00** | |

## Action Items
- [ ] Collect flight confirmation emails
- [ ] Get hotel invoice/folio
- [ ] Save restaurant receipts for meals over $25
- [ ] Document business purpose for client dinner
- [ ] Confirm lunch meeting attendees
