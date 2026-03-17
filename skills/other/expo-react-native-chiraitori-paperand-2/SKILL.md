---
name: Expo React Native Patterns
description: Common patterns for Expo SDK 54 and React Native development
---

# Expo React Native Patterns

## Expo SDK 54 Setup

```bash
# Start dev server
npx expo start

# Run platform
npm run android
npm run ios

# Clear cache
npx expo start -c

# Prebuild native
npx expo prebuild --clean
```

## Component Pattern

```typescript
import React, { useState, useCallback } from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';

interface Props {
  title: string;
  onPress: () => void;
}

export function MyComponent({ title, onPress }: Props) {
  const [loading, setLoading] = useState(false);

  const handlePress = useCallback(async () => {
    setLoading(true);
    await onPress();
    setLoading(false);
  }, [onPress]);

  return (
    <Pressable onPress={handlePress} style={styles.container}>
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  text: { fontSize: 16 },
});
```

## Expo Packages Used

| Package | Import | Usage |
|---------|--------|-------|
| `expo-image` | `import { Image } from 'expo-image'` | Optimized images |
| `expo-file-system` | `import * as FileSystem from 'expo-file-system'` | File operations |
| `expo-haptics` | `import * as Haptics from 'expo-haptics'` | Touch feedback |
| `expo-blur` | `import { BlurView } from 'expo-blur'` | Blur effects |
| `expo-linear-gradient` | `import { LinearGradient } from 'expo-linear-gradient'` | Gradients |

## Image Component

```typescript
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  style={{ width: 120, height: 180 }}
  contentFit="cover"
  cachePolicy="memory-disk"
  placeholder={blurhash}
  transition={200}
/>
```

## File System

```typescript
import * as FileSystem from 'expo-file-system';

// Directories
FileSystem.documentDirectory  // Persistent storage
FileSystem.cacheDirectory     // Temporary cache

// Operations
await FileSystem.writeAsStringAsync(path, content);
await FileSystem.readAsStringAsync(path);
await FileSystem.deleteAsync(path, { idempotent: true });
await FileSystem.getInfoAsync(path);
await FileSystem.makeDirectoryAsync(dir, { intermediates: true });
```

## AsyncStorage

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Save
await AsyncStorage.setItem('@key', JSON.stringify(data));

// Load
const json = await AsyncStorage.getItem('@key');
const data = json ? JSON.parse(json) : defaultValue;

// Remove
await AsyncStorage.removeItem('@key');
```

## Hooks Pattern

```typescript
// Custom hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
```

## FlatList Optimization

```typescript
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ItemComponent item={item} />}
  numColumns={3}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  removeClippedSubviews
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```
