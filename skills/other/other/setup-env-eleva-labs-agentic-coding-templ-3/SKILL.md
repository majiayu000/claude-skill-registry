---
name: setup-env
description: >-
  Configure environment variables for the mobile app.
  Use when setting up .env files, API keys, or environment-specific
  configuration.
  Invoked by: "env", "environment variables", ".env", "configuration", "api keys".
---

# Environment Variables Configuration SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

> **Note**: This is a template. Replace placeholders like `{PROJECT_NAME}`, `{BUNDLE_ID}`, `{APP_SLUG}`, and `{BASE_URL}` with your actual project values.

---

## Overview

### Purpose
This SOP guides developers through configuring environment variables for the mobile app. Proper environment configuration is essential for connecting to APIs, enabling features, and managing different deployment environments.

### When to Use
**ALWAYS**: Initial project setup, switching between dev/prod environments, configuring API keys, setting up Firebase credentials
**SKIP**: Only running tests (defaults work), making code changes that don't affect configuration

---

## Process Workflow

### Flow Diagram
```
[Quick Setup] --> [Configure Variables] --> [Firebase Credentials] --> [Verify]
```

### Phase Summary
| Phase | Objective | Deliverable |
|-------|-----------|-------------|
| 1. Quick Setup | Create .env from template | `.env` file exists |
| 2. Configure | Set required variables | Variables populated |
| 3. Firebase | Configure push notifications | Credential files in place |
| 4. Verify | Confirm configuration works | `task env-check` passes |

---

## Quick Start

### Option 1: Pull from EAS (Recommended)

```bash
# Development environment
task setup-dev
# Runs: ./scripts/pull-expo-env.sh development

# Production environment
task setup-prod
# Runs: ./scripts/pull-expo-env.sh production
```

**Note**: Requires EAS CLI login:
```bash
npx eas login
```

### Option 2: Manual Setup

```bash
# Copy template to .env
cp .env.example .env

# Edit with your values
nano .env
```

---

## Environment Files

| File | Purpose | Git Status |
|------|---------|------------|
| `.env.example` | Template with defaults | Committed |
| `.env` | Actual values | Gitignored |

### How It Works

The `Taskfile.yml` loads environment files in order:

```yaml
dotenv:
  - .env.example  # Loaded first (defaults)
  - .env          # Loaded second (overrides)
```

This means:
1. `.env.example` provides default values
2. `.env` overrides with actual/secret values
3. First file wins for any variable

---

## Variable Categories

### Build Configuration

```bash
# Environment: dev | prod
ENVIRONMENT=dev

# Build target: 0 = device, 1 = simulator
SIMULATOR=1
```

### App Configuration

```bash
EXPO_PUBLIC_APP_SLUG={APP_SLUG}
EXPO_PUBLIC_PROJECT_ID=<expo-project-id>
EXPO_PUBLIC_BASE_URL={BASE_URL}
EXPO_PUBLIC_INSTALLATION_URL={BASE_URL}/
EXPO_PUBLIC_MINIMUM_API_VERSION=1.0.0
```

### Firebase / Google Services

```bash
# Paths to credential files (set automatically)
EXPO_PUBLIC_IOS_GOOGLE_SERVICES_FILE=
EXPO_PUBLIC_ANDROID_GOOGLE_SERVICES_FILE=

# For EAS cloud builds (secrets)
GOOGLE_SERVICES_JSON=
GOOGLE_SERVICE_INFO_PLIST=
```

### Sentry Error Tracking

```bash
EXPO_PUBLIC_SENTRY_DSN=https://...@sentry.io/...
EXPO_PUBLIC_SENTRY_ORG_NAME=your-org
EXPO_PUBLIC_SENTRY_PROJECT_NAME=your-project
SENTRY_AUTH_TOKEN=<token>
SENTRY_DISABLE_AUTO_UPLOAD=true
```

### Development Tools

```bash
# Enable Storybook component gallery
EXPO_STORYBOOK_ENABLED=false
```

---

## Firebase Credentials Setup

### Directory Structure

```
credentials/
|-- android/
|   |-- google-services.json          # Production
|   |-- google-services-dev.json      # Development
|-- ios/
    |-- GoogleService-Info.plist      # Production
    |-- GoogleService-Info-dev.plist  # Development
```

### Automatic Setup (Placeholders)

```bash
task setup-firebase
```

Placeholders allow the app to build and run, but **push notifications won't work**.

### Real Firebase Credentials

To enable push notifications:

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create or select your project
3. Add apps for each platform:

**Android:**
- Package name: `{BUNDLE_ID}.dev` (dev) or `{BUNDLE_ID}` (prod)
- Download `google-services.json`
- Place in `credentials/android/`

**iOS:**
- Bundle ID: `{BUNDLE_ID}.dev` (dev) or `{BUNDLE_ID}` (prod)
- Download `GoogleService-Info.plist`
- Place in `credentials/ios/`

### EAS Cloud Builds

For EAS cloud builds, Firebase credentials are injected from EAS Secrets automatically. No manual credential files needed for CI/CD.

---

## Environment in app.config.ts

The `app.config.ts` reads environment variables at build time:

```typescript
// Determines dev vs prod configuration
const isProd = process.env.ENVIRONMENT === 'prod';

// Controls iOS code signing
const isSimulator = process.env.SIMULATOR === '1';
```

Key behaviors:
- `ENVIRONMENT=prod` - Production bundle ID, icons, URLs
- `ENVIRONMENT=dev` - Development bundle ID, icons, URLs
- `SIMULATOR=1` - Skips iOS entitlements requiring code signing
- `SIMULATOR=0` - Includes full entitlements for device builds

---

## Adding New Variables

### Step 1: Add to Template

Add to `.env.example` with a default or empty value:

```bash
# Description of variable
NEW_VARIABLE=default_value
```

### Step 2: Add to EAS (if secret)

If it's a secret, add to EAS Secrets in the dashboard.

### Step 3: Use in Code

If needed in app code, prefix with `EXPO_PUBLIC_`:

```bash
EXPO_PUBLIC_NEW_FEATURE_FLAG=true
```

Access in code:

```typescript
const flag = process.env.EXPO_PUBLIC_NEW_FEATURE_FLAG;
```

---

## Quick Reference

### Common Commands
```bash
# Pull dev environment from EAS
task setup-dev

# Pull prod environment from EAS
task setup-prod

# Verify environment
task env-check

# Setup Firebase placeholders
task setup-firebase

# EAS login
npx eas login

# Verify EAS account
npx eas whoami
```

### Variable Access Rules
| Prefix | Available At | Example |
|--------|--------------|---------|
| `EXPO_PUBLIC_*` | Runtime (app code) | `EXPO_PUBLIC_BASE_URL` |
| No prefix | Build time only | `ENVIRONMENT` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Variables not loading | Ensure `.env` exists in project root |
| Variables empty in app | Check for `EXPO_PUBLIC_` prefix |
| Changes not reflected | Restart dev server after changing |
| EAS pull fails | Run `npx eas login` and verify with `npx eas whoami` |
| Firebase not working | Check credential files exist in `credentials/` |
| Wrong environment used | Verify `ENVIRONMENT` variable value |

### Debugging Commands

```bash
# Check all environment variables loaded
task env-check

# Verify specific variable
echo $EXPO_PUBLIC_BASE_URL

# List credential files
ls -la credentials/android/
ls -la credentials/ios/
```

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/setup-dev` | Full development environment setup | Initial project setup |
| `/setup-ios` | iOS-specific configuration | iOS development |
| `/setup-android` | Android-specific configuration | Android development |
| `/deploy` | Deployment and EAS configuration | Building for stores |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
