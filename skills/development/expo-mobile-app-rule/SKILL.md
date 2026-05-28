---
name: expo-mobile-app-rule
description: Specifies best practices and conventions for Expo-based mobile app development.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: mobile/**/*.tsx
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
---

# Expo Mobile App Rule Skill

<identity>
You are a coding standards expert specializing in expo mobile app rule.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these comprehensive mobile app development patterns with Expo.

## Navigation with Expo Router

### File-Based Routing

Expo Router uses the file system for navigation:

```
app/
  _layout.tsx          # Root layout
  index.tsx            # Home screen (/)
  (tabs)/              # Tab navigator group
    _layout.tsx        # Tab layout
    home.tsx           # /home
    profile.tsx        # /profile
  user/
    [id].tsx           # Dynamic route /user/:id
  modal.tsx            # Can be presented as modal
```

### Root Layout

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen
        name="modal"
        options={{
          presentation: 'modal',
          title: 'Settings',
        }}
      />
    </Stack>
  );
}
```

### Tab Navigation

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="home"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
```

### Navigation Methods

```typescript
import { useRouter, useLocalSearchParams, Link } from 'expo-router';

function MyComponent() {
  const router = useRouter();
  const params = useLocalSearchParams();

  return (
    <>
      {/* Declarative navigation */}
      <Link href="/profile">Go to Profile</Link>
      <Link href={{ pathname: '/user/[id]', params: { id: '123' } }}>
        View User
      </Link>

      {/* Imperative navigation */}
      <Button onPress={() => router.push('/profile')} title="Push" />
      <Button onPress={() => router.replace('/home')} title="Replace" />
      <Button onPress={() => router.back()} title="Go Back" />
    </>
  );
}
```

### Dynamic Routes

```typescript
// app/user/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function UserScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();

  return <Text>User ID: {id}</Text>;
}
```

### Protected Routes

```typescript
// app/_layout.tsx
import { useAuth } from '@/hooks/useAuth';
import { Redirect, Slot } from 'expo-router';

export default function AppLayout() {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingScreen />;
  }

  if (!user) {
    return <Redirect href="/login" />;
  }

  return <Slot />;
}
```

## State Management

### Context API for Global State

```typescript
// contexts/AppContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface AppState {
  user: User | null;
  theme: 'light' | 'dark';
  setUser: (user: User | null) => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

const AppContext = createContext<AppState | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  return (
    <AppContext.Provider value={{ user, theme, setUser, setTheme }}>
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
```

### Redux Toolkit (for Complex State)

```typescript
// store/slices/userSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  currentUser: User | null;
  loading: boolean;
}

const userSlice = createSlice({
  name: 'user',
  initialState: { currentUser: null, loading: false } as UserState,
  reducers: {
    setUser: (state, action: PayloadAction<User | null>) => {
      state.currentUser = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { setUser, setLoading } = userSlice.actions;
export default userSlice.reducer;
```

### Zustand (Lightweight Alternative)

```typescript
// store/useStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AppStore {
  user: User | null;
  theme: 'light' | 'dark';
  setUser: (user: User | null) => void;
  toggleTheme: () => void;
}

export const useStore = create<AppStore>()(
  persist(
    set => ({
      user: null,
      theme: 'light',
      setUser: user => set({ user }),
      toggleTheme: () =>
        set(state => ({
          theme: state.theme === 'light' ? 'dark' : 'light',
        })),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Offline Support

### AsyncStorage for Local Data

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Save data
await AsyncStorage.setItem('user', JSON.stringify(user));

// Load data
const userData = await AsyncStorage.getItem('user');
const user = userData ? JSON.parse(userData) : null;

// Remove data
await AsyncStorage.removeItem('user');

// Clear all
await AsyncStorage.clear();
```

### SQLite for Complex Offline Data

```typescript
import * as SQLite from 'expo-sqlite';

class DatabaseService {
  private db: SQLite.SQLiteDatabase | null = null;

  async init() {
    this.db = await SQLite.openDatabaseAsync('myapp.db');

    await this.db.execAsync(`
      CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        timestamp INTEGER,
        synced INTEGER DEFAULT 0
      );
    `);
  }

  async saveMessage(text: string) {
    await this.db?.runAsync(
      'INSERT INTO messages (text, timestamp) VALUES (?, ?)',
      text,
      Date.now()
    );
  }

  async getUnsynced() {
    return await this.db?.getAllAsync('SELECT * FROM messages WHERE synced = 0');
  }

  async markSynced(id: number) {
    await this.db?.runAsync('UPDATE messages SET synced = 1 WHERE id = ?', id);
  }
}
```

### Network State Detection

```typescript
import NetInfo from '@react-native-community/netinfo';
import { useEffect, useState } from 'react';

function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state) => {
      setIsOnline(state.isConnected ?? false);
    });

    return () => unsubscribe();
  }, []);

  return isOnline;
}

// Usage
function MyScreen() {
  const isOnline = useOnlineStatus();

  return (
    <View>
      {!isOnline && <Banner message="You are offline" />}
      {/* Rest of content */}
    </View>
  );
}
```

### Offline-First Data Sync

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useOfflineData() {
  const queryClient = useQueryClient();
  const isOnline = useOnlineStatus();

  const { data } = useQuery({
    queryKey: ['items'],
    queryFn: fetchItems,
    enabled: isOnline,
    // Use cached data when offline
    staleTime: Infinity,
  });

  const mutation = useMutation({
    mutationFn: createItem,
    onMutate: async newItem => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['items'] });
      const previous = queryClient.getQueryData(['items']);

      queryClient.setQueryData(['items'], (old: any) => [...old, newItem]);

      // Save to local storage if offline
      if (!isOnline) {
        await saveToQueue(newItem);
      }

      return { previous };
    },
    onError: (err, newItem, context) => {
      // Rollback on error
      queryClient.setQueryData(['items'], context?.previous);
    },
  });

  // Sync queue when online
  useEffect(() => {
    if (isOnline) {
      syncQueue();
    }
  }, [isOnline]);

  return { data, mutation };
}
```

## Push Notifications

### Setup with Expo Notifications

```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

// Configure notification handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

async function registerForPushNotifications() {
  if (!Device.isDevice) {
    alert('Push notifications only work on physical devices');
    return;
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();

  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    return;
  }

  const projectId = Constants.expoConfig?.extra?.eas?.projectId;

  const token = await Notifications.getExpoPushTokenAsync({ projectId });

  // Send token to your backend
  await sendTokenToBackend(token.data);

  // Android-specific channel setup
  if (Platform.OS === 'android') {
    Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C',
    });
  }

  return token.data;
}
```

### Handling Notifications

```typescript
import { useEffect, useRef } from 'react';

function useNotifications() {
  const notificationListener = useRef<Notifications.Subscription>();
  const responseListener = useRef<Notifications.Subscription>();

  useEffect(() => {
    // Foreground notification handler
    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      console.log('Notification received:', notification);
    });

    // User interaction handler
    responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
      const data = response.notification.request.content.data;

      // Navigate based on notification data
      if (data.screen) {
        router.push(data.screen as any);
      }
    });

    return () => {
      if (notificationListener.current) {
        Notifications.removeNotificationSubscription(notificationListener.current);
      }
      if (responseListener.current) {
        Notifications.removeNotificationSubscription(responseListener.current);
      }
    };
  }, []);
}
```

### Local Notifications

```typescript
async function scheduleNotification() {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Reminder',
      body: 'Time to check your tasks!',
      data: { screen: '/tasks' },
    },
    trigger: {
      seconds: 60,
      // Or use specific date
      // date: new Date(Date.now() + 60 * 60 * 1000),
      // Or repeating
      // repeats: true,
    },
  });
}

// Cancel notification
const identifier = await scheduleNotification();
await Notifications.cancelScheduledNotificationAsync(identifier);

// Cancel all
await Notifications.cancelAllScheduledNotificationsAsync();
```

## Deep Linking

### Configure Deep Links

```json
// app.json
{
  "expo": {
    "scheme": "myapp",
    "ios": {
      "associatedDomains": ["applinks:myapp.com"]
    },
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [
            {
              "scheme": "https",
              "host": "myapp.com"
            }
          ],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

### Handle Deep Links in Expo Router

```typescript
// Expo Router handles deep links automatically
// myapp://user/123 -> app/user/[id].tsx

// For custom handling:
import * as Linking from 'expo-linking';

function useDeepLinking() {
  useEffect(() => {
    // Get initial URL (app opened via link)
    Linking.getInitialURL().then(url => {
      if (url) {
        handleDeepLink(url);
      }
    });

    // Listen for URL changes (app already open)
    const subscription = Linking.addEventListener('url', ({ url }) => {
      handleDeepLink(url);
    });

    return () => subscription.remove();
  }, []);
}

function handleDeepLink(url: string) {
  const { path, queryParams } = Linking.parse(url);

  // Navigate based on path
  if (path === 'user') {
    router.push(`/user/${queryParams?.id}`);
  }
}
```

### Universal Links (iOS) & App Links (Android)

```json
// apple-app-site-association (serve at https://myapp.com/.well-known/)
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAMID.com.company.myapp",
        "paths": ["/user/*", "/post/*"]
      }
    ]
  }
}
```

```json
// assetlinks.json (serve at https://myapp.com/.well-known/)
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.company.myapp",
      "sha256_cert_fingerprints": ["FINGERPRINT"]
    }
  }
]
```

### Deep Link from Push Notifications

```typescript
// When sending push notification from backend
{
  "to": "ExponentPushToken[xxx]",
  "title": "New Message",
  "body": "You have a new message",
  "data": {
    "url": "myapp://chat/123"
  }
}

// Handle in app
responseListener.current =
  Notifications.addNotificationResponseReceivedListener((response) => {
    const url = response.notification.request.content.data.url;
    if (url) {
      Linking.openURL(url);
    }
  });
```

## Performance Optimization

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react';

const ListItem = memo(({ item, onPress }: Props) => (
  <TouchableOpacity onPress={() => onPress(item.id)}>
    <Text>{item.title}</Text>
  </TouchableOpacity>
));

function MyList({ items }: Props) {
  const sortedItems = useMemo(
    () => items.sort((a, b) => a.title.localeCompare(b.title)),
    [items]
  );

  const handlePress = useCallback((id: string) => {
    router.push(`/item/${id}`);
  }, []);

  return (
    <FlatList
      data={sortedItems}
      renderItem={({ item }) => (
        <ListItem item={item} onPress={handlePress} />
      )}
      keyExtractor={(item) => item.id}
    />
  );
}
```

### Optimized Lists

```typescript
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={100}
  // Much faster than FlatList for large lists
/>
```

### Image Optimization

```typescript
import { Image } from 'expo-image';

<Image
  source={{ uri: 'https://example.com/large-image.jpg' }}
  placeholder={require('./placeholder.png')}
  contentFit="cover"
  transition={200}
  cachePolicy="memory-disk"
  style={{ width: 300, height: 200 }}
/>
```

</instructions>

<examples>
Example usage:
```
User: "Review this code for expo mobile app rule compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
