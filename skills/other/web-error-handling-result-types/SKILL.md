---
name: web-error-handling-result-types
description: TypeScript Result/Either types for type-safe error handling, railway-oriented programming patterns, error as values
---

# TypeScript Result Type Patterns

> **Quick Guide:** Result types make errors explicit in function signatures, forcing callers to handle both success and failure cases. Use for expected/recoverable errors (validation, API calls, parsing). Keep exceptions for truly exceptional situations (programming bugs, unrecoverable errors). Result types are ~300x faster than exceptions.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST check result.ok before accessing result.value or result.error - TypeScript enforces this)**

**(You MUST wrap ALL throwable operations (JSON.parse, etc.) in tryCatch when inside Result-returning functions)**

**(You MUST use typed error objects with discriminant properties (code, type) - NOT generic Error or string)**

**(You MUST handle ALL Result values - never ignore return value of Result-returning functions)**

**(You MUST use flatMap/andThen for chaining Results - NOT nested if statements)**

</critical_requirements>

---

**Auto-detection:** Result type, Either type, ok err, railway-oriented programming, error as value, flatMap andThen, tryCatch, neverthrow, fp-ts Either, discriminated union error, typed errors

**When to use:**

- Handling expected, recoverable errors (validation, parsing, API calls)
- Building APIs where callers need to know all failure modes
- Performance-critical code (Results are ~300x faster than exceptions)
- Creating explicit error contracts in function signatures
- Chaining operations that may fail (railway-oriented programming)

**Key patterns covered:**

- Basic Result type definition and usage
- Mapping success and error values
- Chaining operations with flatMap/andThen
- Combining multiple Results (fail-fast and collect-all)
- Wrapping throwable operations
- Async Result patterns
- Pattern matching on Results

**When NOT to use:**

- Truly exceptional/unexpected situations (use exceptions)
- Unrecoverable errors (configuration missing at startup)
- Optional values without error info (use `T | null` or Option type)
- Simple boolean checks (use plain boolean)
- Framework boundaries that expect exceptions (Express error handlers)

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For async patterns, see [examples/async.md](examples/async.md)
- For combining multiple Results, see [examples/combining.md](examples/combining.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Result types bring **errors into the type system**, making them impossible to ignore. Unlike exceptions which create hidden control flow, Results are values that must be explicitly handled. The key principle is **errors as data** - a function that can fail returns `Result<T, E>` where both success and failure are first-class citizens.

**Core principles:**

1. **Explicit over implicit** - Function signatures show exactly what can go wrong
2. **Composition over nesting** - Chain operations with map/flatMap instead of nested if/try
3. **Type safety over runtime checks** - TypeScript prevents accessing wrong property
4. **Performance over convenience** - Results are ~300x faster than throwing exceptions

**The Railway Metaphor:**

Think of operations as railway tracks. Success keeps you on the main track. Errors switch you to the error track. Once on the error track, subsequent operations are skipped until you explicitly handle the error.

```
     parseNumber     validatePositive     double
OK   ─────────────────────────────────────────────> success
                  ↘                  ↘
ERR                 ────────────────────────────> failure
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Result Type Definition

The minimal Result type uses a discriminated union with `ok` as the discriminant.

#### Type Definition

```typescript
// result.ts - Zero-dependency implementation
export type Result<T, E = Error> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E };

// Constructor functions
export const ok = <T>(value: T): Result<T, never> => ({
  ok: true,
  value,
});

export const err = <E>(error: E): Result<never, E> => ({
  ok: false,
  error,
});
```

**Why good:** Discriminated union enables TypeScript narrowing, readonly prevents mutation, `never` in constructors enables type inference, zero dependencies

#### Usage

```typescript
// ✅ Good Example - Explicit error handling
interface DivisionError {
  code: "DIVISION_BY_ZERO";
  message: string;
}

const DIVISION_BY_ZERO_ERROR: DivisionError = {
  code: "DIVISION_BY_ZERO",
  message: "Cannot divide by zero",
};

function divide(a: number, b: number): Result<number, DivisionError> {
  if (b === 0) {
    return err(DIVISION_BY_ZERO_ERROR);
  }
  return ok(a / b);
}

// TypeScript FORCES handling both cases
const result = divide(10, 2);
if (result.ok) {
  console.log(`Result: ${result.value}`); // TypeScript knows: number
} else {
  console.error(`Error: ${result.error.message}`); // TypeScript knows: DivisionError
}
```

**Why good:** Error handling is mandatory (not optional), TypeScript narrows types in each branch, error type is known and actionable, pre-created error object avoids allocation in hot paths

```typescript
// ❌ Bad Example - Ignoring Result
function process(input: string): void {
  divide(10, 0); // Result is discarded!
  console.log("Done"); // Continues as if nothing went wrong
}
```

**Why bad:** Defeats the purpose of Result types - errors are silently ignored, no type error because void function discards all returns

---

### Pattern 2: Mapping Values (map and mapError)

Transform success or error values without affecting the other case.

```typescript
// map - Transform success value
export const map = <T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U,
): Result<U, E> => (result.ok ? ok(fn(result.value)) : result);

// mapError - Transform error value
export const mapError = <T, E, F>(
  result: Result<T, E>,
  fn: (error: E) => F,
): Result<T, F> => (result.ok ? result : err(fn(result.error)));
```

#### Usage

```typescript
// ✅ Good Example - Chaining transformations
const DOUBLE_MULTIPLIER = 2;

const result = divide(10, 2);
const doubled = map(result, (n) => n * DOUBLE_MULTIPLIER);
// Result<number, DivisionError> with value 10

// Transform error to add context
const withContext = mapError(divide(10, 0), (e) => ({
  ...e,
  context: "calculating ratio",
}));
```

**Why good:** Transforms only the relevant case, preserves error if already failed, composable with other operations

---

### Pattern 3: Chaining Operations (flatMap/andThen)

Chain operations that each return Results. This is the core of railway-oriented programming.

```typescript
export const flatMap = <T, U, E, F>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, F>,
): Result<U, E | F> => (result.ok ? fn(result.value) : result);

// Alias - some prefer this name
export const andThen = flatMap;
```

#### Usage

```typescript
// ✅ Good Example - Chaining multiple operations
interface ParseError {
  code: "PARSE_ERROR";
  message: string;
}

interface ValidationError {
  code: "VALIDATION_ERROR";
  field: string;
}

const MIN_VALUE = 0;

function parseNumber(input: string): Result<number, ParseError> {
  const num = Number(input);
  if (Number.isNaN(num)) {
    return err({ code: "PARSE_ERROR", message: `Invalid number: ${input}` });
  }
  return ok(num);
}

function validatePositive(num: number): Result<number, ValidationError> {
  if (num <= MIN_VALUE) {
    return err({ code: "VALIDATION_ERROR", field: "number" });
  }
  return ok(num);
}

// Chain operations - error short-circuits the chain
const result = flatMap(parseNumber("42"), validatePositive);
// Result<number, ParseError | ValidationError>
```

**Why good:** Each step can fail with different error type, error in early step skips later steps, error types are unioned automatically

```typescript
// ❌ Bad Example - Nested if statements
function processInput(
  input: string,
): Result<number, ParseError | ValidationError> {
  const parseResult = parseNumber(input);
  if (parseResult.ok) {
    const validateResult = validatePositive(parseResult.value);
    if (validateResult.ok) {
      return ok(validateResult.value);
    }
    return validateResult;
  }
  return parseResult;
}
```

**Why bad:** Deep nesting, harder to read, doesn't scale with more operations, error handling scattered

---

### Pattern 4: Wrapping Throwable Functions

Convert exception-throwing code to Result-returning code at boundaries.

```typescript
export const tryCatch = <T, E>(
  fn: () => T,
  onError: (error: unknown) => E,
): Result<T, E> => {
  try {
    return ok(fn());
  } catch (error) {
    return err(onError(error));
  }
};
```

#### Usage

```typescript
// ✅ Good Example - Wrapping JSON.parse
interface JsonParseError {
  code: "JSON_PARSE_ERROR";
  message: string;
  input: string;
}

function safeJsonParse<T>(json: string): Result<T, JsonParseError> {
  return tryCatch(
    () => JSON.parse(json) as T,
    (error): JsonParseError => ({
      code: "JSON_PARSE_ERROR",
      message: error instanceof Error ? error.message : "Unknown parse error",
      input: json,
    }),
  );
}

const parsed = safeJsonParse<{ name: string }>('{"name": "John"}');
if (parsed.ok) {
  console.log(parsed.value.name); // TypeScript knows shape
}
```

**Why good:** Converts exceptions to Results at boundary, error carries context (input), typed error enables proper handling

```typescript
// ❌ Bad Example - Mixing throw and Result
function parseUser(json: string): Result<User, ParseError> {
  const data = JSON.parse(json); // Can throw SyntaxError!
  if (!data.name) {
    return err({ code: "PARSE_ERROR", message: "Missing name" });
  }
  return ok(data);
}
```

**Why bad:** Function signature lies - can throw exceptions despite returning Result, caller doesn't know to wrap in try/catch

---

### Pattern 5: Pattern Matching (match)

Handle both cases in a single expression with exhaustive pattern matching.

```typescript
export const match = <T, E, U>(
  result: Result<T, E>,
  handlers: { ok: (value: T) => U; err: (error: E) => U },
): U => (result.ok ? handlers.ok(result.value) : handlers.err(result.error));
```

#### Usage

```typescript
// ✅ Good Example - Pattern matching
const message = match(divide(10, 2), {
  ok: (value) => `Result: ${value}`,
  err: (error) => `Error: ${error.message}`,
});

// For HTTP responses
const response = match(fetchUser("123"), {
  ok: (user) => ({ status: 200, body: user }),
  err: (error) => {
    switch (error.code) {
      case "NOT_FOUND":
        return { status: 404, body: { message: `User ${error.id} not found` } };
      case "UNAUTHORIZED":
        return { status: 401, body: { message: "Please log in" } };
      default:
        return { status: 500, body: { message: "Internal error" } };
    }
  },
});
```

**Why good:** Both cases handled in one expression, TypeScript ensures exhaustiveness, clean transformation to other types

---

### Pattern 6: Typed Error Objects

Define specific error types for each failure mode using discriminated unions.

```typescript
// ✅ Good Example - Typed error hierarchy
interface ValidationError {
  code: "VALIDATION_ERROR";
  field: string;
  message: string;
}

interface NotFoundError {
  code: "NOT_FOUND";
  resource: string;
  id: string;
}

interface NetworkError {
  code: "NETWORK_ERROR";
  statusCode: number;
  message: string;
}

// Union of all errors for a domain
type UserError = ValidationError | NotFoundError | NetworkError;

// Function signature documents all failure modes
function fetchUser(id: string): Promise<Result<User, UserError>> {
  // Implementation
}

// Caller can handle each case specifically
const result = await fetchUser("123");
if (!result.ok) {
  switch (result.error.code) {
    case "NOT_FOUND":
      console.log(`User ${result.error.id} not found`);
      break;
    case "UNAUTHORIZED":
      redirectToLogin();
      break;
    case "NETWORK_ERROR":
      showRetryButton();
      break;
  }
}
```

**Why good:** Each error type carries relevant data, switch exhaustiveness checking, callers know exactly what can fail

```typescript
// ❌ Bad Example - Generic error types
function fetchUser(id: string): Result<User, Error> {
  // Caller can't distinguish error types
}

function fetchUser(id: string): Result<User, string> {
  // Even worse - just a message, no structure
}
```

**Why bad:** Caller can't handle different errors differently, error information is lost, defeats type safety benefits

</patterns>

---

<decision_framework>

## Decision Framework

### When to Use Result vs Exceptions

```
Is this an expected, recoverable error?
├─ YES → Use Result type
│   ├─ User input validation
│   ├─ API call that might fail
│   ├─ Parsing untrusted data
│   └─ Business rule violations
└─ NO → Is it a programming bug?
    ├─ YES → Use exceptions (let it crash)
    │   ├─ Index out of bounds (caller bug)
    │   ├─ Null reference (missing check)
    │   └─ Invalid state (logic error)
    └─ NO → Is it unrecoverable?
        ├─ YES → Use exceptions
        │   ├─ Missing required config
        │   └─ Database connection failed
        └─ NO → Evaluate case by case
```

### Choosing a Result Library

```
What are your requirements?
├─ Zero dependencies → Custom implementation
├─ Simple needs + small bundle → neverthrow (~2KB)
├─ Full FP ecosystem → fp-ts (~30KB)
├─ Production app with async → neverthrow (ResultAsync)
└─ Just learning → Custom implementation (understand the pattern)
```

### Result vs Nullable

```
What information does failure carry?
├─ Just "not found" → Use T | null
├─ Error with details → Use Result<T, E>
│   ├─ Why it failed
│   ├─ What to do about it
│   └─ Context for logging
└─ Multiple failure modes → Use Result<T, E>
```

</decision_framework>

---

<integration>

## Integration Points

**Result types integrate with your application through:**

- **Function signatures**: Return type documents all failure modes
- **Error boundaries**: Convert Results to UI at component level
- **API responses**: Transform Results to HTTP status codes
- **Logging**: Extract error details for observability

**Results work alongside:**

- **Exceptions**: For truly exceptional situations at outer boundaries
- **Validation libraries**: Wrap validation results in Result type
- **Data fetching**: Wrap fetch/API calls in Result-returning functions

**Results do NOT replace:**

- **React Error Boundaries**: Boundaries catch render errors; Results handle business logic errors
- **HTTP error handling**: Convert Results to appropriate status codes at API boundary
- **Form validation**: Use Results internally, display errors via your form library

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST check result.ok before accessing result.value or result.error - TypeScript enforces this)**

**(You MUST wrap ALL throwable operations (JSON.parse, etc.) in tryCatch when inside Result-returning functions)**

**(You MUST use typed error objects with discriminant properties (code, type) - NOT generic Error or string)**

**(You MUST handle ALL Result values - never ignore return value of Result-returning functions)**

**(You MUST use flatMap/andThen for chaining Results - NOT nested if statements)**

**Failure to follow these rules will result in silent error handling bugs, loss of type safety, and defeats the purpose of using Result types.**

</critical_reminders>
