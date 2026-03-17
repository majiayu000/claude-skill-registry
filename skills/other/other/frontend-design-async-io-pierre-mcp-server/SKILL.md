---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications.
user-invocable: true
---

# Pierre Frontend Design Skill

When generating UI components or modifying frontend code, follow these principles.

## Design System Quick Reference

### Brand Colors (use these, never raw hex)
```
pierre-violet: #7C3AED  → Primary actions, intelligence, AI
pierre-cyan: #06B6D4    → Data flow, connectivity
gradient-pierre         → Violet to Cyan (hero elements)

Three Pillars (semantic):
pierre-activity: #10B981  → Fitness, movement, energy
pierre-nutrition: #F59E0B → Food, fuel, nourishment
pierre-recovery: #6366F1  → Rest, sleep, restoration
```

### Typography
- Headings: `text-pierre-gray-900 font-semibold`
- Body: `text-pierre-gray-700`
- Secondary: `text-pierre-gray-500`
- Code: `font-mono text-sm bg-pierre-gray-100 px-2 py-1 rounded`

### Spacing Scale
Use only: `1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24` (Tailwind units)

## Component Requirements

### ALWAYS Use Design System Components

| Need | Use | Import from |
|------|-----|-------------|
| Clickable action | `<Button variant="...">` | `./ui` |
| Content container | `<Card>` | `./ui` |
| Status indicator | `<Badge variant="...">` | `./ui` |
| Form input | `<Input>` or `.input-field` class | `./ui` |
| Overlay | `<Modal>` | `./ui` |
| Confirmation | `<ConfirmDialog>` | `./ui` |
| Loading | `.pierre-spinner` class | CSS |

### Button Variants
- `primary` - Main actions (purple)
- `gradient` - Hero/CTA (violet→cyan)
- `secondary` - Secondary actions (white/gray)
- `danger` - Destructive actions (red)
- `success` - Positive actions (green)
- `outline` - Tertiary actions (transparent)

### Badge Variants
- `success` - Active, connected, healthy
- `warning` - Pending, attention needed
- `error` - Failed, disconnected, error
- `info` - Processing, informational
- `trial`, `starter`, `professional`, `enterprise` - API tiers

## Generation Rules

### DO
- Import components from `./ui` barrel export
- Use `pierre-*` color classes
- Apply `pierre-spinner` for all loading states
- Use `Card` for any elevated container
- Use `Badge` for any status text
- Follow spacing scale strictly

### NEVER
- Use raw `<button>` elements
- Use raw `<div className="border...">` for card-like content
- Create custom spinners
- Use raw hex colors like `bg-[#7C3AED]`
- Use non-pierre colors like `text-purple-600`
- Mix spacing values outside the scale

## Code Patterns

### Standard Component Structure
```tsx
import { Button, Card, CardHeader, Badge } from './ui';

export const FeatureComponent: React.FC<Props> = ({ data }) => {
  return (
    <Card>
      <CardHeader title="Title" subtitle="Description" />
      <div className="space-y-4">
        {/* Content */}
      </div>
      <div className="flex justify-end gap-2 mt-6">
        <Button variant="secondary">Cancel</Button>
        <Button variant="primary">Save</Button>
      </div>
    </Card>
  );
};
```

### List Item Pattern
```tsx
{items.map((item) => (
  <Card key={item.id} className="p-4">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <h3 className="text-lg font-medium text-pierre-gray-900">{item.name}</h3>
        <Badge variant={item.isActive ? 'success' : 'error'}>
          {item.isActive ? 'Active' : 'Inactive'}
        </Badge>
      </div>
      <Button variant="secondary" size="sm">Edit</Button>
    </div>
  </Card>
))}
```

### Loading State
```tsx
{isLoading ? (
  <div className="flex items-center justify-center h-64">
    <div className="pierre-spinner" />
  </div>
) : (
  <Content />
)}
```

### Empty State
```tsx
<div className="text-center py-12 text-pierre-gray-500">
  <p className="text-lg mb-2">No items yet</p>
  <p className="text-sm">Create your first item to get started</p>
  <Button variant="primary" className="mt-4">Create Item</Button>
</div>
```

## Accessibility Requirements

- Focus states: Use `.focus-ring` utility
- Color contrast: 4.5:1 minimum for text
- Touch targets: 44x44px minimum
- Keyboard navigation: All interactive elements must be focusable
- ARIA labels: Required for icon-only buttons

## After Writing UI Code

Always invoke the `design-system-guardian` agent to validate compliance.
