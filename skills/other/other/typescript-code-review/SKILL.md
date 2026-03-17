---
name: typescript-code-review
description: Master TypeScript code review patterns including type safety, null handling, discriminated unions, generic types, and async error handling. Use PROACTIVELY when reviewing TypeScript PRs.
---

# TypeScript Code Review

Comprehensive code review checklist and patterns for TypeScript applications, focusing on type safety, null handling, and proper TypeScript idioms.

## When to Use This Skill

- Reviewing TypeScript pull requests
- Establishing TypeScript code review standards
- Training reviewers on TypeScript-specific issues
- Catching type safety issues and anti-patterns
- Ensuring proper async/await patterns

## Quick Checklist

```markdown
## TypeScript Review Checklist

- [ ] No `any` types (use `unknown` if truly unknown)
- [ ] Null safety with optional chaining and nullish coalescing
- [ ] Discriminated unions for variant types
- [ ] Error types properly narrowed in catch blocks
- [ ] External data validated before type assertion
- [ ] Generic types for reusable functions
- [ ] Strict mode enabled in tsconfig
- [ ] No type assertions without validation
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Type Safety

### Avoiding `any`

```typescript
// ❌ Using any defeats TypeScript's purpose
function processData(data: any) {
  return data.value.nested.property; // No type checking!
}

// ✅ Use proper types
interface DataPayload {
  value: {
    nested: {
      property: string;
    };
  };
}

function processData(data: DataPayload): string {
  return data.value.nested.property; // Type checked!
}
```

### Using `unknown` Instead of `any`

```typescript
// ❌ any allows unsafe operations
function handleResponse(data: any): string {
  return data.toUpperCase(); // No error, but might crash!
}

// ✅ unknown requires type checking
function handleResponse(data: unknown): string {
  if (typeof data === "string") {
    return data.toUpperCase(); // Safe!
  }
  throw new Error("Expected string");
}
```

### Type Assertions Without Validation

```typescript
// ❌ Type assertion without validation - dangerous!
const user = JSON.parse(response) as User;
console.log(user.email); // Could be undefined!

// ✅ Validate external data with schema
import { z } from "zod";

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

const user = UserSchema.parse(JSON.parse(response));
console.log(user.email); // Guaranteed to exist!
```

### DOM Element Assertions

```typescript
// ❌ Unsafe type assertion
const element = document.getElementById("app") as HTMLDivElement;
element.innerHTML = "Hello"; // Could be null!

// ✅ Handle null case properly
const element = document.getElementById("app");
if (element instanceof HTMLDivElement) {
  element.innerHTML = "Hello";
}

// ✅ Or with non-null assertion when you're certain
const element = document.getElementById("app")!;
if (element) {
  element.innerHTML = "Hello";
}
```

---

## Null Safety

### Optional Chaining

```typescript
// ❌ Multiple nested checks
function getUserName(user: User | null): string {
  if (user) {
    if (user.profile) {
      if (user.profile.name) {
        return user.profile.name;
      }
    }
  }
  return "Anonymous";
}

// ✅ Optional chaining
function getUserName(user: User | null): string {
  return user?.profile?.name ?? "Anonymous";
}
```

### Nullish Coalescing

```typescript
// ❌ Logical OR treats 0 and '' as falsy
function getCount(count: number | null): number {
  return count || 10; // 0 becomes 10!
}

// ✅ Nullish coalescing only checks null/undefined
function getCount(count: number | null): number {
  return count ?? 10; // 0 stays 0
}
```

### Non-Null Assertion Abuse

```typescript
// ❌ Overusing non-null assertion
function processUser(user: User | null) {
  console.log(user!.name); // Crashes if null!
  console.log(user!.email!.toLowerCase()); // Double danger!
}

// ✅ Proper null handling
function processUser(user: User | null) {
  if (!user) {
    throw new Error("User is required");
  }
  // TypeScript now knows user is not null
  console.log(user.name);
  console.log(user.email?.toLowerCase() ?? "No email");
}
```

---

## Discriminated Unions

### Unsafe Union Handling

```typescript
// ❌ String union with unclear handling
type Status = 'loading' | 'success' | 'error';

interface ApiState {
    status: Status;
    data?: User[];
    error?: Error;
}

function handleState(state: ApiState) {
    if (state.status === 'success') {
        console.log(state.data);  // Could still be undefined!
    }
}

// ✅ Discriminated unions with type narrowing
type ApiState =
    | { status: 'loading' }
    | { status: 'success'; data: User[] }
    | { status: 'error'; error: Error };

function handleState(state: ApiState) {
    switch (state.status) {
        case 'loading':
            return <Spinner />;
        case 'success':
            return <UserList users={state.data} />;  // data guaranteed!
        case 'error':
            return <ErrorMessage error={state.error} />;  // error guaranteed!
    }
}
```

### Exhaustive Checking

```typescript
// ✅ Ensure all cases handled with never
function handleState(state: ApiState): JSX.Element {
    switch (state.status) {
        case 'loading':
            return <Spinner />;
        case 'success':
            return <UserList users={state.data} />;
        case 'error':
            return <ErrorMessage error={state.error} />;
        default:
            // TypeScript error if new status added but not handled
            const _exhaustive: never = state;
            throw new Error(`Unhandled status: ${_exhaustive}`);
    }
}
```

---

## Error Handling

### Untyped Catch Blocks

```typescript
// ❌ Untyped catch block (error is 'unknown' in strict mode)
try {
  await fetchUser(id);
} catch (error) {
  console.log(error.message); // Error: 'error' is of type 'unknown'
}

// ✅ Properly typed error handling
try {
  await fetchUser(id);
} catch (error: unknown) {
  if (error instanceof Error) {
    console.log(error.message);
  } else {
    console.log("Unknown error occurred");
  }
}
```

### Error Type Narrowing

```typescript
// ✅ Create type guard for custom errors
class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
  ) {
    super(message);
  }
}

function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}

try {
  await fetchUser(id);
} catch (error: unknown) {
  if (isApiError(error)) {
    console.log(`API Error ${error.statusCode}: ${error.message}`);
  } else if (error instanceof Error) {
    console.log(`Error: ${error.message}`);
  } else {
    console.log("Unknown error");
  }
}
```

### Missing Async Error Handling

```typescript
// ❌ Missing error handling in async
async function fetchData(): Promise<Data> {
  const response = await fetch("/api/data");
  return response.json(); // What if fetch fails? What if not ok?
}

// ✅ Complete error handling
async function fetchData(): Promise<Data> {
  const response = await fetch("/api/data");

  if (!response.ok) {
    throw new ApiError(
      `HTTP ${response.status}: ${response.statusText}`,
      response.status,
    );
  }

  const data: unknown = await response.json();
  return DataSchema.parse(data); // Validate the response
}
```

---

## Generic Types

### Type-Specific Functions

```typescript
// ❌ Duplicated functions for different types
async function fetchUsers(): Promise<User[]> {
  const response = await fetch("/api/users");
  return response.json();
}

async function fetchProducts(): Promise<Product[]> {
  const response = await fetch("/api/products");
  return response.json();
}

// ✅ Generic function
async function fetchData<T>(url: string, schema: z.ZodType<T>): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new ApiError(`HTTP ${response.status}`, response.status);
  }
  const data: unknown = await response.json();
  return schema.parse(data);
}

// Usage
const users = await fetchData("/api/users", z.array(UserSchema));
const products = await fetchData("/api/products", z.array(ProductSchema));
```

### Generic Constraints

```typescript
// ❌ Too loose generic
function getProperty<T>(obj: T, key: string): unknown {
  return (obj as any)[key];
}

// ✅ Constrained generic
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "John", age: 30 };
const name = getProperty(user, "name"); // Type: string
const age = getProperty(user, "age"); // Type: number
// getProperty(user, 'invalid');         // Error!
```

### Utility Types

```typescript
// ❌ Manual partial type
interface UserUpdate {
  name?: string;
  email?: string;
  age?: number;
}

// ✅ Use Partial utility type
type UserUpdate = Partial<User>;

// Other useful utility types:
type ReadonlyUser = Readonly<User>;
type UserKeys = keyof User;
type PickedUser = Pick<User, "name" | "email">;
type OmittedUser = Omit<User, "password">;
type RequiredUser = Required<Partial<User>>;
```

---

## Async Patterns

### Sequential vs Parallel

```typescript
// ❌ Sequential when parallel is possible
async function getUserData(userId: string): Promise<UserData> {
  const profile = await fetchProfile(userId);
  const posts = await fetchPosts(userId); // Waits for profile!
  const followers = await fetchFollowers(userId); // Waits for posts!
  return { profile, posts, followers };
}

// ✅ Parallel execution
async function getUserData(userId: string): Promise<UserData> {
  const [profile, posts, followers] = await Promise.all([
    fetchProfile(userId),
    fetchPosts(userId),
    fetchFollowers(userId),
  ]);
  return { profile, posts, followers };
}
```

### Promise.allSettled for Partial Failures

```typescript
// ❌ One failure kills everything
async function fetchAllUsers(ids: string[]): Promise<User[]> {
  return Promise.all(ids.map((id) => fetchUser(id)));
  // One failure = all fail
}

// ✅ Handle partial failures
async function fetchAllUsers(ids: string[]): Promise<(User | Error)[]> {
  const results = await Promise.allSettled(ids.map((id) => fetchUser(id)));

  return results.map((result) =>
    result.status === "fulfilled" ? result.value : result.reason,
  );
}
```

---

## Module Patterns

### Barrel Exports

```typescript
// ❌ Deep imports throughout codebase
import { User } from "../../../domain/entities/user";
import { UserService } from "../../../services/user/userService";
import { validateUser } from "../../../utils/validators/userValidator";

// ✅ Barrel file (index.ts)
// src/domain/index.ts
export * from "./entities/user";
export * from "./entities/product";

// src/services/index.ts
export * from "./user/userService";
export * from "./product/productService";

// Clean imports
import { User, UserService, validateUser } from "@/domain";
```

### Re-exporting Types

```typescript
// ✅ Re-export commonly used types
// types/index.ts
export type { User, UserRole } from "./user";
export type { Product, ProductCategory } from "./product";
export type { ApiResponse, ApiError } from "./api";

// Public API types
export type { CreateUserInput, UpdateUserInput } from "./inputs";
```

---

## Common Pitfalls

| Pitfall                | Problem                  | Solution                               |
| ---------------------- | ------------------------ | -------------------------------------- |
| Using `any`            | No type safety           | Use proper types or `unknown`          |
| Unvalidated assertions | Runtime crashes          | Validate with Zod/io-ts                |
| Unchecked null         | `undefined` errors       | Optional chaining + nullish coalescing |
| Untyped catch          | Can't access error props | Type narrow with `instanceof`          |
| Non-exhaustive switch  | Missing cases at runtime | Use `never` for exhaustive check       |
| Sequential awaits      | Slow performance         | Use `Promise.all` for parallel         |

## Best Practices Summary

1. **No `any`** - Use proper types or `unknown`
2. **Validate External Data** - Never trust API responses
3. **Use Discriminated Unions** - For variant types
4. **Handle Null Properly** - Optional chaining + nullish coalescing
5. **Type Errors** - Narrow with `instanceof` or type guards
6. **Exhaustive Switches** - Use `never` for completeness
7. **Generic Functions** - For reusable typed code
8. **Enable Strict Mode** - `"strict": true` in tsconfig


## Parent Hub
- [_frontend-mastery](../_frontend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
