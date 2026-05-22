---
name: chunking-strategy
description: Implement optimal chunking strategies in RAG systems and document processing pipelines. Use when building retrieval-augmented generation systems, vector databases, or processing large documents that require breaking into semantically meaningful segments for embeddings and search.
allowed-tools: Read, Write, Bash
category: artificial-intelligence
tags: [rag, chunking, vector-search, embeddings, document-processing]
version: 1.0.0
---

# Chunking Strategy for RAG Systems

## Overview

Implement optimal chunking strategies for Retrieval-Augmented Generation (RAG) systems and document processing pipelines. This skill provides a comprehensive framework for breaking large documents into smaller, semantically meaningful segments that preserve context while enabling efficient retrieval and search.

## When to Use

Use this skill when building RAG systems, optimizing vector search performance, implementing document processing pipelines, handling multi-modal content, or performance-tuning existing RAG systems with poor retrieval quality.

## Instructions

### Choose Chunking Strategy

Select appropriate chunking strategy based on document type and use case:

1. **Fixed-Size Chunking** (Level 1)
   - Use for simple documents without clear structure
   - Start with 512 tokens and 10-20% overlap
   - Adjust size based on query type: 256 for factoid, 1024 for analytical

2. **Recursive Character Chunking** (Level 2)
   - Use for documents with clear structural boundaries
   - Implement hierarchical separators: paragraphs → sentences → words
   - Customize separators for document types (HTML, Markdown)

3. **Structure-Aware Chunking** (Level 3)
   - Use for structured documents (Markdown, code, tables, PDFs)
   - Preserve semantic units: functions, sections, table blocks
   - Validate structure preservation post-splitting

4. **Semantic Chunking** (Level 4)
   - Use for complex documents with thematic shifts
   - Implement embedding-based boundary detection
   - Configure similarity threshold (0.8) and buffer size (3-5 sentences)

5. **Advanced Methods** (Level 5)
   - Use Late Chunking for long-context embedding models
   - Apply Contextual Retrieval for high-precision requirements
   - Monitor computational costs vs. retrieval improvements

Reference detailed strategy implementations in [references/strategies.md](references/strategies.md).

### Implement Chunking Pipeline

Follow these steps to implement effective chunking:

1. **Pre-process documents**
   - Analyze document structure and content types
   - Identify multi-modal content (tables, images, code)
   - Assess information density and complexity

2. **Select strategy parameters**
   - Choose chunk size based on embedding model context window
   - Set overlap percentage (10-20% for most cases)
   - Configure strategy-specific parameters

3. **Process and validate**
   - Apply chosen chunking strategy
   - Validate semantic coherence of chunks
   - Test with representative documents

4. **Evaluate and iterate**
   - Measure retrieval precision and recall
   - Monitor processing latency and resource usage
   - Optimize based on specific use case requirements

Reference detailed implementation guidelines in [references/implementation.md](references/implementation.md).

### Evaluate Performance

Use these metrics to evaluate chunking effectiveness:

- **Retrieval Precision**: Fraction of retrieved chunks that are relevant
- **Retrieval Recall**: Fraction of relevant chunks that are retrieved
- **End-to-End Accuracy**: Quality of final RAG responses
- **Processing Time**: Latency impact on overall system
- **Resource Usage**: Memory and computational costs

Reference detailed evaluation framework in [references/evaluation.md](references/evaluation.md).

## Examples

### Basic Fixed-Size Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure for factoid queries
splitter = RecursiveCharacterTextSplitter(
    chunk_size=256,
    chunk_overlap=25,
    length_function=len
)

chunks = splitter.split_documents(documents)
```

### Structure-Aware Code Chunking

```python
def chunk_python_code(code):
    """Split Python code into semantic chunks"""
    import ast

    tree = ast.parse(code)
    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            chunks.append(ast.get_source_segment(code, node))

    return chunks
```

### Semantic Chunking with Embeddings

```python
def semantic_chunk(text, similarity_threshold=0.8):
    """Chunk text based on semantic boundaries"""
    sentences = split_into_sentences(text)
    embeddings = generate_embeddings(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])

        if similarity < similarity_threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])

    chunks.append(" ".join(current_chunk))
    return chunks
```

## Best Practices

### Core Principles
- Balance context preservation with retrieval precision
- Maintain semantic coherence within chunks
- Optimize for embedding model constraints
- Preserve document structure when beneficial

### Implementation Guidelines
- Start simple with fixed-size chunking (512 tokens, 10-20% overlap)
- Test thoroughly with representative documents
- Monitor both accuracy metrics and computational costs
- Iterate based on specific document characteristics

### Common Pitfalls to Avoid
- Over-chunking: Creating too many small, context-poor chunks
- Under-chunking: Missing relevant information due to oversized chunks
- Ignoring document structure and semantic boundaries
- Using one-size-fits-all approach for diverse content types
- Neglecting overlap for boundary-crossing information

## Constraints

### Resource Considerations
- Semantic and contextual methods require significant computational resources
- Late chunking needs long-context embedding models
- Complex strategies increase processing latency
- Monitor memory usage for large document processing

### Quality Requirements
- Validate chunk semantic coherence post-processing
- Test with domain-specific documents before deployment
- Ensure chunks maintain standalone meaning where possible
- Implement proper error handling for edge cases

## References

Reference detailed documentation in the [references/](references/) folder:
- [strategies.md](references/strategies.md) - Detailed strategy implementations
- [implementation.md](references/implementation.md) - Complete implementation guidelines
- [evaluation.md](references/evaluation.md) - Performance evaluation framework
- [tools.md](references/tools.md) - Recommended libraries and frameworks
- [research.md](references/research.md) - Key research papers and findings
- [advanced-strategies.md](references/advanced-strategies.md) - 11 comprehensive chunking methods
- [semantic-methods.md](references/semantic-methods.md) - Semantic and contextual approaches
- [visualization-tools.md](references/visualization-tools.md) - Evaluation and visualization tools