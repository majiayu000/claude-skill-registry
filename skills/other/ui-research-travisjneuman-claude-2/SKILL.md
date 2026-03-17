---
name: ui-research
description: Research-first UI/UX design workflow. Use BEFORE any frontend visual work to research modern patterns, gather inspiration from real products, and avoid generic AI-generated looks. Mandatory prerequisite for quality UI work.
---

# UI Research

**Research before you design. Every time.**

This skill ensures UI work is informed by real-world inspiration, modern patterns, and human-centered design - not generic AI output.

**Essential Reference:** See [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md)

---

## When to Use This Skill

**ALWAYS use before:**

- Creating new UI components
- Designing landing pages
- Building dashboards or admin UIs
- Developing mobile app screens
- Any visual/frontend work

**This skill is MANDATORY for quality UI work.**

---

## Research Workflow

### Phase 1: Define (5 min)

Before searching, answer:

```
1. What am I building? (component, page, flow)
2. What platform? (web, iOS, Android, desktop)
3. What industry? (SaaS, e-commerce, fintech, etc.)
4. What feeling? (professional, playful, minimal, bold)
5. What constraints? (existing brand, tech stack, timeline)
```

### Phase 2: Research (15-30 min)

**Search Strategy:**

```bash
# For each UI task, search at least 3 sources:

# 1. Real products (MOST IMPORTANT)
Search: Mobbin, UI Sources, Refero
Why: See how real companies solved this problem

# 2. Curated galleries
Search: Land-book, Awwwards, Godly
Why: High-quality, vetted designs

# 3. Component patterns
Search: shadcn/ui, Collect UI, Dribbble
Why: Specific UI element inspiration
```

**Search Queries by Task:**

| Building     | Search Terms                                              |
| ------------ | --------------------------------------------------------- |
| Dashboard    | "analytics dashboard", "admin panel", "SaaS dashboard"    |
| Landing page | "[industry] landing page", "hero section", "pricing page" |
| Mobile app   | "[app type] iOS", "mobile [feature]", "[competitor] app"  |
| E-commerce   | "product page", "checkout flow", "cart design"            |
| Auth flows   | "login screen", "onboarding", "signup form"               |
| Settings     | "settings page", "profile settings", "preferences"        |

### Phase 3: Collect (10 min)

Save 5-10 examples that resonate. For each, note:

```
URL/Source: [where you found it]
What works: [specific elements you like]
Patterns: [repeating solutions across examples]
Unique: [what makes this stand out]
Adapt: [how to apply to our project]
```

### Phase 4: Analyze (10 min)

**Pattern Recognition:**

```
Common patterns across examples:
- Layout: [grid, spacing, hierarchy]
- Colors: [palette trends, contrast]
- Typography: [fonts, scale, weights]
- Components: [buttons, cards, forms]
- Interactions: [hover, transitions, feedback]
```

**Quality Checklist:**

- [ ] Found 3+ real shipped products (not concepts)
- [ ] Identified repeating patterns
- [ ] Noted unique differentiators
- [ ] Considered accessibility
- [ ] Checked mobile responsiveness

### Phase 5: Design Brief (5 min)

Before implementing, document:

```markdown
## UI Research Brief

### Inspiration Sources

- [Link 1]: [What to adopt]
- [Link 2]: [What to adopt]
- [Link 3]: [What to adopt]

### Key Patterns to Follow

- Layout: [specific approach]
- Color: [palette direction]
- Typography: [font choices]
- Components: [style decisions]

### Differentiation

- [What makes ours unique]
- [Brand personality elements]

### Technical Approach

- Component library: [shadcn/ui, etc.]
- Animation approach: [Framer Motion, CSS]
- Responsive strategy: [mobile-first, etc.]
```

---

## Source Selection Guide

### By Project Type

| Project          | Primary Sources         | Secondary               |
| ---------------- | ----------------------- | ----------------------- |
| **SaaS App**     | Mobbin, UI Sources      | Land-book, shadcn/ui    |
| **Landing Page** | Land-book, Godly        | Awwwards, One Page Love |
| **Mobile App**   | Mobbin, Screenlane      | Pttrns, Apple HIG       |
| **E-commerce**   | Baymard, Awwwards       | Mobbin, UI Sources      |
| **Dashboard**    | Dribbble, UI Sources    | Ant Design, Tremor      |
| **Portfolio**    | Awwwards, One Page Love | Godly, personal sites   |

### By Platform

| Platform           | Required Research                    |
| ------------------ | ------------------------------------ |
| **iOS**            | Apple HIG, Mobbin (iOS filter)       |
| **Android**        | Material 3, Mobbin (Android filter)  |
| **Web**            | Awwwards, Land-book, shadcn/ui       |
| **Desktop**        | Fluent 2, platform-specific apps     |
| **Cross-platform** | All of the above, find common ground |

---

## Avoiding the "AI Look"

### Red Flags to Avoid

```
GENERIC AI PATTERNS (Don't do these):
- Blue/purple gradient backgrounds
- Perfectly symmetrical everything
- Generic blob/wave decorations
- Undraw-style illustrations
- "Hero with laptop mockup" layouts
- Default color schemes unchanged
- Cookie-cutter card grids
- Overused glassmorphism
```

### Human Touch Elements

```
WHAT MAKES DESIGN FEEL HUMAN:
- Custom color palette with personality
- Intentional asymmetry
- Unique typography combinations
- Real photography or custom illustration
- Micro-interactions with character
- Subtle organic shapes
- Brand-specific details
- Thoughtful empty states
- Personality in copywriting
```

### Quality Signals

| Aspect        | Generic AI     | Human-Polished                   |
| ------------- | -------------- | -------------------------------- |
| **Color**     | Default blue   | Custom brand palette             |
| **Layout**    | Perfect grid   | Intentional variation            |
| **Images**    | Stock photos   | Custom/curated imagery           |
| **Copy**      | Lorem ipsum    | Real, personality-rich text      |
| **Animation** | Standard fades | Purposeful, branded motion       |
| **Details**   | None           | Hover states, micro-interactions |

---

## Research Tools

### Browser Extensions

- **Muzli** - Design inspiration feed
- **Panda** - News and inspiration dashboard
- **Stylify Me** - Extract site colors/fonts

### Screenshot Tools

- **Full Page Screen Capture** - Capture entire pages
- **Awesome Screenshot** - Annotate and save

### Organization

- **Figma** - Create mood boards
- **Notion** - Document research
- **Eagle** - Visual bookmark manager
- **Pinterest** - Quick collection

---

## Research Output Template

```markdown
# UI Research: [Component/Page Name]

## Context

- **Building:** [what]
- **Platform:** [where]
- **Constraints:** [limitations]

## Inspiration (5-10 sources)

### 1. [Company/Site Name]

- **URL:** [link]
- **Screenshot:** [attached]
- **What works:** [specific elements]
- **Adopt:** [what to use]

### 2. [Company/Site Name]

...

## Pattern Analysis

### Layout

- [Common layout patterns observed]

### Color

- [Palette trends]

### Typography

- [Font and scale patterns]

### Components

- [UI element patterns]

## Design Direction

### Must Have

- [Non-negotiable elements]

### Nice to Have

- [Enhancement opportunities]

### Avoid

- [Anti-patterns to skip]

## Technical Stack

- **Components:** [library choice]
- **Styling:** [approach]
- **Animation:** [library/method]
```

---

## Integration with Other Skills

After research, proceed to:

| Next Step             | Skill to Use            |
| --------------------- | ----------------------- |
| Visual implementation | `frontend-enhancer`     |
| Design system setup   | `generic-design-system` |
| UX flow design        | `generic-ux-designer`   |
| Animation work        | `ui-animation`          |
| Brand alignment       | `brand-identity`        |

---

## Quick Start Checklist

Before ANY UI work:

- [ ] Defined what I'm building
- [ ] Searched 3+ inspiration sources
- [ ] Collected 5+ relevant examples
- [ ] Identified repeating patterns
- [ ] Noted unique differentiators
- [ ] Created brief design direction
- [ ] Checked for "AI look" red flags
- [ ] Planned human touch elements

---

## See Also

- [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md) - Full source list with URLs
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual design tokens
- `frontend-enhancer` - For implementation after research
- `generic-design-system` - For design system work
- `graphic-design` - For visual design principles

---

_Research is not optional. It's the difference between generic and exceptional._
