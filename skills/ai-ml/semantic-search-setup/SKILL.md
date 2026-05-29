---
name: semantic-search-setup
description: Setup vector embeddings and semantic search for document collections. Use for AI-powered similarity search, finding related documents, and preparing knowledge bases for RAG systems.
version: 1.1.0
last_updated: 2026-01-02
category: document-handling
related_skills:
  - knowledge-base-builder
  - rag-system-builder
  - pdf-text-extractor
---

# Semantic Search Setup Skill

## Overview

This skill sets up vector embedding infrastructure for semantic search. Unlike keyword search (FTS5), semantic search finds conceptually similar content even without exact word matches.

## Quick Start

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
texts = ["How to fix a bug", "Debugging software issues"]
embeddings = model.encode(texts, normalize_embeddings=True)

# Compute similarity
similarity = np.dot(embeddings[0], embeddings[1])
print(f"Similarity: {similarity:.3f}")  # ~0.85
```

## When to Use

- Adding AI-powered search to document collections
- Finding conceptually related documents
- Preparing knowledge bases for RAG Q&A systems
- Building recommendation systems
- Enabling "more like this" functionality

## How Semantic Search Works

```
Text Chunk                    Query
    |                           |
    v                           v
+---------+               +---------+
| Embed   |               | Embed   |
| Model   |               | Model   |
+----+----+               +----+----+
     |                         |
     v                         v
[0.12, -0.34, ...]       [0.15, -0.31, ...]
     |                         |
     +------------+------------+
                  |
                  v
           Cosine Similarity
                  |
                  v
             0.847 (similar!)
```

## Model Selection

| Model | Dimensions | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | General purpose |
| `all-mpnet-base-v2` | 768 | Medium | Better | Higher accuracy |
| `bge-small-en-v1.5` | 384 | Fast | Good | Multilingual |
| `text-embedding-3-small` | 1536 | API | Excellent | Production (OpenAI) |

**Recommended:** `all-MiniLM-L6-v2` for local CPU processing.

## Implementation

### Step 1: Install Dependencies

```bash
pip install sentence-transformers numpy
# or
uv pip install sentence-transformers numpy
```

### Step 2: Database Schema

```python
import sqlite3

def create_embeddings_table(db_path):
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            chunk_id INTEGER UNIQUE,
            embedding BLOB NOT NULL,
            model_name TEXT NOT NULL,
            dimension INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chunk_id) REFERENCES chunks(id)
        )
    ''')

    # Index for fast lookups
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_embeddings_chunk
        ON embeddings(chunk_id)
    ''')

    conn.commit()
    return conn
```

### Step 3: Embedding Generator

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import os

class EmbeddingGenerator:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Force CPU for stability
        os.environ['CUDA_VISIBLE_DEVICES'] = ''

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed_text(self, text):
        """Generate normalized embedding for text."""
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embedding.astype(np.float32)

    def embed_batch(self, texts, batch_size=100):
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        return embeddings.astype(np.float32)

    def save_embedding(self, conn, chunk_id, embedding):
        """Save embedding to database."""
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO embeddings
            (chunk_id, embedding, model_name, dimension)
            VALUES (?, ?, ?, ?)
        ''', (
            chunk_id,
            embedding.tobytes(),
            self.model_name,
            self.dimension
        ))
        conn.commit()
```

### Step 4: Batch Processing

```python
def generate_all_embeddings(db_path, batch_size=100):
    """Generate embeddings for all chunks."""
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    generator = EmbeddingGenerator()

    # Get chunks without embeddings
    cursor.execute('''
        SELECT c.id, c.chunk_text
        FROM chunks c
        LEFT JOIN embeddings e ON c.id = e.chunk_id
        WHERE e.id IS NULL
    ''')

    chunks = cursor.fetchall()
    total = len(chunks)
    print(f"Generating embeddings for {total} chunks...")

    for i in range(0, total, batch_size):
        batch = chunks[i:i + batch_size]
        chunk_ids = [c[0] for c in batch]
        texts = [c[1] for c in batch]

        # Generate batch embeddings
        embeddings = generator.embed_batch(texts)

        # Save to database
        for chunk_id, embedding in zip(chunk_ids, embeddings):
            generator.save_embedding(conn, chunk_id, embedding)

        progress = min(i + batch_size, total)
        print(f"Progress: {progress}/{total} ({100*progress/total:.1f}%)")

    conn.close()
    print("Embedding generation complete!")
```

### Step 5: Semantic Search

```python
def semantic_search(db_path, query, top_k=10):
    """Find most similar chunks to query."""
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    generator = EmbeddingGenerator()
    query_embedding = generator.embed_text(query)

    # Get all embeddings
    cursor.execute('''
        SELECT e.chunk_id, e.embedding, c.chunk_text, d.filename, c.page_num
        FROM embeddings e
        JOIN chunks c ON e.chunk_id = c.id
        JOIN documents d ON c.doc_id = d.id
    ''')

    results = []
    for chunk_id, emb_blob, text, filename, page_num in cursor.fetchall():
        embedding = np.frombuffer(emb_blob, dtype=np.float32)

        # Cosine similarity (embeddings are normalized)
        score = float(np.dot(query_embedding, embedding))

        results.append({
            'chunk_id': chunk_id,
            'score': score,
            'text': text[:500],
            'filename': filename,
            'page': page_num
        })

    # Sort by similarity score
    results.sort(key=lambda x: x['score'], reverse=True)
    conn.close()

    return results[:top_k]
```

### Step 6: Background Service

```bash
#!/bin/bash
# embed-service.sh - Background embedding service

DB_PATH="${1:-./knowledge.db}"
BATCH_SIZE="${2:-100}"
LOG_FILE="/tmp/embed.log"
PID_FILE="/tmp/embed.pid"

start() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Already running (PID: $(cat $PID_FILE))"
        return
    fi

    # Force CPU mode
    export CUDA_VISIBLE_DEVICES=""

    nohup python3 embed.py --db "$DB_PATH" --batch "$BATCH_SIZE" \
        >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Started (PID: $!)"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        kill $(cat "$PID_FILE") 2>/dev/null
        rm "$PID_FILE"
        echo "Stopped"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Running (PID: $(cat $PID_FILE))"
    else
        echo "Not running"
    fi
}

case "$1" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    *) echo "Usage: $0 {start|stop|status}" ;;
esac
```

## Execution Checklist

- [ ] Install sentence-transformers and numpy
- [ ] Choose appropriate embedding model for use case
- [ ] Create embeddings table in database
- [ ] Generate embeddings for all text chunks
- [ ] Test semantic search with sample queries
- [ ] Compare results with keyword search (FTS5)
- [ ] Optimize batch size for available memory
- [ ] Set up background service for continuous updates

## Error Handling

### Common Errors

**Error: CUDA out of memory**
- Cause: GPU memory insufficient for model
- Solution: Set `CUDA_VISIBLE_DEVICES=""` to force CPU mode

**Error: Model download fails**
- Cause: Network issues or model not found
- Solution: Check internet connection, verify model name

**Error: numpy.frombuffer dimension mismatch**
- Cause: Embedding stored with different model
- Solution: Regenerate embeddings with consistent model

**Error: sqlite3.OperationalError (database is locked)**
- Cause: Concurrent write operations
- Solution: Use `timeout=30` and batch commits

**Error: Memory issues with large batches**
- Cause: Batch size too large for available RAM
- Solution: Reduce batch_size to 50 or lower

## Metrics

| Metric | Typical Value |
|--------|---------------|
| Embedding speed (CPU) | ~100 chunks/second |
| Embedding speed (GPU) | ~500 chunks/second |
| Storage per embedding | 1.5KB (384 dims) |
| Search latency (10K) | <100ms |
| Model load time | 2-5 seconds |

## Performance Tips

### 1. CPU vs GPU

```python
# Force CPU (more stable, sufficient for most cases)
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Use GPU if available
# Remove the above line and ensure CUDA is installed
```

### 2. Batch Processing

```python
# Larger batches = faster but more memory
batch_size = 100  # Default
batch_size = 500  # If you have 16GB+ RAM
batch_size = 50   # If memory constrained
```

### 3. Progress Tracking

```python
from tqdm import tqdm

for i in tqdm(range(0, total, batch_size)):
    # Process batch
    pass
```

### 4. Incremental Updates

```python
# Only embed new chunks
cursor.execute('''
    SELECT c.id, c.chunk_text
    FROM chunks c
    LEFT JOIN embeddings e ON c.id = e.chunk_id
    WHERE e.id IS NULL
''')
```

## Best Practices

1. **Use normalized embeddings** - Set `normalize_embeddings=True`
2. **Force CPU mode** - Set `CUDA_VISIBLE_DEVICES=""` for stability
3. **Add SQLite timeout** - Use `timeout=30` for concurrent access
4. **Process in batches** - 100-500 chunks per batch
5. **Track progress** - Save after each batch for resumability
6. **Log errors** - Capture failures for debugging

## Status Monitoring

```python
def get_embedding_status(db_path):
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM chunks')
    total_chunks = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM embeddings')
    embedded = cursor.fetchone()[0]

    conn.close()

    return {
        'total': total_chunks,
        'embedded': embedded,
        'remaining': total_chunks - embedded,
        'progress': f"{100*embedded/total_chunks:.1f}%"
    }
```

## Example Usage

```bash
# Generate embeddings
python embed.py --db knowledge.db --batch 100

# Run as background service
./embed-service.sh start

# Check progress
./embed-service.sh status

# Search
python search.py "fatigue analysis requirements"
```

## Related Skills

- `knowledge-base-builder` - Build the document database first
- `rag-system-builder` - Add AI Q&A on top of semantic search
- `pdf-text-extractor` - Extract text from PDFs

## Dependencies

```bash
pip install sentence-transformers numpy
```

Optional:
- CUDA toolkit (for GPU acceleration)
- tqdm (for progress bars)

---

## Version History

- **1.1.0** (2026-01-02): Added Quick Start, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with sentence-transformers, cosine similarity search, batch processing
