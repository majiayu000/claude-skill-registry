---
name: post-deploy
description: >-
  Mobile post-deployment monitoring and validation. TODO: Implement for mobile.
  Invoked by: "/post-deploy", "verify deployment", "app store check", "crash monitoring".
---

# Post-Deploy (Mobile)

**Status**: Stub - Not Implemented
**Domain**: Mobile

## Overview

Mobile-specific post-deployment skill for monitoring app store submissions, crash reporting, and user feedback after releasing mobile applications via EAS or direct store submission.

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| environment | Target environment | staging, production |
| --platform | Specific platform to check | ios, android |
| --skip-crashlytics | Skip crash monitoring | --skip-crashlytics |

## Usage Examples

```bash
# Run all post-deployment checks
/post-deploy production

# Check iOS App Store status only
/post-deploy production --platform ios

# Check staging without crash monitoring
/post-deploy staging --skip-crashlytics
```

## Mobile-Specific Checks

- App Store Connect review status monitoring
- Google Play Console review status monitoring
- Firebase Crashlytics error spike detection
- Sentry error monitoring
- App rating and review monitoring
- OTA update success rate (for Expo)
- TestFlight/Internal Testing feedback

## TODO

- [ ] Define App Store monitoring workflow
- [ ] Add Crashlytics integration guide
- [ ] Add Sentry integration guide
- [ ] Define review monitoring automation
- [ ] Add OTA update verification for Expo
- [ ] Document rollback procedures for mobile
- [ ] Add user feedback collection workflow

---

**End of Skill**
