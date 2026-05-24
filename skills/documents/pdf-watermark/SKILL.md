---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: PDF Watermark
description: "Add watermarks, page numbers, headers, and footers to PDFs"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - watermark
  - security
  - branding
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
    - add_watermark_to_pdf

# Skill Capabilities
capabilities:
  - watermarking
  - document_protection

# Language Support
languages:
  - en
  - zh
---

# PDF Watermark & Page Elements

Add watermarks, page numbers, headers, footers, and other overlay elements to PDF documents.

## Overview

This skill helps you:
- Add text or image watermarks
- Insert page numbers
- Create headers and footers
- Apply stamps and labels
- Batch process multiple documents

## How to Use

### Watermarks
```
"Add 'CONFIDENTIAL' watermark to this PDF"
"Apply a diagonal 'DRAFT' watermark"
"Add our company logo as a watermark"
```

### Page Numbers
```
"Add page numbers to this PDF"
"Number pages starting from page 3"
"Add 'Page X of Y' at the bottom center"
```

### Headers/Footers
```
"Add a header with the document title"
"Create a footer with date and page number"
"Add company name to every page header"
```

## Watermark Options

### Text Watermarks
```markdown
## Text Watermark Configuration

### Content
- **Text**: CONFIDENTIAL
- **Font**: Arial Bold
- **Size**: 72 pt
- **Color**: #FF0000 (Red)
- **Opacity**: 30%

### Position
- **Placement**: Center
- **Rotation**: 45° diagonal
- **Offset X**: 0
- **Offset Y**: 0

### Pages
- **Apply to**: All pages / First only / Custom range
- **Skip pages**: [None]

### Preview
```
    ╔════════════════════════╗
    ║                        ║
    ║    C O N F I D E N     ║
    ║      T I A L           ║
    ║                        ║
    ╚════════════════════════╝
```
```

### Image Watermarks
```markdown
## Image Watermark Configuration

### Image
- **File**: logo.png
- **Size**: 200 x 100 px
- **Opacity**: 20%
- **Maintain aspect ratio**: Yes

### Position
| Preset | Description |
|--------|-------------|
| Center | Middle of page |
| Top-right | Corner logo |
| Bottom-center | Footer area |
| Tile | Repeated pattern |

### Current Setting
- **Position**: Bottom-right corner
- **Margin**: 20px from edges
- **Behind text**: Yes (background)
```

### Watermark Presets
| Preset | Text | Style | Use Case |
|--------|------|-------|----------|
| **Draft** | DRAFT | Gray, diagonal, 50% | Work in progress |
| **Confidential** | CONFIDENTIAL | Red, diagonal, 30% | Sensitive docs |
| **Copy** | COPY | Blue, horizontal, 25% | Duplicates |
| **Approved** | APPROVED | Green, stamp style | Sign-off |
| **Sample** | SAMPLE | Gray, tiled | Demo documents |
| **Do Not Copy** | DO NOT COPY | Red, diagonal, 40% | Restricted |

## Page Numbers

### Configuration Options
```markdown
## Page Numbering Configuration

### Format
| Style | Example |
|-------|---------|
| Simple | 1, 2, 3 |
| Page X | Page 1 |
| X of Y | 1 of 25 |
| Section | 1-1, 1-2 |
| Roman | i, ii, iii |
| Letter | A, B, C |

### Position
| Location | Alignment |
|----------|-----------|
| Header | Left / Center / Right |
| Footer | Left / Center / Right |

### Current Setting
- **Format**: Page {n} of {total}
- **Position**: Footer, Center
- **Font**: Arial, 10pt
- **Start from**: Page 1
- **Skip pages**: Cover (page 1)
```

### Advanced Numbering
```markdown
## Advanced Page Number Scheme

### Section-Based Numbering
| Pages | Format | Example |
|-------|--------|---------|
| 1 (Cover) | None | - |
| 2-5 (Front matter) | Roman | i, ii, iii, iv |
| 6-100 (Body) | Arabic | 1, 2, 3... |
| 101-110 (Appendix) | Letter | A-1, A-2 |

### Prefix/Suffix
- **Prefix**: "Page "
- **Suffix**: " - Company Name"
- **Result**: "Page 5 - Company Name"
```

## Headers and Footers

### Header Configuration
```markdown
## Header Setup

### Layout (3-column)
| Left | Center | Right |
|------|--------|-------|
| [Logo] | Document Title | [Date] |

### Styling
- **Font**: Arial, 10pt
- **Color**: #333333
- **Line below**: Yes, 0.5pt gray

### Dynamic Fields
| Field | Code | Output |
|-------|------|--------|
| Page number | {page} | 5 |
| Total pages | {pages} | 25 |
| Date | {date} | Jan 29, 2026 |
| Time | {time} | 14:30 |
| Filename | {filename} | report.pdf |
| Title | {title} | Q4 Report |
```

### Footer Configuration
```markdown
## Footer Setup

### Layout
| Left | Center | Right |
|------|--------|-------|
| © 2026 Company | Confidential | Page {page} of {pages} |

### Styling
- **Font**: Arial, 9pt
- **Color**: #666666
- **Line above**: Yes, 0.5pt gray
- **Margin from bottom**: 0.5 inch
```

## Stamps and Labels

### Stamp Options
```markdown
## Document Stamps

### Preset Stamps
| Stamp | Style | Color |
|-------|-------|-------|
| APPROVED | ✓ Checkmark | Green |
| REJECTED | ✗ X mark | Red |
| REVIEWED | ○ Circle | Blue |
| PENDING | △ Triangle | Yellow |
| FINAL | ▢ Box | Black |

### Custom Stamp
- **Text**: SIGNED
- **Date**: Include date below
- **Name**: Include name line
- **Style**: Official stamp look
```

### Bates Numbering
```markdown
## Bates Numbering (Legal)

### Configuration
- **Prefix**: ABC-
- **Start**: 000001
- **Suffix**: -2026
- **Position**: Bottom right

### Example
ABC-000001-2026
ABC-000002-2026
ABC-000003-2026
...

### Across Multiple Documents
| Document | Start | End |
|----------|-------|-----|
| doc1.pdf (50 pages) | ABC-000001 | ABC-000050 |
| doc2.pdf (30 pages) | ABC-000051 | ABC-000080 |
| doc3.pdf (25 pages) | ABC-000081 | ABC-000105 |
```

## Batch Processing

### Batch Watermark Job
```markdown
## Batch Watermark Application

### Input
- **Folder**: /documents/contracts/
- **Files**: 25 PDFs
- **Total Pages**: 450

### Watermark Settings
- **Type**: Text
- **Text**: CONFIDENTIAL
- **Style**: Diagonal, 30% opacity, red

### Progress
| File | Pages | Status |
|------|-------|--------|
| contract_001.pdf | 15 | ✅ Complete |
| contract_002.pdf | 22 | ✅ Complete |
| contract_003.pdf | 18 | ⏳ Processing |
| ... | ... | ... |

### Results
- Processed: 25/25 files
- Total pages watermarked: 450
- Output folder: /documents/contracts_watermarked/
```

## Output Example

### Watermark Report
```markdown
## Watermark Application Report

### Document
- **Input**: quarterly_report.pdf
- **Output**: quarterly_report_watermarked.pdf
- **Pages**: 45

### Applied Elements
| Element | Details | Pages |
|---------|---------|-------|
| Watermark | "CONFIDENTIAL" diagonal | All |
| Logo | Company logo, bottom-right | All |
| Page numbers | "Page X of Y", footer center | 2-45 |
| Header | Title + Date | All |
| Footer | Copyright notice | All |

### Verification
- [ ] Watermark visible but not obscuring content
- [ ] Page numbers sequential and correct
- [ ] Headers/footers properly positioned
- [ ] No content overlap issues
```

## Tool Recommendations

### Online Tools
- **SmallPDF**: Easy watermarking
- **ILovePDF**: Good page numbers
- **PDF24**: Free, configurable
- **Sejda**: Many options

### Desktop Software
- **Adobe Acrobat Pro**: Full control
- **Foxit PDF Editor**: Good features
- **PDF-XChange**: Many options
- **Preview (Mac)**: Basic only

### Programmatic
- **pdf-lib** (JavaScript): Full control
- **PyPDF2** (Python): Basic watermarks
- **iText** (Java/.NET): Professional
- **PDFBox** (Java): Good options

## Limitations

- Cannot perform actual watermarking (provides guidance)
- Image watermarks need proper resolution
- Some secured PDFs prevent modifications
- Complex watermarks may increase file size
- Position may vary with different page sizes
- Font availability affects text watermarks
