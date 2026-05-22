---
name: expo-router
description: Expo Router 6.x file-based routing for React Native. Use when setting up navigation, creating screens, handling route params, or structuring app layouts with Stack/Tabs navigators.
---

# Expo Router

## Overview

File-based routing for React Native using Expo Router 6.x. Maps file system structure in the `app/` directory to navigation screens. Supports Stack and Tab navigators, route groups, dynamic parameters, and nested layouts.

**Install**: Included with Expo SDK 54+. Ensure `expo-router` is in dependencies.

## Workflows

**Setting up routing:**
1. [ ] Create `app/_layout.tsx` as root layout (providers, global chrome)
2. [ ] Create route group directories: `app/(demo)/`, `app/(auth)/`
3. [ ] Add `_layout.tsx` in each group for group-specific navigation
4. [ ] Add `index.tsx` for default screens
5. [ ] Add `[param].tsx` for dynamic routes
6. [ ] Add `+not-found.tsx` for 404 handling

**Adding a new screen:**
1. [ ] Create file in appropriate route group
2. [ ] Export default React component
3. [ ] Configure screen options in parent `_layout.tsx` or via `<Stack.Screen options={...} />`
4. [ ] Navigate using `useRouter()` or `<Link>`

## Guidance

### File Conventions

| File | Purpose |
|------|---------|
| `_layout.tsx` | Layout wrapper for directory (providers, navigators) |
| `index.tsx` | Default screen for directory |
| `[param].tsx` | Dynamic route segment |
| `[...catchAll].tsx` | Catch-all route |
| `+not-found.tsx` | 404 screen |
| `(group)/` | Route group (no URL segment) |

### Root Layout Pattern

The root `_layout.tsx` is the entry point. Use it for global providers:

```
app/_layout.tsx → GestureHandlerRootView > SafeAreaProvider > Context > Stack
```

Keep the root layout thin — push chrome (tabs, headers) into group layouts.

### Route Groups

Route groups `(name)/` organize screens without affecting the URL path. Common pattern:

```
app/
├── _layout.tsx          # Root: providers + Stack
├── (demo)/
│   ├── _layout.tsx      # Tabs or Stack for demo scenes
│   ├── index.tsx        # Home screen
│   └── [id].tsx         # Detail screen
└── +not-found.tsx
```

### Navigation

- **Programmatic**: `const router = useRouter()` → `router.push('/detail/123')`, `router.back()`
- **Declarative**: `<Link href="/detail/123">` component
- **Params**: `const { id } = useLocalSearchParams<{ id: string }>()`
- **Redirect**: `<Redirect href="/login" />` for conditional routing

### Screen Options

Configure screen presentation via layout or inline:

- In layout: `<Stack.Screen name="detail" options={{ title: 'Detail', headerShown: false }} />`
- Inline: `<Stack.Screen options={{ presentation: 'modal' }} />`
- Common options: `title`, `headerShown`, `presentation` ('card' | 'modal'), `animation`

### Layout Nesting

Nest providers in root, chrome in groups:

- Root `_layout.tsx`: `GestureHandlerRootView`, `SafeAreaProvider`, theme context, `<Stack />`
- Group `_layout.tsx`: `<Tabs />` or `<Stack />` with screen options, header configuration

## Best Practices

- Keep route files thin — delegate to view components in `/components/views/`
- Use route groups to separate concerns without affecting URLs
- Type route params with generics: `useLocalSearchParams<{ id: string }>()`
- Set `headerShown: false` when providing custom headers
- Use `<Stack screenOptions={{ animation: 'slide_from_right' }} />` for consistent transitions
- Place shared providers (theme, data context) in root `_layout.tsx`
- Use `+not-found.tsx` for graceful 404 handling

## Anti-Patterns

- Placing business logic in route files (keep them thin, delegate to components)
- Deeply nesting route groups beyond 2 levels
- Using React Navigation directly instead of Expo Router abstractions
- Hardcoding navigation paths as strings without a constants file for complex apps
- Forgetting to export default from route files (causes blank screens)
- Putting providers in group layouts when they should be in root layout
