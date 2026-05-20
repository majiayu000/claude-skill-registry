---
name: js-modern
description: Write modern JavaScript and TypeScript — ES6+ features, async/await, modules, destructuring, optional chaining, TypeScript types, and modern tooling. Use when writing JavaScript/TypeScript for BigCommerce themes, apps, or headless storefronts.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Modern JavaScript & TypeScript

## Before writing code

**Fetch live docs**: Web-search `site:developer.mozilla.org javascript` for MDN JavaScript reference. Check `https://www.typescriptlang.org/docs/` for TypeScript documentation.

## ES6+ Features

### Arrow Functions

Concise function syntax with lexical `this`:
- `const add = (a, b) => a + b;`
- Implicit return for single expressions
- No own `this`, `arguments`, `super`, or `new.target`

### Template Literals

String interpolation and multi-line strings:
- `` `Hello, ${name}!` ``
- Tagged templates for DSLs

### Destructuring

Extract values from objects/arrays:
- `const { name, price } = product;`
- `const [first, ...rest] = items;`
- Default values: `const { name = 'Unknown' } = product;`
- Nested: `const { address: { city } } = customer;`

### Spread / Rest

- Spread: `[...arr1, ...arr2]`, `{ ...obj1, ...obj2 }`
- Rest: `function(...args) {}`, `const { a, ...rest } = obj;`

### Modules (ES Modules)

- `import { func } from './module.js';`
- `export const value = 42;` / `export default class {}`
- Dynamic: `const mod = await import('./lazy.js');`

### Optional Chaining & Nullish Coalescing

- `obj?.property?.nested` — short-circuits to `undefined` if any part is nullish
- `value ?? defaultValue` — returns right side only if left is `null`/`undefined` (not falsy)

## Async Patterns

### Promises

- `new Promise((resolve, reject) => { ... })`
- `.then()`, `.catch()`, `.finally()`
- `Promise.all()`, `Promise.allSettled()`, `Promise.race()`, `Promise.any()`

### Async/Await

- `async function fetchData() { const data = await fetch(url); }`
- Error handling with try/catch
- Parallel: `const [a, b] = await Promise.all([fetchA(), fetchB()]);`

### Fetch API

```javascript
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data),
});
const result = await response.json();
```

## TypeScript

### Type Annotations

- `let name: string = 'Product';`
- `function getPrice(id: number): Promise<number> { ... }`
- `const product: Product = { ... };`

### Interfaces

```typescript
interface Product {
  id: number;
  name: string;
  price: number;
  variants?: Variant[];
}
```

### Type Utilities

- `Partial<T>` — all properties optional
- `Required<T>` — all properties required
- `Pick<T, K>` — subset of properties
- `Omit<T, K>` — exclude properties
- `Record<K, V>` — key-value mapping
- `ReturnType<T>` — extract return type of function

### Generics

```typescript
function fetchResource<T>(url: string): Promise<T> {
  return fetch(url).then(res => res.json());
}
const product = await fetchResource<Product>('/api/products/1');
```

### Enums

```typescript
enum OrderStatus {
  Pending = 'pending',
  Shipped = 'shipped',
  Completed = 'completed',
}
```

### Discriminated Unions

```typescript
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; message: string };
```

## Modern Array Methods

- `map`, `filter`, `reduce`, `find`, `findIndex`
- `some`, `every` — boolean checks
- `flat`, `flatMap` — array flattening
- `Array.from()`, `Array.isArray()`
- `Object.entries()`, `Object.fromEntries()`, `Object.keys()`, `Object.values()`
- `structuredClone()` — deep clone

## For BigCommerce Specifically

### Stencil Theme JS

- ES6 modules bundled with webpack
- jQuery available (Cornerstone ships it)
- Use `PageManager` lifecycle for page-specific code
- Access injected server data via `this.context`

### Catalyst / Next.js

- TypeScript by default
- React components with hooks
- Server Components + Client Components
- Type-safe GraphQL queries

### App Development

- Node.js backend with Express/Fastify
- TypeScript for API type safety
- JWT handling with `jsonwebtoken` library

## Best Practices

- Use `const` by default, `let` when reassignment is needed, never `var`
- Use async/await over raw Promises for readability
- Use TypeScript for all non-trivial projects
- Use optional chaining to simplify null checks
- Use destructuring for cleaner function signatures
- Handle errors at appropriate levels (don't swallow errors)
- Use `===` instead of `==` for comparisons
- Use ESLint + Prettier for consistent code style

Fetch MDN and TypeScript docs for exact syntax, browser compatibility, and new features before implementing.
