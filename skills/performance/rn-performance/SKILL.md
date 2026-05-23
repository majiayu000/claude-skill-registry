---
name: rn-performance
description: Performance optimization for React Native. Use when optimizing lists, preventing re-renders, memoizing components, or debugging performance issues in Expo/React Native apps.
---

# React Native Performance

## Problem Statement

React Native performance issues often stem from unnecessary re-renders, unoptimized lists, and expensive computations on the JS thread. This codebase has performance-critical areas (shot mastery, player lists) with established optimization patterns.

---

## Pattern: FlatList Optimization

### keyExtractor - Stable Keys

```typescript
// ✅ CORRECT: Stable function reference
const keyExtractor = useCallback((item: Session) => item.id, []);

<FlatList
  data={sessions}
  keyExtractor={keyExtractor}
  renderItem={renderItem}
/>

// ❌ WRONG: Creates new function every render
<FlatList
  data={sessions}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}
/>

// ❌ WRONG: Using index (causes issues with reordering/deletion)
keyExtractor={(item, index) => `${index}`}
```

### getItemLayout - Fixed Height Items

```typescript
const ITEM_HEIGHT = 80;
const SEPARATOR_HEIGHT = 1;

const getItemLayout = useCallback(
  (data: Session[] | null | undefined, index: number) => ({
    length: ITEM_HEIGHT,
    offset: (ITEM_HEIGHT + SEPARATOR_HEIGHT) * index,
    index,
  }),
  []
);

<FlatList
  data={sessions}
  getItemLayout={getItemLayout}
  // ... other props
/>
```

**Why it matters:** Without `getItemLayout`, FlatList must measure each item, causing scroll jank.

### renderItem - Memoized

```typescript
// Extract to named component
const SessionItem = memo(function SessionItem({ 
  session, 
  onPress 
}: { 
  session: Session; 
  onPress: (id: string) => void;
}) {
  return (
    <Pressable onPress={() => onPress(session.id)}>
      <Text>{session.title}</Text>
    </Pressable>
  );
});

// Stable callback
const handlePress = useCallback((id: string) => {
  navigation.push(`/session/${id}`);
}, [navigation]);

// Stable renderItem
const renderItem = useCallback(
  ({ item }: { item: Session }) => (
    <SessionItem session={item} onPress={handlePress} />
  ),
  [handlePress]
);

<FlatList
  data={sessions}
  renderItem={renderItem}
  // ...
/>
```

### Additional Optimizations

```typescript
<FlatList
  data={sessions}
  renderItem={renderItem}
  keyExtractor={keyExtractor}
  getItemLayout={getItemLayout}
  
  // Performance props
  removeClippedSubviews={true}           // Unmount off-screen items
  maxToRenderPerBatch={10}               // Items per render batch
  windowSize={5}                         // Render window (screens)
  initialNumToRender={10}                // Initial render count
  updateCellsBatchingPeriod={50}         // Batch update delay (ms)
  
  // Prevent extra renders
  extraData={selectedId}                 // Only re-render when this changes
/>
```

---

## Pattern: FlashList for Large Lists

**When to use:** 1000+ items, complex item components, or FlatList still janky.

```typescript
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={players}
  renderItem={renderItem}
  estimatedItemSize={80}  // Required - estimate item height
  keyExtractor={keyExtractor}
/>
```

**Note:** This codebase doesn't currently use FlashList. Consider for coach player lists.

---

## Pattern: Memoization

### useMemo - Expensive Computations

```typescript
// ✅ CORRECT: Memoize expensive calculation
const sortedAndFilteredItems = useMemo(() => {
  return items
    .filter(item => item.active)
    .sort((a, b) => b.score - a.score)
    .slice(0, 100);
}, [items]);

// ❌ WRONG: Recalculates every render
const sortedAndFilteredItems = items
  .filter(item => item.active)
  .sort((a, b) => b.score - a.score);

// ❌ WRONG: Memoizing simple access (overhead > benefit)
const userName = useMemo(() => user.name, [user.name]);
```

**When to use useMemo:**
- Array transformations (filter, sort, map chains)
- Object creation passed to memoized children
- Computations with O(n) or higher complexity

### useCallback - Stable Function References

```typescript
// ✅ CORRECT: Stable callback for child props
const handlePress = useCallback((id: string) => {
  setSelectedId(id);
}, []);

// Pass to memoized child
<MemoizedItem onPress={handlePress} />

// ❌ WRONG: useCallback with unstable deps
const handlePress = useCallback((id: string) => {
  doSomething(unstableObject); // unstableObject changes every render
}, [unstableObject]); // Defeats the purpose
```

**When to use useCallback:**
- Callbacks passed to memoized children
- Callbacks in dependency arrays
- Event handlers that would cause child re-renders

---

## Pattern: React.memo

```typescript
// Wrap components that receive stable props
const PlayerCard = memo(function PlayerCard({ 
  player, 
  onSelect 
}: Props) {
  return (
    <Pressable onPress={() => onSelect(player.id)}>
      <Text>{player.name}</Text>
      <Text>{player.rating}</Text>
    </Pressable>
  );
});

// Custom comparison for complex props
const PlayerCard = memo(
  function PlayerCard({ player, onSelect }: Props) {
    // ...
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return (
      prevProps.player.id === nextProps.player.id &&
      prevProps.player.rating === nextProps.player.rating
    );
  }
);
```

**When to use React.memo:**
- List item components
- Components receiving stable primitive props
- Components that render frequently but rarely change

**When NOT to use:**
- Components that always receive new props
- Simple components (overhead > benefit)
- Root-level screens

---

## Pattern: Zustand Selector Optimization

**Problem:** Selecting entire store causes re-render on any state change.

```typescript
// ❌ WRONG: Re-renders on ANY store change
const store = useAssessmentStore();
// or
const { userAnswers, isLoading, retakeAreas, ... } = useAssessmentStore();

// ✅ CORRECT: Only re-renders when selected values change
const userAnswers = useAssessmentStore((s) => s.userAnswers);
const isLoading = useAssessmentStore((s) => s.isLoading);

// ✅ CORRECT: Multiple values with shallow comparison
import { useShallow } from 'zustand/react/shallow';

const { userAnswers, isLoading } = useAssessmentStore(
  useShallow((s) => ({ 
    userAnswers: s.userAnswers, 
    isLoading: s.isLoading 
  }))
);
```

**See also:** `rn-zustand-patterns/SKILL.md` for more Zustand patterns.

---

## Pattern: Image Optimization

```typescript
import { Image } from 'expo-image';

// expo-image provides caching and performance optimizations
<Image
  source={{ uri: player.avatarUrl }}
  style={{ width: 50, height: 50 }}
  contentFit="cover"
  placeholder={blurhash}           // Show while loading
  transition={200}                  // Fade in duration
  cachePolicy="memory-disk"         // Cache strategy
/>

// For lists, add priority
<Image
  source={{ uri: player.avatarUrl }}
  priority={isVisible ? 'high' : 'low'}
/>
```

---

## Pattern: Avoiding Re-Renders

### Object/Array Stability

```typescript
// ❌ WRONG: New object every render
<ChildComponent style={{ padding: 10 }} />
<ChildComponent config={{ enabled: true }} />

// ✅ CORRECT: Stable reference
const style = useMemo(() => ({ padding: 10 }), []);
const config = useMemo(() => ({ enabled: true }), []);

<ChildComponent style={style} />
<ChildComponent config={config} />

// ✅ CORRECT: Or use StyleSheet
const styles = StyleSheet.create({
  container: { padding: 10 },
});

<ChildComponent style={styles.container} />
```

### Children Stability

```typescript
// ❌ WRONG: Inline function creates new element each render
<Parent>
  {() => <Child />}
</Parent>

// ✅ CORRECT: Stable element
const child = useMemo(() => <Child />, [deps]);
<Parent>{child}</Parent>
```

---

## Pattern: Detecting Re-Renders

### React DevTools Profiler

1. Open React DevTools
2. Go to Profiler tab
3. Click record, interact, stop
4. Review "Flamegraph" for render times
5. Look for components rendering unnecessarily

### why-did-you-render

```typescript
// Setup in development
import React from 'react';

if (__DEV__) {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}

// Mark specific component for tracking
PlayerCard.whyDidYouRender = true;
```

### Console Logging

```typescript
// Quick check for re-renders
function PlayerCard({ player }: Props) {
  console.log('PlayerCard render:', player.id);
  // ...
}
```

---

## Pattern: Heavy Computation Off Main Thread

**Problem:** JS thread blocked causes UI jank.

```typescript
// ❌ WRONG: Blocks JS thread
const result = heavyComputation(data); // Takes 500ms

// ✅ CORRECT: Use InteractionManager
import { InteractionManager } from 'react-native';

InteractionManager.runAfterInteractions(() => {
  const result = heavyComputation(data);
  setResult(result);
});

// ✅ CORRECT: requestAnimationFrame for visual updates
requestAnimationFrame(() => {
  // Update after current frame
});
```

---

## Performance Checklist

Before shipping list-heavy screens:

- [ ] FlatList has `keyExtractor` (stable callback)
- [ ] FlatList has `getItemLayout` (if fixed height)
- [ ] List items are memoized with `React.memo`
- [ ] Callbacks passed to items use `useCallback`
- [ ] Zustand selectors are specific (not whole store)
- [ ] Images use `expo-image` with caching
- [ ] No inline object/function props to memoized children
- [ ] Profiler shows no unnecessary re-renders

---

## Common Issues

| Issue | Solution |
|-------|----------|
| List scroll jank | Add `getItemLayout`, memoize items |
| Component re-renders too often | Check selector specificity, memoize props |
| Slow initial render | Reduce `initialNumToRender`, defer computation |
| Memory growing | Check for state accumulation, image cache |
| UI freezes on interaction | Move computation off main thread |

---

## Relationship to Other Skills

- **rn-zustand-patterns**: Selector optimization patterns
- **rn-styling**: StyleSheet.create for stable style references
