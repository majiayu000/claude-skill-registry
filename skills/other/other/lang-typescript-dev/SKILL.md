---
name: lang-typescript-dev
description: Foundational TypeScript patterns covering types, interfaces, generics, utility types, and common idioms. Use when writing TypeScript code, understanding the type system, or needing guidance on which specialized TypeScript skill to use. This is the entry point for TypeScript development.
---

# TypeScript Fundamentals

Foundational TypeScript patterns and core type system features. This skill serves as both a reference for common patterns and an index to specialized TypeScript skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   TypeScript Skill Hierarchy                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                 ┌─────────────────────┐                         │
│                 │ lang-typescript-dev │ ◄── You are here        │
│                 │    (foundation)     │                         │
│                 └──────────┬──────────┘                         │
│                            │                                    │
│            ┌───────────────┴───────────────┐                    │
│            │                               │                    │
│            ▼                               ▼                    │
│   ┌─────────────────┐            ┌─────────────────┐           │
│   │    patterns     │            │     library     │           │
│   │      -dev       │            │       -dev      │           │
│   └─────────────────┘            └─────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Basic and advanced types
- Interfaces and type aliases
- Unions, intersections, and type guards
- Generics fundamentals
- Utility types
- Common patterns and idioms

**This skill does NOT cover (see specialized skills):**
- tsconfig.json configuration → `lang-typescript-patterns-dev`
- Best practices and code patterns → `lang-typescript-patterns-dev`
- Library/package publishing → `lang-typescript-library-dev`
- React component typing → frontend skills
- Node.js typing → backend skills

---

## Quick Reference

| Task | Syntax |
|------|--------|
| Type alias | `type Name = string \| number` |
| Interface | `interface User { name: string }` |
| Generic function | `function fn<T>(x: T): T` |
| Optional property | `{ name?: string }` |
| Readonly property | `{ readonly id: number }` |
| Union type | `string \| number` |
| Intersection | `TypeA & TypeB` |
| Type assertion | `value as Type` or `<Type>value` |
| Non-null assertion | `value!` |
| Type guard | `if (typeof x === 'string')` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Configure tsconfig.json | `lang-typescript-patterns-dev` |
| Set up strict mode, path aliases | `lang-typescript-patterns-dev` |
| Publish npm packages | `lang-typescript-library-dev` |
| Configure ESM/CJS dual packages | `lang-typescript-library-dev` |
| Generate declaration files | `lang-typescript-library-dev` |

---

## Basic Types

### Primitive Types

```typescript
// String, number, boolean
let name: string = "Alice";
let age: number = 30;
let active: boolean = true;

// Arrays
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ["Alice", "Bob"];

// Tuple (fixed-length array with specific types)
let pair: [string, number] = ["age", 30];

// Any (escape hatch - avoid when possible)
let data: any = "could be anything";

// Unknown (safer than any - requires type checking)
let input: unknown = getUserInput();
if (typeof input === "string") {
  console.log(input.toUpperCase()); // OK after check
}

// Void (function returns nothing)
function log(msg: string): void {
  console.log(msg);
}

// Never (function never returns)
function fail(msg: string): never {
  throw new Error(msg);
}

// Null and undefined
let nullable: string | null = null;
let optional: string | undefined = undefined;
```

### Object Types

```typescript
// Inline object type
function greet(user: { name: string; age: number }): string {
  return `Hello, ${user.name}`;
}

// Optional properties
function greet(user: { name: string; age?: number }): string {
  return user.age ? `${user.name} is ${user.age}` : user.name;
}

// Index signatures
interface StringMap {
  [key: string]: string;
}

const headers: StringMap = {
  "Content-Type": "application/json",
  "Authorization": "Bearer token",
};
```

---

## Interfaces vs Type Aliases

### Interface

```typescript
// Declaration
interface User {
  id: number;
  name: string;
  email?: string;
}

// Extension
interface Admin extends User {
  permissions: string[];
}

// Declaration merging (interfaces can be extended across files)
interface User {
  createdAt: Date;  // Adds to existing User interface
}

// Implementing interfaces
class UserImpl implements User {
  id = 1;
  name = "Alice";
  createdAt = new Date();
}
```

### Type Alias

```typescript
// Declaration
type User = {
  id: number;
  name: string;
  email?: string;
};

// Intersection (like extends)
type Admin = User & {
  permissions: string[];
};

// Types can represent primitives, unions, tuples
type ID = string | number;
type Point = [number, number];
type Callback = (data: string) => void;

// Cannot be merged (redeclaration is an error)
```

### When to Use Which

| Use Case | Prefer |
|----------|--------|
| Object shapes | Either (interface slightly better for extension) |
| Unions, intersections | Type alias (only option) |
| Primitives, tuples | Type alias (only option) |
| Class implementation | Interface |
| Library public API | Interface (allows consumer extension) |
| Complex computed types | Type alias |

---

## Unions and Intersections

### Union Types

```typescript
// Value can be one of several types
type Status = "pending" | "approved" | "rejected";
type ID = string | number;

function process(id: ID): void {
  // Must handle both cases
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id.toFixed(2));
  }
}

// Discriminated unions (tagged unions)
type Success = { status: "success"; data: string };
type Failure = { status: "failure"; error: Error };
type Result = Success | Failure;

function handle(result: Result): void {
  switch (result.status) {
    case "success":
      console.log(result.data);  // TypeScript knows this is Success
      break;
    case "failure":
      console.error(result.error);  // TypeScript knows this is Failure
      break;
  }
}
```

### Intersection Types

```typescript
// Combine multiple types
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;  // { name: string; age: number }

// Useful for mixins
type Timestamped = { createdAt: Date; updatedAt: Date };
type User = { id: number; name: string };
type TimestampedUser = User & Timestamped;
```

---

## Type Guards

### Built-in Type Guards

```typescript
// typeof (primitives)
function process(value: string | number): void {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  } else {
    console.log(value.toFixed(2));
  }
}

// instanceof (classes)
function handle(error: Error | string): void {
  if (error instanceof Error) {
    console.log(error.message);
  } else {
    console.log(error);
  }
}

// in operator (property check)
type Cat = { meow: () => void };
type Dog = { bark: () => void };

function speak(animal: Cat | Dog): void {
  if ("meow" in animal) {
    animal.meow();
  } else {
    animal.bark();
  }
}

// Array.isArray
function process(value: string | string[]): void {
  if (Array.isArray(value)) {
    console.log(value.join(", "));
  } else {
    console.log(value);
  }
}
```

### Custom Type Guards

```typescript
// Type predicate function
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function process(value: unknown): void {
  if (isString(value)) {
    console.log(value.toUpperCase());  // TypeScript knows it's string
  }
}

// Discriminated union guard
function isSuccess(result: Result): result is Success {
  return result.status === "success";
}
```

---

## Generics

### Generic Functions

```typescript
// Basic generic function
function identity<T>(value: T): T {
  return value;
}

const str = identity("hello");  // Type: string
const num = identity(42);       // Type: number

// Multiple type parameters
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

// With constraints
function getLength<T extends { length: number }>(item: T): number {
  return item.length;
}

getLength("hello");    // OK
getLength([1, 2, 3]);  // OK
getLength(123);        // Error: number has no length
```

### Generic Interfaces and Types

```typescript
// Generic interface
interface Container<T> {
  value: T;
  getValue(): T;
}

// Generic type alias
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Usage
const success: Result<string> = { ok: true, value: "data" };
const failure: Result<string> = { ok: false, error: new Error("fail") };
```

### Generic Constraints

```typescript
// Extends constraint
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

// keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name");  // Type: string
const age = getProperty(user, "age");    // Type: number
// getProperty(user, "foo");  // Error: "foo" not in keyof typeof user
```

---

## Utility Types

### Transformation Types

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

// Partial<T> - All properties optional
type PartialUser = Partial<User>;
// { id?: number; name?: string; email?: string }

// Required<T> - All properties required
type RequiredUser = Required<PartialUser>;

// Readonly<T> - All properties readonly
type ReadonlyUser = Readonly<User>;
// { readonly id: number; readonly name: string; readonly email: string }

// Pick<T, K> - Select properties
type UserName = Pick<User, "name">;
// { name: string }

// Omit<T, K> - Exclude properties
type UserWithoutEmail = Omit<User, "email">;
// { id: number; name: string }
```

### Record and Mapped Types

```typescript
// Record<K, V> - Object with specific key/value types
type UserRoles = Record<string, string[]>;
const roles: UserRoles = {
  alice: ["admin", "user"],
  bob: ["user"],
};

// Index signature equivalent
type SameAsRecord = { [key: string]: string[] };
```

### Conditional Types

```typescript
// Extract<T, U> - Extract types assignable to U
type Numbers = Extract<string | number | boolean, number>;
// number

// Exclude<T, U> - Exclude types assignable to U
type NotNumbers = Exclude<string | number | boolean, number>;
// string | boolean

// NonNullable<T> - Exclude null and undefined
type Defined = NonNullable<string | null | undefined>;
// string
```

### Function Types

```typescript
function greet(name: string, age: number): string {
  return `Hello ${name}, you are ${age}`;
}

// ReturnType<T> - Extract return type
type GreetReturn = ReturnType<typeof greet>;
// string

// Parameters<T> - Extract parameter types as tuple
type GreetParams = Parameters<typeof greet>;
// [string, number]
```

---

## Common Patterns

### Exhaustive Switch

```typescript
type Status = "pending" | "approved" | "rejected";

function handleStatus(status: Status): string {
  switch (status) {
    case "pending":
      return "Waiting...";
    case "approved":
      return "Done!";
    case "rejected":
      return "Failed";
    default:
      // This ensures all cases are handled
      const _exhaustive: never = status;
      return _exhaustive;
  }
}
```

### Branded Types

```typescript
// Create distinct types from primitives
type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

function createOrderId(id: string): OrderId {
  return id as OrderId;
}

function getUser(id: UserId): User { /* ... */ }
function getOrder(id: OrderId): Order { /* ... */ }

const userId = createUserId("user-123");
const orderId = createOrderId("order-456");

getUser(userId);   // OK
// getUser(orderId);  // Error: OrderId not assignable to UserId
```

### Builder Pattern with Types

```typescript
interface RequestConfig {
  url: string;
  method?: "GET" | "POST" | "PUT" | "DELETE";
  headers?: Record<string, string>;
  body?: unknown;
}

class RequestBuilder {
  private config: RequestConfig;

  constructor(url: string) {
    this.config = { url };
  }

  method(m: RequestConfig["method"]): this {
    this.config.method = m;
    return this;
  }

  header(key: string, value: string): this {
    this.config.headers = { ...this.config.headers, [key]: value };
    return this;
  }

  body<T>(data: T): this {
    this.config.body = data;
    return this;
  }

  build(): RequestConfig {
    return this.config;
  }
}

const request = new RequestBuilder("/api/users")
  .method("POST")
  .header("Content-Type", "application/json")
  .body({ name: "Alice" })
  .build();
```

### Assertion Functions

```typescript
function assertDefined<T>(
  value: T | null | undefined,
  message?: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? "Value is not defined");
  }
}

function process(value: string | null): void {
  assertDefined(value, "Value required");
  // TypeScript knows value is string here
  console.log(value.toUpperCase());
}
```

---

## Troubleshooting

### "Object is possibly undefined"

```typescript
// Problem
const user = users.find(u => u.id === 1);
console.log(user.name);  // Error: user might be undefined

// Fix 1: Optional chaining
console.log(user?.name);

// Fix 2: Type guard
if (user) {
  console.log(user.name);
}

// Fix 3: Non-null assertion (use carefully)
console.log(user!.name);
```

### "Type 'X' is not assignable to type 'Y'"

```typescript
// Problem
const status: "active" | "inactive" = "active";
const str: string = "active";
// const status2: "active" | "inactive" = str;  // Error

// Fix: Use const assertion or explicit typing
const status2: "active" | "inactive" = str as "active" | "inactive";
// Or
const literal = "active" as const;
```

### "Property 'X' does not exist on type"

```typescript
// Problem with union types
type Cat = { meow: () => void };
type Dog = { bark: () => void };
type Animal = Cat | Dog;

function speak(animal: Animal): void {
  // animal.meow();  // Error: Dog doesn't have meow

  // Fix: Type guard
  if ("meow" in animal) {
    animal.meow();
  }
}
```

### Index Signature Errors

```typescript
// Problem
interface User {
  name: string;
  age: number;
}

const key = "name";
// const value = user[key];  // Error with noPropertyAccessFromIndexSignature

// Fix 1: Use known key
const value = user.name;

// Fix 2: Type assertion
const value2 = user[key as keyof User];

// Fix 3: Add index signature (if dynamic access needed)
interface FlexibleUser {
  name: string;
  age: number;
  [key: string]: string | number;
}
```

---

## Module System

TypeScript supports ES modules (ESM) as the primary module system, with CommonJS support for Node.js compatibility.

### Import and Export

```typescript
// Named exports
export const PI = 3.14159;
export function add(a: number, b: number): number {
  return a + b;
}
export interface User {
  id: number;
  name: string;
}

// Default export
export default class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// Named imports
import { PI, add, User } from './math';

// Default import
import Calculator from './calculator';

// Namespace import
import * as math from './math';
console.log(math.PI);

// Mixed imports
import Calculator, { PI, add } from './calculator';

// Rename imports
import { add as sum } from './math';
```

### Re-exports

```typescript
// Re-export everything
export * from './types';

// Re-export specific items
export { User, Order } from './models';

// Re-export with rename
export { User as UserModel } from './models';

// Re-export default as named
export { default as Calculator } from './calculator';

// Barrel file (index.ts)
export * from './user';
export * from './order';
export * from './product';
```

### Type-Only Imports

```typescript
// Import only types (removed at runtime)
import type { User, Order } from './models';

// Inline type imports
import { type User, createUser } from './models';

// Type-only re-exports
export type { User, Order } from './models';
```

### Dynamic Imports

```typescript
// Lazy loading modules
async function loadFeature(): Promise<void> {
  const module = await import('./heavy-feature');
  module.initialize();
}

// Conditional imports
const adapter = await import(
  process.env.DB_TYPE === 'postgres'
    ? './postgres-adapter'
    : './mysql-adapter'
);
```

### Module Resolution

```typescript
// Relative imports (start with ./ or ../)
import { utils } from './utils';
import { config } from '../config';

// Non-relative imports (resolved from node_modules)
import express from 'express';
import { z } from 'zod';

// Path aliases (configured in tsconfig.json)
import { User } from '@/models/user';
import { config } from '@config';
```

---

## Error Handling

TypeScript uses JavaScript's exception-based error handling with enhanced type safety.

### Try-Catch-Finally

```typescript
try {
  const data = JSON.parse(userInput);
  processData(data);
} catch (error) {
  // error is 'unknown' in TypeScript 4.4+
  if (error instanceof SyntaxError) {
    console.error('Invalid JSON:', error.message);
  } else if (error instanceof Error) {
    console.error('Error:', error.message);
  } else {
    console.error('Unknown error:', error);
  }
} finally {
  cleanup();
}
```

### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly field?: string
  ) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
  }
}

// Usage
throw new NotFoundError('User');
throw new ValidationError('Email is required', 'email');
```

### Result Pattern (Error as Values)

```typescript
// Result type for explicit error handling
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseUser(json: string): Result<User, string> {
  try {
    const data = JSON.parse(json);
    if (!data.id || !data.name) {
      return { ok: false, error: 'Missing required fields' };
    }
    return { ok: true, value: data as User };
  } catch {
    return { ok: false, error: 'Invalid JSON' };
  }
}

// Usage
const result = parseUser(input);
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error);
}
```

### Assertion Functions

```typescript
function assertIsError(value: unknown): asserts value is Error {
  if (!(value instanceof Error)) {
    throw new Error('Expected an Error instance');
  }
}

function assertNonNull<T>(
  value: T | null | undefined,
  message?: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? 'Value is null or undefined');
  }
}

// Usage
const user = users.find(u => u.id === 1);
assertNonNull(user, 'User not found');
console.log(user.name); // TypeScript knows user is not null
```

### Error Type Guards

```typescript
function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  return 'Unknown error';
}
```

---

## Concurrency

TypeScript uses JavaScript's Promise-based async model with async/await syntax.

### Promises

```typescript
// Creating promises
function fetchUser(id: string): Promise<User> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id === 'invalid') {
        reject(new Error('User not found'));
      } else {
        resolve({ id, name: 'Alice' });
      }
    }, 100);
  });
}

// Promise chaining
fetchUser('123')
  .then(user => fetchOrders(user.id))
  .then(orders => console.log(orders))
  .catch(error => console.error(error));
```

### Async/Await

```typescript
// Async function
async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json();
}

// Error handling with try/catch
async function processUser(id: string): Promise<void> {
  try {
    const user = await getUser(id);
    const orders = await getOrders(user.id);
    console.log(user.name, orders.length);
  } catch (error) {
    console.error('Failed:', error);
  }
}
```

### Parallel Execution

```typescript
// Promise.all - Wait for all (fails fast)
const [users, orders, products] = await Promise.all([
  fetchUsers(),
  fetchOrders(),
  fetchProducts(),
]);

// Promise.allSettled - Wait for all (never rejects)
const results = await Promise.allSettled([
  fetchUsers(),
  fetchOrders(),
  fetchProducts(),
]);

results.forEach((result, i) => {
  if (result.status === 'fulfilled') {
    console.log(`Success ${i}:`, result.value);
  } else {
    console.log(`Failed ${i}:`, result.reason);
  }
});

// Promise.race - First to settle
const fastest = await Promise.race([
  fetchFromPrimary(),
  fetchFromBackup(),
]);
```

### Cancellation with AbortController

```typescript
async function fetchWithTimeout<T>(
  url: string,
  timeoutMs: number
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}

// Manual cancellation
const controller = new AbortController();

async function fetchData(): Promise<void> {
  try {
    const response = await fetch('/api/data', {
      signal: controller.signal,
    });
    console.log(await response.json());
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      console.log('Request was cancelled');
    } else {
      throw error;
    }
  }
}

// Later: cancel the request
controller.abort();
```

### See Also

- `patterns-concurrency-dev` - Cross-language async patterns and comparisons

---

## Serialization

TypeScript provides type-safe patterns for JSON serialization and validation.

### JSON Serialization

```typescript
// Basic JSON handling
const user: User = { id: 1, name: 'Alice' };
const json: string = JSON.stringify(user);
const parsed: unknown = JSON.parse(json);

// Type-safe parsing with type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    typeof (value as User).id === 'number' &&
    typeof (value as User).name === 'string'
  );
}

const data = JSON.parse(json);
if (isUser(data)) {
  console.log(data.name); // TypeScript knows this is User
}
```

### Schema Validation with Zod

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.number(),
  name: z.string().min(1).max(100),
  email: z.string().email().optional(),
  createdAt: z.string().datetime().transform(s => new Date(s)),
});

// Infer TypeScript type from schema
type User = z.infer<typeof UserSchema>;

// Parse and validate
function parseUser(data: unknown): User {
  return UserSchema.parse(data); // Throws on invalid
}

// Safe parsing (returns result)
function safeParseUser(data: unknown): User | null {
  const result = UserSchema.safeParse(data);
  return result.success ? result.data : null;
}
```

### Custom Serialization

```typescript
interface SerializableDate {
  toJSON(): string;
}

class User {
  constructor(
    public id: number,
    public name: string,
    public createdAt: Date
  ) {}

  toJSON(): object {
    return {
      id: this.id,
      name: this.name,
      createdAt: this.createdAt.toISOString(),
    };
  }

  static fromJSON(json: unknown): User {
    if (!isUserJSON(json)) {
      throw new Error('Invalid user JSON');
    }
    return new User(
      json.id,
      json.name,
      new Date(json.createdAt)
    );
  }
}
```

### Class Transformer (Decorator-based)

```typescript
import { Type, Expose, Transform, plainToInstance } from 'class-transformer';
import { IsEmail, Length, IsOptional, validate } from 'class-validator';

class User {
  @Expose({ name: 'user_id' })
  id: number;

  @Length(1, 100)
  name: string;

  @IsEmail()
  @IsOptional()
  email?: string;

  @Type(() => Date)
  @Transform(({ value }) => new Date(value), { toClassOnly: true })
  createdAt: Date;
}

// Usage
const user = plainToInstance(User, jsonData);
const errors = await validate(user);
```

### See Also

- `patterns-serialization-dev` - Cross-language serialization patterns

---

## Build and Dependencies

TypeScript projects use npm/yarn/pnpm for dependencies and tsconfig.json for compilation.

### Package.json Essentials

```json
{
  "name": "my-typescript-app",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js",
    "test": "vitest",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }
}
```

### tsconfig.json Essentials

```json
{
  "compilerOptions": {
    // Output settings
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",

    // Type checking
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,

    // Declaration files
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Path aliases
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Common Configurations

```typescript
// ESM for Node.js
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  }
}

// Library publishing (dual ESM/CJS)
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "declaration": true,
    "declarationMap": true
  }
}

// Frontend (with bundler)
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx"
  }
}
```

### Declaration Files

```typescript
// Manual declaration (module.d.ts)
declare module 'untyped-lib' {
  export function doSomething(input: string): number;
  export interface Config {
    timeout: number;
  }
}

// Ambient declarations (global.d.ts)
declare global {
  interface Window {
    myApp: MyAppConfig;
  }

  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'production' | 'test';
      API_URL: string;
    }
  }
}

export {}; // Make this a module
```

### Dependency Management

```bash
# Install dependencies
npm install express
npm install -D @types/express typescript

# Check for type packages
npx @arethetypeswrong/cli package-name

# Update TypeScript
npm install -D typescript@latest

# Check for outdated
npm outdated
```

---

## Testing

TypeScript testing typically uses Vitest or Jest with type-aware assertions.

### Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts'],
    coverage: {
      reporter: ['text', 'html'],
    },
  },
});
```

### Basic Tests

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('Calculator', () => {
  let calc: Calculator;

  beforeEach(() => {
    calc = new Calculator();
  });

  it('adds two numbers', () => {
    expect(calc.add(2, 3)).toBe(5);
  });

  it('throws on invalid input', () => {
    expect(() => calc.divide(1, 0)).toThrow('Division by zero');
  });
});
```

### Type Testing

```typescript
import { expectTypeOf } from 'vitest';

it('returns the correct type', () => {
  const result = processData({ id: 1 });
  expectTypeOf(result).toEqualTypeOf<ProcessedData>();
});

it('infers generic types correctly', () => {
  const items = createList<User>();
  expectTypeOf(items.get(0)).toEqualTypeOf<User | undefined>();
});
```

### Mocking

```typescript
import { vi, Mock } from 'vitest';

// Mock functions
const mockFn = vi.fn<[string], number>();
mockFn.mockReturnValue(42);
mockFn.mockImplementation((s) => s.length);

// Mock modules
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1 }]),
}));

// Spy on methods
const spy = vi.spyOn(console, 'log');
doSomething();
expect(spy).toHaveBeenCalledWith('expected message');

// Mock timers
vi.useFakeTimers();
setTimeout(callback, 1000);
vi.advanceTimersByTime(1000);
expect(callback).toHaveBeenCalled();
```

### Async Testing

```typescript
it('fetches user data', async () => {
  const user = await fetchUser('123');
  expect(user.name).toBe('Alice');
});

it('handles errors', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Not found');
});

it('waits for condition', async () => {
  await vi.waitFor(() => {
    expect(element.textContent).toBe('Loaded');
  });
});
```

### Test Utilities

```typescript
// Factory functions
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    ...overrides,
  };
}

// Fixtures
const testUsers: User[] = [
  createUser({ id: 1, name: 'Alice' }),
  createUser({ id: 2, name: 'Bob' }),
];

// Type-safe matchers
expect.extend({
  toBeValidUser(received: unknown) {
    const pass = isUser(received);
    return {
      pass,
      message: () => `expected ${received} to be a valid User`,
    };
  },
});
```

---

## Metaprogramming

TypeScript supports decorators for metaprogramming, enabling declarative modifications to classes, methods, and properties. Requires `experimentalDecorators` and optionally `emitDecoratorMetadata` in tsconfig.json.

### Enabling Decorators

```json
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

### Class Decorators

```typescript
// Class decorator - receives the constructor
function Sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

function Entity(tableName: string) {
  return function <T extends { new (...args: any[]): {} }>(constructor: T) {
    return class extends constructor {
      static tableName = tableName;
    };
  };
}

@Sealed
@Entity('users')
class User {
  name: string;
}

// Access metadata
console.log((User as any).tableName); // 'users'
```

### Method Decorators

```typescript
// Method decorator - receives target, key, descriptor
function Log(target: any, key: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${key} with`, args);
    const result = original.apply(this, args);
    console.log(`${key} returned`, result);
    return result;
  };
  return descriptor;
}

function Debounce(ms: number) {
  return function (target: any, key: string, descriptor: PropertyDescriptor) {
    let timeout: NodeJS.Timeout;
    const original = descriptor.value;
    descriptor.value = function (...args: any[]) {
      clearTimeout(timeout);
      timeout = setTimeout(() => original.apply(this, args), ms);
    };
    return descriptor;
  };
}

class API {
  @Log
  @Debounce(300)
  search(query: string): string[] {
    return ['result1', 'result2'];
  }
}
```

### Property Decorators

```typescript
// Property decorator - receives target and key
function Required(target: any, key: string) {
  let value: any;
  const getter = () => value;
  const setter = (newValue: any) => {
    if (newValue === undefined || newValue === null) {
      throw new Error(`${key} is required`);
    }
    value = newValue;
  };
  Object.defineProperty(target, key, {
    get: getter,
    set: setter,
    enumerable: true,
    configurable: true,
  });
}

function Column(options: { type: string; nullable?: boolean }) {
  return function (target: any, key: string) {
    const columns = Reflect.getMetadata('columns', target) || [];
    columns.push({ key, ...options });
    Reflect.defineMetadata('columns', columns, target);
  };
}

class User {
  @Required
  @Column({ type: 'varchar', nullable: false })
  name: string;
}
```

### Parameter Decorators

```typescript
// Parameter decorator - receives target, key, parameter index
function Inject(token: string) {
  return function (target: any, key: string, index: number) {
    const injections = Reflect.getMetadata('injections', target, key) || [];
    injections[index] = token;
    Reflect.defineMetadata('injections', injections, target, key);
  };
}

class UserService {
  constructor(
    @Inject('DATABASE') private db: Database,
    @Inject('LOGGER') private logger: Logger
  ) {}
}
```

### Reflect Metadata

```typescript
import 'reflect-metadata';

// Define metadata
Reflect.defineMetadata('role', 'admin', User);
Reflect.defineMetadata('role', 'user', User.prototype, 'name');

// Get metadata
const classRole = Reflect.getMetadata('role', User);
const propRole = Reflect.getMetadata('role', User.prototype, 'name');

// Get design-time type information (with emitDecoratorMetadata)
function LogType(target: any, key: string) {
  const type = Reflect.getMetadata('design:type', target, key);
  console.log(`${key} type:`, type.name); // e.g., "String", "Number"
}

// Get parameter types
function LogParams(target: any, key: string, descriptor: PropertyDescriptor) {
  const paramTypes = Reflect.getMetadata('design:paramtypes', target, key);
  console.log(`${key} params:`, paramTypes.map((t: any) => t.name));
}
```

### Decorator Factories Pattern

```typescript
// Composable decorator factory
interface ValidatorOptions {
  min?: number;
  max?: number;
  pattern?: RegExp;
  message?: string;
}

function Validate(options: ValidatorOptions) {
  return function (target: any, key: string) {
    const validators = Reflect.getMetadata('validators', target) || {};
    validators[key] = options;
    Reflect.defineMetadata('validators', validators, target);
  };
}

class CreateUserDto {
  @Validate({ min: 1, max: 100, message: 'Name must be 1-100 chars' })
  name: string;

  @Validate({ pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Invalid email' })
  email: string;
}

// Runtime validation
function validate(instance: any): string[] {
  const validators = Reflect.getMetadata('validators', instance) || {};
  const errors: string[] = [];

  for (const [key, opts] of Object.entries(validators) as [string, ValidatorOptions][]) {
    const value = instance[key];
    if (opts.min && value.length < opts.min) errors.push(opts.message || `${key} too short`);
    if (opts.max && value.length > opts.max) errors.push(opts.message || `${key} too long`);
    if (opts.pattern && !opts.pattern.test(value)) errors.push(opts.message || `${key} invalid`);
  }
  return errors;
}
```

### Common Decorator Libraries

| Library | Purpose | Example |
|---------|---------|---------|
| `class-validator` | Validation decorators | `@IsEmail()`, `@Length(1, 100)` |
| `class-transformer` | Serialization decorators | `@Type()`, `@Expose()` |
| `typeorm` | ORM decorators | `@Entity()`, `@Column()` |
| `nestjs` | Framework decorators | `@Controller()`, `@Get()` |
| `inversify` | DI decorators | `@injectable()`, `@inject()` |

### See Also

- `patterns-metaprogramming-dev` - Cross-language decorator/macro patterns

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Async/await, Promise patterns across languages
- `patterns-serialization-dev` - JSON, validation, type-safe parsing across languages
- `patterns-metaprogramming-dev` - Decorators, type system metaprogramming across languages

---

## References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [TypeScript Playground](https://www.typescriptlang.org/play)
- Specialized skills: `lang-typescript-patterns-dev`, `lang-typescript-library-dev`
