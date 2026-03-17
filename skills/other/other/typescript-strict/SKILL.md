---
name: typescript-strict
description: TypeScript strict mode patterns and best practices. Index access, literal types, null checks, generics, type inference. Use when working with TypeScript files.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# TypeScript Strict - Type Safety Patterns

## Purpose

Expert guidance for TypeScript strict mode:

- **Strict Null Checks** - Handle undefined/null properly
- **Index Access** - Safe property access patterns
- **Literal Types** - Const assertions and narrowing
- **Generics** - Type-safe reusable patterns
- **Type Guards** - Runtime type validation

---

## Critical tsconfig.json

```json
{
	"compilerOptions": {
		"strict": true,
		"noUncheckedIndexedAccess": true,
		"noImplicitAny": true,
		"strictNullChecks": true,
		"strictFunctionTypes": true,
		"noImplicitReturns": true,
		"noFallthroughCasesInSwitch": true,
		"exactOptionalPropertyTypes": true,
		"noPropertyAccessFromIndexSignature": true
	}
}
```

---

## Index Access Patterns

### Environment Variables

```typescript
// WRONG - TS7053
const port = process.env.PORT;

// CORRECT - Use bracket notation
const port = process.env['PORT'];
const host = process.env['HOST'] ?? 'localhost';
```

### Object Property Access

```typescript
interface Config {
	[key: string]: string | undefined;
}

const config: Config = { api: 'https://api.example.com' };

// WRONG - Direct access
const url = config.api;

// CORRECT - Bracket access with check
const url = config['api'];
if (url) {
	fetch(url);
}
```

### Array Access

```typescript
const items = ['a', 'b', 'c'];

// WRONG - Could be undefined
const first = items[0].toUpperCase();

// CORRECT - Check first
const first = items[0];
if (first) {
	console.log(first.toUpperCase());
}

// Or use non-null assertion if certain
const guaranteed = items[0]!;
```

---

## Literal Types & Const Assertions

### String Literals

```typescript
// WRONG - Type is string
const status = 'pending';

// CORRECT - Literal type
const status = 'pending' as const;
// type: "pending"

// Object with literals
const config = {
	mode: 'production' as const,
	level: 'high' as const,
};
```

### Object Literals

```typescript
// WRONG - Types are widened
const endpoints = {
	users: '/api/users',
	posts: '/api/posts',
};
// type: { users: string; posts: string }

// CORRECT - Exact types
const endpoints = {
	users: '/api/users',
	posts: '/api/posts',
} as const;
// type: { readonly users: "/api/users"; readonly posts: "/api/posts" }
```

### Discriminated Unions

```typescript
type Result<T> = { success: true; data: T } | { success: false; error: string };

function handleResult<T>(result: Result<T>) {
	if (result.success) {
		// TypeScript knows result.data exists here
		return result.data;
	} else {
		// TypeScript knows result.error exists here
		throw new Error(result.error);
	}
}
```

---

## Null & Undefined Handling

### Optional Chaining

```typescript
interface User {
	profile?: {
		avatar?: string;
	};
}

// CORRECT - Optional chaining
const avatar = user.profile?.avatar ?? '/default.png';
```

### Nullish Coalescing

```typescript
// WRONG - || treats 0, '', false as falsy
const count = input || 10;

// CORRECT - ?? only treats null/undefined as nullish
const count = input ?? 10;
```

### Type Guards

```typescript
// Custom type guard
function isUser(value: unknown): value is User {
	return typeof value === 'object' && value !== null && 'id' in value && 'email' in value;
}

// Usage
function processData(data: unknown) {
	if (isUser(data)) {
		// TypeScript knows data is User here
		console.log(data.email);
	}
}
```

### Assertion Functions

```typescript
function assertDefined<T>(value: T | undefined | null, message: string): asserts value is T {
	if (value === undefined || value === null) {
		throw new Error(message);
	}
}

// Usage
const user = await getUser(id);
assertDefined(user, `User ${id} not found`);
// user is guaranteed to be defined after this
console.log(user.name);
```

---

## Generic Patterns

### Constrained Generics

```typescript
// Ensure T has an id property
function findById<T extends { id: string }>(items: T[], id: string): T | undefined {
	return items.find((item) => item.id === id);
}

// Works with any type that has id
interface User {
	id: string;
	name: string;
}
interface Post {
	id: string;
	title: string;
}

findById(users, '123'); // T is User
findById(posts, '456'); // T is Post
```

### Infer Return Type

```typescript
// Infer return type from callback
function createFetcher<T>(fetcher: () => Promise<T>) {
	return {
		fetch: fetcher,
		refetch: () => fetcher(),
	};
}

// T is automatically inferred
const userFetcher = createFetcher(async () => {
	const res = await fetch('/api/user');
	return res.json() as Promise<User>;
});
// userFetcher.fetch() returns Promise<User>
```

### Mapped Types

```typescript
// Make all properties optional
type Partial<T> = {
	[P in keyof T]?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
	readonly [P in keyof T]: T[P];
};

// Pick specific properties
type Pick<T, K extends keyof T> = {
	[P in K]: T[P];
};

// Custom: Make specific properties required
type RequireFields<T, K extends keyof T> = T & Required<Pick<T, K>>;
```

---

## Utility Types

```typescript
// Exclude null/undefined
type NonNullable<T> = T extends null | undefined ? never : T;

// Extract function return type
type ReturnType<T extends (...args: any) => any> = T extends (...args: any) => infer R ? R : any;

// Extract function parameters
type Parameters<T extends (...args: any) => any> = T extends (...args: infer P) => any ? P : never;

// Usage
type UserSchema = z.infer<typeof userSchema>;
type ApiResponse = Awaited<ReturnType<typeof fetchUser>>;
```

---

## Common Errors & Fixes

### TS2532: Object is possibly 'undefined'

```typescript
// ERROR
const name = user.profile.name;

// FIX - Optional chaining
const name = user.profile?.name ?? 'Unknown';
```

### TS2339: Property does not exist

```typescript
// ERROR
const env = process.env.NODE_ENV;

// FIX - Bracket access
const env = process.env['NODE_ENV'];
```

### TS7053: Index signature

```typescript
// ERROR
const value = obj[key];

// FIX - Type assertion or bracket notation
const value = (obj as Record<string, unknown>)[key];
```

---

## Agent Integration

This skill is used by:

- **ts-strict-checker** agent
- **ts-types-analyzer** agent
- **type-error-resolver** agent
- **quality-checker** for typecheck validation

---

## Commands

```bash
# Type check
bun run typecheck
bunx tsc --noEmit

# Check specific file
bunx tsc --noEmit path/to/file.ts

# Generate types
bunx tsc --declaration --emitDeclarationOnly
```

---

## FORBIDDEN

1. **`any` type** - Use `unknown` instead
2. **Non-null assertion without certainty** - Check first
3. **Type assertion to hide errors** - Fix the actual issue
4. **Ignoring strict errors** - Always fix properly
5. **`@ts-ignore` without explanation** - Use `@ts-expect-error` with comment

---

## Version

- **v1.0.0** - Initial implementation based on TypeScript 5.x strict patterns
