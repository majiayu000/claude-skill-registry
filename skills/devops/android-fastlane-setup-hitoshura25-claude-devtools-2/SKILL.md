---
name: android-fastlane-setup
description: Setup Fastlane for Play Store deployment with supply and screengrab
category: android
version: 1.0.0
inputs:
  - package_name: Android app package name
  - service_account_path: Path to service account JSON
outputs:
  - Gemfile
  - fastlane/Appfile
  - fastlane/Fastfile
  - fastlane/Screengrabfile
  - fastlane/metadata/android/ structure
verify: "bundle exec fastlane --version && bundle exec fastlane lanes"
---

# Android Fastlane Setup

Configures Fastlane with `supply` for Play Store deployment and `screengrab` for screenshot automation.

## Prerequisites

- Ruby 2.7+ installed
- Android project
- Play Store service account JSON

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| package_name | Yes | - | Android app package name (e.g., com.example.app) |
| service_account_path | Yes | - | Path to service account JSON file |

## Process

### Step 1: Check Ruby Installation

```bash
# Check Ruby version
ruby --version || echo "❌ Ruby not found. Please install Ruby 2.7+ first."

# Install Bundler if needed
gem install bundler --no-document
```

### Step 2: Create Gemfile

Create `./Gemfile`:

```ruby
source "https://rubygems.org"

gem "fastlane"
gem "screengrab"
```

### Step 3: Install Dependencies

```bash
bundle install
```

This will create `Gemfile.lock` and install all dependencies.

### Step 4: Create Fastlane Directory Structure

```bash
mkdir -p fastlane
mkdir -p fastlane/metadata/android/en-US/images/phoneScreenshots
mkdir -p fastlane/metadata/android/en-US/images/sevenInchScreenshots
mkdir -p fastlane/metadata/android/en-US/images/tenInchScreenshots
mkdir -p fastlane/metadata/android/en-US/changelogs
```

### Step 5: Create Appfile

Create `./fastlane/Appfile`:

```ruby
# Path to service account JSON for Play Store API
json_key_file(ENV['PLAY_STORE_SERVICE_ACCOUNT'] || "service-account.json")

# Your app's package name
package_name("{PACKAGE_NAME}")
```

**Important:** Replace `{PACKAGE_NAME}` with the actual package name.

### Step 6: Create Fastfile

Create `./fastlane/Fastfile` with comprehensive deployment lanes:

```ruby
default_platform(:android)

platform :android do
  # ============================================
  # Build Lanes
  # ============================================

  desc "Build debug APK and test APK for screenshots"
  lane :build_for_screenshots do
    gradle(task: "clean")
    gradle(task: "assembleDebug")
    gradle(task: "assembleAndroidTest")
  end

  desc "Build release bundle"
  lane :build_release do
    gradle(task: "clean")
    gradle(task: "bundleRelease")
  end

  # ============================================
  # Screenshot Lane
  # ============================================

  desc "Capture screenshots for Play Store"
  lane :screenshots do
    build_for_screenshots
    capture_android_screenshots
  end

  # ============================================
  # Deployment Lanes
  # ============================================

  desc "Deploy to internal testing track"
  lane :deploy_internal do
    build_release
    upload_to_play_store(
      track: "internal",
      release_status: "completed",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Deploy to beta/closed testing track"
  lane :deploy_beta do |options|
    build_release

    # Support staged rollout
    rollout = options[:rollout] || 1.0

    upload_to_play_store(
      track: "beta",
      release_status: rollout < 1.0 ? "inProgress" : "completed",
      rollout: rollout < 1.0 ? rollout.to_s : nil,
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Deploy to production track"
  lane :deploy_production do |options|
    build_release

    # Default to 10% staged rollout for safety
    rollout = options[:rollout] || 0.1

    upload_to_play_store(
      track: "production",
      release_status: rollout < 1.0 ? "inProgress" : "completed",
      rollout: rollout < 1.0 ? rollout.to_s : nil,
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Increase production rollout percentage"
  lane :increase_rollout do |options|
    rollout = options[:rollout] || 0.5

    upload_to_play_store(
      track: "production",
      release_status: rollout < 1.0 ? "inProgress" : "completed",
      rollout: rollout < 1.0 ? rollout.to_s : nil,
      skip_upload_aab: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Halt production rollout"
  lane :halt_rollout do
    upload_to_play_store(
      track: "production",
      release_status: "halted",
      skip_upload_aab: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  # ============================================
  # Metadata Lanes
  # ============================================

  desc "Upload metadata only (no APK/AAB)"
  lane :upload_metadata do
    upload_to_play_store(
      skip_upload_aab: true,
      skip_upload_apk: true
    )
  end

  desc "Upload screenshots only"
  lane :upload_screenshots do
    upload_to_play_store(
      skip_upload_aab: true,
      skip_upload_apk: true,
      skip_upload_metadata: true
    )
  end

  # ============================================
  # Version Management
  # ============================================

  desc "Get current version from version.properties"
  lane :get_version do
    version_file = "../version.properties"
    if File.exist?(version_file)
      props = {}
      File.readlines(version_file).each do |line|
        key, value = line.strip.split("=")
        props[key] = value if key && value
      end
      UI.message("Version: #{props['VERSION_NAME']} (#{props['VERSION_CODE']})")
      props
    else
      UI.user_error!("version.properties not found. Run /devtools:version-management first.")
    end
  end

  # ============================================
  # Full Release Workflows
  # ============================================

  desc "Full internal release: screenshots + build + deploy"
  lane :release_internal do
    screenshots
    deploy_internal
  end

  desc "Full beta release: build + deploy"
  lane :release_beta do |options|
    deploy_beta(rollout: options[:rollout])
  end

  desc "Full production release: build + deploy with staged rollout"
  lane :release_production do |options|
    deploy_production(rollout: options[:rollout])
  end
end
```

### Step 7: Create Screengrabfile

Create `./fastlane/Screengrabfile`:

```ruby
# App package name
app_package_name("{PACKAGE_NAME}")

# Test instrumentation runner (AndroidX)
test_instrumentation_runner("androidx.test.runner.AndroidJUnitRunner")

# APK paths
app_apk_path("app/build/outputs/apk/debug/app-debug.apk")
tests_apk_path("app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk")

# Locales to capture (add more as needed)
locales(["en-US"])

# Output directory (matches supply's expected structure)
output_directory("fastlane/metadata/android")

# Clear old screenshots
clear_previous_screenshots(true)

# Use specific test class for screenshots
use_tests_in_classes(["{PACKAGE_NAME}.screenshots.ScreenshotTest"])

# Ending locale (restore device to this locale after)
ending_locale("en-US")
```

**Important:** Replace `{PACKAGE_NAME}` with the actual package name.

### Step 8: Create Metadata Templates

Create initial metadata files:

#### `fastlane/metadata/android/en-US/title.txt`:
```
Your App Name
```

#### `fastlane/metadata/android/en-US/short_description.txt`:
```
Short description (max 80 characters)
```

#### `fastlane/metadata/android/en-US/full_description.txt`:
```
Full description of your app.

Features:
• Feature 1
• Feature 2
• Feature 3

For more information, visit our website.
```

#### `fastlane/metadata/android/en-US/changelogs/default.txt`:
```
• Bug fixes and performance improvements
```

#### `fastlane/metadata/android/en-US/video.txt`:
```
```
(Empty file - add YouTube URL if you have a promo video)

### Step 9: Update .gitignore

Add to `.gitignore`:

```gitignore
# Fastlane
fastlane/report.xml
fastlane/Preview.html
fastlane/screenshots
fastlane/test_output
fastlane/readme.md
vendor/bundle

# Don't ignore metadata (we want to track store listing)
!fastlane/metadata/
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Verify Fastlane installed
bundle exec fastlane --version

# Verify lanes are available
bundle exec fastlane lanes

# Test service account connection (optional, requires service account JSON)
# bundle exec fastlane run validate_play_store_json_key
```

**Expected output:**
- Fastlane version number
- List of all lanes (deploy_internal, deploy_beta, etc.)

## Completion Criteria

- [ ] `Gemfile` exists with fastlane and screengrab
- [ ] `bundle install` succeeds
- [ ] `fastlane/Appfile` configured with package name
- [ ] `fastlane/Fastfile` has all deployment lanes
- [ ] `fastlane/Screengrabfile` configured
- [ ] Metadata directory structure created
- [ ] Metadata template files created
- [ ] `.gitignore` updated
- [ ] `bundle exec fastlane lanes` shows all lanes

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Gemfile | ./Gemfile | Ruby dependencies |
| Gemfile.lock | ./Gemfile.lock | Locked dependency versions |
| Appfile | ./fastlane/Appfile | Fastlane app configuration |
| Fastfile | ./fastlane/Fastfile | Fastlane lanes |
| Screengrabfile | ./fastlane/Screengrabfile | Screenshot configuration |
| Metadata | ./fastlane/metadata/android/en-US/ | Store listing metadata |

## Troubleshooting

### "Ruby not found"
**Cause:** Ruby not installed
**Fix:** Install Ruby 2.7+ (use rbenv, rvm, or system package manager)

### "bundle: command not found"
**Cause:** Bundler not installed
**Fix:** Run `gem install bundler --no-document`

### "Fastlane lanes don't show"
**Cause:** Fastfile has syntax errors
**Fix:** Run `bundle exec fastlane lanes` and check for Ruby syntax errors

### "Service account validation fails"
**Cause:** Invalid or missing service account JSON
**Fix:** Ensure JSON file exists and has correct permissions in Play Console

## Next Steps

After completing this skill:
1. Run `/devtools:android-app-icon` to generate app icon
2. Run `/devtools:android-screenshot-automation` to setup screenshot capture
3. Run `/devtools:android-store-listing` to create feature graphic and metadata
4. Run `/devtools:android-workflow-internal` to setup GitHub Actions
