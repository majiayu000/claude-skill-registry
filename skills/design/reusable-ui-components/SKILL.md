---
name: reusable-ui-components
description: Guidelines for creating reusable, portable UI components with native-first design, compound patterns, and accessibility
---

# Creating Reusable UI Components for Expo Router

This guide covers building production-quality, portable UI components inspired by shadcn/ui, Base UI, Radix, and Konsta UI. Components follow iOS San Francisco design guidelines with liquid glass aesthetics and prioritize native primitives with graceful fallbacks.

## Philosophy

### Core Principles

1. **Portable & Copy-Paste Ready** - Components should be self-contained and easy to copy between projects
2. **Native-First** - Always check for Expo Router primitives before building custom solutions
3. **iOS Design Language** - Use San Francisco style guide as the baseline for all platforms
4. **Compound Components** - Break complex components into composable sub-components
5. **CSS Variables for Customization** - Use design tokens for theming, not hardcoded values
6. **Accessibility Built-In** - Keyboard handling, safe areas, and screen reader support by default

### Inspiration Sources

| Library | Learn From |
|---------|-----------|
| **shadcn/ui** | Component structure, copy-paste architecture |
| **Radix UI** | Compound component patterns, accessibility primitives |
| **Base UI** | Headless component APIs, composition patterns |
| **Konsta UI** | iOS liquid glass aesthetics, platform-adaptive styling |

## Component File Structure

```
src/components/ui/
├── button.tsx          # Default (shared) implementation
├── button.ios.tsx      # iOS-specific overrides (optional)
├── button.web.tsx      # Web-specific overrides (optional)
└── button.android.tsx  # Android-specific overrides (optional)
```

**Metro Resolution Priority:**
1. `.ios.tsx` / `.android.tsx` / `.web.tsx` (platform-specific)
2. `.native.tsx` (iOS + Android)
3. `.tsx` (fallback for all platforms)

## Design Tokens & CSS Variables

### Global Theme Variables

Define customizable design tokens in `src/global.css`:

```css
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";

/* Import Apple system colors */
@import "./css/sf.css";

@layer theme {
  @theme {
    /* Typography Scale */
    --font-sans: system-ui;
    --font-mono: ui-monospace;
    --font-rounded: ui-rounded;

    /* Component Tokens */
    --component-radius: 12px;
    --component-radius-lg: 16px;
    --component-radius-full: 9999px;

    /* Spacing Scale */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 12px;
    --spacing-lg: 16px;
    --spacing-xl: 24px;

    /* Animation */
    --transition-fast: 150ms;
    --transition-normal: 200ms;
    --transition-slow: 300ms;
  }
}

/* Platform-specific overrides */
@media ios {
  :root {
    --font-sans: system-ui;
    --font-rounded: ui-rounded;
    --component-radius: 10px;
  }
}

@media android {
  :root {
    --font-sans: normal;
    --font-rounded: normal;
    --component-radius: 8px;
  }
}
```

### Apple System Colors

Create platform-adaptive colors in `src/css/sf.css`:

```css
@layer base {
  html {
    color-scheme: light dark;
  }
}

:root {
  /* Primary Colors */
  --sf-blue: light-dark(rgb(0 122 255), rgb(10 132 255));
  --sf-green: light-dark(rgb(52 199 89), rgb(48 209 89));
  --sf-red: light-dark(rgb(255 59 48), rgb(255 69 58));
  --sf-orange: light-dark(rgb(255 149 0), rgb(255 159 10));
  --sf-yellow: light-dark(rgb(255 204 0), rgb(255 214 10));
  --sf-purple: light-dark(rgb(175 82 222), rgb(191 90 242));
  --sf-pink: light-dark(rgb(255 45 85), rgb(255 55 95));

  /* Gray Scale */
  --sf-gray: light-dark(rgb(142 142 147), rgb(142 142 147));
  --sf-gray-2: light-dark(rgb(174 174 178), rgb(99 99 102));
  --sf-gray-3: light-dark(rgb(199 199 204), rgb(72 72 74));
  --sf-gray-4: light-dark(rgb(209 209 214), rgb(58 58 60));
  --sf-gray-5: light-dark(rgb(229 229 234), rgb(44 44 46));
  --sf-gray-6: light-dark(rgb(242 242 247), rgb(28 28 30));

  /* Text Colors */
  --sf-text: light-dark(rgb(0 0 0), rgb(255 255 255));
  --sf-text-2: light-dark(rgb(60 60 67 / 0.6), rgb(235 235 245 / 0.6));
  --sf-text-3: light-dark(rgb(60 60 67 / 0.3), rgb(235 235 245 / 0.3));
  --sf-text-placeholder: light-dark(rgb(60 60 67 / 0.3), rgb(235 235 245 / 0.3));

  /* Background Colors */
  --sf-bg: light-dark(rgb(255 255 255), rgb(0 0 0));
  --sf-bg-2: light-dark(rgb(242 242 247), rgb(28 28 30));
  --sf-grouped-bg: light-dark(rgb(242 242 247), rgb(0 0 0));
  --sf-grouped-bg-2: light-dark(rgb(255 255 255), rgb(28 28 30));

  /* Border & Fill */
  --sf-border: light-dark(rgb(60 60 67 / 0.12), rgb(84 84 88 / 0.65));
  --sf-fill: light-dark(rgb(120 120 128 / 0.2), rgb(120 120 128 / 0.32));

  /* Link Color */
  --sf-link: var(--sf-blue);
}

/* iOS: Use native platform colors */
@media ios {
  :root {
    --sf-blue: platformColor(systemBlue);
    --sf-green: platformColor(systemGreen);
    --sf-red: platformColor(systemRed);
    --sf-orange: platformColor(systemOrange);
    --sf-yellow: platformColor(systemYellow);
    --sf-purple: platformColor(systemPurple);
    --sf-pink: platformColor(systemPink);
    --sf-gray: platformColor(systemGray);
    --sf-gray-2: platformColor(systemGray2);
    --sf-gray-3: platformColor(systemGray3);
    --sf-gray-4: platformColor(systemGray4);
    --sf-gray-5: platformColor(systemGray5);
    --sf-gray-6: platformColor(systemGray6);
    --sf-text: platformColor(label);
    --sf-text-2: platformColor(secondaryLabel);
    --sf-text-3: platformColor(tertiaryLabel);
    --sf-text-placeholder: platformColor(placeholderText);
    --sf-bg: platformColor(systemBackground);
    --sf-bg-2: platformColor(secondarySystemBackground);
    --sf-grouped-bg: platformColor(systemGroupedBackground);
    --sf-grouped-bg-2: platformColor(secondarySystemGroupedBackground);
    --sf-border: platformColor(separator);
    --sf-fill: platformColor(tertiarySystemFill);
    --sf-link: platformColor(link);
  }
}

/* Register as Tailwind theme colors */
@layer theme {
  @theme {
    --color-sf-blue: var(--sf-blue);
    --color-sf-green: var(--sf-green);
    --color-sf-red: var(--sf-red);
    --color-sf-orange: var(--sf-orange);
    --color-sf-yellow: var(--sf-yellow);
    --color-sf-purple: var(--sf-purple);
    --color-sf-pink: var(--sf-pink);
    --color-sf-gray: var(--sf-gray);
    --color-sf-gray-2: var(--sf-gray-2);
    --color-sf-gray-3: var(--sf-gray-3);
    --color-sf-gray-4: var(--sf-gray-4);
    --color-sf-gray-5: var(--sf-gray-5);
    --color-sf-gray-6: var(--sf-gray-6);
    --color-sf-text: var(--sf-text);
    --color-sf-text-2: var(--sf-text-2);
    --color-sf-text-3: var(--sf-text-3);
    --color-sf-text-placeholder: var(--sf-text-placeholder);
    --color-sf-bg: var(--sf-bg);
    --color-sf-bg-2: var(--sf-bg-2);
    --color-sf-grouped-bg: var(--sf-grouped-bg);
    --color-sf-grouped-bg-2: var(--sf-grouped-bg-2);
    --color-sf-border: var(--sf-border);
    --color-sf-fill: var(--sf-fill);
    --color-sf-link: var(--sf-link);
  }
}
```

### Accessing CSS Variables in JavaScript

```tsx
import { useCSSVariable } from "@/tw";

function MyComponent() {
  const primaryColor = useCSSVariable("--sf-blue");
  const borderColor = useCSSVariable("--sf-border");

  return (
    <View style={{ borderColor }}>
      <Text style={{ color: primaryColor }}>Hello</Text>
    </View>
  );
}
```

## Compound Component Pattern

Use compound components for complex, multi-element UI. This provides flexibility while maintaining cohesive behavior.

### Template Structure

```tsx
"use client";

import React, { createContext, use } from "react";
import { View, Text, Pressable } from "@/tw";
import { cn } from "@/lib/utils";
import type { ViewProps, TextProps } from "react-native";

// 1. Define Context for shared state
interface ComponentContextValue {
  variant: "default" | "outline" | "ghost";
  size: "sm" | "md" | "lg";
  disabled?: boolean;
}

const ComponentContext = createContext<ComponentContextValue | null>(null);

function useComponentContext() {
  const context = use(ComponentContext);
  if (!context) {
    throw new Error("Component parts must be used within Component.Root");
  }
  return context;
}

// 2. Root component provides context
interface RootProps extends ViewProps {
  variant?: ComponentContextValue["variant"];
  size?: ComponentContextValue["size"];
  disabled?: boolean;
}

function Root({
  variant = "default",
  size = "md",
  disabled,
  children,
  className,
  ...props
}: RootProps) {
  return (
    <ComponentContext value={{ variant, size, disabled }}>
      <View
        {...props}
        className={cn(
          "flex-row items-center",
          disabled && "opacity-50",
          className
        )}
      >
        {children}
      </View>
    </ComponentContext>
  );
}

// 3. Sub-components consume context
function Label({ className, ...props }: TextProps) {
  const { size } = useComponentContext();

  return (
    <Text
      {...props}
      className={cn(
        "text-sf-text",
        size === "sm" && "text-sm",
        size === "md" && "text-base",
        size === "lg" && "text-lg",
        className
      )}
    />
  );
}

function Icon({ className, ...props }: ViewProps) {
  const { size } = useComponentContext();

  const sizeClass = {
    sm: "w-4 h-4",
    md: "w-5 h-5",
    lg: "w-6 h-6",
  }[size];

  return (
    <View {...props} className={cn(sizeClass, className)} />
  );
}

// 4. Export as compound component
export const Component = {
  Root,
  Label,
  Icon,
};

// 5. Convenience export for simple usage
export function SimpleComponent(props: RootProps & { label: string }) {
  const { label, ...rootProps } = props;
  return (
    <Component.Root {...rootProps}>
      <Component.Label>{label}</Component.Label>
    </Component.Root>
  );
}
```

## Native-First Component Development

### Check for Expo Router Primitives First

Before building custom components, check if Expo Router or Expo provides a native primitive:

| Component Need | Check First |
|----------------|-------------|
| Navigation Stack | `expo-router` Stack |
| Tab Navigation | `expo-router` Tabs |
| Modals/Sheets | `presentation: "modal"` or `presentation: "formSheet"` |
| Links | `expo-router` Link |
| Icons | `expo-symbols` (SF Symbols) |
| Date Picker | `@react-native-community/datetimepicker` |
| Segmented Control | `@react-native-segmented-control/segmented-control` |
| Blur Effects | `expo-blur` or `expo-glass-effect` |
| Haptics | `expo-haptics` |
| Safe Areas | `react-native-safe-area-context` |

### Platform Detection

```tsx
// Check current platform
if (process.env.EXPO_OS === "ios") {
  // iOS-specific behavior
} else if (process.env.EXPO_OS === "android") {
  // Android-specific behavior
} else if (process.env.EXPO_OS === "web") {
  // Web-specific behavior
}

// Check for specific features
import { isLiquidGlassAvailable } from "expo-glass-effect";
const GLASS = isLiquidGlassAvailable(); // iOS 26+ liquid glass
```

### Platform-Specific File Example: Switch

**switch.tsx** (default - re-exports native):
```tsx
export { Switch, type SwitchProps } from "react-native";
```

**switch.web.tsx** (web - iOS-styled custom):
```tsx
"use client";

import { useState, useRef, useEffect } from "react";
import {
  View,
  Animated,
  PanResponder,
  StyleSheet,
  Pressable,
} from "react-native";

export type SwitchProps = {
  value?: boolean;
  onValueChange?: (value: boolean) => void;
  disabled?: boolean;
  thumbColor?: string;
  trackColor?: { true: string; false: string };
  ios_backgroundColor?: string;
};

export function Switch({
  value = false,
  onValueChange,
  disabled = false,
  thumbColor = "#fff",
  trackColor = { true: "#34C759", false: "#E9E9EA" },
  ios_backgroundColor,
}: SwitchProps) {
  const [isOn, setIsOn] = useState(value);
  const animatedValue = useRef(new Animated.Value(value ? 1 : 0)).current;

  useEffect(() => {
    setIsOn(value);
    Animated.spring(animatedValue, {
      toValue: value ? 1 : 0,
      useNativeDriver: false,
      friction: 8,
      tension: 40,
    }).start();
  }, [value, animatedValue]);

  const toggle = () => {
    if (disabled) return;
    const newValue = !isOn;
    setIsOn(newValue);
    onValueChange?.(newValue);
  };

  const translateX = animatedValue.interpolate({
    inputRange: [0, 1],
    outputRange: [2, 22],
  });

  const bgColor = animatedValue.interpolate({
    inputRange: [0, 1],
    outputRange: [
      ios_backgroundColor || trackColor.false,
      trackColor.true,
    ],
  });

  return (
    <Pressable onPress={toggle} disabled={disabled}>
      <Animated.View
        style={[
          styles.track,
          { backgroundColor: bgColor },
          disabled && styles.disabled,
        ]}
      >
        <Animated.View
          style={[
            styles.thumb,
            { backgroundColor: thumbColor, transform: [{ translateX }] },
          ]}
        />
      </Animated.View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  track: {
    width: 51,
    height: 31,
    borderRadius: 15.5,
    justifyContent: "center",
  },
  thumb: {
    width: 27,
    height: 27,
    borderRadius: 13.5,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  disabled: {
    opacity: 0.5,
  },
});
```

## Accessibility Patterns

### Keyboard Avoidance

For forms with text input, proper keyboard handling is critical:

```tsx
import {
  useReanimatedKeyboardAnimation,
  useKeyboardHandler,
} from "react-native-keyboard-controller";
import { useAnimatedStyle } from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";

function KeyboardAwareForm({ children }: { children: React.ReactNode }) {
  const { bottom } = useSafeAreaInsets();
  const { height, progress } = useReanimatedKeyboardAnimation();

  const animatedStyle = useAnimatedStyle(() => ({
    paddingBottom: Math.max(bottom, Math.abs(height.value)),
  }));

  return (
    <Animated.View style={[{ flex: 1 }, animatedStyle]}>
      {children}
    </Animated.View>
  );
}
```

### Safe Area Handling

Always account for safe areas on notched devices:

```tsx
import { useSafeAreaInsets } from "react-native-safe-area-context";

function SafeContainer({ children }: { children: React.ReactNode }) {
  const { top, bottom, left, right } = useSafeAreaInsets();

  return (
    <View
      style={{
        flex: 1,
        paddingTop: top,
        paddingBottom: bottom,
        paddingLeft: left,
        paddingRight: right,
      }}
    >
      {children}
    </View>
  );
}
```

### Form Accessibility Pattern

```tsx
import { View, Text, TextInput } from "@/tw";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { KeyboardAwareScrollView } from "react-native-keyboard-controller";

interface FormFieldProps {
  label: string;
  hint?: string;
  error?: string;
  children: React.ReactNode;
}

function FormField({ label, hint, error, children }: FormFieldProps) {
  return (
    <View className="gap-1">
      <Text
        className="text-sf-text-2 text-sm font-medium"
        accessibilityRole="text"
      >
        {label}
      </Text>
      {children}
      {hint && !error && (
        <Text className="text-sf-text-3 text-xs">{hint}</Text>
      )}
      {error && (
        <Text
          className="text-sf-red text-xs"
          accessibilityRole="alert"
        >
          {error}
        </Text>
      )}
    </View>
  );
}

function AccessibleForm() {
  const { bottom } = useSafeAreaInsets();

  return (
    <KeyboardAwareScrollView
      contentContainerStyle={{
        padding: 16,
        paddingBottom: bottom + 16,
        gap: 16,
      }}
      keyboardShouldPersistTaps="handled"
    >
      <FormField label="Email" hint="We'll never share your email">
        <TextInput
          className="bg-sf-fill rounded-xl px-4 py-3 text-sf-text"
          placeholder="you@example.com"
          keyboardType="email-address"
          autoCapitalize="none"
          autoComplete="email"
          textContentType="emailAddress"
          accessibilityLabel="Email address"
        />
      </FormField>

      <FormField label="Password">
        <TextInput
          className="bg-sf-fill rounded-xl px-4 py-3 text-sf-text"
          placeholder="••••••••"
          secureTextEntry
          autoComplete="password"
          textContentType="password"
          accessibilityLabel="Password"
        />
      </FormField>
    </KeyboardAwareScrollView>
  );
}
```

## iOS Liquid Glass Styling

### Detecting Liquid Glass Support

```tsx
import { isLiquidGlassAvailable } from "expo-glass-effect";

const GLASS = isLiquidGlassAvailable();

const HEADER_OPTIONS = GLASS
  ? {
      headerTransparent: true,
      headerShadowVisible: false,
      headerBlurEffect: "none",
    }
  : {
      headerTransparent: true,
      headerBlurEffect: "systemChromeMaterial",
      headerShadowVisible: true,
    };
```

### Tab Bar with Glass Effect

```tsx
import { BlurView } from "expo-blur";

function GlassTabBarBackground() {
  return (
    <BlurView
      intensity={100}
      tint="systemChromeMaterial"
      style={StyleSheet.absoluteFill}
    />
  );
}

// Usage in Tabs
const TAB_OPTIONS =
  process.env.EXPO_OS === "ios"
    ? {
        tabBarBackground: GlassTabBarBackground,
        tabBarStyle: { position: "absolute" },
      }
    : {};
```

### Glass Card Component

```tsx
import { BlurView } from "expo-blur";
import { View } from "@/tw";
import { cn } from "@/lib/utils";

interface GlassCardProps extends React.ComponentProps<typeof View> {
  intensity?: number;
}

function GlassCard({
  intensity = 50,
  className,
  children,
  ...props
}: GlassCardProps) {
  if (process.env.EXPO_OS !== "ios") {
    // Fallback for non-iOS
    return (
      <View
        {...props}
        className={cn(
          "bg-sf-bg-2/80 rounded-2xl overflow-hidden",
          className
        )}
      >
        {children}
      </View>
    );
  }

  return (
    <View
      {...props}
      className={cn("rounded-2xl overflow-hidden", className)}
    >
      <BlurView
        intensity={intensity}
        tint="systemChromeMaterial"
        style={StyleSheet.absoluteFill}
      />
      <View className="relative">{children}</View>
    </View>
  );
}
```

## Form Components Pattern

The `Form` compound component demonstrates all principles together:

```tsx
"use client";

import React, { createContext, use } from "react";
import { View, Text, TextInput, ScrollView, TouchableHighlight } from "@/tw";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { cn } from "@/lib/utils";
import { useCSSVariable } from "@/tw";

// Context for form styling
const FormContext = createContext<{
  listStyle: "grouped" | "inset";
  sheet?: boolean;
}>({ listStyle: "inset" });

// List wrapper with pull-to-refresh
function List({
  children,
  listStyle = "inset",
  sheet,
  ...props
}: React.ComponentProps<typeof ScrollView> & {
  listStyle?: "grouped" | "inset";
  sheet?: boolean;
}) {
  const { bottom } = useSafeAreaInsets();

  return (
    <FormContext value={{ listStyle, sheet }}>
      <ScrollView
        contentContainerStyle={{ paddingVertical: 16, gap: 24 }}
        contentInsetAdjustmentBehavior="automatic"
        scrollIndicatorInsets={{ bottom }}
        className={cn(
          sheet ? "bg-transparent" : "bg-sf-grouped-bg",
          props.className
        )}
        {...props}
      >
        {children}
      </ScrollView>
    </FormContext>
  );
}

// Section groups related items
function Section({
  children,
  title,
  footer,
  ...props
}: React.ComponentProps<typeof View> & {
  title?: string;
  footer?: string;
}) {
  const { listStyle, sheet } = use(FormContext);
  const isInset = listStyle === "inset";

  return (
    <View style={{ paddingHorizontal: isInset ? 16 : 0 }} {...props}>
      {title && (
        <Text className="uppercase text-sf-text-2 text-sm px-5 pb-2">
          {title}
        </Text>
      )}
      <View
        className={cn(
          sheet ? "bg-sf-bg-2" : "bg-sf-grouped-bg-2",
          isInset ? "rounded-xl overflow-hidden" : "border-y border-sf-border"
        )}
      >
        {React.Children.map(children, (child, index) => (
          <>
            {child}
            {index < React.Children.count(children) - 1 && (
              <View className="border-b border-sf-border ml-4" />
            )}
          </>
        ))}
      </View>
      {footer && (
        <Text className="text-sf-text-2 text-sm px-5 pt-2">{footer}</Text>
      )}
    </View>
  );
}

// Individual form item with optional navigation
function Item({
  children,
  onPress,
  href,
  ...props
}: React.ComponentProps<typeof View> & {
  onPress?: () => void;
  href?: string;
}) {
  const underlayColor = useCSSVariable("--sf-gray-4");

  const content = (
    <View className="flex-row items-center px-4 py-3 min-h-[44px]" {...props}>
      {children}
    </View>
  );

  if (!onPress && !href) return content;

  return (
    <TouchableHighlight
      onPress={onPress}
      underlayColor={underlayColor}
      className="web:hover:bg-sf-fill web:transition-colors"
    >
      {content}
    </TouchableHighlight>
  );
}

// Text label
function Label({ className, ...props }: React.ComponentProps<typeof Text>) {
  return (
    <Text
      {...props}
      className={cn("text-sf-text text-base flex-1", className)}
    />
  );
}

// Hint/value on the right
function Hint({ className, ...props }: React.ComponentProps<typeof Text>) {
  return (
    <Text
      {...props}
      className={cn("text-sf-text-2 text-base", className)}
    />
  );
}

// Export compound component
export const Form = {
  List,
  Section,
  Item,
  Label,
  Hint,
};
```

### Usage

```tsx
<Form.List>
  <Form.Section title="Account" footer="Your account settings">
    <Form.Item href="/profile">
      <Form.Label>Profile</Form.Label>
      <Form.Hint>John Doe</Form.Hint>
      <ChevronRight />
    </Form.Item>
    <Form.Item href="/email">
      <Form.Label>Email</Form.Label>
      <Form.Hint>john@example.com</Form.Hint>
      <ChevronRight />
    </Form.Item>
  </Form.Section>

  <Form.Section title="Preferences">
    <Form.Item>
      <Form.Label>Dark Mode</Form.Label>
      <Switch value={darkMode} onValueChange={setDarkMode} />
    </Form.Item>
  </Form.Section>
</Form.List>
```

## Haptic Feedback

### Platform-Safe Haptics

**lib/haptics.ts** (native):
```tsx
import * as Haptics from "expo-haptics";

export const haptics = {
  light: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light),
  medium: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium),
  heavy: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy),
  success: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success),
  warning: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning),
  error: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error),
  selection: () => Haptics.selectionAsync(),
};
```

**lib/haptics.web.ts** (web - no-op):
```tsx
export const haptics = {
  light: () => {},
  medium: () => {},
  heavy: () => {},
  success: () => {},
  warning: () => {},
  error: () => {},
  selection: () => {},
};
```

### Usage in Components

```tsx
import { haptics } from "@/lib/haptics";

function HapticButton({ onPress, children }) {
  const handlePress = () => {
    haptics.light();
    onPress?.();
  };

  return <Pressable onPress={handlePress}>{children}</Pressable>;
}
```

## Icon System

### SF Symbol Icons with Fallbacks

```tsx
import { SymbolView, SymbolWeight } from "expo-symbols";
import { MaterialIcons } from "@expo/vector-icons";

// Map SF Symbol names to Material Icons
const ICON_MAPPING: Record<string, string> = {
  "house.fill": "home",
  "gear": "settings",
  "person.fill": "person",
  "magnifyingglass": "search",
  "chevron.right": "chevron_right",
};

interface IconProps {
  name: string;
  size?: number;
  color?: string;
  weight?: SymbolWeight;
}

export function Icon({ name, size = 24, color, weight }: IconProps) {
  if (process.env.EXPO_OS === "ios") {
    return (
      <SymbolView
        name={name}
        size={size}
        tintColor={color}
        weight={weight}
      />
    );
  }

  const materialName = ICON_MAPPING[name] || name;
  return <MaterialIcons name={materialName} size={size} color={color} />;
}
```

## Component Checklist

When creating a new component, ensure:

- [ ] **Portable**: Self-contained, minimal external dependencies
- [ ] **Typed**: Full TypeScript types for props
- [ ] **Themed**: Uses CSS variables for colors, not hardcoded values
- [ ] **Accessible**: Proper accessibility roles and labels
- [ ] **Keyboard-aware**: Handles keyboard avoidance for inputs
- [ ] **Safe area-aware**: Respects device safe areas
- [ ] **Platform-adaptive**: Uses native primitives where available
- [ ] **Compound structure**: Complex components use compound pattern
- [ ] **Haptic feedback**: Provides tactile feedback on iOS
- [ ] **Dark mode**: Supports light and dark color schemes
- [ ] **Display name**: Set `displayName` in dev for debugging

```tsx
if (__DEV__) {
  MyComponent.displayName = "MyComponent";
}
```

## Dependencies Reference

| Package | Purpose |
|---------|---------|
| `react-native-css` | CSS runtime for React Native |
| `nativewind` | Metro transformer for Tailwind |
| `tailwindcss` | Utility-first CSS |
| `@tailwindcss/postcss` | PostCSS plugin for Tailwind v4 |
| `tailwind-merge` | Merge Tailwind classes safely |
| `clsx` | Conditional class names |
| `react-native-safe-area-context` | Safe area handling |
| `react-native-keyboard-controller` | Keyboard animations |
| `react-native-reanimated` | Gesture animations |
| `expo-haptics` | Haptic feedback |
| `expo-symbols` | SF Symbols |
| `expo-blur` | Blur effects |
| `expo-glass-effect` | iOS 26 liquid glass |
| `@bacons/apple-colors` | Native iOS colors |
