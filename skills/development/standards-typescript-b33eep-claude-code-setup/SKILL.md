---
name: standards-typescript
description: This skill provides TypeScript coding standards and is automatically loaded for TypeScript projects. It includes naming conventions, best practices, and recommended tooling.
type: context
applies_to: [typescript, nodejs, express, nestjs, nextjs, react, vue, angular, deno, bun, zod]
file_extensions: [".ts", ".tsx", ".jsx"]
---

# TypeScript Coding Standards

## Core Principles

1. **Simplicity**: Simple, understandable code
2. **Readability**: Readability over cleverness
3. **Maintainability**: Code that's easy to maintain
4. **Testability**: Code that's easy to test
5. **DRY**: Don't Repeat Yourself - but don't overdo it

## General Rules

- **Early Returns**: Use early returns to avoid nesting
- **Descriptive Names**: Meaningful names for variables and functions
- **Minimal Changes**: Only change relevant code parts
- **No Over-Engineering**: No unnecessary complexity
- **Minimal Comments**: Code should be self-explanatory. No redundant comments!

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables/Functions | camelCase | `getUserById`, `isActive` |
| Classes/Interfaces/Types | PascalCase | `UserService`, `ApiClient` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private | Prefix with `_` or `#` | `_internalMethod`, `#privateField` |
| Files | kebab-case or camelCase | `user-service.ts`, `userService.ts` |
| Interfaces | No `I` prefix | `User` not `IUser` |
| Type aliases | PascalCase | `UserId`, `HttpMethod` |
| Event Handlers | Prefix with `handle` | `handleClick`, `handleSubmit` |

## Project Structure

```
myproject/
├── src/
│   ├── index.ts              # Entry point
│   ├── config.ts             # Settings, env vars
│   ├── types/
│   │   └── index.ts          # Shared types
│   ├── models/
│   │   └── user.ts           # Domain models
│   ├── services/
│   │   └── user-service.ts   # Business logic
│   ├── repositories/
│   │   └── user-repo.ts      # Data access
│   └── utils/
│       └── helpers.ts        # Utility functions
├── tests/
│   ├── services/
│   │   └── user-service.test.ts
│   └── setup.ts
├── package.json
├── tsconfig.json
└── README.md
```

## Code Style

```typescript
// Use explicit types for function parameters and return values
function getUserById(userId: string): User | undefined {
  if (!userId) {
    throw new Error("userId cannot be empty");
  }
  // implementation...
}

// Prefer interfaces for object shapes
interface User {
  id: string;
  name: string;
  email: string;
  age?: number;
}

// Use type aliases for unions, intersections, or primitives
type UserId = string;
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Result<T> = { success: true; data: T } | { success: false; error: string };
```

## Best Practices

```typescript
// Prefer const over let
const users: User[] = [];

// Use nullish coalescing and optional chaining
const name = user?.profile?.name ?? "Anonymous";

// Prefer template literals
const message = `Hello, ${user.name}!`;

// Use destructuring
const { id, name, email } = user;
function processUser({ id, name }: User): void { }

// Prefer array methods over loops
const activeUsers = users.filter(u => u.isActive);
const userNames = users.map(u => u.name);
const totalAge = users.reduce((sum, u) => sum + u.age, 0);

// Use readonly for immutable data
interface Config {
  readonly apiUrl: string;
  readonly maxRetries: number;
}

// Use as const for literal types
const DIRECTIONS = ["north", "south", "east", "west"] as const;
type Direction = typeof DIRECTIONS[number];

// Prefer unknown over any
function parseJson(input: string): unknown {
  return JSON.parse(input);
}

// Type guards for type narrowing
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null && "id" in value;
}
```

## Utility Types

```typescript
// Partial<T> - Make all properties optional
type UserUpdate = Partial<User>;
// { id?: string; name?: string; email?: string; age?: number }

// Pick<T, K> - Select specific properties
type UserPreview = Pick<User, "id" | "name">;
// { id: string; name: string }

// Omit<T, K> - Exclude specific properties
type UserWithoutEmail = Omit<User, "email">;
// { id: string; name: string; age?: number }

// Record<K, T> - Object with specific keys and value type
type RolePermissions = Record<"admin" | "user" | "guest", string[]>;
// { admin: string[]; user: string[]; guest: string[] }

// ReturnType<F> - Extract return type of function
type FetchResult = ReturnType<typeof fetchUser>;
// Promise<User | undefined>

// Parameters<F> - Extract parameter types
type FetchParams = Parameters<typeof fetchUser>;
// [userId: string]

// Awaited<T> - Unwrap Promise type
type ResolvedUser = Awaited<ReturnType<typeof fetchUser>>;
// User | undefined
```

## Discriminated Unions

```typescript
// Use a common "type" or "status" field as discriminator
type ApiResponse<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: string }
  | { status: "loading" };

function handleResponse(response: ApiResponse<User>) {
  switch (response.status) {
    case "success":
      console.log(response.data.name); // TypeScript knows data exists
      break;
    case "error":
      console.error(response.error); // TypeScript knows error exists
      break;
    case "loading":
      console.log("Loading...");
      break;
  }
}

// State machines with discriminated unions
type AuthState =
  | { state: "idle" }
  | { state: "loading" }
  | { state: "authenticated"; user: User }
  | { state: "error"; message: string };

// Action types for reducers
type UserAction =
  | { type: "SET_USER"; payload: User }
  | { type: "CLEAR_USER" }
  | { type: "UPDATE_NAME"; payload: string };
```

## Runtime Validation with Zod

```typescript
import { z } from "zod";

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

// Infer TypeScript type from schema
type User = z.infer<typeof UserSchema>;

// Validate data (throws on error)
const user = UserSchema.parse(untrustedData);

// Safe validation (returns result object)
const result = UserSchema.safeParse(untrustedData);
if (result.success) {
  console.log(result.data); // User
} else {
  console.error(result.error.issues);
}

// Common patterns
const ConfigSchema = z.object({
  apiUrl: z.string().url(),
  timeout: z.number().default(5000),
  retries: z.number().min(0).max(10).default(3),
});

// Transform and validate
const EmailSchema = z.string().email().transform((val) => val.toLowerCase());
```

## Async/Await

```typescript
// Async function with proper typing
async function fetchUser(userId: string): Promise<User | undefined> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) return undefined;
  return response.json() as Promise<User>;
}

// Use Promise.all for concurrent operations
async function fetchAllUsers(userIds: string[]): Promise<User[]> {
  const users = await Promise.all(userIds.map(fetchUser));
  return users.filter((user): user is User => user !== undefined);
}

// Handle errors with try/catch
async function safeFetch<T>(url: string): Promise<Result<T>> {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: String(error) };
  }
}
```

## Error Handling

```typescript
// Custom error classes for domain errors
class UserNotFoundError extends Error {
  constructor(public readonly userId: string) {
    super(`User not found: ${userId}`);
    this.name = "UserNotFoundError";
  }
}

// Strict vs optional returns
function getUserStrict(userId: string): User {
  const user = repository.get(userId);
  if (!user) throw new UserNotFoundError(userId);
  return user;
}

function getUserOptional(userId: string): User | undefined {
  return repository.get(userId);
}

// Result type for explicit error handling
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

## Comments - Less is More

```typescript
// BAD - redundant comment
// Get the user from database
const user = repository.getUser(userId);

// GOOD - self-explanatory code, no comment needed
const user = repository.getUser(userId);

// GOOD - comment explains WHY (not obvious)
// Rate limit: API allows max 1000 requests/min
await rateLimiter.acquire();
```

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `pnpm` or `bun` | Package manager (faster than npm) |
| `eslint` | Linting with TypeScript rules |
| `prettier` | Code formatting |
| `vitest` or `jest` | Testing framework |
| `tsx` or `ts-node` | TypeScript execution |
| `zod` | Runtime validation with type inference |

## tsconfig.json Recommendations

> **Note:** These are strict settings for new projects. For existing codebases, enable incrementally.

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true
  }
}
```

## Production Best Practices

1. **Strict mode** - Enable `strict: true` in tsconfig.json
2. **Explicit return types** - Always declare return types for public functions
3. **Avoid any** - Use `unknown` and type guards instead
4. **Readonly by default** - Use `readonly` and `as const` for immutable data
5. **Discriminated unions** - For state management and result types
6. **Dependency injection** - Pass dependencies explicitly
7. **Custom errors** - Domain-specific error classes
8. **Environment variables** - Type-safe config with validation (zod, env-var)
9. **Barrel exports** - Use index.ts for clean imports
10. **Path aliases** - Configure `@/` paths in tsconfig for cleaner imports

---

## References

- Utility Types, Discriminated Unions, and Zod sections inspired by [moai-lang-typescript](https://github.com/AJBcoding/claude-skill-eval/tree/main/skills/moai-lang-typescript) by AJBcoding
