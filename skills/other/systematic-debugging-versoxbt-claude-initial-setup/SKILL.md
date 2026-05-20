---
name: systematic-debugging
description: >
  Apply structured debugging techniques to find and fix bugs efficiently.
  Use when the user reports a bug, encounters unexpected behavior, says something
  is "not working", or asks for help debugging. Apply hypothesis-driven debugging
  instead of random changes.
---

# Systematic Debugging

Find bugs efficiently through hypothesis testing, binary search, and structured elimination rather than trial and error.

## When to Use

- A bug report or unexpected behavior is described
- Tests are failing for unknown reasons
- Something "used to work" and now does not
- The user says "it does not work" without a clear cause
- A production issue needs rapid root cause identification

## Core Patterns

### The Debugging Loop

Follow this process for every bug:

```
1. REPRODUCE    — Confirm the bug exists and get consistent repro steps
2. HYPOTHESIZE  — Form 2-3 theories about the cause
3. TEST         — Design the smallest experiment to confirm/reject each theory
4. ISOLATE      — Narrow down to the exact line/condition
5. FIX          — Apply the minimal fix
6. VERIFY       — Confirm the fix resolves the issue without regressions
```

```bash
# Step 1: Reproduce reliably
# Write down exact steps, inputs, and expected vs actual output

# Step 2: Form hypotheses
# "The null pointer is because user.address is undefined when user has no profile"
# "The timeout is because the database connection pool is exhausted"

# Step 3: Test one hypothesis at a time
# Add a focused log or assertion, not 20 print statements
```

### Binary Search Debugging

When you know something worked at point A and is broken at point B, bisect to find the breaking change:

```bash
# Git bisect for finding the breaking commit
git bisect start
git bisect bad                    # Current commit is broken
git bisect good v2.1.0            # This version worked
# Git checks out a midpoint — test it
# Mark as good/bad, repeat until the breaking commit is found
git bisect good   # or: git bisect bad
# ... repeat ...
git bisect reset  # When done

# Automated bisect with a test script
git bisect start HEAD v2.1.0
git bisect run npm test
```

Apply the same principle to code:

```typescript
// Binary search within a function: comment out half the logic
// If bug disappears, the problem is in the commented half
// If bug remains, the problem is in the active half
// Repeat until isolated

async function processOrder(order: Order): Promise<Result> {
  const validated = validateOrder(order);        // Phase 1
  const enriched = await enrichWithPricing(validated); // Phase 2
  const reserved = await reserveInventory(enriched);   // Phase 3
  const result = await chargePayment(reserved);        // Phase 4
  return result;
}

// Does the bug occur after Phase 2?
// Comment out Phase 3 and 4 → test → narrow down
```

### Minimal Reproduction

Strip away everything unrelated to the bug:

```typescript
// Production code with layers of complexity
const result = await pipeline
  .authenticate(req)
  .validate(schema)
  .transform(normalize)
  .execute(handler)
  .catch(errorHandler);

// Minimal reproduction — call only the suspected layer
const testInput = { id: "123", name: null }; // The failing case
const result = normalize(testInput);         // Test in isolation
console.log(result);                         // See exactly what happens
```

```bash
# Create a minimal test file to reproduce in isolation
cat > /tmp/repro.ts << 'EOF'
// Minimal reproduction of the date parsing bug
function parseDate(input: string): Date {
  return new Date(input);
}

// These work
console.log(parseDate("2024-01-15"));       // OK
console.log(parseDate("2024-1-15"));        // OK

// This fails
console.log(parseDate("15/01/2024"));       // NaN — found it
EOF
npx tsx /tmp/repro.ts
```

### Hypothesis Testing with Targeted Logging

Add focused, temporary logging to test one hypothesis at a time:

```typescript
// BAD: Scatter-shot logging
console.log("here 1");
console.log("data:", data);
console.log("here 2");
console.log("result:", result);
console.log("here 3");

// GOOD: Hypothesis-driven logging
// Hypothesis: "order.items is empty when it reaches calculateTotal"
async function processOrder(order: Order): Promise<void> {
  console.log("[DEBUG] order.items at processOrder entry:", {
    count: order.items.length,
    items: order.items.map((i) => i.id),
  });
  // ... rest of function
}
// Test, confirm or reject, then remove the log
```

### Rubber Duck Debugging

When stuck, explain the problem out loud (or in writing). Structure the explanation:

```
1. What SHOULD happen:
   "When a user submits the form, it should validate inputs,
   send a POST to /api/orders, and redirect to the confirmation page."

2. What ACTUALLY happens:
   "The form submits, the API call succeeds (I see 201 in network tab),
   but the redirect never fires."

3. What I have ALREADY checked:
   "The API response is correct. The redirect function is called.
   The URL is correct."

4. What I have NOT checked:
   "Whether the redirect is being blocked by the form's default
   submit behavior reloading the page first."
   // ^ Often the answer reveals itself here
```

### Divide and Conquer for Intermittent Bugs

```typescript
// For bugs that only happen sometimes, add guards and logging
// to narrow down the conditions

function processPayment(order: Order): Result {
  // Capture the exact state when the bug occurs
  if (!order.total || order.total <= 0) {
    console.error("[BUG HUNT] Invalid total detected:", {
      orderId: order.id,
      total: order.total,
      items: order.items.length,
      createdAt: order.createdAt,
      stack: new Error().stack,
    });
  }

  // ... normal processing
}

// For race conditions, add timestamps
const start = performance.now();
await operationA();
console.log(`[TIMING] operationA: ${performance.now() - start}ms`);
await operationB();
console.log(`[TIMING] operationB: ${performance.now() - start}ms`);
```

## Anti-Patterns

### What NOT to Do

- **Random changes**: Changing things until the bug disappears without understanding why. The bug may just be hidden.
- **Fixing symptoms**: Adding null checks to silence errors without understanding why the value is null.
- **Too many changes at once**: Modifying 5 things and testing — if the bug is fixed, you do not know which change fixed it.
- **Ignoring error messages**: Stack traces and error messages contain the answer most of the time. Read them carefully.
- **Debugging in production**: Add the logging or reproduction locally first. Only add production observability through structured logging, not ad-hoc prints.

```typescript
// BAD: Fix the symptom
function getUser(id: string) {
  const user = db.find(id);
  return user || { name: "Unknown" }; // Hides the real bug — why is user null?
}

// GOOD: Investigate the root cause
function getUser(id: string) {
  const user = db.find(id);
  if (!user) {
    throw new Error(`User not found: ${id}`);
    // Now you can trace WHY this ID does not exist
  }
  return user;
}
```

## Quick Reference

```
Debugging Loop:
  REPRODUCE -> HYPOTHESIZE -> TEST -> ISOLATE -> FIX -> VERIFY

Techniques:
  Binary search     Bisect code/commits to narrow down the cause
  Minimal repro     Strip to smallest failing case
  Hypothesis test   One focused log per theory
  Rubber duck       Explain the problem step by step
  Git bisect        Automate finding the breaking commit

Questions to Ask:
  1. What changed recently? (code, deps, config, data)
  2. Can I reproduce it consistently?
  3. What are 2-3 possible causes?
  4. What is the simplest test to eliminate each cause?
  5. What does the error message actually say?

Common Root Causes:
  - Null/undefined where a value is expected
  - Race condition or timing issue
  - Wrong variable or off-by-one error
  - Stale cache or memoization
  - Environment difference (dev vs prod)
  - Dependency version mismatch
  - Incorrect type coercion
```
