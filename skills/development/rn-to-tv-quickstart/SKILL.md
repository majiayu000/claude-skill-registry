---
name: rn-to-tv-quickstart
displayName: "RN to TV Quick Start"
description: "Quick start guide for experienced React Native developers transitioning to TV app development. Covers Fire OS, Android TV, Apple TV (tvOS), Vega OS, and Web TV platforms. Focuses on what's different from mobile: spatial navigation, remote controls, focus management, and 10-foot UI patterns. Skip the basics - get your first TV app running fast."
keywords: ["getting-started", "quickstart", "mobile-to-tv", "transition", "first-tv-app", "new-to-tv", "beginner-tv", "setup-guide", "react-native-tv"]
author: "Giovanni Laquidara"
---

# React Native to TV: Quick Start Guide

You know React Native. Here's what's different for TV.

**Official Docs:**
- Expo TV: https://docs.expo.dev/guides/building-for-tv/
- Vega SDK: https://developer.amazon.com/docs/vega/latest/build-apps-overview.html

---

## The Big 5 Differences from Mobile

### 1. No Touch - Everything is Remote/D-pad

On mobile: Users tap buttons
On TV: Users navigate with D-pad (up/down/left/right) + select

```typescript
// Mobile: TouchableOpacity, Pressable just work
// TV: You need spatial navigation

import { SpatialNavigationNode } from 'react-tv-space-navigation';

const TVButton = ({ onPress, children }) => {
  return (
    <SpatialNavigationNode onSelect={onPress}>
      {({ isFocused }) => (
        <View style={[styles.button, isFocused && styles.focused]}>
          {children}
        </View>
      )}
    </SpatialNavigationNode>
  );
};
```

**Key library**: [react-tv-space-navigation](https://github.com/bamlab/react-tv-space-navigation)

**Important**: v6.0.0+ uses a different API than v5.x:
- v6: `<SpatialNavigationRoot>` wrapper + `<SpatialNavigationNode>` components
- v5: `SpatialNavigation.init()` + `useFocusable()` hook

### 2. Focus is King

Every interactive element MUST have a visible focus state. Users can't tap what they can't see.

```typescript
const styles = StyleSheet.create({
  button: {
    padding: 16,
    backgroundColor: '#333',
  },
  // CRITICAL: Always show what's focused
  focused: {
    backgroundColor: '#555',
    borderWidth: 3,
    borderColor: '#fff',
    transform: [{ scale: 1.05 }],
  },
});
```

**Focus Indicators (Use at least 2):**
- ✅ Border (3px+ white/colored)
- ✅ Scale (1.05x - 1.1x)
- ✅ Background color change
- ✅ Shadow/glow effect
- ✅ Opacity change

**Testing Focus:**
- Navigate with D-pad/arrow keys
- Focused element should be immediately obvious
- Test in a dark room (10-foot viewing distance)
- All interactive elements must be reachable
  button: {
    padding: 16,
    backgroundColor: '#333',
  },
  // CRITICAL: Always show what's focused
  focused: {
    backgroundColor: '#555',
    borderWidth: 3,
    borderColor: '#fff',
    transform: [{ scale: 1.05 }],
  },
});
```

### 3. 10-Foot UI (Bigger Everything)

Users sit 10 feet away. What works on mobile is too small.

| Element | Mobile | TV |
|---------|--------|-----|
| Body text | 14-16px | 24-32px |
| Buttons | 44px height | 60-80px height |
| Touch targets | 44x44px | 80x80px+ |
| Margins | 16px | 48px+ |

### 4. Safe Zones (TV Overscan)

TVs crop edges. Keep content away from borders.

```typescript
const safeZones = {
  horizontal: 48,  // Left/right padding
  vertical: 27,    // Top/bottom padding
};
```

### 5. Landscape Only

TV apps are always landscape. Configure in app.json:
```json
{ "expo": { "orientation": "landscape" } }
```

---

## Platform Quick Reference

| Platform | Technology | Remote Events |
|----------|------------|---------------|
| Android TV | Expo + react-native-tvos | KeyEvent |
| Apple TV | Expo + react-native-tvos | TVEventHandler |
| Fire TV FOS | Expo + react-native-tvos | KeyEvent |
| Fire TV Vega | Amazon Vega SDK | Kepler TVEventHandler |
| Web TV | React Native Web | Keyboard events |

---

## Prerequisites

### For Android TV / Fire TV (Fire OS)
- Node.js LTS (macOS or Linux)
- Android Studio Iguana or later
- Android SDK API 31+ with TV system image
- Android TV emulator configured

### For Apple TV (tvOS)
- Node.js LTS on macOS
- Xcode 16+
- tvOS SDK 17+ (install via `xcodebuild -downloadAllPlatforms`)

### For Fire TV Vega OS
- Amazon Vega SDK installed (see Vega section below)

---

## Complete Project Setup

This guide creates a production-ready monorepo structure supporting all TV platforms.

> **Claude will ask for your app name and package ID when setting up.**

### Step 1: Create Monorepo Structure

```bash
# Create project root
mkdir <PROJECT_NAME> && cd <PROJECT_NAME>

# Initialize Yarn
yarn init -y
yarn set version stable

# Create directory structure
mkdir -p apps packages/shared-ui/src
```

### Step 2: Configure Root package.json

Create `package.json`:
```json
{
  "name": "@<PROJECT_NAME>/monorepo",
  "version": "1.0.0",
  "private": true,
  "packageManager": "yarn@4.5.0",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "yarn workspace @<PROJECT_NAME>/expo-multi-tv start",
    "dev:android": "yarn workspace @<PROJECT_NAME>/expo-multi-tv android",
    "dev:ios": "yarn workspace @<PROJECT_NAME>/expo-multi-tv ios",
    "dev:web": "yarn workspace @<PROJECT_NAME>/expo-multi-tv web",
    "dev:vega": "yarn workspace @<PROJECT_NAME>/vega start",
    "build:vega": "yarn workspace @<PROJECT_NAME>/vega build",
    "lint:all": "yarn workspaces foreach -pt run lint",
    "typecheck": "yarn workspaces foreach -pt run typecheck"
  },
  "resolutions": {
    "metro-source-map": "0.80.12"
  }
}
```

> **CRITICAL**: The `metro-source-map` resolution fixes babel plugin errors in monorepos.

### Step 3: Create Shared TypeScript Config

Create `tsconfig.base.json`:
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "CommonJS",
    "lib": ["ES2021"],
    "jsx": "react-native",
    "strict": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### Step 4: Create Root Babel Config

Create `babel.config.js`:
```javascript
const path = require('path');

module.exports = function (api) {
  api.cache(true);

  let reanimatedPlugin;
  try {
    reanimatedPlugin = require.resolve('react-native-reanimated/plugin', {
      paths: [path.join(__dirname, 'apps/expo-multi-tv/node_modules')]
    });
  } catch (e) {
    reanimatedPlugin = null;
  }

  return {
    presets: ['babel-preset-expo'],
    plugins: reanimatedPlugin ? [reanimatedPlugin] : [],
  };
};
```

### Step 5: Create Expo TV App

```bash
cd apps

# Create Expo TV project
npx create-expo-app@latest expo-multi-tv -e with-tv

cd expo-multi-tv
```

Update `apps/expo-multi-tv/package.json`:
```json
{
  "name": "@<PROJECT_NAME>/expo-multi-tv",
  "dependencies": {
    "@<PROJECT_NAME>/shared-ui": "*"
  }
}
```

Create `apps/expo-multi-tv/metro.config.js`:
```javascript
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

module.exports = config;
```

### Step 6: Add Vega App (Fire TV Vega OS)

```bash
# Create and enter vega directory first (files generate in current directory)
mkdir -p apps/vega
cd apps/vega

# Generate Vega project
vega project generate -n <APP_NAME> --template helloWorld

npm install
```

Update `apps/vega/package.json`:
```json
{
  "name": "@<PROJECT_NAME>/vega",
  "scripts": {
    "build:debug": "react-native build-kepler --build-type Debug",
    "build:release": "react-native build-kepler --build-type Release"
  },
  "dependencies": {
    "@<PROJECT_NAME>/shared-ui": "*",
    "react-tv-space-navigation": "^6.0.0-beta1"
  }
}
```

**CRITICAL: Update `apps/vega/manifest.toml`** - Add the `[processes]` section or the app will crash on launch:
```toml
schema-version = 1

[package]
title = "My App"
version = "0.1.0"
id = "com.mycompany.myapp"

[components]
[[components.interactive]]
id = "com.mycompany.myapp.main"
runtime-module = "/com.amazon.kepler.keplerscript.runtime.loader_2@IKeplerScript_2_0"
launch-type = "singleton"
categories = ["com.amazon.category.main"]

# REQUIRED: Without this section, the app crashes immediately on launch
[processes]
[[processes.group]]
component-ids = ["com.mycompany.myapp.main"]
```

Create `apps/vega/metro.config.js`:
```javascript
const path = require('path');
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = {
  watchFolders: [workspaceRoot],
  resolver: {
    nodeModulesPaths: [
      path.resolve(projectRoot, 'node_modules'),
      path.resolve(workspaceRoot, 'node_modules'),
    ],
    sourceExts: ['kepler.tsx', 'kepler.ts', 'tsx', 'ts', 'js', 'jsx', 'json'],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

### Step 6b: Configure Spatial Navigation for Vega

`react-tv-space-navigation` works with Vega but requires a remote control configuration.

**Create `packages/shared-ui/src/app/remote-control/SupportedKeys.ts`:**
```typescript
export enum SupportedKeys {
  Up = 'up', Down = 'down', Left = 'left', Right = 'right',
  Enter = 'enter', Back = 'back', PlayPause = 'playPause',
  Rewind = 'rewind', FastForward = 'fastForward',
}
```

**Create `packages/shared-ui/src/app/remote-control/RemoteControlManager.kepler.ts`:**
```typescript
import { SupportedKeys } from './SupportedKeys';

const EVENT_MAP: Record<string, SupportedKeys> = {
  left: SupportedKeys.Left, right: SupportedKeys.Right,
  down: SupportedKeys.Down, up: SupportedKeys.Up,
  select: SupportedKeys.Enter, back: SupportedKeys.Back,
};

class RemoteControlManager {
  private listeners = new Set<(e: SupportedKeys) => void>();
  constructor() {
    const { TVEventHandler } = require('react-native');
    new TVEventHandler().enable(this, (_: any, e: any) => {
      if (e.eventKeyAction === 0 || e.eventKeyAction === undefined) {
        const key = EVENT_MAP[e.eventType];
        if (key) this.listeners.forEach(l => l(key));
      }
    });
  }
  addKeydownListener = (l: (e: SupportedKeys) => void) => { this.listeners.add(l); return l; };
  removeKeydownListener = (l: (e: SupportedKeys) => void) => { this.listeners.delete(l); };
}
export default new RemoteControlManager();
```

**Create `packages/shared-ui/src/app/configureRemoteControl.ts`:**
```typescript
import { Directions, SpatialNavigation } from 'react-tv-space-navigation';
import { SupportedKeys } from './remote-control/SupportedKeys';
import RemoteControlManager from './remote-control/RemoteControlManager';

SpatialNavigation.configureRemoteControl({
  remoteControlSubscriber: (callback) => {
    const map = {
      [SupportedKeys.Right]: Directions.RIGHT, [SupportedKeys.Left]: Directions.LEFT,
      [SupportedKeys.Up]: Directions.UP, [SupportedKeys.Down]: Directions.DOWN,
      [SupportedKeys.Enter]: Directions.ENTER,
    };
    return RemoteControlManager.addKeydownListener((k) => callback(map[k] ?? null));
  },
  remoteControlUnsubscriber: (l) => RemoteControlManager.removeKeydownListener(l),
});
```

**Import in Vega App.tsx:**
```typescript
import '../../../packages/shared-ui/src/app/configureRemoteControl';
```

### Step 7: Create Shared UI Package

Create `packages/shared-ui/package.json`:
```json
{
  "name": "@<PROJECT_NAME>/shared-ui",
  "version": "1.0.0",
  "main": "src/index.ts",
  "types": "src/index.ts",
  "peerDependencies": {
    "react": "*",
    "react-native": "*"
  }
}
```

Create `packages/shared-ui/tsconfig.json`:
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

Create `packages/shared-ui/src/index.ts`:
```typescript
// Theme
export * from './theme';

// Components
export * from './components/FocusablePressable';

// Hooks
export * from './hooks/useScale';
```

### Step 8: Create Theme System

Create `packages/shared-ui/src/theme/index.ts`:
```typescript
export const colors = {
  primary: '#E50914',
  background: '#141414',
  card: '#2F2F2F',
  text: '#FFFFFF',
  textSecondary: '#B3B3B3',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const safeZones = {
  horizontal: 48,
  vertical: 27,
};
```

### Step 9: Create useScale Hook

Create `packages/shared-ui/src/hooks/useScale.ts`:
```typescript
import { Dimensions } from 'react-native';

const BASE_WIDTH = 1920;
const BASE_HEIGHT = 1080;

export const useScale = () => {
  const { width, height } = Dimensions.get('window');
  const scaleWidth = width / BASE_WIDTH;
  const scaleHeight = height / BASE_HEIGHT;
  const scale = Math.min(scaleWidth, scaleHeight);

  return {
    scale: (size: number) => size * scale,
    width,
    height,
  };
};
```

### Step 10: Create FocusablePressable Component

Create `packages/shared-ui/src/components/FocusablePressable.tsx`:
```typescript
import React from 'react';
import { Pressable, StyleSheet, ViewStyle } from 'react-native';
import { SpatialNavigationNode } from 'react-tv-space-navigation';

interface FocusablePressableProps {
  children: React.ReactNode;
  onPress?: () => void;
  style?: ViewStyle;
  focusedStyle?: ViewStyle;
}

export const FocusablePressable: React.FC<FocusablePressableProps> = ({
  children,
  onPress,
  style,
  focusedStyle,
}) => {
  return (
    <SpatialNavigationNode onSelect={onPress}>
      {({ isFocused }) => (
        <Pressable
          onPress={onPress}
          style={[
            styles.container,
            style,
            isFocused && styles.focused,
            isFocused && focusedStyle,
          ]}
        >
          {children}
        </Pressable>
      )}
    </SpatialNavigationNode>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  focused: {
    borderWidth: 3,
    borderColor: '#fff',
    transform: [{ scale: 1.05 }],
  },
});
```

**Important**: Pass `onPress` to both `SpatialNavigationNode` (for remote/D-pad) AND `Pressable` (for touch/click).

**Focus Highlighting**: The `isFocused` prop from the render function is used to apply visual feedback:
```typescript
{({ isFocused }) => (
  <Pressable
    onPress={onPress}
    style={[
      styles.container,
      style,
      isFocused && styles.focused,  // Apply focus styles
      isFocused && focusedStyle,    // Allow custom focus styles
    ]}
  >
    {children}
  </Pressable>
)}
```

The default focus styles provide:
- **3px white border** - Clear visual boundary
- **1.05x scale** - Subtle size increase
- **Custom focusedStyle prop** - Override with app-specific styles

**Best Practices for Focus:**
- Always use high-contrast colors (white/yellow on dark backgrounds)
- Combine multiple indicators (border + scale + color)
- Test on actual TV hardware (emulators may not show true visibility)
- Ensure focus is visible from 10 feet away

### Step 11: Install Dependencies and Run

```bash
# From project root
cd ../..
yarn install

# Run on platforms
yarn dev:android    # Android TV / Fire TV FOS
yarn dev:ios        # Apple TV
yarn dev:web        # Web TV
yarn dev:vega       # Fire TV Vega OS
```

---

## Final Project Structure

```
<PROJECT_NAME>/
├── apps/
│   ├── expo-multi-tv/      # Android TV, Apple TV, Fire TV FOS, Web
│   │   ├── App.tsx         # Main app entry point
│   │   ├── app.json
│   │   ├── metro.config.js
│   │   └── package.json
│   └── vega/               # Fire TV Vega OS
│       ├── App.tsx
│       ├── metro.config.js
│       └── package.json
├── packages/
│   └── shared-ui/          # Shared components & utilities
│       ├── src/
│       │   ├── components/
│       │   ├── hooks/
│       │   ├── theme/
│       │   └── index.ts
│       ├── package.json
│       └── tsconfig.json
├── babel.config.js
├── package.json
├── tsconfig.base.json
└── yarn.lock
```

---

## Platform-Specific File Resolution

Metro bundler automatically resolves platform files:
- `.kepler.ts/tsx` - Fire TV Vega OS (highest priority for Vega)
- `.android.ts/tsx` - Android TV & Fire TV Fire OS
- `.ios.ts/tsx` - Apple TV (tvOS)
- `.web.ts/tsx` - Web platforms
- `.ts/tsx` - Default/shared implementation

**Example:**
```
RemoteControlManager.android.ts  → Android TV / Fire TV FOS
RemoteControlManager.ios.ts      → Apple TV
RemoteControlManager.kepler.ts   → Fire TV Vega
```

---

## Build Commands

### Expo TV App (Android TV, Apple TV, Fire TV FOS, Web)

```bash
yarn dev:android    # Run on Android TV emulator
yarn dev:ios        # Run on Apple TV simulator
yarn dev:web        # Run in browser

# Production builds
npx expo build:android
npx expo build:ios
npx expo export --platform web
```

### Vega App (Fire TV Vega OS)

```bash
yarn dev:vega       # Start Metro for Vega

# Build VPKG
vega build --arch armv7 --buildType release     # Fire TV Stick
vega build --arch aarch64 --buildType release   # Fire TV (ARM64)
vega build --arch x86_64 --buildType debug      # Virtual devices

# Deploy
vega device list
vega install --vpkg build/armv7-release/<APP_NAME>.vpkg
vega run --packageId <PACKAGE_ID>
```

---

## Common Build Issues & Solutions

### Java Version Error

**Error:** `Android Gradle plugin requires Java 17 to run. You are currently using Java 11.`

**Solution:** Create `android/gradle.properties`:
```properties
org.gradle.java.home=/path/to/java17
org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=1024m
hermesEnabled=true
android.useAndroidX=true
android.enableJetifier=true
```

### Metro Source Map Error (Monorepo)

**Error:** `Cannot find module 'metro-source-map/private/source-map'`

**Cause:** Expo's metro package expects a `private/` directory that doesn't exist in metro-source-map 0.80.x

**Solution:** Create symlinks after `yarn install`:
```bash
cd node_modules/metro-source-map
mkdir -p private/Consumer
ln -sf ../src/source-map.js private/source-map.js
for file in src/Consumer/*.js; do 
  ln -sf "../../$file" "private/Consumer/$(basename $file)"
done
```

**Better Solution:** Add to `package.json` scripts:
```json
{
  "scripts": {
    "postinstall": "node scripts/fix-metro-source-map.js"
  }
}
```

Create `scripts/fix-metro-source-map.js`:
```javascript
const fs = require('fs');
const path = require('path');

const metroSourceMapPath = path.join(__dirname, '../node_modules/metro-source-map');
const privatePath = path.join(metroSourceMapPath, 'private');
const consumerPath = path.join(privatePath, 'Consumer');

if (!fs.existsSync(privatePath)) {
  fs.mkdirSync(privatePath, { recursive: true });
}
if (!fs.existsSync(consumerPath)) {
  fs.mkdirSync(consumerPath, { recursive: true });
}

// Create source-map.js symlink
const sourceMapSrc = path.join(metroSourceMapPath, 'src/source-map.js');
const sourceMapDest = path.join(privatePath, 'source-map.js');
if (!fs.existsSync(sourceMapDest)) {
  fs.symlinkSync(path.relative(privatePath, sourceMapSrc), sourceMapDest);
}

// Create Consumer symlinks
const consumerSrcPath = path.join(metroSourceMapPath, 'src/Consumer');
const files = fs.readdirSync(consumerSrcPath).filter(f => f.endsWith('.js'));
files.forEach(file => {
  const src = path.join(consumerSrcPath, file);
  const dest = path.join(consumerPath, file);
  if (!fs.existsSync(dest)) {
    fs.symlinkSync(path.relative(consumerPath, src), dest);
  }
});

console.log('✓ Fixed metro-source-map private paths');
```

### App Entry Point Error (Monorepo)

**Error:** `Unable to resolve "../../App" from "node_modules/expo/AppEntry.js"`

**Cause:** In monorepo, Expo's default AppEntry.js looks for App.tsx at wrong path

**Solution:** Create `index.js` in app root:
```javascript
import { registerRootComponent } from 'expo';
import App from './App';

registerRootComponent(App);
```

This overrides Expo's default entry point and uses the correct relative path.

### react-tv-space-navigation API Error

**Error:** `TypeError: SpatialNavigation.init is not a function (it is undefined)`

**Cause:** react-tv-space-navigation v6.0.0+ has breaking API changes from v5.x

**v5.x API (OLD - Don't use):**
```typescript
import { SpatialNavigation, useFocusable } from 'react-tv-space-navigation';

// Initialize
SpatialNavigation.init({ debug: true });

// Use hook
const { ref, focused } = useFocusable({ onEnterPress: onPress });
```

**v6.0.0+ API (NEW - Use this):**
```typescript
import { SpatialNavigationRoot, SpatialNavigationNode } from 'react-tv-space-navigation';

// Wrap app
<SpatialNavigationRoot>
  <App />
</SpatialNavigationRoot>

// Use component with render prop
<SpatialNavigationNode onSelect={onPress}>
  {({ isFocused }) => (
    <View style={isFocused && styles.focused}>
      {children}
    </View>
  )}
</SpatialNavigationNode>
```

**Migration Steps:**
1. Remove `SpatialNavigation.init()` calls
2. Wrap root component in `<SpatialNavigationRoot>`
3. Replace `useFocusable()` with `<SpatialNavigationNode>` render prop
4. Change `focused` to `isFocused` in render prop
5. Change `onEnterPress` to `onSelect`

### Hermes Configuration Missing

**Error:** `Could not get unknown property 'hermesEnabled'`

**Solution:** Add to `android/gradle.properties`:
```properties
hermesEnabled=true
```

---

## Focus Management Troubleshooting

### Focus Not Visible

**Problem:** Can't see which element is focused

**Solutions:**
1. Increase border width: `borderWidth: 4` or higher
2. Use high-contrast colors: `borderColor: '#FFFF00'` (yellow)
3. Add multiple indicators:
```typescript
focused: {
  borderWidth: 4,
  borderColor: '#fff',
  transform: [{ scale: 1.1 }],
  backgroundColor: '#444',
  shadowColor: '#fff',
  shadowOffset: { width: 0, height: 0 },
  shadowOpacity: 0.8,
  shadowRadius: 10,
}
```

### Focus Not Moving Between Elements

**Problem:** D-pad navigation doesn't move focus

**Causes & Solutions:**
1. **Missing SpatialNavigationRoot**: Wrap entire app
2. **Elements not aligned**: Ensure buttons are in proper layout (Row/Column)
3. **Check console**: Look for spatial navigation warnings
4. **Test with multiple elements**: Need at least 2 focusable items

### Button Press Not Working

**Problem:** Focused button doesn't respond to Enter/Select

**Solution:** Ensure both `onSelect` AND `onPress` are set:
```typescript
<SpatialNavigationNode onSelect={handlePress}>
  {({ isFocused }) => (
    <Pressable onPress={handlePress}>  {/* Both needed! */}
```

---

## Common Mistakes (Don't Do These)

### ❌ Using Pressable without Focus Management
```typescript
// WRONG
<Pressable onPress={handlePress}><Text>Click</Text></Pressable>

// RIGHT - Use FocusablePressable from shared-ui
<FocusablePressable onPress={handlePress}><Text>Select</Text></FocusablePressable>
```

### ❌ Forgetting Safe Zones
```typescript
// WRONG - Content at edges
<View style={{ position: 'absolute', top: 0, left: 0 }}>

// RIGHT
<View style={{ position: 'absolute', top: 27, left: 48 }}>
```

### ❌ Small Touch Targets
```typescript
// WRONG - Too small for TV
<View style={{ width: 44, height: 44 }} />

// RIGHT
<View style={{ width: 80, height: 80 }} />
```

---

## Vega Troubleshooting

### App Crashes Immediately on Launch (Black Screen)

**Symptom:** App installs successfully, "Successfully launched" message appears, but app immediately crashes with black screen and no error.

**Cause:** Missing `[processes]` section in `manifest.toml`

**Fix:** Add to `apps/vega/manifest.toml`:
```toml
[processes]
[[processes.group]]
component-ids = ["com.yourcompany.yourapp.main"]
```

### Running on Vega Virtual Device

```bash
# Start simulator
vega simulator

# Check device is ready
vega device list

# Build and run
yarn build:release  # or build:debug
vega run-app build/aarch64-release/<APP_NAME>_aarch64.vpkg <PACKAGE_ID>

# Check if running
vega device is-app-running --appName <PACKAGE_ID>
```

---

## Testing Your TV App

### Android TV
```bash
# In Android Studio: Tools > Device Manager > Create Device > TV
yarn dev:android
```

### Apple TV
```bash
# In Xcode: Window > Devices and Simulators > Simulators
yarn dev:ios
```

### Web (with keyboard)
```bash
yarn dev:web
# Navigate with arrow keys, Enter to select
```

### Physical Devices
- Android TV: Enable developer mode, connect via ADB
- Fire TV: Enable ADB debugging in Settings
- Apple TV: Connect via Xcode

---

## Next Steps

1. **Add screens** - Create screens in `packages/shared-ui/src/screens/`
2. **Add navigation** - Set up React Navigation in shared-ui
3. **Add video player** - Use react-native-video (Expo) or VideoView (Vega)
4. **Handle remote events** - Create platform-specific RemoteControlManagers
5. **Test on real hardware** - Emulators don't show real performance

## Need More?

- **Full knowledge base**: Use the `multi-tv-builder` skill
- **Apple TV issues**: Use the `apple-tv-troubleshooter` skill
- **Movie/TV data API**: Use the `tmdb-integration` skill

## Reference Implementation

For a complete working example with all features implemented:
- **Sample repo**: https://github.com/AmazonAppDev/react-native-multi-tv-app-sample

Use this as a reference to see advanced patterns like video playback, navigation, and remote control handling.


---

# Android TV / Fire TV Runtime Troubleshooting

## TypeError: Cannot read property 'displayName' of undefined

**Symptoms:**
- App builds successfully but crashes immediately
- Metro shows: `ERROR TypeError: Cannot read property 'displayName' of undefined`
- App returns to launcher after brief flash

**Common Causes & Fixes:**

1. **Wrong import in index.js** (Most Common)
   ```javascript
   // ❌ WRONG - Named import when App uses default export
   import { App } from './App';
   
   // ✅ CORRECT - Default import
   import App from './App';
   ```

2. **Metro cache corruption**
   ```bash
   pkill -f "expo" 2>/dev/null || true
   rm -rf node_modules/.cache /tmp/metro-* /tmp/haste-map-*
   npx expo start --clear
   ```

3. **react-tv-space-navigation v6 missing configuration**
   ```typescript
   // Create src/configureRemoteControl.ts
   import { SpatialNavigation } from 'react-tv-space-navigation';
   
   SpatialNavigation.configureRemoteControl({
     remoteControlSubscriber: (callback) => () => {},
     remoteControlUnsubscriber: () => {},
   });
   ```

## Metro Bundler Connection Issues

**Symptoms:**
- `Couldn't connect to "ws://localhost:8081/message..."`
- App shows loading screen indefinitely

**Fixes:**
```bash
# Set up ADB reverse port forwarding
adb reverse tcp:8081 tcp:8081

# Verify emulator connection
adb devices -l

# Restart ADB if stale
adb kill-server && adb start-server
```

## Android TV Emulator Quick Commands

```bash
# Start emulator
emulator -avd Android_TV_720p -no-snapshot-load &

# Wait for boot
adb wait-for-device

# Force restart app
adb shell am force-stop <package_name>
adb shell am start -n <package_name>/.MainActivity

# Check logs for JS errors
adb logcat -d | grep -iE "(ReactNativeJS|error)" | tail -30
```

## Expo Go vs Development Builds

**Important:** TV apps should use **development builds**, not Expo Go.

```bash
# ❌ May cause SDK version issues on TV
npx expo start

# ✅ Correct for TV development
npx expo run:android
# or
npx expo start --dev-client
```


---

# Vega in Monorepo - Critical Setup

## Port Forwarding Required

Vega virtual devices need reverse port forwarding to connect to Metro:

```bash
# REQUIRED before launching app
vega device start-port-forwarding --port 8081 --forward false
```

Without this, the app shows a black screen because it can't fetch the JS bundle.

## React Version Conflicts (Expo + Vega)

If your monorepo has both Expo (React 19) and Vega (React 18), you'll get:
```
TypeError: Cannot read property 'ReactCurrentOwner' of undefined
```

**Fix:** Move root React packages before running Vega:
```bash
mv node_modules/react node_modules/react.bak
mv node_modules/react-native node_modules/react-native.bak
```

## Node.js 23 Compatibility

Node 23 breaks Metro's package exports. Fix by removing `exports` field:

```javascript
// Run this after yarn install
const fs = require('fs');
['metro', 'metro-source-map', 'metro-transform-worker', 'metro-runtime'].forEach(pkg => {
  const p = `node_modules/${pkg}/package.json`;
  if (fs.existsSync(p)) {
    const json = JSON.parse(fs.readFileSync(p));
    delete json.exports;
    fs.writeFileSync(p, JSON.stringify(json, null, 2));
  }
});
```

## Complete Vega Launch Sequence

```bash
# 1. Fix Metro (Node 23 only)
node fix-metro-exports.js

# 2. Move root React (monorepo only)
mv node_modules/react node_modules/react.bak

# 3. Start Metro
cd apps/vega && npm start

# 4. Port forwarding (new terminal)
vega device start-port-forwarding --port 8081 --forward false

# 5. Launch
vega device launch-app --appName com.yourcompany.app

# 6. Verify
vega device running-apps | grep yourapp
```
