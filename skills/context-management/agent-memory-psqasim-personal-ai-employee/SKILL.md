---
name: agent-memory
description: >
  Implement short-term and long-term memory for AI agents using vector databases and PostgreSQL.
  Covers in-session conversation memory (LangChain message history), persistent vector storage
  with pgvector (PostgreSQL + psycopg3 + langchain-postgres), and ChromaDB (both embedded and
  server modes). Use when: (1) adding conversation memory to an AI agent or chatbot, (2) building
  semantic search over past interactions, (3) storing agent memories in PostgreSQL with pgvector,
  (4) using ChromaDB as a local or server vector store, (5) implementing RAG with memory retrieval,
  (6) designing short-term (thread-scoped) vs long-term (cross-thread) agent memory.
---

# Agent Memory Systems

## Memory Architecture Decision

Choose based on your requirements:

| Need | Solution |
|------|---------|
| In-session conversation history | `InMemoryChatMessageHistory` + `RunnableWithMessageHistory` |
| Persist memory across sessions (PostgreSQL) | `PGVector` from `langchain-postgres` |
| Persist memory locally or as embedded DB | `Chroma` from `langchain-chroma` (PersistentClient) |
| Centralized vector server | ChromaDB `HttpClient` |
| Full SQL + vector hybrid queries | pgvector (raw SQL or SQLAlchemy) |

---

## Short-Term Memory (In-Session)

**Install:** `pip install langchain-core langchain-openai`

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Store: session_id → history object
store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap any chain/LLM with message history
chain_with_history = RunnableWithMessageHistory(
    runnable=chain,           # Any LangChain Runnable
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Invoke with session config
response = chain_with_history.invoke(
    {"input": "What is my name?"},
    config={"configurable": {"session_id": "user-123"}},
)
```

**InMemoryChatMessageHistory key methods:**
- `add_message(message)` — add a single BaseMessage
- `add_messages(messages)` — add list of BaseMessage
- `get_messages()` / `aget_messages()` — retrieve history
- `clear()` / `aclear()` — reset history

---

## Long-Term Memory: pgvector (PostgreSQL)

See [`references/pgvector.md`](references/pgvector.md) for full SQL reference, index types, and async patterns.

**Install:** `pip install langchain-postgres psycopg[binary] pgvector`

**Quick start:**
```python
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
connection = "postgresql+psycopg://user:pass@localhost:5432/dbname"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="agent_memories",
    connection=connection,
    use_jsonb=True,
)

# Store memories
vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])

# Retrieve memories
results = vector_store.similarity_search("user preferences", k=5)
results_with_scores = vector_store.similarity_search_with_score("topic", k=3)

# Filter by metadata
filtered = vector_store.similarity_search(
    "query",
    k=5,
    filter={"user_id": {"$eq": "user-123"}},
)

# As retriever for RAG
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20},
)
```

**Supported filter operators:** `$eq`, `$ne`, `$lt`, `$lte`, `$gt`, `$gte`, `$in`, `$nin`, `$between`, `$like`, `$ilike`, `$and`, `$or`

---

## Long-Term Memory: ChromaDB

See [`references/chromadb.md`](references/chromadb.md) for collection configuration, HNSW tuning, and embedding functions.

**Install:** `pip install langchain-chroma chromadb`

**Quick start (persistent local):**
```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

# Option A: LangChain wrapper (simplest)
vector_store = Chroma(
    collection_name="agent_memories",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db",
)

# Option B: Pass pre-configured client
persistent_client = chromadb.PersistentClient(path="./chroma_db")
vector_store = Chroma(
    client=persistent_client,
    collection_name="agent_memories",
    embedding_function=OpenAIEmbeddings(),
)

# Store memories
vector_store.add_documents(documents=docs, ids=uuids)

# Retrieve
results = vector_store.similarity_search("user preferences", k=5)
results_with_scores = vector_store.similarity_search_with_score("topic", k=3)
mmr_results = vector_store.max_marginal_relevance_search("query", k=5)

# As retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},
)
```

---

## LangGraph Long-Term Memory (Cross-Thread)

```python
from langgraph.store.memory import InMemoryStore

# Production: replace with PostgresStore or RedisStore
store = InMemoryStore(index={"embed": embed_func, "dims": 1536})

# Write memory (namespace = folder, key = document ID)
store.put(("memories", user_id), "preference_1", {"content": "Prefers concise answers"})

# Read by key
item = store.get(("memories", user_id), "preference_1")

# Semantic search
results = store.search(
    ("memories", user_id),
    query="communication style",
    limit=5,
)
```

---

## Memory Design Patterns

See [`references/memory-patterns.md`](references/memory-patterns.md) for:
- Sliding window memory (keep last N messages)
- Summarization memory (compress old turns)
- Entity memory (extract and store facts)
- Hybrid memory (short-term + long-term retrieval)
- Memory writing strategies (hot-path vs background)
