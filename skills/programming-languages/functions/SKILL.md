---
name: functions
description: Advanced function patterns including declaration styles, closures, scope chains, hoisting, and this binding. Master function composition and advanced techniques.
sasmp_version: "1.3.0"
bonded_agent: 02-functions-scope
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [pattern_type]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_common_patterns

observability:
  entry_log: "Functions skill activated"
  exit_log: "Function reference provided"
---

# Functions & Scope Skill

## Quick Reference Card

### Function Styles
```javascript
// Declaration (hoisted)
function greet(name) { return `Hello, ${name}!`; }

// Expression (not hoisted)
const greet = function(name) { return `Hello, ${name}!`; };

// Arrow (lexical this)
const greet = (name) => `Hello, ${name}!`;
const greet = name => `Hello, ${name}!`;  // Single param
const getUser = async (id) => await fetch(`/api/${id}`);
```

### Scope Rules
```
Global Scope
  └── Function Scope
        └── Block Scope (let/const)
```

```javascript
const global = 'accessible everywhere';

function outer() {
  const outerVar = 'accessible in outer + inner';

  function inner() {
    const innerVar = 'only accessible here';
    console.log(global, outerVar, innerVar); // All work
  }
}
```

### Closure Pattern
```javascript
function createCounter() {
  let count = 0;  // Private state

  return {
    increment: () => ++count,
    decrement: () => --count,
    get: () => count
  };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
```

### This Binding Rules
| Context | `this` Value |
|---------|--------------|
| Global | `window`/`global` |
| Object method | The object |
| Arrow function | Lexical (outer) |
| `call/apply/bind` | Explicit value |
| Constructor (`new`) | New instance |

```javascript
// Explicit binding
fn.call(thisArg, arg1, arg2);
fn.apply(thisArg, [args]);
const bound = fn.bind(thisArg);
```

### Advanced Patterns
```javascript
// IIFE (Immediately Invoked)
const module = (function() {
  const private = 'hidden';
  return { getPrivate: () => private };
})();

// Currying
const multiply = a => b => a * b;
const double = multiply(2);
double(5); // 10

// Memoization
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) cache.set(key, fn(...args));
    return cache.get(key);
  };
}
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Lost `this` | `undefined` or wrong value | Use arrow fn or `.bind()` |
| Closure loop bug | All callbacks same value | Use `let` not `var` |
| Hoisting confusion | Undefined before declaration | Declare at top |
| TDZ error | ReferenceError | Move `let`/`const` before use |

### The Classic Loop Bug
```javascript
// BUG: var is function-scoped
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3

// FIX: Use let (block-scoped)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2
```

### Debug Checklist
```javascript
// 1. Check this context
console.log('this is:', this);

// 2. Verify closure captures
function test() {
  let x = 1;
  return () => { console.log('x:', x); };
}

// 3. Check hoisting
console.log(typeof myFunc); // 'function' or 'undefined'?
```

## Production Patterns

### Factory Pattern
```javascript
function createLogger(prefix) {
  return {
    log: (msg) => console.log(`[${prefix}] ${msg}`),
    error: (msg) => console.error(`[${prefix}] ${msg}`)
  };
}

const apiLogger = createLogger('API');
apiLogger.log('Request received');
```

### Debounce/Throttle
```javascript
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

## Related

- **Agent 02**: Functions & Scope (detailed learning)
- **Skill: fundamentals**: Variables and basics
- **Skill: asynchronous**: Async functions
