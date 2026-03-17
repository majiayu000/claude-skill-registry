---
name: generic-fullstack-design-system
description: Complete design system reference for full-stack applications. Covers colors, typography, spacing, component patterns (shadcn/ui), effects, GPU-accelerated animations, and WCAG AA accessibility. Use when implementing UI, choosing colors, applying spacing, creating components, or ensuring brand consistency.
---

# Fullstack Design System

Design system patterns for Next.js/NestJS full-stack applications.

**Extends:** [Generic Design System](../generic-design-system/SKILL.md) - Read base skill for color theory, typography scale, spacing system, and component states.

## Theme Configuration

### lib/theme.ts Structure

```typescript
// lib/theme.ts - Single source of truth
export const theme = {
  colors: {
    primary: "hsl(220, 100%, 55%)",
    secondary: "hsl(180, 100%, 50%)",
    accent: "hsl(270, 70%, 60%)",
  },
  spacing: {
    xs: "4px",
    sm: "8px",
    md: "16px",
    lg: "24px",
  },
};
```

### CSS Variables (globals.css)

```css
:root {
  --background: #ffffff;
  --foreground: #0a0a0f;
  --primary: hsl(220, 100%, 55%);
  --primary-foreground: #ffffff;
}

.dark {
  --background: #0a0a0f;
  --foreground: #fafafa;
}
```

### Tailwind Integration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: "var(--primary)",
      },
    },
  },
};
```

## shadcn/ui Patterns

### Button Variants

```tsx
import { Button } from '@/components/ui/button';

<Button>Primary</Button>
<Button variant="outline">Secondary</Button>
<Button variant="destructive">Delete</Button>
<Button variant="ghost">Cancel</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
```

### Form Components

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="user@example.com" />
</div>;
```

### Dialog/Modal

```tsx
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm Action</DialogTitle>
    </DialogHeader>
    {/* Content */}
  </DialogContent>
</Dialog>;
```

## Visual Effects

### Glassmorphism

```css
.glass {
  background: hsl(var(--card) / 0.5);
  backdrop-filter: blur(12px);
  border: 1px solid hsl(var(--border) / 0.5);
}
```

### Gradient Backgrounds

```css
.bg-gradient {
  background: linear-gradient(135deg, var(--primary), var(--accent));
}
```

## Dark Mode Implementation

### Next.js + next-themes

```tsx
// app/layout.tsx
import { ThemeProvider } from "next-themes";

export default function RootLayout({ children }) {
  return (
    <html suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system">
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### Theme Toggle

```tsx
import { useTheme } from "next-themes";

function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  return (
    <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
      Toggle theme
    </button>
  );
}
```

## Asset Organization

```
public/
├── images/
│   ├── logo.svg
│   └── og-image.png    # 1200x630, < 1MB
├── favicons/
│   ├── favicon.ico
│   ├── apple-touch-icon.png
│   └── favicon-32x32.png
└── site.webmanifest
```

## See Also

- [Generic Design System](../generic-design-system/SKILL.md) - Token organization, spacing
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Atomic Design, component docs
- [UX Principles](../_shared/UX_PRINCIPLES.md) - Visual hierarchy
