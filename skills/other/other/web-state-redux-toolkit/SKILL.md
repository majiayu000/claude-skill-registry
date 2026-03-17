---
name: web-state-redux-toolkit
description: Redux Toolkit patterns for complex client state. Use when managing enterprise-scale state, needing DevTools, entity normalization, or RTK Query for data fetching.
---

# Redux Toolkit Patterns

> **Quick Guide:** Use Redux Toolkit for complex client state requiring DevTools, middleware, or entity normalization. Use RTK Query for data fetching with caching. Prefer Zustand for simpler UI state. NEVER use legacy Redux patterns (createStore, combineReducers manually, switch statements in reducers).

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Store setup, slices
  - [typed-hooks.md](examples/typed-hooks.md) - Type-safe hooks
  - [rtk-query.md](examples/rtk-query.md) - Data fetching
  - [entity-adapters.md](examples/entity-adapters.md) - Normalized state
  - [async-thunks.md](examples/async-thunks.md) - Async operations
  - [selectors.md](examples/selectors.md) - Memoized selectors
  - [rtk-2-features.md](examples/rtk-2-features.md) - **RTK 2.0**: combineSlices, inline selectors, buildCreateSlice
  - [middleware.md](examples/middleware.md) - Custom middleware
  - [testing.md](examples/testing.md) - Testing patterns
  - [integrations.md](examples/integrations.md) - Redux Persist
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Managing State with Redux Toolkit

**(You MUST use `configureStore` for store setup - NEVER legacy `createStore`)**

**(You MUST use `createSlice` for all reducers - NEVER switch statements or manual action creators)**

**(You MUST define typed hooks (`useAppSelector`, `useAppDispatch`) once in a hooks file)**

**(You MUST use named exports ONLY - NO default exports in any Redux files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

</critical_requirements>

---

**Auto-detection:** Redux Toolkit, createSlice, configureStore, RTK Query, createAsyncThunk, createEntityAdapter, useSelector, useDispatch

**When to use:**

- Complex client state requiring middleware, DevTools, or time-travel debugging
- Enterprise applications with multiple teams needing predictable state management
- Normalized entity state (lists of items with relationships)
- Data fetching with sophisticated caching (RTK Query)
- Applications requiring strict unidirectional data flow

**Key patterns covered:**

- Store configuration with `configureStore`
- Slice creation with `createSlice` and Immer integration
- **RTK 2.0**: Inline selectors in `createSlice`, `combineSlices`, `buildCreateSlice` for async thunks
- RTK Query for data fetching and caching
- Typed hooks for TypeScript integration
- Entity adapters for normalized state
- Async thunks with `createAsyncThunk`
- Middleware patterns

**When NOT to use:**

- Simple UI state (use Zustand or useState)
- Server state only (use React Query directly)
- Small to medium apps where Redux overhead is unnecessary
- Projects where team unfamiliarity with Redux outweighs benefits

---

<philosophy>

## Philosophy

Redux Toolkit (RTK) is the official, opinionated, batteries-included toolset for efficient Redux development. It eliminates the boilerplate of legacy Redux while maintaining predictable state management through strict unidirectional data flow.

**Core principle:** "One source of truth" - All application state lives in a single store, changes are made through pure reducer functions, and state is never mutated directly.

RTK uses Immer internally, allowing you to write "mutative" code that is actually immutable. This dramatically simplifies reducer logic while maintaining Redux's guarantees.

**Key architecture decisions:**

1. **configureStore** replaces createStore with sensible defaults (DevTools, thunk middleware, development checks)
2. **createSlice** generates action creators and action types automatically from reducer names
3. **RTK Query** provides a purpose-built data fetching and caching solution
4. **createEntityAdapter** standardizes normalized state patterns

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Store Configuration

Use `configureStore` with proper TypeScript types inferred from the store itself.

For store setup, typed hooks, and middleware configuration examples, see [examples/core.md](examples/core.md).

---

### Pattern 2: Slice Creation with createSlice

Use `createSlice` to define reducers, actions, and initial state together. Immer allows "mutative" syntax for immutable updates.

#### When to Use

- All Redux state management
- Generating action creators automatically
- Simplifying immutable update logic

#### When NOT to Use

- State that belongs in URL params (filters, search)
- Truly local component state (useState)
- Server state that should use RTK Query or React Query

For slice creation with typed state and PayloadAction, see [examples/core.md](examples/core.md).

---

### Pattern 3: Typed Hooks for Components

Define typed versions of `useDispatch` and `useSelector` once, then use everywhere. This ensures type safety without repetitive type annotations.

#### Why Typed Hooks Matter

- `useSelector` saves typing `(state: RootState)` every time
- `useDispatch` default type does not know about thunks
- `AppDispatch` includes thunk middleware types for correct dispatch typing

For typed hooks setup with `.withTypes()` (React Redux v9.1.0+), see [examples/typed-hooks.md](examples/typed-hooks.md).

---

### Pattern 4: RTK Query for Data Fetching

RTK Query is a purpose-built data fetching and caching solution. Use it when you need caching, automatic refetching, and cache invalidation.

#### When to Use RTK Query

- Data fetching with caching requirements
- Automatic refetch on focus/reconnect
- Cache invalidation with tags
- Optimistic updates for mutations

#### When NOT to Use

- Simple client state (use createSlice)
- When React Query is already established in the codebase
- When you need features RTK Query does not support

For createApi setup, endpoint definitions, and cache tags, see [examples/rtk-query.md](examples/rtk-query.md).

---

### Pattern 5: Entity Adapters for Normalized State

Use `createEntityAdapter` for collections of items (users, products, posts). It provides standardized CRUD operations and memoized selectors.

#### When to Use

- Lists of items with IDs
- Relational data that needs normalization
- CRUD operations on collections
- Performance-critical large lists

For entity adapter setup, CRUD operations, and selector usage, see [examples/entity-adapters.md](examples/entity-adapters.md).

---

### Pattern 6: Async Thunks with createAsyncThunk

Use `createAsyncThunk` for async operations that need to dispatch multiple actions (pending, fulfilled, rejected).

#### When to Use

- Complex async flows not suited for RTK Query
- Operations that need access to state during async flow
- Chained async operations
- Legacy code migration

#### When NOT to Use

- Standard API calls (prefer RTK Query)
- Simple sync state updates (use createSlice actions)

For async thunk creation and handling lifecycle actions, see [examples/async-thunks.md](examples/async-thunks.md).

---

### Pattern 7: Selectors and Memoization

Create reusable selectors for derived state. Use `createSelector` from Reselect for memoized computed values.

For selector patterns and memoization, see [examples/selectors.md](examples/selectors.md).

---

### Pattern 8: Middleware Patterns

Add custom middleware for logging, analytics, or side effects. Use the middleware callback to extend default middleware.

For middleware configuration and custom middleware, see [examples/middleware.md](examples/middleware.md).

</patterns>

---

<integration>

## Integration Guide

**TypeScript Integration:**

- Infer types from store using `ReturnType` and `typeof`
- Use `PayloadAction<T>` for all action payloads
- Define typed hooks with `.withTypes()` method
- Use `createAppAsyncThunk` for pre-typed async thunks

**DevTools Integration:**

- `configureStore` enables DevTools automatically in development
- Time-travel debugging available out of the box
- Action history and state diff visualization
- Custom DevTools options available via `devTools` config

**Testing Integration:**

- Test slices by importing reducer and calling with actions
- Mock async operations at the network level (not thunk level)
- Use `configureStore` with preloaded state for component tests

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use `configureStore` for store setup - NEVER legacy `createStore`)**

**(You MUST use `createSlice` for all reducers - NEVER switch statements or manual action creators)**

**(You MUST define typed hooks (`useAppSelector`, `useAppDispatch`) once in a hooks file)**

**(You MUST use named exports ONLY - NO default exports in any Redux files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

**Failure to follow these rules will cause type safety issues, unnecessary boilerplate, and convention violations.**

</critical_reminders>
