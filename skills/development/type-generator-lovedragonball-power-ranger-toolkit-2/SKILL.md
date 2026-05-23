# 📝 Type Generator Skill

---
name: type-generator
description: Generate TypeScript types and interfaces from JSON data, API responses, or database schemas
---

## 🎯 Purpose

สร้าง TypeScript types และ interfaces อัตโนมัติจาก JSON data, API responses, หรือ database schemas

## 📋 When to Use

- ได้รับ JSON response จาก API
- ต้องการ types จาก database schema
- Convert JSON to TypeScript
- Sync types กับ backend

## 🔧 Generation Methods

### 1. From JSON Data

```json
// Input JSON
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "isActive": true,
  "roles": ["admin", "user"],
  "profile": {
    "avatar": "https://...",
    "bio": "Developer"
  }
}
```

```typescript
// Generated TypeScript
interface User {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
  roles: string[];
  profile: {
    avatar: string;
    bio: string;
  };
}
```

### 2. From API Response

```typescript
// Fetch and analyze
const response = await fetch('/api/users/1');
const data = await response.json();

// Generate type
type UserResponse = typeof data;
// or more precisely:
interface UserResponse {
  // ... inferred types
}
```

### 3. From Database Schema (Prisma)

```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}
```

```typescript
// Generated types (prisma generate)
interface User {
  id: number;
  email: string;
  name: string | null;
  posts: Post[];
  createdAt: Date;
}
```

## 📝 Type Generation Rules

### Primitive Inference
| JSON Value | TypeScript Type |
|------------|-----------------|
| `"string"` | `string` |
| `123` | `number` |
| `true/false` | `boolean` |
| `null` | `null` |
| `[]` | `T[]` (infer T) |
| `{}` | `interface/type` |

### Special Cases
| JSON Pattern | TypeScript |
|--------------|------------|
| `"2024-01-15"` | `string` (or `Date` with annotation) |
| `["a", 1]` | `(string \| number)[]` |
| Optional field | `field?: Type` |
| Mixed null | `Type \| null` |

## 🔧 Advanced Generation

### Union Types from Values
```typescript
// If JSON has limited values
{ "status": "active" } // or "inactive", "pending"

// Generate union
type Status = 'active' | 'inactive' | 'pending';
```

### Generic Types
```typescript
// API Response wrapper
interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// Usage
type UserResponse = ApiResponse<User>;
type UsersResponse = ApiResponse<User[]>;
```

### Partial and Required
```typescript
// From full type
interface User {
  id: number;
  name: string;
  email: string;
}

// Generate create DTO (without id)
type CreateUserDto = Omit<User, 'id'>;

// Generate update DTO (all optional)
type UpdateUserDto = Partial<CreateUserDto>;
```

## 📋 Generation Template

```typescript
// types/user.ts

// Base interface
export interface User {
  id: number;
  name: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

// Create DTO (for POST)
export type CreateUserDto = Omit<User, 'id' | 'createdAt' | 'updatedAt'>;

// Update DTO (for PATCH)
export type UpdateUserDto = Partial<CreateUserDto>;

// List response
export interface UserListResponse {
  data: User[];
  total: number;
  page: number;
  limit: number;
}

// Query params
export interface UserQueryParams {
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: keyof User;
  order?: 'asc' | 'desc';
}
```

## 🛠️ Tools

### Online
- [quicktype.io](https://quicktype.io) - JSON to types
- [transform.tools](https://transform.tools) - Multiple formats

### CLI
```bash
# quicktype
npx quicktype sample.json -o types.ts

# json-schema-to-typescript
npx json-schema-to-typescript schema.json > types.ts
```

### VS Code
- JSON to TS extension
- Paste JSON as Code

## ✅ Type Quality Checklist

- [ ] All fields typed correctly
- [ ] Optional fields marked with `?`
- [ ] Nullable fields have `| null`
- [ ] Arrays properly typed
- [ ] Nested objects as interfaces
- [ ] Enums for fixed values
- [ ] DTOs for API calls
- [ ] Exported for use

## 🔗 Related Skills

- `api-client-generator` - Generate API clients
- `graphql-development` - GraphQL types
- `database-management` - Database schema types
