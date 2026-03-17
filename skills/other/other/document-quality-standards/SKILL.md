---
name: document-quality-standards
description: Use when creating or editing documents (DOCX, PDF, XLSX, PPTX) that need professional output. Adds visual verification, typography hygiene, and formula patterns to the document-skills plugin.
version: 1.0.0
dependencies:
  - poppler-utils
  - libreoffice
  - openpyxl
---

# Document Quality Standards

Patterns that complement the official `document-skills` plugin. Apply these alongside xlsx, pdf, docx, and pptx skills.

## Visual-First Verification

**Core principle**: Text extraction misses critical details. Always verify visually.

> "Only do python printing as a last resort because you will miss important details with text extraction (e.g. figures, tables, diagrams)."

### The Render-Inspect-Fix Loop

For ANY document operation (create, edit, convert):

```
1. Generate/modify document
2. Convert to PNG:
   pdftoppm -png -r 150 document.pdf output
3. Visually inspect the PNG at 100% zoom
4. Fix any issues found
5. REPEAT until clean
```

**Never deliver a document without PNG verification.** This catches:
- Clipped or overlapping text
- Broken tables
- Missing figures
- Formatting inconsistencies
- Orphans/widows
- Unreadable characters

### Quick Conversion Commands

```bash
# DOCX → PDF → PNG
soffice --headless --convert-to pdf document.docx
pdftoppm -png -r 150 document.pdf page

# PDF → PNG directly
pdftoppm -png -r 150 document.pdf page

# PPTX → PDF → PNG
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -png -r 150 presentation.pdf slide
```

## Typography Hygiene

### Hyphen Safety

**Never use non-breaking hyphens (U+2011)**. They cause rendering failures in many viewers.

```python
# WRONG - may render as boxes or break layouts
text = "co‑author"  # U+2011 non-breaking hyphen

# CORRECT - always use ASCII hyphen
text = "co-author"  # U+002D standard hyphen-minus
```

**Detection and fix**:
```python
# Find problematic hyphens
import re
if '\u2011' in text:
    text = text.replace('\u2011', '-')

# Also watch for other non-ASCII dashes
text = text.replace('\u2013', '-')  # en-dash
text = text.replace('\u2014', '-')  # em-dash (if hyphen intended)
```

### Citation Format

All citations must be human-readable in standard scholarly format:
- No internal tool tokens (e.g., `【4:2†source】`)
- No malformed references
- Include: Author, Title, Source, Date, URL (if applicable)

```
# WRONG
See source 【4:2†source】 for details.

# CORRECT
See Smith (2024), "Document Standards," Journal of Tech, p. 45.
```

## Spreadsheet Formula Patterns

Complements the xlsx skill's color conventions with additional patterns.

### Extended Color Codes

Beyond the standard 5 colors (blue inputs, black formulas, green cross-sheet, red external, yellow assumptions):

| Color | Meaning | Use Case |
|-------|---------|----------|
| **Gray text** | Static constants | Values that never change (tax rates, conversion factors) |
| **Orange background** | Review/caution | Cells needing verification or approval |
| **Light red background** | Errors/issues | Known problems to fix |

### Formula Simplicity

**Use helper cells instead of complex nested formulas.**

```
# WRONG - hard to debug, audit, or modify
=IF(AND(B5>100,C5<50),B5*1.1*IF(D5="A",1.2,1),B5*0.9)

# CORRECT - use helper columns
E5: =B5>100           (Threshold check)
F5: =C5<50            (Secondary check)
G5: =IF(D5="A",1.2,1) (Category multiplier)
H5: =IF(AND(E5,F5),B5*1.1*G5,B5*0.9)  (Final calculation)
```

Benefits:
- Each step is auditable
- Errors are easier to trace
- Business logic is visible
- Modifications are safer

### Avoid Dynamic Array Functions

For maximum compatibility, avoid:
- `FILTER()` - not supported in older Excel
- `XLOOKUP()` - Excel 365+ only
- `SORT()` - dynamic array function
- `SEQUENCE()` - dynamic array function
- `UNIQUE()` - dynamic array function

Use classic equivalents:
- `FILTER()` → `INDEX/MATCH` with helper columns
- `XLOOKUP()` → `INDEX/MATCH`
- `SORT()` → manual sorting or helper columns
- `SEQUENCE()` → manually entered row numbers

### Finance-Specific Formatting

Additional to xlsx skill standards:

```python
# Hide gridlines for cleaner appearance
sheet.sheet_view.showGridLines = False

# Add borders above totals (not around every cell)
from openpyxl.styles import Border, Side
thin_top = Border(top=Side(style='thin'))
total_cell.border = thin_top

# Cite sources in cell comments, not adjacent cells
from openpyxl.comments import Comment
cell.comment = Comment("Source: 10-K FY2024, p.45", "Analyst")
```

## Quality Checklist

Before delivering any document:

- [ ] PNG verification completed at 100% zoom
- [ ] No clipped or overlapping text
- [ ] Tables render correctly
- [ ] Figures/images display properly
- [ ] No U+2011 or problematic Unicode
- [ ] Citations are human-readable
- [ ] Formulas use helper cells where complex
- [ ] No Excel formula errors (#REF!, #DIV/0!, etc.)
- [ ] Professional, client-ready appearance

## Integration with Official Skills

This skill adds patterns **on top of** the document-skills plugin:

| Official Skill | This Skill Adds |
|---------------|-----------------|
| `xlsx` | Helper cells, extended colors, dynamic array warnings |
| `pdf` | Visual-first philosophy, render-inspect-fix loop |
| `docx` | Typography hygiene, PNG verification emphasis |
| `pptx` | Same verification workflow |

**Always read both this skill AND the relevant official skill** when working with documents.
