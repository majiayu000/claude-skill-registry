---
name: native-ui
model: standard
version: 1.0.0
description: >
  Building native mobile UIs with Expo Router and React Native. Covers routing,
  navigation, styling, native controls, animations, and platform conventions
  following Apple Human Interface Guidelines.
tags: [expo, react-native, ios, mobile, navigation, native-ui]
---

# Native UI with Expo Router

Patterns and conventions for building native mobile applications with Expo Router and React Native.

## References

Consult these as needed:

- `./references/route-structure.md` — Route conventions, dynamic routes, groups, folder organization
- `./references/tabs.md` — Native tab bar with NativeTabs, iOS 26 features
- `./references/icons.md` — SF Symbols with expo-symbols, icon names, animations, weights
- `./references/controls.md` — Native iOS controls: Switch, Slider, SegmentedControl, DateTimePicker
- `./references/visual-effects.md` — Blur effects (expo-blur) and liquid glass (expo-glass-effect)
- `./references/animations.md` — Reanimated: entering, exiting, layout, scroll-driven, gestures
- `./references/search.md` — Search bar with headers, useSearch hook, filtering patterns
- `./references/gradients.md` — CSS gradients via experimental_backgroundImage (New Architecture only)
- `./references/media.md` — Camera, audio, video, file saving
- `./references/storage.md` — SQLite, AsyncStorage, SecureStore
- `./references/webgpu-three.md` — 3D graphics and GPU visualizations with WebGPU/Three.js
- `./references/toolbar-and-headers.md` — Stack headers and toolbar with buttons, menus, search bars (iOS)
- `./references/form-sheet.md` — Form sheet presentation patterns

## Running the App

**Always try Expo Go first before creating custom builds.**

1. Start with `npx expo start` and scan the QR code
2. Test features in Expo Go
3. Only create custom builds when required

### When Custom Builds Are Required

Use `npx expo run:ios/android` or `eas build` only for:

- Local Expo modules (custom native code in `modules/`)
- Apple targets (widgets, app clips via `@bacons/apple-targets`)
- Third-party native modules not in Expo Go
- Custom native configuration beyond `app.json`

Expo Go supports all `expo-*` packages, Expo Router, Reanimated, Gesture Handler, push notifications, and deep links out of the box.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install native-ui
```


---

## Code Style

- Escape nested backticks and quotes correctly
- Always use import statements at the top of the file
- Use kebab-case for file names: `comment-card.tsx`
- Remove old route files when restructuring navigation
- No special characters in file names
- Configure `tsconfig.json` path aliases; prefer aliases over relative imports

## Routes

See `./references/route-structure.md` for detailed conventions.

- Routes belong in the `app` directory
- Never co-locate components, types, or utilities in `app/` — this is an anti-pattern
- Always have a route matching `/`, possibly inside a group route

## Library Preferences

| Use | Instead of |
|-----|------------|
| `expo-audio` | `expo-av` |
| `expo-video` | `expo-av` |
| `expo-symbols` | `@expo/vector-icons` |
| `react-native-safe-area-context` | RN SafeAreaView |
| `process.env.EXPO_OS` | `Platform.OS` |
| `React.use` | `React.useContext` |
| `expo-image` | Intrinsic `img` element |
| `expo-glass-effect` | Custom glass backdrops |

Never use deprecated modules: Picker, WebView, SafeAreaView, AsyncStorage (from RN core), or legacy `expo-permissions`.

---

## Responsiveness

- Wrap root components in a scroll view
- Use `<ScrollView contentInsetAdjustmentBehavior="automatic" />` instead of `<SafeAreaView>`
- Apply `contentInsetAdjustmentBehavior="automatic"` to FlatList and SectionList too
- Use flexbox instead of Dimensions API
- Prefer `useWindowDimensions` over `Dimensions.get()` for screen measurement

## Behavior

- Use `expo-haptics` conditionally on iOS for delightful interactions
- Use views with built-in haptics (`<Switch />`, `@react-native-community/datetimepicker`)
- First child of a Stack route should almost always be a ScrollView with `contentInsetAdjustmentBehavior="automatic"`
- Prefer `headerSearchBarOptions` in Stack.Screen options for search bars
- Use `<Text selectable />` on data that users may want to copy
- Format large numbers: 1.4M, 38k
- Never use intrinsic elements (`img`, `div`) outside webviews or Expo DOM components

---

## Styling

Follow Apple Human Interface Guidelines.

### General Rules

- Prefer flex gap over margin and padding
- Prefer padding over margin
- Always account for safe area via stack headers, tabs, or `contentInsetAdjustmentBehavior="automatic"`
- Ensure both top and bottom safe area insets are handled
- Inline styles preferred over `StyleSheet.create` unless reusing styles
- Add entering/exiting animations for state changes
- Use `{ borderCurve: 'continuous' }` for rounded corners (not capsule shapes)
- Use navigation stack title instead of custom text headers
- On ScrollView, use `contentContainerStyle` for padding/gap (avoids clipping)
- CSS and Tailwind are not supported — use inline styles

### Text Styling

- Add `selectable` prop to `<Text/>` elements showing important data or errors
- Use `{ fontVariant: 'tabular-nums' }` on counters for alignment

### Shadows

Use CSS `boxShadow` style prop. Never use legacy RN shadow or elevation styles.

```tsx
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />
```

Inset shadows are supported.

---

## Navigation

### Link

Use `<Link href="/path" />` from `expo-router` for navigation.

```tsx
import { Link } from 'expo-router';

<Link href="/path" />

<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>
```

Include `<Link.Preview>` whenever possible to follow iOS conventions. Add context menus and previews frequently.

### Stack

- Always use `_layout.tsx` files to define stacks
- Use `Stack` from `expo-router/stack` for native navigation stacks
- Set page titles in Stack.Screen options: `options={{ title: "Home" }}`

### Context Menus

Add long-press context menus to Link components:

```tsx
<Link href="/settings" asChild>
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Menu>
    <Link.MenuAction title="Share" icon="square.and.arrow.up" onPress={handleShare} />
    <Link.MenuAction title="Block" icon="nosign" destructive onPress={handleBlock} />
    <Link.Menu title="More" icon="ellipsis">
      <Link.MenuAction title="Copy" icon="doc.on.doc" onPress={() => {}} />
      <Link.MenuAction title="Delete" icon="trash" destructive onPress={() => {}} />
    </Link.Menu>
  </Link.Menu>
</Link>
```

### Link Previews

```tsx
<Link href="/settings">
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Preview />
</Link>
```

Can be combined with context menus.

### Modal

Present a screen as a modal:

```tsx
<Stack.Screen name="modal" options={{ presentation: "modal" }} />
```

Prefer this over custom modal components.

### Sheet

Present as a dynamic form sheet:

```tsx
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

`contentStyle: { backgroundColor: "transparent" }` enables liquid glass on iOS 26+.

---

## Common Route Structure

Standard app layout with tabs and stacks:

```
app/
  _layout.tsx        — <NativeTabs />
  (index,search)/
    _layout.tsx      — <Stack />
    index.tsx        — Main list
    search.tsx       — Search view
```

**Root layout:**

```tsx
// app/_layout.tsx
import { NativeTabs, Icon, Label } from "expo-router/unstable-native-tabs";
import { Theme } from "../components/theme";

export default function Layout() {
  return (
    <Theme>
      <NativeTabs>
        <NativeTabs.Trigger name="(index)">
          <Icon sf="list.dash" />
          <Label>Items</Label>
        </NativeTabs.Trigger>
        <NativeTabs.Trigger name="(search)" role="search" />
      </NativeTabs>
    </Theme>
  );
}
```

**Shared group layout:**

```tsx
// app/(index,search)/_layout.tsx
import { Stack } from "expo-router/stack";
import { PlatformColor } from "react-native";

export default function Layout({ segment }) {
  const screen = segment.match(/\((.*)\)/)?.[1]!;
  const titles: Record<string, string> = { index: "Items", search: "Search" };

  return (
    <Stack
      screenOptions={{
        headerTransparent: true,
        headerShadowVisible: false,
        headerLargeTitleShadowVisible: false,
        headerLargeStyle: { backgroundColor: "transparent" },
        headerTitleStyle: { color: PlatformColor("label") },
        headerLargeTitle: true,
        headerBlurEffect: "none",
        headerBackButtonDisplayMode: "minimal",
      }}
    >
      <Stack.Screen name={screen} options={{ title: titles[screen] }} />
      <Stack.Screen name="i/[id]" options={{ headerLargeTitle: false }} />
    </Stack>
  );
}
```
