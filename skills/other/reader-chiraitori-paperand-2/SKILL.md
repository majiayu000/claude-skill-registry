---
name: Manga Reader
description: Reader screen patterns and image handling
---

# Manga Reader

## Reader Modes

| Mode | Description | Implementation |
|------|-------------|----------------|
| Vertical | Scroll through pages | FlatList vertical |
| Horizontal | Swipe left/right | FlatList horizontal paging |
| Webtoon | Long strip format | FlatList with variable height |

## Reader Screen Structure

```typescript
function ReaderScreen() {
  const { manga, chapter, sourceId } = useRoute().params;
  const [pages, setPages] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [readerMode, setReaderMode] = useState('vertical');

  useEffect(() => {
    loadPages();
  }, [chapter]);

  const loadPages = async () => {
    const urls = await sourceService.getChapterPages(sourceId, chapter.id);
    setPages(urls);
  };

  return (
    <View style={styles.container}>
      {readerMode === 'vertical' ? (
        <VerticalReader pages={pages} onPageChange={setCurrentPage} />
      ) : (
        <HorizontalReader pages={pages} onPageChange={setCurrentPage} />
      )}
      <ReaderOverlay 
        currentPage={currentPage} 
        totalPages={pages.length}
        chapter={chapter}
      />
    </View>
  );
}
```

## Vertical Reader

```typescript
<FlatList
  data={pages}
  keyExtractor={(_, index) => `page-${index}`}
  renderItem={({ item: url, index }) => (
    <Image
      source={{ uri: url }}
      style={styles.page}
      contentFit="contain"
      cachePolicy="memory-disk"
    />
  )}
  onViewableItemsChanged={handleViewableChange}
  viewabilityConfig={{ itemVisiblePercentThreshold: 50 }}
/>
```

## Horizontal Reader

```typescript
<FlatList
  data={pages}
  horizontal
  pagingEnabled
  showsHorizontalScrollIndicator={false}
  keyExtractor={(_, index) => `page-${index}`}
  renderItem={({ item: url }) => (
    <View style={styles.pageContainer}>
      <Image source={{ uri: url }} style={styles.fullPage} />
    </View>
  )}
  getItemLayout={(_, index) => ({
    length: screenWidth,
    offset: screenWidth * index,
    index,
  })}
  onMomentumScrollEnd={handleScrollEnd}
/>
```

## Reading Progress

```typescript
const { updateProgress } = useLibrary();

// Save progress on page change
useEffect(() => {
  updateProgress(manga.id, chapter.id, currentPage);
}, [currentPage]);

// Restore progress on load
useEffect(() => {
  const savedPage = readingProgress[manga.id]?.page || 0;
  flatListRef.current?.scrollToIndex({ index: savedPage });
}, []);
```

## Screen Orientation

```typescript
import * as ScreenOrientation from 'expo-screen-orientation';

// Lock on enter
useEffect(() => {
  ScreenOrientation.unlockAsync(); // Allow all orientations

  return () => {
    ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.PORTRAIT);
  };
}, []);
```

## Gesture Handling

```typescript
// Tap zones for navigation
const handleTap = (x: number) => {
  const width = Dimensions.get('window').width;
  if (x < width * 0.3) {
    goToPreviousPage();
  } else if (x > width * 0.7) {
    goToNextPage();
  } else {
    toggleOverlay();
  }
};
```

## Chapter Navigation

```typescript
// Go to next chapter
const goToNextChapter = () => {
  const currentIndex = chapters.findIndex(c => c.id === chapter.id);
  if (currentIndex > 0) {
    navigation.replace('Reader', {
      manga,
      chapter: chapters[currentIndex - 1],
      sourceId,
    });
  }
};
```

## Image Prefetching

```typescript
import { Image } from 'expo-image';

// Prefetch next pages
useEffect(() => {
  const nextPages = pages.slice(currentPage + 1, currentPage + 4);
  nextPages.forEach(url => Image.prefetch(url));
}, [currentPage]);
```

## Full Screen Mode

```typescript
import * as NavigationBar from 'expo-navigation-bar';
import { StatusBar } from 'expo-status-bar';

// Hide UI
<StatusBar hidden={isFullScreen} />
await NavigationBar.setVisibilityAsync('hidden');
```
