---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: data-extractor
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: parsing
tags:
  - extraction
  - data
  - unstructured
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
    - extract_tables_from_pdf

# Skill Capabilities
capabilities:
  - data_extraction
  - format_handling

# Language Support
languages:
  - en
  - zh
---

# Data Extractor Skill

## Overview

This skill enables extraction of structured data from any document format using **unstructured** - a unified library for processing PDFs, Word docs, emails, HTML, and more. Get consistent, structured output regardless of input format.

## How to Use

1. Provide the document to process
2. Optionally specify extraction options
3. I'll extract structured elements with metadata

**Example prompts:**
- "Extract all text and tables from this PDF"
- "Parse this email and get the body, attachments, and metadata"
- "Convert this HTML page to structured elements"
- "Extract data from these mixed-format documents"

## Domain Knowledge

### unstructured Fundamentals

```python
from unstructured.partition.auto import partition

# Automatically detect and process any document
elements = partition("document.pdf")

# Access extracted elements
for element in elements:
    print(f"Type: {type(element).__name__}")
    print(f"Text: {element.text}")
    print(f"Metadata: {element.metadata}")
```

### Supported Formats

| Format | Function | Notes |
|--------|----------|-------|
| PDF | `partition_pdf` | Native + scanned |
| Word | `partition_docx` | Full structure |
| PowerPoint | `partition_pptx` | Slides & notes |
| Excel | `partition_xlsx` | Sheets & tables |
| Email | `partition_email` | Body & attachments |
| HTML | `partition_html` | Tags preserved |
| Markdown | `partition_md` | Structure preserved |
| Plain Text | `partition_text` | Basic parsing |
| Images | `partition_image` | OCR extraction |

### Element Types

```python
from unstructured.documents.elements import (
    Title,
    NarrativeText,
    Text,
    ListItem,
    Table,
    Image,
    Header,
    Footer,
    PageBreak,
    Address,
    EmailAddress,
)

# Elements have consistent structure
element.text           # Raw text content
element.metadata       # Rich metadata
element.category       # Element type
element.id            # Unique identifier
```

### Auto Partition

```python
from unstructured.partition.auto import partition

# Process any file type
elements = partition(
    filename="document.pdf",
    strategy="auto",          # or "fast", "hi_res", "ocr_only"
    include_metadata=True,
    include_page_breaks=True,
)

# Filter by type
titles = [e for e in elements if isinstance(e, Title)]
tables = [e for e in elements if isinstance(e, Table)]
```

### Format-Specific Partitioning

```python
# PDF with options
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="document.pdf",
    strategy="hi_res",              # High quality extraction
    infer_table_structure=True,     # Detect tables
    include_page_breaks=True,
    languages=["en"],               # OCR language
)

# Word documents
from unstructured.partition.docx import partition_docx

elements = partition_docx(
    filename="document.docx",
    include_metadata=True,
)

# HTML
from unstructured.partition.html import partition_html

elements = partition_html(
    filename="page.html",
    include_metadata=True,
)
```

### Working with Tables

```python
from unstructured.partition.auto import partition

elements = partition("report.pdf", infer_table_structure=True)

# Extract tables
for element in elements:
    if element.category == "Table":
        print("Table found:")
        print(element.text)
        
        # Access structured table data
        if hasattr(element, 'metadata') and element.metadata.text_as_html:
            print("HTML:", element.metadata.text_as_html)
```

### Metadata Access

```python
from unstructured.partition.auto import partition

elements = partition("document.pdf")

for element in elements:
    meta = element.metadata
    
    # Common metadata fields
    print(f"Page: {meta.page_number}")
    print(f"Filename: {meta.filename}")
    print(f"Filetype: {meta.filetype}")
    print(f"Coordinates: {meta.coordinates}")
    print(f"Languages: {meta.languages}")
```

### Chunking for AI/RAG

```python
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from unstructured.chunking.basic import chunk_elements

# Partition document
elements = partition("document.pdf")

# Chunk by title (semantic chunks)
chunks = chunk_by_title(
    elements,
    max_characters=1000,
    combine_text_under_n_chars=200,
)

# Or basic chunking
chunks = chunk_elements(
    elements,
    max_characters=500,
    overlap=50,
)

for chunk in chunks:
    print(f"Chunk ({len(chunk.text)} chars):")
    print(chunk.text[:100] + "...")
```

### Batch Processing

```python
from unstructured.partition.auto import partition
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def process_document(file_path):
    """Process single document."""
    try:
        elements = partition(str(file_path))
        return {
            'file': str(file_path),
            'status': 'success',
            'elements': len(elements),
            'text': '\n\n'.join([e.text for e in elements])
        }
    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'error': str(e)
        }

def batch_process(input_dir, max_workers=4):
    """Process all documents in directory."""
    input_path = Path(input_dir)
    files = list(input_path.glob('*'))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_document, files))
    
    return results
```

### Export Formats

```python
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json, elements_to_dicts

elements = partition("document.pdf")

# To JSON string
json_str = elements_to_json(elements)

# To list of dicts
dicts = elements_to_dicts(elements)

# To DataFrame
import pandas as pd
df = pd.DataFrame(dicts)
```

## Best Practices

1. **Choose Strategy Wisely**: "fast" for speed, "hi_res" for accuracy
2. **Enable Table Detection**: For documents with tables
3. **Specify Language**: For better OCR on non-English docs
4. **Chunk for RAG**: Use semantic chunking for AI applications
5. **Handle Errors**: Some formats may fail gracefully

## Common Patterns

### Document to JSON
```python
def document_to_json(file_path, output_path=None):
    """Convert document to structured JSON."""
    from unstructured.partition.auto import partition
    from unstructured.staging.base import elements_to_json
    import json
    
    elements = partition(file_path)
    
    # Create structured output
    output = {
        'source': file_path,
        'elements': []
    }
    
    for element in elements:
        output['elements'].append({
            'type': type(element).__name__,
            'text': element.text,
            'metadata': {
                'page': element.metadata.page_number,
                'coordinates': element.metadata.coordinates.to_dict() if element.metadata.coordinates else None
            }
        })
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
    
    return output
```

### Email Parser
```python
from unstructured.partition.email import partition_email

def parse_email(email_path):
    """Extract structured data from email."""
    
    elements = partition_email(email_path)
    
    email_data = {
        'subject': None,
        'from': None,
        'to': [],
        'date': None,
        'body': [],
        'attachments': []
    }
    
    for element in elements:
        meta = element.metadata
        
        # Extract headers from metadata
        if meta.subject:
            email_data['subject'] = meta.subject
        if meta.sent_from:
            email_data['from'] = meta.sent_from
        if meta.sent_to:
            email_data['to'] = meta.sent_to
        
        # Body content
        email_data['body'].append({
            'type': type(element).__name__,
            'text': element.text
        })
    
    return email_data
```

## Examples

### Example 1: Research Paper Extraction
```python
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

def extract_paper(pdf_path):
    """Extract structured data from research paper."""
    
    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        infer_table_structure=True,
        include_page_breaks=True
    )
    
    paper = {
        'title': None,
        'abstract': None,
        'sections': [],
        'tables': [],
        'references': []
    }
    
    # Find title (usually first Title element)
    for element in elements:
        if element.category == "Title" and not paper['title']:
            paper['title'] = element.text
            break
    
    # Extract tables
    for element in elements:
        if element.category == "Table":
            paper['tables'].append({
                'page': element.metadata.page_number,
                'content': element.text,
                'html': element.metadata.text_as_html if hasattr(element.metadata, 'text_as_html') else None
            })
    
    # Chunk into sections
    chunks = chunk_by_title(elements, max_characters=2000)
    
    current_section = None
    for chunk in chunks:
        if chunk.category == "Title":
            paper['sections'].append({
                'title': chunk.text,
                'content': ''
            })
        elif paper['sections']:
            paper['sections'][-1]['content'] += chunk.text + '\n'
    
    return paper

paper = extract_paper('research_paper.pdf')
print(f"Title: {paper['title']}")
print(f"Tables: {len(paper['tables'])}")
print(f"Sections: {len(paper['sections'])}")
```

### Example 2: Invoice Data Extraction
```python
from unstructured.partition.auto import partition
import re

def extract_invoice_data(file_path):
    """Extract key data from invoice."""
    
    elements = partition(file_path, strategy="hi_res")
    
    # Combine all text
    full_text = '\n'.join([e.text for e in elements])
    
    invoice = {
        'invoice_number': None,
        'date': None,
        'total': None,
        'vendor': None,
        'line_items': [],
        'tables': []
    }
    
    # Extract patterns
    inv_match = re.search(r'Invoice\s*#?\s*:?\s*(\w+[-\w]*)', full_text, re.I)
    if inv_match:
        invoice['invoice_number'] = inv_match.group(1)
    
    date_match = re.search(r'Date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', full_text, re.I)
    if date_match:
        invoice['date'] = date_match.group(1)
    
    total_match = re.search(r'Total\s*:?\s*\$?([\d,]+\.?\d*)', full_text, re.I)
    if total_match:
        invoice['total'] = float(total_match.group(1).replace(',', ''))
    
    # Extract tables
    for element in elements:
        if element.category == "Table":
            invoice['tables'].append(element.text)
    
    return invoice

invoice = extract_invoice_data('invoice.pdf')
print(f"Invoice #: {invoice['invoice_number']}")
print(f"Total: ${invoice['total']}")
```

### Example 3: Document Corpus Builder
```python
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from pathlib import Path
import json

def build_corpus(input_dir, output_path):
    """Build searchable corpus from document collection."""
    
    input_path = Path(input_dir)
    corpus = []
    
    # Support multiple formats
    patterns = ['*.pdf', '*.docx', '*.html', '*.txt', '*.md']
    files = []
    for pattern in patterns:
        files.extend(input_path.glob(pattern))
    
    for file in files:
        print(f"Processing: {file.name}")
        
        try:
            elements = partition(str(file))
            chunks = chunk_by_title(elements, max_characters=1000)
            
            for i, chunk in enumerate(chunks):
                corpus.append({
                    'id': f"{file.stem}_{i}",
                    'source': str(file),
                    'type': type(chunk).__name__,
                    'text': chunk.text,
                    'page': chunk.metadata.page_number if chunk.metadata.page_number else None
                })
        
        except Exception as e:
            print(f"  Error: {e}")
    
    # Save corpus
    with open(output_path, 'w') as f:
        json.dump(corpus, f, indent=2)
    
    print(f"Corpus built: {len(corpus)} chunks from {len(files)} files")
    return corpus

corpus = build_corpus('./documents', 'corpus.json')
```

## Limitations

- Complex layouts may need manual review
- OCR quality depends on image quality
- Large files may need chunking
- Some proprietary formats not supported
- API rate limits for cloud processing

## Installation

```bash
# Basic installation
pip install unstructured

# With all dependencies
pip install "unstructured[all-docs]"

# For PDF processing
pip install "unstructured[pdf]"

# For specific formats
pip install "unstructured[docx,pptx,xlsx]"
```

## Resources

- [unstructured GitHub](https://github.com/Unstructured-IO/unstructured)
- [Documentation](https://unstructured-io.github.io/unstructured/)
- [Unstructured API](https://unstructured.io/api-key)
