---
name: expo-router
description: Patterns for Expo Router including Stack configuration, native tabs, and file-based routing best practices. Apply when working with navigation, routing, or screen configuration.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Expo Router Patterns

## Stack Navigator Configuration

### Root Layout Setup
Use `screenOptions` on the Stack component to set defaults for all screens. Do NOT explicitly list every screen - routes are auto-discovered from the file structure.

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }} />
  );
}
```

### Per-Screen Configuration
Individual screens configure their own options using `<Stack.Screen>` within the component file:

```tsx
// app/lesson/[id].tsx
import { Stack } from 'expo-router';

export default function LessonScreen() {
  return (
    <View>
      <Stack.Screen
        options={{
          title: 'Lesson',
          headerShown: true,
          headerBackTitle: 'Back',
        }}
      />
      {/* Screen content */}
    </View>
  );
}
```

### Dynamic Header Configuration
Use `useNavigation` with `setOptions` for dynamic header content like buttons:

```tsx
import { useNavigation } from 'expo-router';
import { useLayoutEffect } from 'react';

export default function Screen() {
  const navigation = useNavigation();

  useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <Pressable onPress={handlePress}>
          <Ionicons name="add" size={28} />
        </Pressable>
      ),
    });
  }, [navigation]);

  return <View>{/* content */}</View>;
}
```

## Native Tabs (`expo-router/unstable-native-tabs`)

Native tabs provide platform-native tab bar with SF Symbols on iOS:

```tsx
// app/(tabs)/_layout.tsx
import { Icon, Label, NativeTabs } from 'expo-router/unstable-native-tabs';

export default function TabLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index" options={{ title: 'Home' }}>
        <Icon sf="house.fill" drawable="custom_android_drawable" />
        <Label>Home</Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

## Key Principles

1. **File-based routing**: Routes are auto-discovered from the `app/` directory structure
2. **Minimal configuration**: Only configure what you need to override
3. **Screen-level options**: Screens configure their own headers/options using `<Stack.Screen>` within the component
4. **Layout files**: `_layout.tsx` files define navigation structure for their directory
5. **Route groups**: Parentheses like `(tabs)` create route groups without affecting the URL path

## Common Mistakes to Avoid

- Don't list every screen explicitly in Stack - they're auto-discovered
- Don't use `screenOptions` for route-specific settings - use `<Stack.Screen>` in the route file
- Don't nest navigators deeply - use file-based routing for cleaner structure
