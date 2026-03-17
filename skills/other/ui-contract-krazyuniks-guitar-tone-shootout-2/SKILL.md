---
name: ui-contract
description: Frontend/backend API contract definitions. Use for defining API endpoints, Pydantic to TypeScript mapping, schema validation, error responses, and pagination contracts.
---

# UI Contract Skill

**Activation:** API contract, Pydantic schema, TypeScript types, response format, error contract, pagination, frontend/backend interface

## Overview

Define and maintain API contracts between FastAPI backend and React frontend. Ensures type safety and consistent data shapes across the stack.

## Pydantic to TypeScript Mapping

### Basic Types

| Pydantic | TypeScript |
|----------|------------|
| `str` | `string` |
| `int` | `number` |
| `float` | `number` |
| `bool` | `boolean` |
| `datetime` | `string` (ISO 8601) |
| `date` | `string` (YYYY-MM-DD) |
| `UUID` | `string` |
| `list[T]` | `T[]` |
| `dict[str, T]` | `Record<string, T>` |
| `T | None` | `T \| null` |
| `Literal["a", "b"]` | `"a" \| "b"` |
| `Enum` | Union of string literals |

### Complex Mapping Examples

```python
# apps/webapp/src/webapp/schemas/shootout.py
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Literal
from enum import Enum

class ShootoutStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ShootoutBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    is_public: bool = False

class ShootoutCreate(ShootoutBase):
    signal_chain_ids: list[UUID]

class ShootoutRead(ShootoutBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: ShootoutStatus
    created_at: datetime
    updated_at: datetime
```

```typescript
// astro/src/types/shootout.ts
export type ShootoutStatus = "draft" | "processing" | "completed" | "failed";

export interface ShootoutBase {
  title: string;
  description: string | null;
  is_public: boolean;
}

export interface ShootoutCreate extends ShootoutBase {
  signal_chain_ids: string[];
}

export interface ShootoutRead extends ShootoutBase {
  id: string;
  user_id: string;
  status: ShootoutStatus;
  created_at: string;
  updated_at: string;
}
```

## Standard Response Contracts

### Success Response (Single Item)

```python
# backend
@router.get("/{id}", response_model=ShootoutRead)
async def get_shootout(id: UUID) -> Shootout:
    ...
```

```typescript
// frontend
const shootout: ShootoutRead = await fetchJSON<ShootoutRead>(`/shootouts/${id}`);
```

### Success Response (List with Pagination)

```python
# apps/webapp/src/webapp/schemas/common.py
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int
    has_more: bool

# Usage
class ShootoutListResponse(PaginatedResponse[ShootoutRead]):
    pass
```

```typescript
// astro/src/types/common.ts
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

// Usage
type ShootoutListResponse = PaginatedResponse<ShootoutRead>;
```

### Error Response Contract

```python
# apps/webapp/src/webapp/schemas/error.py
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    field: str | None = None
    message: str

class ErrorResponse(BaseModel):
    error: str
    code: str
    details: list[ErrorDetail] | None = None

# Standard error codes
class ErrorCode:
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    CONFLICT = "conflict"
    INTERNAL_ERROR = "internal_error"
```

```typescript
// astro/src/types/error.ts
export interface ErrorDetail {
  field: string | null;
  message: string;
}

export interface ErrorResponse {
  error: string;
  code: string;
  details?: ErrorDetail[];
}

export const ErrorCode = {
  NOT_FOUND: "not_found",
  VALIDATION_ERROR: "validation_error",
  UNAUTHORIZED: "unauthorized",
  FORBIDDEN: "forbidden",
  CONFLICT: "conflict",
  INTERNAL_ERROR: "internal_error",
} as const;
```

## API Error Handling

### Backend: Consistent Error Responses

```python
# apps/webapp/src/webapp/api/deps.py
from fastapi import HTTPException, status
from webapp.schemas.error import ErrorResponse, ErrorCode

def raise_not_found(resource: str, id: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorResponse(
            error=f"{resource} not found",
            code=ErrorCode.NOT_FOUND,
        ).model_dump(),
    )

def raise_forbidden(message: str = "Access denied") -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ErrorResponse(
            error=message,
            code=ErrorCode.FORBIDDEN,
        ).model_dump(),
    )

# Usage in route
@router.get("/{id}")
async def get_shootout(id: UUID, current_user: User) -> Shootout:
    shootout = await db.get(Shootout, id)
    if not shootout:
        raise_not_found("Shootout", str(id))
    if shootout.user_id != current_user.id:
        raise_forbidden()
    return shootout
```

### Frontend: Typed Error Handling

```typescript
// astro/src/lib/api.ts
import { ErrorResponse, ErrorCode } from '../types/error';

export class APIError extends Error {
  constructor(
    public status: number,
    public response: ErrorResponse,
  ) {
    super(response.error);
    this.name = 'APIError';
  }

  get isNotFound(): boolean {
    return this.response.code === ErrorCode.NOT_FOUND;
  }

  get isUnauthorized(): boolean {
    return this.response.code === ErrorCode.UNAUTHORIZED;
  }

  get validationErrors(): Record<string, string> {
    if (!this.response.details) return {};
    return Object.fromEntries(
      this.response.details
        .filter((d) => d.field)
        .map((d) => [d.field!, d.message])
    );
  }
}

export async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { credentials: 'include' });

  if (!res.ok) {
    const error = await res.json();
    throw new APIError(res.status, error);
  }

  return res.json();
}
```

## Pagination Contract

### Query Parameters

```python
# apps/webapp/src/webapp/schemas/common.py
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class SortParams(BaseModel):
    sort_by: str = "created_at"
    sort_order: Literal["asc", "desc"] = "desc"
```

```typescript
// astro/src/types/common.ts
export interface PaginationParams {
  limit?: number;  // default: 20, max: 100
  offset?: number; // default: 0
}

export interface SortParams {
  sort_by?: string;  // default: "created_at"
  sort_order?: "asc" | "desc";  // default: "desc"
}
```

### Usage in API

```python
# apps/webapp/src/webapp/api/shootouts.py
@router.get("/", response_model=ShootoutListResponse)
async def list_shootouts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ShootoutListResponse:
    query = select(Shootout).where(Shootout.user_id == current_user.id)

    # Apply sorting
    order_column = getattr(Shootout, sort_by, Shootout.created_at)
    query = query.order_by(
        order_column.desc() if sort_order == "desc" else order_column.asc()
    )

    # Get total count
    total = await db.scalar(select(func.count()).select_from(query.subquery()))

    # Apply pagination
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return ShootoutListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
        has_more=offset + len(items) < total,
    )
```

```typescript
// astro/src/lib/hooks/useShootouts.ts
export function useShootouts(params: PaginationParams & SortParams = {}) {
  const searchParams = new URLSearchParams();
  if (params.limit) searchParams.set("limit", String(params.limit));
  if (params.offset) searchParams.set("offset", String(params.offset));
  if (params.sort_by) searchParams.set("sort_by", params.sort_by);
  if (params.sort_order) searchParams.set("sort_order", params.sort_order);

  return useQuery({
    queryKey: ["shootouts", params],
    queryFn: () =>
      fetchJSON<ShootoutListResponse>(`/shootouts?${searchParams}`),
  });
}
```

## Filter Contract

```python
# apps/webapp/src/webapp/schemas/shootout.py
class ShootoutFilters(BaseModel):
    status: ShootoutStatus | None = None
    is_public: bool | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    search: str | None = Field(default=None, max_length=100)
```

```typescript
// astro/src/types/shootout.ts
export interface ShootoutFilters {
  status?: ShootoutStatus;
  is_public?: boolean;
  created_after?: string;  // ISO 8601
  created_before?: string; // ISO 8601
  search?: string;
}
```

## WebSocket Contract

```python
# apps/webapp/src/webapp/schemas/ws.py
from pydantic import BaseModel
from typing import Literal

class WSMessage(BaseModel):
    type: Literal["progress", "error", "complete"]
    job_id: str
    data: dict

class ProgressData(BaseModel):
    progress: int  # 0-100
    stage: str
    message: str | None = None

class ErrorData(BaseModel):
    error: str
    code: str

class CompleteData(BaseModel):
    result_url: str
    duration_ms: int
```

```typescript
// astro/src/types/ws.ts
export type WSMessageType = "progress" | "error" | "complete";

export interface WSMessage {
  type: WSMessageType;
  job_id: string;
  data: ProgressData | ErrorData | CompleteData;
}

export interface ProgressData {
  progress: number;  // 0-100
  stage: string;
  message?: string;
}

export interface ErrorData {
  error: string;
  code: string;
}

export interface CompleteData {
  result_url: string;
  duration_ms: number;
}
```

## Contract Validation Pattern

### Type Guard for Runtime Validation

```typescript
// astro/src/types/guards.ts
import { ShootoutRead, ShootoutStatus } from './shootout';

export function isShootoutRead(obj: unknown): obj is ShootoutRead {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof (obj as ShootoutRead).id === 'string' &&
    typeof (obj as ShootoutRead).title === 'string' &&
    isShootoutStatus((obj as ShootoutRead).status)
  );
}

function isShootoutStatus(value: unknown): value is ShootoutStatus {
  return ['draft', 'processing', 'completed', 'failed'].includes(value as string);
}
```

### Zod Schema (Alternative)

```typescript
// astro/src/schemas/shootout.ts
import { z } from 'zod';

export const ShootoutStatusSchema = z.enum([
  'draft',
  'processing',
  'completed',
  'failed',
]);

export const ShootoutReadSchema = z.object({
  id: z.string().uuid(),
  user_id: z.string().uuid(),
  title: z.string().min(1).max(200),
  description: z.string().nullable(),
  is_public: z.boolean(),
  status: ShootoutStatusSchema,
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type ShootoutRead = z.infer<typeof ShootoutReadSchema>;
```

## Quick Reference

| Backend (Pydantic) | Frontend (TypeScript) |
|--------------------|----------------------|
| `BaseModel` | `interface` |
| `Field(min_length=1)` | Manual or Zod validation |
| `response_model=X` | Return type `Promise<X>` |
| `HTTPException` | `throw new APIError()` |
| Query params | URLSearchParams |
| `list[T]` | `T[]` |
| `T | None` | `T \| null` |
| Enum | Union of string literals |

## Example Contract Definition

When defining a new API endpoint:

1. **Backend Schema** (Pydantic)
```python
# apps/webapp/src/webapp/schemas/{entity}.py
class {Entity}Create(BaseModel): ...
class {Entity}Read(BaseModel): ...
class {Entity}Update(BaseModel): ...
class {Entity}ListResponse(PaginatedResponse[{Entity}Read]): ...
```

2. **Frontend Types** (TypeScript)
```typescript
// astro/src/types/{entity}.ts
export interface {Entity}Create { ... }
export interface {Entity}Read { ... }
export interface {Entity}Update { ... }
export type {Entity}ListResponse = PaginatedResponse<{Entity}Read>;
```

3. **API Hook** (TanStack Query)
```typescript
// astro/src/lib/hooks/use{Entity}.ts
export function use{Entity}(id: string) { ... }
export function use{Entity}List(params: PaginationParams) { ... }
export function useCreate{Entity}() { ... }
```
