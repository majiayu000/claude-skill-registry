---
name: radflow-design
description: Create distinctive RadOS-styled UI components with System 7 heritage and warm California aesthetics. Use when building new UI for RadFlow projects. Generates pixel-perfect, on-brand code that avoids generic AI patterns.
compatibility: Requires RadFlow theme and design tokens
---

# RadFlow Design Skill

Build production-grade UI that honors **Apple System 7's tactile computing aesthetic** while infusing Radiant's **warm, sun-drenched personality**. This skill generates pixel-perfect components that feel like physical objects you can touch.

## Design Philosophy

RadOS tells the story of **a sunset over Silicon Valley**:

```
--color-sun-yellow: #FCE184;     /* Late afternoon light */
--color-warm-cloud: #FEF8E2;     /* Cream-colored clouds */
--color-sunset-fuzz: #FCC383;    /* Warning: sun getting low */
--color-sun-red: #FF6B63;        /* Error: sun dipping below horizon */
--color-sky-blue: #95BAD2;       /* Clear California sky */
--color-green: #CEF5CA;          /* Success: new growth */
--color-black: #0F0E0C;          /* Night arrives */
```

## Before Coding: Pre-Flight Check

1. **Does this component already exist?** Check `/components/ui/` first
2. **Can existing components be composed?** Prefer composition over creation
3. **What nesting level is this?** Determines border radius (see below)

## Core Design Rules

### 1. Hierarchical Border Radius

**Rule: Each nesting level = parent radius ÷ 2**

| Nesting Level | Radius | Class | Examples |
|---------------|--------|-------|----------|
| Level 0 (Window) | 16px | `rounded-lg` | Modal, Dialog, Window, Page container |
| Level 1 (Child) | 8px | `rounded-md` | Card inside modal, Section |
| Level 2 (Grandchild) | 4px | `rounded-sm` | Button inside card, Input |
| Level 3 (Leaf) | 2px | `rounded-xs` | Badge inside button, Tag |

```
╭──────────────────────────────────────╮  ← Window (rounded-lg)
│  ╭────────────────────────────────╮  │  ← Card (rounded-md)
│  │  ╭────────────╮  ╭──────────╮  │  │  ← Buttons (rounded-sm)
│  │  │   Cancel   │  │   Save   │  │  │
│  │  ╰────────────╯  ╰──────────╯  │  │
│  ╰────────────────────────────────╯  │
╰──────────────────────────────────────╯
```

### 2. Hard Pixel Shadows (Light Mode)

**NEVER use blur radius in light mode.** Shadows are hard offsets only.

```tsx
// Correct - hard pixel shadows
className="shadow-btn"           // 0 1px 0 0 black
className="shadow-btn-hover"     // 0 3px 0 0 black
className="shadow-card"          // 2px 2px 0 0 black
className="shadow-card-lg"       // 4px 4px 0 0 black
className="shadow-card-hover"    // 6px 6px 0 0 black

// WRONG - blurred shadows
className="shadow-md"            // Tailwind default has blur
className="shadow-lg"            // Tailwind default has blur
style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}  // blur = wrong
```

### 3. Dark Mode = Glow Mode

In dark mode, hard shadows transform into **warm golden glows**:

```tsx
// Light mode: hard shadow
shadow-card: 2px 2px 0 0 var(--color-black)

// Dark mode: golden glow (automatic via CSS variables)
shadow-card: 0 0 12px rgba(252, 225, 132, 0.3)
```

### 4. Semantic Tokens Only

**NEVER hardcode colors.** Always use semantic tokens.

```tsx
// Correct - semantic tokens
className="bg-surface-primary text-content-primary border-edge-primary"
className="bg-surface-tertiary"  // Sun Yellow for CTAs

// WRONG - hardcoded colors
className="bg-[#FCE184]"
className="bg-yellow-400"
className="text-gray-900"
```

### 5. The "Lift and Press" Pattern

All interactive elements use physical button behavior:

```tsx
// Standard button interaction
className={cn(
  // Base
  "bg-surface-tertiary border border-edge-primary rounded-sm",
  // Shadow
  "shadow-btn",
  // Hover: lift up + deeper shadow
  "hover:-translate-y-0.5 hover:shadow-btn-hover",
  // Active: press down + no shadow
  "active:translate-y-0.5 active:shadow-none",
  // Focus: blue ring
  "focus:ring-2 focus:ring-edge-focus focus:ring-offset-2",
  // Transition
  "transition-all duration-200"
)}
```

### 6. Typography

| Role | Font | Class | Usage |
|------|------|-------|-------|
| Headings | Joystix | `font-joystix` | h1-h6, buttons, labels |
| Body | Mondwest | `font-mondwest` | Paragraphs, descriptions |
| Code | PixelCode | `font-mono` | Code blocks, technical |

## Component Class Recipes

### Primary Button
```
bg-surface-tertiary text-content-primary border border-edge-primary
rounded-sm shadow-btn hover:-translate-y-0.5 hover:shadow-btn-hover
active:translate-y-0.5 active:shadow-none focus:ring-2
focus:ring-edge-focus focus:ring-offset-2 transition-all duration-200
```

### Secondary Button
```
bg-surface-secondary text-content-tertiary border border-edge-primary
rounded-sm shadow-btn hover:-translate-y-0.5 hover:shadow-btn-hover
active:translate-y-0.5 active:shadow-none transition-all duration-200
```

### Card (Level 1)
```
bg-surface-elevated border border-edge-primary rounded-md shadow-card
hover:shadow-card-hover transition-shadow duration-200
```

### Input
```
bg-surface-primary border border-edge-primary rounded-sm px-3 py-2
focus:bg-surface-elevated focus:ring-2 focus:ring-edge-focus
focus:ring-offset-2 placeholder:text-content-primary/40
```

### Modal/Dialog (Level 0)
```
bg-surface-elevated border border-edge-primary rounded-lg shadow-card-lg
```

## Animation Guidelines

| Duration | Easing | Usage |
|----------|--------|-------|
| 150ms | ease-out | Fades, opacity, scale |
| 200ms | ease-out | Transforms, slides |
| 300ms | ease-out | Maximum for any UI |

**NEVER use:**
- Bounce easing (too playful/modern)
- Spring physics (too modern)
- Animations > 300ms (feels sluggish)

## Anti-Patterns (NEVER Do This)

### Visual Mistakes

```tsx
// WRONG: Blurred shadows
<div className="shadow-lg">  // Tailwind blur

// WRONG: Gray colors
<div className="text-gray-600 border-gray-300">

// WRONG: Gradients
<div className="bg-gradient-to-r from-yellow-400 to-orange-500">

// WRONG: Same radius everywhere
<Modal className="rounded-lg">
  <Card className="rounded-lg">     // Should be rounded-md
    <Button className="rounded-lg"> // Should be rounded-sm

// WRONG: Material/iOS patterns
<div className="shadow-xl backdrop-blur-lg">
```

### Code Mistakes

```tsx
// WRONG: Creating new components when existing ones work
function MyCustomButton() { ... }  // Use <Button> from @/components/ui

// WRONG: Hardcoded colors
className="bg-[#FCE184] text-[#0F0E0C]"

// WRONG: Missing interaction states
<button className="bg-surface-tertiary">  // No hover/active/focus

// WRONG: Using default Tailwind
rounded-lg    // Use rounded-sm/md/lg based on nesting
shadow-md     // Use shadow-btn/card/card-lg
text-gray-*   // Use text-content-primary/secondary
bg-gray-*     // Use bg-surface-primary/secondary
```

## Decision Tree: Which Component?

```
Need a clickable element?
├─ Primary action → <Button variant="primary">
├─ Secondary action → <Button variant="secondary">
├─ Destructive → <Button variant="destructive">
├─ Navigation → <a> or <Link>
└─ Icon only → <IconButton>

Need a container?
├─ Top-level page section → rounded-lg (Level 0)
├─ Content grouping → <Card> with rounded-md (Level 1)
├─ Inline grouping → rounded-sm (Level 2)
└─ Badge/tag → rounded-xs (Level 3)

Need user input?
├─ Single line → <Input>
├─ Multi-line → <Textarea>
├─ Selection → <Select> or <RadioGroup>
├─ Toggle → <Checkbox> or <Switch>
└─ File → <FileInput>

Need feedback?
├─ Success/error/warning → <Alert variant="...">
├─ Modal confirmation → <AlertDialog>
├─ Non-blocking message → <Toast>
└─ Loading → <Spinner> or skeleton
```

## Checklist Before Submitting

- [ ] Used existing components from `/components/ui/` where possible
- [ ] Border radius follows nesting hierarchy (16→8→4→2)
- [ ] Uses semantic tokens only (no hardcoded colors)
- [ ] Uses RadOS shadow tokens (shadow-btn, shadow-card, etc.)
- [ ] All buttons have hover/active/focus states
- [ ] No blurred shadows in light mode
- [ ] No gradients
- [ ] No gray colors (use black at opacity)
- [ ] Typography uses Joystix/Mondwest/PixelCode appropriately
- [ ] Animations ≤ 300ms with ease-out
- [ ] Works in both light and dark mode
