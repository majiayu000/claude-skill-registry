---
name: web-utilities-native-js
description: Modern native JavaScript (ES2022-ES2025) utility patterns - array methods, object manipulation, set operations, deep cloning, and function utilities that replace lodash
---

# Native JavaScript Utility Patterns

> **Quick Guide:** Prefer native JavaScript (ES2022-ES2025) for utility operations. Use `structuredClone` for deep cloning, `Object.groupBy` for grouping, ES2023 immutable array methods (`toSorted`, `toReversed`, `with`), and ES2025 Set methods for set operations. Only reach for utility libraries when native alternatives don't exist.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use native ES2022+ methods before considering utility libraries - check this skill first)**

**(You MUST use immutable array methods (`toSorted`, `toReversed`, `toSpliced`, `with`) instead of mutating methods)**

**(You MUST use `structuredClone` for deep cloning - NOT JSON.parse/JSON.stringify hacks)**

**(You MUST define named constants for all numeric values - NO magic numbers in utility functions)**

</critical_requirements>

---

**Auto-detection:** native JavaScript utilities, lodash alternative, ES2023 array methods, toSorted, toReversed, structuredClone, Object.groupBy, Set union, Set intersection, optional chaining, nullish coalescing, at(), findLast

**When to use:**

- Array manipulation (find, filter, map, sort, reverse, chunk, unique)
- Object operations (pick, omit, merge, clone, groupBy)
- Set operations (union, intersection, difference)
- Deep cloning without external libraries
- Function utilities (debounce, throttle, memoize)
- Safe property access with optional chaining

**When NOT to use:**

- Complex deep merge with custom strategies - use a library
- Lazy evaluation chains over large datasets - lodash chains are optimized
- Legacy browser support (IE11) without transpilation
- Objects containing functions that need cloning - `structuredClone` cannot clone functions

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Modern JavaScript (ES2022-ES2025) provides native alternatives for ~80% of common utility library functions. Using native methods means:

1. **Zero bundle cost** - No additional bytes shipped to users
2. **Better performance** - Native implementations are engine-optimized
3. **Future-proof** - Standards evolve, libraries may not
4. **Simpler debugging** - No library internals to step through

**Key principle:** Check native JavaScript first. Only use utility libraries for genuinely missing functionality.

```typescript
// Native is free - no imports needed
const unique = [...new Set(items)];
const last = items.at(-1);
const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name));
const cloned = structuredClone(complexObject);
```

**ES Version Reference:**

| Feature                          | ES Version | Browser Support           |
| -------------------------------- | ---------- | ------------------------- |
| Optional chaining (`?.`)         | ES2020     | All modern browsers       |
| Nullish coalescing (`??`)        | ES2020     | All modern browsers       |
| `at()` negative indexing         | ES2022     | All modern browsers       |
| `toSorted`, `toReversed`, `with` | ES2023     | All modern browsers       |
| `Object.groupBy`, `Map.groupBy`  | ES2024     | Chrome 117+, Safari 17.4+ |
| Set methods (union, etc.)        | ES2025     | Chrome 122+, Safari 17+   |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Safe Property Access

Use optional chaining and nullish coalescing instead of lodash `_.get`.

```typescript
// ✅ Good Example - Optional chaining with nullish coalescing
interface User {
  address?: {
    city?: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
  };
  settings?: {
    theme?: string;
  };
}

const DEFAULT_CITY = "Unknown";
const DEFAULT_THEME = "light";

function getUserCity(user: User | null): string {
  return user?.address?.city ?? DEFAULT_CITY;
}

function getCoordinates(
  user: User | null,
): { lat: number; lng: number } | null {
  return user?.address?.coordinates ?? null;
}

// Method calls with optional chaining
const result = user?.settings?.getTheme?.() ?? DEFAULT_THEME;

// Array access with optional chaining
const firstItem = data?.items?.[0]?.name ?? "No items";
```

**Why good:** zero bundle cost, handles null/undefined gracefully, type-safe with TypeScript inference

```typescript
// ❌ Bad Example - Manual null checks or lodash
import { get } from "lodash";

// Verbose manual checking
const city =
  user && user.address && user.address.city ? user.address.city : "Unknown";

// Lodash adds ~5KB for this
const city = get(user, "address.city", "Unknown");
```

**Why bad:** lodash `get` adds bundle weight for something native does better, manual null checks are verbose and error-prone

---

### Pattern 2: Immutable Array Operations (ES2023)

Use `toSorted`, `toReversed`, `toSpliced`, and `with` for immutable transformations.

```typescript
// ✅ Good Example - ES2023 immutable methods
interface Product {
  id: string;
  name: string;
  price: number;
}

const products: Product[] = [
  { id: "1", name: "Widget", price: 25 },
  { id: "2", name: "Gadget", price: 15 },
  { id: "3", name: "Gizmo", price: 35 },
];

// toSorted - returns new sorted array, original unchanged
const byPrice = products.toSorted((a, b) => a.price - b.price);
const byName = products.toSorted((a, b) => a.name.localeCompare(b.name));

// toReversed - returns new reversed array
const reversed = products.toReversed();

// with - replace element at index immutably
const INDEX_TO_UPDATE = 1;
const updated = products.with(INDEX_TO_UPDATE, {
  ...products[INDEX_TO_UPDATE],
  price: 20,
});

// toSpliced - immutable splice
const START_INDEX = 1;
const DELETE_COUNT = 1;
const withoutSecond = products.toSpliced(START_INDEX, DELETE_COUNT);
const withInserted = products.toSpliced(START_INDEX, 0, {
  id: "4",
  name: "New",
  price: 10,
});

// Original array is unchanged
console.log(products[1].price); // Still 15
```

**Why good:** immutability prevents side effects, works with React state, original data preserved for comparison

```typescript
// ❌ Bad Example - Mutating methods
const sorted = products.sort((a, b) => a.price - b.price);
// products is now also sorted - mutation!

const reversed = products.reverse();
// products is now also reversed - mutation!

products[1] = { ...products[1], price: 20 };
// Direct mutation - React won't detect change
```

**Why bad:** mutations cause bugs in shared state, React cannot detect changes, original data lost

---

### Pattern 3: Negative Indexing with at()

Use `at()` for negative indices instead of `arr[arr.length - 1]`.

```typescript
// ✅ Good Example - Using at() for negative indexing
const items = ["first", "second", "third", "fourth", "last"];

// Access from end
const last = items.at(-1); // "last"
const secondToLast = items.at(-2); // "fourth"
const first = items.at(0); // "first"

// Works with strings too
const str = "hello";
const lastChar = str.at(-1); // "o"

// Useful in functions
function getLastN<T>(arr: T[], n: number): T[] {
  const results: T[] = [];
  for (let i = 1; i <= n; i++) {
    const item = arr.at(-i);
    if (item !== undefined) {
      results.unshift(item);
    }
  }
  return results;
}

const LAST_THREE = 3;
const lastThree = getLastN(items, LAST_THREE); // ["third", "fourth", "last"]
```

**Why good:** cleaner syntax, works with both arrays and strings, handles bounds gracefully (returns undefined)

```typescript
// ❌ Bad Example - Manual length calculation
const last = items[items.length - 1];
const secondToLast = items[items.length - 2];

// Verbose and error-prone
function getLast<T>(arr: T[]): T | undefined {
  if (arr.length === 0) return undefined;
  return arr[arr.length - 1];
}
```

**Why bad:** repetitive length calculations, easy to make off-by-one errors, verbose for a common operation

---

### Pattern 4: Finding from End (ES2023)

Use `findLast` and `findLastIndex` instead of reversing or manual loops.

```typescript
// ✅ Good Example - findLast and findLastIndex
interface LogEntry {
  timestamp: Date;
  level: "info" | "warn" | "error";
  message: string;
}

const logs: LogEntry[] = [
  { timestamp: new Date("2026-01-01"), level: "info", message: "Started" },
  { timestamp: new Date("2026-01-02"), level: "error", message: "Failed" },
  { timestamp: new Date("2026-01-03"), level: "info", message: "Recovered" },
  {
    timestamp: new Date("2026-01-04"),
    level: "error",
    message: "Failed again",
  },
];

// Find last error
const lastError = logs.findLast((log) => log.level === "error");
// { timestamp: ..., level: "error", message: "Failed again" }

// Find index of last error
const lastErrorIndex = logs.findLastIndex((log) => log.level === "error");
// 3

// Combine with other operations
const lastInfoBeforeError = logs.findLast(
  (log, index) => log.level === "info" && index < lastErrorIndex,
);
```

**Why good:** single pass from end, no array reversal needed, matches find/findIndex API

```typescript
// ❌ Bad Example - Reverse then find or manual loop
// Wasteful - creates reversed copy
const lastError = [...logs].reverse().find((log) => log.level === "error");

// Verbose manual loop
let lastError: LogEntry | undefined;
for (let i = logs.length - 1; i >= 0; i--) {
  if (logs[i].level === "error") {
    lastError = logs[i];
    break;
  }
}
```

**Why bad:** reversing creates unnecessary copy, manual loops are verbose and error-prone

---

### Pattern 5: Deep Cloning with structuredClone

Use `structuredClone` for deep cloning instead of JSON tricks or lodash.

```typescript
// ✅ Good Example - structuredClone for deep copies
interface AppState {
  user: {
    id: string;
    profile: {
      name: string;
      settings: Map<string, string>;
    };
  };
  history: Date[];
  data: Set<number>;
}

const originalState: AppState = {
  user: {
    id: "123",
    profile: {
      name: "John",
      settings: new Map([["theme", "dark"]]),
    },
  },
  history: [new Date("2026-01-01"), new Date("2026-01-02")],
  data: new Set([1, 2, 3]),
};

// Deep clone - handles Map, Set, Date, nested objects
const clonedState = structuredClone(originalState);

// Modifications don't affect original
clonedState.user.profile.name = "Jane";
clonedState.user.profile.settings.set("theme", "light");

console.log(originalState.user.profile.name); // "John" - unchanged
console.log(originalState.user.profile.settings.get("theme")); // "dark" - unchanged

// Works with circular references
const circular: { self?: unknown } = {};
circular.self = circular;
const clonedCircular = structuredClone(circular); // Works!
```

**Why good:** handles Map, Set, Date, RegExp, ArrayBuffer, circular references - JSON cannot do any of these

```typescript
// ❌ Bad Example - JSON round-trip or spread
// JSON loses Date, Map, Set, undefined, functions
const broken = JSON.parse(JSON.stringify(originalState));
// broken.history[0] is now a string, not Date!
// broken.user.profile.settings is now {} empty object!
// broken.data is now {} empty object!

// Spread is shallow only
const shallow = { ...originalState };
shallow.user.profile.name = "Jane";
console.log(originalState.user.profile.name); // "Jane" - mutated!
```

**Why bad:** JSON loses type information (Date, Map, Set, undefined), spread only clones one level deep

---

### Pattern 6: Object.groupBy (ES2024)

Use `Object.groupBy` instead of reduce-based grouping or lodash `_.groupBy`.

```typescript
// ✅ Good Example - Object.groupBy
interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
}

const products: Product[] = [
  { id: "1", name: "Laptop", category: "Electronics", price: 999 },
  { id: "2", name: "Phone", category: "Electronics", price: 699 },
  { id: "3", name: "Shirt", category: "Clothing", price: 49 },
  { id: "4", name: "Pants", category: "Clothing", price: 79 },
];

// Group by category
const byCategory = Object.groupBy(products, (product) => product.category);
// { Electronics: [...], Clothing: [...] }

// Group by computed key
const EXPENSIVE_THRESHOLD = 100;
const byPriceRange = Object.groupBy(products, (product) =>
  product.price >= EXPENSIVE_THRESHOLD ? "expensive" : "affordable",
);
// { expensive: [laptop, phone], affordable: [shirt, pants] }

// Use Map.groupBy for object keys
interface StockStatus {
  restock: boolean;
}
const LOW_STOCK_THRESHOLD = 10;
const needsRestock: StockStatus = { restock: true };
const sufficient: StockStatus = { restock: false };

const inventory = [
  { name: "Widget", quantity: 5 },
  { name: "Gadget", quantity: 50 },
  { name: "Gizmo", quantity: 3 },
];

const byStockStatus = Map.groupBy(inventory, (item) =>
  item.quantity < LOW_STOCK_THRESHOLD ? needsRestock : sufficient,
);
// Access: byStockStatus.get(needsRestock)
```

**Why good:** declarative, built-in, returns null-prototype object (no prototype pollution risk)

```typescript
// ❌ Bad Example - Reduce-based grouping
const byCategory = products.reduce<Record<string, Product[]>>(
  (acc, product) => {
    const key = product.category;
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(product);
    return acc;
  },
  {},
);

// Or lodash - adds bundle weight
import { groupBy } from "lodash";
const byCategory = groupBy(products, "category");
```

**Why bad:** reduce-based grouping is verbose and error-prone, lodash adds unnecessary bytes

</patterns>

---

<integration>

## Integration Guide

**Native utilities integrate with:**

- **TypeScript**: Full type inference for all native methods
- **React**: Immutable methods (`toSorted`, `with`) work well with React state
- **Any framework**: Zero dependencies means universal compatibility

**When to use utility libraries instead:**

- Complex deep merge with array handling strategies
- Lazy evaluation chains for performance on large datasets
- Browser compatibility requirements (IE11)
- Functions that native JavaScript doesn't provide (debounce with cancel, etc.)

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use native ES2022+ methods before considering utility libraries - check this skill first)**

**(You MUST use immutable array methods (`toSorted`, `toReversed`, `toSpliced`, `with`) instead of mutating methods)**

**(You MUST use `structuredClone` for deep cloning - NOT JSON.parse/JSON.stringify hacks)**

**(You MUST define named constants for all numeric values - NO magic numbers in utility functions)**

**Failure to follow these rules will cause unnecessary bundle bloat and mutation bugs.**

</critical_reminders>
