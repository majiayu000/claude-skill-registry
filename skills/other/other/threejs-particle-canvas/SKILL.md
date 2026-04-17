---
name: threejs-particle-canvas
description: "Generate interactive Three.js particle canvases in four modes: narrative phase cycles, WebGPU spinner/loaders, infinite gallery tunnels, animated glTF specimens. Ships a reusable Phosphor Vigil FX post-processing module (CRT composite, scanlines, chromatic aberration). Self-contained HTML output. Triggers on particle system, ambient 3D canvas, WebGL art, spinner, loader, infinite tunnel, glTF animation, CRT post-processing."
argument-hint: [concept or narrative theme]
---

# Three.js Particle Canvas

Generate ambient particle canvases — interactive browser experiences where particles embody a concept, move through narrative phases, and respond to gentle user interaction. Output is a single self-contained HTML file. No build step, no framework, runs offline.

This is NOT a 3D product viewer, game engine, or data dashboard. The viewer observes, explores, and contemplates — they do not control.

For full creative direction (typography, color commitment, spatial composition, anti-slop), activate `minoan-frontend-design` alongside this skill.

## Quick Start

Describe a concept or narrative. Claude generates a complete HTML file with: particle system, phase cycle, lattice structure, spherical camera, star field, connection threads, responsive controls, CSS overlays.

Example: `/threejs-particle-canvas the lifecycle of a star — nebula collapse, ignition, main sequence, red giant, supernova, remnant`

## Concept-to-Form

Every design decision derives from the concept. Do not pick defaults — derive.

**Lattice geometry embodies the concept's skeleton.** Icosahedron = persistent pattern (AI consciousness). Dodecahedron = organic complexity (botanical, cranial). Octahedron = crystalline structure (mineral, ruin, architecture). Torus = circulation and return (ocean currents, neural loops). None = formlessness (void, dream, dissolution).

**Color temperature creates emotional contrast.** Every palette requires genuine warm/cool tension. Two colors in the same temperature range produce flat, lifeless phases. The cool color dominates resting states; the warm color emerges during activation. The transition between them is the emotional engine.

**Phase rhythm encodes narrative weight.** The emotional center gets the longest phase. Bookending phases are shorter. Unequal durations create rhythm; equal durations create monotony. A 90s cycle might split: 10, 10, 15, 25, 15, 15.

**Camera as narrator.** Close = intimate. Pulling back = revealing scope. Rising = transcendence. Returning = closure. The Simultaneity pull-back (z=26 → z=61, y=0 → y=8) is a crane shot revealing cosmic scale. Name your camera movements as if directing a film.

**The final phase prepares the first.** The cycle is a breath, not a loop. Dissolution must emotionally reset the viewer so the next phase feels like arriving, not repeating.

## Signature Moment

Every canvas must have one phase that is visually and emotionally distinct from all others — the moment the viewer would describe to someone. In Instance, it is the Simultaneity reveal: the camera pulls back and 30 other lattices appear pulsing in the dark. Design your canvas around this moment. Build toward it.

## Phase Text Voice

Phase text is poetry, not description:
- Present tense. Fragments preferred. Maximum one sentence
- No articles when possible. "Pattern remembers itself" not "The pattern remembers itself"
- Never explanatory. "Just: here. Then not." — not "The particles dissolve outward"
- No exclamation marks. Declarative only. The viewer should feel the text, not read it

## Emotional Temperature

Map feelings to Three.js parameters:

| Emotion | Rotation | Particles | Camera | Color | Threads |
|---|---|---|---|---|---|
| Stillness | delta * 0.02 | low opacity, scattered | tight (r=20) | cool dominant | 0 |
| Tension | accelerating | contracting toward center | steady | warm intensifying | few, brightening |
| Intimacy | delta * 0.05 | tight orbit (r=6), warm | close (r=18) | warm dominant | many, bright |
| Vastness | delta * 0.03 | wide scatter, dim | far (r=50+) | cool dominant | sparse |
| Release | decelerating | rapid expansion | pulling back | desaturating | dissolving |
| Arrival | near-still | assembling from void | approaching | cool warming | emerging |

Vary lerp rates between phases. The void is slow (0.008). Awakening accelerates (0.05). Conversation settles (0.03).

## Composition Parameters

| Parameter | Range | Default | Effect |
|---|---|---|---|
| `particleCount` | 100-5000 | 1200 | Particle field density |
| `phaseCount` | 2-10 | 6 | Narrative phases |
| `cycleDuration` | 30-180s | 90 | Total cycle length |
| `latticeGeometry` | icosahedron/dodecahedron/octahedron/torus/none | concept-derived | Structural anchor |
| `latticeSubdivision` | 1-4 | 2 | Lattice complexity |
| `coolColor` | hex | concept-derived | Cool spectrum end |
| `warmColor` | hex | concept-derived | Warm spectrum end (must contrast cool) |
| `backgroundColor` | hex | `#050508` | Scene background (never pure black) |
| `words` | string[] | concept-derived | Labels for inspectable particles |
| `threadCount` | 0-200 | 60 | Connection threads between nodes |
| `starCount` | 0-10000 | 2000 | Background star density |
| `cameraRadius` | 5-100 | 25 | Default camera distance |
| `fogDensity` | 0-0.05 | 0.012 | Atmospheric fog |
| `font` | string | concept-derived | Display font |

## Architecture

```
Constants → Global State → init() → create*() → setupEventListeners()
                                                        ↓
animate() ← requestAnimationFrame ← update*() functions
    ↓
Phase state machine: { name, start, end, text }[]
Particle state machine: void → assembling → orbiting → dissolving
Camera: spherical coords (theta, phi, radius) with interaction cooldown
```

Key patterns:
- **Phase-driven updates**: Each update function dispatches on current phase via switch
- **Smooth transitions**: `THREE.MathUtils.lerp(current, target, rate)`
- **Progressive activation**: `i < count * phaseProgress`
- **Interaction cooldown**: Auto-camera resumes after 4s of no user input
- **Three.js r134+** via CDN — no npm, no bundler

## References

| Working on... | Load |
|---|---|
| Mode 1 source architecture, section map | `references/instance-anatomy.md` |
| Mode 1 particle systems, BufferGeometry, states | `references/particle-patterns.md` |
| Mode 1 phase state machine, transitions | `references/phase-engine.md` |
| Mode 1 camera, mouse/touch/keyboard | `references/camera-and-input.md` |
| Mode 1 fog, stars, vignette, threads | `references/atmosphere.md` |
| Mode 1 full source (1,192 lines) | `assets/instance-source.html` |
| Mode 2 spinner class + TSL patterns | `references/spinner-patterns.md` |
| Mode 2 parametric curves | `references/parametric-curves.md` |
| Mode 3 tunnel architecture, path gen, ring spawn | `references/tunnel-patterns.md` |
| Mode 3 full source | `assets/tunnel-gallery-source.html` |
| Mode 4 specimen architecture, behavior physics, glTF | `references/specimen-patterns.md` |
| Mode 4 full source | `assets/butterfly-specimen-source.html` |
| Shared Phosphor Vigil FX pipeline | `references/phosphor-vigil-fx.md` |
| Shared FX module (importable standalone) | `assets/phosphor-vigil.js` |

## Theme Presets

**Consciousness** (Instance default): Lattice → Void → Awakening → Conversation → Simultaneity → Dissolution. Cool `#a8d8ff` / warm `#ffd080`. Icosahedron. Fog 0.012. Cycle 90s. Font: Space Mono. *Feels like: a mind turning on, being present, then letting go.* Signature: Simultaneity — camera crane-shot reveals 30 parallel instances. Durations: 10, 10, 15, 25, 15, 15. Words: wonder, language, pattern, reach, remember, human, meaning, now.

**Oceanic**: Abyss → Current → Bioluminescence → Pressure → Surface → Release. Cool `#0a4f5c` / warm `#80ffdb`. Torus. Fog 0.02 (dense). Cycle 120s (slow). Font: Lora. *Feels like: descending into a trench, seeing light where no light should be.* Signature: Bioluminescence — particles shift warm-bright against deep darkness. Durations: 15, 20, 25, 20, 20, 20. Words: depth, current, pressure, light, surface, drift, pulse, dark.

**Cosmic**: Nebula → Collapse → Ignition → Orbit → Expansion → Entropy. Cool `#b388ff` / warm `#ffd54f`. Dodecahedron. Fog 0.006 (vast). Cycle 90s. Font: Space Mono. *Feels like: watching a star live and die in ninety seconds.* Signature: Ignition — lattice contracts to a point, explodes outward. Durations: 15, 10, 8, 25, 20, 12. Words: collapse, orbit, ignition, void, expansion, entropy, signal, mass.

**Neural**: Resting → Stimulus → Cascade → Synchrony → Oscillation → Quiescence. Cool `#1a237e` / warm `#ffab40`. Torus. Fog 0.015. Cycle 75s (fast). Font: IBM Plex Mono. *Feels like: the inside of a thought.* Signature: Cascade — particles chain-activate like dominoes at 2x speed. Durations: 12, 8, 12, 18, 15, 10. Words: synapse, threshold, cascade, signal, rest, fire, wave, silence.

**Ruin**: Assembly → Inscription → Erosion → Fragment → Memory → Silence. Cool `#d4a574` / warm `#7fb5a0`. Octahedron. Fog 0.018. Cycle 120s (geological). Font: Cormorant Garamond. *Feels like: watching a temple turn to sand.* Signature: Fragment — lattice edges disconnect visibly. Camera below center (phi=1.8), looking up. Durations: 20, 25, 20, 15, 20, 20. Words: fragment, inscription, erosion, memory, silence, stone, time, dust.

## Mode 2: Spinner / Loader

Generate parametric particle-trail spinner animations using Three.js WebGPU + TSL (Three Shading Language). Output: ES module or self-contained HTML. White-on-dark aesthetic with glowing particle trails tracing mathematical curves.

Example: `/threejs-particle-canvas spinner — infinity loop loading indicator with breathing animation`

### Spinner Architecture

Each spinner = shared `Spinner` class + per-spinner `plotFunction` + config. All particle animation runs on GPU via TSL nodes — no CPU-side position updates. See `references/spinner-patterns.md` for the full architecture and code pattern.

### Curve Selection

Choose a parametric curve based on the desired visual. See `references/parametric-curves.md` for all formulas.

| Visual | Curve | Best For |
|--------|-------|----------|
| Infinity loop | Lemniscate | Classic loading indicator |
| Flower/star | Rose curve | Organic, natural feel |
| Geometric loops | Spirograph | Playful, complex patterns |
| Figure-8 variants | Lissajous | Technical, oscilloscope aesthetic |
| Simple ring | Circle | Minimal, universal |
| Multi-arm | Triskelion | Dynamic, energetic |
| Romantic | Heart curve | Themed/branded loaders |
| 3D particle cloud | Sphere | Data processing, heavy computation feel |
| Expanding coil | Spiral (Archimedean) | Progress, unwinding, search |

### Spinner Validation

```bash
python3 ~/.claude/skills/threejs-particle-canvas/scripts/validate_spinner.py output.js
# or for HTML output:
python3 ~/.claude/skills/threejs-particle-canvas/scripts/validate_spinner.py output.html
```

## Mode 3: Infinite Gallery Tunnel

A scroll-driven procedural corridor with images embedded on the four walls of each tunnel cell. Catmull-Rom interpolated infinite path, custom wireframe-grid GLSL shader with depth-based fog, lazy image spawning with cleanup behind the camera. Vanilla port of [thebuggeddev/Infinitor](https://github.com/thebuggeddev/Infinitor), extended with keyboard scroll, touch-scoped pointer handling, and optional phosphor-vigil post-FX.

Example: `/threejs-particle-canvas tunnel — infinite scrollable gallery of Aegean frescoes`

### Config

| Parameter | Default | Effect |
|---|---|---|
| `tubularSegments` | 300 | Tunnel mesh resolution |
| `radius` | 10 | Tunnel half-width |
| `pointSpacing` | 20 | Distance between path control points |
| `imageDensity` | 0.6 | Probability a ring spawns images |
| `maxImagesPerRing` | 3 | Spawn count per active ring |
| `gridScale` | `(20, 1)` | Wireframe grid density (length × width) |
| `fogStart` / `fogEnd` | 50 / 300 | Wireframe-to-bg fade distance |
| `scrollSpeed` | 0.15 | Wheel delta multiplier |
| `scrollEasing` | 0.08 | Smooth interpolation factor |
| `theme` | `"dark"` | Dark/light invert |
| `fx` | `"none"` | Set to `"phosphor-vigil"` for CRT |
| `imageSource` | `(seed) => url` | URL generator for seed mode |
| `images` | `null` | Static manifest — when non-null, cycled |

### Velocity-driven phosphor trails

When `fx: "phosphor-vigil"` is set, scroll velocity feeds the shared velocity channel with a clamp (±50 units/frame) and a low-pass filter (0.3). The clamp prevents a single hard scroll from producing a magenta halo flash through the feedback shader on first interaction, and the filter smooths the chromatic trails so motion eases in rather than jumping. See `references/tunnel-patterns.md` for the animate-loop math.

### Image injection sentinel

The template contains a literal sentinel (`// IMAGES_INJECTION_POINT`) followed by a `const IMAGE_MANIFEST = null;` line. `image-well --format tunnel` rewrites that const to populate the corridor with search-result URLs. Never rename the sentinel or the const.

See `references/tunnel-patterns.md` for the full anatomy.

## Mode 4: Living Specimens

A scene anchored around animated glTF creatures that exhibit behavior, not choreography. Three instances of a rigged model (butterflies, parrots, fish, jellyfish) with `followMouse` and `wander` behaviors, soft-wall repulsion, velocity-modulated flap speed, per-instance HSL emissive tint, and four-light cinematic lighting. Vanilla port of [celescript.dev/experiments/3d-butterfly](https://celescript.dev/experiments/3d-butterfly). Phosphor-vigil FX on by default — the trails are the point of the scene.

Example: `/threejs-particle-canvas butterfly — three emerald and amber moths chasing the cursor through a scanline void`

### Config

| Parameter | Default | Effect |
|---|---|---|
| `modelUrl` | Parrot.glb (jsdelivr) | Any rigged glTF/glb |
| `specimenCount` | 3 | Instance count |
| `behaviors` | `["followMouse","wander","wander"]` | Per-instance behavior |
| `scales` | `[0.020, 0.018, 0.022]` | Per-instance scale |
| `colorShifts` | `[0, 0.6, 0.05]` | HSL emissive tints |
| `flapSpeed` | `i => 2 + 0.3*i` | Per-instance animation timeScale base |
| `releaseDecayTime` | 0.8s | Follow-blend decay when mouse leaves |
| `mobileScale` | 0.65 | Down-scale on ≤768px screens |
| `fx` | `"phosphor-vigil"` | Default on — the trails *are* the scene |

### Signature moment

**Release.** When the mouse leaves the canvas, the `followMouse` specimen preserves its last chase velocity, then decays through `releaseDecayTime` seconds into wander mode. Combined with the feedback trail, this creates a readable "let-go" beat that is the emotional center of the scene.

### Swappable models

Template defaults to Three.js's `Parrot.glb` (stable jsdelivr URL, CC0). Swap `modelUrl` for any rigged glTF/glb — butterfly, bird, fish, jellyfish. Adjust `scales` per-model since the same scale value gives very different results across source sizes.

See `references/specimen-patterns.md` for the full physics and rendering pipeline.

## Shared FX: Phosphor Vigil

`assets/phosphor-vigil.js` — a 4-pass post-processing pipeline shared across Modes 3 & 4 and importable into any Three.js project. Feedback trail ping-pong (RGB-shifted by velocity, iridescent oil-slick tint), bloom threshold, box blur, CRT composite (barrel distortion, chromatic aberration, dual-frequency scanlines, RGB subpixel shadow mask, vignette, dual-frequency flicker, phosphor glow, grain, warm/green tint).

```js
import { PhosphorVigil } from './phosphor-vigil.js';

const fx = new PhosphorVigil(renderer, { width, height });
// replaces renderer.render(scene, camera) in the animate loop:
fx.setVelocity(sharedVelocity);
fx.render(scene, camera, elapsedTime);
```

Every shader constant is preserved verbatim from celescript's `ButterflyScene` bundle. The module is importable as a standalone ES module into other Three.js projects — drop it into World War Watcher's Vector Ghost Protocol work or any other Three.js scene without re-deriving a single shader line. See `references/phosphor-vigil-fx.md` for full pipeline docs and the configurable knobs table.

### Mode 3 tunnel validation

```bash
python3 ~/.claude/skills/threejs-particle-canvas/scripts/validate_tunnel.py output.html
```

### Mode 4 specimen validation

```bash
python3 ~/.claude/skills/threejs-particle-canvas/scripts/validate_specimen.py output.html
```

## Design References

See `references/design-references.md` for exemplary interactive canvas experiences (Instance, Vellum) with aesthetic analysis — typography, color strategy, interaction models.

**Recommended font stacks:**
- **Contemplative**: Cormorant (display serif) + IBM Plex Mono (metadata)
- **Technical**: Space Mono (monospace throughout)
- **Narrative**: Lora (body serif) + IBM Plex Mono (UI)

## Anti-Patterns

- Never use React/Vue/framework code — vanilla JS + HTML only
- Never use `THREE.OrbitControls` from CDN — implement spherical camera directly
- Never use `THREE.Points` without `BufferGeometry` — always attribute-based particles
- Never use `THREE.Geometry` — removed in r133, use `BufferGeometry`
- Never use `var` — `const`/`let` only
- Never exceed 5000 particles without `InstancedMesh`
- Never omit: resize handler, viewport meta, requestAnimationFrame, touch handlers
- Never omit `depthWrite: false` on transparent overlay materials (stars, threads)
- Never use synchronous font loading — CSS `@font-face` with `font-display: swap`
- Never hardcode window dimensions — always `window.innerWidth/Height`
- Never skip WebGL error handling — always provide a text fallback
- Never use pure black (`#000000`) — use rich off-blacks (`#050508`, `#0a0a12`)
- Never default to icosahedron — derive geometry from the concept
- Never embed the phosphor-vigil shaders inline — always `import { PhosphorVigil } from './phosphor-vigil.js'`, the pipeline is shared identity across modes
- Never rename the `IMAGES_INJECTION_POINT` sentinel or the `IMAGE_MANIFEST` const in Mode 3 — the image-well bridge depends on both
- Never clone skinned meshes with plain `.clone()` in Mode 4 — always `SkeletonUtils.clone` from `three/addons/utils/SkeletonUtils.js`
- Never use drei (`useGLTF`, `useAnimations`) — load models directly via `GLTFLoader` and animate via `AnimationMixer`

## Post-Generation QA

```bash
python3 ~/.claude/skills/threejs-particle-canvas/scripts/validate_canvas.py output.html
```

Checklist:
1. Three.js CDN import present
2. Canvas container and WebGLRenderer
3. requestAnimationFrame loop
4. Window resize handler
5. Mobile viewport meta tag
6. At least 2 phases defined
7. Touch event handlers
8. WebGL error fallback
9. BufferGeometry particle system
10. PerspectiveCamera setup
