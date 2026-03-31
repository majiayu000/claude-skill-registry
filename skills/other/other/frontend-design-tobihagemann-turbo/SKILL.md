---
name: frontend-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use when the user asks to build landing pages, websites, dashboards, web components, or any frontend UI. Generates creative, polished code that avoids generic AI aesthetics."
---

# Frontend Design

Create distinctive, production-grade frontend interfaces that feel deliberate, premium, and current. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Design Thinking

Before coding, understand the context and commit to a clear aesthetic direction.

Output three things as text before coding:

- **Visual thesis**: one sentence describing mood, material, and energy (e.g., "brutally minimal dark interface with surgical precision" or "warm editorial magazine feel with generous whitespace")
- **Content plan**: hero, support, detail, final CTA
- **Interaction thesis**: 2-3 motion ideas that change the feel of the page

For each, consider:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a direction and commit. Brutally minimal, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, soft pastel, industrial. These are starting points; design one true to the vision.
- **Constraints**: Framework, performance, accessibility requirements.
- **Differentiation**: What makes this unforgettable? What's the one thing someone remembers?

Match ambition to context. A brand landing page warrants bold, expressive choices. A dashboard warrants calm restraint. Both require intentionality.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is production-grade, visually striking, cohesive, and meticulously refined.

## Beautiful Defaults

- Start with composition, not components.
- Prefer a full-bleed hero or full-canvas visual anchor.
- Make the brand or product name the loudest text.
- Keep copy short enough to scan in seconds.
- Use whitespace, alignment, scale, cropping, and contrast before adding chrome.
- Limit the system: two typefaces max, one accent color by default.
- Default to cardless layouts. Use sections, columns, dividers, lists, and media blocks instead.
- Treat the first viewport as a poster, not a document.
- Each section gets one job, one dominant visual idea, and one primary takeaway or action.

## Aesthetics

### Typography

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font. Avoid generic fonts like Arial, Inter, Roboto, and system defaults. Never converge on common AI-favorite choices (Space Grotesk, for example) across generations.

### Color and Theme

Commit to a cohesive palette. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. One accent color unless the product already has a strong system.

### Spatial Composition

Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. Match the spatial approach to the visual thesis.

### Backgrounds and Visual Details

Create atmosphere and depth rather than defaulting to solid colors. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays. Match effects to the overall aesthetic.

## Motion

Use motion to create presence and hierarchy, not noise.

Ship at least 2-3 intentional motions for visually led work:

- One entrance sequence in the hero (staggered reveals with `animation-delay` create more delight than scattered micro-interactions)
- One scroll-linked, sticky, or depth effect
- One hover, reveal, or layout transition that sharpens affordance

Prefer CSS-only solutions for plain HTML. Use Framer Motion when available in React for section reveals, shared layout transitions, scroll-linked shifts, sticky storytelling, and presence effects.

Motion rules:

- Noticeable in a quick recording
- Smooth on mobile
- Fast and restrained
- Consistent across the page
- Removed if ornamental only
- Wrapped in `@media (prefers-reduced-motion: no-preference)` to respect accessibility settings

## Landing Pages

Default sequence:

1. **Hero**: brand or product, promise, CTA, and one dominant visual
2. **Support**: one concrete feature, offer, or proof point
3. **Detail**: atmosphere, workflow, product depth, or story
4. **Final CTA**: convert, start, visit, or contact

Hero rules:

- One composition only. Full-bleed image or dominant visual plane.
- On branded landing pages, the hero runs edge-to-edge with no inherited page gutters or shared max-width. Constrain only the inner text/action column.
- Brand first, headline second, body third, CTA fourth.
- No hero cards, stat strips, logo clouds, pill soup, or floating dashboards by default.
- Keep headlines to roughly 2-3 lines on desktop, readable in one glance on mobile.
- Keep the text column narrow and anchored to a calm area of the image.
- All text over imagery must maintain strong contrast and clear tap targets.

If the first viewport still works after removing the image, the image is too weak. If the brand disappears after hiding the nav, the hierarchy is too weak.

Viewport budget: if the first screen includes a sticky/fixed header, that header counts against the hero. The combined header + hero content must fit within the initial viewport. When using `100vh`/`100svh` heroes, subtract persistent UI chrome or overlay the header.

## App UI

Default to calm, dense restraint:

- Strong typography and spacing
- Few colors
- Dense but readable information
- Minimal chrome
- Cards only when the card is the interaction

Organize around: primary workspace, navigation, secondary context or inspector, one clear accent for action or state.

Avoid: dashboard-card mosaics, thick borders on every region, decorative gradients behind routine product UI, multiple competing accent colors, ornamental icons that do not improve scanning.

If a panel can become plain layout without losing meaning, remove the card treatment.

### Utility Copy for Product UI

On dashboards, admin tools, and operational workspaces, default to utility copy over marketing copy.

- Prioritize orientation, status, and action over promise, mood, or brand voice.
- Start with the working surface itself: KPIs, charts, filters, tables, status. No hero section unless explicitly requested.
- Section headings should say what the area is or what the user can do there.
- If a sentence could appear in a homepage hero or ad, rewrite it until it sounds like product UI.
- If a section does not help someone operate, monitor, or decide, remove it.

## Imagery

Imagery must do narrative work.

- Use at least one strong, real-looking image for brands, venues, editorial pages, and lifestyle products.
- Prefer in-situ photography over abstract gradients for hero anchors.
- Choose or crop images with a stable tonal area for text.
- Do not use images with embedded signage, logos, or typographic clutter fighting the UI.
- If multiple moments are needed, use multiple images, not one collage.

The first viewport needs a real visual anchor. Decorative texture alone is not enough for landing pages (though textures and atmospheric effects work well as supporting elements throughout).

## Copy

- Let the headline carry the meaning.
- Supporting copy: one short sentence.
- Cut repetition between sections.
- Do not include prompt language or design commentary in the UI.
- Give every section one responsibility: explain, prove, deepen, or convert.
- If deleting 30 percent of the copy improves the page, keep deleting.

## Anti-Patterns

Never use generic AI-generated aesthetics:

- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Reject these failures:

- Generic SaaS card grid as the first impression
- Beautiful image with weak brand presence
- Strong headline with no clear action
- Busy imagery behind text
- Sections that repeat the same mood statement
- Carousel with no narrative purpose
- App UI made of stacked cards instead of layout
- Split-screen hero where text isn't on a calm, unified side
- Filler copy or sections that need many tiny UI devices to explain themselves

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. No two designs should feel the same.

## Litmus Checks

Before delivering, verify:

- Is the brand or product unmistakable in the first screen?
- Is there one strong visual anchor?
- Can the page be understood by scanning headlines only?
- Does each section have one job?
- Are cards actually necessary?
- Does motion improve hierarchy or atmosphere?
- Would the design still feel premium if all decorative shadows were removed?
