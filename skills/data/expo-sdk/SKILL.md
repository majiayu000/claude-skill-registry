---
name: expo-sdk
description: Expo SDK 54+ platform patterns. Use when configuring Expo apps, setting up root layouts, using expo-image, expo-haptics, safe areas, bottom sheets, FlashList, or StatusBar.
---

# Expo SDK

## Overview

Expo SDK 54+ provides a managed React Native development environment with file-based routing (Expo Router), native module access, and streamlined build tooling. This skill covers app configuration, the root layout provider pattern, and key Expo/RN libraries.

**Prerequisite**: `npx create-expo-app` or Expo SDK 54+ in `package.json`

## Workflows

**Setting up a new Expo demo:**
1. [ ] Create project: `npx create-expo-app [demo-name] --template blank-typescript`
2. [ ] Install core dependencies: `pnpm add expo-router expo-image expo-haptics react-native-reanimated react-native-gesture-handler react-native-safe-area-context @gorhom/bottom-sheet @shopify/flash-list lucide-react-native nativewind tailwindcss@3`
3. [ ] Configure NativeWind (see `nativewind` skill)
4. [ ] Set up root layout with provider stack
5. [ ] Configure `app.json` with scheme, name, splash
6. [ ] Add route groups and screens
7. [ ] Run: `pnpm start` (Expo dev server)

**Adding a new library:**
1. [ ] Install with pnpm: `pnpm add [library]`
2. [ ] Check if Expo config plugin needed in `app.json`
3. [ ] Rebuild dev client if native module added: `npx expo prebuild`

## Guidance

### app.json Configuration

Key fields for demo apps:

| Field | Purpose |
|-------|---------|
| `expo.name` | Display name |
| `expo.slug` | URL-safe identifier |
| `expo.scheme` | Deep link scheme (e.g., `myapp`) |
| `expo.orientation` | `portrait` (default for demos) |
| `expo.splash` | Splash screen configuration |
| `expo.ios.bundleIdentifier` | iOS bundle ID |
| `expo.android.package` | Android package name |
| `expo.plugins` | Expo config plugins (e.g., `expo-router`) |

### Root Layout Provider Pattern

The root `app/_layout.tsx` wraps the entire app with providers. Standard order:

```
GestureHandlerRootView (flex: 1)
  └── SafeAreaProvider
       └── ThemeProvider / Context
            └── Stack (Expo Router)
```

- `GestureHandlerRootView` must be outermost (required by gesture handler and bottom sheets)
- `SafeAreaProvider` provides safe area insets to all descendants
- App-level context providers go between SafeAreaProvider and Stack
- `<Stack screenOptions={{ headerShown: false }} />` for custom headers

### expo-image (replaces RN Image)

Use `expo-image` for all image rendering — provides caching, blurhash placeholders, content-fit modes, and animated transitions.

Key props:
- `source` — URI string or require() for local images
- `placeholder` — blurhash string for loading state
- `contentFit` — `'cover'` | `'contain'` | `'fill'`
- `transition` — fade-in duration in ms (e.g., `300`)

### expo-haptics

Provide tactile feedback on interactions:

- `Haptics.selectionAsync()` — light tap for selections, toggles
- `Haptics.impactAsync(ImpactFeedbackStyle.Medium)` — button press, card tap
- `Haptics.notificationAsync(NotificationFeedbackType.Success)` — action completion

Use sparingly — haptics on every touch is annoying.

### Safe Area Insets

Account for device notch, status bar, and home indicator:

- `useSafeAreaInsets()` — returns `{ top, bottom, left, right }` in points
- Apply to screen containers: `paddingTop: insets.top`
- NativeWind classes: use `pt-[${insets.top}px]` or wrap in SafeAreaView

### @gorhom/bottom-sheet

Replaces Radix Dialog for mobile modal patterns:

- Use for detail views, selections, filters, forms
- Define snap points: `snapPoints={['25%', '50%', '90%']}`
- Backdrop: `backdropComponent` with press-to-dismiss
- `BottomSheetScrollView` for scrollable content inside sheets
- Requires `GestureHandlerRootView` as ancestor

### FlashList (replaces FlatList)

High-performance list rendering from `@shopify/flash-list`:

- Drop-in FlatList replacement with mandatory `estimatedItemSize` prop
- `estimatedItemSize={80}` — estimated height of each item in points
- Recycling architecture for smooth 60fps scrolling
- Use `contentContainerClassName` for NativeWind styling

### lucide-react-native

Icon library for React Native (matches web lucide-react):

- Import individual icons: `import { Home, Settings, ChevronRight } from 'lucide-react-native'`
- Props: `size`, `color`, `strokeWidth`
- Consistent icon set across mobile and web codebases

### StatusBar

Configure status bar appearance per screen:

- `<StatusBar style="dark" />` for light backgrounds
- `<StatusBar style="light" />` for dark backgrounds
- Import from `expo-status-bar`

## Best Practices

- Wrap root layout in `GestureHandlerRootView` with `style={{ flex: 1 }}`
- Use expo-image for all images (caching, blurhash, performance)
- Add haptics to primary actions only (buttons, major selections) — not every touch
- Set `estimatedItemSize` on all FlashList components
- Place providers in root `_layout.tsx`, not in individual screens
- Use `useSafeAreaInsets()` for manual padding, `SafeAreaView` for simple wrapping
- Test on real device for haptics and performance verification

## Anti-Patterns

- Using React Native `Image` instead of `expo-image`
- Using `FlatList` for large datasets instead of `FlashList`
- Forgetting `GestureHandlerRootView` (causes bottom sheet and gesture crashes)
- Overusing haptics on every interaction
- Hardcoding status bar height instead of using safe area insets
- Missing `estimatedItemSize` on FlashList (required prop, console warning)
- Placing `SafeAreaView` inside ScrollView (causes layout issues)
- Not including `expo-router` plugin in `app.json` plugins array
