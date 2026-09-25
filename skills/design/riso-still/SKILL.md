---
name: riso-still
description: Create or improve procedural risograph still art, illustrations, posters, print series and images in this repo. Develops reference-led composition, perspective, pose and ink plates; delivers a native-resolution PNG and self-contained Canvas 2D source. Use for standalone still requests; use riso-film for moving work.
---

# Riso still

Deliver `prints/<name>/index.html` and a native PNG in `out/`. Same medium as the films: Canvas
2D only, no libraries, fonts, images or network calls. External references are observation
sources, never embedded assets. If the user explicitly wants generated raster imagery, that is a
different workflow; do not quietly substitute it. Commands run in `tools/`.

## Develop the picture

Read `.claude/rules/riso-plates.md`, `docs/visual-development.md` and `docs/drawing.md` (its
composition and frame-budget sections apply in full); add `docs/scene-space.md` when perspective or
attached details matter and `docs/characters.md` for figures. Skip film timelines, transitions and
sound. [examples.md](examples.md) maps the shipped series (`prints/cabinet`, `prints/sceneries`,
`prints/workings`); open the matching source before inventing a routine it already has.

Extract subject, feeling, format and exclusions. If the user wants ideas, offer different scenes
or viewpoints; if they want art, choose and draw. Default to 1080 square only when no format was
given; record other sizes before composing.

- An open request ("a collection", "detailed sceneries", "your strengths") is permission to
  art-direct a series of three to five prints under one principle stated up front: one
  construction style held across different subjects (`prints/cabinet`), or one technical strength
  per print (`prints/sceneries`: constructed perspective with fog, lights with reflection, strata
  with layered haze).
- For an unfamiliar subject, look at real references and note proportions, gesture, construction
  and material; measure in the photo's own pixel frame where it matters (wing outline, vein and
  eyespot positions). A mood adjective or an unopened image link is not enough.
- For ambitious work, compare small compositions with different viewpoints and value groupings,
  then develop the strongest. A local edit needs less setup.
- Solve support, perspective, occlusion and identity before detail. Draw figure landmarks and
  contact points before clothing or texture: the hand reaches the tool, the tool meets the work.
  Build details on shared surfaces so ellipses, slats and legs agree on orientation and scale.
  Grow natural subjects from their own geometry (a logarithmic spiral, Vogel's floret model, a
  distance transform from a cavity wall), so every mark sits where growth put it.
- A film's 0.25 s reading time does not govern a still: sustained detail is allowed, but marks
  should explain form, material or the moment. Concentrate detail at the focus and leave quiet
  areas. Random hatching and misregistration do not rescue weak drawing.

## Build and inspect

```
node new-riso.mjs --kind still --out ../prints/<name>/index.html
node verify.mjs ../prints/<name>/index.html --times 0,1,2
node still.mjs ../prints/<name>/index.html --at 0 --out ../out/<name>.png
```

The starter is blank paper with the print and craft kits and no animation loop. Draw in its art
block. A single picture uses `duration: 1` and a `seek(t)` that draws the same picture; a series
uses integer print indices (`floor(t)`, as `prints/workings` does), verified at every index and
exported one PNG per index. No MP4, score or artificial motion.

For another native size, change canvas, paper, plate dimensions, projection and screen pitch
before baking, and audit square assumptions like `W,W`. Larger prints must rerasterize geometry
and screens at that size; CSS/DPR enlargement and PNG upscaling do not make a higher-resolution
original. Press-ready separations need a separate print-production brief.

- 2160 square (`OUT = 2160`, `K = OUT / W`) served both Cabinet and Sceneries. `PITCH = 4.6 * K`
  (9.2 device px) is the same picture enlarged, right for landscape masses; small dense subjects
  took a finer `3.4 * K` (6.8 px). Registration scales with `K`.
- Fine engraved line needs coverage 1 to print solid; the kit's threshold tile leaves the
  interstices open even at full coverage (right for film tone), which breaks thin line into dots.
- A feature under a few screen cells (florets, scales, birds) is modelled by shape and solid
  overprint, not dot size. A small fixed dither on mid-tones breaks remaining dot-size steps in a
  gentle ramp; leave paper and solids untouched. At 2160, centre the screen's dots on pixels
  (`docs/drawing.md`, tone that prints) or ramps contour into rings.
- Add debug views by query string before polishing: construction lines alone compared against
  the reference diagram (it caught over-curved septa in a shell section), and one ink at a time
  for plate isolation.

Inspect the whole picture at viewing size, a value/silhouette view, and 1:1 crops of difficult
anatomy, attachments and screen. Fix perspective, tangencies, missing support or an unclear
subject before polishing grain; `docs/quality-bar.md` lists the review cases. `still.mjs` exports
the canvas backing store and checks repeatability; it does not judge the art. Confirm dimensions
and open the PNG.

Keep a short `PRINT.md` beside substantial work: request, the series principle, references per
print, viewpoint, geometry and light decisions, native size and pitch, inspected output and each
print's remaining weaknesses. Keep the previous version when revising.
