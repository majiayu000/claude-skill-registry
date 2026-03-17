---
name: Next.js + FastAPI Full-Stack Expert
description: Expert guidance for building full-stack applications with Next.js frontend and FastAPI backend. Use when integrating React/Next.js with Python FastAPI, building API routes, or implementing SSR/SSG with Python backends.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Next.js + FastAPI Full-Stack Expert

Production patterns for integrating Next.js 14+ (App Router) with FastAPI backends.

## Architecture Patterns

### 1. Project Structure

```
project-root/
├── frontend/                 # Next.js app
│   ├── app/
│   │   ├── api/             # Next.js API routes (optional)
│   │   ├── (auth)/          # Route groups
│   │   └── layout.tsx
│   ├── components/
│   ├── lib/
│   │   ├── api-client.ts    # FastAPI client
│   │   └── types.ts
│   ├── next.config.js
│   └── package.json
├── backend/                 # FastAPI app
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/         # Pydantic models
│   │   └── services/
│   ├── requirements.txt
│   └── pyproject.toml
└── docker-compose.yml
```

### 2. FastAPI Backend Setup

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, items, auth
from .config import settings

app = FastAPI(
    title="API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(items.router, prefix="/api/items", tags=["items"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
```

```python
# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import User, UserCreate, UserUpdate
from ..services import user_service

router = APIRouter()

@router.get("/", response_model=list[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return user_service.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=User, status_code=201)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(db, user_in)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(UserBase):
    password: str | None = Field(None, min_length=8)

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

### 3. Next.js Frontend Setup

```typescript
// frontend/lib/api-client.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new APIError(response.status, error.detail);
  }

  return response.json();
}

export const api = {
  users: {
    list: (params?: { skip?: number; limit?: number }) =>
      fetchAPI<User[]>(`/api/users?${new URLSearchParams(params as any)}`),

    get: (id: number) =>
      fetchAPI<User>(`/api/users/${id}`),

    create: (data: UserCreate) =>
      fetchAPI<User>('/api/users', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    update: (id: number, data: UserUpdate) =>
      fetchAPI<User>(`/api/users/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
  },

  auth: {
    login: (credentials: { email: string; password: string }) =>
      fetchAPI<{ access_token: string }>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      }),

    logout: () =>
      fetchAPI('/api/auth/logout', { method: 'POST' }),

    me: () =>
      fetchAPI<User>('/api/auth/me'),
  },
};
```

```typescript
// frontend/lib/types.ts (generated from FastAPI schema)
export interface User {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string;
}

export interface UserCreate {
  email: string;
  full_name?: string;
  password: string;
  is_active?: boolean;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
}
```

### 4. Server Components with FastAPI

```tsx
// app/users/page.tsx (Server Component)
import { api } from '@/lib/api-client';
import { UsersList } from '@/components/users-list';

export default async function UsersPage() {
  const users = await api.users.list();

  return (
    <div>
      <h1>Users</h1>
      <UsersList users={users} />
    </div>
  );
}
```

```tsx
// app/users/[id]/page.tsx
interface Props {
  params: { id: string };
}

export async function generateMetadata({ params }: Props) {
  const user = await api.users.get(parseInt(params.id));
  return {
    title: `${user.full_name} - Users`,
  };
}

export default async function UserPage({ params }: Props) {
  const user = await api.users.get(parseInt(params.id));

  return (
    <div>
      <h1>{user.full_name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### 5. Client Components with React Query

```tsx
// components/users-list.tsx
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';

export function UsersList({ initialUsers }: { initialUsers: User[] }) {
  const queryClient = useQueryClient();

  const { data: users } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.users.list(),
    initialData: initialUsers,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.users.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>
          <span>{user.full_name}</span>
          <button onClick={() => deleteMutation.mutate(user.id)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}
```

### 6. Authentication Pattern

```python
# backend/app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

security = HTTPBearer()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_service.get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user
```

```typescript
// frontend/lib/auth.ts
import { cookies } from 'next/headers';

export async function getServerSession() {
  const token = cookies().get('access_token')?.value;

  if (!token) return null;

  try {
    const user = await fetch(`${API_URL}/api/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }).then(res => res.json());

    return user;
  } catch {
    return null;
  }
}

// middleware.ts
export async function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
```

### 7. Real-time with WebSockets

```python
# backend/app/websocket.py
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

```typescript
// frontend/hooks/use-websocket.ts
'use client';

import { useEffect, useRef, useState } from 'react';

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<string[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => setIsConnected(true);
    ws.current.onclose = () => setIsConnected(false);
    ws.current.onmessage = (event) => {
      setMessages(prev => [...prev, event.data]);
    };

    return () => ws.current?.close();
  }, [url]);

  const send = (message: string) => {
    ws.current?.send(message);
  };

  return { isConnected, messages, send };
}
```

### 8. File Uploads

```python
# backend/app/routers/upload.py
from fastapi import UploadFile, File
import aiofiles

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"

    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return {"filename": file.filename, "size": len(content)}
```

```tsx
// components/file-upload.tsx
'use client';

export function FileUpload() {
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    console.log('Uploaded:', data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button type="submit">Upload</button>
    </form>
  );
}
```

### 9. Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - FRONTEND_URL=http://localhost:3000
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      args:
        - NEXT_PUBLIC_API_URL=http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### 10. Type Safety with OpenAPI

```bash
# Generate TypeScript types from FastAPI OpenAPI schema
npx openapi-typescript http://localhost:8000/openapi.json -o lib/api-types.ts
```

```typescript
// lib/typed-api-client.ts
import type { paths } from './api-types';
import createClient from 'openapi-fetch';

export const client = createClient<paths>({
  baseUrl: 'http://localhost:8000',
});

// Type-safe API calls
const { data, error } = await client.GET('/api/users/{user_id}', {
  params: {
    path: { user_id: 123 },
  },
});
```

## Best Practices

✅ Use Server Components for initial data fetching
✅ Use React Query for client-side mutations
✅ Generate types from OpenAPI schema
✅ Implement proper CORS configuration
✅ Use HTTPOnly cookies for auth tokens
✅ Validate all inputs with Pydantic
✅ Use database migrations (Alembic)
✅ Implement rate limiting
✅ Add comprehensive error handling
✅ Use Docker for consistent environments

---

**When to Use:** Full-stack development with Next.js and FastAPI, API integration, SSR/SSG with Python backends.
