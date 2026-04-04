---
name: mobile-offline-support
description: >
  Implement offline-first mobile apps with local storage, sync strategies, and
  conflict resolution. Covers AsyncStorage, Realm, SQLite, and background sync
  patterns.
---

# Mobile Offline Support

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Reference Guides](#reference-guides)
- [Best Practices](#best-practices)

## Overview

Design offline-first mobile applications that provide seamless user experience regardless of connectivity.

## When to Use

- Building apps that work without internet connection
- Implementing seamless sync when connectivity returns
- Handling data conflicts between device and server
- Reducing server load with intelligent caching
- Improving app responsiveness with local storage

## Quick Start

Minimal working example:

```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

class StorageManager {
  static async saveItems(items) {
    try {
      await AsyncStorage.setItem(
        'items_cache',
        JSON.stringify({ data: items, timestamp: Date.now() })
      );
    } catch (error) {
      console.error('Failed to save items:', error);
    }
  }

  static async getItems() {
    try {
      const data = await AsyncStorage.getItem('items_cache');
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Failed to retrieve items:', error);
      return null;
    }
  }

// ... (see reference guides for full implementation)
```

## Reference Guides

Detailed implementations in the `references/` directory:

| Guide | Contents |
|---|---|
| [React Native Offline Storage](references/react-native-offline-storage.md) | React Native Offline Storage |
| [iOS Core Data Implementation](references/ios-core-data-implementation.md) | iOS Core Data Implementation |
| [Android Room Database](references/android-room-database.md) | Android Room Database |

## Best Practices

### ✅ DO

- Implement robust local storage
- Use automatic sync when online
- Provide visual feedback for offline status
- Queue actions for later sync
- Handle conflicts gracefully
- Cache frequently accessed data
- Implement proper error recovery
- Test offline scenarios thoroughly
- Use compression for large data
- Monitor storage usage

### ❌ DON'T

- Assume constant connectivity
- Sync large files frequently
- Ignore storage limitations
- Force unnecessary syncing
- Lose data on offline mode
- Store sensitive data unencrypted
- Accumulate infinite queue items
- Ignore sync failures silently
- Sync in tight loops
- Deploy without offline testing
