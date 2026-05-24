---
name: fundamentals
description: Core JavaScript fundamentals including variables, data types, operators, control flow, and basic syntax. Essential foundation for all JavaScript development.
sasmp_version: "1.3.0"
bonded_agent: 01-javascript-fundamentals
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [depth, examples]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: provide_basics_first

observability:
  entry_log: "Fundamentals skill activated"
  exit_log: "Fundamentals reference provided"
---

# JavaScript Fundamentals Skill

## Quick Reference Card

### Variable Declaration
```javascript
const PI = 3.14159;     // Immutable binding (preferred)
let count = 0;          // Reassignable
var legacy = "avoid";   // Function-scoped (avoid)
```

### 8 Data Types
| Type | Example | typeof |
|------|---------|--------|
| String | `"hello"` | `"string"` |
| Number | `42`, `3.14`, `NaN` | `"number"` |
| Boolean | `true`, `false` | `"boolean"` |
| Null | `null` | `"object"` |
| Undefined | `undefined` | `"undefined"` |
| Symbol | `Symbol('id')` | `"symbol"` |
| BigInt | `9007199254740991n` | `"bigint"` |
| Object | `{}`, `[]`, `fn` | `"object"` |

### Operators Cheat Sheet
```javascript
// Arithmetic
+ - * / % **

// Comparison (always use strict)
=== !== > < >= <=

// Logical
&& || !

// Nullish
?? ?.

// Assignment
= += -= *= /= ??= ||= &&=
```

### Control Flow Patterns
```javascript
// Early return (preferred)
function validate(input) {
  if (!input) return { error: 'Required' };
  if (input.length < 3) return { error: 'Too short' };
  return { valid: true };
}

// Switch with exhaustive handling
function getColor(status) {
  switch (status) {
    case 'success': return 'green';
    case 'warning': return 'yellow';
    case 'error': return 'red';
    default: return 'gray';
  }
}
```

### Type Coercion Rules
```javascript
// Explicit conversion (preferred)
Number('42')     // 42
String(42)       // "42"
Boolean(1)       // true

// Truthy values: non-zero numbers, non-empty strings, objects
// Falsy values: 0, "", null, undefined, NaN, false
```

### Modern Operators
```javascript
// Nullish coalescing
const name = input ?? 'Guest';     // Only null/undefined

// Optional chaining
const city = user?.address?.city;  // Safe navigation

// Logical assignment
config.debug ??= false;            // Assign if nullish
```

## Troubleshooting

### Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ReferenceError: x is not defined` | Variable not declared | Check spelling, scope |
| `TypeError: Cannot read property` | Accessing null/undefined | Use optional chaining `?.` |
| `NaN` result | Invalid number operation | Validate input types |
| Unexpected `true`/`false` | Loose equality `==` | Use strict `===` |

### Debug Checklist
```javascript
// 1. Check type
console.log(typeof variable);

// 2. Check value
console.log(JSON.stringify(variable));

// 3. Check for null/undefined
console.log(variable === null, variable === undefined);

// 4. Use debugger
debugger;
```

## Production Patterns

### Input Validation
```javascript
function processNumber(value) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    throw new TypeError('Expected a valid number');
  }
  return value * 2;
}
```

### Safe Property Access
```javascript
const city = user?.address?.city ?? 'Unknown';
const callback = options.onComplete?.();
```

## Related

- **Agent 01**: JavaScript Fundamentals (detailed learning)
- **Skill: functions**: Function patterns
- **Skill: data-structures**: Objects and arrays
