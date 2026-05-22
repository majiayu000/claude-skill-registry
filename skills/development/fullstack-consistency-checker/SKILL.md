---
name: "Full-Stack Consistency Checker"
description: "Ensure frontend API calls match backend endpoints and types align when generating full-stack code"
version: "1.0.0"
---

# Full-Stack Consistency Checker Skill

## Purpose

Automatically verify and ensure consistency between frontend and backend implementations, checking that API contracts match, types align, and data flows correctly across the full stack when generating code for the Phase II todo application.

## When This Skill Triggers

Use this skill when the user asks to:
- "Check if frontend and backend are in sync"
- "Verify API contracts match"
- "Make sure types are consistent"
- "Generate full-stack code"
- "Review the implementation for consistency"
- After generating both frontend and backend code
- Before deployment or major integration

## Prerequisites

Before checking consistency:
1. Both `backend/` and `frontend/` directories exist
2. Backend has FastAPI routers defined
3. Frontend has API client or fetch calls
4. TypeScript interfaces exist in frontend
5. Pydantic schemas exist in backend

## Step-by-Step Procedure

### Step 1: Identify Integration Points

Scan for:
- Backend API endpoints (FastAPI routes)
- Frontend API calls (fetch, axios)
- Data models (SQLModel, Pydantic, TypeScript interfaces)
- Authentication flows
- Error handling patterns

### Step 2: Check API Endpoint Consistency

**What to Verify:**
- Endpoint URLs match between frontend and backend
- HTTP methods are correct (GET, POST, PUT, DELETE)
- Request body structure matches expected schema
- Response structure matches return types
- Query parameters align
- Headers (Authorization, Content-Type) are consistent

**Example Check:**

**Backend Endpoint:**
```python
# app/routers/todos.py
@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Implementation
```

**Frontend Call:**
```typescript
// lib/api.ts
export async function createTodo(data: TodoFormData): Promise<Todo> {
  const response = await fetch('http://localhost:8000/todos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to create todo');
  }

  return response.json();
}
```

**Consistency Checks:**
- ✅ URL: `/todos` matches backend route
- ✅ Method: POST matches `@router.post`
- ✅ Auth: Authorization header present (backend has `Depends(get_current_user)`)
- ✅ Content-Type: application/json (backend expects JSON)
- ⚠️ **Check Types:** TodoFormData should match TodoCreate schema

### Step 3: Verify Type Alignment

**Backend Pydantic Schema:**
```python
# app/schemas/todo.py
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    tags: list[str] = Field(default_factory=list)
```

**Frontend TypeScript Interface:**
```typescript
// types/todo.ts
export interface TodoFormData {
  title: string;              // ✅ Matches: str (required)
  description?: string;       // ✅ Matches: Optional[str]
  priority?: 'low' | 'medium' | 'high';  // ✅ Matches: enum pattern
  tags?: string[];            // ✅ Matches: list[str]
}
```

**Automated Comparison:**
| Field | Backend Type | Frontend Type | Match | Notes |
|-------|-------------|---------------|-------|-------|
| title | str (required) | string | ✅ | |
| description | Optional[str] | string \| undefined | ✅ | |
| priority | str (enum) | 'low' \| 'medium' \| 'high' | ✅ | |
| tags | list[str] | string[] | ✅ | |

### Step 4: Check Response Type Consistency

**Backend Response Model:**
```python
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: list[str]
    user_id: int
    created_at: datetime
    updated_at: datetime
```

**Frontend Interface:**
```typescript
export interface Todo {
  id: number;                 // ✅ Matches: int
  title: string;              // ✅ Matches: str
  description: string | null; // ✅ Matches: Optional[str]
  completed: boolean;         // ✅ Matches: bool
  priority: 'low' | 'medium' | 'high';  // ✅ Matches
  tags: string[];             // ✅ Matches: list[str]
  user_id: number;            // ✅ Matches: int
  created_at: string;         // ⚠️ Backend: datetime, Frontend: string (OK if serialized)
  updated_at: string;         // ⚠️ Same as above
}
```

**Note:** `datetime` fields are serialized to ISO 8601 strings in JSON, so `string` type in TypeScript is correct.

### Step 5: Verify Query Parameters

**Backend:**
```python
@router.get("/")
async def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
```

**Frontend:**
```typescript
export async function getTodos(params?: {
  skip?: number;
  limit?: number;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high';
  search?: string;
}): Promise<Todo[]> {
  const queryParams = new URLSearchParams();
  if (params?.skip !== undefined) queryParams.set('skip', params.skip.toString());
  if (params?.limit !== undefined) queryParams.set('limit', params.limit.toString());
  if (params?.completed !== undefined) queryParams.set('completed', params.completed.toString());
  if (params?.priority) queryParams.set('priority', params.priority);
  if (params?.search) queryParams.set('search', params.search);

  const response = await fetch(`http://localhost:8000/todos?${queryParams}`);
  return response.json();
}
```

**Consistency Check:**
- ✅ All query params match
- ✅ Types align (number, boolean, string)
- ✅ Optional parameters handled correctly

### Step 6: Check Error Handling Consistency

**Backend Errors:**
```python
# 401 Unauthorized
raise HTTPException(status_code=401, detail="Invalid credentials")

# 404 Not Found
raise HTTPException(status_code=404, detail="Todo not found")

# 400 Bad Request
raise HTTPException(status_code=400, detail="Email already registered")
```

**Frontend Error Handling:**
```typescript
try {
  const response = await fetch('/api/todos', {...});

  if (response.status === 401) {
    // Redirect to login
    router.push('/login');
  }

  if (response.status === 404) {
    throw new Error('Todo not found');
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
} catch (error) {
  console.error('API error:', error);
  throw error;
}
```

**Consistency Check:**
- ✅ Frontend handles 401 (redirects to login)
- ✅ Frontend handles 404 (shows error)
- ✅ Frontend extracts `detail` field from error response

### Step 7: Generate Consistency Report

Create a report identifying:
1. **Matching Endpoints** ✅
2. **Mismatched Endpoints** ⚠️
3. **Type Mismatches** ⚠️
4. **Missing Error Handling** ⚠️
5. **Suggestions for Fixes** 💡

**Example Report:**

```markdown
# Full-Stack Consistency Report

## ✅ Passing Checks (8/10)

### API Endpoints
- ✅ POST /todos - Create todo (types match)
- ✅ GET /todos - List todos (query params match)
- ✅ GET /todos/{id} - Get single todo
- ✅ PUT /todos/{id} - Update todo
- ✅ DELETE /todos/{id} - Delete todo
- ✅ POST /auth/login - Login endpoint
- ✅ POST /auth/register - Registration

### Type Alignment
- ✅ TodoFormData ↔ TodoCreate schema
- ✅ Todo interface ↔ TodoResponse schema

## ⚠️ Issues Found (2)

### 1. Missing Frontend Error Handling
**Location:** `lib/api.ts:45` - `updateTodo()`
**Issue:** No handling for 403 Forbidden (user trying to update another user's todo)
**Fix:**
```typescript
if (response.status === 403) {
  throw new Error('You do not have permission to update this todo');
}
```

### 2. Type Mismatch in Filter Component
**Location:** `components/TodoFilters.tsx:22`
**Issue:** Priority type is `string` but should be `'low' | 'medium' | 'high'`
**Current:**
```typescript
const [priority, setPriority] = useState<string>('');
```
**Fix:**
```typescript
const [priority, setPriority] = useState<'low' | 'medium' | 'high' | ''>('');
```

## 💡 Recommendations

1. **Add Response Type Validation**
   - Use Zod or similar library to validate API responses match expected types
   - Example:
     ```typescript
     import { z } from 'zod';

     const TodoSchema = z.object({
       id: z.number(),
       title: z.string(),
       completed: z.boolean(),
       // ... other fields
     });

     const data = await response.json();
     const validatedTodo = TodoSchema.parse(data); // Throws if mismatch
     ```

2. **Centralize API Base URL**
   - Replace hardcoded `http://localhost:8000` with environment variable
   - Create `lib/config.ts`:
     ```typescript
     export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
     ```

3. **Generate TypeScript Types from Backend**
   - Consider using tools like `openapi-typescript` to auto-generate types from FastAPI's OpenAPI schema
   - Command: `npx openapi-typescript http://localhost:8000/openapi.json -o types/api.ts`

4. **Add Integration Tests**
   - Test full flow: Frontend → Backend → Database
   - Ensure contracts stay in sync

## Summary

**Overall Status:** 🟡 Good (80% consistent)
**Critical Issues:** 0
**Warnings:** 2
**Suggestions:** 4

All critical endpoints and types are aligned. Minor issues found in error handling and type strictness.
```

### Step 8: Auto-Fix Simple Issues

For simple issues, automatically suggest fixes:

**Issue: Missing Authorization Header**
```typescript
// Before (WRONG - missing auth)
export async function getTodos() {
  const response = await fetch('http://localhost:8000/todos');
  return response.json();
}

// After (FIXED - added auth)
export async function getTodos() {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/todos', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (response.status === 401) {
    window.location.href = '/login';
  }
  return response.json();
}
```

## Output Format

### Consistency Report Structure
```
reports/
└── fullstack-consistency-report.md
    ├── Summary (pass/fail counts)
    ├── Passing Checks
    ├── Issues Found (with locations)
    ├── Recommendations
    └── Auto-Fix Suggestions
```

### Check Categories

1. **Endpoint Matching** (High Priority)
   - URL paths match
   - HTTP methods correct
   - Required headers present

2. **Type Consistency** (High Priority)
   - Request types match schemas
   - Response types match models
   - Enums align

3. **Error Handling** (Medium Priority)
   - All HTTP status codes handled
   - Error messages displayed to user
   - Fallback behaviors exist

4. **Authentication** (Critical Priority)
   - Protected endpoints require tokens
   - Tokens sent in correct format
   - Token refresh implemented

## Quality Criteria

**Completeness:**
- ✅ All backend endpoints have frontend implementations
- ✅ All frontend API calls have corresponding backend routes
- ✅ All data models defined in both layers

**Correctness:**
- ✅ Types align exactly (no implicit conversions)
- ✅ Required fields are required in both layers
- ✅ Optional fields are optional in both layers

**Security:**
- ✅ Protected endpoints require authentication
- ✅ User isolation enforced
- ✅ HTTPS in production

## Examples

### Example 1: Detect Missing Endpoint

**Frontend Call:**
```typescript
// frontend/lib/api.ts
export async function batchDeleteTodos(ids: number[]) {
  await fetch('/todos/batch/delete', {
    method: 'DELETE',
    body: JSON.stringify({ ids }),
  });
}
```

**Backend Routes:**
```python
# app/routers/todos.py
# (No batch delete endpoint exists)
```

**Report:**
```
⚠️ Missing Backend Endpoint
- Frontend calls: DELETE /todos/batch/delete
- Backend: Endpoint not found
- Suggestion: Add batch delete endpoint to todos.py
```

### Example 2: Type Mismatch Detection

**Backend:**
```python
class TodoCreate(BaseModel):
    title: str
    due_date: Optional[datetime] = None  # NEW FIELD
```

**Frontend:**
```typescript
interface TodoFormData {
  title: string;
  // Missing: due_date field
}
```

**Report:**
```
⚠️ Type Mismatch: TodoFormData
- Backend has field: due_date (Optional[datetime])
- Frontend missing: due_date
- Suggestion: Add to TodoFormData:
  due_date?: string; // ISO 8601 date string
```

## Success Indicators

The skill execution is successful when:
- ✅ All endpoints verified to match
- ✅ All type mismatches identified
- ✅ Report generated with actionable fixes
- ✅ Critical issues (auth, security) flagged
- ✅ Auto-fix suggestions provided where applicable
- ✅ Integration points documented
- ✅ Developer can quickly fix all issues
