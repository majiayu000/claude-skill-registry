---
name: nomistakes
description: Error prevention and best practices enforcement for agent-assisted coding. Use when writing code to catch common mistakes, enforce patterns, prevent bugs, validate inputs, handle errors, follow coding standards, avoid anti-patterns, and ensure code quality through proactive checks and guardrails.
---

# No Mistakes: Error Prevention & Best Practices Enforcement

## Purpose

This skill helps agents write higher-quality code by proactively preventing common errors, enforcing best practices, and applying defensive programming patterns. Use this skill when writing any code to reduce bugs, improve maintainability, and follow established patterns.

## Recommended Model Configuration

For best results with this skill:

**Minimum Requirements:**
- **Model**: Claude 3.5 Sonnet or GPT-4 (or better)
- **Reasoning**: Extended thinking enabled (if available)
- **Context**: 8K+ tokens recommended for complex refactors

**Why This Matters:**
Error prevention requires deep reasoning about edge cases, type safety, and failure modes. Stronger models with extended thinking capabilities will:
- Catch more subtle bugs (off-by-one, race conditions, type coercion)
- Generate more robust validation logic
- Provide better error handling strategies
- Reason through complex async/promise chains

**Optimal Setup (February 2026):**
- Claude 3.7 Sonnet with extended thinking (most comprehensive error analysis)
- GPT-4 Turbo with reasoning mode (strong at type safety)
- Claude 3.5 Sonnet (good baseline, fast)

**Suboptimal (will miss issues):**
- Claude 3 Haiku (too fast, skips edge cases)
- GPT-3.5 (lacks reasoning depth)
- Any model without extended thinking for complex code

If your agent doesn't support model selection, this skill will still help, but expect fewer proactive warnings about subtle bugs.

## When to Use This Skill

Activate this skill when:
- Writing new code or functions
- Refactoring existing code
- Implementing API integrations
- Handling user input or external data
- Working with async operations
- Managing state or side effects
- Writing tests or validation logic
- Reviewing code for potential issues

## Core Error Prevention Principles

### 1. Input Validation (Guard at Boundaries)

**Always validate inputs at function boundaries:**

```typescript
// ❌ BAD: No validation
function processUser(id: string) {
  return database.query(id); // What if id is empty? SQL injection?
}

// ✅ GOOD: Guard at entry
function processUser(id: string) {
  if (!id || typeof id !== 'string') {
    throw new Error('Invalid user ID: must be non-empty string');
  }
  if (!/^[a-zA-Z0-9-]+$/.test(id)) {
    throw new Error('Invalid user ID format: alphanumeric and hyphens only');
  }
  return database.query(id);
}
```

**Validation checklist:**
- [ ] Type checking (runtime, not just TypeScript)
- [ ] Null/undefined checks
- [ ] Range validation (min/max, length limits)
- [ ] Format validation (regex, schemas)
- [ ] Business rule validation (allowed states, permissions)

### 2. Error Handling (Fail Fast, Fail Loudly)

**Never silently swallow errors:**

```typescript
// ❌ BAD: Silent failure
try {
  await criticalOperation();
} catch (e) {
  // Silent failure - bug goes unnoticed
}

// ✅ GOOD: Explicit handling
try {
  await criticalOperation();
} catch (e) {
  logger.error('Critical operation failed', { error: e, context });
  throw new ApplicationError('Operation failed', { cause: e });
}
```

**Error handling checklist:**
- [ ] Catch specific errors, not generic `Error`
- [ ] Log errors with context (what, when, why)
- [ ] Preserve error stack traces (`cause` property)
- [ ] Return typed error objects (not strings)
- [ ] Use domain-specific error types

### 3. Null Safety (Avoid Billion Dollar Mistakes)

**Treat null/undefined as exceptional:**

```typescript
// ❌ BAD: Assumes data exists
function getUserName(user) {
  return user.profile.name; // Can crash on null user or profile
}

// ✅ GOOD: Defensive checks
function getUserName(user: User | null): string {
  if (!user?.profile?.name) {
    return 'Unknown User'; // Safe default or throw error
  }
  return user.profile.name;
}
```

**Null safety checklist:**
- [ ] Use optional chaining (`?.`) for nested access
- [ ] Nullish coalescing (`??`) for defaults
- [ ] Early returns for null checks
- [ ] Make nullability explicit in types
- [ ] Avoid `any` type (disables null checks)

### 4. Async Operations (No Race Conditions)

**Handle async errors and edge cases:**

```typescript
// ❌ BAD: Unhandled promise rejection
async function loadData() {
  const data = await fetch(url); // What if network fails?
  return data;
}

// ✅ GOOD: Comprehensive async handling
async function loadData(): Promise<Result<Data>> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);
    
    if (!response.ok) {
      return { error: `HTTP ${response.status}` };
    }
    
    const data = await response.json();
    return { data };
  } catch (e) {
    if (e.name === 'AbortError') {
      return { error: 'Request timeout' };
    }
    return { error: `Network error: ${e.message}` };
  }
}
```

**Async safety checklist:**
- [ ] Always await or return promises
- [ ] Handle promise rejections (try/catch or .catch)
- [ ] Implement timeouts for network calls
- [ ] Use abort controllers for cancelation
- [ ] Avoid fire-and-forget patterns (use `void` intentionally)

### 5. Type Safety (Make Invalid States Unrepresentable)

**Use TypeScript to prevent bugs at compile time:**

```typescript
// ❌ BAD: Stringly-typed
type Status = string; // Can be anything
function setStatus(status: Status) { ... }
setStatus("complted"); // Typo not caught

// ✅ GOOD: Union types
type Status = 'pending' | 'completed' | 'failed';
function setStatus(status: Status) { ... }
setStatus("complted"); // Compile error!

// ✅ BETTER: Discriminated unions for state machines
type State = 
  | { status: 'idle' }
  | { status: 'loading'; startedAt: number }
  | { status: 'success'; data: Data }
  | { status: 'error'; error: Error };
```

**Type safety checklist:**
- [ ] Use literal types instead of strings
- [ ] Use discriminated unions for complex state
- [ ] Avoid `any`, use `unknown` when type is truly unknown
- [ ] Make illegal states unrepresentable
- [ ] Use branded types for IDs and tokens

### 6. Boundary Checks (Arrays, Strings, Numbers)

**Always validate indices and ranges:**

```typescript
// ❌ BAD: No bounds checking
function getItem(index: number) {
  return items[index]; // Returns undefined if out of bounds
}

// ✅ GOOD: Explicit bounds checking
function getItem(index: number): Item {
  if (index < 0 || index >= items.length) {
    throw new RangeError(`Index ${index} out of bounds [0, ${items.length})`);
  }
  return items[index];
}
```

**Boundary checklist:**
- [ ] Check array indices before access
- [ ] Validate string lengths before slicing
- [ ] Check numeric ranges (min/max)
- [ ] Validate pagination parameters
- [ ] Handle empty collections gracefully

### 7. Resource Management (Clean Up After Yourself)

**Always release resources:**

```typescript
// ❌ BAD: Resource leak
async function processFile(path: string) {
  const file = await fs.open(path);
  const data = await file.read();
  return data; // File never closed!
}

// ✅ GOOD: Guaranteed cleanup
async function processFile(path: string) {
  const file = await fs.open(path);
  try {
    const data = await file.read();
    return data;
  } finally {
    await file.close(); // Always executed
  }
}

// ✅ BETTER: Using resource patterns
await using file = await fs.open(path); // Auto-closes
const data = await file.read();
return data;
```

**Resource checklist:**
- [ ] Close file handles (use `finally` or `using`)
- [ ] Clear timeouts and intervals
- [ ] Unsubscribe from event listeners
- [ ] Cancel pending requests on unmount
- [ ] Release database connections

### 8. Immutability (Avoid Mutation Bugs)

**Prefer immutable operations:**

```typescript
// ❌ BAD: Mutates input
function addItem(list: Item[], item: Item) {
  list.push(item); // Mutates caller's array
  return list;
}

// ✅ GOOD: Immutable update
function addItem(list: Item[], item: Item): Item[] {
  return [...list, item]; // New array
}

// ✅ GOOD: Immutable object update
function updateUser(user: User, name: string): User {
  return { ...user, name }; // New object
}
```

**Immutability checklist:**
- [ ] Use spread operators for copies
- [ ] Avoid `.push()`, `.pop()`, `.splice()` on inputs
- [ ] Use `Object.freeze()` for constants
- [ ] Return new objects/arrays instead of mutating
- [ ] Use `readonly` type modifiers

### 9. Configuration Validation (Fail at Startup)

**Validate configuration early:**

```typescript
// ❌ BAD: Lazy validation
function sendEmail(to: string) {
  const apiKey = process.env.SENDGRID_API_KEY; // Might be undefined
  return sendgrid.send({ to, apiKey });
}

// ✅ GOOD: Validate at startup
const config = {
  sendgridApiKey: requireEnv('SENDGRID_API_KEY'),
  databaseUrl: requireEnv('DATABASE_URL'),
};

function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required env var: ${key}`);
  }
  return value;
}
```

**Configuration checklist:**
- [ ] Validate env vars at startup, not at use
- [ ] Use schema validation (Zod, Joi) for config
- [ ] Fail fast if config is invalid
- [ ] Provide clear error messages
- [ ] Document required configuration

### 10. Defensive Programming (Assume the Worst)

**Code as if everything can fail:**

```typescript
// ❌ BAD: Optimistic
function parseJSON(text: string) {
  return JSON.parse(text); // Can throw
}

// ✅ GOOD: Defensive
function parseJSON(text: string): Result<any> {
  try {
    if (!text || text.trim() === '') {
      return { error: 'Empty JSON string' };
    }
    const data = JSON.parse(text);
    return { data };
  } catch (e) {
    return { error: `Invalid JSON: ${e.message}` };
  }
}
```

**Defensive checklist:**
- [ ] Validate external data (APIs, files, user input)
- [ ] Handle parsing errors (JSON, XML, CSV)
- [ ] Check function preconditions
- [ ] Return errors instead of throwing when appropriate
- [ ] Use Result types for fallible operations

## Common Anti-Patterns to Avoid

### 1. The Silent Failure

```typescript
// ❌ NEVER DO THIS
try {
  await importantOperation();
} catch (e) {
  // Empty catch - hides bugs
}
```

**Fix:** Always log, re-throw, or return error.

### 2. The String Error

```typescript
// ❌ BAD: Loses stack trace
throw "Something went wrong";

// ✅ GOOD: Proper Error object
throw new Error("Something went wrong");
```

### 3. The Floating Promise

```typescript
// ❌ BAD: Fire and forget
async function handler() {
  someAsyncOperation(); // Unhandled rejection risk
}

// ✅ GOOD: Explicit handling
async function handler() {
  void someAsyncOperation().catch(logError); // Intentional fire-and-forget
  // OR
  await someAsyncOperation(); // Wait for completion
}
```

### 4. The Type Assertion Lie

```typescript
// ❌ BAD: Assumes shape without validation
const user = apiResponse as User; // Might not be User!

// ✅ GOOD: Runtime validation
const user = UserSchema.parse(apiResponse); // Throws if invalid
```

### 5. The Magic Number

```typescript
// ❌ BAD: Unclear meaning
if (status === 2) { ... }

// ✅ GOOD: Named constant
const STATUS_COMPLETED = 2;
if (status === STATUS_COMPLETED) { ... }

// ✅ BETTER: Enum
enum Status { Pending = 1, Completed = 2 }
if (status === Status.Completed) { ... }
```

## Testing Best Practices

### Test Error Cases First

```typescript
describe('processPayment', () => {
  // Test failure modes first
  it('throws on invalid amount', () => {
    expect(() => processPayment(-10)).toThrow('Invalid amount');
  });
  
  it('throws on missing payment method', () => {
    expect(() => processPayment(10, null)).toThrow('Payment method required');
  });
  
  // Then test happy path
  it('processes valid payment', () => {
    const result = processPayment(10, { type: 'card' });
    expect(result.success).toBe(true);
  });
});
```

### Use Property-Based Testing for Edge Cases

```typescript
// Test invariants across many inputs
test('parseAmount never returns negative', () => {
  fc.assert(fc.property(fc.string(), (input) => {
    const result = parseAmount(input);
    return result === null || result >= 0;
  }));
});
```

## Pre-Commit Checklist

Before completing your task, verify:

- [ ] **Input validation**: All function inputs validated
- [ ] **Error handling**: No empty catch blocks, all errors logged
- [ ] **Null safety**: No unsafe property access (use `?.`)
- [ ] **Type safety**: No `any` types, proper union types
- [ ] **Async safety**: All promises awaited or handled
- [ ] **Resource cleanup**: Files, connections, timers cleaned up
- [ ] **Immutability**: No mutation of input parameters
- [ ] **Tests**: Error cases tested, not just happy paths
- [ ] **Documentation**: Error conditions documented
- [ ] **Logging**: Errors logged with sufficient context

## Quick Reference: Error Prevention Patterns

| Scenario | Pattern |
|----------|---------|
| External API call | Try/catch + timeout + retry logic |
| User input | Validate with schema (Zod, Joi) |
| Array access | Check length before index |
| Object property | Use optional chaining `?.` |
| Async operation | Always await or .catch() |
| Configuration | Validate at startup |
| Type unknown | Use `unknown` + type guards |
| Resource (file/socket) | Use finally or `using` |
| State machine | Discriminated unions |
| Error context | Include error cause chain |

## Further Reading

For detailed examples and reference implementations, see:
- `references/error-handling-patterns.md` - Comprehensive error handling guide
- `references/typescript-safety.md` - Advanced TypeScript safety patterns
- `references/testing-strategies.md` - Test coverage for error conditions
- `references/ai-review-checklist.md` - Code review checklist for AI agents
- `references/adversarial-review.md` - VDD pattern for hostile code review
- `references/api-reference.md` - Quick lookup for patterns and code examples
- `references/real-world-patterns.md` - Real-world implementation examples
- `references/BIOME_MIGRATION.md` - ESLint/Prettier to Biome migration guide

## When NOT to Use This Skill

- Writing proof-of-concept code (but refactor before production)
- Performance-critical hot paths (after profiling shows overhead)
- Throwaway scripts (but consider: will this become production code?)
