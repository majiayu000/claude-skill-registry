---
name: typescript-refactorer
description: Identify TypeScript code smells and suggest type-safe refactoring. Use when asked to refactor, improve types, clean up TypeScript code, tighten types, reduce any usage, or improve type safety.
---

# TypeScript Refactorer

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Analysis Process

1. Scan the specified files for type-related code smells
2. Categorize issues by severity
3. Provide corrected code for each issue

## Code Smells to Detect

### Explicit `any` Usage
```typescript
// BAD
function process(data: any) {
  return data.value;
}

// GOOD: Use specific type or generic
function process<T extends { value: unknown }>(data: T) {
  return data.value;
}

// GOOD: Use unknown with type guard
function process(data: unknown) {
  if (isValidData(data)) {
    return data.value;
  }
  throw new Error('Invalid data');
}
```

### Implicit `any` from Missing Types
```typescript
// BAD: Parameter implicitly has 'any' type
function calculate(x, y) {
  return x + y;
}

// GOOD
function calculate(x: number, y: number): number {
  return x + y;
}
```

### Unnecessary Type Assertions
```typescript
// BAD: Assertion when type is already known
const value = getValue() as string; // getValue already returns string

// BAD: Double assertion (type laundering)
const data = response as unknown as User;

// GOOD: Fix the source type or use type guard
const data = isUser(response) ? response : null;
```

### Overly Broad Union Types
```typescript
// BAD
type Status = string;

// GOOD: Use literal union
type Status = 'pending' | 'active' | 'completed' | 'failed';

// BAD
type Result = { success: boolean; data?: any; error?: string };

// GOOD: Discriminated union
type Result =
  | { success: true; data: User }
  | { success: false; error: string };
```

### Missing Discriminated Unions
```typescript
// BAD: Ambiguous state
interface State {
  loading: boolean;
  data: User | null;
  error: Error | null;
}

// GOOD: Discriminated union makes invalid states unrepresentable
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: Error };
```

### Implicit Return Types
```typescript
// BAD: Return type inferred as complex union
function getUser(id: string) {
  if (!id) return null;
  return fetchUser(id); // Returns Promise<User>
}
// Inferred: (id: string) => null | Promise<User>

// GOOD: Explicit return type catches errors
function getUser(id: string): Promise<User | null> {
  if (!id) return Promise.resolve(null);
  return fetchUser(id);
}
```

### Non-null Assertions (!)
```typescript
// BAD: Hiding potential null issues
const name = user!.name;

// GOOD: Explicit null check
const name = user?.name ?? 'Anonymous';

// GOOD: Early return / throw
if (!user) throw new Error('User required');
const name = user.name;
```

### Type-unsafe Object Access
```typescript
// BAD
const value = obj['dynamicKey'];

// GOOD: Use Record type
const obj: Record<string, number> = {};
const value = obj['dynamicKey']; // value: number | undefined

// BETTER: Use Map for dynamic keys
const map = new Map<string, number>();
const value = map.get('dynamicKey');
```

### Missing readonly
```typescript
// BAD: Mutable when shouldn't be
interface Config {
  apiUrl: string;
  timeout: number;
}

// GOOD: Immutable config
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// Or use Readonly utility
type Config = Readonly<{
  apiUrl: string;
  timeout: number;
}>;
```

### Function Overloads Instead of Unions
```typescript
// BAD: Unclear relationship between input and output
function parse(input: string | Buffer): string | Uint8Array;

// GOOD: Overloads make it explicit
function parse(input: string): string;
function parse(input: Buffer): Uint8Array;
function parse(input: string | Buffer): string | Uint8Array {
  // Implementation
}
```

## Output Format

```
## TypeScript Analysis

### Critical (type safety compromised)
- **Explicit any** in `src/utils/api.ts:23`
  - Issue: `data: any` parameter loses all type information
  - Fix: [code block with typed version]

### Warnings (potential issues)
- **Missing discriminated union** in `src/types/state.ts:5`
  - Issue: State type allows invalid combinations
  - Fix: [code block with discriminated union]

### Suggestions (improvements)
- **Implicit return type** in `src/services/user.ts:45`
  - Issue: Complex inferred return type
  - Fix: [code block with explicit return type]

### Summary
- Critical: X issues
- Warnings: X issues
- Suggestions: X issues
```

## Before/After Verification

After suggesting refactoring changes, verify that the refactored code is type-correct by checking for: consistent type usage across the changed files, no introduced type errors in function signatures, all imports still valid. If a suggested refactoring would break a downstream consumer, flag it: `BREAKING: this change affects [file/function] — update those references too.`

## Reference

See `references/code-smells.md` for a complete catalog of TypeScript anti-patterns.
