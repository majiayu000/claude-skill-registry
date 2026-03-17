---
description: Use this skill when the user asks to "generate dark mode", "create dark theme", "add dark mode support", "convert to dark mode colors", "generate dark color palette", or wants to automatically generate dark mode variants for their components with intelligent color inversion and accessibility preservation.
---

# Dark Mode Generation Skill

## Overview

Automatically generate dark mode color schemes from light mode designs with intelligent color inversion, contrast preservation, and accessibility compliance (WCAG 2.2).

**Input:** Light mode component
**Output:** Dark mode CSS variables, color mappings, theme toggle, updated stories

## How It Works

### 1. Analyze Light Mode Colors

Extract all colors from component:
```tsx
// Detected colors
Background: #FFFFFF
Text: #1F2937 (gray-800)
Primary: #2196F3 (blue-500)
Border: #E5E7EB (gray-200)
Shadow: rgba(0, 0, 0, 0.1)
```

### 2. Generate Dark Palette

Apply intelligent transformations:

```css
/* Light Mode */
--bg-primary: #FFFFFF;      /* white */
--text-primary: #1F2937;    /* dark gray */
--color-primary: #2196F3;   /* blue */
--border: #E5E7EB;          /* light gray */

/* Dark Mode (Generated) */
--bg-primary: #1F2937;      /* dark gray (inverted) */
--text-primary: #F9FAFB;    /* off-white (inverted) */
--color-primary: #60A5FA;   /* lighter blue (adjusted for contrast) */
--border: #374151;          /* medium gray (adjusted) */
```

**Rules:**
- Backgrounds: Darken significantly (#FFF → #1F2937)
- Text: Lighten for readability (#000 → #F9FAFB)
- Brand colors: Adjust for contrast (may lighten or darken)
- Borders: Medium grays (#E5E7EB → #374151)
- Shadows: Invert or remove (dark shadows on dark BG don't work)

### 3. Preserve Contrast Ratios

Ensure WCAG compliance maintained:

```
Light Mode: #1F2937 on #FFFFFF = 16.1:1 (AAA) ✓
Dark Mode:  #F9FAFB on #1F2937 = 15.8:1 (AAA) ✓

Light Mode: #2196F3 on #FFFFFF = 3.1:1 (AA Large) ✓
Dark Mode:  #60A5FA on #1F2937 = 4.7:1 (AA Normal) ✓ (Improved!)
```

### 4. Generate Theme System

Create complete dark mode implementation:

**CSS Variables:**
```css
/* themes/colors.css */
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F9FAFB;
  --text-primary: #1F2937;
  --text-secondary: #6B7280;
  --color-primary: #2196F3;
  --border: #E5E7EB;
  --shadow: rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
  --bg-primary: #1F2937;
  --bg-secondary: #111827;
  --text-primary: #F9FAFB;
  --text-secondary: #D1D5DB;
  --color-primary: #60A5FA;
  --border: #374151;
  --shadow: rgba(0, 0, 0, 0.3);
}
```

**Theme Toggle Component:**
```tsx
// components/ThemeToggle.tsx
'use client';

import { useEffect, useState } from 'react';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved as 'light' | 'dark');
    document.documentElement.setAttribute('data-theme', saved);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <button
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
    >
      {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
    </button>
  );
}
```

### 5. Update Storybook Stories

Add dark mode variants:

```tsx
// Button.stories.tsx
export const LightMode: Story = {
  parameters: {
    backgrounds: { default: 'light' },
    theme: 'light',
  },
};

export const DarkMode: Story = {
  parameters: {
    backgrounds: { default: 'dark' },
    theme: 'dark',
  },
  decorators: [
    (Story) => (
      <div data-theme="dark">
        <Story />
      </div>
    ),
  ],
};

export const AllThemes: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-4">
      <div data-theme="light" className="p-4 bg-white">
        <h3>Light Mode</h3>
        <Button variant="primary">Click me</Button>
      </div>
      <div data-theme="dark" className="p-4 bg-gray-900">
        <h3>Dark Mode</h3>
        <Button variant="primary">Click me</Button>
      </div>
    </div>
  ),
};
```

## Color Transformation Rules

### Surface Colors
```
Light → Dark
#FFFFFF → #1F2937  (primary background)
#F9FAFB → #111827  (secondary background)
#F3F4F6 → #0F172A  (tertiary background)
```

### Text Colors
```
Light → Dark
#111827 → #F9FAFB  (primary text)
#374151 → #E5E7EB  (secondary text)
#6B7280 → #9CA3AF  (tertiary text)
```

### Brand Colors
Adjust for contrast, not just invert:
```
Primary Blue:
#2196F3 → #60A5FA  (lighter for dark BG)

Success Green:
#10B981 → #34D399  (lighter)

Error Red:
#EF4444 → #F87171  (lighter)

Warning Yellow:
#F59E0B → #FBBF24  (lighter)
```

### Borders & Dividers
```
#E5E7EB → #374151  (visible on dark)
#D1D5DB → #4B5563  (medium)
#9CA3AF → #6B7280  (subtle)
```

### Shadows
```
Light Mode: rgba(0, 0, 0, 0.1)
Dark Mode: rgba(0, 0, 0, 0.3)  (darker, more pronounced)
```

## Semantic Color Mapping

Maintain semantic meaning across themes:

```css
/* Semantic tokens */
:root {
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;
}

[data-theme="dark"] {
  --color-success: #34D399;  /* Lighter green */
  --color-warning: #FBBF24;  /* Lighter yellow */
  --color-error: #F87171;    /* Lighter red */
  --color-info: #60A5FA;     /* Lighter blue */
}
```

## Best Practices

### ✅ Do's
- Test contrast ratios (use WCAG checker)
- Adjust brand colors for readability
- Provide theme toggle in accessible location
- Persist user preference (localStorage)
- Use CSS variables for easy switching
- Test with real users in dark environments

### ❌ Don'ts
- Don't just invert all colors
- Don't use pure black (#000) as background (harsh)
- Don't forget to adjust shadows
- Don't ignore semantic colors (success, error, etc.)
- Don't make dark mode an afterthought

## Integration

### With Tailwind CSS
```js
// tailwind.config.js
module.exports = {
  darkMode: 'class',  // or 'media'
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#2196F3',
          dark: '#60A5FA',
        },
      },
    },
  },
};

// Usage
<div className="bg-white dark:bg-gray-900">
  <h1 className="text-gray-900 dark:text-gray-100">
```

### With CSS Modules
```css
/* Component.module.css */
.container {
  background: var(--bg-primary);
  color: var(--text-primary);
}

[data-theme="dark"] .container {
  /* Inherits CSS variables */
}
```

## Files Generated

1. **themes/colors.css** - CSS variable definitions
2. **components/ThemeToggle.tsx** - Theme switcher
3. **stories/ThemePreviews.stories.tsx** - Side-by-side comparisons
4. **docs/DarkModeGuide.md** - Usage documentation

## Summary

Automatic dark mode generation:
1. Analyzes light mode colors
2. Generates accessible dark palette
3. Creates theme system (CSS vars + toggle)
4. Updates Storybook stories
5. Maintains WCAG compliance

**Result:** Production-ready dark mode in minutes, not hours.
