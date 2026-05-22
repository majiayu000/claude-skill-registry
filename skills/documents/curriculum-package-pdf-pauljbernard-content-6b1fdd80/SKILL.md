---
name: curriculum-package-pdf
description: Generate professionally formatted PDF materials including student handouts, teacher guides, workbooks with proper typography, accessibility, and print layout. Use when creating print materials, PDFs, or formatted documents. Activates on "create PDF", "generate handout", "print materials", or "teacher guide".
---

# Print & PDF Material Generation

Create professionally formatted, accessible PDF documents for student handouts, teacher guides, and print distribution.

## When to Use

- Create student handouts
- Generate teacher guides
- Format workbooks
- Print-ready materials
- Accessible PDF documents

## Required Inputs

- **Content**: What to include in PDF
- **Format**: Handout, guide, workbook, assessment
- **Layout**: Letter, A4, custom
- **Accessibility**: WCAG compliance level

## Workflow

### 1. Format Student Handout

```markdown
# Design Specifications
- Page Size: Letter (8.5" × 11")
- Margins: 1" all sides
- Font: Sans-serif, 12pt body, 18pt+ headings
- Line Spacing: 1.5
- Color: High contrast (black text on white)
- Headers/Footers: Title, page numbers
```

### 2. Format Teacher Guide

```markdown
# Teacher Guide Format
- Two-column layout
  - Left: Student view
  - Right: Teacher notes
- Answer keys highlighted
- Teaching tips in callout boxes
- Time allocations noted
- Material lists included
```

### 3. Ensure Accessibility

✅ Tagged PDF structure
✅ Heading hierarchy (H1, H2, H3)
✅ Alt text for images
✅ Correct reading order
✅ Form field labels
✅ Table headers
✅ List structures
✅ Bookmarks for navigation

### 4. CLI Interface

```bash
# Student handout
/curriculum.package-pdf --type "handout" --content "lesson1.md" --output "lesson1-handout.pdf"

# Teacher guide
/curriculum.package-pdf --type "teacher-guide" --lessons "lessons/*.md" --answers "answer-keys.md"

# Workbook
/curriculum.package-pdf --type "workbook" --unit "Unit 1" --accessible

# Help
/curriculum.package-pdf --help
```

## Exit Codes

- **0**: PDF created successfully
- **1**: Invalid PDF type
- **2**: Cannot load content
- **3**: PDF generation failed
