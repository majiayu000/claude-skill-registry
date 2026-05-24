---
name: TypeScript Type Safety Expert
description: Expert guidance for advanced TypeScript type safety, generics, type inference, and compile-time validation. Use when implementing complex type systems, improving type safety, or eliminating runtime errors.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
---

# TypeScript Type Safety Expert

Advanced TypeScript patterns for bulletproof type safety.

## Advanced Type Patterns

### Branded Types

```typescript
// Prevent mixing incompatible types
type Brand<K, T> = K & { __brand: T };

type UserId = Brand<string, 'UserId'>;
type ProductId = Brand<string, 'ProductId'>;

const userId = 'user_123' as UserId;
const productId = 'prod_456' as ProductId;

function getUser(id: UserId) { /* ... */ }

getUser(userId);      // ✅ OK
getUser(productId);   // ❌ Type error!
```

### Discriminated Unions

```typescript
type Success<T> = { success: true; data: T };
type Error = { success: false; error: string };
type Result<T> = Success<T> | Error;

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    // TypeScript knows result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows result.error exists
    console.error(result.error);
  }
}
```

### Template Literal Types

```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Route = `/${string}`;
type Endpoint = `${HttpMethod} ${Route}`;

const endpoint: Endpoint = 'GET /users';  // ✅
const invalid: Endpoint = 'FETCH /data'; // ❌ Type error

// Dynamic key generation
type EventName = `on${Capitalize<string>}`;
const onClick: EventName = 'onClick';  // ✅
const invalid: EventName = 'click';    // ❌
```

### Recursive Types

```typescript
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };

const validJSON: JSONValue = {
  name: "Alice",
  age: 30,
  tags: ["developer", "typescript"],
  metadata: {
    created: "2024-01-01",
    nested: {
      deep: true
    }
  }
};
```

### Utility Type Combinations

```typescript
// Make all properties optional recursively
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Make specific keys required
type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Exclude null and undefined
type NonNullableKeys<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};

// Extract function parameters
type Params<T extends (...args: any) => any> = T extends (...args: infer P) => any ? P : never;
```

### Type-Safe API Client

```typescript
type API = {
  '/users': {
    GET: { response: User[] };
    POST: { body: UserCreate; response: User };
  };
  '/users/:id': {
    GET: { params: { id: string }; response: User };
    PUT: { params: { id: string }; body: UserUpdate; response: User };
    DELETE: { params: { id: string }; response: void };
  };
};

type ExtractParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractParams<Rest>]: string }
    : T extends `${infer _}:${infer Param}`
    ? { [K in Param]: string }
    : {};

async function apiCall<
  Path extends keyof API,
  Method extends keyof API[Path]
>(
  method: Method,
  path: Path,
  options?: API[Path][Method] extends { body: infer B }
    ? { body: B; params?: ExtractParams<Path> }
    : { params?: ExtractParams<Path> }
): Promise<API[Path][Method] extends { response: infer R } ? R : never> {
  // Implementation
  return {} as any;
}

// Usage - fully type-safe!
const user = await apiCall('GET', '/users/:id', {
  params: { id: '123' }  // ✅ Required
});

const newUser = await apiCall('POST', '/users', {
  body: { email: 'test@test.com', name: 'Test' }  // ✅ Required
});
```

### Builder Pattern with Type State

```typescript
class QueryBuilder<T extends Record<string, any>, HasWhere = false> {
  private whereClause?: string;

  where<K extends keyof T>(key: K, value: T[K]): QueryBuilder<T, true> {
    this.whereClause = `${String(key)} = ${value}`;
    return this as any;
  }

  // execute() only available after where() is called
  execute(this: QueryBuilder<T, true>): Promise<T[]> {
    return Promise.resolve([]);
  }
}

const query = new QueryBuilder<User>();
query.execute();  // ❌ Type error - must call where() first
query.where('id', 123).execute();  // ✅ OK
```

### Strict Event Emitter

```typescript
type EventMap = {
  'user:created': { id: string; name: string };
  'user:deleted': { id: string };
  'data:update': { data: any[] };
};

class TypedEventEmitter<T extends Record<string, any>> {
  private listeners: {
    [K in keyof T]?: Array<(data: T[K]) => void>;
  } = {};

  on<K extends keyof T>(event: K, callback: (data: T[K]) => void) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(callback);
  }

  emit<K extends keyof T>(event: K, data: T[K]) {
    this.listeners[event]?.forEach(cb => cb(data));
  }
}

const emitter = new TypedEventEmitter<EventMap>();

emitter.on('user:created', (data) => {
  console.log(data.id, data.name);  // ✅ Fully typed
});

emitter.emit('user:created', { id: '1', name: 'Alice' });  // ✅ OK
emitter.emit('user:created', { wrong: 'data' });  // ❌ Type error
```

### Zod Integration

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(0).max(150),
  role: z.enum(['admin', 'user', 'guest']),
  metadata: z.record(z.unknown()).optional(),
});

type User = z.infer<typeof UserSchema>;

// Runtime validation with compile-time types
function validateUser(data: unknown): User {
  return UserSchema.parse(data);
}
```

## TSConfig Best Practices

```json
{
  "compilerOptions": {
    "strict": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noFallthroughCasesInSwitch": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}
```

## Quick Patterns

```typescript
// Const assertions
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
// Type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }

// Satisfies operator
const colors = {
  red: [255, 0, 0],
  green: [0, 255, 0],
} satisfies Record<string, [number, number, number]>;

// Index signatures with template literals
type HTTPHeaders = {
  [K in `x-${string}`]: string;
};

// Conditional types
type IsArray<T> = T extends any[] ? true : false;
type Test1 = IsArray<string[]>;  // true
type Test2 = IsArray<string>;    // false
```

---

**When to Use:** Advanced TypeScript features, eliminating runtime errors, type-safe APIs, complex type systems.
