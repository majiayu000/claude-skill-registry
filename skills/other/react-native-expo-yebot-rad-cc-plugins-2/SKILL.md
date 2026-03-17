---
name: react-native-expo
description: >
  Comprehensive React Native and Expo development skill for building cross-platform mobile apps.
  Use when creating React Native or Expo projects, building screens and navigation with Expo Router,
  using Expo SDK packages (camera, location, notifications, file system, etc.), configuring app.json
  or eas.json for builds, working with React Native core components (View, Text, FlatList, etc.),
  implementing state management, forms, and common patterns, setting up EAS Build, Submit, or Update,
  or troubleshooting React Native and Expo issues.
---

# React Native & Expo Development

Build cross-platform mobile apps for iOS and Android using React Native with Expo.

## Instructions

1. For Expo SDK packages (camera, location, notifications), see [references/expo-sdk-reference.md](references/expo-sdk-reference.md)
2. For React Native core components, see [references/react-native-reference.md](references/react-native-reference.md)
3. For Expo Router navigation, see [references/expo-router-reference.md](references/expo-router-reference.md)
4. For app.json, eas.json, and builds, see [references/expo-config-eas-reference.md](references/expo-config-eas-reference.md)
5. For state management and patterns, see [references/common-patterns.md](references/common-patterns.md)
6. PROACTIVELY fetch https://docs.expo.dev/llms.txt for comprehensive Expo documentation links when you need deeper information on any Expo topic not covered in the local references
7. PROACTIVELY fetch https://reactnative.dev/llms.txt for comprehensive React Native documentation links when you need deeper information on React Native core APIs, components, or architecture

## Quick Start

```bash
# Create new project
npx create-expo-app@latest my-app
cd my-app
npx expo start

# Install packages (always use expo install for compatibility)
npx expo install expo-camera expo-image-picker expo-location
```

## Reference Files

Load these based on the task at hand:

| Task                                                      | Reference File                            |
| --------------------------------------------------------- | ----------------------------------------- |
| Expo SDK packages (camera, location, notifications, etc.) | `references/expo-sdk-reference.md`        |
| React Native core components and APIs                     | `references/react-native-reference.md`    |
| Expo Router navigation and routing                        | `references/expo-router-reference.md`     |
| app.json, eas.json, builds, and deployment                | `references/expo-config-eas-reference.md` |
| State management, hooks, patterns                         | `references/common-patterns.md`           |

## Essential Commands

```bash
# Development
npx expo start              # Start dev server
npx expo start -c           # Clear cache and start
npx expo start --dev-client # For development builds

# Package management
npx expo install <package>  # Install with version matching
npx expo install --fix      # Fix mismatched versions

# Building
npx expo prebuild           # Generate native projects
npx expo run:ios            # Build and run iOS locally
npx expo run:android        # Build and run Android locally

# EAS
eas build --profile development --platform ios
eas build --profile preview --platform all
eas build --profile production --platform all
eas submit --platform ios
eas update --branch production --message "Update"
```

## Project Structure

```
my-app/
├── app/                    # Expo Router screens
│   ├── _layout.tsx         # Root layout (required)
│   ├── index.tsx           # / route
│   ├── (tabs)/             # Tab group
│   │   ├── _layout.tsx     # Tab navigator
│   │   └── home.tsx
│   └── [id].tsx            # Dynamic route
├── src/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── stores/
├── assets/
├── app.json
├── eas.json
└── tsconfig.json
```

## Common Patterns Quick Reference

### Navigation (Expo Router)

```tsx
// Navigate
import { router, Link } from 'expo-router';
router.push('/details');
router.push({ pathname: '/user/[id]', params: { id: '123' } });
router.replace('/home');
router.back();

// Link component
<Link href="/about">About</Link>
<Link href="/user/123" asChild><Pressable>...</Pressable></Link>

// Read params
const { id } = useLocalSearchParams<{ id: string }>();
```

### Layout Structure

```tsx
// Stack (default)
import { Stack } from "expo-router";
export default function Layout() {
  return <Stack screenOptions={{ headerShown: true }} />;
}

// Tabs
import { Tabs } from "expo-router";
export default function Layout() {
  return (
    <Tabs>
      <Tabs.Screen name="home" options={{ title: "Home" }} />
    </Tabs>
  );
}
```

### Core Components

```tsx
import { View, Text, TextInput, FlatList, Pressable, StyleSheet } from 'react-native';

// Basic layout
<View style={styles.container}>
  <Text style={styles.title}>Hello</Text>
</View>

// List
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <Text>{item.name}</Text>}
/>

// Touch handling
<Pressable
  onPress={() => {}}
  style={({ pressed }) => [styles.button, pressed && styles.pressed]}
>
  <Text>Press Me</Text>
</Pressable>
```

### Common Expo SDK Usage

```tsx
// Camera
import { CameraView, useCameraPermissions } from "expo-camera";
const [permission, requestPermission] = useCameraPermissions();

// Image Picker
import * as ImagePicker from "expo-image-picker";
const result = await ImagePicker.launchImageLibraryAsync({
  mediaTypes: ["images"],
});

// Location
import * as Location from "expo-location";
await Location.requestForegroundPermissionsAsync();
const location = await Location.getCurrentPositionAsync({});

// Secure Storage
import * as SecureStore from "expo-secure-store";
await SecureStore.setItemAsync("token", "value");
const value = await SecureStore.getItemAsync("token");
```

## Troubleshooting

### Common Issues

**"Unable to resolve module" error**

```bash
npx expo start -c  # Clear cache
rm -rf node_modules && npm install
```

**Native module not found**

```bash
npx expo prebuild --clean
npx expo run:ios  # or run:android
```

**Incompatible package versions**

```bash
npx expo install --fix
```

**EAS build fails**

- Check eas.json configuration
- Verify credentials with `eas credentials`
- Check build logs at expo.dev

### Platform-Specific Code

```tsx
import { Platform } from "react-native";

// Conditional value
const padding = Platform.OS === "ios" ? 20 : 16;

// Platform.select
const styles = {
  shadow: Platform.select({
    ios: { shadowColor: "#000", shadowOffset: { width: 0, height: 2 } },
    android: { elevation: 4 },
  }),
};

// File-based: Component.ios.tsx, Component.android.tsx
```

## Best Practices

1. **Always use `npx expo install`** for packages to ensure version compatibility
2. **Use TypeScript** for type safety and better DX
3. **Use Expo Router** for file-based navigation
4. **Store sensitive data** in expo-secure-store, not AsyncStorage
5. **Use development builds** instead of Expo Go for production apps
6. **Memoize** expensive computations and callbacks
7. **Use FlatList** for long lists, not ScrollView with map()
8. **Test on real devices** before submitting to stores
9. **Use EAS Update** for OTA updates
10. **Keep SDK version current** - update quarterly
