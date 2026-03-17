---
name: web-state-jotai
description: Atomic state management with auto-dependency tracking
---

# Jotai Atomic State Management

> **Quick Guide:** Jotai provides atomic, bottom-up state management with automatic dependency tracking. Use primitive atoms for simple values, derived atoms for computed state, and async atoms with Suspense for data loading. Components only re-render when their specific atoms change.

**Detailed Resources:**

- For code examples, see [examples.md](examples.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Using Jotai

**(You MUST define atoms OUTSIDE components - creating atoms inside render causes broken state)**

**(You MUST wrap async atom consumers in Suspense boundaries - async atoms trigger Suspense by default)**

**(You MUST use write atoms (action atoms) to encapsulate state updates after async operations)**

**(You MUST use named exports ONLY - NO default exports in any atom files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in atom code)**

</critical_requirements>

---

**Auto-detection:** Jotai, atom, useAtom, useAtomValue, useSetAtom, atomWithStorage, atomFamily, derived atoms, computed atoms

**When to use:**

- Fine-grained reactivity without manual memoization
- Bottom-up state composition with automatic dependency tracking
- Async state with React Suspense integration
- Computed/derived state that auto-updates when dependencies change
- Avoiding prop drilling for shared UI state

**Key patterns covered:**

- Primitive atoms for basic state values
- Derived (read-only) atoms for computed values
- Write-only atoms for encapsulated actions
- Read-write atoms for lens-like patterns
- Async atoms with Suspense and loadable utilities
- atomFamily for parameterized atoms
- atomWithStorage for persistence
- splitAtom for array item isolation

**When NOT to use:**

- Server/API data (use your data fetching solution)
- Simple local component state (use useState)
- State that should be in URL (use searchParams)

---

<philosophy>

## Philosophy

Jotai takes an **atomic, bottom-up approach** to state management. The core principle: **"Anything that can be derived from the application state should be derived automatically."**

Think of atoms like cells in a spreadsheet:

- Each atom is an independent cell holding a value
- Derived atoms are formulas that reference other cells
- When a cell changes, only formulas depending on it recalculate
- This provides the minimum necessary work automatically

**Key characteristics:**

- **Bottom-up state design**: Build state from small, composable atoms
- **Automatic dependency tracking**: Like a spreadsheet - atoms automatically update when dependencies change
- **Fine-grained reactivity**: Components only re-render when their specific atoms change
- **First-class async support**: Async operations integrate seamlessly with React Suspense

**Mental Model:**
Instead of one large store, you have many small atoms that can be combined. This creates natural code splitting and enables precise re-render optimization without manual memoization.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Primitive Atoms

The simplest atom type - holds a single value with automatic type inference.

For implementation examples, see [examples.md](examples.md#pattern-1-primitive-atoms).

---

### Pattern 2: Derived (Read-Only) Atoms

Compute values from other atoms - cannot be written to directly. Dependencies are tracked automatically.

For implementation examples, see [examples.md](examples.md#pattern-2-derived-read-only-atoms).

---

### Pattern 3: Write-Only Atoms (Action Atoms)

Encapsulate side effects and update logic. Enable code splitting and lazy loading.

For implementation examples, see [examples.md](examples.md#pattern-3-write-only-atoms-action-atoms).

---

### Pattern 4: Read-Write Atoms

Atoms that can both read derived state and accept writes. Useful for lens-like patterns.

For implementation examples, see [examples.md](examples.md#pattern-4-read-write-atoms).

---

### Pattern 5: Async Atoms with Suspense

Async atoms trigger Suspense by default. Use loadable utility for non-Suspense handling.

For implementation examples, see [examples.md](examples.md#pattern-5-async-atoms-with-suspense).

---

### Pattern 6: atomFamily for Parameterized Atoms

Create atoms on-demand based on parameters. Ideal for collections where each item needs its own atom.

For implementation examples, see [examples.md](examples.md#pattern-6-atomfamily-for-parameterized-atoms).

---

### Pattern 7: atomWithStorage for Persistence

Persist atom values to localStorage, sessionStorage, or custom storage.

For implementation examples, see [examples.md](examples.md#pattern-7-atomwithstorage-for-persistence).

---

### Pattern 8: splitAtom for Array Optimization

Split an array atom into individual item atoms for optimized re-renders.

For implementation examples, see [examples.md](examples.md#pattern-8-splitatom-for-array-optimization).

---

### Pattern 9: selectAtom for Large Objects

Select specific properties from large objects to prevent unnecessary re-renders.

For implementation examples, see [examples.md](examples.md#pattern-9-selectatom-for-large-objects).

---

### Pattern 10: Store and Provider Patterns

Use custom stores for isolation, testing, or accessing state outside React.

For implementation examples, see [examples.md](examples.md#pattern-10-store-and-provider-patterns).

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST define atoms OUTSIDE components - creating atoms inside render causes broken state)**

**(You MUST wrap async atom consumers in Suspense boundaries - async atoms trigger Suspense by default)**

**(You MUST use write atoms (action atoms) to encapsulate state updates after async operations)**

**(You MUST use named exports ONLY - NO default exports in any atom files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in atom code)**

**Failure to follow these rules will cause state corruption, Suspense errors, and convention violations.**

</critical_reminders>
