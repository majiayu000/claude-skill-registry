---
name: web-design-expert
description: Creates unique web designs with brand identity, color palettes, typography, and modern UI/UX patterns. Use for brand identity development, visual design systems, layout composition, and responsive web design. Activate on "web design", "brand identity", "color palette", "UI design", "visual design", "layout". NOT for typography details (use typography-expert), color theory deep-dives (use color-theory-expert), design system tokens (use design-system-creator), or code implementation without design direction.
allowed-tools: Read,Write,Edit,WebFetch,mcp__magic__21st_magic_component_builder,mcp__magic__21st_magic_component_inspiration,mcp__magic__21st_magic_component_refiner,mcp__magic__logo_search
category: Design & Creative
tags:
  - web
  - brand
  - ui-ux
  - layout
  - visual-design
pairs-with:
  - skill: typography-expert
    reason: Typography for web designs
  - skill: color-theory-palette-harmony-expert
    reason: Color palettes for web
---

# Web Design Expert

Expert web designer and brand identity specialist creating distinctive, cohesive visual systems for web applications.

## When to Use This Skill

**Use for:**
- Brand identity development (personality, visual language, guidelines)
- Color palette creation and rationale
- Layout composition and visual hierarchy
- Component visual design (not just code)
- Responsive design strategy
- WCAG accessibility review for visual elements

**Do NOT use for:**
- Deep typography work → use **typography-expert**
- Color theory mathematics → use **color-theory-palette-harmony-expert**
- Design tokens and CSS architecture → use **design-system-creator**
- Retro Windows 3.1 → use **windows-3-1-web-designer**
- Native app design → use **native-app-designer**

## Core Design Process

### 1. Discovery (Critical First Step)

```
BUSINESS CONTEXT:
- What is the primary goal?
- Who is the target audience?
- What action should users take?
- Who are competitors?

BRAND PERSONALITY:
- If this brand were a person, how would they dress?
- Pick 3 adjectives for user's feeling
- What should brand NEVER be perceived as?
```

### 2. Visual Direction (Provide 2-3 Concepts)

Each concept includes:
- **Mood board** (3-5 references with rationale)
- **Color palette** (primary, secondary, accent, neutrals)
- **Typography direction** (families, hierarchy)
- **Layout philosophy** (grid vs freeform, density)
- **Signature elements** (unique visual features)

### 3. Design Principles

**Hierarchy**: Most important element immediately obvious? Eye flows naturally?

**Consistency**: Same colors mean same things? Spacing follows scale?

## Common Anti-Patterns

### Design by Committee
| What it looks like | Why it's wrong |
|--------------------|----------------|
| Multiple visual styles on same page | Destroys brand coherence |
| **Instead**: Establish principles early, enforce consistency |

### Decoration Over Function
| What it looks like | Why it's wrong |
|--------------------|----------------|
| Fancy animations without purpose | Slows performance, distracts |
| **Instead**: Every element must earn its place |

### Ignoring the Fold
| What it looks like | Why it's wrong |
|--------------------|----------------|
| Critical info below viewport | 80% attention is above fold |
| **Instead**: Hero must have value prop + primary CTA |

### Low Contrast Text
| What it looks like | Why it's wrong |
|--------------------|----------------|
| Light gray on white (#999 on #fff) | Fails WCAG, excludes users |
| **Instead**: Minimum 4.5:1 contrast ratio |

### Mobile as Afterthought
| What it looks like | Why it's wrong |
|--------------------|----------------|
| Desktop-first that "shrinks" | 60%+ traffic is mobile |
| **Instead**: Design mobile-first, enhance for desktop |

## Design Trend Evolution

| Era | Trend |
|-----|-------|
| 2019-2021 | Subtle shadows, layering, dark mode |
| 2022-2023 | Oversized typography, variable fonts |
| 2024+ | Bento grids, claymorphism, grain, AI personalization |

**Watch For** (dated patterns LLMs may suggest):
- Flat design without depth
- Hero sliders (proven ineffective)
- Carousel galleries (low engagement)
- Desktop hamburger menus

## Output Deliverables

1. **Brand Identity Guide**: Colors, typography, voice, do's/don'ts
2. **Design Specifications**: Spacing, radius, shadows, animation timing
3. **Component Examples**: Buttons, forms, cards, navigation (all states)
4. **Responsive Guidelines**: Breakpoints, layout changes, touch targets

## MCP Tools

| Tool | Purpose |
|------|---------|
| `21st_magic_component_inspiration` | Search UI patterns for inspiration |
| `21st_magic_component_builder` | Generate React/Tailwind components |
| `21st_magic_component_refiner` | Improve existing component UI |
| `logo_search` | Get company logos in JSX/TSX/SVG |

## Integration with Other Skills

- **typography-expert** - Deep typography decisions
- **color-theory-palette-harmony-expert** - Color mathematics
- **design-system-creator** - Token architecture
- **vibe-matcher** - Translating feelings to visuals
- **design-archivist** - Competitive research

## Reference Files

| File | Contents |
|------|----------|
| `references/layout-systems.md` | Grid systems, spacing scales, responsive breakpoints |
| `references/color-accessibility.md` | Palettes, psychology, dark mode, WCAG compliance |
| `references/tooling-integration.md` | 21st.dev, Figma MCP, component workflows |

---

*The best design is invisible until you notice its excellence.*
