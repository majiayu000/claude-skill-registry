---
name: component
description: |
  Create React components following Darkroom standards. Use when:
  - User says "create component", "new component", "add component"
  - User wants to build a UI element, widget, or reusable piece
  - User mentions a component name like "Button", "Header", "Card"
argument-hint: "[ComponentName]"
---

# Create Darkroom Component

Create a React component following Darkroom conventions.

## Structure

```
components/<name>/
├── index.tsx           # Component implementation
└── <name>.module.css   # Component styles
```

## Template

### index.tsx
```tsx
// 'use client' - Only add if component needs:
// - useState, useEffect, or other hooks
// - Event handlers (onClick, onChange, etc.)
// - Browser APIs (window, document, etc.)

import s from './<name>.module.css'

interface <Name>Props {
  children?: React.ReactNode
  className?: string
}

export function <Name>({ children, className }: <Name>Props) {
  return (
    <div className={`${s.<name>} ${className ?? ''}`}>
      {children}
    </div>
  )
}
```

### <name>.module.css
```css
.<name> {
  /* Component styles */
}
```

## Before You Start

If this component wraps or uses an external library (Radix, Framer Motion, GSAP, etc.):
1. **Fetch docs first** — run `/docs <library>` to get current API via context7
2. **Check version** — run `bun info <package>` before installing

Never implement against external library APIs from memory.

## Conventions

1. **Server Component by default** - Only add `'use client'` if needed
2. **CSS Module as `s`** - Always import as `s` for consistency
3. **Props interface** - Define explicitly, include `className` for composition
4. **Named export** - Use `export function`, not `export default`
5. **Image wrapper** - Use `import { Image } from '@/components/image'`
6. **Link wrapper** - Use `import { Link } from '@/components/link'`

## Arguments

- `$ARGUMENTS` - Component name (e.g., "Button", "Header")
- `--client` flag - Force client component

## Example

```
User: "create a Button component"
→ Creates components/button/index.tsx and button.module.css
```
