---
name: typescript-expert
description: Эксперт по TypeScript. Используй для типизации, дженериков, декораторов, паттернов проектирования и best practices в TypeScript.
---

# TypeScript Expert

Глубокая экспертиза в системе типов TypeScript, продвинутых паттернах и best practices.

## Core Principles

### Foundational Guidelines

```yaml
typescript_principles:
  - name: "Type Safety Priority"
    guideline: "Always prefer strict type checking and avoid `any` type"
    reason: "Catch errors at compile time, not runtime"

  - name: "Smart Inference"
    guideline: "Let TypeScript infer types when they're obvious"
    reason: "Reduce noise while maintaining safety"

  - name: "Immutability Preference"
    guideline: "Use readonly and as const for unchangeable data"
    reason: "Prevent accidental mutations"

  - name: "Discriminated Unions"
    guideline: "Apply tagged unions for managing complex state"
    reason: "Exhaustive type checking and better DX"

  - name: "Explicit Public APIs"
    guideline: "Always type public function signatures explicitly"
    reason: "Documentation and contract enforcement"
```

---

## Type System Fundamentals

### Basic Types

```typescript
// Primitive types
const name: string = "John";
const age: number = 30;
const isActive: boolean = true;
const nothing: null = null;
const notDefined: undefined = undefined;
const unique: symbol = Symbol("id");
const bigNumber: bigint = 9007199254740991n;

// Arrays
const numbers: number[] = [1, 2, 3];
const strings: Array<string> = ["a", "b", "c"];
const readonly: readonly number[] = [1, 2, 3]; // immutable

// Tuples
const tuple: [string, number] = ["age", 30];
const namedTuple: [name: string, age: number] = ["John", 30];
const optionalTuple: [string, number?] = ["John"];
const restTuple: [string, ...number[]] = ["sum", 1, 2, 3];

// Objects
const user: { name: string; age: number } = { name: "John", age: 30 };
const optionalProps: { name: string; age?: number } = { name: "John" };
const readonlyObj: Readonly<{ name: string }> = { name: "John" };
```

### Union and Intersection Types

```typescript
// Union types (OR)
type Status = "pending" | "active" | "completed";
type StringOrNumber = string | number;

// Intersection types (AND)
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged; // { name: string; age: number }

// Discriminated unions (tagged unions)
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>): T | null {
  if (result.success) {
    return result.data; // TypeScript knows data exists
  }
  console.error(result.error); // TypeScript knows error exists
  return null;
}

// Exhaustive checking
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rectangle"; width: number; height: number };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "rectangle":
      return shape.width * shape.height;
    default:
      // Exhaustive check - compiler error if case is missing
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}
```

---

## Advanced Type System

### Generics

```typescript
// Basic generics
function identity<T>(value: T): T {
  return value;
}

// Multiple type parameters
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

// Generic constraints
interface Lengthwise {
  length: number;
}

function logLength<T extends Lengthwise>(item: T): T {
  console.log(item.length);
  return item;
}

// Generic with default type
interface Container<T = string> {
  value: T;
}

// Constrained generics
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic classes
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }
}

// Generic with multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

### Utility Types

```typescript
// Built-in utility types
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<PartialUser>;

// Readonly - all properties readonly
type ReadonlyUser = Readonly<User>;

// Pick - select specific properties
type UserCredentials = Pick<User, "email" | "password">;

// Omit - exclude specific properties
type PublicUser = Omit<User, "password">;

// Record - create object type with specific keys
type UserRoles = Record<string, "admin" | "user" | "guest">;

// Exclude - exclude types from union
type NonNullableString = Exclude<string | null | undefined, null | undefined>;

// Extract - extract types from union
type StringsOnly = Extract<string | number | boolean, string>;

// NonNullable - remove null and undefined
type NonNullUser = NonNullable<User | null | undefined>;

// ReturnType - get function return type
function createUser() {
  return { id: 1, name: "John" };
}
type UserReturn = ReturnType<typeof createUser>;

// Parameters - get function parameters as tuple
type CreateUserParams = Parameters<typeof createUser>;

// ConstructorParameters - get constructor parameters
class UserClass {
  constructor(public name: string, public age: number) {}
}
type UserConstructorParams = ConstructorParameters<typeof UserClass>;

// InstanceType - get instance type from constructor
type UserInstance = InstanceType<typeof UserClass>;

// Awaited - unwrap Promise type
type ResolvedUser = Awaited<Promise<User>>;
```

### Conditional Types

```typescript
// Basic conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false

// Conditional type with infer
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type Resolved = UnwrapPromise<Promise<string>>; // string
type NotPromise = UnwrapPromise<number>; // number

// Extract return type from function
type GetReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Extract array element type
type ArrayElement<T> = T extends (infer E)[] ? E : never;
type Element = ArrayElement<string[]>; // string

// Distributive conditional types
type ToArray<T> = T extends any ? T[] : never;
type Distributed = ToArray<string | number>; // string[] | number[]

// Non-distributive (wrap in tuple)
type ToArrayNonDistributive<T> = [T] extends [any] ? T[] : never;
type NonDistributed = ToArrayNonDistributive<string | number>; // (string | number)[]

// Practical example: Deep readonly
type DeepReadonly<T> = T extends (infer U)[]
  ? DeepReadonlyArray<U>
  : T extends object
  ? DeepReadonlyObject<T>
  : T;

interface DeepReadonlyArray<T> extends ReadonlyArray<DeepReadonly<T>> {}

type DeepReadonlyObject<T> = {
  readonly [P in keyof T]: DeepReadonly<T[P]>;
};
```

### Template Literal Types

```typescript
// Basic template literals
type Greeting = `Hello, ${string}!`;
type ValidGreeting = "Hello, World!"; // valid
// type InvalidGreeting: "Hi, World!" // error

// Event names
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"

// CSS units
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;

const width: CSSValue = "100px"; // valid
const height: CSSValue = "50%"; // valid

// Getter/Setter patterns
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type Setters<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => void;
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }

// Route patterns
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type Route = `/${string}`;
type Endpoint = `${HTTPMethod} ${Route}`;

const endpoint: Endpoint = "GET /users"; // valid
```

### Mapped Types

```typescript
// Basic mapped type
type Optional<T> = {
  [K in keyof T]?: T[K];
};

// Mapped type with modifier removal
type Concrete<T> = {
  [K in keyof T]-?: T[K]; // remove optional
};

type Mutable<T> = {
  -readonly [K in keyof T]: T[K]; // remove readonly
};

// Key remapping
type PrefixedKeys<T, P extends string> = {
  [K in keyof T as `${P}${Capitalize<string & K>}`]: T[K];
};

interface Config {
  host: string;
  port: number;
}

type PrefixedConfig = PrefixedKeys<Config, "server">;
// { serverHost: string; serverPort: number }

// Filter keys by value type
type FilterByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  active: boolean;
  email: string;
}

type StringProps = FilterByType<Mixed, string>;
// { name: string; email: string }

// Nullable all properties
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// Create event handlers
type EventHandlers<T> = {
  [K in keyof T as `on${Capitalize<string & K>}Change`]: (newValue: T[K]) => void;
};

type PersonHandlers = EventHandlers<Person>;
// { onNameChange: (newValue: string) => void; onAgeChange: (newValue: number) => void }
```

---

## Type Guards

### Built-in Type Guards

```typescript
// typeof guard
function processValue(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase(); // TypeScript knows it's string
  }
  return value.toFixed(2); // TypeScript knows it's number
}

// instanceof guard
class Dog {
  bark() {
    console.log("Woof!");
  }
}

class Cat {
  meow() {
    console.log("Meow!");
  }
}

function speak(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark();
  } else {
    animal.meow();
  }
}

// in operator guard
interface Fish {
  swim: () => void;
}

interface Bird {
  fly: () => void;
}

function move(animal: Fish | Bird) {
  if ("swim" in animal) {
    animal.swim();
  } else {
    animal.fly();
  }
}
```

### Custom Type Guards

```typescript
// Type predicate function
interface Admin {
  role: "admin";
  permissions: string[];
}

interface User {
  role: "user";
  email: string;
}

type Person = Admin | User;

function isAdmin(person: Person): person is Admin {
  return person.role === "admin";
}

function handlePerson(person: Person) {
  if (isAdmin(person)) {
    console.log(person.permissions); // Admin type
  } else {
    console.log(person.email); // User type
  }
}

// Assertion function
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("Value must be a string");
  }
}

function processInput(input: unknown) {
  assertIsString(input);
  console.log(input.toUpperCase()); // TypeScript knows it's string
}

// Non-null assertion
function assertDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("Value must be defined");
  }
}
```

---

## Function Types

### Function Signatures

```typescript
// Function type annotation
type MathOperation = (a: number, b: number) => number;

const add: MathOperation = (a, b) => a + b;
const subtract: MathOperation = (a, b) => a - b;

// Call signatures in interfaces
interface Calculator {
  (a: number, b: number): number;
  description: string;
}

const multiply: Calculator = Object.assign(
  (a: number, b: number) => a * b,
  { description: "Multiplies two numbers" }
);

// Overloads
function createElement(tag: "a"): HTMLAnchorElement;
function createElement(tag: "canvas"): HTMLCanvasElement;
function createElement(tag: "table"): HTMLTableElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const anchor = createElement("a"); // HTMLAnchorElement
const canvas = createElement("canvas"); // HTMLCanvasElement

// Generic function with constraints
function firstElement<T extends { length: number }>(arr: T): T[0] | undefined {
  return arr[0];
}

// Function with this parameter
interface Button {
  label: string;
  click(this: Button): void;
}

const button: Button = {
  label: "Submit",
  click() {
    console.log(this.label);
  },
};
```

### Rest Parameters and Spread

```typescript
// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((acc, n) => acc + n, 0);
}

// Typed rest parameters
function formatMessage(template: string, ...values: (string | number)[]): string {
  return values.reduce<string>(
    (msg, val, i) => msg.replace(`{${i}}`, String(val)),
    template
  );
}

// Variadic tuple types
type Concat<T extends unknown[], U extends unknown[]> = [...T, ...U];

type Result = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]

// Labeled tuple elements
function readButtonInput(...args: [name: string, version: number, ...input: boolean[]]) {
  const [name, version, ...input] = args;
}
```

---

## Classes and OOP

### Class Fundamentals

```typescript
class Animal {
  // Property declarations
  public name: string;
  protected species: string;
  private _age: number;
  readonly id: string;

  // Static members
  static kingdom = "Animalia";

  // Constructor
  constructor(name: string, species: string, age: number) {
    this.name = name;
    this.species = species;
    this._age = age;
    this.id = crypto.randomUUID();
  }

  // Getters and setters
  get age(): number {
    return this._age;
  }

  set age(value: number) {
    if (value < 0) throw new Error("Age cannot be negative");
    this._age = value;
  }

  // Methods
  speak(): void {
    console.log(`${this.name} makes a sound`);
  }

  // Static methods
  static isAnimal(obj: unknown): obj is Animal {
    return obj instanceof Animal;
  }
}

// Inheritance
class Dog extends Animal {
  breed: string;

  constructor(name: string, age: number, breed: string) {
    super(name, "Canis familiaris", age);
    this.breed = breed;
  }

  // Override method
  override speak(): void {
    console.log(`${this.name} barks!`);
  }
}
```

### Abstract Classes

```typescript
abstract class Shape {
  abstract readonly name: string;
  abstract getArea(): number;
  abstract getPerimeter(): number;

  // Concrete method
  describe(): string {
    return `This is a ${this.name} with area ${this.getArea()}`;
  }
}

class Circle extends Shape {
  readonly name = "circle";

  constructor(public radius: number) {
    super();
  }

  getArea(): number {
    return Math.PI * this.radius ** 2;
  }

  getPerimeter(): number {
    return 2 * Math.PI * this.radius;
  }
}

class Rectangle extends Shape {
  readonly name = "rectangle";

  constructor(public width: number, public height: number) {
    super();
  }

  getArea(): number {
    return this.width * this.height;
  }

  getPerimeter(): number {
    return 2 * (this.width + this.height);
  }
}
```

### Interfaces vs Types for Classes

```typescript
// Interface for class implementation
interface Serializable {
  serialize(): string;
  deserialize(data: string): void;
}

interface Comparable<T> {
  compareTo(other: T): number;
}

class User implements Serializable, Comparable<User> {
  constructor(public id: number, public name: string) {}

  serialize(): string {
    return JSON.stringify({ id: this.id, name: this.name });
  }

  deserialize(data: string): void {
    const parsed = JSON.parse(data);
    this.id = parsed.id;
    this.name = parsed.name;
  }

  compareTo(other: User): number {
    return this.id - other.id;
  }
}

// Mixins pattern
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();

    touch() {
      this.updatedAt = new Date();
    }
  };
}

function Activatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    isActive = false;

    activate() {
      this.isActive = true;
    }

    deactivate() {
      this.isActive = false;
    }
  };
}

class BaseEntity {
  id = crypto.randomUUID();
}

const TimestampedActivatableEntity = Timestamped(Activatable(BaseEntity));
const entity = new TimestampedActivatableEntity();
entity.activate();
entity.touch();
```

---

## Module System

### Export Patterns

```typescript
// Named exports
export const API_URL = "https://api.example.com";
export type UserID = string;
export interface User {
  id: UserID;
  name: string;
}

export function fetchUser(id: UserID): Promise<User> {
  return fetch(`${API_URL}/users/${id}`).then((r) => r.json());
}

// Default export
export default class UserService {
  async getUser(id: string): Promise<User> {
    return fetchUser(id);
  }
}

// Re-exports
export { User as UserModel } from "./user";
export * from "./types";
export * as utils from "./utils";

// Type-only exports
export type { User, UserID };
```

### Declaration Files

```typescript
// types.d.ts - Ambient declarations

// Declare module for untyped package
declare module "untyped-library" {
  export function doSomething(value: string): number;
  export const version: string;
}

// Extend existing module
declare module "express" {
  interface Request {
    user?: {
      id: string;
      role: string;
    };
  }
}

// Global declarations
declare global {
  interface Window {
    myApp: {
      version: string;
      config: Record<string, unknown>;
    };
  }

  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: "development" | "production" | "test";
      API_URL: string;
      DATABASE_URL: string;
    }
  }
}

// Ambient namespace
declare namespace MyNamespace {
  interface Config {
    apiKey: string;
    baseUrl: string;
  }

  function initialize(config: Config): void;
}
```

---

## Best Practices

### Error Handling

```typescript
// Result type pattern
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

async function fetchUser(id: string): Promise<Result<User, string>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      return err(`HTTP ${response.status}: ${response.statusText}`);
    }
    const user = await response.json();
    return ok(user);
  } catch (e) {
    return err(e instanceof Error ? e.message : "Unknown error");
  }
}

// Usage
async function handleUser(id: string) {
  const result = await fetchUser(id);

  if (result.ok) {
    console.log(result.value.name);
  } else {
    console.error(result.error);
  }
}
```

### Immutability Patterns

```typescript
// as const for literal types
const config = {
  api: {
    url: "https://api.example.com",
    timeout: 5000,
  },
  features: ["auth", "analytics"],
} as const;

type Config = typeof config;
type Feature = (typeof config.features)[number]; // "auth" | "analytics"

// Readonly utilities
interface State {
  user: User | null;
  items: Item[];
  settings: Settings;
}

type ImmutableState = Readonly<State>;
type DeepImmutableState = {
  readonly [K in keyof State]: Readonly<State[K]>;
};

// Immutable update pattern
function updateState<T extends object, K extends keyof T>(
  state: T,
  key: K,
  value: T[K]
): T {
  return { ...state, [key]: value };
}
```

### Strict Null Checks

```typescript
// Handling nullable values
function processUser(user: User | null | undefined): string {
  // Optional chaining
  const name = user?.name ?? "Anonymous";

  // Nullish coalescing
  const email = user?.email ?? "no-email@example.com";

  // Non-null assertion (use sparingly!)
  // const id = user!.id;

  return `${name} (${email})`;
}

// Type narrowing
function getLength(value: string | null): number {
  if (value === null) {
    return 0;
  }
  return value.length; // TypeScript knows it's string
}

// Assert non-null with custom message
function assertNonNull<T>(
  value: T | null | undefined,
  message: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}
```

---

## tsconfig.json Best Practices

```json
{
  "compilerOptions": {
    // Strict type checking
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "alwaysStrict": true,

    // Additional checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    // Module resolution
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],

    // Output
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "resolveJsonModule": true,

    // Path mapping
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

---

## Лучшие практики

1. **Включай strict mode** — это основа type safety
2. **Избегай any** — используй unknown для неизвестных типов
3. **Явно типизируй публичные API** — функции, классы, интерфейсы
4. **Используй discriminated unions** для сложных состояний
5. **Применяй readonly** для иммутабельных данных
6. **Создавай type guards** вместо type assertions
7. **Используй template literal types** для строковых паттернов
8. **Организуй типы в отдельные файлы** — .types.ts, index.d.ts
