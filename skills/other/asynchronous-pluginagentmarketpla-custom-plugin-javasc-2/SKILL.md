---
name: asynchronous
description: Master asynchronous JavaScript patterns including callbacks, promises, async/await, event loop mechanics, and real-world async patterns.
sasmp_version: "1.3.0"
bonded_agent: 04-asynchronous-javascript
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
  fallback: show_async_await_first

observability:
  entry_log: "Async skill activated"
  exit_log: "Async reference provided"
---

# Asynchronous JavaScript Skill

## Quick Reference Card

### Event Loop Order
```
1. Call Stack (sync code)
2. Microtasks (Promise.then, queueMicrotask)
3. Macrotasks (setTimeout, setInterval, I/O)
```

```javascript
console.log('1');                    // Sync
setTimeout(() => console.log('2'), 0);  // Macro
Promise.resolve().then(() => console.log('3')); // Micro
console.log('4');                    // Sync
// Output: 1, 4, 3, 2
```

### Promise Basics
```javascript
// Create
const promise = new Promise((resolve, reject) => {
  if (success) resolve(value);
  else reject(new Error('Failed'));
});

// Chain
fetch('/api/data')
  .then(res => res.json())
  .then(data => process(data))
  .catch(err => handleError(err))
  .finally(() => cleanup());
```

### Async/Await
```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}
```

### Promise Combinators
```javascript
// All must succeed
const [a, b, c] = await Promise.all([p1, p2, p3]);

// All results (even failures)
const results = await Promise.allSettled([p1, p2, p3]);
results.forEach(r => {
  if (r.status === 'fulfilled') console.log(r.value);
  else console.log(r.reason);
});

// First to settle
const fastest = await Promise.race([p1, p2, p3]);

// First to succeed
const firstSuccess = await Promise.any([p1, p2, p3]);
```

### Parallel vs Sequential
```javascript
// Sequential (slow)
const a = await fetch('/a');
const b = await fetch('/b');

// Parallel (fast)
const [a, b] = await Promise.all([
  fetch('/a'),
  fetch('/b')
]);
```

## Production Patterns

### Retry with Backoff
```javascript
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      if (i === retries - 1) throw err;
      await new Promise(r => setTimeout(r, 2 ** i * 1000));
    }
  }
}
```

### Timeout
```javascript
async function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), ms);

  try {
    const res = await fetch(url, { signal: controller.signal });
    return await res.json();
  } finally {
    clearTimeout(timeout);
  }
}
```

### Debounce
```javascript
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

### Rate Limiter
```javascript
class RateLimiter {
  constructor(limit, interval) {
    this.tokens = limit;
    setInterval(() => this.tokens = limit, interval);
  }

  async acquire() {
    while (this.tokens <= 0) {
      await new Promise(r => setTimeout(r, 100));
    }
    this.tokens--;
  }
}
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Unhandled rejection | Console warning | Add `.catch()` or try/catch |
| Sequential instead of parallel | Slow execution | Use `Promise.all()` |
| Missing `await` | Promise instead of value | Add `await` |
| Race condition | Inconsistent results | Use proper sequencing |

### Debug Checklist
```javascript
// 1. Add timing
console.time('fetch');
await fetchData();
console.timeEnd('fetch');

// 2. Log promise state
promise.then(console.log).catch(console.error);

// 3. Check for missing await
const result = fetchData();
console.log(result); // Promise? Add await!

// 4. Trace async chain
async function debug() {
  console.log('Step 1');
  const a = await step1();
  console.log('Step 2', a);
  const b = await step2(a);
  console.log('Done', b);
}
```

### Error Handling Pattern
```javascript
// Wrapper for tuple return
async function safeAsync(promise) {
  try {
    return [await promise, null];
  } catch (error) {
    return [null, error];
  }
}

const [data, error] = await safeAsync(fetchData());
if (error) handleError(error);
```

## Related

- **Agent 04**: Asynchronous JavaScript (detailed learning)
- **Skill: functions**: Callbacks and closures
- **Skill: ecosystem**: API integration
