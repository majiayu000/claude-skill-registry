---
name: implementing-api-patterns
description: API design and implementation across REST, GraphQL, gRPC, and tRPC patterns. Use when building backend services, public APIs, or service-to-service communication. Covers REST frameworks (FastAPI, Axum, Gin, Hono), GraphQL libraries (Strawberry, async-graphql, gqlgen, Pothos), gRPC (Tonic, Connect-Go), tRPC for TypeScript, pagination strategies (cursor-based, offset-based), rate limiting, caching, versioning, and OpenAPI documentation generation. Includes frontend integration patterns for forms, tables, dashboards, and ai-chat skills.
---

# API Patterns Skill

## Purpose

Design and implement APIs using the optimal pattern and framework for the use case. Choose between REST, GraphQL, gRPC, and tRPC based on API consumers, performance requirements, and type safety needs.

## When to Use This Skill

Use when:
- Building backend APIs for web, mobile, or service consumers
- Connecting frontend components (forms, tables, dashboards) to databases
- Implementing pagination, rate limiting, or caching strategies
- Generating OpenAPI documentation automatically
- Choosing between REST, GraphQL, gRPC, or tRPC patterns
- Integrating authentication and authorization
- Optimizing API performance and scalability

## Quick Decision Framework

```
WHO CONSUMES YOUR API?
├─ PUBLIC/THIRD-PARTY DEVELOPERS → REST with OpenAPI
│  ├─ Python → FastAPI (auto-docs, 40k req/s)
│  ├─ TypeScript → Hono (edge-first, 50k req/s, 14KB)
│  ├─ Rust → Axum (140k req/s, <1ms latency)
│  └─ Go → Gin (100k+ req/s, mature ecosystem)
│
├─ FRONTEND TEAM (same org)
│  ├─ TypeScript full-stack? → tRPC (E2E type safety)
│  └─ Complex data needs? → GraphQL
│      ├─ Python → Strawberry
│      ├─ Rust → async-graphql
│      ├─ Go → gqlgen
│      └─ TypeScript → Pothos
│
├─ SERVICE-TO-SERVICE (microservices)
│  └─ High performance → gRPC
│      ├─ Rust → Tonic
│      ├─ Go → Connect-Go (browser-friendly)
│      └─ Python → grpcio
│
└─ MOBILE APPS
   ├─ Bandwidth constrained → GraphQL (request only needed fields)
   └─ Simple CRUD → REST (standard, well-understood)
```

## REST Framework Selection

### Python: FastAPI (Recommended)

**Key Features:** Auto OpenAPI docs, Pydantic v2 validation, async/await, 40k req/s

**Basic Example:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    return {"id": 1, **item.dict()}
```

See `references/rest-design-principles.md` for FastAPI patterns and `examples/python-fastapi/`.

### TypeScript: Hono (Edge-First)

**Key Features:** 14KB bundle, runs on any runtime (Node/Deno/Bun/edge), Zod validation, 50k req/s

**Basic Example:**
```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()
app.post('/items', zValidator('json', z.object({
  name: z.string(), price: z.number()
})), (c) => c.json({ id: 1, ...c.req.valid('json') }))
```

See `references/rest-design-principles.md` for Hono patterns and `examples/typescript-hono/`.

### TypeScript: tRPC (Full-Stack Type Safety)

**Key Features:** Zero codegen, E2E type safety, React Query integration, WebSocket subscriptions

**Basic Example:**
```typescript
import { initTRPC } from '@trpc/server'
import { z } from 'zod'

const t = initTRPC.create()
export const appRouter = t.router({
  createItem: t.procedure
    .input(z.object({ name: z.string(), price: z.number() }))
    .mutation(({ input }) => ({ id: '1', ...input }))
})
export type AppRouter = typeof appRouter
```

See `references/trpc-setup-guide.md` for setup patterns and `examples/typescript-trpc/`.

### Rust: Axum (High Performance)

**Key Features:** Tower middleware, type-safe extractors, 140k req/s, compile-time verification

**Basic Example:**
```rust
use axum::{routing::post, Json, Router};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateItem { name: String, price: f64 }

#[derive(Serialize)]
struct Item { id: u64, name: String, price: f64 }

async fn create_item(Json(payload): Json<CreateItem>) -> Json<Item> {
    Json(Item { id: 1, name: payload.name, price: payload.price })
}
```

See `references/rest-design-principles.md` for Axum patterns and `examples/rust-axum/`.

### Go: Gin (Mature Ecosystem)

**Key Features:** Largest Go ecosystem, 100k+ req/s, struct tag validation

**Basic Example:**
```go
type Item struct {
    Name  string  `json:"name" binding:"required"`
    Price float64 `json:"price" binding:"required,gt=0"`
}

r := gin.Default()
r.POST("/items", func(c *gin.Context) {
    var item Item
    if c.ShouldBindJSON(&item); err != nil {
        c.JSON(400, gin.H{"error": err.Error()}); return
    }
    c.JSON(201, item)
})
```

See `references/rest-design-principles.md` for Gin patterns and `examples/go-gin/`.

## Performance Benchmarks

| Language | Framework | Req/s | Latency | Cold Start | Memory | Best For |
|----------|-----------|-------|---------|------------|--------|----------|
| Rust | Actix-web | ~150k | <1ms | N/A | 2-5MB | Maximum throughput |
| Rust | Axum | ~140k | <1ms | N/A | 2-5MB | Ergonomics + performance |
| Go | Gin | ~100k+ | 1-2ms | N/A | 5-10MB | Mature ecosystem |
| TypeScript | Hono | ~50k | <5ms | <5ms | 128MB | Edge deployment |
| Python | FastAPI | ~40k | 5-10ms | 1-2s | 30-50MB | Developer experience |
| TypeScript | Express | ~15k | 10-20ms | 1-3s | 50-100MB | Legacy systems |

**Notes:**
- Benchmarks assume single-core, JSON responses
- Actual performance varies with workload complexity
- Cold start only applies to serverless/edge deployments

## Pagination Strategies

### Cursor-Based (Recommended)

**Advantages:** Handles real-time changes, no skipped/duplicate records, scales to billions

**FastAPI Example:**
```python
@app.get("/items")
async def list_items(cursor: Optional[str] = None, limit: int = 20):
    query = db.query(Item).filter(Item.id > cursor) if cursor else db.query(Item)
    items = query.limit(limit).all()
    return {
        "items": items,
        "next_cursor": items[-1].id if items else None,
        "has_more": len(items) == limit
    }
```

### Offset-Based (Simple Cases Only)

Use only for static datasets (<10k records) with direct page access needs.

See `references/pagination-patterns.md` for complete patterns and frontend integration.

## OpenAPI Documentation

| Framework | OpenAPI Support | Docs UI | Configuration |
|-----------|----------------|---------|---------------|
| FastAPI | Automatic | Swagger UI + ReDoc | Built-in |
| Hono | Middleware plugin | Swagger UI | `@hono/swagger-ui` |
| Axum | utoipa crate | Swagger UI | Manual annotations |
| Gin | swaggo/swag | Swagger UI | Comment annotations |

**FastAPI Example (Zero Config):**
```python
app = FastAPI(title="My API", version="1.0.0")

@app.post("/items", tags=["items"])
async def create_item(item: Item) -> Item:
    """Create item with name and price"""
    return item
# Docs at /docs, /redoc, /openapi.json
```

See `references/openapi-documentation.md` for framework-specific setup.
Use `scripts/generate_openapi.py` to extract specs programmatically.

## Frontend Integration Patterns

### Forms → REST POST/PUT

**Backend:**
```python
class UserCreate(BaseModel):
    email: EmailStr; name: str; age: int

@app.post("/api/users", status_code=201)
async def create_user(user: UserCreate):
    return {"id": 1, **user.dict()}
```

**Frontend:**
```typescript
const res = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
if (!res.ok) throw new Error((await res.json()).detail)
```

### Tables → GET with Pagination

See cursor pagination example above and `references/pagination-patterns.md`.

### AI Chat → SSE Streaming

**Backend:**
```python
from sse_starlette.sse import EventSourceResponse

@app.post("/api/chat")
async def chat(message: str):
    async def gen():
        for chunk in llm_stream(message):
            yield {"event": "message", "data": chunk}
    return EventSourceResponse(gen())
```

**Frontend:**
```typescript
const es = new EventSource('/api/chat')
es.addEventListener('message', (e) => appendToChat(e.data))
```

See `examples/` for complete integration examples with each frontend skill.

## Rate Limiting

**FastAPI Example (Token Bucket):**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/items")
@limiter.limit("100/minute")
async def list_items():
    return {"items": []}
```

See `references/rate-limiting-strategies.md` for sliding window, distributed patterns, and Redis implementation.

## GraphQL Libraries

Use when frontend needs flexible data fetching or mobile apps have bandwidth constraints.

**By Language:**
- **Python**: Strawberry 0.287 (type-hint-based, async)
- **Rust**: async-graphql (high performance, tokio)
- **Go**: gqlgen (code generation from schema)
- **TypeScript**: Pothos (type-safe builder, no codegen)

See `references/graphql-schema-design.md` for schema patterns and N+1 prevention.
See `examples/graphql-strawberry/` for complete Python example.

## gRPC for Microservices

Use for service-to-service communication with strong typing and high performance.

**By Language:**
- **Rust**: Tonic (async, type-safe, code generation)
- **Go**: Connect-Go (gRPC-compatible + browser-friendly)
- **Python**: grpcio (official implementation)
- **TypeScript**: @connectrpc/connect (browser + Node.js)

See `references/grpc-protobuf-guide.md` for Protocol Buffers guide.
See `examples/grpc-tonic/` for complete Rust example.

## Additional Resources

### References
- `references/rest-design-principles.md` - REST resource modeling, HTTP methods, status codes
- `references/graphql-schema-design.md` - Schema patterns, resolver optimization, N+1 prevention
- `references/grpc-protobuf-guide.md` - Proto3 syntax, service definitions, streaming
- `references/trpc-setup-guide.md` - Router patterns, middleware, Zod validation
- `references/pagination-patterns.md` - Cursor vs offset with mathematical explanation
- `references/rate-limiting-strategies.md` - Token bucket, sliding window, Redis
- `references/caching-patterns.md` - HTTP caching, application caching strategies
- `references/versioning-strategies.md` - URI, header, media type versioning
- `references/openapi-documentation.md` - Swagger/OpenAPI best practices by framework

### Scripts (Token-Free Execution)
- `scripts/generate_openapi.py` - Generate OpenAPI spec from code
- `scripts/validate_api_spec.py` - Validate OpenAPI 3.1 compliance
- `scripts/benchmark_endpoints.py` - Load test API endpoints

### Examples
- `examples/python-fastapi/` - Complete FastAPI REST API
- `examples/typescript-hono/` - Hono edge-first API
- `examples/typescript-trpc/` - tRPC E2E type-safe API
- `examples/rust-axum/` - Axum REST API
- `examples/go-gin/` - Gin REST API
- `examples/graphql-strawberry/` - Python GraphQL
- `examples/grpc-tonic/` - Rust gRPC

## Quick Reference

**Choose REST when:** Public API, standard CRUD, need caching, OpenAPI docs required
**Choose GraphQL when:** Frontend needs flexible queries, mobile bandwidth constraints, complex nested data
**Choose gRPC when:** Service-to-service communication, high performance, bidirectional streaming
**Choose tRPC when:** TypeScript full-stack, same team owns frontend + backend, E2E type safety

**Pagination:** Always use cursor-based for production scale, offset-based only for simple cases
**Documentation:** Prefer frameworks with automatic OpenAPI generation (FastAPI, Hono)
**Performance:** Rust (Axum) for max throughput, Go (Gin) for maturity, Python (FastAPI) for DX
