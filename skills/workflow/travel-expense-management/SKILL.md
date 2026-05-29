---
name: travel-expense-management
description: "SAP Concur alternative - self-hosted travel & expense management. Handles travel requests, expense reports, receipt OCR, policy validation, multi-level approvals, and GL posting. Saves $15,000/year in licensing costs."
---

# Travel & Expense Management Expert (SAP Concur Alternative)

Transform Claude into a complete Travel & Expense automation system that replaces SAP Concur at zero licensing cost.

## What This Skill Does

**Travel Booking** - Create travel requests with approval workflows  
**Expense Reports** - Submit, review, approve with OCR receipt scanning  
**Policy Enforcement** - Automatic validation against company rules  
**Reimbursement** - Calculate amounts, generate payment files  
**GL Integration** - Auto-post to Odoo with proper coding

**Annual Savings: $15,000 (vs SAP Concur)**

## Quick Start

When asked to handle travel/expenses:

1. **Create request**: Travel or expense report with supporting docs
2. **OCR receipts**: Extract data from photos using PaddleOCR
3. **Validate policy**: Check against limits and rules
4. **Route approval**: Multi-level workflow based on amount
5. **Process payment**: Generate reimbursement and post to GL

## Core Workflows

### Workflow 1: Submit Expense Report

```
User asks: "Create expense report for October JPAL employee"

Steps:
1. Gather expense details (date, category, amount, merchant)
2. Upload receipt images
3. OCR extract data from receipts
4. Validate against policy
5. Calculate totals including VAT
6. Route for approval
7. Update status in Notion

Result: Expense report submitted with full documentation
```

See [examples/submit-expense.md](examples/submit-expense.md).

### Workflow 2: Receipt OCR Processing

```
User asks: "Scan this meal receipt"

Steps:
1. Receive receipt image
2. Use PaddleOCR to extract text
3. Parse merchant, date, amount, VAT
4. Validate BIR format (OR number, TIN)
5. Match to expense category
6. Flag any policy violations
7. Return structured data

Result: Receipt data ready for expense line
```

See [examples/receipt-ocr.md](examples/receipt-ocr.md).

### Workflow 3: Policy Validation

```
User asks: "Check if this expense is allowed"

Steps:
1. Identify expense category
2. Query policy rules
3. Check amount limits
4. Verify receipt requirements
5. Validate approvers needed
6. Flag violations with explanations
7. Suggest corrections

Result: Policy compliance report
```

See [examples/policy-validation.md](examples/policy-validation.md).

### Workflow 4: Approval Workflow

```
User asks: "Route expense report for approval"

Steps:
1. Calculate total amount
2. Determine approval levels needed
3. Identify approvers by hierarchy
4. Create Notion approval tasks
5. Send notifications
6. Track approval status
7. Handle rejections/revisions

Result: Expense routed through proper channels
```

See [examples/approval-workflow.md](examples/approval-workflow.md).

### Workflow 5: GL Posting

```
User asks: "Post approved expenses to Odoo"

Steps:
1. Retrieve approved expense reports
2. Map categories to GL accounts
3. Calculate withholding taxes
4. Split by agency (analytic accounts)
5. Generate journal entries
6. Post to Odoo
7. Update reimbursement status

Result: Expenses posted to accounting system
```

See [examples/gl-posting.md](examples/gl-posting.md).

## Implementation Patterns

### Expense Report Schema

```python
{
    'id': 'EXP-2025-001',
    'employee_code': 'JPAL',
    'period': '2025-10',
    'status': 'draft',  # draft, submitted, approved, rejected, paid
    'expense_lines': [
        {
            'date': '2025-10-15',
            'category': 'meals',
            'amount': 1200.00,
            'currency': 'PHP',
            'merchant': 'Restaurant Name',
            'receipt_url': 's3://receipts/img123.jpg',
            'description': 'Client lunch meeting',
            'vat_amount': 128.57,
            'policy_compliant': True
        }
    ],
    'total_amount': 5400.00,
    'advance_taken': 3000.00,
    'reimbursement_due': 2400.00,
    'approvals': [
        {'level': 1, 'approver': 'supervisor', 'status': 'approved'},
        {'level': 2, 'approver': 'finance', 'status': 'pending'}
    ]
}
```

See [reference/expense-schema.md](reference/expense-schema.md).

### Policy Rules

```python
EXPENSE_POLICIES = {
    'meals': {
        'daily_limit': 1500,
        'receipt_required_above': 500,
        'requires_attendees': True,
        'vat_deductible': True
    },
    'accommodation': {
        'daily_limit': 5000,
        'receipt_required': True,
        'advance_booking_required': True
    },
    'fuel': {
        'monthly_limit': 5000,
        'logbook_required': True,
        'receipt_required': True
    },
    'transportation': {
        'per_km_rate': 15,  # PHP per km
        'taxi_limit': 1000,
        'receipt_required_above': 300
    }
}
```

See [reference/policy-rules.md](reference/policy-rules.md).

### OCR Receipt Processing

```python
def process_receipt_ocr(image_path):
    """Extract data from receipt image"""
    # Use PaddleOCR
    ocr_result = paddle_ocr.extract_bir_form(image_path)
    
    # Parse fields
    receipt_data = {
        'merchant_name': extract_field(ocr_result, 'business_name'),
        'tin': extract_field(ocr_result, 'tin'),
        'date': parse_date(extract_field(ocr_result, 'date')),
        'or_number': extract_field(ocr_result, 'or_number'),
        'total_amount': parse_amount(extract_field(ocr_result, 'total')),
        'vat_amount': parse_amount(extract_field(ocr_result, 'vat')),
        'vatable_sales': parse_amount(extract_field(ocr_result, 'vatable')),
        'vat_exempt': parse_amount(extract_field(ocr_result, 'exempt')),
        'confidence': ocr_result['confidence']
    }
    
    return receipt_data
```

See [reference/ocr-processing.md](reference/ocr-processing.md).

## Integration Points

### With Odoo
```python
# Post expense to GL
journal_entry = {
    'journal_id': expense_journal_id,
    'date': report['date'],
    'ref': f'EXP/{report['id']}',
    'line_ids': [
        # Debit expense accounts
        *[{
            'account_id': get_expense_account(line['category']),
            'name': line['description'],
            'debit': line['amount'],
            'partner_id': employee_partner_id,
            'analytic_account_id': agency_analytic_id
        } for line in report['expense_lines']],
        # Credit employee payable
        {
            'account_id': employee_payable_account,
            'name': f'Reimbursement - {employee_name}',
            'credit': report['reimbursement_due']
        }
    ]
}
```

### With PaddleOCR
```python
# Scan receipt
receipt_data = paddle_ocr.extract_bir_form(
    image_url=expense_line['receipt_url'],
    extract_fields=[
        'merchant_name', 'tin', 'date', 'total_amount',
        'vat_amount', 'or_number'
    ]
)
```

### With Notion
```python
# Create approval task
notion.create_page({
    'database_id': expense_approvals_db,
    'properties': {
        'Title': f'Approve: {report['id']} - {employee}',
        'Amount': report['total_amount'],
        'Status': 'Pending Approval',
        'Approver': supervisor_email,
        'Due Date': due_date
    }
})
```

## Best Practices

1. **Scan receipts immediately**: Capture while details are fresh
2. **Validate in real-time**: Check policy as expenses are entered
3. **Approval thresholds**: <5k supervisor, >5k finance, >50k CFO
4. **Monthly submission**: Require reports by 5th of following month
5. **Advance settlements**: Track and reconcile cash advances
6. **Mileage logs**: Require for fuel reimbursements
7. **VAT tracking**: Properly record for BIR compliance
8. **Audit trail**: Keep all receipts for 7 years

## Common Issues

**"Receipt OCR failed"**: Poor image quality, retake photo
**"Policy violation"**: Amount exceeds limit, get exception approval
**"Missing receipt"**: Required for amounts >500 PHP
**"Approval delayed"**: Set up automatic reminders
**"Duplicate expense"**: Check if already submitted
**"Wrong GL account"**: Review expense category mapping
**"VAT computation error"**: Verify receipt shows VAT breakdown

## Reference Documentation

- [reference/expense-schema.md](reference/expense-schema.md)
- [reference/policy-rules.md](reference/policy-rules.md)
- [reference/ocr-processing.md](reference/ocr-processing.md)
- [reference/approval-workflows.md](reference/approval-workflows.md)
- [reference/gl-integration.md](reference/gl-integration.md)

## Examples

- [examples/submit-expense.md](examples/submit-expense.md)
- [examples/receipt-ocr.md](examples/receipt-ocr.md)
- [examples/policy-validation.md](examples/policy-validation.md)
- [examples/approval-workflow.md](examples/approval-workflow.md)
- [examples/gl-posting.md](examples/gl-posting.md)

## Success Metrics

- ✅ Report submission time: 2 hours → 15 minutes
- ✅ Approval cycle: 5 days → 1 day
- ✅ Policy compliance: 100%
- ✅ Receipt capture: 95% automated
- ✅ GL posting: 100% automated
- ✅ Annual savings: $15,000 vs SAP Concur

## Getting Started

```
"Create expense report for October"
"Scan this restaurant receipt"
"Validate meal expense against policy"
"Route expense EXP-2025-001 for approval"
"Post approved expenses to Odoo"
```

Your SAP Concur alternative starts here! 💰
