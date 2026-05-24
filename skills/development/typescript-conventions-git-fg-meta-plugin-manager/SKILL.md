---
name: typescript-conventions
description: "Apply TypeScript conventions when writing or refactoring TypeScript code to ensure type safety and consistency. Not for JavaScript or other languages."
user-invocable: false
---

# TypeScript Team Conventions

TypeScript conventions that auto-apply when writing TypeScript code. These conventions ensure consistency, type safety, and maintainability across the codebase.

## Type Strictness

**Always enforce:**

- Use strict mode: `"strict": true` in tsconfig.json
- Never use `any` (use `unknown` instead)
- Define explicit return types for all functions
- Prefer interfaces over types for object shapes

**Example - Good:**

```typescript
interface UserRepository {
  findById(id: UserId): Promise<Result<User, NotFoundError>>;
  save(user: User): Promise<Result<void, DatabaseError>>;
}

function validateEmail(email: string): Result<Email, ValidationError> {
  // implementation
}
```

**Example - Bad:**

```typescript
function validateEmail(email: any): any {
  // DON'T use 'any'
}
```

## Error Handling

**Requirements:**

- Never throw bare errors; use typed error classes
- Always include context: `new ValidationError('message', { context })`
- Use Result<T> pattern for operations that can fail
- Handle async errors with try/catch in async functions

**Example - Good:**

```typescript
class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field?: string,
    public readonly context?: Record<string, unknown>,
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

function validateUser(
  user: unknown,
): Result<UserValidationResult, ValidationError> {
  try {
    // validation logic
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: new ValidationError("Validation failed", "user", {
        error: error.message,
      }),
    };
  }
}
```

**Example - Bad:**

```typescript
function validateUser(user: any) {
  if (!user) throw new Error("Invalid user"); // DON'T use bare Error
  return user;
}
```

## Naming Conventions

**Follow these patterns:**

| Type                | Convention                        | Example                          |
| ------------------- | --------------------------------- | -------------------------------- |
| Interfaces          | PascalCase with descriptive names | `UserRepository`, `MarketData`   |
| Types               | PascalCase                        | `UserId`, `ApiResponse<T>`       |
| Enums               | PascalCase                        | `UserRole`, `HttpStatus`         |
| Variables/functions | camelCase                         | `getUserById`, `userData`        |
| Constants           | UPPER_SNAKE_CASE                  | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |

**Examples:**

```typescript
interface UserRepository {} // ✅ Good
type UserId = string; // ✅ Good
enum UserRole {} // ✅ Good
const MAX_RETRIES = 3; // ✅ Good
function getUserById(id: UserId) {} // ✅ Good
```

## Module Organization

**File structure:**

- Use: `src/<domain>/<feature>/<File.ts>`
- Export only public interfaces from index.ts
- Keep files under 300 lines
- Use named exports, avoid default exports

**Example - Good:**

```typescript
// src/user/UserRepository.ts
export interface UserRepository {
  findById(id: UserId): Promise<Result<User, NotFoundError>>;
}

export class DatabaseUserRepository implements UserRepository {
  async findById(id: UserId): Promise<Result<User, NotFoundError>> {
    // implementation
  }
}
```

## Immutability Pattern (CRITICAL)

**WHY**: Prevents stale closures, makes state predictable, enables React optimizations.

**✅ ALWAYS use spread operator:**

```typescript
const updatedUser = { ...user, name: "New Name" };
const updatedArray = [...items, newItem];
```

**❌ NEVER mutate directly:**

```typescript
user.name = "New Name"; // BAD - causes bugs
items.push(newItem); // BAD - breaks React optimizations
```

## Code Organization

**Best practices:**

- Group related functionality into classes or modules
- Use dependency injection for services
- Keep pure functions separate from side-effect code
- Prefer composition over inheritance
- Use early returns over deep nesting

**Example - Good:**

```typescript
function processUser(user: User): Result<ProcessedUser, ValidationError> {
  if (!user) {
    return { success: false, error: new ValidationError("User required") };
  }

  if (!isValidEmail(user.email)) {
    return { success: false, error: new ValidationError("Invalid email") };
  }

  return { success: true, data: process(user) };
}
```

## Testing Standards

**Requirements:**

- Write tests for all public functions
- Use descriptive test names: `should_return_user_when_id_exists`
- Mock external dependencies
- Aim for 80%+ code coverage

**Example - Good:**

```typescript
describe("UserRepository", () => {
  describe("findById", () => {
    it("should return user when id exists", async () => {
      const repo = new DatabaseUserRepository(mockDb);
      const result = await repo.findById("user-123");
      expect(result.success).toBe(true);
      expect(result.data).toEqual(expectedUser);
    });

    it("should return error when user not found", async () => {
      const repo = new DatabaseUserRepository(mockDb);
      const result = await repo.findById("non-existent");
      expect(result.success).toBe(false);
    });
  });
});
```

## Type Safety Over Convenience

**WHY**: Types catch bugs at compile-time, serve as documentation, enable refactoring.

**✅ GOOD (proper types):**

```typescript
interface Market {
  id: string;
  name: string;
  status: "active" | "resolved" | "closed";
}

function getMarket(id: string): Promise<Market> {}
```

**❌ BAD (using `any`):**

```typescript
function getMarket(id: any): Promise<any> {}
```

## Constants Over Magic Numbers

**Use named constants instead of magic numbers:**

**✅ Good:**

```typescript
const MIN_AGE = 18;
const MAX_AGE = 120;
const MIN_NAME_LENGTH = 2;
const MAX_NAME_LENGTH = 100;

if (user.age < MIN_AGE || user.age > MAX_AGE) {
  throw new ValidationError("Age out of range");
}
```

**❌ Bad:**

```typescript
if (user.age < 18 || user.age > 120) {
  // Magic numbers
  throw new Error("Invalid age");
}
```

## Performance Best Practices

**Use for:**

- Expensive computations (`useMemo`)
- Functions passed to children (`useCallback`)
- Pure components (`React.memo`)

```typescript
const sortedMarkets = useMemo(() => {
  return markets.sort((a, b) => b.volume - a.volume);
}, [markets]);

const handleSearch = useCallback((query: string) => {
  setSearchQuery(query);
}, []);
```

## Common Anti-Patterns to Avoid

❌ **Using `any` for types**

```typescript
// DON'T
function process(data: any): any {}
```

❌ **Default exports**

```typescript
// DON'T
export default function process() {}
```

❌ **Bare `throw new Error()`**

```typescript
// DON'T
throw new Error("Something went wrong");
```

❌ **Mixed concerns in single file**

```typescript
// DON'T - mixing business logic, UI, and data access
function UserComponent() {
  // UI logic
  // Data access
  // Business logic
}
```

❌ **Magic numbers without constants**

```typescript
// DON'T
if (retries > 3) {
}
```

❌ **Console.log in production**

```typescript
// DON'T
console.log("User data:", user);
```

## Verification Checklist

Before considering TypeScript code complete:

- [ ] Strict mode enabled in tsconfig.json
- [ ] No `any` types (use `unknown` instead)
- [ ] Explicit return types defined
- [ ] Typed error classes used (not bare Error)
- [ ] Result<T> pattern for operations that can fail
- [ ] Immutability pattern followed (spread operators)
- [ ] Constants instead of magic numbers
- [ ] Descriptive naming conventions
- [ ] Files under 300 lines
- [ ] Named exports (no default)
- [ ] Tests written for all public functions
- [ ] 80%+ code coverage

## Integration

This skill integrates with:

- `coding-standards` - Universal coding best practices
- `engineering-lifecycle` - Testing requirements
- `frontend-patterns` - React/TypeScript patterns
- `backend-patterns` - TypeScript backend patterns

---

## Dynamic Sourcing Protocol

<fetch_protocol>
**CONDITIONAL FETCH**: For TypeScript language questions, fetch from:

- https://www.typescriptlang.org/docs/handbook/ (Type fundamentals)

This skill contains Seed System-specific conventions (Result<T> pattern, immutability, naming conventions) that extend TypeScript fundamentals.
</fetch_protocol>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming
  MANDATORY: Define explicit return types for all functions
  MANDATORY: Use Result<T> pattern for operations that can fail
  MANDATORY: Use typed error classes, never bare Error
  MANDATORY: Never mutate objects directly (use spread operator)
  No exceptions. Type safety prevents runtime bugs.
  </critical_constraint>
