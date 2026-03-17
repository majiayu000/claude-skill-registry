---
name: android-playstore-setup
description: Complete Play Store setup - orchestrates scanning, privacy policy, version management, Fastlane, and workflows (Internal track only)
category: android
version: 4.0.0
---

# Android Play Store Setup

This skill orchestrates complete Google Play Store deployment setup with automated publishing to the **internal testing track** using **Fastlane**.

## What This Does

**Scope:** Internal track deployment only (simplified for quick testing)

Sets up everything needed for automated Play Store deployment using **Fastlane**:
1. **Scan Project** - Analyze project and generate setup checklist
2. **Fastlane Setup** - Configure Fastlane with supply and screengrab
3. **App Icon** - Generate and place icon assets
4. **Screenshots** - Automated screenshot capture
5. **Store Listing** - Feature graphic and metadata
6. **Privacy Policy** - Generate privacy policy for GitHub Pages
7. **Version Management** - Setup Git tag-based versioning
8. **Signing Configuration** - Configure release signing
9. **Service Account** - Play Store API access
10. **GitHub Actions** - CI/CD workflows with Fastlane

## Prerequisites

- Google Play Developer account ($25 one-time)
- Google Cloud Platform account (free)
- Admin access to Play Console
- Package name reserved in Play Console

## Workflow Overview

```
1. Scan → 2. Review → 3. Setup → 4. Deploy
   ↓          ↓          ↓          ↓
  📋        ✅         🔧         🚀
```

## Process

### Step 1: Scan Project (Analysis Only)

Run `/devtools:android-playstore-scan`

**What it does:**
- Scans AndroidManifest.xml and build.gradle
- Detects Health Connect, ads, analytics
- Checks for privacy policy
- Generates `PLAY_CONSOLE_SETUP.md` with pre-filled answers

**Output:** `PLAY_CONSOLE_SETUP.md`

**Action:** Review the generated file and address any warnings

---

### Step 2: Generate Privacy Policy (If Needed)

If `PLAY_CONSOLE_SETUP.md` shows privacy policy is missing:

Run `/devtools:privacy-policy-generate`

**What it does:**
- Scans project for app info
- Detects Health Connect and third-party SDKs
- Prompts for developer info
- Generates `docs/privacy-policy.md`
- Creates GitHub Pages setup guide

**Verify:**
```bash
test -f docs/privacy-policy.md && echo "✓ Privacy policy created"
```

**Next:** Enable GitHub Pages (Settings → Pages → Source: docs/)

---

### Step 3: Setup Version Management

Run `/devtools:version-management` with platform=gradle

**What it does:**
- Creates `scripts/version-manager.sh` (core)
- Creates `scripts/gradle-version.sh` (Android adapter)
- Creates `version.properties` with initial version
- Updates `app/build.gradle.kts` to read from version.properties

**Verify:**
```bash
./scripts/version-manager.sh latest
./scripts/gradle-version.sh generate patch
```

---

### Step 4: Generate Keystores

Run `/devtools:android-keystore-generation`

**What it does:**
- Generates production-release.jks (for CI/CD)
- Generates local-dev-release.jks (for local testing)
- Creates KEYSTORE_INFO.txt with credentials
- Updates .gitignore

**Verify:**
```bash
ls keystores/*.jks
cat keystores/KEYSTORE_INFO.txt
```

---

### Step 5: Configure Signing

Run `/devtools:android-signing-config`

**What it does:**
- Adds signing configuration to app/build.gradle.kts
- Configures dual-source credentials (env vars + gradle.properties)
- Updates local ~/.gradle/gradle.properties
- Adds validation for release builds

**Verify:**
```bash
./gradlew assembleRelease
```

---

### Step 6: Configure ProGuard (If Not Already Setup)

Run `/devtools:android-proguard-setup`

**What it does:**
- Creates app/proguard-rules.pro with safe defaults
- Enables minification and resource shrinking
- Adds library-specific rules if needed

**Verify:**
```bash
grep "isMinifyEnabled = true" app/build.gradle.kts
```

---

### Step 7: Setup Fastlane

Run `/devtools:android-fastlane-setup`

**What it does:**
- Creates Gemfile with fastlane and screengrab
- Creates fastlane/Appfile with package name
- Creates fastlane/Fastfile with deployment lanes
- Creates fastlane/Screengrabfile for screenshot automation
- Creates fastlane/metadata/ directory structure

**Verify:**
```bash
bundle exec fastlane --version
bundle exec fastlane lanes
```

---

### Step 7a: Generate App Icon

Run `/devtools:android-app-icon`

**What it does:**
- Analyzes project for app name and colors
- Generates docs/APP_ICON_SETUP.md with IconKitchen instructions
- Provides helper script to process IconKitchen downloads
- Copies mipmap resources and Play Store icon

**Verify:**
```bash
test -f fastlane/metadata/android/en-US/images/icon.png
file fastlane/metadata/android/en-US/images/icon.png | grep "512 x 512"
```

---

### Step 7b: Setup Screenshot Automation

Run `/devtools:android-screenshot-automation`

**What it does:**
- Adds screengrab dependency to app/build.gradle.kts
- Creates debug manifest with required permissions
- Creates ScreenshotTest.kt for automated capture
- Creates DemoModeRule.kt for clean status bar

**Verify:**
```bash
bundle exec fastlane screenshots
ls fastlane/metadata/android/en-US/images/phoneScreenshots/
```

---

### Step 7c: Create Store Listing Assets

Run `/devtools:android-store-listing`

**What it does:**
- Generates docs/STORE_LISTING_GUIDE.md
- Creates metadata templates (title, description, etc.)
- Provides feature graphic generation script
- Guides user through asset creation

**Verify:**
```bash
test -f fastlane/metadata/android/en-US/images/featureGraphic.png
wc -c fastlane/metadata/android/en-US/*.txt
```

---

### Step 8: Create Deployment Workflows

Run `/devtools:android-workflow-internal`

**What it does:**
- Creates .github/workflows/build.yml (CI only - runs on push/PR)
- Creates .github/workflows/release-internal.yml (Manual releases with Fastlane)
- Adds Ruby setup and bundle caching
- Uses `bundle exec fastlane deploy_internal` for deployment
- All actions pinned to SHAs

**Verify:**
```bash
test -f .github/workflows/build.yml
test -f .github/workflows/release-internal.yml
grep "bundle exec fastlane" .github/workflows/release-internal.yml
```

---

### Step 9: Service Account Setup

Run `/devtools:android-service-account-guide`

**What it does:**
- Provides step-by-step guide for Google Cloud setup
- Documents service account creation
- Creates Play Console setup documentation

**Manual steps required:**
1. Create service account in Google Cloud
2. Download JSON key
3. Grant permissions in Play Console
4. Add JSON to GitHub Secrets as `SERVICE_ACCOUNT_JSON_PLAINTEXT`

---

### Step 10: Add Keystore to GitHub Secrets

From `keystores/KEYSTORE_INFO.txt`, add these secrets to GitHub:

```bash
# From KEYSTORE_INFO.txt, copy the base64 encoded keystore:
SIGNING_KEY_STORE_BASE64: <base64_string>
SIGNING_KEY_ALIAS: upload
SIGNING_STORE_PASSWORD: <password>
SIGNING_KEY_PASSWORD: <password>
```

---

### Step 11: Validate API Connection

Run `/devtools:android-playstore-api-validation`

**What it does:**
- Creates scripts/validate-playstore.py
- Tests Play Store API connection
- Verifies service account permissions

**Verify:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-auth google-api-python-client
python3 scripts/validate-playstore.py /path/to/service-account.json com.example.app
```

---

## Step 12: First Manual Upload (CRITICAL)

⚠️ **Before GitHub Actions can deploy, you MUST manually upload your first release.**

### Why?

1. Google Play requires manual first upload to complete store listing
2. Your production keystore becomes the **upload key**
3. Play App Signing is automatically enabled

### Steps:

```bash
# 1. Build release bundle locally
./gradlew bundleRelease

# 2. Verify it's signed
jarsigner -verify -verbose app/build/outputs/bundle/release/app-release.aab

# 3. Manual upload via Play Console
```

**In Play Console:**
1. Go to **Release** → **Internal testing**
2. Click **Create new release**
3. Upload `app-release.aab`
4. Complete store listing (title, description, icon)
5. Complete app content declarations
6. Publish to internal testing

**IMPORTANT:** The keystore used for this first upload must be the same one configured in GitHub Secrets!

---

## Step 13: Test Fastlane Deployment

After first manual upload is complete:

```bash
# Push to main branch to trigger deployment
git add .
git commit -m "Setup Play Store deployment"
git push origin main
```

**What happens:**
1. GitHub Actions workflow triggers
2. Runs unit tests
3. Builds release bundle
4. Deploys to internal testing track

**Monitor:** Go to repository → Actions tab

---

## Understanding Play App Signing

### Two Keys System

| Key Type | Purpose | Holder | Can Reset? |
|----------|---------|--------|------------|
| **App Signing Key** | Signs APKs for users | Google | No (permanent) |
| **Upload Key** | Authenticates your uploads | You | Yes (via Play Console) |

### Automatic Setup

For apps created after August 2021, Play App Signing is **automatic**:
1. First upload: Google generates app signing key
2. Your production keystore = upload key
3. Google re-signs with app signing key before distribution

**No action needed** - it just works!

---

## Final Verification Checklist

```bash
# Project files
✓ Fastlane configured (Gemfile, Fastfile, Appfile)
✓ Version management scripts in scripts/
✓ Keystores in keystores/ (gitignored)
✓ Privacy policy in docs/privacy-policy.md
✓ Metadata in fastlane/metadata/android/en-US/
✓ CI workflow in .github/workflows/build.yml
✓ Release workflow in .github/workflows/release-internal.yml

# Build verification
✓ ./gradlew assembleRelease succeeds
✓ Unit tests pass
✓ ProGuard enabled

# GitHub Secrets configured
✓ SERVICE_ACCOUNT_JSON_PLAINTEXT
✓ SIGNING_KEY_STORE_BASE64
✓ SIGNING_KEY_ALIAS
✓ SIGNING_STORE_PASSWORD
✓ SIGNING_KEY_PASSWORD

# Play Console
✓ First manual upload completed
✓ Internal testing track active
✓ Service account has permissions

# API validation
✓ scripts/validate-playstore.py passes
```

---

## Next Steps

### For Beta/Production Deployment

Once internal testing is working:

```bash
# Add beta track
/devtools:android-workflow-beta

# Add production track
/devtools:android-workflow-production
```

### Track Information

| Track | Audience | Review Time | Use Case |
|-------|----------|-------------|----------|
| **Internal** | Up to 100 testers | Instant | Quick testing, no review |
| **Closed (Alpha)** | Invited testers | < 24h | Beta testing |
| **Open (Beta)** | Anyone can join | < 24h | Public beta |
| **Production** | All users | 1-7 days | Full release |

---

## Troubleshooting

### "Package not found" in API validation
- Ensure app exists in Play Console
- Verify package name matches exactly
- Complete first manual upload

### "Upload key mismatch"
- Your first upload keystore ≠ GitHub Secrets keystore
- Fix: Use Play Console → App signing → Request upload key reset
- Re-upload with correct keystore

### "Permission denied" for service account
- Grant "Release to production" permission in Play Console
- Wait 5-10 minutes for permissions to propagate

### GitHub Actions fails to deploy
- Verify all GitHub Secrets are set correctly
- Check workflow logs for specific error
- Ensure first manual upload was completed

---

## Summary

You've successfully setup:
- ✅ Privacy policy (GitHub Pages ready)
- ✅ Version management (Git tag-based)
- ✅ Release signing (production + local dev)
- ✅ Fastlane deployment automation
- ✅ GitHub Actions CI/CD (internal track)
- ✅ Play Store API connection

**Your app is now ready for continuous integration and deployment!**

Every push to main or PR → Automatic build & test (CI) ✅
Manual workflow trigger → Version management + deployment to internal track 🚀

**All checks must pass** before marking this skill as complete.

## Completion Criteria

Do NOT mark complete unless ALL are verified:

✅ **Service Account Setup**
  - [ ] Service account created in Google Cloud
  - [ ] JSON key downloaded and stored securely
  - [ ] Play Developer API enabled
  - [ ] Service account linked to Play Console
  - [ ] "Release" permission granted

✅ **Store Metadata Structure**
  - [ ] fastlane/metadata/android/en-US/ directory exists
  - [ ] At least en-US locale configured
  - [ ] Metadata files created (title, description, changelogs)
  - [ ] docs/PLAY_STORE_TRACKS.md documentation created

✅ **API Validation**
  - [ ] scripts/validate-playstore.py exists
  - [ ] Validation script runs successfully
  - [ ] API connection confirmed
  - [ ] Package access confirmed

✅ **Documentation**
  - [ ] PLAY_CONSOLE_SETUP.md exists (project root)
  - [ ] GITHUB_SECRETS.md exists (if needed)

## Summary Report

After completion, provide this summary:

```
✅ Android Play Store Setup Complete!

🔐 Service Account:
  ✓ Created in Google Cloud
  ✓ JSON key downloaded
  ✓ Linked to Play Console
  ✓ Permissions granted

📝 Store Metadata:
  ✓ Structure created: fastlane/metadata/android/en-US/
  ✓ Locales configured
  ✓ Templates ready

✅ API Validation:
  ✓ Validation script created
  ✓ API connection tested
  ✓ Package access confirmed

📋 Next Steps:

  For GitHub:
    1. Add secrets (see GITHUB_SECRETS.md if it exists)
    2. Create "production" environment with reviewers

  For Deployment:
    1. Run: /devtools:android-playstore-publish
    2. Generate deployment workflows

⚠️  CRITICAL REMINDERS:
  - NEVER commit service account JSON to git
  - Store JSON key in password manager
  - Add all 5 secrets to GitHub before deploying
  - Wait 5-10 minutes after granting permissions
```

## Integration with Other Skills

This skill is prerequisite for:
- `android-playstore-publishing` - Uses service account for deployment
- `android-playstore-pipeline` - Complete pipeline setup

## Troubleshooting

If any skill fails:
1. Fix the specific issue in that skill
2. Re-run that skill until it completes
3. Continue with remaining skills
4. Run final verification

Common issues:
- **Service account not found** → Check Google Cloud project
- **Permissions denied** → Grant "Release" permission
- **API validation fails** → Wait 5-10 minutes for propagation
