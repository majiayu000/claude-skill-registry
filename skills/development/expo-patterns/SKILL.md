---
name: expo-patterns
description: Comprehensive Expo/React Native patterns - NativeTabs, SF Symbols, Apple HIG, EAS builds, animations, and SDK patterns
agents: [tap]
triggers: [expo, react native, mobile, ios, android, eas, native tabs, sf symbols, expo router]
---

# Expo Mobile Patterns

Complete guide for building beautiful cross-platform mobile apps with Expo. Combines official Expo skills with foundational patterns.

## Running the App

**CRITICAL: Always try Expo Go first before creating custom builds.**

Most Expo apps work in Expo Go without any custom native code.

```bash
npx expo start  # Scan QR with Expo Go
```

### When Custom Builds Are Required

You need `npx expo run:ios/android` or `eas build` ONLY when using:

- Local Expo modules (custom native code in `modules/`)
- Apple targets (widgets, app clips via `@bacons/apple-targets`)
- Third-party native modules not in Expo Go
- Custom native configuration

## Core Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Framework | Expo SDK | Native modules |
| Navigation | Expo Router | File-based routing |
| CLI | Expo CLI / EAS CLI | Development and builds |
| Build | EAS Build | Cloud builds |
| Deploy | EAS Submit/Update | Store submission, OTA |
| State | TanStack Query, Zustand | Server and client state |
| Animation | Reanimated | 60fps native animations |
| Gestures | Gesture Handler | Native touch handling |
| Icons | expo-symbols | SF Symbols |

## Context7 Library IDs

Query these for current best practices:

- **Expo**: `expo`
- **React Native**: `/facebook/react-native`
- **Better Auth**: `/better-auth/better-auth`

## Library Preferences

| Old/Avoid | Use Instead |
|-----------|-------------|
| `expo-av` | `expo-audio` and `expo-video` |
| `expo-permissions` | Individual package permission APIs |
| `@expo/vector-icons` | `expo-symbols` (SF Symbols) |
| `AsyncStorage` | `expo-sqlite/localStorage/install` |
| `expo-app-loading` | `expo-splash-screen` |
| `Platform.OS` | `process.env.EXPO_OS` |
| `React.useContext` | `React.use` |
| Intrinsic `img` | `expo-image` Image component |
| `expo-linear-gradient` | `experimental_backgroundImage` + CSS gradients |
| React Native `SafeAreaView` | `react-native-safe-area-context` |

## Code Style

- Always use kebab-case for file names: `comment-card.tsx`
- Routes belong in the `app` directory only
- Never co-locate components in the app directory
- Configure tsconfig.json with path aliases
- Ensure app always has a route matching "/"

## Native Tabs (SDK 54+)

Always prefer NativeTabs from `expo-router/unstable-native-tabs`:

```tsx
import { NativeTabs, Icon, Label, Badge } from "expo-router/unstable-native-tabs";

export default function TabLayout() {
  return (
    <NativeTabs minimizeBehavior="onScrollDown">
      <NativeTabs.Trigger name="index">
        <Label>Home</Label>
        <Icon sf="house.fill" />
        <Badge>9+</Badge>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="settings">
        <Icon sf="gear" />
        <Label>Settings</Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="(search)" role="search">
        <Label>Search</Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

### NativeTabs Rules

- Include a trigger for each tab
- `name` must match route name exactly (including parentheses)
- Place search tab last to combine with search bar
- Use `role` prop: `search`, `favorites`, `more`, etc.

### Icon Component

```tsx
<Icon sf="house.fill" />                              // SF Symbol only
<Icon sf="house.fill" drawable="ic_home" />           // With Android drawable
<Icon src={require('./icon.png')} />                  // Custom image
<Icon sf={{ default: "house", selected: "house.fill" }} /> // State variants
```

## SF Symbols (expo-symbols)

Use SF Symbols for native feel. Never use FontAwesome or Ionicons.

```tsx
import { SymbolView } from "expo-symbols";
import { PlatformColor } from "react-native";

<SymbolView
  tintColor={PlatformColor("label")}
  resizeMode="scaleAspectFit"
  name="square.and.arrow.down"
  style={{ width: 16, height: 16 }}
/>
```

### Common Icons

| Category | Icons |
|----------|-------|
| Navigation | `house.fill`, `gear`, `magnifyingglass`, `plus`, `xmark`, `chevron.left/right` |
| Media | `play.fill`, `pause.fill`, `stop.fill`, `speaker.wave.2.fill` |
| Social | `heart`, `heart.fill`, `star`, `star.fill`, `person`, `person.fill` |
| Actions | `square.and.arrow.up` (share), `doc.on.doc` (copy), `trash`, `pencil` |
| Status | `checkmark.circle.fill`, `xmark.circle.fill`, `exclamationmark.triangle` |

### Animated Symbols

```tsx
<SymbolView
  name="checkmark.circle"
  animationSpec={{ effect: { type: "bounce", direction: "up" } }}
/>
```

Effects: `bounce`, `pulse`, `variableColor`, `scale`

## Expo Router Navigation

### Basic Layouts

```tsx
// app/_layout.tsx - Root layout with Stack
import { Stack } from 'expo-router';
export default function RootLayout() {
  return <Stack />;
}

// app/(tabs)/_layout.tsx - Tab navigation
import { Tabs } from 'expo-router';
export default function TabLayout() {
  return <Tabs />;
}
```

### Link Navigation

```tsx
import { Link, router } from 'expo-router';

// Declarative
<Link href="/profile">Go to Profile</Link>

// With custom component
<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>

// Programmatic
router.push('/settings');
router.replace('/home');
router.back();
```

### Link Previews & Context Menus

```tsx
<Link href="/settings">
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Preview />
  <Link.Menu>
    <Link.MenuAction title="Share" icon="square.and.arrow.up" onPress={handleShare} />
    <Link.MenuAction title="Delete" icon="trash" destructive onPress={handleDelete} />
  </Link.Menu>
</Link>
```

### Modal & Sheet

```tsx
// Modal
<Stack.Screen name="modal" options={{ presentation: "modal" }} />

// Sheet with liquid glass (iOS 26+)
<Stack.Screen
  name="sheet"
  options={{
    presentation: "formSheet",
    sheetGrabberVisible: true,
    sheetAllowedDetents: [0.5, 1.0],
    contentStyle: { backgroundColor: "transparent" },
  }}
/>
```

### Dynamic Routes

```tsx
// app/[id].tsx
import { useLocalSearchParams } from 'expo-router';
export default function Detail() {
  const { id } = useLocalSearchParams();
  return <View>...</View>;
}
```

## Common Route Structure

```
app/
  _layout.tsx          — <NativeTabs />
  (index,search)/
    _layout.tsx        — <Stack />
    index.tsx          — Main list
    search.tsx         — Search view
    i/[id].tsx         — Detail view
```

## Styling (Apple HIG)

- Prefer flex gap over margin/padding
- Inline styles, not StyleSheet.create (unless reusing)
- Use `{ borderCurve: 'continuous' }` for rounded corners
- Use CSS `boxShadow`, NEVER legacy React Native shadow

```tsx
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />
```

### Responsiveness

- Use `<ScrollView contentInsetAdjustmentBehavior="automatic" />` instead of SafeAreaView
- Apply to FlatList and SectionList too
- Use flexbox, not Dimensions API
- ALWAYS prefer `useWindowDimensions` over `Dimensions.get()`

### Text

- Add `selectable` prop for copyable data
- Use `{ fontVariant: 'tabular-nums' }` for counters

## Reanimated Animations

```tsx
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring 
} from 'react-native-reanimated';

function AnimatedBox() {
  const offset = useSharedValue(0);
  
  const animatedStyles = useAnimatedStyle(() => ({
    transform: [{ translateX: withSpring(offset.value * 255) }],
  }));
  
  return <Animated.View style={[styles.box, animatedStyles]} />;
}
```

## Gesture Handling

```tsx
import { GestureDetector, Gesture } from 'react-native-gesture-handler';

function SwipeableCard() {
  const gesture = Gesture.Pan()
    .onUpdate((event) => {
      offset.value = event.translationX;
    })
    .onEnd(() => {
      offset.value = withSpring(0);
    });

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={animatedStyles} />
    </GestureDetector>
  );
}
```

## Visual Effects

```tsx
// Blur
import { BlurView } from 'expo-blur';
<BlurView intensity={50} style={StyleSheet.absoluteFill} />

// Liquid Glass (iOS 26+)
import { GlassView } from 'expo-glass-effect';
<GlassView style={styles.glass} cornerRadius={16} />
```

## Common Expo SDK Patterns

```tsx
// Camera
import { CameraView, useCameraPermissions } from 'expo-camera';

// Notifications  
import * as Notifications from 'expo-notifications';

// Location
import * as Location from 'expo-location';

// Secure Storage
import * as SecureStore from 'expo-secure-store';

// Haptics (iOS)
import * as Haptics from 'expo-haptics';

// Splash Screen
import * as SplashScreen from 'expo-splash-screen';
SplashScreen.preventAutoHideAsync();
SplashScreen.hideAsync();
```

## App Configuration

```typescript
// app.config.ts
export default {
  expo: {
    name: "MyApp",
    slug: "my-app",
    version: "1.0.0",
    ios: {
      bundleIdentifier: "com.company.myapp",
      supportsTablet: true,
    },
    android: {
      package: "com.company.myapp",
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#ffffff"
      }
    },
    plugins: [
      "expo-router",
      ["expo-splash-screen", { backgroundColor: "#ffffff" }],
    ]
  }
};
```

## EAS Build Configuration

```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "...", "ascAppId": "..." },
      "android": { "track": "internal" }
    }
  }
}
```

### Build Commands

```bash
npm install -g eas-cli && eas login

# Development build
eas build --platform ios --profile development
eas build --platform android --profile development

# Production build
eas build --platform all --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android

# OTA Update (no app store review!)
eas update --branch production --message "Bug fix"
```

## Environment Variables

```bash
# .env (EXPO_PUBLIC_ prefix required)
EXPO_PUBLIC_API_URL=https://api.example.com

# Access in code
const apiUrl = process.env.EXPO_PUBLIC_API_URL;

# EAS environments
eas env:pull --environment development
```

## Validation Commands

```bash
npx tsc --noEmit        # Type check
npx eslint .            # Lint
npm test                # Tests
npx expo-doctor         # Doctor check
npx expo start          # Start dev
```

## Mobile Best Practices

- **Expo Go first** - only create custom builds when needed
- **Use Expo Router** for navigation (file-based, automatic deep linking)
- **Respect platform conventions** (iOS HIG, Material Design)
- **60fps animations** with Reanimated worklets
- **Handle safe areas** with `contentInsetAdjustmentBehavior="automatic"`
- **Use expo-haptics** conditionally on iOS
- **Offline-first** with proper loading/error states
- **Test on real devices** via EAS internal distribution
- **Accessibility** - use `accessibilityLabel`, `accessibilityRole`
- **OTA updates** - use EAS Update for instant bug fixes
