---
name: js-micro-utilities
description: Zero-dependency JavaScript utilities using native APIs and just-* micro-packages. Use when manipulating objects, arrays, strings, numbers, or functions. Scan tables for native solution first (backticks), fall back to just-* package only when needed. Prefer native over dependencies.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# JavaScript Micro-Utilities

Zero-dependency utilities for common JavaScript operations. **Prefer native APIs** (in backticks) over packages. Install `just-*` packages only when native solutions don't exist.

## Installation

```bash
npm i just-diff just-compare just-extend just-pick just-omit  # objects
npm i just-shuffle just-partition just-range just-order-by    # arrays
npm i just-debounce-it just-throttle just-memoize just-once   # functions
```

Import with ESM:
```javascript
import diff from 'just-diff';
import shuffle from 'just-shuffle';
```

---

## Collections `{}[]`

| Need | Solution |
|------|----------|
| Deep diff two objects/arrays | `just-diff` |
| Apply JSON-patch to object | `just-diff-apply` |
| Deep equality check | `just-compare` |
| Deep clone | `structuredClone(obj)` |
| Extract property from array | `arr.map(x => x.prop)` |
| Remove nullish from array | `arr.filter(x => x != null)` |

---

## Objects `{}`

### Merging

| Need | Solution |
|------|----------|
| Deep merge | `just-extend` |
| Shallow merge | `{...a, ...b}` or `Object.assign(target, src)` |

### Extracting

| Need | Solution |
|------|----------|
| Values as array | `Object.values(obj)` |
| Key-value pairs | `Object.entries(obj)` |
| Keep only certain keys | `just-pick` |
| Exclude certain keys | `just-omit` |

### Transforming

```javascript
// Filter properties
Object.fromEntries(Object.entries(obj).filter(([k, v]) => predicate(k, v)))

// Map values
Object.fromEntries(Object.entries(obj).map(([k, v]) => [k, fn(v)]))

// Map keys
Object.fromEntries(Object.entries(obj).map(([k, v]) => [fn(k), v]))

// Swap keys/values
Object.fromEntries(Object.entries(obj).map(([k, v]) => [v, k]))

// Reduce to value
Object.entries(obj).reduce((acc, [k, v]) => ..., init)
```

### Deep Operations

| Need | Solution |
|------|----------|
| Map values recursively | `just-deep-map-values` |
| Safe nested get | `obj?.a?.b?.c` |
| Safe nested set | `just-safe-set` |
| Check nested exists | `obj?.a?.b !== undefined` |

### Type Checking

| Need | Solution |
|------|----------|
| Is empty | `just-is-empty` |
| Has circular refs | `just-is-circular` |
| Is primitive | `typeof x !== 'object' \|\| x === null` |
| Better typeof | `just-typeof` (distinguishes array, null, date, regexp) |

---

## Arrays `[]`

### Access

| Need | Solution |
|------|----------|
| Last element | `arr.at(-1)` |
| All except first | `arr.slice(1)` |
| Random element | `just-random` |

### Creating

| Need | Solution |
|------|----------|
| Number sequence | `just-range` |
| All combinations | `just-cartesian-product` |
| All orderings | `just-permutations` |

### Transforming

| Need | Solution |
|------|----------|
| Dedupe primitives | `[...new Set(arr)]` |
| Flatten nested | `arr.flat(depth)` |
| Remove falsy | `arr.filter(Boolean)` |
| Shuffle | `just-shuffle` |
| Chunk into groups | `just-split` |

### Sorting

| Need | Solution |
|------|----------|
| Immutable sort by prop | `arr.toSorted((a, b) => a.prop - b.prop)` |
| Multi-prop sort | `just-order-by` |

### Set Operations

| Need | Solution |
|------|----------|
| Intersection | `arr1.filter(x => arr2.includes(x))` |
| Difference | `arr.filter(x => !remove.includes(x))` |
| Union (deduped) | `[...new Set([...a, ...b])]` |

### Splitting

```javascript
// Split at index
[arr.slice(0, i), arr.slice(i)]

// Split by predicate → [matches, nonMatches]
import partition from 'just-partition';
const [evens, odds] = partition(arr, x => x % 2 === 0);
```

### Grouping

```javascript
// Native grouping (ES2024)
Object.groupBy(arr, item => item.category)

// Array to object by key
Object.fromEntries(arr.map(x => [x[key], x]))

// Zip arrays together
import zip from 'just-zip-it';
zip([1, 2], ['a', 'b']) // [[1, 'a'], [2, 'b']]
```

### Inserting

```javascript
// Insert at index (immutable)
arr.toSpliced(i, 0, ...items)
```

---

## Statistics `Σ`

| Need | Solution |
|------|----------|
| Average | `arr.reduce((a, b) => a + b, 0) / arr.length` |
| Median | `just-median` |
| Mode | `just-mode` |
| Percentile | `just-percentile` |
| Variance | `just-variance` |
| Std deviation | `just-standard-deviation` |
| Skewness | `just-skewness` |

---

## Strings `""`

### Padding & Truncation

| Need | Solution |
|------|----------|
| Pad start | `str.padStart(n, char)` |
| Pad end | `str.padEnd(n, char)` |
| Truncate with `...` | `just-truncate` |
| Truncate at word | `just-prune` |

### Case Conversion

| Need | Solution |
|------|----------|
| camelCase | `just-camel-case` |
| kebab-case | `just-kebab-case` |
| snake_case | `just-snake-case` |
| PascalCase | `just-pascal-case` |
| Capitalize first | `str[0].toUpperCase() + str.slice(1)` |

### Replacement

| Need | Solution |
|------|----------|
| Replace all | `str.replaceAll(find, replace)` |
| Remove whitespace | `str.replaceAll(' ', '')` |
| Template interpolation | `just-template` (supports `{{a.b.c}}` paths) |

---

## Numbers `+-`

| Need | Solution |
|------|----------|
| Clamp to range | `Math.min(Math.max(n, min), max)` |
| Is prime | `just-is-prime` |
| True modulo (neg-safe) | `just-modulo` |
| Random int in range | `Math.floor(Math.random() * (max - min + 1)) + min` |

---

## Functions `=>`

### Composition

| Need | Solution |
|------|----------|
| Right-to-left `f(g(h(x)))` | `just-compose` |
| Left-to-right `h(g(f(x)))` | `just-pipe` |

### Partial Application

| Need | Solution |
|------|----------|
| Curry | `just-curry-it` |
| Fix args with placeholders | `just-partial-it` |
| Swap first two args | `just-flip` |
| Method to function | `Function.prototype.call.bind(method)` |

### Rate Limiting

| Need | Solution |
|------|----------|
| Debounce (wait for pause) | `just-debounce-it` |
| Throttle (once per interval) | `just-throttle` |
| Run only first call | `just-once` |

### Caching

| Need | Solution |
|------|----------|
| Memoize by args | `just-memoize` |
| Cache last call only | `just-memoize-last` |

---

## Quick Reference

### Most Common Native

```javascript
// Clone
const copy = structuredClone(obj);

// Dedupe
const unique = [...new Set(arr)];

// Last element
const last = arr.at(-1);

// Safe access
const val = obj?.deeply?.nested?.prop;

// Group by
const grouped = Object.groupBy(items, x => x.type);

// Immutable sort
const sorted = arr.toSorted((a, b) => a.name.localeCompare(b.name));
```

### Most Common just-*

```javascript
import debounce from 'just-debounce-it';
import throttle from 'just-throttle';
import pick from 'just-pick';
import omit from 'just-omit';
import shuffle from 'just-shuffle';
import partition from 'just-partition';

// Debounce input handler
const handleInput = debounce(value => search(value), 300);

// Throttle scroll handler
const handleScroll = throttle(() => updatePosition(), 100);

// Pick specific keys
const subset = pick(user, ['id', 'name', 'email']);

// Omit sensitive keys
const safe = omit(user, ['password', 'token']);

// Shuffle array
const randomized = shuffle(cards);

// Split by condition
const [valid, invalid] = partition(inputs, x => x.isValid);
```

---

## Decision Tree

1. **Can native API do it?** → Use native (zero deps)
2. **Is it a one-liner?** → Write inline
3. **Need tested edge cases?** → Use `just-*` package
4. **Complex algorithm?** → Use `just-*` package
