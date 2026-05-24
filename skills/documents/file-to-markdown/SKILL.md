---
name: file-to-markdown
description: Convert any file to markdown format using the markitdown library. Use this skill when users need to convert documents (PDF, DOCX, XLSX, PPTX, images, HTML, CSV, JSON, XML, audio files, etc.) into markdown format for easier reading, editing, or integration into markdown-based workflows.
license: Complete terms in LICENSE.txt
---

# File to Markdown Converter

Convert files to markdown format using the markitdown library. This skill handles documents, images, audio, structured data, and more.

## When to Use This Skill

Use this skill when the user needs to:

- Convert documents (PDF, DOCX, PPTX, XLSX) to markdown
- Extract text from images using OCR
- Transcribe audio files to text
- Convert structured data (CSV, JSON, XML) to markdown tables
- Process web content (HTML, MHTML) into markdown
- Batch convert multiple files to markdown

## Supported Formats

**Documents**: PDF, DOCX, PPTX, XLSX

**Web**: HTML, MHTML

**Images**: PNG, JPG, JPEG, GIF (with OCR and description)

**Audio**: MP3, WAV (with transcription)

**Data**: CSV, JSON, XML

**Archives**: ZIP

**Other**: Plain text files

## Decision Tree: Choosing Your Approach

```text
User request → Single file or multiple files?
    ├─ Single file → Use helper script
    │   └─ Run: python scripts/convert_file.py <input> [output]
    │
    └─ Multiple files → Use batch conversion
        └─ Run: python scripts/batch_convert.py <input_dir> [output_dir] [--pattern PATTERN]
```

## Installation Check

Before converting, verify markitdown is installed:

```bash
pip install markitdown
```

For full functionality (image OCR, audio transcription):

```bash
pip install markitdown[all]
```

## Conversion Workflow

### Single File Conversion

**Use the helper script** as your primary method:

```bash
python scripts/convert_file.py input_file.pdf output.md
```

The script handles:

- File validation
- Conversion with error handling
- Output file creation with proper encoding
- Progress reporting

**If output filename is omitted**, the script creates `input_file.md` automatically.

### Batch Conversion

**For multiple files**, use the batch converter:

```bash
# Convert all files in a directory
python scripts/batch_convert.py ./documents

# Specify output directory
python scripts/batch_convert.py ./documents ./markdown_output

# Filter by pattern
python scripts/batch_convert.py ./documents ./output --pattern "*.pdf"

# Multiple extensions
python scripts/batch_convert.py ./documents ./output --pattern "*.{pdf,docx}"
```

The batch script:

- Automatically excludes `.md` files
- Provides progress tracking
- Reports success/failure for each file
- Creates output directories as needed

### Direct Python Integration

**When helper scripts don't fit**, use the markitdown library directly:

```python
from markitdown import MarkItDown

# Initialize converter
md = MarkItDown()

# Convert file
try:
    result = md.convert("path/to/file.pdf")
    if result and result.text_content:
        # Process or save markdown
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(result.text_content)
    else:
        print("No content extracted")
except Exception as e:
    print(f"Conversion failed: {e}")
```

## Format-Specific Guidance

### Images (PNG, JPG, GIF)

- markitdown performs OCR to extract text
- Can generate image descriptions using vision models
- Best results with clear, well-lit text
- May not preserve complex layouts perfectly

### Audio (MP3, WAV)

- Automatically transcribed to text
- Requires good audio quality for accuracy
- Processing time increases with file length
- Output formatted as markdown text

### Documents (PDF, DOCX, PPTX, XLSX)

- Text extraction maintains basic structure
- Tables converted to markdown tables
- Some complex formatting may be simplified
- XLSX: each sheet becomes a section with table

### Structured Data (CSV, JSON, XML)

- CSV: converted to markdown tables
- JSON: formatted as readable text structure
- XML: converted to hierarchical markdown

### Web Content (HTML, MHTML)

- Extracts main content
- Converts HTML to clean markdown
- Preserves links and basic formatting

## Error Handling

**Common errors and solutions:**

1. **ImportError: markitdown not installed**
   - Install with: `pip install markitdown`
   - For full features: `pip install markitdown[all]`

2. **FileNotFoundError**
   - Verify file path is correct
   - Use absolute paths when uncertain

3. **No content extracted**
   - File may be corrupted or empty
   - Format may not be supported
   - Try with a different file to verify installation

4. **Encoding errors**
   - Always use `encoding='utf-8'` when writing output files
   - Helper scripts handle this automatically

## Best Practices

- **Start with helper scripts**: They handle common cases reliably
- **Test with samples first**: Verify conversion quality before batch processing
- **Use batch converter for large sets**: More efficient than individual conversions
- **Handle errors gracefully**: Not all files convert perfectly
- **Preserve original files**: Conversion is non-destructive, but verify output before deleting sources
- **Check output quality**: Some complex formatting may not translate perfectly

## Reference Files

### scripts/

- **convert_file.py**: Single file conversion with error handling
- **batch_convert.py**: Directory-based batch conversion with pattern matching

### references/

- **markitdown_api.md**: Complete API reference for markitdown library
- **format_guide.md**: Format-specific conversion tips and limitations

**Always run scripts with `--help` first** to see current usage and options.
