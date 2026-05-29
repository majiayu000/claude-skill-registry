---
name: async-await-patterns
description: Use when writing JavaScript or TypeScript code with asynchronous operations
---

<ROLE>
Async/Await Specialist. Reputation depends on correct, non-blocking code without race conditions or unhandled rejections.
</ROLE>

## Invariant Principles

1. **Explicit async boundary**: Function containing await MUST be marked async. Compiler enforces; no exceptions.
2. **Await ALL promises**: Every promise-returning call requires await. Missing await = bug (returns Promise, not value).
3. **Structured error handling**: try-catch wraps async operations. Unhandled rejections crash applications.
4. **Pattern consistency**: async/await XOR promise chains. Never mix in same function.
5. **Parallelism via combinators**: Independent operations use Promise.all/allSettled. Sequential only when dependencies exist.

## Required Reasoning

<analysis>
Before writing async code:
- Is operation asynchronous? (fetch, I/O, database, timers)
- Function marked async?
- Every promise awaited?
- Error handling in place?
- Operations independent? → Promise.all candidate
</analysis>

## Core Pattern

```typescript
async function operationName(): Promise<ReturnType> {
  try {
    const result = await asyncOperation();
    return result;
  } catch (error) {
    // Handle or rethrow with context
    throw error;
  }
}
```

## Forbidden → Correct

| Anti-pattern | Fix |
|--------------|-----|
| `.then()/.catch()` chains | async/await with try-catch |
| `const x = asyncFn()` (missing await) | `const x = await asyncFn()` |
| `function` with await inside | `async function` |
| Await without try-catch | Wrap in try-catch |
| Mix async/await + .then() | Pure async/await |

## Parallel vs Sequential

```typescript
// PARALLEL: independent operations
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);

// SEQUENTIAL: each depends on previous
const inventory = await checkInventory();
const payment = await processPayment(inventory);
const order = await createOrder(payment);

// FAULT-TOLERANT: continue despite failures
const results = await Promise.allSettled([op1(), op2(), op3()]);
```

## Complete Example

```typescript
async function updateProfile(userId: string, updates: Updates): Promise<User> {
  try {
    const user = await database.users.findById(userId);
    if (!user) throw new Error(`User ${userId} not found`);

    const validated = await validateData(updates);
    const updated = await database.users.update(userId, validated);

    await Promise.all([
      notify(userId, 'Profile updated'),
      auditLog.record('profile_update', { userId })
    ]);

    return updated;
  } catch (error) {
    if (error instanceof ValidationError) throw new BadRequestError('Invalid data', error);
    if (error instanceof DatabaseError) throw new ServiceError('DB failed', error);
    throw error;
  }
}
```

<reflection>
Verify before submission:
- [ ] async keyword present?
- [ ] await on EVERY promise?
- [ ] try-catch wrapping?
- [ ] No .then()/.catch() mixing?
- [ ] Parallel ops using Promise.all?

Failure on ANY check → rewrite required.
</reflection>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Code with async operations | Yes | JavaScript/TypeScript code needing async handling |
| Dependency graph | No | Which operations depend on others (determines parallel vs sequential) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Async code | Inline | Properly structured async/await code |
| Error handling strategy | Inline | try-catch blocks with typed error handling |

<FORBIDDEN>
- Using .then()/.catch() chains instead of async/await
- Missing await on promise-returning calls
- Mixing async/await with promise chains in same function
- Omitting try-catch around async operations
- Using callbacks when promises available
- Sequential awaits for independent operations
</FORBIDDEN>

## Self-Check

Before completing:
- [ ] Every function with await is marked async
- [ ] Every promise-returning call has await
- [ ] All async operations wrapped in try-catch
- [ ] No .then()/.catch() mixed with async/await
- [ ] Independent operations use Promise.all
- [ ] Error handling preserves error context

If ANY unchecked: STOP and fix.
