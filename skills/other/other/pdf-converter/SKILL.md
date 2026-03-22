---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: PDF Converter
description: "Convert PDF files to and from Word, Excel, Image, and other formats"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - conversion
  - format
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
    - pdf_to_docx
    - docx_to_pdf
    - html_to_pdf

# Skill Capabilities
capabilities:
  - format_conversion
  - document_transformation

# Language Support
languages:
  - en
  - zh
---

# PDF Converter

Convert PDF files to various formats and vice versa while preserving formatting.

## Overview

This skill helps you:
- Convert PDFs to editable formats (Word, Excel)
- Convert documents to PDF
- Extract images from PDFs
- Optimize conversion quality
- Handle batch conversions

## Supported Conversions

### PDF to Other Formats
| Target Format | Best For | Quality |
|---------------|----------|---------|
| **Word (.docx)** | Text-heavy documents | ⭐⭐⭐⭐ |
| **Excel (.xlsx)** | Tables and data | ⭐⭐⭐⭐ |
| **PowerPoint (.pptx)** | Presentations | ⭐⭐⭐ |
| **Images (.png/.jpg)** | Visual snapshots | ⭐⭐⭐⭐⭐ |
| **Text (.txt)** | Plain text extraction | ⭐⭐⭐⭐ |
| **HTML** | Web content | ⭐⭐⭐ |
| **Markdown (.md)** | Structured text | ⭐⭐⭐ |

### Other Formats to PDF
| Source Format | Quality Notes |
|---------------|---------------|
| **Word (.docx)** | Excellent preservation |
| **Excel (.xlsx)** | Good, check page breaks |
| **PowerPoint (.pptx)** | Excellent with animations flat |
| **Images** | Depends on resolution |
| **HTML** | Variable, CSS may differ |
| **Text (.txt)** | Perfect, but basic |

## How to Use

### Basic Conversion
```
"Convert this PDF to Word"
"Save this document as PDF"
"Extract this PDF as images"
```

### With Options
```
"Convert PDF to Word, preserve exact formatting"
"Export PDF pages 1-5 as PNG images at 300 DPI"
"Convert Excel to PDF, fit all columns on one page"
```

### Batch Conversion
```
"Convert all PDFs in this folder to Word documents"
"Create PDFs from these 10 Word files"
```

## Conversion Guidelines

### PDF to Word
```markdown
## PDF to Word Conversion

### Best Practices
1. **Check source PDF type**:
   - Native PDF (from Word/etc): Best results
   - Scanned PDF: Use OCR first
   - Image-based: Limited accuracy

2. **Formatting considerations**:
   - Complex layouts may shift
   - Fonts substitute if not installed
   - Tables may need adjustment
   - Headers/footers require review

### Quality Settings
| Setting | Result |
|---------|--------|
| **Exact** | Matches layout precisely, harder to edit |
| **Editable** | Optimized for editing, may shift layout |
| **Text only** | Plain text, no formatting |

### Common Issues
| Issue | Solution |
|-------|----------|
| Text as image | Run OCR before converting |
| Missing fonts | Embed or substitute fonts |
| Broken tables | Manually adjust in Word |
| Lost colors | Check color profile settings |
```

### PDF to Excel
```markdown
## PDF to Excel Conversion

### Ideal Sources
- PDF with clear table structure
- Financial statements
- Data reports
- Invoices with line items

### Extraction Methods
| Method | Use When |
|--------|----------|
| **Auto-detect tables** | Clear table borders |
| **Select area** | Tables without borders |
| **Full page** | Entire page is data |

### Quality Tips
1. Ensure PDF has selectable text (not scanned)
2. Clean table borders help detection
3. Merged cells may cause issues
4. Multi-page tables need manual merge

### Data Cleanup
After conversion, check:
- [ ] Column alignment
- [ ] Number formatting
- [ ] Date formats
- [ ] Merged cell handling
- [ ] Header row detection
```

### PDF to Images
```markdown
## PDF to Image Conversion

### Resolution Settings
| DPI | Use Case | File Size |
|-----|----------|-----------|
| 72 | Screen viewing | Small |
| 150 | Email/web | Medium |
| 300 | Print quality | Large |
| 600 | High-quality print | Very large |

### Format Selection
| Format | Best For |
|--------|----------|
| **PNG** | Text, graphics, transparency |
| **JPG** | Photos, smaller files |
| **TIFF** | Print production |
| **WebP** | Web optimization |

### Output Options
- All pages → separate images
- Specific pages → selected images
- Page range → batch export
```

### Document to PDF
```markdown
## Converting to PDF

### From Word
**Settings**:
- [ ] Embed fonts
- [ ] Include bookmarks
- [ ] Set PDF/A for archival
- [ ] Compress images (optional)

### From Excel
**Settings**:
- [ ] Define print area
- [ ] Set page breaks
- [ ] Choose orientation
- [ ] Fit to page options

### From PowerPoint
**Settings**:
- [ ] Slide range
- [ ] Include notes (optional)
- [ ] Quality level
- [ ] Handout format (optional)

### Universal Tips
1. Review in print preview first
2. Check page breaks
3. Ensure fonts are embedded
4. Verify hyperlinks work
```

## Batch Processing

### Batch Conversion Template
```markdown
## Batch Conversion Job

**Source**: [Folder path]
**Target Format**: [Format]
**Output Folder**: [Path]

### Files to Convert
| File | Pages | Status |
|------|-------|--------|
| document1.pdf | All | ✅ Complete |
| document2.pdf | All | ✅ Complete |
| document3.pdf | 1-5 | ⏳ Processing |

### Settings Applied
- Resolution: [X] DPI
- Quality: [High/Medium/Low]
- Naming: [Original name]_converted.[ext]

### Summary
- Total files: [X]
- Successful: [Y]
- Failed: [Z]
```

## Troubleshooting

### Common Issues
| Problem | Cause | Solution |
|---------|-------|----------|
| Text not selectable | Scanned PDF | Apply OCR first |
| Missing characters | Font issues | Embed fonts or convert |
| Poor image quality | Low DPI | Use higher resolution |
| Large file size | Uncompressed | Apply compression |
| Lost formatting | Complex layout | Use "exact" mode |

### Quality Checklist
After conversion, verify:
- [ ] All text present and readable
- [ ] Formatting approximately preserved
- [ ] Images included and clear
- [ ] Tables properly structured
- [ ] Links functional (if applicable)
- [ ] Page count matches

## Tool Recommendations

### Online Tools
- Adobe Acrobat (best quality)
- SmallPDF (easy to use)
- ILovePDF (batch friendly)
- PDF24 (free, good quality)

### Desktop Software
- Adobe Acrobat Pro
- Microsoft Office (built-in)
- LibreOffice (free)
- Foxit PDF Editor

### Command Line
- Pandoc (text formats)
- ImageMagick (images)
- pdftk (PDF manipulation)
- Poppler utilities

## Limitations

- Cannot perform actual file conversion (provides guidance)
- Scanned PDFs require OCR preprocessing
- Complex layouts may not convert perfectly
- Password-protected PDFs need password
- Some formatting always lost in conversion
- Quality depends on source PDF type
