---
name: gluestack-nativewind
description: This skill enforces Gluestack UI v3 and NativeWind v4 design patterns for consistent, performant, and maintainable styling. It should be used when creating or reviewing components, fixing styling issues, or refactoring styles to follow the constrained design system.
---

# Gluestack NativeWind Design Patterns

This skill enforces constrained, opinionated styling patterns that reduce decision fatigue, improve performance, enable consistent theming, and limit the solution space to canonical patterns.

## Core Principles

1. **Gluestack components over React Native primitives** - Gluestack wraps RN with theming, accessibility, and cross-platform consistency
2. **Semantic tokens over arbitrary values** - Tokens encode intent, not just appearance
3. **className over inline styles** - Inline styles bypass optimization and consistency
4. **Spacing scale over pixel values** - Arbitrary values create unsustainable exceptions
5. **Remove dead code** - Unused patterns mislead AI and increase cognitive load

## When to Use This Skill

- Creating new components with styling
- Reviewing existing component styles
- Refactoring styles to follow the design system
- Fixing styling inconsistencies
- Adding dark mode support
- Theming components

## Rule 1: Gluestack Components Over React Native Primitives

Always use Gluestack components instead of direct React Native imports:

| React Native                           | Gluestack Equivalent                               |
| -------------------------------------- | -------------------------------------------------- |
| `View` from "react-native"             | `Box` from "@/components/ui/box"                   |
| `Text` from "react-native"             | `Text` from "@/components/ui/text"                 |
| `TouchableOpacity` from "react-native" | `Pressable` from "@/components/ui/pressable"       |
| `ScrollView` from "react-native"       | `ScrollView` from "@/components/ui/scroll-view"    |
| `Image` from "react-native"            | `Image` from "@/components/ui/image"               |
| `TextInput` from "react-native"        | `Input`, `InputField` from "@/components/ui/input" |
| `FlatList` from "react-native"         | `FlashList` from "@shopify/flash-list"             |

### Correct Pattern

```tsx
import { Box } from "@/components/ui/box";
import { Text } from "@/components/ui/text";
import { Pressable } from "@/components/ui/pressable";

const Component = () => (
  <Box className="p-4">
    <Text className="text-typography-900">Hello</Text>
    <Pressable onPress={handlePress}>
      <Text>Press Me</Text>
    </Pressable>
  </Box>
);
```

### Incorrect Pattern

```tsx
import { View, Text, TouchableOpacity } from "react-native";

const Component = () => (
  <View style={{ padding: 16 }}>
    <Text style={{ color: "#333" }}>Hello</Text>
    <TouchableOpacity onPress={handlePress}>
      <Text>Press Me</Text>
    </TouchableOpacity>
  </View>
);
```

### Exceptions

- Platform-specific code where RN primitives are explicitly required
- Deep integration with native modules
- Performance-critical paths where wrapper overhead matters (rare, must document)

## Rule 2: Semantic Color Tokens Over Raw Values

Use Gluestack semantic tokens instead of raw Tailwind colors:

| Instead of         | Use                   |
| ------------------ | --------------------- |
| `text-red-500`     | `text-error-500`      |
| `text-green-500`   | `text-success-500`    |
| `text-yellow-500`  | `text-warning-500`    |
| `text-blue-500`    | `text-info-500`       |
| `text-gray-500`    | `text-typography-500` |
| `bg-blue-600`      | `bg-primary-600`      |
| `border-gray-200`  | `border-outline-200`  |
| `#DC2626` (inline) | `text-error-600`      |

### Available Semantic Token Categories

| Token                | Purpose                                  | Scale |
| -------------------- | ---------------------------------------- | ----- |
| `primary-{0-950}`    | Brand identity, key interactive elements | 0-950 |
| `secondary-{0-950}`  | Secondary actions, supporting elements   | 0-950 |
| `tertiary-{0-950}`   | Tertiary accents                         | 0-950 |
| `error-{0-950}`      | Validation errors, destructive actions   | 0-950 |
| `success-{0-950}`    | Positive feedback, completions           | 0-950 |
| `warning-{0-950}`    | Alerts, attention-required states        | 0-950 |
| `info-{0-950}`       | Informational content                    | 0-950 |
| `typography-{0-950}` | Text colors                              | 0-950 |
| `outline-{0-950}`    | Border colors                            | 0-950 |
| `background-{0-950}` | Background colors                        | 0-950 |

### Special Background Tokens

Use state-based background tokens:

- `bg-background-error` - Error state backgrounds
- `bg-background-warning` - Warning state backgrounds
- `bg-background-success` - Success state backgrounds
- `bg-background-muted` - Muted/disabled backgrounds
- `bg-background-info` - Informational backgrounds

### Correct Pattern

```tsx
<Box className="bg-error-500">
  <Text className="text-typography-0">Error message</Text>
</Box>

<Box className="border border-outline-300 bg-background-50">
  <Text className="text-success-600">Success!</Text>
</Box>
```

### Incorrect Pattern

```tsx
<Box className="bg-red-500">
  <Text className="text-white">Error message</Text>
</Box>

<Box style={{ backgroundColor: '#DC2626' }}>
  <Text style={{ color: 'green' }}>Success!</Text>
</Box>
```

For complete token reference, see `references/color-tokens.md`.

## Rule 3: No Inline Styles

Avoid inline `style` props when className can achieve the same result.

### Resolution Hierarchy (in order of preference)

1. **className utilities** - Use existing Tailwind/NativeWind classes
2. **Gluestack component variants** - Use built-in component variants
3. **tva (Tailwind Variant Authority)** - Create reusable variant patterns
4. **NativeWind interop** - Enable className on third-party components
5. **Inline styles** - Only as absolute last resort with documented justification

### Correct Pattern

```tsx
<Box className="w-20 h-20 rounded-full bg-background-100" />

<Text className="text-lg font-bold text-typography-900" />
```

### Incorrect Pattern

```tsx
<Box
  style={{
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: "rgba(255, 255, 255, 0.1)",
  }}
/>
```

### Acceptable Exceptions

Inline styles are acceptable for:

1. **Dynamic values** - Values computed at runtime (e.g., animation values, safe area insets)
2. **Third-party component requirements** - Components that don't support className
3. **Platform-specific overrides** - When Platform.select is needed

```tsx
// Acceptable: dynamic value from hook
<Box style={{ paddingBottom: bottomInset }} />

// Acceptable: animation value
<Animated.View style={{ transform: [{ translateX: animatedValue }] }} />
```

## Rule 4: Spacing Scale Adherence

Use only values from the standard spacing scale. Arbitrary values create maintenance burden.

### Allowed Spacing Values

| Class | Size  |
| ----- | ----- |
| `0`   | 0px   |
| `0.5` | 2px   |
| `1`   | 4px   |
| `1.5` | 6px   |
| `2`   | 8px   |
| `2.5` | 10px  |
| `3`   | 12px  |
| `3.5` | 14px  |
| `4`   | 16px  |
| `5`   | 20px  |
| `6`   | 24px  |
| `7`   | 28px  |
| `8`   | 32px  |
| `9`   | 36px  |
| `10`  | 40px  |
| `11`  | 44px  |
| `12`  | 48px  |
| `14`  | 56px  |
| `16`  | 64px  |
| `20`  | 80px  |
| `24`  | 96px  |
| `28`  | 112px |
| `32`  | 128px |
| `36`  | 144px |
| `40`  | 160px |
| `44`  | 176px |
| `48`  | 192px |
| `52`  | 208px |
| `56`  | 224px |
| `60`  | 240px |
| `64`  | 256px |
| `72`  | 288px |
| `80`  | 320px |
| `96`  | 384px |

### Prohibited Patterns

- Arbitrary values: `p-[13px]`, `m-[27px]`, `gap-[15px]`
- Non-scale decimals: `p-2.7`, `m-4.3`

### Correct Pattern

```tsx
<Box className="p-4 m-2 gap-3" />
<Box className="px-6 py-4 mt-8" />
```

### Incorrect Pattern

```tsx
<Box className="p-[13px] m-[27px]" />
<Box style={{ padding: 13, margin: 27 }} />
```

For complete spacing reference, see `references/spacing-scale.md`.

## Rule 5: Dark Mode Using CSS Variables

Use the CSS variables approach with `dark:` prefix for dark mode support.

### Correct Pattern

```tsx
<Box className="bg-background-0 dark:bg-background-950" />
<Text className="text-typography-900 dark:text-typography-0" />
```

### Component-Level Dark Mode

```tsx
const CardView = ({ isDark }: { readonly isDark: boolean }) => (
  <Box className={isDark ? "bg-background-950" : "bg-background-0"}>
    <Text className={isDark ? "text-typography-0" : "text-typography-900"}>
      Content
    </Text>
  </Box>
);
```

## Rule 6: Gluestack Sub-Component Pattern

Use Gluestack's composable sub-component pattern for complex components.

### Correct Pattern

```tsx
<Button action="primary" size="md">
  <ButtonText>Click Me</ButtonText>
  <ButtonIcon as={ChevronRightIcon} />
</Button>

<Input variant="outline" size="md">
  <InputField placeholder="Enter text" />
  <InputSlot>
    <InputIcon as={SearchIcon} />
  </InputSlot>
</Input>

<Select>
  <SelectTrigger>
    <SelectInput placeholder="Select option" />
    <SelectIcon as={ChevronDownIcon} />
  </SelectTrigger>
  <SelectPortal>
    <SelectBackdrop />
    <SelectContent>
      <SelectItem label="Option 1" value="1" />
      <SelectItem label="Option 2" value="2" />
    </SelectContent>
  </SelectPortal>
</Select>
```

### Incorrect Pattern

```tsx
// Missing sub-components
<Button>Click Me</Button>

// Text must be wrapped in ButtonText
<Button>
  Click Me  {/* Will not render correctly */}
</Button>
```

## Rule 7: Variant-Based Styling with tva

For components with multiple style variants, use `tva` (Tailwind Variant Authority).

### Correct Pattern

```tsx
import { tva } from "@gluestack-ui/nativewind-utils/tva";

const cardStyles = tva({
  base: "rounded-lg p-4",
  variants: {
    variant: {
      elevated: "bg-background-0 shadow-hard-2",
      outlined: "bg-transparent border border-outline-200",
      filled: "bg-background-50",
    },
    size: {
      sm: "p-2",
      md: "p-4",
      lg: "p-6",
    },
  },
  defaultVariants: {
    variant: "elevated",
    size: "md",
  },
});

const Card = ({ variant, size, className }: CardProps) => (
  <Box className={cardStyles({ variant, size, className })} />
);
```

## Rule 8: className Merging for Custom Components

Allow className override in custom components using string concatenation.

### Correct Pattern

```tsx
interface BoxCardProps {
  readonly className?: string;
  readonly children: React.ReactNode;
}

const BoxCard = ({ className, children }: BoxCardProps) => (
  <Box className={`rounded-lg bg-background-0 p-4 ${className ?? ""}`}>
    {children}
  </Box>
);
```

## Validation

To validate styling compliance, run:

```bash
python3 .claude/skills/gluestack-nativewind/scripts/validate_styling.py [path]
```

The script detects:

1. Direct React Native component imports with Gluestack equivalents
2. Raw color values without semantic tokens
3. Inline style objects where className could be used
4. Arbitrary bracket notation values
5. Non-scale spacing values

## Escalation Guidance

When a design request cannot be satisfied with existing patterns:

1. **Push back early** - Explain performance and maintenance implications
2. **Propose alternatives** - Map to existing tokens or suggest new semantic tokens
3. **Add to design system** - If truly needed, add token to tailwind.config.js
4. **Document exception** - If inline style is unavoidable, add JSDoc explaining why

## Reference Documentation

For detailed mappings and complete token lists:

- `references/component-mapping.md` - Gluestack equivalents for React Native primitives
- `references/color-tokens.md` - Complete semantic color token reference
- `references/spacing-scale.md` - Allowed spacing values with pixel equivalents
