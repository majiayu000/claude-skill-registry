---
name: bknd-api-discovery
description: Use when exploring Bknd's auto-generated API endpoints. Covers REST endpoint patterns, route listing, module base paths, SDK method mapping, admin panel API explorer, and understanding the API structure.
---

# API Discovery

Explore and understand Bknd's auto-generated REST API endpoints.

## Prerequisites

- Running Bknd instance (local or deployed)
- Access to admin panel (optional but helpful)
- Basic understanding of REST APIs

## When to Use UI Mode

- Browsing available entities and their fields
- Viewing schema structure visually
- Quick endpoint exploration via browser

**UI steps:** Admin Panel > Data > Entities

## When to Use Code Mode

- Listing all registered routes programmatically
- Understanding endpoint patterns for integration
- Debugging route registration issues
- Building API documentation

## Understanding Bknd's API Structure

Bknd auto-generates REST endpoints for all configured modules:

```
┌─────────────────────────────────────────────────────────────┐
│                    Bknd API Structure                       │
├─────────────────────────────────────────────────────────────┤
│  /api/data      → CRUD for all entities                     │
│  /api/auth      → Authentication (login, register, logout)  │
│  /api/media     → File uploads and serving                  │
│  /api/system    → System operations                         │
│  /flow          → Flow management and triggers              │
│  /admin         → Admin UI (if enabled)                     │
└─────────────────────────────────────────────────────────────┘
```

## Code Approach

### Step 1: List All Routes (CLI)

Use the debug command to list all registered routes:

```bash
bknd debug routes
```

**Output:**

```
GET     /admin/*
GET     /api/auth/me
POST    /api/auth/password/login
POST    /api/auth/logout
POST    /api/auth/register
GET     /api/data/:entity
POST    /api/data/:entity
GET     /api/data/:entity/:id
PATCH   /api/data/:entity/:id
DELETE  /api/data/:entity/:id
POST    /api/media/upload
GET     /api/media/:path
...
```

### Step 2: Data API Endpoints

All entities get CRUD endpoints automatically:

| Method | Path | Description | SDK Method |
|--------|------|-------------|------------|
| GET | `/api/data/:entity` | List records | `api.data.readMany(entity)` |
| POST | `/api/data/:entity/query` | List (complex query) | `api.data.readMany(entity, query)` |
| GET | `/api/data/:entity/:id` | Get single record | `api.data.readOne(entity, id)` |
| GET | `/api/data/:entity/:id/:ref` | Get related records | `api.data.readManyByReference(...)` |
| POST | `/api/data/:entity` | Create record(s) | `api.data.createOne/Many(entity, data)` |
| PATCH | `/api/data/:entity/:id` | Update single | `api.data.updateOne(entity, id, data)` |
| PATCH | `/api/data/:entity` | Update many | `api.data.updateMany(entity, where, data)` |
| DELETE | `/api/data/:entity/:id` | Delete single | `api.data.deleteOne(entity, id)` |
| DELETE | `/api/data/:entity` | Delete many | `api.data.deleteMany(entity, where)` |
| POST | `/api/data/:entity/fn/count` | Count records | `api.data.count(entity, where)` |
| POST | `/api/data/:entity/fn/exists` | Check existence | `api.data.exists(entity, where)` |

**Example: Explore posts entity**

```bash
# List all posts
curl http://localhost:7654/api/data/posts

# Get post by ID
curl http://localhost:7654/api/data/posts/1

# Get with query params
curl "http://localhost:7654/api/data/posts?limit=10&sort[created_at]=desc"

# Get with relations
curl "http://localhost:7654/api/data/posts?with[]=author&with[]=comments"

# Complex query via POST
curl -X POST http://localhost:7654/api/data/posts/query \
  -H "Content-Type: application/json" \
  -d '{"where": {"status": "published"}, "limit": 10}'
```

### Step 3: Auth API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/auth/me` | Current user info |
| POST | `/api/auth/:strategy/login` | Login (e.g., `/api/auth/password/login`) |
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/:strategy/redirect` | OAuth redirect |
| GET | `/api/auth/:strategy/callback` | OAuth callback |

**Example:**

```bash
# Check current user
curl http://localhost:7654/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Login
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "pass123"}'

# Register
curl -X POST http://localhost:7654/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "new@test.com", "password": "pass123"}'
```

### Step 4: Media API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/media/upload` | Upload file |
| GET | `/api/media/:path` | Serve/download file |

**Example:**

```bash
# Upload file
curl -X POST http://localhost:7654/api/media/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@image.png"

# Serve file
curl http://localhost:7654/api/media/uploads/image.png
```

### Step 5: Flow Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/flow` | List all flows |
| GET | `/flow/:name` | Get flow details |
| GET | `/flow/:name/run` | Manually run flow |
| * | Custom trigger path | HTTP trigger endpoints |

**Example:**

```bash
# List flows
curl http://localhost:7654/flow

# Run flow manually
curl http://localhost:7654/flow/my-flow/run
```

### Step 6: Programmatic Route Discovery

Access route information from your code:

```typescript
import { App } from "bknd";

const app = new App({ /* config */ });
await app.build();

// Get Hono server instance
const server = app.server;

// Routes are registered on the Hono instance
// Use bknd debug routes for listing
```

### Step 7: Discover Entity Schema

Query the system to understand available entities:

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// List available entities by checking which respond
const entities = ["posts", "users", "comments", "categories"];

for (const entity of entities) {
  const { ok } = await api.data.readMany(entity, { limit: 1 });
  if (ok) {
    console.log(`Entity exists: ${entity}`);
  }
}
```

### Step 8: Response Format Discovery

All endpoints return consistent response format:

**Success (list):**

```json
{
  "data": [
    { "id": 1, "title": "Post 1" },
    { "id": 2, "title": "Post 2" }
  ],
  "meta": {
    "total": 50,
    "limit": 20,
    "offset": 0
  }
}
```

**Success (single):**

```json
{
  "data": { "id": 1, "title": "Post 1" }
}
```

**Error:**

```json
{
  "error": {
    "message": "Record not found",
    "code": "NOT_FOUND"
  }
}
```

## UI Approach: Admin Panel

### Step 1: Access Admin Panel

Navigate to: `http://localhost:7654/admin`

### Step 2: Browse Entities

1. Click **Data** in sidebar
2. View list of all entities
3. Click entity to see:
   - All fields with types
   - Relationships
   - Sample data

### Step 3: View Entity Structure

Admin panel shows:
- Field names and types
- Required vs optional fields
- Default values
- Relation configurations

### Step 4: Test Queries

Admin panel provides:
- Data browser for each entity
- Filter/sort interface
- Create/edit forms
- Relationship navigation

## Query Parameter Reference

### Data Endpoints

| Parameter | Example | Description |
|-----------|---------|-------------|
| `limit` | `?limit=10` | Max records to return |
| `offset` | `?offset=20` | Skip N records |
| `sort[field]` | `?sort[created_at]=desc` | Sort by field |
| `where[field]` | `?where[status]=published` | Filter by field |
| `with[]` | `?with[]=author` | Include relation |
| `join[]` | `?join[]=author` | Join relation (same result) |
| `select[]` | `?select[]=id&select[]=title` | Select specific fields |

### Complex Queries (POST)

```bash
curl -X POST http://localhost:7654/api/data/posts/query \
  -H "Content-Type: application/json" \
  -d '{
    "where": {
      "status": "published",
      "views": { "$gt": 100 }
    },
    "sort": { "created_at": "desc" },
    "limit": 10,
    "offset": 0,
    "with": ["author", "category"]
  }'
```

## SDK Method to Endpoint Mapping

```typescript
import { Api } from "bknd";
const api = new Api({ host: "http://localhost:7654" });

// Method                        → Endpoint
api.data.readMany("posts")       // GET  /api/data/posts
api.data.readOne("posts", 1)     // GET  /api/data/posts/1
api.data.createOne("posts", {})  // POST /api/data/posts
api.data.updateOne("posts", 1, {})// PATCH /api/data/posts/1
api.data.deleteOne("posts", 1)   // DELETE /api/data/posts/1

api.auth.login("password", {})   // POST /api/auth/password/login
api.auth.register({})            // POST /api/auth/register
api.auth.logout()                // POST /api/auth/logout
api.auth.me()                    // GET  /api/auth/me

api.media.upload(file)           // POST /api/media/upload
```

## Testing Endpoints

### Quick Health Check

```bash
# Check if API is running
curl http://localhost:7654/api/auth/me
# Returns user info or 401
```

### Explore Available Data

```bash
# Try common entity names
for entity in posts users comments products orders; do
  echo "Testing $entity..."
  curl -s -o /dev/null -w "%{http_code}" http://localhost:7654/api/data/$entity
  echo ""
done
```

### Debug Script

```typescript
async function discoverApi(host: string) {
  const api = new Api({ host });

  console.log("API Discovery Report");
  console.log("===================");

  // Test auth
  const { ok: authOk } = await api.auth.me();
  console.log(`Auth endpoint: ${authOk ? "working" : "requires auth"}`);

  // Test common entities
  const testEntities = ["posts", "users", "comments", "products"];
  for (const entity of testEntities) {
    const { ok, meta } = await api.data.readMany(entity, { limit: 1 });
    if (ok) {
      console.log(`Entity "${entity}": ${meta?.total ?? "?"} records`);
    }
  }
}

discoverApi("http://localhost:7654");
```

## Common Pitfalls

### Wrong Base Path

**Problem:** 404 errors on API calls

**Fix:** Use correct base paths:

```bash
# WRONG
curl http://localhost:7654/data/posts
curl http://localhost:7654/posts

# CORRECT
curl http://localhost:7654/api/data/posts
```

### Auth Strategy in Path

**Problem:** Login fails

**Fix:** Include strategy name:

```bash
# WRONG
curl -X POST http://localhost:7654/api/auth/login

# CORRECT (password strategy)
curl -X POST http://localhost:7654/api/auth/password/login
```

### Query vs GET Params

**Problem:** Complex queries don't work via GET

**Fix:** Use POST for complex queries:

```bash
# Limited filtering via GET
curl "http://localhost:7654/api/data/posts?where[status]=published"

# Complex filtering via POST
curl -X POST http://localhost:7654/api/data/posts/query \
  -H "Content-Type: application/json" \
  -d '{"where": {"$or": [{"status": "published"}, {"featured": true}]}}'
```

### Entity Name Mismatch

**Problem:** 404 on entity endpoints

**Fix:** Use exact entity names (case-sensitive, usually lowercase):

```bash
# WRONG
curl http://localhost:7654/api/data/Posts
curl http://localhost:7654/api/data/post

# CORRECT
curl http://localhost:7654/api/data/posts
```

### Missing Content-Type

**Problem:** POST/PATCH returns 400

**Fix:** Include Content-Type header:

```bash
# WRONG
curl -X POST http://localhost:7654/api/data/posts \
  -d '{"title": "Test"}'

# CORRECT
curl -X POST http://localhost:7654/api/data/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
```

## Endpoint Quick Reference

| Module | Base Path | Key Operations |
|--------|-----------|----------------|
| **Data** | `/api/data` | CRUD for all entities |
| **Auth** | `/api/auth` | Login, register, logout, me |
| **Media** | `/api/media` | Upload, serve files |
| **Flows** | `/flow` | List, view, run flows |
| **Admin** | `/admin` | Admin UI |

## DOs and DON'Ts

**DO:**
- Use `bknd debug routes` to list all endpoints
- Check admin panel for visual schema exploration
- Use POST `/query` endpoint for complex filters
- Include Content-Type header on POST/PATCH
- Test endpoints with curl before implementing

**DON'T:**
- Forget `/api/` prefix on API paths
- Mix up entity names (case matters)
- Use GET for complex queries with nested operators
- Assume entity names - verify they exist first
- Forget auth strategy in login path (`/api/auth/password/login`)

## Related Skills

- **bknd-client-setup** - Set up SDK in frontend
- **bknd-crud-read** - Query data with filtering
- **bknd-custom-endpoint** - Create custom API endpoints
- **bknd-login-flow** - Implement authentication
- **bknd-local-setup** - Set up local development
