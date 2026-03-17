---
name: designing-systems
description: Use when creating design systems, tokens, color palettes, typography scales, or theming. Covers OKLCH colors, CSS variables, Tailwind v4 @theme.
versions:
  tailwindcss: "4.1"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Task
references: references/color-system.md, references/typography.md, references/theme-presets.md, references/grids-layout.md, references/ui-hierarchy.md, references/ui-spacing.md, references/ui-trends-2026.md, references/gradients-guide.md, references/tailwind-config.md, references/tailwind-utilities.md, references/tailwind-performance.md
related-skills: generating-components, theming-tokens, dark-light-modes
---

# Designing Systems

## Agent Workflow (MANDATORY)

Before ANY design system work, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Find existing CSS variables, Tailwind config, colors
2. **fuse-ai-pilot:research-expert** - Verify latest OKLCH and Tailwind v4 patterns
3. **mcp__context7__query-docs** - Check Tailwind v4 @theme syntax

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **OKLCH Colors** | Wide gamut P3 color space |
| **CSS Variables** | Semantic token architecture |
| **Tailwind v4 @theme** | CSS-first configuration |
| **60-30-10 Rule** | Color distribution ratio |

---

## Critical Rules

1. **OKLCH only** - No hex or RGB for colors
2. **Forbidden fonts** - Inter, Roboto, Arial are BANNED
3. **CSS variables** - Never hard-code colors
4. **Analyze first** - Document existing system before changes
5. **Dark mode** - Always define both light and dark tokens

---

## Architecture

```
styles/
├── tokens/
│   ├── colors.css       (~50 lines)
│   ├── typography.css   (~30 lines)
│   └── spacing.css      (~20 lines)
└── app.css              (~40 lines - @import + @theme)
```

→ See [color-system.md](references/color-system.md) for token examples

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Colors** | [color-system.md](references/color-system.md) | OKLCH palettes, psychology |
| **Typography** | [typography.md](references/typography.md) | Fonts, scale, mobile sizes |
| **Theme Presets** | [theme-presets.md](references/theme-presets.md) | Brutalist, Solarpunk, etc. |
| **Grids** | [grids-layout.md](references/grids-layout.md) | 12-column, spacing |
| **UI Hierarchy** | [ui-hierarchy.md](references/ui-hierarchy.md) | Visual hierarchy patterns |
| **UI Spacing** | [ui-spacing.md](references/ui-spacing.md) | Spacing systems |
| **UI Trends** | [ui-trends-2026.md](references/ui-trends-2026.md) | 2026 design trends |
| **Gradients** | [gradients-guide.md](references/gradients-guide.md) | Gradient patterns |
| **Tailwind Config** | [tailwind-config.md](references/tailwind-config.md) | v4 @theme setup |
| **Tailwind Utils** | [tailwind-utilities.md](references/tailwind-utilities.md) | Utility patterns |
| **Tailwind Perf** | [tailwind-performance.md](references/tailwind-performance.md) | Performance tips |

### Templates

Templates are in generating-components skill for implementation examples.

---

## Quick Reference

### OKLCH Color Token

```css
:root {
  --color-primary: oklch(55% 0.20 260);
  --color-primary-foreground: oklch(98% 0.01 260);
}

.dark {
  --color-primary: oklch(65% 0.20 260);
}
```

→ See [color-system.md](references/color-system.md) for full palette

### Typography Scale

```css
--font-display: 'Clash Display', sans-serif;
--font-sans: 'Satoshi', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

→ See [typography.md](references/typography.md) for approved fonts

### Tailwind v4 @theme

```css
@import "tailwindcss";

@theme {
  --color-primary: var(--color-primary);
  --font-display: var(--font-display);
}
```

→ See [tailwind-best-practices.md](references/tailwind-best-practices.md) for config

---

## Best Practices

### DO
- Use OKLCH for wide gamut colors
- Define semantic tokens (primary, success, destructive)
- Support dark mode from the start
- Follow 60-30-10 color distribution
- Use approved fonts only

### DON'T
- Hard-code hex/RGB colors
- Use Inter, Roboto, Arial fonts
- Skip dark mode variables
- Create tokens without semantic meaning
- Mix color spaces (stick to OKLCH)
