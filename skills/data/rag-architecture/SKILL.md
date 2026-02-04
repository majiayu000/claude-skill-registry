---
name: rag-architecture
description: "Use when building retrieval-augmented generation systems. Covers chunking strategies, embedding models, vector databases, retrieval patterns, and hybrid search. Apply when adding knowledge bases, document Q&A, or semantic search to applications."
---

# RAG Architecture

## Core Principle

RAG quality depends on retrieval quality. Optimize the retrieval pipeline before tuning the generation.

## When to Use This Skill

- Building document Q&A systems
- Adding knowledge bases to chatbots
- Implementing semantic search
- Creating context-aware AI features
- Reducing hallucinations with grounded responses
- Building enterprise search systems

## The Iron Law

**GARBAGE IN, GARBAGE OUT.**

If your chunks are poorly structured or your embeddings don't capture semantics, no amount of prompt engineering will save you.

## Why RAG?

**Benefits:**
- Grounds LLM responses in actual data
- Reduces hallucinations significantly
- Enables domain-specific knowledge
- Keeps data private (no fine-tuning needed)
- Easy to update (just re-index)
- Cost-effective vs fine-tuning

**Without RAG:**
- LLM makes up facts
- Knowledge cutoff limits usefulness
- No access to private data
- Expensive fine-tuning for updates
- Generic responses

## RAG Pipeline Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Documents  │───▶│  Chunking   │───▶│  Embedding  │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Response   │◀───│     LLM     │◀───│  Retrieval  │
└─────────────┘    └─────────────┘    └─────────────┘
                          ▲
                          │
                   ┌─────────────┐
                   │    Query    │
                   └─────────────┘
```

## Step 1: Document Ingestion

### Supported Formats

```python
# Common document loaders
SUPPORTED_FORMATS = {
    'text': ['.txt', '.md', '.rst'],
    'documents': ['.pdf', '.docx', '.doc', '.pptx'],
    'code': ['.py', '.js', '.ts', '.java', '.go'],
    'data': ['.csv', '.json', '.xml'],
    'web': ['html', 'urls', 'sitemaps'],
}
```

### Pre-processing

```python
def preprocess_document(doc):
    """Clean and prepare document for chunking."""
    # 1. Extract text
    text = extract_text(doc)

    # 2. Clean artifacts
    text = remove_headers_footers(text)
    text = normalize_whitespace(text)
    text = fix_encoding_issues(text)

    # 3. Preserve structure
    sections = identify_sections(text)

    # 4. Extract metadata
    metadata = {
        'source': doc.path,
        'title': extract_title(doc),
        'date': extract_date(doc),
        'type': doc.type,
    }

    return text, sections, metadata
```

## Step 2: Chunking Strategies

### Strategy Selection

| Content Type | Strategy | Chunk Size | Overlap |
|--------------|----------|------------|---------|
| Documentation | Semantic | 500-1000 | 100-200 |
| Code | Function/Class | Varies | Minimal |
| Legal/Contracts | Paragraph | 300-500 | 50-100 |
| Chat logs | Message groups | 5-10 msgs | 2-3 msgs |
| Q&A pairs | Per pair | Full pair | None |

### Fixed-Size Chunking

```python
def fixed_size_chunk(text, chunk_size=500, overlap=100):
    """Simple but effective for uniform content."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Don't cut mid-word
        if end < len(text):
            last_space = chunk.rfind(' ')
            if last_space > chunk_size * 0.8:
                chunk = chunk[:last_space]
                end = start + last_space

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks
```

### Semantic Chunking

```python
def semantic_chunk(text, max_chunk_size=1000):
    """Chunk by semantic boundaries (paragraphs, sections)."""
    # Split by semantic boundaries
    paragraphs = text.split('\n\n')

    chunks = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para)

        if current_size + para_size > max_chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(para)
        current_size += para_size

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks
```

### Recursive Chunking (LangChain style)

```python
def recursive_chunk(text, chunk_size=500, separators=None):
    """Recursively split on increasingly fine separators."""
    if separators is None:
        separators = ['\n\n', '\n', '. ', ' ', '']

    separator = separators[0]
    splits = text.split(separator)

    chunks = []
    current = []
    current_len = 0

    for split in splits:
        if current_len + len(split) > chunk_size:
            if current:
                chunk_text = separator.join(current)
                # Recursively split if still too large
                if len(chunk_text) > chunk_size and len(separators) > 1:
                    chunks.extend(recursive_chunk(
                        chunk_text, chunk_size, separators[1:]
                    ))
                else:
                    chunks.append(chunk_text)
            current = [split]
            current_len = len(split)
        else:
            current.append(split)
            current_len += len(split) + len(separator)

    if current:
        chunks.append(separator.join(current))

    return chunks
```

### Code-Aware Chunking

```python
def code_chunk(source_code, language='python'):
    """Chunk code by logical units."""
    import ast

    if language == 'python':
        tree = ast.parse(source_code)
        chunks = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                chunk = ast.get_source_segment(source_code, node)
                chunks.append({
                    'content': chunk,
                    'type': type(node).__name__,
                    'name': node.name,
                    'line_start': node.lineno,
                })

        return chunks
```

### Chunking Best Practices

```
DO:
- Keep related content together
- Include context in each chunk
- Preserve code blocks intact
- Add metadata for filtering
- Test with real queries

DON'T:
- Cut mid-sentence
- Split code functions
- Ignore document structure
- Use one-size-fits-all
- Forget about overlap
```

## Step 3: Embedding Models

### Model Selection

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| OpenAI text-embedding-3-small | 1536 | Fast | Good | $0.02/1M |
| OpenAI text-embedding-3-large | 3072 | Medium | Best | $0.13/1M |
| Cohere embed-v3 | 1024 | Fast | Good | $0.10/1M |
| Voyage-2 | 1024 | Medium | Excellent | $0.10/1M |
| BGE-large (local) | 1024 | Varies | Good | Free |
| all-MiniLM-L6 (local) | 384 | Fast | Decent | Free |

### Embedding Implementation

```python
from openai import OpenAI

client = OpenAI()

def embed_texts(texts, model="text-embedding-3-small"):
    """Embed multiple texts efficiently."""
    # Batch for efficiency (max 2048 texts per call)
    embeddings = []
    batch_size = 2048

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            model=model,
            input=batch
        )
        embeddings.extend([e.embedding for e in response.data])

    return embeddings

def embed_query(query, model="text-embedding-3-small"):
    """Embed a single query."""
    response = client.embeddings.create(
        model=model,
        input=query
    )
    return response.data[0].embedding
```

### Local Embedding (Cost-Free)

```python
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_local(texts):
    """Free local embedding."""
    return model.encode(texts, convert_to_numpy=True)
```

## Step 4: Vector Database Selection

### Database Comparison

| Database | Type | Scale | Features | Best For |
|----------|------|-------|----------|----------|
| **Pinecone** | Managed | Billions | Metadata, namespaces | Production, scale |
| **Weaviate** | Self/Managed | Millions | Hybrid search, GraphQL | Flexibility |
| **Qdrant** | Self/Managed | Millions | Filtering, payloads | Performance |
| **ChromaDB** | Embedded | Thousands | Simple API | Prototyping |
| **pgvector** | Extension | Millions | SQL integration | Existing Postgres |
| **Milvus** | Self-hosted | Billions | Enterprise features | Large scale |

### ChromaDB (Quick Start)

```python
import chromadb

# Initialize
client = chromadb.Client()
collection = client.create_collection("documents")

# Add documents
collection.add(
    documents=["Doc 1 content", "Doc 2 content"],
    metadatas=[{"source": "file1"}, {"source": "file2"}],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(
    query_texts=["search query"],
    n_results=5
)
```

### Pinecone (Production)

```python
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
index = pc.Index("your-index")

# Upsert vectors
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": embedding_vector,
            "metadata": {"source": "file1", "category": "docs"}
        }
    ],
    namespace="production"
)

# Query with metadata filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": {"$eq": "docs"}},
    include_metadata=True,
    namespace="production"
)
```

### pgvector (Postgres)

```sql
-- Enable extension
CREATE EXTENSION vector;

-- Create table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),
    metadata JSONB
);

-- Create index for fast search
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Query
SELECT content, metadata,
       1 - (embedding <=> $1) AS similarity
FROM documents
ORDER BY embedding <=> $1
LIMIT 10;
```

## Step 5: Retrieval Strategies

### Basic Similarity Search

```python
def retrieve_similar(query, k=5):
    """Basic vector similarity search."""
    query_embedding = embed_query(query)

    results = vector_db.query(
        vector=query_embedding,
        top_k=k
    )

    return [r.content for r in results]
```

### Hybrid Search (Vector + Keyword)

```python
def hybrid_search(query, k=5, alpha=0.5):
    """Combine semantic and keyword search."""
    # Semantic search
    semantic_results = vector_search(query, k=k*2)

    # Keyword search (BM25)
    keyword_results = bm25_search(query, k=k*2)

    # Reciprocal Rank Fusion
    combined = reciprocal_rank_fusion(
        [semantic_results, keyword_results],
        weights=[alpha, 1-alpha]
    )

    return combined[:k]

def reciprocal_rank_fusion(result_lists, weights, k=60):
    """RRF scoring for combining rankings."""
    scores = {}

    for results, weight in zip(result_lists, weights):
        for rank, doc in enumerate(results):
            doc_id = doc.id
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += weight * (1 / (k + rank + 1))

    sorted_docs = sorted(scores.items(), key=lambda x: -x[1])
    return [doc_id for doc_id, score in sorted_docs]
```

### Multi-Query Retrieval

```python
def multi_query_retrieve(query, k=5):
    """Generate query variations for better recall."""
    # Generate variations
    variations = generate_query_variations(query)

    all_results = []
    for q in [query] + variations:
        results = vector_search(q, k=k)
        all_results.extend(results)

    # Dedupe and rank
    unique = deduplicate_by_id(all_results)
    return rerank(query, unique)[:k]

def generate_query_variations(query):
    """Use LLM to generate query variations."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""Generate 3 alternative phrasings of this search query.
            Return only the queries, one per line.

            Query: {query}"""
        }]
    )
    return response.choices[0].message.content.strip().split('\n')
```

### Contextual Retrieval

```python
def contextual_retrieve(query, conversation_history, k=5):
    """Consider conversation context for retrieval."""
    # Rewrite query with context
    contextualized_query = rewrite_with_context(
        query,
        conversation_history
    )

    return vector_search(contextualized_query, k=k)

def rewrite_with_context(query, history):
    """Make query self-contained using conversation context."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": "Rewrite the query to be self-contained, incorporating relevant context from the conversation."
        }, {
            "role": "user",
            "content": f"Conversation:\n{history}\n\nQuery: {query}"
        }]
    )
    return response.choices[0].message.content
```

## Step 6: Reranking

### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, documents, top_k=5):
    """Rerank retrieved documents for relevance."""
    pairs = [[query, doc.content] for doc in documents]
    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, score in ranked[:top_k]]
```

### Cohere Rerank API

```python
import cohere

co = cohere.Client("your-api-key")

def cohere_rerank(query, documents, top_k=5):
    """Use Cohere's rerank endpoint."""
    response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=[d.content for d in documents],
        top_n=top_k
    )

    return [documents[r.index] for r in response.results]
```

## Step 7: Generation with Context

### Basic RAG Prompt

```python
def generate_response(query, retrieved_docs):
    """Generate response using retrieved context."""
    context = "\n\n".join([
        f"[Source: {doc.metadata['source']}]\n{doc.content}"
        for doc in retrieved_docs
    ])

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Answer the question based on the provided context.
                If the context doesn't contain the answer, say so.
                Cite sources using [Source: filename] format."""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
    )

    return response.choices[0].message.content
```

### Streaming Response

```python
def stream_rag_response(query, retrieved_docs):
    """Stream the RAG response for better UX."""
    context = format_context(retrieved_docs)

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

## Advanced Patterns

### Parent-Child Chunking

```python
def parent_child_index(document):
    """Index small chunks but retrieve larger context."""
    # Create parent chunks (larger)
    parent_chunks = semantic_chunk(document, max_size=2000)

    # Create child chunks (smaller, for retrieval)
    for i, parent in enumerate(parent_chunks):
        child_chunks = fixed_size_chunk(parent, chunk_size=200)

        for j, child in enumerate(child_chunks):
            index_chunk(
                content=child,
                metadata={
                    'parent_id': f'parent_{i}',
                    'parent_content': parent,  # Store parent
                }
            )

def retrieve_with_parent(query, k=3):
    """Retrieve children, return parents."""
    results = vector_search(query, k=k*3)

    # Get unique parents
    parent_ids = list(set(r.metadata['parent_id'] for r in results))

    # Return parent content
    return [get_parent_content(pid) for pid in parent_ids[:k]]
```

### Self-Querying Retriever

```python
def self_query_retrieve(natural_query):
    """Extract structured filters from natural language."""
    # Use LLM to parse query
    parsed = parse_query_with_llm(natural_query)

    # Example: "Show me Python tutorials from 2024"
    # parsed = {
    #     "query": "Python tutorials",
    #     "filters": {"language": "python", "year": 2024}
    # }

    return vector_search(
        query=parsed["query"],
        filter=parsed["filters"]
    )
```

## Evaluation Metrics

### Retrieval Metrics

```python
def evaluate_retrieval(queries, ground_truth):
    """Evaluate retrieval quality."""
    metrics = {
        'precision@k': [],
        'recall@k': [],
        'mrr': [],  # Mean Reciprocal Rank
    }

    for query, relevant_ids in zip(queries, ground_truth):
        retrieved = retrieve(query, k=10)
        retrieved_ids = [r.id for r in retrieved]

        # Precision@K
        relevant_retrieved = len(set(retrieved_ids) & set(relevant_ids))
        metrics['precision@k'].append(relevant_retrieved / len(retrieved_ids))

        # Recall@K
        metrics['recall@k'].append(relevant_retrieved / len(relevant_ids))

        # MRR
        for i, rid in enumerate(retrieved_ids):
            if rid in relevant_ids:
                metrics['mrr'].append(1 / (i + 1))
                break
        else:
            metrics['mrr'].append(0)

    return {k: sum(v)/len(v) for k, v in metrics.items()}
```

### End-to-End Evaluation

```python
def evaluate_rag(test_cases):
    """Evaluate full RAG pipeline."""
    results = []

    for case in test_cases:
        response = rag_pipeline(case['question'])

        results.append({
            'question': case['question'],
            'expected': case['expected_answer'],
            'actual': response,
            'relevance': judge_relevance(response, case['expected_answer']),
            'faithfulness': judge_faithfulness(response, retrieved_context),
        })

    return results
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Chunks too small | Lost context | Increase size, add overlap |
| Chunks too large | Noise in retrieval | Decrease size, semantic split |
| Wrong embedding model | Poor retrieval | Match model to content type |
| No metadata | Can't filter | Add source, date, category |
| Ignoring structure | Broken code/tables | Use format-aware chunking |
| No reranking | Irrelevant results | Add cross-encoder reranker |

## Integration with Skills

**Use with:**
- `llm-integration` - API patterns for embeddings and generation
- `agentic-design` - RAG as a tool in agent systems
- `test-driven-development` - Test retrieval quality

## Checklist

Before deploying RAG:
- [ ] Document formats properly handled
- [ ] Chunking strategy tested with real queries
- [ ] Embedding model appropriate for domain
- [ ] Vector database can handle scale
- [ ] Metadata indexed for filtering
- [ ] Retrieval quality measured
- [ ] Reranking improves results
- [ ] Response cites sources
- [ ] Latency acceptable
- [ ] Cost estimated

## Authority

**Based on:**
- Anthropic RAG best practices
- OpenAI cookbook patterns
- LangChain documentation
- Academic research on dense retrieval
- Production systems at scale

---

**Bottom Line**: RAG quality = Retrieval quality. Invest in chunking, embeddings, and retrieval before optimizing prompts. Test with real queries, measure retrieval metrics, iterate.
