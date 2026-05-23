---
name: docling
description: Turn ANY File (PDF, DOCX, Audio) into LLM-Knowledge in SECONDS using Docling.
trigger: docling OR pdf parse OR rag pipeline OR document conversion OR chunking
scope: global
---

# Docling - Universal Document Converter

> [!IMPORTANT]
> Docling is the specialized tool for the "Data Curation" step of RAG (Retrieval Augmented Generation). It turns complex, messy file formats into clean, structured Markdown that LLMs love.

## 1. Core Capabilities

- **Universal Parsing**: Handles PDF, DOCX, PPTX, Images, HTML, AsciiDoc, Markdown, and Audio (via Whisper).
- **Layout Awareness**: Understands tables, headers, footers, page numbers, and reading order in PDFs (OCR included).
- **Hybrid Chunking**: Smart chunking strategy that uses embedding models to keep semantically related text together, rather than just splitting by character count.
- **Export to Markdown**: The gold standard format for LLM context.

## 2. Quick Start

### Installation

```bash
pip install docling
# Optional: Audio support
pip install ffmpeg-python openai-whisper
```

### Basic Extraction (PDF to Markdown)

```python
from docling.document_converter import DocumentConverter

source = "path/to/document.pdf"  # Can be URL or local path
converter = DocumentConverter()
result = converter.convert(source)

# Export to Markdown
markdown_output = result.document.export_to_markdown()
print(markdown_output)
```

## 3. Advanced Usage: Hybrid Chunking

This is the killer feature for RAG. Don't just split by characters; split by _meaning_.

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

doc_converter = DocumentConverter()
conv_res = doc_converter.convert("complex_report.pdf")
doc = conv_res.document

# Initialize Hybrid Chunker
chunker = HybridChunker(
    tokenizer="intfloat/multilingual-e5-base" # Or other embedding model tokenizer
)

# Generate Chunks
chunk_iter = chunker.chunk(doc)
chunks = list(chunk_iter)

for chunk in chunks:
    print(f"Chunk Text:\n{chunk.text}\n---\n")
    # Store 'chunk.vector' in your DB if using embedded creation here
```

## 4. Working with Audio (Transcription)

Docling streamlines the audio-to-text pipeline for RAG.

```python
# Requires: pip install openai-whisper
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("meeting_recording.mp3")

# Output includes timestamps and speaker separation if supported
print(result.document.export_to_markdown())
```

## 5. RAG Integration Pattern

1. **Ingest**: Use `DocumentConverter` to read files from your source directory.
2. **Process**: Convert every file (PDF, Word, Audio) into a uniform `DoclingDocument`.
3. **Chunk**: Apply `HybridChunker` to split documents intelligently.
4. **Embed & Store**: Send chunks to your Vector DB (PGVector, Pinecone, etc.).
5. **Retrieve**: Query your DB for relevant chunks and feed them to the LLM.

## Resources

- [Docling GitHub & Docs](https://github.com/DS4SD/docling)
- Recommended for robust Parsing vs. "Crawl4AI" for Web Parsing.
