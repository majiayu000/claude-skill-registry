---
name: docling
description: Python document processing library for parsing PDF, DOCX, and 10+ formats with advanced layout understanding, unified document representation, and AI ecosystem integrations (LangChain, LlamaIndex, MCP server)
repository: https://github.com/DS4SD/docling
documentation: https://docling-project.github.io/docling/
version: 2.66.0
license: MIT
stars: 48400
languages:
  - Python (98.7%)
category: Document Processing
tags:
  - docling
  - document-processing
  - pdf-parsing
  - ocr
  - document-ai
  - langchain
  - llamaindex
  - mcp-server
  - rag
  - python
  - ml-extraction
---

# Docling - Document Processing for Gen AI

## Overview

**Docling** is a powerful Python library developed by IBM Research that simplifies document processing for generative AI applications. With 48,400+ GitHub stars and 159 contributors, Docling excels at parsing diverse document formats—including advanced PDF understanding with layout analysis—and provides seamless integrations with AI frameworks like LangChain, LlamaIndex, and Model Context Protocol (MCP) servers.

## Key Features

### 📄 Multi-Format Document Processing
- **12+ Input Formats**: PDF, DOCX, XLSX, PPTX, HTML, Markdown, AsciiDoc, CSV, Images (PNG, JPEG, TIFF), USPTO XML, JATS XML, WebVTT
- **Advanced PDF Understanding**: Page layout analysis, reading order detection, table structure recognition, code block extraction, mathematical formula parsing, image classification
- **Unified Document Representation**: All formats parsed into consistent Docling Document structure
- **5+ Export Formats**: Markdown, HTML, JSON (lossless), Plain Text, Doctags markup

### 🤖 AI Ecosystem Integration
- **LangChain Official Extension**: `langchain-docling` package with document loaders
- **LlamaIndex Integration**: Docling Reader + Node Parser for RAG applications
- **MCP Server**: Model Context Protocol server for agentic applications
- **Framework Support**: Compatible with Crew AI, Haystack, and other AI frameworks

### 🚀 Production Features
- **Local Execution**: Run entirely offline for sensitive data (no remote service dependencies)
- **OCR Support**: Built-in optical character recognition for scanned documents
- **Vision Language Models**: VLM integration for enhanced understanding
- **Audio/ASR Support**: Transcription capabilities for audio formats
- **Table Extraction**: TableFormer with FAST/ACCURATE modes
- **Code Detection**: Automatic code block identification and preservation

## Architecture

### Document Processing Pipeline
```
Input Document → Format Detection → Backend Selection → Pipeline Execution → Docling Document
                                                                               ↓
                                                         [Export] → Markdown, HTML, JSON, Text
                                                         [Serialize] → Chunking, Embedding
```

### Core Components
1. **Document Converter**: Orchestrates format-specific workflows
2. **Format Backends**: Specialized parsers per format (PDF, DOCX, etc.)
3. **Processing Pipelines**: Layout analysis, table extraction, OCR
4. **Docling Document**: Unified document representation (Pydantic v2)
5. **Serializers**: Export to various formats with customization

### Extensibility
- Base classes available for subclassing (custom backends, pipelines)
- Custom model integration (HuggingFace models)
- Configurable processing options per document type

## Installation

### Basic Installation
```bash
# Standard installation
pip install docling

# Verify installation
python -c "import docling; print(docling.__version__)"
```

### Platform Support
- **Operating Systems**: macOS, Linux, Windows
- **Architectures**: x86_64, arm64
- **Python**: 3.9+ (Pydantic v2 requirement)

### Dependencies
- **Core**: Pydantic v2, PyMuPDF (PDF processing)
- **Optional**: TensorFlow/PyTorch (for ML models), OpenCV (image processing)
- **Auto-Downloaded**: ML models (layout analysis, table extraction) on first use

### Offline/Air-Gapped Installation
```bash
# Prefetch models
docling-tools models download

# Or specify artifacts path
export DOCLING_ARTIFACTS_PATH=/path/to/models

# Download custom HuggingFace models
docling-tools download-hf-repo --repo-id <model_id>
```

## Use Cases

### 1. Basic Document Conversion
```python
from docling.document_converter import DocumentConverter

# Initialize converter
converter = DocumentConverter()

# Convert document
result = converter.convert("document.pdf")

# Export to Markdown
markdown_content = result.document.export_to_markdown()
print(markdown_content)

# Export to HTML
html_content = result.document.export_to_html()

# Export to JSON (lossless)
json_data = result.document.export_to_dict()
```

### 2. Advanced PDF Processing
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode
)

# Configure PDF processing
pipeline_options = PdfPipelineOptions()
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
pipeline_options.do_ocr = True

# Initialize converter with options
converter = DocumentConverter(
    pipeline_options=pipeline_options
)

# Convert with advanced features
result = converter.convert("complex_report.pdf")

# Access structured content
for table in result.document.tables:
    print(f"Table: {table.to_markdown()}")

for figure in result.document.pictures:
    print(f"Figure caption: {figure.caption}")
```

### 3. Batch Processing with Resource Limits
```python
from docling.document_converter import DocumentConverter

# Configure resource constraints
converter = DocumentConverter(
    max_file_size=50_000_000,  # 50 MB limit
    max_num_pages=100           # First 100 pages only
)

# Process multiple documents
documents = ["doc1.pdf", "doc2.docx", "doc3.xlsx"]

for doc_path in documents:
    try:
        result = converter.convert(doc_path)
        output_path = doc_path.replace(".pdf", ".md")
        with open(output_path, "w") as f:
            f.write(result.document.export_to_markdown())
        print(f"✅ Converted: {doc_path}")
    except Exception as e:
        print(f"❌ Failed: {doc_path} - {e}")
```

### 4. LangChain Integration (RAG Pipeline)
```python
from langchain_docling import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load documents with Docling
loader = DoclingLoader(
    file_path="technical_manual.pdf",
    export_type="markdown"  # or "json" for lossless
)
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(splits, embeddings)

# Query the documents
retriever = vectorstore.as_retriever()
relevant_docs = retriever.get_relevant_documents("What is the installation process?")

for doc in relevant_docs:
    print(doc.page_content)
```

### 5. LlamaIndex Integration
```python
from llama_index.readers.docling import DoclingReader
from llama_index.node_parser.docling import DoclingNodeParser
from llama_index.core import VectorStoreIndex

# Load documents with Docling Reader
reader = DoclingReader(export_type="json")  # Lossless serialization
documents = reader.load_data(file_path="research_paper.pdf")

# Parse into nodes
node_parser = DoclingNodeParser()
nodes = node_parser.get_nodes_from_documents(documents)

# Build index
index = VectorStoreIndex(nodes)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the methodology section")
print(response)
```

### 6. Custom Pipeline Configuration
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pdf_backend import PyPdfiumBackend
import os

# Configure threading (for performance)
os.environ["OMP_NUM_THREADS"] = "8"  # Use 8 CPU threads

# Custom pipeline options
pipeline_options = PdfPipelineOptions()
pipeline_options.do_cell_matching = True  # Enable table cell matching
pipeline_options.generate_page_images = True  # Extract page images
pipeline_options.generate_picture_images = True  # Extract figures

# Use specific backend
converter = DocumentConverter(
    allowed_formats=["pdf"],
    format_options={"pdf": PyPdfiumBackend}
)

# Convert with custom settings
result = converter.convert(
    "scientific_paper.pdf",
    pipeline_options=pipeline_options
)

# Save extracted images
for i, image in enumerate(result.document.pictures):
    image.save(f"figure_{i}.png")
```

### 7. Binary Stream Processing
```python
from docling.document_converter import DocumentConverter, DocumentStream
from io import BytesIO

# Load PDF as binary stream
with open("document.pdf", "rb") as f:
    pdf_bytes = BytesIO(f.read())

# Create document stream
doc_stream = DocumentStream(
    name="document.pdf",
    stream=pdf_bytes
)

# Convert from stream
converter = DocumentConverter()
result = converter.convert(doc_stream)

markdown = result.document.export_to_markdown()
```

### 8. Remote Services (Cloud OCR)
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions

# IMPORTANT: Explicit opt-in required for remote services
# Main purpose of Docling is local execution
pipeline_options = PdfPipelineOptions()
pipeline_options.enable_remote_services = True  # Explicit consent

# Configure cloud OCR (if needed)
converter = DocumentConverter(pipeline_options=pipeline_options)

# Process document (may use cloud services)
result = converter.convert("scanned_document.pdf")
```

## Advanced Features

### Table Extraction Modes
```python
from docling.datamodel.pipeline_options import TableFormerMode

# FAST mode (faster processing)
pipeline_options.table_structure_options.mode = TableFormerMode.FAST

# ACCURATE mode (better quality)
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
```

**Trade-offs**:
- **FAST**: ~2x faster, good for simple tables
- **ACCURATE**: Higher precision, better for complex tables with merged cells

### Output Format Customization

**Markdown Export**:
```python
# With embedded images
markdown = result.document.export_to_markdown(image_mode="embedded")

# With image references
markdown = result.document.export_to_markdown(image_mode="referenced")
```

**HTML Export**:
```python
# With custom CSS
html = result.document.export_to_html(
    include_styles=True,
    custom_css="body { font-family: Arial; }"
)
```

**JSON Export (Lossless)**:
```python
# Complete document structure
json_data = result.document.export_to_dict()

# Includes:
# - Full layout information
# - Reading order
# - Bounding boxes
# - Confidence scores
# - Metadata
```

### Document Chunking Strategies
```python
from docling.chunking import HybridChunker

# Configure chunker
chunker = HybridChunker(
    chunk_size=1000,        # Target chunk size
    chunk_overlap=200,      # Overlap between chunks
    respect_boundaries=True # Respect document structure
)

# Chunk document
chunks = chunker.chunk(result.document)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i}:")
    print(chunk.text)
    print(f"Metadata: {chunk.metadata}")
```

### Confidence Scores
```python
# Access confidence scores for extracted content
for element in result.document.elements:
    if hasattr(element, 'confidence'):
        print(f"Element: {element.text[:50]}")
        print(f"Confidence: {element.confidence}")
```

## MCP Server Integration

Docling provides a Model Context Protocol (MCP) server for integration with agentic applications like Claude Desktop.

### MCP Server Setup
```bash
# Install MCP server
pip install docling-mcp-server

# Start server
docling-mcp-server --port 3000
```

### MCP Configuration (Claude Desktop)
```json
{
  "mcpServers": {
    "docling": {
      "command": "docling-mcp-server",
      "args": ["--port", "3000"],
      "env": {
        "DOCLING_ARTIFACTS_PATH": "/path/to/models"
      }
    }
  }
}
```

### MCP Use Cases
- **Document Parsing Tool**: Convert documents to structured format for AI agents
- **RAG Pipeline Integration**: Extract and chunk documents for retrieval
- **Multi-Format Support**: Handle various document types in agentic workflows

## Performance Optimization

### CPU Thread Control
```bash
# Set number of threads (default: 4)
export OMP_NUM_THREADS=8

# Or in Python
import os
os.environ["OMP_NUM_THREADS"] = "8"
```

### Memory Management
```python
# Process documents in batches to manage memory
def process_batch(file_paths, batch_size=10):
    converter = DocumentConverter()

    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i+batch_size]

        for file_path in batch:
            result = converter.convert(file_path)
            # Process result

        # Clear memory between batches
        import gc
        gc.collect()
```

### Prefetching Models
```bash
# Download all models in advance
docling-tools models download

# Verify models
ls $HOME/.cache/docling/models
```

## Supported Formats

### Input Formats (12+)

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Advanced layout understanding, table extraction |
| Microsoft Word | `.docx` | Office 2007+ (Open XML) |
| Excel | `.xlsx` | Spreadsheet data extraction |
| PowerPoint | `.pptx` | Slide content and structure |
| HTML | `.html`, `.xhtml` | Web page content |
| Markdown | `.md` | Plain text markup |
| AsciiDoc | `.adoc`, `.asciidoc` | Technical documentation |
| CSV | `.csv` | Tabular data |
| Images | `.png`, `.jpg`, `.tiff`, `.bmp`, `.webp` | OCR processing |
| USPTO XML | `.xml` | Patent documents |
| JATS XML | `.xml` | Journal articles |
| WebVTT | `.vtt` | Video subtitle files |

### Output Formats

| Format | Use Case | Lossless |
|--------|----------|----------|
| Markdown | Human-readable, AI-friendly | No |
| HTML | Web rendering | No |
| JSON | Complete structure preservation | Yes |
| Plain Text | Simple text extraction | No |
| Doctags | Layout-aware markup | Partial |

## Common Workflows

### 1. PDF to Markdown for RAG
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("whitepaper.pdf")

# Export to Markdown
markdown = result.document.export_to_markdown()

# Save for RAG ingestion
with open("whitepaper.md", "w") as f:
    f.write(markdown)
```

### 2. Extract Tables from Excel
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("financial_report.xlsx")

# Extract all tables
for table in result.document.tables:
    print(table.to_markdown())
    # Or: table.to_dataframe() for pandas integration
```

### 3. Multi-Format Document Collection
```python
from docling.document_converter import DocumentConverter
from pathlib import Path

converter = DocumentConverter()

# Process directory
input_dir = Path("documents/")
output_dir = Path("processed/")

for file_path in input_dir.glob("*"):
    if file_path.suffix in [".pdf", ".docx", ".xlsx", ".pptx"]:
        result = converter.convert(str(file_path))

        output_file = output_dir / f"{file_path.stem}.md"
        with open(output_file, "w") as f:
            f.write(result.document.export_to_markdown())
```

## Troubleshooting

### Model Download Issues
```bash
# Manually download models
docling-tools models download

# Check model cache
ls ~/.cache/docling/models

# Set custom cache location
export DOCLING_ARTIFACTS_PATH=/custom/path
```

### Memory Errors with Large PDFs
```python
# Limit pages processed
converter = DocumentConverter(max_num_pages=50)

# Or limit file size
converter = DocumentConverter(max_file_size=20_000_000)  # 20 MB
```

### OCR Not Working
```python
# Ensure OCR is enabled
from docling.datamodel.pipeline_options import PdfPipelineOptions

pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True

converter = DocumentConverter(pipeline_options=pipeline_options)
```

### Table Extraction Failures
```python
# Try ACCURATE mode
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

# Enable cell matching
pipeline_options.do_cell_matching = True
```

## Security & Privacy

### Local Execution (Default)
- **No Remote Calls**: All processing happens locally by default
- **Sensitive Data Safe**: No data transmitted to external services
- **Offline Capable**: Works in air-gapped environments

### Remote Services (Opt-In)
```python
# MUST explicitly enable
pipeline_options.enable_remote_services = True
```

**Only use remote services when:**
- Processing non-sensitive documents
- Need cloud OCR for scanned documents
- Using vision model APIs

## Community & Resources

### Official Links
- **Documentation**: https://docling-project.github.io/docling/
- **GitHub**: https://github.com/DS4SD/docling (48.4k ⭐)
- **Technical Report**: https://arxiv.org/abs/2408.09869
- **PyPI**: https://pypi.org/project/docling/

### Key Statistics
- **Stars**: 48,400
- **Forks**: 3,400
- **Contributors**: 159
- **Latest Release**: v2.66.0 (December 2025)
- **License**: MIT

### Integration Packages
- **LangChain**: `langchain-docling`
- **LlamaIndex**: `llama-index-readers-docling`, `llama-index-node-parser-docling`
- **MCP Server**: `docling-mcp-server`

### Learning Resources
- LangChain Integration Guide: https://python.langchain.com/docs/integrations/document_loaders/docling/
- LlamaIndex Documentation: Official integration docs
- Example Notebooks: GitHub repository examples/

## When to Use This Skill

Use the Docling skill when:
- ✅ Processing PDFs with complex layouts (tables, figures, multi-column)
- ✅ Building RAG applications that need structured document understanding
- ✅ Extracting data from multiple document formats (PDF, DOCX, XLSX, etc.)
- ✅ Need local/offline document processing (sensitive data, air-gapped)
- ✅ Integrating with LangChain, LlamaIndex, or AI frameworks
- ✅ Converting documents to Markdown for LLM consumption
- ✅ Extracting tables, figures, and code blocks programmatically
- ✅ Building document processing pipelines for AI applications
- ✅ Need MCP server for agentic document workflows
- ✅ OCR for scanned documents or images

## Related Technologies

- **PyMuPDF**: PDF processing library (used by Docling)
- **Pydantic v2**: Data validation (Docling Document structure)
- **LangChain**: AI application framework (official integration)
- **LlamaIndex**: Data framework for LLM applications (official integration)
- **Model Context Protocol (MCP)**: Tool integration standard (Docling MCP server)
- **TableFormer**: Table extraction model (integrated)
- **Tesseract OCR**: Open-source OCR engine (alternative)

---

**Skill Type**: Document Processing Library
**Complexity Level**: Intermediate to Advanced
**Maintenance Status**: ✅ Active (v2.66.0, December 2025)
**Community Health**: ✅ Excellent (48.4k stars, 159 contributors)
