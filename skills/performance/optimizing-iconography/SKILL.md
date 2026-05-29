---
name: optimizing-iconography
description: Rules for using icons efficiently to maintain performance. Use when adding icons from Lucide React.
---

# Iconography and Assets

## When to use this skill
- Adding wayfinding icons (Pin, Map, Star).
- Implementing navigation icons (Menu, Auth, Cart).

## Best Practices
- **Dynamic Imports**: Do not import the entire library.
- **Consistency**: Use a fixed stroke width (usually `strokeWidth={2}`) for a cohesive look.
- **Colors**: Use Tailwind colors (e.g., `text-primary`, `text-yellow-500` for stars).

## Usage
```typescript
import { MapPin, Calendar, Users } from 'lucide-react';

const Features = () => (
    <div>
        <MapPin className="w-5 h-5 text-primary" />
        <span>Location</span>
    </div>
);
```

## Instructions
- **Accessibility**: Add `aria-hidden="true"` to decorative icons.
- **Sizing**: Keep icons in standard containers (`w-5 h-5` for text inline, `w-8 h-8` for headers).
