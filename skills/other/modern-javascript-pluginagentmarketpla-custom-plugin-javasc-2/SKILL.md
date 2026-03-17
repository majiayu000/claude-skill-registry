---
name: modern-javascript
description: Modern ES6+ JavaScript features including classes, modules, destructuring, iterators, proxies, and latest ECMAScript features.
sasmp_version: "1.3.0"
bonded_agent: 06-modern-es6-advanced
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [es_version]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_es6_basics

observability:
  entry_log: "Modern JS skill activated"
  exit_log: "Modern JS reference provided"
---

# Modern JavaScript Skill

## Quick Reference Card

### Classes
```javascript
class Service {
  #privateField;           // Private (ES2022)
  static VERSION = '1.0';  // Static property

  constructor(config) {
    this.#privateField = config.secret;
  }

  async fetch(url) {
    return this.#request('GET', url);
  }

  #request(method, url) {  // Private method
    return fetch(url, { method });
  }

  get config() { return this.#privateField; }
}

class ExtendedService extends Service {
  constructor(config) {
    super(config);
  }
}
```

### Modules
```javascript
// Named exports
export const API_URL = '/api';
export function fetchData() { }

// Default export
export default class ApiClient { }

// Import
import ApiClient, { API_URL, fetchData } from './api.js';
import * as api from './api.js';

// Dynamic import
const { Editor } = await import('./editor.js');

// Re-export (barrel file)
export { ApiClient } from './api.js';
export { default as Utils } from './utils.js';
```

### Destructuring
```javascript
// Object
const { name, age = 0, address: { city } } = user;
const { id, ...rest } = data;

// Array
const [first, , third, ...others] = arr;
[a, b] = [b, a];  // Swap

// Function params
function create({ name, type = 'default' } = {}) { }
```

### Spread & Rest
```javascript
// Spread
const merged = { ...obj1, ...obj2 };
const combined = [...arr1, ...arr2];
Math.max(...numbers);

// Rest
function sum(...nums) { return nums.reduce((a,b) => a+b, 0); }
```

### Iterators & Generators
```javascript
// Custom iterable
class Range {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }

  *[Symbol.iterator]() {
    for (let i = this.start; i <= this.end; i++) yield i;
  }
}

[...new Range(1, 5)]; // [1, 2, 3, 4, 5]

// Async generator
async function* fetchPages(url) {
  let page = 1;
  while (true) {
    const data = await fetch(`${url}?page=${page++}`).then(r => r.json());
    if (!data.length) break;
    yield data;
  }
}
```

### Proxy
```javascript
// Validation proxy
const validated = new Proxy({}, {
  set(obj, prop, value) {
    if (prop === 'age' && value < 0) {
      throw new Error('Age must be positive');
    }
    return Reflect.set(obj, prop, value);
  }
});

// Observable proxy
function observable(target, onChange) {
  return new Proxy(target, {
    set(obj, prop, value) {
      const result = Reflect.set(obj, prop, value);
      onChange(prop, value);
      return result;
    }
  });
}
```

### Latest Features (ES2020-2024)
```javascript
// Optional chaining & nullish coalescing
const city = user?.address?.city ?? 'Unknown';

// Logical assignment
config.debug ??= false;
count ||= 1;

// Private fields
class Counter { #count = 0; }

// Top-level await
const config = await fetch('/config').then(r => r.json());

// Array.at()
arr.at(-1);  // Last element

// Object.groupBy (ES2024)
Object.groupBy(users, u => u.role);

// Promise.withResolvers (ES2024)
const { promise, resolve, reject } = Promise.withResolvers();
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Module not found | Import error | Check path/extension |
| Private field access | TypeError | Use class method |
| Iterator exhausted | Empty results | Create new iterator |

### Debug Checklist
```javascript
// 1. Check exports
import * as mod from './module.js';
console.log(Object.keys(mod));

// 2. Verify class instance
console.log(obj instanceof MyClass);

// 3. Check symbols
console.log(Object.getOwnPropertySymbols(obj));
```

## Related

- **Agent 06**: Modern ES6+ (detailed learning)
- **Skill: functions**: Function patterns
- **Skill: ecosystem**: Build tools
