---
name: expo-upgrading
description: Guidelines for upgrading Expo SDK versions, fixing dependency issues, and migrating to new architecture
agents: [tap]
triggers: [expo upgrade, sdk upgrade, expo install, expo-doctor, breaking changes, deprecated packages, new architecture]
---

# Expo SDK Upgrade Guide

Guidelines for upgrading Expo SDK versions and fixing dependency issues. Based on official Expo skills.

## Step-by-Step Upgrade Process

### 1. Upgrade Expo and Dependencies

```bash
# Upgrade to latest SDK
npx expo install expo@latest

# Fix peer dependencies
npx expo install --fix
```

### 2. Run Diagnostics

```bash
npx expo-doctor
```

### 3. Clear Caches and Reinstall

```bash
# Clear Expo cache
npx expo export -p ios --clear

# Clean install
rm -rf node_modules .expo
watchman watch-del-all
npm install  # or bun install
```

## Breaking Changes Checklist

- [ ] Check for removed APIs in release notes
- [ ] Update import paths for moved modules
- [ ] Review native module changes requiring prebuild
- [ ] Test all camera, audio, and video features
- [ ] Verify navigation still works correctly
- [ ] Test push notifications
- [ ] Verify deep linking

## Prebuild for Native Changes

If upgrading requires native changes:

```bash
npx expo prebuild --clean
```

This regenerates the `ios` and `android` directories. **Only run on managed workflow projects.**

## Clear Caches for Bare Workflow

### iOS

```bash
# Clear CocoaPods cache
cd ios && pod install --repo-update

# Clear derived data
npx expo run:ios --no-build-cache

# Full clean
rm -rf ios/Pods ios/Podfile.lock
cd ios && pod install
```

### Android

```bash
# Clear Gradle cache
cd android && ./gradlew clean

# Full clean
rm -rf android/.gradle android/build android/app/build
```

## Deprecated Packages

| Old Package | Replacement |
|-------------|-------------|
| `expo-av` | `expo-audio` and `expo-video` |
| `expo-permissions` | Individual package permission APIs |
| `@expo/vector-icons` | `expo-symbols` (for SF Symbols) |
| `AsyncStorage` | `expo-sqlite/localStorage/install` |
| `expo-app-loading` | `expo-splash-screen` |
| `expo-linear-gradient` | `experimental_backgroundImage` + CSS gradients in View |

### Migration Examples

#### expo-av to expo-audio/expo-video

```tsx
// Before
import { Audio, Video } from 'expo-av';

// After
import { Audio } from 'expo-audio';
import { VideoView } from 'expo-video';
```

#### AsyncStorage to expo-sqlite

```tsx
// Before
import AsyncStorage from '@react-native-async-storage/async-storage';

// After
import { localStorage } from 'expo-sqlite/localStorage';
await localStorage.setItem('key', 'value');
const value = await localStorage.getItem('key');
```

## Housekeeping

### Remove from package.json

These are now implicit dependencies:
- `@babel/core`
- `babel-preset-expo`
- `expo-constants`

### Delete Redundant Config Files

If `babel.config.js` only contains 'babel-preset-expo', delete it.

If `metro.config.js` only contains expo defaults, delete it.

### app.json Cleanup

- Delete `sdkVersion` - let Expo manage it automatically
- Remove `"newArchEnabled": true` in SDK 53+ (it's the default)

## SDK-Specific Changes

### SDK 54+ (React 19)

#### React 19 Changes

```tsx
// Before - useContext
const value = React.useContext(MyContext);

// After - use
const value = React.use(MyContext);

// Before - Context.Provider
<MyContext.Provider value={value}>

// After - Context directly
<MyContext value={value}>

// Before - forwardRef
const Component = React.forwardRef((props, ref) => { ... });

// After - ref in props
const Component = ({ ref, ...props }) => { ... };
```

#### React Compiler (Recommended)

Enable in `app.json`:

```json
{
  "expo": {
    "experiments": {
      "reactCompiler": true
    }
  }
}
```

#### Required Dependencies

```bash
# Required for react-native-reanimated in SDK 54+
npx expo install react-native-worklets
```

### SDK 53+ (New Architecture)

The new architecture is enabled by default. Expo Go only supports new architecture.

#### Metro Config

Remove redundant options (now defaults):
- `resolver.unstable_enablePackageExports`
- `experimentalImportSupport` (SDK 54+)
- `EXPO_USE_FAST_RESOLVER=1` (removed in SDK 54)

#### PostCSS

- `autoprefixer` isn't needed in SDK 53+
- Use `postcss.config.mjs` (not `.js`)

### SDK 50+

- cjs and mjs extensions supported by default
- Expo Webpack deprecated - migrate to Expo Router + Metro web

## Troubleshooting

### Common Issues

#### "Cannot find module" errors

```bash
# Clear Metro cache
npx expo start --clear
```

#### TypeScript errors after upgrade

```bash
# Reinstall types
npx expo install --fix
npm install @types/react@latest @types/react-native@latest
```

#### Native module not found

```bash
# Rebuild native projects
npx expo prebuild --clean
npx expo run:ios  # or run:android
```

#### CocoaPods issues

```bash
# Full pod reinstall
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
```

### Verifying the Upgrade

```bash
# Check for issues
npx expo-doctor

# Verify TypeScript
npx tsc --noEmit

# Run tests
npm test

# Start development
npx expo start
```

## Removing Patches

Check `patches/` directory for outdated patches that may no longer be needed after upgrade. Remove and test.

## Resources

- Release notes: https://expo.dev/changelog
- Upgrade helper: https://docs.expo.dev/workflow/upgrading-expo-sdk/
- Breaking changes: https://docs.expo.dev/versions/latest/
