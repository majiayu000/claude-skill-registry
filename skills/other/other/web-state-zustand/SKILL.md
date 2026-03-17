---
name: web-state-zustand
description: Zustand stores, client state patterns. Use when deciding between Zustand vs useState, managing global state, avoiding Context misuse, or handling form state.
---

# Client State Management Patterns

> **Quick Guide:** Local UI state? useState. Shared UI (2+ components)? Zustand. Server data? Use your data fetching solution. URL-appropriate filters? searchParams. NEVER use Context for state management.

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md) and [examples/forms.md](examples/forms.md)
- For anti-pattern code examples, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Managing Client State

**(You MUST use a data fetching solution for ALL server/API data - NEVER useState, Zustand, or Context)**

**(You MUST use Zustand for ALL shared UI state (2+ components) - NOT Context or prop drilling)**

**(You MUST use useState ONLY for truly component-local state - NOT for anything shared)**

**(You MUST use named exports ONLY - NO default exports in any state files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

</critical_requirements>

---

**Auto-detection:** Deciding between Zustand vs useState, global state management, Context misuse, client state patterns

**When to use:**

- Deciding between Zustand or useState for a use case
- Setting up Zustand for shared UI state (modals, sidebars, preferences)
- Understanding when NOT to use Context for state management
- Managing form state and validation patterns

**Key patterns covered:**

- Client state = useState (local) or Zustand (shared, 2+ components)
- Context for dependency injection only (NEVER for state management)
- URL params for shareable/bookmarkable state (filters, search)
- Form patterns with controlled components and Zod validation

**When NOT to use:**

- Server/API data (use a dedicated data fetching solution)
- State that should be shareable via URL (use searchParams)
- Any Context-based state management approach

---

<philosophy>

## Philosophy

React provides multiple tools for managing client state, but each has a specific purpose. The key principle: **use the right tool for the right job**. Server data belongs in a dedicated data fetching layer with caching and synchronization. Local UI state stays in useState. Shared UI state lives in Zustand for performance. URL state makes filters shareable. Context is ONLY for dependency injection, never state management.

The decision tree at the top of this skill guides you to the right solution based on your specific use case. Follow it strictly to avoid common pitfalls like using Context for state or putting server data in client state.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Server State vs Client State Decision

**STRICT SEPARATION REQUIRED**

The most critical decision: is this server data or client data?

#### Decision Tree

```
Is it server data (from API)?
├─ YES → Data fetching solution (not this skill's scope)
└─ NO → Is it URL-appropriate (filters, search)?
    ├─ YES → URL params (searchParams)
    └─ NO → Is it needed in 2+ components?
        ├─ YES → Zustand
        └─ NO → Is it truly component-local?
            ├─ YES → useState
            └─ NO → Is it a singleton/dependency?
                └─ YES → Context (ONLY for DI, not state)
```

#### Constants

```typescript
// File naming convention
// stores/ui-store.ts (kebab-case, named export)

const MIN_PASSWORD_LENGTH = 8;
const MAX_RETRY_ATTEMPTS = 3;
const DEBOUNCE_DELAY_MS = 300;
```

For implementation examples, see [examples/core.md](examples/core.md#pattern-1-server-state-vs-client-state).

---

### Pattern 2: Local State with useState

Use ONLY when state is truly component-local and never shared.

#### When to Use

- State used ONLY in one component (isExpanded, isOpen)
- Temporary UI state that never needs to be shared
- Form input values (if form is self-contained)

#### When NOT to Use

- State needed in 2+ components (use Zustand)
- Prop drilling 3+ levels (use Zustand)
- Server data (use a data fetching solution)

For implementation examples and good/bad comparisons, see [examples/core.md](examples/core.md#pattern-2-local-state-with-usestate).

---

### Pattern 3: Global State with Zustand

Use as soon as state is needed in 2+ components across the tree.

#### When to Use

- State needed by 2+ components across the tree
- Modal state (trigger from header, render in layout)
- Sidebar collapsed (header button + sidebar component)
- User preferences (theme, language, layout)
- Shopping cart, filters, selected items
- Any shared UI state

For store setup, usage patterns, and shallow comparison examples, see [examples/core.md](examples/core.md#pattern-3-global-state-with-zustand).

---

### Pattern 4: Context API - Dependency Injection ONLY

Context is NOT a state management solution. It's for dependency injection and singletons ONLY.

#### ONLY Use Context For

- Framework providers (QueryClientProvider, Router, etc.)
- Dependency injection (services, API clients, DB connections)
- Singletons that NEVER or RARELY change (theme configuration, i18n)
- Values that are set once at app initialization

#### NEVER Use Context For

- **ANY state management** (use Zustand instead)
- **ANY frequently updating values** (massive performance issues)
- Server data (use a data fetching solution)
- UI state (use Zustand for shared, useState for local)
- User interactions, selections, filters (use Zustand)
- Shopping carts, modals, sidebars (use Zustand)

For examples of why Context fails for state and acceptable usage, see [examples/core.md](examples/core.md#pattern-4-context-api---dependency-injection-only).

---

### Pattern 5: URL State for Shareable Filters

Use URL params for shareable/bookmarkable state.

#### When to Use URL State

- Filter selections
- Search queries
- Pagination state
- Sort order
- Any state that should be shareable via URL

For Next.js implementation examples, see [examples/core.md](examples/core.md#pattern-5-url-state-for-shareable-filters).

---

### Pattern 6: Form State and Validation

Use controlled components with Zod validation.

For controlled component patterns and Zod schema validation examples, see [examples/forms.md](examples/forms.md#pattern-6-form-state-and-validation).

</patterns>

---

<decision_framework>

## Decision Framework

### State Management Decision Tree

```
What kind of state do I have?

Is it server data (from API)?
├─ YES → Use your data fetching solution (not this skill's scope)
└─ NO → Is it URL-appropriate (filters, search, shareable)?
    ├─ YES → URL params (searchParams)
    └─ NO → Is it needed in 2+ components?
        ├─ YES → Zustand
        └─ NO → Is it truly component-local?
            ├─ YES → useState
            └─ NO → Is it a singleton/dependency?
                └─ YES → Context (ONLY for DI)
```

### Form Library Decision

```
What kind of form do I have?

Simple form (1-3 fields, minimal validation)?
├─ YES → Vanilla React (useState + Zod)
└─ NO → Complex form (10+ fields, field-level validation)?
    └─ YES → React Hook Form
```

### Quick Reference Table

| Use Case                        | Solution               | Why                                          |
| ------------------------------- | ---------------------- | -------------------------------------------- |
| Server/API data                 | Data fetching solution | Caching, synchronization, loading states     |
| Shareable filters               | URL params             | Bookmarkable, browser navigation             |
| Shared UI state (2+ components) | Zustand                | Fast, selective re-renders, no prop drilling |
| Local UI state (1 component)    | useState               | Simple, component-local                      |
| Framework providers             | Context                | Singletons that never change                 |
| Dependency injection            | Context                | Services, DB connections                     |
| **ANY state management**        | **NEVER Context**      | **Use Zustand instead**                      |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Storing server/API data in client state (useState, Context, Zustand)** - causes stale data, no caching, manual sync complexity
- **Using Context with useState/useReducer for state management** - every consumer re-renders on any change, performance nightmare
- **Using useState for state needed in 2+ components** - causes prop drilling, tight coupling, refactoring difficulty
- **Default exports in state files** - violates project conventions, breaks tree-shaking
- **Magic numbers in validation or initial state** - makes rules unclear, hard to maintain

**Medium Priority Issues:**

- Prop drilling 3+ levels instead of using Zustand
- Filter state in useState instead of URL params (not shareable)
- Creating unnecessary object references in Zustand selectors (causes re-renders)
- Subscribing to entire Zustand store instead of specific values
- Validating on every keystroke instead of on blur/submit

**Common Mistakes:**

- Mixing controlled and uncontrolled inputs in forms
- Not preventing default on form submit
- Showing validation errors before user finishes typing
- Not typing form events explicitly (use `ChangeEvent<HTMLInputElement>`, `FormEvent<HTMLFormElement>`)
- Disabling input fields during submission (only disable submit button)
- Not handling submit errors with user-friendly messages
- Missing loading states during async operations

**Gotchas & Edge Cases:**

- Context re-renders ALL consumers when ANY value changes - no way to select specific values
- Zustand selectors that return new objects cause re-renders even if values identical (use `useShallow` from `zustand/react/shallow` or primitive selectors)
- URL params are always strings - need parsing for numbers/booleans
- Form validation on every keystroke kills performance - validate on blur/submit
- Persisting modal/sidebar state across sessions confuses users - only persist preferences
- **Zustand v5:** Selectors must return stable references - returning new functions/objects inline causes infinite loops
- **Zustand v5:** The old `shallow` second argument pattern is deprecated - use `useShallow` hook wrapper instead
- **Zustand v5:** The persist middleware no longer stores initial state during store creation - set computed/random initial values explicitly after store creation with `useStore.setState({ count: initialValue })`
- **Zustand v5:** Requires React 18+ and TypeScript 4.5+
- **Zustand v5:** `use-sync-external-store` is a peer dependency when using `zustand/traditional` (for `createWithEqualityFn`)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use a data fetching solution for ALL server/API data - NEVER useState, Zustand, or Context)**

**(You MUST use Zustand for ALL shared UI state (2+ components) - NOT Context or prop drilling)**

**(You MUST use useState ONLY for truly component-local state - NOT for anything shared)**

**(You MUST use named exports ONLY - NO default exports in any state files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

**Failure to follow these rules will cause stale data issues, performance problems, and convention violations.**

</critical_reminders>
