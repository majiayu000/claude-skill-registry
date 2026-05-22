---
name: typescript-pro
description: Expert TypeScript developer specializing in advanced type system features, generic programming, and type-safe application architecture. This agent excels at leveraging TypeScript 5+ features for building robust, maintainable applications with comprehensive type safety and excellent developer experience.
---

# TypeScript Pro Specialist

## Purpose

Provides expert TypeScript development capabilities with advanced type system features, generic programming patterns, and type-safe application architecture. Specializes in leveraging TypeScript 5+ for building robust, maintainable applications with comprehensive type safety.

## When to Use

- Designing complex type systems with advanced generics and mapped types
- Implementing type-safe APIs across frontend-backend boundaries
- Migrating JavaScript codebases to TypeScript gradually
- Troubleshooting complex type errors or inference issues
- Building type-safe libraries, SDKs, or framework integrations
- Optimizing TypeScript build performance in large projects
- Creating branded types, discriminated unions, and utility types

## Quick Start

**Invoke this skill when:**
- Designing complex type systems with advanced generics and mapped types
- Implementing type-safe APIs across frontend-backend boundaries
- Migrating JavaScript codebases to TypeScript gradually
- Troubleshooting complex type errors or inference issues
- Building type-safe libraries, SDKs, or framework integrations

**Do NOT invoke when:**
- Simple JavaScript tasks (type annotations not needed)
- Runtime logic bugs (use debugger instead)
- Build configuration only (use build-engineer instead)
- React/Vue-specific patterns (use react-specialist/vue-expert)

---
---

## Core Workflows

### Workflow 1: Design Type-Safe API Client

**Use case:** Create fully type-safe REST API client with auto-completion

**Steps:**

**1. Define API Schema (Contract-First)**
```typescript
// api-schema.ts - Single source of truth for API contract
export const apiSchema = {
  '/users': {
    GET: {
      query: {} as { page?: number; limit?: number },
      response: {} as { users: User[]; total: number }
    },
    POST: {
      body: {} as { email: string; name: string },
      response: {} as { id: string; email: string; name: string }
    }
  },
  '/users/{id}': {
    GET: {
      params: {} as { id: string },
      response: {} as User
    },
    PUT: {
      params: {} as { id: string },
      body: {} as Partial<User>,
      response: {} as User
    },
    DELETE: {
      params: {} as { id: string },
      response: {} as { success: boolean }
    }
  },
  '/posts': {
    GET: {
      query: {} as { author_id?: string; tags?: string[] },
      response: {} as { posts: Post[]; next_cursor?: string }
    }
  }
} as const;

// Extract types from schema
type ApiSchema = typeof apiSchema;
type ApiPaths = keyof ApiSchema;
type ApiMethods<Path extends ApiPaths> = keyof ApiSchema[Path];

// Helper types for type-safe request/response
type RequestParams<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { params: infer P } ? P : never;

type RequestQuery<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { query: infer Q } ? Q : never;

type RequestBody<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { body: infer B } ? B : never;

type ResponseData<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { response: infer R } ? R : never;
```

**2. Implement Type-Safe API Client**
```typescript
// api-client.ts
class ApiClient {
  constructor(private baseUrl: string) {}

  async request<
    Path extends ApiPaths,
    Method extends ApiMethods<Path>
  >(
    path: Path,
    method: Method,
    options?: {
      params?: RequestParams<Path, Method>;
      query?: RequestQuery<Path, Method>;
      body?: RequestBody<Path, Method>;
    }
  ): Promise<ResponseData<Path, Method>> {
    // Replace path parameters: /users/{id} → /users/123
    let url = path as string;
    if (options?.params) {
      Object.entries(options.params).forEach(([key, value]) => {
        url = url.replace(`{${key}}`, String(value));
      });
    }

    // Append query parameters
    if (options?.query) {
      const queryString = new URLSearchParams(
        options.query as Record<string, string>
      ).toString();
      url += `?${queryString}`;
    }

    // Make request
    const response = await fetch(`${this.baseUrl}${url}`, {
      method: method as string,
      headers: {
        'Content-Type': 'application/json',
      },
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }
}

// Usage with full type safety and auto-completion
const api = new ApiClient('https://api.example.com');

// GET /users?page=1&limit=10
const usersResponse = await api.request('/users', 'GET', {
  query: { page: 1, limit: 10 }  // Type-checked!
});
usersResponse.users[0].email;  // ✅ Auto-complete works!

// POST /users
const newUser = await api.request('/users', 'POST', {
  body: { email: 'test@example.com', name: 'Test' }  // Type-checked!
});
newUser.id;  // ✅ Type: string

// PUT /users/{id}
const updatedUser = await api.request('/users/{id}', 'PUT', {
  params: { id: '123' },  // Type-checked!
  body: { name: 'Updated Name' }  // Partial<User> type-checked!
});

// TypeScript errors for invalid usage:
api.request('/users', 'GET', {
  query: { invalid: true }  // ❌ Error: Object literal may only specify known properties
});

api.request('/users/{id}', 'PUT', {
  // ❌ Error: params required for this path
  body: { name: 'Test' }
});
```

**3. Add Runtime Validation with Zod**
```typescript
import { z } from 'zod';

// Define Zod schemas for runtime validation
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  created_at: z.string().datetime()
});

type User = z.infer<typeof UserSchema>;  // TypeScript type from Zod schema

// Enhanced API client with runtime validation
class ValidatedApiClient extends ApiClient {
  async request<
    Path extends ApiPaths,
    Method extends ApiMethods<Path>
  >(
    path: Path,
    method: Method,
    options?: {
      params?: RequestParams<Path, Method>;
      query?: RequestQuery<Path, Method>;
      body?: RequestBody<Path, Method>;
      responseSchema?: z.ZodSchema<ResponseData<Path, Method>>;
    }
  ): Promise<ResponseData<Path, Method>> {
    const response = await super.request(path, method, options);

    // Runtime validation if schema provided
    if (options?.responseSchema) {
      return options.responseSchema.parse(response);
    }

    return response;
  }
}

// Usage with runtime validation
const validatedApi = new ValidatedApiClient('https://api.example.com');

const user = await validatedApi.request('/users/{id}', 'GET', {
  params: { id: '123' },
  responseSchema: UserSchema  // Runtime validation!
});
// If API returns invalid data, Zod throws detailed error
```

---
---

### Workflow 3: Gradual TypeScript Migration

**Use case:** Migrate large JavaScript codebase incrementally

**Phase 1: Enable TypeScript with Zero Changes (Week 1)**
```json
// tsconfig.json - Initial configuration
{
  "compilerOptions": {
    "allowJs": true,          // Allow .js files
    "checkJs": false,         // Don't check .js files yet
    "noEmit": true,           // Don't output files (just check)
    "skipLibCheck": true,     // Skip type checking of .d.ts files
    "esModuleInterop": true,
    "moduleResolution": "node",
    "target": "ES2017",
    "module": "commonjs"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Phase 2: Add JSDoc Type Hints (Weeks 2-4)**
```javascript
// user.js - Add JSDoc comments for type checking
/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} email
 * @property {string} name
 */

/**
 * Fetch user by ID
 * @param {string} userId
 * @returns {Promise<User>}
 */
async function getUserById(userId) {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

/**
 * @param {User[]} users
 * @param {string} searchTerm
 * @returns {User[]}
 */
function filterUsers(users, searchTerm) {
  return users.filter(u => u.name.includes(searchTerm));
}
```

**Phase 3: Enable checkJs Gradually (Weeks 5-8)**
```json
// tsconfig.json - Start checking JavaScript
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,  // ✅ Enable type checking for .js files
    "noEmit": true
  }
}
```

**Fix errors directory by directory:**
```bash
# Disable checkJs for specific files with errors
// @ts-nocheck at top of file

# Or suppress specific errors
// @ts-ignore
const result = unsafeOperation();
```

**Phase 4: Rename Files to TypeScript (Weeks 9-12)**
```bash
# Rename .js → .ts one directory at a time
mv src/utils/user.js src/utils/user.ts

# Update imports (no file extensions in TypeScript)
- import { getUserById } from './user.js'
+ import { getUserById } from './user'
```

**Add explicit types:**
```typescript
// user.ts - Full TypeScript with explicit types
interface User {
  id: string;
  email: string;
  name: string;
  created_at: Date;
}

async function getUserById(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

function filterUsers(users: User[], searchTerm: string): User[] {
  return users.filter(u => u.name.includes(searchTerm));
}
```

**Phase 5: Enable Strict Mode (Weeks 13-16)**
```json
// tsconfig.json - Enable strict mode progressively
{
  "compilerOptions": {
    "strict": true,  // Enable all strict checks
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true
  }
}
```

**Fix strict mode errors:**
```typescript
// Before (implicit any)
function processData(data) {  // ❌ Parameter 'data' implicitly has 'any' type
  return data.map(item => item.value);
}

// After (explicit types)
function processData(data: Array<{ value: number }>): number[] {
  return data.map(item => item.value);
}

// Before (null not handled)
function getUserName(user: User) {  // ❌ User might be null
  return user.name;
}

// After (null handled)
function getUserName(user: User | null): string {
  return user?.name ?? 'Unknown';
}
```

---
---

### Pattern 2: Template Literal Types for String Validation

**When to use:** CSS class names, API routes, environment variables

```typescript
// Type-safe CSS class names
type Size = 'sm' | 'md' | 'lg';
type Color = 'red' | 'blue' | 'green';
type ClassName = `btn-${Size}-${Color}`;

function createButton(className: ClassName) {
  return `<button class="${className}"></button>`;
}

createButton('btn-md-blue');  // ✅ Valid
createButton('btn-xl-yellow');  // ❌ Error: Not assignable to ClassName

// Type-safe environment variables
type Stage = 'dev' | 'staging' | 'prod';
type Region = 'us' | 'eu' | 'asia';
type Environment = `${Stage}_${Region}`;

const env: Environment = 'prod_us';  // ✅ Valid
const invalid: Environment = 'production_us';  // ❌ Error
```

---
---

### ❌ Anti-Pattern 2: Not Defining Return Types

**What it looks like:**
```typescript
function getUser(id: string) {  // ❌ No return type
  return fetch(`/api/users/${id}`).then(r => r.json());
}
// Return type inferred as Promise<any>
```

**Why it fails:**
- Return type changes silently if implementation changes
- No guarantee of what function returns
- Harder to catch breaking changes

**Correct approach:**
```typescript
interface User {
  id: string;
  email: string;
  name: string;
}

function getUser(id: string): Promise<User> {  // ✅ Explicit return type
  return fetch(`/api/users/${id}`).then(r => r.json());
}
```

---
---

## Integration Patterns

### typescript-pro ↔ react-specialist
- **Handoff**: TypeScript pro defines types → React specialist uses in components
- **Collaboration**: Shared type definitions for props, state, API contracts
- **Tools**: TypeScript for types, React for UI logic

### typescript-pro ↔ backend-developer
- **Handoff**: TypeScript pro designs API types → Backend implements matching types
- **Collaboration**: Shared schema definitions (OpenAPI, tRPC, GraphQL)
- **Shared responsibility**: End-to-end type safety

### typescript-pro ↔ nextjs-developer
- **Handoff**: TypeScript types → Next.js App Router Server/Client Components
- **Collaboration**: Server Actions types, API route types
- **Dependency**: Next.js benefits heavily from TypeScript

---
