---
name: fastlane
description: >
  iOS and Android app deployment automation with Fastlane. Use when building,
  signing, and distributing apps to TestFlight, App Store, or Google Play.
  Covers Match code signing, CI/CD keychain setup, and Tauri integration.
  Triggers on Fastfile, Appfile, Matchfile, fastlane commands.
---

# Fastlane Deployment Skill

> Automate iOS and Android app building, code signing, and distribution.

## When to Apply

Reference this skill when:
- Setting up Fastlane for a new project
- Configuring code signing with Match
- Building lanes for TestFlight or App Store distribution
- Setting up Android Play Store deployment
- Debugging code signing or build failures
- Configuring CI/CD pipelines for mobile apps
- Integrating Fastlane with Tauri v2 projects

## Quick Start

### Minimal Fastfile Structure

```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    match(type: "appstore", readonly: true)
    build_app(scheme: "MyApp")
    upload_to_testflight
  end
end

platform :android do
  desc "Build and upload to Play Store beta"
  lane :beta do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(track: "beta")
  end
end
```

## Tool Aliases

Fastlane provides shorter aliases for common actions:

| Alias | Action | Purpose |
|-------|--------|---------|
| `gym` | `build_app` | Build and sign iOS/macOS apps |
| `pilot` | `upload_to_testflight` | Upload to TestFlight |
| `deliver` | `upload_to_app_store` | Submit to App Store |
| `supply` | `upload_to_play_store` | Upload to Google Play |
| `match` | `sync_code_signing` | Sync certificates and profiles |
| `cert` | `get_certificates` | Download signing certificates |
| `sigh` | `get_provisioning_profile` | Download provisioning profiles |
| `scan` | `run_tests` | Run unit and UI tests |
| `snapshot` | `capture_screenshots` | Automated App Store screenshots |
| `frameit` | `frame_screenshots` | Add device frames to screenshots |
| `produce` | `create_app_online` | Create app in App Store Connect |
| `pem` | `get_push_certificate` | Download push notification certs |
| `precheck` | `check_app_store_metadata` | Validate metadata before submission |

## iOS Workflows

### TestFlight Deployment

```ruby
lane :beta do
  # Sync code signing
  match(type: "appstore", readonly: true)

  # Increment build number
  increment_build_number(
    build_number: Time.now.utc.strftime("%y%m%d%H%M")
  )

  # Build the app
  build_app(
    scheme: "MyApp",
    export_method: "app-store",
    output_directory: "./build"
  )

  # Upload to TestFlight
  upload_to_testflight(
    skip_waiting_for_build_processing: true,
    uses_non_exempt_encryption: false
  )
end
```

### App Store Release

```ruby
lane :release do
  match(type: "appstore", readonly: true)

  build_app(
    scheme: "MyApp",
    export_method: "app-store"
  )

  upload_to_app_store(
    skip_screenshots: true,
    skip_metadata: true,
    submit_for_review: false
  )
end
```

### App Store Connect API Key

```ruby
def api_key
  app_store_connect_api_key(
    key_id: ENV['APP_STORE_CONNECT_API_KEY_KEY_ID'],
    issuer_id: ENV['APP_STORE_CONNECT_API_KEY_ISSUER_ID'],
    key_content: ENV['APP_STORE_CONNECT_API_KEY_KEY'],
    is_key_content_base64: true
  )
end

lane :beta do
  upload_to_testflight(api_key: api_key)
end
```

## Android Workflows

### Play Store Beta

```ruby
platform :android do
  lane :beta do
    gradle(
      task: "bundle",
      build_type: "Release",
      project_dir: "./android"
    )

    upload_to_play_store(
      track: "beta",
      aab: "./android/app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true,
      skip_upload_images: true
    )
  end
end
```

### Play Store Production

```ruby
lane :release do
  gradle(task: "bundle", build_type: "Release")

  upload_to_play_store(
    track: "production",
    aab: "./android/app/build/outputs/bundle/release/app-release.aab"
  )
end
```

## Code Signing with Match

### Initial Setup

```bash
# Initialize Match configuration
fastlane match init

# Generate certificates (run once per team)
fastlane match appstore
fastlane match development
```

### Matchfile Configuration

```ruby
# fastlane/Matchfile
git_url("git@github.com:your-org/certificates.git")
storage_mode("git")
type("appstore")
app_identifier("com.example.app")
team_id("TEAM_ID")
```

### S3/MinIO Storage (Alternative to Git)

```ruby
# Matchfile for S3-compatible storage
storage_mode("s3")
s3_region("us-east-1")
s3_bucket("certificates")
s3_access_key(ENV['AWS_ACCESS_KEY_ID'])
s3_secret_access_key(ENV['AWS_SECRET_ACCESS_KEY'])

# For MinIO, set endpoint
# ENV['AWS_ENDPOINT_URL'] = "https://minio.example.com"
```

### Using Match in Lanes

```ruby
lane :beta do
  match(
    type: "appstore",
    readonly: true,  # Don't create new certs
    keychain_name: ENV['CI'] ? "fastlane_ci" : nil,
    keychain_password: ENV['CI'] ? "fastlane_ci_password" : nil
  )
end
```

## CI/CD Integration

### Keychain Setup for CI

```ruby
CI_KEYCHAIN_NAME = "fastlane_ci"
CI_KEYCHAIN_PASSWORD = "fastlane_ci_password"

def setup_ci_keychain
  if ENV['CI']
    create_keychain(
      name: CI_KEYCHAIN_NAME,
      password: CI_KEYCHAIN_PASSWORD,
      default_keychain: true,
      unlock: true,
      timeout: 3600,
      lock_when_sleeps: false,
      add_to_search_list: true
    )
  end
end

def cleanup_ci_keychain
  if ENV['CI']
    delete_keychain(name: CI_KEYCHAIN_NAME)
  end
end

lane :beta do
  setup_ci_keychain
  match(
    type: "appstore",
    keychain_name: CI_KEYCHAIN_NAME,
    keychain_password: CI_KEYCHAIN_PASSWORD
  )
  # ... build and upload
  cleanup_ci_keychain
end
```

### GitHub Actions Example

```yaml
# .github/workflows/ios.yml
name: iOS Build
on: [push]

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Fastlane
        run: brew install fastlane

      - name: Build and Deploy
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_URL: ${{ secrets.MATCH_GIT_URL }}
          APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.ASC_KEY_CONTENT }}
          CI: true
        run: fastlane ios beta
```

## Environment Variables

### iOS (App Store Connect)

| Variable | Description |
|----------|-------------|
| `APP_STORE_CONNECT_API_KEY_KEY_ID` | API Key ID from App Store Connect |
| `APP_STORE_CONNECT_API_KEY_ISSUER_ID` | Issuer ID from App Store Connect |
| `APP_STORE_CONNECT_API_KEY_KEY` | Base64-encoded .p8 key content |
| `MATCH_PASSWORD` | Encryption password for Match |
| `MATCH_GIT_URL` | Git repository URL for certificates |

### Android (Google Play)

| Variable | Description |
|----------|-------------|
| `SUPPLY_JSON_KEY_DATA` | Google Play service account JSON (base64) |
| `SUPPLY_JSON_KEY` | Path to service account JSON file |

### Encoding API Keys

```bash
# Encode .p8 file to base64
base64 -i AuthKey_XXXXXXXXXX.p8 | tr -d '\n'

# Encode Google Play JSON
base64 -i play-store-key.json | tr -d '\n'
```

## App Store Requirements

### Metadata Character Limits

| Field | Limit |
|-------|-------|
| App Name | 30 characters |
| Subtitle | 30 characters |
| Keywords | 100 characters |
| Description | 4000 characters |
| Release Notes | 4000 characters |
| Promotional Text | 170 characters |

### Screenshot Requirements (2024)

| Device | Size | Required |
|--------|------|----------|
| iPhone 6.7" | 1290 x 2796 | Yes (primary) |
| iPhone 6.5" | 1284 x 2778 | Alternative |
| iPhone 5.5" | 1242 x 2208 | Optional |
| iPad Pro 12.9" | 2048 x 2732 | If iPad supported |
| iPad Pro 11" | 1668 x 2388 | Alternative |

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| "Multiple commands produce" | Duplicate files in build | Remove duplicates from sources |
| Code signing fails in CI | No keychain access | Use `create_keychain` + Match |
| Build number rejected | Duplicate build number | Use timestamp: `Time.now.utc.strftime("%y%m%d%H%M")` |
| Profile not found | Wrong Match type | Use `appstore` for TestFlight/App Store |
| Invalid PEM format | Wrong key encoding | Ensure base64 with `is_key_content_base64: true` |
| "Missing compliance" | Encryption declaration | Set `uses_non_exempt_encryption: false` |
| Gradle build fails | Missing SDK/NDK | Set `ANDROID_HOME` and `ANDROID_NDK_HOME` |

## Tauri Integration

### Version from Cargo.toml

```ruby
ROOT_DIR = File.expand_path("..", __dir__)

def get_app_version
  cargo_toml = File.read("#{ROOT_DIR}/src-tauri/Cargo.toml")
  if cargo_toml =~ /^version\s*=\s*"([^"]+)"/
    $1
  else
    "1.0.0"
  end
end

def get_next_build_number
  Time.now.utc.strftime("%y%m%d%H%M").to_i
end
```

### Update tauri.conf.json

```ruby
def update_tauri_config_version
  app_version = get_app_version
  build_number = get_next_build_number

  tauri_conf_path = "#{ROOT_DIR}/src-tauri/tauri.conf.json"
  tauri_conf = JSON.parse(File.read(tauri_conf_path))
  tauri_conf["version"] = app_version
  tauri_conf["bundle"] ||= {}
  tauri_conf["bundle"]["iOS"] ||= {}
  tauri_conf["bundle"]["iOS"]["bundleVersion"] = build_number.to_s

  File.write(tauri_conf_path, JSON.pretty_generate(tauri_conf))
end
```

### Fix Tauri project.yml (Duplicate libapp.a)

```ruby
def fix_tauri_project_yml
  project_yml_path = "#{ROOT_DIR}/src-tauri/gen/apple/project.yml"
  return unless File.exist?(project_yml_path)

  content = File.read(project_yml_path)

  # Remove "- path: Externals" to prevent duplicate libapp.a
  if content.include?("- path: Externals")
    content.gsub!(/^\s*- path: Externals\n/, "")
    File.write(project_yml_path, content)
    sh("cd #{ROOT_DIR}/src-tauri/gen/apple && xcodegen generate")
  end
end
```

### Tauri iOS Build Lane

```ruby
lane :beta do
  match(type: "appstore", readonly: true)

  update_tauri_config_version
  fix_tauri_project_yml

  # Configure signing
  update_code_signing_settings(
    use_automatic_signing: false,
    path: "#{ROOT_DIR}/src-tauri/gen/apple/MyApp.xcodeproj",
    team_id: TEAM_ID,
    bundle_identifier: APP_IDENTIFIER,
    profile_name: "match AppStore #{APP_IDENTIFIER}",
    code_sign_identity: "Apple Distribution"
  )

  # Build with Tauri
  sh("cd #{ROOT_DIR}/src-tauri && npx tauri ios build --export-method app-store-connect")

  upload_to_testflight(
    ipa: "#{ROOT_DIR}/src-tauri/gen/apple/build/arm64/MyApp.ipa",
    skip_waiting_for_build_processing: true
  )
end
```

### Tauri Android Build Lane

```ruby
platform :android do
  lane :beta do
    ENV['ANDROID_HOME'] = "/opt/homebrew/share/android-commandlinetools"
    ENV['ANDROID_NDK_HOME'] = "#{ENV['ANDROID_HOME']}/ndk/28.2.13676358"

    # Update version in tauri.conf.json
    app_version = get_app_version
    build_number = get_next_build_number

    tauri_conf_path = "#{ROOT_DIR}/src-tauri/tauri.conf.json"
    tauri_conf = JSON.parse(File.read(tauri_conf_path))
    tauri_conf["version"] = app_version
    tauri_conf["bundle"]["android"] ||= {}
    tauri_conf["bundle"]["android"]["versionCode"] = build_number
    File.write(tauri_conf_path, JSON.pretty_generate(tauri_conf))

    # Build with Tauri
    sh("cd #{ROOT_DIR}/src-tauri && npx tauri android build")

    upload_to_play_store(
      track: "beta",
      aab: "#{ROOT_DIR}/src-tauri/gen/android/app/build/outputs/bundle/release/app-release.aab"
    )
  end
end
```

## Essential Commands

```bash
# Initialize Fastlane
fastlane init

# List available actions
fastlane actions

# Run a specific lane
fastlane ios beta
fastlane android release

# Debug with verbose output
fastlane ios beta --verbose

# Run Match commands
fastlane match appstore
fastlane match development
fastlane match nuke distribution  # Reset all distribution certs
```

## Sources

- [Fastlane Documentation](https://docs.fastlane.tools/)
- [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
- [Google Play Developer API](https://developers.google.com/android-publisher)
- [Tauri v2 Mobile Guide](https://v2.tauri.app/distribute/)
