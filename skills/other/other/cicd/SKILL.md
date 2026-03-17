---
name: Flutter CI/CD
description: Continuous Integration and Deployment standards for Flutter apps.
metadata:
  labels: [cicd, github-actions, automation, codemagic, fastlane]
  triggers:
    files:
      [
        '.github/workflows/**.yml',
        'fastlane/**',
        'android/fastlane/**',
        'ios/fastlane/**',
      ]
    keywords: [ci, cd, pipeline, build, deploy, release, action, workflow]
---

# CI/CD Standards

## **Priority: P1 (HIGH)**

Automates code quality checks, testing, and deployment to prevent regressions and accelerate delivery.

## Core Pipeline Steps

1. **Environment Setup**: Use stable Flutter channel. Cache dependencies (pub, gradle, cocoapods).
2. **Static Analysis**: Enforce `flutter analyze` and `dart format`. Fail on any warning in strict mode.
3. **Testing**: Run unit, widget, and integration tests. Upload coverage reports (e.g., Codecov).
4. **Build**:
   - **Android**: Build App Bundle (`.aab`) for Play Store.
   - **iOS**: Sign and build `.ipa` (requires macOS runner).
5. **Deployment** (CD): Automated upload to TestFlight/Play Console using standard tools (Fastlane, Codemagic).

## Best Practices

- **Timeout Limits**: Always set `timeout-minutes` (e.g., 30m) to save costs on hung jobs.
- **Fail Fast**: Run Analyze/Format _before_ Tests/Builds.
- **Secrets**: Never commit keys. Use GitHub Secrets or secure vaults for `keystore.jks` and `.p8` certs.
- **Versioning**: Automate version bumping based on git tags or semantic version scripts.

## Reference

- [**GitHub Actions Template**](references/github-actions.md) - Standard workflow file.
- [**Advanced Large-Scale Workflow**](references/advanced-workflow.md) - Parallel jobs, Caching, Strict Mode.
- [**Fastlane Standards**](references/fastlane.md) - Automated Signing & Deployment.

## Related Topics

flutter/testing | dart/tooling
