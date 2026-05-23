---
name: convert-to-markdown
description: Convert documents and files to Markdown using markitdown with Windows/WSL path handling. Supports PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs. Use when converting files to markdown, processing Confluence exports, handling Windows/WSL path conversions, extracting images from PDFs, or working with markitdown utility.
description_vi: Chuyển đổi tài liệu và file sang Markdown bằng markitdown với hỗ trợ đường dẫn Windows/WSL. Hỗ trợ PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (EXIF/OCR), audio (transcription), ZIP archives, YouTube URLs, hoặc EPubs. Dùng khi chuyển file sang markdown, xử lý Confluence exports, chuyển đổi path Windows/WSL, trích xuất images từ PDFs, hoặc làm việc với markitdown.
keywords_vi: [markdown, convert, markitdown, pdf to markdown, word to markdown, chuyển đổi tài liệu, exif, ocr, transcription, windows, wsl]
---

# Markdown Tools

Convert documents to markdown using `markitdown` with support for multiple formats, image extraction, and Windows/WSL path handling.

## Quick Start

### Installation Options

**Option 1: uvx (no installation required)**
```bash
# Run directly without installing
uvx markitdown input.pdf -o output.md
```

**Option 2: uv tool install (recommended for PDF support)**
```bash
# Install with PDF support
uv tool install "markitdown[pdf]"

# Or via pip
pip install "markitdown[pdf]"

# Then use directly
markitdown "document.pdf" -o output.md
```

## Supported Formats

- **Documents**: PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls)
- **Web/Data**: HTML, CSV, JSON, XML
- **Media**: Images (EXIF + OCR), Audio (EXIF + transcription)
- **Other**: ZIP (iterates contents), YouTube URLs, EPub

## Basic Usage

### Using uvx (no install)

```bash
# Convert to stdout
uvx markitdown input.pdf

# Save to file
uvx markitdown input.pdf -o output.md
uvx markitdown input.docx > output.md

# From stdin
cat input.pdf | uvx markitdown
```

### Using installed markitdown

```bash
# Basic conversion
markitdown "document.pdf" -o output.md

# Redirect output
markitdown "document.pdf" > output.md
```

## Command Options

```bash
-o OUTPUT      # Output file
-x EXTENSION   # Hint file extension (for stdin)
-m MIME_TYPE   # Hint MIME type
-c CHARSET     # Hint charset (e.g., UTF-8)
-d             # Use Azure Document Intelligence
-e ENDPOINT    # Document Intelligence endpoint
--use-plugins  # Enable 3rd-party plugins
--list-plugins # Show installed plugins
```

## PDF Conversion with Images

markitdown extracts text only. For PDFs with images, use this workflow:

### Step 1: Convert Text

```bash
markitdown "document.pdf" -o output.md
```

### Step 2: Extract Images

```bash
# Create assets directory alongside the markdown
mkdir -p assets

# Extract images using PyMuPDF
uv run --with pymupdf python scripts/extract_pdf_images.py "document.pdf" ./assets
```

### Step 3: Add Image References

Insert image references in the markdown where needed:

```markdown
![Description](assets/img_page1_1.png)
```

### Step 4: Format Cleanup

markitdown output often needs manual fixes:
- Add proper heading levels (`#`, `##`, `###`)
- Reconstruct tables in markdown format
- Fix broken line breaks
- Restore indentation structure

## Path Conversion (Windows/WSL)

```bash
# Windows → WSL conversion
C:\Users\name\file.pdf → /mnt/c/Users/name/file.pdf

# Use helper script
python scripts/convert_path.py "C:\Users\name\Documents\file.pdf"
```

## Advanced Examples

### Convert Word document

```bash
uvx markitdown report.docx -o report.md
```

### Convert Excel spreadsheet

```bash
uvx markitdown data.xlsx > data.md
```

### Convert PowerPoint presentation

```bash
uvx markitdown slides.pptx -o slides.md
```

### Convert with file type hint (for stdin)

```bash
cat document | uvx markitdown -x .pdf > output.md
```

### Use Azure Document Intelligence for better PDF extraction

```bash
uvx markitdown scan.pdf -d -e "https://your-resource.cognitiveservices.azure.com/"
```

## Common Issues

**"dependencies needed to read .pdf files"**
```bash
# Install with PDF support
uv tool install "markitdown[pdf]" --force
```

**FontBBox warnings during PDF conversion**
- These are harmless font parsing warnings, output is still correct

**Images missing from output**
- Use `scripts/extract_pdf_images.py` to extract images separately

## Notes

- Output preserves document structure: headings, tables, lists, links
- First run caches dependencies; subsequent runs are faster
- For complex PDFs with poor extraction, use `-d` with Azure Document Intelligence
- Works on Windows, WSL, macOS, and Linux

## Resources

- `scripts/extract_pdf_images.py` - Extract images from PDF using PyMuPDF
- `scripts/convert_path.py` - Windows to WSL path converter
- `references/conversion-examples.md` - Detailed examples for batch operations
