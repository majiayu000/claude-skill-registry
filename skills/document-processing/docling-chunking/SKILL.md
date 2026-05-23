---
name: Docling Chunking
description: This skill should be used when the user asks about "Docling chunking", "HybridChunker", "HierarchicalChunker", "structure-aware chunking", "Docling metadata extraction", "export modes", "DOC_CHUNKS vs MARKDOWN", "chunking strategies", or mentions preparing documents for RAG with Docling.
version: 0.1.0
---

# Docling Chunking

## Overview

Docling provides structure-aware chunking that preserves document hierarchy while creating semantically meaningful chunks for RAG applications. Unlike arbitrary text splitting, Docling's chunkers respect document structure (sections, paragraphs, tables, figures) and attach rich metadata to every chunk.

**Key concepts:**
- **HybridChunker**: Combines hierarchical structure with token-aware sizing
- **HierarchicalChunker**: Pure structure-based chunking following document hierarchy
- **Export modes**: DOC_CHUNKS (one chunk per item) vs MARKDOWN (full document)
- **Rich metadata**: Page numbers, section titles, document items, provenance

## Chunking Strategies

### HybridChunker (Recommended for RAG)

Combines document structure awareness with tokenization constraints for optimal embedding model compatibility.

**How it works:**
1. Identifies document structure (sections, paragraphs, tables)
2. Groups related elements hierarchically
3. Adjusts chunk sizes to respect embedding model token limits
4. Preserves semantic boundaries

**Use when:**
- Building RAG applications with vector search
- Using embedding models with token limits
- Need balance between structure and chunk size
- Processing for LLM consumption

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
result = converter.convert("document.pdf")

chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

for chunk in chunks:
    print(f"Chunk: {chunk.text[:100]}...")
    print(f"Metadata: {chunk.meta}")
```

**Typical output:** 200-800 token chunks respecting document structure.

### HierarchicalChunker (Best for Structure Preservation)

Pure structure-based chunking that follows document hierarchy without token constraints.

**How it works:**
1. Parses document hierarchy (sections → subsections → paragraphs)
2. Creates chunks that align with structural boundaries
3. Maintains parent-child relationships in metadata
4. Preserves tables and figures as complete units

**Use when:**
- Document structure is critical (legal docs, research papers)
- Need exact section-level granularity
- Citation tracking requires structural context
- Building hierarchical knowledge representations

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HierarchicalChunker

converter = DocumentConverter()
result = converter.convert("document.pdf")

chunker = HierarchicalChunker()
chunks = list(chunker.chunk(result.document))

for chunk in chunks:
    print(f"Section: {chunk.meta.doc_items[0].label if chunk.meta.doc_items else 'N/A'}")
    print(f"Text: {chunk.text[:100]}...")
```

**Typical output:** Variable-sized chunks aligned to document sections.

### When to Use Which

| Requirement | Chunker | Reason |
|-------------|---------|--------|
| RAG with embeddings | HybridChunker | Token-aware, optimal for embedding models |
| Preserve exact structure | HierarchicalChunker | Respects document hierarchy |
| Citation-heavy workflows | HierarchicalChunker | Section-level granularity |
| Vector search | HybridChunker | Consistent chunk sizes for retrieval |
| Profile synthesis | HybridChunker | Balanced semantic units |
| Legal/compliance docs | HierarchicalChunker | Preserve structural integrity |

For detailed comparison and use cases, see **`references/chunking-strategies.md`**.

## Export Modes

Docling supports two primary export modes for different workflows.

### DOC_CHUNKS Mode (Default for RAG)

Exports each chunk as a separate item, ideal for RAG applications.

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions, TableFormatOption
from docling.chunking import HybridChunker

# Configure for chunked export
converter = DocumentConverter()
result = converter.convert("document.pdf")

chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

# Each chunk is a separate object
import json
output = []
for chunk in chunks:
    output.append({
        "text": chunk.text,
        "metadata": {
            "page": chunk.meta.doc_items[0].prov[0].page_no if chunk.meta.doc_items and chunk.meta.doc_items[0].prov else None,
            "type": chunk.meta.doc_items[0].label if chunk.meta.doc_items else None
        }
    })

# Save as JSONL (one chunk per line)
with open("chunks.jsonl", "w") as f:
    for item in output:
        f.write(json.dumps(item) + "\n")
```

**Output format:** JSONL with one chunk per line, ready for downstream processing.

### MARKDOWN Mode (For Human Review)

Exports full document as single Markdown file, ideal for documentation and review.

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")

# Export full document as markdown
markdown_content = result.document.export_to_markdown()

# Save
with open("document.md", "w") as f:
    f.write(markdown_content)
```

**Output format:** Single Markdown file preserving document structure.

### Choosing Export Mode

| Use Case | Mode | Format |
|----------|------|--------|
| RAG pipeline | DOC_CHUNKS | JSONL (one chunk/line) |
| Vector database ingestion | DOC_CHUNKS | JSONL or JSON |
| Human review | MARKDOWN | Single .md file |
| Documentation | MARKDOWN | Single .md file |
| BAML processing | DOC_CHUNKS | JSONL |
| LLM prompts | MARKDOWN | String |

## Metadata Structure

Every Docling chunk includes rich metadata for source attribution and filtering.

### Available Metadata Fields

```python
chunk.meta contains:
  - doc_items: List of document items (paragraphs, tables, etc.)
    - label: Item type ("paragraph", "table", "section_header", etc.)
    - text: Item content
    - prov: Provenance information
      - page_no: Page number in source document
      - bbox: Bounding box coordinates
  - headings: Section hierarchy context
  - origin: Source document information
```

### Accessing Metadata

```python
for chunk in chunks:
    # Get page number
    if chunk.meta.doc_items and chunk.meta.doc_items[0].prov:
        page = chunk.meta.doc_items[0].prov[0].page_no
        print(f"Page: {page}")

    # Get item type
    if chunk.meta.doc_items:
        item_type = chunk.meta.doc_items[0].label
        print(f"Type: {item_type}")

    # Get section context
    if hasattr(chunk.meta, 'headings') and chunk.meta.headings:
        section = chunk.meta.headings[0]
        print(f"Section: {section}")
```

For complete metadata schema, see **`references/metadata-schema.md`**.

## Source Attribution Patterns

Maintaining source attribution is critical for RAG applications and expert verification.

### Pattern 1: Inline Citations

Embed source information directly in chunk:

```python
def chunk_with_citations(pdf_path: str):
    """Create chunks with inline citations."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    chunker = HybridChunker()
    chunks = list(chunker.chunk(result.document))

    cited_chunks = []
    for chunk in chunks:
        page = chunk.meta.doc_items[0].prov[0].page_no if chunk.meta.doc_items and chunk.meta.doc_items[0].prov else None

        cited_text = f"{chunk.text}\n\n[Source: {pdf_path}, Page {page}]"

        cited_chunks.append({
            "text": cited_text,
            "source": pdf_path,
            "page": page
        })

    return cited_chunks
```

### Pattern 2: Structured Metadata

Keep citations as separate metadata:

```python
def chunk_with_metadata(pdf_path: str):
    """Create chunks with structured metadata."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    chunker = HybridChunker()
    chunks = list(chunker.chunk(result.document))

    structured_chunks = []
    for chunk in chunks:
        item = chunk.meta.doc_items[0] if chunk.meta.doc_items else None

        structured_chunks.append({
            "content": chunk.text,
            "metadata": {
                "source_file": pdf_path,
                "page_number": item.prov[0].page_no if item and item.prov else None,
                "item_type": item.label if item else None,
                "section_context": chunk.meta.headings[0] if hasattr(chunk.meta, 'headings') and chunk.meta.headings else None
            }
        })

    return structured_chunks
```

### Pattern 3: Citation Registry

Maintain separate citation index:

```python
def chunk_with_registry(pdf_path: str):
    """Create chunks with citation registry."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    chunker = HybridChunker()
    chunks = list(chunker.chunk(result.document))

    registry = {
        "chunks": [],
        "citations": []
    }

    for i, chunk in enumerate(chunks):
        item = chunk.meta.doc_items[0] if chunk.meta.doc_items else None

        # Add chunk with citation ID
        registry["chunks"].append({
            "id": f"chunk_{i}",
            "text": chunk.text,
            "citation_id": f"cite_{i}"
        })

        # Add citation to registry
        registry["citations"].append({
            "id": f"cite_{i}",
            "source": pdf_path,
            "page": item.prov[0].page_no if item and item.prov else None,
            "type": item.label if item else None
        })

    return registry
```

For more patterns, see **`examples/citation_tracking.py`**.

## Output Format: JSONL

JSONL (JSON Lines) is the recommended format for Docling chunks in RAG workflows.

### Why JSONL

- **Streamable**: Process one chunk at a time (low memory)
- **Appendable**: Add chunks incrementally
- **Tool-friendly**: Works with `grep`, `head`, `tail`
- **BAML-compatible**: Direct input for `/baml-toolkit:batch-gemini`
- **Fault-tolerant**: One corrupt line doesn't break entire file

### JSONL Output Example

```python
import json
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
result = converter.convert("document.pdf")

chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

# Write JSONL
with open("chunks.jsonl", "w") as f:
    for chunk in chunks:
        item = chunk.meta.doc_items[0] if chunk.meta.doc_items else None

        record = {
            "text": chunk.text,
            "source": "document.pdf",
            "page": item.prov[0].page_no if item and item.prov else None,
            "type": item.label if item else None
        }

        f.write(json.dumps(record) + "\n")
```

### Reading JSONL

```python
import json

chunks = []
with open("chunks.jsonl") as f:
    for line in f:
        chunks.append(json.loads(line))

# Process one at a time (memory-efficient)
with open("chunks.jsonl") as f:
    for line in f:
        chunk = json.loads(line)
        # Process chunk
```

## Integration with BAML Toolkit

Docling chunks work seamlessly with BAML batch processing.

### Workflow

```bash
# 1. Extract with Docling (this plugin)
python process_documents.py --output extracts.jsonl

# 2. Process with BAML (baml-toolkit plugin)
/baml-toolkit:batch-gemini GenerateProfile \
  extracts.jsonl \
  --output profiles.json
```

### Data Format

Docling JSONL output is directly compatible with BAML:

```jsonl
{"text": "Company XYZ focuses on circular economy...", "source": "company.pdf", "page": 1}
{"text": "Their impact metrics include...", "source": "company.pdf", "page": 2}
```

BAML can read these and synthesize structured profiles while preserving citations.

## Common Patterns

### Pattern: Process Multiple Documents

```python
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
import json

converter = DocumentConverter()
chunker = HybridChunker()

with open("all_chunks.jsonl", "w") as output:
    for pdf in Path("data/").glob("*.pdf"):
        result = converter.convert(str(pdf))
        chunks = list(chunker.chunk(result.document))

        for chunk in chunks:
            item = chunk.meta.doc_items[0] if chunk.meta.doc_items else None

            record = {
                "text": chunk.text,
                "source": pdf.name,
                "page": item.prov[0].page_no if item and item.prov else None
            }

            output.write(json.dumps(record) + "\n")
```

### Pattern: Filter by Type

```python
# Extract only tables
tables = [
    chunk for chunk in chunks
    if chunk.meta.doc_items
    and chunk.meta.doc_items[0].label == "table"
]

# Extract only paragraphs
paragraphs = [
    chunk for chunk in chunks
    if chunk.meta.doc_items
    and chunk.meta.doc_items[0].label == "paragraph"
]
```

### Pattern: Group by Section

```python
from collections import defaultdict

sections = defaultdict(list)

for chunk in chunks:
    section_title = chunk.meta.headings[0] if hasattr(chunk.meta, 'headings') and chunk.meta.headings else "Unknown"
    sections[section_title].append(chunk.text)

# Access chunks by section
intro_chunks = sections["Introduction"]
```

## Quick Reference

### Chunk and Export to JSONL

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
import json

# Convert and chunk
converter = DocumentConverter()
result = converter.convert("doc.pdf")
chunks = list(HybridChunker().chunk(result.document))

# Export to JSONL
with open("chunks.jsonl", "w") as f:
    for chunk in chunks:
        item = chunk.meta.doc_items[0] if chunk.meta.doc_items else None
        f.write(json.dumps({
            "text": chunk.text,
            "page": item.prov[0].page_no if item and item.prov else None
        }) + "\n")
```

### Choose Chunker

```python
# For RAG/embeddings
from docling.chunking import HybridChunker
chunker = HybridChunker()

# For structure preservation
from docling.chunking import HierarchicalChunker
chunker = HierarchicalChunker()
```

## Additional Resources

### Reference Files

For detailed guidance:
- **`references/chunking-strategies.md`** - Deep dive on chunking strategies and trade-offs
- **`references/metadata-schema.md`** - Complete metadata structure and fields

### Example Files

Working examples in `examples/`:
- **`hybrid_chunking.py`** - HybridChunker with JSONL output
- **`hierarchical_chunking.py`** - HierarchicalChunker with structure analysis
- **`citation_tracking.py`** - Complete citation tracking patterns

---

This skill covers Docling's chunking capabilities. For installation and basic usage, see **docling-fundamentals** skill. For advanced features like Granite model, see **docling-advanced** skill.
