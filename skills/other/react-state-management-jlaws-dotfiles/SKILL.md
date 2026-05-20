---
name: react-state-management
description: Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions.
---

# React State Management

## Selection Criteria

| Type | Solutions |
|------|-----------|
| **Local State** | useState, useReducer |
| **Global State** | Redux Toolkit, Zustand, Jotai |
| **Server State** | React Query, SWR, RTK Query |
| **URL State** | React Router, nuqs |
| **Form State** | React Hook Form, Formik |

```
Small app, simple state       -> Zustand or Jotai
Large app, complex state      -> Redux Toolkit
Heavy server interaction      -> React Query + light client state
Atomic/granular updates       -> Jotai
```

## Zustand

Create stores with `create<State>()`. Wrap with `devtools()` and `persist()` middleware. Use slice pattern with `StateCreator` for scalable stores. Select specific state to prevent re-renders: `useStore(s => s.user)`.

### Zustand Advanced

Stack middleware: `devtools(subscribeWithSelector(persist(immer(...))))`. Use `partialize` for partial persistence, `subscribeWithSelector` for external subscriptions. Test via `useStore.getState()`.

## Redux Toolkit

Use `configureStore` + `createSlice`. Type `RootState` and `AppDispatch` from store. Use `createAsyncThunk` for async operations with `pending/fulfilled/rejected` matchers.

## Jotai

Use `atom()` for base state, `atom(get => ...)` for derived, `atomWithStorage` for persistence. Write-only action atoms: `atom(null, (get, set) => ...)`.

## React Query

Use query key factories for cache organization. `useMutation` with `onMutate` for optimistic updates: cancel queries, snapshot previous, set optimistic data, rollback `onError`, invalidate `onSettled`.

## Combining Client + Server State

Zustand for UI state (sidebar, modal), React Query for server state. Never duplicate server data in client stores.

## Cross-References

- **frontend:nextjs-app-router-patterns** -- server/client state boundary, React Server Components context
- **frontend:form-patterns** -- form state management, React Hook Form integration
- **frontend:i18n-and-localization** -- locale state management, context providers
