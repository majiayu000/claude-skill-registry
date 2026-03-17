# 🔌 API Client Generator Skill

---
name: api-client-generator
description: Generate type-safe API clients from OpenAPI/Swagger specs or existing API endpoints
---

## 🎯 Purpose

สร้าง API client ที่ type-safe อัตโนมัติ จาก OpenAPI/Swagger specs หรือจาก API endpoints ที่มีอยู่

## 📋 When to Use

- เชื่อมต่อกับ API ใหม่
- อัพเดท API client หลัง spec เปลี่ยน
- สร้าง SDK จาก OpenAPI
- Generate types จาก API response

## 🔧 Generation Methods

### 1. From OpenAPI/Swagger Spec

```bash
# Using openapi-typescript
npx openapi-typescript ./api-spec.yaml -o ./types/api.ts

# Using swagger-typescript-api
npx swagger-typescript-api -p ./swagger.json -o ./api -n api.ts
```

### 2. From Existing Endpoints

```typescript
// Analyze endpoint and generate types
// GET /api/users → 
interface User {
  id: number;
  name: string;
  email: string;
}

// Generate client
async function getUsers(): Promise<User[]> {
  const response = await fetch('/api/users');
  return response.json();
}
```

## 📝 Generated Client Template

```typescript
// api/client.ts
const BASE_URL = process.env.API_URL || 'http://localhost:3000';

interface RequestConfig {
  headers?: Record<string, string>;
  params?: Record<string, string>;
}

class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;

  constructor(baseUrl: string = BASE_URL) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  setAuthToken(token: string) {
    this.defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: unknown,
    config?: RequestConfig
  ): Promise<T> {
    const url = new URL(endpoint, this.baseUrl);
    
    if (config?.params) {
      Object.entries(config.params).forEach(([key, value]) => {
        url.searchParams.set(key, value);
      });
    }

    const response = await fetch(url.toString(), {
      method,
      headers: { ...this.defaultHeaders, ...config?.headers },
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }

    return response.json();
  }

  // Generated methods
  users = {
    getAll: () => this.request<User[]>('GET', '/api/users'),
    getById: (id: string) => this.request<User>('GET', `/api/users/${id}`),
    create: (data: CreateUserDto) => this.request<User>('POST', '/api/users', data),
    update: (id: string, data: UpdateUserDto) => this.request<User>('PUT', `/api/users/${id}`, data),
    delete: (id: string) => this.request<void>('DELETE', `/api/users/${id}`),
  };
}

export const api = new ApiClient();
```

## 🔧 With React Query

```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.users.getAll(),
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => api.users.getById(id),
    enabled: !!id,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.users.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

## 📊 OpenAPI to Types Mapping

| OpenAPI Type | TypeScript Type |
|--------------|-----------------|
| `string` | `string` |
| `integer` | `number` |
| `number` | `number` |
| `boolean` | `boolean` |
| `array` | `T[]` |
| `object` | `interface` |
| `enum` | `enum` or union |

## 🔄 Auto-Generation Workflow

```
1. GET OpenAPI spec
   - Download from API endpoint
   - Or use local file

2. PARSE spec
   - Extract endpoints
   - Extract schemas
   - Extract parameters

3. GENERATE types
   - Create interfaces
   - Create enums
   - Create DTOs

4. GENERATE client
   - Create request methods
   - Add type annotations
   - Add error handling

5. ADD hooks (optional)
   - React Query hooks
   - SWR hooks
   - Custom hooks
```

## 📋 Generated Files Structure

```
api/
├── client.ts        # API client class
├── types/
│   ├── models.ts    # Data models
│   ├── requests.ts  # Request DTOs
│   └── responses.ts # Response DTOs
├── hooks/
│   ├── useUsers.ts  # User hooks
│   └── usePosts.ts  # Post hooks
└── index.ts         # Exports
```

## ✅ Generation Checklist

- [ ] All endpoints covered
- [ ] Types match API spec
- [ ] Error handling included
- [ ] Auth handling included
- [ ] Query params supported
- [ ] Request body typed
- [ ] Response typed
- [ ] Hooks generated (if needed)

## 🔗 Related Skills

- `type-generator` - Generate types from JSON
- `api-design` - Design APIs
- `testing` - Test API clients
