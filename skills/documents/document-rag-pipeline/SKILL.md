---
name: document-rag-pipeline
description: Build complete document knowledge bases with PDF text extraction, OCR for scanned documents, vector embeddings, and semantic search. Use this for creating searchable document libraries from folders of PDFs, technical standards, or any document collection.
version: 1.1.0
last_updated: 2026-01-02
category: document-handling
related_skills:
  - pdf-text-extractor
  - semantic-search-setup
  - rag-system-builder
  - knowledge-base-builder
---

# Document RAG Pipeline Skill

## Overview

This skill creates a complete Retrieval-Augmented Generation (RAG) system from a folder of documents. It handles:
- Regular PDF text extraction
- OCR for scanned/image-based PDFs
- DRM-protected file detection
- Text chunking with overlap
- Vector embedding generation
- SQLite storage with full-text search
- Semantic similarity search

## Quick Start

```bash
# Install dependencies
pip install PyMuPDF pytesseract Pillow sentence-transformers numpy tqdm

# Build knowledge base
python build_knowledge_base.py /path/to/documents --embed

# Search documents
python build_knowledge_base.py /path/to/documents --search "your query"
```

## When to Use

- Building searchable knowledge bases from document folders
- Processing technical standards libraries (API, ISO, ASME, etc.)
- Creating semantic search over engineering documents
- OCR processing of scanned historical documents
- Any collection of PDFs needing intelligent search

## Architecture

```
Document Folder
      │
      ▼
┌─────────────────────┐
│ 1. Build Inventory  │  SQLite catalog of all files
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. Extract Text     │  PyMuPDF for regular PDFs
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. OCR Scanned PDFs │  Tesseract + pytesseract
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. Chunk Text       │  1000 chars, 200 overlap
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 5. Generate Embeds  │  sentence-transformers
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 6. Semantic Search  │  Cosine similarity
└─────────────────────┘
```

## Prerequisites

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng poppler-utils

# macOS
brew install tesseract poppler

# Verify Tesseract
tesseract --version  # Should show 5.x
```

### Python Dependencies

```bash
pip install PyMuPDF pytesseract Pillow sentence-transformers numpy tqdm
```

Or with UV:
```bash
uv pip install PyMuPDF pytesseract Pillow sentence-transformers numpy tqdm
```

## Implementation

### Step 1: Database Schema

```python
import sqlite3
from pathlib import Path
from datetime import datetime

def create_database(db_path):
    """Create SQLite database with full schema."""
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    # Documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT UNIQUE NOT NULL,
            file_size INTEGER,
            file_type TEXT,
            page_count INTEGER,
            extraction_method TEXT,  -- 'text', 'ocr', 'failed', 'drm_protected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Text chunks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_num INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            char_count INTEGER,
            embedding BLOB,
            embedding_model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents(id),
            UNIQUE(document_id, chunk_num)
        )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON text_chunks(document_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_docs_filepath ON documents(filepath)')

    conn.commit()
    return conn
```

### Step 2: PDF Text Extraction

```python
import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(text)

        doc.close()
        full_text = "\n".join(text_parts)

        # Check if meaningful text extracted
        if len(full_text.strip()) < 100:
            return None, "no_text"

        return full_text, "text"

    except Exception as e:
        if "encrypted" in str(e).lower() or "drm" in str(e).lower():
            return None, "drm_protected"
        return None, f"error: {str(e)}"
```

### Step 3: OCR for Scanned PDFs

```python
import fitz
import pytesseract
from PIL import Image
import io

def ocr_pdf(pdf_path, dpi=200):
    """OCR scanned PDF using Tesseract."""
    try:
        doc = fitz.open(pdf_path)
        text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Convert page to image
            mat = fitz.Matrix(dpi/72, dpi/72)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))

            # OCR with Tesseract
            text = pytesseract.image_to_string(img, lang='eng')
            if text.strip():
                text_parts.append(text)

        doc.close()
        full_text = "\n".join(text_parts)

        if len(full_text.strip()) < 100:
            return None, "ocr_failed"

        return full_text, "ocr"

    except Exception as e:
        return None, f"ocr_error: {str(e)}"
```

### Step 4: Text Chunking

```python
def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at sentence boundary
        if end < text_len:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)

            if break_point > chunk_size * 0.7:
                chunk = text[start:start + break_point + 1]
                end = start + break_point + 1

        chunks.append(chunk.strip())
        start = end - overlap

        if start >= text_len:
            break

    return chunks
```

### Step 5: Embedding Generation

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

# Force CPU mode (for CUDA compatibility issues)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

def create_embeddings(db_path, model_name='all-MiniLM-L6-v2', batch_size=100):
    """Generate embeddings for all chunks without embeddings."""

    model = SentenceTransformer(model_name)
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    # Get chunks needing embeddings
    cursor.execute('''
        SELECT id, chunk_text FROM text_chunks
        WHERE embedding IS NULL
    ''')
    chunks = cursor.fetchall()

    print(f"Generating embeddings for {len(chunks)} chunks...")

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        ids = [c[0] for c in batch]
        texts = [c[1] for c in batch]

        # Generate embeddings
        embeddings = model.encode(texts, normalize_embeddings=True)

        # Store as pickled numpy arrays
        for chunk_id, emb in zip(ids, embeddings):
            emb_blob = pickle.dumps(emb.astype(np.float32))
            cursor.execute('''
                UPDATE text_chunks
                SET embedding = ?, embedding_model = ?
                WHERE id = ?
            ''', (emb_blob, model_name, chunk_id))

        conn.commit()
        print(f"  Embedded {min(i+batch_size, len(chunks))}/{len(chunks)}")

    conn.close()
    print("Embedding complete!")
```

### Step 6: Semantic Search

```python
def semantic_search(db_path, query, top_k=10, sample_size=50000):
    """Search for similar chunks using cosine similarity."""

    # Force CPU mode
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_emb = model.encode(query, normalize_embeddings=True)

    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    # Get chunks with embeddings (sample if large)
    cursor.execute('SELECT COUNT(*) FROM text_chunks WHERE embedding IS NOT NULL')
    total = cursor.fetchone()[0]

    if total > sample_size:
        # Random sample for large databases
        cursor.execute(f'''
            SELECT tc.id, tc.chunk_text, tc.embedding, d.filename
            FROM text_chunks tc
            JOIN documents d ON tc.document_id = d.id
            WHERE tc.embedding IS NOT NULL
            ORDER BY RANDOM()
            LIMIT {sample_size}
        ''')
    else:
        cursor.execute('''
            SELECT tc.id, tc.chunk_text, tc.embedding, d.filename
            FROM text_chunks tc
            JOIN documents d ON tc.document_id = d.id
            WHERE tc.embedding IS NOT NULL
        ''')

    results = []
    for chunk_id, text, emb_blob, filename in cursor.fetchall():
        emb = pickle.loads(emb_blob)

        # Cosine similarity (embeddings are normalized)
        similarity = np.dot(query_emb, emb)

        results.append({
            'id': chunk_id,
            'text': text[:500],  # Truncate for display
            'filename': filename,
            'score': float(similarity)
        })

    conn.close()

    # Sort by similarity
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]
```

## Complete Pipeline Script

```python
#!/usr/bin/env python3
"""
Document RAG Pipeline - Build searchable knowledge base from PDF folder.

Usage:
    python build_knowledge_base.py /path/to/documents --db inventory.db
    python build_knowledge_base.py /path/to/documents --search "query text"
"""

import argparse
import os
from pathlib import Path
from tqdm import tqdm

def build_inventory(folder_path, db_path):
    """Build document inventory from folder."""
    conn = create_database(db_path)
    cursor = conn.cursor()

    pdf_files = list(Path(folder_path).rglob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")

    for pdf_path in tqdm(pdf_files, desc="Building inventory"):
        # Check if already processed
        cursor.execute('SELECT id FROM documents WHERE filepath = ?',
                       (str(pdf_path),))
        if cursor.fetchone():
            continue

        file_size = pdf_path.stat().st_size

        cursor.execute('''
            INSERT INTO documents (filename, filepath, file_size, file_type)
            VALUES (?, ?, ?, 'pdf')
        ''', (pdf_path.name, str(pdf_path), file_size))

    conn.commit()
    conn.close()

def process_documents(db_path, use_ocr=True):
    """Extract text from all unprocessed documents."""
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    # Get unprocessed documents
    cursor.execute('''
        SELECT id, filepath FROM documents
        WHERE extraction_method IS NULL
    ''')
    docs = cursor.fetchall()

    stats = {'text': 0, 'ocr': 0, 'failed': 0, 'drm': 0}

    for doc_id, filepath in tqdm(docs, desc="Extracting text"):
        # Try regular extraction first
        text, method = extract_pdf_text(filepath)

        # Try OCR if no text and OCR enabled
        if text is None and use_ocr and method == "no_text":
            text, method = ocr_pdf(filepath)

        if text:
            # Chunk and store
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                cursor.execute('''
                    INSERT OR IGNORE INTO text_chunks
                    (document_id, chunk_num, chunk_text, char_count)
                    VALUES (?, ?, ?, ?)
                ''', (doc_id, i, chunk, len(chunk)))

            stats['text' if method == 'text' else 'ocr'] += 1
        else:
            if 'drm' in method:
                stats['drm'] += 1
            else:
                stats['failed'] += 1

        # Update document status
        cursor.execute('''
            UPDATE documents SET extraction_method = ? WHERE id = ?
        ''', (method, doc_id))

        conn.commit()

    conn.close()
    return stats

def main():
    parser = argparse.ArgumentParser(description='Document RAG Pipeline')
    parser.add_argument('folder', help='Folder containing documents')
    parser.add_argument('--db', default='_inventory.db', help='Database path')
    parser.add_argument('--no-ocr', action='store_true', help='Skip OCR')
    parser.add_argument('--embed', action='store_true', help='Generate embeddings')
    parser.add_argument('--search', help='Search query')
    parser.add_argument('--top-k', type=int, default=10, help='Number of results')

    args = parser.parse_args()

    db_path = Path(args.folder) / args.db

    if args.search:
        # Search mode
        results = semantic_search(str(db_path), args.search, args.top_k)
        print(f"\nTop {len(results)} results for: '{args.search}'\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['score']:.3f}] {r['filename']}")
            print(f"   {r['text'][:200]}...\n")
    else:
        # Build mode
        print("Step 1: Building inventory...")
        build_inventory(args.folder, str(db_path))

        print("\nStep 2: Extracting text...")
        stats = process_documents(str(db_path), use_ocr=not args.no_ocr)
        print(f"Results: {stats}")

        if args.embed:
            print("\nStep 3: Generating embeddings...")
            create_embeddings(str(db_path))

if __name__ == '__main__':
    main()
```

## Usage Examples

### Build Knowledge Base

```bash
# Full pipeline with OCR and embeddings
python build_knowledge_base.py /path/to/documents --embed

# Skip OCR (faster, text PDFs only)
python build_knowledge_base.py /path/to/documents --no-ocr --embed

# Just build inventory (no extraction)
python build_knowledge_base.py /path/to/documents
```

### Search Documents

```bash
# Semantic search
python build_knowledge_base.py /path/to/documents --search "subsea wellhead design"

# More results
python build_knowledge_base.py /path/to/documents --search "fatigue analysis" --top-k 20
```

### Quick Search Script

```bash
#!/bin/bash
# search_docs.sh - Quick semantic search

DB_PATH="${1:-/path/to/_inventory.db}"
QUERY="$2"

CUDA_VISIBLE_DEVICES="" python3 -c "
import sqlite3, pickle, numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
query_emb = model.encode('$QUERY', normalize_embeddings=True)

conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()
cursor.execute('''
    SELECT tc.chunk_text, tc.embedding, d.filename
    FROM text_chunks tc
    JOIN documents d ON tc.document_id = d.id
    WHERE tc.embedding IS NOT NULL
    ORDER BY RANDOM() LIMIT 50000
''')

results = []
for text, emb_blob, filename in cursor.fetchall():
    emb = pickle.loads(emb_blob)
    sim = float(np.dot(query_emb, emb))
    results.append((sim, filename, text[:200]))

for score, fname, text in sorted(results, reverse=True)[:10]:
    print(f'[{score:.3f}] {fname}')
    print(f'  {text}...\n')
"
```

## Execution Checklist

- [ ] Install system dependencies (Tesseract, Poppler)
- [ ] Install Python dependencies
- [ ] Verify document folder exists
- [ ] Run inventory to catalog documents
- [ ] Extract text (with or without OCR)
- [ ] Generate embeddings
- [ ] Test semantic search
- [ ] Monitor for DRM-protected files

## Error Handling

### Common Errors

**Error: CUDA not available**
- Cause: CUDA driver issues or incompatible GPU
- Solution: Force CPU mode with `CUDA_VISIBLE_DEVICES=""`

**Error: Tesseract not found**
- Cause: Tesseract OCR not installed
- Solution: Install with `apt-get install tesseract-ocr` or `brew install tesseract`

**Error: DRM-protected files**
- Cause: FileOpen or other DRM encryption
- Solution: Skip these files; list with `extraction_method = 'drm_protected'`

**Error: SQLite database locked**
- Cause: Concurrent access without timeout
- Solution: Use `timeout=30` in sqlite3.connect()

**Error: Out of memory**
- Cause: Large batch sizes or too many embeddings
- Solution: Reduce batch_size, use sampling for search

## Metrics

| Metric | Typical Value |
|--------|---------------|
| Text extraction | ~50 pages/second |
| OCR processing | ~2-5 pages/minute |
| Embedding generation | ~100 chunks/second (CPU) |
| Search latency | <2 seconds (50K chunks) |
| Memory usage | ~2GB for embeddings |

## Performance Metrics (Real-World)

From O&G Standards processing (957 documents):

| Metric | Value |
|--------|-------|
| Total documents | 957 |
| Text extraction | 811 PDFs |
| OCR processed | 96 PDFs |
| DRM protected | 50 PDFs |
| Total chunks | 1,043,616 |
| Embedding time | ~4 hours (CPU) |
| Search latency | <2 seconds |

## Related Skills

- `pdf-text-extractor` - Just text extraction
- `semantic-search-setup` - Just embeddings/search
- `rag-system-builder` - Add LLM Q&A layer
- `knowledge-base-builder` - Simpler document catalog

---

## Version History

- **1.1.0** (2026-01-02): Added Quick Start, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with OCR support, chunking, vector embeddings, semantic search
