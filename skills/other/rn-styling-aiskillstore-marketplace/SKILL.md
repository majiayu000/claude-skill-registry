---
name: rn-styling
description: Styling patterns for React Native with NativeWind and BrandColors. Use when working with styles, themes, colors, responsive layouts, or platform-specific UI in Expo/React Native.
---

# React Native Styling

## Problem Statement

React Native styling differs fundamentally from web CSS. NativeWind bridges the gap but has its own rules. This codebase uses a hybrid approach: BrandColors for semantic colors, NativeWind for layout utilities.

---

## Pattern: BrandColors vs NativeWind Classes

**Rule:** Use BrandColors for semantic colors, NativeWind for layout/spacing.

```typescript
// ✅ CORRECT: Hybrid approach
<View className="flex-1 p-4 rounded-lg" style={{ backgroundColor: BrandColors.background }}>
  <Text className="text-lg font-semibold" style={{ color: BrandColors.textPrimary }}>
    Title
  </Text>
</View>

// ❌ WRONG: Hardcoded hex colors (violation scanner blocks this)
<View className="flex-1 p-4 bg-[#1a1a2e]">

// ❌ WRONG: NativeWind color classes for brand colors
<View className="flex-1 p-4 bg-blue-500">

// ✅ ACCEPTABLE: NativeWind brand aliases (if configured)
<View className="flex-1 p-4 bg-brand-blue">
```

**When to use which:**

| Use Case | Approach |
|----------|----------|
| Brand colors (primary, secondary) | `BrandColors.primary` |
| Background colors | `BrandColors.background` |
| Text colors | `BrandColors.textPrimary`, `textSecondary` |
| Layout (flex, padding, margin) | NativeWind classes |
| Borders, radius | NativeWind classes |
| Shadows | Style object (NativeWind shadows limited on iOS) |

---

## Pattern: Theme-Aware Colors

**Problem:** Supporting light/dark mode with BrandColors.

```typescript
// BrandColors.ts exports both themes
import { BrandColors, BrandColorsDark } from '@/constants/BrandColors';

// Hook for current theme colors
import { useColorScheme } from 'react-native';

function useThemeColors() {
  const colorScheme = useColorScheme();
  return colorScheme === 'dark' ? BrandColorsDark : BrandColors;
}

// Component usage
function ThemedCard({ title }: { title: string }) {
  const colors = useThemeColors();
  
  return (
    <View 
      className="p-4 rounded-lg"
      style={{ backgroundColor: colors.cardBackground }}
    >
      <Text style={{ color: colors.textPrimary }}>{title}</Text>
    </View>
  );
}
```

---

## Pattern: NativeWind Class Ordering

**Problem:** Unlike web CSS, React Native doesn't cascade. Last class wins for conflicting properties.

```typescript
// Class order matters!
<View className="p-4 p-2" />  // p-2 wins (last)
<View className="p-2 p-4" />  // p-4 wins (last)

// Conditional classes - be explicit
<View className={`p-4 ${isCompact ? 'p-2' : ''}`} />  
// If isCompact: "p-4 p-2" → p-2 wins ✅

// Merging className props
interface Props {
  className?: string;
}

function Card({ className }: Props) {
  // Parent classes override defaults (they come last)
  return <View className={`p-4 rounded-lg ${className ?? ''}`} />;
}

// Usage: <Card className="p-8" />  → p-8 wins over p-4
```

---

## Pattern: Platform-Specific Styles

```typescript
import { Platform, StyleSheet } from 'react-native';

// Option 1: Platform.select
const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
  }),
});

// Option 2: Platform.OS check
<View style={Platform.OS === 'ios' ? styles.iosShadow : styles.androidShadow} />

// Option 3: NativeWind platform prefixes
<View className="ios:pt-12 android:pt-8" />
```

---

## Pattern: Safe Area Handling

```typescript
import { SafeAreaView } from 'react-native-safe-area-context';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

// Option 1: SafeAreaView wrapper (simplest)
function Screen() {
  return (
    <SafeAreaView className="flex-1" edges={['top', 'bottom']}>
      <Content />
    </SafeAreaView>
  );
}

// Option 2: Manual insets (more control)
function Screen() {
  const insets = useSafeAreaInsets();
  
  return (
    <View 
      className="flex-1"
      style={{ paddingTop: insets.top, paddingBottom: insets.bottom }}
    >
      <Content />
    </View>
  );
}

// Option 3: NativeWind safe area utilities (if configured)
<View className="flex-1 pt-safe pb-safe">
```

---

## Pattern: Keyboard Avoiding

```typescript
import { KeyboardAvoidingView, Platform } from 'react-native';

function FormScreen() {
  return (
    <KeyboardAvoidingView
      className="flex-1"
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 64 : 0} // Adjust for header
    >
      <ScrollView className="flex-1">
        <TextInput />
        <TextInput />
        <SubmitButton />
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
```

---

## Pattern: Responsive Breakpoints

**Note:** NativeWind v2 breakpoints differ from web Tailwind.

```typescript
// NativeWind v2 breakpoints (based on window width)
// sm: 640px, md: 768px, lg: 1024px, xl: 1280px

// Responsive padding
<View className="p-2 sm:p-4 md:p-6" />

// Responsive flex direction
<View className="flex-col sm:flex-row" />

// Check screen size programmatically
import { useWindowDimensions } from 'react-native';

function ResponsiveLayout() {
  const { width } = useWindowDimensions();
  const isTablet = width >= 768;
  
  return isTablet ? <TabletLayout /> : <PhoneLayout />;
}
```

---

## Pattern: Animated Styles

**Problem:** Avoiding re-renders with Animated values.

```typescript
import { Animated } from 'react-native';

function FadeInCard() {
  // useRef to persist Animated.Value across renders
  const fadeAnim = useRef(new Animated.Value(0)).current;
  
  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true, // Always use when animating opacity/transform
    }).start();
  }, []);
  
  return (
    <Animated.View 
      className="p-4 rounded-lg"
      style={[
        { backgroundColor: BrandColors.cardBackground },
        { opacity: fadeAnim }, // Animated style in array
      ]}
    >
      <Text>Content</Text>
    </Animated.View>
  );
}
```

**Style arrays:** Combine static + animated styles.

```typescript
// ✅ CORRECT: Style array
style={[styles.card, { opacity: fadeAnim }]}

// ❌ WRONG: Spread (creates new object each render)
style={{ ...styles.card, opacity: fadeAnim }}
```

---

## Pattern: StyleSheet vs Inline

```typescript
// Use StyleSheet for:
// - Complex styles reused across renders
// - Styles with many properties
// - Performance-critical components

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: BrandColors.cardBackground,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
});

// Use inline/NativeWind for:
// - Simple layout utilities
// - One-off styles
// - Conditional styles

<View className="flex-1 p-4" />
<View style={{ marginTop: dynamicValue }} />
```

---

## BrandColors Pattern

Create a centralized color constants file:

```typescript
// constants/BrandColors.ts
export const BrandColors = {
  primary: '#...',
  secondary: '#...',
  background: '#...',
  cardBackground: '#...',
  textPrimary: '#...',
  textSecondary: '#...',
  // ... etc
};

export const BrandColorsDark = {
  // Dark mode variants
};
```

### Recommended: Violation Scanner

Consider adding a violation scanner to block:
- Hardcoded hex colors (except allowed exceptions)
- Direct color strings

### NativeWind Notes

If using NativeWind v2 (not v4), note these differences:
- `className` prop on RN components
- Limited web Tailwind parity
- Some utilities unsupported

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Color not applying | Check BrandColors import, verify theme context |
| NativeWind class ignored | Not all Tailwind utilities work - check v2 docs |
| Shadow not showing (iOS) | Use StyleSheet with shadowColor/Offset/Opacity/Radius |
| Shadow not showing (Android) | Use `elevation` property |
| Safe area not respected | Wrap in SafeAreaView or use insets |
| Style flicker on mount | Use Animated for transitions |

---

## Recommended File Structure

```
constants/
  BrandColors.ts       # Color definitions
  designSystem.ts      # Spacing, typography scales
components/
  ui/Card.tsx          # Example hybrid styling
app/
  _layout.tsx          # Theme provider setup
```
