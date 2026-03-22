---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: office-mcp
description: "MCP server with 39 tools for Word, Excel, PowerPoint, PDF, OCR operations"
version: "2.1"
author: claude-office-skills
license: MIT

# Categorization
category: workflow
tags:
  - office
  - mcp
  - pdf
  - excel
  - word
  - powerpoint
  - automation
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

# Skill Capabilities
capabilities:
  - office_automation
  - mcp_tools
  - pdf_processing
  - spreadsheet_analysis
  - document_generation
  - presentation_creation
  - format_conversion

# Language Support
languages:
  - en
  - zh
---

# Office MCP Server

## Overview

A complete MCP (Model Context Protocol) server providing **39 tools** for Office document operations. Implemented in TypeScript/Node.js with real functionality (not placeholders).

## Tool Categories

### PDF Tools (10)
| Tool | Description |
|------|-------------|
| `extract_text_from_pdf` | Extract text content, supports page selection |
| `extract_tables_from_pdf` | Extract table data from PDFs |
| `merge_pdfs` | Merge multiple PDFs into one |
| `split_pdf` | Split PDF by page ranges |
| `compress_pdf` | Reduce PDF file size |
| `add_watermark_to_pdf` | Add text/image watermarks |
| `fill_pdf_form` | Fill PDF form fields |
| `get_pdf_metadata` | Get PDF properties and metadata |
| `ocr_pdf` | OCR on scanned PDFs (multi-language) |
| `ocr_image` | OCR on image files (PNG, JPG, TIFF, etc.) |

### Spreadsheet Tools (7)
| Tool | Description |
|------|-------------|
| `read_xlsx` | Read Excel files with sheet/range selection |
| `create_xlsx` | Create multi-sheet Excel files |
| `analyze_spreadsheet` | Statistical analysis (min/max/mean/median) |
| `apply_formula` | Apply Excel formulas to cells |
| `create_chart` | Generate chart configurations |
| `pivot_table` | Create pivot tables with aggregation |
| `xlsx_to_json` | Convert Excel to JSON |

### Document Tools (6)
| Tool | Description |
|------|-------------|
| `extract_text_from_docx` | Extract text from Word documents |
| `create_docx` | Create DOCX with headings, lists, tables |
| `fill_docx_template` | Fill templates with {{placeholders}} |
| `analyze_document_structure` | Analyze headings, tables, word count |
| `insert_table_to_docx` | Insert tables into documents |
| `merge_docx_files` | Merge multiple Word documents |

### Conversion Tools (9)
| Tool | Description |
|------|-------------|
| `xlsx_to_csv` | Convert Excel to CSV |
| `csv_to_xlsx` | Convert CSV to Excel |
| `json_to_xlsx` | Convert JSON arrays to Excel |
| `docx_to_md` | Convert Word to Markdown |
| `md_to_docx` | Convert Markdown to Word |
| `pdf_to_docx` | Convert PDF to Word (text extraction) |
| `docx_to_pdf` | Convert Word to PDF (external tool required) |
| `html_to_pdf` | Convert HTML to PDF (external tool required) |
| `batch_convert` | Batch convert multiple files |

### Presentation Tools (7)
| Tool | Description |
|------|-------------|
| `create_pptx` | Create PowerPoint with themes |
| `extract_from_pptx` | Extract text and images from PPTX |
| `md_to_pptx` | Convert Markdown to slides |
| `add_slide` | Add slides to existing presentations |
| `update_slide` | Update slide content |
| `pptx_to_html` | Convert to reveal.js HTML |
| `get_pptx_outline` | Get presentation structure |

## Installation

### 1. Clone and Build

```bash
cd mcp-servers/office-mcp
npm install
npm run build
```

### 2. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "office-mcp": {
      "command": "/usr/local/bin/node",
      "args": ["/path/to/claude-office-skills/mcp-servers/office-mcp/dist/index.js"]
    }
  }
}
```

### 3. Restart Claude Desktop

## Example Prompts

- "Read the Excel file at ~/Documents/sales.xlsx"
- "Create a PowerPoint with 5 slides about AI trends"
- "Extract text from this PDF and convert to Markdown"
- "Merge these 3 Word documents into one"
- "Analyze the data in this spreadsheet"

## Dependencies

```
pdf-parse, pdf-lib       - PDF operations
tesseract.js             - OCR (pure JavaScript, no native binary needed)
xlsx                     - Excel operations
mammoth, docx            - Word operations
docxtemplater, pizzip    - Template filling
pptxgenjs, jszip         - PowerPoint operations
turndown, marked         - Markdown conversion
```

### Supported OCR Languages
- `eng` - English
- `chi_sim` - Simplified Chinese
- `chi_tra` - Traditional Chinese
- `jpn` - Japanese
- `kor` - Korean
- `fra` - French
- `deu` - German
- `spa` - Spanish

## Resources

- [MCP Server Code](https://github.com/claude-office-skills/skills/tree/main/mcp-servers/office-mcp)
- [Implementation Plan](./mcp-servers/office-mcp/IMPLEMENTATION_PLAN.md)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
