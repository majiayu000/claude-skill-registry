---
name: expo-router
description: >
  Expo Router file-based routing for Universal React Native applications.
  Trigger: When working with Expo Router navigation, file-based routes, layouts, tabs, modals, typed routes, or understanding how routing works in Liftera mobile app.
license: Apache-2.0
metadata:
  author: liftera
  version: "1.0"
  scope: [root, mobile]
  auto_invoke: "Working with Expo Router navigation"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## What is Expo Router?

Expo Router is a **file-based router** for Universal React Native applications. It brings the best file-system routing concepts from the web to native applications, allowing your routing to work seamlessly across Android, iOS, and web platforms.

### Core Principles

1. **File-based routing**: When a file is added to the `app/` directory, it automatically becomes a route
2. **Universal**: Same navigation structure works on Android, iOS, and web
3. **Built on React Navigation**: Provides native platform-optimized navigation
4. **Deep linkable**: Every screen is automatically shareable with URLs
5. **Offline-first**: Routes are cached and run without network connection
6. **Type-safe**: Full TypeScript support with auto-generated typed routes

---

## File Notation System

Expo Router uses special file naming conventions to define routing behavior:

### 1. Static Routes (No Notation)

```
app/
├── home.tsx        # /home
├── feed/
│   └── favorites.tsx  # /feed/favorites
```

Regular file and directory names create **static routes**. The URL matches exactly as it appears in the file tree.

### 2. Dynamic Routes (Square Brackets)

```
app/
├── [userName].tsx           # /evanbacon, /expo, etc.
├── products/
│   └── [productId]/
│       └── index.tsx        # /products/123
```

Square brackets `[param]` create **dynamic segments**. The parameter is accessible via `useLocalSearchParams()` hook:

```typescript
// app/[userName].tsx
import { useLocalSearchParams } from "expo-router";

export default function UserProfile() {
  const { userName } = useLocalSearchParams<{ userName: string }>();
  // userName = "evanbacon" when visiting /evanbacon
}
```

### 3. Route Groups (Parentheses)

```
app/
├── (tabs)/
│   ├── index.tsx      # / (not /tabs)
│   └── settings.tsx   # /settings (not /tabs/settings)
├── (auth)/
│   ├── login.tsx      # /login (not /auth/login)
│   └── signup.tsx     # /signup
```

Parentheses `(group)` create **route groups** that organize files without affecting the URL structure. Critical for:

- Organizing related routes
- Sharing layouts between routes
- Creating multiple navigation contexts (tabs, stacks)

### 4. Index Routes

```
app/
├── index.tsx           # / (root)
├── profile/
│   └── index.tsx       # /profile
```

`index.tsx` files define the **default route** for a directory. Like `index.html` on the web.

### 5. Layout Routes (\_layout.tsx)

```
app/
├── _layout.tsx         # Root layout (wraps everything)
├── (tabs)/
│   ├── _layout.tsx     # Tab navigator layout
│   └── index.tsx
```

`_layout.tsx` files are **not routes themselves** but define how routes inside their directory relate to each other:

- Define navigation structure (Stack, Tabs, Drawer)
- Wrap child routes with providers
- Configure screen options
- Rendered **before** child routes

**Critical**: The root `app/_layout.tsx` is where initialization code goes (previously in `App.jsx`).

### 6. Special Routes (Plus Sign)

```
app/
├── +not-found.tsx      # 404 handler
├── +html.tsx           # Web HTML customization
├── +native-intent.tsx  # Deep link handler
├── +middleware.ts      # Request middleware
```

Routes with `+` prefix have special meaning:

- `+not-found`: Catches unmatched routes (404)
- `+html`: Customizes HTML boilerplate on web
- `+native-intent`: Handles third-party deep links
- `+middleware`: Runs code before route renders

---

## Navigation Structures

### Stack Navigator

A **stack** is the foundational navigation pattern. Routes animate on top of each other:

- **Android**: Slides up from bottom
- **iOS**: Slides in from right
- **Web**: Browser-like navigation

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="details" options={{ title: 'Details' }} />
      <Stack.Screen
        name="modal"
        options={{ presentation: 'modal' }}
      />
    </Stack>
  );
}
```

**How it works**: Each `<Stack.Screen>` corresponds to a file in the same directory. The `name` prop matches the filename (without extension).

### Tab Navigator

**Tabs** create a persistent bottom navigation bar (iOS/Android) or top tabs:

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: 'blue' }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <HomeIcon color={color} />
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <UserIcon color={color} />
        }}
      />
    </Tabs>
  );
}
```

**File structure**:

```
app/
├── _layout.tsx          # Root stack
└── (tabs)/              # Route group (no URL segment)
    ├── _layout.tsx      # Tab navigator
    ├── index.tsx        # First tab (/)
    └── profile.tsx      # Second tab (/profile)
```

**Why route groups?** The `(tabs)` group prevents `/tabs/profile` and creates clean URLs like `/profile`.

### Nested Navigation

Layouts can be nested to create complex navigation hierarchies:

```
app/
├── _layout.tsx              # Root Stack
└── (tabs)/                  # Route group
    ├── _layout.tsx          # Tabs (Home, Feed, Profile)
    ├── index.tsx            # Home tab
    ├── feed/
    │   ├── _layout.tsx      # Stack inside Feed tab
    │   ├── index.tsx        # Feed list
    │   └── [id].tsx         # Feed detail (pushed on stack)
    └── profile.tsx          # Profile tab
```

**Navigation flow**:

1. Root layout renders Tabs
2. Tabs render Home/Feed/Profile
3. Feed tab has its own Stack for list → detail navigation

---

## Navigation APIs

### Imperative Navigation

```typescript
import { router } from "expo-router";

// Push new route on stack
router.push("/profile");
router.push({ pathname: "/user/[id]", params: { id: "123" } });

// Replace current route (no back button)
router.replace("/login");

// Go back
router.back();

// Navigate to specific route in stack
router.navigate("/settings");

// Dismiss modal/stack
router.dismiss();
router.dismissAll();
```

### Declarative Navigation

```typescript
import { Link } from 'expo-router';

// Static route
<Link href="/profile">Go to Profile</Link>

// Dynamic route
<Link href={{ pathname: '/user/[id]', params: { id: userId } }}>
  View User
</Link>

// Replace instead of push
<Link href="/login" replace>Login</Link>
```

### Navigation State Hooks

```typescript
import { usePathname, useSegments, useLocalSearchParams } from "expo-router";

// Current path
const pathname = usePathname(); // "/feed/123"

// Path segments
const segments = useSegments(); // ["feed", "123"]

// Route parameters
const { id } = useLocalSearchParams<{ id: string }>();
```

---

## Typed Routes (Liftera Enabled)

Liftera has `experiments.typedRoutes: true` in `app.json`, enabling **compile-time route validation**.

### How It Works

1. Expo CLI scans `app/` directory
2. Generates `.expo/types/router.d.ts` with all valid routes
3. TypeScript validates `href` props at compile time

### Type-Safe Navigation

```typescript
import { router, Link } from 'expo-router';

// ✅ Valid routes - TypeScript happy
<Link href="/profile" />
<Link href="/feed/favorites" />
<Link href={{ pathname: '/user/[id]', params: { id: '123' } }} />

// ❌ TypeScript errors - route doesn't exist
<Link href="/profle" />  // Typo caught at compile time
<Link href="/invalid" />

// ❌ TypeScript errors - missing required params
<Link href="/user/[id]" />  // Must use object form with params

// ❌ TypeScript errors - invalid params
<Link href={{ pathname: '/user/[id]', params: { userId: '123' } }} />
// Param name must be 'id', not 'userId'
```

### Benefits

- **Catch typos** before runtime
- **Autocomplete** for all routes
- **Refactor safely** - rename files, TypeScript finds all usages
- **Parameter validation** - ensure correct param names

---

## Modals

Modals are **routes presented differently**, not separate components.

```typescript
// app/_layout.tsx
<Stack>
  <Stack.Screen name="index" />
  <Stack.Screen
    name="modal"
    options={{
      presentation: 'modal',      // Modal presentation
      headerShown: false,
      animation: 'slide_from_bottom'
    }}
  />
</Stack>
```

**Navigate to modal**:

```typescript
router.push("/modal"); // Presents as modal
router.back(); // Dismisses modal
```

**Deep linking**: Modals work with deep links. Opening `myapp://modal` presents the modal correctly.

---

## Deep Linking & Universal Links

Every route is automatically deep linkable:

```json
// app.json
{
  "expo": {
    "scheme": "liftera"
  }
}
```

**URL mapping**:

- `liftera://` → `/` (index)
- `liftera://profile` → `/profile`
- `liftera://user/123` → `/user/[id]` with `id: "123"`

**Web URLs** (when deployed):

- `https://liftera.app/` → `/`
- `https://liftera.app/profile` → `/profile`

**Same code, all platforms** - no platform-specific linking logic needed.

---

## Critical Patterns

### Protected Routes

```typescript
// app/_layout.tsx
import { useAuth } from '@/hooks/useAuth';
import { Redirect, Slot } from 'expo-router';

export default function RootLayout() {
  const { user, loading } = useAuth();

  if (loading) return <LoadingScreen />;
  if (!user) return <Redirect href="/login" />;

  return <Slot />;
}
```

**How it works**: Root layout checks auth state. Unauthenticated users are redirected before any child routes render.

### Shared Layouts

```typescript
// app/(app)/_layout.tsx - Authenticated app
<Stack>
  <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
</Stack>

// app/(auth)/_layout.tsx - Auth flow
<Stack screenOptions={{ headerShown: false }}>
  <Stack.Screen name="login" />
  <Stack.Screen name="signup" />
</Stack>
```

Route groups let you define different layout contexts for different parts of your app.

### Error Boundaries

```typescript
// app/_layout.tsx
export { ErrorBoundary } from 'expo-router';

// Or custom
export function ErrorBoundary({ error, retry }: ErrorBoundaryProps) {
  return (
    <View>
      <Text>Error: {error.message}</Text>
      <Button onPress={retry}>Try Again</Button>
    </View>
  );
}
```

**Automatic error handling**: Errors in routes are caught and displayed without crashing the app.

---

## Critical Rules

### File Naming

- **ALWAYS** use `.tsx` extension for TypeScript routes
- **NEVER** use `.js` - Liftera is TypeScript-first
- **ALWAYS** use lowercase for route files (convention)

### Layouts

- **ALWAYS** define `_layout.tsx` when using Stack/Tabs
- **NEVER** skip root `app/_layout.tsx` - it's required
- **ALWAYS** render `<Slot />` in layouts without navigators

### Navigation

- **ALWAYS** use typed routes with `useLocalSearchParams<T>()`
- **NEVER** hardcode route strings - let TypeScript validate
- **ALWAYS** use object form for dynamic routes with params
- **NEVER** import React Navigation directly - use Expo Router APIs

### Route Groups

- **ALWAYS** use `(group)` for organizing without URL impact
- **NEVER** nest route groups unnecessarily
- **ALWAYS** use route groups for tabs/auth flows

---

## Resources

- **Expo Router Docs**: https://docs.expo.dev/router/introduction/
- **File Notation**: https://docs.expo.dev/router/basics/notation/
- **Typed Routes**: https://docs.expo.dev/router/reference/typed-routes/
- **Stack Navigator**: https://docs.expo.dev/router/advanced/stack/
- **Tabs Navigator**: https://docs.expo.dev/router/advanced/tabs/
- **Modals**: https://docs.expo.dev/router/advanced/modals/
