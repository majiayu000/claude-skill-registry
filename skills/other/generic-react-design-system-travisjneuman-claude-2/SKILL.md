---
name: generic-react-design-system
description: Complete design system reference for React applications. Covers colors, typography, spacing, component patterns, glassmorphism effects, GPU-accelerated animations, and WCAG AA accessibility. Use when implementing UI, choosing colors, applying spacing, creating components, or ensuring brand consistency.
---

# React Design System

Design system patterns for React/TypeScript applications.

**Extends:** [Generic Design System](../generic-design-system/SKILL.md) - Read base skill for color theory, typography scale, spacing system, and component states.

## Tailwind Configuration

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: "var(--primary)",
        secondary: "var(--secondary)",
        accent: "var(--accent)",
      },
      spacing: {
        18: "72px",
      },
      borderRadius: {
        xl: "16px",
      },
    },
  },
};
```

### CSS Variables Setup

```css
:root {
  /* Brand - customize per project */
  --primary: #3b82f6;
  --primary-rgb: 59, 130, 246;
  --secondary: #10b981;
  --accent: #8b5cf6;

  /* Surfaces */
  --background: #ffffff;
  --foreground: #000000;
  --muted: #64748b;
}

[data-theme="dark"] {
  --background: #121212;
  --foreground: #ffffff;
}
```

## React Component Patterns

### Button Variants

```tsx
// Primary
<button className="px-6 py-3 bg-primary text-white rounded-lg shadow
  hover:shadow-lg hover:-translate-y-0.5 transition-all">
  Primary
</button>

// Secondary
<button className="px-6 py-3 border border-primary text-primary rounded-lg
  hover:bg-primary/10 transition-all">
  Secondary
</button>

// Ghost
<button className="px-4 py-2 text-muted hover:bg-slate-100 rounded-lg transition-all">
  Ghost
</button>
```

### Input Fields

```tsx
<input
  className="w-full px-4 py-3 bg-white border border-slate-300 rounded-md
    focus:border-primary focus:ring-2 focus:ring-primary/50 transition-all"
  placeholder="Enter text..."
/>
```

### Cards

```tsx
<div className="p-6 bg-white dark:bg-slate-800 rounded-xl shadow-soft">
  {/* Card content */}
</div>
```

### Modals with Framer Motion

```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{ opacity: 1, scale: 1 }}
  exit={{ opacity: 0, scale: 0.95 }}
  className="glass p-8 rounded-2xl max-w-md"
  role="dialog"
  aria-modal="true"
>
  {/* Modal content */}
</motion.div>
```

### Loading Skeleton

```tsx
<div className="animate-pulse space-y-4">
  <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-3/4" />
  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded" />
</div>
```

## Visual Effects

### Glassmorphism

```css
.glass {
  backdrop-filter: blur(12px) saturate(180%);
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.25);
}

.glass-dark {
  background: rgba(255, 255, 255, 0.05);
}
```

### Shadows

```css
--shadow-soft: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-medium: 0 10px 15px rgba(0, 0, 0, 0.15);
--shadow-floating: 0 25px 50px rgba(0, 0, 0, 0.3);
--shadow-glow: 0 0 20px rgba(var(--primary-rgb), 0.4);
```

## Framer Motion Patterns

### Hover Lift

```tsx
<motion.div
  whileHover={{ y: -4 }}
  transition={{ type: "spring", stiffness: 300 }}
  className="card"
>
  {/* Content */}
</motion.div>
```

### Page Transitions

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.2 }}
>
  {/* Page content */}
</motion.div>
```

### Stagger Children

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map((i) => (
    <motion.li key={i} variants={item} />
  ))}
</motion.ul>;
```

## Dark Mode Implementation

### React Context Approach

```tsx
// ThemeProvider.tsx
const ThemeContext = createContext<{
  theme: "light" | "dark";
  toggle: () => void;
}>({ theme: "light", toggle: () => {} });

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggle: () => setTheme((t) => (t === "light" ? "dark" : "light")),
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}
```

### System Preference Detection

```tsx
useEffect(() => {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");
  setTheme(prefersDark.matches ? "dark" : "light");

  prefersDark.addEventListener("change", (e) =>
    setTheme(e.matches ? "dark" : "light"),
  );
}, []);
```

## Accessibility in React

### Focus States (Tailwind)

```css
*:focus-visible {
  @apply outline-2 outline-primary outline-offset-2;
}
```

### Skip Link

```tsx
<a
  href="#main"
  className="sr-only focus:not-sr-only focus:absolute
  focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2
  focus:bg-primary focus:text-white focus:rounded"
>
  Skip to content
</a>
```

## See Also

- [Generic Design System](../generic-design-system/SKILL.md) - Tokens, spacing, typography
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Atomic Design, component docs
- [UX Principles](../_shared/UX_PRINCIPLES.md) - Visual hierarchy, interaction patterns
