---
name: xlsx-generator
description: "Create and manipulate Excel XLSX files programmatically. Use when the user needs to generate spreadsheets, modify XLSX templates, extract spreadsheet content, or automate Excel workflows. Supports both template-based generation (for branding compliance) and from-scratch creation. Keywords: Excel, XLSX, spreadsheet, workbook, worksheet, data, report, template, financial, analysis."
license: MIT
compatibility: Requires Deno with --allow-read, --allow-write permissions
metadata:
  author: agent-skills
  version: "1.0"
---

# XLSX Generator

## When to Use This Skill

Use this skill when:
- Creating Excel spreadsheets programmatically from data or specifications
- Populating branded templates with dynamic content while preserving formatting
- Extracting cell data, formulas, and structure from existing XLSX files
- Finding and replacing placeholder text like `{{TITLE}}` or `${date}` in cells
- Automating spreadsheet generation workflows (reports, data exports, financial statements)

Do NOT use this skill when:
- User wants to open/view spreadsheets (use native Excel or viewer)
- Complex pivot tables or charts are required (limited support)
- Working with older .xls format (XLSX only)
- Real-time collaborative editing is needed

## Prerequisites

- Deno installed (https://deno.land/)
- Input XLSX files for template-based operations
- JSON specification for scratch generation

## Quick Start

### Two Modes of Operation

1. **Template Mode**: Modify existing branded templates
   - Analyze template to find placeholders and structure
   - Replace `{{PLACEHOLDERS}}` with actual values

2. **Scratch Mode**: Create spreadsheets from nothing using JSON specifications

## Instructions

### Mode 1: Template-Based Generation

#### Step 1a: Analyze the Template

Extract cell inventory to understand what can be replaced:

```bash
deno run --allow-read scripts/analyze-template.ts financial-template.xlsx > inventory.json
```

**Output** (inventory.json):
```json
{
  "filename": "financial-template.xlsx",
  "sheetCount": 3,
  "sheets": [
    {
      "name": "Summary",
      "rowCount": 25,
      "colCount": 8,
      "usedRange": "A1:H25",
      "cells": [
        { "address": "A1", "row": 1, "col": 1, "value": "{{REPORT_TITLE}}", "type": "string" },
        { "address": "B3", "row": 3, "col": 2, "value": "{{DATE}}", "type": "string" },
        { "address": "C5", "row": 5, "col": 3, "value": null, "type": "number", "formula": "SUM(C6:C20)" }
      ]
    }
  ],
  "placeholders": [
    { "tag": "{{REPORT_TITLE}}", "location": "Summary!A1", "sheet": "Summary", "address": "A1" },
    { "tag": "{{DATE}}", "location": "Summary!B3", "sheet": "Summary", "address": "B3" }
  ],
  "hasFormulas": true
}
```

#### Step 1b: Create Replacement Specification

Create `replacements.json`:
```json
{
  "textReplacements": [
    { "tag": "{{REPORT_TITLE}}", "value": "Q4 2024 Financial Report" },
    { "tag": "{{DATE}}", "value": "December 15, 2024" },
    { "tag": "{{COMPANY}}", "value": "Acme Corporation", "sheets": ["Summary", "Cover"] }
  ],
  "cellUpdates": [
    { "sheet": "Data", "address": "B5", "value": 1250000 },
    { "sheet": "Data", "address": "B6", "value": 750000 }
  ]
}
```

#### Step 1c: Generate Output

```bash
deno run --allow-read --allow-write scripts/generate-from-template.ts \
  financial-template.xlsx replacements.json output.xlsx
```

### Mode 2: From-Scratch Generation

#### Step 2a: Create Specification

Create `spec.json`:
```json
{
  "title": "Sales Report",
  "author": "Finance Team",
  "sheets": [
    {
      "name": "Sales Data",
      "data": [
        ["Product", "Q1", "Q2", "Q3", "Q4", "Total"],
        ["Widget A", 10000, 12000, 15000, 18000, null],
        ["Widget B", 8000, 9000, 11000, 13000, null],
        ["Widget C", 5000, 6000, 7000, 8000, null]
      ],
      "cells": [
        { "address": "F2", "formula": "SUM(B2:E2)" },
        { "address": "F3", "formula": "SUM(B3:E3)" },
        { "address": "F4", "formula": "SUM(B4:E4)" }
      ],
      "columns": [
        { "col": "A", "width": 15 },
        { "col": "B", "width": 10 },
        { "col": "C", "width": 10 },
        { "col": "D", "width": 10 },
        { "col": "E", "width": 10 },
        { "col": "F", "width": 12 }
      ],
      "freezePane": "A2",
      "autoFilter": "A1:F4"
    }
  ]
}
```

#### Step 2b: Generate Spreadsheet

```bash
deno run --allow-read --allow-write scripts/generate-scratch.ts spec.json output.xlsx
```

## Examples

### Example 1: Monthly Sales Report

**Scenario**: Generate a monthly sales report from template.

**Steps**:
```bash
# 1. Analyze template for replaceable content
deno run --allow-read scripts/analyze-template.ts sales-template.xlsx --pretty

# 2. Create replacements.json with monthly data
# 3. Generate report
deno run --allow-read --allow-write scripts/generate-from-template.ts \
  sales-template.xlsx replacements.json November-Sales.xlsx
```

### Example 2: Data Export with Formulas

**Scenario**: Create a spreadsheet with calculated totals.

**spec.json**:
```json
{
  "sheets": [{
    "name": "Expenses",
    "data": [
      ["Category", "January", "February", "March", "Total"],
      ["Office", 1500, 1600, 1400, null],
      ["Travel", 3000, 2500, 4000, null],
      ["Software", 500, 500, 500, null],
      ["Total", null, null, null, null]
    ],
    "cells": [
      { "address": "E2", "formula": "SUM(B2:D2)" },
      { "address": "E3", "formula": "SUM(B3:D3)" },
      { "address": "E4", "formula": "SUM(B4:D4)" },
      { "address": "B5", "formula": "SUM(B2:B4)" },
      { "address": "C5", "formula": "SUM(C2:C4)" },
      { "address": "D5", "formula": "SUM(D2:D4)" },
      { "address": "E5", "formula": "SUM(E2:E4)" }
    ]
  }]
}
```

### Example 3: Multi-Sheet Workbook

**Scenario**: Create a workbook with summary and detail sheets.

**spec.json**:
```json
{
  "title": "Q4 Report",
  "sheets": [
    {
      "name": "Summary",
      "data": [
        ["Department", "Budget", "Actual", "Variance"],
        ["Sales", 500000, 520000, null],
        ["Marketing", 200000, 195000, null]
      ],
      "cells": [
        { "address": "D2", "formula": "C2-B2" },
        { "address": "D3", "formula": "C3-B3" }
      ]
    },
    {
      "name": "Sales Detail",
      "data": [
        ["Month", "Revenue", "Cost", "Profit"],
        ["October", 180000, 120000, null],
        ["November", 170000, 115000, null],
        ["December", 170000, 110000, null]
      ],
      "cells": [
        { "address": "D2", "formula": "B2-C2" },
        { "address": "D3", "formula": "B3-C3" },
        { "address": "D4", "formula": "B4-C4" }
      ]
    }
  ]
}
```

## Script Reference

| Script | Purpose | Permissions |
|--------|---------|-------------|
| `analyze-template.ts` | Extract cells, formulas, placeholders from XLSX | `--allow-read` |
| `generate-from-template.ts` | Replace placeholders in templates | `--allow-read --allow-write` |
| `generate-scratch.ts` | Create XLSX from JSON specification | `--allow-read --allow-write` |

## Specification Reference

### Sheet Options

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Sheet name |
| `data` | array | 2D array of cell values starting at A1 |
| `cells` | array | Individual cell specifications |
| `rows` | array | Row-based data specifications |
| `columns` | array | Column width and visibility settings |
| `merges` | array | Merged cell ranges |
| `freezePane` | string | Freeze panes at this cell (e.g., "A2") |
| `autoFilter` | string | Auto-filter range (e.g., "A1:F10") |

### Cell Options

| Property | Type | Description |
|----------|------|-------------|
| `address` | string | Cell address (e.g., "A1", "B2") |
| `value` | mixed | Cell value (string, number, boolean, null) |
| `formula` | string | Formula without = sign |
| `format` | string | Number format (e.g., "#,##0.00") |
| `type` | string | Force type: "string", "number", "boolean", "date" |

### Column Options

| Property | Type | Description |
|----------|------|-------------|
| `col` | string | Column letter (e.g., "A", "B", "AA") |
| `width` | number | Column width in characters |
| `hidden` | boolean | Hide column |

### Template Replacement Options

| Property | Type | Description |
|----------|------|-------------|
| `tag` | string | Placeholder to find (e.g., "{{TITLE}}") |
| `value` | mixed | Replacement value |
| `sheets` | array | Limit to specific sheets |
| `range` | string | Limit to cell range (e.g., "A1:D10") |

## Common Issues and Solutions

### Issue: Placeholders not being replaced

**Symptoms**: Output XLSX still contains `{{PLACEHOLDER}}` tags.

**Solution**:
1. Run `analyze-template.ts` to verify exact tag text and location
2. Check that placeholder is in a string cell, not a formula
3. Verify sheet filter in replacement spec

### Issue: Formulas showing as text

**Symptoms**: Formulas display as text instead of calculating.

**Solution**:
- Ensure formula doesn't start with "=" in spec (it's added automatically)
- Check cell type is not forced to "string"

### Issue: Numbers formatted as text

**Symptoms**: Numbers have green triangle indicating text storage.

**Solution**:
- Use numeric values in spec, not quoted strings
- For template replacement, if entire cell is placeholder and replacement is number, it converts automatically

### Issue: Column widths not applied

**Symptoms**: Columns have default width despite specification.

**Solution**:
- Ensure column letters are uppercase
- Verify column spec is in array format

## Limitations

- **XLSX only**: Does not support legacy .xls or .xlsb formats
- **No macros**: Cannot create or preserve VBA macros
- **Limited charting**: No native chart creation support
- **No pivot tables**: Cannot create pivot tables programmatically
- **Basic styling**: Limited cell formatting options
- **No conditional formatting**: Cannot set conditional format rules
- **Formula recalc**: Formulas are stored but not recalculated (Excel recalculates on open)

## Related Skills

- **pptx-generator**: For creating PowerPoint presentations
- **docx-generator**: For creating Word documents
- **csv-processor**: For simpler CSV data processing
