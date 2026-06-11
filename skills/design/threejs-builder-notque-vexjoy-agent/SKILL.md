---
name: threejs-builder
description: "Three.js app builder: imperative, React Three Fiber, and WebGPU in 4 phases."
agent: typescript-frontend-engineer
user-invocable: false
command: /threejs
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
    - threejs
    - three.js
    - 3D web
    - 3D scene
    - WebGL
    - WebGPU
    - 3D animation
    - 3D graphics
    - react three fiber
    - r3f
    - drei
    - react-three
    - "@react-three/fiber"
    - postprocessing 3D
    - TSL shader
    - three shading language
    - compute shader three
    - WebGPURenderer
    - node material three
    - game architecture three
    - gltf loading
    - glb model
    - animation state machine three
    - eventbus game
    - game state management three
    - three.js game
  pairs_with:
    - typescript-frontend-engineer
    - react-native-engineer
    - distinctive-frontend-design
  complexity: Medium
  category: frontend
---

# Three.js Builder Skill

## Overview

This skill builds complete Three.js web applications using a **Phased Construction** pattern with four phases: Design, Build, Animate, Polish. It supports three paradigms — imperative Three.js, React Three Fiber (R3F), and WebGPU — detected automatically from project context. Only the relevant paradigm's reference is loaded.

**Scope**: Use for 3D web apps, interactive scenes, WebGL/WebGPU visualizations, R3F declarative 3D, and product viewers. For game engines, 3D model creation, VR/AR experiences, or CAD workflows, use a more specialized skill.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| `@react-three/fiber`, `r3f`, `drei`, `useFrame`, `<Canvas>`, `<mesh>`, React project with 3D | `react-three-fiber.md` | **React Three Fiber** |
| `WebGPURenderer`, `TSL`, `tsl`, `compute shader`, `wgsl`, `node material`, WebGPU mentioned | `webgpu.md` | **WebGPU** |
| Standalone HTML, CDN imports, `new THREE.Scene()`, no React, vanilla JS/TS | `advanced-topics.md` (load as needed)` | **Imperative** |
| Game project: `EventBus`, `GameState`, player controller, enemies, scoring, multiple game systems | `game-patterns.md` (alongside paradigm reference)` | **Game architecture** |
| GLTF/GLB model loading, `.glb` files, animated characters, skeletal rigs, model import | `gltf-loading.md` (alongside paradigm reference)` | **GLTF loading** |
| `references/build-recipes.md` | `build-recipes.md` | Phase 2/3 build, error diagnosis |
| `references/advanced-topics.md` | `advanced-topics.md` | Imperative paradigm |
| `references/react-three-fiber.md` | `react-three-fiber.md` | R3F paradigm |
| `references/webgpu.md` | `webgpu.md` | WebGPU paradigm |
| `references/visual-polish.md` | `visual-polish.md` | Visual quality signal |
| `references/gltf-loading.md` | `gltf-loading.md` | GLTF/GLB model loading signal |
| `references/game-patterns.md` | `game-patterns.md` | Game project signal |
| `references/game-architecture.md` | `game-architecture.md` | Game project signal |
| `references/shader-patterns.md` | `shader-patterns.md` | Custom GLSL / visual effects |
| `references/performance-patterns.md` | `performance-patterns.md` | Performance / many objects |
| `references/advanced-animation.md` | `advanced-animation.md` | Animation systems / skeletal rigs |

## Instructions

### Phase 1: DESIGN

**Goal**: Detect the paradigm, understand what the user wants, and select appropriate components.

**Core Constraints**:
- **Build only what the user asked for** — no speculative features or "while I'm here" additions
- **Detect the paradigm before selecting components** — imperative, R3F, and WebGPU have fundamentally different patterns; using the wrong one is the #1 source of bugs
- **Structure through the scene graph** — use `Group` for logical groupings and maintain proper hierarchy
- **Vary style by context** — portfolio/showcase use elegant muted palettes; games use bright colors; data viz uses clean lines; backgrounds use subtle slow movement; product viewers use realistic PBR lighting
- **Read repository CLAUDE.md before building** — ensure compliance with local development standards

**Step 0: Detect paradigm**

Scan the user's request, existing project files (package.json, imports), and stated requirements to identify which paradigm applies:

| Signal | Paradigm / Context | Reference to Load |
|--------|-------------------|-------------------|
| `@react-three/fiber`, `r3f`, `drei`, `useFrame`, `<Canvas>`, `<mesh>`, React project with 3D | **React Three Fiber** | `references/react-three-fiber.md` |
| `WebGPURenderer`, `TSL`, `tsl`, `compute shader`, `wgsl`, `node material`, WebGPU mentioned | **WebGPU** | `references/webgpu.md` |
| Standalone HTML, CDN imports, `new THREE.Scene()`, no React, vanilla JS/TS | **Imperative** | `references/advanced-topics.md` (load as needed) |
| Game project: `EventBus`, `GameState`, player controller, enemies, scoring, multiple game systems | **Game architecture** | `references/game-architecture.md` + `references/game-patterns.md` (alongside paradigm reference) |
| GLTF/GLB model loading, `.glb` files, animated characters, skeletal rigs, model import | **GLTF loading** | `references/gltf-loading.md` (alongside paradigm reference) |

If ambiguous (e.g., user says "3D scene" with no project context), ask which paradigm — don't guess, because imperative Three.js patterns actively conflict with R3F patterns (OrbitControls setup, animation loops, component lifecycle).

Game and GLTF references load **alongside** the paradigm reference — they are complementary, not alternative. A game project using R3F loads both `react-three-fiber.md` and the relevant game references.

**After detecting paradigm**: Read the corresponding reference file. The reference contains paradigm-specific patterns, failure modes, and component selection guidance that override the generic steps below.

Additional reference loading signals (visual-polish, shader-patterns, performance-patterns, advanced-animation) are listed in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 1: Additional Reference Loading Signals).

**Step 1: Identify the core visual element**

Determine from the user request:
- What is the primary 3D content? (geometric shapes, loaded model, particles, terrain)
- What interaction is needed? (none, orbit, click, mouse tracking)
- What animation brings it to life? (rotation, oscillation, morphing, physics)
- What is the context? (portfolio, game, data viz, background, product viewer)

**Step 2: Select components**

See the Scene Plan template in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 1: Scene Plan Template).

**Step 3: Document visual style**

Record the visual direction for this scene (e.g., "elegant minimal portfolio style", "vibrant interactive game", "clean data visualization"). Use this to guide material colors, lighting warmth, and animation pacing.

**Gate**: Scene plan documented with geometry, material, lighting, animation, and controls selected. Proceed only when gate passes.

### Phase 2: BUILD

**Goal**: Construct the scene with proper structure and modern patterns.

**Paradigm-specific build instructions**: If you loaded a paradigm reference in Step 0, follow its build patterns instead of the imperative defaults. R3F uses JSX components and `<Canvas>`, not manual renderer setup. WebGPU uses `WebGPURenderer` with different initialization. The reference file is authoritative for its paradigm.

Core constraints for the imperative paradigm (single HTML, resize handling, CONFIG object, modular setup functions, three-point lighting, `renderer.setAnimationLoop()`) are in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 2: Core Constraints).

**Step 1: Create HTML boilerplate**

See the HTML boilerplate in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 2: HTML Boilerplate).

**Step 2: Build scene infrastructure**

See the scene infrastructure code (CONFIG object, scene/camera/renderer setup, resize handler) in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 2: Scene Infrastructure).

**Step 3: Add lighting, geometry, and materials per scene plan**

Build each component from the Phase 1 plan. Create geometry once and reuse where possible (avoid allocating new geometries in animation loops). Use `Group` for hierarchical transforms and logical scene organization.

**Gate**: Scene renders without errors. All planned geometry, materials, and lights are present. Proceed only when gate passes.

### Phase 3: ANIMATE

**Goal**: Add motion, interaction, and life to the scene.

**Paradigm-specific animation**: R3F uses `useFrame` hooks (never `requestAnimationFrame` or `setAnimationLoop`). WebGPU may use compute shaders for GPU-driven animation. See the loaded paradigm reference for patterns.

Core constraints for the imperative paradigm (no geometry/material allocation in the loop, `time` parameter usage, OrbitControls default, transform-only-per-frame) are in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 3: Core Constraints).

**Step 1: Set up animation loop**

See the animation loop pattern in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 3: Animation Loop).

**Step 2: Implement planned animations**

Apply transforms per frame. Time-based animation follows the pattern shown in `references/build-recipes.md`.

**Step 3: Add interaction handlers**

Wire up mouse/touch events, orbit controls, or raycasting per the scene plan.

**Gate**: Animations run smoothly. Interactions respond correctly. No console errors. Proceed only when gate passes.

### Phase 4: POLISH

**Goal**: Ensure quality, performance, and completeness.

Core constraints (remove debug helpers / commented code, handle window resize, ensure visible lighting, match visual style) and the four verification steps (responsive behavior, visual quality, output testing, cleanup) are in `${CLAUDE_SKILL_DIR}/references/build-recipes.md` (Phase 4: Core Constraints + Polish Verification Steps).

**Gate**: All verification steps pass. Output is complete and ready to deliver.

---

## Error Handling

See `${CLAUDE_SKILL_DIR}/references/build-recipes.md` for error cases: black screen / nothing renders, OrbitControls not defined, model loads but is invisible or tiny.

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/build-recipes.md` | Phase 2/3 build, error diagnosis | HTML boilerplate, CONFIG + scene/camera/renderer setup, animation loop, error handling (black screen, OrbitControls, model scale) |
| `references/advanced-topics.md` | Imperative paradigm | GLTF loading, post-processing, shaders, raycasting, physics, InstancedMesh, TypeScript |
| `references/react-three-fiber.md` | R3F paradigm | Declarative patterns, Drei helpers, camera pitfalls, post-processing, Zustand, performance |
| `references/webgpu.md` | WebGPU paradigm | WebGPURenderer, TSL shaders, compute shaders, version-specific changes, device loss |
| `references/visual-polish.md` | Visual quality signal | Material recipes, dramatic lighting, post-processing stacking, HDR environments, shadow quality |
| `references/gltf-loading.md` | GLTF/GLB model loading signal | Coordinate system contract, SkeletonUtils.clone, model caching, auto-centering, bone hierarchy, asset manifest |
| `references/game-patterns.md` | Game project signal | Animation state machine, camera-relative movement, delta capping, mobile input, player controller |
| `references/game-architecture.md` | Game project signal | EventBus, GameState singleton, Constants module, restart-safety, pre-ship checklist |
| `references/shader-patterns.md` | Custom GLSL / visual effects | ShaderMaterial vs RawShaderMaterial, vertex displacement, fragment effects (holographic, dissolve, chromatic aberration), EffectComposer postprocessing pipeline |
| `references/performance-patterns.md` | Performance / many objects | InstancedMesh, BufferGeometry typed arrays, draw call batching, LOD, KTX2 textures, dispose patterns |
| `references/advanced-animation.md` | Animation systems / skeletal rigs | AnimationMixer morph targets, bone manipulation, procedural IK, spring physics, GSAP integration, particle animation |
