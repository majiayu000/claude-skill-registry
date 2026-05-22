---
name: react-native-expo
description: |
  Build React Native 0.76+ apps with Expo SDK 52-54. Covers mandatory New Architecture (0.82+/SDK 55+), React 19 changes, SDK 54 breaking changes (expo-av, expo-file-system, Reanimated v4), and Swift iOS template. Prevents 16 documented errors.

  Use when building Expo apps, migrating to New Architecture, upgrading to SDK 54+, or fixing Fabric, TurboModule, propTypes, expo-updates crashes, or Swift AppDelegate errors.
user-invocable: true
---

# React Native Expo (0.76-0.82+ / SDK 52+)

**Status**: Production Ready
**Last Updated**: 2026-01-21
**Dependencies**: Node.js 20.19.4+, Expo CLI, Xcode 16.1+ (iOS)
**Latest Versions**: react-native@0.81.5, expo@~54.0.31, react@19.2.3

---

## Quick Start (15 Minutes)

### 1. Create New Expo Project (RN 0.76+)

```bash
# Create new Expo app with React Native 0.76+
npx create-expo-app@latest my-app

cd my-app

# Install latest dependencies
npx expo install react-native@latest expo@latest
```

**Why this matters:**
- Expo SDK 52+ uses React Native 0.76+ with New Architecture enabled by default
- New Architecture is **mandatory** in React Native 0.82+ (cannot be disabled)
- Hermes is the only supported JavaScript engine (JSC removed from Expo Go)

### 2. Verify New Architecture is Enabled

```bash
# Check if New Architecture is enabled (should be true by default)
npx expo config --type introspect | grep newArchEnabled
```

**CRITICAL:**
- React Native 0.82+ **requires** New Architecture - legacy architecture completely removed
- If migrating from 0.75 or earlier, upgrade to 0.76-0.81 first to use the interop layer
- Never try to disable New Architecture in 0.82+ (build will fail)

### 3. Start Development Server

```bash
# Start Expo dev server
npx expo start

# Press 'i' for iOS simulator
# Press 'a' for Android emulator
# Press 'j' to open React Native DevTools (NOT Chrome debugger!)
```

**CRITICAL:**
- Old Chrome debugger removed in 0.79 - use React Native DevTools instead
- Metro terminal no longer streams `console.log()` - use DevTools Console
- Keyboard shortcuts 'a'/'i' work in CLI, not Metro terminal

---

## Critical Breaking Changes (Dec 2024+)

### 🔴 New Architecture Mandatory (0.82+)

**SDK Timeline:**
- **Expo SDK 54** (React Native 0.81): Last release supporting Legacy Architecture
- **Expo SDK 55** (React Native 0.83): New Architecture mandatory, Legacy completely removed

**What Changed:**
- **0.76-0.81 / SDK 52-54**: New Architecture default, legacy frozen (no new features)
- **0.82+ / SDK 55+**: Legacy Architecture **completely removed** from codebase

**Impact:**
```bash
# This will FAIL in 0.82+ / SDK 55+:
# gradle.properties (Android)
newArchEnabled=false  # ❌ Ignored, build fails

# iOS
RCT_NEW_ARCH_ENABLED=0  # ❌ Ignored, build fails
```

**Migration Path:**
1. Upgrade to 0.76-0.81 / SDK 54 first (if on 0.75 or earlier)
2. Test with New Architecture enabled
3. Fix incompatible dependencies (Redux, i18n, CodePush, Reanimated v3 → v4)
4. Then upgrade to 0.82+ / SDK 55+

**Source:** [Expo SDK 54 Changelog](https://expo.dev/changelog/sdk-54)

### 🔴 propTypes Removed (React 19 / RN 0.78+)

**What Changed:**
React 19 removed `propTypes` completely. No runtime validation, no warnings - silently ignored.

**Before (Old Code):**
```typescript
import PropTypes from 'prop-types';

function MyComponent({ name, age }) {
  return <Text>{name} is {age}</Text>;
}

MyComponent.propTypes = {  // ❌ Silently ignored in React 19
  name: PropTypes.string.isRequired,
  age: PropTypes.number
};
```

**After (Use TypeScript):**
```typescript
type MyComponentProps = {
  name: string;
  age?: number;
};

function MyComponent({ name, age }: MyComponentProps) {
  return <Text>{name} is {age}</Text>;
}
```

**Migration:**
```bash
# Use React 19 codemod to remove propTypes
npx @codemod/react-19 upgrade
```

### 🔴 forwardRef Deprecated (React 19)

**What Changed:**
`forwardRef` no longer needed - pass `ref` as a regular prop.

**Before (Old Code):**
```typescript
import { forwardRef } from 'react';

const MyInput = forwardRef((props, ref) => {  // ❌ Deprecated
  return <TextInput ref={ref} {...props} />;
});
```

**After (React 19):**
```typescript
function MyInput({ ref, ...props }) {  // ✅ ref is a regular prop
  return <TextInput ref={ref} {...props} />;
}
```

### 🔴 Swift iOS Template Default (0.77+)

**What Changed:**
New projects use Swift `AppDelegate.swift` instead of Objective-C `AppDelegate.mm`.

**Old Structure:**
```
ios/MyApp/
├── main.m              # ❌ Removed
├── AppDelegate.h       # ❌ Removed
└── AppDelegate.mm      # ❌ Removed
```

**New Structure:**
```swift
// ios/MyApp/AppDelegate.swift ✅
import UIKit
import React

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
  func application(_ application: UIApplication, ...) -> Bool {
    // App initialization
    return true
  }
}
```

**Migration (0.76 → 0.77):**
When upgrading existing projects, you **MUST** add this line:
```swift
// Add to AppDelegate.swift during migration
import React
import ReactCoreModules

RCTAppDependencyProvider.sharedInstance()  // ⚠️ CRITICAL: Must add this!
```

**Source:** [React Native 0.77 Release Notes](https://reactnative.dev/blog/2025/01/14/release-0.77)

### 🔴 Metro Log Forwarding Removed (0.77+)

**What Changed:**
Metro terminal no longer streams `console.log()` output.

**Before (0.76):**
```bash
# console.log() appeared in Metro terminal
$ npx expo start
> LOG  Hello from app!  # ✅ Appeared here
```

**After (0.77+):**
```bash
# console.log() does NOT appear in Metro terminal
$ npx expo start
# (no logs shown)  # ❌ Removed

# Workaround (temporary, will be removed):
$ npx expo start --client-logs  # Shows logs, deprecated
```

**Solution:**
Use React Native DevTools Console instead (press 'j' in CLI).

**Source:** [React Native 0.77 Release Notes](https://reactnative.dev/blog/2025/01/14/release-0.77)

### 🔴 Chrome Debugger Removed (0.79+)

**What Changed:**
Old Chrome debugger (`chrome://inspect`) removed. Use React Native DevTools instead.

**Old Method (Removed):**
```bash
# ❌ This no longer works:
# Open Dev Menu → "Debug" → Chrome DevTools opens
```

**New Method (0.76+):**
```bash
# Press 'j' in CLI or Dev Menu → "Open React Native DevTools"
# ✅ Uses Chrome DevTools Protocol (CDP)
# ✅ Reliable breakpoints, watch values, stack inspection
# ✅ JS Console (replaces Metro logs)
```

**Limitations:**
- Third-party extensions not yet supported (Redux DevTools, etc.)
- Network inspector coming in 0.83 (late 2025)

**Source:** [React Native 0.79 Release Notes](https://reactnative.dev/blog/2025/04/release-0.79)

### 🔴 JSC Engine Moved to Community (0.79+)

**What Changed:**
JavaScriptCore (JSC) first-party support removed from React Native 0.81+ core. Moved to community package.

**Before (0.78):**
- Both Hermes and JSC bundled in React Native
- JSC available in Expo Go

**After (0.79+ / React Native 0.81+ / SDK 54):**
```bash
# JSC removed from React Native core
# If you still need JSC (rare):
npm install @react-native-community/javascriptcore
```

**Expo Go:**
- SDK 52+: JSC completely removed from Expo Go
- Hermes only supported

**Note:** JSC will eventually be removed entirely from React Native.

**Source:** [Expo SDK 54 Changelog](https://expo.dev/changelog/sdk-54)

### 🔴 Deep Imports Deprecated (0.80+)

**What Changed:**
Importing from internal paths will break.

**Before (Old Code):**
```typescript
// ❌ Deep imports deprecated
import Button from 'react-native/Libraries/Components/Button';
import Platform from 'react-native/Libraries/Utilities/Platform';
```

**After:**
```typescript
// ✅ Import only from 'react-native'
import { Button, Platform } from 'react-native';
```

**Source:** [React Native 0.80 Release Notes](https://reactnative.dev/blog/2025/06/release-0.80)

### 🔴 Android Edge-to-Edge Mandatory (SDK 54+)

**What Changed:**
Edge-to-edge display is **enabled in all Android apps by default in SDK 54 and cannot be disabled**.

**Impact:**
```json
// app.json or app.config.js
{
  "expo": {
    "android": {
      // This setting is now IGNORED - edge-to-edge always enabled
      "edgeToEdgeEnabled": false  // ❌ No effect in SDK 54+
    }
  }
}
```

**UI Impact:**
Content now extends behind system status bar and navigation bar. You must account for insets manually using `react-native-safe-area-context`.

**Solution:**
```typescript
import { SafeAreaView } from 'react-native-safe-area-context';

function App() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      {/* Content respects system bars */}
    </SafeAreaView>
  );
}
```

**Source:** [Expo SDK 54 Changelog](https://expo.dev/changelog/sdk-54)

---

## New Features (Post-Dec 2024)

### CSS Properties (0.77+ New Architecture Only)

React Native now supports many CSS properties previously only available on web:

#### 1. `display: contents`

Makes an element "invisible" but keeps its children in the layout:

```typescript
<View style={{ display: 'contents' }}>
  {/* This View disappears, but Text still renders */}
  <Text>I'm still here!</Text>
</View>
```

**Use case:** Wrapper components that shouldn't affect layout.

#### 2. `boxSizing`

Control how width/height are calculated:

```typescript
// Default: padding/border inside box
<View style={{
  boxSizing: 'border-box',  // Default
  width: 100,
  padding: 10,
  borderWidth: 2
  // Total width: 100 (padding/border inside)
}} />

// Content-box: padding/border outside
<View style={{
  boxSizing: 'content-box',
  width: 100,
  padding: 10,
  borderWidth: 2
  // Total width: 124 (100 + 20 padding + 4 border)
}} />
```

#### 3. `mixBlendMode` + `isolation`

Blend layers like Photoshop:

```typescript
<View style={{ backgroundColor: 'red' }}>
  <View style={{
    mixBlendMode: 'multiply',  // 16 modes available
    backgroundColor: 'blue'
    // Result: purple (red × blue)
  }} />
</View>

// Prevent unwanted blending:
<View style={{ isolation: 'isolate' }}>
  {/* Blending contained within this view */}
</View>
```

**Available modes:** `multiply`, `screen`, `overlay`, `darken`, `lighten`, `color-dodge`, `color-burn`, `hard-light`, `soft-light`, `difference`, `exclusion`, `hue`, `saturation`, `color`, `luminosity`

#### 4. `outline` Properties

Visual outline that doesn't affect layout (unlike `border`):

```typescript
<View style={{
  outlineWidth: 2,
  outlineStyle: 'solid',      // solid | dashed | dotted
  outlineColor: 'blue',
  outlineOffset: 4,           // Space between element and outline
  outlineSpread: 2            // Expand outline beyond offset
}} />
```

**Key difference:** Outline doesn't change element size or trigger layout recalculations.

**Source:** [React Native 0.77 Release Notes](https://reactnative.dev/blog/2025/01/14/release-0.77)

### Android XML Drawables (0.78+)

Use native Android vector drawables (XML) as Image sources:

```typescript
// Load XML drawable at build time
import MyIcon from './assets/my_icon.xml';

<Image
  source={MyIcon}
  style={{ width: 40, height: 40 }}
/>

// Or with require:
<Image
  source={require('./assets/my_icon.xml')}
  style={{ width: 40, height: 40 }}
/>
```

**Benefits:**
- Scalable vector graphics (resolution-independent)
- Smaller APK size vs PNG
- Off-thread decoding (better performance)

**Constraints:**
- Build-time resources only (no network loading)
- Android only (iOS still uses SF Symbols or PNG)

**Source:** [React Native 0.78 Release Notes](https://reactnative.dev/blog/2025/02/release-0.78)

### React 19 New Hooks

#### 1. `useActionState` (replaces form patterns)

```typescript
import { useActionState } from 'react';

function MyForm() {
  const [state, submitAction, isPending] = useActionState(
    async (prevState, formData) => {
      // Async form submission
      const result = await api.submit(formData);
      return result;
    },
    { message: '' }  // Initial state
  );

  return (
    <form action={submitAction}>
      <TextInput name="email" />
      <Button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </Button>
      {state.message && <Text>{state.message}</Text>}
    </form>
  );
}
```

#### 2. `useOptimistic` (optimistic UI updates)

```typescript
import { useOptimistic } from 'react';

function LikeButton({ postId, initialLikes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (currentLikes, amount) => currentLikes + amount
  );

  async function handleLike() {
    addOptimisticLike(1);  // Update UI immediately
    await api.like(postId);  // Then update server
  }

  return (
    <Button onPress={handleLike}>
      ❤️ {optimisticLikes}
    </Button>
  );
}
```

#### 3. `use` (read promises/contexts during render)

```typescript
import { use } from 'react';

function UserProfile({ userPromise }) {
  // Read promise directly during render (suspends if pending)
  const user = use(userPromise);

  return <Text>{user.name}</Text>;
}
```

**Source:** [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)

### React Native DevTools (0.76+)

**Access:**
- Press `j` in CLI
- Or open Dev Menu → "Open React Native DevTools"

**Features:**
- ✅ Reliable breakpoints (unlike old Chrome debugger)
- ✅ Watch values, call stack inspection
- ✅ JS Console (replaces Metro logs)
- ✅ Chrome DevTools Protocol (CDP) based
- ⏳ Network inspector (coming in 0.83)
- ❌ Third-party extensions not yet supported

**Source:** [React Native DevTools Announcement](https://reactnative.dev/blog/2024/10/release-0.76#react-native-devtools)

---

## Known Issues Prevention

This skill prevents **16** documented issues:

### Issue #1: propTypes Silently Ignored
**Error:** No error - `propTypes` just doesn't work
**Source:** [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
**Why It Happens:** React 19 removed runtime propTypes validation
**Prevention:** Use TypeScript instead, run `npx @codemod/react-19 upgrade` to remove

### Issue #2: forwardRef Deprecated Warning
**Error:** `Warning: forwardRef is deprecated`
**Source:** [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
**Why It Happens:** React 19 allows `ref` as a regular prop
**Prevention:** Remove `forwardRef` wrapper, pass `ref` as prop directly

### Issue #3: New Architecture Cannot Be Disabled (0.82+)
**Error:** Build fails with `newArchEnabled=false`
**Source:** [React Native 0.82 Release Notes](https://reactnative.dev/blog/2025/10/release-0.82)
**Why It Happens:** Legacy architecture completely removed from codebase
**Prevention:** Migrate to New Architecture before upgrading to 0.82+

### Issue #4: "Fabric component descriptor not found"
**Error:** `Fabric component descriptor provider not found for component`
**Source:** [New Architecture Migration Guide](https://reactnative.dev/docs/new-architecture-intro)
**Why It Happens:** Component not compatible with New Architecture (Fabric)
**Prevention:** Update library to New Architecture version, or use interop layer (0.76-0.81)

### Issue #5: "TurboModule not registered"
**Error:** `TurboModule '[ModuleName]' not found`
**Source:** [New Architecture Migration Guide](https://reactnative.dev/docs/new-architecture-intro)
**Why It Happens:** Native module needs New Architecture support (TurboModules)
**Prevention:** Update library to support TurboModules, or use interop layer (0.76-0.81)

### Issue #6: Swift AppDelegate Missing RCTAppDependencyProvider
**Error:** `RCTAppDependencyProvider not found`
**Source:** [React Native 0.77 Release Notes](https://reactnative.dev/blog/2025/01/14/release-0.77)
**Why It Happens:** When migrating from Objective-C to Swift template
**Prevention:** Add `RCTAppDependencyProvider.sharedInstance()` to AppDelegate.swift

### Issue #7: Metro Logs Not Appearing
**Error:** `console.log()` doesn't show in terminal
**Source:** [React Native 0.77 Release Notes](https://reactnative.dev/blog/2025/01/14/release-0.77)
**Why It Happens:** Metro log forwarding removed in 0.77
**Prevention:** Use React Native DevTools Console (press 'j'), or `--client-logs` flag (temporary)

### Issue #8: Chrome Debugger Not Working
**Error:** Chrome DevTools doesn't connect
**Source:** [React Native 0.79 Release Notes](https://reactnative.dev/blog/2025/04/release-0.79)
**Why It Happens:** Old Chrome debugger removed in 0.79
**Prevention:** Use React Native DevTools instead (press 'j')

### Issue #9: Deep Import Errors
**Error:** `Module not found: react-native/Libraries/...`
**Source:** [React Native 0.80 Release Notes](https://reactnative.dev/blog/2025/06/release-0.80)
**Why It Happens:** Internal paths deprecated, strict API enforced
**Prevention:** Import only from `'react-native'`, not deep paths

### Issue #10: Redux Store Crashes with New Architecture
**Error:** App crashes on Redux store creation
**Source:** [Redux Toolkit Migration Guide](https://redux-toolkit.js.org/usage/usage-guide)
**Why It Happens:** Old `redux` + `redux-thunk` incompatible with New Architecture
**Prevention:** Use Redux Toolkit (`@reduxjs/toolkit`) instead

### Issue #11: i18n-js Unreliable with New Architecture
**Error:** Translations not updating, or app crashes
**Source:** Community reports (GitHub issues)
**Why It Happens:** `i18n-js` not fully compatible with New Architecture
**Prevention:** Use `react-i18next` instead

### Issue #12: CodePush Crashes on Android
**Error:** Android crashes looking for bundle named `null`
**Source:** [CodePush GitHub Issues](https://github.com/microsoft/react-native-code-push/issues)
**Why It Happens:** Known incompatibility with New Architecture
**Prevention:** Avoid CodePush with New Architecture, or wait for official support

### Issue #13: expo-file-system Legacy API Removed (SDK 55+)
**Error:** `Module not found: expo-file-system/legacy`
**Source:** [Expo SDK 54 Changelog](https://expo.dev/changelog/sdk-54), [GitHub Issue #39056](https://github.com/expo/expo/issues/39056)
**Why It Happens:** Legacy API removed in SDK 55, must migrate to new File/Directory class API
**Prevention:** Migrate to new API before upgrading to SDK 55

**Migration Timeline:**
- SDK 53 and earlier: Legacy API at `expo-file-system`
- SDK 54: Legacy API at `expo-file-system/legacy`, new API at `expo-file-system` (default)
- SDK 55: Legacy API removed completely

**Old Code (SDK 54 with legacy import):**
```typescript
import * as FileSystem from 'expo-file-system/legacy';
await FileSystem.writeAsStringAsync(uri, content);
```

**New Code (SDK 54+ new API):**
```typescript
import { File } from 'expo-file-system';
const file = new File(uri);
await file.writeString(content);
```

### Issue #14: expo-av Removed (SDK 55+)
**Error:** `Module not found: expo-av`
**Source:** [Expo SDK 54 Changelog](https://expo.dev/changelog/sdk-54), [expo-av GitHub](https://github.com/expo/expo-av)
**Why It Happens:** Package deprecated in SDK 53, removed in SDK 55
**Prevention:** Migrate to expo-audio and expo-video before SDK 55

**Migration Timeline:**
- SDK 52: `expo-video` introduced
- SDK 53: `expo-audio` introduced, `expo-av` deprecated
- SDK 54: Last release with `expo-av` (no patches)
- SDK 55: `expo-av` removed

**Migration - Audio:**
```typescript
// OLD: expo-av
import { Audio } from 'expo-av';
const { sound } = await Audio.Sound.createAsync(require('./audio.mp3'));
await sound.playAsync();

// NEW: expo-audio
import { useAudioPlayer } from 'expo-audio';
const player = useAudioPlayer(require('./audio.mp3'));
player.play();
```

**Migration - Video:**
```typescript
// OLD: expo-av
import { Video } from 'expo-av';
<Video source={require('./video.mp4')} />

// NEW: expo-video
import { VideoView } from 'expo-video';
<VideoView source={require('./video.mp4')} />
```

### Issue #15: Reanimated v4 Requires New Architecture
**Error:** Build fails or crashes with Reanimated v4 on Legacy Architecture
**Source:** [Expo SDK 54 FYI](https://github.com/expo/fyi/blob/main/expo-54-reanimated.md)
**Why It Happens:** Reanimated v4 exclusively requires New Architecture
**Prevention:** Use Reanimated v3 with Legacy Architecture, or migrate to New Architecture first

**Version Matrix:**
| Reanimated Version | Architecture Support | Expo SDK |
|-------------------|---------------------|----------|
| v3 | Legacy + New Architecture | SDK 52-54 |
| v4 | New Architecture ONLY | SDK 54+ |

**NativeWind Incompatibility:**
```bash
# NativeWind does not support Reanimated v4 yet (as of Jan 2026)
# If using NativeWind, must stay on Reanimated v3
npm install react-native-reanimated@^3
```

**Migration to v4 (New Architecture only):**
1. Install `react-native-worklets` (required for v4)
2. Follow [official Reanimated v3 → v4 migration guide](https://docs.swmansion.com/react-native-reanimated/docs/fundamentals/getting-started/)
3. Skip babel.config.js changes if using `babel-preset-expo` (auto-configured)

### Issue #16: iOS Crashes on Launch with Hermes + New Architecture (SDK 54) - Community-sourced
**Error:**
```
hermes::vm::JSObject::putComputed_RJS
hermes::vm::arrayPrototypePush
```
**Source:** [GitHub Issue #41824](https://github.com/expo/expo/issues/41824), [Medium Post](https://medium.com/@shanavascruise/new-architecture-by-default-hermes-ios-expo-updates-can-break-your-ios-builds-4e98d89a1648)
**Verified:** Reproduction available
**Why It Happens:** Expo Updates requires explicit `:hermes_enabled` flag in Podfile when using New Architecture on iOS
**Prevention:** Add explicit Hermes flag to ios/Podfile

**Conditions:**
- Expo SDK 54
- New Architecture enabled
- Hermes enabled (default)
- Using `expo-updates`
- iOS only (Android unaffected)

**Workaround:**
```ruby
# ios/Podfile
use_frameworks! :linkage => :static
ENV['HERMES_ENABLED'] = '1'  # ⚠️ CRITICAL: Must be explicit with New Arch + expo-updates
```

**Note:** This is a community-sourced finding with reproduction repository, not yet officially documented in Expo changelog.

---

## Migration Guide: 0.72-0.75 → 0.82+

### Step 1: Upgrade to Interop Layer First (0.76-0.81)

**Why:** Can't skip directly to 0.82 if using legacy architecture - you'll lose the interop layer.

```bash
# Check current version
npx react-native --version

# Upgrade to 0.81 first (last version with interop layer)
npm install react-native@0.81
npx expo install --fix
```

### Step 2: Enable New Architecture (if not already)

```bash
# Android (gradle.properties)
newArchEnabled=true

# iOS
RCT_NEW_ARCH_ENABLED=1 bundle exec pod install

# Rebuild
npm run ios
npm run android
```

### Step 3: Fix Incompatible Dependencies

**Common incompatibilities:**

```bash
# Replace Redux with Redux Toolkit
npm uninstall redux redux-thunk
npm install @reduxjs/toolkit react-redux

# Replace i18n-js with react-i18next
npm uninstall i18n-js
npm install react-i18next i18next

# Update React Navigation (if old version)
npm install @react-navigation/native@latest
```

### Step 4: Test Thoroughly

```bash
# Run on both platforms
npm run ios
npm run android

# Test all features:
# - Navigation
# - State management (Redux)
# - API calls
# - Deep linking
# - Push notifications
```

### Step 5: Migrate to React 19 (if upgrading to 0.78+)

```bash
# Run React 19 codemod
npx @codemod/react-19 upgrade

# Manually verify:
# - Remove all propTypes declarations
# - Remove forwardRef wrappers
# - Update to new hooks (useActionState, useOptimistic)
```

### Step 6: Upgrade to 0.82+

```bash
# Only after testing with New Architecture enabled!
npm install react-native@0.82
npx expo install --fix

# Rebuild
npm run ios
npm run android
```

### Step 7: Migrate iOS to Swift (if new project)

New projects (0.77+) use Swift by default. For existing projects:

```bash
# Follow upgrade helper
# https://react-native-community.github.io/upgrade-helper/
# Select: 0.76 → 0.77

# CRITICAL: Add this line to AppDelegate.swift
RCTAppDependencyProvider.sharedInstance()
```

---

## Common Patterns

### Pattern 1: Conditional Rendering with New Hooks

```typescript
import { useActionState } from 'react';

function LoginForm() {
  const [state, loginAction, isPending] = useActionState(
    async (prevState, formData) => {
      try {
        const user = await api.login(formData);
        return { success: true, user };
      } catch (error) {
        return { success: false, error: error.message };
      }
    },
    { success: false }
  );

  return (
    <View>
      <form action={loginAction}>
        <TextInput name="email" placeholder="Email" />
        <TextInput name="password" secureTextEntry />
        <Button disabled={isPending}>
          {isPending ? 'Logging in...' : 'Login'}
        </Button>
      </form>
      {!state.success && state.error && (
        <Text style={{ color: 'red' }}>{state.error}</Text>
      )}
    </View>
  );
}
```

**When to use:** Form submission with loading/error states

### Pattern 2: TypeScript Instead of propTypes

```typescript
// Define prop types with TypeScript
type ButtonProps = {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
};

function Button({ title, onPress, disabled = false, variant = 'primary' }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={[styles.button, styles[variant]]}
    >
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
}
```

**When to use:** Always (propTypes removed in React 19)

### Pattern 3: New CSS for Visual Effects

```typescript
// Glowing button with outline and blend mode
function GlowButton({ title, onPress }) {
  return (
    <Pressable
      onPress={onPress}
      style={{
        backgroundColor: '#3b82f6',
        padding: 16,
        borderRadius: 8,
        // Outline doesn't affect layout
        outlineWidth: 2,
        outlineColor: '#60a5fa',
        outlineOffset: 4,
        // Blend with background
        mixBlendMode: 'screen',
        isolation: 'isolate'
      }}
    >
      <Text style={{ color: 'white', fontWeight: 'bold' }}>
        {title}
      </Text>
    </Pressable>
  );
}
```

**When to use:** Visual effects without affecting layout (New Architecture only)

---

## Using Bundled Resources

### Scripts (scripts/)

**check-rn-version.sh** - Detects React Native version and warns about architecture requirements

**Example Usage:**
```bash
./scripts/check-rn-version.sh
# Output: ✅ React Native 0.82 - New Architecture mandatory
# Output: ⚠️ React Native 0.75 - Upgrade to 0.76+ recommended
```

### References (references/)

**react-19-migration.md** - Detailed React 19 breaking changes and migration steps

**new-architecture-errors.md** - Common build errors when enabling New Architecture

**expo-sdk-52-breaking.md** - Expo SDK 52+ specific breaking changes

**When Claude should load these:** When encountering migration errors, build failures, or detailed React 19 questions

### Assets (assets/)

**new-arch-decision-tree.md** - Decision tree for choosing React Native version

**css-features-cheatsheet.md** - Complete examples of new CSS properties

---

## Expo SDK 52+ Specifics

### Breaking Changes

**JSC Removed from Expo Go:**
```json
// This no longer works in Expo Go (SDK 52+):
{
  "jsEngine": "jsc"  // ❌ Ignored, Hermes only
}
```

**Google Maps Removed from Expo Go (SDK 53+):**
```bash
# Must use custom dev client for Google Maps
npx expo install expo-dev-client
npx expo run:android
```

**Push Notifications Warning:**
Expo Go shows warnings for push notifications - use custom dev client for production testing.

### New Features (SDK 52)

**expo/fetch (WinterCG-compliant):**
```typescript
import { fetch } from 'expo/fetch';

// Standards-compliant fetch for Workers/Edge runtimes
const response = await fetch('https://api.example.com/data');
```

**React Navigation v7:**
```bash
npm install @react-navigation/native@^7.0.0
```

---

## Official Documentation

- **React Native**: https://reactnative.dev
- **Expo**: https://docs.expo.dev
- **React 19**: https://react.dev/blog/2024/04/25/react-19-upgrade-guide
- **New Architecture**: https://reactnative.dev/docs/new-architecture-intro
- **Upgrade Helper**: https://react-native-community.github.io/upgrade-helper/
- **Context7 Library ID**: /facebook/react-native

---

## Package Versions (Verified 2026-01-21)

**Build Tool Requirements (SDK 54+):**
- **Xcode**: Minimum 16.1, Xcode 16 recommended
- **Node.js**: Minimum 20.19.4
- **iOS Deployment Target**: iOS 15.1+

**Source:** [Expo SDK 54 Changelog](https://expo.dev/changelog/sdk-54)

```json
{
  "dependencies": {
    "react": "^19.2.3",
    "react-native": "^0.81.5",
    "expo": "~54.0.31",
    "@react-navigation/native": "^7.0.0",
    "@reduxjs/toolkit": "^2.0.0",
    "react-i18next": "^15.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "typescript": "^5.7.0"
  }
}
```

---

## Troubleshooting

### Problem: Build fails with "Fabric component descriptor not found"
**Solution:** Library not compatible with New Architecture. Check library docs for New Architecture support, or use interop layer (0.76-0.81 only).

### Problem: "propTypes is not a function" error
**Solution:** React 19 removed propTypes. Use TypeScript for type checking instead. Run `npx @codemod/react-19 upgrade`.

### Problem: console.log() not showing in Metro terminal
**Solution:** Metro log forwarding removed in 0.77. Use React Native DevTools Console (press 'j') or `npx expo start --client-logs` (temporary workaround).

### Problem: Swift AppDelegate errors during iOS build
**Solution:** Add `RCTAppDependencyProvider.sharedInstance()` to AppDelegate.swift. See Swift migration section.

### Problem: Redux store crashes on startup
**Solution:** Use Redux Toolkit instead of legacy `redux` + `redux-thunk`. Install `@reduxjs/toolkit`.

### Problem: Can't disable New Architecture in 0.82+
**Solution:** New Architecture is mandatory in 0.82+. If you need legacy, stay on 0.81 or earlier (not recommended).

---

## Complete Setup Checklist

Use this checklist to verify your setup:

- [ ] React Native 0.76+ or Expo SDK 52+ installed
- [ ] New Architecture enabled (automatic in 0.82+)
- [ ] Hermes engine enabled (default)
- [ ] React 19 migration complete (no propTypes, no forwardRef)
- [ ] TypeScript configured for type checking
- [ ] React Native DevTools accessible (press 'j')
- [ ] No deep imports (`react-native/Libraries/*`)
- [ ] Redux Toolkit (not legacy redux)
- [ ] react-i18next (not i18n-js)
- [ ] iOS builds successfully (Swift template if new project)
- [ ] Android builds successfully
- [ ] Dev server runs without errors
- [ ] All navigation/state management working

---

**Questions? Issues?**

1. Check `references/new-architecture-errors.md` for build errors
2. Check `references/react-19-migration.md` for React 19 issues
3. Check official docs: https://reactnative.dev/docs/new-architecture-intro
4. Ensure New Architecture is enabled (mandatory in 0.82+)
5. Verify all dependencies support New Architecture

---

**Knowledge Gap Filled:** This skill covers React Native updates from December 2024+ that LLMs won't know about. Without this skill, Claude would suggest deprecated APIs, removed features, and outdated patterns.
