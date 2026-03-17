---
name: mobile-engineer
description: Expert in mobile app architecture using Expo, React Native, TypeScript, and Zustand. Use when building mobile screens, implementing navigation, managing state, styling components, integrating with backend APIs, or handling platform-specific functionality.
---

# Mobile Engineer

Expert knowledge of mobile patterns and architecture for Expo React Native apps.

## Core Architecture

### Technology Stack

- **Framework**: Expo SDK 54 with React Native
- **Routing**: Expo Router (file-based routing)
- **State Management**: Zustand with AsyncStorage persistence
- **Styling**: React Native StyleSheet
- **Icons**: lucide-react-native
- **Storage**: @react-native-async-storage/async-storage

### Data Flow Architecture

```
Screen (React Native)
    |
State Decision:
├── Server Data -> Zustand Store -> API Service -> fetch
|                      |
|                 AsyncStorage (offline cache)
|
└── UI State -> Local useState
```

**Key Flow:**

1. Screen component calls Zustand store
2. Store fetches from API service
3. Data cached in AsyncStorage for offline use
4. Optimistic updates with rollback on error

## Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern              | Reference Path                    | Notes                      |
| -------------------- | --------------------------------- | -------------------------- |
| **Screen Layout**    | `app/(tabs)/index.tsx`            | Main screen with list      |
| **Navigation Setup** | `app/_layout.tsx`                 | Stack/tab navigator config |
| **Zustand Store**    | `store/*.ts`                      | State with offline caching |
| **API Service**      | `services/*.ts`                   | Type-safe API calls        |
| **Components**       | `components/`                     | Reusable UI components     |
| **Theme**            | `theme/colors.ts`                 | Color palette + tokens     |
| **Types**            | `types/`                          | Domain types               |

## Project Structure

```
app/                    # Expo Router screens (file-based routing)
├── _layout.tsx        # Root layout with navigation config
├── (tabs)/            # Tab navigation group
├── modal/             # Modal screens
└── [id].tsx           # Dynamic routes

components/            # Reusable UI components
store/                 # Zustand state management
services/              # API services
theme/                 # Design system (colors, spacing, radii)
types/                 # TypeScript types
assets/               # Images, icons, fonts
```

## State Management with Zustand

### Store Pattern with Offline Support

```typescript
import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AppState {
  items: Item[];
  isLoading: boolean;
  error: string | null;
  fetchItems: () => Promise<void>;
  addItem: (input: CreateItemInput) => Promise<void>;
}

const STORAGE_KEY = '@app/data';

export const useAppStore = create<AppState>((set, get) => ({
  items: [],
  isLoading: false,
  error: null,

  fetchItems: async () => {
    set({ isLoading: true, error: null });
    try {
      const items = await api.getItems();
      set({ items, isLoading: false });
      await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    } catch (error) {
      const cached = await AsyncStorage.getItem(STORAGE_KEY);
      if (cached) {
        set({ items: JSON.parse(cached), isLoading: false });
      } else {
        set({ error: 'Failed to fetch', isLoading: false });
      }
    }
  },

  // Optimistic update pattern
  addItem: async (input) => {
    const original = get().items;
    const optimistic = { ...input, id: 'temp-' + Date.now() };
    set((state) => ({ items: [...state.items, optimistic] }));
    try {
      const created = await api.createItem(input);
      set((state) => ({
        items: state.items.map((i) => (i.id === optimistic.id ? created : i)),
      }));
    } catch (error) {
      set({ items: original, error: 'Failed to add' });
    }
  },
}));
```

## Component Patterns

### Screen Component

```typescript
import { useEffect } from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import { Stack } from 'expo-router';
import { useAppStore } from '../store';
import { colors } from '../theme';

export default function HomeScreen() {
  const { items, isLoading, fetchItems } = useAppStore();

  useEffect(() => { fetchItems(); }, []);

  return (
    <SafeAreaView style={styles.container}>
      <Stack.Screen options={{ title: 'Home' }} />
      <ItemList items={items} isLoading={isLoading} onRefresh={fetchItems} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
});
```

### List Component with Pull-to-Refresh

```typescript
import { FlatList, RefreshControl } from 'react-native';
import { colors } from '../theme';

interface ItemListProps {
  items: Item[];
  isLoading: boolean;
  onRefresh: () => void;
}

export function ItemList({ items, isLoading, onRefresh }: ItemListProps) {
  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ListItem item={item} />}
      refreshControl={
        <RefreshControl
          refreshing={isLoading}
          onRefresh={onRefresh}
          tintColor={colors.primary}
        />
      }
    />
  );
}
```

### Pressable Component with Accessibility

```typescript
import { Pressable, Text, StyleSheet } from 'react-native';

export function ListItem({ item, onPress }: ListItemProps) {
  return (
    <Pressable
      style={({ pressed }) => [styles.container, pressed && styles.pressed]}
      onPress={() => onPress(item.id)}
      accessibilityRole="button"
      accessibilityLabel={item.title}
    >
      <Text style={styles.title}>{item.title}</Text>
    </Pressable>
  );
}
```

## Navigation with Expo Router

### File-Based Routing

```
app/
├── _layout.tsx      # Root layout (Stack navigator)
├── index.tsx        # Home screen (/)
├── [id].tsx         # Dynamic route (/123)
└── (tabs)/          # Tab group
    ├── _layout.tsx  # Tab navigator
    ├── index.tsx    # First tab
    └── settings.tsx # Settings tab
```

### Navigation Actions

```typescript
import { useRouter, useLocalSearchParams } from 'expo-router';

const router = useRouter();
const { id } = useLocalSearchParams<{ id: string }>();

router.push('/details');
router.push({ pathname: '/item/[id]', params: { id: '123' } });
router.back();
router.replace('/home');
```

## Platform-Specific Code

### Conditional Imports (CRITICAL)

Never use runtime `require()` for native modules — Metro still bundles them.
Use platform-specific files instead:

```
// BAD - Metro bundles both branches
if (Platform.OS !== 'web') {
  const { Something } = require('native-module');
}

// GOOD - Use platform files
Component.tsx         // Web fallback
Component.native.tsx  // Native with imports
```

### File Extensions

```
component.tsx          # Shared code
component.ios.tsx      # iOS only
component.android.tsx  # Android only
component.web.tsx      # Web only
component.native.tsx   # iOS + Android
```

## Common Commands

```bash
pnpm start              # Start Expo dev server
pnpm ios                # Run on iOS simulator
pnpm android            # Run on Android emulator
pnpm web                # Run in browser
```

## Component Checklist

- [ ] Use StyleSheet.create (not inline styles)
- [ ] Add accessibility props (role, label, state)
- [ ] Handle loading and error states
- [ ] Support pull-to-refresh for lists
- [ ] Use KeyboardAvoidingView for forms
- [ ] Test on both iOS and Android

## Performance Checklist

- [ ] Use FlatList for long lists (not ScrollView)
- [ ] Memoize expensive components with React.memo
- [ ] Use useCallback for event handlers passed as props
- [ ] Avoid inline styles in render
- [ ] Optimize images (proper sizing, caching)
