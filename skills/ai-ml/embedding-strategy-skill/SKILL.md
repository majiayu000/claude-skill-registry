---
name: embedding-strategy
version: 1.0
last_updated: 2025-12-04
description: PROTECTED - Chunking strategy and embedding dimension management
license: MIT
priority: critical
triggers:
  - "chunking", "embedding", "dimension", "overlap", "splitting"
dependencies:
  - docs/protected-schemas.md
  - templates/rag-checklist.md
---

# 📐 Embedding Strategy SKILL

## Purpose

**PROTECTED:** Manage chunking strategies and embedding dimensions. Changes require user approval + full impact analysis.

---

## Chunking Strategies

### 1. RecursiveCharacterTextSplitter (Recommended)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,          # PROTECTED
    chunk_overlap=50,        # PROTECTED
    separators=["\n\n", "\n", " ", ""],
    length_function=len
)

chunks = splitter.split_text(document)
```

**When to use:** General purpose (paragraphs, sentences)

**Chunk Size Guidelines:**
- **256 tokens:** Very focused Q&A
- **512 tokens:** Balanced (recommended for most cases)
- **1024 tokens:** Broad context (summarization)
- **2048 tokens:** Document understanding

---

### 2. TokenTextSplitter

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
```

**When to use:** LLM context window management (token-based limits)

---

### 3. MarkdownTextSplitter

```python
from langchain.text_splitter import MarkdownTextSplitter

splitter = MarkdownTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
```

**When to use:** Markdown documents (preserves structure)

---

## Chunk Overlap Strategy

### Why Overlap Matters

```
Without overlap (BAD):
Chunk 1: "...end of sentence A."
Chunk 2: "Start of sentence B..."
→ Context lost between chunks

With overlap (GOOD):
Chunk 1: "...end of sentence A. Start of sentence B..."
Chunk 2: "...end of sentence A. Start of sentence B. More context..."
→ Continuity preserved
```

### Overlap Guidelines

- **Small chunks (256):** 20-30 tokens overlap
- **Medium chunks (512):** 50-100 tokens overlap
- **Large chunks (1024):** 100-200 tokens overlap

**Rule of thumb:** 10-20% of chunk_size

---

## Embedding Dimensions (PROTECTED)

### Common Models

| Model | Dimension | Use Case |
|-------|-----------|----------|
| OpenAI text-embedding-ada-002 | 1536 | General purpose |
| OpenAI text-embedding-3-small | 1536 | Cost-effective |
| OpenAI text-embedding-3-large | 3072 | Highest quality |
| Cohere embed-english-v3.0 | 1024 | English docs |
| HuggingFace all-MiniLM-L6-v2 | 384 | Fast, local |

### Protection Rule

**NEVER change dimension without:**
1. User approval
2. Full re-indexing plan
3. Backup of existing vectors

**See:** `templates/rag-checklist.md` Q1

---

## Chunk Size Optimization

### A/B Testing

```python
from ragas.metrics import ContextRelevance

# Test different chunk sizes
chunk_sizes = [256, 512, 1024]
results = {}

for size in chunk_sizes:
    splitter = RecursiveCharacterTextSplitter(chunk_size=size)
    # Re-index with new chunk size
    # Run evaluation
    score = evaluate_retrieval(splitter)
    results[size] = score

# Choose best
best_size = max(results, key=results.get)
print(f"Best chunk size: {best_size}")
```

---

## Pre-Processing Best Practices

### 1. Clean Text

```python
import re

def clean_text(text: str) -> str:
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters
    text = re.sub(r'[^\w\s.,!?-]', '', text)

    # Normalize line breaks
    text = text.replace('\r\n', '\n')

    return text.strip()
```

### 2. Remove Boilerplate

```python
def remove_boilerplate(text: str) -> str:
    # Remove headers/footers
    text = re.sub(r'Page \d+ of \d+', '', text)

    # Remove navigation
    text = re.sub(r'Home \| About \| Contact', '', text)

    return text
```

---

## Integration

**See:** `templates/rag-checklist.md` for pre-modification checklist

**Last Updated:** 2025-12-04
