---
name: api-contract-sync
description: Use this skill when backend API contracts change and frontend types need synchronization. Triggers on: Pydantic model changes, REST endpoint updates, WebSocket message formats, or GraphQL schema modifications. Dynamically detects contract type from context. NOT for unrelated type definitions or internal backend-only changes.
---

# API Contract Sync

## Overview

Automatically detect and synchronize API contracts between backend and frontend when data structures, endpoints, or message formats change. Ensures type safety and prevents runtime errors from contract mismatches.

## Core Principle: Context-Driven Detection

This skill **does not assume** Pydantic ↔ TypeScript. It:
1. **Detects contract type** from project context (REST, WebSocket, GraphQL, gRPC)
2. **Identifies source of truth** (backend models, OpenAPI spec, GraphQL schema)
3. **Determines target** (TypeScript types, Zod schemas, client SDKs)
4. **Syncs appropriately** based on detected patterns

## When to Use

Invoke this skill when:
- **Backend model changes**: Pydantic models, SQLAlchemy models, dataclasses modified
- **Endpoint modifications**: New fields, renamed properties, changed response structure
- **Message format updates**: WebSocket events, SSE payloads, message queue schemas
- **API versioning**: New API version with breaking changes
- **Type drift detected**: Frontend using outdated or incorrect types

**DO NOT use** when:
- Internal backend types (not exposed via API)
- Frontend-only type definitions (UI state, component props)
- No communication between backend and frontend
- Types already synchronized manually

## Contract Detection Workflow

### Step 1: Identify Contract Type

Analyze project structure to determine contract mechanism:

**Detection heuristics:**

```python
# Check project files and structure
if exists("backend/app/models/*.py") and uses("pydantic"):
    contract_type = "Pydantic → TypeScript"
    source_files = glob("backend/app/models/*.py")
    target_files = glob("frontend/types/*.ts") or "frontend/src/types/"

elif exists("backend/schema.graphql"):
    contract_type = "GraphQL Schema → TypeScript"
    source_files = ["backend/schema.graphql"]
    target_files = ["frontend/generated/graphql.ts"]

elif exists("backend/openapi.json") or exists("backend/openapi.yaml"):
    contract_type = "OpenAPI → TypeScript"
    source_files = ["backend/openapi.json"]
    target_files = ["frontend/api/client.ts"]

elif exists("backend/app/websocket.py"):
    contract_type = "WebSocket Messages → TypeScript"
    source_files = ["backend/app/websocket.py"]  # Message definitions
    target_files = ["frontend/types/websocket.ts"]

else:
    contract_type = "Unknown - manual analysis required"
```

**Output contract type to user for confirmation** before proceeding.

### Step 2: Extract Backend Contract

Based on detected type, extract API contract:

#### Type A: Pydantic → TypeScript

**Source:** Pydantic models used in API responses

```python
# Example: backend/app/models/task.py
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime
```

**Extraction:** Parse Pydantic model fields and types

**Mapping:**
- `int` → `number`
- `str` → `string`
- `bool` → `boolean`
- `datetime` → `string` (ISO8601)
- `Optional[T]` → `T | null`
- `list[T]` → `T[]`

#### Type B: GraphQL Schema → TypeScript

**Source:** GraphQL schema file

```graphql
type Task {
  id: ID!
  title: String!
  completed: Boolean!
  createdAt: DateTime!
}
```

**Extraction:** Use GraphQL codegen or parse schema directly

**Tool:** `@graphql-codegen/cli` (if configured)

#### Type C: WebSocket Messages → TypeScript

**Source:** WebSocket message classes/types

```python
# backend/app/websocket.py
class NotificationEvent(BaseModel):
    type: Literal["notification"]
    message: str
    timestamp: datetime
    user_id: int
```

**Extraction:** Parse message definitions, create discriminated unions

#### Type D: OpenAPI → TypeScript

**Source:** OpenAPI spec (usually auto-generated from FastAPI)

```yaml
components:
  schemas:
    Task:
      type: object
      properties:
        id: { type: integer }
        title: { type: string }
        completed: { type: boolean }
```

**Extraction:** Use OpenAPI TypeScript generators

**Tool:** `openapi-typescript` or `swagger-typescript-api`

### Step 3: Generate Frontend Types

Based on contract type, generate appropriate frontend types:

#### For Pydantic → TypeScript (Manual)

```typescript
// frontend/types/task.ts
export interface Task {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;  // ISO8601 datetime
}

export interface TaskCreate {
  title: string;
  completed?: boolean;
}

export interface TaskUpdate {
  title?: string;
  completed?: boolean;
}
```

#### For GraphQL (Codegen)

```bash
# Use GraphQL Code Generator
npx graphql-codegen --config codegen.yml
```

Generates `frontend/generated/graphql.ts` automatically

#### For WebSocket Messages

```typescript
// frontend/types/websocket.ts
export type WebSocketMessage =
  | { type: "notification"; message: string; timestamp: string; user_id: number }
  | { type: "status_update"; status: string }
  | { type: "ping" };

export interface NotificationEvent {
  type: "notification";
  message: string;
  timestamp: string;
  user_id: number;
}
```

#### For OpenAPI (Codegen)

```bash
# Use OpenAPI TypeScript generator
npx openapi-typescript http://localhost:8000/openapi.json -o frontend/types/api.ts
```

### Step 4: Validate Synchronization

After sync, verify:

**Validation checklist:**
- [ ] All backend models used in API have corresponding frontend types
- [ ] Field names match exactly (or mapping documented)
- [ ] Data types are compatible (no `string` ↔ `number` mismatches)
- [ ] Optional/required fields match
- [ ] Nested types resolved correctly
- [ ] No circular dependencies in type definitions

**Validation methods:**

1. **Type-check frontend**: Run `tsc --noEmit` or `npm run typecheck`
2. **Runtime validation**: Use Zod or similar to validate API responses
3. **Integration tests**: Test actual API calls with typed responses

### Step 5: Handle Mismatches

When backend and frontend types diverge:

**Mismatch scenarios:**

1. **Breaking change**: Backend removed field frontend uses
   ```
   Solution: Version API (/v1 vs /v2) or add deprecated field temporarily
   ```

2. **Field renamed**: Backend `created_at` → `createdAt`
   ```
   Solution: Add alias in Pydantic model or transform in API layer
   ```

3. **Type changed**: `int` → `str` (e.g., ID changed to UUID)
   ```
   Solution: Breaking change - version API, update all consumers
   ```

4. **New required field**: Backend added required field
   ```
   Solution: Make optional temporarily, or provide default value
   ```

**Resolution workflow:**
```
Detect mismatch
↓
Assess impact (breaking vs non-breaking)
├─ Non-breaking (new optional field) → Add to frontend types
├─ Breaking (removed/changed field) → Version API or add migration path
└─ Critical (security/data integrity) → Block until resolved
```

## Contract Sync Patterns

### Pattern 1: Pydantic Models → TypeScript (Direct)

**When:** Simple FastAPI project, manual type management

**Workflow:**
1. Read Pydantic models in `backend/app/models/`
2. Generate equivalent TypeScript interfaces
3. Save to `frontend/types/`
4. Import in frontend code

**Example:**
```python
# backend/app/models/user.py
class User(BaseModel):
    id: int
    email: str
    role: Literal["admin", "user"]
```

→

```typescript
// frontend/types/user.ts
export interface User {
  id: number;
  email: string;
  role: "admin" | "user";
}
```

### Pattern 2: OpenAPI → TypeScript (Automated)

**When:** FastAPI auto-generates OpenAPI, want full automation

**Workflow:**
1. Start backend server (generates OpenAPI at `/openapi.json`)
2. Run `openapi-typescript` to generate types
3. Commit generated types to version control
4. CI/CD verifies no manual edits to generated files

**Setup:**
```json
// package.json
{
  "scripts": {
    "generate:api": "openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts"
  }
}
```

### Pattern 3: GraphQL Schema → TypeScript (Codegen)

**When:** Using GraphQL, schema-first approach

**Workflow:**
1. Define GraphQL schema in `backend/schema.graphql`
2. Run GraphQL Code Generator
3. Use generated types + hooks in React components

**Config:**
```yaml
# codegen.yml
schema: http://localhost:8000/graphql
generates:
  frontend/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
```

### Pattern 4: WebSocket Messages → Discriminated Unions

**When:** Real-time features with multiple message types

**Workflow:**
1. Define message types in backend (Pydantic models)
2. Create TypeScript discriminated union
3. Use type guards for runtime type narrowing

**Backend:**
```python
class PingMessage(BaseModel):
    type: Literal["ping"] = "ping"

class NotificationMessage(BaseModel):
    type: Literal["notification"] = "notification"
    message: str
    user_id: int

WebSocketMessage = PingMessage | NotificationMessage
```

**Frontend:**
```typescript
export type WebSocketMessage =
  | { type: "ping" }
  | { type: "notification"; message: string; user_id: number };

function handleMessage(msg: WebSocketMessage) {
  if (msg.type === "notification") {
    // TypeScript knows msg has message and user_id here
    console.log(msg.message);
  }
}
```

## Automation Strategies

### Strategy 1: Pre-commit Hook

Generate types before every commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash
npm run generate:api
git add frontend/types/
```

### Strategy 2: CI/CD Validation

Verify types are synchronized:

```yaml
# .github/workflows/type-check.yml
- name: Generate API types
  run: npm run generate:api

- name: Check for drift
  run: |
    git diff --exit-code frontend/types/
    # Fails if generated types differ from committed
```

### Strategy 3: Development Watch Mode

Auto-regenerate on backend changes:

```json
// package.json
{
  "scripts": {
    "dev": "concurrently \"backend\" \"npm run watch:types\"",
    "watch:types": "nodemon --watch backend/app/models --exec 'npm run generate:api'"
  }
}
```

## Advanced Topics

### Handling Nested Types

**Backend:**
```python
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    id: int
    address: Address
```

**Frontend:**
```typescript
export interface Address {
  street: string;
  city: string;
}

export interface User {
  id: number;
  address: Address;  // Nested type
}
```

### Handling Generics

**Backend:**
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
```

**Frontend:**
```typescript
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
}

// Usage
type TasksPage = PaginatedResponse<Task>;
```

### Handling Enums

**Backend:**
```python
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
```

**Frontend:**
```typescript
export enum TaskStatus {
  TODO = "todo",
  IN_PROGRESS = "in_progress",
  DONE = "done",
}

// Or as union type
export type TaskStatus = "todo" | "in_progress" | "done";
```

## Anti-Patterns

- **Manual duplication**: Retyping backend models manually (error-prone)
- **Ignoring mismatches**: Frontend types drift from backend reality
- **Over-engineering**: Creating complex mapping layers for simple projects
- **No validation**: Trusting types without runtime checks
- **Hardcoded types**: Not using contract as single source of truth

## Examples

### Example 1: Pydantic Model Change

**Scenario:** Added `priority` field to Task model

**Backend change:**
```python
class Task(BaseModel):
    id: int
    title: str
    completed: bool
    priority: Literal["low", "medium", "high"] = "medium"  # NEW
```

**Sync action:**
```typescript
// frontend/types/task.ts
export interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: "low" | "medium" | "high";  // ADDED
}
```

**Verification:** `tsc --noEmit` passes ✓

### Example 2: WebSocket Message Addition

**Scenario:** Added new `task_updated` event

**Backend:**
```python
class TaskUpdatedEvent(BaseModel):
    type: Literal["task_updated"] = "task_updated"
    task_id: int
    updated_fields: dict[str, Any]
```

**Frontend:**
```typescript
export type WebSocketMessage =
  | { type: "ping" }
  | { type: "notification"; message: string }
  | { type: "task_updated"; task_id: number; updated_fields: Record<string, any> }; // NEW
```

### Example 3: Breaking Change (Field Removed)

**Scenario:** Removed `completed` field, replaced with `status`

**Backend:**
```python
class Task(BaseModel):
    id: int
    title: str
    status: Literal["todo", "in_progress", "done"]  # Replaces 'completed'
```

**Sync strategy:**
1. **Immediate**: Add migration - keep `completed` as computed property
   ```python
   @property
   def completed(self) -> bool:
       return self.status == "done"
   ```

2. **Gradual**: Version API (/v1 has `completed`, /v2 has `status`)

3. **Breaking**: Update all frontend consumers, remove old field

## Integration with Other Skills

- **parallel-coordinator**: Ensures backend and frontend agents sync types
- **fastapi-backend-expert**: Generates Pydantic models this skill syncs
- **React Frontend Expert (F1)**: Consumes synced types in components
- **artifact-aggregator**: Documents contract changes in reports

## Notes

- Contract type detection is context-driven, not hardcoded
- Prefer automation (OpenAPI codegen) over manual sync for large projects
- Always validate sync with type checker + runtime validation (Zod)
- Breaking changes require API versioning or careful migration
- Keep generated types in version control for audit trail
