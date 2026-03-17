---
name: finance-manager
description: Comprehensive personal finance management system for analyzing transaction data, generating insights, creating visualizations, and providing actionable financial recommendations. Use when users need to analyze spending patterns, track budgets, visualize financial data, extract transactions from PDFs, calculate savings rates, identify spending trends, generate financial reports, or receive personalized budget recommendations. Triggers include requests like "analyze my finances", "track my spending", "create a financial report", "extract transactions from PDF", "visualize my budget", "where is my money going", "financial insights", "spending breakdown", or any finance-related analysis tasks.
---

# Finance Manager

A comprehensive toolkit for personal finance management that processes transaction data, performs sophisticated financial analysis, generates actionable insights, and creates beautiful visual reports.

## Core Capabilities

1. **Transaction Data Processing**: Extract financial data from PDFs, CSVs, or JSON files
2. **Financial Analysis**: Calculate key metrics, identify spending patterns, and track savings
3. **Visualization**: Generate interactive HTML reports with charts and graphs
4. **Budget Recommendations**: Provide personalized, actionable advice based on spending patterns
5. **Trend Analysis**: Identify spending patterns, anomalies, and opportunities for optimization

## Workflow

### 1. Data Extraction and Preparation

**For PDF files:**
```bash
python scripts/extract_pdf_data.py <input.pdf> <output.csv>
```

**For CSV/JSON files:**
- Ensure data has columns: `Date`, `Description`, `Income` (category), `Type`, `Amount`
- Date format: YYYY-MM-DD or parseable date string
- Amount: Positive for income, negative for expenses

### 2. Financial Analysis

Run comprehensive analysis on transaction data:
```bash
python scripts/analyze_finances.py <transactions.csv> > analysis_output.json
```

**Output includes:**
- Summary statistics (total income, expenses, net savings, savings rate)
- Spending trends (daily averages, top expenses, category percentages)
- Budget recommendations (personalized based on spending patterns)
- Visualization data (prepared for charting)

### 3. Report Generation

Create interactive HTML report with visualizations:
```bash
python scripts/generate_report.py <analysis_output.json> <report.html>
```

**Report features:**
- Summary dashboard with key metrics
- Interactive pie chart showing spending by category
- Bar chart comparing income vs expenses over time
- Color-coded indicators (green for positive, red for negative)
- Personalized recommendations section
- Responsive design for all devices

### 4. Complete Workflow Example

```bash
# Extract data from PDF
python scripts/extract_pdf_data.py finance_data.pdf transactions.csv

# Analyze the data
python scripts/analyze_finances.py transactions.csv > analysis.json

# Generate visual report
python scripts/generate_report.py analysis.json financial_report.html
```

## Key Metrics and Benchmarks

### Savings Rate
```
Savings Rate = (Total Income - Total Expenses) / Total Income × 100
```

**Benchmarks:**
- Below 10%: Needs improvement
- 10-20%: Good
- 20-30%: Excellent  
- Above 30%: Outstanding

### Category Guidelines (% of income)
- Housing: 25-30%
- Transportation: 10-15%
- Food: 10-15%
- Utilities: 5-10%
- Savings: Minimum 20%

For detailed frameworks and methodologies, see `references/financial_frameworks.md`.

## Analysis Features

### Summary Statistics
- Total income and expenses for the period
- Net savings (can be positive or negative)
- Savings rate percentage
- Transaction count
- Date range covered

### Spending Trends
- Daily average spending
- Top 5 largest expenses with details
- Category percentage breakdown
- Spending patterns over time

### Budget Recommendations

The system generates personalized recommendations based on:
- Savings rate thresholds
- Category spending percentages
- Income diversification
- Budget guideline comparisons

**Example recommendations:**
- "⚠️ Your savings rate is below 10%. Consider reducing discretionary spending."
- "🍽️ Food spending is 18% of expenses. Consider meal planning to reduce costs."
- "✅ Excellent savings rate! You're on track for strong financial health."

## Visualization Components

### Category Spending Chart (Doughnut)
Shows proportional breakdown of expenses by category with color coding.

### Income vs Expenses Chart (Bar)
Displays monthly comparison of income and expenses to identify cash flow trends.

### Interactive Features
- Hover tooltips showing exact values
- Responsive design adapting to screen size
- Color-coded positive (green) and negative (red) indicators

## Tips for Best Results

### Data Quality
- Ensure all transactions are properly categorized
- Use consistent category names
- Include complete date information
- Verify amounts are correctly signed (+ for income, - for expenses)

### Analysis Frequency
- Run monthly analysis for trend tracking
- Generate reports at month-end for review
- Compare month-over-month to identify changes

### Action on Recommendations
- Prioritize recommendations by potential impact
- Set specific, measurable goals based on insights
- Track progress by re-running analysis regularly

## Dependencies

All scripts require Python 3.7+ with standard libraries. Additional requirements:

**For PDF extraction:**
```bash
pip install pdfplumber --break-system-packages
```

**For data analysis:**
```bash
pip install pandas --break-system-packages
```

All visualization dependencies are loaded from CDN in the HTML output (Chart.js).

## File Organization

```
finance-manager/
├── scripts/
│   ├── extract_pdf_data.py     # PDF → CSV conversion
│   ├── analyze_finances.py     # Financial analysis engine
│   └── generate_report.py      # HTML report generator
└── references/
    └── financial_frameworks.md # Detailed analysis methodologies
```

## Customization

### Adding Custom Categories
Edit the category definitions in `analyze_finances.py` to match your tracking system.

### Adjusting Thresholds
Modify recommendation thresholds in the `generate_budget_recommendations()` function to match personal goals.

### Styling Reports
Customize the HTML_TEMPLATE in `generate_report.py` to adjust colors, fonts, or layout.

## Common Use Cases

**Monthly Review:**
"Analyze my October spending and create a report"

**Budget Optimization:**  
"Where am I spending too much money?"

**Trend Analysis:**
"How does my spending this month compare to last month?"

**Goal Setting:**
"What's my savings rate and how can I improve it?"

**Category Insights:**
"Break down my food spending by transaction"

**PDF Processing:**
"Extract all transactions from my bank statement PDF"

## Best Practices

1. **Consistent Categorization**: Use the same category names across all transactions
2. **Regular Analysis**: Run monthly to spot trends early
3. **Act on Insights**: Use recommendations to make specific spending changes
4. **Track Progress**: Compare reports month-over-month
5. **Verify Data**: Always check extracted PDF data for accuracy before analysis

## Reference Materials

For comprehensive financial frameworks, budgeting guidelines, and analysis methodologies, read:
```bash
view references/financial_frameworks.md
```

This includes:
- The 50/30/20 budget rule
- Category spending benchmarks  
- Financial health indicators
- Analysis workflow details
- Visualization best practices
- Recommendation logic
