---
name: expo-config-setup
description: Эксперт Expo конфигурации. Используй для React Native Expo, app.json и EAS Build.
---

# Expo Config Setup Expert

Expert at configuring Expo projects with app.json, app.config.js, and platform-specific settings for optimal development and production builds.

## Core Configuration Principles

### Static vs Dynamic Configuration
- Use `app.json` for static configuration that doesn't change between environments
- Use `app.config.js` for dynamic configuration requiring environment variables or conditional logic
- Never mix sensitive data directly in configuration files - use environment variables

### Platform-Specific Settings
- Always configure both iOS and Android platforms explicitly
- Use platform-specific overrides for different requirements
- Consider platform differences in permissions, capabilities, and UI guidelines

## Essential App Configuration Structure

```javascript
// app.config.js
export default {
  expo: {
    name: process.env.APP_NAME || "My App",
    slug: "my-app",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "automatic",
    splash: {
      image: "./assets/splash.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    assetBundlePatterns: [
      "**/*"
    ],
    ios: {
      supportsTablet: true,
      bundleIdentifier: process.env.IOS_BUNDLE_ID || "com.company.myapp",
      buildNumber: process.env.IOS_BUILD_NUMBER || "1",
      infoPlist: {
        NSCameraUsageDescription: "This app uses the camera to take photos.",
        NSLocationWhenInUseUsageDescription: "This app uses location to provide location-based features."
      }
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#FFFFFF"
      },
      package: process.env.ANDROID_PACKAGE || "com.company.myapp",
      versionCode: parseInt(process.env.ANDROID_VERSION_CODE) || 1,
      permissions: [
        "android.permission.CAMERA",
        "android.permission.ACCESS_FINE_LOCATION"
      ]
    },
    web: {
      favicon: "./assets/favicon.png",
      bundler: "metro"
    }
  }
};
```

## Environment-Specific Configuration

```javascript
// app.config.js with environment handling
const IS_DEV = process.env.APP_VARIANT === 'development';
const IS_PREVIEW = process.env.APP_VARIANT === 'preview';

const getAppName = () => {
  if (IS_DEV) return 'MyApp (Dev)';
  if (IS_PREVIEW) return 'MyApp (Preview)';
  return 'MyApp';
};

const getBundleId = () => {
  if (IS_DEV) return 'com.company.myapp.dev';
  if (IS_PREVIEW) return 'com.company.myapp.preview';
  return 'com.company.myapp';
};

export default {
  expo: {
    name: getAppName(),
    slug: IS_DEV ? 'myapp-dev' : IS_PREVIEW ? 'myapp-preview' : 'myapp',
    scheme: IS_DEV ? 'myapp-dev' : IS_PREVIEW ? 'myapp-preview' : 'myapp',
    version: process.env.APP_VERSION || '1.0.0',
    ios: {
      bundleIdentifier: getBundleId(),
    },
    android: {
      package: getBundleId(),
    },
    extra: {
      apiUrl: process.env.API_URL,
      environment: process.env.APP_VARIANT || 'production',
      eas: {
        projectId: process.env.EAS_PROJECT_ID
      }
    },
    updates: {
      url: `https://u.expo.dev/${process.env.EAS_PROJECT_ID}`
    },
    runtimeVersion: {
      policy: 'sdkVersion'
    }
  }
};
```

## EAS Build Configuration

```json
// eas.json
{
  "cli": {
    "version": ">= 5.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      },
      "env": {
        "APP_VARIANT": "development"
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "resourceClass": "m-medium"
      },
      "android": {
        "buildType": "apk"
      },
      "env": {
        "APP_VARIANT": "preview"
      }
    },
    "production": {
      "ios": {
        "resourceClass": "m-medium"
      },
      "env": {
        "APP_VARIANT": "production"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCD1234"
      },
      "android": {
        "serviceAccountKeyPath": "./google-services.json",
        "track": "internal"
      }
    }
  }
}
```

## Plugin Configuration Best Practices

```javascript
// Advanced plugin configuration
export default {
  expo: {
    plugins: [
      "expo-font",
      "expo-router",
      [
        "expo-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera",
          "microphonePermission": "Allow $(PRODUCT_NAME) to access your microphone",
          "recordAudioAndroid": true
        }
      ],
      [
        "expo-location",
        {
          "locationAlwaysAndWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location.",
          "locationAlwaysPermission": "Allow $(PRODUCT_NAME) to use your location.",
          "locationWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location."
        }
      ],
      [
        "expo-notifications",
        {
          "icon": "./assets/notification-icon.png",
          "color": "#ffffff",
          "sounds": ["./assets/notification-sound.wav"],
          "mode": "production"
        }
      ],
      [
        "expo-build-properties",
        {
          "ios": {
            "deploymentTarget": "13.4",
            "useFrameworks": "static"
          },
          "android": {
            "compileSdkVersion": 34,
            "targetSdkVersion": 34,
            "buildToolsVersion": "34.0.0",
            "minSdkVersion": 23,
            "kotlinVersion": "1.9.0"
          }
        }
      ],
      [
        "expo-image-picker",
        {
          "photosPermission": "Allow $(PRODUCT_NAME) to access your photos",
          "cameraPermission": "Allow $(PRODUCT_NAME) to take pictures"
        }
      ]
    ]
  }
};
```

## Asset and Icon Configuration

```javascript
// Comprehensive asset configuration
export default {
  expo: {
    icon: "./assets/images/icon.png", // 1024x1024
    splash: {
      image: "./assets/images/splash.png", // 1284x2778 for iPhone 13 Pro Max
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    ios: {
      icon: "./assets/images/icon-ios.png", // iOS-specific icon if needed
      splash: {
        image: "./assets/images/splash-ios.png",
        resizeMode: "cover",
        backgroundColor: "#ffffff",
        tabletImage: "./assets/images/splash-tablet.png"
      }
    },
    android: {
      icon: "./assets/images/icon-android.png",
      adaptiveIcon: {
        foregroundImage: "./assets/images/adaptive-icon.png", // 1024x1024
        backgroundImage: "./assets/images/adaptive-icon-background.png",
        backgroundColor: "#FFFFFF"
      },
      splash: {
        image: "./assets/images/splash-android.png",
        resizeMode: "cover",
        backgroundColor: "#ffffff",
        mdpi: "./assets/images/splash-mdpi.png",    // 320x480
        hdpi: "./assets/images/splash-hdpi.png",    // 480x800
        xhdpi: "./assets/images/splash-xhdpi.png",  // 720x1280
        xxhdpi: "./assets/images/splash-xxhdpi.png", // 960x1600
        xxxhdpi: "./assets/images/splash-xxxhdpi.png" // 1280x1920
      }
    }
  }
};
```

## Deep Linking and Scheme Configuration

```javascript
// Complete deep linking setup
export default {
  expo: {
    scheme: "myapp",
    web: {
      bundler: "metro"
    },
    ios: {
      bundleIdentifier: "com.company.myapp",
      associatedDomains: [
        "applinks:myapp.com",
        "applinks:www.myapp.com"
      ]
    },
    android: {
      package: "com.company.myapp",
      intentFilters: [
        {
          action: "VIEW",
          autoVerify: true,
          data: [
            {
              scheme: "https",
              host: "myapp.com",
              pathPrefix: "/app"
            },
            {
              scheme: "https",
              host: "www.myapp.com",
              pathPrefix: "/app"
            }
          ],
          category: ["BROWSABLE", "DEFAULT"]
        },
        {
          action: "VIEW",
          data: [
            {
              scheme: "myapp"
            }
          ],
          category: ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
};
```

## OTA Updates Configuration

```javascript
// Over-the-air updates setup
export default {
  expo: {
    updates: {
      enabled: true,
      checkAutomatically: "ON_LOAD",
      fallbackToCacheTimeout: 30000,
      url: `https://u.expo.dev/${process.env.EAS_PROJECT_ID}`
    },
    runtimeVersion: {
      policy: "appVersion" // or "sdkVersion", "nativeVersion", "fingerprint"
    },
    // For custom update logic
    extra: {
      updateChannel: process.env.APP_VARIANT || 'production'
    }
  }
};
```

### Update Logic in App

```javascript
// App.js or updates hook
import * as Updates from 'expo-updates';

async function checkForUpdates() {
  if (__DEV__) return;

  try {
    const update = await Updates.checkForUpdateAsync();
    if (update.isAvailable) {
      await Updates.fetchUpdateAsync();
      await Updates.reloadAsync();
    }
  } catch (error) {
    console.error('Error checking for updates:', error);
  }
}
```

## Notifications Configuration

```javascript
// Push notifications setup
export default {
  expo: {
    notification: {
      icon: "./assets/notification-icon.png", // 96x96, white on transparent
      color: "#3498db",
      androidMode: "default",
      androidCollapsedTitle: "#{unread_notifications} new notifications"
    },
    ios: {
      infoPlist: {
        UIBackgroundModes: ["remote-notification"]
      }
    },
    android: {
      googleServicesFile: "./google-services.json",
      useNextNotificationsApi: true
    },
    plugins: [
      [
        "expo-notifications",
        {
          icon: "./assets/notification-icon.png",
          color: "#3498db",
          sounds: ["./assets/sounds/notification.wav"],
          mode: "production"
        }
      ]
    ]
  }
};
```

## Security Best Practices

```javascript
// Secure configuration patterns
export default ({ config }) => {
  // Validate required env vars
  const requiredEnvVars = ['API_URL', 'EAS_PROJECT_ID'];
  for (const envVar of requiredEnvVars) {
    if (!process.env[envVar]) {
      console.warn(`Warning: ${envVar} is not set`);
    }
  }

  return {
    ...config,
    expo: {
      ...config.expo,
      // Never expose sensitive keys in extra
      extra: {
        apiUrl: process.env.API_URL,
        // Use EAS Secrets for sensitive values
        // NOT: apiKey: process.env.API_KEY
      },
      // Certificate pinning for production
      ios: {
        ...config.expo?.ios,
        infoPlist: {
          NSAppTransportSecurity: {
            NSAllowsArbitraryLoads: false,
            NSExceptionDomains: {
              "myapp.com": {
                NSExceptionRequiresForwardSecrecy: true,
                NSIncludesSubdomains: true
              }
            }
          }
        }
      }
    }
  };
};
```

## Common Configuration Pitfalls

```yaml
Missing Bundle Identifiers:
  problem: Build fails with "missing bundleIdentifier"
  solution: Always set ios.bundleIdentifier and android.package

Incorrect Asset Dimensions:
  problem: Icons/splash screens look blurry or cropped
  solution: Follow exact size requirements (icon: 1024x1024)

Version Code Issues:
  problem: Store rejects upload due to version code
  solution: Increment android.versionCode for each upload

Missing Permissions:
  problem: Feature crashes on first use
  solution: Declare all required permissions with descriptions

OTA Update Failures:
  problem: Updates not applying
  solution: Check runtimeVersion policy matches native builds
```

## Validation and Testing

```bash
# Validate configuration
npx expo doctor

# Check for common issues
npx expo-cli diagnostics

# Test deep links
# iOS
xcrun simctl openurl booted "myapp://path"
# Android
adb shell am start -a android.intent.action.VIEW -d "myapp://path"

# Preview configuration
npx expo config --type public
npx expo config --type introspect
```

## Лучшие практики

1. **Environment separation** — разные конфиги для dev/preview/prod
2. **Dynamic config** — app.config.js для переменных окружения
3. **EAS Secrets** — храните sensitive данные в EAS Secrets
4. **Version management** — автоматизируйте версии через CI/CD
5. **Plugin audit** — регулярно обновляйте и проверяйте плагины
6. **Test deep links** — тестируйте на обеих платформах
