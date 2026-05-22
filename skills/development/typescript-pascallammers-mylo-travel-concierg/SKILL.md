---
name: typescript
description: Auto-activates when user mentions TypeScript, types, interfaces, generics, or type safety. Expert in TypeScript best practices including advanced types, utility types, and strict mode configuration.
category: language
---

# TypeScript Best Practices

**Official TypeScript guidelines - Generics, utility types, advanced types, strict mode**

## Core Principles

1. **ALWAYS Use Strict Mode** - Enable `strict: true` in tsconfig.json
2. **Avoid `any`** - Use `unknown`, generics, or proper types
3. **Leverage Inference** - Let TypeScript infer when possible
4. **Generics for Reusability** - Make functions and components type-safe and reusable
5. **Utility Types** - Use built-in helpers like `Partial`, `Pick`, `Omit`, `ReturnType`

## Strict Mode Configuration

### ✅ Good: tsconfig.json with Strict Mode
```json
{
  "compilerOptions": {
    "strict": true,                          // Enable all strict checks
    "noUncheckedIndexedAccess": true,       // Index signatures return T | undefined
    "noImplicitOverride": true,             // Require override keyword
    "exactOptionalPropertyTypes": true,     // Distinguish undefined vs optional
    "noFallthroughCasesInSwitch": true,    // Prevent switch fallthrough
    "noUnusedLocals": true,                // Error on unused locals
    "noUnusedParameters": true,            // Error on unused parameters
    "noImplicitReturns": true,             // All code paths must return
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}
```

### ❌ Bad: Loose Configuration
```json
{
  "compilerOptions": {
    "strict": false,                 // ❌ Disables important checks
    "noImplicitAny": false,         // ❌ Allows implicit any
    "strictNullChecks": false       // ❌ Null/undefined issues
  }
}
```

## Avoiding `any`

### ✅ Good: Use `unknown` for Unknown Types
```typescript
// ✅ unknown requires type checking before use
function processData(data: unknown) {
  if (typeof data === 'string') {
    return data.toUpperCase()  // OK - type narrowed
  }
  
  if (typeof data === 'number') {
    return data.toFixed(2)     // OK - type narrowed
  }
  
  throw new Error('Unsupported type')
}

// ✅ Type guard for objects
function isUser(value: unknown): value is { name: string; age: number } {
  return (
    typeof value === 'object' &&
    value !== null &&
    'name' in value &&
    'age' in value &&
    typeof value.name === 'string' &&
    typeof value.age === 'number'
  )
}

function greetUser(data: unknown) {
  if (isUser(data)) {
    console.log(`Hello ${data.name}, age ${data.age}`)  // OK - type guarded
  }
}
```

### ❌ Bad: Using `any`
```typescript
// ❌ any bypasses type checking
function processData(data: any) {
  return data.toUpperCase()  // No error if data is not a string!
}

processData(123)  // Runtime error!
```

## Generics - Complete Guide

### ✅ Good: Generic Functions
```typescript
// Simple generic function
function identity<T>(value: T): T {
  return value
}

const num = identity(42)        // T inferred as number
const str = identity('hello')   // T inferred as string

// Generic array function
function firstElement<T>(arr: T[]): T | undefined {
  return arr[0]
}

const first = firstElement([1, 2, 3])     // number | undefined
const firstStr = firstElement(['a', 'b']) // string | undefined

// Multiple type parameters
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second]
}

const p1 = pair('hello', 42)      // [string, number]
const p2 = pair(true, 'world')    // [boolean, string]
```

### ✅ Good: Generic Constraints
```typescript
// Constraint: T must have length property
function logLength<T extends { length: number }>(value: T): void {
  console.log(value.length)
}

logLength('hello')       // OK - string has length
logLength([1, 2, 3])     // OK - array has length
logLength({ length: 5 }) // OK - object has length
// logLength(123)        // Error - number doesn't have length

// Constraint: T extends specific types
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 }
}

const merged = merge({ a: 1 }, { b: 2 })  // { a: number, b: number }

// Constraint: keyof for object keys
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

const user = { name: 'Alice', age: 30 }
const name = getProperty(user, 'name')  // string
const age = getProperty(user, 'age')    // number
// getProperty(user, 'invalid')         // Error
```

### ✅ Good: Generic Classes
```typescript
class Box<T> {
  private value: T

  constructor(value: T) {
    this.value = value
  }

  getValue(): T {
    return this.value
  }

  setValue(value: T): void {
    this.value = value
  }
}

const numberBox = new Box(123)
const stringBox = new Box('hello')

// Generic with constraints
class Collection<T extends { id: string }> {
  private items: T[] = []

  add(item: T): void {
    this.items.push(item)
  }

  findById(id: string): T | undefined {
    return this.items.find(item => item.id === id)
  }
}

const users = new Collection<{ id: string; name: string }>()
users.add({ id: '1', name: 'Alice' })
```

### ✅ Good: Generic Interfaces
```typescript
interface Repository<T> {
  getAll(): Promise<T[]>
  getById(id: string): Promise<T | null>
  create(item: Omit<T, 'id'>): Promise<T>
  update(id: string, item: Partial<T>): Promise<T>
  delete(id: string): Promise<void>
}

interface User {
  id: string
  name: string
  email: string
}

class UserRepository implements Repository<User> {
  async getAll(): Promise<User[]> {
    // Implementation
    return []
  }

  async getById(id: string): Promise<User | null> {
    // Implementation
    return null
  }

  async create(item: Omit<User, 'id'>): Promise<User> {
    // Implementation
    return { id: '1', ...item }
  }

  async update(id: string, item: Partial<User>): Promise<User> {
    // Implementation
    return { id, name: '', email: '', ...item }
  }

  async delete(id: string): Promise<void> {
    // Implementation
  }
}
```

### ✅ Good: Generic Default Parameters
```typescript
interface Response<T = unknown> {
  data: T
  status: number
  message: string
}

// Use with explicit type
const userResponse: Response<User> = {
  data: { id: '1', name: 'Alice', email: 'alice@example.com' },
  status: 200,
  message: 'Success'
}

// Use with default (unknown)
const genericResponse: Response = {
  data: { anything: 'goes' },
  status: 200,
  message: 'Success'
}
```

## Utility Types

### ✅ Good: Partial<T> - Make All Properties Optional
```typescript
interface User {
  id: string
  name: string
  email: string
  age: number
}

function updateUser(id: string, updates: Partial<User>) {
  // All properties optional
}

updateUser('1', { name: 'Bob' })             // OK
updateUser('1', { name: 'Bob', age: 25 })    // OK
updateUser('1', {})                          // OK
```

### ✅ Good: Required<T> - Make All Properties Required
```typescript
interface Config {
  apiUrl?: string
  timeout?: number
  retries?: number
}

const defaultConfig: Required<Config> = {
  apiUrl: 'https://api.example.com',  // Now required
  timeout: 5000,                      // Now required
  retries: 3                          // Now required
}
```

### ✅ Good: Pick<T, K> - Select Specific Properties
```typescript
interface User {
  id: string
  name: string
  email: string
  password: string
  createdAt: Date
}

// Pick only specific properties
type UserProfile = Pick<User, 'id' | 'name' | 'email'>

const profile: UserProfile = {
  id: '1',
  name: 'Alice',
  email: 'alice@example.com'
  // password not included
}
```

### ✅ Good: Omit<T, K> - Exclude Specific Properties
```typescript
interface User {
  id: string
  name: string
  email: string
  password: string
}

// Omit password
type SafeUser = Omit<User, 'password'>

const safeUser: SafeUser = {
  id: '1',
  name: 'Alice',
  email: 'alice@example.com'
  // password excluded
}

// Omit multiple properties
type UserInput = Omit<User, 'id' | 'createdAt'>
```

### ✅ Good: Record<K, T> - Object with Specific Keys/Values
```typescript
// Record with string keys
type UserRoles = Record<string, boolean>

const roles: UserRoles = {
  admin: true,
  editor: false,
  viewer: true
}

// Record with literal keys
type Status = 'pending' | 'active' | 'inactive'
type StatusConfig = Record<Status, { color: string; label: string }>

const config: StatusConfig = {
  pending: { color: 'yellow', label: 'Pending' },
  active: { color: 'green', label: 'Active' },
  inactive: { color: 'red', label: 'Inactive' }
}
```

### ✅ Good: Exclude<T, U> and Extract<T, U>
```typescript
type Status = 'pending' | 'active' | 'inactive' | 'archived'

// Exclude specific values
type ActiveStatus = Exclude<Status, 'inactive' | 'archived'>
// 'pending' | 'active'

// Extract specific values
type InactiveStatus = Extract<Status, 'inactive' | 'archived'>
// 'inactive' | 'archived'

// Exclude null and undefined
type NonNullable<T> = Exclude<T, null | undefined>

type MaybeString = string | null | undefined
type DefiniteString = NonNullable<MaybeString>  // string
```

### ✅ Good: ReturnType<T> and Parameters<T>
```typescript
function createUser(name: string, age: number) {
  return { id: '1', name, age, createdAt: new Date() }
}

// Get return type
type User = ReturnType<typeof createUser>
// { id: string; name: string; age: number; createdAt: Date }

// Get parameters type
type CreateUserParams = Parameters<typeof createUser>
// [name: string, age: number]

function callCreateUser(...args: CreateUserParams) {
  return createUser(...args)
}
```

### ✅ Good: Readonly<T> and ReadonlyArray<T>
```typescript
interface Config {
  apiUrl: string
  timeout: number
}

const config: Readonly<Config> = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
}

// config.apiUrl = 'new-url'  // Error - readonly

// Readonly array
const numbers: ReadonlyArray<number> = [1, 2, 3]
// numbers.push(4)  // Error - readonly
// numbers[0] = 10  // Error - readonly
```

### ✅ Good: Awaited<T> - Unwrap Promise Type
```typescript
async function fetchUser(): Promise<{ id: string; name: string }> {
  return { id: '1', name: 'Alice' }
}

type User = Awaited<ReturnType<typeof fetchUser>>
// { id: string; name: string }

type DeepPromise = Promise<Promise<Promise<number>>>
type Unwrapped = Awaited<DeepPromise>  // number
```

## Advanced Types

### ✅ Good: Conditional Types
```typescript
// Simple conditional type
type IsString<T> = T extends string ? true : false

type A = IsString<string>   // true
type B = IsString<number>   // false

// Extract array element type
type ArrayElement<T> = T extends (infer E)[] ? E : never

type Num = ArrayElement<number[]>     // number
type Str = ArrayElement<string[]>     // string
type Never = ArrayElement<number>     // never

// Flatten nested arrays
type Flatten<T> = T extends Array<infer U> ? Flatten<U> : T

type Flat = Flatten<number[][][]>  // number
```

### ✅ Good: infer Keyword
```typescript
// Extract function return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never

// Extract first argument type
type FirstArg<T> = T extends (first: infer F, ...args: any[]) => any ? F : never

type Add = (a: number, b: number) => number
type First = FirstArg<Add>  // number

// Extract Promise value
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T

type A = UnwrapPromise<Promise<string>>  // string
type B = UnwrapPromise<number>           // number
```

### ✅ Good: Mapped Types
```typescript
// Make all properties optional
type Optional<T> = {
  [K in keyof T]?: T[K]
}

// Make all properties readonly
type Immutable<T> = {
  readonly [K in keyof T]: T[K]
}

// Make all properties nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null
}

interface User {
  id: string
  name: string
  age: number
}

type OptionalUser = Optional<User>
// { id?: string; name?: string; age?: number }

// Remove optional modifier
type Concrete<T> = {
  [K in keyof T]-?: T[K]
}

// Remove readonly modifier
type Mutable<T> = {
  -readonly [K in keyof T]: T[K]
}
```

### ✅ Good: Template Literal Types
```typescript
// String manipulation
type Greeting = `Hello, ${string}!`

const g1: Greeting = 'Hello, World!'  // OK
const g2: Greeting = 'Hello, Alice!'  // OK
// const g3: Greeting = 'Hi, Bob!'    // Error

// Event names
type EventName<T extends string> = `on${Capitalize<T>}`

type ClickEvent = EventName<'click'>  // 'onClick'
type HoverEvent = EventName<'hover'>  // 'onHover'

// Combine types
type Status = 'success' | 'error' | 'warning'
type Message = `${Status}_message`
// 'success_message' | 'error_message' | 'warning_message'

// CSS properties
type CSSProperty = `${'margin' | 'padding'}${' Top' | 'Right' | 'Bottom' | 'Left'}`
// 'marginTop' | 'marginRight' | ... | 'paddingLeft'
```

### ✅ Good: Type Guards
```typescript
// Typeof guard
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

// Instance guard
class User {
  name: string
  constructor(name: string) {
    this.name = name
  }
}

function isUser(value: unknown): value is User {
  return value instanceof User
}

// Property guard
interface Cat {
  meow(): void
}

interface Dog {
  bark(): void
}

function isCat(animal: Cat | Dog): animal is Cat {
  return 'meow' in animal
}

function makeSound(animal: Cat | Dog) {
  if (isCat(animal)) {
    animal.meow()  // OK - type narrowed to Cat
  } else {
    animal.bark()  // OK - type narrowed to Dog
  }
}

// Discriminated unions
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number }
  | { kind: 'square'; size: number }

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2
    case 'rectangle':
      return shape.width * shape.height
    case 'square':
      return shape.size ** 2
  }
}
```

## Type Assertion

### ✅ Good: Type Assertions (Use Sparingly)
```typescript
// as syntax
const input = document.getElementById('input') as HTMLInputElement
input.value = 'Hello'

// Non-null assertion
const user = users.find(u => u.id === '1')!  // Assert non-null

// Const assertion
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
} as const
// type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }

// Array const assertion
const colors = ['red', 'green', 'blue'] as const
// type: readonly ["red", "green", "blue"]
```

### ❌ Bad: Unsafe Type Assertions
```typescript
// ❌ Double assertion (almost always wrong)
const value = 'hello' as unknown as number  // Bypasses type safety!

// ❌ Asserting wrong type
const num: number = 'hello' as any as number  // Runtime error waiting to happen
```

## Function Overloads

### ✅ Good: Function Overloads
```typescript
// Overload signatures
function getValue(key: string): string
function getValue(key: number): number
function getValue(keys: string[]): string[]

// Implementation signature
function getValue(key: string | number | string[]): string | number | string[] {
  if (typeof key === 'string') {
    return 'string value'
  } else if (typeof key === 'number') {
    return 42
  } else {
    return ['value1', 'value2']
  }
}

const str = getValue('key')      // string
const num = getValue(123)        // number
const arr = getValue(['a', 'b']) // string[]
```

## Index Signatures

### ✅ Good: Index Signatures
```typescript
// String index
interface StringMap {
  [key: string]: string | number
}

const map: StringMap = {
  name: 'Alice',
  age: 30
}

// Number index (arrays)
interface NumberArray {
  [index: number]: string
}

const arr: NumberArray = ['a', 'b', 'c']

// Record type (preferred over index signature)
type UserRoles = Record<string, 'admin' | 'editor' | 'viewer'>

const roles: UserRoles = {
  alice: 'admin',
  bob: 'editor'
}
```

## Intersection and Union Types

### ✅ Good: Union Types
```typescript
type Status = 'success' | 'error' | 'loading'

function handleStatus(status: Status) {
  switch (status) {
    case 'success':
      console.log('Success!')
      break
    case 'error':
      console.log('Error!')
      break
    case 'loading':
      console.log('Loading...')
      break
  }
}

// Union with different types
type Result = { success: true; data: string } | { success: false; error: string }

function processResult(result: Result) {
  if (result.success) {
    console.log(result.data)  // OK - type narrowed
  } else {
    console.log(result.error) // OK - type narrowed
  }
}
```

### ✅ Good: Intersection Types
```typescript
interface Timestamped {
  createdAt: Date
  updatedAt: Date
}

interface User {
  id: string
  name: string
}

type TimestampedUser = User & Timestamped

const user: TimestampedUser = {
  id: '1',
  name: 'Alice',
  createdAt: new Date(),
  updatedAt: new Date()
}

// Combining multiple types
type WithId = { id: string }
type WithName = { name: string }
type WithEmail = { email: string }

type Person = WithId & WithName & WithEmail
```

## Const Assertions and Enums

### ✅ Good: Const Assertions (Preferred)
```typescript
// Const assertion for literal types
const STATUS = {
  PENDING: 'pending',
  ACTIVE: 'active',
  INACTIVE: 'inactive'
} as const

type Status = typeof STATUS[keyof typeof STATUS]
// 'pending' | 'active' | 'inactive'

function setStatus(status: Status) {
  console.log(status)
}

setStatus(STATUS.PENDING)  // OK
// setStatus('invalid')    // Error
```

### ✅ Good: Enums (When Needed)
```typescript
// String enum
enum Direction {
  Up = 'UP',
  Down = 'DOWN',
  Left = 'LEFT',
  Right = 'RIGHT'
}

function move(direction: Direction) {
  console.log(`Moving ${direction}`)
}

move(Direction.Up)

// Numeric enum
enum LogLevel {
  Debug = 0,
  Info = 1,
  Warn = 2,
  Error = 3
}

// Const enum (inlined at compile time)
const enum Color {
  Red = '#FF0000',
  Green = '#00FF00',
  Blue = '#0000FF'
}

const red: Color = Color.Red  // Inlined to '#FF0000'
```

## Modules and Namespaces

### ✅ Good: ES Modules (Preferred)
```typescript
// user.ts
export interface User {
  id: string
  name: string
}

export function createUser(name: string): User {
  return { id: '1', name }
}

// main.ts
import { User, createUser } from './user'

const user = createUser('Alice')
```

### ✅ Good: Type-Only Imports
```typescript
// Only import type, not value
import type { User } from './user'

// Or import specific types
import { type User, createUser } from './user'
```

## Error Handling

### ✅ Good: Result Type Pattern
```typescript
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E }

function divide(a: number, b: number): Result<number> {
  if (b === 0) {
    return { success: false, error: new Error('Division by zero') }
  }
  return { success: true, value: a / b }
}

const result = divide(10, 2)
if (result.success) {
  console.log(result.value)  // number
} else {
  console.error(result.error)  // Error
}
```

## Best Practices Summary

### ✅ DO:
- Enable strict mode
- Use `unknown` instead of `any`
- Leverage type inference
- Use utility types (`Partial`, `Pick`, `Omit`, etc.)
- Use generics for reusable code
- Use type guards for narrowing
- Use const assertions for literal types
- Prefer interfaces for object shapes
- Use type aliases for unions/intersections
- Add JSDoc comments for better IDE support

### ❌ DON'T:
- Use `any` (use `unknown` instead)
- Disable strict checks
- Over-use type assertions
- Create overly complex types
- Use `namespace` (use ES modules)
- Use `enum` when const object works
- Ignore compiler errors
- Use `!` non-null assertion carelessly

**CRITICAL: ALWAYS use strict mode, avoid `any`, leverage generics for reusability, use utility types for transformations, and implement type guards for safe narrowing.**
