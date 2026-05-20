---
name: expo-native-ui
model: standard
version: 1.0.0
description: >
  Build beautiful native iOS/Android apps with Expo Router. Covers route structure,
  native tabs, animations, blur effects, liquid glass, SF Symbols, and platform patterns.
tags: [expo, react-native, ios, android, mobile, navigation, animations]
---

# Expo Native UI

Build production-quality native mobile apps with Expo Router following Apple Human Interface Guidelines and modern React Native patterns.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install expo-native-ui
```


## WHAT This Skill Does

Guides implementation of native mobile apps using Expo Router with:
- File-based routing with native navigation stacks
- Native tab bars (NativeTabs) and iOS 26 features
- SF Symbols integration via expo-symbols
- Blur effects (expo-blur) and liquid glass (expo-glass-effect)
- Reanimated animations and gesture handling
- Native controls: Switch, Slider, SegmentedControl, DateTimePicker

## WHEN To Use

- Building a new Expo Router app
- Adding native tab navigation
- Implementing iOS-style blur or liquid glass effects
- Creating smooth animations with entering/exiting transitions
- Integrating SF Symbols for icons
- Setting up route structure with groups and dynamic routes

## KEYWORDS

expo router, react native, native tabs, sf symbols, expo blur, liquid glass, reanimated, ios, android, mobile app, navigation stack, form sheet, modal, context menu, link preview

## References

Consult these resources for detailed implementation:

| Reference | Purpose |
|-----------|---------|
| `references/route-structure.md` | Route conventions, dynamic routes, groups, query params |
| `references/tabs.md` | NativeTabs, migration from JS tabs, iOS 26 features |
| `references/icons.md` | SF Symbols with expo-symbols, animations, weights |
| `references/controls.md` | Native iOS controls: Switch, Slider, DateTimePicker, Picker |
| `references/visual-effects.md` | Blur effects and liquid glass |
| `references/animations.md` | Reanimated: entering, exiting, layout, scroll-driven |
| `references/search.md` | Search bar integration, useSearch hook, filtering |
| `references/gradients.md` | CSS gradients via experimental_backgroundImage |
| `references/media.md` | Camera, audio, video, file saving |
| `references/storage.md` | SQLite, AsyncStorage, SecureStore |
| `references/webgpu-three.md` | WebGPU, Three.js for 3D graphics |
| `references/toolbar-and-headers.md` | Stack headers, toolbar customization (iOS) |

## Core Principles

### Running the App

**Try Expo Go first** before creating custom builds:

```bash
npx expo start  # Scan QR with Expo Go
```

Custom builds (`npx expo run:ios`) only needed for:
- Local Expo modules (custom native code in `modules/`)
- Apple targets (widgets, app clips via `@bacons/apple-targets`)
- Third-party native modules not in Expo Go

### Code Style

- **Kebab-case file names**: `comment-card.tsx`
- **Path aliases in tsconfig** over relative imports
- **Never co-locate** components/utilities in `app/` directory
- **Always ensure** a route matches "/" (may be in a group)
- **Escape nested backticks** carefully in strings

### Library Preferences

| Use | Instead Of |
|-----|------------|
| `expo-audio` | `expo-av` |
| `expo-video` | `expo-av` |
| `expo-symbols` | `@expo/vector-icons` |
| `react-native-safe-area-context` | RN SafeAreaView |
| `process.env.EXPO_OS` | `Platform.OS` |
| `React.use` | `React.useContext` |
| `expo-image` | intrinsic `img` element |
| `expo-glass-effect` | custom blur views |

### Responsiveness

```tsx
// Always wrap root in ScrollView with automatic insets
<ScrollView contentInsetAdjustmentBehavior="automatic">
  {children}
</ScrollView>

// Use useWindowDimensions, not Dimensions.get()
const { width, height } = useWindowDimensions();

// Flexbox over Dimensions API
<View style={{ flex: 1, flexDirection: 'row', gap: 16 }} />
```

## Navigation Patterns

### Link with Preview and Context Menu

```tsx
import { Link } from 'expo-router';

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

### Form Sheet Modal

```tsx
// In _layout.tsx
<Stack.Screen
  name="sheet"
  options={{
    presentation: "formSheet",
    sheetGrabberVisible: true,
    sheetAllowedDetents: [0.5, 1.0],
    contentStyle: { backgroundColor: "transparent" }, // Liquid glass on iOS 26+
  }}
/>
```

### Native Tabs Structure

```
app/
  _layout.tsx — <NativeTabs />
  (index,search)/
    _layout.tsx — <Stack />
    index.tsx
    search.tsx
```

```tsx
// app/_layout.tsx
import { NativeTabs, Icon, Label } from "expo-router/unstable-native-tabs";

export default function Layout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="(index)">
        <Icon sf="list.dash" />
        <Label>Items</Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="(search)" role="search" />
    </NativeTabs>
  );
}
```

## Styling Guidelines

- **Flex gap** over margin/padding where possible
- **`borderCurve: 'continuous'`** for rounded corners (not capsules)
- **`boxShadow`** style prop, never legacy RN shadow/elevation
- **Stack title** instead of custom text elements for page headers
- **Inline styles**, not `StyleSheet.create` unless reusing
- **`fontVariant: 'tabular-nums'`** for numeric counters
- **`selectable` prop** on Text displaying copiable data

```tsx
// Shadow example
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />

// Continuous border curve
<View style={{ borderRadius: 12, borderCurve: 'continuous' }} />
```

## Behavior Patterns

- **Haptics**: Use `expo-haptics` conditionally on iOS
- **Search bar**: Prefer `headerSearchBarOptions` in Stack.Screen
- **Selectable text**: Add `selectable` prop to important data
- **Format large numbers**: 1.4M, 38k instead of 1,400,000
- **Never use** intrinsic elements (`img`, `div`) outside DOM components

## NEVER Do

1. **NEVER use** legacy modules: Picker, WebView, SafeAreaView from react-native, AsyncStorage (old), expo-permissions
2. **NEVER use** `Dimensions.get()` — always `useWindowDimensions`
3. **NEVER co-locate** components in the `app/` directory
4. **NEVER use** `Platform.OS` — use `process.env.EXPO_OS`
5. **NEVER use** legacy shadow styles — use CSS `boxShadow`
6. **NEVER start** with custom builds — try Expo Go first
7. **NEVER use** StyleSheet.create for one-time styles
8. **NEVER use** `@expo/vector-icons` — use `expo-symbols`
