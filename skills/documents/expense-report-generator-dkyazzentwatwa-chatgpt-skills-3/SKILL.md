---
name: expense-report-generator
description: Generate formatted expense reports from receipt data or CSV. Create professional PDF reports with categorization, totals, and approval workflows.
---

# Expense Report Generator

Create professional expense reports from receipt data with automatic categorization and totals.

## Features

- **Multiple Input Formats**: CSV, JSON, or manual entry
- **Auto-Categorization**: Classify expenses by type
- **Receipt Tracking**: Link receipts to expenses
- **Approval Workflow**: Status tracking and approver info
- **Policy Compliance**: Flag out-of-policy expenses
- **PDF Export**: Professional formatted reports
- **Reimbursement Calculation**: Track paid/unpaid amounts

## Quick Start

```python
from expense_report import ExpenseReportGenerator

report = ExpenseReportGenerator()

# Set report info
report.set_employee("John Doe", "EMP001", "Engineering")
report.set_period("2024-01-01", "2024-01-31")

# Add expenses
report.add_expense(
    date="2024-01-15",
    description="Client dinner",
    category="Meals",
    amount=125.50,
    receipt="receipt_001.jpg"
)

report.add_expense(
    date="2024-01-18",
    description="Uber to airport",
    category="Transportation",
    amount=45.00
)

# Generate report
report.generate_pdf("expense_report.pdf")
```

## CLI Usage

```bash
# From CSV
python expense_report.py --input expenses.csv --employee "John Doe" --output report.pdf

# With date range
python expense_report.py --input data.csv --start 2024-01-01 --end 2024-01-31 -o report.pdf

# Set department and approver
python expense_report.py --input data.csv --employee "Jane Smith" --dept Sales \
    --approver "Bob Manager" -o report.pdf

# With policy limits
python expense_report.py --input data.csv --policy policy.json -o report.pdf
```

## Input Format

### CSV Format
```csv
date,description,category,amount,receipt,notes
2024-01-15,Client dinner at Restaurant,Meals,125.50,receipt_001.jpg,Met with ABC Corp
2024-01-16,Uber to client site,Transportation,32.00,,
2024-01-17,Office supplies,Supplies,45.99,receipt_002.jpg,
2024-01-18,Flight to NYC,Travel,450.00,flight_confirm.pdf,Project kickoff
```

### JSON Format
```json
{
  "employee": "John Doe",
  "employee_id": "EMP001",
  "department": "Engineering",
  "period": {"start": "2024-01-01", "end": "2024-01-31"},
  "expenses": [
    {
      "date": "2024-01-15",
      "description": "Client dinner",
      "category": "Meals",
      "amount": 125.50,
      "receipt": "receipt_001.jpg"
    }
  ]
}
```

### Policy Configuration
```json
{
  "limits": {
    "Meals": 75,
    "Transportation": 100,
    "Lodging": 250,
    "Supplies": 200
  },
  "requires_receipt": 25,
  "requires_approval": 500,
  "prohibited": ["Alcohol", "Personal items"]
}
```

## API Reference

### ExpenseReportGenerator Class

```python
class ExpenseReportGenerator:
    def __init__(self)

    # Report Setup
    def set_employee(self, name: str, employee_id: str = None,
                    department: str = None) -> 'ExpenseReportGenerator'
    def set_period(self, start: str, end: str) -> 'ExpenseReportGenerator'
    def set_approver(self, name: str, title: str = None) -> 'ExpenseReportGenerator'
    def set_project(self, project_name: str, project_code: str = None) -> 'ExpenseReportGenerator'

    # Adding Expenses
    def add_expense(self, date: str, description: str, category: str,
                   amount: float, receipt: str = None, notes: str = None,
                   reimbursable: bool = True) -> 'ExpenseReportGenerator'
    def load_csv(self, filepath: str) -> 'ExpenseReportGenerator'
    def load_json(self, filepath: str) -> 'ExpenseReportGenerator'

    # Policy
    def set_policy(self, policy: Dict) -> 'ExpenseReportGenerator'
    def check_compliance(self) -> List[Dict]

    # Analysis
    def get_summary(self) -> Dict
    def by_category(self) -> Dict[str, float]
    def by_date(self) -> Dict[str, float]
    def get_total(self) -> float

    # Export
    def generate_pdf(self, output: str) -> str
    def generate_html(self, output: str) -> str
    def to_csv(self, output: str) -> str
    def to_json(self, output: str) -> str
```

## Expense Categories

Standard categories:
- **Meals**: Business meals and entertainment
- **Transportation**: Taxi, rideshare, rental car, parking
- **Travel**: Flights, trains, hotels
- **Lodging**: Hotel, accommodation
- **Supplies**: Office supplies, equipment
- **Communication**: Phone, internet
- **Professional**: Conferences, training, memberships
- **Other**: Miscellaneous expenses

## Report Summary

```python
summary = report.get_summary()
# Returns:
# {
#     "employee": "John Doe",
#     "period": {"start": "2024-01-01", "end": "2024-01-31"},
#     "total_expenses": 1250.50,
#     "expense_count": 15,
#     "categories": {
#         "Meals": 325.00,
#         "Transportation": 180.50,
#         "Travel": 650.00,
#         "Supplies": 95.00
#     },
#     "reimbursable": 1150.50,
#     "non_reimbursable": 100.00,
#     "receipts_attached": 12,
#     "receipts_missing": 3
# }
```

## Policy Compliance

```python
# Set spending limits
report.set_policy({
    "limits": {
        "Meals": 75,      # Per transaction limit
        "Daily_meals": 100  # Daily limit
    },
    "requires_receipt": 25,  # Receipts required above this
    "requires_approval": 500  # Manager approval above this
})

# Check compliance
violations = report.check_compliance()
# Returns:
# [
#     {"expense_id": 3, "type": "over_limit", "category": "Meals",
#      "amount": 125.50, "limit": 75},
#     {"expense_id": 7, "type": "missing_receipt", "amount": 45.00}
# ]
```

## Generated Report Contents

The PDF report includes:

1. **Header**
   - Company logo (optional)
   - Report title and date range
   - Employee information

2. **Summary Section**
   - Total amount
   - Category breakdown
   - Reimbursement status

3. **Expense Details Table**
   - Date, description, category
   - Amount, receipt status
   - Notes

4. **Category Charts**
   - Pie chart of spending by category
   - Daily spending bar chart

5. **Compliance Notes**
   - Policy violations (if any)
   - Missing receipts

6. **Approval Section**
   - Employee signature line
   - Approver signature line
   - Date fields

## Example Workflows

### Monthly Employee Report
```python
report = ExpenseReportGenerator()
report.set_employee("Sarah Johnson", "EMP042", "Marketing")
report.set_period("2024-02-01", "2024-02-29")
report.set_approver("Mike Director", "VP Marketing")

# Load from tracking spreadsheet
report.load_csv("february_expenses.csv")

# Check policy
violations = report.check_compliance()
if violations:
    print(f"Warning: {len(violations)} policy violations")

# Generate report
report.generate_pdf("sarah_feb_expenses.pdf")
print(f"Total: ${report.get_total():,.2f}")
```

### Project Expense Tracking
```python
report = ExpenseReportGenerator()
report.set_employee("Project Team")
report.set_project("Website Redesign", "PRJ-2024-001")
report.set_period("2024-01-01", "2024-03-31")

# Add project expenses
report.add_expense("2024-01-15", "Design software license", "Software", 299.00)
report.add_expense("2024-02-01", "User testing incentives", "Research", 500.00)
report.add_expense("2024-02-20", "Stock photos", "Creative", 150.00)

summary = report.by_category()
print("Project Expenses by Category:")
for cat, amount in summary.items():
    print(f"  {cat}: ${amount:,.2f}")
```

## Dependencies

- pandas>=2.0.0
- reportlab>=4.0.0
- matplotlib>=3.7.0
