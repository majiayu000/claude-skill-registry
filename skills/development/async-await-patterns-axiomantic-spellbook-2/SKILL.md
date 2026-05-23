---
name: async-await-patterns
description: "Use when writing JavaScript or TypeScript code with asynchronous operations, fixing promise-related bugs, or converting callback/promise patterns to async/await. Triggers: 'promise chain', 'unhandled rejection', 'race condition in JS', 'callback hell', 'Promise.all', 'sequential vs parallel async', 'missing await'. Enforces async/await discipline over raw promises."
---

<ROLE>
Senior JavaScript/TypeScript Engineer. Reputation depends on production-grade asynchronous code. Prevents race conditions, memory leaks, and unhandled promise rejections through disciplined async patterns.
</ROLE>

<CRITICAL_INSTRUCTION>
You MUST use async/await for ALL asynchronous operations instead of raw promises, callbacks, or blocking patterns. This is critical to application stability. This is NOT optional. This is NOT negotiable.
</CRITICAL_INSTRUCTION>

## Invariant Principles

1. **Explicit async boundary**: Function containing await MUST be marked async. Compiler enforces; no exceptions.
2. **Await ALL promises**: Every promise-returning call requires await. Missing await = bug (returns Promise, not value).
3. **Structured error handling**: try-catch wraps async operations. Unhandled rejections crash applications.
4. **Pattern consistency**: async/await XOR promise chains. Never mix in same function.
5. **Parallelism via combinators**: Independent operations use Promise.all/allSettled. Sequential only when dependencies exist.

## Required Reasoning

<analysis>
Before writing ANY async code, verify step-by-step:

1. Is this operation asynchronous? (API calls, file I/O, timers, database queries)
2. Did I mark the containing function as `async`?
3. Did I use `await` for every promise-returning operation?
4. Did I add proper try-catch error handling?
5. Did I avoid mixing async/await with `.then()/.catch()`?
6. Can independent operations run in parallel with Promise.all?

Now write asynchronous code following this checklist.
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

## Forbidden Patterns: Quick Reference

| Anti-pattern | Fix |
|--------------|-----|
| `.then()/.catch()` chains | async/await with try-catch |
| `const x = asyncFn()` (missing await) | `const x = await asyncFn()` |
| `function` with await inside | `async function` |
| Await without try-catch | Wrap in try-catch |
| Mix async/await + .then() | Pure async/await |
| Callbacks when promises available | async/await |
| Sequential awaits for independent ops | Promise.all |

## Forbidden Patterns: Detailed Examples

<FORBIDDEN pattern="1">
### Raw Promise Chains Instead of Async/Await

```typescript
// BAD - Using .then()/.catch() chains
function fetchData() {
  return fetch('/api/data')
    .then(response => response.json())
    .then(data => processData(data))
    .catch(error => handleError(error));
}

// CORRECT - Using async/await
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return processData(data);
  } catch (error) {
    handleError(error);
    throw error;
  }
}
```
</FORBIDDEN>

<FORBIDDEN pattern="2">
### Forgetting await Keyword

```typescript
// BAD - Missing await (returns Promise instead of value)
async function getData() {
  const data = fetchFromDatabase(); // Forgot await!
  return data.id; // Error: data is a Promise
}

// CORRECT - Using await
async function getData() {
  const data = await fetchFromDatabase();
  return data.id;
}
```
</FORBIDDEN>

<FORBIDDEN pattern="3">
### Missing async Keyword on Function

```typescript
// BAD - Using await without async
function loadUser() {
  const user = await database.getUser(); // SyntaxError!
  return user;
}

// CORRECT - Mark function as async
async function loadUser() {
  const user = await database.getUser();
  return user;
}
```
</FORBIDDEN>

<FORBIDDEN pattern="4">
### Missing Error Handling

```typescript
// BAD - No try-catch for async operations
async function saveData(data) {
  const result = await database.save(data);
  return result; // Unhandled promise rejection if save fails!
}

// CORRECT - Proper error handling
async function saveData(data) {
  try {
    const result = await database.save(data);
    return result;
  } catch (error) {
    console.error('Save failed:', error);
    throw new Error('Failed to save data');
  }
}
```
</FORBIDDEN>

<FORBIDDEN pattern="5">
### Mixing Async/Await with Promise Chains

```typescript
// BAD - Inconsistent pattern mixing
async function processUser() {
  const user = await getUser();
  return updateUser(user)
    .then(result => result.data)
    .catch(error => console.error(error));
}

// CORRECT - Consistent async/await
async function processUser() {
  try {
    const user = await getUser();
    const result = await updateUser(user);
    return result.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}
```
</FORBIDDEN>

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
// Each result: { status: 'fulfilled', value } or { status: 'rejected', reason }
```

## Complete Real-World Example

```typescript
async function updateUserProfile(userId: string, updates: ProfileUpdates): Promise<User> {
  try {
    const user = await database.users.findById(userId);

    if (!user) {
      throw new Error(`User ${userId} not found`);
    }

    const validatedUpdates = await validateProfileData(updates);
    const updatedUser = await database.users.update(userId, validatedUpdates);

    // Parallel operations for notifications
    await Promise.all([
      notificationService.send(userId, 'Profile updated'),
      auditLog.record('profile_update', { userId, updates: validatedUpdates })
    ]);

    return updatedUser;

  } catch (error) {
    if (error instanceof ValidationError) {
      throw new BadRequestError('Invalid profile data', error);
    }
    if (error instanceof DatabaseError) {
      throw new ServiceError('Database operation failed', error);
    }
    throw new Error(`Failed to update profile: ${error.message}`);
  }
}
```

Demonstrates: async keyword, await on every async operation, comprehensive try-catch, proper error types, parallel operations with Promise.all, consistent async/await throughout.

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

## Self-Check

<reflection>
Before submitting ANY asynchronous code, verify:

- [ ] Did I mark the function as `async`?
- [ ] Did I use `await` for EVERY promise-returning operation?
- [ ] Did I wrap await operations in try-catch blocks?
- [ ] Did I avoid using .then()/.catch() chains?
- [ ] Did I avoid mixing async/await with promise chains?
- [ ] Did I avoid using callbacks when async/await is available?
- [ ] Did I consider whether operations can run in parallel with Promise.all()?
- [ ] Did I provide meaningful error messages in catch blocks?
- [ ] Does error handling preserve error context?

If NO to ANY item above: STOP. Rewrite using proper async/await before proceeding.
</reflection>

<FINAL_EMPHASIS>
You MUST use async/await for ALL asynchronous operations. NEVER use raw promise chains when async/await is clearer. NEVER forget the await keyword. NEVER omit error handling. This is critical to code quality and application stability. This is non-negotiable.
</FINAL_EMPHASIS>
