---
name: ui-patterns
description: "Opinionated UI constraints and patterns for building better interfaces. Focuses on accessibility, usability, and implementation best practices."
enabled: true
visibility: default
allowedTools: ["read", "write", "edit", "glob", "grep"]
---

# UI Patterns Skill

Opinionated constraints for building better, more usable interfaces.

## Core Principles

1. **Accessibility first** - Use accessible primitives, not custom implementations
2. **Performance matters** - Animate only transform/opacity, respect user preferences
3. **Convention over configuration** - Follow established patterns
4. **User respect** - Never block paste, always provide escape hatches

---

## Technical Stack

| Category | Default |
|----------|---------|
| CSS Framework | Tailwind CSS |
| Animation (JS) | motion/react |
| Class Logic | cn() utility (clsx + tailwind-merge) |
| Accessible Components | Base UI, React Aria, or Radix |

---

## Component Patterns

### Keyboard-Interactive Components

```
RULE: NEVER rebuild keyboard/focus behavior manually

Required: Use accessible primitives
- Dialogs → Base UI / Radix / React Aria
- Dropdowns → Base UI / Radix / React Aria
- Tabs → Base UI / Radix / React Aria
- Tooltips → Radix / Floating UI

Why: Custom implementations miss edge cases
- Focus trapping, focus restoration
- Arrow key navigation
- Screen reader announcements
- Escape key handling
```

### Icon-Only Buttons

```tsx
// ❌ Wrong
<button><Icon /></button>

// ✅ Correct
<button aria-label="Close dialog"><Icon /></button>
```

### Destructive Actions

```tsx
// Always require confirmation via AlertDialog

<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogTitle>Are you sure?</AlertDialogTitle>
    <AlertDialogDescription>
      This action cannot be undone.
    </AlertDialogDescription>
    <AlertDialogCancel>Cancel</AlertDialogCancel>
    <AlertDialogAction>Delete</AlertDialogAction>
  </AlertDialogContent>
</AlertDialog>
```

### Error Messages

```
RULE: Display errors near where the action happens

✅ Inline validation under form fields
✅ Toast/notification after action failure
❌ Generic error page
❌ Console-only errors
```

### Empty States

```
RULE: Always provide one actionable path forward

✅ "No items yet. Create your first item →"
❌ "No items"
```

---

## Animation Constraints

### General Rules

```
1. NO animations unless explicitly requested
2. Animate ONLY transform and opacity
3. Duration ≤ 200ms for interactions
4. ALWAYS respect prefers-reduced-motion
```

### Implementation

```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// Motion library pattern
import { motion } from 'motion/react'

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.2 }}
>
  Content
</motion.div>
```

---

## Typography Patterns

### Text Balance & Wrap

```tsx
// Headings: prevent orphans
<h1 className="text-balance">
  Heading that wraps nicely
</h1>

// Body text: better line breaks
<p className="text-pretty">
  Longer paragraph text
</p>

// Data/numbers: consistent width
<span className="tabular-nums">
  1,234.56
</span>
```

### Responsive Typography

```tsx
// Fluid type scale with clamp
className="text-[clamp(1rem,2vw,1.5rem)]"

// Or Tailwind responsive
className="text-base md:text-lg lg:text-xl"
```

---

## Form Patterns

### Never Block Paste

```tsx
// ❌ Never do this
<input onPaste={(e) => e.preventDefault()} />

// ✅ Always allow paste
<input />
```

### Input Validation

```tsx
// Prefer native validation + progressive enhancement

<input
  type="email"
  required
  pattern="[^@]+@[^@]+\.[^@]+"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  {error && error}
</span>
```

### Form Layout

```tsx
// Labels always visible, above inputs
<div className="flex flex-col gap-1.5">
  <label htmlFor="email" className="text-sm font-medium">
    Email
  </label>
  <input id="email" type="email" className="..." />
</div>
```

---

## Layout Patterns

### Container Queries (Modern)

```tsx
<div className="@container">
  <div className="@md:flex-row flex flex-col gap-4">
    {/* Responds to container, not viewport */}
  </div>
</div>
```

### Responsive Grid

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

### Sticky Elements

```tsx
<header className="sticky top-0 z-50 bg-white/80 backdrop-blur-sm">
  Navigation
</header>
```

---

## Color & Theme Patterns

### CSS Variables

```css
:root {
  --color-primary: 220 90% 56%;
  --color-background: 0 0% 100%;
  --color-foreground: 220 10% 10%;
}

.dark {
  --color-primary: 220 90% 66%;
  --color-background: 220 10% 10%;
  --color-foreground: 0 0% 98%;
}
```

### Usage with Tailwind

```tsx
<div className="bg-[hsl(var(--color-background))] text-[hsl(var(--color-foreground))]">
  <button className="bg-[hsl(var(--color-primary))]">
    Action
  </button>
</div>
```

---

## Common Anti-Patterns

### ❌ Avoid

| Pattern | Problem | Solution |
|---------|---------|----------|
| Custom focus ring | Inconsistent | Use focus-visible |
| onClick on div | Not keyboard accessible | Use button/link |
| Placeholder as label | Disappears on focus | Real label |
| Disabled submit | Confusing UX | Show validation errors |
| Horizontal scroll | Mobile unfriendly | Responsive design |
| Fixed heights | Content overflow | min-height or auto |

### ✅ Prefer

```tsx
// Focus states
className="focus-visible:ring-2 focus-visible:ring-offset-2"

// Semantic buttons
<button type="button" onClick={handleClick}>
  Click me
</button>

// Proper labels
<label htmlFor="field">Label</label>
<input id="field" />
```

---

## Checklist

Before completing UI work:

- [ ] All interactive elements are keyboard accessible
- [ ] Icon buttons have aria-labels
- [ ] Destructive actions require confirmation
- [ ] Errors display near the action
- [ ] Empty states have actionable paths
- [ ] Animations respect prefers-reduced-motion
- [ ] Paste is not blocked
- [ ] Focus states are visible
- [ ] Color contrast meets WCAG AA (4.5:1)
