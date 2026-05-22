---
name: coding-javascript
cluster: coding
description: "JavaScript ES2024+: DOM, fetch, promises, generators, WeakRef, Proxy, modern patterns"
tags: ["javascript","js","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "javascript js es6 modern browser frontend async promises"
---

# coding-javascript

## Purpose
This skill equips OpenClaw to assist with JavaScript coding tasks using ES2024 features, focusing on modern browser-based development like DOM manipulation, asynchronous operations, and advanced patterns.

## When to Use
Use this skill when users need help with frontend JavaScript, such as building interactive web apps, handling API requests, or implementing efficient memory management with WeakRef. Apply it for tasks involving promises, generators, or Proxies in ES6+ environments, especially in browser contexts.

## Key Capabilities
- Manipulate DOM elements using querySelector and event listeners.
- Handle asynchronous code with fetch API, promises, and async/await.
- Use generators for iterative processes, e.g., yielding values in loops.
- Manage memory with WeakRef for garbage collection-friendly references.
- Implement Proxies for custom object behavior, like trapping property access.
- Apply modern patterns such as modules, arrow functions, and destructuring.

## Usage Patterns
To invoke this skill, prefix user queries with "use coding-javascript" in OpenClaw commands, e.g., "openclaw use coding-javascript and write a fetch function". For code generation, provide specific inputs like variable names or API endpoints. Always specify ES2024 features if needed, e.g., "generate code using WeakRef". Integrate by chaining skills, like "use coding-javascript then coding-web for full-stack advice". Test outputs in a browser console before deployment.

## Common Commands/API
Use OpenClaw CLI to activate: `openclaw run coding-javascript --query="explain promises"`. For JavaScript specifics:
- Fetch API: Use `fetch('https://api.example.com/data', { method: 'GET' })` to make requests; handle responses with `.then(response => response.json())`.
- Promises: Chain with `.then()` and `.catch()`, e.g., `new Promise(resolve => resolve('data')).then(data => console.log(data))`.
- Generators: Define with `function* gen() { yield 1; yield 2; }` and iterate using `for (let value of gen()) { console.log(value); }`.
- WeakRef: Create with `new WeakRef(object)` and dereference via `.deref()` for potential null if garbage collected.
- Proxy: Set up with `new Proxy(target, { get: (target, prop) => console.log(prop) })` to intercept access.
Config format: Use JSON for skill inputs, e.g., `{ "feature": "promises", "example": true }` in OpenClaw configs. If external APIs are involved, set auth via env vars like `$JAVASCRIPT_API_KEY` in your script.

## Integration Notes
Integrate this skill with OpenClaw by including it in multi-skill workflows, e.g., "openclaw chain coding-javascript and coding-css". For browser environments, ensure code runs in a modern engine like Chrome or Node.js v14+. Use env vars for secrets, e.g., export `$FETCH_API_KEY` and reference in code as `process.env.FETCH_API_KEY`. Avoid conflicts by specifying versions, like "use ES2024 only". For testing, wrap code in modules: `import { fetch } from 'whatwg-fetch';`.

## Error Handling
Always wrap asynchronous code in try-catch blocks, e.g.:
```javascript
try {
  await fetch('url').then(res => res.json());
} catch (error) {
  console.error('Fetch failed:', error.message);
}
```
For promises, use `.catch()`: `promise.then(data => process(data)).catch(err => logError(err))`. With generators, handle iteration errors via try-catch in the loop. For Proxies, trap errors in handlers, e.g., `new Proxy({}, { get: (target, prop) => { if (!target[prop]) throw new Error('Property not found'); } })`. Check for WeakRef validity: `if (weakRef.deref() !== undefined) { useObject(); }`. In OpenClaw, log errors with `openclaw log --skill=coding-javascript --error=details`.

## Concrete Usage Examples
1. To fetch and display user data: Use `openclaw use coding-javascript and generate: const userId = 1; fetch(`https://api.example.com/users/${userId}`).then(res => res.json()).then(data => console.log(data.name));`.
2. For Proxy-based validation: Invoke with `openclaw use coding-javascript and code: const handler = { set: (obj, prop, value) => { if (prop === 'age' && value < 18) throw Error('Underage'); obj[prop] = value; } }; const proxy = new Proxy({}, handler); proxy.age = 16; // Throws error`.

## Graph Relationships
- Related to: coding-python (for cross-language comparisons), coding-web (for frontend integration).
- Depends on: general-coding (for base syntax), async-patterns (for promise handling).
- Conflicts with: legacy-javascript (due to ES5 focus).
