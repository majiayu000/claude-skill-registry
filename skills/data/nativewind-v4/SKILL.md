---
name: nativewind-v4
description: >
  NativeWind v4 patterns for Liftera (React Native + React Native Web).
  Trigger: When styling React Native components with className, configuring Tailwind/NativeWind, or debugging style differences between web and mobile.
license: Apache-2.0
metadata:
  author: liftera
  version: "1.0"
  scope: [root, ui]
  auto_invoke: "Working with NativeWind styles"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Styling Decision Tree

```
Tailwind class exists?  → className="..."
Dynamic value?          → style={{ width: `${x}%` }}
Conditional styles?     → cn("base", condition && "variant")
Static only?            → className="..." (no cn() needed)
Library can't use class?→ style prop with var() constants
```

## Critical Rules

### Never Use var() in className

```typescript
// ❌ NEVER: var() in className
<View className="bg-[var(--color-primary)]" />
<Text className="text-[var(--text-color)]" />

// ✅ ALWAYS: Use Tailwind semantic classes
<View className="bg-primary" />
<Text className="text-slate-400" />
```

### Never Use Hex Colors

```typescript
// ❌ NEVER: Hex colors in className
<Text className="text-[#ffffff]" />
<View className="bg-[#1e293b]" />

// ✅ ALWAYS: Use Tailwind color classes
<Text className="text-white" />
<View className="bg-slate-800" />
```

## The cn() Utility

```typescript
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### When to Use cn()

```typescript
// ✅ Conditional classes
<View className={cn("base-class", isActive && "active-class")} />

// ✅ Merging with potential conflicts
<Pressable className={cn("px-4 py-2", className)} />  // className might override

// ✅ Multiple conditions
<View className={cn(
  "rounded-lg border",
  variant === "primary" && "bg-blue-500",
  variant === "secondary" && "bg-gray-200",
  disabled && "opacity-50"
)} />
```

### When NOT to Use cn()

```typescript
// ❌ Static classes - unnecessary wrapper
<View className={cn("flex items-center gap-2")} />

// ✅ Just use className directly
<View className="flex items-center gap-2" />
```

## Style Constants for Charts/Libraries

When libraries don't accept className (like Recharts):

```typescript
// ✅ Constants with var() - ONLY for library props
const CHART_COLORS = {
  primary: "var(--color-primary)",
  secondary: "var(--color-secondary)",
  text: "var(--color-text)",
  gridLine: "var(--color-border)",
};

// Usage with Recharts (can't use className)
<XAxis tick={{ fill: CHART_COLORS.text }} />
<CartesianGrid stroke={CHART_COLORS.gridLine} />
```

## Dynamic Values

```typescript
// ✅ style prop for truly dynamic values
<View style={{ width: `${percentage}%` }} />
<View style={{ opacity: isVisible ? 1 : 0 }} />
```

## Common Patterns

### Flexbox

```typescript
<View className="flex items-center justify-between gap-4" />
<View className="flex flex-col gap-2" />
<View className="flex items-center" />
```

### Grid

```typescript
<View className="flex flex-row flex-wrap gap-4" />
<View className="flex flex-row flex-wrap gap-6" />
```

### Spacing

```typescript
// Padding
<View className="p-4" />           // All sides
<View className="px-4 py-2" />     // Horizontal, vertical
<View className="pt-4 pb-2" />     // Top, bottom

// Margin
<View className="m-4" />
<View className="mx-auto" />       // Center horizontally
<View className="mt-8 mb-4" />
```

### Typography

```typescript
<Text className="text-2xl font-bold text-white" />
<Text className="text-sm text-slate-400" />
<Text className="text-xs font-medium uppercase tracking-wide" />
```

### Borders & Shadows

```typescript
<View className="rounded-lg border border-slate-700" />
<View className="rounded-full shadow-lg" />
<View className="border-2 border-blue-500" />
```

### States

```typescript
<Pressable className="active:bg-blue-600 active:scale-95" />
<TextInput className="focus:border-blue-500" />
<View className="opacity-100" />
```

### Responsive

```typescript
<View className="w-full md:w-1/2 lg:w-1/3" />
<View className="hidden md:flex" />
<Text className="text-sm md:text-base lg:text-lg" />
```

### Dark Mode

```typescript
<View className="bg-white dark:bg-slate-900" />
<Text className="text-gray-900 dark:text-white" />
```

## Arbitrary Values (Escape Hatch)

```typescript
// ✅ OK for one-off values not in design system
<View className="w-[327px]" />
<View className="top-[117px]" />

// ❌ Don't use for colors - use theme instead
<View className="bg-[#1e293b]" />  // NO
```

## Cross-Platform Styling (REQUIRED)

- **ALWAYS** use `className` for styling where supported.
- **ALWAYS** ensure styles render correctly in:
  - Expo (native)
  - React Native Web (Next.js)

## Avoid Platform Assumptions (REQUIRED)

- **NEVER** assume CSS-only features exist in native.
- **ALWAYS** prefer utility classes and shared tokens over platform hacks.

## When to Use style Prop

- Use `style={{ ... }}` only for truly dynamic values that are not representable as utility classes.

## Debugging Checklist

- Confirm the component runs in both apps.
- Confirm the Tailwind config is shared/compatible.
- If a style differs web vs native, isolate whether it is a layout difference (flexbox) or a platform limitation.
