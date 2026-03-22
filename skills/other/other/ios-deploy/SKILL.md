---
name: ios-deploy
cluster: mobile
description: "iOS: Xcode Archive, TestFlight, App Store Connect, certificates, provisioning, Fastlane, Xcode Cloud"
tags: ["deployment","testflight","appstore","fastlane","ios"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ios deploy testflight app store fastlane ci xcode cloud signing"
---

## ios-deploy

### Purpose
This skill automates iOS app deployment workflows, including archiving apps with Xcode, uploading to TestFlight or App Store Connect, managing certificates and provisioning profiles, and integrating with tools like Fastlane and Xcode Cloud. It streamlines CI/CD for iOS projects.

### When to Use
Use this skill when deploying iOS apps to TestFlight for beta testing, submitting to the App Store, or handling signing and provisioning in CI pipelines. Apply it in scenarios involving Fastlane automation, Xcode Cloud builds, or when troubleshooting certificate issues in enterprise environments.

### Key Capabilities
- Archive iOS apps using Xcode's command-line tools with specific build configurations.
- Upload builds to TestFlight via App Store Connect API, requiring authentication.
- Manage certificates and provisioning profiles using Fastlane's match or sigh actions.
- Automate workflows with Fastlane lanes for CI, including code signing and beta deployment.
- Integrate with Xcode Cloud for cloud-based builds and automated testing.
- Handle App Store metadata updates via Spaceship API for release notes and screenshots.

### Usage Patterns
Always start by ensuring Xcode and Fastlane are installed. For CI integration, wrap commands in scripts that check for environment variables like `$FASTLANE_APP_ID`. Use in pipelines where builds are triggered on code changes, followed by automated testing and deployment. For local development, run commands interactively to verify outputs before automation. Include error checks in scripts to halt on failures, e.g., verify provisioning profiles exist before archiving.

### Common Commands/API
Use Fastlane for most tasks; here's how to execute key operations:
- **Archive and build an app**: Run `xcodebuild archive -scheme MyApp -archivePath build/MyApp.xcarchive -configuration Release`. Follow with `xcodebuild -exportArchive -archivePath build/MyApp.xcarchive -exportPath build/export -exportOptionsPlist exportOptions.plist`.
- **Upload to TestFlight**: Use Fastlane: `fastlane upload_to_testflight` with config in Fastfile: `lane :beta do |options| upload_to_testflight(changelog: options[:changelog]) end`. Requires `$APP_STORE_CONNECT_API_KEY` in env vars.
- **Manage certificates**: Run `fastlane match development` to create or download profiles; config via Matchfile with `type: "development"` and `git_url: "git@github.com:user/repo.git"`.
- **Xcode Cloud API**: Trigger builds via API endpoint: POST to `https://api.apple.com/v1/builds` with JSON payload `{ "workflowId": "12345", "sourceBranch": "main" }`, authenticated with `$XCODE_CLOUD_TOKEN`.
- **App Store Connect API**: Fetch app info with `spaceship::Tunes::App.find("com.example.app")` in a Ruby script: `require 'spaceship'; Spaceship::Tunes.login; app = Spaceship::Tunes::App.find('bundle_id')`.

### Integration Notes
Integrate by adding Fastlane to your project via `gem install fastlane`, then create a Fastfile in the root directory. For authentication, set env vars like `export FASTLANE_SESSION=$APP_STORE_CONNECT_API_KEY` for App Store Connect access. Use Xcode Cloud by enabling it in App Store Connect and referencing the workflow ID in scripts. For CI tools like GitHub Actions, include steps like: `run: fastlane beta` in your YAML file, ensuring dependencies are cached. Handle multiple environments by using Fastlane's lanes, e.g., define a lane for staging with different provisioning profiles.

### Error Handling
Common errors include invalid certificates; check with `fastlane match nuke development` to reset and retry. For upload failures, verify API key with `fastlane spaceauth -o` and ensure bundle ID matches. If archiving fails due to code signing, run `fastcode sign --force` and specify the profile in exportOptions.plist: `<key>signingStyle</key><string>Manual</string>`. Handle network errors in scripts by adding retries, e.g., in bash: `for i in {1..3}; do fastlane upload_to_testflight && break || sleep 5; done`. Log outputs with `fastlane --verbose` for debugging.

### Concrete Usage Examples
1. **Deploy to TestFlight**: In a CI script, first build: `xcodebuild -scheme MyApp -configuration Release clean build`. Then upload: `fastlane run upload_to_testflight api_key: $APP_STORE_CONNECT_API_KEY changelog: "Fixed bugs"`. This assumes a Fastfile with the lane defined and env var set.
2. **Manage Provisioning and Archive**: Run `fastlane match adhoc` to fetch profiles, then archive: `xcodebuild archive -scheme MyApp -archivePath build/MyApp.xcarchive`. Export with: `xcodebuild -exportArchive -archivePath build/MyApp.xcarchive -exportOptionsPlist ExportOptions.plist`. Use in a workflow for ad-hoc distribution.

### Graph Relationships
- Related to: mobile cluster (e.g., android-deploy skill for cross-platform deployment).
- Connected via: deployment tag (links to general deployment skills like ci-cd).
- Associated with: fastlane and ios tags (e.g., relates to fastlane-specific tools and other iOS skills).
- Dependencies: appstore tag implies integration with skills handling API keys and authentication.
