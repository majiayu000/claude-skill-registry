---
name: expo-app-design
description: Official Expo UI guidelines - build beautiful apps with Expo Router, NativeTabs, SF Symbols, animations, and Apple HIG patterns
agents: [tap]
triggers: [expo ui, expo design, native tabs, sf symbols, expo router navigation, mobile ui, ios design, expo patterns]
---

# Expo App Design

Complete guide for building beautiful apps with Expo Router. Based on official Expo skills from expo/skills repository.

## Running the App

**CRITICAL: Always try Expo Go first before creating custom builds.**

Most Expo apps work in Expo Go without any custom native code. Before running `npx expo run:ios` or `npx expo run:android`:

1. **Start with Expo Go**: Run `npx expo start` and scan the QR code with Expo Go
2. **Check if features work**: Test your app thoroughly in Expo Go
3. **Only create custom builds when required**

### When Custom Builds Are Required

You need `npx expo run:ios/android` or `eas build` ONLY when using:

- **Local Expo modules** (custom native code in `modules/`)
- **Apple targets** (widgets, app clips, extensions via `@bacons/apple-targets`)
- **Third-party native modules** not included in Expo Go
- **Custom native configuration** that can't be expressed in `app.json`

## Code Style

- Always use kebab-case for file names, e.g. `comment-card.tsx`
- Always remove old route files when moving or restructuring navigation
- Never use special characters in file names
- Configure tsconfig.json with path aliases, prefer aliases over relative imports
- Be cautious of unterminated strings and escape nested backticks properly

## Routes

- Routes belong in the `app` directory
- Never co-locate components, types, or utilities in the app directory
- Ensure the app always has a route that matches "/"

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

## Responsiveness

- Always wrap root component in a scroll view for responsiveness
- Use `<ScrollView contentInsetAdjustmentBehavior="automatic" />` instead of `<SafeAreaView>`
- Apply `contentInsetAdjustmentBehavior="automatic"` to FlatList and SectionList
- Use flexbox instead of Dimensions API
- ALWAYS prefer `useWindowDimensions` over `Dimensions.get()`

## Styling (Apple HIG)

- Prefer flex gap over margin and padding styles
- Prefer padding over margin where possible
- Inline styles not StyleSheet.create unless reusing styles
- Add entering and exiting animations for state changes
- Use `{ borderCurve: 'continuous' }` for rounded corners unless creating a capsule
- ALWAYS use a navigation stack title instead of custom text element
- Use CSS `boxShadow` style prop, NEVER use legacy React Native shadow or elevation
- CSS and Tailwind are not supported - use inline styles

```tsx
// Correct shadow usage
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />
```

### Text Styling

- Add `selectable` prop to `<Text/>` displaying important data or error messages
- Counters should use `{ fontVariant: 'tabular-nums' }` for alignment

## Navigation

### Link

Use `<Link href="/path" />` from 'expo-router' for navigation:

```tsx
import { Link } from 'expo-router';

// Basic link
<Link href="/path" />

// Wrapping custom components
<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>
```

Include `<Link.Preview>` to follow iOS conventions for context menus and previews:

```tsx
<Link href="/settings">
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Preview />
</Link>
```

### Context Menus

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

### Modal

```tsx
<Stack.Screen name="modal" options={{ presentation: "modal" }} />
```

### Sheet

```tsx
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

## Native Tabs (SDK 54+)

Always prefer NativeTabs from 'expo-router/unstable-native-tabs':

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
- Use `role` prop for common tab types: `search`, `favorites`, `more`, etc.

### Icon Component

```tsx
<Icon sf="house.fill" />                              // SF Symbol only
<Icon sf="house.fill" drawable="ic_home" />           // With Android drawable
<Icon src={require('./icon.png')} />                  // Custom image
<Icon sf={{ default: "house", selected: "house.fill" }} /> // State variants
```

### Badge Component

```tsx
<Badge>9+</Badge>  // Numeric badge
<Badge />          // Dot indicator
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
| Actions | `square.and.arrow.up` (share), `doc.on.doc` (copy), `trash` (delete), `pencil` (edit) |
| Status | `checkmark.circle.fill`, `xmark.circle.fill`, `exclamationmark.triangle`, `bell.fill` |

### Animated Symbols

```tsx
<SymbolView
  name="checkmark.circle"
  animationSpec={{
    effect: { type: "bounce", direction: "up" }
  }}
/>
```

Effects: `bounce`, `pulse`, `variableColor`, `scale`

### Symbol Weights

`ultraLight`, `thin`, `light`, `regular`, `medium`, `semibold`, `bold`, `heavy`, `black`

## Common Route Structure

```
app/
  _layout.tsx          — <NativeTabs />
  (index,search)/
    _layout.tsx        — <Stack />
    index.tsx          — Main list
    search.tsx         — Search view
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

```tsx
// app/(index,search)/_layout.tsx - Shared stack for both tabs
import { Stack } from "expo-router/stack";
import { PlatformColor } from "react-native";

export default function Layout({ segment }) {
  const screen = segment.match(/\((.*)\\)/)?.[1]!;
  const titles = { index: "Items", search: "Search" };

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

## Behavior

- Use expo-haptics conditionally on iOS for delightful experiences
- Use views with built-in haptics like `<Switch />` and `@react-native-community/datetimepicker`
- When a route belongs to a Stack, its first child should be a ScrollView with `contentInsetAdjustmentBehavior="automatic"`
- Prefer `headerSearchBarOptions` in Stack.Screen options to add a search bar
- Use `<Text selectable />` for data that could be copied
- Format large numbers (1.4M, 38k)
- Never use intrinsic elements like 'img' or 'div' unless in webview or DOM component

## Visual Effects

### Blur Effects (expo-blur)

```tsx
import { BlurView } from 'expo-blur';

<BlurView intensity={50} style={StyleSheet.absoluteFill} />
```

### Liquid Glass (expo-glass-effect)

```tsx
import { GlassView } from 'expo-glass-effect';

<GlassView style={styles.glass} cornerRadius={16} />
```

## Validation Commands

```bash
npx tsc --noEmit        # Type check
npx eslint .            # Lint
npm test                # Tests
npx expo-doctor         # Doctor check
npx expo start          # Start dev
```
