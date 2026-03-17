---
name: expo-deployment
description: Deploying Expo apps to iOS App Store, Android Play Store, web hosting, and CI/CD workflows with EAS
agents: [tap]
triggers: [eas build, eas submit, testflight, app store, play store, expo deploy, eas update, ota update]
---

# Expo Deployment

Deploy Expo applications across all platforms using EAS (Expo Application Services). Based on official Expo skills.

## Quick Start

### Install EAS CLI

```bash
npm install -g eas-cli
eas login
```

### Initialize EAS

```bash
npx eas-cli@latest init
```

This creates `eas.json` with build profiles.

## Build Commands

### Production Builds

```bash
# iOS App Store build
npx eas-cli@latest build -p ios --profile production

# Android Play Store build
npx eas-cli@latest build -p android --profile production

# Both platforms
npx eas-cli@latest build --profile production
```

### Development Builds

```bash
# iOS development (includes dev tools)
npx eas-cli@latest build -p ios --profile development

# Android development
npx eas-cli@latest build -p android --profile development

# iOS Simulator build
npx eas-cli@latest build -p ios --profile development --local
```

### Submit to Stores

```bash
# iOS: Build and submit to App Store Connect
npx eas-cli@latest build -p ios --profile production --submit

# Android: Build and submit to Play Store
npx eas-cli@latest build -p android --profile production --submit

# Shortcut for iOS TestFlight
npx testflight
```

## EAS Configuration

Standard `eas.json` for production deployments:

```json
{
  "cli": {
    "version": ">= 16.0.1",
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "autoIncrement": true,
      "ios": {
        "resourceClass": "m-medium"
      }
    },
    "preview": {
      "distribution": "internal"
    },
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

## Web Deployment

Deploy web apps using EAS Hosting:

```bash
# Export web build
npx expo export -p web

# Deploy to production
npx eas-cli@latest deploy --prod

# Deploy PR preview
npx eas-cli@latest deploy
```

## OTA Updates (EAS Update)

Push JavaScript updates without app store review:

```bash
# Create an update for production branch
eas update --branch production --message "Bug fix"

# Create an update for all platforms
eas update --branch preview --message "New feature"

# Roll back to previous update
eas update:rollback --branch production
```

### Configure Runtime Version

In `app.json`:

```json
{
  "expo": {
    "runtimeVersion": {
      "policy": "appVersion"
    },
    "updates": {
      "url": "https://u.expo.dev/your-project-id"
    }
  }
}
```

## iOS Specific

### TestFlight Submission

```bash
# Quick TestFlight submission
npx testflight

# Or manually
npx eas-cli@latest build -p ios --profile production
npx eas-cli@latest submit -p ios --profile production
```

### Configure Apple Credentials

```bash
# Interactive credential setup
eas credentials

# Configure App Store Connect
eas credentials:configure --platform ios
```

### App Store Metadata

Configure in `store.config.json` or use EAS Metadata:

```bash
# Push metadata to App Store Connect
eas metadata:push

# Pull current metadata
eas metadata:pull
```

## Android Specific

### Play Store Submission

```bash
# Build and submit to internal track
npx eas-cli@latest build -p android --profile production --submit

# Submit existing build
npx eas-cli@latest submit -p android --latest
```

### Track Progression

1. `internal` - Internal testing (up to 100 testers)
2. `alpha` - Closed testing
3. `beta` - Open testing
4. `production` - Full release

```json
{
  "submit": {
    "production": {
      "android": {
        "track": "internal",
        "releaseStatus": "completed"
      }
    }
  }
}
```

### Service Account Setup

1. Create service account in Google Cloud Console
2. Grant "Service Account User" role
3. Enable Google Play Android Developer API
4. Download JSON key
5. Add service account to Play Console with release permissions

## CI/CD Workflows

### EAS Workflows

Create `.eas/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  build-ios:
    type: build
    params:
      platform: ios
      profile: production

  submit-ios:
    type: submit
    needs: [build-ios]
    params:
      platform: ios
      profile: production

  build-android:
    type: build
    params:
      platform: android
      profile: production

  submit-android:
    type: submit
    needs: [build-android]
    params:
      platform: android
      profile: production
```

### PR Preview Workflow

```yaml
name: PR Preview

on:
  pull_request:

jobs:
  deploy-preview:
    type: deploy
    params:
      platform: web

  build-preview:
    type: build
    params:
      platform: ios
      profile: preview
```

## Version Management

EAS manages version numbers automatically with `appVersionSource: "remote"`:

```bash
# Check current versions
eas build:version:get

# Manually set version
eas build:version:set -p ios --build-number 42
eas build:version:set -p android --version-code 42

# Sync versions between platforms
eas build:version:sync
```

## Monitoring

```bash
# List recent builds
eas build:list

# Check build status
eas build:view

# View submission status
eas submit:list

# View update deployments
eas update:list
```

## Environment Variables

### EAS Secrets

```bash
# Add a secret
eas secret:create --name API_KEY --value "your-api-key"

# List secrets
eas secret:list

# Delete a secret
eas secret:delete API_KEY
```

### Per-Environment Configuration

```bash
# Pull environment variables
eas env:pull --environment production

# Push environment variables
eas env:push --environment production
```

## Troubleshooting

### Build Issues

```bash
# Clear build cache
eas build --clear-cache

# View build logs
eas build:view --logs

# Check project configuration
npx expo-doctor
```

### Submission Issues

```bash
# Verify credentials
eas credentials

# Check submission status
eas submit:list

# View submission details
eas submit:view
```

### Common Errors

| Error | Solution |
|-------|----------|
| "Missing Apple credentials" | Run `eas credentials` |
| "Version already exists" | Increment version in `app.json` or use `autoIncrement` |
| "Service account not found" | Verify `serviceAccountKeyPath` in `eas.json` |
| "Build queue full" | Wait or upgrade EAS plan for priority builds |
