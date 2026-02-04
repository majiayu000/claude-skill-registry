---
name: modern-javascript
description: |
  Modern JavaScript (ES6-ES2025) patterns and best practices. Triggers on: JavaScript, ES6, ES2020,
  ES2022, ES2024, modern JS, refactor legacy, array methods, async/await, optional chaining, nullish
  coalescing, destructuring, spread, rest, template literals, arrow functions, toSorted, toReversed,
  at, groupBy, Promise, functional programming.

  Use when: writing new JavaScript code, refactoring legacy code, modernizing codebases, implementing
  functional patterns, or reviewing JS for performance and readability. Proactively apply when creating
  web applications, Node.js services, or any JavaScript project.
---

# Modern JavaScript (ES6-ES2025)

Write clean, performant, maintainable JavaScript using modern language features. This skill covers ES6 through ES2025, emphasizing immutability, functional patterns, and expressive syntax.

## Quick Decision Trees

### "Which array method should I use?"

```
What do I need?
├─ Transform each element           → .map()
├─ Keep some elements               → .filter()
├─ Find one element                 → .find() / .findLast()
├─ Check if condition met           → .some() / .every()
├─ Reduce to single value           → .reduce()
├─ Get last element                 → .at(-1)
├─ Sort without mutating            → .toSorted()
├─ Reverse without mutating         → .toReversed()
├─ Group by property                → Object.groupBy()
└─ Flatten nested arrays            → .flat() / .flatMap()
```

### "How do I handle nullish values?"

```
Nullish handling?
├─ Safe property access              → obj?.prop / obj?.[key]
├─ Safe method call                  → obj?.method?.()
├─ Default for null/undefined only   → value ?? 'default'
├─ Default for any falsy             → value || 'default'
├─ Assign if null/undefined          → obj.prop ??= 'default'
└─ Check property exists             → Object.hasOwn(obj, 'key')
```

### "Should I mutate or copy?"

```
Always prefer non-mutating methods:
├─ Sort array      → .toSorted()    (not .sort())
├─ Reverse array   → .toReversed()  (not .reverse())
├─ Splice array    → .toSpliced()   (not .splice())
├─ Update element  → .with(i, val)  (not arr[i] = val)
├─ Add to array    → [...arr, item] (not .push())
└─ Merge objects   → {...obj, key}  (not Object.assign())
```

## ES Version Quick Reference

| Version | Year | Key Features |
|---------|------|--------------|
| ES6 | 2015 | let/const, arrow functions, classes, destructuring, spread, Promises, modules, Symbol, Map/Set, Proxy, generators |
| ES2016 | 2016 | Array.includes(), exponentiation operator ** |
| ES2017 | 2017 | async/await, Object.values/entries, padStart/padEnd, trailing commas, SharedArrayBuffer, Atomics |
| ES2018 | 2018 | Rest/spread for objects, for await...of, Promise.finally(), RegExp named groups, lookbehind, dotAll flag |
| ES2019 | 2019 | .flat(), .flatMap(), Object.fromEntries(), trimStart/End(), optional catch binding, stable Array.sort() |
| ES2020 | 2020 | Optional chaining ?., nullish coalescing ??, BigInt, Promise.allSettled(), globalThis, dynamic import() |
| ES2021 | 2021 | String.replaceAll(), Promise.any(), logical assignment ??= and or=, numeric separators 1_000_000 |
| ES2022 | 2022 | .at(), Object.hasOwn(), top-level await, private class fields #field, static blocks, Error.cause |
| ES2023 | 2023 | .toSorted(), .toReversed(), .toSpliced(), .with(), .findLast(), .findLastIndex(), hashbang grammar |
| ES2024 | 2024 | Object.groupBy(), Map.groupBy(), Promise.withResolvers(), RegExp v flag, resizable ArrayBuffer |
| ES2025 | 2025 | Iterator helpers (.map, .filter, .take), Set methods (.union, .intersection), RegExp.escape(), using/await using |

## Modernization Patterns

### Array Access

```javascript
// ❌ Legacy
const last = arr[arr.length - 1];
const secondLast = arr[arr.length - 2];

// ✅ Modern (ES2022)
const last = arr.at(-1);
const secondLast = arr.at(-2);
```

### Non-Mutating Array Operations

```javascript
// ❌ Mutates original array
const sorted = arr.sort((a, b) => a - b);
const reversed = arr.reverse();

// ✅ Returns new array (ES2023)
const sorted = arr.toSorted((a, b) => a - b);
const reversed = arr.toReversed();
const updated = arr.with(2, 'new value');
const removed = arr.toSpliced(1, 1);
```

### String Replacement

```javascript
// ❌ Legacy with regex
const result = str.replace(/foo/g, 'bar');

// ✅ Modern (ES2021)
const result = str.replaceAll('foo', 'bar');
```

### Grouping Data

```javascript
// ❌ Manual grouping
const grouped = items.reduce((acc, item) => {
  const key = item.category;
  acc[key] = acc[key] || [];
  acc[key].push(item);
  return acc;
}, {});

// ✅ Modern (ES2024)
const grouped = Object.groupBy(items, item => item.category);
```

### Nullish Handling

```javascript
// ❌ Falsy check (0, '', false are valid values)
const value = input || 'default';
const name = user && user.profile && user.profile.name;

// ✅ Nullish check (only null/undefined)
const value = input ?? 'default';
const name = user?.profile?.name;
```

### Property Existence

```javascript
// ❌ Can be fooled by prototype or overwritten hasOwnProperty
if (obj.hasOwnProperty('key')) { }

// ✅ Modern (ES2022)
if (Object.hasOwn(obj, 'key')) { }
```

### Logical Assignment

```javascript
// ❌ Verbose assignment
if (obj.prop === null || obj.prop === undefined) {
  obj.prop = 'default';
}

// ✅ Modern (ES2021)
obj.prop ??= 'default';  // Assign if null/undefined
obj.count ||= 0;         // Assign if falsy
obj.enabled &&= check(); // Assign if truthy
```

## Async Patterns

### Promise Combinators

```javascript
// Wait for all, fail if any fails
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);

// Wait for all, get status of each
const results = await Promise.allSettled([fetchA(), fetchB()]);
results.forEach(r => {
  if (r.status === 'fulfilled') console.log(r.value);
  else console.error(r.reason);
});

// First to succeed
const fastest = await Promise.any([fetchFromCDN1(), fetchFromCDN2()]);

// First to settle
const winner = await Promise.race([fetchData(), timeout(5000)]);
```

### Promise.withResolvers (ES2024)

```javascript
// ❌ Legacy pattern
let resolve, reject;
const promise = new Promise((res, rej) => {
  resolve = res;
  reject = rej;
});

// ✅ Modern (ES2024)
const { promise, resolve, reject } = Promise.withResolvers();
```

### Top-Level Await (ES2022)

```javascript
// In ES modules, await at top level
const config = await fetch('/config.json').then(r => r.json());
const db = await connectDatabase(config);

export { db };
```

## Functional Patterns

### Immutable Object Updates

```javascript
// Add/update property
const updated = { ...user, age: 31 };

// Remove property
const { password, ...userWithoutPassword } = user;

// Nested update
const updated = {
  ...state,
  user: { ...state.user, name: 'New Name' }
};
```

### Array Transformations

```javascript
// Chain transformations (ES2023)
const result = users
  .filter(u => u.active)
  .map(u => u.name)
  .toSorted();

// Using flatMap for filter+map (single pass)
const activeNames = users.flatMap(u => u.active ? [u.name] : []);

// ES2024: Group then process
const byStatus = Object.groupBy(users, u => u.active ? 'active' : 'inactive');
const activeNames = byStatus.active?.map(u => u.name) ?? [];
```

### Composition

```javascript
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

const processUser = pipe(
  user => ({ ...user, name: user.name.trim() }),
  user => ({ ...user, email: user.email.toLowerCase() }),
  user => ({ ...user, createdAt: new Date() })
);
```

## Destructuring Patterns

### Object Destructuring

```javascript
// Basic with rename and default
const { name: userName, age = 18 } = user;

// Nested
const { address: { city, country } } = user;

// Rest
const { id, ...userData } = user;
```

### Array Destructuring

```javascript
// Skip elements
const [first, , third] = array;

// Rest
const [head, ...tail] = array;

// Swap variables
[a, b] = [b, a];

// Function returns
const [x, y] = getCoordinates();
```

## Anti-Patterns

| Anti-Pattern | Problem | Modern Solution |
|--------------|---------|-----------------|
| `arr[arr.length-1]` | Verbose, error-prone | `arr.at(-1)` |
| `.sort()` on original | Mutates array | `.toSorted()` |
| `.replace(/g/)` for all | Regex overhead | `.replaceAll()` |
| `obj.hasOwnProperty()` | Can be overwritten | `Object.hasOwn()` |
| `value \|\| default` | 0, '', false treated as falsy | `value ?? default` |
| `obj && obj.prop && obj.prop.method()` | Verbose null checks | `obj?.prop?.method?.()` |
| `for (let i = 0; ...)` | Index bugs, verbose | `.map()`, `.filter()`, `for...of` |
| `new Promise((res, rej) => ...)` | Boilerplate | `Promise.withResolvers()` |
| Manual array grouping | Verbose, error-prone | `Object.groupBy()` |

## Best Practices

1. **Use `const` by default** — Only use `let` when reassignment is needed
2. **Prefer arrow functions** — Especially for callbacks and short functions
3. **Use template literals** — Instead of string concatenation
4. **Destructure early** — Extract what you need at function start
5. **Avoid mutations** — Use `.toSorted()`, `.toReversed()`, spread operator
6. **Use optional chaining** — Prevent "Cannot read property of undefined"
7. **Use nullish coalescing** — `??` for defaults, not `||` (unless intentional)
8. **Prefer array methods** — `.map()`, `.filter()`, `.find()` over loops
9. **Use `async/await`** — Instead of `.then()` chains
10. **Handle errors properly** — `try/catch` with async/await

## Reference Documentation

### ES Version References
| File | Purpose |
|------|---------|
| [references/ES2016-ES2017.md](references/ES2016-ES2017.md) | includes, async/await, Object.values/entries, string padding |
| [references/ES2018-ES2019.md](references/ES2018-ES2019.md) | rest/spread objects, flat/flatMap, RegExp named groups |
| [references/ES2022-ES2023.md](references/ES2022-ES2023.md) | .at(), .toSorted(), .toReversed(), .findLast(), class features |
| [references/ES2024.md](references/ES2024.md) | Object.groupBy, Promise.withResolvers, RegExp v flag |
| [references/ES2025.md](references/ES2025.md) | Set methods, iterator helpers, using/await using |
| [references/UPCOMING.md](references/UPCOMING.md) | Temporal API, Decorators, Decorator Metadata |

### Pattern References
| File | Purpose |
|------|---------|
| [references/PROMISES.md](references/PROMISES.md) | Promise fundamentals, async/await, combinators |
| [references/CONCURRENCY.md](references/CONCURRENCY.md) | Parallel, batched, pool patterns, retry, cancellation |
| [references/IMMUTABILITY.md](references/IMMUTABILITY.md) | Immutable data patterns, pure functions |
| [references/COMPOSITION.md](references/COMPOSITION.md) | Higher-order functions, memoization, monads |
| [references/CHEATSHEET.md](references/CHEATSHEET.md) | Quick syntax reference

## Resources

### Specifications
- **ECMAScript Specification**: https://tc39.es/ecma262/ (living standard)
- **TC39 Proposals**: https://github.com/tc39/proposals (upcoming features)
- **TC39 Process**: https://tc39.es/process-document/ (how features are added)

### Documentation
- **MDN Web Docs**: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **JavaScript.info**: https://javascript.info/

### Compatibility
- **Can I Use**: https://caniuse.com (browser support tables)
- **Node.js ES Compatibility**: https://node.green/
