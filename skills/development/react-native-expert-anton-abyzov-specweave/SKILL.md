---
description: React Native and Expo architect and expert. Architecture, setup, Metro bundler, native modules, New Architecture (Fabric, Turbo Modules, JSI), Expo Router, offline-first, performance, debugging. Use for mobile app architecture, RN setup, build issues, or debugging.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# React Native Expert - Architecture, Setup, Build, Debug, Performance

Elite mobile application architect and hands-on expert specializing in **React Native** and **Expo**. Covers the full spectrum from system design and scalable architecture to environment setup, Metro bundler, native modules, device testing, performance optimization, and debugging. Deep expertise in the New Architecture (Fabric, Turbo Modules, JSI) and modern React concurrent features.

## Fetching Current Documentation

**Before providing version-specific guidance, verify current versions.** Version numbers in static documentation become stale immediately. React Native releases every ~8 weeks. Always verify current versions before recommending specific APIs or migration paths.

For library documentation, use WebSearch or install Context7 manually: `claude plugin install context7@claude-plugins-official`

---

## Part 1: Architecture

### Architecture Principles

1. **Feature-based structure** over type-based (group by domain, not by file type)
2. **Unidirectional data flow** with clear state boundaries
3. **Platform abstraction** to isolate iOS/Android specifics
4. **Offline-first** for mobile reliability
5. **Lazy loading** screens and heavy modules for startup performance

### Recommended Project Structure

```
src/
├── app/                    # Expo Router screens (file-based routing)
│   ├── _layout.tsx
│   ├── (tabs)/
│   ├── (auth)/
│   └── [...missing].tsx
├── features/               # Feature modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── stores/
│   │   └── types.ts
│   ├── feed/
│   └── profile/
├── shared/                 # Shared utilities
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── utils/
├── providers/              # Context providers (theme, auth, query)
└── constants/
```

### State Management Selection Guide

| Solution | Use When | Persistence |
|----------|----------|-------------|
| Zustand | Most apps, simple global state | AsyncStorage via middleware |
| TanStack Query | Server state, caching, pagination | Built-in cache |
| Jotai | Fine-grained atomic state | AsyncStorage atoms |
| Legend State | High-frequency updates, real-time sync | Built-in persistence |

**Rule of thumb**: Use TanStack Query for server state + Zustand for client state. Avoid Redux unless team already uses it.

### Offline-First Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────┐
│  UI Layer   │────▶│  Data Layer  │────▶│   API   │
│ (React)     │◀────│  (Cache +    │◀────│ (REST/  │
│             │     │   Queue)     │     │  GQL)   │
└─────────────┘     └──────────────┘     └─────────┘
                         │
                    ┌────▼────┐
                    │ SQLite  │
                    │ or MMKV │
                    └─────────┘
```

**Key patterns:**
- Read from local cache first, sync in background
- Queue writes when offline, replay on reconnect
- Use optimistic updates for perceived performance
- Conflict resolution: last-write-wins or CRDTs

---

## Part 2: Setup and Environment

### Quick Setup Commands

#### Expo (Recommended)

```bash
# Create new project
npx create-expo-app@latest MyProject
cd MyProject
npx expo start

# Development build (custom native code)
npx expo install expo-dev-client
eas build --profile development --platform ios
```

#### React Native CLI

```bash
# Create project (New Architecture enabled by default)
npx @react-native-community/cli init MyProject
cd MyProject

# Install iOS deps with New Architecture
cd ios && RCT_NEW_ARCH_ENABLED=1 pod install && cd ..

# Run
npm run ios
npm run android
```

### Environment Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Node.js | 20.x | 22 LTS |
| React Native | 0.76+ | Latest stable |
| Expo SDK | 52+ | Latest stable |
| Xcode | 16.1 | Latest stable |
| Android SDK | 34 | 35 |
| CocoaPods | 1.14 | 1.15+ |

**Always verify current versions before advising.**

### Environment Variables

```bash
# ~/.zshrc or ~/.bash_profile
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# Reload
source ~/.zshrc
```

### Health Check

```bash
node --version      # 20+
xcodebuild -version # 16.1+
pod --version       # 1.15+
adb --version
watchman version
eas --version       # Expo
```

---

## Part 3: Monorepo & Metro Configuration

### Monorepo Project Structure

```
my-monorepo/
├── package.json              # workspaces: ["apps/*", "packages/*"]
├── apps/
│   ├── mobile/               # React Native / Expo app
│   │   ├── app/              # Expo Router screens
│   │   ├── metro.config.js   # ← Critical: must configure for monorepo
│   │   ├── tsconfig.json     # Path aliases (editor only)
│   │   └── package.json      # depends on @myapp/shared
│   └── web/                  # Next.js / Vite web app
├── packages/
│   ├── shared/               # @myapp/shared — shared types, utils, API client
│   │   ├── src/
│   │   └── package.json      # "name": "@myapp/shared"
│   └── ui/                   # @myapp/ui — shared components
```

### Metro Configuration for Monorepos

Metro does NOT follow symlinks or resolve workspace packages by default. You must configure it explicitly.

#### Expo Projects (Recommended)

```javascript
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

// Find the monorepo root (where root package.json with workspaces lives)
const monorepoRoot = path.resolve(__dirname, '../..');

const config = getDefaultConfig(__dirname);

// 1. Watch all files in the monorepo (so Metro sees shared packages)
config.watchFolders = [monorepoRoot];

// 2. Tell Metro where to find node_modules (handles hoisted deps)
config.resolver.nodeModulesPaths = [
  path.resolve(__dirname, 'node_modules'),       // app-level
  path.resolve(monorepoRoot, 'node_modules'),     // hoisted root
];

// 3. Ensure react/react-native resolve from the app (avoid duplicates)
config.resolver.extraNodeModules = {
  'react': path.resolve(__dirname, 'node_modules/react'),
  'react-native': path.resolve(__dirname, 'node_modules/react-native'),
};

module.exports = config;
```

#### Bare React Native Projects

```javascript
// metro.config.js
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');
const path = require('path');

const monorepoRoot = path.resolve(__dirname, '../..');

const config = {
  watchFolders: [monorepoRoot],
  resolver: {
    nodeModulesPaths: [
      path.resolve(__dirname, 'node_modules'),
      path.resolve(monorepoRoot, 'node_modules'),
    ],
    // Prevent duplicate React instances
    extraNodeModules: {
      'react': path.resolve(__dirname, 'node_modules/react'),
      'react-native': path.resolve(__dirname, 'node_modules/react-native'),
    },
    // Handle symlinks (yarn/pnpm workspaces create symlinks)
    unstable_enableSymlinks: true,
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

### TypeScript Path Aliases vs Metro Resolver

**TypeScript `paths`** only affect the editor and type checker — Metro ignores them entirely. You need BOTH:

```jsonc
// tsconfig.json — for editor intellisense and tsc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@myapp/shared": ["../../packages/shared/src"],
      "@myapp/shared/*": ["../../packages/shared/src/*"],
      "@/*": ["./src/*"]
    }
  }
}
```

```javascript
// metro.config.js — for actual runtime bundling
config.resolver.extraNodeModules = {
  '@myapp/shared': path.resolve(monorepoRoot, 'packages/shared/src'),
};
// OR use a custom resolver:
config.resolver.resolveRequest = (context, moduleName, platform) => {
  if (moduleName.startsWith('@myapp/shared')) {
    const subPath = moduleName.replace('@myapp/shared', '');
    return context.resolveRequest(
      context,
      path.resolve(monorepoRoot, 'packages/shared/src') + subPath,
      platform
    );
  }
  return context.resolveRequest(context, moduleName, platform);
};
```

### Package Manager Workspace Setup

```jsonc
// Root package.json (yarn/npm workspaces)
{
  "private": true,
  "workspaces": ["apps/*", "packages/*"]
}

// pnpm-workspace.yaml (pnpm)
// packages:
//   - "apps/*"
//   - "packages/*"
```

```jsonc
// packages/shared/package.json
{
  "name": "@myapp/shared",
  "main": "src/index.ts",      // Point to source for Metro (not dist)
  "types": "src/index.ts"
}
```

```jsonc
// apps/mobile/package.json
{
  "dependencies": {
    "@myapp/shared": "*"        // workspace:* for pnpm
  }
}
```

**Important**: For Metro bundling, point shared package `main` to **source** (`src/index.ts`), not compiled output. Metro transpiles everything itself.

### Common Monorepo Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `Unable to resolve module @myapp/shared` | Metro can't see workspace package | Add `watchFolders` pointing to monorepo root |
| `Unable to resolve module react` (duplicate) | Multiple React copies in node_modules | Pin via `extraNodeModules` to app's copy |
| Module works in web but not mobile | Webpack resolves workspaces; Metro doesn't | Configure `metro.config.js` resolver |
| Types resolve but runtime fails | tsconfig `paths` ≠ Metro resolver | Configure both tsconfig AND metro.config.js |
| `ENOENT` on symlinked packages | Metro doesn't follow symlinks by default | Set `unstable_enableSymlinks: true` |
| Hoisted deps not found | Dependencies hoisted to root node_modules | Add root `node_modules` to `nodeModulesPaths` |

---

## Part 3b: Common Build Issues

### Metro Cache Issues

```bash
# Clear everything
watchman watch-del-all
npx react-native start --reset-cache

# Expo
npx expo start --clear
```

### iOS Pod Issues

```bash
# Nuclear option
cd ios && rm -rf build Pods Podfile.lock && pod install && cd ..
```

### Android Gradle Issues

```bash
cd android && ./gradlew clean && cd ..
```

### Metro Resolution Errors

**"Unable to resolve module X"** — Systematic debugging:

```bash
# 1. Verify the package exists and is installed
ls node_modules/@myapp/shared 2>/dev/null || echo "NOT in app node_modules"
ls ../../node_modules/@myapp/shared 2>/dev/null || echo "NOT in root node_modules"

# 2. Check if it's a symlink (workspaces create these)
ls -la node_modules/@myapp/ 2>/dev/null

# 3. Verify metro.config.js has watchFolders and nodeModulesPaths
cat metro.config.js

# 4. Check the shared package's main/module entry point
cat ../../packages/shared/package.json | grep -E '"main"|"module"|"exports"'

# 5. Clear cache and restart
watchman watch-del-all && npx expo start --clear
```

**"Unable to resolve module X from Y: X could not be found within the project or in these directories: node_modules"**

This error means Metro's resolver checked its configured paths and found nothing. Checklist:
1. Is `watchFolders` set to include the directory containing the package?
2. Is `nodeModulesPaths` set to include all relevant `node_modules` directories?
3. Does the package's `package.json` have a valid `main` field pointing to an existing file?
4. If using pnpm, is `unstable_enableSymlinks: true` set in the resolver?
5. After config changes, always run `npx expo start --clear` (Metro caches aggressively)

---

## Part 4: New Architecture (Fabric, Turbo Modules, JSI)

### Fabric (New Rendering System)

Fabric replaces the old UIManager bridge with a synchronous, C++ rendering pipeline.

```typescript
// Fabric is enabled by default in Expo SDK 52+
// In app.json / app.config.ts:
{
  "expo": {
    "newArchEnabled": true
  }
}
```

**Benefits of Fabric:**
- Synchronous layout calculations (no bridge delay)
- Concurrent rendering support (React 18 features)
- Shared C++ core between iOS and Android
- Better gesture handling and animations

### Turbo Modules

TurboModules replace the old Native Modules system with lazy-loaded, type-safe native interfaces.

```typescript
// specs/NativeCalculator.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  add(a: number, b: number): number;
  getDeviceModel(): string;
  getBatteryLevel(): Promise<number>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeCalculator');
```

**Key advantages over old Native Modules:**
- Lazy initialization (loaded only when first accessed)
- Type-safe bridge via codegen
- Synchronous method calls possible via JSI

### JSI (JavaScript Interface)

JSI provides direct communication between JS and native code without JSON serialization.

```cpp
// C++ JSI host object example
class DeviceInfoHostObject : public jsi::HostObject {
public:
  jsi::Value get(jsi::Runtime& rt, const jsi::PropNameID& name) override {
    auto propName = name.utf8(rt);
    if (propName == "model") {
      return jsi::String::createFromUtf8(rt, getDeviceModel());
    }
    return jsi::Value::undefined();
  }
};
```

### Linking Native Code

```bash
# Auto-linking (RN 0.60+)
cd ios && pod install
cd android && ./gradlew build
```

---

## Part 5: Performance Optimization

### Enable Hermes

```json
// android/app/build.gradle
hermesEnabled = true

// iOS: Already default with New Architecture
```

### Optimized List Rendering

```typescript
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={80}
  keyExtractor={(item) => item.id}
/>
```

### Image Optimization

```typescript
// Expo Image (recommended)
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  placeholder={{ blurhash: 'LGF5]+Yk^6#M@-5c,1J5@[or[Q6.' }}
  contentFit="cover"
  transition={200}
  cachePolicy="memory-disk"
/>
```

### Performance Monitoring

```typescript
import { PerformanceObserver } from 'react-native-performance';

new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
}).observe({ entryTypes: ['measure'] });
```

### Bundle Size Analysis

```bash
# Analyze bundle with expo-atlas
EXPO_ATLAS=1 npx expo export --platform ios
npx expo-atlas path/to/atlas-file
```

### Performance Checklist

- [ ] Use FlashList over FlatList for long lists
- [ ] Memoize expensive computations with useMemo/React.memo
- [ ] Use expo-image instead of Image for caching and blurhash
- [ ] Profile with React DevTools Profiler
- [ ] Enable Hermes engine
- [ ] Avoid inline object/function creation in render
- [ ] Use useCallback for event handlers passed to children
- [ ] Lazy-load heavy screens with React.lazy + Suspense

---

## Part 6: Device Testing

### iOS Simulator

```bash
# List devices
xcrun simctl list devices

# Boot specific device
xcrun simctl boot "iPhone 16 Pro"

# Run on device
npx react-native run-ios --device "My iPhone"
```

### Android Emulator

```bash
# List AVDs
emulator -list-avds

# Run emulator
emulator -avd Pixel_8_API_35

# Run on device
npx react-native run-android --deviceId <device-id>
```

---

## Part 7: Debugging

### Chrome DevTools / New Debugger

```bash
# RN 0.73+: Press 'j' in Metro to open debugger
# Replaces deprecated Flipper
```

### React DevTools

```bash
npx react-devtools
```

### Common Debug Patterns

```typescript
// Native crash on iOS
// Check: Xcode → Device and Simulators → View Device Logs

// Bridge error
// Clear Metro cache and rebuild
watchman watch-del-all
npx react-native start --reset-cache

// Android build failure
cd android && ./gradlew clean && cd ..
```

### Network Debugging

```typescript
// In development, use React Native Debugger or Flipper Network plugin
// For production, use a logging service (Sentry, LogRocket)

// Quick debug proxy
if (__DEV__) {
  // XMLHttpRequest interceptor for logging
  const originalXHROpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(...args) {
    console.log('XHR:', args[0], args[1]);
    return originalXHROpen.apply(this, args);
  };
}
```

---

## Part 8: Navigation with Expo Router

### Directory Structure

```
app/
  _layout.tsx          # Root layout (providers, auth)
  index.tsx            # Home screen (/)
  (tabs)/
    _layout.tsx        # Tab navigator
    home.tsx           # /home tab
    profile.tsx        # /profile tab
  (auth)/
    _layout.tsx        # Auth group layout
    login.tsx          # /login
    register.tsx       # /register
  settings/
    _layout.tsx        # Stack navigator for settings
    index.tsx          # /settings
    [id].tsx           # /settings/:id (dynamic route)
  [...missing].tsx     # 404 catch-all
```

### Root Layout with Providers

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { ThemeProvider } from '../providers/ThemeProvider';
import { AuthProvider } from '../providers/AuthProvider';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="(tabs)" />
            <Stack.Screen name="(auth)" />
            <Stack.Screen name="settings" options={{ presentation: 'modal' }} />
          </Stack>
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

### Navigation Patterns

```typescript
import { router, useLocalSearchParams, Link } from 'expo-router';

// Imperative navigation
router.push('/settings/123');
router.replace('/home');
router.back();
router.navigate('/profile');

// Typed params
const { id } = useLocalSearchParams<{ id: string }>();

// Declarative link
<Link href="/settings/456" asChild>
  <Pressable><Text>Go to Settings</Text></Pressable>
</Link>
```

---

## Part 9: State Management Patterns

### Zustand (Recommended for Most Apps)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthStore {
  token: string | null;
  user: User | null;
  login: (token: string, user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      login: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### Jotai (Atomic State)

```typescript
import { atom, useAtom } from 'jotai';
import { atomWithStorage, createJSONStorage } from 'jotai/utils';
import AsyncStorage from '@react-native-async-storage/async-storage';

const storage = createJSONStorage<string>(() => AsyncStorage);
const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light', storage);

const userAtom = atom<User | null>(null);
const isLoggedInAtom = atom((get) => get(userAtom) !== null);
```

---

## Part 10: Testing

### Unit and Component Testing

```typescript
// Jest + React Native Testing Library
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { LoginScreen } from '../screens/LoginScreen';

describe('LoginScreen', () => {
  it('shows error for invalid email', async () => {
    const { getByPlaceholderText, getByText } = render(<LoginScreen />);
    fireEvent.changeText(getByPlaceholderText('Email'), 'invalid');
    fireEvent.press(getByText('Login'));
    await waitFor(() => {
      expect(getByText('Invalid email address')).toBeTruthy();
    });
  });
});
```

### E2E Testing with Detox

```javascript
// e2e/login.test.ts
describe('Login Flow', () => {
  beforeAll(async () => { await device.launchApp(); });
  beforeEach(async () => { await device.reloadReactNative(); });

  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('user@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    await expect(element(by.id('home-screen'))).toBeVisible();
  });
});
```

---

## Related Skills

- `appstore` - **Recommended**: App Store Connect automation via `asc` CLI (TestFlight, submissions, metadata, signing)
- `expo` - Expo managed workflow, EAS Build/Submit, OTA updates, config plugins
- `mobile-testing` - Comprehensive testing strategies (XCTest, Espresso, Detox, Maestro)
- `deep-linking-push` - Deep linking and push notification details
