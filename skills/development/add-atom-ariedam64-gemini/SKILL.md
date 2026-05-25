---
name: add-atom
description: Add a new Jotai atom to the state system with type definitions, registry, and Store API access
aliases: [new-atom, create-atom]
---

# Add Atom Skill

## Usage
```
/add-atom <atomName>
```

---

## Step 1: Ask Questions

### 1. Atom Purpose
```
What state does this atom hold?
Brief description:
```

### 2. Data Source
```
Where does the data come from?

A) Game WebSocket - Captured from server messages
B) User input - Settings, preferences
C) Derived - Computed from other atoms
D) Internal - Module/feature internal state
```

### 3. Update Frequency
```
How often does this atom update?

A) Rarely - User actions only
B) Occasionally - Every few seconds
C) Frequently - Multiple times per second
→ If C: Consider adding a Signature function
```

### 4. Public API
```
Should this atom be exposed in window.Gemini?

A) Yes - Part of public API
B) No - Internal only
```

---

## Step 2: Define Types

### In `src/atoms/types.ts`

```typescript
// 1. Add to AtomKey union
export type AtomKey =
    | "existingAtom"
    | "<atomName>"  // Add this
    // ...

// 2. Define the state type
export interface <AtomName>State {
    // Define fields
}

// 3. Add to AtomTypeMap
export interface AtomTypeMap {
    existingAtom: ExistingState;
    <atomName>: <AtomName>State;  // Add this
    // ...
}
```

---

## Step 3: Declare Atom

### In `src/atoms/atoms.ts`

```typescript
import { atom } from 'jotai';
import type { <AtomName>State } from './types';

export const <atomName>Atom = atom<<AtomName>State | null>(null);
```

---

## Step 4: Register in Lookup

### In `src/atoms/lookup.ts`

```typescript
import { <atomName>Atom } from './atoms';

export const atomRegistry = {
    // ... existing
    <atomName>: <atomName>Atom,
} as const;
```

---

## Step 5: Export (if public)

### In `src/atoms/index.ts`

```typescript
export { <atomName>Atom } from './atoms';
export type { <AtomName>State } from './types';
```

---

## Step 6: Optional - Signature (for frequent updates)

### In `src/atoms/signature.ts`

```typescript
import type { <AtomName>State } from './types';

/**
 * Returns a stable hash for change detection
 * Only reacts to meaningful changes, not every tick
 */
export function get<AtomName>Signature(state: <AtomName>State | null): string {
    if (!state) return 'null';
    // Hash only fields that matter
    return `${state.id}-${state.version}`;
}
```

---

## Step 7: Optional - View (for UI consumption)

### In `src/atoms/view.ts`

```typescript
import type { <AtomName>State } from './types';

export interface <AtomName>View {
    // UI-friendly format
    items: string[];
    total: number;
}

export function get<AtomName>View(state: <AtomName>State | null): <AtomName>View {
    if (!state) return { items: [], total: 0 };

    return {
        items: state.items.map(item => item.name),
        total: state.items.length,
    };
}
```

---

## Step 8: Validate

### Registration
- [ ] Key added to `AtomKey` type in `types.ts`
- [ ] State type added to `AtomTypeMap` in `types.ts`
- [ ] Atom declared in `atoms.ts` with `atom<T | null>(null)`
- [ ] Atom registered in `lookup.ts`
- [ ] Exported from `index.ts` (if public)

### Store API
- [ ] `Store.select('<atomName>')` works
- [ ] `Store.set('<atomName>', value)` works
- [ ] `Store.subscribe('<atomName>', callback)` works

### Optional
- [ ] Signature added (if frequent updates)
- [ ] View added (if UI needs transformed data)

---

## Store API Usage

```typescript
// Read
const value = await Store.select('<atomName>');

// Write
await Store.set('<atomName>', newValue);

// Subscribe
const unsub = await Store.subscribe('<atomName>', (value) => {
    console.log('Changed:', value);
});

// Cleanup
unsub();
```

---

## References

- Rules: `.claude/rules/state/atoms.md`
- Existing atoms: `src/atoms/`
- Store implementation: `src/atoms/store.ts`
