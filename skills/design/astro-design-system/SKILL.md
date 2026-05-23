# Astro Design System Skill

## When to Use This Skill

Use this skill when:
- Creating or modifying CSS styles
- Adding new UI components
- Changing colors, spacing, typography, or other visual properties
- Implementing theme switching (light/dark mode)

## Design System Architecture

### File Structure

```
src/styles/
├── design-system.css  # Base tokens (typography, spacing, radius, etc.)
├── theme-dark.css     # Dark theme color variables (warm amber)
└── theme-light.css    # Light theme color variables (teal)
```

### How Themes Work

1. **Base tokens** in `design-system.css` are theme-agnostic (spacing, fonts, etc.)
2. **Color tokens** are defined per-theme in `theme-*.css`
3. Theme is set via `data-theme` attribute on `<html>`:
   - `data-theme="dark"` → Dark theme
   - `data-theme="light"` → Light theme
   - No attribute or `data-theme="auto"` → Follows system preference

### Key CSS Variables

#### Colors (Theme-Dependent)
```css
var(--color-accent)       /* Primary accent color */
var(--color-accent-hover) /* Accent hover state */
var(--color-accent-dim)   /* Subtle accent background */

var(--color-bg)           /* Page background */
var(--color-bg-sidebar)   /* Sidebar background */
var(--color-surface)      /* Cards, elevated elements */

var(--color-text)         /* Primary text */
var(--color-text-muted)   /* Secondary text */
var(--color-border)       /* Borders */
```

#### Typography
```css
var(--text-xs)    /* 0.75rem - 12px */
var(--text-sm)    /* 0.875rem - 14px */
var(--text-base)  /* 1rem - 16px */
var(--text-lg)    /* 1.125rem - 18px */
var(--text-xl)    /* 1.25rem - 20px */
var(--text-2xl)   /* 1.5rem - 24px */
var(--text-3xl)   /* 2rem - 32px */
var(--text-4xl)   /* 2.5rem - 40px */

var(--font-normal)    /* 400 */
var(--font-medium)    /* 500 */
var(--font-semibold)  /* 600 */
var(--font-bold)      /* 700 */
```

#### Spacing
```css
var(--space-1)   /* 0.25rem - 4px */
var(--space-2)   /* 0.5rem - 8px */
var(--space-3)   /* 0.75rem - 12px */
var(--space-4)   /* 1rem - 16px */
var(--space-6)   /* 1.5rem - 24px */
var(--space-8)   /* 2rem - 32px */
var(--space-12)  /* 3rem - 48px */
```

#### Other Tokens
```css
var(--radius-sm)  /* 2px */
var(--radius-md)  /* 4px */
var(--radius-lg)  /* 8px */

var(--shadow-sm)  /* Subtle elevation */
var(--shadow-md)  /* Default card shadow */
var(--shadow-lg)  /* Modal/dropdown shadow */

var(--transition-fast)   /* 0.1s */
var(--transition-base)   /* 0.15s */
var(--transition-slow)   /* 0.3s */
```

## Rules

### DO:
- Always use `var(--token-name)` instead of hardcoded values
- Use semantic color names (`--color-text-muted`) not raw values
- Define styles in CSS files, not inline when possible
- Use utility classes from design-system.css when they exist

### DON'T:
- Never use hardcoded hex colors like `#1a1a1a`
- Never use hardcoded pixel values for spacing (use `var(--space-*)`)
- Never modify the design system files without explicit permission
- Don't duplicate tokens - use existing ones

## Examples

### Good: Using Design Tokens
```css
.nav-item {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.nav-item:hover {
  background: var(--color-accent-dim);
  color: var(--color-accent);
}
```

### Bad: Hardcoded Values
```css
/* DON'T DO THIS */
.nav-item {
  padding: 8px 12px;
  font-size: 14px;
  color: #a8a29e;
  border-radius: 4px;
  transition: all 0.15s ease;
}
```

### In React/Astro Components
```tsx
// Inline styles should still use CSS variables
<div style={{
  padding: 'var(--space-4)',
  backgroundColor: 'var(--color-surface)',
  borderRadius: 'var(--radius-lg)'
}}>
  Content
</div>
```

## Theme Switching

### Adding Theme Toggle (Vanilla JS)
```astro
<script is:inline>
  // Initialize theme from localStorage or system preference
  const stored = localStorage.getItem('theme');
  if (stored) {
    document.documentElement.setAttribute('data-theme', stored);
  }
  // else: CSS @media query handles auto-detection
</script>

<script is:inline>
  document.getElementById('theme-toggle')?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
</script>
```

## Importing Styles

In your main layout:
```astro
---
// Layout.astro
---
<html>
  <head>
    <style is:global>
      @import '../styles/design-system.css';
      @import '../styles/theme-dark.css';
      @import '../styles/theme-light.css';
    </style>
  </head>
</html>
```

Or import in your Astro config if using a build tool that supports it.
