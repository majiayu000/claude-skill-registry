---
name: js-ts-performance-readability
description: "Write JavaScript/TypeScript that is performant, readable, and easy to trust with minimal inspection. Use when generating or reviewing JS/TS code—scripts, utilities, data processing, or performance-sensitive logic—so outputs are correct, fast, and maintainable without heavy manual review."
compatibility: "JavaScript or TypeScript; Node, Deno, or browser. Assumes ES2020+ (optional chaining, nullish coalescing, .at(), .findLast(), Promise.allSettled, etc.)."
metadata:
  author: icyJoseph
  version: "1.0"
---

# JavaScript/TypeScript performance, readability, and trust

Apply these practices so generated code is **correct**, **performant**, and **readable** with minimal inspection.

## Goals

- **Correctness**: Explicit types, no silent coercion, clear edge handling.
- **Performance**: Prefer Map/Set for lookups, avoid redundant work, use appropriate data structures and async patterns.
- **Readability**: Small named helpers, modular structure, predictable control flow.
- **Trust**: Code that type-checks and follows consistent patterns is easier to verify at a glance.

---

## 1. Model the problem first

Before writing code, understand what you're solving and what can go wrong.

### Clarify inputs and outputs

- **What is the input?** File, API response, user input, command-line args? What's the shape and size?
- **What is the expected output?** A transformed value, a file, a side effect? What's the contract?
- **What are the constraints?** Size limits, time constraints, memory concerns?

### Identify edge cases upfront

Think through edge cases *before* implementation—they're easier to handle when designed for, not patched in:

- **Empty input**: Empty string, empty array, null/undefined. What should happen?
- **Single element**: Does your logic assume at least 2 items? Handle the 1-item case.
- **Boundary values**: Zero, negative numbers, MAX_SAFE_INTEGER, very long strings.
- **Invalid/malformed input**: Missing fields, wrong types, unexpected formats.
- **Duplicates**: Does your logic handle or assume uniqueness?
- **Order sensitivity**: Does input order matter? What about sorted vs unsorted?

### Design tests before or alongside code

- Write test cases (or at least list them) for: happy path, edge cases, error cases.
- For scripts, define example inputs and expected outputs before implementing.
- If the problem is complex, start with the simplest case that exercises the core logic, get that working, then expand.

### When in doubt, ask

If requirements are ambiguous, clarify before implementing. Questions like:
- "What should happen if X is empty?"
- "Should this throw or return a default for invalid input?"
- "Is this expected to handle very large inputs?"

Getting alignment on edge cases early prevents rework.

---

## 2. Correctness and trust

### Use explicit types

- Prefer TypeScript with explicit types for inputs and outputs (e.g. `type Config = { name: string; timeout: number; retries: number }`).
- Use `as const` for tuple return types so callers get narrow types: `return [success, count] as const`.
- Define return types explicitly for public functions; let inference handle internal helpers.

### Avoid silent coercion

- Parse numbers explicitly: `line.split(" ").map(Number)` or `Number(ch)`; validate with `!isNaN(n)` or `Number.isNaN(n)` when needed.
- Use nullish coalescing for "default if missing": `map.get(key) ?? 0`, `arr.find(predicate) ?? fallback`.

### Handle edges explicitly

- Check "no value" with `next == null` (or `next === undefined`) and return early.
- When mutating shared state for a branch (e.g. backtracking search), **restore state** after the branch so other branches see clean state.

---

## 3. Performance

### Prefer Map and Set for lookups and deduplication

- Use `Set` for "visited" and "already seen" (e.g. BFS/DFS, loop detection).
- Use `Map` for frequency counts or keyed caches: `freq.set(key, (freq.get(key) ?? 0) + 1)`.

### Avoid redundant work

- Parse input once; reuse the parsed structure across multiple operations or stages.
- For recursive or repeated computations, memoize with a **deterministic cache key** (e.g. serialize relevant state to a string). Prefer a single cache Map keyed by string.

### Use appropriate algorithms and data structures

- BFS/DFS: explicit queue/stack and `Set` for visited.
- When the problem involves distances or costs, consider precomputing distances (e.g. BFS from key nodes) then doing targeted search instead of raw recursion over the full graph.
- Prefer `.reduce((acc, n) => acc + n, 0)` or a small `sum(arr)` helper for numeric aggregation instead of manual loops when it stays readable.

### Prefer single-pass or linear structures where possible

- Use `.find(predicate)` and `.findLast(predicate)` instead of scanning manually twice.
- Use `toSorted((a, b) => a - b)` (or `.slice().sort(...)`) when you need a sorted copy without mutating the original.
- Avoid chaining methods that each iterate the full array when a single pass would suffice (e.g. `.filter().map()` when `.flatMap()` or `.reduce()` could do both).

### Async patterns: parallelize independent work

- **`Promise.all`**: Use when you have independent async operations that can run concurrently. Fails fast—if any promise rejects, the whole result rejects.
  ```ts
  const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);
  ```
- **`Promise.allSettled`**: Use when you need results from all promises regardless of individual failures. Returns `{ status: 'fulfilled', value }` or `{ status: 'rejected', reason }` for each.
  ```ts
  const results = await Promise.allSettled(urls.map(fetch));
  const succeeded = results.filter(r => r.status === 'fulfilled').map(r => r.value);
  ```
- **`Promise.race`**: Use when you want the first promise to settle (e.g. timeout patterns).
- **Avoid sequential awaits for independent work**:
  ```ts
  // Bad: sequential, takes sum of times
  const a = await fetchA();
  const b = await fetchB();
  
  // Good: parallel, takes max of times
  const [a, b] = await Promise.all([fetchA(), fetchB()]);
  ```

### Avoid common performance traps

- **Regex in loops**: Compile regex once outside the loop (`const re = /pattern/g`), not inside.
- **Repeated JSON.parse/stringify**: Parse once, pass the object; don't serialize/deserialize repeatedly.
- **Unnecessary cloning**: Use spread or `structuredClone` only when mutation is a real concern; don't defensively clone everything.
- **String concatenation in tight loops**: Use array + `.join()` or template literals for building large strings.

---

## 4. Readability and structure

### Small named helpers

- Extract pure helpers: `sum`, `groupBy`, `keyBy`, `chunk`, `unique`, `clamp`, `debounce`.
- Keep helpers focused; name them by intent (e.g. `parseConfig`, `validateInput`, `formatOutput`) so the main flow reads like prose.

### Modular structure

- Separate concerns: parsing/input, processing/logic, output/formatting.
- Use a clear entry point (e.g. `main()`, `run()`, `process()`) that orchestrates the stages; keep it thin so the flow is obvious.
- Group related logic into functions or modules; avoid monolithic functions that do parsing, processing, and output all in one.

### Prefer const and explicit control flow

- Use `const` by default; use `let` only when reassignment is needed.
- Use early returns for edge cases; avoid deep nesting.
- In loops, use `continue` for "skip this item" and keep the main path obvious.

### Parsing and input handling

- Prefer declarative parsing: `input.split("\n").map(line => line.split(" ").map(Number))` when the format is simple.
- For complex parsing, use a small function or iterator so the main logic stays clear.
- Validate input shape early; fail fast with clear error messages rather than silently producing garbage.

---

## 5. Consistency and style

- **One way to do things**: Use either `.reduce()` or a `for` loop for summing, but don't mix styles randomly in the same file.
- **Naming**: Use consistent names across the codebase (e.g. always `visited` or always `seen`, not both). Name variables by what they represent, not by type (`users` not `userArray`).
- **Error handling**: Be consistent—either throw exceptions, return `Result` types, or return `null`/`undefined`, but pick one pattern per codebase or module.

---

## 6. Checklist before suggesting code

- [ ] **Problem modeled**: Inputs, outputs, and edge cases identified before implementation.
- [ ] **Edge cases covered**: Empty, single-element, boundary values, invalid input handled explicitly.
- [ ] **Tests considered**: Happy path + edge cases have test cases (or at least documented expectations).
- [ ] Types are explicit for any non-trivial data (inputs, outputs, intermediate structures).
- [ ] No silent coercion; numbers parsed explicitly and validated when needed.
- [ ] Map/Set used for lookups and deduplication; no unnecessary array scans.
- [ ] Independent async operations use `Promise.all` or `Promise.allSettled`, not sequential awaits.
- [ ] If mutating shared state in a branch, state is restored after the branch.
- [ ] Helpers are small and named by intent; main flow is easy to follow.
- [ ] Common perf traps avoided (regex in loops, repeated parsing, unnecessary cloning).

Following these practices keeps JS/TS code correct, fast, and easy to trust with minimal inspection.
