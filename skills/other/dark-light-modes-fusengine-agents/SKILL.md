---
name: dark-light-modes
description: Use when implementing theme modes, color schemes, or system preference detection. Covers prefers-color-scheme, CSS variables, next-themes.
versions:
  next-themes: "0.4"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: theming-tokens, designing-systems
---

# Dark/Light Modes

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing theme setup
2. **fuse-ai-pilot:research-expert** - next-themes or theme provider docs

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **CSS Variables** | Token-based theming |
| **System Detection** | prefers-color-scheme |
| **Manual Toggle** | User preference |
| **No FOUC** | Prevent flash |

---

## Quick Reference

### CSS Variables

```css
:root {
  --background: oklch(100% 0 0);
  --foreground: oklch(10% 0 0);
  --glass-bg: rgba(255, 255, 255, 0.8);
}

.dark {
  --background: oklch(10% 0.01 260);
  --foreground: oklch(98% 0 0);
  --glass-bg: rgba(0, 0, 0, 0.4);
}
```

### System Preference

```css
@media (prefers-color-scheme: dark) {
  :root:not(.light) {
    --background: oklch(10% 0.01 260);
  }
}
```

### Next.js with next-themes

```tsx
// app/providers.tsx
"use client";
import { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}
```

### Theme Toggle

```tsx
"use client";
import { Moon, Sun, Monitor } from "lucide-react";
import { useTheme } from "next-themes";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex gap-1 p-1 bg-muted rounded-lg">
      <button onClick={() => setTheme("light")}>
        <Sun className="h-4 w-4" />
      </button>
      <button onClick={() => setTheme("dark")}>
        <Moon className="h-4 w-4" />
      </button>
      <button onClick={() => setTheme("system")}>
        <Monitor className="h-4 w-4" />
      </button>
    </div>
  );
}
```

### Prevent FOUC

```tsx
<html suppressHydrationWarning>
  <head>
    <script dangerouslySetInnerHTML={{
      __html: `
        (function() {
          const theme = localStorage.getItem('theme') || 'system';
          const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
          if (theme === 'dark' || (theme === 'system' && systemDark)) {
            document.documentElement.classList.add('dark');
          }
        })();
      `,
    }} />
  </head>
```

---

## Validation Checklist

```
[ ] CSS variables for both modes
[ ] prefers-color-scheme respected
[ ] Manual toggle available
[ ] No FOUC (flash of unstyled content)
[ ] Glass variants for both modes
[ ] Stored preference in localStorage
```

---

## Best Practices

### DO
- Use CSS variables for theming
- Support system preference
- Provide manual toggle
- Prevent FOUC with script

### DON'T
- Hard-code dark: classes everywhere
- Ignore system preference
- Forget localStorage
- Allow flash on load
