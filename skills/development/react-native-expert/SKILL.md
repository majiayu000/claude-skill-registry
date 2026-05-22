---
name: react-native-expert
description: React Native core patterns, navigation, state management, and performance optimization.
---

# React Native Expert

## Project Structure

```
src/
├── components/       # Reusable UI components
├── screens/          # Screen components
├── navigation/       # Navigation config
├── hooks/            # Custom hooks
├── services/         # API, storage
├── store/            # State management
├── utils/            # Helpers
└── types/            # TypeScript types
```

## Navigation

```typescript
// navigation/RootNavigator.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## State Management

```typescript
// Zustand (recommended)
import { create } from 'zustand';

interface AuthStore {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

## Performance

### Memoization

```typescript
// Memoize expensive components
const MemoizedList = memo(({ items }) => (
  <FlatList
    data={items}
    renderItem={renderItem}
    keyExtractor={(item) => item.id}
  />
));

// Memoize callbacks
const handlePress = useCallback(() => {
  // ...
}, [dependency]);
```

### FlatList Optimization

```typescript
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  windowSize={5}
  maxToRenderPerBatch={10}
  removeClippedSubviews={true}
/>
```

## Platform-Specific Code

```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
    ...Platform.select({
      ios: { shadowColor: '#000' },
      android: { elevation: 4 },
    }),
  },
});
```
