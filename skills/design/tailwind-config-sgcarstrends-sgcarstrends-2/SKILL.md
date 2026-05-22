---
name: tailwind-config
description: Update Tailwind CSS configuration, custom themes, and design tokens across packages. Use when adding new colors, spacing scales, or customizing the design system.
allowed-tools: Read, Edit, Grep, Glob
---

# Tailwind CSS Configuration Skill

## Configuration Structure

```
packages/ui/
├── tailwind.config.ts       # Base config with shadcn/ui theming
└── src/styles/globals.css   # CSS variables

apps/web/
├── tailwind.config.ts       # Extends UI package config
└── src/app/globals.css      # App-specific styles
```

## CSS Variables

Defined in `packages/ui/src/styles/globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --muted: 210 40% 96.1%;
    --accent: 210 40% 96.1%;
    --destructive: 0 84.2% 60.2%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode values */
  }
}
```

## Adding Custom Colors

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#0070F3",
          secondary: "#7928CA",
        },
      },
    },
  },
};
```

## Adding Animations

```typescript
theme: {
  extend: {
    keyframes: {
      shimmer: {
        "0%": { backgroundPosition: "-200% 0" },
        "100%": { backgroundPosition: "200% 0" },
      },
    },
    animation: {
      shimmer: "shimmer 2s linear infinite",
    },
  },
}
```

## Custom Utilities

```css
/* globals.css */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}
```

## Plugins

```typescript
plugins: [
  require("@tailwindcss/typography"),  // prose classes
  require("@tailwindcss/forms"),        // form resets
  require("tailwindcss-animate"),       // animations
]
```

## Size Utility Convention

Use `size-*` instead of `h-* w-*` for equal dimensions:

```tsx
// ✅ Good
<div className="size-4">Icon</div>
<div className="size-8">Avatar</div>

// ❌ Avoid
<div className="h-4 w-4">Icon</div>
```

## Dark Mode

```typescript
// tailwind.config.ts
export default {
  darkMode: ["class"],
};
```

Toggle with next-themes:

```tsx
import { useTheme } from "next-themes";
const { theme, setTheme } = useTheme();
```

## Debugging

```bash
# Check resolved config
npx tailwindcss config

# Watch for generated classes
TAILWIND_MODE=watch npx tailwindcss -i ./src/styles/globals.css -o ./dist/output.css --watch
```

**Common issues:**
- Classes not applying → Check content paths
- Dark mode not working → Verify `darkMode: ["class"]` and ThemeProvider
- Classes purged → Add to safelist or use complete class names

## Best Practices

1. **Mobile-first** - Default styles for mobile, add breakpoints up
2. **CSS Variables** - Use for theming (enables dark mode)
3. **Content paths** - Include all component paths
4. **Semantic names** - Use `brand`, `accent` not `blue-500`
5. **Size utility** - Use `size-*` for equal dimensions

## References

- Tailwind CSS: https://tailwindcss.com
- Design tokens: See `design-language-system` skill
