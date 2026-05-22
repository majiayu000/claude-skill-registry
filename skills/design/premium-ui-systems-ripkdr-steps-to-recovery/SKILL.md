---
name: premium-ui-systems
description: Comprehensive system for building exceptional, production-ready UIs that avoid generic "vibe-coded" aesthetics. Use when building any web interface (dashboards, landing pages, SaaS products, React components, HTML/CSS layouts) to create distinctive, systematically premium designs. Covers hierarchy-first methodology, systematic design tokens, glassmorphism patterns, component libraries, creative direction, and avoiding AI-generated template aesthetics. Applies to Next.js, React, HTML/CSS, Tailwind, or any frontend stack.
---

# Premium UI Systems

Build exceptional interfaces with systematic quality and distinctive aesthetic. This skill prevents "vibe-coded" UI—the template look that results from applying effects before solving structure.

## Quick Decision Tree

```
Are you building UI? → Start here ↓

┌─ Step 1: What are you building?
│  ├─ Dashboard/Data UI → [Dashboard Workflow](#dashboard-workflow)
│  ├─ Landing/Marketing → [Marketing Workflow](#marketing-workflow)
│  └─ Product Feature/App → [Product Workflow](#product-workflow)
│
├─ Step 2: Does it look "vibe-coded"?
│  └─ Run [De-Vibe Audit](#de-vibe-audit) → Fix foundation first
│
└─ Step 3: Ready to polish?
   └─ Apply [Premium Pass](#premium-pass) → Systematic refinement
```

---

## De-Vibe Audit

**CRITICAL**: Run this before adding features. Order matters—fix foundation before effects.

### Visual Tests (30 seconds)

1. **Grayscale test**: Convert to grayscale—hierarchy should still be obvious
2. **Effects-off test**: Mentally remove glass/glow/motion—still premium?
3. **Squint test**: Squint at screen—can you identify the primary action?

### Foundation Checklist

| Area            | Quick Check                         | Common Fix                                    |
| --------------- | ----------------------------------- | --------------------------------------------- |
| **Hierarchy**   | One dominant element per screen?    | Strengthen primary with size/weight/placement |
| **Spacing**     | Consistent padding/margins?         | Adopt 4/8/12/16/24/32px scale                 |
| **Typography**  | Clear size hierarchy (3-4 sizes)?   | Define scale once, use everywhere             |
| **Radii**       | Same border-radius throughout?      | Pick 2 values: cards (16px), inputs (8px)     |
| **Colors**      | Too many competing colors?          | 1 brand accent + neutral gray scale           |
| **Alignment**   | Everything on a grid?               | 8px grid alignment                            |
| **Consistency** | Same component behaves differently? | Standardize button/card/input patterns        |

### Symptoms Diagnostic

| Symptom                 | Root Cause              | Fix                                      |
| ----------------------- | ----------------------- | ---------------------------------------- |
| "Looks like a template" | Inconsistent tokens     | Audit radii/spacing/shadows—standardize  |
| "Too busy/noisy"        | Weak hierarchy          | Grayscale test → strengthen scale/weight |
| "Feels cheap"           | Low contrast on effects | Test worst-case backgrounds → go solid   |
| "Demo reel energy"      | Motion without purpose  | Cut to 2-4 meaningful transitions        |
| "Doesn't feel cohesive" | Mixed conventions       | One button hierarchy, one modal pattern  |

**Failed the audit?** → Fix foundation first. Effects won't save weak structure.

**Passed?** → Continue to workflow-specific guidance below.

---

## Dashboard Workflow

### Structure

```
┌─────────────────────────────────────────────────────┐
│  KPI ROW (3-7 metrics with deltas)                  │  ← "How are we doing?"
├─────────────────────────────────────────────────────┤
│  TREND BAND (1-3 charts)                            │  ← "Why?"
├─────────────────────────────────────────────────────┤
│  ACTION TABLE (where users do work)                 │  ← "What do I do?"
└─────────────────────────────────────────────────────┘
```

### Critical Rules

- **Solid surfaces for data**: Tables, KPI cards, charts → always solid backgrounds
- **Glass only for chrome**: Nav, filters, toolbars → translucent OK
- **Direct labeling**: Annotate charts directly, avoid legends when possible
- **Sticky headers**: Tables need sticky headers for scanning
- **Clear row rhythm**: Consistent row height, hover states

**Detailed guide**: [references/dashboard-patterns.md](references/dashboard-patterns.md)

---

## Marketing Workflow

### Hero Anatomy

```
┌─────────────────────────────────────────────────────┐
│  [Logo]                    [Nav]    [CTA]           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ONE HEADLINE (what you do)                         │
│  Subhead (for whom / why now)                       │
│                                                     │
│  [Primary CTA]  [Secondary CTA]                     │
│                                                     │
│  [Product Screenshot / Demo / Hero Moment]          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Critical Rules

- **One story per viewport**: Each section answers one question
- **Card hierarchy in bento**: Varied sizing shows importance (no box soup)
- **One hero moment**: One 3D effect/parallax/animation per page max
- **Glass for atmosphere**: Hero backgrounds, footer CTAs OK for glass
- **Bold typography**: Marketing allows expressive display fonts

**Detailed guide**: [references/marketing-patterns.md](references/marketing-patterns.md)

---

## Product Workflow

Building core product features? Follow this sequence:

### 1. Foundation First

- Define component hierarchy (primary/secondary/tertiary buttons)
- Establish spacing scale and apply everywhere
- Set up typography scale (3-4 sizes maximum)
- Create color tokens (1 brand accent, neutral scale)

### 2. Build Solid

- All forms/tables/dense content on solid surfaces
- Test readability in worst-case scenarios
- Ensure interactive states are obvious

### 3. Add Chrome (Selective)

- Glass only for layering (nav, sheets, toolbars)
- Motion only for feedback (150-220ms, purposeful)
- One hero moment if marketing-adjacent

### 4. Polish

- Consistent component geometry (radii, elevation)
- Microinteractions for key actions only
- Respect `prefers-reduced-motion`

**Detailed guide**: [references/foundation-first.md](references/foundation-first.md)

---

## Premium Pass

Systematic refinement checklist. Apply after foundation is solid.

### Token System

Define once, use everywhere:

```css
/* Spacing scale */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 24px;
--space-6: 32px;

/* Radii */
--radius-sm: 8px; /* inputs */
--radius-md: 12px; /* buttons */
--radius-lg: 16px; /* cards */
--radius-xl: 24px; /* modals */

/* Motion */
--duration-fast: 150ms;
--duration-base: 220ms;
--ease-out: cubic-bezier(0.33, 1, 0.68, 1);
```

### Glass System

Only use where it clarifies layering:

| Surface          | Glass OK?  | Notes                         |
| ---------------- | ---------- | ----------------------------- |
| Navigation       | ✅ Yes     | Sticky nav feels premium      |
| Filters/toolbars | ✅ Yes     | Chrome element                |
| Modals/sheets    | ✅ Yes     | Glass shell, solid insets     |
| Data tables      | ❌ No      | Readability critical          |
| Forms            | ❌ No      | Keep on solid                 |
| KPI cards        | ⚠️ Careful | Only if background controlled |

```tsx
// Chrome glass (nav, toolbars)
className = 'backdrop-blur-md bg-white/70 border border-white/20';

// Overlay glass (modals)
className = 'backdrop-blur-lg bg-white/80 border border-white/30';
```

### Motion Budget

Pick 2-4 transitions and reuse:

1. **Fade/slide** — Overlays, modals (150-220ms)
2. **Hover lift** — Cards, buttons (translateY -2px)
3. **Expand/collapse** — Accordions
4. **Page transitions** — Route changes (if any)

Always include:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Accessibility Validation

- [ ] Text contrast ≥ 4.5:1 (WCAG 1.4.3)
- [ ] Interactive elements ≥ 3:1 (WCAG 1.4.11)
- [ ] Reduced motion support (WCAG 2.3.3)
- [ ] Focus indicators visible
- [ ] Touch targets ≥ 44×44px

---

## Creative Direction (Avoiding AI Slop)

**The Problem**: Generic AI aesthetics lack intentionality. They converge on safe choices (Inter fonts, purple gradients, predictable layouts).

**The Solution**: Choose bold aesthetic direction and execute with precision.

### Bold Aesthetic Framework

Before coding, commit to a direction:

- **Purpose**: What problem does this solve? Who uses it?
- **Tone**: Pick an extreme aesthetic (see examples below)
- **Differentiation**: What's the ONE thing users will remember?

**Aesthetic Directions** (examples, not exhaustive):

- Brutally minimal (Vercel)
- Editorial luxury (Stripe)
- Technical precision (Linear)
- Motion-forward (Framer)
- Organic/natural
- Retro-futuristic
- Industrial/utilitarian
- Art deco/geometric

### Typography Distinctiveness

**Avoid**: Inter, Roboto, Arial, system fonts (overused AI defaults)

**Prefer**: Distinctive pairings that match your tone

- Display font (headlines) + Refined body font
- Unexpected but appropriate character
- Generous size hierarchy (marketing can go bigger)

### Color Distinctiveness

**Avoid**: Purple gradients on white, generic SaaS palettes

**Prefer**:

- One dominant brand accent
- Atmospheric backgrounds (gradients, noise, mesh)
- High contrast for CTAs
- Contextual color that matches purpose

### Layout Distinctiveness

**Avoid**: Centered everything, predictable grid

**Prefer**:

- Asymmetry with purpose
- Overlap and layering
- Diagonal flow
- Grid-breaking elements where appropriate

**CRITICAL**: Minimalist and maximalist both work—the key is intentionality and execution quality, not intensity.

**Detailed guide**: [references/creative-direction.md](references/creative-direction.md)

---

## Component Library

Systematic component patterns to maintain consistency:

### Button Hierarchy

```tsx
// Primary (ONE per section)
<button className="px-4 py-2 rounded-lg bg-gray-900 text-white
                   hover:bg-gray-800 transition-colors">

// Secondary
<button className="px-4 py-2 rounded-lg border border-gray-300
                   hover:bg-gray-50 transition-colors">

// Ghost
<button className="px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors">
```

### Card Patterns

```tsx
// Solid card (default for content)
<div className="p-6 rounded-2xl border border-gray-200 bg-white shadow-sm
               hover:shadow-md hover:-translate-y-0.5 transition-all">

// Glass card (chrome only)
<div className="p-6 rounded-2xl border border-white/20
               backdrop-blur-md bg-white/70 shadow-sm">
```

### Input Standards

```tsx
<input
  className="w-full px-3 py-2 rounded-lg border border-gray-300 
                  focus:border-gray-900 focus:ring-1 focus:ring-gray-900 
                  transition-colors"
/>
```

**Full component guide**: [references/component-library.md](references/component-library.md)

---

## Benchmark Patterns

Learn from premium products:

| Brand      | Signature                            | Steal This                      |
| ---------- | ------------------------------------ | ------------------------------- |
| **Linear** | Spacing discipline + subtle lighting | 8px grid, muted colors          |
| **Stripe** | Editorial typography + gradients     | Large headlines, atmospheric BG |
| **Vercel** | Technical clarity + high contrast    | Black/white, sharp CTAs         |
| **Framer** | Motion-forward + gallery             | Smooth transitions, showcases   |

**Key insight**: Premium = recognizable system. Everything obeys the same rules.

---

## Progressive Disclosure

### When to Read References

| Reference                                              | When to Use                            |
| ------------------------------------------------------ | -------------------------------------- |
| [Foundation First](references/foundation-first.md)     | Building product features from scratch |
| [Creative Direction](references/creative-direction.md) | Want bold, distinctive aesthetics      |
| [Component Library](references/component-library.md)   | Standardizing components across app    |
| [Dashboard Patterns](references/dashboard-patterns.md) | Building KPI layouts, charts, tables   |
| [Marketing Patterns](references/marketing-patterns.md) | Heroes, pricing, feature sections      |

---

## Critical Reminders

1. **Foundation before effects**: Fix hierarchy/spacing/consistency before adding glass/motion
2. **Solid for data**: Tables, forms, dense content always solid backgrounds
3. **One hero moment**: Marketing pages get ONE special effect max
4. **Systematic tokens**: Define spacing/radii/colors once, use everywhere
5. **Test worst-case**: Glass effects must work over busiest possible background
6. **Motion budget**: 2-4 transition types maximum, reused consistently
7. **Accessibility**: Not optional—text contrast, reduced motion, focus states
8. **Creative boldness**: Generic AI aesthetics come from timid choices—commit to direction
