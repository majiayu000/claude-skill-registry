---
name: design-component
description: Design components for Empathy Ledger - storyteller cards, story cards, and culturally sensitive UI patterns.
---

# Design Component

UI component patterns for Empathy Ledger with cultural sensitivity.

## When to Use
- Building storyteller/story cards
- Implementing data displays
- Adding AI content enrichment
- Creating profile components

## Quick Reference

### Card Data Hierarchy
1. **Always show**: name, avatar, cultural_background, story_count
2. **On card**: badges, top specialties, location
3. **On hover**: bio, all specialties, themes
4. **Profile only**: contact, full stories, connections

### Badge Priority
1. Elder (gold crown)
2. Featured (star)
3. Knowledge Keeper (book)
4. Verified (check)

### Cultural Colors
| Color | Meaning | Usage |
|-------|---------|-------|
| Amber | Wisdom | Elder badges |
| Emerald | Growth | Story counts |
| Purple | Sacred | Knowledge keeper |
| Terracotta | Connection | Cultural affiliation |

## Reference Files
| Topic | File |
|-------|------|
| Storyteller card data model | `refs/storyteller-card.md` |
| AI enrichment patterns | `refs/ai-enrichment.md` |
| Component patterns | `refs/component-patterns.md` |

## Key Patterns
```tsx
// Avatar with fallback
<Avatar>
  <AvatarImage src={url} alt={name} />
  <AvatarFallback>{initials}</AvatarFallback>
</Avatar>

// Badge
<Badge variant="elder">Elder</Badge>

// Card structure
<Card>
  <CardHeader>Avatar + Badges</CardHeader>
  <CardContent>Info + Metrics</CardContent>
  <CardFooter>Actions</CardFooter>
</Card>
```

## Anti-Patterns
❌ Auto-publish AI content
❌ Suggest connections without consent
❌ Skip cultural context display
❌ Use disrespectful terminology

## Related Skills
- `design-system-guardian` - Design tokens
- `cultural-review` - Cultural sensitivity
- `empathy-ledger-codebase` - Architecture
