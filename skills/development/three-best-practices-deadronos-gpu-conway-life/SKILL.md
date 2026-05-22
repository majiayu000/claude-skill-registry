---
name: three-best-practices
description: Three.js performance optimization and best practices guidelines. Use when writing, reviewing, or optimizing Three.js code. Triggers on tasks involving 3D scenes, WebGL/WebGPU rendering, geometries, materials, textures, lighting, shaders, or TSL.
license: MIT
metadata:
  author: three-agent-skills
  version: "2.0.0"
  three-version: "0.182.0+"
---

# Three.js Best Practices

Comprehensive performance optimization guide for Three.js applications. Contains 100+ rules across 17 categories, prioritized by impact.

> Based on official guidelines from Three.js `llms` branch maintained by mrdoob.

## When to Apply

Reference these guidelines when:
- Setting up a new Three.js project
- Writing or reviewing Three.js code
- Optimizing performance or fixing memory leaks
- Working with custom shaders (GLSL or TSL)
- Implementing WebGPU features
- Building VR/AR experiences with WebXR
- Integrating physics engines
- Optimizing for mobile devices

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 0 | Modern Setup & Imports | FUNDAMENTAL | `setup-` |
| 1 | Memory Management & Dispose | CRITICAL | `memory-` |
| 2 | Render Loop Optimization | CRITICAL | `render-` |
| 3 | Geometry & Buffer Management | HIGH | `geometry-` |
| 4 | Material & Texture Optimization | HIGH | `material-` |
| 5 | Lighting & Shadows | MEDIUM-HIGH | `lighting-` |
| 6 | Scene Graph Organization | MEDIUM | `scene-` |
| 7 | Shader Best Practices (GLSL) | MEDIUM | `shader-` |
| 8 | TSL (Three.js Shading Language) | MEDIUM | `tsl-` |
| 9 | Loading & Assets | MEDIUM | `loading-` |
| 10 | Camera & Controls | LOW-MEDIUM | `camera-` |
| 11 | Animation System | MEDIUM | `animation-` |
| 12 | Physics Integration | MEDIUM | `physics-` |
| 13 | WebXR / VR / AR | MEDIUM | `webxr-` |
| 14 | Audio | LOW-MEDIUM | `audio-` |
| 15 | Mobile Optimization | HIGH | `mobile-` |
| 16 | Production | HIGH | `error-`, `migration-` |
| 17 | Debug & DevTools | LOW | `debug-` |

## Quick Reference

### 0. Modern Setup (FUNDAMENTAL)

- `setup-use-import-maps` - Use Import Maps, not old CDN scripts
- `setup-choose-renderer` - WebGLRenderer (default) vs WebGPURenderer (TSL/compute)
- `setup-animation-loop` - Use `renderer.setAnimationLoop()` not manual RAF
- `setup-basic-scene-template` - Complete modern scene template

### 1. Memory Management (CRITICAL)

- `memory-dispose-geometry` - Always dispose geometries
- `memory-dispose-material` - Always dispose materials and textures
- `memory-dispose-textures` - Dispose dynamically created textures
- `memory-dispose-render-targets` - Always dispose WebGLRenderTarget
- `memory-dispose-recursive` - Use recursive disposal for hierarchies
- `memory-dispose-on-unmount` - Dispose in React cleanup/unmount
- `memory-renderer-dispose` - Dispose renderer when destroying view
- `memory-reuse-objects` - Reuse geometries and materials

### 2. Render Loop (CRITICAL)

- `render-single-raf` - Single requestAnimationFrame loop
- `render-conditional` - Render on demand for static scenes
- `render-delta-time` - Use delta time for animations
- `render-avoid-allocations` - Never allocate in render loop
- `render-cache-computations` - Cache expensive computations
- `render-frustum-culling` - Enable frustum culling
- `render-update-matrix-manual` - Disable auto matrix updates for static objects
- `render-pixel-ratio` - Limit pixel ratio to 2
- `render-antialias-wisely` - Use antialiasing judiciously

### 3. Geometry (HIGH)

- `geometry-buffer-geometry` - Always use BufferGeometry
- `geometry-merge-static` - Merge static geometries
- `geometry-instanced-mesh` - Use InstancedMesh for identical objects
- `geometry-lod` - Use Level of Detail for complex models
- `geometry-index-buffer` - Use indexed geometry
- `geometry-vertex-count` - Minimize vertex count
- `geometry-attributes-typed` - Use appropriate typed arrays
- `geometry-interleaved` - Consider interleaved buffers

### 4. Materials & Textures (HIGH)

- `material-reuse` - Reuse materials across meshes
- `material-simplest-sufficient` - Use simplest material that works
- `material-texture-size-power-of-two` - Power-of-two texture dimensions
- `material-texture-compression` - Use compressed textures (KTX2/Basis)
- `material-texture-mipmaps` - Enable mipmaps appropriately
- `material-texture-anisotropy` - Use anisotropic filtering for floors
- `material-texture-atlas` - Use texture atlases
- `material-avoid-transparency` - Minimize transparent materials
- `material-onbeforecompile` - Use onBeforeCompile for shader mods (or TSL)

### 5. Lighting & Shadows (MEDIUM-HIGH)

- `lighting-limit-lights` - Minimize dynamic lights
- `lighting-bake-static` - Bake lighting for static scenes
- `lighting-shadow-camera-tight` - Fit shadow camera tightly
- `lighting-shadow-map-size` - Choose appropriate shadow resolution
- `lighting-shadow-selective` - Enable shadows selectively
- `lighting-shadow-cascade` - Use CSM for large scenes
- `lighting-probe` - Use Light Probes

### 6. Scene Graph (MEDIUM)

- `scene-group-objects` - Use Groups for organization
- `scene-layers` - Use Layers for selective rendering
- `scene-visible-toggle` - Use visible flag, not add/remove
- `scene-flatten-static` - Flatten static hierarchies
- `scene-name-objects` - Name objects for debugging
- `scene-object-pooling` - Use object pooling

### 7. Shaders GLSL (MEDIUM)

- `shader-precision` - Use appropriate precision
- `shader-avoid-branching` - Minimize branching
- `shader-precompute-cpu` - Precompute on CPU
- `shader-avoid-discard` - Avoid discard, use alphaTest
- `shader-texture-lod` - Use textureLod for known mip levels
- `shader-uniform-arrays` - Prefer uniform arrays
- `shader-varying-interpolation` - Use flat when appropriate
- `shader-chunk-injection` - Use Three.js shader chunks

### 8. TSL - Three.js Shading Language (MEDIUM)

- `tsl-why-use` - Use TSL instead of onBeforeCompile
- `tsl-setup-webgpu` - WebGPU setup for TSL
- `tsl-complete-reference` - Full TSL type system and functions
- `tsl-material-slots` - Material node properties reference
- `tsl-node-materials` - Use NodeMaterial classes
- `tsl-basic-operations` - Types, operations, swizzling
- `tsl-functions` - Creating TSL functions with Fn()
- `tsl-conditionals` - If, select, loops in TSL
- `tsl-textures` - Textures and triplanar mapping
- `tsl-post-processing` - bloom, blur, dof, ao
- `tsl-compute-shaders` - GPGPU and compute operations
- `tsl-glsl-to-tsl` - GLSL to TSL translation

### 9. Loading & Assets (MEDIUM)

- `loading-draco-compression` - Use Draco for large meshes
- `loading-gltf-preferred` - Use glTF format
- `gltf-loading-optimization` - Full loader setup with DRACO/Meshopt/KTX2
- `loading-progress-feedback` - Show loading progress
- `loading-async-await` - Use async/await for loading
- `loading-lazy` - Lazy load non-critical assets
- `loading-cache-assets` - Enable caching
- `loading-dispose-unused` - Unload unused assets

### 10. Camera & Controls (LOW-MEDIUM)

- `camera-near-far` - Set tight near/far planes
- `camera-fov` - Choose appropriate FOV
- `camera-controls-damping` - Use damping for smooth controls
- `camera-resize-handler` - Handle resize properly
- `camera-orbit-limits` - Set orbit control limits

### 11. Animation (MEDIUM)

- `animation-system` - AnimationMixer, blending, morph targets, skeletal

### 12. Physics (MEDIUM)

- `physics-integration` - Rapier, Cannon-es integration patterns

### 13. WebXR (MEDIUM)

- `webxr-setup` - VR/AR buttons, controllers, hit testing

### 14. Audio (LOW-MEDIUM)

- `audio-spatial` - PositionalAudio, HRTF, spatial sound

### 15. Optimization (HIGH)

- `mobile-optimization` - Mobile-specific optimizations and checklist
- `raycasting-optimization` - BVH, layers, GPU picking

### 16. Production (HIGH)

- `error-handling-recovery` - WebGL context loss and recovery
- `migration-checklist` - Breaking changes by version

### 17. Debug (LOW)

- `debug-stats` - Use Stats.js
- `debug-helpers` - Use built-in helpers
- `debug-gui` - Use lil-gui for tweaking
- `debug-renderer-info` - Check renderer.info
- `debug-conditional` - Remove debug code in production

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/setup-use-import-maps.md
rules/memory-dispose-geometry.md
rules/tsl-complete-reference.md
rules/mobile-optimization.md
```

Each rule file contains:
- Brief explanation of why it matters
- BAD code example with explanation
- GOOD code example with explanation
- Additional context and references

## Key Patterns

### Modern Import Maps

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.182.0/examples/jsm/",
    "three/tsl": "https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.tsl.js"
  }
}
</script>
```

### Proper Disposal

```javascript
function disposeObject(obj) {
  if (obj.geometry) obj.geometry.dispose();
  if (obj.material) {
    if (Array.isArray(obj.material)) {
      obj.material.forEach(m => m.dispose());
    } else {
      obj.material.dispose();
    }
  }
}
```

### TSL Basic Usage

```javascript
import { texture, uv, color, time, sin } from 'three/tsl';

const material = new THREE.MeshStandardNodeMaterial();
material.colorNode = texture(map).mul(color(0xff0000));
material.colorNode = color(0x00ff00).mul(sin(time).mul(0.5).add(0.5));
```

### Mobile Detection

```javascript
const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
```
