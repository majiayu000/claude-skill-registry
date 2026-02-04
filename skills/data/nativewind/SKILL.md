---
name: nativewind
description: NativeWind 4.x styling for React Native. Use when applying Tailwind classes to RN components, configuring NativeWind, or converting web Tailwind patterns to mobile.
---

# NativeWind

## Overview

NativeWind 4.x bridges Tailwind CSS 3.x into React Native, enabling `className` props on View, Text, Pressable, ScrollView, and other RN components. Provides familiar Tailwind utility classes with native rendering.

**Install**: `pnpm add nativewind tailwindcss@3` + babel/metro configuration

## Workflows

**Initial setup:**
1. [ ] Install: `pnpm add nativewind tailwindcss@3`
2. [ ] Create `tailwind.config.js` with content paths pointing to `app/`, `components/`, etc.
3. [ ] Create `global.css` with `@tailwind base; @tailwind components; @tailwind utilities;`
4. [ ] Update `babel.config.js`: add `nativewind/babel` preset
5. [ ] Update `metro.config.js`: wrap with `withNativeWind`
6. [ ] Create `nativewind-env.d.ts` with `/// <reference types="nativewind/types" />`
7. [ ] Import `global.css` in root `_layout.tsx`

**Styling a component:**
1. [ ] Import RN component (View, Text, Pressable, etc.)
2. [ ] Apply `className` prop with Tailwind utilities
3. [ ] Use `contentContainerClassName` for ScrollView/FlashList inner styling
4. [ ] Test on device/simulator to verify rendering

## Guidance

### Configuration Files

Three config files are required:

**`babel.config.js`**: Add NativeWind preset
```
presets: ['babel-preset-expo', 'nativewind/babel']
```

**`metro.config.js`**: Wrap Metro config with NativeWind
```
withNativeWind(config, { input: './global.css' })
```

**`tailwind.config.js`**: Standard Tailwind 3.x config with RN content paths
```
content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}']
```

### className Prop

NativeWind adds `className` support to all RN core components:

- `<View className="flex-1 bg-white p-4">`
- `<Text className="text-lg font-bold text-gray-900">`
- `<Pressable className="bg-blue-500 rounded-lg p-3">`
- `<ScrollView className="flex-1" contentContainerClassName="p-4 gap-3">`

### Key Differences from Web Tailwind

| Web Tailwind | NativeWind (RN) | Notes |
|-------------|-----------------|-------|
| `hover:bg-gray-100` | Not available | No hover on touch devices |
| `cursor-pointer` | Not applicable | Use Pressable instead |
| `flex` (row default) | `flex` (column default) | RN flexbox defaults to column |
| Bare strings | Must wrap in `<Text>` | RN requires Text component |
| `div` | `View` | No HTML elements |
| `gap-4` | `gap-4` | Supported in NativeWind 4.x |
| `grid` | Not available | Use flex layouts |

### Conditional Classes

Concatenate class strings conditionally:

```
className={`px-4 py-2 rounded-lg ${isActive ? 'bg-blue-500' : 'bg-gray-200'}`}
```

Or use a utility like `clsx`/`cn` for cleaner conditionals.

### ScrollView Styling

ScrollView has two className targets:

- `className` — outer container styling
- `contentContainerClassName` — inner content styling (padding, gap, alignment)

Always use `contentContainerClassName` for padding and spacing of scroll content.

### Theme Customization

Extend via `tailwind.config.js` theme:

```
theme: {
  extend: {
    colors: { brand: { 50: '...', 500: '...', 900: '...' } },
    fontFamily: { sans: ['Inter'] }
  }
}
```

## Best Practices

- Always create `nativewind-env.d.ts` for TypeScript `className` type support
- Use `contentContainerClassName` on ScrollView, not `className` for inner spacing
- Remember flex defaults to column in RN — add `flex-row` explicitly when needed
- Import `global.css` at the top of root `_layout.tsx`
- Use Tailwind's spacing scale consistently (avoid mixing with StyleSheet)
- Keep `tailwind.config.js` content paths accurate to avoid missing styles
- Use `gap-*` instead of margin between siblings for consistent spacing

## Anti-Patterns

- Mixing `StyleSheet.create()` with `className` in the same component (pick one)
- Using `hover:` or `cursor-` utilities (not available on mobile)
- Forgetting `contentContainerClassName` on ScrollView (padding won't work on `className`)
- Using `grid` utilities (not supported in RN — use flex layouts)
- Placing bare strings without `<Text>` wrapper (crashes on RN)
- Not including all source directories in `tailwind.config.js` content array
- Using Tailwind CSS 4.x syntax (NativeWind requires Tailwind 3.x)
