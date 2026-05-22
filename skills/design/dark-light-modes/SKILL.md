---
name: dark-light-modes
description: Light and dark mode implementation with prefers-color-scheme, CSS variables, and automatic switching. Use when implementing theme modes, color schemes, or system preference detection.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Dark/Light Modes

Robust theme system with system preference detection.

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Check existing theme setup
2. **fuse-ai-pilot:research-expert** - next-themes or theme provider docs

After: Run **fuse-ai-pilot:sniper** for validation.

## CSS Variables Approach

```css
:root {
  /* Light mode (default) */
  --background: oklch(100% 0 0);
  --foreground: oklch(10% 0 0);
  --surface: oklch(98% 0.01 260);
  --muted: oklch(95% 0.01 260);
  --border: oklch(90% 0.01 260);

  /* Glass */
  --glass-bg: rgba(255, 255, 255, 0.8);
  --glass-border: rgba(255, 255, 255, 0.2);
}

.dark {
  --background: oklch(10% 0.01 260);
  --foreground: oklch(98% 0 0);
  --surface: oklch(15% 0.01 260);
  --muted: oklch(20% 0.01 260);
  --border: oklch(25% 0.01 260);

  /* Glass - darker */
  --glass-bg: rgba(0, 0, 0, 0.4);
  --glass-border: rgba(255, 255, 255, 0.1);
}
```

## System Preference Detection

```css
/* Automatic system preference */
@media (prefers-color-scheme: dark) {
  :root:not(.light) {
    --background: oklch(10% 0.01 260);
    --foreground: oklch(98% 0 0);
    /* ... dark values */
  }
}
```

## React Implementation

```tsx
// ThemeProvider.tsx
"use client";
import { createContext, useContext, useEffect, useState } from "react";

type Theme = "light" | "dark" | "system";

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
}>({ theme: "system", setTheme: () => {} });

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>("system");

  useEffect(() => {
    const root = document.documentElement;

    if (theme === "system") {
      const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      root.classList.toggle("dark", systemDark);
    } else {
      root.classList.toggle("dark", theme === "dark");
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

## Next.js with next-themes

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

## Theme Toggle Component

```tsx
"use client";
import { Moon, Sun, Monitor } from "lucide-react";
import { useTheme } from "next-themes";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex gap-1 p-1 bg-muted rounded-lg">
      <button
        onClick={() => setTheme("light")}
        className={cn("p-2 rounded", theme === "light" && "bg-background")}
      >
        <Sun className="h-4 w-4" />
      </button>
      <button
        onClick={() => setTheme("dark")}
        className={cn("p-2 rounded", theme === "dark" && "bg-background")}
      >
        <Moon className="h-4 w-4" />
      </button>
      <button
        onClick={() => setTheme("system")}
        className={cn("p-2 rounded", theme === "system" && "bg-background")}
      >
        <Monitor className="h-4 w-4" />
      </button>
    </div>
  );
}
```

## Tailwind Dark Mode

```tsx
/* Component with dark mode */
className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white"

/* Glass with dark mode */
className="bg-white/80 dark:bg-black/40 backdrop-blur-xl
           border-white/20 dark:border-white/10"
```

## Prevent Flash (FOUC)

```tsx
// app/layout.tsx
<html suppressHydrationWarning>
  <head>
    <script
      dangerouslySetInnerHTML={{
        __html: `
          (function() {
            const theme = localStorage.getItem('theme') || 'system';
            const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (theme === 'dark' || (theme === 'system' && systemDark)) {
              document.documentElement.classList.add('dark');
            }
          })();
        `,
      }}
    />
  </head>
```

## Validation

```
[ ] CSS variables for both modes
[ ] prefers-color-scheme respected
[ ] Manual toggle available
[ ] No FOUC (flash of unstyled content)
[ ] Glass variants for both modes
[ ] Stored preference in localStorage
```

## References

- `../../references/color-system.md` - Color definitions
- `../../skills/theming-tokens/SKILL.md` - Token architecture
