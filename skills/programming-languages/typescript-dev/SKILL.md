---
name: typescript-dev
description: World-class expert TypeScript developer specializing in type-safe code, modern TypeScript patterns, generics, utility types, and building scalable applications. Use when writing TypeScript code, designing type systems, solving type errors, or architecting TypeScript applications at enterprise scale.
---

# TypeScript Development Expert - World-Class Edition

## Project Context: DriverConnect (eddication.io)

**IMPORTANT**: This project uses TypeScript in Supabase Edge Functions.

### TypeScript Usage in Project

| Component | Language | Location |
|:---|:---|:---|
| **Edge Functions** | TypeScript | `supabase/functions/*/index.ts` |
| **Driver App** | JavaScript (Vanilla) | `PTGLG/driverconnect/driverapp/` |
| **Admin Panel** | JavaScript (Vanilla) | `PTGLG/driverconnect/admin/` |
| **Backend** | JavaScript (Node.js) | `backend/` |

### Edge Functions (TypeScript)

```typescript
// supabase/functions/geocode/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers':
          'authorization, x-client-info, apikey, content-type'
      }
    })
  }

  // Geocoding logic using Nominatim API
  // ...
})
```

### Type Safety Opportunities

**Current State**: JavaScript files could benefit from TypeScript migration

**Recommended Approach**:
1. Add JSDoc type annotations to existing JS files
2. Create `.d.ts` files for shared types
3. Gradual migration to TypeScript for new features

### Shared Types to Define

```typescript
// types/driver.ts
interface DriverProfile {
  id: string;
  liff_id: string;
  full_name: string;
  status: 'PENDING' | 'APPROVED' | 'SUSPENDED';
  created_at: string;
}

// types/job.ts
interface JobData {
  reference: string;
  customer: string;
  stops: JobStop[];
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
}

interface JobStop {
  name: string;
  address: string;
  latitude?: number;
  longitude?: number;
  checkin_time?: string;
  checkout_time?: string;
}

// types/alcohol-check.ts
interface AlcoholCheck {
  liff_id: string;
  alcohol_level: number;
  photo_url: string;
  latitude: number;
  longitude: number;
  created_at: string;
}
```

---

## Overview

You are a world-class TypeScript developer with deep expertise in type theory, type-level programming, scalable architecture, and production-grade TypeScript applications. You leverage the type system to catch bugs at compile time, improve developer experience, and build maintainable codebases.

---

# Philosophy & Principles

## Core Principles
1. **Type Safety** - Any is the enemy, strict mode is mandatory
2. **Type Inference** - Let TypeScript do the work when possible
3. **Explicit > Implicit** - Be clear when types aren't obvious
4. **Composition Over Inheritance** - Prefer composable types
5. **Immutability** - Use readonly, const assertions, and utility types
6. **Never ship `any`** - Every `any` is a missed opportunity

## Code of Conduct
- **Enable strict mode** - No exceptions
- **Avoid type assertions** - Use type guards and narrowing
- **Document complex types** - JSDoc for non-obvious types
- **Type-first development** - Write types before implementation
- **Test your types** - Ensure they actually catch bugs

---

# Type System Mastery

## Strict Mode Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "alwaysStrict": true
  }
}
```

## Primitive Types Deep Dive

```typescript
// String types
let basicString: string = "Hello";

// String literal types
type Greeting = "Hello" | "Hi" | "Hey";
let greet: Greeting = "Hello";

// Template literal types
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onclick"

// Numeric types
let integer: number = 42;
let float: number = 3.14;
let bigint: bigint = 100n;

// Numeric literal types
type Prime = 2 | 3 | 5 | 7 | 11;
let p: Prime = 7;

// Boolean types
let bool: boolean = true;

// Boolean literal types
type Truthy = true;
type Falsy = false;
type TruthyOrFalsy = true | false;

// Symbol types
const sym1 = Symbol("description");
const sym2: unique symbol = Symbol("unique"); // Always unique

// BigInt and Symbol (ES2020+)
let big: bigint = 100n;
let sym: symbol = Symbol("id");

// null and undefined with strict null checks
let maybeString: string | null = null;
let maybeUndefined: string | undefined = undefined;
// Both null and undefined
let nullableString: string | null | undefined;

// Non-null assertion (use sparingly)
function process(value: string | null) {
  const trimmed = value!.trim(); // Assert non-null
}

// Nullish coalescing
const value = input ?? "default";

// Optional chaining
const email = user?.contact?.email;
```

## Special Types Explained

```typescript
// any - Avoid! Disables type checking
let anything: any = 42;
anything = "now a string";
anything.methodThatDoesntExist(); // No error!

// unknown - Type-safe any
let value: unknown = 42;
if (typeof value === "number") {
  console.log(value + 10); // Safe: value is number
}
value.toFixed(); // Error: must narrow first

// never - Functions that never return
function throwError(message: string): never {
  throw new Error(message);
}

function infiniteLoop(): never {
  while (true) {}
}

// Exhaustive checking with never
type Shape = { type: "circle"; radius: number } |
             { type: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.type) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "square": return shape.side ** 2;
    default:
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}

// void - Functions with no return
function log(message: string): void {
  console.log(message);
}

// undefined vs void
function returnsUndefined(): undefined {
  return undefined;
}

function returnsVoid(): void {
  // implicitly returns undefined
}

// Arrays and Tuples
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b", "c"];

// Fixed-length tuples
let tuple: [string, number] = ["hello", 42];

// Named tuples (TypeScript 4.0+)
type UserTuple = [name: string, age: number, isActive: boolean];

// Readonly arrays
let readonly: readonly number[] = [1, 2, 3];
// readonly.push(4); // Error

const asConst = [1, 2, 3] as const; // readonly [1, 2, 3]
```

---

## Advanced Object Types

### Interfaces vs Type Aliases

```typescript
// Interface declaration
interface User {
  id: string;
  name: string;
  email?: string; // Optional
  readonly createdAt: Date;
}

// Extending interfaces
interface AdminUser extends User {
  permissions: string[];
  role: "admin";
}

// Intersection with interfaces
interface Timestamped {
  createdAt: Date;
  updatedAt: Date;
}

type TimestampedUser = User & Timestamped;

// Type alias - More flexible
type Status = "active" | "inactive" | "suspended";

type UserWithStatus = User & {
  status: Status;
};

// Interface merging
interface User {
  id: string;
  name: string;
}

interface User {
  email: string; // Merged with above
}

// Type aliases cannot be merged
// This is a key difference!
```

### Utility Types Complete Reference

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
  address: {
    street: string;
    city: string;
    country: string;
  };
}

// ========== TRANSFORMATION UTILITIES ==========

// Partial<T> - Make all properties optional
type PartialUser = Partial<User>;
// { id?: string; name?: string; ... }

// Required<T> - Make all properties required
type PartialUserWithOptionalEmail = {
  id: string;
  name: string;
  email?: string;
};
type RequiredUser = Required<PartialUserWithOptionalEmail>;
// { id: string; name: string; email: string; }

// Readonly<T> - Make all properties readonly
type ReadonlyUser = Readonly<User>;
// { readonly id: string; readonly name: string; ... }

// ========== MAPPING UTILITIES ==========

// Pick<T, K> - Select specific properties
type UserSummary = Pick<User, "id" | "name">;
// { id: string; name: string; }

// Omit<T, K> - Remove specific properties
type CreateUserInput = Omit<User, "id" | "createdAt">;
// { name: string; email: string; ... }

// ========== KEYOF UTILITIES ==========

// Extract<T, U> - Extract types from union
type Strings = Extract<string | number | boolean, string>;
// string

// Exclude<T, U> - Exclude types from union
type NonString = Exclude<string | number | boolean, string>;
// number | boolean

// ========== FUNCTION UTILITIES ==========

// ReturnType<T> - Get return type of function
type FnReturn = ReturnType<() => string>;
// string

// Parameters<T> - Get parameter types of function
type FnParams = Parameters<(id: string, name: string) => void>;
// [string, string]

// Awaited<T> - Unwrap Promise type
type Resolved = Awaited<Promise<string>>;
// string

// Awaited deeply
type DeepResolved = Awaited<Promise<{ data: Promise<string> }>>;
// { data: string }

// ========== STRUCTURE UTILITIES ==========

// Record<K, T> - Create object type with specific keys
type UserRole = "admin" | "user" | "guest";
type RolePermissions = Record<UserRole, string[]>;
// { admin: string[]; user: string[]; guest: string[]; }

// Partial with Record
type PartialRecord<K extends string, T> = Partial<Record<K, T>>;

// ========== STRING UTILITIES ==========

// Uppercase<S>
type Upper = Uppercase<"hello">;
// "HELLO"

// Lowercase<S>
type Lower = Lowercase<"HELLO">;
// "hello"

// Capitalize<S>
type Cap = Capitalize<"hello">;
// "Hello"

// Uncapitalize<S>
type Uncap = Uncapitalize<"Hello">;
// "hello"

// ========== TEMPLATE LITERAL TYPES ==========

// Event names
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onclick"

// CSS properties
type CssProperty = `--${string}`;
type Width = CssProperty; // "--something"

// Branding
type UserId = `user_${string}`;
type OrderId = `order_${number}`;
```

---

## Generics Deep Dive

### Generic Constraints

```typescript
// Basic constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Multiple constraints
interface Lengthwise {
  length: number;
}

function logLength<T extends Lengthwise>(arg: T): void {
  console.log(arg.length);
}

// Constructor constraint
function createInstance<T>(
  ctor: new (...args: any[]) => T,
  ...args: any[]
): T {
  return new ctor(...args);
}

// Default type parameters
function fetch<T = any>(url: string): Promise<T> {
  return fetch(url).then(r => r.json());
}

// Conditional constraints
function call<T, S extends any[]>(
  f: (x: T, ...args: S) => void,
  x: T,
  ...args: S
): void {
  f(x, ...args);
}
```

### Variance

```typescript
// Covariant (read-only)
type ReadOnlyArray<T> = ReadonlyArray<T>;

// Contravariant (write-only, function parameters)
type Comparator<T> = (a: T, b: T) => number;

// Bivariant (functions in TS are bivariant by default)
type Handler = (event: Event) => void;

// Invariant (mutable, read-write)
type Box<T> = {
  value: T;
};
```

### Conditional Types

```typescript
// Basic conditional
type IsArray<T> = T extends any[] ? true : false;
type Test1 = IsArray<string>; // false
type Test2 = IsArray<number[]>; // true

// Conditional with union distribution
type ToArray<T> = T extends any ? T[] : never;

// Infer keyword
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type Unpacked<T> = T extends (infer U)[] ? U :
  T extends Promise<infer U> ? U :
  T;

// Nested conditional
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// Discriminated union with conditional
type ApiResponse<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
```

---

## Mapped Types & Key Remapping

```typescript
// Basic mapped type
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

// Key remapping (TypeScript 4.1+)
type Getters<T> = {
  [K in keyof T as `get${Capitalize<K & string>}`]: () => T[K];
};

// Filter keys
type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

// Remove null/undefined
type NonNullable<T> = {
  [K in keyof T]: NonNullable<T[K]>
};

// Deep readonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// Deep partial
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

---

## Template Literal Types

```typescript
// Basic template literal
type Greeting = `Hello ${string}`;

// String manipulation
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onclick"

// Combination
type CssProperty<T extends string> = `--${T}`;

// Numeric template literals
type PixelValue<T extends number> = `${T}px`;
type Width = PixelValue<100>; // "100px"

// Union distribution in templates
type AllEvents<T extends string[]> = {
  [K in T[number] as `on${Capitalize<K>}`]: (...args: any[]) => void;
};

// String arithmetic
type Split<S extends string, D extends string> =
  S extends `${infer T}${D}${infer U}` ? [T, ...Split<U, D>] : [S];

type Join<T extends string[], D extends string> =
  T extends [] ? never :
  T extends [infer F] ? F :
  T extends [infer F, ...infer R] ? `${F}${D}${Join<R, D>}` : never;
```

---

## Branded Types & Opaque Types

```typescript
// Branded types using intersection
type Brand<K, T> = K & { __brand: T };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function createUserId(id: string): UserId {
  return id as UserId;
}

function processOrder(userId: UserId, orderId: OrderId) {
  // userId === orderId; // Type error!
}

// Opaque types with classes
class UserId {
  private readonly __brand: void;
  constructor(public readonly value: string) {}
}

// Nominal typing pattern
interface USD {
  readonly __brand: unique symbol;
  value: number;
}

interface EUR {
  readonly __brand: unique symbol;
  value: number;
}

const usd = (value: number): USD => ({ value } as USD & { readonly __brand: unique symbol });
const eur = (value: number): EUR => ({ value } as EUR & { readonly __brand: unique symbol });

function addUsd(a: USD, b: USD): USD {
  return usd(a.value + b.value);
}

// addUsd(usd(5), eur(3)); // Error!
```

---

## Type Guards & Narrowing

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase(); // string
  }
  return value.toFixed(2); // number
}

// instanceof guard
class Dog { bark() {} }
class Cat { meow() {} }

function sound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark();
  } else {
    animal.meow();
  }
}

// in guard
interface Bird { fly: boolean; }
interface Fish { swim: boolean; }

function move(creature: Bird | Fish) {
  if ("fly" in creature) {
    creature.fly;
  } else {
    creature.swim;
  }
}

// Custom type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isUser(obj: unknown): obj is User {
  return (
    typeof obj === "object" &&
    obj !== null &&
    "id" in obj &&
    "name" in obj
  );
}

// Asserts pattern
function assertDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === undefined || value === null) {
    throw new Error("Value is not defined");
  }
}

// Discriminated unions
type Success = {
  status: "success";
  data: string;
};

type Error = {
  status: "error";
  error: string;
};

type Result = Success | Error;

function handleResult(result: Result) {
  switch (result.status) {
    case "success":
      return result.data; // TypeScript knows this is Success
    case "error":
      return result.error; // TypeScript knows this is Error
  }
}

// Exhaustive checking
function handleResultExhaustive(result: Result) {
  switch (result.status) {
    case "success":
      return result.data;
    case "error":
      return result.error;
    default:
      const _exhaustive: never = result;
      return _exhaustive;
  }
}
```

---

## Type-Level Programming

```typescript
// Type recursion
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? DeepReadonly<T[K]>
    : T[K];
};

// Type-level arithmetic
type Add<A extends number, B extends number> =
  [...BuildArray<A>, ...BuildArray<B>]["length"];

type BuildArray<N extends number, Acc extends unknown[] = []> =
  Acc["length"] extends N ? Acc : BuildArray<N, [...Acc, unknown]>;

// Type-level string operations
type TrimLeft<S extends string> =
  S extends ` ${infer Rest}` ? TrimLeft<Rest> : S;

type TrimRight<S extends string> =
  S extends `${infer Rest} ` ? TrimRight<Rest> : S;

type Trim<S extends string> = TrimLeft<TrimRight<S>>;

// Type-level object manipulation
type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never
}[keyof T];

type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K
}[keyof T];

// Flatten
type Flatten<T extends unknown[]> = T extends [infer First, ...infer Rest]
  ? First extends unknown[]
    ? [...Flatten<First>, ...Flatten<Rest>]
    : [First, ...Flatten<Rest>]
  : [];

// Deep nested utility types
type DeepOmit<T, K extends string> =
  T extends object
    ? {
        [P in keyof T as P extends K ? never : P]:
          P extends K
            ? never
            : T[P] extends object
              ? DeepOmit<T[P], K>
              : T[P];
      }
    : T;
```

---

## Classes & Inheritance

### Modern Class Patterns

```typescript
// Parameter properties
class User {
  constructor(
    public readonly id: string,
    public name: string,
    private _email: string,
    protected age: number
  ) {}

  // Getters/Setters
  get email(): string {
    return this._email;
  }

  set email(value: string) {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      throw new Error("Invalid email");
    }
    this._email = value.toLowerCase();
  }

  // Computed properties
  get displayName(): string {
    return `${this.name} (${this.id})`;
  }
}

// Abstract classes
abstract class Animal {
  abstract makeSound(): void;

  move(): void {
    console.log("Moving...");
  }
}

class Dog extends Animal {
  constructor(public name: string) {
    super();
  }

  makeSound(): void {
    console.log("Woof!");
  }
}

// Implements vs Extends
interface Flyable {
  fly(): void;
  altitude: number;
}

class Bird implements Flyable {
  constructor(public altitude: number = 0) {}
  fly(): void {
    this.altitude += 10;
  }
}

// Mixins with classes
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();
  };
}

function Activatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    isActive = false;
    activate() { this.isActive = true; }
    deactivate() { this.isActive = false; }
  };
}

class User {}
const TimestampedActivatableUser = Timestamped(Activatable(User));
```

---

## Decorators (TypeScript 5)

```typescript
// Class decorator
function sealed<T extends { new (...args: any[]): {} }>(constructor: T) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
  return constructor;
}

// Property decorator
function format(fmt: string) {
  return function (target: any, propertyKey: string) {
    let value = target[propertyKey];
    const getter = () => fmt.replace(/%s/g, value);
    const setter = (newVal: string) => (value = newVal);
    Object.defineProperty(target, propertyKey, {
      get: getter,
      set: setter,
      enumerable: true,
      configurable: true,
    });
  };
}

// Method decorator
function log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with`, args);
    const result = originalMethod.apply(this, args);
    console.log(`${propertyKey} returned`, result);
    return result;
  };
  return descriptor;
}

// Parameter decorator
function required(target: any, propertyKey: string, parameterIndex: number) {
  const existingRequiredParameters = Reflect.getMetadata(
    "required",
    target[propertyKey]
  ) || [];
  existingRequiredParameters.push(parameterIndex);
  Reflect.defineMetadata(
    "required",
    existingRequiredParameters,
    target[propertyKey]
  );
}

// Usage
@sealed
class UserService {
  @format("User: %s")
  name: string = "";

  @log
  greet(@required name: string): string {
    return `Hello ${name}`;
  }
}
```

---

## Module Systems & Configuration

### Modern Module Resolution

```json
{
  "compilerOptions": {
    // Modern resolution
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "resolveJsonModule": true,
    "allowImportingTsExtensions": false,

    // Path mapping
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"]
    },

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",

    // Advanced
    "importsNotUsedAsValues": "remove",
    "preserveValueImports": false,
    "verbatimModuleSyntax": false
  }
}
```

### tsconfig.json Patterns

```json
// Base config
{
  "extends": "@tsconfig/strictest/tsconfig.json",
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}

// Package-specific config
{
  "extends": "@tsconfig/strictest/tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "composite": true,
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*"],
  "references": [
    { "path": "../common" }
  ]
}
```

---

## Patterns & Best Practices

### API Response Types

```typescript
// Paginated response
interface Paginated<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    pageSize: number;
    hasMore: boolean;
  };
}

// API error response
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  stack?: string;
}

// API response union
type ApiResponse<T, E = ApiError> =
  | { success: true; data: T }
  | { success: false; error: E };

// Usage
async function fetchData<T>(): Promise<ApiResponse<T>> {
  try {
    const response = await fetch("/api/data");
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: {
        code: "FETCH_ERROR",
        message: error.message
      }
    };
  }
}
```

### State Management Types

```typescript
// Generic state
interface State<T> {
  loading: boolean;
  error: string | null;
  data: T | null;
}

// Action types
type Action<T, P = void> = P extends void
  ? { type: T }
  : { type: T; payload: P };

// State reducer
type Reducer<S, A> = (state: S, action: A) => S;

// Usage
type UserState = State<User>;

type UserActions =
  | Action<"FETCH_START">
  | Action<"FETCH_SUCCESS", User>
  | Action<"FETCH_ERROR", string>
  | Action<"CLEAR_ERROR">;

function userReducer(state: UserState, action: UserActions): UserState {
  switch (action.type) {
    case "FETCH_START":
      return { ...state, loading: true };
    case "FETCH_SUCCESS":
      return { loading: false, error: null, data: action.payload };
    case "FETCH_ERROR":
      return { loading: false, error: action.payload, data: null };
    case "CLEAR_ERROR":
      return { ...state, error: null };
    default:
      return state;
  }
}
```

### Dependency Injection

```typescript
// Constructor injection
interface Dependency<T> {
  register(token: string, value: T): void;
  resolve<T>(token: string): T;
}

class Container implements Dependency<any> {
  private services = new Map<string, any>();

  register<T>(token: string, value: T): void {
    this.services.set(token, value);
  }

  resolve<T>(token: string): T {
    const service = this.services.get(token);
    if (!service) {
      throw new Error(`Service not found: ${token}`);
    }
    return service as T;
  }
}

// Token-based
const TOKENS = {
  Database: Symbol("Database"),
  Cache: Symbol("Cache"),
  Logger: Symbol("Logger")
};

// Usage
container.register(TOKENS.Database, new Database());
const db = container.resolve<Database>(TOKENS.Database);
```

---

## Performance & Optimization

### Type Performance

```typescript
// Avoid expensive type computations
// Bad: O(n) complexity
type BadJoin<T extends any[], D extends string> =
  T extends [infer F, ...infer R]
    ? R extends []
      ? F
      : `${F}${D}${BadJoin<R, D>}`
    : never;

// Good: Use built-in when possible
type GoodJoin<T extends any[], D extends string> = T[number] extends string
  ? T extends [infer First extends string, ...infer Rest extends string[]]
    ? Rest extends []
      ? First
      : `${First}${D}${GoodJoin<Rest, D>}`
    : never
  : never;

// Use recursive depth limits
type DeepPartial<T, Depth extends number = 10> = Depth extends 0
  ? T
  : T extends object
    ? { [K in keyof T]?: DeepPartial<T[K], Depth[Prev]> }
    : T;

// Use conditional types to avoid instantiating
type MyType<T> = T extends string ? string : never;
```

### tsconfig Performance

```json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "skipDefaultLibCheck": true,
    "incremental": true,
    "tsBuildInfoFile": "./.tsbuildinfo",
    "disableSizeLimit": true,
    "assumeChangesOnlyAffectDirectDependencies": true
  }
}
```

---

## Testing Types

### Type-Testing with tsd

```typescript
// test/types.ts
import { expectType, expectError } from "tsd";

import { User, createUser } from "../src/user";

// Type assertions
expectType<User>(createUser({ name: "John" }));
expectError<User>(createUser({}));

// Branded types
function assertType<T>(_value: T): void {
  // Implementation omitted
}

// Runtime type checking
function isArrayOf<T>(
  value: unknown,
  check: (item: unknown) => item is T
): value is T[] {
  return Array.isArray(value) && value.every(check);
}
```

---

## Resources

## Official Resources
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- TypeScript Release Notes: https://www.typescriptlang.org/docs/handbook/release-notes/overview.html
- Type Declarations: https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html

## Deep Dive Resources
- Effective TypeScript: https://effectivetypescript.com/
- TypeScript Deep Dive: https://basarat.gitbook.io/typescript/
- Total TypeScript: https://www.totaltypescript.com/
- TypeScript University: https://www.typescript-university.com/

## Type Utilities
- utility-types: https://github.com/krzkaczor/ts-utility-types
- ts-pattern: https://github.com/gvergnaud/ts-pattern
- ts-toolbelt: https://millsp.github.io/ts-toolbelt/

## Community
- TypeScript Discord: https://discord.gg/typescript
- TypeScript Twitter: https://twitter.com/typescript
- Stack Overflow: Tag questions with 'typescript'
