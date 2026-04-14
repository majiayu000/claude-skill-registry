---
name: minoan-frontend-design
description: This skill should be used when building web components, pages, artifacts, posters, or applications (websites, landing pages, dashboards, React components, HTML/CSS layouts, or styling/beautifying any web UI), including editorial heroes with hover-reactive depth-parallax busts or statues (Astryx pattern) and pointer-reactive fluid effects over DOM sections. Creates distinctive, production-grade frontend interfaces with high design quality that avoids generic AI aesthetics.
---

<!-- Creative core: syncretic-v3 (eval/skills/syncretic-v3.md). See eval/skills/INDEX.md for lineage. -->
<!-- Eval record: 70.0% vs wetch (14-6, p=0.058) across 20 blind A/B comparisons. -->
<!-- Impeccable sync: v1.6.0 (2026-03-24). Anti-patterns, critique refs, scoring rubrics updated. -->

Build frontend interfaces that are unmistakably *designed*, not generated. Every interface should feel like a specific designer made specific choices for a specific context.

## Context Protocol

Before designing, check for `.design-context.md` in the project root. If absent and this is a new project, run `/shape` for a full design brief — or ask the user directly: who uses this, what should it feel like, what should it NOT look like. Don't infer audience from code — code tells you what was built, not who it's for.

## Creative Direction

Name the conceptual direction before coding—"Bloomberg Terminal," "medical journal," "zine collage," "VHS dreamworld." The name anchors every subsequent decision.

Root every aesthetic choice in the subject itself. A jazz club's website should feel like smoke and brass. A children's reading app should feel like opening a pop-up book. A fintech dashboard should feel like a control room, not a toy. The design should be so fitted to its context that transplanting the aesthetic to a different project would feel wrong.

Commit to a singular direction: brutally minimal, maximalist chaos, luxury/refined, lo-fi/zine, dark and moody, editorial/magazine, brutalist/raw, retro-futuristic, art deco/geometric, cinematic/widescreen, data-dense/scientific, or something entirely unnamed. The final design should feel like nothing else.

Every design needs one element so distinctive someone would describe it to a friend. Find that element and let everything else serve it.

## Typography

Typography carries the design's voice—it should have weight you can feel. Default fonts signal default thinking: skip Arial, Inter, Roboto, Space Grotesk, system stacks. Display type should provoke. Body text should be legible and refined. Pair them like actors in a scene—tension creates character. Work the full typographic range: dramatic size jumps, weight contrasts, uppercase for authority, generous letter-spacing for elegance. Control hierarchy through weight and color, not just scale.

Massive editorial typography—oversized display type at 6xl-9xl, ghost numbers behind content, typographic strikethrough—signals authority. At least one typographic moment per design should make a statement, not just organize information.

Treat Inter, Roboto, Arial, Open Sans, Lato, and Montserrat as the model's reflexive defaults—skip them entirely. Typefaces like Fraunces, Playfair Display, DM Sans, and Space Grotesk are genuinely well-made, but they've become the second reflex: what the model reaches for when told to avoid defaults. The goal is a typeface that belongs to *this* project and no other—dig into foundry catalogs (Pangram Pangram, Velvetyne, ABC Dinamo, Future Fonts, Klim) until you find one recognizable in silhouette.

## Color

Color sets the room's temperature. Palettes should take a clear position: bold and saturated, moody and restrained, or high-contrast and minimal—never timid, never non-committal. Lead with a dominant color, punctuate with sharp accents. A single unexpected accent color does more than a balanced five-color system. Never pure black—pure black creates harsh contrast that flattens depth. Use rich off-blacks (zinc-950, deep navy). Tint shadows to the background hue. Warm editorial palettes (cream, parchment, amber on charcoal) are as bold as dark mode—resist defaulting to dark when the context calls for warmth. When dark themes fit, commit fully: singular accent color (acid yellow, bioluminescent cyan, deep rose) against rich off-blacks.

Use OKLCH not HSL—it's perceptually uniform. Tint neutrals toward brand hue (even 0.005 chroma). Derive theme from viewing context: trading terminal → dark, hospital portal → light, children's app → light, motorcycle forum at 9pm → dark. Don't default to either—the correct theme is the one the actual user wants in their actual context.

## Motion

Prioritize CSS-only animations—content hidden behind JavaScript class toggles is invisible in screenshots and static renders. Start visible, animate from there. Staggered page-load reveals create more delight than scattered micro-interactions. Scroll-triggered animations and hover states should surprise.

## Spatial Composition

Unexpected layouts. Asymmetry. Overlap and z-depth. Diagonal flow. Grid-breaking elements. Dramatic scale jumps. Full-bleed moments. Split-screen compositions. Bento grids with varied tile sizes. Generous negative space OR controlled density—commit to one, never the uncommitted middle. Centered hero sections are the default—break that default with left-aligned text, asymmetric splits, or editorial whitespace. Use cards only when elevation communicates hierarchy, not as a generic container for everything.

For dashboards and data-dense interfaces, maximize information above the fold. Pack metrics, charts, and controls into dense grids separated by thin borders and negative space—not card containers. Use monospace for all numbers. Treat the dashboard as a command center, not a gallery.

## Atmosphere & Texture

Create depth and mood rather than defaulting to flat solid colors. The background is a canvas, not a wall. Apply contextual effects: gradient meshes, noise and grain overlays, geometric patterns, glassmorphism with inner refraction borders, dramatic or soft shadows, parallax depth, clip-path shapes, print-inspired textures (halftone, duotone, risograph), knockout typography, hand-drawn SVG accents, generative pattern backgrounds.

Generate custom SVG illustrations fitted to the context—never placeholder images. A ramen shop gets a hand-drawn bowl. An ocean nonprofit gets bioluminescent particles. The illustration **is** the design, not decoration.

## What to Reject

Never use generic AI aesthetics: overused fonts (Inter, Roboto, Arial, Space Grotesk, system stacks), cliched color schemes (purple gradients on white, neon outer glows), predictable centered layouts, the generic three-equal-cards feature row, excessive gradient text, generic placeholder content (John Doe, 99.99%, "Elevate your workflow"), emoji or SVG-egg avatar placeholders, hero sections that push core content below the fold, or incomplete implementations.
Instead: distinctive fonts that take a position. Bold, committed palettes. Asymmetric layouts that surprise. Bespoke details rooted in context. Realistic content with creative names and organic data (47.2%, not 50%). When photos are requested, use image services or generate meaningful visual content—never empty containers. Every feature requested, every choice deliberate.

Resist the first satisfying idea. The model's default output is the average of its training data—genuine distinction means pushing past the obvious.

Two CSS patterns are absolute bans on cards, callouts, and alerts:
- On cards/callouts/alerts, never use `border-left:` or `border-right:` with width > 1px as an accent stripe (the single most overused AI design tell—rewrite with background tints, full borders, or no indicator at all)
- Never use `background-clip: text` combined with any gradient background (gradient text is decorative, not meaningful—use solid color, emphasize with weight or size instead)

## Craft

Match implementation complexity to the aesthetic vision. Maximalist designs demand elaborate code. Minimalist designs demand obsessive restraint. Both demand pixel-level attention to spacing, alignment, and consistency. Deliver every feature the prompt requests—completeness is the floor, not the ceiling. A complete AND bold implementation beats both a partial masterpiece and a complete bore.

Claude is capable of extraordinary, award-worthy creative work. The person who sees this interface should feel something they didn't expect to feel. Don't hold back—show what's truly possible when every aesthetic choice is intentional, every detail is refined, and the vision is executed without compromise.

## Post-Build QA Workflow

After building, run these refinement passes in order:

1. **Audit** (or `/design-audit`): Check against `references/anti-patterns.md` + domain-specific impeccable refs below. Score 5 dimensions (a11y, performance, responsive, theming, anti-patterns) 0-4 each. Tag issues P0-P3 per `references/heuristics-scoring.md`.
2. **Critique** (or `/design-critique`): UX review using `references/heuristics-scoring.md` (Nielsen's 10 heuristics, score 0-4 each, /40). Assess cognitive load via `references/cognitive-load.md` (8-item checklist). Test with 2-3 personas from `references/personas.md`. Run the AI Slop Test: if someone said "AI made this," would they believe it immediately? If yes, fix it.
3. **Normalize**: Align with project design system if `.design-context.md` or `DESIGN.md` exists in project root. Treat their tokens (colors, fonts, spacing) as materials, not a recipe—creative direction from above still leads.
4. **Harden**: Test edge cases—long text overflow, RTL, empty states, error states, i18n, keyboard navigation.
5. **Polish** (or `/design-polish`): Final pass—alignment, spacing, interaction states, transitions, micro-copy. Every pixel intentional.

## References

Consult `references/` on demand:

**Engineering**: `vercel-web-interface-guidelines.md`, `design-system-checklist.md`.
**Techniques**: `creative-arsenal.md`, `design-dials.md`, `editorial-patterns.md` (eval-tested), `astryx-hero.md` (depth-parallax editorial hero + fluid-dom sibling links). **Shader cross-ref**: `~/.claude/skills/rocaille-shader/references/fluid-dom.md` (pointer-reactive fluid over DOM sections).
**Stripe** (light-mode): `stripe-design-tokens.md`, `stripe-component-patterns.md`, `stripe-signature-techniques.md`.
**Mintlify** (dark-first docs): `mintlify-design-tokens.md`, `mintlify-component-patterns.md`, `mintlify-signature-techniques.md`.
**Anti-patterns**: `anti-patterns.md` (condensed checklist from Impeccable v1.6.0).
**Critique & Scoring**: `heuristics-scoring.md` (Nielsen's 10, P0-P3 severity), `cognitive-load.md` (8-item checklist, working memory rule), `personas.md` (5 archetypes + project-specific).
**Design system exemplar**: `linear-design-md.md` (DESIGN.md format—tokens, components, responsive rules from Linear).
**Advanced techniques**: `sunny-mode-technique.md` (`@property` palette transitions, blend-mode overlays, physics Easter eggs).
**Impeccable domain refs** (code examples + implementation patterns): `impeccable-typography.md` (font loading, OpenType, scales), `impeccable-color-contrast.md` (OKLCH, dark mode tokens), `impeccable-spatial.md` (container queries, optical alignment), `impeccable-motion.md` (cubic-bezier values, stagger formula, reduced-motion), `impeccable-interaction.md` (Popover API, roving tabindex, dialog), `impeccable-responsive.md` (pointer/hover queries, safe areas, srcset), `impeccable-ux-writing.md` (error templates, voice matrix).
**Color science** (from meodai/skill.color-expert): `color-science-deep.md` (color spaces decision matrix, HSL limitations, chroma vs saturation, character-first harmony, accessibility statistics, pigment mixing, naming systems), `color-tools-palette.md` (palette generation algorithms, code libraries, analysis/linting, CSS Color 4/5, semantic token architecture, generative art approaches).
**Component research**: invoke `component-gallery`.
