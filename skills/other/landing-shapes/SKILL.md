---
name: landing-shapes
description: Use whenever `landing-systems` names the signature element's geometry personality and family (Chain Method step 6), `landing-sequencer` picks a concrete transition/divider technique for it, or `landing-builder` implements any section shape, divider, or icon. Trigger on "implement the signature element", "write the divider", "section transition CSS", "src/shapes/*", or an icon/illustration sourcing question. Gives the concrete construction techniques — curved and angular alike — and the one pinned icon source, so shapes come from a formula or a sourced icon instead of hand-typed or hand-measured geometry.
---

# Landing Shapes

`landing-systems` decides *what* the signature element is and *why* —
its source in the subject statement, persistence, continuity, scale
range, literalness (Chain Method step 6). This skill covers *how* to
build it, and every other section shape or divider the build needs: the
geometry personality, the technique library, and the one pinned SVG
source. It never decides what a shape means or where it recurs — that
traceability stays with the Chain Method phases and `landing-critic`'s
audit.

## Hard rule: never hand-draw a shape — compute it or source it

Never type out an SVG `<path d="M...">` by imagination, and never guess
`clip-path: polygon()` coordinates or `border-radius` blob percentages
by eye. Both fail the same way: there's no way to tell what a shape
looks like from raw numbers while writing them, so hand-typed geometry
drifts into lumpy, asymmetric, or misaligned results.

Instead, every shape comes from one of:

- **A formula.** A named, computable rule — a seeded-random function
  producing 4 `border-radius` percentages, a small function generating
  N `clip-path: polygon()` points, a sine wave or noise function driving
  a point set assigned to `clip-path: path(...)` or drawn to
  `<canvas>` — with named parameters, never a manually plotted point
  list. This is the only construction path for an irregular blob or
  facet shape: compute the numbers, don't eyeball them, and don't rely
  on a GUI generator's output either — this skill is followed by an
  agent, not a person clicking a drag-point editor, so the shape must be
  something code can produce unattended.
- **A sourced Lucide icon** — see Icons, below. Importing a published
  icon is not hand-authoring; the shape wasn't guessed.

If a shape doesn't fit a formula or a sourced icon, that's a signal to
simplify what the shape is, not a reason to fall back to freehand SVG,
CSS, or a coordinate read off a live DOM measurement (see the note on
measured coordinates below).

## Step 0: Decide, don't default

Before implementing the signature element or any section divider, work
through this quickly:

1. **Geometry personality** — pick one on purpose, don't default to
   organic:
   - *Fully organic* — curves, blobs, domes everywhere.
   - *Fully angular* — sharp diagonal cuts, hard edges, clip-path
     polygons, zero curves, on purpose.
   - *Mixed* — a strict grid/layout with one curved element as
     contrast, or an organic page with one hard geometric anchor.
   - *Geometric-precise* — perfect circles/arcs and straight lines only,
     no irregular organic blobs — reads as engineered, not organic.
   Let the target feeling (below) and `landing-systems`'s tokens drive
   this: futuristic, bold/confident, urgent targets often want angular
   or geometric-precise over organic; cozy, nostalgic, playful targets
   almost always want organic.
2. **Element family**, matched to the geometry personality:
   - *Organic* — vine/growth (blobs, tendrils, clusters) · terrain
     (ridgelines, dunes, strata) · fluid/tide (wave caps, droplets,
     ripples) · cellular (membranes, clusters) · mycology (spores,
     branching) · culinary (steam curls, marbling) · calligraphy (ink
     strokes, swashes).
   - *Angular* — architectural (facets, girders, cantilevers) ·
     circuit/blueprint (traces, grids, schematics) · industrial
     (conveyor lines, riveted panels, ductwork) · cartography (routes,
     grid coordinates) · knotwork as straight interlace.
   - *Either* — celestial (orbits as circles = geometric, or soft glows
     = organic) · textile/ribbon (folded = angular, draped = organic) ·
     **oversized type as the graphic element itself** (a display word,
     a huge numeral, or a repeated letterform used as the composition's
     anchor rather than as reading matter — the shape work is
     typographic, so the geometry personality shows up in the
     letterform's character and how it's cropped, layered, or bled off
     the edge).
   Commit fully to the family the Chain Method named — don't blend
   three.
3. **Shape technique**, from the libraries below, matched to the
   geometry personality. Use 2–3 techniques in combination across the
   page rather than one technique doing everything.

## Curve techniques without SVG

1. **Dome dividers (`border-radius` trick).** A full-bleed element sits
   flush at a section boundary, colored like the *next* section, with
   `border-radius: 50% 50% 0 0 / 100% 100% 0 0` and `width: 130–150%`
   (wider than the viewport so the arc reads as one continuous sweep).
   Vary `left` offset and height per boundary so the rhythm doesn't feel
   mechanical. The fastest, most reliable default for section-to-section
   transitions.
2. **`clip-path: path()` ribbons and edges.** For a true winding line (a
   vine, a river) that isn't just a dome, compute a bezier path string
   in JS (the same math as an SVG path `d`, assigned to `clip-path` on a
   plain `<div>`) and reveal it via a scroll-driven `clip-path: inset()`
   wipe or by animating the path's control points with Motion.
3. **Organic blobs.** `border-radius: 63% 37% 54% 46% / 55% 48% 52% 45%`
   (irregular, all four corners different) reads as a soft blob. Animate
   between 2–3 such strings on a `@keyframes` loop for a breathing/
   morphing effect.
4. **Arc/curve via border trick.** A square with `border-radius: 50%`
   and only 1–2 border sides colored (others transparent), rotated,
   produces a quarter/half-circle arc. Chain several for a winding path
   down the page without any path math.
5. **Shape composition from circles.** Clusters of `border-radius: 50%`
   divs (clusters, bubble fields, orbit rings) — cheap, flexible for an
   element that repeats as small shapes rather than one large form.
6. **`shape-outside`** on a floated blob lets body text wrap along a
   curve — good for editorial-feeling sections.
7. **Canvas 2D with computed coordinates**, for anything formula-driven
   (noise, jitter, growth) that needs to react to pointer/scroll
   continuously. Derive every coordinate from the formula — never an
   eyeballed pixel value, and never a coordinate read from
   `getBoundingClientRect()` or similar (see the note below). Reach for
   `ogl` (this core's WebGL library) if the field needs to span the full
   page as one continuous surface rather than redraw per section.

**A note on measured DOM coordinates.** Don't build a shape (a
connecting line, a thread between sections) by reading real element
positions with `getBoundingClientRect()` or similar at render time. A
measurement taken at one viewport size is wrong the moment the layout
reflows — a resize, a font load, a content-length difference between
builds — and this skill exists specifically to stop shapes from
breaking across breakpoints. If two elements need to look connected,
express that with relative/percentage-based CSS positioning within a
shared container, or a formula that doesn't depend on a live
measurement — not a one-time read of the DOM.

## Angular techniques

1. **Diagonal-cut dividers.** Same flush-at-the-boundary technique as
   dome dividers, using `clip-path: polygon(0 0, 100% 30%, 100% 100%,
   0 100%)` (or similar) instead of `border-radius` — a hard diagonal
   slice between sections.
2. **Faceted/angular blobs.** `clip-path: polygon(...)` with 5–8
   irregular points reads as a crystalline facet shape — the angular
   sibling of the organic blob.
3. **Grid-strict layout with hard gutters.** Precise column/row grids,
   sharp 1px or thick hairline dividers, zero `border-radius` anywhere.
4. **Rotated square/rectangle stacks.** Plain divs rotated 15–45°,
   stacked or overlapping, for a dynamic angular composition without any
   path math.
5. **Chevron/zigzag rhythm.** Repeating `clip-path: polygon()` or
   `linear-gradient()` stripes at an angle for a driving divider
   pattern.
6. **Canvas-drawn geometric fields.** Particle grids, wireframes, or
   vector fields (via `ogl` or raw canvas) snapped to straight lines and
   hard angles instead of flow curves.
7. **Overlapping/bleeding panels.** Negative margins to bleed a panel
   into its neighbor, `z-index` layering so one panel visibly sits on
   top of another, a rotated panel or two for collage energy. Pair with
   a thick (5–10px) solid border on every panel to read as a panel
   gutter.
8. **Starburst/badge shapes.** `clip-path: polygon()` with 8–12
   alternating long/short points around a center — a comic burst or
   price-tag badge, for a callout that should interrupt the grid rather
   than sit inside it.

## Icons: Lucide only

[Lucide](https://lucide.dev), via `@lucide/astro` — the one pinned icon
source for this core. Import icons as Astro components:

```astro
---
import { Sparkles } from '@lucide/astro';
---

<Sparkles size={24} color="var(--color-accent)" />
```

Importing a Lucide icon is sourcing, not hand-authoring — its SVG
wasn't guessed. Don't reach for a second icon library or a stock
illustration set to fill a gap Lucide doesn't cover; a genuine gap is a
signal to build the shape from a technique above instead, not to add a
new dependency.

Photography (not vector, but worth noting alongside): Unsplash or Pexels
for a photo-led build — outside this skill's shape/icon scope, but the
right tool when the build needs real images rather than illustration.

## Texture and interaction — reference, not required every build

These are dials with no owner elsewhere in the Chain Method. Pick
deliberately per build rather than defaulting to none:

- **Texture/grain** — none/flat · paper grain overlay · noise/dither ·
  halftone dots · fine grid lines · subtle drop-shadow/paper-stack
  depth.
- **Interaction signature** — cursor-follow element · magnetic buttons
  (pull toward cursor) · scroll-scrubbed canvas animation · hover-reveal
  content swap · marquee that speeds up on scroll velocity.

Palette, typography, layout paradigm, and animation personality are
`landing-systems`'s token system and `landing-sequencer`'s pacing spec —
this skill doesn't restate or re-decide those; if a shape choice here
seems to need a different color or pacing than the token system
specifies, flag it back rather than inventing a value.

## Style for a feeling — geometry parameters

Once `landing-strategist`'s adjectives have named a target feeling, pull
the geometry-side parameters from this table rather than eyeballing
them fresh. Color, saturation, and type weight stay owned by
`landing-systems`'s token system — only the columns below have no
existing Chain Method owner.

| Feeling | Geometry lean | Corner radius | Line/stroke weight | Grain |
|---|---|---|---|---|
| Playful | organic, occasionally mixed | large, irregular (40–70% asymmetric blobs) | thin-to-medium, varies | light noise or none |
| Luxurious | organic sweep or geometric-precise, never irregular-angular | small-to-none or one very large sweep | thin, precise hairlines | none, or fine metallic-feel gradient |
| Urgent/energetic | angular or mixed | sharp-to-medium, minimal softness | bold, thick | none |
| Trustworthy/calm | geometric-precise or mixed | medium, consistent (not irregular) | medium, consistent weight | none or barely-there grain |
| Nostalgic | organic | soft, slightly imperfect | variable/hand-drawn feel | paper grain, dust, halftone |
| Futuristic | angular or geometric-precise | sharp geometric or perfect circles, no in-between | thin precise lines or glowing thick | scan lines, fine grid, chromatic aberration |
| Cozy/intimate | organic | large, soft, rounded everywhere | soft, medium weight | soft paper grain |
| Bold/confident | angular or fully organic (dramatic sweep), rarely mixed | minimal, or one dramatic sweep | thick, decisive | none |
| Mysterious/moody | organic, irregular | irregular, partially obscured shapes | thin, sometimes broken/dashed | heavy grain, vignette, noise |
| Minimal/zen | geometric-precise | consistent, quiet radius (small or none) | thin, sparse | none |

A build can blend two adjacent rows — average or alternate the
parameters rather than picking one wholesale.

## Quality checklist before presenting

- No hand-authored SVG paths or freehand-guessed `clip-path`/
  `border-radius` coordinates anywhere — every shape traces to a
  formula or a sourced Lucide icon.
- No shape depends on a live `getBoundingClientRect()` (or similar)
  measurement — connections between elements are relative/percentage
  CSS positioning or a formula, not a DOM read.
- Responsive down to mobile — curves and blobs don't overflow or force
  horizontal scroll at narrow widths (test full-bleed elements sized
  wider than the viewport).
- Section transitions read as one continuous, deliberate flow (curved
  or angular, per the chosen geometry personality) — not isolated
  decorations bolted onto flat rectangles.
- `prefers-reduced-motion` respected on anything animated (blob
  morphing, canvas fields, cursor-follow interactions).

## Constraints

- This skill covers construction technique only. What the signature
  element is, why it recurs, and where it must appear are
  `landing-systems`'s step 6 decisions, audited by `landing-critic`'s
  traceability test — this skill doesn't originate those choices, only
  implements them.
- Lucide is the only icon source. Don't add a second icon library, an
  illustration set, or an animation-file format (Rive, Lottie) to work
  around a gap — build the shape from the technique library above
  instead.
- Don't install a new geometry or animation library to cover something
  this skill's techniques don't reach — `ogl` (canvas/WebGL) and CSS
  are this core's locked tools for shape construction; a felt need for
  another one is a signal to simplify the shape, not add a dependency.
