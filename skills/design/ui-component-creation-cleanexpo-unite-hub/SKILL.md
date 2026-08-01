---
name: ui-component-creation
description: Skill from CleanExpo/Unite-Hub
---

# UI Component Creation Skill
## shadcn/ui + Design System Patterns

**When to Use**: Creating new UI components

---

## CRITICAL: Read Design System First

**BEFORE generating any UI**: Read `/DESIGN-SYSTEM.md`

**Quality Gate**: 9/10 minimum on:
- Visual distinctiveness
- Brand alignment
- Accessibility

---

## Pattern: shadcn/ui Component

```typescript
'use client';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function MyComponent({ data }: { data: any }) {
  return (
    <Card className="p-6 border-border-subtle bg-bg-card">
      <h2 className="text-xl font-semibold text-text-primary mb-4">
        {data.title}
      </h2>
      <p className="text-text-secondary mb-4">
        {data.description}
      </p>
      <Button variant="default" className="bg-accent-500 hover:bg-accent-600">
        Action
      </Button>
    </Card>
  );
}
```

---

## Design Tokens (Required)

**Use these, not raw values**:

**Colors**:
- `bg-bg-card` (not `bg-white`)
- `text-text-primary` (not `text-gray-900`)
- `accent-500` (#ff6b35 orange)
- `border-border-subtle`

**Spacing**:
- Tailwind classes (p-4, mb-6, etc.)

---

## Forbidden Patterns

❌ `bg-white` (use `bg-bg-card`)
❌ `text-gray-600` (use `text-text-secondary`)
❌ `grid grid-cols-3 gap-4` without responsive (add `md:`, `lg:`)

---

## Required Patterns

✅ Design tokens from system
✅ All states (hover, focus, disabled)
✅ Responsive breakpoints
✅ Accessibility (aria-labels)

---

**Standard**: Use design tokens, implement all states, ensure accessibility
