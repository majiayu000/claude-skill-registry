---
name: mobile-development
description: Build native and cross-platform mobile apps with React Native and Expo. USE THIS when user mentions mobile apps, iOS/Android development, React Native components, native modules, app navigation, mobile UI, responsive mobile layouts, touch interactions, or cross-platform development. Include for Expo projects, Expo Router, native configuration, or device API integration.
---

# Mobile Development Skill

Build high-quality, cross-platform mobile applications with React Native and Expo.

## Your Mobile Stack

### Framework & Platform
- **Primary**: React Native with Expo
- **Language**: TypeScript/JavaScript
- **Navigation**: Expo Router (file-based routing)
- **State Management**: Zustand or Redux
- **Styling**: NativeWind (Tailwind for React Native) or StyleSheet

### Project Structure
```
app/
├── _layout.tsx          # Root layout
├── (tabs)/              # Tab navigation group
│   ├── _layout.tsx      # Tab layout
│   ├── index.tsx        # Home screen
│   ├── learn.tsx        # Learn screen
│   └── documents.tsx    # Documents screen
├── details/
│   └── [id].tsx         # Dynamic routes
└── modals/              # Modal screens

components/
├── ui/                  # Reusable UI components
├── screens/             # Screen-specific components
└── shared/              # Shared utilities

hooks/
├── use-theme.ts
├── use-navigation.ts
└── custom-hooks.ts

constants/
├── theme.ts
├── api.ts
└── translations.ts
```

## Core Concepts

### Navigation with Expo Router
```typescript
// File-based routing - no route config needed
// Structure determines routing automatically
app/
  index.tsx           // (app)
  details/
    [id].tsx          // (app)/details/:id
  (tabs)/
    _layout.tsx       // (app)/(tabs) with tab UI
    home.tsx          // (app)/(tabs)/home
```

### Native Components
- Use `react-native` components: `View`, `Text`, `ScrollView`, `FlatList`, `TouchableOpacity`
- Avoid web-only APIs (no DOM elements)
- Handle keyboard, safe area, orientation changes
- Platform-specific code with `.ios.ts` and `.android.ts` files

### Styling Strategy
```typescript
// Option 1: NativeWind (Tailwind-like)
<View className="flex-1 bg-white p-4 dark:bg-black">
  <Text className="text-lg font-bold text-gray-900 dark:text-white">
    Title
  </Text>
</View>

// Option 2: StyleSheet (traditional)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 16
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold'
  }
})
```

### State Management
```typescript
// Zustand example for mobile
import create from 'zustand'

const useStore = create(set => ({
  count: 0,
  increment: () => set(state => ({ count: state.count + 1 }))
}))

// In component
export function Counter() {
  const { count, increment } = useStore()
  return (
    <Pressable onPress={increment}>
      <Text>{count}</Text>
    </Pressable>
  )
}
```

### FlatList for Lists (Optimized)
```typescript
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ListItem item={item} />}
  numColumns={2}
  onEndReached={loadMore}
  onEndReachedThreshold={0.7}
  scrollEventThrottle={16}
/>
```

## Mobile-First Design

### Responsive Design
- Avoid fixed dimensions (use flex)
- Use `useWindowDimensions()` for adaptive layouts
- Test on multiple device sizes
- Handle notches and safe areas with `useSafeAreaInsets()`

### Touch Interactions
```typescript
<Pressable
  onPress={() => navigate('details')}
  onLongPress={handleLongPress}
  android_ripple={{ color: 'rgba(0,0,0,0.2)' }}
  style={({ pressed }) => ({
    opacity: pressed ? 0.6 : 1
  })}
>
  <Text>Press me</Text>
</Pressable>
```

### Performance Optimization
- Memoize expensive components: `React.memo()`
- Use `useCallback` for handlers passed to children
- Lazy load screens with `React.lazy()` + code splitting
- Optimize images with appropriate dimensions
- Virtualize long lists with FlatList

## Native API Integration

### Device APIs (via Expo)
- Camera & photo library
- Location services
- Push notifications
- FileSystem
- Audio/Video
- Biometrics

### Example: Camera Access
```typescript
import * as ImagePicker from 'expo-image-picker'

async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [4, 3],
    quality: 1,
  })
  
  if (!result.cancelled) {
    handleImage(result.assets[0].uri)
  }
}
```

## Testing Mobile Apps

- Unit tests with Jest
- Component tests with React Native Testing Library
- E2E tests with Detox
- Manual testing on real devices

## Deployment

### iOS (App Store)
- Build with EAS: `eas build --platform ios`
- Sign with certificates
- Create App Store listing

### Android (Google Play)
- Build with EAS: `eas build --platform android`
- Generate signed APK
- Create Play Store listing

### Expo Publishing
- Use `eas submit` for app stores
- Test builds with internal distribution first

## Common Patterns

### Authentication Flow
```typescript
const [user, setUser] = useState(null)

useEffect(() => {
  checkAuthStatus().then(authUser => {
    setUser(authUser)
    if (!authUser) {
      navigate('login')
    }
  })
}, [])
```

### Tab Navigation with Screens
```typescript
export function TabsBrowser() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          headerShown: false,
          tabBarIcon: HomeIcon
        }}
      />
      <Tabs.Screen
        name="documents"
        options={{
          title: 'Documents',
          tabBarIcon: FileIcon
        }}
      />
    </Tabs>
  )
}
```

## Accessibility

- Use `accessible` prop on interactive elements
- Set `accessibilityLabel` for clarity
- Test with screen readers
- Ensure sufficient text contrast
- Support keyboard navigation on Android

---

**Output**: Production-ready mobile applications with smooth navigation, optimized performance, and native-like user experience.
