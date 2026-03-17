---
name: expo
description: Expo React Native development platform. Use for React Native apps.
---

# Expo

Expo is an open-source framework for apps that run natively on Android, iOS, and the web. It builds on top of React Native, providing a curated set of tools and libraries (SDK) to simplify the development lifecycle.

## When to Use

- Building React Native apps without managing Xcode/Android Studio projects manually.
- Needing fast Over-the-Air (OTA) updates via EAS Update.
- Rapid prototyping with the Expo Go app.
- Teams that prefer a "Managed" workflow but still need native capabilities (via Config Plugins).

## Quick Start

```bash
# Create a new app with Expo Router (default in 2025)
npx create-expo-app@latest my-safe-app
cd my-safe-app
npx expo start
```

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Home" }} />
    </Stack>
  );
}

// app/index.tsx
import { View, Text, StyleSheet } from "react-native";
import { Link } from "expo-router";
import { Image } from "expo-image";

export default function Index() {
  return (
    <View style={styles.container}>
      <Image
        source="https://picsum.photos/200"
        style={{ width: 100, height: 100, marginBottom: 20 }}
        contentFit="cover"
      />
      <Text style={styles.text}>Welcome to Expo!</Text>
      <Link href="/details/123" style={styles.link}>
        Go to Details
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  text: { fontSize: 20, fontWeight: "bold" },
  link: { marginTop: 15, color: "#007AFF" },
});
```

## Core Concepts

### Managed Workflow & Prebuild

Historically, Expo had a "ejected" vs "managed" split. Modern Expo uses **Prebuild** (Continuous Native Generation). You don't commit `android` or `ios` folders; instead, they are generated on demand from `app.json` configuration.

### EAS (Expo Application Services)

- **EAS Build**: Compiles your app in the cloud (or locally) into `.apk` / `.ipa`.
- **EAS Submit**: Uploads binary to stores.
- **EAS Update**: Pushes JS/asset fixes instantly to users.

### Config Plugins

Functions that modify native files (`Info.plist`, `AndroidManifest.xml`) during prebuild. This allows you to use _any_ native library without "ejecting".

## Common Patterns

### Development Builds

Instead of Expo Go (which has a fixed set of native code), create a **Development Build**. This is a custom version of Expo Go that includes _your_ specific native dependencies.

- `npx expo run:ios` or `npx eas build --profile development --platform ios`.

### Expo Router

File-system based routing (like Next.js).

- `app/home.tsx` -> `/home`
- `app/user/[id].tsx` -> `/user/123`

## Best Practices

**Do**:

- Use `npx expo install` to install libraries (ensures version compatibility).
- Use **Expo Image** (`expo-image`) for performant image loading and caching.
- Use **EAS Build** for creating production binaries.
- Use **Config Plugins** instead of manually editing native files.

**Don't**:

- Don't use Expo Go if you need custom native code (use Dev Builds).
- Don't commit `ios` and `android` directories if using CNG (Continuous Native Generation).
- Don't ignore `npx expo doctor` warnings.

## Troubleshooting

| Error                          | Cause                                     | Solution                                            |
| :----------------------------- | :---------------------------------------- | :-------------------------------------------------- |
| `Native module cannot be null` | Library installed but not in the runtime. | Rebuild the Development Build (`npx expo run:ios`). |
| `EAS Build failed`             | Configuration error or build timeout.     | Check logs on expo.dev; run `npx expo-doctor`.      |
| `Expo Go crashes on launch`    | Incompatible SDK version or native code.  | Update Expo Go or switch to Development Build.      |

## References

- [Expo Documentation](https://docs.expo.dev)
- [EAS Documentation](https://docs.expo.dev/eas)
- [Expo Core Libraries](https://docs.expo.dev/versions/latest/)
