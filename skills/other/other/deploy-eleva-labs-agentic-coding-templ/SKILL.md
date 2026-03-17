---
name: deploy
description: >-
  Deploy the mobile app using EAS Build and Submit.
  Use when building for app stores, creating preview builds, or managing
  releases.
  Invoked by: "deploy", "build", "release", "eas", "app store", "publish".
---

# App Deployment SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

> **Note**: This is a template. Replace placeholders like `{PROJECT_NAME}`, `{BUNDLE_ID}`, and `{BASE_URL}` with your actual project values.

---

## Overview

### Purpose
Build and deploy the mobile app to the App Store and Google Play using EAS Build (Expo Application Services). This guide covers build profiles, code signing, store submission, version management, and over-the-air updates.

### When to Use
**ALWAYS**: App store submissions, production builds, preview builds, OTA updates, version management
**SKIP**: Local development builds, debugging, environment setup

---

## Quick Start

1. **Install EAS CLI**: `npm install -g eas-cli`
2. **Login**: `npx eas login`
3. **Build iOS**: `eas build -p ios --profile production`
4. **Build Android**: `eas build -p android --profile production`
5. **Submit**: `eas submit -p ios` or `eas submit -p android`

---

## Process Workflow

### Flow Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Setup EAS      │────>│  Configure      │────>│  Build App      │
│  CLI & Login    │     │  Credentials    │     │  (Cloud/Local)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        v
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Release to     │<────│  Store Review   │<────│  Submit to      │
│  Users          │     │  Process        │     │  App Store      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Phase Summary
| Phase | Description | Time |
|-------|-------------|------|
| 1 | Setup EAS | 10 min |
| 2 | Configure Credentials | 15-30 min |
| 3 | Build App | 15-45 min |
| 4 | Submit to Store | 5 min |
| 5 | Store Review | 1-7 days |

---

## Build Profiles

| Profile | Environment | Use Case |
|---------|-------------|----------|
| `development` | dev | Development builds with dev client |
| `development:simulator` | dev | iOS simulator builds |
| `preview` | dev | Internal distribution builds |
| `production` | prod | Store-ready builds |

---

## Build Caching

EAS Build includes automatic caching to speed up builds:

### Cache Configuration

Each build profile includes cache configuration in `eas.json`:

```json
{
  "cache": {
    "disabled": false,
    "key": "profile-v1",
    "cacheDefaultPaths": true,
    "customPaths": ["./ios/Podfile.lock"]
  }
}
```

### Cache Keys

| Profile | Cache Key | Purpose |
|---------|-----------|---------|
| development | `dev-v1` | Development client builds |
| development:simulator | `dev-sim-v1` | Simulator builds |
| preview | `preview-v1` | Internal distribution |
| production | `prod-v1` | Store builds |

### Invalidating Cache

To force a fresh build (when cache causes issues):

```bash
# Bump the cache key version in eas.json
# e.g., "key": "dev-v1" -> "key": "dev-v2"
```

Or use the EAS dashboard to clear cache for a specific build.

---

## Phase 1: Setup EAS

### Install EAS CLI

```bash
npm install -g eas-cli
```

### Login to EAS

```bash
npx eas login
npx eas whoami  # Verify logged in
```

### Update EAS CLI

```bash
npm install -g eas-cli@latest
```

---

## Phase 2: Prerequisites

### iOS (App Store Connect)

Required:
- Apple Developer Program membership ($99/year)
- App created in App Store Connect
- App-specific password for CI (optional)

### Android (Google Play Console)

Required:
- Google Play Developer account ($25 one-time)
- App created in Play Console
- Service account key for automated submissions

---

## Phase 3: Building

### Development Builds

For testing on devices with development features:

```bash
# iOS (device)
task eas-build-ios
# Or: eas build -p ios --profile development

# Android
task eas-build-android
# Or: eas build -p android --profile development

# iOS (simulator only)
eas build -p ios --profile development:simulator
```

### Production Builds

For store submission:

```bash
# iOS
eas build -p ios --profile production

# Android
eas build -p android --profile production
```

### Local Builds

Build on your machine instead of EAS cloud:

```bash
# iOS (requires macOS + Xcode)
task eas-build-ios-local

# Android
task eas-build-android-local
```

---

## Phase 4: Store Submission

### Automatic Submission

Submit immediately after build:

```bash
# iOS
eas build -p ios --profile production --auto-submit

# Android
eas build -p android --profile production --auto-submit
```

### Manual Submission

Submit an existing build:

```bash
# List recent builds
eas build:list

# Submit specific build
eas submit -p ios --id <build-id>
eas submit -p android --id <build-id>
```

---

## Version Management

### Automatic Version Management

Version numbers are managed automatically by EAS:

```json
// eas.json
{
  "cli": {
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "autoIncrement": true
    }
  }
}
```

| Setting | Description |
|---------|-------------|
| `appVersionSource: "remote"` | EAS tracks version numbers |
| `autoIncrement: true` | Build number increments automatically |

### Manual Version Setting

```bash
eas build:version:set
```

---

## Code Signing

### iOS Code Signing

EAS manages iOS code signing automatically. On first build:

1. EAS prompts to create/select certificates
2. Credentials are stored securely in EAS
3. Subsequent builds use stored credentials

To manage credentials:
```bash
eas credentials
```

### Android Code Signing

EAS generates and manages the keystore. For Play Store:

1. First build creates a new keystore
2. Upload the app to Play Store
3. Subsequent builds use the same keystore

---

## Environment Variables

### EAS Secrets

Sensitive variables are stored in EAS Secrets (not in code):

1. Go to [expo.dev](https://expo.dev) > Project > Secrets
2. Add secrets for each environment:
   - `GOOGLE_SERVICES_JSON` - Firebase Android config (base64)
   - `GOOGLE_SERVICE_INFO_PLIST` - Firebase iOS config (base64)
   - `SENTRY_AUTH_TOKEN` - Sentry upload token

### Environment-Specific Config

The `ENVIRONMENT` variable controls which config is used:

| ENVIRONMENT | Bundle ID | API URL |
|-------------|-----------|---------|
| `dev` | `{BUNDLE_ID}.dev` | `{BASE_URL_DEV}` |
| `prod` | `{BUNDLE_ID}` | `{BASE_URL_PROD}` |

---

## Over-the-Air Updates

For JavaScript-only updates (no native changes):

```bash
# Publish update to production channel
eas update --branch production --message "Bug fixes"

# Publish update to development channel
eas update --branch development --message "New feature"
```

Updates are automatically downloaded when users open the app.

### When to Use OTA

**Use OTA for**:
- JavaScript/TypeScript bug fixes
- UI/UX changes
- Copy/text updates
- Logic changes

**Requires full build for**:
- Native module updates
- SDK version changes
- New native dependencies
- Permission changes

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm install -g eas-cli && pnpm install

      - name: Build iOS
        run: eas build -p ios --profile production --non-interactive
        env:
          EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}

      - name: Build Android
        run: eas build -p android --profile production --non-interactive
        env:
          EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}
```

### EXPO_TOKEN Setup

For CI/CD, create a robot token:

1. Go to [expo.dev](https://expo.dev) > Account Settings > Access Tokens
2. Create new token
3. Add as `EXPO_TOKEN` secret in your CI

---

## Quick Reference

### Common Commands

```bash
# Check build status
eas build:list

# View build details
eas build:view

# Cancel a build
eas build:cancel

# View submission status
eas submit:list

# Configure project
eas build:configure

# Update EAS CLI
npm install -g eas-cli@latest

# View credentials
eas credentials

# Publish OTA update
eas update --branch production --message "Description"
```

### Build Commands

```bash
# Development iOS
eas build -p ios --profile development

# Development Android
eas build -p android --profile development

# Production iOS
eas build -p ios --profile production

# Production Android
eas build -p android --profile production

# iOS Simulator
eas build -p ios --profile development:simulator

# Local builds
task eas-build-ios-local
task eas-build-android-local
```

### Submit Commands

```bash
# Submit iOS
eas submit -p ios

# Submit Android
eas submit -p android

# Auto-submit after build
eas build -p ios --profile production --auto-submit
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build failed on EAS | Check build logs on [expo.dev](https://expo.dev); common issues: missing env vars, credential issues, native deps |
| iOS submission rejected | Common: missing privacy policy, incomplete metadata, guideline violations |
| Android submission rejected | Common: missing privacy policy, incorrect content rating, policy violations |
| Credentials issues | Run `eas credentials` to view/reset; select "Remove" to clear and recreate |
| Build queue is long | Consider local builds with `task eas-build-ios-local` |
| OTA update not appearing | Ensure app is closed/reopened; check update branch matches build branch |
| Version number conflict | Run `eas build:version:set` to manually set version |

---

## Store Requirements Checklist

### iOS App Store

- [ ] App icons (all sizes)
- [ ] Screenshots for required device sizes
- [ ] App description and keywords
- [ ] Privacy policy URL
- [ ] Support URL
- [ ] Age rating questionnaire
- [ ] App-specific content disclosures

### Google Play Store

- [ ] App icons and feature graphic
- [ ] Screenshots for phone and tablet
- [ ] Short and full description
- [ ] Privacy policy URL
- [ ] Content rating questionnaire
- [ ] Target audience declaration
- [ ] Data safety form

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/setup-dev` | Environment setup | Before first build |
| `/setup-ios` | iOS environment | Local iOS builds |
| `/setup-android` | Android environment | Local Android builds |
| `/setup-env` | Environment variables | Configuring EAS secrets |
| `/test` | Testing | Before production builds |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
