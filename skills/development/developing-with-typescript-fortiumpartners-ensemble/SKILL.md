---
name: developing-with-typescript
description: TypeScript 5.x development with type system, generics, utility types, and strict mode patterns. Use when writing TypeScript code or adding types to JavaScript projects.
---

# TypeScript Development Skill

TypeScript 5.x development with modern patterns including strict mode, generics, utility types, and modules.

**Progressive Disclosure**: Quick reference patterns here. See [REFERENCE.md](REFERENCE.md) for advanced topics.

---

## When to Use

Loaded by `backend-developer` or `frontend-developer` when:
- `tsconfig.json` present in project
- `package.json` contains `typescript` dependency
- `.ts` or `.tsx` files in project

---

## Quick Start

### Basic Types

```typescript
// Primitives
const name: string = "Alice";
const age: number = 30;
const isActive: boolean = true;

// Arrays and Tuples
const numbers: number[] = [1, 2, 3];
const point: [number, number] = [10, 20];
const rest: [string, ...number[]] = ["scores", 1, 2, 3];
```

### Interfaces vs Type Aliases

```typescript
// Interfaces - object shapes, extensible, declaration merging
interface User {
  id: string;
  name: string;
  email: string;
}

interface Admin extends User {
  permissions: string[];
}

// Type aliases - unions, tuples, primitives, complex types
type ID = string | number;
type Point = [number, number];
type Callback = (data: string) => void;
type AdminUser = User & { permissions: string[] };
```

### Functions

```typescript
// Basic function
function greet(name: string): string {
  return `Hello, ${name}`;
}

// Arrow with optional/default params
const createUser = (name: string, age?: number, role = "user") => ({ name, age, role });

// Function overloads
function parse(input: string): string[];
function parse(input: string[]): string;
function parse(input: string | string[]): string | string[] {
  return typeof input === "string" ? input.split(",") : input.join(",");
}
```

---

## Type System Essentials

### Union and Intersection Types

```typescript
// Union - one of multiple types
type Status = "pending" | "approved" | "rejected";
type Result = string | Error;

// Intersection - combine types
type Timestamped = { createdAt: Date; updatedAt: Date };
type Entity = User & Timestamped;
```

### Literal Types

```typescript
type Direction = "north" | "south" | "east" | "west";
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;

// Template literal types
type EventName = `on${Capitalize<string>}`;
type Getter<T extends string> = `get${Capitalize<T>}`;
```

### Type Narrowing

```typescript
// typeof guard
function format(value: string | number): string {
  return typeof value === "string" ? value.trim() : value.toFixed(2);
}

// in operator
function speak(animal: { bark(): void } | { meow(): void }): void {
  if ("bark" in animal) animal.bark();
  else animal.meow();
}

// Discriminated unions (recommended)
type Success = { status: "success"; data: string };
type Failure = { status: "failure"; error: Error };
type Result = Success | Failure;

function handle(result: Result): string {
  return result.status === "success" ? result.data : result.error.message;
}
```

---

## Generics

### Basic Generics

```typescript
function identity<T>(value: T): T {
  return value;
}

interface Box<T> {
  value: T;
  map<U>(fn: (value: T) => U): Box<U>;
}

class Container<T> {
  constructor(private value: T) {}
  get(): T { return this.value; }
}
```

### Constraints

```typescript
// extends constraint
function getLength<T extends { length: number }>(item: T): number {
  return item.length;
}

// keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Default type
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
}
```

---

## Utility Types

### Transformation

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

type PartialUser = Partial<User>;           // All optional
type RequiredUser = Required<PartialUser>;  // All required
type ReadonlyUser = Readonly<User>;         // All readonly

type UserPreview = Pick<User, "id" | "name">;
type UserWithoutEmail = Omit<User, "email">;

type UserRoles = Record<string, "admin" | "user">;
```

### Extraction

```typescript
// Extract/Exclude from unions
type Numbers = Extract<string | number | boolean, number>;  // number
type NotNumber = Exclude<string | number | boolean, number>; // string | boolean

// Remove null/undefined
type Defined = NonNullable<string | null | undefined>;  // string

// Function types
type Return = ReturnType<typeof createUser>;
type Params = Parameters<typeof createUser>;

// Unwrap Promise
type Unwrapped = Awaited<Promise<string>>;  // string
```

---

## tsconfig.json Essentials

### Recommended Strict Config

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "declaration": true,
    "outDir": "./dist",
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Key Strict Flags

| Flag | Purpose |
|------|---------|
| `strict` | Enable all strict checks |
| `noImplicitAny` | Error on implicit any |
| `strictNullChecks` | null/undefined require handling |
| `noUncheckedIndexedAccess` | Index access may be undefined |

---

## Module Patterns

### Import/Export

```typescript
// Named exports
export const PI = 3.14159;
export function calculate(r: number): number { return PI * r ** 2; }
export interface Circle { radius: number; }

// Default export
export default class Calculator { }

// Re-exports
export { User } from "./user";
export * from "./utils";

// Type-only imports
import type { User } from "./types";
export type { Config } from "./config";
```

### Declaration Files

```typescript
// types.d.ts
declare module "untyped-library" {
  export function process(input: string): string;
}

// Extend existing module
declare module "express" {
  interface Request { userId?: string; }
}

// Global declarations
declare global {
  interface Window { myApp: { version: string }; }
}
```

---

## Common Patterns

### Type Guards

```typescript
// User-defined type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isUser(obj: unknown): obj is User {
  return typeof obj === "object" && obj !== null && "id" in obj && "name" in obj;
}

// Assertion function
function assertDefined<T>(value: T | undefined): asserts value is T {
  if (value === undefined) throw new Error("Value is undefined");
}
```

### Branded Types

```typescript
// Prevent type confusion
type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId { return id as UserId; }
function createOrderId(id: string): OrderId { return id as OrderId; }

function getUser(id: UserId): User { /* ... */ }

const userId = createUserId("user-123");
getUser(userId);  // OK
// getUser(createOrderId("order-456"));  // Error!
```

### Result Type

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return { success: false, error: "Division by zero" };
  return { success: true, data: a / b };
}

const result = divide(10, 2);
if (result.success) console.log(result.data);
else console.error(result.error);
```

---

## Quick Reference

### Assertions

```typescript
const value = someValue as string;           // Type assertion
const element = document.getElementById("app")!;  // Non-null assertion
const config = { api: "/api" } as const;     // Const assertion
```

### Index Signatures

```typescript
interface StringMap { [key: string]: string; }
interface NumberMap { [index: number]: string; }
interface DataAttrs { [key: `data-${string}`]: string; }
```

### Mapped Types

```typescript
type Optional<T> = { [K in keyof T]?: T[K] };
type Immutable<T> = { readonly [K in keyof T]: T[K] };
type Mutable<T> = { -readonly [K in keyof T]: T[K] };
```

---

## See Also

- [REFERENCE.md](REFERENCE.md) - Advanced generics, conditional types, decorators
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
