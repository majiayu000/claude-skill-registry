---
name: palette-stylist
description: Create cohesive UI color systems from vibes and reference images. Use when starting a new page/component, unifying assets that feel off, or need consistent color tokens. Outputs core palette (primary, accent, background, surface, text), Tailwind config snippets, gradient suggestions, and accessibility notes.
---

# Palette Stylist (Farben-Chef)

Create cohesive UI color systems from vibes and reference images.

## When to Use

- Starting a new page/component
- Unifying assets that feel off
- Need consistent color tokens
- Colors are clashing or competing

## Process

### 1. Gather Input

Ask for:
- **Vibe words**: Adjectives + references (e.g., "night ice climbing, moody, magical forest")
- **Constraints**: Accessibility/brand requirements
- **Base colors**: Any existing hex colors to keep

### 2. Generate Palette

Output a complete color system:

| Token | Hex | Usage |
|-------|-----|-------|
| primary | #hexcode | Main brand/action color |
| primary-soft | #hexcode | Lighter variant, hover states |
| accent | #hexcode | Highlight/CTA |
| background | #hexcode | Page background |
| surface | #hexcode | Cards, modals |
| text | #hexcode | Primary text |
| muted | #hexcode | Secondary text |

### 3. Tailwind Config

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: '#...',
      'primary-soft': '#...',
      accent: '#...',
      background: '#...',
      surface: '#...',
      text: '#...',
      muted: '#...',
    }
  }
}
```

### 4. Gradient Suggestions

Provide 2-3 gradient backgrounds with CSS and Tailwind classes:

```css
/* Hero gradient */
background: linear-gradient(180deg, #base 0%, #mid 50%, #base 100%);
/* Tailwind: bg-gradient-to-b from-[#base] via-[#mid] to-[#base] */
```

### 5. Accessibility Notes

- Check contrast ratios (WCAG AA = 4.5:1 for text)
- Note any problematic combinations
- Suggest alternatives for low-contrast pairs

## Example

**Vibe:** "Winter night, ice climbing, magical but professional"

**Palette:**
| Token | Hex | Usage |
|-------|-----|-------|
| primary | #1e3a5f | Headers, primary buttons |
| primary-soft | #2d4a6f | Hover states, borders |
| accent | #64b5f6 | CTAs, highlights |
| background | #0c1e2b | Page background |
| surface | #1a2f3d | Cards, modals |
| text | #e8f4fc | Primary text |
| muted | #8ba3b5 | Secondary text |

## Resources

- [Coolors.co](https://coolors.co) - Palette generation
- [Contrast Checker](https://webaim.org/resources/contrastchecker/) - WCAG validation
