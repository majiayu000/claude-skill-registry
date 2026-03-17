---
name: markitdown
description: Expert guidance for converting files to Markdown using Microsoft's MarkItDown utility. Convert PDF, Word, PowerPoint, Excel, images, audio, HTML, CSV, JSON, XML, ZIP, and EPub files to LLM-friendly Markdown format. Use when processing documents for AI analysis, extracting content from files, or preparing data for language models.
---

# MarkItDown File Conversion Expert

Expert guidance for converting diverse file formats to Markdown using Microsoft's MarkItDown utility. Transform documents, media, web content, and structured data into token-efficient Markdown optimized for LLM consumption.

## Core Capabilities

1. **Document Conversion** - PDF, Word, PowerPoint, Excel
2. **Media Processing** - Images (OCR), Audio (transcription)
3. **Web Content** - HTML, YouTube URLs
4. **Structured Data** - CSV, JSON, XML
5. **Archive Handling** - ZIP files, EPub e-books
6. **LLM Optimization** - Token-efficient output for AI models

## Quick Reference

### Supported Formats

| Category | Formats |
|----------|---------|
| **Documents** | PDF, DOCX, PPTX, XLSX/XLS |
| **Media** | Images (PNG, JPG, GIF), Audio (WAV, MP3) |
| **Web** | HTML, YouTube URLs |
| **Data** | CSV, JSON, XML |
| **Archives** | ZIP, EPub |

### Key Features

- **Structure Preservation** - Maintains headings, lists, tables, links
- **Token Efficiency** - Optimized for LLM consumption
- **OCR Support** - Extract text from images
- **Audio Transcription** - Convert speech to text
- **EXIF Metadata** - Extract image metadata
- **Azure Integration** - Advanced PDF processing
- **LLM Descriptions** - Image descriptions via OpenAI

---

## Instructions

### Installation

**Python 3.10+ Required**

**Full Installation (All Features):**
```bash
pip install 'markitdown[all]'
```

**Selective Installation:**
```bash
# PDF support only
pip install 'markitdown[pdf]'

# Office documents
pip install 'markitdown[docx,pptx,xlsx]'

# Media files
pip install 'markitdown[audio,image]'

# Multiple features
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

### Command-Line Usage

**Basic Con```bash
# Output to stdout
markitdown document.pdf

# Save to file
markitdown document.pdf > output.md

# Specify output file
markitdown document.pdf -o output.md
```

**Batch Con```bash
# Convert multiple files
for file in *.pdf; do
  markitdown "$file" > "${file%.pdf}.md"
done
```

### Python API Usage

**Basic Con```python
from markitdown import MarkItDown

# Initialize converter
md = MarkItDown()

# Convert file
result = md.convert("document.pdf")
print(result.text_content)

# Save to file
with open("output.md", "w") as f:
    f.write(result.text_content)
```

**Convert from Stream:**
```python
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)
```

**Batch Processing:**
```python
import os
from markitdown import MarkItDown

md = MarkItDown()
input_dir = "./documents"
output_dir = "./markdown"

for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)
    if os.path.isfile(input_path):
        result = md.convert(input_path)

        # Create output filename
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.md")

        with open(output_path, "w") as f:
            f.write(result.text_content)

        print(f"Converted: {filename}")
```

---

## Advanced Features

### Azure Document Intelligence

Enhanced PDF processing with Azure AI.

**Setup:**
```bash
pip install 'markitdown[azure-doc-intelligence]'
```

**Configuration:**
```python
from markitdown import MarkItDown

md = MarkItDown(
    azure_doc_intelligence_endpoint="https://your-resource.cognitiveservices.azure.com",
    azure_doc_intelligence_key="your-key-here"
)

result = md.convert("complex-document.pdf")
```

**Benefits:**
- Better table extraction
- Improved layout understanding
- Enhanced text recognition
- Complex document handling

---

### LLM-Powered Image Descriptions

Generate AI descriptions for images in documents.

**Setup:**
```bash
pip install 'markitdown[llm]'
```

**Configuration:**
```python
from markitdown import MarkItDown

md = MarkItDown(
    llm_model="gpt-4o",  # or gpt-4o-mini
    llm_client=None       # Uses default Azure OpenAI or OpenAI
)

# Convert PowerPoint with image descriptions
result = md.convert("presentation.pptx")
```

**Supported:**
- PowerPoint slides with images
- Standalone image files
- Images in other document types

---

### Docker Usage

**Build Image:**
```bash
docker build -t markitdown:latest .
```

**Run Con```bash
docker run --rm -i markitdown:latest < document.pdf > output.md
```

**Volume Mounting:**
```bash
docker run --rm -v $(pwd):/data markitdown:latest /data/document.pdf > output.md
```

---

## Common Workflows

### Document Processing Pipeline

**Workflow:**
```
1. Receive document (PDF, Word, Excel, etc.)
2. Convert to Markdown with MarkItDown
3. Process Markdown with LLM
4. Extract insights or generate summaries
5. Present results
```

**Python Implementation:**
```python
from markitdown import MarkItDown

def process_document(file_path):
    # Convert to Markdown
    md = MarkItDown()
    result = md.convert(file_path)
    markdown_content = result.text_content

    # Process with LLM (your code here)
    # insights = analyze_with_llm(markdown_content)

    return markdown_content

# Process multiple documents
documents = ["report.pdf", "data.xlsx", "slides.pptx"]
for doc in documents:
    content = process_document(doc)
    print(f"Processed: {doc}")
```

---

### Batch Document Conversion

**Script:**
```python
import os
from pathlib import Path
from markitdown import MarkItDown

def batch_convert(input_folder, output_folder):
    md = MarkItDown()

    # Create output folder
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Get all supported files
    supported_extensions = [
        '.pdf', '.docx', '.pptx', '.xlsx', '.xls',
        '.html', '.csv', '.json', '.xml', '.zip', '.epub',
        '.png', '.jpg', '.jpeg', '.gif',
        '.wav', '.mp3'
    ]

    files = [
        f for f in os.listdir(input_folder)
        if any(f.lower().endswith(ext) for ext in supported_extensions)
    ]

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_filename = Path(filename).stem + ".md"
        output_path = os.path.join(output_folder, output_filename)

        try:
            result = md.convert(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.text_content)
            print(f"✓ Converted: {filename}")
        except Exception as e:
            print(f"✗ Failed: {filename} - {e}")

# Usage
batch_convert("./input_docs", "./output_markdown")
```

---

### Audio Transcription Pipeline

**Workflow:**
```python
from markitdown import MarkItDown

def transcribe_audio(audio_file):
    md = MarkItDown()
    result = md.convert(audio_file)

    # result.text_content contains transcription
    return result.text_content

# Process audio file
transcript = transcribe_audio("meeting.wav")

# Save transcript
with open("meeting_transcript.md", "w") as f:
    f.write(f"# Meeting Transcript\n\n{transcript}")
```

---

### Image OCR Extraction

**Workflow:**
```python
from markitdown import MarkItDown

def extract_text_from_image(image_file):
    md = MarkItDown()
    result = md.convert(image_file)

    # Includes EXIF metadata and OCR text
    return result.text_content

# Extract text from scanned document
text = extract_text_from_image("scanned_page.png")
print(text)
```

---

## Best Practices

### File Processing

1. **Check File Size** - Large files take longer to process
2. **Validate Format** - Ensure file extension matches content
3. **Handle Errors** - Implement try-catch for conversion failures
4. **Test Output** - Verify Markdown quality for critical documents
5. **Use Streams** - For large files, use `convert_stream()` for memory efficiency

### LLM Integration

1. **Token Limits** - Check Markdown length before sending to LLM
2. **Chunking** - Split long documents for processing
3. **Preserve Structure** - Markdown headers help LLMs understand context
4. **Clean Output** - Remove unnecessary formatting if needed
5. **Metadata** - Include file name and type in LLM context

### Performance Optimization

1. **Batch Processing** - Convert multiple files in parallel
2. **Cache Results** - Store converted Markdown to avoid re-processing
3. **Selective Features** - Only install needed dependencies
4. **Stream Processing** - Use streams for memory efficiency
5. **Azure Services** - Use Azure Document Intelligence for complex PDFs

---

## Supported Format Details

### PDF
- Text extraction
- Table preservation
- Link extraction
- Structure maintenance
- **Enhanced:** Azure Document Intelligence for complex layouts

### Word (DOCX)
- Headings hierarchy
- Lists (ordered/unordered)
- Tables
- Images (with optional descriptions)
- Links

### PowerPoint (PPTX)
- Slide titles
- Content structure
- Tables
- Images (with optional LLM descriptions)
- Notes

### Excel (XLSX/XLS)
- Sheet names
- Tables with headers
- Data preservation
- Multiple sheets

### Images
- EXIF metadata extraction
- OCR text extraction
- Optional LLM descriptions (with OpenAI)
- Supported: PNG, JPG, JPEG, GIF

### Audio
- Transcription to text
- Speaker detection
- Timestamp support
- Formats: WAV, MP3

### HTML
- Content extraction
- Link preservation
- Table conversion
- Header hierarchy

### CSV/JSON/XML
- Structure-aware conversion
- Data table formatting
- Key-value preservation

### YouTube
- Video metadata
- Transcript extraction
- Description and comments

### ZIP/EPub
- Archive extraction
- Recursive processing
- Content aggregation

---

## Troubleshooting

### Installation Issues

**Problem:** Dependency conflicts

**Solution:**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install 'markitdown[all]'
```

### Conversion Failures

**Problem:** "Unsupported file format"

**Solutions:**
- Verify file extension matches content
- Check file isn't corrupted
- Ensure required dependencies installed
- Try opening file in native application first

**Problem:** "Memory error" on large files

**Solutions:**
- Use stream processing: `convert_stream()`
- Process file in chunks
- Increase available memory
- Use Azure Document Intelligence for PDFs

### Output Quality

**Problem:** Poor OCR results

**Solutions:**
- Ensure image is high resolution
- Check image is not rotated
- Use Azure Document Intelligence
- Pre-process image (contrast, brightness)

**Problem:** Missing tables or structure

**Solutions:**
- Use Azure Document Intelligence for PDFs
- Verify source document is well-formatted
- Check PDF isn't scanned image (needs OCR)

---

## When to Use This Skill

- Converting documents for LLM analysis
- Extracting text from PDFs and images
- Processing Office documents programmatically
- Transcribing audio to text
- Building document processing pipelines
- Preparing data for AI/ML workflows
- Creating searchable archives from documents
- Extracting structured data from files

## Keywords

markitdown, file conversion, markdown, pdf to markdown, document processing, ocr, audio transcription, llm preprocessing, document extraction, text extraction, file parsing, microsoft, autogen, python utility, batch conversion
