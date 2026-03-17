---
name: strict-typing
description: Use when writing code in typed languages - enforces full typing with no any/unknown/untyped escapes, even if it requires extra time
---

# Strict Typing

## Overview

No `any` types. No `unknown` escapes. Everything fully typed.

**Core principle:** Types are documentation that the compiler verifies.

**This skill applies to:** TypeScript, Python (with type hints), Go, Rust, Java, C#, and any typed language.

## The Rule

```
NEVER use any, unknown, or equivalent type escapes.
ALWAYS provide explicit, accurate types.
TAKE EXTRA TIME if needed to type correctly.
```

## TypeScript Specifics

### Forbidden Patterns

```typescript
// NEVER
const data: any = fetchData();
const items: unknown[] = parseItems();
function process(input: any): any { }
const config = {} as any;
// @ts-ignore
// @ts-expect-error (unless truly necessary with documentation)
```

### Required Patterns

```typescript
// ALWAYS
interface UserData {
  id: string;
  name: string;
  email: string;
}

const data: UserData = fetchData();

function process<T extends Processable>(input: T): ProcessResult<T> {
  // ...
}
```

### Configuration

Ensure `tsconfig.json` has strict mode:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Handling Third-Party Types

When library types are missing:

```typescript
// Create type definitions
declare module 'untyped-library' {
  export interface Config {
    option1: string;
    option2: number;
  }

  export function init(config: Config): void;
}
```

Or contribute types to DefinitelyTyped.

### Handling Dynamic Data

For API responses or parsed JSON:

```typescript
// Define expected shape
interface ApiResponse {
  users: User[];
  pagination: Pagination;
}

// Use type guard for runtime validation
function isApiResponse(data: unknown): data is ApiResponse {
  return (
    typeof data === 'object' &&
    data !== null &&
    'users' in data &&
    Array.isArray((data as ApiResponse).users)
  );
}

// Use with validation
const response = await fetch('/api/users');
const data: unknown = await response.json();

if (!isApiResponse(data)) {
  throw new Error('Invalid API response');
}

// data is now typed as ApiResponse
```

### Using Zod for Runtime Validation

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

// Parse and validate
const user = UserSchema.parse(unknownData);
// user is now typed as User
```

## Python Specifics

### Forbidden Patterns

```python
# NEVER
def process(data):  # Missing type hints
    pass

def fetch() -> Any:  # Using Any
    pass

from typing import Any
result: Any = compute()
```

### Required Patterns

```python
# ALWAYS
from typing import TypeVar, Generic, Protocol
from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str

def process(data: User) -> ProcessResult:
    ...

T = TypeVar('T', bound='Processable')

def transform(items: list[T]) -> list[T]:
    ...
```

### Configuration

Use strict mypy settings:

```ini
# mypy.ini
[mypy]
strict = True
disallow_any_generics = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
warn_redundant_casts = True
warn_unused_ignores = True
```

## Go Specifics

Go is statically typed, but avoid:

```go
// AVOID
interface{} // empty interface
any         // Go 1.18+ alias for interface{}

// PREFER
type specific interfaces or concrete types
```

When `interface{}` is truly needed, document why and add type assertions.

## When Typing Is Hard

If typing seems impossible:

### Step 1: Question the Design

```
Is the type hard to express because the design is complex?
→ Consider simplifying the design
```

### Step 2: Use Generics

```typescript
// Instead of any
function process<T>(input: T): T {
  return input;
}
```

### Step 3: Use Union Types

```typescript
// Instead of any for multiple types
type Input = string | number | User;

function process(input: Input): void {
  if (typeof input === 'string') {
    // input is string
  } else if (typeof input === 'number') {
    // input is number
  } else {
    // input is User
  }
}
```

### Step 4: Create Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}
```

### Step 5: Document and Justify (Last Resort)

If `any` is truly unavoidable (extremely rare):

```typescript
// JUSTIFIED: Third-party library `foo` has no types and
// creating accurate types requires reverse-engineering
// the entire library. See issue #123 for type contribution.
// TODO(#456): Remove when @types/foo is available
const result: any = thirdPartyCall();
```

This should be exceptionally rare.

## Time Investment

Proper typing takes time. That's acceptable.

| Situation | Acceptable Time |
|-----------|-----------------|
| Simple interface | 5 minutes |
| Complex generic | 30 minutes |
| Type guards | 15 minutes |
| Library types | 1 hour |

If typing is taking longer, the design may need reconsideration.

## Checklist

Before committing code:

- [ ] No `any` types
- [ ] No `unknown` without type guards
- [ ] No `@ts-ignore` or `# type: ignore`
- [ ] All functions have typed parameters
- [ ] All functions have typed return values
- [ ] All interfaces/types are exported if public
- [ ] Type configuration is strict

## Common Excuses Rejected

| Excuse | Response |
|--------|----------|
| "It's just temporary" | Temporary code becomes permanent. Type it now. |
| "I'll fix types later" | Later never comes. Type it now. |
| "any is faster" | Technical debt is slower. Type it now. |
| "The library has no types" | Create types or use Zod. |
| "It's too complex to type" | Simplify the design. |

## Integration

This skill is applied by:
- `issue-driven-development` - Step 7

This skill ensures:
- Self-documenting code
- Compile-time error catching
- Refactoring safety
- Better IDE support
