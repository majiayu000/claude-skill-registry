---
name: mteb-retrieve
description: This skill provides guidance for semantic similarity retrieval tasks using embedding models (e.g., MTEB benchmarks, document ranking). It should be used when computing embeddings for documents/queries, ranking documents by similarity, or identifying top-k similar items. Covers data preprocessing, model selection, similarity computation, and result verification.
---

# MTEB Retrieve

## Overview

This skill guides semantic similarity retrieval tasks where documents must be ranked by their similarity to a query using embedding models. These tasks typically involve loading documents, computing embeddings, calculating similarity scores, and identifying documents at specific ranks.

## Workflow

### Step 1: Data Inspection and Preprocessing

Before computing embeddings, thoroughly inspect the input data format:

1. **Examine raw file contents** - Read a sample of lines to understand the actual format
2. **Identify formatting artifacts** - Look for:
   - Line number prefixes (e.g., `1→`, `2→`, `11→`)
   - Index markers or delimiters
   - Whitespace padding or alignment characters
   - Header rows or metadata lines
3. **Clean the data** - Remove any non-semantic content:
   - Strip line numbers and prefixes using regex (e.g., `re.sub(r'^\s*\d+→', '', line)`)
   - Remove leading/trailing whitespace
   - Filter empty lines
4. **Validate preprocessing** - Print sample cleaned documents to verify they contain only semantic content

Example preprocessing pattern:
```python
import re

def clean_line(line):
    # Remove line number prefix like "  1→" or "11→"
    cleaned = re.sub(r'^\s*\d+[→\t]', '', line)
    return cleaned.strip()

documents = [clean_line(line) for line in raw_lines if clean_line(line)]
```

### Step 2: Model Selection

Select an appropriate embedding model for the content language and domain:

1. **Check model language** - Models often have language indicators in their names:
   - `zh` = Chinese (e.g., `bge-small-zh-v1.5`)
   - `en` = English (e.g., `bge-small-en-v1.5`)
   - No suffix often means multilingual or English
2. **Match model to content** - Using a Chinese-optimized model for English text (or vice versa) produces suboptimal embeddings
3. **Consider model size** - Larger models generally produce better embeddings but are slower

### Step 3: Embedding Computation

When computing embeddings:

1. **Normalize embeddings** - Use `normalize_embeddings=True` to enable cosine similarity via dot product
2. **Batch processing** - For large document sets, process in batches to manage memory
3. **Verify dimensions** - Confirm embedding dimensions match expectations for the model

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('model-name')
doc_embeddings = model.encode(documents, normalize_embeddings=True)
query_embedding = model.encode(query, normalize_embeddings=True)
```

### Step 4: Similarity Computation and Ranking

1. **Compute similarities** - Use dot product for normalized embeddings (equivalent to cosine similarity)
2. **Handle ties** - Be aware that identical similarity scores produce arbitrary ordering
3. **Use correct indexing** - For k-th highest, use index `k-1` after sorting in descending order

```python
import numpy as np

similarities = np.dot(doc_embeddings, query_embedding)
sorted_indices = np.argsort(similarities)[::-1]  # Descending order

# For 5th highest: index 4 (0-indexed)
fifth_highest_idx = sorted_indices[4]
fifth_highest_doc = documents[fifth_highest_idx]
```

### Step 5: Result Verification

Before writing final results, verify correctness:

1. **Print document count** - Confirm expected number of documents were loaded
2. **Show sample documents** - Display first few cleaned documents to verify preprocessing
3. **Display top-k results** - Print at least the top 5-10 documents with their similarity scores
4. **Cross-check output format** - Ensure the output contains only the semantic content, not formatting artifacts

```python
# Verification checklist
print(f"Total documents: {len(documents)}")
print(f"Sample document: {documents[0][:100]}...")
print("\nTop 10 by similarity:")
for i in range(min(10, len(sorted_indices))):
    idx = sorted_indices[i]
    print(f"  {i+1}. [{similarities[idx]:.4f}] {documents[idx][:50]}...")
```

## Common Pitfalls

### Data Format Issues
- **Line number prefixes** - Input files often include line numbers (e.g., `1→Text`) that corrupt embeddings if not removed
- **Invisible characters** - Watch for tabs, non-breaking spaces, or Unicode formatting characters
- **Mixed encodings** - Explicitly specify file encoding (`encoding='utf-8'`)

### Model Mismatches
- **Language mismatch** - Using language-specific models on wrong-language content
- **Version confusion** - Ensure model revision matches expected behavior

### Indexing Errors
- **Off-by-one errors** - k-th highest uses index `k-1` in 0-indexed arrays
- **Original vs sorted indices** - Track the mapping between sorted positions and original document indices

### Verification Gaps
- **No sanity checks** - Always verify document count, sample content, and score distribution
- **Missing tie handling** - Document when ties exist and how they affect results
