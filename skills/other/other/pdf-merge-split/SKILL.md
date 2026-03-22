---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: PDF Merge & Split
description: "Combine multiple PDFs or split into separate files"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - merge
  - split
  - combine
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - merge_pdfs
    - split_pdf

# Skill Capabilities
capabilities:
  - pdf_merging
  - pdf_splitting
  - page_management

# Language Support
languages:
  - en
  - zh
---

# PDF Merge & Split

Combine multiple PDF files into one or split PDFs into separate documents.

## Overview

This skill helps you:
- Merge multiple PDFs into a single file
- Split PDFs by page ranges
- Extract specific pages
- Reorder pages within a PDF
- Create custom arrangements

## How to Use

### Merge PDFs
```
"Merge these 3 PDFs into one file"
"Combine document1.pdf and document2.pdf"
"Join all PDFs in this folder in alphabetical order"
```

### Split PDF
```
"Split this PDF into individual pages"
"Extract pages 5-10 from this PDF"
"Split this PDF every 5 pages"
```

### Reorder
```
"Move page 3 to the end"
"Reorder pages: 1, 3, 2, 4, 5"
"Reverse the page order"
```

## Merge Operations

### Basic Merge
```markdown
## PDF Merge Plan

### Input Files
| Order | File | Pages | Size |
|-------|------|-------|------|
| 1 | cover.pdf | 1 | 50 KB |
| 2 | chapter1.pdf | 15 | 2.1 MB |
| 3 | chapter2.pdf | 22 | 3.4 MB |
| 4 | appendix.pdf | 8 | 1.2 MB |

### Output
- **Filename**: combined_document.pdf
- **Total Pages**: 46
- **Estimated Size**: ~6.7 MB

### Merge Options
- [ ] Add bookmarks for each source file
- [ ] Preserve original bookmarks
- [ ] Include blank page between files
- [ ] Optimize/compress output
```

### Advanced Merge
```markdown
## Advanced PDF Merge

### Custom Page Selection
| Source | Pages to Include | Insert Position |
|--------|------------------|-----------------|
| main.pdf | 1-10 | 1-10 |
| insert.pdf | All (5 pages) | After page 10 |
| main.pdf | 11-20 | 16-25 |
| appendix.pdf | 2-4 only | 26-28 |

### Output Configuration
- **Filename**: custom_merged.pdf
- **Page numbering**: Reset to 1 / Continue from original
- **Bookmarks**: Create from filenames / Preserve all

### Quality Settings
- Resolution: Original / Reduce to [X] DPI
- Compression: None / Low / Medium / High
```

## Split Operations

### Split by Range
```markdown
## PDF Split Plan

### Source
- **File**: large_document.pdf
- **Total Pages**: 100

### Split Configuration
| Output File | Page Range | Pages |
|-------------|------------|-------|
| part1.pdf | 1-25 | 25 |
| part2.pdf | 26-50 | 25 |
| part3.pdf | 51-75 | 25 |
| part4.pdf | 76-100 | 25 |

### Naming Pattern
`[original_name]_part[N].pdf`
```

### Split by Size
```markdown
## Split by File Size

### Source
- **File**: huge_report.pdf
- **Total Pages**: 500
- **File Size**: 250 MB

### Target
- **Max file size**: 25 MB
- **Estimated splits**: ~10 files

### Output
| File | Pages | Actual Size |
|------|-------|-------------|
| report_001.pdf | 1-52 | 24.8 MB |
| report_002.pdf | 53-98 | 23.2 MB |
| ... | ... | ... |
```

### Split by Bookmark
```markdown
## Split by Bookmarks/Chapters

### Source Structure
- large_manual.pdf
  - Chapter 1: Introduction (p.1)
  - Chapter 2: Setup (p.15)
  - Chapter 3: Usage (p.45)
  - Chapter 4: Advanced (p.120)
  - Appendix (p.180)

### Split Output
| File | Chapter | Pages |
|------|---------|-------|
| ch1_introduction.pdf | Introduction | 1-14 |
| ch2_setup.pdf | Setup | 15-44 |
| ch3_usage.pdf | Usage | 45-119 |
| ch4_advanced.pdf | Advanced | 120-179 |
| appendix.pdf | Appendix | 180-end |
```

### Extract Specific Pages
```markdown
## Page Extraction

### Source
- **File**: contract.pdf (20 pages)

### Pages to Extract
- [x] Page 1 (Cover)
- [x] Pages 5-7 (Terms)
- [x] Page 15 (Signatures)
- [x] Page 20 (Appendix A)

### Output
- **File**: contract_key_pages.pdf
- **Pages**: 6 total (1, 5, 6, 7, 15, 20)
```

## Page Operations

### Reorder Pages
```markdown
## Page Reorder Plan

### Current Order
1, 2, 3, 4, 5, 6, 7, 8, 9, 10

### New Order
1, 2, 4, 3, 5, 6, 8, 7, 9, 10

### Changes
- Page 3 ↔ Page 4 (swapped)
- Page 7 ↔ Page 8 (swapped)
```

### Delete Pages
```markdown
## Page Deletion

### Source
- document.pdf (25 pages)

### Pages to Remove
- Page 3 (blank page)
- Pages 12-14 (outdated section)
- Page 25 (draft watermark)

### Result
- New page count: 20
- Output: document_cleaned.pdf
```

### Insert Pages
```markdown
## Page Insertion

### Base Document
- main.pdf (10 pages)

### Insertions
| Insert | After Page | From |
|--------|------------|------|
| Cover page | 0 (beginning) | cover.pdf |
| Diagram | 5 | diagrams.pdf (page 2) |
| Appendix | 10 (end) | appendix.pdf |

### Result
- New page count: 14
```

### Rotate Pages
```markdown
## Page Rotation

### File: scanned_doc.pdf

### Rotations Needed
| Page(s) | Current | Rotation | New |
|---------|---------|----------|-----|
| 3 | Portrait | 90° CW | Landscape |
| 7-9 | Upside down | 180° | Correct |
| 15 | Landscape | 90° CCW | Portrait |
```

## Batch Processing

### Batch Merge
```markdown
## Batch Merge Job

### Task: Merge PDFs by Project

### Folder Structure
```
/reports/
  /project-a/
    report1.pdf
    report2.pdf
  /project-b/
    summary.pdf
    details.pdf
```

### Output
| Merged File | Sources |
|-------------|---------|
| project-a_combined.pdf | report1.pdf, report2.pdf |
| project-b_combined.pdf | summary.pdf, details.pdf |
```

### Batch Split
```markdown
## Batch Split Job

### Input
- /monthly_reports/ (12 files, each ~50 pages)

### Operation
- Split each file into 5-page chunks

### Output
- /monthly_reports_split/
  - jan_001.pdf, jan_002.pdf, ...
  - feb_001.pdf, feb_002.pdf, ...
  - ...
```

## Tool Recommendations

### Free Tools
- **PDF24**: Web and desktop, full featured
- **ILovePDF**: Web-based, easy to use
- **PDFsam Basic**: Desktop, open source
- **Preview (Mac)**: Built-in, drag and drop

### Professional
- **Adobe Acrobat Pro**: Industry standard
- **Foxit PDF Editor**: Full featured
- **Nitro Pro**: Good for business

### Command Line
- **pdftk**: Classic, powerful
- **qpdf**: Fast, scriptable
- **pdfcpu**: Modern Go-based tool

## Limitations

- Cannot perform actual file operations (provides guidance)
- Password-protected PDFs need password first
- Very large files may need chunked processing
- Some PDFs with restrictions cannot be modified
- Merging different page sizes may cause issues
