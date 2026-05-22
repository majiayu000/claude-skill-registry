---
name: jutsu-expo:expo-config
description: Use when configuring Expo apps with app.json, app.config.js, and EAS configuration. Covers app metadata, plugins, build configuration, and environment variables.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Expo Configuration

Use this skill when configuring Expo applications using app.json, app.config.js/ts, and EAS (Expo Application Services) configuration files.

## Key Concepts

### app.json Configuration

Basic static configuration:

```json
{
  "expo": {
    "name": "MyApp",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.mycompany.myapp",
      "buildNumber": "1"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.mycompany.myapp",
      "versionCode": 1
    },
    "web": {
      "favicon": "./assets/favicon.png"
    }
  }
}
```

### Dynamic Configuration (app.config.js)

Use JavaScript for dynamic configuration:

```javascript
export default ({ config }) => ({
  ...config,
  name: process.env.APP_NAME || 'MyApp',
  slug: 'my-app',
  version: '1.0.0',
  extra: {
    apiUrl: process.env.API_URL,
    environment: process.env.NODE_ENV,
  },
  ios: {
    bundleIdentifier:
      process.env.NODE_ENV === 'production'
        ? 'com.mycompany.myapp'
        : 'com.mycompany.myapp.dev',
  },
  android: {
    package:
      process.env.NODE_ENV === 'production'
        ? 'com.mycompany.myapp'
        : 'com.mycompany.myapp.dev',
  },
});
```

### TypeScript Configuration

Use TypeScript for type-safe config:

```typescript
// app.config.ts
import { ExpoConfig, ConfigContext } from '@expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: 'MyApp',
  slug: 'my-app',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#ffffff',
  },
  plugins: [
    'expo-router',
    [
      'expo-camera',
      {
        cameraPermission: 'Allow $(PRODUCT_NAME) to access your camera.',
      },
    ],
  ],
  extra: {
    apiUrl: process.env.API_URL,
  },
});
```

## Best Practices

### Environment Variables

Use environment-specific configuration:

```typescript
// app.config.ts
import { ExpoConfig, ConfigContext } from '@expo/config';

const IS_DEV = process.env.NODE_ENV === 'development';
const IS_PROD = process.env.NODE_ENV === 'production';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: IS_PROD ? 'MyApp' : 'MyApp (Dev)',
  slug: 'my-app',
  extra: {
    apiUrl: IS_PROD
      ? 'https://api.myapp.com'
      : 'https://dev-api.myapp.com',
    environment: process.env.NODE_ENV,
    eas: {
      projectId: process.env.EAS_PROJECT_ID,
    },
  },
  ios: {
    bundleIdentifier: IS_PROD
      ? 'com.mycompany.myapp'
      : 'com.mycompany.myapp.dev',
  },
  android: {
    package: IS_PROD
      ? 'com.mycompany.myapp'
      : 'com.mycompany.myapp.dev',
  },
});
```

### Plugin Configuration

Configure Expo plugins:

```json
{
  "expo": {
    "plugins": [
      "expo-router",
      [
        "expo-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access camera"
        }
      ],
      [
        "expo-location",
        {
          "locationAlwaysAndWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location"
        }
      ],
      [
        "expo-notifications",
        {
          "icon": "./assets/notification-icon.png",
          "color": "#ffffff"
        }
      ]
    ]
  }
}
```

### EAS Build Configuration

Configure EAS builds with eas.json:

```json
{
  "cli": {
    "version": ">= 5.9.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": false
      },
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {}
  }
}
```

### Access Config in Code

Access configuration at runtime:

```tsx
import Constants from 'expo-constants';

export function App() {
  const apiUrl = Constants.expoConfig?.extra?.apiUrl;
  const environment = Constants.expoConfig?.extra?.environment;

  console.log('API URL:', apiUrl);
  console.log('Environment:', environment);

  return <View />;
}
```

## Common Patterns

### Multi-Environment Setup

```typescript
// app.config.ts
import { ExpoConfig, ConfigContext } from '@expo/config';

type Environment = 'development' | 'staging' | 'production';

const ENV: Environment = (process.env.APP_ENV as Environment) || 'development';

const config: Record<Environment, { apiUrl: string; name: string }> = {
  development: {
    apiUrl: 'http://localhost:3000',
    name: 'MyApp (Dev)',
  },
  staging: {
    apiUrl: 'https://staging-api.myapp.com',
    name: 'MyApp (Staging)',
  },
  production: {
    apiUrl: 'https://api.myapp.com',
    name: 'MyApp',
  },
};

export default ({ config: baseConfig }: ConfigContext): ExpoConfig => ({
  ...baseConfig,
  name: config[ENV].name,
  slug: 'my-app',
  extra: {
    apiUrl: config[ENV].apiUrl,
    environment: ENV,
  },
});
```

### Feature Flags

```typescript
// app.config.ts
export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  extra: {
    features: {
      enableNewUI: process.env.ENABLE_NEW_UI === 'true',
      enableAnalytics: process.env.ENABLE_ANALYTICS !== 'false',
      enableBetaFeatures: process.env.ENABLE_BETA === 'true',
    },
  },
});

// In code
import Constants from 'expo-constants';

const features = Constants.expoConfig?.extra?.features;

if (features?.enableNewUI) {
  // Show new UI
}
```

### Platform-Specific Assets

```json
{
  "expo": {
    "ios": {
      "icon": "./assets/icon-ios.png",
      "splash": {
        "image": "./assets/splash-ios.png"
      }
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon-android.png",
        "backgroundColor": "#ffffff"
      },
      "splash": {
        "image": "./assets/splash-android.png"
      }
    }
  }
}
```

### Deep Linking Configuration

```json
{
  "expo": {
    "scheme": "myapp",
    "slug": "my-app",
    "web": {
      "bundler": "metro"
    },
    "ios": {
      "associatedDomains": ["applinks:myapp.com"]
    },
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [
            {
              "scheme": "https",
              "host": "myapp.com",
              "pathPrefix": "/app"
            }
          ],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

### Version Management

```typescript
// app.config.ts
import packageJson from './package.json';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  version: packageJson.version,
  ios: {
    buildNumber: process.env.IOS_BUILD_NUMBER || '1',
  },
  android: {
    versionCode: parseInt(process.env.ANDROID_VERSION_CODE || '1', 10),
  },
});
```

## Anti-Patterns

### Don't Hardcode Secrets

```typescript
// Bad - Secrets in config
export default {
  extra: {
    apiKey: 'sk_live_1234567890',
    apiSecret: 'secret_key_here',
  },
};

// Good - Use environment variables
export default {
  extra: {
    apiKey: process.env.API_KEY,
    // Never commit secrets
  },
};
```

### Don't Use app.json for Dynamic Config

```json
// Bad - Can't use dynamic values in app.json
{
  "expo": {
    "name": process.env.APP_NAME
  }
}

// Good - Use app.config.js/ts
// app.config.ts
export default {
  name: process.env.APP_NAME || 'MyApp',
};
```

### Don't Forget Platform-Specific Requirements

```json
// Bad - Missing required fields
{
  "expo": {
    "name": "MyApp",
    "slug": "my-app"
  }
}

// Good - Include all required fields
{
  "expo": {
    "name": "MyApp",
    "slug": "my-app",
    "ios": {
      "bundleIdentifier": "com.mycompany.myapp"
    },
    "android": {
      "package": "com.mycompany.myapp"
    }
  }
}
```

### Don't Mix Config Types

```javascript
// Bad - Mixing static and dynamic
// app.json
{
  "expo": {
    "name": "MyApp"
  }
}
// app.config.js also exists - creates conflicts

// Good - Use one or the other
// Either app.json for static config
// Or app.config.js/ts for dynamic config
```

## Related Skills

- **expo-modules**: Using Expo modules configured via plugins
- **expo-build**: Building apps with EAS Build
- **expo-updates**: Configuring OTA updates
