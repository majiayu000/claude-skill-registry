---
name: threejs-agents-scene-builder
description: >
  Use when composing a complete Three.js scene from scratch or when
  asked to create a 3D visualization. Provides decision trees for
  choosing lighting setup, materials, camera type, controls, and
  post-processing pipeline. Orchestrates other Three.js skills.
  Keywords: create scene, build 3D, Three.js project, scene setup,
  visualization, product viewer, 3D application, scene composition.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-agents-scene-builder

## Purpose

This skill is an **orchestration guide** for building complete Three.js scenes. It provides decision trees that map use cases to the correct combination of lighting, materials, camera, controls, environment, and post-processing. ALWAYS consult this skill first when asked to create a 3D scene or visualization.

---

## Master Decision Tree: Use Case to Scene Recipe

### Step 1 — Identify the Use Case

| Use Case | Go To |
|----------|-------|
| Product viewer / configurator | Recipe A |
| Architectural walkthrough | Recipe B |
| Game level / interactive 3D | Recipe C |
| Data visualization / chart | Recipe D |
| Portfolio / hero section | Recipe E |
| CAD / BIM / IFC viewer | Recipe F |
| AR / XR experience | Recipe G |

### Step 2 — Choose R3F vs Imperative

| Condition | Decision |
|-----------|----------|
| Project uses React | ALWAYS use React Three Fiber (R3F) |
| Project uses Vue, Svelte, or vanilla JS | ALWAYS use imperative Three.js |
| Need maximum control over render loop | Prefer imperative Three.js |
| Rapid prototyping with component reuse | Prefer R3F + Drei |
| Static scene, no interaction framework | Either works; imperative is lighter |

**Cross-reference:** `threejs-impl-r3f` for R3F patterns, `threejs-core-scene-graph` for imperative patterns.

---

## Decision Tree: Lighting Setup

### Step 1 — Scene Type to Lighting Strategy

| Scene Type | Primary Light | Fill Light | Shadows |
|------------|--------------|------------|---------|
| Outdoor / daylight | DirectionalLight (sun) | HemisphereLight (sky/ground) | DirectionalLight shadow, PCFSoftShadowMap |
| Indoor / room | PointLight or SpotLight (fixtures) | AmbientLight (low) | SpotLight shadows, limit to 2-3 |
| Studio / product | SpotLight (key) + SpotLight (rim) | AmbientLight or HemisphereLight | ContactShadows (Drei) or AccumulativeShadows |
| Stylized / toon | DirectionalLight | HemisphereLight | Optional; BasicShadowMap for hard edges |
| HDR environment only | None (IBL provides all lighting) | None | ContactShadows or AccumulativeShadows |
| Night / dark | SpotLight (focused pools) | AmbientLight (very low, ~0.05) | SpotLight shadows |

### Step 2 — Lighting Intensity (Physically Correct, r160+)

| Light Type | Unit | Typical Indoor | Typical Outdoor |
|------------|------|---------------|-----------------|
| DirectionalLight | lux | 1-5 | 1-3 (scene scale dependent) |
| PointLight | candela | 50-200 | N/A |
| SpotLight | candela | 100-500 | N/A |
| AmbientLight | unitless | 0.1-0.5 | 0.2-0.5 |
| HemisphereLight | unitless | 0.3-0.8 | 0.5-1.0 |

### Step 3 — Light Count Budget

| Platform | Max Real-Time Lights | Max Shadow-Casting Lights |
|----------|---------------------|--------------------------|
| Mobile | 3-4 | 1 (DirectionalLight only) |
| Desktop | 8-16 | 2-3 (NEVER PointLight shadows on mobile) |
| High-end | 16+ (use TiledLighting) | 4-5 |

**Critical rules:**
- NEVER use PointLight shadows on mobile — each costs 6 shadow map renders
- ALWAYS add `directionalLight.target` to the scene when repositioning the target
- ALWAYS call `RectAreaLightUniformsLib.init()` before creating RectAreaLight

**Cross-reference:** `threejs-impl-lighting-shadows` for shadow tuning and artifact fixes.

---

## Decision Tree: Material Selection

| Visual Goal | Material | Notes |
|-------------|----------|-------|
| Realistic / PBR | MeshStandardMaterial | Default choice for most scenes |
| Realistic + clearcoat, transmission, sheen | MeshPhysicalMaterial | Heavier than Standard; use only when needed |
| Toon / cel-shaded | MeshToonMaterial | Requires `gradientMap` texture for steps |
| Unlit / flat color | MeshBasicMaterial | Zero lighting cost; good for wireframes, UI |
| Performance-critical (many objects) | MeshLambertMaterial | Vertex-lit; cheaper than Standard |
| Glass / transparent | MeshPhysicalMaterial (`transmission: 1`) | Or Drei's MeshTransmissionMaterial in R3F |
| Reflective floor | Drei MeshReflectorMaterial | R3F only |
| Custom shader | ShaderMaterial or RawShaderMaterial | Full GLSL control |
| Node-based (WebGPU) | MeshStandardNodeMaterial | TSL node system; r160+ |

**Critical rules:**
- NEVER use MeshPhysicalMaterial when MeshStandardMaterial suffices — it is significantly more expensive
- ALWAYS set `material.needsUpdate = true` after changing `defines` or `extensions`
- ALWAYS dispose materials when removing objects from the scene

**Cross-reference:** `threejs-syntax-materials` for material properties and textures.

---

## Decision Tree: Camera Selection

| Use Case | Camera Type | Typical Settings |
|----------|-------------|-----------------|
| Most 3D scenes | PerspectiveCamera | `fov: 50-75`, `near: 0.1`, `far: 1000` |
| Product viewer (no perspective distortion) | PerspectiveCamera | `fov: 35-45` (narrow = less distortion) |
| Architectural (wide angle) | PerspectiveCamera | `fov: 60-90` |
| 2D game / isometric | OrthographicCamera | Frustum sized to world units |
| CAD / technical drawing | OrthographicCamera | ALWAYS |
| Data visualization (flat) | OrthographicCamera | Frustum = data range |
| Cinematic / dramatic | PerspectiveCamera | `fov: 20-35` (telephoto effect) |

**Critical rules:**
- ALWAYS call `camera.updateProjectionMatrix()` after changing `fov`, `near`, `far`, or `aspect`
- NEVER set `near` to `0` — this causes z-fighting across the entire scene
- ALWAYS keep the `near/far` ratio as small as possible (ideally < 1:10000)

**Cross-reference:** `threejs-core-renderer-camera` for camera API details.

---

## Decision Tree: Controls Selection

| Interaction Pattern | Controls | Notes |
|--------------------|----------|-------|
| Orbit around object (most common) | OrbitControls | ALWAYS enable damping |
| Map / top-down navigation | MapControls | Left-drag = pan, right-drag = rotate |
| First-person / walkthrough | PointerLockControls | Requires pointer lock API |
| Fly-through (6DOF) | FlyControls | Keyboard + mouse |
| Drag-to-rotate (presentation) | Drei PresentationControls | R3F only; spring physics |
| Scroll-driven animation | Drei ScrollControls | R3F only |
| Object manipulation (translate/rotate/scale) | TransformControls | Attach to selected object |
| Mobile-friendly orbit | OrbitControls | Touch gestures built-in |

**Critical rules:**
- ALWAYS call `controls.update()` in the animation loop when `enableDamping` is true
- ALWAYS call `controls.dispose()` on cleanup
- NEVER combine OrbitControls and TransformControls without disabling OrbitControls during transform interaction

**Cross-reference:** `threejs-syntax-controls` for controls API details.

---

## Decision Tree: Environment Setup

| Visual Goal | Approach | Implementation |
|-------------|----------|---------------|
| Realistic reflections + ambient | HDR environment map | `scene.environment = pmremGenerator.fromEquirectangular(hdrTexture)` |
| Solid color background | `scene.background = new Color(...)` | Simplest option |
| Gradient background | Custom shader on background plane | Or CSS gradient behind transparent canvas |
| Skybox | CubeTexture on `scene.background` | 6 face images |
| Procedural sky | Drei `<Sky>` or Three.js `Sky` addon | Dynamic sun position |
| No background (transparent) | `renderer = new WebGLRenderer({ alpha: true })` | CSS controls what shows behind |
| R3F environment | Drei `<Environment preset="studio" />` | Presets: apartment, city, dawn, forest, lobby, night, park, studio, sunset, warehouse |

**Critical rules:**
- ALWAYS use `PMREMGenerator` to prefilter environment maps for PBR materials
- NEVER use unprocessed HDR textures as `scene.environment` — they MUST be PMREM-processed
- Setting `scene.environment` provides IBL to ALL PBR materials automatically

**Cross-reference:** `threejs-syntax-materials` for environment map usage on materials.

---

## Decision Tree: Post-Processing

### When to Add Post-Processing

| Condition | Decision |
|-----------|----------|
| Scene looks flat or lacks depth | Add SSAO/GTAO + subtle bloom |
| Need glow / emissive highlights | Add UnrealBloomPass |
| Need anti-aliasing (no MSAA) | Add FXAA or SMAA |
| Cinematic look | Add BokehPass (DoF) + FilmPass (grain) + LUTPass (color grading) |
| Outline selection | Add OutlinePass |
| Performance is critical (mobile) | NEVER add post-processing; use baked effects |

### Post-Processing Pipeline Order

ALWAYS follow this pass order:

1. `RenderPass` (beauty render) — ALWAYS first
2. Geometry passes: SSAO, GTAO, SSR
3. Effect passes: Bloom, DoF, Outline
4. Anti-aliasing: FXAA or SMAA
5. Color grading: LUT, Film
6. `OutputPass` (tone mapping + color space) — ALWAYS last

### R3F Post-Processing

In R3F, use `@react-three/postprocessing` (wraps pmndrs/postprocessing library):

```jsx
import { EffectComposer, Bloom, SSAO } from '@react-three/postprocessing'

<EffectComposer>
  <SSAO />
  <Bloom luminanceThreshold={0.9} intensity={0.5} />
</EffectComposer>
```

**Critical rules:**
- ALWAYS resize the composer when the window resizes: `composer.setSize(w, h)`
- NEVER forget `OutputPass` at the end — without it, tone mapping and color space conversion are skipped
- In R3F, `@react-three/postprocessing` handles pass ordering automatically

**Cross-reference:** `threejs-impl-postprocessing` for pass configuration and tuning.

---

## Scene Composition Checklist

ALWAYS follow this checklist when building a scene:

1. **Renderer** — Create WebGLRenderer with `antialias: true`, set pixel ratio, set size
2. **Scene** — Create Scene, set background and/or environment
3. **Camera** — Choose type per decision tree, set position
4. **Lighting** — Choose recipe per decision tree, respect budget
5. **Ground/Environment** — Add ground plane, environment map, or sky
6. **Content** — Add geometries, load models, create materials
7. **Controls** — Choose per decision tree, configure constraints
8. **Shadows** — Enable on renderer + lights + objects (3-step opt-in)
9. **Post-processing** — Add if needed, follow pipeline order
10. **Resize handling** — ALWAYS handle window resize (camera + renderer + composer)
11. **Animation loop** — `requestAnimationFrame` or R3F `useFrame`
12. **Disposal** — ALWAYS dispose geometries, materials, textures on cleanup

---

## Performance Quick Reference

| Optimization | When to Apply |
|-------------|--------------|
| `InstancedMesh` | >50 identical objects |
| `LOD` (Level of Detail) | Large scenes with distant objects |
| `frustumCulled: true` (default) | ALWAYS keep enabled unless object must render off-screen |
| `matrixAutoUpdate: false` | Static objects that NEVER move |
| Texture compression (KTX2/Basis) | ALWAYS for production; reduces GPU memory 4-6x |
| Geometry merging | Many small static meshes with same material |
| `frameloop="demand"` (R3F) | Static scenes / configurators |
| Baked lighting | Static environments |
| Object pooling | Frequently created/destroyed objects |

**Cross-reference:** `threejs-errors-performance` for detailed optimization strategies.

---

## Reference Links

- [references/methods.md](references/methods.md) — Decision trees with detailed selection criteria
- [references/examples.md](references/examples.md) — Complete scene recipes for each use case
- [references/anti-patterns.md](references/anti-patterns.md) — Common scene composition mistakes

### Related Skills

| Skill | When to Consult |
|-------|----------------|
| `threejs-core-scene-graph` | Scene hierarchy, Object3D API, disposal |
| `threejs-core-renderer-camera` | Renderer setup, camera configuration |
| `threejs-core-math-transforms` | Vectors, matrices, coordinate transforms |
| `threejs-syntax-geometry` | BufferGeometry, built-in shapes, InstancedMesh |
| `threejs-syntax-materials` | Material properties, textures, environment maps |
| `threejs-syntax-loaders` | GLTF, FBX, OBJ loading and optimization |
| `threejs-syntax-controls` | Camera controls setup and configuration |
| `threejs-impl-lighting-shadows` | Light types, shadow configuration, artifacts |
| `threejs-impl-animation` | Keyframe animation, morph targets, skeletal |
| `threejs-impl-postprocessing` | EffectComposer, bloom, SSAO, anti-aliasing |
| `threejs-impl-physics` | Rapier/Cannon.js integration |
| `threejs-impl-r3f` | React Three Fiber patterns and hooks |
| `threejs-impl-webgpu` | WebGPU renderer, TSL node materials |
| `threejs-impl-ifc` | IFC/BIM model loading and processing |
| `threejs-errors-performance` | FPS optimization, memory leaks, draw calls |
| `threejs-errors-rendering` | Visual artifacts, z-fighting, color issues |
| `threejs-agents-model-optimizer` | GLTF optimization, compression, LOD generation |

### Official Sources

- https://threejs.org/docs/
- https://threejs.org/examples/
- https://r3f.docs.pmnd.rs/
- https://drei.docs.pmnd.rs/
