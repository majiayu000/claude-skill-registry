---
name: design-tokens
description: Pulse Radar design system - semantic colors, spacing grid, component patterns.
---

# Design Tokens Skill

## Token Import
```typescript
import { semantic, status, atom, badges, cards, gap } from '@/shared/tokens';
```

## Color Categories

### Semantic (general purpose)
```typescript
semantic.success.bg   // "bg-semantic-success"
semantic.warning.text // "text-semantic-warning"
semantic.error.border // "border-semantic-error"
semantic.info.ring    // "ring-semantic-info"
```

### Status (connection states)
```typescript
status.connected   // Green - active, success
status.validating  // Blue - processing
status.pending     // Yellow - waiting
status.error       // Red - failed
```

### Atom Types
```typescript
atom.problem      // Red
atom.solution     // Green
atom.decision     // Blue
atom.question     // Yellow
atom.insight      // Purple
atom.pattern      // Cyan
atom.requirement  // Violet
```

## Spacing (4px Grid)

```typescript
// ONLY multiples of 4!
gap.xs   // 4px  (gap-1)
gap.sm   // 8px  (gap-2)
gap.md   // 16px (gap-4)
gap.lg   // 24px (gap-6)
gap.xl   // 32px (gap-8)
```

**Forbidden:** gap-3, gap-5, gap-7, p-3, p-5, m-7

## Patterns

### Badge with Status
```typescript
<Badge className={badges.status.connected}>
  <CheckCircle className="h-3.5 w-3.5" />
  Connected
</Badge>
```

### Interactive Card
```typescript
<Card className={cards.interactive}>
  <CardContent className={gap.md}>
    Content
  </CardContent>
</Card>
```

## ESLint Enforcement
- `no-raw-tailwind-colors` — blocks bg-red-*, text-green-*
- `no-odd-spacing` — blocks gap-3, p-5, m-7
- `no-heroicons` — only lucide-react allowed

## References
- @references/css-variables.md — Full CSS custom properties list
- @references/patterns.md — All UI patterns (badges, cards, forms, lists)