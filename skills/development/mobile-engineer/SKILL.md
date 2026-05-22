---
name: mobile-engineer
description: Expert in Template Project mobile architecture using Expo, React Native, TypeScript, and Zustand. Use when building mobile screens, implementing navigation, managing state, styling components, integrating with backend APIs, or handling platform-specific functionality.
---

# Template Mobile Engineer

Expert knowledge of mobile patterns and architecture for the Template Project using Expo and React Native.

## Core Architecture

### Technology Stack

- **Framework**: Expo SDK 54 with React Native 0.81
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

## CRITICAL: Where to Look Before Making Changes

### Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern                  | Primary Reference                | Notes                          |
| ------------------------ | -------------------------------- | ------------------------------ |
| **Screen Layout**        | `app/index.tsx`                  | Main screen with list          |
| **Navigation Setup**     | `app/_layout.tsx`                | Stack navigator config         |
| **Zustand Store**        | `store/todoStore.ts`             | State with offline caching     |
| **API Service**          | `services/api.ts`                | Type-safe API calls            |
| **List Component**       | `components/TodoList.tsx`        | FlatList with pull-to-refresh  |
| **Item Component**       | `components/TodoItem.tsx`        | Pressable with gestures        |
| **Form Component**       | `components/AddTodoForm.tsx`     | Input with keyboard handling   |
| **Theme Colors**         | `theme/colors.ts`                | Color palette + shadows        |
| **Types**                | `types/todo.ts`                  | Domain types                   |

## Project Structure

```
packages/mobile/
├── app/                    # Expo Router screens (file-based routing)
│   ├── _layout.tsx        # Root layout with navigation config
│   └── index.tsx          # Home screen
├── components/            # Reusable UI components
│   ├── TodoItem.tsx      # Single todo item
│   ├── TodoList.tsx      # List with pull-to-refresh
│   └── AddTodoForm.tsx   # Form for new todos
├── store/                 # Zustand state management
│   └── todoStore.ts      # Todo state + API integration
├── services/              # API services
│   └── api.ts            # Backend API client
├── theme/                 # Design system
│   └── colors.ts         # Colors, shadows, elevation
├── types/                 # TypeScript types
│   └── todo.ts           # Domain types
└── assets/               # Images, icons, fonts
```

## State Management with Zustand

### Store Pattern with Offline Support

```typescript
import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { api } from '../services/api';

interface TodoState {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;

  fetchTodos: () => Promise<void>;
  addTodo: (input: CreateTodoInput) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}

const STORAGE_KEY = '@todos/data';

export const useTodoStore = create<TodoState>((set, get) => ({
  todos: [],
  isLoading: false,
  error: null,

  fetchTodos: async () => {
    set({ isLoading: true, error: null });

    try {
      const todos = await api.getTodos();
      set({ todos, isLoading: false });

      // Cache for offline use
      await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
    } catch (error) {
      // Load from cache on error
      const cached = await AsyncStorage.getItem(STORAGE_KEY);
      if (cached) {
        set({ todos: JSON.parse(cached), isLoading: false });
      } else {
        set({ error: 'Failed to fetch', isLoading: false });
      }
    }
  },

  // Optimistic update pattern
  toggleTodo: async (id: string) => {
    const originalTodos = get().todos;

    // Optimistic update
    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      ),
    }));

    try {
      await api.toggleTodo(id);
    } catch (error) {
      // Rollback on error
      set({ todos: originalTodos, error: 'Failed to toggle' });
    }
  },
}));
```

## Component Patterns

### Screen Component

```typescript
import React, { useEffect } from 'react';
import { View, SafeAreaView, StyleSheet } from 'react-native';
import { Stack } from 'expo-router';
import { useTodoStore } from '../store';
import { colors } from '../theme';

export default function HomeScreen() {
  const { todos, isLoading, fetchTodos, toggleTodo } = useTodoStore();

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <Stack.Screen options={{ title: 'My Todos' }} />
      <TodoList
        todos={todos}
        isLoading={isLoading}
        onRefresh={fetchTodos}
        onToggle={toggleTodo}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.DEFAULT,
  },
});
```

### List Component with Pull-to-Refresh

```typescript
import React from 'react';
import { FlatList, RefreshControl } from 'react-native';
import { TodoItem } from './TodoItem';
import { colors } from '../theme';

interface TodoListProps {
  todos: Todo[];
  isLoading: boolean;
  onRefresh: () => void;
  onToggle: (id: string) => void;
}

export function TodoList({ todos, isLoading, onRefresh, onToggle }: TodoListProps) {
  return (
    <FlatList
      data={todos}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <TodoItem todo={item} onToggle={onToggle} />
      )}
      refreshControl={
        <RefreshControl
          refreshing={isLoading}
          onRefresh={onRefresh}
          tintColor={colors.primary.DEFAULT}
        />
      }
    />
  );
}
```

### Pressable Component with Accessibility

```typescript
import React from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';
import { Check } from 'lucide-react-native';
import { colors, shadows } from '../theme';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
}

export function TodoItem({ todo, onToggle }: TodoItemProps) {
  return (
    <Pressable
      style={({ pressed }) => [
        styles.container,
        shadows.sm,
        pressed && styles.pressed,
      ]}
      onPress={() => onToggle(todo.id)}
      accessibilityRole="checkbox"
      accessibilityState={{ checked: todo.completed }}
      accessibilityLabel={todo.title}
    >
      <View style={[styles.checkbox, todo.completed && styles.checked]}>
        {todo.completed && <Check size={14} color="#fff" />}
      </View>
      <Text style={[styles.title, todo.completed && styles.completed]}>
        {todo.title}
      </Text>
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

### Stack Navigator Config

```typescript
import { Stack } from 'expo-router';
import { colors } from '../theme';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: colors.background.DEFAULT },
        headerTintColor: colors.text.primary,
        contentStyle: { backgroundColor: colors.background.DEFAULT },
      }}
    />
  );
}
```

### Navigation Actions

```typescript
import { useRouter, useLocalSearchParams } from 'expo-router';

function MyComponent() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();

  // Navigate
  router.push('/details');
  router.push({ pathname: '/todo/[id]', params: { id: '123' } });

  // Go back
  router.back();

  // Replace (no back)
  router.replace('/home');
}
```

## Styling Patterns

### StyleSheet Best Practices

```typescript
import { StyleSheet, Platform } from 'react-native';
import { colors, shadows, elevation } from '../theme';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.DEFAULT,
  },
  card: {
    backgroundColor: colors.background.card,
    borderRadius: 12,
    padding: 16,
    // Platform-specific shadows
    ...Platform.select({
      ios: shadows.md,
      android: { elevation: elevation.md },
    }),
  },
  text: {
    fontSize: 16,
    color: colors.text.primary,
    fontWeight: '500',
  },
});
```

### Responsive Design

```typescript
import { Dimensions, useWindowDimensions } from 'react-native';

function ResponsiveComponent() {
  const { width, height } = useWindowDimensions();
  const isTablet = width >= 768;

  return (
    <View style={[styles.container, isTablet && styles.tabletContainer]}>
      {/* Content */}
    </View>
  );
}
```

## API Integration

### Service Pattern

```typescript
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:3000';

interface ApiResponse<T> {
  success: boolean;
  data: T;
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  const json = await response.json();
  return (json as ApiResponse<T>).data;
}

export const api = {
  getTodos: () => request<Todo[]>('/api/todos'),
  createTodo: (data: CreateTodoInput) =>
    request<Todo>('/api/todos', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
```

## Platform-Specific Code

### Platform Select

```typescript
import { Platform } from 'react-native';

// Inline
const padding = Platform.OS === 'ios' ? 20 : 16;

// Object select
const styles = Platform.select({
  ios: { shadowOpacity: 0.2 },
  android: { elevation: 4 },
  default: {},
});
```

### File Extensions

```
component.tsx        # Shared code
component.ios.tsx    # iOS only
component.android.tsx # Android only
component.web.tsx    # Web only
```

## Common Commands

```bash
# Navigate to package first
cd packages/mobile

# Development
pnpm start              # Start Expo dev server
pnpm ios                # Run on iOS simulator
pnpm android            # Run on Android emulator
pnpm web                # Run in browser

# Type checking
pnpm type-check         # Run TypeScript checks

# Building
npx expo build:ios      # Build for iOS
npx expo build:android  # Build for Android
```

## Quick Reference

### Essential Hooks

```typescript
// Navigation
useRouter()                    // Navigation actions
useLocalSearchParams()         // Route params
usePathname()                  // Current path

// State
useTodoStore()                 // Zustand store

// React Native
useWindowDimensions()          // Screen size
useColorScheme()               // Light/dark mode
```

### Component Checklist

- [ ] Use StyleSheet.create (not inline styles)
- [ ] Add accessibility props (role, label, state)
- [ ] Handle loading states
- [ ] Handle error states
- [ ] Support pull-to-refresh for lists
- [ ] Use KeyboardAvoidingView for forms
- [ ] Test on both iOS and Android

### Performance Checklist

- [ ] Use FlatList for long lists (not ScrollView)
- [ ] Memoize expensive components with React.memo
- [ ] Use useCallback for event handlers
- [ ] Avoid inline styles in render
- [ ] Optimize images (proper sizing, caching)

---

## Critical Reminders

**Before Any Development:**

1. Check existing components in `components/`
2. Check types in `types/`
3. Use Zustand for shared state, useState for local UI state
4. Test on both iOS and Android
5. Add proper accessibility props

**Architecture Flow:**

```
Screen -> Zustand Store -> API Service -> Backend
              |
         AsyncStorage (offline cache)
```

**Remember**: Mobile apps need offline support, proper loading states, and platform-specific handling. Always test on real devices before release.
