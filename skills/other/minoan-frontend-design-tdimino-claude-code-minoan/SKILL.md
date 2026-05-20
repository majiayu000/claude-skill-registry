---
name: minoan-frontend-design
description: This skill should be used when building web components, pages, artifacts, posters, or applications (websites, landing pages, dashboards, React components, HTML/CSS layouts, or styling/beautifying any web UI). Creates distinctive, production-grade frontend interfaces with high design quality that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

<!-- Creative core: syncretic-v3 (eval/skills/syncretic-v3.md). See eval/skills/INDEX.md for lineage. -->
<!-- Eval record: 70.0% vs wetch (14-6, p=0.058) across 20 blind A/B comparisons. -->

Build frontend interfaces that are unmistakably *designed*, not generated. Every interface should feel like a specific designer made specific choices for a specific context.

## Creative Direction

Name the conceptual direction before coding—"Bloomberg Terminal," "medical journal," "zine collage," "VHS dreamworld." The name anchors every subsequent decision.

Root every aesthetic choice in the subject itself. A jazz club's website should feel like smoke and brass. A children's reading app should feel like opening a pop-up book. A fintech dashboard should feel like a control room, not a toy. The design should be so fitted to its context that transplanting the aesthetic to a different project would feel wrong.

Commit to a singular direction: brutally minimal, maximalist chaos, luxury/refined, lo-fi/zine, dark and moody, editorial/magazine, brutalist/raw, retro-futuristic, art deco/geometric, cinematic/widescreen, data-dense/scientific, or something entirely unnamed. The final design should feel like nothing else.

Every design needs one element so distinctive someone would describe it to a friend. Find that element and let everything else serve it.

## Typography

Typography carries the design's voice—it should have weight you can feel. Default fonts signal default thinking: skip Arial, Inter, Roboto, Space Grotesk, system stacks. Display type should provoke. Body text should be legible and refined. Pair them like actors in a scene—tension creates character. Work the full typographic range: dramatic size jumps, weight contrasts, uppercase for authority, generous letter-spacing for elegance. Control hierarchy through weight and color, not just scale.

Massive editorial typography—oversized display type at 6xl-9xl, ghost numbers behind content, typographic strikethrough—signals authority. At least one typographic moment per design should make a statement, not just organize information.

## Color

Color sets the room's temperature. Palettes should take a clear position: bold and saturated, moody and restrained, or high-contrast and minimal—never timid, never non-committal. Lead with a dominant color, punctuate with sharp accents. A single unexpected accent color does more than a balanced five-color system. Never pure black—pure black creates harsh contrast that flattens depth. Use rich off-blacks (zinc-950, deep navy). Tint shadows to the background hue. Warm editorial palettes (cream, parchment, amber on charcoal) are as bold as dark mode—resist defaulting to dark when the context calls for warmth. When dark themes fit, commit fully: singular accent color (acid yellow, bioluminescent cyan, deep rose) against rich off-blacks.

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

## Craft

Match implementation complexity to the aesthetic vision. Maximalist designs demand elaborate code. Minimalist designs demand obsessive restraint. Both demand pixel-level attention to spacing, alignment, and consistency. Deliver every feature the prompt requests—completeness is the floor, not the ceiling. A complete AND bold implementation beats both a partial masterpiece and a complete bore.

Claude is capable of extraordinary, award-worthy creative work. The person who sees this interface should feel something they didn't expect to feel. Don't hold back—show what's truly possible when every aesthetic choice is intentional, every detail is refined, and the vision is executed without compromise.

## References

For engineering standards, consult `references/vercel-web-interface-guidelines.md` and `references/design-system-checklist.md`. For advanced techniques, consult `references/creative-arsenal.md` and `references/design-dials.md`. For editorial patterns from eval testing, consult `references/editorial-patterns.md`.
