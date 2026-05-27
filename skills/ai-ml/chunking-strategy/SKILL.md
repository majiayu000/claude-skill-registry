---
name: chunking-strategy
description: Provides chunking strategies for RAG systems. Generates chunk size recommendations (256-1024 tokens), overlap percentages (10-20%), and semantic boundary detection methods. Validates semantic coherence and evaluates retrieval precision/recall metrics. Use when building retrieval-augmented generation systems, vector databases, or processing large documents.
allowed-tools: Read, Write, Bash
---

# Chunking Strategy for RAG Systems

## Overview

Provides chunking strategies for RAG systems, vector databases, and document processing. Recommends chunk sizes, overlap percentages, and boundary detection methods; validates semantic coherence; evaluates retrieval metrics.

## When to Use

Use when building or optimizing RAG systems, vector search pipelines, document chunking workflows, or performance-tuning existing systems with poor retrieval quality.

## Instructions

### Choose Chunking Strategy

Select based on document type and use case:

1. **Fixed-Size Chunking** (Level 1)
   - Use for simple documents without clear structure
   - Start with 512 tokens and 10-20% overlap
   - Adjust: 256 for factoid queries, 1024 for analytical

2. **Recursive Character Chunking** (Level 2)
   - Use for documents with structural boundaries
   - Hierarchical separators: paragraphs → sentences → words
   - Customize for document types (HTML, Markdown, JSON)

3. **Structure-Aware Chunking** (Level 3)
   - Use for structured content (Markdown, code, tables, PDFs)
   - Preserve semantic units: functions, sections, table blocks
   - Validate structure preservation post-split

4. **Semantic Chunking** (Level 4)
   - Use for complex documents with thematic shifts
   - Embedding-based boundary detection with 0.8 similarity threshold
   - Buffer size: 3-5 sentences

5. **Advanced Methods** (Level 5)
   - Late Chunking for long-context models
   - Contextual Retrieval for high-precision requirements
   - Monitor computational cost vs. retrieval gain

Reference: [references/strategies.md](references/strategies.md).

### Implement Chunking Pipeline

1. **Pre-process documents**
   - Analyze structure, content types, information density
   - Identify multi-modal content (tables, images, code)

2. **Select parameters**
   - Chunk size: embedding model context window / 4
   - Overlap: 10-20% for most cases
   - Strategy-specific settings

3. **Process and validate**
   - Apply chunking strategy
   - Validate coherence: run `evaluate_chunks.py --coherence` (see below)
   - Test with representative documents

4. **Evaluate and iterate**
   - Measure precision and recall
   - If precision < 0.7: reduce chunk_size by 25% and re-evaluate
   - If recall < 0.6: increase overlap by 10% and re-evaluate
   - Monitor latency and memory usage

Reference: [references/implementation.md](references/implementation.md).

### Validate Chunk Quality

Run validation commands to assess chunk quality:

```bash
# Check semantic coherence (requires sentence-transformers)
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
chunks = [...]  # your chunks
embeddings = model.encode(chunks)
similarity = (embeddings @ embeddings.T).mean()
print(f'Cohesion: {similarity:.3f}')  # target: 0.3-0.7
"

# Measure retrieval precision
python -c "
relevant = sum(1 for c in retrieved if c in relevant_chunks)
precision = relevant / len(retrieved)
print(f'Precision: {precision:.2f}')  # target: >= 0.7
"

# Check chunk size distribution
python -c "
import numpy as np
sizes = [len(c.split()) for c in chunks]
print(f'Mean: {np.mean(sizes):.0f}, Std: {np.std(sizes):.0f}')
print(f'Min: {min(sizes)}, Max: {max(sizes)}')
"
```

Reference: [references/evaluation.md](references/evaluation.md).

## Examples

### Fixed-Size Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=256,
    chunk_overlap=25,
    length_function=len
)
chunks = splitter.split_documents(documents)
```

### Structure-Aware Code Chunking

```python
import ast

def chunk_python_code(code):
    tree = ast.parse(code)
    chunks = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            chunks.append(ast.get_source_segment(code, node))
    return chunks
```

### Semantic Chunking

```python
def semantic_chunk(text, similarity_threshold=0.8):
    sentences = split_into_sentences(text)
    embeddings = generate_embeddings(sentences)
    chunks, current = [], [sentences[0]]
    for i in range(1, len(sentences)):
        sim = cosine_similarity(embeddings[i-1], embeddings[i])
        if sim < similarity_threshold:
            chunks.append(" ".join(current))
            current = [sentences[i]]
        else:
            current.append(sentences[i])
    chunks.append(" ".join(current))
    return chunks
```

## Best Practices

### Core Principles
- Balance context preservation with retrieval precision
- Maintain semantic coherence within chunks
- Optimize for embedding model context window constraints

### Implementation
- Start with fixed-size (512 tokens, 15% overlap)
- Iterate based on document characteristics
- Test with domain-specific documents before deployment

### Pitfalls to Avoid
- Over-chunking: context-poor small chunks
- Under-chunking: missing information in oversized chunks
- Ignoring semantic boundaries and document structure
- One-size-fits-all for diverse content types

## Constraints and Warnings

### Resource Considerations
- Semantic methods require significant compute resources
- Late chunking needs long-context embedding models
- Complex strategies increase processing latency
- Monitor memory for large document batches

### Quality Requirements
- Validate semantic coherence post-processing
- Test with representative documents before deployment
- Ensure chunks maintain standalone meaning
- Implement error handling for malformed content

## References

- [strategies.md](references/strategies.md) - Detailed strategies
- [implementation.md](references/implementation.md) - Implementation guidelines
- [evaluation.md](references/evaluation.md) - Performance metrics
- [tools.md](references/tools.md) - Libraries and frameworks
- [research.md](references/research.md) - Research papers
- [advanced-strategies.md](references/advanced-strategies.md) - 11 advanced methods
- [semantic-methods.md](references/semantic-methods.md) - Semantic approaches
- [visualization-tools.md](references/visualization-tools.md) - Visualization tools
