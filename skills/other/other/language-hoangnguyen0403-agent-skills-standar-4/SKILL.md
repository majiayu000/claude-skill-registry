---
name: JavaScript Language Patterns
description: Modern JavaScript (ES2022+) patterns for clean, maintainable code.
metadata:
  labels: [javascript, language, es6, modern-js]
  triggers:
    files: ['**/*.js', '**/*.mjs', '**/*.cjs']
    keywords:
      [const, let, arrow, async, await, promise, destructuring, spread, class]
---

# JavaScript Language Patterns

## **Priority: P0 (CRITICAL)**

## Implementation Guidelines

- **Variables**: `const` default. `let` if needed. No `var`.
- **Functions**: Arrows for callbacks. Declarations for top-level.
- **Async**: `async/await` + `try/catch`.
- **Objects**: Destructuring, Spread `...`, Optional Chain `?.`, Nullish `??`.
- **Strings**: Template literals `${}`.
- **Arrays**: `map`, `filter`, `reduce`. No loops.
- **Modules**: ESM `import`/`export`. Export only what is necessary.
- **Classes**: Use `#private` fields for true privacy.

## Anti-Patterns

- **No `var`**: Block scope only.
- **No `==`**: Strict `===`.
- **No `new Object()`**: Use literals `{}`.
- **No Callbacks**: Promisify everything.
- **No Mutation**: Immutability first.

## Code

```javascript
// Modern Syntax
const [x, ...rest] = items;
const name = user?.profile?.name ?? 'Guest';

// Async + Error Handling
async function getUser(id) {
  const res = await fetch(`/api/${id}`);
  return res.json(); // Errors propagate
}

// Private Fields
class Service {
  #key;
  constructor(k) {
    this.#key = k;
  }
}
```

## Reference & Examples

For advanced patterns and functional programming:
See [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

best-practices | tooling
