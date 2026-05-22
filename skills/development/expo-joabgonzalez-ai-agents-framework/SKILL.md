---
name: expo
description: "Building, testing, and deploying cross-platform mobile applications using Expo with React Native. EAS Build, OTA updates, native modules. Trigger: When developing with Expo, configuring EAS services, or building cross-platform mobile apps."
skills:
  - conventions
  - react-native
  - typescript
  - a11y
dependencies:
  expo: ">=50.0.0 <51.0.0"
  react-native: ">=0.73.0 <1.0.0"
  react: ">=18.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
  - file-reader
---

# Expo Skill

## Overview

This skill provides guidance for developing cross-platform mobile applications using Expo, covering setup, development workflow, native features, and deployment.

## Objective

Enable developers to build, test, and deploy mobile applications efficiently using Expo's managed workflow with proper TypeScript support and React Native best practices.

---

## When to Use

Use this skill when:

- Building cross-platform mobile apps (iOS + Android)
- Using Expo managed workflow
- Configuring EAS Build or EAS Update
- Accessing native features via Expo SDK
- Deploying OTA updates

Don't use this skill for:

- Bare React Native projects (use react-native skill)
- Web-only applications
- Custom native modules not supported by Expo

---

## Critical Patterns

### ✅ REQUIRED: Use Expo SDK for Native Features

```typescript
// ✅ CORRECT: Expo SDK modules
import * as Location from "expo-location";
import { Camera } from "expo-camera";

// ❌ WRONG: Direct React Native linking (use Expo modules)
import { NativeModules } from "react-native";
```

### ✅ REQUIRED: Handle Permissions Properly

```typescript
// ✅ CORRECT: Request permissions before using
const { status } = await Location.requestForegroundPermissionsAsync();
if (status === "granted") {
  const location = await Location.getCurrentPositionAsync();
}

// ❌ WRONG: No permission check
const location = await Location.getCurrentPositionAsync(); // May crash
```

### ✅ REQUIRED: Use TypeScript

```typescript
// ✅ CORRECT: Typed props and state
interface Props {
  title: string;
}

const Component: React.FC<Props> = ({ title }) => {
  const [count, setCount] = useState<number>(0);
};
```

---

## Conventions

- Use TypeScript for type safety
- Follow React Native component patterns
- Leverage Expo SDK for native features
- Use Expo Go for development testing
- Implement proper error handling for native features

---

## Decision Tree

**Need native feature?** → Check Expo SDK first, use managed module if available.

**Custom native code needed?** → Use config plugins or eject to bare workflow.

**Building for stores?** → Use EAS Build for cloud builds.

**Need OTA updates?** → Use EAS Update for instant app updates.

**Platform-specific code?** → Use `Platform.select()` or `.ios.tsx`/`.android.tsx` files.

**Testing?** → Use Expo Go for development, physical devices or simulators for final testing.

**Navigation?** → Use Expo Router or React Navigation.

---

## Example

```typescript
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Welcome to Expo</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
```

## Edge Cases

- Handle platform-specific code with Platform API
- Manage permissions properly
- Test on both iOS and Android
- Handle offline scenarios

## References

- https://docs.expo.dev/
- https://reactnative.dev/
