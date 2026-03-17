---
name: mobile-offline-support
description: Offline-first mobile apps with local storage, sync queues, conflict resolution. Use for offline functionality, data sync, connectivity handling, or encountering sync conflicts, queue management, storage limits, network transition errors.
---

# Mobile Offline Support

Build offline-first mobile applications with local storage and synchronization.

## React Native Implementation

```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

class OfflineManager {
  constructor() {
    this.syncQueue = [];
    this.isOnline = true;
    // Maximum items in sync queue before discarding oldest
    this.MAX_SYNC_QUEUE_LENGTH = 1000;

    NetInfo.addEventListener(state => {
      this.isOnline = state.isConnected;
      if (this.isOnline) this.processQueue();
    });
  }

  /**
   * Fetch data from server.
   * TODO: Replace with actual API endpoint implementation.
   */
  async fetchFromServer(key) {
    try {
      // Example implementation - replace with your API
      const response = await fetch(`${API_BASE_URL}/data/${key}`);
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('fetchFromServer failed:', error);
      throw new Error(`Failed to fetch ${key}: ${error.message}`);
    }
  }

  /**
   * Sync data to server.
   * TODO: Replace with actual API endpoint implementation.
   */
  async syncToServer(key, data) {
    try {
      // Example implementation - replace with your API
      const response = await fetch(`${API_BASE_URL}/data/${key}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('syncToServer failed:', error);
      throw new Error(`Failed to sync ${key}: ${error.message}`);
    }
  }

  async getData(key) {
    const cached = await AsyncStorage.getItem(key);
    if (cached) return JSON.parse(cached);

    if (this.isOnline) {
      const data = await this.fetchFromServer(key);
      await AsyncStorage.setItem(key, JSON.stringify(data));
      return data;
    }

    return null;
  }

  async saveData(key, data) {
    await AsyncStorage.setItem(key, JSON.stringify(data));

    if (this.isOnline) {
      await this.syncToServer(key, data);
    } else {
      // Add to queue
      this.syncQueue.push({ key, data, timestamp: Date.now() });

      // Enforce queue bounds - discard oldest if exceeded
      while (this.syncQueue.length > this.MAX_SYNC_QUEUE_LENGTH) {
        const discarded = this.syncQueue.shift();
        console.warn(`Sync queue full - discarded oldest item: ${discarded.key}`);
      }

      // Persist trimmed queue
      await AsyncStorage.setItem('syncQueue', JSON.stringify(this.syncQueue));
    }
  }

  async processQueue() {
    const failedItems = [];
    for (const item of this.syncQueue) {
      try {
        await this.syncToServer(item.key, item.data);
      } catch (err) {
        console.error('Sync failed:', err);
        failedItems.push(item);
      }
    }
    this.syncQueue = failedItems;
    if (failedItems.length === 0) {
      await AsyncStorage.removeItem('syncQueue');
    } else {
      await AsyncStorage.setItem('syncQueue', JSON.stringify(failedItems));
    }
  }
}
```

## Conflict Resolution

```javascript
function resolveConflict(local, server) {
  // Last-write-wins
  if (local.updatedAt > server.updatedAt) return local;
  return server;

  // Or merge changes
  // return { ...server, ...local };
}
```

## UI Indicators

```jsx
function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    return NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected);
    });
  }, []);

  if (isOnline) return null;

  return (
    <View style={styles.banner}>
      <Text>You're offline. Changes will sync when connected.</Text>
    </View>
  );
}
```

## Best Practices

- Cache frequently accessed data locally
- Queue actions for later sync
- Show clear offline indicators
- Handle sync conflicts gracefully
- Compress stored data
- Test offline scenarios thoroughly

## Native Implementations

See [references/native-implementations.md](references/native-implementations.md) for:
- iOS Core Data with sync manager
- Android Room database with WorkManager sync

## Avoid

- Assuming connectivity
- Losing data on sync failures
- Unbounded queue growth
- Syncing sensitive data insecurely
