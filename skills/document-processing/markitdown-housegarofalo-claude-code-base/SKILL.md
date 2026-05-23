---
name: markitdown
description: Expert guidance for converting files to Markdown using Microsoft's MarkItDown utility. Convert PDF, Word, PowerPoint, Excel, images, audio, HTML, CSV, JSON, XML, ZIP, and EPub files to LLM-friendly Markdown format. Use when processing documents for AI analysis, extracting content from files, or preparing data for language models. Triggers on markitdown, document conversion, pdf to markdown, docx to markdown, file extraction, document processing.
---

# MarkItDown Document Conversion

Convert files to Markdown using Microsoft's MarkItDown utility.

## Installation

### Full Installation

```bash
pip install 'markitdown[all]'
```

### Selective Installation

```bash
pip install 'markitdown[pdf]'                    # PDF only
pip install 'markitdown[docx]'                   # Word documents
pip install 'markitdown[pptx]'                   # PowerPoint
pip install 'markitdown[xlsx]'                   # Excel
pip install 'markitdown[audio]'                  # Audio transcription
pip install 'markitdown[image]'                  # Image OCR
pip install 'markitdown[azure-doc-intelligence]' # Azure AI PDF
pip install 'markitdown[llm]'                    # LLM image descriptions
```

## Command-Line Usage

```bash
# Basic conversion
markitdown file.pdf

# Save to file
markitdown file.pdf > output.md
markitdown file.pdf -o output.md

# Batch conversion
for file in *.pdf; do markitdown "$file" > "${file%.pdf}.md"; done
```

## Python API

### Basic Usage

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

### Stream Processing

```python
with open("file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```

### With Azure Document Intelligence

```python
md = MarkItDown(
    azure_doc_intelligence_endpoint="https://your-resource.cognitiveservices.azure.com",
    azure_doc_intelligence_key="your-key"
)
```

### With LLM Image Descriptions

```python
md = MarkItDown(
    llm_model="gpt-4o",
    llm_client=None  # Uses default client
)
```

## Supported Formats

| Format | Extensions | Features |
|--------|-----------|----------|
| **PDF** | .pdf | Text, tables, links, structure |
| **Word** | .docx | Headings, lists, tables, images, links |
| **PowerPoint** | .pptx | Slides, titles, content, images |
| **Excel** | .xlsx, .xls | Sheets, tables, headers |
| **Images** | .png, .jpg, .gif | EXIF, OCR, LLM descriptions |
| **Audio** | .wav, .mp3 | Transcription, timestamps |
| **HTML** | .html | Content, links, tables |
| **CSV** | .csv | Data tables |
| **JSON** | .json | Structure preservation |
| **XML** | .xml | Data extraction |
| **ZIP** | .zip | Archive processing |
| **EPub** | .epub | E-book content |
| **YouTube** | URLs | Metadata, transcripts |

## Common Patterns

### Batch Processing

```python
import os
from markitdown import MarkItDown

md = MarkItDown()

for filename in os.listdir("input/"):
    if filename.endswith(('.pdf', '.docx', '.pptx')):
        result = md.convert(f"input/{filename}")
        base = os.path.splitext(filename)[0]
        with open(f"output/{base}.md", "w") as f:
            f.write(result.text_content)
```

### Error Handling

```python
try:
    result = md.convert("file.pdf")
    markdown = result.text_content
except Exception as e:
    print(f"Conversion failed: {e}")
```

### Memory-Efficient Processing

```python
with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```

## Docker Usage

```bash
# Build
docker build -t markitdown:latest .

# Run
docker run --rm -i markitdown:latest < input.pdf > output.md

# With volume
docker run --rm -v $(pwd):/data markitdown:latest /data/file.pdf
```

## Output Format

MarkItDown produces clean, structured Markdown:

```markdown
# Document Title

## Section Heading

Content with **bold** and *italic* formatting.

- Bullet lists
- Preserved from source

| Table | Headers |
|-------|---------|
| Data  | Values  |

[Links](https://example.com) maintained.
```

## Best Practices

### Performance
- Use streams for files >10MB
- Batch process multiple files
- Cache converted results
- Use selective dependencies

### Quality
- High-resolution images for OCR
- Well-formatted source documents
- Azure Document Intelligence for complex PDFs
- LLM descriptions for important images

### Integration
- Check token counts for LLM limits
- Chunk long documents
- Preserve metadata in context
- Validate output structure

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | `pip install --upgrade 'markitdown[all]'` |
| Memory errors | Use `convert_stream()` instead of `convert()` |
| Poor OCR | Increase image resolution, use Azure |
| Missing content | Check source file quality |

## Requirements

- Python 3.10+
- Virtual environment recommended
- Optional: Azure subscription for enhanced features
- Optional: OpenAI API for image descriptions

## When to Use This Skill

- Converting documents for AI analysis
- Extracting content from PDFs
- Processing Word/PowerPoint files
- Preparing data for language models
- Batch document conversion
- Building document pipelines
