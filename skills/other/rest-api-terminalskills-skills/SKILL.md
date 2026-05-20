---
name: rest-api
description: >-
  Design and build RESTful APIs. Use when a user asks to create a REST API,
  design API endpoints, implement CRUD operations, add authentication to an API,
  handle pagination and filtering, set up API versioning, generate
  OpenAPI/Swagger docs, implement rate limiting, build middleware, handle file
  uploads, add CORS, implement HATEOAS, or structure an
  Express/Fastify/Koa/Flask/FastAPI backend. Covers HTTP methods, status codes,
  resource modeling, error handling, validation, and production deployment
  patterns.
license: Apache-2.0
compatibility: 'Node.js 18+ (Express, Fastify) or Python 3.9+ (FastAPI, Flask)'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - rest
    - api
    - express
    - fastapi
    - openapi
---

# REST API

## Overview

Design and build production-grade RESTful APIs following industry conventions. This skill covers resource modeling, HTTP semantics, authentication, validation, pagination, versioning, documentation, error handling, and security — with examples in Express (Node.js) and FastAPI (Python).

## Instructions

### Step 1: Project Setup

**Express:**
```bash
npm install express cors helmet morgan compression zod jsonwebtoken bcrypt swagger-jsdoc swagger-ui-express
```

**FastAPI:**
```bash
pip install "fastapi[standard]" uvicorn sqlalchemy pydantic-settings python-jose[cryptography] passlib[bcrypt]
```

### Step 2: Resource Design

```
Resource        Endpoint                    Methods
Users           /api/v1/users               GET, POST
User            /api/v1/users/:id           GET, PUT, PATCH, DELETE
User Posts      /api/v1/users/:id/posts     GET
Posts           /api/v1/posts               GET, POST
Post Comments   /api/v1/posts/:id/comments  GET, POST
```

Rules: plural nouns (`/users`), no verbs in URLs, max 2 nesting levels, kebab-case (`/user-profiles`).

### Step 3: HTTP Methods and Status Codes

```
Method   Purpose          Success Code   Body
GET      Read             200 OK         Resource/collection
POST     Create           201 Created    Created resource + Location header
PUT      Full replace     200 OK         Updated resource
PATCH    Partial update   200 OK         Updated resource
DELETE   Remove           204 No Content (empty)

Key error codes: 400 (bad input), 401 (unauthenticated), 403 (forbidden),
404 (not found), 409 (conflict), 422 (validation), 429 (rate limited)
```

### Step 4: Express Implementation

```javascript
// src/app.js
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';

const app = express();
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') || '*' }));
app.use(express.json({ limit: '10kb' }));
app.use('/api/v1/users', usersRouter);
app.get('/health', (req, res) => res.json({ status: 'ok' }));
app.use(notFound);
app.use(errorHandler);
```

```javascript
// src/routes/users.js — validation with Zod
import { Router } from 'express';
import { z } from 'zod';

const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    name: z.string().min(2).max(100),
    password: z.string().min(8).max(128),
  }),
});

router.get('/',       authenticate, validate(listSchema), usersController.list);
router.post('/',      validate(createUserSchema),          usersController.create);
router.get('/:id',    authenticate,                        usersController.getOne);
router.patch('/:id',  authenticate, validate(updateSchema), usersController.update);
router.delete('/:id', authenticate, authorize('admin'),    usersController.remove);
```

```javascript
// src/controllers/users.js
export async function list(req, res) {
  const { page, limit, sort, search } = req.query;
  const [users, total] = await Promise.all([
    db.user.findMany({ where: search ? { name: { contains: search } } : {}, skip: (page - 1) * limit, take: limit }),
    db.user.count(),
  ]);
  res.json({ data: users, meta: { page, limit, total, totalPages: Math.ceil(total / limit) } });
}

export async function create(req, res) {
  const existing = await db.user.findUnique({ where: { email: req.body.email } });
  if (existing) throw new AppError(409, 'Email already registered');
  const user = await db.user.create({ data: { ...req.body, password: await hashPassword(req.body.password) } });
  res.status(201).location(`/api/v1/users/${user.id}`).json({ data: user });
}
```

### Step 5: Middleware (Auth, Validation, Errors)

```javascript
// Auth
export function authenticate(req, res, next) {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) throw new AppError(401, 'Missing token');
  try { req.user = jwt.verify(header.slice(7), process.env.JWT_SECRET); next(); }
  catch { throw new AppError(401, 'Invalid token'); }
}

// Validation
export function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse({ body: req.body, query: req.query, params: req.params });
    if (!result.success) throw new AppError(400, 'Validation failed', result.error.issues);
    Object.assign(req, result.data);
    next();
  };
}

// Error handler
export function errorHandler(err, req, res, next) {
  const status = err.statusCode || 500;
  res.status(status).json({
    error: { code: err.code || 'INTERNAL_ERROR', message: status === 500 ? 'Internal server error' : err.message },
  });
}
```

### Step 6: FastAPI Implementation

```python
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="My API", version="1.0.0", docs_url="/api/docs")

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: str; email: str; name: str; created_at: datetime
    model_config = {"from_attributes": True}

router = APIRouter()

@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), db=Depends(get_db)):
    users, total = await user_service.get_many(db, page=page, limit=limit)
    return {"data": users, "meta": {"page": page, "limit": limit, "total": total}}

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(body: UserCreate, db=Depends(get_db)):
    existing = await user_service.get_by_email(db, body.email)
    if existing: raise HTTPException(409, "Email already registered")
    return await user_service.create(db, body)

app.include_router(router, prefix="/api/v1/users", tags=["users"])
```

### Step 7: Pagination and Filtering

**Offset-based:** `GET /api/v1/posts?page=2&limit=20` — returns `{ data, meta: { page, limit, total, totalPages } }`

**Cursor-based:** `GET /api/v1/posts?cursor=eyJpZCI6MTAwfQ&limit=20` — returns `{ data, meta: { nextCursor, hasMore } }`

Common query params: `sort=-createdAt,title`, `fields=id,title`, `search=keyword`, `status=active`, `createdAfter=2024-01-01`.

## Examples

### Example 1: Build a CRUD API for a project management app
**User prompt:** "Create a REST API with Express for managing projects and tasks. Include JWT authentication, input validation, and paginated list endpoints."

The agent will:
1. Set up Express with `helmet`, `cors`, `compression`, and JSON body parsing
2. Define routes: `GET/POST /api/v1/projects`, `GET/PATCH/DELETE /api/v1/projects/:id`, `GET/POST /api/v1/projects/:id/tasks`
3. Create Zod schemas for `createProject` and `updateProject` input validation
4. Implement JWT authentication middleware that extracts the user from the Bearer token
5. Add paginated list endpoints returning `{ data, meta: { page, limit, total, totalPages } }`
6. Set up a global error handler returning `{ error: { code, message } }` with proper HTTP status codes

### Example 2: Add FastAPI endpoints with auto-generated docs
**User prompt:** "Create a FastAPI backend for a blog with users and posts. I want automatic OpenAPI documentation and Pydantic validation."

The agent will:
1. Define Pydantic models: `UserCreate`, `UserResponse`, `PostCreate`, `PostResponse`, and `PaginatedResponse[T]`
2. Create routers for `/api/v1/users` and `/api/v1/posts` with proper HTTP methods and status codes
3. Add dependency injection for database sessions and current user authentication
4. FastAPI automatically generates interactive docs at `/api/docs` (Swagger UI) and `/api/redoc`
5. Implement proper error handling with `HTTPException` using correct status codes (409 for duplicate email, 404 for missing resources)

## Guidelines

1. **Consistent response format** — always wrap in `{ data: ... }` or `{ error: ... }`
2. **Validate all input** — never trust request body, query, or params
3. **Use proper status codes** — 201 for creation, 204 for delete, 409 for conflicts
4. **Include Location header** — on 201 responses, point to the created resource
5. **Pagination by default** — never return unbounded collections
6. **Rate limit everything** — stricter limits on auth endpoints
7. **CORS configured explicitly** — never use `*` in production
8. **Idempotent PUT/DELETE** — calling twice produces the same result
9. **Error responses include machine-readable codes** — `VALIDATION_FAILED`, not just messages
10. **Version from day one** — `/api/v1/` costs nothing and saves future pain
