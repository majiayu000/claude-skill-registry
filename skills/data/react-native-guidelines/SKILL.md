---
name: react-native-guidelines
description: React Native best practices optimized for AI agents. Contains 16 rules across 7 sections covering performance, architecture, and platform-specific patterns. Use when building React Native or Expo apps, optimizing mobile performance, implementing animations or gestures, or working with native modules.
metadata:
  author: vercel
  version: "1.0.0"
  license: MIT
---

# React Native Guidelines

Best practices for React Native and Expo development, focusing on performance, architecture, and platform-specific patterns.

## When to Use

- Building React Native or Expo apps
- Optimizing mobile performance
- Implementing animations or gestures
- Working with native modules or platform APIs

## Rules by Priority

### 1. Performance (CRITICAL)

**Use FlashList instead of FlatList:**
```tsx
// ❌ BAD - FlatList
import { FlatList } from 'react-native'

// ✅ GOOD - FlashList (10x faster)
import { FlashList } from '@shopify/flash-list'

<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
/>
```

**Avoid inline functions in render:**
```tsx
// ❌ BAD - new function each render
<TouchableOpacity onPress={() => setCount(c => c + 1)}>

// ✅ GOOD - stable function
const increment = useCallback(() => setCount(c => c + 1), [])
<TouchableOpacity onPress={increment}>
```

**Memoize expensive computations:**
```tsx
// ✅ GOOD - memoize
const sortedData = useMemo(() =>
  data.sort((a, b) => a.date - b.date),
  [data]
)
```

**Move heavy work off main thread:**
```tsx
// ✅ GOOD - use runOnJS for callbacks
useDerivedValue(() => {
  runOnJS(updateUI)(value.value)
}, [value])

// ✅ GOOD - use WebWorker for CPU tasks
import { Worker } from 'react-native-workers'
```

### 2. Layout (HIGH)

**Use flex patterns correctly:**
```tsx
// ✅ GOOD - flex-1 for full space
<View style={{ flex: 1 }}>

// ✅ GOOD - flexGrow for remaining space
<View style={{ flexGrow: 1 }}>

// ❌ BAD - width/height percentages
<View style={{ width: '100%' }}>
```

**Use safe area insets:**
```tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context'

function Screen() {
  const insets = useSafeAreaInsets()

  return (
    <View style={{ paddingTop: insets.top, paddingBottom: insets.bottom }}>
      {/* Content */}
    </View>
  )
}
```

**Handle keyboard properly:**
```tsx
import { KeyboardAvoidingView, Platform } from 'react-native'

<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  style={{ flex: 1 }}
>
  {/* Form */}
</KeyboardAvoidingView>
```

### 3. Animation (HIGH)

**Use Reanimated 2+ for performant animations:**
```tsx
// ✅ GOOD - Reanimated runs on UI thread
import Animated, { useSharedValue, useAnimatedStyle } from 'react-native-reanimated'

function FadeIn() {
  const opacity = useSharedValue(0)

  const style = useAnimatedStyle(() => ({
    opacity: opacity.value
  }))

  useEffect(() => {
    opacity.value = withTiming(1)
  }, [])

  return <Animated.View style={style} />
}
```

**Use gesture handler properly:**
```tsx
import { GestureDetector, Gesture } from 'react-native-gesture-handler'

function Draggable() {
  const translateX = useSharedValue(0)
  const pan = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX
    })

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={{ transform: [{ translateX }] }} />
    </GestureDetector>
  )
}
```

**Avoid animating layout properties:**
```tsx
// ❌ BAD - causes reflow
<Animated.View style={{ width: animatedWidth }} />

// ✅ GOOD - use transform
<Animated.View style={{ transform: [{ scaleX }] }} />
```

### 4. Images (MEDIUM)

**Use expo-image for fast loading:**
```tsx
// ✅ GOOD - expo-image with caching
import { Image } from 'expo-image'

<Image
  source="https://example.com/image.jpg"
  style={{ width: 200, height: 200 }}
  transition={200}
/>
```

**Optimize image sizes:**
```tsx
// ✅ GOOD - specify dimensions
<Image
  source={{ uri: 'https://example.com/image.jpg' }}
  style={{ width: 200, height: 200 }}
/>

// ✅ GOOD - use cache policy
<Image
  source={{ uri: 'https://example.com/image.jpg', cache: 'force-cache' }}
/>
```

**Lazy load images in lists:**
```tsx
// ✅ GOOD - FlashList handles this automatically
<FlashList
  data={items}
  renderItem={({ item }) => (
    <Image source={{ uri: item.image }} />
  )}
  estimatedItemSize={200}
/>
```

### 5. State Management (MEDIUM)

**Use Zustand for simple state:**
```tsx
// ✅ GOOD - Zustand for global state
import create from 'zustand'

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }))
}))
```

**Consider React Compiler:**
```tsx
// ✅ GOOD - React Compiler handles optimization
// No manual useCallback/useMemo needed when enabled
function MyComponent() {
  const [count, setCount] = useState(0)
  const handleClick = () => setCount(c => c + 1) // Auto-memoized
  return <Button onPress={handleClick}>{count}</Button>
}
```

### 6. Architecture (MEDIUM)

**Use monorepo structure:**
```
apps/
  mobile/
packages/
  ui/
  shared/
  navigation/
```

**Organize by feature:**
```
src/
  features/
    auth/
      components/
      hooks/
      screens/
      api/
    profile/
      components/
      hooks/
      screens/
      api/
```

**Use absolute imports:**
```tsx
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@features/*": ["src/features/*"]
    }
  }
}

// Usage
import { Button } from '@components/ui/Button'
```

### 7. Platform (MEDIUM)

**Handle platform differences:**
```tsx
import { Platform, StyleSheet } from 'react-native'

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: '#000' },
      android: { elevation: 4 }
    })
  }
})

// Or separate files
// Button.ios.tsx
// Button.android.tsx
```

**Use platform APIs properly:**
```tsx
// iOS specific
import { PushNotificationIOS } from '@react-native-community/push-notification-ios'

// Android specific
import { ToastAndroid } from 'react-native'

// Cross-platform
import { Platform } from 'react-native'

if (Platform.OS === 'ios') {
  // iOS code
}
```

## Expo Best Practices

**Use Expo Router for navigation:**
```tsx
// app/index.tsx
import { Stack } from 'expo-router'

export default function Layout() {
  return <Stack screenOptions={{ headerShown: false }} />
}
```

**Use development builds (not Expo Go):**
```bash
# Create development build
eas build --profile development --platform ios

# Run on device
eas build --profile development --platform android
```

**Configure app.json properly:**
```json
{
  "expo": {
    "name": "My App",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "bundleIdentifier": "com.myapp",
      "buildNumber": "1"
    },
    "android": {
      "package": "com.myapp",
      "versionCode": 1
    }
  }
}
```

## Common Issues

**Yellow box warnings:**
- Fix deprecated APIs
- Don't ignore warnings

**Memory leaks:**
```tsx
useEffect(() => {
  const subscription = someAPI.subscribe()

  return () => subscription.unsubscribe()
}, [])
```

**Jank in animations:**
- Use Reanimated
- Avoid animating layout props
- Run on UI thread

**Slow list rendering:**
- Use FlashList
- Implement getItemType
- Use keyExtractor

## Related Skills

- `vercel-react-best-practices` - React patterns that apply to RN
- `composition-patterns` - Component architecture

## Resources

- [React Native Performance](https://reactnative.dev/docs/performance)
- [Reanimated Docs](https://docs.swmansion.com/react-native-reanimated/)
- [Expo Router](https://docs.expo.dev/router/introduction/)
