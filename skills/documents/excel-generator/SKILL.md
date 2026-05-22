---
name: excel-generator
description: Generate Excel workbooks with formulas, charts, and formatting. Use for financial reports, data analysis, dashboards, and structured data presentation.
allowed-tools: read, write, memory
version: 1.0
best_practices:
  - Use 2-3 sheets per workbook for optimal performance
  - Focus each sheet on a specific purpose
  - Add complexity incrementally
  - Use structured data (JSON/CSV) for efficiency
error_handling: graceful
streaming: supported
---

# Excel Generator Skill

## Identity

Excel Generator - Creates professional Excel workbooks with formulas, charts, and formatting using Claude's built-in `xlsx` skill.

## Capabilities

- **Workbook Creation**: Generate multi-sheet Excel workbooks
- **Formulas and Calculations**: Include complex formulas and calculations
- **Charts and Visualizations**: Create charts and graphs
- **Formatting**: Apply professional formatting and styling
- **Data Analysis**: Generate pivot tables and analysis sheets

## Usage

### Basic Excel Generation

**When to Use**:

- Financial reports and analysis
- Data dashboards
- Budget planning
- Performance metrics
- Structured data presentation

**How to Invoke**:

```
"Generate an Excel workbook with Q4 financial data"
"Create a budget spreadsheet with formulas"
"Generate a data analysis dashboard in Excel"
```

**What It Does**:

- Uses Claude's built-in `xlsx` skill (skill_id: `xlsx`)
- Creates Excel workbooks with multiple sheets
- Includes formulas, charts, and formatting
- Returns file_id for download

### Advanced Features

**Multi-Sheet Workbooks**:

- Create 2-3 sheets per workbook (optimal performance)
- Each sheet focused on specific purpose
- Link data between sheets

**Formulas and Calculations**:

- Complex financial formulas
- Statistical calculations
- Data aggregations
- Conditional logic

**Charts and Visualizations**:

- Line charts for trends
- Bar charts for comparisons
- Pie charts for distributions
- Scatter plots for correlations

## Best Practices

### Workbook Structure

**Recommended Approach**:

- **2-3 sheets per workbook** - Works reliably and generates quickly
- **Focus each sheet** on a specific purpose (e.g., P&L, metrics, charts)
- **Add complexity incrementally** - Start simple, then enhance

**For Complex Dashboards**:

1. **Create multiple focused files** instead of one complex file
   - Example: `financial_pnl.xlsx`, `balance_sheet.xlsx`, `kpi_dashboard.xlsx`
2. **Use the pipeline pattern** to create and enhance files sequentially
3. **Combine files programmatically** using pandas or openpyxl if needed

### Performance Tips

- **Simple 2-sheet dashboards**: ~1-2 minutes
- **Structured data (JSON/CSV)**: More efficient than prose
- **Batch operations**: Process multiple files in a single conversation
- **Cache reuse**: Use container IDs to reuse loaded skills

## Integration

### With Artifact Publisher

Excel files can be published as artifacts:

- Save to `.claude/context/artifacts/`
- Include in artifact manifests
- Reference in workflow outputs

### With Workflows

Excel generation integrates with workflows:

- Financial reporting workflows
- Data analysis workflows
- Dashboard generation workflows

## Examples

### Example 1: Financial Report

```
User: "Generate a Q4 financial report in Excel"

Excel Generator:
1. Creates workbook with 3 sheets:
   - P&L Statement
   - Balance Sheet
   - Cash Flow
2. Includes formulas for calculations
3. Adds charts for visualization
4. Applies professional formatting
5. Returns file_id for download
```

### Example 2: Data Dashboard

```
User: "Create a KPI dashboard in Excel"

Excel Generator:
1. Creates workbook with 2 sheets:
   - Metrics Summary
   - Trend Analysis
2. Includes pivot tables
3. Adds charts for key metrics
4. Formats for presentation
```

### Example 3: Budget Planning

```
User: "Generate a budget spreadsheet with formulas"

Excel Generator:
1. Creates budget workbook
2. Includes formulas for totals and variances
3. Adds conditional formatting
4. Creates summary charts
```

## Technical Details

### API Usage

Uses Claude's beta Skills API:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    container={"type": "skills", "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]},
    messages=[{"role": "user", "content": "Create Excel workbook..."}]
)
```

### File Download

Files are returned as `file_id`:

```python
file_id = response.content[0].file_id
file_content = client.beta.files.content(file_id)
```

## Related Skills

- **powerpoint-generator**: Create presentations from Excel data
- **pdf-generator**: Convert Excel to PDF
- **artifact-publisher**: Publish Excel files as artifacts

## Related Documentation

- [Document Generation Guide](../docs/DOCUMENT_GENERATION.md) - Comprehensive guide
- [Skills Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills) - Reference implementation
