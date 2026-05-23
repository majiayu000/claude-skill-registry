---
name: react-native-web-performance
description: Use when optimizing React Native Web performance. Provides patterns for code splitting, bundle optimization, memoization, and web-specific performance improvements.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Native Web - Performance

Performance optimization patterns for React Native Web, focusing on bundle size, rendering performance, and web-specific optimizations.

## Key Concepts

### Code Splitting

Use dynamic imports for lazy loading:

```typescript
import React, { lazy, Suspense } from 'react';
import { View, ActivityIndicator } from 'react-native';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<ActivityIndicator />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Memoization

Prevent unnecessary re-renders with React.memo and hooks:

```typescript
import React, { memo, useMemo, useCallback } from 'react';

interface Props {
  items: Item[];
  onItemPress: (id: string) => void;
}

export const ItemList = memo(function ItemList({ items, onItemPress }: Props) {
  const sortedItems = useMemo(
    () => items.sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  );

  const handlePress = useCallback(
    (id: string) => {
      onItemPress(id);
    },
    [onItemPress]
  );

  return (
    <View>
      {sortedItems.map(item => (
        <Item key={item.id} item={item} onPress={handlePress} />
      ))}
    </View>
  );
});
```

### FlatList for Large Lists

Use FlatList for efficient rendering of long lists:

```typescript
import { FlatList, View, Text } from 'react-native';

interface Item {
  id: string;
  title: string;
}

function ItemsList({ items }: { items: Item[] }) {
  return (
    <FlatList
      data={items}
      keyExtractor={item => item.id}
      renderItem={({ item }) => (
        <View>
          <Text>{item.title}</Text>
        </View>
      )}
      initialNumToRender={10}
      maxToRenderPerBatch={10}
      windowSize={5}
      removeClippedSubviews
    />
  );
}
```

## Best Practices

### Optimize Images

✅ Use optimized image formats and lazy loading:

```typescript
import { Image } from 'react-native';

function OptimizedImage({ uri }: { uri: string }) {
  return (
    <Image
      source={{ uri }}
      style={{ width: 200, height: 200 }}
      resizeMode="cover"
      // Web-specific: lazy loading
      {...(Platform.OS === 'web' && {
        loading: 'lazy',
      })}
    />
  );
}
```

### Avoid Inline Functions

✅ Use useCallback for event handlers:

```typescript
import { useCallback } from 'react';

function Component({ onSave }: { onSave: (data: Data) => void }) {
  const [data, setData] = useState<Data>();

  const handleSave = useCallback(() => {
    if (data) {
      onSave(data);
    }
  }, [data, onSave]);

  return <Button onPress={handleSave} title="Save" />;
}
```

### Optimize StyleSheet

✅ Create StyleSheet outside component:

```typescript
import { StyleSheet } from 'react-native';

// Good - created once
const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
});

function Component() {
  return <View style={styles.container} />;
}

// Bad - recreated on every render
function BadComponent() {
  const styles = StyleSheet.create({
    container: { flex: 1 },
  });
  return <View style={styles.container} />;
}
```

## Examples

### Virtualized List with Optimization

```typescript
import React, { useCallback, memo } from 'react';
import { FlatList, View, Text, StyleSheet } from 'react-native';

interface Item {
  id: string;
  title: string;
  description: string;
}

interface ItemCardProps {
  item: Item;
  onPress: (id: string) => void;
}

const ItemCard = memo(function ItemCard({ item, onPress }: ItemCardProps) {
  const handlePress = useCallback(() => {
    onPress(item.id);
  }, [item.id, onPress]);

  return (
    <Pressable onPress={handlePress}>
      <View style={styles.card}>
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.description}>{item.description}</Text>
      </View>
    </Pressable>
  );
});

export function OptimizedList({ items, onItemPress }: {
  items: Item[];
  onItemPress: (id: string) => void;
}) {
  const renderItem = useCallback(
    ({ item }: { item: Item }) => (
      <ItemCard item={item} onPress={onItemPress} />
    ),
    [onItemPress]
  );

  const keyExtractor = useCallback((item: Item) => item.id, []);

  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      initialNumToRender={10}
      maxToRenderPerBatch={10}
      windowSize={5}
      removeClippedSubviews
      getItemLayout={(data, index) => ({
        length: 80,
        offset: 80 * index,
        index,
      })}
    />
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    backgroundColor: '#fff',
    marginBottom: 8,
    borderRadius: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  description: {
    fontSize: 14,
    color: '#666',
  },
});
```

### Dynamic Imports

```typescript
import React, { lazy, Suspense, useState } from 'react';
import { View, Button, ActivityIndicator } from 'react-native';

// Lazy load heavy components
const Chart = lazy(() => import('./Chart'));
const DataTable = lazy(() => import('./DataTable'));

export function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <View>
      <Button
        title="Show Chart"
        onPress={() => setShowChart(true)}
      />

      {showChart && (
        <Suspense fallback={<ActivityIndicator />}>
          <Chart />
        </Suspense>
      )}
    </View>
  );
}
```

### Optimized Context

```typescript
import React, { createContext, useContext, useMemo, ReactNode } from 'react';

interface User {
  id: string;
  name: string;
}

interface UserContextValue {
  user: User | null;
  isLoading: boolean;
}

const UserContext = createContext<UserContextValue | undefined>(undefined);

export function UserProvider({
  user,
  isLoading,
  children,
}: {
  user: User | null;
  isLoading: boolean;
  children: ReactNode;
}) {
  // Memoize context value to prevent unnecessary re-renders
  const value = useMemo(
    () => ({ user, isLoading }),
    [user, isLoading]
  );

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}
```

## Common Patterns

### Debounced Input

```typescript
import { useState, useEffect } from 'react';
import { TextInput } from 'react-native';

function SearchInput({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(query);
    }, 300);

    return () => clearTimeout(timer);
  }, [query, onSearch]);

  return (
    <TextInput
      value={query}
      onChangeText={setQuery}
      placeholder="Search..."
    />
  );
}
```

### Intersection Observer (Web)

```typescript
import { useEffect, useRef, useState } from 'react';
import { View, Platform } from 'react-native';

function LazyLoadComponent({ children }: { children: React.ReactNode }) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<View>(null);

  useEffect(() => {
    if (Platform.OS !== 'web') {
      setIsVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    const element = ref.current as any;
    if (element) {
      observer.observe(element);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <View ref={ref}>
      {isVisible ? children : <View style={{ height: 200 }} />}
    </View>
  );
}
```

### Bundle Size Optimization

```typescript
// webpack.config.js or metro.config.js
module.exports = {
  resolve: {
    alias: {
      // Use lightweight alternatives
      'react-native$': 'react-native-web',
      'lodash': 'lodash-es',
    },
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
        },
      },
    },
  },
};
```

## Anti-Patterns

❌ Don't create StyleSheet inside render:

```typescript
// Bad
function Component() {
  const styles = StyleSheet.create({ container: { flex: 1 } });
  return <View style={styles.container} />;
}

// Good
const styles = StyleSheet.create({ container: { flex: 1 } });
function Component() {
  return <View style={styles.container} />;
}
```

❌ Don't use inline functions in FlatList:

```typescript
// Bad
<FlatList
  data={items}
  renderItem={({ item }) => <Item item={item} onPress={() => handlePress(item.id)} />}
/>

// Good
const renderItem = useCallback(({ item }) => (
  <Item item={item} onPress={handlePress} />
), [handlePress]);

<FlatList data={items} renderItem={renderItem} />
```

❌ Don't import entire libraries:

```typescript
// Bad
import _ from 'lodash';

// Good
import debounce from 'lodash/debounce';
```

❌ Don't render all items in long lists:

```typescript
// Bad
{items.map(item => <Item key={item.id} item={item} />)}

// Good
<FlatList
  data={items}
  renderItem={({ item }) => <Item item={item} />}
/>
```

## Related Skills

- **react-native-web-core**: Core React Native Web concepts
- **react-native-web-styling**: Optimized styling patterns
- **react-native-web-testing**: Performance testing strategies
