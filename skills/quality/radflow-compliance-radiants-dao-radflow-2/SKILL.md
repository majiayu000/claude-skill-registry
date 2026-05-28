---
name: radflow-compliance
description: Audit and fix AI-generated or existing code for RadOS design compliance. Use after generating UI code or when reviewing PRs. Catches common mistakes like wrong shadows, hardcoded colors, missing components, and incorrect radius hierarchy.
compatibility: Requires RadFlow theme and design tokens
---

# RadFlow Compliance Audit

This skill audits code for **RadOS design system compliance**. Use it to catch and fix common AI-generated mistakes before they ship.

## When to Use

- After generating new UI code
- When reviewing pull requests
- When refactoring existing components
- When onboarding code from other projects

---

## HARD RULES (Never Break These)

These rules are **absolute** and must never be violated. Claude must self-audit code before submitting.

### Rule 1: NEVER use raw `<button>` elements
```tsx
// ❌ FORBIDDEN - Always use Button component
<button onClick={...} className="...">Click</button>

// ✅ REQUIRED
import { Button } from '@radflow/ui';
<Button onClick={...} variant="outline">Click</Button>
```

### Rule 2: NEVER use raw brand color names in className
```tsx
// ❌ FORBIDDEN - Direct brand color references
bg-sky-blue
text-sky-blue
bg-sun-yellow
text-sun-yellow
bg-sun-red
text-sun-red
bg-warm-cloud
bg-cream
hover:bg-sun-yellow

// ✅ REQUIRED - Use semantic tokens only
bg-surface-primary      // instead of bg-warm-cloud, bg-cream
bg-surface-secondary    // instead of bg-black
bg-surface-tertiary     // instead of bg-sun-yellow
text-content-primary    // instead of text-black
text-content-secondary  // instead of text-sun-yellow
border-edge-primary     // instead of border-black
border-edge-focus       // instead of border-sky-blue
```

### Rule 3: NEVER hardcode hex values in TypeScript/TSX
```tsx
// ❌ FORBIDDEN
value: '#888888'
color: '#FCE184'
backgroundColor: '#0F0E0C'

// ✅ REQUIRED - Use CSS variables or semantic tokens
// If you need a fallback color, use a semantic token reference
value: 'var(--color-content-tertiary)'
// Or reference from the design system
const color = baseColors.find(c => c.name === 'black')?.value
```

### Rule 4: NEVER use opacity on brand colors, only on semantic tokens
```tsx
// ❌ FORBIDDEN
bg-sky-blue/20
text-sun-yellow/50
border-sun-red/30

// ✅ REQUIRED - Opacity only on semantic tokens
bg-surface-tertiary/20
text-content-primary/50
border-edge-primary/30
```

### Rule 5: ALWAYS include full interaction states on clickable elements
```tsx
// ❌ FORBIDDEN - Partial interaction states
<button className="hover:bg-surface-secondary">

// ✅ REQUIRED - Full interaction state set
<Button variant="outline" />
// Or if custom element is absolutely necessary:
className="
  shadow-btn
  hover:-translate-y-0.5 hover:shadow-btn-hover
  active:translate-y-0.5 active:shadow-none
  focus:ring-2 focus:ring-edge-focus focus:ring-offset-2
  transition-all duration-200
"
```

### Rule 6: ALWAYS specify font family for headings and labels
```tsx
// ❌ FORBIDDEN - Relying on inherited fonts
<h3 className="text-lg font-semibold">Title</h3>

// ✅ REQUIRED - Explicit font family
<h3 className="text-lg font-semibold font-joystix">Title</h3>
// Or use semantic HTML elements which have @layer base styles
```

### Rule 7: NEVER create category/status badges with raw colors
```tsx
// ❌ FORBIDDEN - Color-coded badges with brand colors
const getBadgeColor = (type) => {
  switch(type) {
    case 'success': return 'bg-green/20 text-green';
    case 'warning': return 'bg-sun-yellow/20 text-sun-yellow';
  }
}

// ✅ REQUIRED - Use semantic status tokens
const getBadgeColor = (type) => {
  switch(type) {
    case 'success': return 'bg-surface-success text-content-success';
    case 'warning': return 'bg-surface-warning text-content-warning';
    case 'error': return 'bg-surface-error text-content-error';
    default: return 'bg-surface-secondary text-content-primary';
  }
}
```

### Rule 8: ALWAYS use Button component for any clickable action
```tsx
// ❌ FORBIDDEN - Any of these patterns
<button>...</button>
<div onClick={...}>...</div>
<span onClick={...} className="cursor-pointer">...</span>

// ✅ REQUIRED
<Button variant="primary|secondary|outline|ghost" size="sm|md|lg">
```

---

## Audit Categories

### 1. Component Duplication Check

**Problem:** AI often creates new components instead of using existing ones.

```bash
# Check what components exist
ls -la /components/ui/
```

**Common duplicates to catch:**

| If you see... | Use instead |
|---------------|-------------|
| `MyButton`, `CustomButton`, `StyledButton` | `<Button>` from `/components/ui/Button` |
| `MyCard`, `Container`, `Box` | `<Card>` from `/components/ui/Card` |
| `MyInput`, `TextField`, `TextInput` | `<Input>` from `/components/ui/Input` |
| `MyModal`, `Popup`, `Overlay` | `<Dialog>` from `/components/ui/Dialog` |
| `Wrapper`, `Layout` | Check if `<Card>` or semantic HTML works |

**Fix pattern:**
```tsx
// Before (wrong)
function MyCustomCard({ children }) {
  return <div className="bg-white rounded-lg shadow-md p-4">{children}</div>
}

// After (correct)
import Card from '@/components/ui/Card';
// Just use <Card>{children}</Card>
```

### 2. Shadow Compliance

**Problem:** AI defaults to Tailwind's blurred shadows.

**Find violations:**
```tsx
// Search for these patterns:
shadow-sm
shadow-md
shadow-lg
shadow-xl
shadow-2xl
box-shadow:.*blur
box-shadow:.*rgba.*\d+px  // blur radius present
```

**Correct shadows:**
```tsx
shadow-btn          // 0 1px 0 0 black (buttons resting)
shadow-btn-hover    // 0 3px 0 0 black (buttons hover)
shadow-card         // 2px 2px 0 0 black (cards)
shadow-card-lg      // 4px 4px 0 0 black (elevated cards)
shadow-card-hover   // 6px 6px 0 0 black (card hover)
shadow-none         // remove shadow (active state)
```

**Fix pattern:**
```tsx
// Before (wrong)
<div className="shadow-lg">
<div style={{ boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>

// After (correct)
<div className="shadow-card">
```

### 3. Color Token Compliance

**Problem:** AI hardcodes colors instead of using semantic tokens.

**Find violations:**
```tsx
// Search for these patterns:
bg-\[#
text-\[#
border-\[#
bg-yellow-
bg-gray-
text-gray-
border-gray-
#FCE184
#FEF8E2
#0F0E0C
rgb\(
rgba\(
```

**Correct tokens:**

| Wrong | Correct |
|-------|---------|
| `bg-[#FCE184]`, `bg-yellow-400` | `bg-surface-tertiary` |
| `bg-[#FEF8E2]`, `bg-white` | `bg-surface-primary` or `bg-surface-elevated` |
| `bg-[#0F0E0C]`, `bg-black` | `bg-surface-secondary` |
| `text-[#0F0E0C]`, `text-gray-900` | `text-content-primary` |
| `text-gray-500`, `text-gray-600` | `text-content-primary/50` (use opacity) |
| `border-gray-300` | `border-edge-primary` |
| `border-blue-500` | `border-edge-focus` |

**Fix pattern:**
```tsx
// Before (wrong)
<button className="bg-[#FCE184] text-[#0F0E0C] border-gray-300">

// After (correct)
<button className="bg-surface-tertiary text-content-primary border-edge-primary">
```

### 4. Border Radius Hierarchy

**Problem:** AI uses same radius everywhere regardless of nesting.

**The rule:** Each nesting level = parent radius ÷ 2

| Nesting Level | Radius | Class |
|---------------|--------|-------|
| Level 0 (Window/Modal) | 16px | `rounded-lg` |
| Level 1 (Card/Section) | 8px | `rounded-md` |
| Level 2 (Button/Input) | 4px | `rounded-sm` |
| Level 3 (Badge/Tag) | 2px | `rounded-xs` |

**Find violations:**
```tsx
// Check for same radius at multiple nesting levels
// Example of WRONG pattern:
<Modal className="rounded-lg">         // Level 0: OK
  <Card className="rounded-lg">        // Level 1: WRONG (should be rounded-md)
    <Button className="rounded-lg">    // Level 2: WRONG (should be rounded-sm)
```

**Fix pattern:**
```tsx
// Before (wrong - same radius everywhere)
<Dialog className="rounded-lg">
  <div className="rounded-lg p-4">
    <Button className="rounded-lg">Save</Button>
  </div>
</Dialog>

// After (correct - cascading radius)
<Dialog className="rounded-lg">
  <div className="rounded-md p-4">
    <Button className="rounded-sm">Save</Button>
  </div>
</Dialog>
```

### 5. Interaction States

**Problem:** AI forgets hover/active/focus states.

**Required states for interactive elements:**

```tsx
// Buttons MUST have:
hover:-translate-y-0.5    // lift up
hover:shadow-btn-hover    // deeper shadow
active:translate-y-0.5    // press down
active:shadow-none        // no shadow when pressed
focus:ring-2              // focus ring
focus:ring-edge-focus     // blue ring color
focus:ring-offset-2       // ring offset
transition-all            // smooth transitions
duration-200              // animation timing
```

**Find violations:**
```tsx
// Search for buttons/links missing these:
<button className="..."      // check for hover/active/focus
<a className="..."           // check for hover states
onClick={                    // interactive element needs states
```

**Fix pattern:**
```tsx
// Before (wrong - no interaction states)
<button className="bg-surface-tertiary border border-edge-primary rounded-sm">

// After (correct - full interaction)
<button className="bg-surface-tertiary border border-edge-primary rounded-sm
  shadow-btn hover:-translate-y-0.5 hover:shadow-btn-hover
  active:translate-y-0.5 active:shadow-none
  focus:ring-2 focus:ring-edge-focus focus:ring-offset-2
  transition-all duration-200">
```

### 6. Typography

**Problem:** AI uses wrong fonts or generic system fonts.

**Find violations:**
```tsx
// Search for these patterns:
font-sans
font-serif
font-inter
font-arial
font-roboto
font-system
```

**Correct fonts:**

| Usage | Font | Class |
|-------|------|-------|
| Headings, labels, buttons | Joystix | `font-joystix` |
| Body text, paragraphs | Mondwest | `font-mondwest` |
| Code, technical | PixelCode | `font-mono` |

### 7. Gray Color Usage

**Problem:** AI uses gray hex values instead of black with opacity.

**Rule:** RadOS has NO gray. Use black at reduced opacity.

**Find violations:**
```tsx
// Search for gray patterns:
gray-100
gray-200
gray-300
gray-400
gray-500
gray-600
gray-700
gray-800
gray-900
#[0-9a-fA-F]{6}  // check if it's a gray hex
```

**Fix pattern:**
```tsx
// Before (wrong)
<p className="text-gray-500">Muted text</p>
<div className="border-gray-300">

// After (correct)
<p className="text-content-primary/50">Muted text</p>
<div className="border-edge-primary/20">
```

### 8. Animation Timing

**Problem:** AI uses wrong easing or duration.

**Find violations:**
```tsx
// Search for these patterns:
ease-bounce
ease-in-out
duration-500
duration-700
duration-1000
animate-bounce
spring
```

**Correct values:**
- Easing: `ease-out` only
- Duration: 150ms (fades), 200ms (transforms), 300ms max
- No bounce, no spring physics

## Quick Audit Commands

Run these grep patterns to find violations:

```bash
# Shadow violations
grep -rn "shadow-sm\|shadow-md\|shadow-lg\|shadow-xl" --include="*.tsx"

# Hardcoded colors
grep -rn "bg-\[#\|text-\[#\|border-\[#" --include="*.tsx"
grep -rn "bg-gray-\|text-gray-\|border-gray-" --include="*.tsx"

# Wrong fonts
grep -rn "font-sans\|font-inter\|font-roboto" --include="*.tsx"

# Missing interaction states (buttons without hover)
grep -rn "<button" --include="*.tsx" | grep -v "hover:"

# Gradient usage (not allowed)
grep -rn "bg-gradient\|from-\|to-" --include="*.tsx"
```

## Compliance Checklist

After auditing, verify:

- [ ] No custom components that duplicate existing UI primitives
- [ ] All shadows use RadOS tokens (shadow-btn, shadow-card, etc.)
- [ ] No hardcoded hex colors or Tailwind color palette
- [ ] Border radius follows nesting hierarchy (16→8→4→2)
- [ ] All interactive elements have hover/active/focus states
- [ ] Typography uses Joystix/Mondwest/PixelCode
- [ ] No gray colors (use black with opacity)
- [ ] Animations use ease-out, ≤300ms
- [ ] No gradients
- [ ] Works in both light and dark mode

## Auto-Fix Suggestions

When you find violations, suggest these replacements:

| Find | Replace With |
|------|--------------|
| `shadow-md`, `shadow-lg` | `shadow-card` |
| `shadow-sm` | `shadow-btn` |
| `bg-white` | `bg-surface-elevated` |
| `bg-gray-100` | `bg-surface-primary` |
| `bg-yellow-*` | `bg-surface-tertiary` |
| `text-gray-*` | `text-content-primary` + opacity |
| `border-gray-*` | `border-edge-primary` + opacity |
| `rounded-lg` (on buttons) | `rounded-sm` |
| `rounded-lg` (on cards inside modals) | `rounded-md` |
| `font-sans` | `font-joystix` or `font-mondwest` |

## Report Format

After auditing, provide a summary:

```
## RadOS Compliance Report

### Summary
- ✅ Passed: X checks
- ⚠️ Warnings: X issues
- ❌ Violations: X issues

### Violations Found

1. **Shadow Compliance** (X issues)
   - Line 42: `shadow-lg` → should be `shadow-card`
   - Line 87: `shadow-md` → should be `shadow-btn`

2. **Color Tokens** (X issues)
   - Line 23: `bg-[#FCE184]` → should be `bg-surface-tertiary`

3. **Radius Hierarchy** (X issues)
   - Line 56: Button inside card uses `rounded-lg` → should be `rounded-sm`

### Recommended Fixes
[Provide specific code changes]
```
