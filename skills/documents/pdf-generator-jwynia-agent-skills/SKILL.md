---
name: pdf-generator
description: "Create and manipulate PDF files programmatically. Use when the user needs to generate PDFs, fill PDF forms, extract PDF content, add watermarks/overlays, or merge documents. Supports both template-based generation (form filling, overlays) and from-scratch creation. Keywords: PDF, document, form, fillable, merge, watermark, extract, text, report."
license: MIT
compatibility: Requires Deno with --allow-read, --allow-write permissions
metadata:
  author: agent-skills
  version: "1.0"
---

# PDF Generator

## When to Use This Skill

Use this skill when:
- Creating PDF documents programmatically from data or specifications
- Filling PDF forms with dynamic data
- Adding watermarks, stamps, or overlays to existing PDFs
- Extracting text and metadata from PDF files
- Merging multiple PDFs into one document
- Analyzing PDF structure and form fields

Do NOT use this skill when:
- User wants to open/view PDFs (use native PDF viewer)
- Complex page layout with flowing text is needed (consider HTML-to-PDF tools)
- Working with password-protected PDFs (limited support)
- OCR is needed for scanned documents

## Prerequisites

- Deno installed (https://deno.land/)
- Input PDF files for template-based operations
- JSON specification for scratch generation

## Quick Start

### Two Modes of Operation

1. **Template Mode**: Modify existing PDF templates
   - Fill form fields (text, checkbox, dropdown)
   - Add overlays (text, images, shapes)
   - Merge and combine PDFs

2. **Scratch Mode**: Create PDFs from nothing using JSON specifications

## Instructions

### Mode 1: Template-Based Generation

#### Step 1a: Analyze the Template

Extract form fields and structure from an existing PDF:

```bash
deno run --allow-read scripts/analyze-template.ts form-template.pdf > inventory.json
```

**Output** (inventory.json):
```json
{
  "filename": "form-template.pdf",
  "pageCount": 2,
  "title": "Application Form",
  "author": "Company Inc",
  "pages": [
    { "pageNumber": 1, "width": 612, "height": 792, "text": "..." }
  ],
  "formFields": [
    { "name": "FullName", "type": "text", "value": "" },
    { "name": "Email", "type": "text", "value": "" },
    { "name": "AgreeToTerms", "type": "checkbox", "value": false }
  ],
  "placeholders": [
    { "tag": "{{DATE}}", "location": "page 1", "pageNumber": 1 }
  ],
  "hasFormFields": true
}
```

#### Step 1b: Create Fill Specification

Create `form-data.json`:
```json
{
  "formFields": [
    { "name": "FullName", "value": "John Smith" },
    { "name": "Email", "value": "john@example.com" },
    { "name": "AgreeToTerms", "value": true }
  ],
  "flattenForm": true
}
```

#### Step 1c: Generate Filled PDF

```bash
deno run --allow-read --allow-write scripts/generate-from-template.ts \
  form-template.pdf form-data.json filled-form.pdf
```

### Adding Overlays (Watermarks, Stamps)

Create `watermark-spec.json`:
```json
{
  "overlays": [
    {
      "type": "text",
      "page": 1,
      "x": 200,
      "y": 400,
      "text": "CONFIDENTIAL",
      "fontSize": 48,
      "color": { "r": 1, "g": 0, "b": 0 },
      "rotate": 45
    },
    {
      "type": "image",
      "page": 1,
      "x": 450,
      "y": 700,
      "path": "logo.png",
      "width": 100,
      "height": 50
    }
  ]
}
```

### Merging PDFs

Create `merge-spec.json`:
```json
{
  "prependPdfs": [
    { "path": "cover-page.pdf" }
  ],
  "appendPdfs": [
    { "path": "appendix-a.pdf", "pages": [1, 2, 3] },
    { "path": "appendix-b.pdf" }
  ],
  "excludePages": [5, 6]
}
```

### Mode 2: From-Scratch Generation

#### Step 2a: Create Specification

Create `spec.json`:
```json
{
  "title": "Quarterly Report",
  "author": "Finance Team",
  "pages": [
    {
      "size": "A4",
      "elements": [
        {
          "type": "text",
          "x": 50,
          "y": 750,
          "text": "Q4 2024 Financial Report",
          "fontSize": 28,
          "font": "HelveticaBold",
          "color": { "r": 0, "g": 0, "b": 0.5 }
        },
        {
          "type": "line",
          "startX": 50,
          "startY": 740,
          "endX": 550,
          "endY": 740,
          "thickness": 2
        },
        {
          "type": "text",
          "x": 50,
          "y": 700,
          "text": "Executive Summary",
          "fontSize": 18,
          "font": "HelveticaBold"
        },
        {
          "type": "text",
          "x": 50,
          "y": 670,
          "text": "This quarter showed strong growth across all divisions...",
          "fontSize": 12,
          "maxWidth": 500,
          "lineHeight": 16
        }
      ]
    }
  ]
}
```

#### Step 2b: Generate PDF

```bash
deno run --allow-read --allow-write scripts/generate-scratch.ts spec.json output.pdf
```

## Examples

### Example 1: Fill Application Form

**Scenario**: Automatically fill a job application form.

```bash
# 1. Analyze form to find field names
deno run --allow-read scripts/analyze-template.ts application.pdf --pretty

# 2. Create form-data.json with applicant info
# 3. Generate filled form
deno run --allow-read --allow-write scripts/generate-from-template.ts \
  application.pdf form-data.json john-smith-application.pdf
```

### Example 2: Add Approval Stamp

**Scenario**: Add an "APPROVED" stamp to a document.

**stamp-spec.json**:
```json
{
  "overlays": [
    {
      "type": "rectangle",
      "page": 1,
      "x": 400,
      "y": 700,
      "width": 150,
      "height": 50,
      "color": { "r": 0.9, "g": 1, "b": 0.9 }
    },
    {
      "type": "text",
      "page": 1,
      "x": 410,
      "y": 720,
      "text": "APPROVED",
      "fontSize": 20,
      "font": "HelveticaBold",
      "color": { "r": 0, "g": 0.5, "b": 0 }
    },
    {
      "type": "text",
      "page": 1,
      "x": 410,
      "y": 705,
      "text": "2024-12-15",
      "fontSize": 10
    }
  ]
}
```

### Example 3: Create Report with Table

**Scenario**: Generate a simple report with a data table.

**report-spec.json**:
```json
{
  "title": "Sales Report",
  "pages": [{
    "size": "Letter",
    "elements": [
      {
        "type": "text",
        "x": 72,
        "y": 720,
        "text": "Monthly Sales Report",
        "fontSize": 24,
        "font": "HelveticaBold"
      },
      {
        "type": "table",
        "x": 72,
        "y": 680,
        "rows": [
          ["Product", "Units", "Revenue"],
          ["Widget A", "150", "$15,000"],
          ["Widget B", "75", "$11,250"],
          ["Widget C", "200", "$8,000"]
        ],
        "columnWidths": [150, 80, 100],
        "rowHeight": 25,
        "headerBackground": { "r": 0.9, "g": 0.9, "b": 0.9 }
      }
    ]
  }]
}
```

## Script Reference

| Script | Purpose | Permissions |
|--------|---------|-------------|
| `analyze-template.ts` | Extract text, metadata, form fields from PDF | `--allow-read` |
| `generate-from-template.ts` | Fill forms, add overlays, merge PDFs | `--allow-read --allow-write` |
| `generate-scratch.ts` | Create PDF from JSON specification | `--allow-read --allow-write` |

## Element Types (Scratch Mode)

| Type | Description | Key Options |
|------|-------------|-------------|
| `text` | Text content | `x`, `y`, `text`, `fontSize`, `font`, `color`, `rotate` |
| `image` | PNG/JPEG images | `x`, `y`, `path`, `width`, `height`, `opacity` |
| `rectangle` | Filled/outlined rectangles | `x`, `y`, `width`, `height`, `color`, `borderColor` |
| `line` | Straight lines | `startX`, `startY`, `endX`, `endY`, `thickness` |
| `circle` | Filled/outlined circles | `x`, `y`, `radius`, `color`, `borderColor` |
| `table` | Basic table layout | `x`, `y`, `rows`, `columnWidths`, `rowHeight` |

## Available Fonts

- `Helvetica` (default)
- `HelveticaBold`
- `HelveticaOblique`
- `TimesRoman`
- `TimesBold`
- `Courier`
- `CourierBold`

## Page Sizes

- `A4` (595.28 x 841.89 points)
- `Letter` (612 x 792 points)
- `Legal` (612 x 1008 points)
- Custom: `[width, height]` in points

## Common Issues and Solutions

### Issue: Form fields not found

**Symptoms**: Error saying field name doesn't exist.

**Solution**:
1. Run `analyze-template.ts` to get exact field names
2. Field names are case-sensitive
3. Some PDFs have non-fillable text that looks like form fields

### Issue: Text positioning is off

**Symptoms**: Text appears in wrong location.

**Solution**:
- PDF coordinates start from bottom-left (0,0)
- Y increases upward, X increases rightward
- Use `analyze-template.ts` to see page dimensions

### Issue: Images not appearing

**Symptoms**: Image overlay not visible.

**Solution**:
1. Check file path is relative to spec.json location
2. Verify image is PNG or JPEG format
3. Ensure coordinates are within page bounds

### Issue: Merged PDF has wrong page order

**Symptoms**: Pages appear in unexpected order.

**Solution**:
- `prependPdfs` add pages before template
- `appendPdfs` add pages after template
- Use `pages` array to select specific pages: `[1, 3, 5]`

## Limitations

- **No built-in table layout**: Tables require manual column width specification
- **Standard fonts only**: Custom font embedding not supported in scratch mode
- **No flowing text**: Text doesn't automatically wrap to next page
- **Limited form field creation**: Can fill existing forms, not create new fields
- **No encryption**: Cannot create password-protected PDFs
- **Basic graphics**: No gradients, patterns, or complex paths
- **Text extraction**: May not work perfectly on all PDFs (depends on PDF structure)

## Related Skills

- **pptx-generator**: For creating PowerPoint presentations
- **docx-generator**: For creating Word documents
- **xlsx-generator**: For creating Excel spreadsheets
