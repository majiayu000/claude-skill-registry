---
name: expo-glass-effect
description: Guide for using expo-glass-effect to create iOS native liquid glass UI effects. Apply when implementing glass effect UI components, cards, or surfaces on iOS.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Expo Glass Effect

Guide for using `expo-glass-effect` to create iOS native liquid glass UI effects.

## Overview

- **Platform**: iOS 26+ only (falls back to regular `View` on unsupported platforms)
- **Native API**: Uses `UIVisualEffectView` under the hood
- **Package**: `expo-glass-effect`

## Installation

```bash
npx expo install expo-glass-effect
```

## Core Components

### GlassView

Primary component for rendering glass effect surfaces.

```tsx
import { GlassView } from 'expo-glass-effect';

<GlassView
  style={styles.glass}
  glassEffectStyle="regular"  // 'regular' | 'clear'
  isInteractive={false}       // Enable interactive glass effect
  tintColor="#ffffff"         // Optional tint overlay
/>
```

**Props:**
- `glassEffectStyle`: `'regular'` (default) or `'clear'`
- `isInteractive`: Boolean for interactive behavior (default: `false`)
- `tintColor`: Optional color string for tinting the glass
- All standard `View` props (style, children, etc.)

### GlassContainer

Wrapper for combining multiple glass views with merged effects.

```tsx
import { GlassContainer, GlassView } from 'expo-glass-effect';

<GlassContainer spacing={10} style={styles.container}>
  <GlassView style={styles.glass1} isInteractive />
  <GlassView style={styles.glass2} />
  <GlassView style={styles.glass3} />
</GlassContainer>
```

**Props:**
- `spacing`: Distance (number) at which glass elements start merging effects
- All standard `View` props

## Utility Functions

### isLiquidGlassAvailable()

Check if glass components are available (validates system version, compiler version, Info.plist settings).

```tsx
import { isLiquidGlassAvailable } from 'expo-glass-effect';

if (isLiquidGlassAvailable()) {
  // Render GlassView
} else {
  // Render fallback UI
}
```

**Note**: This checks component availability, not user accessibility settings. Use `AccessibilityInfo.isReduceTransparencyEnabled()` to check if user disabled transparency.

### isGlassEffectAPIAvailable()

Runtime check for Glass Effect API availability on device (important for iOS 26 beta compatibility).

```tsx
import { isGlassEffectAPIAvailable } from 'expo-glass-effect';

if (isGlassEffectAPIAvailable()) {
  // Safe to use GlassView
}
```

## Common Patterns

### Basic Glass Card

```tsx
import { StyleSheet, View, Image, Text } from 'react-native';
import { GlassView } from 'expo-glass-effect';

export default function GlassCard() {
  return (
    <View style={styles.container}>
      <Image
        style={styles.background}
        source={{ uri: 'https://example.com/image.jpg' }}
      />
      <GlassView style={styles.card}>
        <Text style={styles.text}>Glass Effect Card</Text>
      </GlassView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  background: {
    ...StyleSheet.absoluteFill,
  },
  card: {
    position: 'absolute',
    top: 100,
    left: 50,
    width: 200,
    height: 100,
    borderRadius: 12,
    padding: 20,
  },
});
```

### Merged Glass Elements

```tsx
import { GlassContainer, GlassView } from 'expo-glass-effect';

<GlassContainer spacing={10} style={styles.row}>
  <GlassView style={styles.circle1} isInteractive />
  <GlassView style={styles.circle2} />
  <GlassView style={styles.circle3} />
</GlassContainer>
```

### Conditional Rendering with Fallback

```tsx
import { isLiquidGlassAvailable, GlassView } from 'expo-glass-effect';
import { View } from 'react-native';

function Card({ children, style }) {
  const GlassComponent = isLiquidGlassAvailable() ? GlassView : View;

  return (
    <GlassComponent style={[styles.card, style]}>
      {children}
    </GlassComponent>
  );
}
```

## Known Issues & Limitations

### 1. isInteractive Cannot Change Dynamically

```tsx
// ❌ BAD - Won't work after initial render
const [interactive, setInteractive] = useState(false);
<GlassView isInteractive={interactive} />

// ✅ GOOD - Remount with different key
const [interactive, setInteractive] = useState(false);
<GlassView key={interactive ? 'interactive' : 'static'} isInteractive={interactive} />
```

### 2. Opacity Issues

**Avoid `opacity < 1`** on `GlassView` or parent views - causes rendering issues.

```tsx
// ❌ BAD
<View style={{ opacity: 0.8 }}>
  <GlassView />
</View>

// ✅ GOOD - Use tintColor instead
<GlassView tintColor="rgba(255, 255, 255, 0.8)" />
```

### 3. Platform Support

Always wrap in platform checks or use fallback components for cross-platform apps:

```tsx
import { Platform } from 'react-native';
import { isLiquidGlassAvailable, GlassView } from 'expo-glass-effect';

const useGlass = Platform.OS === 'ios' && isLiquidGlassAvailable();
```

## Styling Best Practices

1. **Always use `position: 'absolute'`** for layering over background content
2. **Use `borderRadius`** to create rounded glass surfaces
3. **Layer backgrounds** using `StyleSheet.absoluteFill` for full coverage
4. **Avoid shadows** - glass effect provides natural depth
5. **Use `padding`** for content spacing within glass views

## Accessibility

Check user preference for reduced transparency:

```tsx
import { AccessibilityInfo } from 'react-native';
import { isLiquidGlassAvailable, GlassView } from 'expo-glass-effect';

const [reduceTransparency, setReduceTransparency] = useState(false);

useEffect(() => {
  AccessibilityInfo.isReduceTransparencyEnabled().then(setReduceTransparency);
}, []);

const shouldUseGlass = isLiquidGlassAvailable() && !reduceTransparency;
```

## References

- [Expo Glass Effect Docs](https://docs.expo.dev/versions/latest/sdk/glass-effect/)
- [Apple UIVisualEffectView](https://developer.apple.com/documentation/uikit/uivisualeffectview)
- [GitHub Issue #41024](https://github.com/expo/expo/issues/41024) - Opacity rendering bug
- [GitHub Issue #40911](https://github.com/expo/expo/issues/40911) - iOS 26 beta API availability
