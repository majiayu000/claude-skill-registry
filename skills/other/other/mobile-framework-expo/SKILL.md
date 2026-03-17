---
name: mobile-framework-expo
description: Expo managed workflow
---

# Expo Development Patterns

> **Quick Guide:** Build production-ready React Native apps with Expo. Use managed workflow with Continuous Native Generation for most projects, Expo Router for file-based navigation, and EAS for builds/updates. Development builds replace Expo Go for production testing.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use development builds for production testing - Expo Go is for prototyping only)**

**(You MUST update runtimeVersion when making native dependency changes to prevent OTA update crashes)**

**(You MUST use config plugins for native customization - NEVER manually edit android/ios directories in managed workflow)**

**(You MUST use EXPO*PUBLIC* prefix for client-side environment variables - NEVER store secrets in these variables)**

</critical_requirements>

---

**Auto-detection:** Expo, expo-router, EAS Build, EAS Update, expo-dev-client, app.config.js, app.json, expo prebuild, npx expo, eas.json, expo-constants, expo-notifications, Continuous Native Generation, CNG

**When to use:**

- Starting new React Native projects with rapid development needs
- Building apps that need OTA (over-the-air) updates
- Using file-based routing similar to Next.js
- Managing native code without maintaining android/ios directories
- Deploying to app stores with cloud builds

**Key patterns covered:**

- Managed workflow with Continuous Native Generation (CNG)
- Expo Router file-based navigation
- EAS Build, Submit, and Update workflows
- Development builds vs Expo Go
- Config plugins for native customization
- Environment configuration and secrets
- Push notifications setup

**When NOT to use:**

- Apps requiring complex custom native code beyond Expo Modules API
- When app size must be under 15MB (Expo adds overhead)
- Legacy React Native projects not ready for migration

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Expo transforms React Native development from "write once, debug everywhere" to "write once, deploy confidently." The key insight is that **most apps don't need direct native access** - they need well-maintained native modules with consistent APIs.

**Core principles:**

1. **Managed by default** - Let Expo handle native complexity; prebuild only when necessary
2. **Continuous Native Generation** - Treat android/ios as build artifacts, not source code
3. **Development builds for truth** - Expo Go is for learning; development builds show production reality
4. **OTA for velocity** - Ship JavaScript updates without app store delays
5. **Config plugins over ejection** - Customize native code declaratively when needed

**Mental model:**

Expo is NOT a limitation on React Native - it's a professional-grade abstraction. You can always drop down to native code via Expo Modules API or prebuild, but most apps never need to.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Project Configuration

Configure Expo projects using `app.json` (static) or `app.config.js` (dynamic).

#### Static Configuration

```typescript
// app.json - Static configuration
{
  "expo": {
    "name": "MyApp",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "newArchEnabled": true,
    "splash": {
      "image": "./assets/splash-icon.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.example.myapp"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.example.myapp"
    },
    "plugins": [
      "expo-router"
    ]
  }
}
```

#### Dynamic Configuration

```typescript
// app.config.ts - Dynamic configuration with TypeScript
import type { ExpoConfig, ConfigContext } from "expo/config";

const IS_PRODUCTION = process.env.APP_ENV === "production";
const APP_VERSION = "1.0.0";
const BUILD_NUMBER = 1;

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: IS_PRODUCTION ? "MyApp" : "MyApp (Dev)",
  slug: "my-app",
  version: APP_VERSION,
  ios: {
    supportsTablet: true,
    bundleIdentifier: IS_PRODUCTION
      ? "com.example.myapp"
      : "com.example.myapp.dev",
    buildNumber: String(BUILD_NUMBER),
  },
  android: {
    package: IS_PRODUCTION ? "com.example.myapp" : "com.example.myapp.dev",
    versionCode: BUILD_NUMBER,
    adaptiveIcon: {
      foregroundImage: "./assets/adaptive-icon.png",
      backgroundColor: "#ffffff",
    },
  },
  extra: {
    eas: {
      projectId: process.env.EAS_PROJECT_ID,
    },
  },
});
```

**Why good:** Named constants prevent magic numbers, dynamic config enables environment-specific builds, TypeScript provides type safety

---

### Pattern 2: Config Plugins for Native Customization

Modify native code declaratively without maintaining android/ios directories.

```typescript
// app.config.ts - Config plugins
import type { ExpoConfig } from "expo/config";

const IOS_DEPLOYMENT_TARGET = "15.1";
const ANDROID_COMPILE_SDK = 35;
const ANDROID_TARGET_SDK = 35;
const ANDROID_MIN_SDK = 24;

export default (): ExpoConfig => ({
  name: "MyApp",
  slug: "my-app",
  plugins: [
    // Camera with custom permission message
    [
      "expo-camera",
      {
        cameraPermission:
          "Allow $(PRODUCT_NAME) to access your camera for photos.",
        microphonePermission:
          "Allow $(PRODUCT_NAME) to access your microphone for video.",
      },
    ],
    // Build properties for SDK versions
    [
      "expo-build-properties",
      {
        android: {
          compileSdkVersion: ANDROID_COMPILE_SDK,
          targetSdkVersion: ANDROID_TARGET_SDK,
          minSdkVersion: ANDROID_MIN_SDK,
        },
        ios: {
          deploymentTarget: IOS_DEPLOYMENT_TARGET,
        },
      },
    ],
    // Location with background permission
    [
      "expo-location",
      {
        locationAlwaysAndWhenInUsePermission:
          "Allow $(PRODUCT_NAME) to use your location for navigation.",
      },
    ],
  ],
});
```

**Why good:** Declarative native configuration survives `expo prebuild --clean`, config plugins compose, permissions are explicit

---

### Pattern 3: Environment Variables

Use `EXPO_PUBLIC_` prefix for client-side variables.

```typescript
// .env
EXPO_PUBLIC_API_URL=https://api.example.com
EXPO_PUBLIC_SENTRY_DSN=https://xxxx@sentry.io/xxxx

// .env.local (gitignored - local overrides)
EXPO_PUBLIC_API_URL=http://localhost:3000
```

```typescript
// config/env.ts - Type-safe environment access
const API_URL = process.env.EXPO_PUBLIC_API_URL;
const SENTRY_DSN = process.env.EXPO_PUBLIC_SENTRY_DSN;

// IMPORTANT: These patterns DON'T work - Metro requires static analysis
// const { EXPO_PUBLIC_API_URL } = process.env;  // BAD
// process.env['EXPO_PUBLIC_API_URL'];           // BAD

if (!API_URL) {
  throw new Error("EXPO_PUBLIC_API_URL is required");
}

export const env = {
  apiUrl: API_URL,
  sentryDsn: SENTRY_DSN,
} as const;
```

```typescript
// Using expo-constants for runtime config
import Constants from "expo-constants";

// Access extra config from app.config.ts
const projectId = Constants.expoConfig?.extra?.eas?.projectId;
const environment = Constants.expoConfig?.extra?.environment;
```

**Why good:** Type-safe access with validation, clear separation of public/private config, build-time substitution for security

---

### Pattern 4: Development Builds

Create custom development builds with `expo-dev-client`.

```bash
# Install dev client
npx expo install expo-dev-client

# Create development build (cloud)
eas build --profile development --platform ios
eas build --profile development --platform android

# Create development build (local)
npx expo run:ios
npx expo run:android
```

```typescript
// eas.json - Development build configuration
{
  "cli": {
    "version": ">= 7.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      },
      "android": {
        "buildType": "apk"
      }
    },
    "development-device": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": false
      }
    }
  }
}
```

**Why good:** Development builds include your native dependencies, support push notifications and deep links, allow testing app icons and splash screens

---

### Pattern 5: Asset Management

Load fonts and images efficiently.

```typescript
// app/_layout.tsx - Font loading with splash screen
import { useFonts } from "expo-font";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import { Stack } from "expo-router";

const SPLASH_HIDE_DELAY_MS = 0;

// Prevent splash screen from auto-hiding
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [fontsLoaded, fontError] = useFonts({
    "Inter-Regular": require("../assets/fonts/Inter-Regular.ttf"),
    "Inter-Medium": require("../assets/fonts/Inter-Medium.ttf"),
    "Inter-Bold": require("../assets/fonts/Inter-Bold.ttf"),
  });

  useEffect(() => {
    if (fontsLoaded || fontError) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded, fontError]);

  if (!fontsLoaded && !fontError) {
    return null;
  }

  return <Stack />;
}
```

```typescript
// Using expo-image for optimized image loading
import { Image } from "expo-image";

const BLUR_HASH = "L6PZfSi_.AyE_3t7t7R**0o#DgR4";
const IMAGE_TRANSITION_MS = 200;

interface OptimizedImageProps {
  uri: string;
  width: number;
  height: number;
}

export function OptimizedImage({ uri, width, height }: OptimizedImageProps) {
  return (
    <Image
      source={{ uri }}
      placeholder={BLUR_HASH}
      contentFit="cover"
      transition={IMAGE_TRANSITION_MS}
      cachePolicy="memory-disk"
      style={{ width, height }}
    />
  );
}
```

**Why good:** SplashScreen prevents flash of unstyled content, expo-image provides caching and blur hash placeholders, named constants for configuration

</patterns>

---

<integration>

## Integration Guide

**Expo works with your existing mobile development knowledge:**

**Navigation:**

- Use Expo Router for file-based routing (Next.js-like experience)
- See [examples/router.md](examples/router.md) for patterns

**Build and Deploy:**

- Use EAS Build for cloud compilation
- Use EAS Submit for app store submission
- Use EAS Update for OTA updates
- See [examples/eas.md](examples/eas.md) for workflows

**Native Code:**

- Use config plugins for most native customization
- Use Expo Modules API for custom native modules
- Prebuild to bare workflow only when absolutely necessary

**State Management:**

- Expo works with any React state solution
- Use AsyncStorage for persistent client storage

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use development builds for production testing - Expo Go is for prototyping only)**

**(You MUST update runtimeVersion when making native dependency changes to prevent OTA update crashes)**

**(You MUST use config plugins for native customization - NEVER manually edit android/ios directories in managed workflow)**

**(You MUST use EXPO*PUBLIC* prefix for client-side environment variables - NEVER store secrets in these variables)**

**Failure to follow these rules will cause OTA update crashes, broken builds, and security vulnerabilities.**

</critical_reminders>
