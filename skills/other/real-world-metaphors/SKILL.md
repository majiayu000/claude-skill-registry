---
name: real-world-metaphors
description: UI patterns borrowed from the physical world feel immediately intuitive — cards feel graspable, carousels feel scrollable, drawers feel pullable. Use real-world metaphors deliberately to reduce the learning curve and make interactions feel natural. Use when designing layout patterns, gestures, or navigation paradigms.
metadata:
  priority: 6
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "card"
      - "carousel"
      - "drawer"
      - "metaphor"
      - "physical"
      - "skeuomorphic"
      - "gesture"
      - "swipe"
retrieval:
  aliases:
    - real world metaphors
    - skeuomorphism
    - physical ui patterns
    - card pattern
    - carousel
    - drawer navigation
  intents:
    - make ui feel intuitive
    - choose a layout pattern
    - design a card component
    - use familiar patterns
  examples:
    - should I use a card or a list here
    - make this feel more natural to interact with
    - which pattern fits this content best
---

# Real-World Metaphors in UI

UI patterns borrowed from the physical world reduce the learning curve because users already know how they work. A card feels like something you can pick up. A carousel feels like flipping through a stack. A drawer feels like it slides out from the side. These metaphors carry affordance — the user knows what to do before reading any instructions.

Use them deliberately, not decoratively.

## Common Metaphors and When to Use Them

### Card
A card is a bounded, self-contained unit of content — like a physical index card or a product on a shelf.

**Use when:**
- Content items are discrete and comparable (products, people, articles, tasks)
- Each item needs to be scanned quickly and potentially acted on
- Items benefit from a visual thumbnail, image, or icon

**Key properties:**
- Cards should be graspable: elevation (`--shadow-sm`), border-radius, and clear boundary
- All cards in a set should be the same width; height can vary with content
- One primary action per card — secondary actions appear on hover or inside a detail view
- Cards imply "I can pick this up and do something with it" — if nothing happens on click, use a list instead

### Carousel / Horizontal Scroll
A carousel borrows from the physical act of flipping through a stack or sliding items along a rail.

**Use when:**
- There are more items than fit the viewport and browsing is the primary mode
- Items have a natural visual order (steps, featured content, media)
- The user is expected to explore, not to find a specific item

**Caution:**
- Carousels hide content — important items should not live only inside a carousel
- Auto-advancing carousels reduce user control; prefer user-driven navigation
- On mobile, a horizontal scroll without explicit navigation dots feels more natural than arrows

### Drawer / Side Panel
A drawer slides in from an edge, like a physical desk drawer — it brings additional context without replacing the current view.

**Use when:**
- Secondary detail is needed without losing context of the main view
- Editing or configuring an item while keeping the list visible behind
- Mobile navigation patterns (hamburger menu opens a side drawer)

**Key properties:**
- The drawer should feel anchored to an edge — left for navigation, right for detail/settings
- Always provide a clear close action (× button and clicking outside)
- The content behind should dim slightly (overlay) to signal the drawer is a layer above

### Accordion
Like a physical folder that expands to reveal contents — collapses to save space, expands to show detail.

**Use when:**
- Content has a clear parent–child hierarchy
- Most users need only a few sections at a time
- Vertical space is constrained

### Tabs
Like physical divider tabs in a binder — select a tab to see its section.

**Use when:**
- Content is divided into mutually exclusive, peer-level sections
- The user switches between sections frequently
- All tabs are equally relevant to the same context

**Caution:** Tabs imply peer-level, equal-importance sections. Do not use tabs for hierarchical navigation (use breadcrumbs or sidebar instead).

### Tooltip
Like a sticky note attached to an object — appears on hover, provides brief additional context.

**Use when:**
- An icon or control needs a short label that would clutter the layout if always visible
- A term or value needs brief explanation in context

**Not a replacement for:** clear labels, inline help text, or documentation for complex features.

## Principles for Using Metaphors Well

1. **The metaphor should match the interaction** — a card that does nothing on click creates a false affordance
2. **Don't mix metaphors** — a carousel inside a card inside a drawer creates cognitive noise
3. **Mobile borrows different metaphors than desktop** — swipe-to-dismiss, bottom sheets, and pull-to-refresh are mobile-native; forcing them onto desktop feels wrong in both directions
4. **Elevation reinforces the metaphor** — a card without shadow doesn't feel graspable; a drawer without an overlay doesn't feel layered

## Review Checklist

- [ ] Does the chosen pattern match the physical metaphor users will intuit?
- [ ] Do cards have a clear primary action — not just decoration?
- [ ] Does the carousel or horizontal scroll have navigation affordance (dots, arrows, or partial next item visible)?
- [ ] Do drawers dim the background content to signal layering?
- [ ] Are physical metaphors consistent — the same pattern used for the same type of content throughout the product?
