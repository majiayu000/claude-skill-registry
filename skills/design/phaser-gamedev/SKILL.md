---
name: phaser-gamedev
description: "Phaser 3 2D game dev: scenes, physics, tilemaps, sprites, polish."
agent: typescript-frontend-engineer
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - phaser
    - 2d game
    - platformer
    - arcade physics
    - tilemap
    - sprite sheet
    - side scroller
  pairs_with:
    - typescript-frontend-engineer
    - game-asset-generator
  complexity: Medium
  category: game-development
---

# Phaser Gamedev Skill

## Overview

This skill builds complete Phaser 3 2D games using a **Phased Construction** pattern: DESIGN (plan game type, physics, scenes) → BUILD (scene lifecycle, sprites, tilemaps) → ANIMATE (physics, animation state machines, input) → POLISH (camera effects, particles, tweens, sound, mobile). Targets Phaser 3.60+ throughout.

**Scope**: Platformers, arcade shooters, top-down RPGs, puzzle games, and side-scrollers — anything 2D in Phaser 3. Use `threejs-builder` for 3D games, native mobile games, and non-Phaser canvas work.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| `references/core-patterns.md` | `core-patterns.md` | Always |
| `references/build-scaffolds.md` | `build-scaffolds.md` | Phase 2 BUILD |
| `references/animate-scaffolds.md` | `animate-scaffolds.md` | Phase 3 ANIMATE |
| `references/polish-scaffolds.md` | `polish-scaffolds.md` | Phase 4 POLISH |
| `references/errors.md` | `errors.md` | Error Handling |
| `references/arcade-physics.md` | `arcade-physics.md` | Arcade physics |
| `references/tilemaps.md` | `tilemaps.md` | Tilemap / Tiled |
| `references/spritesheets.md` | `spritesheets.md` | Sprites / animation |
| `references/performance.md` | `performance.md` | Performance concern |
| `references/game-feel-patterns.md` | `game-feel-patterns.md` | Polish / juice signal |
| `references/tilemaps-and-physics.md` | `tilemaps-and-physics.md` | Complex maps / Matter.js |

## Instructions

### Phase 1: DESIGN

**Goal**: Understand what to build, select the physics system, and plan the scene graph before writing any code.

**Core constraints**:
- **Read repository CLAUDE.md before building** — local standards override defaults here
- **Select physics system before any other decision** — Arcade (fast AABB), Matter.js (complex shapes), or no physics cannot be mixed per scene without deliberate design
- **Plan scenes upfront** — Boot → Preload → Game → UI is the standard flow; diverge only when the game requires it

**Step 1: Identify the game type**

From the user's request, determine: game genre (platformer, shooter, RPG, puzzle, side-scroller), primary physics need, number of scenes, tilemap or procedural world, spritesheet or texture atlas.

**Step 2: Select the physics system**

| Physics | Use When | When Not to Use |
|---------|----------|------------|
| Arcade | Platformers, shooters, simple AABB | Rotating bodies, non-rectangular shapes |
| Matter.js | Physics puzzles, destructible terrain | Performance-critical (100+ bodies) |
| None | Puzzles, card games, UI-only | Any meaningful collision detection |

**Step 3: Document the scene plan and load references**

Write a short markdown scene plan covering: Boot, Game, UI, Physics choice, World, Sprites (measured frame dimensions).

Load these references based on the plan:
- Always: `references/core-patterns.md` (scene lifecycle, transitions, input)
- If tilemap: `references/tilemaps.md`
- If sprites/animation: `references/spritesheets.md`
- If Arcade physics: `references/arcade-physics.md`
- If performance concern or many moving objects: `references/performance.md`
- If polish / game feel / juice signal ("screen shake", "particles", "game feel", "hit feedback", "satisfying"): `references/game-feel-patterns.md`
- If Matter.js, slopes, object layers, complex collision, or enemy spawning from Tiled: `references/tilemaps-and-physics.md`

**Gate**: Scene plan documented. Physics system selected. References loaded. Proceed only when gate passes.

---

### Phase 2: BUILD

**Goal**: Implement the scene lifecycle skeleton, load assets, place sprites, wire up tilemaps.

**Core constraints**:
- **MEASURE spritesheet frames before loading** — wrong `frameWidth`/`frameHeight` is the #1 Phaser bug; open the PNG, count pixels per frame before writing `this.load.spritesheet()`
- **Preload all assets in `preload()`** — never load assets in `create()` or `update()`
- **Use a Boot scene for asset loading** — shows a progress bar, keeps Game scene clean

Full TypeScript scaffolds (entry point, BootScene with progress bar, GameScene skeleton): `references/build-scaffolds.md`.

**Gate**: Boot and Game scenes compile. Assets load without console errors. Scene transitions work. Proceed only when gate passes.

---

### Phase 3: ANIMATE

**Goal**: Add physics-driven movement, animation state machines, and player input.

**Core constraints**:
- **Never allocate objects in `update()`** — no `new Phaser.Math.Vector2()`, no `this.physics.add.sprite()`, no array creation per frame; allocate in `create()`, reuse in `update()`
- **Use `delta` for frame-rate-independent movement** — `velocity = speed * (delta / 1000)` ensures consistent feel at any FPS
- **State machine over boolean flags** — `'idle' | 'walk' | 'jump' | 'attack' | 'dead'` prevents impossible states like `isJumping && isAttacking`

Animation definitions (`anims.create`), the Player state machine, and input handling scaffolds: `references/animate-scaffolds.md`. Collision groups, overlap callbacks, and physics tuning: `references/arcade-physics.md`.

**Gate**: Player moves. Animations transition correctly. State machine has no impossible state combinations. No per-frame allocations. Proceed only when gate passes.

---

### Phase 4: POLISH

**Goal**: Add camera work, particles, tweens, sound, and mobile controls. Verify performance.

**Core constraints**:
- **Remove `debug: true` from physics config** before shipping
- **Remove all `console.log` calls** unless the user explicitly requested logging
- **Test on a 60 FPS budget** — Arcade + 200 active bodies + 50 particles is the practical ceiling on mid-range mobile

Full scaffolds for camera effects, particles (Phaser 3.60+ API), tweens, sound, mobile virtual controls, and final verification steps: `references/polish-scaffolds.md`.

**Gate**: Polish checks pass. Performance within budget. Debug config removed. Game is shippable.

---

## Error Handling

Common errors and fixes (spritesheet frame mismatches, undefined body access, tilemap collision no-ops, animation failures, mobile slowdowns): `references/errors.md`.

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/core-patterns.md` | Always | Scene lifecycle, transitions, input, state machines |
| `references/build-scaffolds.md` | Phase 2 BUILD | TypeScript entry point, BootScene with progress bar, GameScene skeleton |
| `references/animate-scaffolds.md` | Phase 3 ANIMATE | Animation definitions, Player state machine, input handling |
| `references/polish-scaffolds.md` | Phase 4 POLISH | Camera, particles, tweens, sound, mobile controls, verification |
| `references/errors.md` | Error Handling | Common Phaser error scenarios and fixes |
| `references/arcade-physics.md` | Arcade physics | Groups, colliders, velocity, physics tuning, pitfalls |
| `references/tilemaps.md` | Tilemap / Tiled | Layer system, collision, animated tiles, object layers |
| `references/spritesheets.md` | Sprites / animation | Frame measurement, loading, atlases, nine-slice |
| `references/performance.md` | Performance concern | Object pooling, GC avoidance, texture atlases, mobile |
| `references/game-feel-patterns.md` | Polish / juice signal | Screen shake, particle bursts, hit-stop, scale punch, tween chains, sound timing |
| `references/tilemaps-and-physics.md` | Complex maps / Matter.js | Tiled integration pipeline, Matter.js vs Arcade decision table, collision categories, slopes, object layer spawning |
