---
name: expo-build-deploy
description: Building and deploying Expo React Native apps to iOS. Use when configuring EAS Build, submitting to TestFlight, App Store deployment, managing certificates, or troubleshooting build issues.
---

# Expo Build & Deploy (iOS)

## EAS Build Setup

### Initial configuration

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo account
eas login

# Initialize EAS in project
eas build:configure
```

This creates `eas.json`:

```json
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
      }
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

### app.json iOS configuration

```json
{
  "expo": {
    "name": "MyApp",
    "slug": "myapp",
    "version": "1.0.0",
    "scheme": "myapp",
    "ios": {
      "bundleIdentifier": "com.yourcompany.myapp",
      "buildNumber": "1",
      "supportsTablet": false,
      "infoPlist": {
        "NSCameraUsageDescription": "Take photos for your profile",
        "NSLocationWhenInUseUsageDescription": "Find locations near you"
      }
    }
  }
}
```

## Build Types

### Development build (for development)

```bash
# For simulator
eas build --profile development --platform ios

# For physical device
eas build --profile development --platform ios --local
```

Use with `npx expo start --dev-client`

### Preview build (internal testing)

```bash
eas build --profile preview --platform ios
```

Distributes via ad-hoc provisioning. Testers install via link.

### Production build (App Store)

```bash
eas build --profile production --platform ios
```

## Credentials Management

EAS manages credentials automatically, but you can control them:

```bash
# View current credentials
eas credentials

# Let EAS manage everything (recommended)
# Just run build, it handles certificates

# Use existing credentials
eas credentials --platform ios
# Select "Use existing" and provide paths
```

### Manual credential setup (if needed)

1. Create App ID in Apple Developer Portal
2. Create Distribution Certificate
3. Create Provisioning Profile
4. Configure in `eas.json`:

```json
{
  "build": {
    "production": {
      "ios": {
        "credentialsSource": "local"
      }
    }
  }
}
```

## Environment Variables

### In eas.json

```json
{
  "build": {
    "production": {
      "env": {
        "API_URL": "https://api.yourapp.com"
      }
    },
    "preview": {
      "env": {
        "API_URL": "https://staging-api.yourapp.com"
      }
    }
  }
}
```

### Secrets (sensitive values)

```bash
# Set secret
eas secret:create --name API_KEY --value "sk_live_xxx" --scope project

# List secrets
eas secret:list

# Use in app.json
{
  "extra": {
    "apiKey": process.env.API_KEY
  }
}
```

Access in code:

```typescript
import Constants from 'expo-constants';

const apiKey = Constants.expoConfig?.extra?.apiKey;
```

## TestFlight Deployment

### Configure submit profile

```json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "XXXXXXXXXX"
      }
    }
  }
}
```

Get `ascAppId` from App Store Connect URL: `https://appstoreconnect.apple.com/apps/1234567890`

### Submit to TestFlight

```bash
# Build and submit in one command
eas build --profile production --platform ios --auto-submit

# Or submit existing build
eas submit --platform ios --latest

# Submit specific build
eas submit --platform ios --id <build-id>
```

### App Store Connect setup (first time)

1. Create app in App Store Connect
2. Fill in app information
3. Set up TestFlight:
   - Add internal testers (immediate access)
   - Create external testing group (requires review)

## App Store Submission

### Pre-submission checklist

- [ ] App icons (1024x1024 for App Store)
- [ ] Screenshots for required device sizes
- [ ] Privacy policy URL
- [ ] App description and keywords
- [ ] Age rating questionnaire
- [ ] Export compliance (encryption)

### Submit for review

1. Build with production profile
2. Submit to App Store Connect
3. In App Store Connect:
   - Select build for submission
   - Complete app information
   - Submit for review

```bash
# Automated submission
eas submit --platform ios --latest
```

## Over-the-Air Updates

For JS/asset-only changes (no native code changes):

```bash
# Publish update
eas update --branch production --message "Bug fix for login"

# Preview before publishing
eas update --branch preview --message "Testing new feature"
```

### Configure update channels

```json
{
  "build": {
    "production": {
      "channel": "production"
    },
    "preview": {
      "channel": "preview"
    }
  }
}
```

### Check for updates in app

```typescript
import * as Updates from 'expo-updates';

async function checkForUpdates() {
  if (__DEV__) return; // Skip in development
  
  try {
    const update = await Updates.checkForUpdateAsync();
    if (update.isAvailable) {
      await Updates.fetchUpdateAsync();
      await Updates.reloadAsync();
    }
  } catch (error) {
    console.log('Update check failed:', error);
  }
}
```

## Version Management

### Increment version for new features

```json
{
  "expo": {
    "version": "1.1.0"  // Shown to users
  }
}
```

### Increment buildNumber for each build

```json
{
  "expo": {
    "ios": {
      "buildNumber": "2"  // Must increase for each upload
    }
  }
}
```

### Automate with EAS

```json
{
  "build": {
    "production": {
      "ios": {
        "autoIncrement": "buildNumber"
      }
    }
  }
}
```

## Local Builds

Build on your machine instead of EAS servers:

```bash
# Requires Xcode installed
eas build --platform ios --local
```

Useful for:
- Faster iteration during debugging
- Inspecting build output
- Offline builds

## Troubleshooting

### Build fails with signing error

```bash
# Reset credentials and let EAS regenerate
eas credentials --platform ios
# Select "Remove" then rebuild
```

### "Missing compliance" warning

Add to `app.json`:

```json
{
  "expo": {
    "ios": {
      "infoPlist": {
        "ITSAppUsesNonExemptEncryption": false
      }
    }
  }
}
```

### Build succeeds but app crashes

```bash
# Check native logs
eas build:view <build-id>

# Download and inspect build
eas build:download <build-id>
```

### TestFlight build stuck in processing

- Usually takes 10-30 minutes
- Check App Store Connect for status
- Ensure buildNumber is unique

### OTA update not applied

- Verify channel matches
- Check `Updates.checkForUpdateAsync()` is called
- Ensure not in development mode
- Updates only apply on next cold start

## Common Commands Reference

```bash
# Build
eas build --platform ios --profile production
eas build --platform ios --profile preview
eas build --platform ios --local

# Submit
eas submit --platform ios --latest
eas submit --platform ios --id <build-id>

# Updates
eas update --branch production --message "Fix"
eas update:list

# Credentials
eas credentials --platform ios
eas credentials:configure

# View builds
eas build:list
eas build:view <build-id>
eas build:cancel <build-id>

# Secrets
eas secret:create --name KEY --value "xxx"
eas secret:list
```
