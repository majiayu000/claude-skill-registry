---
name: react-native
description: Cross-platform mobile development with React Native and Expo. Use when building iOS/Android apps with JavaScript/TypeScript, implementing native features, or optimizing mobile performance.
---

# React Native Development

Build native iOS and Android apps with React Native and Expo.

## Framework Options

| Framework                | Use When                                        |
| ------------------------ | ----------------------------------------------- |
| **Expo** (Recommended)   | Most apps, faster development, managed workflow |
| **React Native CLI**     | Need custom native modules, brownfield apps     |
| **Expo with Dev Client** | Best of both - Expo DX with native modules      |

---

## Project Setup

### Expo (Recommended)

```bash
npx create-expo-app@latest my-app
cd my-app
npx expo start
```

### React Native CLI

```bash
npx @react-native-community/cli init MyApp
cd MyApp
npx react-native run-ios  # or run-android
```

---

## Core Components

### Basic Structure

```tsx
import { View, Text, StyleSheet, ScrollView, SafeAreaView } from "react-native";

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Hello World</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  content: {
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
  },
});
```

### Common Components

```tsx
import {
  View,
  Text,
  Image,
  TextInput,
  TouchableOpacity,
  Pressable,
  FlatList,
  ActivityIndicator,
  Modal,
  Switch,
} from 'react-native';

// Touchable with feedback
<Pressable
  onPress={handlePress}
  style={({ pressed }) => [
    styles.button,
    pressed && styles.buttonPressed,
  ]}
>
  <Text>Press Me</Text>
</Pressable>

// Text Input
<TextInput
  value={text}
  onChangeText={setText}
  placeholder="Enter text"
  style={styles.input}
  autoCapitalize="none"
  keyboardType="email-address"
  returnKeyType="done"
  onSubmitEditing={handleSubmit}
/>

// Image
<Image
  source={{ uri: 'https://example.com/image.jpg' }}
  style={{ width: 100, height: 100 }}
  resizeMode="cover"
/>
```

---

## Navigation

### React Navigation Setup

```bash
npm install @react-navigation/native @react-navigation/native-stack
npx expo install react-native-screens react-native-safe-area-context
```

### Stack Navigation

```tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

type RootStackParamList = {
  Home: undefined;
  Details: { itemId: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: "My App" }}
        />
        <Stack.Screen
          name="Details"
          component={DetailsScreen}
          options={({ route }) => ({ title: route.params.itemId })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigate
navigation.navigate("Details", { itemId: "123" });

// Go back
navigation.goBack();
```

### Tab Navigation

```tsx
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Ionicons } from "@expo/vector-icons";

const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const iconName =
            route.name === "Home"
              ? focused
                ? "home"
                : "home-outline"
              : focused
                ? "settings"
                : "settings-outline";
          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}
```

---

## State Management

### Zustand (Recommended)

```tsx
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import AsyncStorage from "@react-native-async-storage/async-storage";

interface AuthStore {
  user: User | null;
  token: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: "auth-storage",
      storage: createJSONStorage(() => AsyncStorage),
    },
  ),
);
```

### React Query

```tsx
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";

const queryClient = new QueryClient();

// Wrap app
<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>;

// Use in component
function ItemList() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["items"],
    queryFn: fetchItems,
  });

  if (isLoading) return <ActivityIndicator />;
  if (error) return <Text>Error: {error.message}</Text>;

  return (
    <FlatList
      data={data}
      renderItem={({ item }) => <ItemRow item={item} />}
      keyExtractor={(item) => item.id}
      onRefresh={refetch}
      refreshing={isLoading}
    />
  );
}
```

---

## Styling

### StyleSheet

```tsx
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#ffffff",
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: 16,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#ccc",
  },
  text: {
    fontSize: 16,
    color: "#333",
  },
  shadow: {
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3, // Android
  },
});
```

### NativeWind (Tailwind for RN)

```bash
npm install nativewind tailwindcss
```

```tsx
import { Text, View } from "react-native";

export function Card() {
  return (
    <View className="bg-white rounded-lg p-4 shadow-md">
      <Text className="text-lg font-bold text-gray-900">Card Title</Text>
      <Text className="text-gray-600 mt-2">Card content goes here</Text>
    </View>
  );
}
```

---

## Native Features

### Camera (Expo)

```tsx
import { Camera, CameraType } from "expo-camera";

function CameraScreen() {
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const cameraRef = useRef<Camera>(null);

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync();
      console.log(photo.uri);
    }
  };

  if (!permission?.granted) {
    return <Button title="Grant Permission" onPress={requestPermission} />;
  }

  return (
    <Camera ref={cameraRef} style={styles.camera} type={CameraType.back}>
      <TouchableOpacity onPress={takePicture}>
        <Text>Take Photo</Text>
      </TouchableOpacity>
    </Camera>
  );
}
```

### Push Notifications (Expo)

```tsx
import * as Notifications from "expo-notifications";
import { useEffect } from "react";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== "granted") return;

  const token = await Notifications.getExpoPushTokenAsync();
  return token.data;
}

// Listen for notifications
useEffect(() => {
  const subscription = Notifications.addNotificationReceivedListener(
    (notification) => {
      console.log(notification);
    },
  );
  return () => subscription.remove();
}, []);
```

### Location

```tsx
import * as Location from "expo-location";

async function getLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== "granted") return;

  const location = await Location.getCurrentPositionAsync({});
  return {
    latitude: location.coords.latitude,
    longitude: location.coords.longitude,
  };
}
```

---

## Performance

### FlatList Optimization

```tsx
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  // Performance optimizations
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>;

// Memoize render item
const renderItem = useCallback(
  ({ item }: { item: Item }) => <MemoizedItem item={item} />,
  [],
);

const MemoizedItem = memo(({ item }: { item: Item }) => (
  <View>
    <Text>{item.name}</Text>
  </View>
));
```

### Image Optimization

```tsx
import { Image } from "expo-image";

<Image
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  placeholder={blurhash}
  transition={200}
  cachePolicy="memory-disk"
/>;
```

---

## Testing

### Jest + React Native Testing Library

```tsx
import { render, fireEvent, waitFor } from "@testing-library/react-native";
import { LoginScreen } from "./LoginScreen";

describe("LoginScreen", () => {
  it("should login successfully", async () => {
    const onLogin = jest.fn();
    const { getByPlaceholderText, getByText } = render(
      <LoginScreen onLogin={onLogin} />,
    );

    fireEvent.changeText(getByPlaceholderText("Email"), "test@example.com");
    fireEvent.changeText(getByPlaceholderText("Password"), "password123");
    fireEvent.press(getByText("Login"));

    await waitFor(() => {
      expect(onLogin).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "password123",
      });
    });
  });
});
```

---

## App Store Deployment

### Expo EAS Build

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

### app.json Configuration

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "ios": {
      "bundleIdentifier": "com.mycompany.myapp",
      "buildNumber": "1"
    },
    "android": {
      "package": "com.mycompany.myapp",
      "versionCode": 1
    }
  }
}
```

---

## Best Practices

### DO:

- Use Expo for faster development
- Implement proper TypeScript types
- Use FlashList for large lists
- Handle keyboard properly
- Test on real devices

### DON'T:

- Inline styles in render
- Skip memoization for lists
- Ignore platform differences
- Block JS thread with heavy computation
- Forget to handle deep linking

---

## New Architecture (React Native 0.76+)

React Native's New Architecture replaces the legacy bridge with a more performant, synchronous layer.

### Core Components

| Component          | Replaces     | Benefit                                        |
| ------------------ | ------------ | ---------------------------------------------- |
| **Fabric**         | Paper        | Synchronous rendering, concurrent features     |
| **TurboModules**   | Native Modules | Lazy loading, synchronous access, type safety |
| **JSI**            | Bridge       | Direct JS-to-native communication, no JSON     |
| **Bridgeless Mode** | Bridge      | Removes bridge entirely, lower memory usage    |

### Enabling New Architecture

```json
// app.json (Expo)
{
  "expo": {
    "newArchEnabled": true
  }
}
```

```ruby
# ios/Podfile (bare React Native)
ENV['RCT_NEW_ARCH_ENABLED'] = '1'
```

### TurboModules (Type-Safe Native Modules)

```typescript
// NativeCalculator.ts
import type { TurboModule } from "react-native";
import { TurboModuleRegistry } from "react-native";

export interface Spec extends TurboModule {
  add(a: number, b: number): number; // Synchronous!
  fetchData(url: string): Promise<string>; // Async
}

export default TurboModuleRegistry.getEnforcing<Spec>("NativeCalculator");
```

### Fabric Components (New Renderer)

Fabric enables concurrent rendering features from React 18/19, including Suspense for data fetching, transitions, and automatic batching.

---

## Expo Router (File-Based Routing)

```bash
npx create-expo-app@latest --template tabs
```

### File Structure

```
app/
├── _layout.tsx          # Root layout
├── index.tsx            # Home screen (/)
├── (tabs)/              # Tab group
│   ├── _layout.tsx      # Tab navigator
│   ├── index.tsx        # First tab
│   └── settings.tsx     # Settings tab
├── [id].tsx             # Dynamic route (/123)
├── modal.tsx            # Modal screen
└── +not-found.tsx       # 404 screen
```

### Layout and Navigation

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: "modal" }} />
    </Stack>
  );
}

// Navigate with type-safe links
import { Link, router } from "expo-router";

<Link href="/settings">Settings</Link>
<Link href={{ pathname: "/[id]", params: { id: "123" } }}>Details</Link>

// Programmatic navigation
router.push("/settings");
router.replace("/login");
router.back();
```

---

## React 19 Compatibility

React Native supports React 19 features when using New Architecture:

- **use() hook** for reading promises and context
- **ref as prop** (no forwardRef needed)
- **React Compiler** support for auto-memoization
- **useActionState** and **useOptimistic** for form handling

---

## EAS Update (OTA Updates)

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure updates
eas update:configure

# Push an OTA update (no app store review)
eas update --branch production --message "Bug fix for login"
eas update --branch preview --message "New feature preview"
```

```typescript
// Check for updates in app
import * as Updates from "expo-updates";

async function checkForUpdates() {
  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync(); // Apply update
  }
}
```

---

## Hermes Engine

Hermes is the default JS engine for React Native, optimized for mobile:

- **Faster startup** via bytecode precompilation
- **Lower memory** usage than JavaScriptCore
- **Better debugging** with Chrome DevTools Protocol

```json
// app.json - Hermes is enabled by default in Expo SDK 52+
{
  "expo": {
    "jsEngine": "hermes"
  }
}
```

---

## Expo SDK 52+ Features

| Feature                   | Description                                    |
| ------------------------- | ---------------------------------------------- |
| **Expo Router v4**        | File-based routing with API routes              |
| **expo-camera (next)**    | Camera API with barcode scanning               |
| **expo-video**            | Modern video player replacing expo-av           |
| **expo-sqlite**           | SQLite with synchronous API via JSI             |
| **DOM Components**        | Render web components inside React Native       |
| **React 19 support**      | Full React 19 features with New Architecture   |
| **Universal links**       | Deep linking configured via app.json            |
