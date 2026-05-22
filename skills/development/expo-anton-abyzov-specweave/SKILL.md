---
description: Expo and React Native New Architecture expert. Expo SDK 52+, Fabric, TurboModules, JSI, EAS Build/Submit, Expo Router, Expo Modules API, OTA updates, push notifications. Use for Expo projects, managed workflow, EAS pipelines, or migrating from bare RN.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Expo / React Native New Architecture Expert

Comprehensive expertise in **Expo SDK 52+**, the **managed workflow**, and the **React Native New Architecture** (Fabric, TurboModules, JSI). Covers the full lifecycle from project creation through App Store and Play Store submission using EAS.

## Fetching Current Documentation

**Before providing version-specific guidance, verify current versions.** Expo SDK releases every ~3 months and React Native every ~8 weeks. Static version numbers go stale quickly.

For library documentation, use WebSearch or install Context7 manually: `claude plugin install context7@claude-plugins-official`

## Expo SDK 52+ and the Managed Workflow

### Project Creation

```bash
# Create a new Expo project (always use latest)
npx create-expo-app@latest MyApp
cd MyApp

# Start development server
npx expo start

# Create with a specific template
npx create-expo-app@latest MyApp --template tabs
npx create-expo-app@latest MyApp --template blank-typescript
```

### Managed vs Bare Workflow

| Aspect | Managed Workflow | Bare Workflow |
|--------|-----------------|---------------|
| Native code | Handled by Expo | You manage it |
| Build system | EAS Build | Xcode / Gradle |
| Config | `app.json` / `app.config.ts` | Native project files |
| Updates | OTA via expo-updates | Manual or CodePush |
| Recommended | Yes (for 95% of apps) | Only when necessary |

**Key principle**: Stay managed as long as possible. Use **config plugins** and **Expo Modules API** instead of ejecting.

### app.config.ts (Dynamic Configuration)

```typescript
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: 'MyApp',
  slug: 'my-app',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  scheme: 'myapp',
  newArchEnabled: true,
  ios: {
    bundleIdentifier: 'com.example.myapp',
    supportsTablet: true,
    infoPlist: {
      NSCameraUsageDescription: 'Camera access for profile photos',
    },
  },
  android: {
    adaptiveIcon: {
      foregroundImage: './assets/adaptive-icon.png',
      backgroundColor: '#ffffff',
    },
    package: 'com.example.myapp',
    permissions: ['CAMERA', 'ACCESS_FINE_LOCATION'],
  },
  plugins: [
    'expo-router',
    'expo-notifications',
    ['expo-camera', { cameraPermission: 'Allow camera access' }],
  ],
});
```

## React Native New Architecture

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

### TurboModules

TurboModules replace the old Native Modules system with lazy-loaded, type-safe native interfaces.

```typescript
// specs/NativeDeviceInfo.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  getDeviceModel(): string;
  getBatteryLevel(): Promise<number>;
  getStorageInfo(): Promise<{ total: number; free: number }>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeDeviceInfo');
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

## Expo Monorepo Setup

### Monorepo with Expo (Workspaces)

Expo supports monorepos but requires explicit Metro configuration. Metro does NOT resolve workspace packages or follow symlinks by default.

### Step-by-Step Setup

#### 1. Root package.json

```jsonc
{
  "private": true,
  "workspaces": ["apps/*", "packages/*"]
}
```

#### 2. Shared Package

```jsonc
// packages/shared/package.json
{
  "name": "@myapp/shared",
  "main": "src/index.ts",    // Point to SOURCE, not dist — Metro transpiles
  "types": "src/index.ts"
}
```

#### 3. Mobile App Dependencies

```jsonc
// apps/mobile/package.json
{
  "dependencies": {
    "@myapp/shared": "*"      // workspace:* for pnpm
  }
}
```

#### 4. Metro Config (Critical)

```javascript
// apps/mobile/metro.config.js
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const monorepoRoot = path.resolve(__dirname, '../..');
const config = getDefaultConfig(__dirname);

// Watch the entire monorepo
config.watchFolders = [monorepoRoot];

// Resolve node_modules from both app and root (for hoisted deps)
config.resolver.nodeModulesPaths = [
  path.resolve(__dirname, 'node_modules'),
  path.resolve(monorepoRoot, 'node_modules'),
];

// Prevent duplicate React/RN instances (crashes at runtime)
config.resolver.extraNodeModules = {
  'react': path.resolve(__dirname, 'node_modules/react'),
  'react-native': path.resolve(__dirname, 'node_modules/react-native'),
  'react-dom': path.resolve(__dirname, 'node_modules/react-dom'),
};

// Enable symlink resolution (workspace packages are symlinked)
config.resolver.unstable_enableSymlinks = true;

module.exports = config;
```

#### 5. TypeScript Path Aliases (Editor Only)

```jsonc
// apps/mobile/tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@myapp/shared": ["../../packages/shared/src"],
      "@myapp/shared/*": ["../../packages/shared/src/*"]
    }
  }
}
```

**Important**: `tsconfig.json` paths only affect the editor and `tsc`. Metro uses its own resolver configured in `metro.config.js`.

### EAS Build with Monorepos

```jsonc
// apps/mobile/eas.json
{
  "build": {
    "production": {
      "node": "20.0.0"
    }
  }
}
```

EAS Build automatically detects monorepo structure. If using pnpm:

```bash
# Set install command for EAS
eas secret:create --name EAS_BUILD_INSTALL_COMMAND --value "pnpm install --frozen-lockfile"
```

For yarn workspaces, EAS uses `yarn install` by default — no extra config needed.

### Troubleshooting Monorepo Issues

| Error | Fix |
|-------|-----|
| `Unable to resolve module @myapp/shared` | Add `watchFolders: [monorepoRoot]` to metro.config.js |
| `Unable to resolve module react` (duplicate) | Set `extraNodeModules.react` to app's copy |
| Module found by TS but crashes at runtime | Configure Metro resolver (tsconfig paths ≠ Metro) |
| `ENOENT` errors on workspace packages | Set `resolver.unstable_enableSymlinks: true` |
| EAS Build fails with missing packages | Verify workspace setup, add `EAS_BUILD_INSTALL_COMMAND` for pnpm |

---

## EAS Build and EAS Submit

### EAS Configuration

```json
// eas.json
{
  "cli": { "version": ">= 12.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal",
      "ios": { "resourceClass": "m-medium" }
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "TEAM_ID"
      },
      "android": {
        "serviceAccountKeyPath": "./google-services-key.json",
        "track": "production"
      }
    }
  }
}
```

### Build Commands

```bash
# Development build (includes dev client)
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview build (internal distribution)
eas build --profile preview --platform all

# Production build
eas build --profile production --platform all

# Submit to stores
eas submit --platform ios --latest
eas submit --platform android --latest

# Build and submit in one step
eas build --profile production --platform ios --auto-submit
```

### EAS Environment Variables

```bash
# Set secrets (never commit these)
eas secret:create --name SENTRY_DSN --value "https://..." --scope project
eas secret:create --name API_KEY --value "sk-..." --scope project

# List secrets
eas secret:list
```

## Expo Router (File-Based Routing)

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

## Expo Modules API

Build native modules that work with the managed workflow without ejecting.

```typescript
// modules/my-module/index.ts
import { NativeModule, requireNativeModule } from 'expo-modules-core';

interface MyModuleEvents {
  onDataReceived: { data: string };
}

declare class MyModuleType extends NativeModule<MyModuleEvents> {
  greet(name: string): string;
  fetchDataAsync(): Promise<string>;
}

export default requireNativeModule<MyModuleType>('MyModule');
```

```swift
// modules/my-module/ios/MyModule.swift
import ExpoModulesCore

public class MyModule: Module {
  public func definition() -> ModuleDefinition {
    Name("MyModule")

    Function("greet") { (name: String) -> String in
      return "Hello, \(name)!"
    }

    AsyncFunction("fetchDataAsync") { (promise: Promise) in
      DispatchQueue.global().async {
        let result = performExpensiveWork()
        promise.resolve(result)
      }
    }

    Events("onDataReceived")
  }
}
```

## State Management

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

## OTA Updates with expo-updates

```typescript
// app.config.ts
export default {
  updates: {
    url: 'https://u.expo.dev/your-project-id',
    fallbackToCacheTimeout: 0,
    checkAutomatically: 'ON_LOAD',
  },
  runtimeVersion: {
    policy: 'appVersion', // or 'fingerprint' for auto-detection
  },
};
```

```typescript
// Manual update check
import * as Updates from 'expo-updates';

async function checkForUpdates() {
  if (__DEV__) return; // Skip in development

  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync();
  }
}
```

```bash
# Publish OTA update
eas update --branch production --message "Fix checkout bug"

# Preview channel mapping
eas channel:edit production --branch production
eas channel:edit preview --branch staging
```

## Push Notifications with expo-notifications

```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

async function registerForPushNotifications(): Promise<string | null> {
  if (!Device.isDevice) return null;

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') return null;

  const projectId = Constants.expoConfig?.extra?.eas?.projectId;
  const token = (await Notifications.getExpoPushTokenAsync({ projectId })).data;
  return token;
}
```

## Deep Linking and Universal Links

```typescript
// app.config.ts
export default {
  scheme: 'myapp',
  ios: {
    associatedDomains: ['applinks:example.com'],
  },
  android: {
    intentFilters: [
      {
        action: 'VIEW',
        autoVerify: true,
        data: [{ scheme: 'https', host: 'example.com', pathPrefix: '/app' }],
        category: ['BROWSABLE', 'DEFAULT'],
      },
    ],
  },
};
```

## Performance Optimization

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
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  placeholder={{ blurhash: 'LGF5]+Yk^6#M@-5c,1J5@[or[Q6.' }}
  contentFit="cover"
  transition={200}
  cachePolicy="memory-disk"
/>
```

### Bundle Size Analysis

```bash
# Analyze bundle with expo-atlas
EXPO_ATLAS=1 npx expo export --platform ios
npx expo-atlas path/to/atlas-file
```

## Migration from Bare RN to Expo

```bash
# 1. Install expo in existing project
npx install-expo-modules@latest

# 2. Create app.json
npx expo config --type public

# 3. Install Expo-compatible libraries
npx expo install react-native-reanimated react-native-gesture-handler

# 4. Enable prebuild (generates native projects from config)
npx expo prebuild --clean

# 5. Use EAS Build instead of manual native builds
eas build --profile development --platform all
```

## Testing

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

## Config Plugins

Modify native project files without ejecting from the managed workflow.

```typescript
// plugins/withCustomSplash.ts
import { ConfigPlugin, withAndroidStyles } from 'expo/config-plugins';

const withCustomSplash: ConfigPlugin = (config) => {
  return withAndroidStyles(config, (modConfig) => {
    const styles = modConfig.modResults;
    // Modify Android styles.xml
    return modConfig;
  });
};

export default withCustomSplash;
```

```typescript
// app.config.ts
export default {
  plugins: [
    './plugins/withCustomSplash',
    ['expo-build-properties', {
      ios: { deploymentTarget: '15.0', flipper: false },
      android: { compileSdkVersion: 35, targetSdkVersion: 35, minSdkVersion: 24 },
    }],
  ],
};
```

## App Store and Play Store Submission with EAS

### Pre-Submission Checklist

1. **Version bump**: Update `version` in app.config.ts
2. **Build**: `eas build --profile production --platform all`
3. **Test**: Download and test the production build
4. **Submit**: `eas submit --platform all --latest`

### iOS-Specific Requirements

```json
// eas.json submit config
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "developer@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCDE12345"
      }
    }
  }
}
```

### Android-Specific Requirements

```bash
# Generate upload key (first time only)
eas credentials --platform android

# Submit with service account
eas submit --platform android --latest
```

## Related Skills

- `appstore` - **Recommended**: App Store Connect automation via `asc` CLI (TestFlight, submissions, metadata, signing)
- `react-native-expert` - Architecture decisions and patterns
- `react-native-expert` - Bare RN setup, Metro, debugging
- `mobile-testing` - Comprehensive testing strategies
- `deep-linking-push` - Deep linking and push notification details
