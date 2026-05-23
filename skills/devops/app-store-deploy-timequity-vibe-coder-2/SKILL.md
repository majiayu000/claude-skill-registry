---
name: app-store-deploy
description: iOS App Store and Google Play submission requirements and process.
---

# App Store Deployment

## iOS App Store

### Requirements

- Apple Developer Account ($99/year)
- App Icon: 1024x1024 PNG
- Screenshots: All required sizes
- Privacy Policy URL
- App Review Guidelines compliance

### EAS Submit

```bash
# Configure credentials
eas credentials

# Submit to App Store Connect
eas submit --platform ios
```

### App Store Connect

1. Create App in App Store Connect
2. Fill metadata (description, keywords, categories)
3. Upload screenshots
4. Set pricing
5. Submit for review

### Common Rejections

| Issue | Solution |
|-------|----------|
| Crash on launch | Test on real devices |
| Incomplete metadata | Fill all required fields |
| Placeholder content | Use real content |
| Login required | Provide demo account |

## Google Play

### Requirements

- Google Play Developer Account ($25 one-time)
- App Icon: 512x512 PNG
- Feature Graphic: 1024x500
- Screenshots: Phone + 7" + 10" tablets

### EAS Submit

```bash
# First time: upload manually
# Then: eas submit --platform android
```

### Play Console

1. Create app in Play Console
2. Complete app content questionnaire
3. Set up pricing and distribution
4. Upload AAB (not APK)
5. Roll out to production

### Pre-Launch Report

- Automatic testing on real devices
- Crash detection
- Performance metrics
- Security scanning

## Testing Tracks

### iOS

- TestFlight: Up to 10,000 testers
- Internal: 100 testers, instant

### Android

- Internal: 100 testers
- Closed: Invite-only
- Open: Public link
- Production: Full release
