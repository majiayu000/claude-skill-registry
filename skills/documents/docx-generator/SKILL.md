---
name: docx-generator
description: "Create and manipulate Word DOCX files programmatically. Use when the user needs to generate documents, modify DOCX templates, extract document content, or automate Word document workflows. Supports both template-based generation (for branding compliance) and from-scratch creation. Keywords: Word, DOCX, document, report, template, contract, letter, corporate, branding."
license: MIT
compatibility: Requires Deno with --allow-read, --allow-write permissions
metadata:
  author: agent-skills
  version: "1.0"
---

# DOCX Generator

## When to Use This Skill

Use this skill when:
- Creating Word documents programmatically from data or specifications
- Populating branded templates with dynamic content while preserving corporate styling
- Extracting text, tables, and structure from existing DOCX files for analysis
- Finding and replacing placeholder text like `{{TITLE}}` or `${author}`
- Automating document generation workflows (reports, contracts, letters)

Do NOT use this skill when:
- User wants to open/view documents (use native Word or viewer)
- Complex mail merge with data sources (use native Word mail merge)
- Working with older .doc format (DOCX only)
- PDF output is needed (use pdf-generator skill instead)

## Prerequisites

- Deno installed (https://deno.land/)
- Input DOCX files for template-based operations
- JSON specification for scratch generation

## Quick Start

### Two Modes of Operation

1. **Template Mode**: Modify existing branded templates
   - Analyze template to find placeholders
   - Replace `{{PLACEHOLDERS}}` with actual content

2. **Scratch Mode**: Create documents from nothing using JSON specifications

## Instructions

### Mode 1: Template-Based Generation

#### Step 1a: Analyze the Template

Extract text inventory to understand what can be replaced:

```bash
deno run --allow-read scripts/analyze-template.ts corporate-template.docx > inventory.json
```

**Output** (inventory.json):
```json
{
  "filename": "corporate-template.docx",
  "paragraphCount": 25,
  "tableCount": 2,
  "imageCount": 1,
  "paragraphs": [
    {
      "index": 0,
      "style": "Title",
      "fullText": "{{DOCUMENT_TITLE}}",
      "runs": [
        { "text": "{{DOCUMENT_TITLE}}", "bold": true, "fontSize": 28 }
      ]
    }
  ],
  "placeholders": [
    { "tag": "{{DOCUMENT_TITLE}}", "location": "paragraph", "paragraphIndex": 0 },
    { "tag": "{{AUTHOR}}", "location": "footer-default", "paragraphIndex": 0 },
    { "tag": "${date}", "location": "table", "tableIndex": 0, "cellLocation": "R1C2" }
  ]
}
```

#### Step 1b: Create Replacement Specification

Create `replacements.json`:
```json
{
  "textReplacements": [
    { "tag": "{{DOCUMENT_TITLE}}", "value": "Q4 2024 Financial Report" },
    { "tag": "{{AUTHOR}}", "value": "Finance Department" },
    { "tag": "${date}", "value": "December 15, 2024" },
    { "tag": "{{COMPANY}}", "value": "Acme Corporation" }
  ],
  "includeHeaders": true,
  "includeFooters": true
}
```

#### Step 1c: Generate Output

```bash
deno run --allow-read --allow-write scripts/generate-from-template.ts \
  corporate-template.docx replacements.json output.docx
```

### Mode 2: From-Scratch Generation

#### Step 2a: Create Specification

Create `spec.json`:
```json
{
  "title": "Quarterly Report",
  "creator": "Finance Team",
  "styles": {
    "defaultFont": "Calibri",
    "defaultFontSize": 11
  },
  "sections": [
    {
      "header": {
        "paragraphs": [
          { "text": "Acme Corporation", "alignment": "right" }
        ]
      },
      "footer": {
        "paragraphs": [
          { "text": "Confidential", "alignment": "center" }
        ]
      },
      "content": [
        {
          "text": "Q4 2024 Financial Report",
          "heading": 1,
          "alignment": "center"
        },
        {
          "runs": [
            { "text": "Executive Summary: ", "bold": true },
            { "text": "This report provides an overview of our financial performance for Q4 2024." }
          ]
        },
        { "pageBreak": true },
        {
          "text": "Revenue Breakdown",
          "heading": 2
        },
        {
          "rows": [
            {
              "cells": [
                { "content": [{ "text": "Category" }], "shading": "DDDDDD" },
                { "content": [{ "text": "Amount" }], "shading": "DDDDDD" },
                { "content": [{ "text": "Change" }], "shading": "DDDDDD" }
              ],
              "isHeader": true
            },
            {
              "cells": [
                { "content": [{ "text": "Product Sales" }] },
                { "content": [{ "text": "$1,250,000" }] },
                { "content": [{ "text": "+15%" }] }
              ]
            },
            {
              "cells": [
                { "content": [{ "text": "Services" }] },
                { "content": [{ "text": "$750,000" }] },
                { "content": [{ "text": "+8%" }] }
              ]
            }
          ],
          "width": 100,
          "borders": true
        }
      ]
    }
  ]
}
```

#### Step 2b: Generate Document

```bash
deno run --allow-read --allow-write scripts/generate-scratch.ts spec.json output.docx
```

## Examples

### Example 1: Contract Generation

**Scenario**: Generate contracts from a branded template.

**Steps**:
```bash
# 1. Analyze template for replaceable content
deno run --allow-read scripts/analyze-template.ts contract-template.docx --pretty

# 2. Create replacements.json with client data
# 3. Generate contract
deno run --allow-read --allow-write scripts/generate-from-template.ts \
  contract-template.docx replacements.json acme-contract.docx
```

### Example 2: Report with Tables

**Scenario**: Generate a data report with tables and formatting.

**spec.json**:
```json
{
  "title": "Sales Report",
  "sections": [{
    "content": [
      { "text": "Monthly Sales Report", "heading": 1 },
      { "text": "January 2025", "heading": 2 },
      {
        "runs": [
          { "text": "Total Sales: ", "bold": true },
          { "text": "$125,000", "color": "2E7D32" }
        ]
      }
    ]
  }]
}
```

### Example 3: Letter with Headers/Footers

**Scenario**: Create a formal letter with letterhead.

**spec.json**:
```json
{
  "sections": [{
    "header": {
      "paragraphs": [
        { "text": "ACME CORPORATION", "alignment": "center", "runs": [{"text": "ACME CORPORATION", "bold": true, "fontSize": 16}] },
        { "text": "123 Business Ave, City, ST 12345", "alignment": "center" }
      ]
    },
    "content": [
      { "text": "December 15, 2024", "alignment": "right" },
      { "text": "" },
      { "text": "Dear Valued Customer," },
      { "text": "" },
      { "text": "Thank you for your continued business..." },
      { "text": "" },
      { "text": "Sincerely," },
      { "text": "John Smith" },
      { "runs": [{ "text": "CEO", "italic": true }] }
    ],
    "footer": {
      "paragraphs": [
        { "text": "www.acme.com | contact@acme.com", "alignment": "center" }
      ]
    }
  }]
}
```

## Script Reference

| Script | Purpose | Permissions |
|--------|---------|-------------|
| `analyze-template.ts` | Extract text, tables, placeholders from DOCX | `--allow-read` |
| `generate-from-template.ts` | Replace placeholders in templates | `--allow-read --allow-write` |
| `generate-scratch.ts` | Create DOCX from JSON specification | `--allow-read --allow-write` |

## Specification Reference

### Paragraph Options

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | Simple text content |
| `runs` | array | Formatted text runs (for mixed formatting) |
| `heading` | 1-6 | Heading level |
| `alignment` | string | `left`, `center`, `right`, `justify` |
| `bullet` | boolean | Bulleted list item |
| `numbering` | boolean | Numbered list item |
| `spacing` | object | `before`, `after`, `line` spacing |
| `indent` | object | `left`, `right`, `firstLine` indentation |
| `pageBreakBefore` | boolean | Insert page break before paragraph |

### Text Run Options

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | Text content |
| `bold` | boolean | Bold formatting |
| `italic` | boolean | Italic formatting |
| `underline` | boolean | Underline formatting |
| `strike` | boolean | Strikethrough |
| `fontSize` | number | Font size in points |
| `font` | string | Font family name |
| `color` | string | Text color (hex, no #) |
| `highlight` | string | Highlight color |
| `superScript` | boolean | Superscript |
| `subScript` | boolean | Subscript |

### Table Options

| Property | Type | Description |
|----------|------|-------------|
| `rows` | array | Array of row specifications |
| `width` | number | Table width as percentage |
| `borders` | boolean | Show table borders |

### Hyperlink Options

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | Link text |
| `url` | string | Target URL |
| `bold` | boolean | Bold formatting |
| `italic` | boolean | Italic formatting |

## Common Issues and Solutions

### Issue: Placeholders not being replaced

**Symptoms**: Output DOCX still contains `{{PLACEHOLDER}}` tags.

**Solution**:
1. Run `analyze-template.ts` to verify exact tag text
2. Tags may be split across XML runs - the script consolidates these automatically
3. Ensure `includeHeaders` and `includeFooters` are true if placeholders are there

### Issue: Formatting lost after replacement

**Symptoms**: Replaced text doesn't match original formatting.

**Solution**:
- Text replacement preserves the formatting of the original placeholder
- Ensure placeholder is formatted the way you want the final text to appear

### Issue: Images not appearing

**Symptoms**: Image elements are blank in output.

**Solution**:
1. Use paths relative to the spec.json file location
2. Verify image file exists and is readable
3. Check supported formats: PNG, JPEG, GIF

### Issue: Table cell content incorrect

**Symptoms**: Table cells have wrong content or formatting.

**Solution**:
- Each cell's `content` must be an array of paragraph specifications
- Use `shading` for background color, `verticalAlign` for alignment

## Limitations

- **DOCX only**: Does not support legacy .doc format
- **No track changes**: Cannot add or process track changes
- **No comments**: Cannot add document comments
- **No macros**: Cannot include VBA macros
- **Basic numbering**: Limited support for complex numbering schemes
- **Text run splitting**: Word may split text across XML elements; script handles common cases

## Related Skills

- **pptx-generator**: For creating PowerPoint presentations
- **xlsx-generator**: For creating Excel spreadsheets
- **pdf-generator**: For creating PDF documents
