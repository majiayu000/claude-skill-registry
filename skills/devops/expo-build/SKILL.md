---
name: jutsu-expo:expo-build
description: Use when building and deploying Expo apps with EAS Build. Covers build configuration, development builds, production builds, and app store submission.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Expo Build with EAS

Use this skill when building and deploying Expo applications using EAS (Expo Application Services) Build.

## Key Concepts

### EAS Build Configuration

```json
// eas.json
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
      "distribution": "internal"
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

### Build Commands

```bash
# Development build
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview build
eas build --profile preview --platform all

# Production build
eas build --profile production --platform all

# Local build
eas build --profile production --platform ios --local
```

### Development Builds

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": {
        "NODE_ENV": "development"
      }
    }
  }
}
```

## Best Practices

### Environment Variables

```json
// eas.json
{
  "build": {
    "production": {
      "env": {
        "APP_ENV": "production",
        "API_URL": "https://api.myapp.com"
      }
    },
    "staging": {
      "env": {
        "APP_ENV": "staging",
        "API_URL": "https://staging-api.myapp.com"
      }
    }
  }
}
```

### Secrets Management

```bash
# Set secrets
eas secret:create --scope project --name API_KEY --value your_api_key
eas secret:create --scope project --name GOOGLE_SERVICES_JSON --value "$(cat google-services.json)" --type file

# List secrets
eas secret:list

# Use in eas.json
{
  "build": {
    "production": {
      "env": {
        "API_KEY": "$(EAS_SECRET_API_KEY)"
      }
    }
  }
}
```

### Version Management

```json
// eas.json
{
  "build": {
    "production": {
      "autoIncrement": true,
      "ios": {
        "buildNumber": "1"
      },
      "android": {
        "versionCode": 1
      }
    }
  }
}
```

### Build Hooks

```json
{
  "build": {
    "production": {
      "prebuild": "npm run generate-assets",
      "postbuild": "npm run cleanup"
    }
  }
}
```

## Common Patterns

### Multi-Environment Builds

```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "channel": "development",
      "distribution": "internal"
    },
    "staging": {
      "channel": "staging",
      "distribution": "internal",
      "ios": {
        "bundleIdentifier": "com.myapp.staging"
      },
      "android": {
        "package": "com.myapp.staging"
      }
    },
    "production": {
      "channel": "production",
      "autoIncrement": true
    }
  }
}
```

### Custom Native Code

```json
{
  "build": {
    "production": {
      "ios": {
        "buildConfiguration": "Release"
      },
      "android": {
        "gradleCommand": ":app:bundleRelease"
      }
    }
  }
}
```

### App Store Submission

```bash
# iOS
eas submit --platform ios

# Android
eas submit --platform android

# Configure submission
# eas.json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your.apple.id@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "AB12CD34EF"
      },
      "android": {
        "serviceAccountKeyPath": "./service-account.json",
        "track": "production"
      }
    }
  }
}
```

### Build Monitoring

```bash
# View build status
eas build:list

# View specific build
eas build:view [build-id]

# Cancel build
eas build:cancel [build-id]
```

## Anti-Patterns

### Don't Commit Secrets

```json
// Bad - Secrets in eas.json
{
  "build": {
    "production": {
      "env": {
        "API_KEY": "sk_live_1234567890"
      }
    }
  }
}

// Good - Use EAS Secrets
eas secret:create --scope project --name API_KEY --value sk_live_1234567890
```

### Don't Skip Version Increments

```json
// Bad - Manual version management
{
  "build": {
    "production": {
      "autoIncrement": false
    }
  }
}

// Good - Auto increment
{
  "build": {
    "production": {
      "autoIncrement": true
    }
  }
}
```

## Related Skills

- **expo-config**: Configuring app for builds
- **expo-updates**: OTA updates after builds
