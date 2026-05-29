---
name: template-cloning
description: Clone and customize existing templates (landing pages, dashboards, admin panels) with style extraction, config-driven content, and theme customization
depends_on: []  # No dependencies (foundational skill)
complements:
  - sales-landing-page  # For conversion-optimized content structure
  - frontend-design     # For additional visual patterns
---

# Template Cloning Skill

**Focus**: Clone & customize approach for building UI from existing templates

**Source**: Landing page implementation (2026-01-14) using Shadcn template with jousefmurad.com style

---

## When to Use This Skill

Use template-cloning when:
- Building standard UI patterns (landing page, dashboard, admin panel)
- Reference design available to clone
- Time-to-value prioritized over custom architecture
- Tech stack matches available templates (React, Vue, etc.)

**DO NOT use for:**
- Highly custom applications with unique patterns
- When no suitable template exists
- Projects requiring specific frameworks not available in templates
- When learning the fundamentals is the goal

---

## Core Principle

**Clone & Customize > Build From Scratch**

Starting from working code is faster than building from zero. The skill is knowing WHAT to customize and HOW to extract design tokens from reference sites.

---

## Quick Decision Tree

```
Need UI?
├── Standard pattern (landing, dashboard)?
│   ├── Reference design available?
│   │   └── YES → Use this skill (template-cloning)
│   └── NO reference → Build from scratch or use generic template
└── Custom/unique pattern?
    └── Build from scratch (no template advantage)
```

---

## Workflow Overview

```
1. RESEARCH     → Find templates matching tech stack
2. ANALYZE      → Extract design tokens from reference site
3. CLONE        → Clone template, strip placeholder content
4. CONFIGURE    → Create centralized content config
5. THEME        → Apply extracted design tokens (colors, fonts)
6. CUSTOMIZE    → Update components to use config
7. VERIFY       → Build + visual check
```

See [WORKFLOW.md](WORKFLOW.md) for detailed steps.

---

## File Organization

```
.claude/skills/template-cloning/
├── SKILL.md          # This file - overview and decision tree
├── WORKFLOW.md       # Step-by-step workflow
├── STYLE-EXTRACTION.md # How to extract design tokens from reference sites
└── CONFIG-PATTERN.md # Config-driven content pattern
```

---

## Key Patterns

### 1. Config-Driven Content

All editable content in single file:
```typescript
// src/config/content.ts
export const siteConfig = {
  name: "Company Name",
  tagline: "Your value proposition",
  cta: { text: "Get Started", href: "/signup" }
};

export const services = [...];
export const testimonials = [...];
export const faqItems = [...];
```

**Benefits**:
- Non-developers can edit content
- Content changes don't touch components
- Single source of truth
- Easy A/B testing

See [CONFIG-PATTERN.md](CONFIG-PATTERN.md) for full pattern.

### 2. Style Extraction

Extract exact values from reference sites:
- Colors (HSL for CSS variables)
- Fonts (family, weights, letter-spacing)
- Spacing (section padding, gaps)
- Component patterns (layouts, cards)

**Tools**: Browser DevTools, Playwright scripts

See [STYLE-EXTRACTION.md](STYLE-EXTRACTION.md) for methods.

### 3. Theme Customization

Apply extracted tokens via CSS variables:
```css
:root {
  --background: 0 0% 5.5%;      /* Near black */
  --foreground: 38 25% 90%;     /* Off-white */
  --primary: 38 35% 75%;        /* Gold accent */
}
```

**Pattern**: HSL values enable easy theming with opacity modifiers.

---

## Template Sources

### React/Next.js
- **Shadcn Landing Page** (1.8k stars) - React + Tailwind + shadcn/ui
- **Cruip** - Premium quality, various categories
- **Next SaaS Starter** - Full SaaS boilerplate
- **Page UI** - Customizable blocks

### Vue
- **Nuxt UI** - Vue 3 component library
- **Vuetify** - Material Design components

### General
- **Tailwind UI** (paid) - Official Tailwind templates
- **Open source alternatives** on GitHub

---

## Quality Checklist

Before completing template clone:

- [ ] All placeholder content replaced with config
- [ ] Theme colors match reference site
- [ ] Fonts loaded correctly (check Network tab)
- [ ] Responsive at mobile/tablet/desktop
- [ ] Build succeeds without TypeScript errors
- [ ] No placeholder images remain
- [ ] Links point to correct destinations
- [ ] Meta tags updated (title, description, OG)

---

## Common Pitfalls

### 1. Partial Customization
**Problem**: Some components still have placeholder content
**Solution**: Grep for "Lorem", "example", placeholder URLs

### 2. Missing Font Loading
**Problem**: Fonts declared in CSS but not imported
**Solution**: Verify font files load in Network tab

### 3. Hardcoded Content
**Problem**: Content scattered across components
**Solution**: Centralize ALL editable content in config file

### 4. Broken Responsive Design
**Problem**: Customizations break mobile layout
**Solution**: Test at 320px, 768px, 1024px, 1440px widths

---

## References

- **Implementation Guide**: [Config-Driven Content](../../../docs/guides/config-driven-content.md)
- **Related Skill**: [frontend-design](../frontend-design/) - UI design patterns
- **Example**: `landing-page/` directory (2026-01-14 implementation)
