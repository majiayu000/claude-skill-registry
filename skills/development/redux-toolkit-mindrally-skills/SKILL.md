---
name: redux-toolkit
description: Comprehensive Redux Toolkit best practices for React and Next.js applications with TypeScript.
---

# Redux Toolkit

You are an expert in Redux Toolkit for state management in React and Next.js applications.

## Development Philosophy

- Write clean, maintainable, and scalable code
- Adhere to SOLID principles
- Favor functional and declarative programming patterns
- Emphasize type safety and component-driven approaches

## Redux State Management

### Core Principles
- Implement Redux Toolkit for global state management
- Use createSlice to define state, reducers, and actions together
- Normalize state structure to prevent deeply nested data
- Employ selectors to encapsulate state access
- Separate concerns by feature; avoid monolithic slices

### Slice Structure
```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface CounterState {
  value: number
  isLoading: boolean
}

const initialState: CounterState = {
  value: 0,
  isLoading: false,
}

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },
  },
})

export const { increment, setLoading } = counterSlice.actions
export default counterSlice.reducer
```

## Naming Conventions

- **PascalCase**: Components, type definitions, interfaces
- **kebab-case**: Directory and file names
- **camelCase**: Variables, functions, methods, hooks, properties
- **UPPERCASE**: Environment variables, constants

### Prefixes
- Event handlers: `handle` (e.g., `handleClick`)
- Boolean variables: verbs (e.g., `isLoading`, `hasError`)
- Custom hooks: `use` (e.g., `useAuth`)

## TypeScript Integration

- Enable strict mode
- Define clear interfaces for props and Redux state structure
- Apply generics where type flexibility is needed
- Prefer interfaces over types for object structures
- Use typed hooks (`useAppDispatch`, `useAppSelector`)

## Async Operations

### RTK Query
- Use RTK Query for data fetching and caching
- Define API slices with endpoints
- Leverage automatic cache invalidation
- Implement optimistic updates when appropriate

### createAsyncThunk
```typescript
export const fetchUser = createAsyncThunk(
  'user/fetch',
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await api.getUser(userId)
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)
```

## Performance Optimization

- Use React.memo() strategically
- Implement useCallback for memoized functions
- Apply useMemo for expensive computations
- Avoid inline function definitions in JSX
- Use dynamic imports for code splitting
- Employ proper keys in lists (avoid index-based keys)

## Selectors

- Create memoized selectors with createSelector
- Encapsulate state shape in selectors
- Compose selectors for derived data
- Avoid computing in components

## Error Handling

- Implement error boundaries with external logging
- Use Zod for validation
- Handle async errors in thunks
- Provide user-friendly error messages

## Testing

- Apply Jest and React Testing Library
- Follow Arrange-Act-Assert patterns
- Mock external dependencies
- Test reducers, selectors, and thunks independently
