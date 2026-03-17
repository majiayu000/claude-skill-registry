---
name: Download System
description: Background chapter downloads and offline reading
---

# Download System

## Download Service

```typescript
import { downloadService } from '../services/downloadService';

// Download a chapter
await downloadService.downloadChapter(manga, chapter, sourceId);

// Download multiple chapters
await downloadService.downloadChapters(manga, chapters, sourceId);

// Cancel download
await downloadService.cancelDownload(chapterId);

// Get download status
const status = await downloadService.getDownloadStatus(chapterId);

// Get all downloads
const downloads = await downloadService.getAllDownloads();

// Delete downloaded chapter
await downloadService.deleteDownload(chapterId);
```

## Download Status

```typescript
type DownloadStatus = 
  | 'pending'
  | 'downloading'
  | 'completed'
  | 'failed'
  | 'cancelled';

interface Download {
  mangaId: string;
  chapterId: string;
  status: DownloadStatus;
  progress: number;      // 0-100
  totalPages: number;
  downloadedPages: number;
  error?: string;
}
```

## Background Downloads (Android)

Uses `react-native-background-actions`:

```typescript
import BackgroundService from 'react-native-background-actions';

const options = {
  taskName: 'Download',
  taskTitle: 'Downloading chapters',
  taskDesc: 'Chapter 1 of 10',
  taskIcon: { name: 'ic_launcher', type: 'mipmap' },
  progressBar: { max: 100, value: 0 },
};

await BackgroundService.start(downloadTask, options);
await BackgroundService.updateNotification({ taskDesc: 'Chapter 2 of 10' });
await BackgroundService.stop();
```

## Foreground Service (Android 14+)

Required config in `plugins/withBackgroundActionsServiceType.js`:

```javascript
// Adds foregroundServiceType="dataSync" to AndroidManifest.xml
module.exports = function withBackgroundActionsServiceType(config) {
  return withAndroidManifest(config, (config) => {
    // Modify service declaration
    return config;
  });
};
```

## Headless Extension Runtime

When the app goes to background, the `ExtensionRunner` WebView may become unavailable.
The `headlessExtensionRuntime.ts` provides a fallback that runs extensions directly in
the React Native JS engine:

```typescript
import { headlessRuntime } from '../services/headlessExtensionRuntime';

// Check if headless runtime is available
if (headlessRuntime.isAvailable()) {
  // Run extension method without WebView
  const result = await headlessRuntime.runExtensionMethod(
    extensionId,
    'getChapterDetails',
    [mangaId, chapterId]
  );
}
```

The headless runtime:
- Executes extension JavaScript using `eval()` in a sandboxed environment
- Provides mock `App` object with `createRequestManager`, `createSourceStateManager`, etc.
- Uses native `fetch` for HTTP requests (no CORS in React Native)
- Falls back automatically when WebView bridge is unavailable

## Storage Structure

```
documentDirectory/
└── downloads/
    └── {mangaId}/
        └── {chapterId}/
            ├── page_001.jpg
            ├── page_002.jpg
            └── ...
```

## File Operations

```typescript
import * as FileSystem from 'expo-file-system';

const downloadDir = `${FileSystem.documentDirectory}downloads/`;

// Create directory
await FileSystem.makeDirectoryAsync(
  `${downloadDir}${mangaId}/${chapterId}`,
  { intermediates: true }
);

// Download image
await FileSystem.downloadAsync(
  imageUrl,
  `${downloadDir}${mangaId}/${chapterId}/page_${index}.jpg`
);

// Check if exists
const info = await FileSystem.getInfoAsync(path);
if (info.exists) { /* ... */ }

// Delete
await FileSystem.deleteAsync(path, { idempotent: true });
```

## Download Queue

```typescript
// Queue management
const queue: DownloadTask[] = [];
let isProcessing = false;

async function processQueue() {
  if (isProcessing || queue.length === 0) return;
  isProcessing = true;
  
  const task = queue.shift();
  await downloadChapter(task);
  
  isProcessing = false;
  processQueue(); // Process next
}

function addToQueue(task: DownloadTask) {
  queue.push(task);
  processQueue();
}
```

## Notifications

```typescript
import * as Notifications from 'expo-notifications';

// Show progress notification
await Notifications.scheduleNotificationAsync({
  content: {
    title: 'Downloading',
    body: `${manga.title} - Chapter ${chapter.chapNum}`,
    data: { mangaId, chapterId },
  },
  trigger: null, // Immediate
});
```
