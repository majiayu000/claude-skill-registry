---
name: expo-workflows
description: Expo SDK, EAS Build, EAS Update, and managed workflow best practices.
---

# Expo Workflows

## Project Setup

```bash
# Create new project
npx create-expo-app@latest my-app --template tabs

# Install dependencies
npx expo install expo-router expo-status-bar
```

## EAS Build

```json
// eas.json
{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

```bash
# Build for iOS
eas build --platform ios --profile production

# Build for Android
eas build --platform android --profile production
```

## EAS Update (OTA)

```bash
# Configure
eas update:configure

# Push update
eas update --branch production --message "Bug fixes"
```

```typescript
// Check for updates
import * as Updates from 'expo-updates';

async function checkForUpdates() {
  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync();
  }
}
```

## Environment Variables

```bash
# .env
EXPO_PUBLIC_API_URL=https://api.example.com
```

```typescript
// Usage
const apiUrl = process.env.EXPO_PUBLIC_API_URL;
```

## Common Packages

```bash
npx expo install expo-camera
npx expo install expo-location
npx expo install expo-notifications
npx expo install expo-secure-store
npx expo install expo-image-picker
```

## Development

```bash
# Start dev server
npx expo start

# Run on device
npx expo start --dev-client

# Clear cache
npx expo start -c
```
