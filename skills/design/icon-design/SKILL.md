---
name: icon-design
description: |
  Select semantically appropriate icons for websites using Lucide, Heroicons, or Phosphor. Covers concept-to-icon mapping, React/HTML templates, and tree-shaking patterns.

  Use when: building feature sections, service grids, contact info, navigation, or any UI needing icons. Prevents emoji usage, ensures consistency.
---

# Icon Design

Select the right icon for the job. Maps concepts to icons, provides templates, prevents common mistakes.

## Quick Reference (Top 20 Concepts)

| Concept | Lucide | Heroicons | Phosphor |
|---------|--------|-----------|----------|
| Award/Quality | `Trophy` | `trophy` | `Trophy` |
| Price/Value | `Tag` | `tag` | `Tag` |
| Location | `MapPin` | `map-pin` | `MapPin` |
| Expertise | `GraduationCap` | `academic-cap` | `GraduationCap` |
| Support | `MessageCircle` | `chat-bubble-left-right` | `ChatCircle` |
| Security | `Shield` | `shield-check` | `Shield` |
| Speed | `Zap` | `bolt` | `Lightning` |
| Phone | `Phone` | `phone` | `Phone` |
| Email | `Mail` | `envelope` | `Envelope` |
| User/Profile | `User` | `user` | `User` |
| Team | `Users` | `user-group` | `Users` |
| Settings | `Settings` | `cog-6-tooth` | `Gear` |
| Home | `Home` | `home` | `House` |
| Search | `Search` | `magnifying-glass` | `MagnifyingGlass` |
| Check/Success | `Check` | `check` | `Check` |
| Close/Cancel | `X` | `x-mark` | `X` |
| Menu | `Menu` | `bars-3` | `List` |
| Calendar | `Calendar` | `calendar` | `Calendar` |
| Clock/Time | `Clock` | `clock` | `Clock` |
| Heart/Favourite | `Heart` | `heart` | `Heart` |

## Library Selection

| Library | Best For | Package |
|---------|----------|---------|
| **Lucide** | General use, React projects | `lucide-react` |
| **Heroicons** | Tailwind projects, minimal style | `@heroicons/react` |
| **Phosphor** | Weight variations needed | `@phosphor-icons/react` |

**Default recommendation**: Lucide (1,400+ icons, excellent React integration)

See `references/library-comparison.md` for detailed comparison.

## Icon Style Rules

### Sizing

| Context | Tailwind Class | Pixels |
|---------|----------------|--------|
| Inline with text | `w-4 h-4` or `w-5 h-5` | 16-20px |
| Feature cards | `w-8 h-8` | 32px |
| Hero sections | `w-10 h-10` or `w-12 h-12` | 40-48px |
| Large decorative | `w-16 h-16` | 64px |

### Consistency Rules

1. **Never mix styles** - Use all outline OR all solid in a section
2. **Never use emoji** - Use proper icon components (tree-shakeable)
3. **Use currentColor** - Icons inherit text color via `stroke="currentColor"`
4. **Semantic colours** - Use `text-primary`, not `text-blue-500`

### Tree-Shaking (Critical)

Dynamic icon selection breaks tree-shaking. Use explicit maps:

```tsx
// BAD - all icons bundled
import * as Icons from 'lucide-react'
const Icon = Icons[iconName]  // Tree-shaken away!

// GOOD - explicit map
import { Home, Users, Settings, type LucideIcon } from 'lucide-react'
const ICON_MAP: Record<string, LucideIcon> = { Home, Users, Settings }
const Icon = ICON_MAP[iconName]
```

## Selection Process

1. **Identify the concept** - What does the label/title communicate?
2. **Check semantic mapping** - See `references/semantic-mapping.md`
3. **Choose library** - Lucide (default), Heroicons (Tailwind), Phosphor (weights)
4. **Apply template** - See `references/icon-templates.md`
5. **Verify consistency** - Same style, same size in section

## Decision Tree

When unsure which icon:

```
Is it about recognition/awards? → Trophy, Star, Award
Is it about money/price? → Tag, DollarSign, CreditCard
Is it about location? → MapPin, Globe, Map
Is it about people/team? → Users, UserGroup, User
Is it about communication? → MessageCircle, Phone, Mail
Is it about safety/trust? → Shield, Lock, ShieldCheck
Is it about speed/time? → Zap, Clock, Timer
Is it trade-specific? → Check semantic-mapping.md
Still unsure? → CheckCircle (generic positive) or Sparkles (generic feature)
```

## Resources

- `references/semantic-mapping.md` - Full concept→icon tables by category
- `references/icon-templates.md` - React/HTML patterns with Tailwind
- `references/library-comparison.md` - Lucide vs Heroicons vs Phosphor
- `references/migration-guide.md` - FA/Material → modern equivalents
- `rules/icon-design.md` - Correction rules for projects
