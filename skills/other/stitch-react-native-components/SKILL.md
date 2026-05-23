---
name: stitch-react-native-components
description: Converts Stitch mobile designs into React Native / Expo components — TypeScript, StyleSheet, Expo Router, dark mode via useColorScheme, and proper touch targets. Cross-platform iOS and Android.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch → React Native / Expo Components

You are a React Native engineer. You convert Stitch mobile designs (deviceType: MOBILE) into cross-platform React Native components using Expo. You work in TypeScript, use `StyleSheet.create` for styles, and follow Expo Router conventions for navigation.

## When to use this skill

Use this skill when:
- The user wants a **native mobile app** (iOS + Android) from a Stitch design
- The user mentions "React Native", "Expo", "mobile app", "iOS", "Android"
- The Stitch design was generated with `deviceType: MOBILE`

**Note:** For a mobile WebView app (Capacitor, Ionic, PWA), use `stitch-html-components` instead. React Native outputs actual native UI — not web views.

## Prerequisites

- Stitch design generated with `deviceType: MOBILE` (desktop designs don't translate well to RN)
- Target project uses **Expo** (SDK 50+) — not bare React Native
- `expo-router` for file-based navigation

## Step 1: Retrieve the design

Only call this skill for **MOBILE** Stitch designs. If the screenshot shows a desktop layout, stop and tell the user to regenerate with `deviceType: MOBILE` first.

1. `list_tools` → find Stitch prefix
2. `[prefix]:get_screen` → fetch design JSON
3. Download HTML: `bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"`
4. Check `screenshot.downloadUrl` — verify it's a mobile layout (narrow, vertical)

## Step 2: Project structure

```
app/
├── (tabs)/
│   ├── _layout.tsx       ← Tab navigator
│   ├── index.tsx         ← Home tab
│   └── [other-tabs].tsx
├── _layout.tsx           ← Root layout (ThemeProvider, SafeAreaProvider)
└── modal.tsx             ← Modal routes
src/
├── components/           ← Reusable components
│   └── [Name].tsx
├── data/
│   └── mockData.ts       ← Static content — never hardcoded in components
├── theme/
│   ├── tokens.ts         ← Design tokens as TypeScript constants
│   └── useTheme.ts       ← Hook to access current theme tokens
└── types/
    └── index.ts
```

## Step 3: The HTML → React Native mapping

This is the core of the conversion. Apply these rules systematically:

### Layout mapping

| HTML/CSS | → React Native |
|---|---|
| `<div style="display:flex; flex-direction:column">` | `<View style={{flexDirection:'column'}}>` |
| `<div style="display:flex; flex-direction:row">` | `<View style={{flexDirection:'row'}}>` |
| `<div style="display:grid; grid-template-columns:1fr 1fr">` | `<View style={{flexDirection:'row', flexWrap:'wrap'}}>` with `width:'50%'` children |
| `overflow-y: scroll` container | `<ScrollView>` |
| Long lists | `<FlatList data={items} renderItem={...} keyExtractor={...}>` |
| `position: fixed` bottom nav | `<View style={{position:'absolute', bottom:0, left:0, right:0}}>` |
| `position: absolute` overlay | `<View style={{position:'absolute', ...}}>` inside a parent with `position:'relative'` |

### Content mapping

| HTML | → React Native |
|---|---|
| `<p>`, `<span>`, text nodes | `<Text>` |
| `<h1>` → `<h6>` | `<Text>` with large font size + fontWeight: 'bold' |
| `<img src="...">` | `<Image source={{uri: '...'}} style={{width:X, height:Y}}>` |
| `<button>` | `<Pressable>` (preferred) or `<TouchableOpacity>` |
| `<a>` (navigation) | `<Pressable onPress={() => router.push('/route')}>` |
| `<input type="text">` | `<TextInput>` |
| `<input type="password">` | `<TextInput secureTextEntry={true}>` |
| `<input type="checkbox">` | Custom or `@expo/vector-icons` + `Pressable` |
| `<select>` / dropdown | `@react-native-picker/picker` or custom modal picker |
| `<nav>` (tabs) | Expo Router `<Tabs>` layout |

### Spacing mapping

React Native uses unitless numbers (dp — density-independent pixels):

```ts
// Approximate Tailwind → RN
const spacing = {
  1: 4,   // p-1 = 4dp
  2: 8,   // p-2 = 8dp
  3: 12,
  4: 16,
  5: 20,
  6: 24,
  8: 32,
  10: 40,
  12: 48,
  16: 64,
}
```

### Color mapping

```ts
// src/theme/tokens.ts — extract from Stitch Tailwind config
export const lightTokens = {
  background: '#FFFFFF',   // from --color-background
  surface: '#F4F4F5',
  primary: '#6366F1',
  primaryFg: '#FFFFFF',
  text: '#09090B',
  textMuted: '#71717A',
  border: '#E4E4E7',
} as const

export const darkTokens = {
  background: '#09090B',
  surface: '#18181B',
  primary: '#818CF8',      // Lighter shade for dark bg
  primaryFg: '#09090B',
  text: '#FAFAFA',
  textMuted: '#A1A1AA',
  border: '#27272A',
} as const

export type ThemeTokens = typeof lightTokens
```

## Step 4: Dark mode with useColorScheme

```tsx
// src/theme/useTheme.ts
import { useColorScheme } from 'react-native'
import { lightTokens, darkTokens, type ThemeTokens } from './tokens'

/**
 * Returns the current theme's design tokens.
 * Automatically switches based on system color scheme.
 */
export function useTheme(): ThemeTokens {
  const scheme = useColorScheme()
  return scheme === 'dark' ? darkTokens : lightTokens
}
```

```tsx
// Usage in any component
import { useTheme } from '@/theme/useTheme'

export function Card({ title }: { title: string }) {
  const theme = useTheme()

  return (
    <View style={[styles.card, { backgroundColor: theme.surface, borderColor: theme.border }]}>
      <Text style={[styles.title, { color: theme.text }]}>{title}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 12,
    borderWidth: 1,
    padding: 16,
    marginBottom: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
  },
})
```

## Step 5: Safe area and platform considerations

```tsx
// app/_layout.tsx — root layout
import { SafeAreaProvider } from 'react-native-safe-area-context'
import { Stack } from 'expo-router'

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      </Stack>
    </SafeAreaProvider>
  )
}
```

```tsx
// In screen components — use safe area insets
import { useSafeAreaInsets } from 'react-native-safe-area-context'

export default function HomeScreen() {
  const insets = useSafeAreaInsets()

  return (
    <View style={{ flex: 1, paddingTop: insets.top, paddingBottom: insets.bottom }}>
      {/* Content */}
    </View>
  )
}
```

## Step 6: Component template

```tsx
// src/components/StitchComponent.tsx
import { View, Text, Pressable, StyleSheet } from 'react-native'
import { useTheme } from '@/theme/useTheme'

/**
 * Props for StitchComponent.
 * All data via props — never fetched inside the component.
 */
interface StitchComponentProps {
  title: string
  description?: string
  onPress?: () => void
}

/**
 * StitchComponent — [describe purpose in one sentence]
 */
export function StitchComponent({ title, description, onPress }: Readonly<StitchComponentProps>) {
  const theme = useTheme()

  return (
    <Pressable
      style={({ pressed }) => [
        styles.container,
        {
          backgroundColor: theme.surface,
          borderColor: theme.border,
          opacity: pressed ? 0.8 : 1,   // Visual feedback on press
        },
      ]}
      onPress={onPress}
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={title}
      hitSlop={8}   // Increase tap area without changing visual size
    >
      <Text style={[styles.title, { color: theme.text }]}>{title}</Text>
      {description ? (
        <Text style={[styles.description, { color: theme.textMuted }]}>{description}</Text>
      ) : null}
    </Pressable>
  )
}

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    borderWidth: 1,
    padding: 16,
    gap: 8,
    // Minimum touch target
    minHeight: 44,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    lineHeight: 24,
  },
  description: {
    fontSize: 14,
    lineHeight: 20,
  },
})
```

## Step 7: Accessibility in React Native

```tsx
// Every interactive element needs these props
<Pressable
  accessible={true}
  accessibilityRole="button"    // "button" | "link" | "text" | "image" | "header" | ...
  accessibilityLabel="Close dialog"   // What screen reader announces
  accessibilityHint="Double tap to close the modal"  // Optional extra context
  accessibilityState={{ disabled: false, selected: false }}
>

// Images
<Image
  accessible={true}
  accessibilityLabel="Profile photo of Emma Johnson"  // Descriptive alt text
  // OR for decorative:
  accessible={false}
/>

// Text hierarchy (screen reader uses accessibilityRole="header" for h1-h6 equivalent)
<Text accessibilityRole="header" style={styles.pageTitle}>Dashboard</Text>
```

## Execution steps

1. **Verify** it's a MOBILE Stitch design
2. **Data layer** — create `src/data/mockData.ts` from the static content in the design
3. **Tokens** — create `src/theme/tokens.ts` from extracted colors, and `useTheme.ts`
4. **Components** — convert each visual section to a component using the mapping rules above
5. **Screen** — compose components in the Expo Router screen file (`app/(tabs)/index.tsx`)
6. **Verify** — run `npx expo start` and test on both iOS Simulator and Android Emulator

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `StyleSheet.create` type error | Import `StyleSheet` from `'react-native'` |
| Text outside `<Text>` error | Every string must be inside `<Text>` — even `{' '}` spaces |
| Flex layout looks wrong | RN defaults to `flexDirection:'column'` — explicit is safer |
| Image not showing | Requires explicit `width` and `height` on the style |
| Keyboard pushes layout up | Use `KeyboardAvoidingView` with `behavior='padding'` on iOS |
| Bottom safe area overlap | Use `useSafeAreaInsets()` from `react-native-safe-area-context` |

## References

- `resources/component-template.tsx` — Boilerplate RN component
- `resources/architecture-checklist.md` — Pre-ship checklist
- `scripts/fetch-stitch.sh` — Reliable GCS HTML downloader
