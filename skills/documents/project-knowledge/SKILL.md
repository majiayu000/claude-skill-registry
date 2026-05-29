---
name: project-knowledge
description: CEI architecture, modules, data flows, conventions, tech stack decisions
---

# Project Knowledge — CEI-001

## Project Overview

**Name:** CEI-001 — Guide Interactif Pré-Projet ERP  
**Purpose:** Evaluate ERP implementation readiness for small manufacturing enterprises  
**Users:** SME manufacturers, CEI consultants, admins  
**Timeline:** 50 hours forfait  
**Budget:** Free access for users, admin requires auth  

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **Chat + Evaluation hybrid** | Chat for exploration, Evaluation for structured assessment |
| **OpenAI GPT-4** | Quality > cost for strategic consulting |
| **Weaviate RAG** | Open source, semantic search, admin-friendly |
| **PostgreSQL** | Relational, JSON support, proven reliability |
| **FastAPI** | Async native, auto-docs, type safety |
| **React + TypeScript** | Type safety, ecosystem maturity |
| **JWT auth** | Stateless, simple for admin-only protection |
| **Docker Compose** | Easy deployment, local development |

## Core Modules (8)

1. **Vision & Objectives** — Why ERP? Strategic alignment
2. **Organizational Prep** — Stakeholders, roles, change management
3. **Data & Processes** — Inventory, quality, documentation
4. **Technical Infrastructure** — Current setup, connectivity needs
5. **Resources & Budget** — Costs, availability, timeline
6. **Pitfalls to Avoid** — Common failures, risks
7. **Implementation Process** — Phases, deliverables, success criteria
8. **Post-Implementation** — Training, support, optimization

## Data Flows

### Chat Flow
```
User input → Frontend
  → POST /api/chat/message
    → Save message (PostgreSQL)
    → Query Weaviate (semantic search)
    → Build RAG context
    → Call OpenAI API (with context)
    → Stream response back
    → Save assistant message
  → Frontend displays with sources
```

### Evaluation Flow
```
User starts evaluation → Load questions (8 modules)
  → User answers module by module
  → Answers saved to PostgreSQL
  → On completion:
    → Scoring engine calculates scores
    → Generate recommendations
    → Create report
    → Return PDF
```

### Admin Document Flow
```
Admin uploads document → Upload to server
  → Save metadata (PostgreSQL)
  → Start pipeline:
    → Anonymize (OpenAI)
    → Whitelabel (OpenAI)
    → Normalize (OpenAI)
    → Enrich with summary (OpenAI)
    → Generate Q&A (OpenAI)
    → Chunk for RAG
  → Index into Weaviate
  → Publish
```

## Key Entities

- **User:** Email-based, role-based access
- **Conversation:** Chat history, multi-turn context
- **Message:** User/assistant messages with sources
- **Evaluation:** User's assessment session
- **Answer:** User's response to each question
- **Question:** Pre-defined evaluation questions (8 modules)
- **Document:** Knowledge base documents
- **DocumentChunk:** Indexed document sections (Weaviate)

## Naming Conventions

- **Routes:** `/api/[resource]/[action]`
- **Tables:** `lowercase_plural`
- **Columns:** `snake_case`
- **Models:** `PascalCase`
- **Functions:** `camelCase` (Python: `snake_case`)
- **Components:** `PascalCase.tsx`
- **Hooks:** `useXxx`

## Configuration

```python
# Core
DEBUG = False
ENVIRONMENT = "production"

# Database
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/cei"

# Weaviate
WEAVIATE_HOST = "weaviate:8080"
WEAVIATE_SCHEME = "http"

# OpenAI
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4-turbo-preview"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# Auth
JWT_SECRET = "your-secret-key-32-chars-min"
JWT_EXPIRE_HOURS = 24

# Frontend
VITE_API_URL = "https://api.yourdomain.com"
```

## Tech Stack Summary

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | React 18 + TS | Type safety, ecosystem |
| Styling | TailwindCSS 3 | Rapid, consistent UI |
| Build | Vite 5 | Fast HMR, modern |
| Backend | FastAPI 0.109 | Async, auto-docs |
| Database | PostgreSQL 16 | Relational, JSON |
| ORM | SQLAlchemy 2.0 | Async support, mature |
| Vector DB | Weaviate 1.24 | Open source, semantic |
| LLM | OpenAI API | Quality responses |
| Auth | JWT + bcrypt | Standard, simple |
| Container | Docker Compose | Multi-service |

---

---
name: rag-weaviate
description: Document indexing, semantic search, RAG pipelines, chunking, Weaviate integration
---

# RAG & Weaviate — CEI-001

## Weaviate Schema

```python
# app/services/rag_service.py
from weaviate import Client
import weaviate.classes as wvc

class RAGService:
    def __init__(self, weaviate_url: str):
        self.client = Client(f"http://{weaviate_url}")
        self._ensure_schema()
    
    def _ensure_schema(self):
        """Create Weaviate schema if not exists"""
        # Document class for indexed documents
        self.client.collections.create(
            name="Document",
            description="CEI knowledge base documents",
            vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvc.Property(
                    name="title",
                    data_type=wvc.DataType.TEXT,
                    description="Document title"
                ),
                wvc.Property(
                    name="content",
                    data_type=wvc.DataType.TEXT,
                    description="Document chunk content"
                ),
                wvc.Property(
                    name="section",
                    data_type=wvc.DataType.TEXT,
                    description="Section title"
                ),
                wvc.Property(
                    name="module",
                    data_type=wvc.DataType.TEXT,
                    description="Evaluation module (vision, org, data, etc.)"
                ),
                wvc.Property(
                    name="document_id",
                    data_type=wvc.DataType.UUID,
                    description="PostgreSQL document ID"
                ),
                wvc.Property(
                    name="chunk_index",
                    data_type=wvc.DataType.INT,
                    description="Chunk position in document"
                ),
            ]
        )
```

## Indexing Pipeline

```python
async def index_document(self, doc_id: str, chunks: List[str]):
    """Index document chunks into Weaviate"""
    
    collection = self.client.collections.get("Document")
    
    # Prepare objects
    objects = []
    for idx, chunk in enumerate(chunks):
        obj = wvc.DataObject(
            properties={
                "title": f"Document {doc_id}",
                "content": chunk,
                "section": "unknown",
                "module": "general",
                "document_id": doc_id,
                "chunk_index": idx,
            }
        )
        objects.append(obj)
    
    # Batch import
    uuids = collection.data.insert_multiple(objects)
    return uuids

async def search(self, query: str, limit: int = 3):
    """Semantic search in Weaviate"""
    
    collection = self.client.collections.get("Document")
    
    results = collection.query.near_text(
        query=query,
        limit=limit,
        where_filter=wvc.Filter.by_property("module").not_equal("archived")
    ).objects
    
    return [
        {
            "title": obj.properties["title"],
            "content": obj.properties["content"],
            "section": obj.properties["section"],
            "module": obj.properties["module"],
            "score": obj.metadata.score
        }
        for obj in results
    ]

async def reindex_document(self, doc_id: str):
    """Remove old chunks and reindex"""
    
    collection = self.client.collections.get("Document")
    
    # Delete old chunks
    collection.data.delete_many(
        where=wvc.Filter.by_property("document_id").equal(doc_id)
    )
```

## Chunking Strategy

```python
def chunk_text(
    content: str,
    chunk_size: int = 800,
    chunk_overlap: int = 100
) -> List[str]:
    """Smart chunking: split by paragraphs, then sentences"""
    
    chunks = []
    paragraphs = content.split('\n\n')
    
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Handle overlap
            if len(para) > chunk_overlap:
                current_chunk = para
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
```

## RAG Response Generation

```python
async def generate_rag_response(
    self,
    user_query: str,
    chat_history: List[Dict],
    openai_client: AsyncOpenAI
) -> Tuple[str, List[Dict]]:
    """Generate response with RAG context"""
    
    # 1. Search knowledge base
    context_docs = await self.search(user_query, limit=3)
    
    # 2. Build context
    context_text = "\n\n".join([
        f"Source: {doc['title']}\n{doc['content']}"
        for doc in context_docs
    ])
    
    # 3. Build prompt
    system_prompt = f"""Tu es un expert ERP pour PME manufacturières.

Contexte de connaissances:
{context_text}

Réponds en utilisant ce contexte. Cite les sources quand pertinent.
Sois concis et pratique."""
    
    # 4. Call OpenAI
    response = await openai_client.messages.create(
        model="gpt-4-turbo-preview",
        max_tokens=1024,
        system=system_prompt,
        messages=chat_history
    )
    
    return response.content[0].text, context_docs
```

## Embedding Configuration

```python
# app/config.py
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSION = 1536

# Cost optimization: use smaller embeddings
# text-embedding-3-small: 1536 dimensions, cheap
# text-embedding-3-large: 3072 dimensions, more precise
```

## Similarity Threshold

```python
# Search with confidence threshold
async def search_with_confidence(self, query: str, min_score: float = 0.5):
    """Only return results above confidence threshold"""
    
    results = await self.search(query, limit=5)
    
    return [
        r for r in results
        if r["score"] >= min_score
    ]
```

## Conventions

- Chunk size: 800 tokens (good for context windows)
- Chunk overlap: 100 tokens (preserve context)
- Min similarity: 0.5 (high confidence)
- Update frequency: on document publish
- Archive old versions (don't delete)
