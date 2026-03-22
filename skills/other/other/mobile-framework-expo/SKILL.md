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

**(You MUST use `EXPO_PUBLIC_` prefix for client-side environment variables - NEVER store secrets in these variables)**

</critical_requirements>

---

**Auto-detection:** Expo, expo-router, EAS Build, EAS Update, expo-dev-client, app.config.js, app.json, expo prebuild, npx expo, eas.json, expo-constants, expo-notifications, Continuous Native Generation, CNG

**When to use:**

- Starting new React Native projects with rapid development needs
- Building apps that need OTA (over-the-air) updates
- Using file-based routing with convention-over-configuration
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

### Pattern 1: Dynamic Configuration with `app.config.ts`

Use `app.config.ts` for environment-specific builds. Use named constants for SDK versions and build numbers.

```typescript
// app.config.ts - Environment-aware config
const IS_PRODUCTION = process.env.APP_ENV === "production";
const BUILD_NUMBER = 1;

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: IS_PRODUCTION ? "MyApp" : "MyApp (Dev)",
  ios: {
    bundleIdentifier: IS_PRODUCTION ? "com.app" : "com.app.dev",
    buildNumber: String(BUILD_NUMBER),
  },
  android: {
    package: IS_PRODUCTION ? "com.app" : "com.app.dev",
    versionCode: BUILD_NUMBER,
  },
});
```

> Full examples: [examples/core.md](examples/core.md) - App Configuration section

---

### Pattern 2: Config Plugins for Native Customization

Modify native code declaratively -- changes survive `expo prebuild --clean`. Use config plugins for permissions, SDK versions, and native settings.

```typescript
// app.config.ts plugins array
plugins: [
  [
    "expo-camera",
    { cameraPermission: "Allow $(PRODUCT_NAME) to access your camera." },
  ],
  [
    "expo-build-properties",
    { android: { minSdkVersion: 24 }, ios: { deploymentTarget: "15.1" } },
  ],
];
```

> Full examples: [examples/core.md](examples/core.md) - Config Plugins section

---

### Pattern 3: Environment Variables

Use `EXPO_PUBLIC_` prefix for client-side variables. Metro requires direct property access -- destructuring and bracket notation don't work.

```typescript
// MUST use direct access - Metro static analysis requirement
const API_URL = process.env.EXPO_PUBLIC_API_URL; // Works
// const { EXPO_PUBLIC_API_URL } = process.env;  // BROKEN - undefined at runtime
```

> Full examples: [examples/core.md](examples/core.md) - Environment Variables section

---

### Pattern 4: Development Builds

Use `expo-dev-client` for production-accurate testing. Expo Go is for prototyping only -- it lacks your native dependencies, push notifications, and accurate splash screens.

```bash
# Cloud build
eas build --profile development --platform ios
# Local build
npx expo run:ios
```

> Full configuration: [examples/eas.md](examples/eas.md) - Development Builds section

---

### Pattern 5: Asset Management

Block splash screen while loading fonts, use `expo-image` for remote images with blur hash placeholders and disk caching.

```typescript
SplashScreen.preventAutoHideAsync();
// Load fonts, then call SplashScreen.hideAsync() when ready
```

> Full examples: [examples/core.md](examples/core.md) - Font Loading and Image Handling sections

</patterns>

---

<red_flags>

## RED FLAGS

- **Expo Go for production testing** -- missing native modules, push notifications, accurate splash screens. Always use development builds.
- **Not updating runtimeVersion after native changes** -- OTA updates crash on apps with incompatible native code. Use `"fingerprint"` policy for automatic detection.
- **Storing secrets in `EXPO_PUBLIC_` variables** -- embedded in JS bundle, visible to anyone who decompiles. Use EAS Secrets and backend proxies.
- **Manually editing android/ios directories** -- changes lost on `expo prebuild --clean`. Use config plugins.
- **Destructuring `process.env`** -- Metro requires direct property access (`process.env.EXPO_PUBLIC_*`). Destructuring and bracket notation produce `undefined`.
- **Using `expo-av`** -- removed in SDK 55. Migrate to `expo-video` and `expo-audio`.
- **Legacy Architecture** -- removed after SDK 54. React Native 0.82+ requires New Architecture.

> Full anti-patterns and gotchas: [reference.md](reference.md)

</red_flags>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Project config, environment variables, fonts, images
- [examples/router.md](examples/router.md) - File-based routing, tabs, auth flows, modals
- [examples/eas.md](examples/eas.md) - Cloud builds, app store submission, OTA updates
- [reference.md](reference.md) - Decision frameworks, SDK compatibility, anti-patterns

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use development builds for production testing - Expo Go is for prototyping only)**

**(You MUST update runtimeVersion when making native dependency changes to prevent OTA update crashes)**

**(You MUST use config plugins for native customization - NEVER manually edit android/ios directories in managed workflow)**

**(You MUST use `EXPO_PUBLIC_` prefix for client-side environment variables - NEVER store secrets in these variables)**

**Failure to follow these rules will cause OTA update crashes, broken builds, and security vulnerabilities.**

</critical_reminders>
