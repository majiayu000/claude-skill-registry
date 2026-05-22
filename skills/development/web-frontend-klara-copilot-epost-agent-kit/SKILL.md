---
name: web-frontend
description: (ePost) Use when working with .tsx/.jsx files, React components, hooks, state management, or frontend UI
user-invocable: false

metadata:
  agent-affinity: [epost-fullstack-developer, epost-tester, epost-debugger, epost-code-reviewer]
  keywords: [react, frontend, ui, hooks, components, state, typescript, redux]
  platforms: [web]
  triggers: [".tsx", ".jsx", "react", "frontend", "ui component", "redux", "hook"]
---

# Frontend Development — React/Redux Patterns

## Purpose

React 18 + TypeScript frontend patterns. Covers Redux Toolkit (dual-store), session management, component composition, hooks, and render optimization.

## State Management — Redux Toolkit

Uses **two Redux stores**:

### Global Store (persisted, app-wide)

**Location**: `libs/utils/src/redux/store.ts`

```typescript
import { configureStore } from '@reduxjs/toolkit';
import { persistReducer, persistStore } from 'redux-persist';

const rootReducer = combineReducers({
  selectedItemReducer: itemSlice,
  fileReducer: uploadSlice,
  userPreferencesReducer: userPreferencesSlice,
  // Add your app-wide reducers here
});

export const store = configureStore({
  reducer: persistReducer(persistConfig, rootReducer),
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({ serializableCheck: false }),
});

export type RootState = ReturnType<typeof store.getState>;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

Mounted via `ReduxProvider` (with `PersistGate`) in root locale layout.

### Feature Store (scoped, RTK Query)

**Location**: `app/[locale]/(auth)/feature-name/_stores/feature-store.tsx`

Own `configureStore` + `Provider`, scoped to the feature layout:

```typescript
export const store = configureStore({
  reducer: {
    listReducer, filterReducer, selectionReducer,
    [featureApi.reducerPath]: featureApi.reducer,
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({ serializableCheck: false })
      .concat(featureApi.middleware),
});
```

### Slice Template

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

const initialState = { selectedItem: { id: '', name: '' } };

export const selectedItem = createSlice({
  name: 'selectedItem',
  initialState,
  reducers: {
    removeItem: () => initialState,
    setItem: (state, action: PayloadAction<{ id: string; name: string }>) => ({
      selectedItem: action.payload,
    }),
  },
});

export const { removeItem, setItem } = selectedItem.actions;
export default selectedItem.reducer;
```

### Selector Best Practices

See `references/render-optimization.md` for selector patterns and memoization.

## Provider Nesting Order

See `web-auth` skill for provider nesting order.

## Component Patterns

### forwardRef + displayName

```typescript
'use client';
import { forwardRef, Ref, useImperativeHandle } from 'react';

const SearchField = forwardRef((props: ISearchFieldProps, ref: Ref<ICustomSearchFieldRef>) => {
  useImperativeHandle(ref, () => ({
    setValue: setSearchValue,
    focus: () => inputRef.current?.focus(),
  }));
  return <TextField {...textFieldProps} />;
});
SearchField.displayName = 'SearchField';  // Always set for DevTools
```

### Compound Components (klara-theme pattern)

See `references/composition.md` for compound component patterns.

### Explicit Variants (not boolean props)

See `references/composition.md` for explicit variant patterns.

## Hook Patterns

### Utility Hook (no React state)

```typescript
export const useSessionData = () => {
  const getSessionFields = (session: ExtendedSession | null) => ({
    isAuthenticated: !!session?.accessToken,
    organizationId: session?.organizationId ?? '',
    roles: session?.roles ?? [],
  });
  return { getSessionFields };
};
```

### Hook with Effect + Cleanup

```typescript
export const useWebSocketMembers = (socket: WebSocket, channelId: string) => {
  const [members, setMembers] = useState<Member[]>([]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => { /* update members */ };
    socket.addEventListener('message', handleMessage);
    return () => socket.removeEventListener('message', handleMessage);
  }, [socket, channelId]);

  return { members };
};
```

### Context Hook with Guard

```typescript
const SelectedRoom = createContext<Room | null>(null);
export const SelectedRoomProvider = SelectedRoom.Provider;

export function useSelectedRoom(): Room {
  const room = useContext(SelectedRoom);
  if (!room) throw new Error('Room not found!');
  return room;
}
```

## Build Commands

```bash
npm run dev          # Development server
npm run build        # Production build
npm run lint         # ESLint
npx tsc --noEmit     # Type check
npm test             # Unit tests (Jest + RTL)
npx playwright test  # E2E tests
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/composition.md` | Compound components, state decoupling, children composition |
| `references/render-optimization.md` | React.memo, derived state, transitions, lazy init |

## Sub-Skill Routing

When this skill is active and user intent matches a sub-skill, delegate:

| Intent | Sub-Skill | When |
|--------|-----------|------|
| Next.js patterns | `web-nextjs` | App Router, Server Components, RSC |
| API routes | `web-api-routes` | API endpoints, server actions |
| Module integration | `web-modules` | B2B module patterns |
| Prototyping | `web-prototype` | `/convert`, rapid prototype |
| RAG search | `web-rag` | Vector search web codebase |
| i18n | `web-i18n` | Translations, locale routing |
| Auth | `web-auth` | Session, OAuth, feature flags |
| Testing | `web-testing` | Jest, Playwright, coverage |

## Rules

- Use Redux Toolkit for state — NOT Zustand, NOT React Query
- Use `useAppSelector` with narrow selectors — subscribe to booleans, not objects
- Always set `displayName` on `forwardRef` components
- Use explicit variant props (via `cva()`), not boolean props
- Keep components under 200 lines
- Mobile-first responsive design with Tailwind
- WCAG AA accessibility
- React 18 only — do NOT use React 19 features (`use()`, `<Activity>`, no-forwardRef)

## Dependencies

- React 18+
- TypeScript
- Redux Toolkit + redux-persist
- React Testing Library
- Tailwind CSS (styling)
- klara-theme (UI components)
