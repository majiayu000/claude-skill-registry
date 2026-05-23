---
name: citations-retrieval
description: Document citations and RAG (Retrieval-Augmented Generation) patterns for Claude. Activate for source attribution, document grounding, citation extraction, and contextual retrieval.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
triggers:
  - citation
  - citations
  - rag
  - retrieval
  - source
  - document
  - grounding
  - reference
  - attribution
dependencies:
  - llm-integration
related-skills:
  - vision-multimodal
  - prompt-caching
---

# Citations & Retrieval Skill

Implement document-based citations and RAG patterns for grounded, verifiable AI responses.

## When to Use This Skill

- Document Q&A with source attribution
- RAG (Retrieval-Augmented Generation) systems
- Grounding responses in provided documents
- Building trustworthy AI applications
- Research and analysis with citations

## Core Concepts

### Citation Types

| Type | Use Case | Format |
|------|----------|--------|
| `char_location` | Text documents | Character ranges |
| `page_location` | PDFs | Page numbers |
| `content_block_location` | Custom content | Block indexes |

## Basic Citations

### Enable Citations

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    documents=[
        {
            "type": "document",
            "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": "The company was founded in 2020. Revenue reached $10M in 2023."
            },
            "title": "Company Overview",
            "citations": {"enabled": True}  # Enable citations!
        }
    ],
    messages=[{"role": "user", "content": "When was the company founded and what was the revenue?"}]
)

# Extract citations from response
for block in response.content:
    if block.type == "text":
        for citation in block.citations:
            print(f"Cited: {citation.document_title}")
            print(f"Location: chars {citation.start_char_index}-{citation.end_char_index}")
```

### Custom Content Blocks

```python
# Fine-grained control over citation granularity
documents = [{
    "type": "document",
    "source": {
        "type": "content",
        "content": [
            {"type": "text", "text": "Section 1: Introduction..."},
            {"type": "text", "text": "Section 2: Methods..."},
            {"type": "text", "text": "Section 3: Results..."}
        ]
    },
    "title": "Research Paper",
    "citations": {"enabled": True}
}]
```

## RAG Implementation

### Basic RAG Pipeline

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Embed documents
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def embed_documents(documents):
    chunks = []
    embeddings = []
    for doc in documents:
        # Chunk the document
        doc_chunks = chunk_document(doc, chunk_size=512)
        chunks.extend(doc_chunks)
        embeddings.extend(embedder.encode(doc_chunks))
    return chunks, np.array(embeddings)

# 2. Retrieve relevant chunks
def retrieve(query, chunks, embeddings, top_k=5):
    query_embedding = embedder.encode([query])[0]
    similarities = np.dot(embeddings, query_embedding)
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

# 3. Generate with retrieved context
def rag_query(query, chunks, embeddings):
    relevant_chunks = retrieve(query, chunks, embeddings)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        documents=[{
            "type": "document",
            "source": {"type": "text", "media_type": "text/plain", "data": chunk},
            "title": f"Source {i+1}",
            "citations": {"enabled": True}
        } for i, chunk in enumerate(relevant_chunks)],
        messages=[{"role": "user", "content": query}]
    )
    return response
```

### Contextual Retrieval (49-67% Better)

```python
# Add context to each chunk before embedding
def add_chunk_context(chunk, full_document):
    """Prepend context to improve retrieval accuracy by 49-67%"""

    context_prompt = f"""<document>
{full_document}
</document>

Please provide a short, succinct context for this chunk that will help with retrieval:

<chunk>
{chunk}
</chunk>

Context:"""

    response = client.messages.create(
        model="claude-haiku-4-20250514",  # Fast, cheap
        max_tokens=100,
        messages=[{"role": "user", "content": context_prompt}]
    )

    context = response.content[0].text
    return f"{context}\n\n{chunk}"

# Apply to all chunks
contextual_chunks = [add_chunk_context(chunk, full_doc) for chunk in chunks]
```

## Citation Formatting

### Format as Numbered References

```python
def format_with_citations(response):
    """Format response with numbered inline citations"""
    text = ""
    citations = []
    citation_map = {}

    for block in response.content:
        if block.type == "text":
            current_text = block.text

            for citation in block.citations:
                key = (citation.document_title, citation.start_char_index)
                if key not in citation_map:
                    citation_map[key] = len(citations) + 1
                    citations.append(citation)

                # Insert citation number
                ref_num = citation_map[key]
                current_text += f" [{ref_num}]"

            text += current_text

    # Add references section
    text += "\n\n## References\n"
    for i, citation in enumerate(citations, 1):
        text += f"[{i}] {citation.document_title}\n"

    return text
```

### Academic Citation Formats

```python
def format_apa(author, year, title, source):
    """APA format: Author (Year). Title. Source."""
    return f"{author} ({year}). {title}. {source}."

def format_mla(author, title, source, year):
    """MLA format: Author. "Title." Source, Year."""
    return f'{author}. "{title}." {source}, {year}.'

def format_chicago(author, title, source, year):
    """Chicago format: Author. Title. Source, Year."""
    return f"{author}. {title}. {source}, {year}."
```

## Multi-Document Q&A

```python
def multi_doc_qa(question, documents):
    """Answer questions across multiple documents with citations"""

    doc_inputs = []
    for i, doc in enumerate(documents):
        doc_inputs.append({
            "type": "document",
            "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": doc["content"]
            },
            "title": doc.get("title", f"Document {i+1}"),
            "citations": {"enabled": True}
        })

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        documents=doc_inputs,
        messages=[{
            "role": "user",
            "content": f"Answer this question based on the provided documents. Cite your sources.\n\nQuestion: {question}"
        }]
    )

    return response
```

## Prompt Caching for RAG

```python
# Cache static documents for repeated queries
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    documents=[{
        "type": "document",
        "source": {"type": "text", "media_type": "text/plain", "data": large_document},
        "title": "Knowledge Base",
        "citations": {"enabled": True},
        "cache_control": {"type": "ephemeral"}  # Cache this document!
    }],
    messages=[{"role": "user", "content": query}]
)
```

## Error Handling and Validation

### Validate Citation Integrity

```python
def validate_citations(response, documents):
    """Ensure all citations reference provided documents"""

    cited_titles = set()
    for block in response.content:
        if block.type == "text":
            for citation in block.citations:
                cited_titles.add(citation.document_title)

    provided_titles = {doc.get("title") for doc in documents}

    # Check for invalid citations
    invalid = cited_titles - provided_titles
    if invalid:
        raise ValueError(f"Citations reference unknown documents: {invalid}")

    return True

def extract_citation_spans(response):
    """Extract text spans for each citation"""

    citation_data = []
    for block in response.content:
        if block.type == "text":
            text = block.text
            for citation in block.citations:
                span = text[citation.start_char_index:citation.end_char_index]
                citation_data.append({
                    "text": span,
                    "document": citation.document_title,
                    "start": citation.start_char_index,
                    "end": citation.end_char_index
                })

    return citation_data
```

## Best Practices

### DO:
- Enable citations for all document-based queries
- Use contextual retrieval for better accuracy (+49-67%)
- Cache static documents with cache_control
- Provide clear document titles for attribution
- Chunk documents appropriately (512-1024 tokens)
- Validate citation integrity before using responses
- Format citations consistently (APA, MLA, Chicago)
- Test citation extraction in production systems

### DON'T:
- Rely on citations without enabling them
- Use very small chunks (<100 tokens)
- Ignore citation verification in production
- Skip document preprocessing
- Mix citation formats in the same document
- Assume all LLM responses are cited by default
- Deploy without citation validation tests

## Troubleshooting

### No Citations Returned

```python
# Ensure citations are enabled
documents = [{
    "type": "document",
    "source": {"type": "text", "media_type": "text/plain", "data": content},
    "citations": {"enabled": True}  # Must be explicit!
}]
```

### Citations Point to Wrong Text

```python
# Verify character indexes match actual text
text = block.text
cited_text = text[citation.start_char_index:citation.end_char_index]
print(f"Cited text: {cited_text}")
print(f"Expected: {expected_text}")
```

### Large Document Performance

```python
# Use chunking for large documents
def chunk_with_overlap(text, chunk_size=1024, overlap=256):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# Pass chunks individually for better retrieval
large_chunks = chunk_with_overlap(large_text)
```

## Integration Example

```python
#!/usr/bin/env python3
"""Complete RAG + Citations example"""

import anthropic
from sentence_transformers import SentenceTransformer
import numpy as np

def create_rag_system():
    """Initialize RAG system with citations"""

    client = anthropic.Anthropic()
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # Sample documents
    documents = [
        {
            "title": "Python Guide",
            "content": "Python 3.11 introduced exception groups..."
        },
        {
            "title": "Web Standards",
            "content": "HTTP/2 introduced multiplexing capabilities..."
        }
    ]

    # Embed documents
    chunks = []
    embeddings = []
    for doc in documents:
        # Add document title as context
        chunk = f"[{doc['title']}]\n{doc['content']}"
        chunks.append(chunk)
        embeddings.append(embedder.encode(chunk))

    embeddings = np.array(embeddings)

    # Query function
    def query(question):
        # Retrieve relevant chunks
        query_emb = embedder.encode(question)
        similarities = np.dot(embeddings, query_emb)
        top_idx = np.argmax(similarities)
        relevant_chunk = chunks[top_idx]

        # Get cited answer
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            documents=[{
                "type": "document",
                "source": {
                    "type": "text",
                    "media_type": "text/plain",
                    "data": relevant_chunk
                },
                "title": documents[top_idx]["title"],
                "citations": {"enabled": True}
            }],
            messages=[{
                "role": "user",
                "content": question
            }]
        )

        return response

    return query

if __name__ == "__main__":
    query_fn = create_rag_system()
    response = query_fn("What is Python 3.11?")

    # Display with citations
    for block in response.content:
        if block.type == "text":
            print(f"Answer: {block.text}")
            for citation in block.citations:
                print(f"  - Cited from: {citation.document_title}")
```

## Performance Tips

- **Batch queries** for throughput (10-20 concurrent requests)
- **Cache frequent documents** with prompt caching
- **Use Haiku for context generation** (faster, cheaper)
- **Chunk strategically** (sentence/paragraph boundaries)
- **Monitor token usage** for citation overhead (~5-10%)

## Limitations

- Citations only from provided documents
- Character index citations require exact text matching
- PDF support requires structured parsing
- Citation extraction costs tokens (~5-10% overhead)
- Batch operations not supported for cited responses

## See Also

- [[llm-integration]] - API basics and authentication
- [[prompt-caching]] - Cache documents for cost savings
- [[vision-multimodal]] - PDF and image processing
- [[complex-reasoning]] - Extended thinking with citations
