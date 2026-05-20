---
name: shadcn-ui
description: |
  Implements shadcn/ui accessible components with Radix UI primitives for the Bookkeep frontend.
  Use when: building UI with Dialog, Button, Badge, Tabs, Card, Form, or other shadcn components; combining components for complex interfaces; implementing accessible patterns.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# shadcn/ui Skill

Bookkeep uses shadcn/ui with Radix UI primitives in `src/components/ui/`. Components use CVA for variants, `cn()` for class merging, and integrate with the custom dark theme via CSS variables.

## Quick Start

### Button with Variants

```tsx
import { Button } from '@/components/ui/button';

// Default with primary glow shadow
<Button>Submit Request</Button>

// Variants: default, destructive, outline, secondary, ghost, link
<Button variant="outline" size="sm">Cancel</Button>
<Button variant="destructive">Delete</Button>

// As child (renders as Link/anchor)
<Button asChild>
  <Link to="/settings">Settings</Link>
</Button>
```

### Dialog with Form

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent className="sm:max-w-md bg-card border-border">
    <DialogHeader>
      <DialogTitle>Request Book</DialogTitle>
      <DialogDescription>Select your preferred format</DialogDescription>
    </DialogHeader>
    {/* Form content */}
    <div className="flex justify-end gap-3">
      <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
      <Button onClick={handleSubmit}>Submit</Button>
    </div>
  </DialogContent>
</Dialog>
```

### Badge for Status

```tsx
import { Badge } from '@/components/ui/badge';

// Variants: default, secondary, destructive, outline
<Badge variant="secondary">Pending</Badge>
<Badge variant="outline" className="border-destructive/40 text-destructive">Not Found</Badge>
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `cn()` | Merge Tailwind classes | `cn('base', condition && 'active')` |
| CVA variants | Type-safe style variants | `buttonVariants({ variant: 'ghost' })` |
| `asChild` | Polymorphic rendering via Slot | `<Button asChild><Link>...</Link></Button>` |
| `forwardRef` | Expose DOM ref to parent | All components support `ref` prop |
| CSS variables | Theme colors from `:root` | `bg-primary`, `text-muted-foreground` |

## Component Location

All primitives in `src/components/ui/` (kebab-case filenames):
- `button.tsx`, `dialog.tsx`, `badge.tsx`, `tabs.tsx`, `card.tsx`
- `form.tsx` (react-hook-form integration)
- `select.tsx`, `checkbox.tsx`, `input.tsx`, `textarea.tsx`

## See Also

- [patterns](references/patterns.md) - Component composition patterns
- [workflows](references/workflows.md) - Adding components, form handling

## Related Skills

For styling patterns, see the **tailwind** skill. For TypeScript interfaces, see the **typescript** skill. For form state management, see the **tanstack-query** skill (mutations). For React patterns, see the **react** skill.