---
name: rag-patterns
description: Retrieval-Augmented Generation patterns and best practices. Implement chunking, embedding, retrieval, reranking, and generation pipelines. Use for knowledge-grounded AI, document QA, and semantic search applications.
---

# RAG Patterns

Expert guidance for Retrieval-Augmented Generation systems.

## Basic RAG Pipeline

```python
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize
client = OpenAI()
embedder = SentenceTransformer('all-MiniLM-L6-v2')
chroma = chromadb.Client()
collection = chroma.create_collection("documents")

# Index documents
def index_documents(documents: list[str]):
    embeddings = embedder.encode(documents)
    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        ids=[f"doc_{i}" for i in range(len(documents))]
    )

# Retrieve and generate
def rag_query(query: str, top_k: int = 5) -> str:
    # Embed query
    query_embedding = embedder.encode([query])[0]

    # Retrieve
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    # Format context
    context = "\n\n".join(results['documents'][0])

    # Generate
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Answer based on context:\n\n{context}"},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content
```

## Chunking Strategies

### Fixed Size Chunking

```python
def chunk_fixed_size(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
```

### Semantic Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_text(document)
```

### Sentence-Based Chunking

```python
import nltk
nltk.download('punkt')

def chunk_by_sentences(text: str, sentences_per_chunk: int = 5) -> list[str]:
    sentences = nltk.sent_tokenize(text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk)
    return chunks
```

### Document Structure Chunking

```python
import re

def chunk_by_sections(text: str) -> list[dict]:
    # Split by headers
    sections = re.split(r'(#{1,6}\s+.+)', text)

    chunks = []
    current_header = ""

    for i, section in enumerate(sections):
        if re.match(r'#{1,6}\s+', section):
            current_header = section.strip()
        elif section.strip():
            chunks.append({
                "header": current_header,
                "content": section.strip()
            })

    return chunks
```

## Embedding Strategies

### Hybrid Embeddings

```python
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self, documents: list[str]):
        self.documents = documents
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.embedder.encode(documents)

        # BM25 for keyword matching
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, top_k: int = 5, alpha: float = 0.5) -> list[str]:
        # Semantic search
        query_emb = self.embedder.encode([query])[0]
        semantic_scores = np.dot(self.embeddings, query_emb)

        # BM25 search
        bm25_scores = self.bm25.get_scores(query.lower().split())

        # Normalize and combine
        semantic_norm = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min())
        bm25_norm = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-6)

        combined = alpha * semantic_norm + (1 - alpha) * bm25_norm
        top_indices = np.argsort(combined)[-top_k:][::-1]

        return [self.documents[i] for i in top_indices]
```

### Multi-Vector Embeddings

```python
from openai import OpenAI

def create_multi_vector_embeddings(document: str) -> dict:
    client = OpenAI()

    # Generate summary
    summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize:\n{document}"}]
    ).choices[0].message.content

    # Generate questions
    questions = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Generate 3 questions this answers:\n{document}"}]
    ).choices[0].message.content

    # Embed all representations
    embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=[document, summary, questions]
    )

    return {
        "document": document,
        "document_embedding": embeddings.data[0].embedding,
        "summary_embedding": embeddings.data[1].embedding,
        "questions_embedding": embeddings.data[2].embedding
    }
```

## Retrieval Strategies

### Query Expansion

```python
def expand_query(query: str) -> list[str]:
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Generate 3 alternative phrasings of this query:\n{query}"
        }]
    )

    alternatives = response.choices[0].message.content.split('\n')
    return [query] + [alt.strip() for alt in alternatives if alt.strip()]
```

### HyDE (Hypothetical Document Embeddings)

```python
def hyde_retrieval(query: str, retriever) -> list[str]:
    client = OpenAI()

    # Generate hypothetical answer
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Write a detailed answer to: {query}"
        }]
    )

    hypothetical_doc = response.choices[0].message.content

    # Retrieve using hypothetical document
    return retriever.search(hypothetical_doc)
```

## Reranking

### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, documents: list[str], top_k: int = 3) -> list[str]:
    pairs = [[query, doc] for doc in documents]
    scores = reranker.predict(pairs)

    ranked_indices = np.argsort(scores)[::-1][:top_k]
    return [documents[i] for i in ranked_indices]
```

### Cohere Rerank

```python
import cohere

co = cohere.Client("your-api-key")

def cohere_rerank(query: str, documents: list[str], top_k: int = 3) -> list[str]:
    results = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=documents,
        top_n=top_k
    )

    return [documents[r.index] for r in results.results]
```

## Generation Strategies

### Context Compression

```python
def compress_context(query: str, documents: list[str], max_tokens: int = 2000) -> str:
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""Extract only the parts relevant to the query.
            Query: {query}

            Documents:
            {chr(10).join(documents)}

            Relevant excerpts:"""
        }]
    )

    return response.choices[0].message.content
```

### Citation Generation

```python
def generate_with_citations(query: str, documents: list[dict]) -> str:
    # Format with source IDs
    context = "\n\n".join([
        f"[{i+1}] {doc['content']}"
        for i, doc in enumerate(documents)
    ])

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""Answer using the context below.
            Cite sources using [1], [2], etc.

            Context:
            {context}"""},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content
```

## Evaluation

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Prepare dataset
dataset = {
    "question": ["What is X?"],
    "answer": ["X is ..."],
    "contexts": [["Context 1", "Context 2"]],
    "ground_truth": ["X is actually ..."]
}

# Evaluate
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])
print(results)
```

## Resources

- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [RAGAS Evaluation](https://docs.ragas.io/)
