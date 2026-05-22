---
name: design
description: Creates distinctive UI with preserved structure. Avoids generic AI aesthetics. Use when designing or refining user interfaces.
triggers:
  - design
  - ui
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
user-invocable: true
---

# Frontend Design

Create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.

## When to Use

- Building web components, pages, or applications
- Creating marketing/landing pages
- UI that needs to look professionally designed
- Any frontend where visual quality matters

## Design Thinking

Before coding, commit to a **BOLD aesthetic direction**:

1. **Purpose**: What problem does this solve? Who uses it?
2. **Tone**: Pick an extreme:
   - Brutally minimal
   - Maximalist chaos
   - Retro-futuristic
   - Organic/natural
   - Luxury/refined
   - Playful/toy-like
   - Editorial/magazine
   - Brutalist/raw
   - Art deco/geometric
   - Soft/pastel
   - Industrial/utilitarian
3. **Differentiation**: What makes this UNFORGETTABLE?

Choose a clear direction and execute with precision. Bold maximalism and refined minimalism both work - the key is **intentionality, not intensity**.

## Implementation

Create working code (React/Vue/HTML) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with clear aesthetic point-of-view
- Meticulously refined in every detail
- **Responsive across mobile (375px), tablet (768px), and desktop**

## Responsive Design (MANDATORY)

Every layout must adapt to mobile-first breakpoints:

| Pattern | Mobile | Tablet+ | Desktop+ |
|---------|--------|---------|----------|
| Sidebar | Hidden + hamburger | Collapsed icons | Full sidebar |
| Grid | 1 column | 2 columns | 3-4 columns |
| Navigation | Bottom tabs or drawer | Side nav | Full nav |
| Cards | Full-width stack | 2-up grid | 3-4 up grid |
| Modals | Full-screen sheet | Centered dialog | Centered dialog |
| Tables | Card view or scroll | Horizontal scroll | Full table |

```tsx
// Mobile-first: hidden sidebar with toggle
<Sheet>
  <SheetTrigger className="md:hidden"><Menu /></SheetTrigger>
  <SheetContent side="left">
    <Nav />
  </SheetContent>
</Sheet>
<aside className="hidden md:flex md:w-64 md:flex-col">
  <Nav />
</aside>
```

Test at 375px width before considering any UI complete.

## Aesthetics Guidelines

### Typography
- Choose **unique, interesting fonts** - avoid generic fonts
- Pair distinctive display font with refined body font
- Use Google Fonts or custom fonts, not system defaults

### Color & Theme
- Commit to a cohesive palette
- Use CSS variables for consistency
- **Dominant colors with sharp accents** > timid, evenly-distributed palettes

### Motion
- Use animations for micro-interactions
- CSS-only for HTML, Motion library for React
- Focus on high-impact moments: orchestrated page load with staggered reveals
- Scroll-triggering and hover states that surprise

### Spatial Composition
- Unexpected layouts
- Asymmetry, overlap, diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

### Backgrounds & Visual Details
- Create atmosphere and depth (not just solid colors)
- Gradient meshes, noise textures, geometric patterns
- Layered transparencies, dramatic shadows
- Decorative borders, custom cursors, grain overlays

## Avoid

**Generic AI aesthetics to avoid:**
- Inter, Roboto, Arial, system fonts
- Purple/blue gradients on white backgrounds
- Predictable layouts and component patterns
- Cookie-cutter designs lacking character
- Space Grotesk (overused)
- Same design across generations — vary themes, fonts, aesthetics

No design should be the same. Interpret creatively and make unexpected choices that feel genuinely designed for the context.

## Pro Tips

### Generate Multiple Variants
Ask for 5 different designs on /1, /2, /3, /4, /5:
- Model makes each unique from the others
- Better variety than 5 separate prompts
- Reveals model's template biases

### Iterate on Favorites
After seeing variants, tell the model:
- Which designs you liked
- What you liked about them
- Ask for 5 more iterations based on those

This is where Opus shines - it actually understands your preferences and iterates meaningfully.

## Match Complexity to Vision

- **Maximalist designs** → elaborate code, extensive animations, effects
- **Minimalist designs** → restraint, precision, spacing, typography, subtle details

Elegance comes from executing the vision well.

---

## Detailed Rules

Load specific references for engineering quality:

| Reference | When to Load |
|-----------|--------------|
| `references/web-interface-guidelines.md` | Forms, focus states, animation, a11y, dark mode, touch, i18n |

## Component Composition

Avoid boolean prop proliferation. Use composition:

```tsx
// Bad - boolean explosion
<Card isCompact isHighlighted hasBorder isClickable />

// Good - composition
<Card variant="compact">
  <Card.Highlight>
    <Card.Clickable>...</Card.Clickable>
  </Card.Highlight>
</Card>
```

Create explicit variant components instead of boolean modes. Use compound components with shared context for complex UI.

---

## Integration with Other Skills

| Skill | How It Integrates |
|-------|-------------------|
| `standards` | Ensure new designs use semantic tokens, handle all states |
| `audit` | Design issues flagged here inform UI/UX audit agent |
| `brainstorm` | Feature proposals validated against design system |

**Before creating new components:**
1. Check the Preserve UI Structure section below - can we extend existing?
2. Check design tokens - use CSS variables
3. Check `standards` - handle loading/empty/error states

---

Remember: Claude is capable of extraordinary creative work. Don't hold back - show what can be created when thinking outside the box and committing fully to a distinctive vision.

---

## Preserve UI Structure

When modifying existing UI: **read before write, match don't invent, extend don't replace.**

Key rules:
1. Read the target, parent, siblings, and layout before touching anything
2. Match existing grid, spacing, component patterns exactly
3. Use existing components — never create "similar but different" ones
4. Check all breakpoints match siblings

Load `references/preserve-ui.md` for the full protocol, checklists, and common traps.
