---
name: typescript-dev
description: TypeScript development best practices, code quality tools, and documentation templates. Activated when working with .ts, .tsx files or TypeScript projects.
allowed-tools: ['Read', 'Glob', 'Grep', 'Bash']
---

# TypeScript Development Expert

This skill supports TypeScript project development.

## 🎯 Core Rules

### Package Management
- **Required**: Use `pnpm` as package manager
- Do not use `npm` or `yarn`

### Type Safety
- **tsconfig.json**: `strict: true` required
- **Null Handling**: Leverage optional chaining `?.` and nullish coalescing `??`
- **Imports**: Use ES modules, avoid `require()`
- **NO ANY**: Do not use `any` type in production code

### Best Practices
- **Type Inference**: Let TypeScript infer when obvious
- **Generics**: Use for reusable components
- **Union Types**: Prefer union types over enums for string literals
- **Utility Types**: Leverage built-in types (Partial, Pick, Omit)

### Documentation
- **Required**: Use TSDoc format for documentation comments
- **Public APIs only**: Document exported functions, classes, and interfaces
- **Self-documenting code**: Prefer clear naming over excessive comments
- **Document when necessary**: Add TSDoc only when the code intent isn't obvious from the signature

## 🛠️ Code Quality Tools

### Development Workflow
```bash
# Format code
pnpm run format

# Run linter
pnpm run lint

# Type check
pnpm tsc --noEmit

# Run tests with coverage
pnpm test -- --coverage
```

## 🎯 Quality Checklist

Check these during code review:

- [ ] Public APIs have TSDoc comments (when intent isn't clear from signature)
- [ ] No `any` type usage
- [ ] Proper error handling
- [ ] Test coverage above 80%
- [ ] Type inference properly leveraged
- [ ] Utility Types utilized
- [ ] Optional chaining (`?.`) and Nullish coalescing (`??`) used
- [ ] ES modules used (avoid `require()`)

## 🚀 Common Patterns

### Error Handling
```typescript
// Good: Clear error types
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Good: Result type pattern
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
```

### Async/Await
```typescript
// Good: With error handling
async function fetchUserData(id: string): Promise<Result<UserData>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

### Type Guards
```typescript
// Good: Custom type guard
function isUserProfile(value: unknown): value is UserProfile {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'username' in value
  );
}
```

## 💡 Performance Tips

1. **Avoid unnecessary re-renders** (React)
   - Use `React.memo` for expensive components
   - Use `useMemo` / `useCallback` appropriately

2. **Lazy Loading**
   - Dynamic imports for code splitting
   - `React.lazy()` for components

3. **Type-only imports**
   ```typescript
   import type { UserProfile } from './types';
   ```

## 🔍 Common Anti-patterns to Avoid

❌ **Don't**:
```typescript
// Using any type
function process(data: any) { }

// Implicit any
function getValue(obj, key) { }

// Excessive type assertions
const user = data as User;
```

✅ **Do**:
```typescript
// Proper type definitions
function process(data: UserData) { }

// Explicit types
function getValue<T>(obj: T, key: keyof T) { }

// Use type guards
if (isUser(data)) {
  // data is User here
}
```
