---
name: financial-reporting
cluster: financial
description: "Generates and analyzes financial reports using data aggregation, visualization, and compliance tools."
tags: ["finance","reporting","accounting","data-analysis"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "finance reporting accounting analysis compliance"
---

# financial-reporting

## Purpose
This skill enables the generation and analysis of financial reports by aggregating data, creating visualizations, and ensuring compliance with standards like GAAP or IFRS. It processes financial datasets to produce actionable insights for reporting tasks.

## When to Use
Use this skill for quarterly financial summaries, annual audits, compliance checks, or ad-hoc analyses of income statements and balance sheets. Apply it when integrating with accounting software or when visualizing trends in financial metrics.

## Key Capabilities
- Data aggregation: Pulls data from sources via API endpoint `/api/v1/aggregate?start_date=2023-01-01&end_date=2023-12-31`, supporting filters for accounts and currencies.
- Visualization: Generates charts using libraries like Matplotlib; e.g., creates a pie chart for expense breakdown with `plot_type='pie'&data_source='expenses'`.
- Compliance tools: Checks reports against rules, such as validating totals with `compliance_check('GAAP', report_data)`, returning boolean results.
- Analysis functions: Performs ratio analysis, e.g., `calculate_ratio('debt_to_equity', balance_sheet_data)`, outputting a float value.
- Export formats: Supports JSON, CSV, or PDF output; configure with `export_format='PDF'&file_path='/reports/q1.pdf'`.

## Usage Patterns
To use this skill, import the module in Python scripts or call via CLI. Start by authenticating with `$FINANCIAL_API_KEY`, then aggregate data before analysis. For scripts, wrap calls in try-except blocks for error resilience. Common pattern: Fetch data, process it, visualize, and export. Example workflow: `aggregate_data() -> analyze_data() -> generate_report()`.

## Common Commands/API
- CLI Command: `openclaw financial-report aggregate --start-date 2023-01-01 --end-date 2023-12-31 --key $FINANCIAL_API_KEY`
  - Aggregates data and outputs to stdout.
- API Endpoint: POST `/api/v1/reports/generate` with JSON body: `{"type": "balance_sheet", "data": {"assets": 100000}}`
  - Requires header: `Authorization: Bearer $FINANCIAL_API_KEY`
- Code Snippet (Python):
  ```
  import openclaw_financial
  api_key = os.environ.get('FINANCIAL_API_KEY')
  report = openclaw_financial.generate_report('income_statement', api_key)
  ```
- Another Snippet (for analysis):
  ```
  from openclaw_financial import analyze
  result = analyze.calculate_ratio('quick_ratio', {'cash': 50000, 'receivables': 30000, 'liabilities': 100000})
  print(result)  # Outputs: 0.8
  ```
- Config Format: Use JSON for configurations, e.g., `{"api_endpoint": "/api/v1/aggregate", "auth_key": "$FINANCIAL_API_KEY", "default_currency": "USD"}` in a file named `.financial-config.json`.

## Integration Notes
Integrate by setting the environment variable `$FINANCIAL_API_KEY` for authentication before running commands. For external systems, use the SDK to connect; e.g., in a Node.js app, require the package and pass the key: `const client = new FinancialClient(process.env.FINANCIAL_API_KEY);`. Ensure data sources are compatible (e.g., CSV or API-compatible). For web apps, handle CORS on the `/api/v1/*` endpoints by adding headers in your server config.

## Error Handling
Handle authentication errors by checking for 401 responses and prompting for `$FINANCIAL_API_KEY`. For data errors (e.g., invalid dates), catch exceptions like `ValueError` in code: `try: openclaw_financial.aggregate_data(start_date) except ValueError as e: print(f"Error: {e} - Use YYYY-MM-DD format")`. API timeouts use retry logic with exponential backoff; implement via `requests` library: `response = requests.get(url, headers, timeout=10)`. Log all errors with details like error codes (e.g., 404 for missing endpoints) for debugging.

## Concrete Usage Examples
1. Generate a quarterly balance sheet: Use CLI: `openclaw financial-report generate --type balance_sheet --period Q1-2024 --key $FINANCIAL_API_KEY`. This aggregates assets/liabilities and outputs a PDF report for auditing.
2. Analyze earnings trends: In Python, fetch data and visualize: 
   ```
   import openclaw_financial
   data = openclaw_financial.aggregate_data('earnings', os.environ['FINANCIAL_API_KEY'])
   openclaw_financial.visualize(data, 'line', 'earnings_trend.png')
   ```
   This plots quarterly earnings to identify growth patterns.

## Graph Relationships
- Related Skills: accounting-tools (for ledger management), data-visualization (for chart generation)
- Cluster: financial (shares data sources with budgeting and forecasting skills)
- Dependencies: Requires data-analysis cluster for underlying functions
- Connections: Links to compliance-auditing via shared API endpoints like /api/v1/compliance-check
