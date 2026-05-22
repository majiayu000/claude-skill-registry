---
name: dev-typescript
description: FIX TypeScript errors, WRITE better types, and CONVERT JavaScript to TypeScript. Use when encountering type errors, improving type safety, or migrating JS files.
---

# TypeScript Skill

## When to Use

Activate this skill when:
- Encountering TypeScript compilation errors (TS2322, TS2345, TS7006, etc.)
- Improving type safety in existing code
- Converting JavaScript files to TypeScript
- Writing new TypeScript interfaces, types, or generics
- Working with Vue 3 + TypeScript patterns

## Finding TypeScript Errors

**CRITICAL**: `npm run build` does NOT catch all TypeScript errors! Vite only transpiles, it doesn't type-check.

### Commands to Find Errors

```bash
# Vue projects - ALWAYS run this to find TS errors
npm run type-check:watch

# Or one-time check
npx vue-tsc --noEmit

# Non-Vue TypeScript projects
npx tsc --noEmit

# Check specific file
npx vue-tsc --noEmit src/path/to/file.vue
```

### Verification Workflow

1. **Before claiming code works**: Run `npm run type-check:watch`
2. **After fixing errors**: Run again to verify all resolved
3. **Before committing**: Ensure zero TypeScript errors

### Common Gotcha

| Command | What it checks |
|---------|----------------|
| `npm run build` | Syntax only (Vite transpiles) - **NOT SUFFICIENT** |
| `npm run type-check:watch` | Full type checking (vue-tsc) - **USE THIS** |
| `npm run lint` | ESLint rules (separate from TS errors) |

## Fix Type Errors

### TS2322: Type 'X' is not assignable to type 'Y'

**Cause**: Assigning a value of incompatible type.

```typescript
// BAD
const count: number = "5"

// GOOD - Option 1: Fix the type
const count: number = 5

// GOOD - Option 2: Change the annotation
const count: string = "5"

// GOOD - Option 3: Parse the value
const count: number = parseInt("5", 10)
```

### TS2345: Argument type mismatch

**Cause**: Function argument doesn't match parameter type.

```typescript
// BAD
function process(value: string) { /*...*/ }
process(undefined)

// GOOD - Handle undefined
function process(value: string | undefined) {
  if (!value) return
  // ...
}

// GOOD - Use type guard
function process(value: unknown) {
  if (typeof value === 'string') {
    // value is now string
  }
}
```

### TS7006: Parameter implicitly has 'any' type

**Cause**: Missing type annotation on parameter.

```typescript
// BAD
const handler = (event) => { /*...*/ }

// GOOD
const handler = (event: MouseEvent) => { /*...*/ }

// GOOD - For callbacks
array.map((item: string) => item.toUpperCase())
```

### TS2532: Object is possibly 'undefined'

**Cause**: Accessing property on potentially undefined value.

```typescript
// BAD
const name = user.profile.name

// GOOD - Optional chaining
const name = user?.profile?.name

// GOOD - Null check
if (user && user.profile) {
  const name = user.profile.name
}

// GOOD - Non-null assertion (when you're certain)
const name = user!.profile!.name
```

### TS2339: Property does not exist on type

**Cause**: Accessing undeclared property.

```typescript
// BAD
interface User { name: string }
const user: User = { name: 'John', age: 30 } // age doesn't exist

// GOOD - Add to interface
interface User {
  name: string
  age?: number  // Optional property
}

// GOOD - Use index signature
interface User {
  name: string
  [key: string]: unknown
}
```

## Write Better Types

### Use `unknown` Instead of `any`

```typescript
// BAD - any disables type checking
function parse(data: any) {
  return data.value  // No error, but unsafe
}

// GOOD - unknown requires type checking
function parse(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: string }).value
  }
  throw new Error('Invalid data')
}
```

### Use `satisfies` for Type Constraints

```typescript
// BAD - Loses specific type info
const config: Record<string, string> = {
  apiUrl: 'https://api.example.com',
  timeout: '5000'  // We want to catch this isn't a number
}

// GOOD - Maintains inference + validates structure
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
} satisfies Record<string, string | number>

// config.apiUrl is typed as string, not string | number
```

### Discriminated Unions for State

```typescript
// Model different states with a discriminant property
type LoadingState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: string[] }
  | { status: 'error'; error: Error }

function handle(state: LoadingState) {
  switch (state.status) {
    case 'idle':
      return 'Ready'
    case 'loading':
      return 'Loading...'
    case 'success':
      return state.data.join(', ')  // TypeScript knows data exists
    case 'error':
      return state.error.message    // TypeScript knows error exists
  }
}
```

### Template Literal Types

```typescript
// Create dynamic string types
type EventName = 'click' | 'focus' | 'blur'
type Handler = `on${Capitalize<EventName>}`
// Result: 'onClick' | 'onFocus' | 'onBlur'

// API routes
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'
type ApiRoute = `/api/${string}`
type Endpoint = `${HttpMethod} ${ApiRoute}`
// e.g., 'GET /api/users'
```

### Generics with Constraints

```typescript
// Constrain generic to specific shape
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

// With default type
function createStore<T = Record<string, unknown>>(initial: T) {
  let state = initial
  return {
    get: () => state,
    set: (value: T) => { state = value }
  }
}
```

## Utility Types Reference

```typescript
// Partial - Make all properties optional
type PartialUser = Partial<User>

// Required - Make all properties required
type RequiredUser = Required<User>

// Pick - Select specific properties
type UserName = Pick<User, 'firstName' | 'lastName'>

// Omit - Remove specific properties
type PublicUser = Omit<User, 'password' | 'secretKey'>

// Record - Create object type with specific keys
type Flags = Record<'dark' | 'compact', boolean>

// ReturnType - Extract function return type
type Result = ReturnType<typeof fetchData>

// Parameters - Extract function parameters
type Args = Parameters<typeof fetchData>

// NonNullable - Remove null and undefined
type DefiniteValue = NonNullable<string | null | undefined>  // string

// Extract/Exclude - Filter union types
type Numbers = Extract<string | number | boolean, number>  // number
type NotNumbers = Exclude<string | number | boolean, number>  // string | boolean
```

## Convert JavaScript to TypeScript

### Migration Workflow

1. **Rename file**: `.js` → `.ts` (or `.vue` stays same)
2. **Add explicit types** to function parameters
3. **Define interfaces** for objects and props
4. **Handle null/undefined** with optional chaining or guards
5. **Run `npm run build`** to find remaining errors

### Common Conversions

```typescript
// JavaScript
function fetchUser(id) {
  return fetch(`/api/users/${id}`).then(r => r.json())
}

// TypeScript
interface User {
  id: string
  name: string
  email: string
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  return response.json() as Promise<User>
}
```

## Vue 3 + TypeScript

See `references/vue-typescript.md` for:
- `defineProps<T>()` patterns
- `defineEmits<T>()` (old and Vue 3.3+ syntax)
- Pinia store typing
- Composable return types
- Template ref typing

## Anti-Patterns to Avoid

### Never Do This

```typescript
// DON'T use any
const data: any = fetchData()

// DON'T use @ts-ignore without explanation
// @ts-ignore
brokenCode()

// DON'T use non-null assertion carelessly
user!.profile!.settings!.theme

// DON'T leave implicit any in parameters
array.map(x => x.value)  // x is implicitly any
```

### Do This Instead

```typescript
// Use unknown + type guards
const data: unknown = fetchData()
if (isValidData(data)) { /* use data */ }

// Use @ts-expect-error with reason
// @ts-expect-error - Legacy API returns number as string
const count: number = parseInt(response.value)

// Use optional chaining
user?.profile?.settings?.theme ?? 'default'

// Always type parameters
array.map((x: Item) => x.value)
```

## tsconfig.json Recommendations

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

## Additional References

- `references/common-errors.md` - Detailed error solutions
- `references/utility-types.md` - Full utility type guide
- `references/vue-typescript.md` - Vue 3 + TypeScript patterns
