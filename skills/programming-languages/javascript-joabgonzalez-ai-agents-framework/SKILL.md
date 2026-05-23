---
name: javascript
description: "Modern JavaScript (ES2020+) patterns and best practices. ES modules, async/await, destructuring, optional chaining, nullish coalescing. Trigger: When writing modern JavaScript code, using ES2020+ features, or refactoring legacy JavaScript."
skills:
  - conventions
allowed-tools:
  - documentation-reader
  - web-search
---

# JavaScript Skill

## Overview

Modern JavaScript patterns and best practices for ES2020+ development.

## Objective

Guide developers in writing clean, efficient JavaScript using modern language features and patterns.

---

## When to Use

Use this skill when:

- Writing JavaScript code with ES2020+ features
- Refactoring legacy JavaScript to modern syntax
- Implementing async operations with promises/async-await
- Using destructuring, optional chaining, nullish coalescing

Don't use this skill for:

- TypeScript-specific patterns (use typescript skill)
- React patterns (use react skill)
- Node.js backend specifics (general JS only)

---

## Critical Patterns

### ✅ REQUIRED: Use const/let, Never var

```javascript
// ✅ CORRECT: const for immutable, let for mutable
const API_URL = "https://api.example.com";
let count = 0;

// ❌ WRONG: var (function-scoped, causes issues)
var count = 0;
```

### ✅ REQUIRED: Use async/await for Async Operations

```javascript
// ✅ CORRECT: async/await
async function fetchData() {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.error(error);
  }
}

// ❌ WRONG: Promise chains (less readable)
function fetchData() {
  return fetch(url)
    .then((res) => res.json())
    .catch((error) => console.error(error));
}
```

### ✅ REQUIRED: Optional Chaining and Nullish Coalescing

```javascript
// ✅ CORRECT: Safe property access with optional chaining (?.)
const name = user?.profile?.name ?? "Anonymous";
const result = obj?.method?.(); // Safe method call

// ✅ CORRECT: Nullish coalescing (??) only for null/undefined
const port = config.port ?? 3000; // 0 is valid, won't fallback

// ❌ WRONG: OR operator (|| treats 0, '', false as falsy)
const port = config.port || 3000; // 0 would fallback to 3000!

// ❌ WRONG: Manual null checks
const name = (user && user.profile && user.profile.name) || "Anonymous";
```

### ✅ REQUIRED: Use Double Negation (!!) for Boolean Coercion

```javascript
// ✅ CORRECT: Explicit boolean conversion
const hasData = !!data; // true if data exists, false otherwise
const isValid = Boolean(value); // Alternative explicit conversion

// ❌ WRONG: Implicit coercion (unclear intent)
if (data) {
} // Unclear if checking existence or truthiness
```

### ✅ REQUIRED: Promise.all for Parallel Operations

```javascript
// ✅ CORRECT: Parallel execution with Promise.all
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);

// ❌ WRONG: Sequential awaits (3x slower!)
const users = await fetchUsers();
const posts = await fetchPosts();
const comments = await fetchComments();
```

### ✅ REQUIRED: Prefer async/await Over Promise Chains

```javascript
// ✅ CORRECT: async/await (readable, easier error handling)
async function processData() {
  try {
    const response = await fetch(url);
    const data = await response.json();
    const processed = await transform(data);
    return processed;
  } catch (error) {
    console.error("Processing failed:", error);
    throw error;
  }
}

// ❌ WRONG: Promise chains (harder to read and debug)
function processData() {
  return fetch(url)
    .then((res) => res.json())
    .then((data) => transform(data))
    .catch((error) => console.error(error));
}
```

---

## Conventions

Refer to conventions for:

- Code organization
- Naming patterns
- Documentation

### JavaScript Specific

- Use const/let instead of var
- Prefer arrow functions for callbacks
- Use template literals for string interpolation
- Leverage destructuring for objects and arrays
- Use async/await for asynchronous operations
- Apply optional chaining (?.) and nullish coalescing (??)
- **Use `!!` for explicit boolean conversion**
- **Prefer `Promise.all()` for parallel async operations**
- **Use `===` for strict equality, never `==`**
- **Prefer modern array methods** (`.map()`, `.filter()`, `.reduce()`) over loops

---

## Decision Tree

**Async operation?** → Use `async/await` with try/catch for error handling.

**String concatenation?** → Use template literals: `string ${variable}`.

**Default value needed?** → Use nullish coalescing `??` for null/undefined, `||` for any falsy value.

**Property might not exist?** → Use optional chaining: `obj?.prop?.nested`.

**Iterate array?** → Use `.map()`, `.filter()`, `.reduce()` over for loops. Use `for...of` for early breaks.

**Copy object/array?** → Use spread operator: `{...obj}`, `[...arr]`.

**Function as callback?** → Use arrow function unless you need `this` context.

---

## Example

```javascript
const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data?.results ?? [];
  } catch (error) {
    console.error("Fetch failed:", error);
    return [];
  }
};

const { name, age = 18 } = user;
const greeting = `Hello, ${name}!`;
```

---

## Edge Cases

**Parallel async operations:** Use `Promise.all()` for concurrent execution, not sequential awaits.

**Array holes:** Sparse arrays with holes behave differently in `.map()` vs `.forEach()`. Use `.filter(Boolean)` to remove.

**Number precision:** Floating point math may be imprecise. Use libraries like decimal.js for financial calculations.

**Equality:** Use `===` for strict equality. `==` coerces types and causes bugs.

**this binding:** Arrow functions don't bind `this`. Use regular functions for methods that need `this` context.

---

## References

- https://developer.mozilla.org/en-US/docs/Web/JavaScript
- https://tc39.es/ecma262/
