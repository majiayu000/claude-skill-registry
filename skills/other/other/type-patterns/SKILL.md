---
name: type-patterns
description: >
  Advanced TypeScript type patterns for modeling complex domains safely.
  Use when the user needs discriminated unions, branded types, template literal
  types, type guards, exhaustive checking, const assertions, or is designing
  type-safe APIs and domain models.
---

# TypeScript Type Patterns

Apply advanced type-level patterns to model domains precisely and catch
logic errors at compile time instead of runtime.

## When to Use
- Modeling state machines or multi-variant data
- Preventing invalid values (e.g., mixing IDs of different entities)
- Building type-safe string patterns or event systems
- Ensuring all union cases are handled in switch/if chains
- Creating immutable constant objects with full type inference

## Core Patterns

### Pattern 1: Discriminated Unions

Use a shared literal property to let TypeScript narrow union members automatically.

```typescript
interface Loading { status: "loading" }
interface Success<T> { status: "success"; data: T }
interface Failure { status: "error"; error: Error }

type AsyncState<T> = Loading | Success<T> | Failure;

function render(state: AsyncState<string>): string {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "success":
      return state.data; // narrowed to Success<string>
    case "error":
      return state.error.message; // narrowed to Failure
  }
}
```

### Pattern 2: Exhaustive Checking with never

Guarantee every union variant is handled. If a new variant is added, the
compiler flags every switch that misses it.

```typescript
function assertNever(value: never): never {
  throw new Error(`Unhandled value: ${JSON.stringify(value)}`);
}

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rect":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      return assertNever(shape); // compile error if a case is missing
  }
}
```

### Pattern 3: Branded Types

Prevent mixing structurally identical types by attaching a phantom brand.

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function createUserId(id: string): UserId {
  return id as UserId;
}

function createOrderId(id: string): OrderId {
  return id as OrderId;
}

function getUser(id: UserId): void { /* ... */ }

const userId = createUserId("u-123");
const orderId = createOrderId("o-456");

getUser(userId);   // OK
// getUser(orderId); // Compile error -- OrderId is not UserId
```

### Pattern 4: Template Literal Types

Build type-safe string patterns that the compiler validates.

```typescript
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiVersion = "v1" | "v2";
type Resource = "users" | "orders" | "products";

type ApiRoute = `/${ApiVersion}/${Resource}`;
// "/v1/users" | "/v1/orders" | "/v1/products" | "/v2/users" | ...

type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"

// Infer parts from template literals
type ExtractResource<T> = T extends `/${string}/${infer R}` ? R : never;
type Route = ExtractResource<"/v1/users">; // "users"
```

### Pattern 5: Const Assertions and Readonly Tuples

Use `as const` to preserve literal types and create fully immutable structures.

```typescript
// Without as const: type is { method: string; url: string }
// With as const: type preserves exact literals
const config = {
  method: "GET",
  url: "/api/users",
  headers: ["Content-Type", "Authorization"],
} as const;

// config.method is "GET", not string
// config.headers is readonly ["Content-Type", "Authorization"]

// Derive union types from const objects
const STATUS_CODES = {
  OK: 200,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
} as const;

type StatusCode = (typeof STATUS_CODES)[keyof typeof STATUS_CODES];
// 200 | 404 | 500

// Derive from const arrays
const ROLES = ["admin", "editor", "viewer"] as const;
type Role = (typeof ROLES)[number]; // "admin" | "editor" | "viewer"
```

### Pattern 6: Type Guards

Create reusable runtime checks that inform the compiler.

```typescript
interface ApiError {
  code: number;
  message: string;
}

function isApiError(value: unknown): value is ApiError {
  return (
    typeof value === "object" &&
    value !== null &&
    "code" in value &&
    "message" in value &&
    typeof (value as ApiError).code === "number" &&
    typeof (value as ApiError).message === "string"
  );
}

async function fetchData(url: string): Promise<string> {
  const response = await fetch(url);
  const body: unknown = await response.json();

  if (isApiError(body)) {
    throw new Error(`API error ${body.code}: ${body.message}`);
  }

  return body as string;
}
```

## Anti-Patterns

- **String enums without discrimination** -- Use discriminated unions instead of plain string
  enums when variants carry different data. Enums alone cannot narrow.

- **Overusing `as` for branded types** -- Limit `as` to brand constructors only. Every other
  usage should rely on narrowing.

- **Forgetting the `default: assertNever`** -- Without the exhaustive check, new union members
  silently fall through with `undefined` behavior.

- **`as const` on mutable variables** -- `as const` makes the value deeply readonly.
  Do not assign it to a mutable variable and expect mutation to work.

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| Discriminated unions | Multi-state data, state machines |
| Exhaustive check (never) | Guarantee all cases handled |
| Branded types | Prevent ID/value mixing |
| Template literal types | Type-safe string patterns |
| const assertions | Immutable configs, derive unions |
| Type guards | Runtime validation with type narrowing |
