---
name: service-layer
description: 'Service 层架构与前后端联调规范。Use when creating API services, writing Service
  classes, or handling backend integration. Triggers on: creating services, API calls,
  BaseService pattern, rewrites configuration, er'
---

---
name: service-layer
description: Service 层架构与前后端联调规范。Use when creating API services, writing Service classes, or handling backend integration. Triggers on: creating services, API calls, BaseService pattern, rewrites configuration, error handling.
---

# Service Layer Guide

Service 层架构与前后端联调规范。

## Directory Structure

```
lib/services/
├── core/
│   ├── api-client.ts
│   ├── base.service.ts
│   └── errors.ts
├── auth/
│   ├── auth.service.ts
│   └── types.ts
├── user/
│   ├── user.service.ts
│   └── types.ts
└── index.ts
```

## Service Pattern

```typescript
export class UserService extends BaseService {
  protected static readonly basePath = '/api/v1/users';

  static async list(): Promise<User[]> {
    return this.get<User[]>('/');
  }

  static async getById({ id }: { id: string }): Promise<User> {
    return this.get<User>(`/${id}`);
  }

  static async create(request: CreateUserRequest): Promise<User> {
    return this.post<User>('/', request);
  }
}
```

## Usage

```typescript
// ✅ Through services
import services from '@/lib/services';
const users = await services.user.list();

// ❌ Direct axios/fetch
await axios.get('http://localhost:8000/api/users');
```

## Rewrites Configuration

```typescript
// next.config.ts
async rewrites() {
  return [{
    source: '/api/:path*',
    destination: `${process.env.BACKEND_URL}/api/:path*`,
  }];
}
```

## Error Types

```typescript
ApiErrorBase
├── NetworkError      // Network issues
├── UnauthorizedError // 401
├── ForbiddenError    // 403
├── NotFoundError     // 404
├── ValidationError   // 400
└── ServerError       // 5xx
```

## Error Handling

```typescript
try {
  const user = await services.user.getById({ id });
} catch (error) {
  if (error instanceof NotFoundError) {
    toast.error('User not found');
  }
}
```
