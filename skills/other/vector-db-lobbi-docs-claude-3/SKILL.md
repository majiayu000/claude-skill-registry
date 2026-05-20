---
name: vectordb
description: Vector database operations for embeddings and semantic search. Activate for Pinecone, Weaviate, Chroma, pgvector, RAG, and similarity search.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Vector Database Skill

Provides comprehensive vector database capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Semantic search implementation
- RAG (Retrieval Augmented Generation)
- Embedding storage and retrieval
- Similarity search
- Vector index management

## Embedding Generation

\`\`\`python
import openai
from anthropic import Anthropic

# OpenAI embeddings
def get_openai_embedding(text: str) -> list[float]:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Batch embeddings
def get_batch_embeddings(texts: list[str]) -> list[list[float]]:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]
\`\`\`

## Pinecone

\`\`\`python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Create index
pc.create_index(
    name="agents",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-west-2"
    )
)

# Get index
index = pc.Index("agents")

# Upsert vectors
index.upsert(
    vectors=[
        {
            "id": "agent-1",
            "values": embedding,
            "metadata": {
                "name": "Claude Agent",
                "type": "claude",
                "description": "General assistant"
            }
        }
    ],
    namespace="production"
)

# Query
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    namespace="production",
    filter={"type": {"$eq": "claude"}}
)

for match in results.matches:
    print(f"{match.id}: {match.score} - {match.metadata}")

# Delete
index.delete(ids=["agent-1"], namespace="production")
\`\`\`

## Chroma

\`\`\`python
import chromadb
from chromadb.config import Settings

# Initialize
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="agents",
    metadata={"hnsw:space": "cosine"}
)

# Add documents
collection.add(
    ids=["agent-1", "agent-2"],
    embeddings=[embedding1, embedding2],
    documents=["Document 1 text", "Document 2 text"],
    metadatas=[
        {"type": "claude", "version": "3"},
        {"type": "gpt", "version": "4"}
    ]
)

# Query
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={"type": "claude"},
    include=["documents", "metadatas", "distances"]
)

# Update
collection.update(
    ids=["agent-1"],
    metadatas=[{"type": "claude", "version": "3.5"}]
)

# Delete
collection.delete(ids=["agent-1"])
\`\`\`

## pgvector (PostgreSQL)

\`\`\`sql
-- Enable extension
CREATE EXTENSION vector;

-- Create table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}'
);

-- Create index (IVFFlat for larger datasets)
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Or HNSW for better recall
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Insert
INSERT INTO documents (content, embedding, metadata)
VALUES ('Document content', '[0.1, 0.2, ...]', '{"type": "manual"}');

-- Similarity search
SELECT id, content, 1 - (embedding <=> $1) AS similarity
FROM documents
ORDER BY embedding <=> $1
LIMIT 10;

-- With filter
SELECT id, content, 1 - (embedding <=> $1) AS similarity
FROM documents
WHERE metadata->>'type' = 'manual'
ORDER BY embedding <=> $1
LIMIT 10;
\`\`\`

### Python with pgvector

\`\`\`python
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID

class Document(Base):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    embedding = Column(Vector(1536))
    metadata = Column(JSON, default={})

# Insert
doc = Document(
    content="Document content",
    embedding=embedding,
    metadata={"type": "manual"}
)
session.add(doc)
session.commit()

# Query
from sqlalchemy import select
from pgvector.sqlalchemy import cosine_distance

results = session.execute(
    select(Document)
    .order_by(cosine_distance(Document.embedding, query_embedding))
    .limit(10)
).scalars().all()
\`\`\`

## RAG Implementation

\`\`\`python
class RAGService:
    def __init__(self, vector_store, llm_client):
        self.vector_store = vector_store
        self.llm = llm_client

    async def query(self, question: str, top_k: int = 5) -> str:
        # 1. Generate query embedding
        query_embedding = await self.get_embedding(question)

        # 2. Retrieve relevant documents
        docs = await self.vector_store.search(
            embedding=query_embedding,
            top_k=top_k
        )

        # 3. Build context
        context = "\n\n".join([
            f"Document {i+1}:\n{doc.content}"
            for i, doc in enumerate(docs)
        ])

        # 4. Generate response
        prompt = f"""Answer the question based on the following context.

Context:
{context}

Question: {question}

Answer:"""

        response = await self.llm.generate(prompt)
        return response

    async def add_document(self, content: str, metadata: dict = None):
        # Chunk document
        chunks = self.chunk_text(content)

        # Generate embeddings
        embeddings = await self.get_batch_embeddings(chunks)

        # Store
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            await self.vector_store.upsert(
                id=f"{metadata.get('doc_id', 'doc')}-{i}",
                embedding=embedding,
                content=chunk,
                metadata=metadata
            )

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks
\`\`\`

## Best Practices

1. **Choose appropriate index type** (HNSW for recall, IVFFlat for scale)
2. **Chunk documents appropriately** (typically 500-1000 tokens)
3. **Include overlap** between chunks (10-20%)
4. **Store metadata** for filtering
5. **Use namespaces/collections** to organize data
6. **Monitor query latency** and index performance
7. **Batch operations** for bulk inserts
