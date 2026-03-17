---
name: gpus-theme
description: "Portable GPUS design system theme (Portal Grupo US). This skill should be used when applying GPUS branding to other projects, setting up shadcn/ui with Navy/Gold palette, or copying the complete light/dark theme configuration. Includes CSS variables, Tailwind v4 theme, and shadcn configuration."
---

# GPUS Theme

Portable design system from the Portal Grupo US project featuring a Navy/Gold color palette with complete light and dark theme support.

> **Identity:** Navy backgrounds + Gold accents. Professional, premium, educational.

---

## Quick Start

### Option 1: Copy CSS Variables

Copy `assets/theme-tokens.css` to your project's main CSS file.

```css
@import "tailwindcss";
@import "./theme-tokens.css"; /* Copy from assets/ */
```

### Option 2: Use shadcn Configuration

Copy `assets/components.json` to your project root:

```bash
cp .agent/skills/gpus-theme/assets/components.json ./components.json
```

### Option 3: Tailwind v3 Config

Import theme tokens into `tailwind.config.ts`:

```typescript
import { gpusTheme } from './.agent/skills/gpus-theme/assets/tailwind-theme';

export default {
  theme: {
    extend: {
      colors: gpusTheme.colors,
    },
  },
};
```

---

## Theme Overview

### Color Palette

| Token | Light Mode | Dark Mode | Purpose |
|-------|------------|-----------|---------|
| **background** | White `0 0% 100%` | Navy `211 49% 10%` | Page background |
| **foreground** | Dark blue `222 47% 11%` | Gold `39 44% 65%` | Text color |
| **primary** | Gold `38 60% 45%` | Gold `39 44% 65%` | Main actions |
| **accent** | Light gold `38 60% 95%` | Muted `26 5% 27%` | Highlights |
| **destructive** | Red `0 84% 60%` | Red `0 84% 60%` | Errors |

### Border Radius

- Base: `0.625rem` (10px)
- Derived: `--radius-lg`, `--radius-md`, `--radius-sm`

### Custom Utilities

| Class | Effect |
|-------|--------|
| `.bg-mesh` | Radial gradient mesh background |
| `.glass-card` | Glassmorphism with blur |
| `.bg-noise` | Subtle noise texture overlay |
| `.animate-ripple` | Button ripple animation |

---

## Component Configuration

### shadcn/ui Settings

- **Style:** `new-york`
- **Base color:** `zinc`
- **CSS Variables:** Enabled
- **Icon Library:** `lucide`

### Extended Registries

| Registry | URL | Components |
|----------|-----|------------|
| @kokonutui | kokonutui.com | Premium components |
| @aceternity | ui.aceternity.com | Animated components |
| @magicui | magicui.design | Magic effects |
| @tweakcn | tweakcn.com | Theme generator |
| @shadcnui-blocks | shadcnui-blocks.com | Page blocks |
| @cult-ui | cult-ui.com | Cult components |
| @originui | originui.com | Origin components |
| @tailark | tailark.com | Tailark components |

---

## Files Reference

| File | Purpose |
|------|---------|
| `references/css-variables.md` | Complete CSS variable reference |
| `references/shadcn-config.md` | shadcn/ui configuration details |
| `assets/theme-tokens.css` | Portable CSS file |
| `assets/tailwind-theme.ts` | Tailwind v3 config export |
| `assets/components.json` | shadcn configuration |

---

## Usage Tips

### Dark Mode Toggle

The theme uses `.dark` class on `<html>` element:

```typescript
document.documentElement.classList.toggle('dark');
```

### Smooth Transitions

Theme includes CSS for smooth color transitions:

```css
body {
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

### View Transition API

For animated theme toggle, use the View Transition API selectors in `theme-tokens.css`.
