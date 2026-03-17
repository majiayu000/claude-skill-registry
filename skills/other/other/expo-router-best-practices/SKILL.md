---
name: expo-router-best-practices
description: This skill should be used when creating new routes, configuring navigation layouts, implementing deep linking, or organizing the app/ directory structure in Expo Router projects. It provides best practices for file-based routing patterns.
---

# Expo Router Best Practices

This skill provides guidance for implementing file-based routing with Expo Router following established best practices and official documentation patterns.

## Core Principles

### 1. Routes Are Thin Wrappers

Route files in the `app/` directory should be minimal pass-throughs to feature screen components. Business logic and complex UI components belong in feature directories, not route files.

```typescript
// app/players/[playerId]/compare.tsx - CORRECT
import { Main } from "@/features/compare-players/screens/Main";

/**
 * Compare players route.
 * URL: /players/[playerId]/compare
 */
export default function CompareScreen() {
  return <Main />;
}
```

```typescript
// app/players/[playerId]/compare.tsx - INCORRECT
export default function CompareScreen() {
  const { playerId } = useLocalSearchParams();
  const [data, setData] = useState(null);
  // ... 200 lines of business logic
  return <ComplexUI />;
}
```

### 2. Descriptive Component Names

Use descriptive names for route components, not generic names.

```typescript
// CORRECT
export default function CompareScreen() { ... }
export default function PlayerDetailScreen() { ... }
export default function SettingsScreen() { ... }

// INCORRECT
export default function Screen() { ... }
export default function Page() { ... }
export default function Index() { ... }  // only acceptable for index.tsx files
```

### 3. Document Route URLs in JSDoc

Include the URL pattern in route file documentation.

```typescript
/**
 * Player detail route.
 * URL: /players/[playerId]
 */
export default function PlayerDetailScreen() {
  return <Main />;
}
```

## File Structure Patterns

### Directory Organization

```
app/
├── _layout.tsx              # Root layout (initialization, providers)
├── index.tsx                # Default route (/)
├── +not-found.tsx           # 404 handling
├── +html.tsx                # Web HTML customization (optional)
├── (tabs)/                  # Tab navigator group
│   ├── _layout.tsx          # Tab configuration
│   ├── index.tsx            # Default tab
│   ├── feed/                # Stack within tab
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   └── [postId].tsx
│   └── settings.tsx
├── (auth)/                  # Auth screens group
│   ├── sign-in.tsx
│   └── create-account.tsx
└── modal.tsx                # Modal route
```

### Route Notation Reference

| Notation         | Purpose                     | Example              | URL      |
| ---------------- | --------------------------- | -------------------- | -------- |
| `file.tsx`       | Static route                | `about.tsx`          | `/about` |
| `[param].tsx`    | Dynamic route               | `[userId].tsx`       | `/123`   |
| `[...slug].tsx`  | Catch-all route             | `[...path].tsx`      | `/a/b/c` |
| `(group)/`       | Route group (no URL impact) | `(tabs)/`            | `/`      |
| `index.tsx`      | Default route               | `feed/index.tsx`     | `/feed`  |
| `_layout.tsx`    | Layout definition           | `(tabs)/_layout.tsx` | -        |
| `+not-found.tsx` | 404 handler                 | `+not-found.tsx`     | -        |

## Layout Patterns

### Root Layout

The root `_layout.tsx` replaces `App.jsx/tsx`. Place initialization code here.

```typescript
// app/_layout.tsx
import { useFonts } from "expo-font";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded] = useFonts({
    SpaceMono: require("../assets/fonts/SpaceMono-Regular.ttf"),
  });

  useEffect(() => {
    if (loaded) {
      SplashScreen.hide();
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return <Stack />;
}
```

### Stack Layout

```typescript
// app/products/_layout.tsx
import { Stack } from "expo-router";

export const unstable_settings = {
  initialRouteName: "index",
};

export default function ProductsLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Products" }} />
      <Stack.Screen name="[productId]" options={{ headerShown: false }} />
    </Stack>
  );
}
```

### Tab Layout

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from "expo-router";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ headerShown: false }}>
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color }) => (
            <MaterialIcons size={28} name="home" color={color} />
          ),
        }}
      />
      <Tabs.Screen name="feed" options={{ title: "Feed" }} />
      <Tabs.Screen name="settings" options={{ title: "Settings" }} />
    </Tabs>
  );
}
```

### Protected Routes (SDK 53+)

```typescript
// app/_layout.tsx
import { Stack } from "expo-router";
import { useAuthState } from "@/hooks/useAuthState";

export default function RootLayout() {
  const { isLoggedIn } = useAuthState();

  return (
    <Stack>
      <Stack.Protected guard={isLoggedIn}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="modal" options={{ presentation: "modal" }} />
      </Stack.Protected>

      <Stack.Protected guard={!isLoggedIn}>
        <Stack.Screen name="sign-in" />
        <Stack.Screen name="create-account" />
      </Stack.Protected>
    </Stack>
  );
}
```

## Navigation Patterns

### Declarative Navigation (Preferred)

```typescript
import { Link } from "expo-router";

// Basic link
<Link href="/about">About</Link>

// With custom component
<Link href="/profile" asChild>
  <Pressable>
    <Text>Profile</Text>
  </Pressable>
</Link>

// Dynamic route
<Link href={{ pathname: "/user/[id]", params: { id: "123" } }}>
  View User
</Link>

// With prefetching
<Link href="/heavy-page" prefetch>Heavy Page</Link>
```

### Imperative Navigation

```typescript
import { useRouter } from "expo-router";

export default function Component() {
  const router = useRouter();

  const handleNavigate = () => {
    // Navigate (adds to history)
    router.navigate("/about");

    // Push (always adds to stack)
    router.push("/details");

    // Replace (no back navigation)
    router.replace("/home");

    // Back
    router.back();

    // Dynamic route
    router.navigate({
      pathname: "/user/[id]",
      params: { id: "123" },
    });
  };

  return <Button onPress={handleNavigate} title="Navigate" />;
}
```

### Defensive Navigation Guards

Always validate parameters before navigation to prevent broken URLs.

```typescript
const handleNavigation = useCallback(() => {
  if (!entityId) {
    console.error("Cannot navigate: entity ID is missing");
    return;
  }
  router.push(`/players/${entityId}`);
}, [entityId, router]);
```

### Reading Route Parameters

```typescript
import { useLocalSearchParams, useGlobalSearchParams } from "expo-router";

export default function UserPage() {
  // Local params (current route only)
  const { id, tab } = useLocalSearchParams<{ id: string; tab?: string }>();

  // Global params (entire URL)
  const globalParams = useGlobalSearchParams();

  return <Text>User ID: {id}</Text>;
}
```

## Deep Linking

### Configure URL Scheme

In `app.json` or `app.config.js`:

```json
{
  "expo": {
    "scheme": "myapp"
  }
}
```

### Initial Route for Deep Links

Ensure proper back navigation when deep linking.

```typescript
// app/feed/_layout.tsx
export const unstable_settings = {
  initialRouteName: "index",
};

export default function FeedLayout() {
  return <Stack />;
}
```

### Deep Link with Anchor

```typescript
// Forces initial route to load first
<Link href="/feed/post/123" withAnchor>
  View Post
</Link>
```

## Common Patterns

### Stacks Inside Tabs

```
app/
├── (tabs)/
│   ├── _layout.tsx         # Tab navigator
│   ├── index.tsx           # Home tab
│   ├── feed/               # Feed tab with stack
│   │   ├── _layout.tsx     # Stack navigator
│   │   ├── index.tsx       # Feed list
│   │   └── [postId].tsx    # Post detail
│   └── settings.tsx        # Settings tab
```

### Shared Routes Between Tabs

```
app/
├── (tabs)/
│   ├── _layout.tsx
│   ├── (feed)/             # Feed tab group
│   │   └── index.tsx
│   ├── (search)/           # Search tab group
│   │   └── index.tsx
│   └── (feed,search)/      # Shared between both
│       └── users/
│           └── [userId].tsx
```

### Modal Routes

```typescript
// app/_layout.tsx
<Stack>
  <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
  <Stack.Screen
    name="modal"
    options={{
      presentation: "modal",
      animation: "slide_from_bottom",
    }}
  />
</Stack>
```

## Anti-Patterns to Avoid

### 1. Business Logic in Route Files

Route files should only import and render feature components.

### 2. Deeply Nested Navigators

Avoid nesting stacks within stacks unnecessarily. Use route groups instead.

### 3. Missing initialRouteName

Always set `initialRouteName` in stack layouts for proper deep link behavior.

### 4. Hardcoded Navigation Paths

Use typed routes or constants instead of string literals.

```typescript
// AVOID
router.push("/players/123/compare");

// PREFER
router.push({
  pathname: "/players/[playerId]/compare",
  params: { playerId: "123" },
});
```

### 5. Using window APIs Without Platform Checks

```typescript
// AVOID
const width = window.innerWidth;

// PREFER
import { useWindowDimensions } from "react-native";
const { width } = useWindowDimensions();
```

## Resources

For detailed documentation on specific topics, refer to:

- `references/official-docs.md` - Condensed official Expo Router documentation
- `scripts/generate-route.py` - Route scaffolding script

Official Documentation: https://docs.expo.dev/router/introduction/
