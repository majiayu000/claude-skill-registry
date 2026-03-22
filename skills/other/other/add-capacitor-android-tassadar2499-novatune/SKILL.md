---
description: Add Capacitor wrapper for NovaTune Player Android app with secure storage (project)
---
# Add Capacitor Android Skill

Package the NovaTune Player as an Android application using Capacitor with secure token storage.

## Overview

This skill adds Capacitor to `apps/player` for:
- Android app builds
- Secure refresh token storage
- Native Android integration
- Deep linking support

## Project Structure

```
apps/player/
├── capacitor.config.ts
├── android/                    (generated)
│   ├── app/
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── AndroidManifest.xml
│   │   │       └── res/
│   │   └── build.gradle
│   └── build.gradle
├── src/
│   └── ...                     (Vue app source)
└── dist/                       (built web app)
```

## Capacitor Configuration

### capacitor.config.ts

```typescript
import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'dev.novatune.player',
  appName: 'NovaTune',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    // For development only:
    // url: 'http://10.0.2.2:5173',
    // cleartext: true,
  },
  plugins: {
    SecureStoragePlugin: {
      // Uses Android Keystore by default
    },
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#1a1a1a',
      showSpinner: false,
    },
    StatusBar: {
      style: 'dark',
      backgroundColor: '#1a1a1a',
    },
  },
  android: {
    allowMixedContent: false,
    webContentsDebuggingEnabled: false, // Set to true for development
  },
};

export default config;
```

## Setup Steps

### 1. Install Capacitor

```bash
cd apps/player

# Core Capacitor packages
pnpm add @capacitor/core
pnpm add -D @capacitor/cli

# Initialize Capacitor
npx cap init NovaTune dev.novatune.player --web-dir=dist

# Add Android platform
pnpm add @capacitor/android
npx cap add android
```

### 2. Install Plugins

```bash
# Secure storage for tokens
pnpm add capacitor-secure-storage-plugin

# Optional: native features
pnpm add @capacitor/status-bar
pnpm add @capacitor/splash-screen
pnpm add @capacitor/app
```

## Secure Storage Integration

### packages/core/src/auth/storage-capacitor.ts

```typescript
import { SecureStoragePlugin } from 'capacitor-secure-storage-plugin';

const REFRESH_TOKEN_KEY = 'refresh_token';

export const capacitorStorage = {
  async getRefreshToken(): Promise<string | null> {
    try {
      const { value } = await SecureStoragePlugin.get({ key: REFRESH_TOKEN_KEY });
      return value;
    } catch (error) {
      // Key not found returns error
      return null;
    }
  },

  async setRefreshToken(token: string): Promise<void> {
    await SecureStoragePlugin.set({
      key: REFRESH_TOKEN_KEY,
      value: token,
    });
  },

  async clearRefreshToken(): Promise<void> {
    try {
      await SecureStoragePlugin.remove({ key: REFRESH_TOKEN_KEY });
    } catch {
      // Ignore if key doesn't exist
    }
  },
};
```

### packages/core/src/auth/storage.ts

```typescript
import { Capacitor } from '@capacitor/core';

export interface TokenStorage {
  getRefreshToken(): Promise<string | null>;
  setRefreshToken(token: string): Promise<void>;
  clearRefreshToken(): Promise<void>;
}

export async function createTokenStorage(): Promise<TokenStorage> {
  // Native mobile (Capacitor)
  if (Capacitor.isNativePlatform()) {
    const { capacitorStorage } = await import('./storage-capacitor');
    return capacitorStorage;
  }

  // Electron
  if (typeof window !== 'undefined' && window.electronAPI) {
    return {
      getRefreshToken: () => window.electronAPI.getSecureToken(),
      setRefreshToken: (token) => window.electronAPI.setSecureToken(token),
      clearRefreshToken: () => window.electronAPI.deleteSecureToken(),
    };
  }

  // Web fallback
  return {
    getRefreshToken: () => Promise.resolve(localStorage.getItem('refresh_token')),
    setRefreshToken: (token) => {
      localStorage.setItem('refresh_token', token);
      return Promise.resolve();
    },
    clearRefreshToken: () => {
      localStorage.removeItem('refresh_token');
      return Promise.resolve();
    },
  };
}
```

## Android Manifest Updates

### android/app/src/main/AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="false">

        <activity
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|smallestScreenSize|screenLayout|uiMode"
            android:exported="true"
            android:launchMode="singleTask"
            android:name=".MainActivity"
            android:theme="@style/AppTheme.NoActionBarLaunch">

            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>

            <!-- Deep linking -->
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https" android:host="novatune.dev" />
            </intent-filter>

        </activity>

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>

    </application>

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />

</manifest>
```

## Build Workflow

### Development

```bash
# Build web app
pnpm build

# Sync to Android project
npx cap sync android

# Open in Android Studio
npx cap open android

# Or run directly
npx cap run android
```

### Production Build

```bash
# Build optimized web app
pnpm build

# Sync to Android
npx cap sync android

# Build APK/AAB in Android Studio
# or use Gradle directly:
cd android
./gradlew assembleRelease    # APK
./gradlew bundleRelease      # AAB for Play Store
```

## Scripts Addition

### apps/player/package.json

```json
{
  "scripts": {
    "android:sync": "cap sync android",
    "android:open": "cap open android",
    "android:run": "cap run android",
    "android:build": "pnpm build && cap sync android"
  }
}
```

## Network Configuration

### android/app/src/main/res/xml/network_security_config.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <!-- Development only -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
    </domain-config>
</network-security-config>
```

## Splash Screen

### android/app/src/main/res/values/styles.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
    </style>

    <style name="AppTheme.NoActionBarLaunch" parent="Theme.SplashScreen">
        <item name="android:background">@color/splash_background</item>
    </style>
</resources>
```

### android/app/src/main/res/values/colors.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#6366f1</color>
    <color name="colorPrimaryDark">#4f46e5</color>
    <color name="colorAccent">#8b5cf6</color>
    <color name="splash_background">#1a1a1a</color>
</resources>
```

## Background Audio (Future Enhancement)

For background audio playback, consider adding:

```typescript
// Future: Background audio service
import { App } from '@capacitor/app';

App.addListener('appStateChange', ({ isActive }) => {
  if (!isActive) {
    // App went to background
    // Audio continues via native service
  }
});
```

## Implementation Checklist

- [ ] Initialize Capacitor in apps/player
- [ ] Add Android platform
- [ ] Install secure storage plugin
- [ ] Update token storage to use platform detection
- [ ] Configure Android Manifest
- [ ] Add network security config
- [ ] Create app icons and splash screen
- [ ] Test secure storage on device
- [ ] Test audio playback
- [ ] Configure release signing

## Related Documentation

- **Frontend Plan**: `doc/implementation/frontend/main.md`
- **Section 13**: Android (Capacitor) Packaging

## Related Skills

- **implement-player-app** - Base player app
- **add-electron-wrapper** - Desktop packaging

## Claude Agents

- **vue-app-implementer** - Base app implementation
- **capacitor-android-implementer** - Android-specific tasks
