---
name: preserve-ui
description: Preserve existing UI structure when modifying components - auto-applied
user-invocable: false
model: sonnet
---

# UI Preservation Protocol

When modifying ANY UI component, follow this protocol to avoid breaking existing layouts.

## Before Touching UI (MANDATORY)

### 1. Context Loading
```
MUST READ before any UI change:
1. The TARGET component file (entire file)
2. The PARENT component that renders it
3. 2-3 SIBLING components in same directory
4. The layout/page that contains the component
```

### 2. Pattern Identification
Before writing, identify and document:
- [ ] Grid system used (CSS Grid, Flexbox, custom)
- [ ] Spacing pattern (gap-4, space-y-6, etc.)
- [ ] Component structure (Card > CardHeader > CardTitle)
- [ ] Responsive breakpoints (sm:, md:, lg:)
- [ ] Animation patterns (if any)

### 3. Design Token Check
```bash
# Run mentally before adding styles:
grep -r "className=" src/components/ui/ | head -20
# What tokens do existing components use?
```

## Rules for UI Changes

### Extend, Don't Replace
```tsx
// BAD: Replacing existing structure
<div className="flex gap-4">  // Your new layout
  {children}
</div>

// GOOD: Adding within existing structure
<ExistingLayout>
  <NewFeature />  // Fits the pattern
</ExistingLayout>
```

### Match Siblings
If adding a new card to a grid of cards:
1. Read an existing card component
2. Match its: padding, border-radius, shadow, spacing
3. Use the SAME component (don't create a new one)

### Preserve Hierarchy
```
Page Layout
  └── Section Container
      └── Grid/Flex Container
          └── Card Components
              └── Content

DO NOT flatten this. Add at the appropriate level.
```

### Use Existing Components
Before creating anything new:
```bash
# Check what exists:
ls src/components/ui/
ls src/components/

# Use existing:
import { Card, CardHeader, CardContent } from "@/components/ui/card"
```

## Forbidden Actions

### Never Do
- Create new layout when parent already has one
- Use different spacing than sibling components
- Add new color tokens without checking theme
- Ignore existing responsive breakpoints
- Create a "similar but different" component
- Add inline styles when Tailwind classes exist

### Red Flags
If you're about to:
- Add a `<div>` just for styling → Check if parent handles it
- Create `MyCustomCard` → Use existing `Card` component
- Write `style={{}}` → Use Tailwind classes
- Add `grid-cols-3` → Check what siblings use

## Responsive Considerations

### Check Existing Breakpoints
```tsx
// Find the pattern in existing components:
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

// Match it exactly, don't invent new breakpoints
```

### Mobile-First
- Base styles for mobile
- Add complexity at larger breakpoints
- Test your mental model: "What happens at 320px?"

## Before Submitting UI Changes

### Visual Verification Checklist
- [ ] Does it look like it belongs? (Not obviously "new")
- [ ] Same spacing as neighbors?
- [ ] Same border/shadow treatment?
- [ ] Responsive at all breakpoints?
- [ ] Loading state matches other loading states?
- [ ] Empty state matches other empty states?
- [ ] Error state matches other error states?

### Integration Check
- [ ] Parent component still renders correctly?
- [ ] Sibling components unaffected?
- [ ] No layout shifts or jumps?
- [ ] Animations consistent with existing?

## Common Mistakes

### The "Fresh Start" Trap
```tsx
// You see messy code and think "I'll rewrite this properly"
// DON'T. The "messy" code probably handles edge cases you don't see.
// Extend it. Don't replace it.
```

### The "Better Way" Trap
```tsx
// You know a "better" way to do the layout
// DON'T change it unless asked. Consistency > Perfection.
// The codebase should look like ONE person wrote it.
```

### The Orphan Component
```tsx
// You create a component that doesn't match anything else
// It works, but it looks out of place
// DELETE IT. Use existing components or extend them.
```

## Summary

1. **Read before write** - Know the context
2. **Match, don't invent** - Use existing patterns
3. **Extend, don't replace** - Add to what's there
4. **Check siblings** - Your component should look like family
5. **Test visually** - Does it belong?
