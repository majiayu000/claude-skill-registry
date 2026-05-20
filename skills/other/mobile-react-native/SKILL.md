---
name: mobile-react-native
description: React Native patterns for cross-platform mobile apps. Use when building iOS/Android apps with React Native, Expo, navigation, device APIs, push notifications, or mobile-specific UI patterns.
---

# React Native / Expo Patterns

## Project Setup (Expo)
```bash
# Create new project
npx create-expo-app MyApp --template blank-typescript
cd MyApp

# Key dependencies
npx expo install expo-router react-native-safe-area-context react-native-screens
npx expo install expo-secure-store expo-notifications expo-camera
npm install @tanstack/react-query zustand react-hook-form
```

## Navigation (Expo Router — file-based)
```
app/
  _layout.tsx         # Root layout (providers, auth check)
  (tabs)/
    _layout.tsx       # Tab bar layout
    index.tsx         # Home tab
    profile.tsx       # Profile tab
  (auth)/
    login.tsx         # Login screen
    register.tsx      # Register screen
  product/
    [id].tsx          # Dynamic route: /product/123
```

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router'
import { useAuthStore } from '@/store/auth'

export default function RootLayout() {
  const isLoggedIn = useAuthStore(s => !!s.token)
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} redirect={!isLoggedIn} />
      <Stack.Screen name="(auth)" options={{ headerShown: false }} redirect={isLoggedIn} />
    </Stack>
  )
}

// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Home, User, Settings } from 'lucide-react-native'

export default function TabsLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#3b82f6' }}>
      <Tabs.Screen name="index" options={{ title: 'Home', tabBarIcon: ({ color }) => <Home color={color} size={24} /> }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile', tabBarIcon: ({ color }) => <User color={color} size={24} /> }} />
    </Tabs>
  )
}
```

## Screen Component
```typescript
// app/(tabs)/index.tsx
import { View, Text, FlatList, StyleSheet, RefreshControl } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
import { useQuery } from '@tanstack/react-query'
import { router } from 'expo-router'

export default function HomeScreen() {
  const { data, isLoading, refetch, isRefetching } = useQuery({
    queryKey: ['posts'],
    queryFn: () => api.getPosts(),
  })

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={data}
        keyExtractor={(item) => item.id}
        refreshControl={<RefreshControl refreshing={isRefetching} onRefresh={refetch} />}
        renderItem={({ item }) => (
          <PostCard
            post={item}
            onPress={() => router.push(`/post/${item.id}`)}
          />
        )}
        ListEmptyComponent={isLoading ? <LoadingSpinner /> : <EmptyState />}
      />
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
})
```

## Secure Storage (tokens)
```typescript
import * as SecureStore from 'expo-secure-store'

export const tokenStorage = {
  async get(key: string): Promise<string | null> {
    return SecureStore.getItemAsync(key)
  },
  async set(key: string, value: string): Promise<void> {
    await SecureStore.setItemAsync(key, value)
  },
  async delete(key: string): Promise<void> {
    await SecureStore.deleteItemAsync(key)
  },
}

// Zustand with secure storage
import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'

const secureStorage = createJSONStorage(() => ({
  getItem: (key) => tokenStorage.get(key),
  setItem: (key, value) => tokenStorage.set(key, value),
  removeItem: (key) => tokenStorage.delete(key),
}))

export const useAuthStore = create(persist(
  (set) => ({
    token: null as string | null,
    setToken: (token: string) => set({ token }),
    logout: () => set({ token: null }),
  }),
  { name: 'auth', storage: secureStorage }
))
```

## Push Notifications
```typescript
import * as Notifications from 'expo-notifications'
import * as Device from 'expo-device'

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
})

export async function registerForPushNotifications(): Promise<string | null> {
  if (!Device.isDevice) return null // Simulator doesn't support push

  const { status: existing } = await Notifications.getPermissionsAsync()
  let finalStatus = existing
  if (existing !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync()
    finalStatus = status
  }
  if (finalStatus !== 'granted') return null

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: Constants.expoConfig?.extra?.eas?.projectId,
  })
  return token.data
}

// Use in component
useEffect(() => {
  registerForPushNotifications().then(token => {
    if (token) api.savePushToken(token)
  })

  const sub = Notifications.addNotificationReceivedListener(notification => {
    console.log('Notification received:', notification)
  })
  return () => sub.remove()
}, [])
```

## Camera & Image Picker
```typescript
import * as ImagePicker from 'expo-image-picker'

export async function pickImage(): Promise<string | null> {
  const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync()
  if (status !== 'granted') {
    Alert.alert('Permission needed', 'Please allow access to your photo library')
    return null
  }

  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.8,
  })

  if (result.canceled) return null
  return result.assets[0].uri
}

// Upload to API
async function uploadAvatar(uri: string): Promise<string> {
  const formData = new FormData()
  formData.append('file', {
    uri,
    name: 'avatar.jpg',
    type: 'image/jpeg',
  } as any)

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  const { url } = await response.json()
  return url
}
```

## Styling Patterns
```typescript
import { StyleSheet, Platform } from 'react-native'

// Platform-specific styles
const styles = StyleSheet.create({
  shadow: {
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 4,
      },
    }),
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 8,
  },
})

// NativeWind (Tailwind for React Native)
// <View className="flex-1 bg-white p-4">
//   <Text className="text-lg font-bold text-gray-900">Hello</Text>
// </View>
```

## Rules
- Use Expo Router for navigation (file-based, better DX than React Navigation)
- Always store sensitive data in SecureStore — never AsyncStorage for tokens
- Use FlatList not ScrollView+map for long lists (virtualization)
- Test on real device early — simulators miss camera, notifications, biometrics
- Platform.select() for iOS/Android differences in shadows, fonts, keyboard
- Request permissions lazily (only when needed) — not at app startup
- Use SafeAreaView for all screens (notch/home indicator safe zones)
- Bundle size matters: use expo-image not <Image> for better performance
