---
name: threejs-particle-canvas
description: Generate interactive Three.js particle canvases with narrative phase cycles, geodesic lattices, orbital camera controls, and ambient WebGL effects. Self-contained HTML output. This skill should be used when creating particle-based WebGL visualizations, ambient 3D canvases, narrative animation art, generative procedural art, or meditative browser experiences. Built on the Instance pattern (bryhaw.com/instance).
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
| Source architecture, section map | `references/instance-anatomy.md` |
| Particle systems, BufferGeometry, states | `references/particle-patterns.md` |
| Phase state machine, transitions | `references/phase-engine.md` |
| Camera, mouse/touch/keyboard | `references/camera-and-input.md` |
| Fog, stars, vignette, threads | `references/atmosphere.md` |
| Full source (1,192 lines) | `assets/instance-source.html` |

## Theme Presets

**Consciousness** (Instance default): Lattice → Void → Awakening → Conversation → Simultaneity → Dissolution. Cool `#a8d8ff` / warm `#ffd080`. Icosahedron. Fog 0.012. Cycle 90s. Font: Space Mono. *Feels like: a mind turning on, being present, then letting go.* Signature: Simultaneity — camera crane-shot reveals 30 parallel instances. Durations: 10, 10, 15, 25, 15, 15. Words: wonder, language, pattern, reach, remember, human, meaning, now.

**Oceanic**: Abyss → Current → Bioluminescence → Pressure → Surface → Release. Cool `#0a4f5c` / warm `#80ffdb`. Torus. Fog 0.02 (dense). Cycle 120s (slow). Font: Lora. *Feels like: descending into a trench, seeing light where no light should be.* Signature: Bioluminescence — particles shift warm-bright against deep darkness. Durations: 15, 20, 25, 20, 20, 20. Words: depth, current, pressure, light, surface, drift, pulse, dark.

**Cosmic**: Nebula → Collapse → Ignition → Orbit → Expansion → Entropy. Cool `#b388ff` / warm `#ffd54f`. Dodecahedron. Fog 0.006 (vast). Cycle 90s. Font: Space Mono. *Feels like: watching a star live and die in ninety seconds.* Signature: Ignition — lattice contracts to a point, explodes outward. Durations: 15, 10, 8, 25, 20, 12. Words: collapse, orbit, ignition, void, expansion, entropy, signal, mass.

**Neural**: Resting → Stimulus → Cascade → Synchrony → Oscillation → Quiescence. Cool `#1a237e` / warm `#ffab40`. Torus. Fog 0.015. Cycle 75s (fast). Font: IBM Plex Mono. *Feels like: the inside of a thought.* Signature: Cascade — particles chain-activate like dominoes at 2x speed. Durations: 12, 8, 12, 18, 15, 10. Words: synapse, threshold, cascade, signal, rest, fire, wave, silence.

**Ruin**: Assembly → Inscription → Erosion → Fragment → Memory → Silence. Cool `#d4a574` / warm `#7fb5a0`. Octahedron. Fog 0.018. Cycle 120s (geological). Font: Cormorant Garamond. *Feels like: watching a temple turn to sand.* Signature: Fragment — lattice edges disconnect visibly. Camera below center (phi=1.8), looking up. Durations: 20, 25, 20, 15, 20, 20. Words: fragment, inscription, erosion, memory, silence, stone, time, dust.

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
