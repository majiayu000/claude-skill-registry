---
name: anima
description: "Summarizes how to use the Anima animation engine (Scene, Mobjects, Fluent API, Pro API, camera, timeline, rendering, and CLI). Use when authoring or explaining Anima animations."
---

# Using the Anima Engine

Anima is a TypeScript animation engine for mathematical visualizations. It runs on Bun and renders to canvas.

Import everything from `'anima'` (the package index). All classes, animations, and easing functions are exported from there.

## Quick Start

```ts
import { Scene, Circle, Rectangle, Color, easeInOutQuad } from 'anima';

export class MyScene extends Scene {
  constructor() {
    super({ width: 1920, height: 1080, frameRate: 60, backgroundColor: Color.BLACK });

    const circle = new Circle(1).stroke(Color.WHITE, 2).pos(-2, 0); // radius 1, at position (-2, 0)
    const rect = new Rectangle(2, 1).fill(Color.BLUE, 0.6).pos(2, 0); // 2×1, at position (2, 0)

    // Items in the same play() call run in PARALLEL
    this.play(
      circle.fadeIn(1).moveTo(0, 0, 1), // fadeIn 1s, then move to (x=0, y=0) over 1s
      rect.fadeIn(1)                     // fadeIn 1s (runs in parallel with circle's chain)
    );

    this.wait(0.5); // 0.5 second pause

    // Successive play() calls run SEQUENTIALLY
    this.play(circle.fadeOut(0.5)); // fadeOut over 0.5s
  }
}
```

Render with CLI: `anima render myfile.ts -s MyScene -o output.mp4`

## Coordinate System

Origin `(0, 0)` is screen center. Y-axis points **up**. Visible frame is ~14.2 × 8 world units at 1920×1080.

## Skill Modules

For detailed usage of each subsystem, read the relevant module:

| Module | What it covers |
|---|---|
| [Scene](rules/scene.md) | Scene setup, config, coordinate system, `play()`, `wait()`, `add()`/`remove()`, lifecycle rules |
| [Mobjects](rules/mobjects.md) | Mobject/VMobject hierarchy, immediate setters (`pos`, `show`, `hide`, `setScale`, `setRotation`), `saveState()`/`restore()` |
| [Geometry](rules/geometry.md) | `Circle`, `Rectangle`, `Line`, `Arrow`, `Arc`, `Polygon`, `Point` — constructors and usage |
| [Styling](rules/styling.md) | `Color` class (presets, `fromHex`, `fromHSL`), `.stroke()`, `.fill()`, default appearance rules |
| [Animations](rules/animations.md) | Fluent API (chaining), Pro API (explicit objects), `Sequence`, `Parallel`, `MorphTo`, `delay()`, hybrid usage |
| [Easing](rules/easing.md) | All 30+ easing functions: standard, bounce, Manim-style rate functions, choosing guide |
| [Camera](rules/camera.md) | `CameraFrame` animations (`zoomIn`, `zoomOut`, `centerOn`, `fitTo`, `zoomToPoint`), `Shake`, `Follow`, bounds, instant methods |
| [Text](rules/text.md) | `Text` creation from font files, `TextStyle`, glyph access, animating text |
| [Graph](rules/graph.md) | `Graph` nodes/edges, layout algorithms (`circular`, `tree`, `force-directed`), `updateEdges()` |
| [VGroup](rules/vgroup.md) | `VGroup` children management, `arrange()`, `center()`, `toCorner()`, `alignTo()`, cascading styles |
| [Keyframes](rules/keyframes.md) | `KeyframeAnimation`, `KeyframeTrack` — fine-grained multi-property keyframe control |
| [Rendering](rules/rendering.md) | `Renderer`, formats (mp4/webp/gif/sprite/png), `Resolution` presets, quality, CLI commands, `serialize`/`deserialize` |

## Core Rules for Authoring Scenes

1. **Extend `Scene`** and build everything in the constructor.
2. **Intro animations** (`fadeIn`, `write`, `draw`, `FadeIn`, `Write`, `Draw`) auto-add objects to the scene.
3. **Transform/exit animations** (`moveTo`, `rotate`, `scaleTo`, `fadeOut`, etc.) require the target to already be in the scene.
4. Use `this.add(obj)` for static objects that should be visible without animation.
5. All durations are in **seconds**.
6. All angles are in **radians**.
7. Multiple items in one `this.play(...)` call run in **parallel**. Successive `play()` calls run **sequentially**.
8. Use `this.wait(seconds)` to insert gaps between play calls.

## Long Video Tips

For 30–50 minute videos:

- **Structure in sections**: Group related animations with `this.wait()` between logical sections.
- **Use `saveState()` / `restore()`**: Save object positions before zooming in, restore to return.
- **Camera management**: Use `centerOn`, `fitTo`, and `zoomIn`/`zoomOut` to guide the viewer's focus.
- **Reuse objects**: `remove()` objects when done, `add()` new ones. Don't leave hundreds of invisible objects in the scene.
- **Use `Sequence` and `Parallel`**: For complex choreography, compose explicitly rather than deeply nesting fluent chains.
- **Keyframes**: For complex motion paths, use `KeyframeAnimation` instead of chaining dozens of `moveTo` calls.
- **Preview quality**: Use `quality: 'preview'` or the CLI `preview` command during iteration, switch to `production` for final render.
