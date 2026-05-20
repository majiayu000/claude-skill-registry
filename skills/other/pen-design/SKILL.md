---
name: pen-design
description: Use when creating, editing, or visually reviewing Pencil (.pen) screens, components, or flows.
---

# UI Design in Pencil

Design interfaces that look intentional, not generated. This skill teaches design thinking — Pencil is the tool, not the subject.

For Pencil MCP tool mechanics (operations, component reuse, variables, asset management):
!references/pencil-workflow.md

## Design Framing

Before touching any tool, answer these questions. Write them down — they constrain every decision that follows.

**What is this?** Product type, screen purpose, who sees it, when and where (commute? desk? presentation?).

**What does it evoke?** Describe the feeling in 2-3 sentences. Not "modern and clean" — that's nothing. "A confident, unhurried conversation with someone who knows more than you" or "The satisfying click of a well-made mechanical object." This is the emotional compass.

**What inspires it?** Name 2-3 existing products, magazines, physical objects, or art that capture the feeling. This grounds the aesthetic in something real instead of generic AI defaults.

**What's the palette?** Define before building — not after. Follow the 60/30/10 rule:
- 60% dominant (background, surfaces) — sets the mood
- 30% secondary (cards, sections, supporting elements) — creates rhythm
- 10% accent (CTAs, highlights, key moments) — directs attention

Define these as design tokens immediately. Every color decision flows from this palette.

**What's the type system?** Pick two fonts maximum:
- Display/heading: characterful, sets the tone (never Inter, Roboto, or system defaults)
- Body: readable, complements without competing

Define a scale. Pick a ratio (1.125 minor second for dense UIs, 1.25 major third for editorial, 1.333 perfect fourth for bold hierarchies) and generate sizes from it. Typical mobile scale: 12 / 14 / 16 / 20 / 25 / 32. Assign roles: caption, body, subheading, heading, display.

## Visual Hierarchy

Every screen has one job. One primary action, one focal point, one thing the eye hits first. Everything else supports it.

**Tools for directing attention** (use in combination):
- **Size** — the biggest thing wins. Display text, hero images, primary CTAs.
- **Weight** — bold pulls the eye before regular. Use 2-3 weights max.
- **Contrast** — high contrast = important. Muted = secondary. Use your accent color sparingly — it's a spotlight, not a floodlight.
- **Spacing** — generous space around an element elevates it. Cramped = secondary. The most important element gets the most breathing room.
- **Position** — top-left reads first (LTR). Primary content goes where eyes naturally land.

**Common hierarchy failures:**
- Everything is the same size/weight → nothing stands out → user doesn't know where to start
- Too many accent colors → nothing feels special → visual noise
- Equal spacing everywhere → no grouping → cognitive load increases

## Layout & Composition

**Mobile (375-430px):**
- Single column. Content stacks vertically.
- Horizontal padding 16-20px. Content never touches screen edges.
- Bottom-heavy interaction — primary CTAs in thumb reach zone.
- Safe areas: respect notch, home indicator, status bar.

**Tablet & Desktop:**
- Multi-column layouts. Sidebars, split views, card grids.
- Max content width (~1200px) with centered layout — don't stretch to fill ultrawide screens.
- Consider F-pattern (content-heavy pages) or Z-pattern (landing pages) for information flow.

**Spatial composition principles:**
- Asymmetry is more interesting than symmetry. Off-center placements feel designed; perfect centering feels default.
- Group related elements with proximity. Separate unrelated elements with space — not lines or borders.
- White space is a design element, not wasted space. Generous margins signal quality.
- Break the grid intentionally — one overlapping element or one oversized image creates visual interest without chaos.

## Color

**Palette strategy:**
- Start from the brand or product context — not from a random palette generator.
- Warm palettes (amber, terracotta, sage) feel approachable. Cool palettes (slate, navy, teal) feel professional. Neutral palettes (stone, zinc) feel minimal.  
- Dark mode is not inverted light mode. Desaturate colors, use lighter tonal variants, test contrast independently.

**Semantic tokens:** Name colors by function, not appearance — `primary`, `surface`, `error`, `muted` — not `blue-500`, `gray-100`. This enables theming and dark mode.

**Contrast:** Body text ≥ 4.5:1 against its background. Large text (18px+ bold or 24px+) ≥ 3:1. Interactive elements need visible focus and hover states. Don't convey meaning through color alone — pair with icons or text.

## Typography in Practice

- **Line height:** 1.4-1.6 for body text. Tighter (1.2-1.3) for headings. Never 1.0.
- **Line length:** 45-75 characters for comfortable reading. On mobile this usually means full-width text with proper padding.
- **Weight hierarchy:** Bold headings (600-700), regular body (400), medium labels (500). Using more than 3 weights creates noise.
- **Truncation:** Prefer wrapping over truncation. When truncating, use ellipsis and ensure the full text is accessible (tooltip, expand).

## Responsive Thinking

Design mobile-first, then scale up. Each breakpoint should feel designed for that size — not stretched or compressed.

- **What changes between sizes:** column count, visibility of secondary elements, spacing scale, font sizes, navigation pattern (bottom tabs → sidebar)
- **What stays the same:** hierarchy, brand feel, core content, interaction patterns
- **Content priority:** Show the essential on mobile. Reveal the secondary on larger screens. Don't just shrink everything.

## Accessibility as Design Quality

Accessible design is better design — it forces clarity and intentionality.

- **Touch targets:** 44x44px minimum for interactive elements. Extend hit areas beyond visual bounds if the element is smaller.
- **Focus states:** Visible focus rings (2-4px) on all interactive elements. Never remove them.
- **Semantic structure:** Heading hierarchy (h1 → h2 → h3, no skipping). Labels on form fields (not placeholder-only).
- **Motion:** Respect `prefers-reduced-motion`. Keep micro-interactions 150-300ms. Complex transitions ≤ 400ms. Exit animations shorter than enter.
- **Screen readers:** Alt text on meaningful images. `aria-label` on icon-only buttons. Logical reading order.

## Parallelization

For multi-screen projects, don't design sequentially — fan out after establishing shared context.

**The orchestrator does the setup** (this cannot be parallelized — it's the shared contract):
1. Design framing (palette, type system, tone, spatial approach)
2. Design system inventory (`batch_get` with `{ reusable: true }`)
3. Token setup (`get_variables`, create missing tokens)

**Then spawn teammates per screen.** Each teammate gets:
- The design framing decisions (palette, type system, tone description)
- The design system component list
- The token set
- Their specific screen assignment
- The Pencil workflow reference

Teammates work independently — each builds their screen section by section with verification. The orchestrator stays responsive for user interaction and reviews results as they come in.

**When to parallelize:** 2+ independent screens. Not worth it for a single screen or tightly coupled screens (e.g., a wizard flow where each step depends on the previous).

**Polish pass** can also be parallelized — spawn a teammate per screen to screenshot, assess, and fix.

## Visual QA

After completing a screen, screenshot it and react as a user — first impression, no context about how it was built.

Ask: *Does this look like a human designed it with intention, or like an AI assembled it from parts?*

Signs of AI-assembled design:
- Everything is the same visual weight — no hierarchy
- Safe, predictable layout — nothing surprising or memorable
- Colors are present but not cohesive — no clear palette strategy
- Typography is functional but characterless — system fonts, no personality
- Spacing is even everywhere — no rhythm, no breathing room

Signs of intentional design:
- Clear focal point — you know where to look first
- Consistent but not rigid — rhythm with variation
- Color serves a purpose — accent draws the eye where it should go
- Typography has personality — the fonts feel chosen, not defaulted
- Space is used deliberately — some areas are tight, others breathe

For Pencil-specific QA failures and bulk fix tools, see the workflow reference.
