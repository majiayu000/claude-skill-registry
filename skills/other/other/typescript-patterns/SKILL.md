---
name: typescript-patterns
description: TypeScript best practices and patterns. Use when writing TypeScript code, defining types, working with generics, or converting JavaScript to TypeScript.
---

# TypeScript Patterns

## Strict Config (tsconfig.json)
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  }
}
```

## Type Patterns

### Discriminated Union (never use string + optional fields)
```typescript
// BAD
type ApiResponse = { success: boolean; data?: User; error?: string }

// GOOD
type ApiResponse =
  | { success: true; data: User }
  | { success: false; error: string }

function handle(res: ApiResponse) {
  if (res.success) {
    console.log(res.data.email)  // TypeScript knows data exists
  } else {
    console.error(res.error)     // TypeScript knows error exists
  }
}
```

### Generic Repository
```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>
  findAll(): Promise<T[]>
  create(data: Omit<T, 'id' | 'createdAt'>): Promise<T>
  update(id: ID, data: Partial<T>): Promise<T>
  delete(id: ID): Promise<void>
}
```

### Branded Types (prevent mixing IDs)
```typescript
type UserId = number & { readonly _brand: 'UserId' }
type PostId = number & { readonly _brand: 'PostId' }

const userId = 123 as UserId
const postId = 456 as PostId

function getUser(id: UserId): Promise<User> { ... }
getUser(postId)  // TypeScript error! Can't pass PostId as UserId
```

### Utility Types
```typescript
// Pick only what you need
type UserSummary = Pick<User, 'id' | 'name' | 'email'>

// Make all optional for updates
type UserUpdate = Partial<Pick<User, 'name' | 'email'>>

// Require specific fields
type UserCreate = Required<Pick<User, 'email' | 'password'>> & Partial<Pick<User, 'name'>>

// Readonly for immutable data
type Config = Readonly<{ apiUrl: string; timeout: number }>

// Record for maps
const rolePermissions: Record<UserRole, Permission[]> = { ... }
```

### Result Type (instead of throwing everywhere)
```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

async function safeParseJson<T>(text: string): Promise<Result<T>> {
  try {
    return { ok: true, value: JSON.parse(text) as T }
  } catch (e) {
    return { ok: false, error: e as Error }
  }
}
```

### Type Guards
```typescript
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null &&
    'id' in obj && 'email' in obj && typeof (obj as User).email === 'string'
}
```

## Rules
- Enable `strict: true` — never disable it for individual files
- Never use `any` — use `unknown` and narrow with type guards
- Prefer `interface` for object shapes, `type` for unions/intersections
- Use discriminated unions over optional fields
- Type return values of exported functions explicitly
- Use `as const` for literal arrays/objects that shouldn't be widened
- Avoid type assertions (`as X`) — use type guards instead
- Prefer `readonly` properties for data that shouldn't change
