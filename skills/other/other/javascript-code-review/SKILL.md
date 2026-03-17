---
name: javascript-code-review
description: Master JavaScript code review patterns including modern syntax, async/await, equality operators, memory leaks, and DOM manipulation. Use PROACTIVELY when reviewing JavaScript PRs.
---

# JavaScript Code Review

Comprehensive code review checklist and patterns for JavaScript applications, focusing on modern syntax, async patterns, and common pitfalls.

## When to Use This Skill

- Reviewing JavaScript pull requests
- Establishing JavaScript code review standards
- Training reviewers on JavaScript-specific issues
- Catching common JS bugs and anti-patterns
- Ensuring modern JavaScript best practices

## Quick Checklist

```markdown
## JavaScript Review Checklist

- [ ] Strict equality (===) used, not loose (==)
- [ ] No var, use const/let appropriately
- [ ] Promises properly chained with error handling
- [ ] No callbacks in modern code (use async/await)
- [ ] Array methods used correctly (map/filter/reduce)
- [ ] No prototype pollution risks
- [ ] Event listeners cleaned up
- [ ] Memory leaks checked (closures, listeners)
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Modern Syntax

### var vs let/const

```javascript
// ❌ Using var - hoisting issues, function scoped
var user = "John";
if (true) {
  var user = "Jane"; // Overwrites outer variable!
}
console.log(user); // 'Jane'

// ✅ Use const by default, let when reassignment needed
const user = "John";
if (true) {
  const user = "Jane"; // Block scoped, separate variable
}
console.log(user); // 'John'
```

### const vs let

```javascript
// ❌ Using let when const would work
let config = { timeout: 5000 };
let users = [];
users.push({ name: "John" }); // Mutating, not reassigning

// ✅ Use const for references that don't change
const config = { timeout: 5000 };
const users = [];
users.push({ name: "John" }); // OK - mutating content, not reference
```

### Template Literals

```javascript
// ❌ String concatenation
const greeting = "Hello, " + name + "! You have " + count + " messages.";
const multiline = "Line 1\n" + "Line 2\n" + "Line 3";

// ✅ Template literals
const greeting = `Hello, ${name}! You have ${count} messages.`;
const multiline = `
Line 1
Line 2
Line 3
`;
```

### Arrow Functions

```javascript
// ❌ Anonymous callbacks
users
  .filter(function (user) {
    return user.active;
  })
  .map(function (user) {
    return user.name;
  });

// ✅ Arrow functions
users.filter((user) => user.active).map((user) => user.name);
```

### Destructuring

```javascript
// ❌ Repetitive property access
function processUser(user) {
  console.log(user.name);
  console.log(user.email);
  console.log(user.role);
}

// ✅ Destructuring
function processUser({ name, email, role }) {
  console.log(name);
  console.log(email);
  console.log(role);
}

// ✅ With defaults
function processUser({ name, email, role = "user" }) {
  // role defaults to 'user' if not provided
}
```

### Spread Operator

```javascript
// ❌ Object.assign for shallow copy
const newConfig = Object.assign({}, config, { timeout: 10000 });
const allItems = array1.concat(array2);

// ✅ Spread operator
const newConfig = { ...config, timeout: 10000 };
const allItems = [...array1, ...array2];
```

---

## Equality and Type Coercion

### Strict vs Loose Equality

```javascript
// ❌ Loose equality - type coercion bugs
if (value == null) {
} // true for null AND undefined
if (value == 0) {
} // true for 0, '', false, []
if (value == false) {
} // true for 0, '', null, undefined
if ("5" == 5) {
} // true - string coerced!

// ✅ Strict equality
if (value === null || value === undefined) {
}
if (value === 0) {
}
if (value === false) {
}
if ("5" === 5) {
} // false - different types

// ✅ Exception: null/undefined check (intentional)
if (value == null) {
} // OK for specifically null/undefined check
```

### Falsy vs Nullish

```javascript
// ❌ Falsy check when you want null check
function process(value) {
  if (!value) {
    // Fails for 0, '', false
    return "default";
  }
  return value;
}

process(0); // Returns 'default' - probably wrong!
process(""); // Returns 'default' - probably wrong!
process(false); // Returns 'default' - probably wrong!

// ✅ Nullish coalescing for null/undefined only
function process(value) {
  return value ?? "default"; // Only null/undefined trigger default
}

process(0); // Returns 0
process(""); // Returns ''
process(false); // Returns false
process(null); // Returns 'default'
```

### Truthy Checks with Default Values

```javascript
// ❌ Logical OR treats 0, '', false as falsy
const count = options.count || 10; // 0 becomes 10!
const name = options.name || "Guest"; // '' becomes 'Guest'!

// ✅ Nullish coalescing
const count = options.count ?? 10; // 0 stays 0
const name = options.name ?? "Guest"; // '' stays ''
```

---

## Async Patterns

### Callback Hell

```javascript
// ❌ Callback hell (pyramid of doom)
getUser(id, function (user) {
  getPosts(user.id, function (posts) {
    getComments(posts[0].id, function (comments) {
      getAuthor(comments[0].authorId, function (author) {
        // deeply nested, hard to maintain
      });
    });
  });
});

// ✅ Async/await
async function getPostData(id) {
  const user = await getUser(id);
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  const author = await getAuthor(comments[0].authorId);
  return { user, posts, comments, author };
}
```

### Unhandled Promise Rejections

```javascript
// ❌ Unhandled promise rejection
async function fetchData() {
  const response = await fetch("/api/data");
  return response.json();
}
fetchData(); // Rejection silently ignored!

// ✅ Always handle errors
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw error; // Re-throw or handle appropriately
  }
}

fetchData().catch((error) => handleError(error));
```

### Sequential vs Parallel

```javascript
// ❌ Sequential when parallel is possible
const user = await getUser(id);
const posts = await getPosts(id);
const settings = await getSettings(id);
// Each waits for the previous - slow!

// ✅ Parallel execution
const [user, posts, settings] = await Promise.all([
  getUser(id),
  getPosts(id),
  getSettings(id),
]);
// All run simultaneously - fast!
```

### Promise.allSettled for Partial Failures

```javascript
// ❌ One failure cancels everything
try {
  const results = await Promise.all([
    fetchUser(1),
    fetchUser(2), // If this fails...
    fetchUser(3),
  ]);
} catch (error) {
  // All results lost!
}

// ✅ Handle partial failures
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3),
]);

results.forEach((result, index) => {
  if (result.status === "fulfilled") {
    console.log(`User ${index + 1}:`, result.value);
  } else {
    console.log(`User ${index + 1} failed:`, result.reason);
  }
});
```

---

## Memory Leaks

### Event Listeners Not Cleaned Up

```javascript
// ❌ Event listener not cleaned up - memory leak
class Widget {
  constructor() {
    window.addEventListener("resize", this.handleResize);
  }

  handleResize() {
    console.log("Resized");
  }
  // Widget removed but listener stays!
}

// ✅ Clean up listeners
class Widget {
  constructor() {
    this.handleResize = this.handleResize.bind(this);
    window.addEventListener("resize", this.handleResize);
  }

  handleResize() {
    console.log("Resized");
  }

  destroy() {
    window.removeEventListener("resize", this.handleResize);
  }
}
```

### Closures Holding References

```javascript
// ❌ Closure holding large data
function createHandler(largeData) {
  return function onClick() {
    console.log("Clicked");
    // largeData is captured in closure but never used!
    // Memory never released while handler exists
  };
}

// ✅ Don't capture unnecessary data
function createHandler() {
  return function onClick() {
    console.log("Clicked");
  };
}

// If data is needed, only capture what's necessary
function createHandler(userName) {
  // Just the name, not whole object
  return function onClick() {
    console.log(`${userName} clicked`);
  };
}
```

### Timers Not Cleared

```javascript
// ❌ Timer continues after component removed
function startPolling() {
  setInterval(() => {
    fetchData(); // Keeps running forever!
  }, 5000);
}

// ✅ Clear timer on cleanup
function startPolling() {
  const intervalId = setInterval(() => {
    fetchData();
  }, 5000);

  return () => clearInterval(intervalId);
}

// Usage
const stopPolling = startPolling();
// Later...
stopPolling();
```

### Subscriptions Not Unsubscribed

```javascript
// ❌ Observable not unsubscribed
class Component {
  init() {
    eventEmitter.on("update", this.handleUpdate);
    // Never unsubscribed - memory leak!
  }
}

// ✅ Unsubscribe on cleanup
class Component {
  init() {
    this.handleUpdate = this.handleUpdate.bind(this);
    eventEmitter.on("update", this.handleUpdate);
  }

  destroy() {
    eventEmitter.off("update", this.handleUpdate);
  }
}
```

---

## Array Methods

### Incorrect Method Usage

```javascript
// ❌ forEach for transformation (should use map)
const names = [];
users.forEach((user) => {
  names.push(user.name);
});

// ✅ map for transformation
const names = users.map((user) => user.name);

// ❌ filter + length for counting
const count = items.filter((item) => item.active).length;

// ✅ reduce for counting (no intermediate array)
const count = items.reduce((acc, item) => (item.active ? acc + 1 : acc), 0);

// Or just filter if readability matters more than perf
const count = items.filter((item) => item.active).length;
```

### Mutating Original Array

```javascript
// ❌ sort mutates original array!
const sorted = users.sort((a, b) => a.age - b.age);
// users array is now sorted too!

// ✅ Copy before sorting
const sorted = [...users].sort((a, b) => a.age - b.age);
// Or
const sorted = users.toSorted((a, b) => a.age - b.age); // ES2023+

// Same issue with reverse()
const reversed = [...items].reverse();
// Or
const reversed = items.toReversed(); // ES2023+
```

---

## Object Patterns

### Prototype Pollution

```javascript
// ❌ Dangerous - prototype pollution possible
function merge(target, source) {
  for (const key in source) {
    target[key] = source[key];
  }
  return target;
}
// Attacker could set __proto__!

// ✅ Check for dangerous keys
function merge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === "__proto__" || key === "constructor" || key === "prototype") {
      continue;
    }
    target[key] = source[key];
  }
  return target;
}

// ✅ Or use Object.assign / spread
const merged = { ...target, ...source };
```

### for...in vs for...of

```javascript
// ❌ for...in on arrays - iterates indices as strings, includes prototype
for (const item in array) {
  console.log(item); // '0', '1', '2' (strings!)
}

// ✅ for...of for arrays - iterates values
for (const item of array) {
  console.log(item); // actual values
}

// ✅ for...in for objects - iterates keys
for (const key in object) {
  if (Object.hasOwn(object, key)) {
    // Skip inherited
    console.log(key, object[key]);
  }
}

// ✅ Better: Object.entries
for (const [key, value] of Object.entries(object)) {
  console.log(key, value);
}
```

---

## Common Pitfalls

| Pitfall              | Problem                      | Solution                       |
| -------------------- | ---------------------------- | ------------------------------ |
| `var` usage          | Hoisting, function scope     | Use `const`/`let`              |
| `==` equality        | Type coercion bugs           | Use `===`                      |
| Falsy defaults       | 0, '', false treated as null | Use `??`                       |
| Uncaught promises    | Silent failures              | Always catch errors            |
| No cleanup           | Memory leaks                 | Remove listeners, clear timers |
| `sort()` mutation    | Changes original array       | Copy first with `[...arr]`     |
| `for...in` on arrays | Wrong iteration              | Use `for...of`                 |

## Best Practices Summary

1. **Use const by default** - `let` only when reassignment needed
2. **Strict equality** - `===` and `!==` always
3. **Nullish coalescing** - `??` for defaults, not `||`
4. **async/await** - Over callbacks and `.then()` chains
5. **Always handle errors** - No uncaught promise rejections
6. **Clean up resources** - Event listeners, timers, subscriptions
7. **Don't mutate** - Copy before `sort()`, `reverse()`, etc.
8. **Use modern methods** - `Object.entries`, `Array.from`, etc.


## Parent Hub
- [_frontend-mastery](../_frontend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
