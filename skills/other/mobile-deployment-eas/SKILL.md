---
name: mobile-deployment-eas
description: EAS Build, Update, Submit deployment patterns
---

# EAS Deployment Patterns

> **Quick Guide:** EAS (Expo Application Services) handles cloud builds, OTA updates, and app store submission. Use build profiles in `eas.json` to separate development/preview/production builds. Use EAS Update with runtime version fingerprinting for safe OTA deploys. Use `--environment` flag (SDK 55+) instead of `--channel` when publishing updates. Let EAS manage credentials unless you have enterprise requirements.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `--environment` flag with `eas update` on SDK 55+ projects -- the `--channel` flag is replaced)**

**(You MUST set `runtimeVersion` with `"fingerprint"` policy for projects with native dependencies -- mismatched runtime versions crash apps on OTA update)**

**(You MUST use EAS Secrets for sensitive values -- NEVER put API keys or tokens in `eas.json` env blocks or `EXPO_PUBLIC_` variables)**

**(You MUST run `eas build` from the app directory in monorepos -- NOT from the repository root)**

</critical_requirements>

---

**Auto-detection:** EAS Build, EAS Update, EAS Submit, eas.json, eas build, eas update, eas submit, eas credentials, eas secret, EAS Workflows, build profiles, OTA updates, runtime version, fingerprint policy, app store submission, code signing, eas-cli

**When to use:**

- Configuring cloud builds for iOS and Android
- Publishing OTA (over-the-air) updates to deployed apps
- Submitting builds to App Store or Google Play
- Managing iOS provisioning profiles and Android keystores
- Setting up CI/CD pipelines for mobile deployment
- Configuring build profiles for different environments

**Key patterns covered:**

- `eas.json` build profiles with inheritance (`extends`)
- EAS Update channels, branches, and runtime versions
- EAS Submit for iOS App Store and Google Play
- Credentials management (automatic vs local)
- EAS Secrets for sensitive build-time values
- EAS Workflows for CI/CD automation
- Monorepo build configuration
- Version management with `autoIncrement` and `appVersionSource`

**When NOT to use:**

- General Expo SDK development (app.config.ts, Expo Router, components)
- Local-only builds with `npx expo run:ios/android` without EAS
- Projects not using Expo managed workflow

---

<philosophy>

## Philosophy

EAS separates **building**, **updating**, and **submitting** into distinct services that compose into a deployment pipeline. The key insight is that most mobile deployment complexity lives in credentials, versioning, and environment management -- EAS automates all three.

**Core principles:**

1. **Profiles over flags** -- Define build configurations in `eas.json`, not as CLI arguments scattered across scripts
2. **Channels isolate environments** -- Production, preview, and development builds receive only their intended updates
3. **Fingerprint prevents crashes** -- Runtime version fingerprinting auto-detects native changes so OTA updates never land on incompatible builds
4. **Credentials are managed** -- Let EAS handle signing unless you have enterprise requirements; it generates, stores, and renews certificates automatically
5. **Secrets stay server-side** -- Sensitive values live in EAS Secrets, never in config files or client-side variables

**Mental model:**

`eas.json` is your deployment configuration hub. Build profiles define HOW to build (development client, APK vs AAB, simulator vs device). Channels define WHERE updates go. Runtime versions define WHAT is compatible. Secrets define access to external services during builds.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Build Profiles with Inheritance

Use `extends` to share configuration between profiles. Define a `base` profile for shared settings, then extend for each environment.

```json
{
  "build": {
    "base": {
      "node": "20.17.0",
      "env": { "EXPO_PUBLIC_APP_ENV": "development" }
    },
    "development": {
      "extends": "base",
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true },
      "android": { "buildType": "apk" }
    },
    "production": {
      "extends": "base",
      "autoIncrement": "buildNumber",
      "channel": "production",
      "env": { "EXPO_PUBLIC_APP_ENV": "production" }
    }
  }
}
```

**Why good:** `extends` eliminates duplication across profiles, `autoIncrement` handles version bumps automatically, environment-specific env vars prevent mixing configurations

> Full profile examples with all options: [examples/core.md](examples/core.md) - Build Profiles section

---

### Pattern 2: Runtime Versions and Fingerprinting

Runtime version determines which builds are compatible with which OTA updates. The `"fingerprint"` policy auto-detects native changes.

```typescript
// app.config.ts
export default {
  runtimeVersion: {
    policy: "fingerprint", // Auto-detects native code changes
  },
  updates: {
    url: `https://u.expo.dev/${process.env.EAS_PROJECT_ID}`,
  },
};
```

| Policy        | Behavior                       | Best For                         |
| ------------- | ------------------------------ | -------------------------------- |
| `fingerprint` | Hashes all native dependencies | Complex apps with native modules |
| `appVersion`  | Uses `version` from app config | Simple apps, manual control      |
| Custom string | Exact match (e.g., `"1.0.0"`)  | Full manual control              |

**Gotcha:** `fingerprint` can be aggressive -- it may flag changes that don't actually affect native code, requiring more builds than necessary. Use `appVersion` for simpler projects.

> Full configuration examples: [examples/core.md](examples/core.md) - Runtime Versions section

---

### Pattern 3: Publishing OTA Updates

Updates go to a channel, which points to a branch. Builds pull updates from their assigned channel.

```bash
# SDK 55+ uses --environment (REQUIRED)
eas update --environment production --message "Fix login crash"

# SDK 54 and earlier uses --channel
eas update --channel production --message "Fix login crash"
```

**Channel-branch relationship:** By default, a channel auto-links to a branch with the same name. You can reassign: `eas channel:edit production --branch hotfix-v2`.

**Rollback:** If a bad update ships, roll back immediately:

```bash
eas update:rollback --channel production
```

> Full update workflow with client-side hook: [examples/updates.md](examples/updates.md)

---

### Pattern 4: App Store Submission

EAS Submit handles both iOS App Store and Google Play submission. Use `--auto-submit` to chain build and submit.

```bash
# Submit latest build
eas submit --platform ios
eas submit --platform android

# Build and submit in one step
eas build --profile production --platform ios --auto-submit

# Submit a specific build by ID
eas submit --platform ios --id [build-id]
```

```json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABC123DEF"
      },
      "android": {
        "serviceAccountKeyPath": "./google-services.json",
        "track": "internal",
        "releaseStatus": "draft"
      }
    }
  }
}
```

**Why good:** `track: "internal"` starts with internal testing before promoting, `releaseStatus: "draft"` gives manual control over publishing in Play Console

> Full submission configuration: [examples/core.md](examples/core.md) - Submit Configuration section

---

### Pattern 5: Credentials Management

Let EAS manage credentials by default. Use `eas credentials` to inspect or override.

```bash
# Interactive credential management
eas credentials --platform ios
eas credentials --platform android

# Register iOS test devices for internal distribution
eas device:create
eas device:list
```

**Automatic management** (recommended): EAS creates Distribution Certificates, Provisioning Profiles (iOS), and keystores (Android) automatically on first build. Teammates with EAS access can build without Apple Developer credentials.

**Local credentials** (enterprise): Use `credentials.json` at the app root with paths to your own signing files. Set `"credentialsSource": "local"` in the build profile.

> Full credentials patterns: [examples/credentials.md](examples/credentials.md)

---

### Pattern 6: EAS Secrets

Store sensitive build-time values server-side. Secrets are injected as environment variables during builds.

```bash
# Project-scoped secret
eas secret:create --scope project --name MY_AUTH_TOKEN --value "your-token"

# Account-scoped secret (shared across projects)
eas secret:create --scope account --name GOOGLE_SERVICES_JSON --type file --value ./google-services.json

# List and manage
eas secret:list
eas secret:delete --name MY_AUTH_TOKEN
```

Secrets are available as environment variables in the build process -- no `eas.json` configuration needed.

**Key distinction:** `EXPO_PUBLIC_*` variables are embedded in the JS bundle (visible to users). EAS Secrets are build-time only (never in the bundle).

---

### Pattern 7: EAS Workflows (CI/CD)

Define complete CI/CD pipelines in `.eas/workflows/*.yaml`. Workflows orchestrate builds, tests, submissions, and notifications.

```yaml
# .eas/workflows/deploy-production.yaml
name: Deploy Production
on:
  push:
    branches: [main]

jobs:
  build_ios:
    type: build
    params:
      platform: ios
      profile: production

  build_android:
    type: build
    params:
      platform: android
      profile: production

  submit_ios:
    needs: [build_ios]
    type: submit
    params:
      platform: ios

  submit_android:
    needs: [build_android]
    type: submit
    params:
      platform: android
```

**Why good:** Single YAML defines the entire deployment pipeline, `needs` enforces job ordering, pre-packaged job types (`build`, `submit`) eliminate boilerplate

> Full workflow examples with custom steps: [examples/workflows.md](examples/workflows.md)

---

### Pattern 8: Monorepo Builds

Run EAS CLI from the app directory, not the repo root. Each app has its own `eas.json`.

```
my-monorepo/
  apps/
    mobile/          <-- Run eas build from HERE
      eas.json
      app.config.ts
      package.json
  packages/
    shared/
  package.json       <-- NOT from here
```

```bash
cd apps/mobile
eas build --profile preview --platform ios
```

**Gotcha:** EAS auto-detects your package manager (npm, pnpm, Yarn, Bun) and installs from the monorepo root. If detection fails with pnpm, ensure your `pnpm-workspace.yaml` is at the repo root.

> Full monorepo configuration: [examples/core.md](examples/core.md) - Monorepo section

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Build profiles, eas.json configuration, runtime versions, submit config, monorepo setup
- [examples/updates.md](examples/updates.md) - OTA update workflows, client-side update hook, channel strategies
- [examples/credentials.md](examples/credentials.md) - iOS provisioning, Android keystores, local credentials, code signing
- [examples/workflows.md](examples/workflows.md) - EAS Workflows YAML, custom build steps, GitHub integration
- [reference.md](reference.md) - Decision frameworks, CLI commands, version management, anti-patterns

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Using `--channel` on SDK 55+ projects** -- replaced by `--environment` flag; old flag no longer works
- **Missing `runtimeVersion` in app config** -- OTA updates fail silently or crash on incompatible builds
- **Putting secrets in `eas.json` env blocks** -- config is committed to version control; use EAS Secrets instead
- **Running `eas build` from monorepo root** -- must run from the app directory (`apps/mobile/`, not repo root)
- **Not setting `autoIncrement` for production** -- Android versionCode must strictly increase; Play Store rejects same or lower values

**Medium Priority Issues:**

- **Using `distribution: "store"` for preview builds** -- use `"internal"` for ad hoc/internal distribution
- **Not configuring `resourceClass`** -- default may be slow for large projects; `"medium"` or `"large"` speeds up builds
- **Skipping `--non-interactive` in CI** -- EAS prompts for input by default; CI pipelines hang without this flag
- **Forgetting `--auto-submit` when build + submit are always paired** -- saves a manual step and avoids submitting the wrong build

**Gotchas & Edge Cases:**

- **`fingerprint` policy can be too aggressive** -- may flag changes that don't affect native code, forcing unnecessary rebuilds
- **iOS provisioning profiles expire after 12 months** -- won't affect apps in production, but next build requires regeneration via `eas credentials`
- **`autoIncrement: "version"` vs `"buildNumber"`** -- `"version"` bumps the user-visible version string; `"buildNumber"` bumps the internal build number only
- **EAS Update has ~50MB asset limit** -- large assets should use a CDN, not be bundled in updates
- **`appVersionSource: "remote"` requires paid plan** -- tracks versions server-side; free tier must manage locally
- **Android `buildType: "apk"` is for testing only** -- Play Store requires `"app-bundle"` (AAB) for production submissions
- **Code signing (end-to-end) requires Production or Enterprise plan** -- not available on free tier
- **`extends` depth limit is 5 levels** -- circular dependencies cause build errors
- **iOS simulator builds cannot install on physical devices** -- need a separate `development-device` profile with `"simulator": false`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use the `--environment` flag with `eas update` on SDK 55+ projects -- the `--channel` flag is replaced)**

**(You MUST set `runtimeVersion` with `"fingerprint"` policy for projects with native dependencies -- mismatched runtime versions crash apps on OTA update)**

**(You MUST use EAS Secrets for sensitive values -- NEVER put API keys or tokens in `eas.json` env blocks or `EXPO_PUBLIC_` variables)**

**(You MUST run `eas build` from the app directory in monorepos -- NOT from the repository root)**

**Failure to follow these rules will cause OTA update crashes, credential exposure, and build failures.**

</critical_reminders>
