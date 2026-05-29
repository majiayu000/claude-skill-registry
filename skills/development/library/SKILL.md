---
name: Library Management
description: User library, favorites, and reading progress
---

# Library Management

## Library Context

```typescript
import { useLibrary } from '../context/LibraryContext';

const {
  // State
  library,           // Manga[] - all saved manga
  favorites,         // string[] - favorite manga IDs
  readingProgress,   // { [mangaId]: { chapterId, page } }
  history,           // HistoryItem[] - reading history
  
  // Actions
  addToLibrary,      // (manga: Manga) => void
  removeFromLibrary, // (mangaId: string) => void
  isInLibrary,       // (mangaId: string) => boolean
  toggleFavorite,    // (mangaId: string) => void
  isFavorite,        // (mangaId: string) => boolean
  updateProgress,    // (mangaId, chapterId, page) => void
  addToHistory,      // (manga, chapter) => void
} = useLibrary();
```

## Add to Library

```typescript
function MangaDetailScreen() {
  const { addToLibrary, removeFromLibrary, isInLibrary } = useLibrary();
  const inLibrary = isInLibrary(manga.id);

  const handleLibraryToggle = () => {
    if (inLibrary) {
      removeFromLibrary(manga.id);
    } else {
      addToLibrary(manga);
    }
  };

  return (
    <Button
      title={inLibrary ? 'Remove from Library' : 'Add to Library'}
      onPress={handleLibraryToggle}
    />
  );
}
```

## Favorites

```typescript
function LibraryScreen() {
  const { library, favorites, toggleFavorite } = useLibrary();

  // Filter favorites
  const favoritesList = library.filter(m => favorites.includes(m.id));

  return (
    <FlatList
      data={library}
      renderItem={({ item }) => (
        <MangaCard
          manga={item}
          isFavorite={favorites.includes(item.id)}
          onFavoritePress={() => toggleFavorite(item.id)}
        />
      )}
    />
  );
}
```

## Reading Progress

```typescript
function ReaderScreen() {
  const { updateProgress, readingProgress } = useLibrary();
  const { manga, chapter } = useRoute().params;

  // Get saved progress
  const savedProgress = readingProgress[manga.id];
  const startPage = savedProgress?.chapterId === chapter.id 
    ? savedProgress.page 
    : 0;

  // Save on page change
  const handlePageChange = (page: number) => {
    updateProgress(manga.id, chapter.id, page);
  };

  return <Reader startPage={startPage} onPageChange={handlePageChange} />;
}
```

## Reading History

```typescript
// Add to history when opening a chapter
const handleOpenChapter = (chapter: Chapter) => {
  addToHistory(manga, chapter);
  navigation.navigate('Reader', { manga, chapter, sourceId });
};

// Display history
function HistoryScreen() {
  const { history } = useLibrary();

  return (
    <FlatList
      data={history}
      keyExtractor={(item) => `${item.mangaId}-${item.chapterId}`}
      renderItem={({ item }) => (
        <HistoryItem
          manga={item.manga}
          chapter={item.chapter}
          timestamp={item.timestamp}
        />
      )}
    />
  );
}
```

## Data Types

```typescript
interface LibraryManga extends Manga {
  addedAt: Date;
  sourceId: string;
}

interface ReadingProgress {
  [mangaId: string]: {
    chapterId: string;
    page: number;
    updatedAt: Date;
  };
}

interface HistoryItem {
  mangaId: string;
  manga: Manga;
  chapterId: string;
  chapter: Chapter;
  timestamp: Date;
  sourceId: string;
}
```

## Storage

```typescript
// AsyncStorage keys
const LIBRARY_KEY = '@library';
const FAVORITES_KEY = '@favorites';
const PROGRESS_KEY = '@reading_progress';
const HISTORY_KEY = '@history';

// Save library
await AsyncStorage.setItem(LIBRARY_KEY, JSON.stringify(library));

// Load library
const json = await AsyncStorage.getItem(LIBRARY_KEY);
const library = json ? JSON.parse(json) : [];
```

## Library Filters

```typescript
type LibraryFilter = 'all' | 'favorites' | 'reading' | 'completed';

function filterLibrary(library: Manga[], filter: LibraryFilter) {
  switch (filter) {
    case 'favorites':
      return library.filter(m => favorites.includes(m.id));
    case 'reading':
      return library.filter(m => readingProgress[m.id]);
    case 'completed':
      return library.filter(m => m.status === 'completed');
    default:
      return library;
  }
}
```
