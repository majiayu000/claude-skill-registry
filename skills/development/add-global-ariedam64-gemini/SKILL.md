---
name: add-global
description: Create a reactive global variable that derives from atoms with subscription support
aliases: [new-global, create-global]
---

# Add Global Skill

## Usage
```
/add-global <globalName>
```

---

## Step 1: Ask Questions

### 1. Global Purpose
```
What derived state does this global provide?
Brief description:
```

### 2. Source Atoms
```
Which atoms does this global derive from?
(List atom names from src/atoms/)

Examples: myInventoryAtom, myGardenAtom, weatherAtom
```

### 3. Derivation Logic
```
How is the global value computed from atoms?

A) Simple merge - Combine fields from multiple atoms
B) Transformation - Transform/filter atom data
C) Aggregation - Compute stats/totals from atoms
D) Complex - Multiple transformations
```

### 4. Update Sensitivity
```
Should subscribers react to every atom change?

A) Yes - Every change triggers update
B) No - Only meaningful changes (use subscribeStable)
```

### 5. Public API
```
Expose in window.Gemini.Globals?

A) Yes
B) No - Internal only
```

---

## Step 2: Create Global File

### Create `src/globals/variables/<globalName>.ts`

```typescript
import { createReactiveGlobal } from '../core/reactive';
import { Store } from '../../atoms';
import type { GlobalVariable, Unsubscribe } from '../core/types';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export interface <GlobalName> {
    // Derived fields
    field1: string;
    field2: number;
}

// ─────────────────────────────────────────────────────────────────────────────
// Derivation
// ─────────────────────────────────────────────────────────────────────────────

async function derive<GlobalName>(): Promise<<GlobalName>> {
    const atom1 = await Store.select('sourceAtom1');
    const atom2 = await Store.select('sourceAtom2');

    return {
        field1: atom1?.value ?? 'default',
        field2: atom2?.count ?? 0,
    };
}

// ─────────────────────────────────────────────────────────────────────────────
// Reactive Global
// ─────────────────────────────────────────────────────────────────────────────

const <globalName>Global = createReactiveGlobal<<GlobalName>>({
    name: '<globalName>',
    atomKeys: ['sourceAtom1', 'sourceAtom2'],  // Atoms to watch
    derive: derive<GlobalName>,
});

// ─────────────────────────────────────────────────────────────────────────────
// Public API
// ─────────────────────────────────────────────────────────────────────────────

let instance: GlobalVariable<<GlobalName>> | null = null;

export function get<GlobalName>(): GlobalVariable<<GlobalName>> {
    if (!instance) {
        instance = <globalName>Global;
    }
    return instance;
}
```

---

## Step 3: Register

### In `src/globals/index.ts`

```typescript
export { get<GlobalName> } from './variables/<globalName>';
export type { <GlobalName> } from './variables/<globalName>';
```

### In `src/api/index.ts` (if public)

```typescript
import { get<GlobalName> } from '../globals';

Globals: {
    // ... existing
    <globalName>: get<GlobalName>(),
}
```

---

## Step 4: Validate

### Structure
- [ ] File created in `src/globals/variables/<name>.ts`
- [ ] Type interface defined
- [ ] Derivation function implemented
- [ ] `createReactiveGlobal()` with correct `atomKeys`
- [ ] Lazy singleton getter exported

### API
- [ ] `get()` returns current value
- [ ] `subscribe(callback)` receives all updates
- [ ] `subscribeStable(callback)` receives meaningful updates only
- [ ] `destroy()` is idempotent

### Registration
- [ ] Exported from `src/globals/index.ts`
- [ ] Exposed in `src/api/index.ts` (if public)

---

## Usage Patterns

### Basic subscription
```typescript
const global = get<GlobalName>();

// Get current value
const value = global.get();

// Subscribe to all changes
const unsub = global.subscribe((value) => {
    console.log('Updated:', value);
});

// Cleanup
unsub();
```

### Stable subscription (less frequent)
```typescript
const unsub = global.subscribeStable((value) => {
    // Only fires on meaningful changes
    updateUI(value);
});
```

### In components/features
```typescript
const cleanups: (() => void)[] = [];

function start(): void {
    const unsub = get<GlobalName>().subscribe((value) => {
        onValueChange(value);
    });
    cleanups.push(unsub);
}

function stop(): void {
    cleanups.forEach(fn => fn());
    cleanups.length = 0;
}
```

---

## References

- Rules: `.claude/rules/state/globals.md`
- Existing globals: `src/globals/variables/`
- Core: `src/globals/core/`
