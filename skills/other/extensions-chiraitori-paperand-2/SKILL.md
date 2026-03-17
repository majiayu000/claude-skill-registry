---
name: Extension System
description: Paperback-compatible extension runtime and source API
---

# Extension System

## Architecture

Extensions run in an isolated WebView (`ExtensionRunner.tsx`) that:
1. Loads Paperback-compatible JavaScript bundles
2. Executes source methods via message passing
3. Returns manga/chapter data to the app

## Source Service API

```typescript
import { sourceService } from '../services/sourceService';

// Get discover sections (homepage)
const sections = await sourceService.getDiscoverSections(sourceId);

// Get manga from a section
const manga = await sourceService.getDiscoverSection(sourceId, sectionId);

// Search manga
const results = await sourceService.searchManga(sourceId, query);

// Get manga details
const details = await sourceService.getMangaDetails(sourceId, mangaId);

// Get chapter list
const chapters = await sourceService.getChapters(sourceId, mangaId);

// Get chapter pages (image URLs)
const pages = await sourceService.getChapterPages(sourceId, chapterId);
```

## Extension Service

```typescript
import { extensionService } from '../services/extensionService';

// Get installed extensions
const extensions = await extensionService.getInstalledExtensions();

// Install extension
await extensionService.installExtension(repositoryUrl, extensionId);

// Uninstall extension
await extensionService.uninstallExtension(extensionId);

// Get extension info
const info = await extensionService.getExtensionInfo(extensionId);
```

## Data Types

```typescript
interface Manga {
  id: string;
  title: string;
  image: string;
  author?: string;
  artist?: string;
  desc?: string;
  status?: string;
  genres?: string[];
}

interface Chapter {
  id: string;
  mangaId: string;
  title: string;
  chapNum?: number;
  volume?: number;
  time?: Date;
  langCode?: string;
}

interface Extension {
  id: string;
  name: string;
  version: string;
  icon: string;
  sourceId: string;
  repositoryUrl: string;
}
```

## Extension Runner Component

```typescript
// ExtensionRunner.tsx handles WebView communication
<ExtensionRunner
  sourceId={sourceId}
  onReady={() => setLoaded(true)}
  onError={(error) => console.error(error)}
/>
```

## WebView Message Protocol

```typescript
// App -> WebView
webViewRef.current.postMessage(JSON.stringify({
  type: 'getMangaDetails',
  mangaId: 'manga-123',
}));

// WebView -> App (via onMessage)
const handleMessage = (event) => {
  const { type, data, error } = JSON.parse(event.nativeEvent.data);
  if (type === 'mangaDetails') {
    setManga(data);
  }
};
```

## Repository Format

Extensions are hosted in repositories with this structure:

```
repository/
├── versioning.json    # Repository metadata
├── sources/
│   ├── source1/
│   │   ├── source.js  # Extension bundle
│   │   └── info.json  # Extension metadata
│   └── source2/
│       └── ...
```

## Adding New Source Support

1. Extension must implement Paperback source interface
2. Bundle is loaded via WebView
3. Methods are called via message passing
4. Results are parsed and returned to app

## Error Handling

```typescript
try {
  const manga = await sourceService.getMangaDetails(sourceId, mangaId);
} catch (error) {
  if (error.message.includes('timeout')) {
    // Extension took too long
  } else if (error.message.includes('not found')) {
    // Manga doesn't exist
  } else {
    // Generic error
  }
}
```
