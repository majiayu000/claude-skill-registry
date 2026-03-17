---
name: structured-data
description: CSV parsing, JSON-to-CSV conversion, and SVG chart generation
---

## Structured Data

You have tools for working with structured data and creating visualizations:

**CSV handling:**
- `parse_csv` — parse CSV text into a JSON array of objects
  - Auto-detects delimiter (comma, tab, semicolon, pipe)
  - Handles quoted fields with embedded commas and newlines
  - Returns `data` (full array), `columns`, `row_count`, and `preview` (first 5 rows)
  - Use `limit` parameter for large datasets to get just the first N rows

- `json_to_csv` — convert a JSON array of objects to CSV text
  - Auto-quotes fields containing delimiters, newlines, or quotes
  - Use `columns` parameter to select/reorder specific columns
  - Nested objects are serialized via JSON.stringify

**Charts:**
- `generate_chart` — generate an SVG chart from data
  - Chart types: `bar`, `line`, `pie`
  - Single series: `{ labels: ["A", "B"], values: [10, 20] }`
  - Multi-series: `{ labels: ["Q1", "Q2"], series: [{ name: "2024", values: [10, 20] }, { name: "2025", values: [15, 25] }] }`
  - Returns `svg` (raw SVG) and `data_uri` (base64 for embedding in markdown)
  - Embed in markdown: `![Chart](data:image/svg+xml;base64,...)`

**Best practices:**
- Use `parse_csv` to convert CSV data into JSON for processing
- Use `json_to_csv` to convert results back to CSV for delivery
- Use `generate_chart` to create visualizations for reports
- Combine with `execute_js` (code-sandbox skill) for complex data transformations
- Combine with `store_deliverable` to save charts and processed data as job evidence
- Embed charts in PDF deliverables via the `data_uri` output
