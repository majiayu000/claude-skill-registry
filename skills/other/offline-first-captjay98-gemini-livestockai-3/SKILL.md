---
name: Offline-First
description: PWA patterns and offline functionality in LivestockAI
---

# Offline-First

LivestockAI is designed to work offline in areas with unreliable internet connectivity.

## Architecture

- **IndexedDB**: Local data persistence
- **Service Worker**: Caching and offline support
- **Sync Queue**: Pending operations stored locally

## Sync Status Indicators

Always show sync status to users:

```
● Synced          - Green dot, all data uploaded
◐ Syncing...      - Animated, upload in progress
○ Offline (3)     - Gray dot, 3 items pending
⚠ Sync Failed     - Red, tap to retry
```

## PWA Configuration

The PWA manifest is in `public/manifest.json`:

```json
{
  "name": "LivestockAI",
  "short_name": "LivestockAI",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#10b981"
}
```

## Offline Data Flow

```
User Action → IndexedDB (local) → Sync Queue → Server (when online)
```

## TanStack Query Persistence

```typescript
import { persistQueryClient } from '@tanstack/react-query-persist-client'
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister'

const persister = createSyncStoragePersister({
  storage: window.localStorage,
})

persistQueryClient({
  queryClient,
  persister,
})
```

## Offline Indicator Component

```typescript
// app/components/offline-indicator.tsx
export function OfflineIndicator() {
  const isOnline = useOnlineStatus()
  const pendingCount = usePendingSync()

  if (isOnline && pendingCount === 0) {
    return <span className="text-green-500">● Synced</span>
  }

  if (!isOnline) {
    return (
      <span className="text-gray-500">
        ○ Offline {pendingCount > 0 && `(${pendingCount})`}
      </span>
    )
  }

  return <span className="text-blue-500">◐ Syncing...</span>
}
```

## Error Recovery

```
┌─────────────────────────────────────────────┐
│ ⚠️ Failed to save feed record               │
│                                              │
│ Check your connection and try again.         │
│                                              │
│ [Retry]                      [Save Offline]  │
└─────────────────────────────────────────────┘
```

## Performance Targets

- Initial load: <3 seconds on 3G
- Offline mode: Full functionality without internet
- Sync performance: <5 seconds for data synchronization

## Related Skills

- `rugged-utility` - Sync status indicators
- `tanstack-query` - Query persistence
