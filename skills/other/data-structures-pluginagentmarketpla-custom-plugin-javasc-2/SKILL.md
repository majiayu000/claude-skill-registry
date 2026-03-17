---
name: data-structures
description: Master JavaScript objects and arrays including manipulation methods, prototypal inheritance, and complex data structure patterns.
sasmp_version: "1.3.0"
bonded_agent: 03-objects-arrays
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [method_type]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_method_list

observability:
  entry_log: "Data structures skill activated"
  exit_log: "Data structures reference provided"
---

# Data Structures Skill

## Quick Reference Card

### Object Operations
```javascript
// Create
const obj = { name: 'Alice', age: 30 };

// Access
obj.name;           // Dot notation
obj['name'];        // Bracket notation
obj?.address?.city; // Optional chaining

// Modify
obj.email = 'a@b.com';       // Add/update
delete obj.age;              // Remove
const { name, ...rest } = obj; // Destructure
```

### Object Methods
```javascript
Object.keys(obj);       // ['name', 'age']
Object.values(obj);     // ['Alice', 30]
Object.entries(obj);    // [['name','Alice'], ['age',30]]
Object.fromEntries(entries);  // Reverse

Object.assign({}, a, b);  // Shallow merge
{ ...a, ...b };           // Spread merge (preferred)

Object.freeze(obj);       // Immutable
Object.seal(obj);         // No add/delete
```

### Array Methods Cheat Sheet

**Transform (new array)**
```javascript
arr.map(x => x * 2);         // Transform each
arr.filter(x => x > 0);      // Keep matches
arr.slice(1, 3);             // Extract portion
arr.flat(2);                 // Flatten nested
arr.flatMap(x => [x, x*2]);  // Map + flatten
```

**Search**
```javascript
arr.find(x => x > 5);        // First match
arr.findIndex(x => x > 5);   // First index
arr.findLast(x => x > 5);    // Last match (ES2023)
arr.includes(5);             // Boolean check
arr.indexOf(5);              // Index or -1
```

**Reduce**
```javascript
arr.reduce((acc, x) => acc + x, 0);  // Sum
arr.reduce((acc, x) => ({ ...acc, [x.id]: x }), {});  // Index by
```

**Check**
```javascript
arr.every(x => x > 0);       // All pass
arr.some(x => x > 0);        // Any pass
```

**Mutate (modify original)**
```javascript
arr.push(x);     // Add end
arr.pop();       // Remove end
arr.unshift(x);  // Add start
arr.shift();     // Remove start
arr.splice(i, n, ...items);  // Remove/insert
arr.sort((a,b) => a - b);    // Sort
arr.reverse();   // Reverse
```

### Destructuring
```javascript
// Object
const { name, age = 0 } = user;
const { name: userName } = user;  // Rename
const { address: { city } } = user;  // Nested

// Array
const [first, , third] = arr;  // Skip
const [head, ...tail] = arr;   // Rest
[a, b] = [b, a];               // Swap
```

### Data Transformation Patterns
```javascript
// Group by
const byRole = users.reduce((acc, u) => {
  (acc[u.role] ??= []).push(u);
  return acc;
}, {});

// Unique values
const unique = [...new Set(arr)];

// Index by ID
const byId = arr.reduce((acc, x) => ({ ...acc, [x.id]: x }), {});
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Shallow copy bug | Nested changes shared | Use `structuredClone()` |
| Mutation side effect | Original changed | Use spread/map |
| `undefined` access | Property doesn't exist | Use `?.` optional chain |
| Sort not working | Wrong order | Provide compare function |

### Deep Clone
```javascript
// Modern (preferred)
const deep = structuredClone(original);

// JSON (limited - no functions, dates)
const deep = JSON.parse(JSON.stringify(original));
```

### Debug Checklist
```javascript
// 1. Inspect structure
console.log(JSON.stringify(obj, null, 2));

// 2. Check array vs object
console.log(Array.isArray(value));

// 3. Check prototype
console.log(Object.getPrototypeOf(obj));
```

## Production Patterns

### Immutable Update
```javascript
// Object
const updated = { ...user, name: 'New Name' };

// Array
const added = [...arr, newItem];
const removed = arr.filter(x => x.id !== id);
const updated = arr.map(x => x.id === id ? { ...x, ...changes } : x);
```

### Safe Access
```javascript
const city = user?.address?.city ?? 'Unknown';
const first = arr?.[0] ?? defaultValue;
```

## Related

- **Agent 03**: Objects & Arrays (detailed learning)
- **Skill: fundamentals**: Variables and types
- **Skill: modern-javascript**: ES6+ features
