---
name: analytics-design
description: Design data analysis from purpose clarification to visualization. Use when analyzing data, exploring BigQuery schemas, building queries, or creating Looker Studio reports.
---

# Analytics Design

**Rules**: Follow [document-writing](../../rules/document-writing.md) and [text-formatting-ja](../../rules/text-formatting-ja.md) for Japanese documents.

## Workflow

Use [references/analytics-design-template.md](references/analytics-design-template.md) to document every analysis.

1. **Clarify Purpose**: What do you want to know? Why is this analysis needed? Who will use it? One-time or ongoing monitoring?

2. **Discover Data**: Explore available datasets and understand schema.
   - Ask user for project/dataset context and business background
   - Use `/bq-query` skill for BigQuery schema exploration
   - `db/schema.rb` for Rails projects
   - API docs or sample data for external services
   - Document schema and table relationships in the report

3. **Build Query**: Use `/bq-query` skill to design and execute queries.
   - Requirements and schema from Steps 1-2 provide context
   - Interpret results and document findings

4. **Create Dashboard** (if ongoing monitoring needed):
   - Use [references/looker-studio-template.md](references/looker-studio-template.md) to design
   - Define decisions: What actions will users take based on this dashboard?
   - Check existing resources: Similar dashboards or queries already exist?
   - Align time granularity with usage frequency (daily/weekly/monthly)
   - Design data sources, pages, and charts

## Looker Studio Best Practices

### Reference Documentation

- [Data types](https://cloud.google.com/looker/docs/studio/data-types): Field data types (Number, Text, Date & Time, Currency, Percent, etc.)
- [Types of charts](https://cloud.google.com/looker/docs/studio/types-of-charts-in-looker-studio): Chart types (Time series, Combo chart, Table, etc.)
- [Parameters](https://cloud.google.com/looker/docs/studio/parameters): Data source parameters

### Settings Documentation

- Verify setting names against actual Looker Studio UI before documenting
- Use exact terminology from the UI

### Data Source Design

- One data source per analytical purpose
- Pre-aggregate in SQL for performance
- Include bucket fields for distribution analysis
- Include sort-order fields for proper chart ordering
- Descriptive data source names

### Report Structure

- Separate pages by time granularity (daily/monthly)
- Group related metrics per page
- Consistent filter scopes within pages

### Chart Type Selection

| Purpose | Chart Type |
|---------|------------|
| KPI current value | Scorecard |
| Time series trend | Time series chart |
| Category breakdown over time | Stacked area / Stacked bar |
| Category comparison | Bar chart |
| Composition | Pie chart |
| Detailed data | Table |
| Distribution (percentile) | Time series (multiple metrics) |
