---
name: jutsu-expo:expo-updates
description: Use when implementing over-the-air (OTA) updates with Expo Updates. Covers update configuration, checking for updates, and update strategies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Expo Updates

Use this skill when implementing over-the-air (OTA) updates to deploy JavaScript and asset updates without app store releases.

## Key Concepts

### Configuration

```json
// app.json
{
  "expo": {
    "updates": {
      "enabled": true,
      "checkAutomatically": "ON_LOAD",
      "fallbackToCacheTimeout": 0,
      "url": "https://u.expo.dev/[project-id]"
    },
    "runtimeVersion": {
      "policy": "sdkVersion"
    }
  }
}
```

### Checking for Updates

```tsx
import * as Updates from 'expo-updates';
import { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';

export default function App() {
  const [updateAvailable, setUpdateAvailable] = useState(false);

  useEffect(() => {
    async function checkForUpdates() {
      if (!__DEV__) {
        const update = await Updates.checkForUpdateAsync();
        setUpdateAvailable(update.isAvailable);
      }
    }
    checkForUpdates();
  }, []);

  const handleUpdate = async () => {
    const { isNew } = await Updates.fetchUpdateAsync();
    if (isNew) {
      await Updates.reloadAsync();
    }
  };

  if (updateAvailable) {
    return (
      <View>
        <Text>Update Available!</Text>
        <Button title="Update Now" onPress={handleUpdate} />
      </View>
    );
  }

  return <View>{/* Your app */}</View>;
}
```

### Runtime Versions

```typescript
// app.config.ts
export default {
  expo: {
    runtimeVersion: {
      policy: 'appVersion', // Match app version
    },
    // Or use custom logic
    runtimeVersion: '1.0.0',
  },
};
```

## Best Practices

### Update Hook

```tsx
import * as Updates from 'expo-updates';
import { useEffect, useState } from 'react';

export function useUpdates() {
  const [isChecking, setIsChecking] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [updateAvailable, setUpdateAvailable] = useState(false);

  useEffect(() => {
    const subscription = Updates.addListener((event) => {
      if (event.type === Updates.UpdateEventType.UPDATE_AVAILABLE) {
        setUpdateAvailable(true);
      }
    });

    return () => subscription.remove();
  }, []);

  const checkForUpdate = async () => {
    if (__DEV__) return;

    setIsChecking(true);
    try {
      const update = await Updates.checkForUpdateAsync();
      setUpdateAvailable(update.isAvailable);
    } finally {
      setIsChecking(false);
    }
  };

  const downloadAndApplyUpdate = async () => {
    if (__DEV__) return;

    setIsDownloading(true);
    try {
      const update = await Updates.fetchUpdateAsync();
      if (update.isNew) {
        await Updates.reloadAsync();
      }
    } finally {
      setIsDownloading(false);
    }
  };

  return {
    isChecking,
    isDownloading,
    updateAvailable,
    checkForUpdate,
    downloadAndApplyUpdate,
  };
}
```

### Silent Updates

```tsx
import { useEffect } from 'react';
import * as Updates from 'expo-updates';

export function useSilentUpdates() {
  useEffect(() => {
    async function update() {
      if (__DEV__) return;

      try {
        const update = await Updates.checkForUpdateAsync();
        if (update.isAvailable) {
          await Updates.fetchUpdateAsync();
          // Don't reload immediately - wait for next app start
        }
      } catch (error) {
        console.error('Update check failed:', error);
      }
    }

    update();
  }, []);
}
```

## Common Patterns

### Update Screen

```tsx
import * as Updates from 'expo-updates';
import { useState } from 'react';
import { View, Text, Button, ActivityIndicator } from 'react-native';

export function UpdateScreen() {
  const [loading, setLoading] = useState(false);

  const handleUpdate = async () => {
    setLoading(true);
    try {
      const update = await Updates.fetchUpdateAsync();
      if (update.isNew) {
        await Updates.reloadAsync();
      }
    } catch (error) {
      console.error('Update failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
        <Text>Updating...</Text>
      </View>
    );
  }

  return (
    <View>
      <Text>Update Available</Text>
      <Button title="Update Now" onPress={handleUpdate} />
    </View>
  );
}
```

### EAS Update Configuration

```json
// eas.json
{
  "build": {
    "production": {
      "channel": "production"
    },
    "preview": {
      "channel": "preview"
    }
  }
}
```

## Related Skills

- **expo-config**: Configuring updates
- **expo-build**: Building with EAS
