---
name: pdf-text-extractor
description: Extract text from PDF files with intelligent chunking and metadata preservation. IMPORTANT - For best results, first convert PDFs to markdown using OpenAI Codex (see pdf skill), then process the markdown. Also supports direct PDF text extraction for batch processing, technical documents, standards libraries, research papers, or any PDF collection.
version: 1.2.0
last_updated: 2026-01-04
category: document-handling
related_skills:
  - pdf
  - knowledge-base-builder
  - semantic-search-setup
  - document-inventory
---

# PDF Text Extractor Skill

## Overview

This skill extracts text from PDF files using PyMuPDF (fitz), with intelligent chunking, page tracking, and metadata preservation. Handles large PDF collections with batch processing and error recovery.

**RECOMMENDED WORKFLOW:** For all PDF documents, first convert to markdown using OpenAI Codex (see `pdf` skill), then process the structured markdown. This skill is best used for:
- Batch processing where Codex conversion is impractical
- Legacy workflows requiring direct PDF extraction
- Cases where raw text is sufficient

## Quick Start

**Recommended Approach (with Codex conversion):**
```python
# 1. Convert PDF to markdown first (see pdf skill)
from pdf_skill import pdf_to_markdown_codex

md_path = pdf_to_markdown_codex("document.pdf")

# 2. Process the markdown
with open(md_path) as f:
    markdown = f.read()
    # Work with structured markdown
```

**Direct Extraction (when Codex not needed):**
```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")
for page in doc:
    text = page.get_text()
    print(text)
doc.close()
```

## When to Use

- Processing PDF document collections for search indexing
- Extracting text from technical standards and specifications
- Converting PDF libraries to searchable text databases
- Preparing documents for AI/ML processing
- Building knowledge bases from PDF archives

## Features

- **Page-aware extraction** - Track which page text comes from
- **Intelligent chunking** - Split long pages into manageable chunks
- **Metadata extraction** - Title, author, creation date
- **Batch processing** - Handle thousands of PDFs efficiently
- **Error recovery** - Skip corrupted files, continue processing
- **Progress tracking** - Resume interrupted extractions

## Implementation

### Dependencies

```bash
pip install PyMuPDF
# or
uv pip install PyMuPDF
```

### Basic Extraction

```python
import fitz  # PyMuPDF

def extract_pdf_text(filepath):
    """Extract all text from a PDF file."""
    doc = fitz.open(filepath)

    pages = []
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        if text.strip():
            pages.append({
                'page': page_num,
                'text': text,
                'char_count': len(text)
            })

    doc.close()
    return pages
```

### Chunked Extraction

```python
def extract_with_chunks(filepath, chunk_size=2000, overlap=200):
    """Extract text with overlapping chunks for better context."""
    doc = fitz.open(filepath)
    chunks = []

    for page_num, page in enumerate(doc, 1):
        text = page.get_text().strip()
        if not text:
            continue

        # Split page into chunks with overlap
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.7:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1

            chunks.append({
                'page_num': page_num,
                'chunk_index': len([c for c in chunks if c['page_num'] == page_num]),
                'text': chunk,
                'char_count': len(chunk),
                'start_pos': start
            })

            start = end - overlap  # Overlap for context

    doc.close()
    return chunks
```

### Metadata Extraction

```python
def extract_metadata(filepath):
    """Extract PDF metadata."""
    doc = fitz.open(filepath)

    metadata = {
        'filename': Path(filepath).name,
        'filepath': str(filepath),
        'page_count': len(doc),
        'file_size': Path(filepath).stat().st_size,
        'title': doc.metadata.get('title', ''),
        'author': doc.metadata.get('author', ''),
        'subject': doc.metadata.get('subject', ''),
        'creator': doc.metadata.get('creator', ''),
        'creation_date': doc.metadata.get('creationDate', ''),
    }

    doc.close()
    return metadata
```

### Batch Processor

```python
import sqlite3
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFBatchExtractor:
    def __init__(self, db_path, chunk_size=2000):
        self.db_path = db_path
        self.chunk_size = chunk_size
        self.conn = sqlite3.connect(db_path, timeout=30)
        self._setup_tables()

    def _setup_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                filename TEXT NOT NULL,
                filepath TEXT UNIQUE NOT NULL,
                page_count INTEGER,
                file_size INTEGER,
                extracted BOOLEAN DEFAULT FALSE,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                doc_id INTEGER,
                page_num INTEGER,
                chunk_index INTEGER,
                chunk_text TEXT,
                char_count INTEGER,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            )
        ''')

        self.conn.commit()

    def process_directory(self, root_path):
        """Process all PDFs in directory."""
        pdf_files = list(Path(root_path).rglob('*.pdf'))
        total = len(pdf_files)

        logger.info(f"Found {total} PDF files")

        for i, filepath in enumerate(pdf_files, 1):
            self.process_file(filepath)

            if i % 100 == 0:
                logger.info(f"Progress: {i}/{total} ({100*i/total:.1f}%)")

        logger.info("Extraction complete!")

    def process_file(self, filepath):
        """Process single PDF file."""
        cursor = self.conn.cursor()

        # Check if already processed
        cursor.execute(
            'SELECT id, extracted FROM documents WHERE filepath = ?',
            (str(filepath),)
        )
        row = cursor.fetchone()

        if row and row[1]:  # Already extracted
            return

        try:
            # Extract metadata
            doc = fitz.open(filepath)

            # Insert or update document record
            if row:
                doc_id = row[0]
            else:
                cursor.execute('''
                    INSERT INTO documents (filename, filepath, page_count, file_size)
                    VALUES (?, ?, ?, ?)
                ''', (
                    filepath.name,
                    str(filepath),
                    len(doc),
                    filepath.stat().st_size
                ))
                doc_id = cursor.lastrowid

            # Extract chunks
            for page_num, page in enumerate(doc, 1):
                text = page.get_text().strip()
                if not text:
                    continue

                # Chunk the page
                for chunk_idx, start in enumerate(range(0, len(text), self.chunk_size)):
                    chunk = text[start:start + self.chunk_size]

                    cursor.execute('''
                        INSERT INTO chunks (doc_id, page_num, chunk_index, chunk_text, char_count)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (doc_id, page_num, chunk_idx, chunk, len(chunk)))

            # Mark as extracted
            cursor.execute(
                'UPDATE documents SET extracted = TRUE WHERE id = ?',
                (doc_id,)
            )

            doc.close()
            self.conn.commit()

        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            cursor.execute('''
                INSERT OR REPLACE INTO documents (filename, filepath, error_message)
                VALUES (?, ?, ?)
            ''', (filepath.name, str(filepath), str(e)))
            self.conn.commit()

    def get_stats(self):
        """Get extraction statistics."""
        cursor = self.conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM documents')
        total_docs = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM documents WHERE extracted = TRUE')
        extracted = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM chunks')
        total_chunks = cursor.fetchone()[0]

        cursor.execute('SELECT SUM(char_count) FROM chunks')
        total_chars = cursor.fetchone()[0] or 0

        return {
            'total_documents': total_docs,
            'extracted': extracted,
            'remaining': total_docs - extracted,
            'total_chunks': total_chunks,
            'total_characters': total_chars,
            'progress': f"{100*extracted/total_docs:.1f}%" if total_docs > 0 else "0%"
        }
```

### CLI Script

```python
#!/usr/bin/env python3
"""PDF Text Extraction CLI."""

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDFs')
    parser.add_argument('path', help='PDF file or directory')
    parser.add_argument('--db', default='documents.db', help='Database path')
    parser.add_argument('--chunk-size', type=int, default=2000)
    parser.add_argument('--stats', action='store_true', help='Show statistics')

    args = parser.parse_args()

    extractor = PDFBatchExtractor(args.db, args.chunk_size)

    if args.stats:
        stats = extractor.get_stats()
        print(f"Documents: {stats['extracted']}/{stats['total_documents']}")
        print(f"Chunks: {stats['total_chunks']}")
        print(f"Progress: {stats['progress']}")
        return

    path = Path(args.path)
    if path.is_file():
        extractor.process_file(path)
    else:
        extractor.process_directory(path)

    stats = extractor.get_stats()
    print(f"\nExtraction complete!")
    print(f"Documents: {stats['extracted']}")
    print(f"Chunks: {stats['total_chunks']}")

if __name__ == '__main__':
    main()
```

## Handling Edge Cases

### Encrypted PDFs

```python
def extract_with_password(filepath, password=None):
    doc = fitz.open(filepath)

    if doc.is_encrypted:
        if password:
            if not doc.authenticate(password):
                raise ValueError("Invalid password")
        else:
            raise ValueError("PDF is encrypted")

    # Continue extraction...
```

### Scanned PDFs (OCR)

```python
# For scanned PDFs, use OCR
import pytesseract
from PIL import Image

def extract_with_ocr(filepath):
    doc = fitz.open(filepath)
    pages = []

    for page in doc:
        # Check if page has text
        text = page.get_text()

        if not text.strip():
            # Convert to image and OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)

        pages.append(text)

    return pages
```

### Large PDFs

```python
def extract_large_pdf(filepath, max_pages=None):
    """Extract with memory-efficient streaming."""
    doc = fitz.open(filepath)

    for page_num, page in enumerate(doc, 1):
        if max_pages and page_num > max_pages:
            break

        text = page.get_text()
        yield {
            'page': page_num,
            'text': text
        }

        # Free memory
        page = None

    doc.close()
```

## Execution Checklist

- [ ] Verify input PDF exists and is readable
- [ ] Check if PDF is encrypted or password-protected
- [ ] Choose appropriate chunk size (1500-2500 chars optimal)
- [ ] Configure batch size for large collections
- [ ] Set up error logging for failed extractions
- [ ] Validate extracted text quality
- [ ] Check for OCR requirements (scanned documents)

## Error Handling

### Common Errors

**Error: FileNotFoundError**
- Cause: PDF file path is incorrect or file doesn't exist
- Solution: Verify file path and ensure file exists

**Error: fitz.FileDataError (encrypted)**
- Cause: PDF is password-protected
- Solution: Provide password or use `doc.authenticate(password)`

**Error: Empty text extraction**
- Cause: PDF contains scanned images, not text
- Solution: Use OCR with pytesseract and PIL

**Error: MemoryError on large PDFs**
- Cause: Loading entire PDF into memory
- Solution: Use streaming extraction with page-by-page processing

**Error: UnicodeDecodeError**
- Cause: Non-standard encoding in PDF
- Solution: Handle encoding errors with `errors='replace'`

## Metrics

| Metric | Typical Value |
|--------|---------------|
| Extraction speed | ~100 pages/second |
| OCR processing | ~2-5 pages/minute |
| Chunk generation | ~10,000 chunks/minute |
| Memory usage | ~50MB per 1000 pages |
| Batch processing | ~500 PDFs/hour |

## Best Practices

1. **Use timeout for SQLite** - `timeout=30` prevents lock errors
2. **Batch commits** - Commit every 100 files, not every file
3. **Handle errors gracefully** - Log and continue on failures
4. **Track progress** - Enable resumption of interrupted jobs
5. **Chunk appropriately** - 1500-2500 chars optimal for search
6. **Preserve page numbers** - Essential for citations

## Example Usage

```bash
# Extract single PDF
python extract.py document.pdf --db output.db

# Extract directory
python extract.py /path/to/pdfs --db knowledge.db

# Check progress
python extract.py --stats --db knowledge.db

# With custom chunk size
python extract.py /path/to/pdfs --chunk-size 1500
```

## Related Skills

- `knowledge-base-builder` - Build searchable database from extracted text
- `semantic-search-setup` - Add vector embeddings for AI search
- `document-inventory` - Catalog documents before extraction

## Dependencies

```bash
pip install PyMuPDF pytesseract pillow
```

System tools (for OCR):
- Tesseract OCR (`apt-get install tesseract-ocr` or `brew install tesseract`)

---

## Version History

- **1.2.0** (2026-01-04): Added OpenAI Codex workflow recommendation as preferred approach; updated Quick Start to show Codex-first workflow; added reference to `pdf` skill for markdown conversion
- **1.1.0** (2026-01-02): Added Quick Start, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with PyMuPDF, batch processing, OCR support, metadata extraction
