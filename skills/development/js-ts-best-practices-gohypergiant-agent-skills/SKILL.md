---
name: js-ts-best-practices
description: JavaScript and TypeScript best practices covering naming conventions, control flow, state management, TypeScript patterns (avoid any/enum, prefer type over interface), safety (input validation, assertions, error handling), performance optimization (reduce branching/looping, memoization, defer await, cache property access, storage API caching, avoid needless allocations, currying for hot paths), and documentation (JSDoc, comment markers). Use when writing JS/TS functions, refactoring code for performance, reviewing code quality, fixing type errors, optimizing loops or conditionals, adding validation, or improving error messages.
metadata:
  author: gohypergiant
  version: "1.1"
---

# JavaScript and TypeScript Best Practices

Comprehensive coding standards and performance optimization guide for JavaScript and TypeScript applications, designed for AI agents and LLMs working with modern JavaScript/TypeScript codebases.

## When to Activate This Skill

Use this skill when the task involves:

### Writing JavaScript/TypeScript Code
- Creating new functions, classes, or modules
- Implementing control flow logic (conditionals, loops, early returns)
- Managing state with variables (`const` vs `let`)
- Writing TypeScript type definitions, interfaces, or generics
- Defining enums or constant objects
- Structuring code with proper naming conventions

### TypeScript-Specific Tasks
- Fixing type errors or improving type safety
- Replacing `any` with proper types (`unknown`, generics)
- Converting `enum` to `as const` objects
- Choosing between `type` and `interface`
- Adding type annotations to untyped code
- Implementing generic functions or utilities

### Code Quality & Style
- Refactoring nested conditionals to early returns
- Simplifying complex control flow
- Improving variable naming (descriptive names, proper prefixes for booleans)
- Reducing code duplication (extracting common patterns)
- Applying consistent code style
- Removing commented-out code or outdated comments

### Safety & Validation
- Adding input validation at system boundaries
- Implementing assertions for programmer error detection
- Improving error handling patterns
- Writing better error messages (user-facing or developer-facing)
- Validating external data with schemas (Zod, etc.)
- Preventing null/undefined propagation

### Performance Optimization
- Reducing unnecessary branching or conditionals
- Optimizing array operations (reduce instead of chained filter/map)
- Implementing efficient data structures (Set vs Array for lookups)
- Caching expensive computations or API calls
- Optimizing loops (cache property access, array length)
- Deferring `await` operations to avoid blocking
- Caching `localStorage`, `sessionStorage`, or cookie reads

### Documentation
- Adding JSDoc comments to exported functions
- Using proper comment markers (TODO, FIXME, HACK, NOTE, PERF)
- Removing unnecessary comments
- Preserving important comments (business logic, linter directives)
- Documenting function parameters, return types, and examples

### Code Review
- Reviewing code for style violations
- Identifying performance anti-patterns
- Checking for safety issues (missing validation, poor error handling)
- Ensuring TypeScript best practices
- Verifying proper documentation

## When NOT to Use This Skill

Do not activate for:
- Framework-specific code (React, Vue, Angular) - use framework-specific skills instead
- Node.js-specific APIs or server-side concerns (unless general JS/TS patterns apply)
- Build tooling configuration (webpack, vite, tsconfig.json) unless code quality-related
- Testing code (use a testing-specific skill if available)
- Database queries or ORM usage
- CSS, HTML, or styling (unless embedded in JS/TS files)
- Package management (npm, yarn, pnpm)

## How to Use

This skill uses a **progressive disclosure** structure to minimize context usage:

### 1. Start with the Overview (AGENTS.md)
Read [AGENTS.md](AGENTS.md) for a concise overview of all rules with one-line summaries organized by category.

### 2. Load Specific Rules as Needed
When you identify a relevant pattern or issue, load the corresponding reference file for detailed implementation guidance:

**General Best Practices:**
- [naming-conventions.md](references/naming-conventions.md) - Descriptive names, qualifier ordering, boolean prefixes
- [functions.md](references/functions.md) - Function size, parameters, explicit values
- [control-flow.md](references/control-flow.md) - Early returns, flat structure, block style
- [state-management.md](references/state-management.md) - const vs let, immutability, pure functions
- [return-values.md](references/return-values.md) - Return zero values instead of null/undefined
- [misc.md](references/misc.md) - Line endings, defensive programming, technical debt
- [code-duplication.md](references/code-duplication.md) - Extract common patterns, DRY principle, when to consolidate

**TypeScript:**
- [any.md](references/any.md) - Avoid any, use unknown or generics
- [enums.md](references/enums.md) - Use as const objects instead of enum
- [type-vs-interface.md](references/type-vs-interface.md) - Prefer type over interface

**Safety:**
- [input-validation.md](references/input-validation.md) - Validate external data with schemas
- [assertions.md](references/assertions.md) - Split assertions, include values
- [error-handling.md](references/error-handling.md) - Handle all errors explicitly
- [error-messages.md](references/error-messages.md) - User-friendly vs developer-specific messages

**Performance:**
- [reduce-branching.md](references/reduce-branching.md) - Convert conditionals to lookups, hoist invariants, early returns
- [reduce-looping.md](references/reduce-looping.md) - Single-pass operations, O(1) lookups, typed arrays
- [memoization.md](references/memoization.md) - Hoist invariants, precompute constants, cache expensive operations
- [batching.md](references/batching.md) - Batch I/O operations
- [predictable-execution.md](references/predictable-execution.md) - Sequential access, cache locality, grouped data
- [bounded-iteration.md](references/bounded-iteration.md) - Set limits on loops and queues
- [defer-await.md](references/defer-await.md) - Move await into branches that need it
- [cache-property-access.md](references/cache-property-access.md) - Cache lookups, eliminate aliases, avoid unnecessary destructuring
- [cache-storage-api.md](references/cache-storage-api.md) - Cache localStorage/sessionStorage/cookie reads
- [object-operations.md](references/object-operations.md) - Safe mutation, shallow clones, preallocate shapes
- [avoid-allocations.md](references/avoid-allocations.md) - Inline simple computations, avoid needless variables, reduce GC pressure
- [currying.md](references/currying.md) - Curry to precompute constant parameters, optimize hot paths
- [performance-misc.md](references/performance-misc.md) - Strings, regex, async overhead, closures, try/catch

**Documentation:**
- [jsdoc.md](references/jsdoc.md) - Well-formed JSDoc for exports
- [comment-markers.md](references/comment-markers.md) - TODO, FIXME, HACK, NOTE markers
- [comments-to-remove.md](references/comments-to-remove.md) - Commented code, edit history
- [comments-to-preserve.md](references/comments-to-preserve.md) - Markers, linter directives, business logic
- [comments-placement.md](references/comments-placement.md) - Move end-of-line comments above code

### 3. Apply the Pattern
Each reference file contains:
- ❌ Incorrect examples showing the anti-pattern
- ✅ Correct examples showing the optimal implementation
- Explanations of why the pattern matters

## Examples

### Example 1: Optimizing Array Operations
**Task:** "This filter().map() chain is slow on large arrays"

**Approach:**
1. Read AGENTS.md overview
2. Identify issue: multiple iterations over same array
3. Load [reduce-looping.md](references/reduce-looping.md)
4. Replace chained methods with single reduce() call

**Before:**
```ts
const result = items.filter(x => x.active).map(x => x.id);
```

**After:**
```ts
const result = items.reduce((acc, x) =>
  x.active ? [...acc, x.id] : acc,
  []
);
```

### Example 2: Fixing TypeScript `any` Usage
**Task:** "Replace `any` types with proper TypeScript types"

**Approach:**
1. Read AGENTS.md overview
2. Identify need for type safety
3. Load [any.md](references/any.md)
4. Replace `any` with `unknown` or generics based on use case

**Before:**
```ts
function process(data: any): any { /**/ }
```

**After:**
```ts
function process<T>(data: T): Result<T> { /**/ }
// or
function process(data: unknown): User { /**/ }
```

### Example 3: Improving Error Messages
**Task:** "Make error messages more helpful for users"

**Approach:**
1. Read AGENTS.md overview
2. Identify need for better error messaging
3. Load [error-messages.md](references/error-messages.md)
4. Replace technical errors with user-friendly, actionable messages

**Before:**
```ts
throw new Error('500');
```

**After:**
```ts
alert(
  'We\'re having trouble connecting to our server.\n' +
  'Please check your internet connection and try again.'
);
```

### Example 4: Caching Storage API Calls
**Task:** "This function calls localStorage.getItem() 100 times in a loop"

**Approach:**
1. Read AGENTS.md overview
2. Identify performance issue: repeated storage reads
3. Load [cache-storage-api.md](references/cache-storage-api.md)
4. Implement Map-based cache with invalidation strategy

**Before:**
```ts
for (const item of items) {
  const theme = localStorage.getItem('theme');
  // ... 100 storage reads
}
```

**After:**
```ts
const storageCache = new Map();
function getCached(key) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key));
  }
  return storageCache.get(key);
}

for (const item of items) {
  const theme = getCached('theme');
  // ... 1 storage read
}
```

### Example 5: Avoiding Needless Allocations
**Task:** "This random number function has GC pressure when called in a loop"

**Approach:**
1. Read AGENTS.md overview
2. Identify issue: intermediate variable creating unnecessary allocations
3. Load [avoid-allocations.md](references/avoid-allocations.md)
4. Inline simple computation to eliminate allocation

**Before:**
```ts
function randomInt(min: number, max: number): number {
  const minCeil = Math.ceil(min);
  const maxFloor = Math.floor(max);
  const range = maxFloor - minCeil + 1;
  return Math.floor(Math.random() * range + minCeil);
}
```

**After:**
```ts
function randomInt(min: number, max: number): number {
  const minCeil = Math.ceil(min);
  const maxFloor = Math.floor(max);
  return Math.floor(Math.random() * (maxFloor - minCeil + 1) + minCeil);
}
```

### Example 6: Currying for Performance
**Task:** "This round() function recomputes 10 ** precision on every call in a loop"

**Approach:**
1. Read AGENTS.md overview
2. Identify issue: expensive exponentiation repeated with constant parameter
3. Load [currying.md](references/currying.md)
4. Convert to curried form to precompute multiplier

**Before:**
```ts
export function round(precision: number, value: number): number {
  const multiplier = 10 ** precision;
  return Math.round(value * multiplier) / multiplier;
}

for (const price of prices) {
  rounded.push(round(2, price)); // Recomputes 10 ** 2 every time
}
```

**After:**
```ts
export function round(precision: number): (value: number) => number;
export function round(precision: number, value: number): number;
export function round(
  precision: number,
  value?: number,
): number | ((value: number) => number) {
  const multiplier = 10 ** precision;

  if (value === undefined) {
    return (v: number) => Math.round(v * multiplier) / multiplier;
  }

  return Math.round(value * multiplier) / multiplier;
}

const roundTo2 = round(2); // Compute once
for (const price of prices) {
  rounded.push(roundTo2(price)); // Reuse precomputed multiplier
}
```

## Important Notes

### Performance Philosophy
Design for performance from the start. Optimize slowest resources first:
```
network >> disk >> memory >> cpu
```

Always **benchmark your assumptions** before moving on. Premature optimization of CPU-bound operations while ignoring network bottlenecks wastes time.

### State Management Principles
- **Prefer `const`**: Use `let` only for valid performance reasons
- **Immutability**: Never mutate passed references; create copies
- **Pure functions**: Keep leaf functions pure; centralize state in parents
- **Zero values**: Return `[]`, `{}`, `0`, `''` instead of `null`/`undefined`

### TypeScript Best Practices
- **Avoid `any`**: Use `unknown` for truly unknown types, generics for flexibility
- **Avoid `enum`**: Use `as const` objects for better tree-shaking and type inference
- **Prefer `type`**: Use `interface` only for declaration merging or class contracts

### Code Quality Principles
- **Functions under 50 lines**: Break down large functions
- **Early returns**: Prefer flat control flow over nested conditionals
- **Descriptive names**: Use complete words, append qualifiers in descending order
- **Explicit values**: Avoid default parameters; make all values explicit at call site

### Safety First
- **Validate at boundaries**: All external data must be validated (user input, API responses)
- **Assertions for programmer errors**: Crash on corrupted code state
- **Split compound assertions**: One assertion per invariant
- **Include values in messages**: Always show actual vs expected values

### Documentation Standards
- **All code needs JSDoc**: Functions, types, interfaces, constants, and classes require JSDoc
- **Required tags (all code)**: Description, `@param`, `@template`, `@returns`
- **Required tags (exports only)**: `@throws`, `@example` (in addition to above)
- **Use comment markers**: TODO, FIXME, HACK, NOTE, REVIEW, PERF
- **Remove dead code**: No commented-out code or edit history
- **Preserve business logic**: Keep comments explaining "why", not "what"

## Optimization Strategies

When optimizing performance:

1. **Measure first**: Use profiling tools to identify actual bottlenecks
2. **Network first**: Optimize network requests before code execution
3. **Reduce iterations**: Single reduce() instead of chained filter().map()
4. **Cache lookups**: Use Set for O(1) membership checks, cache property access in loops
5. **Defer work**: Move expensive operations (await, computation) into branches that need them
6. **Batch operations**: Group I/O operations to reduce overhead
7. **Predictable paths**: Write code with clear execution flow for CPU optimization

## Additional Context

### When Functions Are Too Small
Some patterns (like lookup tables) may seem to violate the "no premature optimization" principle. These are **architectural choices**, not optimizations:
- Lookup tables improve maintainability (add entries without new conditionals)
- Early returns reduce cognitive load (fewer nested levels)
- Const over let prevents accidental mutations (correctness, not speed)

### Defensive Programming
This skill emphasizes "negative-space" or defensive programming:
- Return zero values to eliminate downstream null checks
- Assert invariants to catch bugs early
- Validate at boundaries to contain invalid data
- Handle all errors explicitly (no silent failures)

The goal is **correctness first, performance second**.
