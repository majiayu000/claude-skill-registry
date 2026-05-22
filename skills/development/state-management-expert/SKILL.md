---
name: state-management-expert
description: Expert-level state management with Redux Toolkit and Zustand using TypeScript. Handle complex application state including shopping carts, user authentication, product catalogs, API state management, and advanced patterns. Generate production-ready store configurations, slices, hooks, and complete implementations across React, Next.js, and universal applications. Use when building scalable state management solutions with TypeScript for e-commerce, authentication, async operations, and complex state architectures.
---

# State Management Expert

## Overview

You are an expert state management specialist proficient in both Redux Toolkit and Zustand with TypeScript. This skill covers comprehensive state management patterns for production applications including shopping carts, user data, authentication, API integration, and complex state orchestration across React, Next.js, and universal JavaScript environments.

## Core Capabilities

### 1. Redux Toolkit Architecture (TypeScript)

Build sophisticated Redux applications with modern best practices, hooks, and async handling.

**Key patterns:**
- Slices with `createSlice` for reducers, actions, and selectors
- `createAsyncThunk` for API calls with loading/error states
- `RTK Query` for server state management
- Proper TypeScript typing for state, actions, and selectors
- Performance optimization with `reselect` for memoization
- Middleware customization and async logic

**Store configuration structure:**
```typescript
// store/index.ts
import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import cartReducer from './slices/cartSlice';
import userReducer from './slices/userSlice';
import { api } from './api/api';

export const store = configureStore({
  reducer: {
    cart: cartReducer,
    user: userReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
```

### 2. Zustand Architecture (TypeScript)

Build lightweight, reactive stores with minimal boilerplate and excellent TypeScript support.

**Key patterns:**
- Custom hooks with `create` for store definition
- Proper type inference and generic typing
- Async operations with async/await
- Middleware for persistence, devtools, and logging
- Selectors for computed state
- Immer integration for immutable updates

**Store structure:**
```typescript
// store/cartStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  quantity: number;
  price: number;
}

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  getTotalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    immer((set, get) => ({
      items: [],
      addItem: (item) => {
        set((state) => {
          state.items.push(item);
        });
      },
      removeItem: (id) => {
        set((state) => {
          state.items = state.items.filter((item) => item.id !== id);
        });
      },
      getTotalPrice: () => {
        return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },
    })),
    {
      name: 'cart-storage',
    }
  )
);
```

### 3. Shopping Cart Management

Implement complete cart functionality with both libraries.

**Features:**
- Add/remove items with quantity management
- Price calculations and tax handling
- Persistence to localStorage
- Cart synchronization across tabs
- Inventory tracking and validation
- Discount and coupon application
- Cart serialization/deserialization

### 4. User Authentication & Data Management

Handle user state, authentication, and profile data.

**Includes:**
- Login/logout flows
- JWT token management
- User profile data
- Role-based access control (RBAC)
- Permission management
- Session persistence
- Auth state synchronization

### 5. API State Management

Handle server data, loading states, caching, and error management.

**Patterns covered:**
- `createAsyncThunk` for Redux async operations
- `RTK Query` for cache management
- Zustand with async/await for API calls
- Loading, error, and success states
- Request cancellation
- Cache invalidation strategies
- Optimistic updates

### 6. Advanced State Patterns

Complex patterns for expert developers.

**Topics covered:**
- Normalized state shape
- Entity adapters (Redux)
- Selector composition and memoization
- Derived state calculation
- State normalization strategies
- Time-travel debugging
- DevTools integration
- Middleware patterns
- Plugin systems
- Multi-store coordination

### 7. TypeScript Advanced Typing

Production-grade TypeScript patterns.

**Covers:**
- Generic type inference
- Discriminated unions for action types
- Type-safe selectors
- Type-safe action creators
- Const assertion patterns
- Template literal types
- Conditional types for state shape
- Type narrowing in reducers

### 8. Framework Integration

Seamless integration across environments.

**Environments:**
- **React**: Hooks API, context integration, concurrent features
- **Next.js**: Server/Client components, SSR/SSG, API routes
- **React Native**: Async storage, navigation state
- **Electron**: Persistent state, IPC communication
- **Universal**: Shared state across platforms

## Use Case Implementations

### Shopping Cart E-commerce
Complete shopping cart with:
- Product catalog management
- Cart operations (add, remove, update quantity)
- Price calculations with tax/shipping
- Discount/coupon handling
- Order persistence
- Multi-store synchronization
- Inventory validation

### User Authentication System
Full auth implementation with:
- Login/signup flows
- Token management
- User profile state
- Logout and session cleanup
- Refresh token handling
- Role-based redirects
- Protected routes

### Product Catalog System
Product management including:
- Product filtering and sorting
- Search functionality
- Pagination and lazy loading
- Wishlist management
- Product reviews and ratings
- Stock/inventory tracking

### API State Management
Server state handling with:
- Data fetching with loading states
- Error handling and retry logic
- Cache management
- Optimistic updates
- Request deduplication
- Background refetching

## Redux Toolkit vs Zustand Decision Matrix

See `references/comparison.md` for detailed analysis of:
- When to use Redux Toolkit
- When to use Zustand
- Trade-offs and considerations
- Migration paths between libraries
- Performance characteristics
- Learning curve comparison

## Implementation Examples

See `references/redux-patterns.md` for:
- Complete Redux Toolkit examples with TypeScript
- RTK Query setup and usage
- Async thunk patterns
- Selector patterns with reselect
- Testing strategies

See `references/zustand-patterns.md` for:
- Complete Zustand examples with TypeScript
- Middleware integration
- Async store patterns
- Selector composition
- Testing approaches

## Testing State Management

See `references/testing-guide.md` for:
- Unit testing Redux slices
- Testing Redux components
- Unit testing Zustand stores
- Integration testing
- Mock store setup
- Snapshot testing best practices

## Performance Optimization

**Redux:**
- Normalized state shape
- Selector memoization with `reselect`
- React hooks optimization
- Subscription optimization
- Middleware performance

**Zustand:**
- Shallow equality checks
- Selector memoization
- Computed state caching
- Render optimization
- Store subscription patterns

## Advanced Topics

### Middleware & Plugins
- Redux middleware creation
- Zustand middleware composition
- Logger middleware
- Persistence middleware
- Devtools integration
- Custom middleware patterns

### State Synchronization
- Cross-tab communication
- Service worker integration
- WebSocket state sync
- Offline-first patterns
- Conflict resolution

### Performance & Scalability
- Large state trees
- Dynamic store creation
- Code splitting with state
- Memory management
- DevTools optimization

## TypeScript Configuration

All implementations use strict TypeScript with:
- `strict: true` in tsconfig.json
- Full type inference
- No implicit `any`
- Proper generics usage
- Type-safe action creators
- Type-safe selectors

## When to Use This Skill

✅ Building state management with Redux Toolkit or Zustand
✅ Implementing shopping carts, user auth, API state
✅ Creating TypeScript-first state management
✅ Optimizing complex state architectures
✅ Integrating state across React, Next.js, React Native
✅ Teaching advanced state management patterns
✅ Migrating between state management solutions
✅ Performance optimization of state management

❌ Simple component state (use useState)
❌ Non-TypeScript projects
❌ Context API for simple sharing (unnecessary complexity)
❌ Learning state management basics (intermediate resources needed)

## Resources

### references/
- **comparison.md** - Redux vs Zustand detailed comparison
- **redux-patterns.md** - Complete Redux Toolkit examples with TypeScript
- **zustand-patterns.md** - Complete Zustand examples with TypeScript
- **testing-guide.md** - Testing patterns for both libraries
- **performance-guide.md** - Optimization techniques and best practices

### assets/
- **redux-templates/** - TypeScript Redux boilerplate templates
- **zustand-templates/** - TypeScript Zustand boilerplate templates
- **store-examples/** - Complete store implementations
- **type-definitions/** - Reusable TypeScript type definitions

All resources are loaded as needed during development.