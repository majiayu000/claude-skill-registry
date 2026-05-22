---
name: vector-database
description: Work with vector databases for RAG, embeddings, and semantic search using ChromaDB or similar. Use when building knowledge bases for PSI Engine or AI-powered search.
---

# 🧮 Vector Database Skill

## ChromaDB Setup

### Installation
```bash
pip install chromadb
```

### Initialize
```python
import chromadb

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# In-memory (testing)
client = chromadb.Client()

# Get or create collection
collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}
)
```

---

## CRUD Operations

### Add Documents
```python
collection.add(
    documents=["How to fix null pointer exception in Python"],
    metadatas=[{
        "source": "agent_1",
        "category": "debugging",
        "language": "python",
        "date": "2026-01-14"
    }],
    ids=["doc_001"]
)
```

### Query (Semantic Search)
```python
results = collection.query(
    query_texts=["null reference error"],
    n_results=5,
    where={"category": "debugging"},
    include=["documents", "metadatas", "distances"]
)

# Results
for i, doc in enumerate(results['documents'][0]):
    print(f"Score: {results['distances'][0][i]}")
    print(f"Doc: {doc}")
```

### Update
```python
collection.update(
    ids=["doc_001"],
    documents=["Updated solution for null pointer"],
    metadatas=[{"updated": True}]
)
```

### Delete
```python
collection.delete(ids=["doc_001"])
# or
collection.delete(where={"category": "outdated"})
```

---

## RAG Pattern

```python
def rag_query(question: str, context_limit: int = 5) -> str:
    # 1. Search similar documents
    results = collection.query(
        query_texts=[question],
        n_results=context_limit
    )
    
    # 2. Build context
    context = "\n\n".join(results['documents'][0])
    
    # 3. Generate answer with LLM
    prompt = f"""Based on this context:
{context}

Answer this question: {question}"""
    
    return llm.generate(prompt)
```

---

## Custom Embeddings

```python
from chromadb.utils import embedding_functions

# OpenAI
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-key",
    model_name="text-embedding-ada-002"
)

# Sentence Transformers (local)
st_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=st_ef
)
```

---

## Filtering

```python
# Where clause
results = collection.query(
    query_texts=["error handling"],
    where={
        "$and": [
            {"category": {"$eq": "debugging"}},
            {"language": {"$in": ["python", "javascript"]}}
        ]
    }
)

# Where document (full-text)
results = collection.query(
    query_texts=["error"],
    where_document={"$contains": "exception"}
)
```

---

## PSI Engine Integration

```python
class KnowledgeHarvester:
    def __init__(self):
        self.client = chromadb.PersistentClient("./knowledge")
        self.collection = self.client.get_or_create_collection("learnings")
    
    def harvest(self, task_result: dict):
        self.collection.add(
            documents=[task_result['solution']],
            metadatas=[{
                'task': task_result['task'],
                'agent': task_result['agent_id'],
                'timestamp': datetime.now().isoformat()
            }],
            ids=[f"learning_{uuid.uuid4()}"]
        )
    
    def find_similar(self, query: str, limit: int = 5):
        return self.collection.query(
            query_texts=[query],
            n_results=limit
        )
```
