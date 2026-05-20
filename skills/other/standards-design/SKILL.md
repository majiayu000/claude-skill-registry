---
name: standards-design
description: Create visually distinctive frontend interfaces that avoid generic AI-generated aesthetics. Apply when building landing pages, dashboards, product UIs, selecting fonts, choosing color palettes, designing layouts, adding animations or micro-interactions, or when the output risks looking like typical AI-generated UI.
---

# Design Standards

**Rule:** Commit to a clear aesthetic direction and execute it with precision. Every visual choice must be intentional, not default.

## When to use this skill

- When building new pages, landing pages, or marketing sites
- When creating dashboards, product UIs, or admin interfaces
- When selecting fonts, color palettes, or visual themes
- When adding animations, transitions, or micro-interactions
- When the output risks looking generic or like typical AI-generated UI
- When creating visual atmosphere with backgrounds, gradients, or textures
- When designing component layouts, spacing, and visual hierarchy
- When polishing an interface for production or launch readiness
- When a user asks for something "beautiful", "polished", "modern", or "distinctive"

## Design Direction Before Code

Before writing any styles, establish a clear aesthetic direction.

**Ask these questions:**
1. **Purpose** - What does this interface communicate? Professional trust? Creative energy? Technical precision?
2. **Audience** - Who uses this? Developers? Consumers? Enterprise buyers?
3. **Tone** - Pick a specific direction: minimalist, editorial, brutalist, playful, luxurious, industrial, organic, retro-futuristic, geometric, soft
4. **Differentiator** - What single visual element will make this memorable?

**Then commit.** A bold minimalist design and a rich maximalist design are both good. A directionless design that hedges is always bad.

## Typography

### Font Selection

Choose fonts that match the aesthetic direction and have character.

**Bad - Generic defaults:**
```css
font-family: Arial, sans-serif;
font-family: 'Inter', sans-serif;
font-family: 'Roboto', sans-serif;
font-family: system-ui, sans-serif;
```

**Good - Intentional choices:**
```css
/* Editorial / Magazine */
font-family: 'Playfair Display', serif;      /* Display */
font-family: 'Source Serif 4', serif;         /* Body */

/* Technical / Developer */
font-family: 'JetBrains Mono', monospace;     /* Display */
font-family: 'IBM Plex Sans', sans-serif;     /* Body */

/* Modern / Clean */
font-family: 'Outfit', sans-serif;            /* Display */
font-family: 'DM Sans', sans-serif;           /* Body */

/* Bold / Statement */
font-family: 'Cabinet Grotesk', sans-serif;   /* Display */
font-family: 'General Sans', sans-serif;      /* Body */
```

### Font Pairing

Pair a distinctive display font with a readable body font. Contrast in style, unite in tone.

**Principles:**
- Display fonts carry personality (headings, hero text, callouts)
- Body fonts prioritize readability (paragraphs, UI labels, form text)
- Limit to 2 fonts per project (3 maximum with a monospace)
- Use weight variation within a family before adding another font

### Font Anti-Patterns

Never default to these without a specific reason:
- Inter, Roboto, Arial, Helvetica (overused, signals no design thought)
- Space Grotesk (AI-generated UI cliche)
- Using the same font for display and body without weight contrast

## Color

### Palette Construction

Build a cohesive palette with clear hierarchy. Avoid distributing colors evenly.

**Structure:**
```
Primary   - Brand color, CTAs, key actions (1 color)
Accent    - Highlights, badges, secondary emphasis (1-2 colors)
Neutral   - Text, borders, backgrounds (gray scale)
Semantic  - Success, warning, error, info (functional only)
```

**Bad - Even distribution:**
```css
/* 5 colors used equally across the page */
--blue: #3b82f6;
--purple: #8b5cf6;
--pink: #ec4899;
--green: #10b981;
--orange: #f97316;
```

**Good - Clear hierarchy:**
```css
--primary: #0f172a;        /* Dominant: dark navy */
--accent: #f59e0b;         /* Sharp contrast: amber */
--text: #334155;           /* Readable body text */
--text-muted: #94a3b8;     /* Secondary text */
--surface: #f8fafc;        /* Background */
--border: #e2e8f0;         /* Subtle borders */
```

### Color Anti-Patterns

- Purple-to-blue gradients on white (the quintessential AI look)
- Rainbow or multi-color schemes without hierarchy
- Low-contrast text that fails WCAG AA (4.5:1 minimum)
- Using brand color for everything instead of as an accent

### Dark Mode

If implementing dark mode, design it separately. Don't just invert colors.

```css
/* Bad: simple inversion */
--bg: white → black;
--text: black → white;

/* Good: designed for dark */
--bg: #0f172a;           /* Deep navy, not pure black */
--surface: #1e293b;       /* Elevated surfaces slightly lighter */
--text: #e2e8f0;          /* Off-white, not pure white */
--text-muted: #64748b;    /* Muted but readable */
--border: #334155;        /* Subtle, not stark */
```

## Spacing and Composition

### Visual Hierarchy

Guide the eye through deliberate size, weight, and spacing differences.

**Bad - Flat hierarchy:**
```
[Same size heading]
[Same size text]
[Same size button]
[Same size text]
```

**Good - Clear hierarchy:**
```
[Large bold heading]          ← Immediate attention
[Spacious subtext in muted]  ← Context
                              ← Breathing room
[Prominent CTA button]       ← Action
[Small supporting text]      ← Secondary
```

### Whitespace

Use generous whitespace to create focus. Cramped layouts signal low quality.

**Bad:**
```css
.section { padding: 1rem; }
.card { margin-bottom: 0.5rem; }
```

**Good:**
```css
.section { padding: 4rem 2rem; }       /* Generous section spacing */
.card { margin-bottom: 2rem; }         /* Room to breathe */

@media (min-width: 1024px) {
  .section { padding: 6rem 4rem; }     /* Even more space on desktop */
}
```

### Layout Composition

Not every layout needs to be a symmetric grid. Consider:
- **Asymmetric splits** (60/40, 70/30) for visual interest
- **Overlapping elements** for depth
- **Varied column widths** instead of equal divisions
- **Full-bleed sections** breaking the container for emphasis
- **Negative space** as a deliberate design element

## Motion and Interaction

### Purposeful Animation

Every animation should serve a purpose: guide attention, provide feedback, or create continuity.

**Bad - Decorative motion:**
```css
/* Everything bounces, spins, or fades for no reason */
.card { animation: bounce 2s infinite; }
```

**Good - Purposeful motion:**
```css
/* Staggered entrance reveals content hierarchy */
.card {
  opacity: 0;
  transform: translateY(1rem);
  animation: reveal 0.5s ease-out forwards;
}

.card:nth-child(1) { animation-delay: 0ms; }
.card:nth-child(2) { animation-delay: 100ms; }
.card:nth-child(3) { animation-delay: 200ms; }

@keyframes reveal {
  to { opacity: 1; transform: translateY(0); }
}
```

### Micro-Interactions

Add subtle feedback on interactive elements:

```css
/* Button with tactile feedback */
.button {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.button:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

### Motion Anti-Patterns

- Animations longer than 500ms for UI elements (feels sluggish)
- Infinite animations on static content (distracting)
- Animating layout properties (width, height) instead of transform/opacity (poor performance)
- Motion without `prefers-reduced-motion` respect:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Visual Atmosphere

### Backgrounds and Depth

Flat solid-color backgrounds are the minimum. Create atmosphere that matches the aesthetic direction.

**Techniques by tone:**

Subtle and professional:
```css
/* Soft radial gradient */
background: radial-gradient(ellipse at top, #f0f4ff 0%, #ffffff 70%);

/* Noise texture overlay */
background-image: url("data:image/svg+xml,..."); /* subtle noise */
opacity: 0.03;
```

Bold and modern:
```css
/* Gradient mesh */
background:
  radial-gradient(at 20% 80%, #1e40af33 0%, transparent 50%),
  radial-gradient(at 80% 20%, #7c3aed33 0%, transparent 50%),
  #0f172a;

/* Geometric patterns */
background-image: repeating-linear-gradient(
  45deg, transparent, transparent 35px, rgba(255,255,255,.03) 35px, rgba(255,255,255,.03) 70px
);
```

### Shadows and Elevation

Use shadows to create depth hierarchy, not just borders.

**Bad - Flat or harsh:**
```css
box-shadow: 0 0 10px rgba(0,0,0,0.5);  /* Too harsh */
border: 1px solid #ccc;                  /* Flat */
```

**Good - Layered and natural:**
```css
/* Subtle elevation */
box-shadow:
  0 1px 2px rgba(0, 0, 0, 0.04),
  0 4px 8px rgba(0, 0, 0, 0.04);

/* Higher elevation (modals, dropdowns) */
box-shadow:
  0 4px 6px rgba(0, 0, 0, 0.04),
  0 12px 24px rgba(0, 0, 0, 0.08);
```

## AI Aesthetic Anti-Patterns

These patterns signal "AI-generated" and should be avoided:

| Anti-Pattern | Why It's Bad | Alternative |
|-------------|-------------|-------------|
| Purple gradient on white | Most common AI cliche | Choose palette matching purpose |
| Inter/Roboto/Space Grotesk | Default AI font choices | Select fonts matching tone |
| Symmetric 3-column grid | Predictable, no visual interest | Asymmetric or varied layouts |
| Generic stock illustrations | Impersonal, disconnected | Custom icons or photography |
| Rounded cards with light shadow | Every AI UI looks like this | Match card style to aesthetic |
| Blue CTA buttons | Safe but forgettable | Brand-aligned accent color |
| Gradient text on everything | Overused effect | Reserve for one focal element |
| Emoji as design elements | Lazy visual shorthand | Custom icons or typography |

## Verification Checklist

Before completing design work:

- [ ] Established clear aesthetic direction before coding
- [ ] Typography uses intentional font choices (not defaults)
- [ ] Color palette has clear hierarchy (not evenly distributed)
- [ ] Spacing is generous with clear visual hierarchy
- [ ] Animations serve a purpose (feedback, attention, continuity)
- [ ] `prefers-reduced-motion` is respected
- [ ] Backgrounds create atmosphere (not flat solid colors)
- [ ] Does not match common AI aesthetic anti-patterns
- [ ] Consistent tone across all elements
- [ ] Color contrast meets WCAG AA (4.5:1)

## Quick Reference

| Situation | Action |
|-----------|--------|
| Starting new UI | Establish aesthetic direction first |
| Choosing fonts | Avoid Inter/Roboto/Arial, pick fonts matching tone |
| Choosing colors | Build hierarchy: 1 primary, 1 accent, neutrals |
| Setting spacing | More generous than you think, especially sections |
| Adding animation | Ask "what purpose does this serve?" |
| Background feels flat | Add subtle gradient, texture, or pattern |
| Result looks generic | Check against AI anti-patterns table |
| Dark mode | Design separately, don't just invert |
