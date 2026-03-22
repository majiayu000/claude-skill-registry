---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: PDF OCR Extraction
description: "Extract text from scanned PDFs using optical character recognition"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - ocr
  - scan
  - text-extraction
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
    - extract_text_from_pdf

# Skill Capabilities
capabilities:
  - ocr_processing
  - scanned_document_handling

# Language Support
languages:
  - en
  - zh
---

# PDF OCR Extraction

Extract text from scanned documents and image-based PDFs using OCR technology.

## Overview

This skill helps you:
- Extract text from scanned documents
- Make image PDFs searchable
- Digitize paper documents
- Process handwritten text (limited)
- Batch process multiple documents

## How to Use

### Basic OCR
```
"Extract text from this scanned PDF"
"OCR this document image"
"Make this PDF searchable"
```

### With Options
```
"Extract text from pages 1-10, English language"
"OCR this document, preserve layout"
"Extract and output as structured data"
```

## Document Types

### OCR Quality by Document Type
| Document Type | Expected Quality | Tips |
|---------------|------------------|------|
| **Typed documents** | ⭐⭐⭐⭐⭐ 95%+ | Best results |
| **Printed books** | ⭐⭐⭐⭐ 90%+ | Watch for aging |
| **Forms** | ⭐⭐⭐⭐ 85%+ | Check boxes may need manual |
| **Tables/Data** | ⭐⭐⭐ 80%+ | Structure may need fixing |
| **Handwritten (neat)** | ⭐⭐ 60-80% | Variable results |
| **Handwritten (cursive)** | ⭐ 30-60% | Often needs manual review |
| **Mixed content** | ⭐⭐⭐ 75%+ | Depends on complexity |

## Output Formats

### Plain Text Extraction
```markdown
## OCR Result: [Document Name]

**Pages Processed**: [X]
**Language**: [Detected/Specified]
**Confidence**: [X]%

---

[Extracted text content here]

---

### Notes
- [Any issues or uncertainties]
- [Characters that may be incorrect]
```

### Structured Extraction
```markdown
## OCR Extraction: [Document Name]

### Document Info
| Field | Value |
|-------|-------|
| Title | [Extracted or inferred] |
| Date | [If found] |
| Author | [If found] |

### Content by Section

#### [Header 1]
[Content under this header]

#### [Header 2]
[Content under this header]

### Tables Found
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| [Data] | [Data] | [Data] |

### Uncertain Text
| Page | Original | Confidence | Possible |
|------|----------|------------|----------|
| 3 | "teh" | 70% | "the" |
| 5 | "l0ve" | 65% | "love" |
```

### Searchable PDF Output
```markdown
## OCR to Searchable PDF

**Source**: [filename.pdf]
**Output**: [filename_searchable.pdf]

### Processing Summary
| Metric | Value |
|--------|-------|
| Pages | [X] |
| Words extracted | [Y] |
| Average confidence | [Z]% |
| Processing time | [T] seconds |

### Quality Report
- [X] pages with 95%+ confidence
- [Y] pages with 80-94% confidence
- [Z] pages with <80% confidence (review recommended)

### Searchability
✅ Document is now text-searchable
✅ Original images preserved
✅ Text layer added behind images
```

## Pre-Processing Tips

### Image Quality Checklist
Before OCR, ensure:
- [ ] **Resolution**: 300 DPI minimum (600 for small text)
- [ ] **Contrast**: Clear black text on white background
- [ ] **Alignment**: Document is straight (not skewed)
- [ ] **Completeness**: No cut-off edges
- [ ] **Cleanliness**: No stains, marks, or shadows

### Common Pre-Processing Steps
| Issue | Solution |
|-------|----------|
| Low resolution | Upscale image first |
| Skewed/rotated | Auto-deskew |
| Poor contrast | Adjust levels/threshold |
| Noise/specks | Apply noise reduction |
| Shadows | Flatten lighting |
| Color document | Convert to grayscale |

## Language Support

### Supported Languages
- **Excellent**: English, Spanish, French, German, Italian
- **Good**: Chinese (Simplified/Traditional), Japanese, Korean
- **Moderate**: Arabic, Hebrew (RTL support), Hindi
- **Basic**: Many others with varying quality

### Multi-Language Documents
```
"OCR this document, detect language automatically"
"Extract text, primary: English, secondary: Chinese"
```

## Handling Specific Content

### Forms and Checkboxes
```markdown
## Form Extraction: [Form Name]

### Field Values
| Field | Value | Confidence |
|-------|-------|------------|
| Name | John Smith | 98% |
| Date | 01/15/2026 | 95% |
| Address | 123 Main St | 92% |

### Checkboxes
| Question | Checked |
|----------|---------|
| Option A | ☑️ Yes |
| Option B | ☐ No |
| Option C | ☑️ Yes |

### Signature
[Signature detected on page X - cannot extract text]
```

### Tables
```markdown
## Table Extraction

### Table 1 (Page 2)
| Header A | Header B | Header C |
|----------|----------|----------|
| Value 1 | Value 2 | Value 3 |
| Value 4 | Value 5 | Value 6 |

**Table confidence**: 85%
**Note**: Column 3 may have alignment issues
```

### Handwritten Text
```markdown
## Handwritten Text Extraction

**Legibility Assessment**: [Good/Fair/Poor]
**Recommended**: Manual review

### Extracted Text (Confidence: 65%)
[Extracted text with uncertain words marked]

### Uncertain Words
| Original | Best Guess | Alternatives |
|----------|------------|--------------|
| [image] | "meeting" | "meeting", "meaning" |
| [image] | "Tuesday" | "Tuesday", "Thursday" |

⚠️ **Low confidence extraction - please verify manually**
```

## Batch Processing

### Batch OCR Job
```markdown
## Batch OCR Processing

**Folder**: [Path]
**Total Documents**: [X]
**Status**: [In Progress/Complete]

### Results
| File | Pages | Confidence | Status |
|------|-------|------------|--------|
| doc1.pdf | 5 | 96% | ✅ Complete |
| doc2.pdf | 12 | 88% | ✅ Complete |
| doc3.pdf | 3 | 72% | ⚠️ Review |
| doc4.pdf | 8 | - | ❌ Failed |

### Issues
- doc3.pdf: Pages 2-3 have handwriting
- doc4.pdf: File corrupted

### Summary
- Successful: [X]
- Need Review: [Y]
- Failed: [Z]
```

## Tool Recommendations

### Cloud Services
- Google Cloud Vision (excellent accuracy)
- Amazon Textract (good for forms)
- Azure Computer Vision (balanced)
- Adobe Acrobat (integrated)

### Desktop Software
- ABBYY FineReader (best accuracy)
- Adobe Acrobat Pro (reliable)
- Readiris (good value)
- Tesseract (free, open source)

### Programming Libraries
- pytesseract (Python + Tesseract)
- EasyOCR (Python, multi-language)
- PaddleOCR (Python, good for Asian languages)

## Limitations

- Cannot guarantee 100% accuracy
- Handwritten text has low accuracy
- Very small text may not extract well
- Decorative fonts are problematic
- Background images reduce quality
- Cannot read text in complex graphics
- Processing time increases with pages
