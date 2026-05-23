---
name: budget-analyzer
description: Analyze personal or business expenses from CSV/Excel. Categorize spending, identify trends, compare periods, and get savings recommendations.
---

# Budget Analyzer

Comprehensive expense analysis tool for personal finance and business budgeting.

## Features

- **Auto-Categorization**: Classify expenses by merchant/description
- **Trend Analysis**: Month-over-month spending patterns
- **Period Comparison**: Compare spending across time periods
- **Category Breakdown**: Pie charts and bar graphs by category
- **Savings Recommendations**: Identify areas to reduce spending
- **Budget vs Actual**: Track against budget targets
- **Export Reports**: PDF and HTML summaries

## Quick Start

```python
from budget_analyzer import BudgetAnalyzer

analyzer = BudgetAnalyzer()

# Load transaction data
analyzer.load_csv("transactions.csv",
                  date_col="date",
                  amount_col="amount",
                  description_col="description")

# Analyze spending
summary = analyzer.analyze()
print(summary)

# Get category breakdown
categories = analyzer.by_category()
print(categories)

# Generate report
analyzer.generate_report("budget_report.pdf")
```

## CLI Usage

```bash
# Basic analysis
python budget_analyzer.py --input transactions.csv --date date --amount amount

# With custom categories
python budget_analyzer.py --input data.csv --categories custom_categories.json

# Compare two periods
python budget_analyzer.py --input data.csv --compare "2024-01" "2024-02"

# Generate PDF report
python budget_analyzer.py --input data.csv --report report.pdf

# Set budget targets
python budget_analyzer.py --input data.csv --budget budget.json --report report.pdf
```

## Input Format

### Transaction CSV
```csv
date,amount,description,category
2024-01-15,45.99,Amazon Purchase,Shopping
2024-01-16,12.50,Starbucks,Food & Dining
2024-01-17,150.00,Electric Company,Utilities
```

### Custom Categories (JSON)
```json
{
  "Food & Dining": ["starbucks", "mcdonalds", "restaurant", "uber eats"],
  "Transportation": ["uber", "lyft", "gas station", "shell"],
  "Shopping": ["amazon", "walmart", "target"],
  "Utilities": ["electric", "water", "gas", "internet"]
}
```

### Budget Targets (JSON)
```json
{
  "Food & Dining": 500,
  "Transportation": 200,
  "Shopping": 300,
  "Utilities": 250,
  "Entertainment": 150
}
```

## API Reference

### BudgetAnalyzer Class

```python
class BudgetAnalyzer:
    def __init__(self)

    # Data Loading
    def load_csv(self, filepath: str, date_col: str, amount_col: str,
                 description_col: str = None, category_col: str = None) -> 'BudgetAnalyzer'
    def load_dataframe(self, df: pd.DataFrame) -> 'BudgetAnalyzer'

    # Categorization
    def set_categories(self, categories: Dict[str, List[str]]) -> 'BudgetAnalyzer'
    def auto_categorize(self) -> 'BudgetAnalyzer'

    # Analysis
    def analyze(self) -> Dict  # Full summary
    def by_category(self) -> pd.DataFrame
    def by_month(self) -> pd.DataFrame
    def by_day_of_week(self) -> pd.DataFrame
    def top_expenses(self, n: int = 10) -> pd.DataFrame
    def recurring_expenses(self) -> pd.DataFrame

    # Comparison
    def compare_periods(self, period1: str, period2: str) -> Dict
    def year_over_year(self) -> pd.DataFrame

    # Budgeting
    def set_budget(self, budget: Dict[str, float]) -> 'BudgetAnalyzer'
    def budget_vs_actual(self) -> pd.DataFrame
    def budget_alerts(self) -> List[Dict]

    # Insights
    def get_recommendations(self) -> List[str]
    def spending_score(self) -> Dict

    # Visualization
    def plot_categories(self, output: str) -> str
    def plot_trends(self, output: str) -> str
    def plot_budget_comparison(self, output: str) -> str

    # Export
    def generate_report(self, output: str, format: str = "pdf") -> str
    def to_csv(self, output: str) -> str
```

## Analysis Features

### Summary Statistics
```python
summary = analyzer.analyze()
# Returns:
# {
#     "total_spent": 2500.00,
#     "transaction_count": 45,
#     "date_range": {"start": "2024-01-01", "end": "2024-01-31"},
#     "average_transaction": 55.56,
#     "largest_expense": {"amount": 500, "description": "Rent"},
#     "categories": {"Food": 450, "Transport": 200, ...}
# }
```

### Category Breakdown
```python
categories = analyzer.by_category()
# Returns DataFrame:
#   category        | amount  | percentage | count
#   Food & Dining   | 450.00  | 18.0%      | 15
#   Transportation  | 200.00  | 8.0%       | 8
#   ...
```

### Monthly Trends
```python
monthly = analyzer.by_month()
# Returns DataFrame:
#   month    | total    | avg_transaction | count
#   2024-01  | 2500.00  | 55.56          | 45
#   2024-02  | 2800.00  | 60.87          | 46
```

### Period Comparison
```python
comparison = analyzer.compare_periods("2024-01", "2024-02")
# Returns:
# {
#     "period1_total": 2500.00,
#     "period2_total": 2800.00,
#     "difference": 300.00,
#     "percent_change": 12.0,
#     "category_changes": {
#         "Food": {"change": 50, "percent": 11.1},
#         ...
#     }
# }
```

## Budget Tracking

### Set Budget Targets
```python
analyzer.set_budget({
    "Food & Dining": 500,
    "Transportation": 200,
    "Shopping": 300
})
```

### Budget vs Actual
```python
comparison = analyzer.budget_vs_actual()
# Returns DataFrame:
#   category        | budget | actual | difference | status
#   Food & Dining   | 500    | 450    | 50         | under
#   Transportation  | 200    | 250    | -50        | over
```

### Budget Alerts
```python
alerts = analyzer.budget_alerts()
# Returns:
# [
#     {"category": "Transportation", "status": "over", "amount": 250, "budget": 200, "percent_over": 25},
#     {"category": "Shopping", "status": "warning", "amount": 280, "budget": 300, "percent_used": 93}
# ]
```

## Recommendations Engine

```python
recommendations = analyzer.get_recommendations()
# Returns:
# [
#     "Food & Dining spending increased 15% from last month. Consider meal prepping.",
#     "You have 3 subscription services totaling $45/month. Review for unused subscriptions.",
#     "Transportation costs are 25% over budget. Consider carpooling or public transit.",
#     "Top merchant: Amazon ($350). Set spending limits for online shopping."
# ]
```

## Spending Score

```python
score = analyzer.spending_score()
# Returns:
# {
#     "overall_score": 72,  # 0-100
#     "factors": {
#         "budget_adherence": 65,
#         "spending_consistency": 80,
#         "savings_rate": 70
#     },
#     "grade": "B",
#     "summary": "Good spending habits with room for improvement in budget adherence."
# }
```

## Auto-Categorization

Built-in category patterns:
```python
DEFAULT_CATEGORIES = {
    "Food & Dining": ["restaurant", "cafe", "starbucks", "mcdonald", "uber eats", "doordash"],
    "Transportation": ["uber", "lyft", "gas", "shell", "chevron", "parking"],
    "Shopping": ["amazon", "walmart", "target", "costco", "best buy"],
    "Utilities": ["electric", "water", "gas", "internet", "phone", "verizon"],
    "Entertainment": ["netflix", "spotify", "hulu", "movie", "theater"],
    "Healthcare": ["pharmacy", "cvs", "walgreens", "doctor", "hospital"],
    "Travel": ["airline", "hotel", "airbnb", "booking"],
    "Subscriptions": ["subscription", "membership", "monthly"]
}
```

## Visualizations

### Category Pie Chart
```python
analyzer.plot_categories("categories.png")
# Creates pie chart of spending by category
```

### Spending Trends
```python
analyzer.plot_trends("trends.png")
# Creates line chart of monthly spending over time
```

### Budget Comparison
```python
analyzer.plot_budget_comparison("budget.png")
# Creates bar chart comparing budget vs actual by category
```

## Report Generation

### PDF Report
```python
analyzer.generate_report("report.pdf")
# Includes:
# - Executive summary
# - Category breakdown with charts
# - Monthly trends
# - Top expenses
# - Budget vs actual (if set)
# - Recommendations
```

### HTML Report
```python
analyzer.generate_report("report.html", format="html")
# Interactive HTML report with charts
```

## Example Workflows

### Personal Finance Review
```python
analyzer = BudgetAnalyzer()
analyzer.load_csv("bank_transactions.csv",
                  date_col="Date",
                  amount_col="Amount",
                  description_col="Description")

# Auto-categorize transactions
analyzer.auto_categorize()

# Set monthly budget
analyzer.set_budget({
    "Food & Dining": 600,
    "Transportation": 250,
    "Entertainment": 200
})

# Get full analysis
print(analyzer.analyze())
print(analyzer.budget_vs_actual())
print(analyzer.get_recommendations())

# Generate report
analyzer.generate_report("monthly_review.pdf")
```

### Business Expense Tracking
```python
analyzer = BudgetAnalyzer()
analyzer.load_csv("business_expenses.csv",
                  date_col="date",
                  amount_col="amount",
                  category_col="expense_type")

# Compare quarters
q1_vs_q2 = analyzer.compare_periods("2024-Q1", "2024-Q2")

# Top expense categories
top = analyzer.by_category().head(5)

# Generate report for accounting
analyzer.generate_report("quarterly_expenses.pdf")
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
- reportlab>=4.0.0
