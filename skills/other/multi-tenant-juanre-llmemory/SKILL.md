---
name: multi-tenant
description: Use when building SaaS applications needing data isolation between customers - implements owner-based filtering for secure multi-tenant document storage and search with workspace, organization, or tenant-level separation
version: 0.5.0
---

# LLMemory Multi-Tenant Patterns

## Installation

```bash
uv add llmemory
# or
pip install llmemory
```

## Overview

llmemory provides built-in multi-tenancy through the `owner_id` parameter. Every document operation is scoped to an owner, ensuring complete data isolation between tenants.

**Key concepts:**
- `owner_id`: Top-level tenant identifier (workspace, organization, customer)
- `id_at_origin`: Secondary identifier within owner (user, thread, project)
- Automatic filtering: All queries filtered by owner_id
- Schema isolation: Optional PostgreSQL schema per tenant

**When to use this pattern:**
- Building SaaS applications
- B2B platforms with customer accounts
- Workspace-based applications (Slack, Notion style)
- Any application requiring data isolation

## Quick Start

```python
from llmemory import LLMemory

async with LLMemory(connection_string="postgresql://localhost/mydb") as memory:
    # Add document for workspace-1
    await memory.add_document(
        owner_id="workspace-1",  # Tenant identifier
        id_at_origin="user-123", # User within workspace
        document_name="Q4 Report.pdf",
        document_type=DocumentType.PDF,
        content="..."
    )

    # Search is automatically filtered to workspace-1
    results = await memory.search(
        owner_id="workspace-1",  # Only returns workspace-1 documents
        query_text="quarterly revenue"
    )

    # workspace-2 cannot see workspace-1 data
    results = await memory.search(
        owner_id="workspace-2",  # No results from workspace-1
        query_text="quarterly revenue"
    )
```

## Security Implementation Details

### Database-Level Filtering Enforcement

llmemory enforces multi-tenant isolation at the PostgreSQL database level, not just in application logic. Every operation that reads or modifies data includes SQL `WHERE` clauses that filter by `owner_id`, ensuring complete data isolation.

**Key security guarantees:**
- All filtering happens in PostgreSQL using SQL WHERE clauses
- No possibility of cross-tenant data leakage via API manipulation
- Client cannot bypass owner_id filtering through any API call
- Row-level filtering is automatic and enforced by the database

### Vector Search Filtering

Vector similarity search joins documents table and applies owner_id filtering:

```python
# From src/llmemory/db.py:407
# Vector search SQL pattern:
SELECT
    c.chunk_id,
    c.document_id,
    c.content,
    c.metadata,
    1 - (e.embedding <=> $1::vector) as similarity
FROM document_chunks c
JOIN documents d ON c.document_id = d.document_id
JOIN embeddings_table e ON c.chunk_id = e.chunk_id
WHERE d.owner_id = $2  -- PostgreSQL enforces this filter
ORDER BY e.embedding <=> $1::vector
LIMIT $3
```

The `owner_id` parameter is bound to `$2` in the SQL query, making it impossible to retrieve documents belonging to other tenants even if the client attempts to manipulate the API.

### Full-Text Search Filtering

Text search also enforces owner_id at the database level:

```python
# From src/llmemory/manager.py:752-755
# Text search SQL pattern:
SELECT
    c.chunk_id,
    c.document_id,
    c.content,
    c.metadata,
    ts_rank_cd(c.search_vector, websearch_to_tsquery('english', $1)) as rank
FROM document_chunks c
JOIN documents d ON c.document_id = d.document_id
WHERE c.search_vector @@ websearch_to_tsquery('english', $1)
AND d.owner_id = $2  -- Database-level tenant filtering
ORDER BY rank DESC
LIMIT $3
```

### Hybrid Search Filtering

Hybrid search combines vector and text search, with both branches enforcing owner_id filtering:

```python
# From src/llmemory/db.py (hybrid_search method)
# Both vector and text searches apply the same owner_id filter
# Results are then fused using Reciprocal Rank Fusion

# Vector branch filters:
WHERE d.owner_id = $2

# Text branch filters:
WHERE d.owner_id = $2
AND c.search_vector @@ websearch_to_tsquery('english', $1)
```

### List and Statistics Operations

Document listing and statistics queries also filter by owner_id:

```python
# List documents
SELECT * FROM documents
WHERE owner_id = $1
ORDER BY created_at DESC
LIMIT $2 OFFSET $3

# Count documents
SELECT COUNT(*) FROM documents
WHERE owner_id = $1

# Delete documents
DELETE FROM documents
WHERE document_id = ANY($1)
AND owner_id = $2  -- Prevents deleting other tenants' documents
```

### Security Model Summary

**PostgreSQL-enforced isolation:**
1. All queries join `documents` table and filter on `d.owner_id`
2. Owner_id is a bound parameter (`$2`), not string-interpolated
3. PostgreSQL's query planner uses owner_id indexes for performance
4. No application-level bypass possible - filtering happens in database

**Additional safeguards:**
- Document deletion requires both `document_id` AND `owner_id` match
- All statistics queries scope to owner_id
- Search history logging includes owner_id for audit trails
- Embedding tables don't contain owner_id directly but access is mediated through document joins

**What this means:**
- Even if a client sends `owner_id="*"` or SQL injection attempts, PostgreSQL parameterized queries prevent abuse
- A compromised API key for one tenant cannot access another tenant's data
- Database administrators can verify isolation by examining query logs
- No trust boundary exists at the application layer - PostgreSQL enforces all isolation

## Complete API Documentation

### owner_id Parameter

**Required in all operations:**

Every llmemory operation requires `owner_id` for multi-tenant isolation:

```python
# Document operations
await memory.add_document(owner_id="...", ...)
await memory.list_documents(owner_id="...")
await memory.delete_documents(owner_id="...")
await memory.get_statistics(owner_id="...")

# Search operations
await memory.search(owner_id="...", ...)
await memory.search_with_documents(owner_id="...")
```

**Validation:**
- Must be alphanumeric with hyphens, underscores, or dots
- Maximum length: 255 characters
- Pattern: `^[a-zA-Z0-9_\-\.]+$`

**Examples of valid owner_ids:**
```python
owner_id="workspace-123"
owner_id="org_abc_def"
owner_id="customer.456"
owner_id="tenant-uuid-here"
```

### id_at_origin Parameter

Secondary identifier within an owner (optional but recommended):

```python
await memory.add_document(
    owner_id="workspace-1",      # Who owns this
    id_at_origin="user-123",     # Who created it within owner
    document_name="report.pdf",
    content="..."
)

# Search by origin
results = await memory.search(
    owner_id="workspace-1",
    query_text="report",
    id_at_origin="user-123"  # Filter to this user's documents
)

# Search across multiple origins
results = await memory.search(
    owner_id="workspace-1",
    query_text="report",
    id_at_origins=["user-123", "user-456"]  # Documents from either user
)
```

**Common id_at_origin patterns:**
- User IDs: `"user-123"`, `"auth0|abc"`
- Thread/conversation IDs: `"thread-789"`, `"conversation-xyz"`
- Project IDs: `"project-456"`
- Channel IDs: `"channel-general"`
- Any hierarchical identifier within the owner

## Multi-Tenant Architecture Patterns

### Pattern 1: Single Database, owner_id Filtering (Recommended)

All tenants in one database, filtered by `owner_id`:

```python
# Single LLMemory instance serves all tenants
memory = LLMemory(connection_string="postgresql://localhost/shared_db")
await memory.initialize()

# Each request provides its owner_id
async def handle_search_request(tenant_id: str, query: str):
    results = await memory.search(
        owner_id=tenant_id,  # Automatic filtering
        query_text=query
    )
    return results

# tenant-1 request
results_1 = await handle_search_request("tenant-1", "query")

# tenant-2 request
results_2 = await handle_search_request("tenant-2", "query")

# Results are completely isolated by owner_id
```

**Advantages:**
- Simple deployment and maintenance
- Efficient resource usage
- Easy to add new tenants
- Built-in isolation via database queries

**Disadvantages:**
- All tenants share database resources
- Cannot easily migrate single tenant to dedicated instance

### Pattern 2: Schema Isolation

Each tenant gets their own PostgreSQL schema:

```python
from pgdbm import AsyncDatabaseManager, DatabaseConfig

# Create shared pool
config = DatabaseConfig(connection_string="postgresql://localhost/mydb")
shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

# Create LLMemory instance per tenant with schema isolation
async def get_memory_for_tenant(tenant_id: str) -> LLMemory:
    db_manager = AsyncDatabaseManager(
        pool=shared_pool,
        schema=f"tenant_{tenant_id}"  # Dedicated schema per tenant
    )

    memory = LLMemory.from_db_manager(db_manager)
    await memory.initialize()  # Creates tables in tenant schema
    return memory

# Tenant 1 uses schema "tenant_workspace1"
memory_1 = await get_memory_for_tenant("workspace1")

# Tenant 2 uses schema "tenant_workspace2"
memory_2 = await get_memory_for_tenant("workspace2")

# Complete data isolation via schemas
```

**Advantages:**
- Stronger isolation (schema-level)
- Easier to backup/restore single tenant
- Can set per-tenant resource limits
- Easier data export per tenant

**Disadvantages:**
- More complex setup
- Higher overhead per tenant
- Schema management complexity

### Pattern 3: Database Per Tenant

Each tenant gets their own database:

```python
# Separate database per tenant
async def get_memory_for_tenant(tenant_id: str) -> LLMemory:
    connection_string = f"postgresql://localhost/{tenant_id}_db"

    memory = LLMemory(connection_string=connection_string)
    await memory.initialize()
    return memory

# Tenant 1: database "workspace1_db"
memory_1 = await get_memory_for_tenant("workspace1")

# Tenant 2: database "workspace2_db"
memory_2 = await get_memory_for_tenant("workspace2")
```

**Advantages:**
- Complete isolation
- Easy to scale individual tenants
- Can use different database servers
- Simplest backup/restore per tenant

**Disadvantages:**
- High resource overhead
- Complex connection management
- More databases to maintain

## Recommended Pattern: owner_id + Shared Pool

For most SaaS applications:

```python
from pgdbm import AsyncDatabaseManager, DatabaseConfig
from llmemory import LLMemory

# Global shared pool (create once at startup)
config = DatabaseConfig(
    connection_string="postgresql://localhost/app_db",
    min_connections=10,
    max_connections=50
)
shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

# Global LLMemory instance (create once)
db_manager = AsyncDatabaseManager(pool=shared_pool, schema="llmemory")
memory = LLMemory.from_db_manager(db_manager)
await memory.initialize()

# Use in request handlers
async def add_document_handler(tenant_id: str, user_id: str, doc_data: dict):
    # Validate tenant_id matches authenticated user's tenant
    if not verify_tenant_access(tenant_id):
        raise PermissionError("Access denied")

    result = await memory.add_document(
        owner_id=tenant_id,        # Tenant isolation
        id_at_origin=user_id,      # User within tenant
        document_name=doc_data["name"],
        document_type=doc_data["type"],
        content=doc_data["content"]
    )
    return result

async def search_handler(tenant_id: str, query: str, filters: dict):
    # Validate tenant_id
    if not verify_tenant_access(tenant_id):
        raise PermissionError("Access denied")

    results = await memory.search(
        owner_id=tenant_id,  # Automatic filtering to tenant
        query_text=query,
        **filters
    )
    return results
```

## Security Best Practices

### Always Validate owner_id

```python
from fastapi import HTTPException, Depends

async def get_current_tenant(user: User = Depends(get_current_user)) -> str:
    """Get tenant ID from authenticated user."""
    return user.tenant_id

async def verify_tenant_access(
    tenant_id: str,
    current_tenant: str = Depends(get_current_tenant)
) -> str:
    """Verify user has access to requested tenant."""
    if tenant_id != current_tenant:
        raise HTTPException(status_code=403, detail="Access denied")
    return tenant_id

# Use in endpoints
@app.post("/documents")
async def add_document(
    doc: DocumentCreate,
    tenant_id: str = Depends(verify_tenant_access)
):
    result = await memory.add_document(
        owner_id=tenant_id,  # Validated tenant
        id_at_origin=doc.user_id,
        document_name=doc.name,
        document_type=doc.type,
        content=doc.content
    )
    return result
```

### Never Trust Client-Provided owner_id

❌ **Wrong: Using owner_id from client**
```python
@app.post("/documents")
async def add_document(owner_id: str, doc: DocumentCreate):
    # SECURITY RISK: Client can specify any owner_id!
    result = await memory.add_document(
        owner_id=owner_id,  # From client - DO NOT DO THIS
        id_at_origin=doc.user_id,
        document_name=doc.name,
        document_type=doc.type,
        content=doc.content
    )
    return result
```

✅ **Right: Derive owner_id from authentication**
```python
@app.post("/documents")
async def add_document(
    doc: DocumentCreate,
    user: User = Depends(get_current_user)
):
    # Get owner_id from authenticated user's session
    tenant_id = user.tenant_id  # From auth, not client
result = await memory.add_document(
        owner_id=tenant_id,  # Validated from auth
        id_at_origin=user.user_id,
        document_name=doc.name,
        document_type=doc.type,
        content=doc.content
    )
    return result
```

## FastAPI Integration Example

Complete multi-tenant setup:

```python
from fastapi import FastAPI, Depends, HTTPException
from pgdbm import AsyncDatabaseManager, DatabaseConfig
from llmemory import LLMemory, DocumentType, SearchType
from typing import Optional

# Global state
app = FastAPI()
memory: Optional[LLMemory] = None

@app.on_event("startup")
async def startup():
    global memory

    # Create shared pool
    config = DatabaseConfig(
        connection_string="postgresql://localhost/app_db",
        min_connections=10,
        max_connections=50
    )
    shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

    # Create LLMemory
    db_manager = AsyncDatabaseManager(pool=shared_pool, schema="llmemory")
    memory = LLMemory.from_db_manager(db_manager)
    await memory.initialize()

@app.on_event("shutdown")
async def shutdown():
    if memory:
        await memory.close()

# Auth dependency
async def get_current_user():
    # Your auth logic here
    # Return user object with tenant_id
    pass

async def get_tenant_id(user = Depends(get_current_user)) -> str:
    return user.tenant_id

# Endpoints
@app.post("/api/documents")
async def add_document(
    name: str,
    content: str,
    doc_type: str,
    tenant_id: str = Depends(get_tenant_id),
    user = Depends(get_current_user)
):
    result = await memory.add_document(
        owner_id=tenant_id,
        id_at_origin=user.user_id,
        document_name=name,
        document_type=DocumentType(doc_type),
        content=content
    )
    return {
        "document_id": str(result.document.document_id),
        "chunks_created": result.chunks_created
    }

@app.get("/api/search")
async def search(
    q: str,
    limit: int = 10,
    tenant_id: str = Depends(get_tenant_id)
):
    results = await memory.search(
        owner_id=tenant_id,
        query_text=q,
        search_type=SearchType.HYBRID,
        limit=limit
    )
    return {"results": [r.to_dict() for r in results]}

@app.get("/api/documents")
async def list_documents(
    limit: int = 20,
    offset: int = 0,
    tenant_id: str = Depends(get_tenant_id)
):
    result = await memory.list_documents(
        owner_id=tenant_id,
        limit=limit,
        offset=offset
    )
    return {
        "documents": [d.to_dict() for d in result.documents],
        "total": result.total
    }

@app.get("/api/statistics")
async def get_stats(tenant_id: str = Depends(get_tenant_id)):
    stats = await memory.get_statistics(owner_id=tenant_id)
    return {
        "document_count": stats.document_count,
        "chunk_count": stats.chunk_count,
        "total_size_mb": stats.total_size_bytes / 1024 / 1024
    }
```

## Hierarchical Multi-Tenancy

Support for organization → workspace → user hierarchy:

```python
# Structure: org-123/workspace-456/user-789

# Add document with full hierarchy
await memory.add_document(
    owner_id="org-123/workspace-456",  # Combined owner ID
    id_at_origin="user-789",           # User within workspace
    document_name="doc.pdf",
    document_type=DocumentType.PDF,
    content="..."
)

# Search within workspace
results = await memory.search(
    owner_id="org-123/workspace-456",
    query_text="query",
    id_at_origin="user-789"  # User's documents
)

# Search across user's documents in workspace
results = await memory.search(
    owner_id="org-123/workspace-456",
    query_text="query",
    id_at_origins=["user-789", "user-123"]  # Multiple users
)

# Organization-wide search (if permitted)
# Use separate owner_id per workspace and aggregate client-side
workspaces = ["org-123/workspace-456", "org-123/workspace-789"]
all_results = []
for workspace in workspaces:
    results = await memory.search(
        owner_id=workspace,
        query_text="query",
        limit=10
    )
    all_results.extend(results)
```

## Monitoring Per Tenant

```python
# Get statistics per tenant
async def get_tenant_metrics(tenant_id: str):
    stats = await memory.get_statistics(
        owner_id=tenant_id,
        include_breakdown=True
    )

    return {
        "tenant_id": tenant_id,
        "documents": stats.document_count,
        "chunks": stats.chunk_count,
        "size_mb": stats.total_size_bytes / 1024 / 1024,
        "document_types": {
            str(k): v for k, v in (stats.document_type_breakdown or {}).items()
        }
    }

# Monitor all tenants
active_tenants = ["tenant-1", "tenant-2", "tenant-3"]
metrics = [await get_tenant_metrics(t) for t in active_tenants]

# Alert on unusual usage
for metric in metrics:
    if metric["size_mb"] > 1000:  # 1 GB limit
        send_alert(f"Tenant {metric['tenant_id']} exceeds storage limit")
```

## Data Export Per Tenant

```python
async def export_tenant_data(tenant_id: str, output_path: str):
    """Export all documents for a tenant."""
    offset = 0
    limit = 100

    with open(output_path, "w") as f:
        while True:
            result = await memory.list_documents(
                owner_id=tenant_id,
                limit=limit,
                offset=offset
            )

            if not result.documents:
                break

            for doc in result.documents:
                # Get document with chunks
                doc_data = await memory.get_document(
                    owner_id=tenant_id,
                    document_id=doc.document_id,
                    include_chunks=True
                )

                # Write to export file
                f.write(json.dumps({
                    "document_id": str(doc_data.document.document_id),
                    "document_name": doc_data.document.document_name,
                    "metadata": doc_data.document.metadata,
                    "chunks": [chunk.content for chunk in (doc_data.chunks or [])]
                }) + "\n")

            offset += limit
            if offset >= result.total:
                break

# Export tenant data
await export_tenant_data("tenant-123", "tenant-123-export.jsonl")
```

## Tenant Deletion

```python
async def delete_tenant_data(tenant_id: str):
    """Delete all data for a tenant (GDPR compliance)."""
    # Get all documents for tenant
    offset = 0
    deleted_total = 0

    while True:
        result = await memory.list_documents(
            owner_id=tenant_id,
            limit=100,
            offset=0  # Always 0 since we're deleting
        )

        if not result.documents:
            break

        # Delete batch
        doc_ids = [str(doc.document_id) for doc in result.documents]
        delete_result = await memory.delete_documents(
            owner_id=tenant_id,
            document_ids=doc_ids
        )

        deleted_total += delete_result.deleted_count

    return {
        "tenant_id": tenant_id,
        "documents_deleted": deleted_total
    }

# Delete tenant
result = await delete_tenant_data("tenant-to-delete")
print(f"Deleted {result['documents_deleted']} documents")
```

## Common Mistakes

❌ **Wrong: Forgetting owner_id validation**
```python
@app.get("/search")
async def search(owner_id: str, q: str):
    # User can pass any owner_id!
    results = await memory.search(owner_id=owner_id, query_text=q)
    return results
```

✅ **Right: Always validate from auth**
```python
@app.get("/search")
async def search(q: str, user = Depends(get_current_user)):
    # owner_id from authenticated session
    results = await memory.search(
        owner_id=user.tenant_id,
        query_text=q
    )
    return results
```

❌ **Wrong: Mixing tenants in id_at_origin**
```python
# Don't use id_at_origin for tenant separation
await memory.add_document(
    owner_id="shared",  # Same owner
    id_at_origin="tenant-1",  # Trying to use this for tenant
    document_name="doc",
    content="..."
)
# This doesn't provide proper isolation!
```

✅ **Right: Use owner_id for tenant isolation**
```python
await memory.add_document(
    owner_id="tenant-1",  # Proper tenant separation
    id_at_origin="user-123",  # User within tenant
    document_name="doc",
    content="..."
)
```

## Related Skills

- `basic-usage` - Core operations with owner_id
- `hybrid-search` - Search within tenant boundaries
- `rag` - Building multi-tenant RAG systems

## Important Notes

**Data Isolation Guarantees:**
- All llmemory operations filter by `owner_id` at the database level
- No cross-tenant data leakage possible through API
- PostgreSQL row-level security can add additional safeguards

**Performance at Scale:**
- owner_id is indexed for fast filtering
- Tested with millions of documents across thousands of tenants
- Consider partitioning by owner_id for very large deployments

**Schema vs owner_id:**
- Use owner_id filtering for most cases (simpler, sufficient)
- Use schema isolation for regulatory compliance or very large tenants
- Can combine both: schema for major tenants, owner_id within schema

**Embedding Providers:**
- Embedding tables include owner_id for proper isolation
- Vector indexes are global but filtered by owner_id during search
- No cross-tenant information leakage through embeddings
