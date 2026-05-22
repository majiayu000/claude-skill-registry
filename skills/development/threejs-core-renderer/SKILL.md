---
name: threejs-core-renderer
description: >
  Use when initializing a Three.js renderer, setting up the render loop,
  handling window resize, configuring tone mapping, or managing color
  spaces. Prevents the common mistake of not capping pixel ratio, using
  wrong color space, or forgetting to enable shadow maps. Covers
  WebGLRenderer, render targets, tone mapping, color management.
  Keywords: WebGLRenderer, render loop, setSize, setPixelRatio,
  toneMapping, outputColorSpace, shadowMap, WebGLRenderTarget, dispose,
  setAnimationLoop, compileAsync.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-core-renderer

## Quick Reference

### Standard Initialization Pattern

```javascript
import {
  WebGLRenderer, SRGBColorSpace, ACESFilmicToneMapping,
  PCFSoftShadowMap, PerspectiveCamera, Scene
} from 'three';

const renderer = new WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = SRGBColorSpace;
renderer.toneMapping = ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const scene = new Scene();
const camera = new PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);

renderer.setAnimationLoop((time) => {
  renderer.render(scene, camera);
});
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `canvas` | `HTMLCanvasElement` | new canvas | Existing canvas element |
| `context` | `WebGLRenderingContext` | new context | Existing WebGL context |
| `precision` | `'highp' \| 'mediump' \| 'lowp'` | `'highp'` | Shader precision |
| `alpha` | `boolean` | `false` | Transparent canvas background |
| `premultipliedAlpha` | `boolean` | `true` | Premultiplied alpha blending |
| `antialias` | `boolean` | `false` | MSAA anti-aliasing |
| `stencil` | `boolean` | `true` | Stencil buffer |
| `preserveDrawingBuffer` | `boolean` | `false` | Required for screenshots |
| `powerPreference` | `'high-performance' \| 'low-power' \| 'default'` | `'default'` | GPU selection hint |
| `failIfMajorPerformanceCaveat` | `boolean` | `false` | Fail if software renderer |
| `depth` | `boolean` | `true` | Depth buffer |
| `logarithmicDepthBuffer` | `boolean` | `false` | Fix Z-fighting for large scenes |

**NEVER** change `antialias` after construction -- it CANNOT be modified post-creation.

### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `domElement` | `HTMLCanvasElement` | -- | The canvas. ALWAYS append to DOM |
| `shadowMap.enabled` | `boolean` | `false` | MUST set `true` for any shadows |
| `shadowMap.type` | `ShadowMapType` | `PCFShadowMap` | Shadow filtering algorithm |
| `toneMapping` | `ToneMapping` | `NoToneMapping` | HDR tone mapping algorithm |
| `toneMappingExposure` | `number` | `1` | Exposure for tone mapping |
| `outputColorSpace` | `string` | `SRGBColorSpace` | Output color space |
| `autoClear` | `boolean` | `true` | Clear before each render call |
| `sortObjects` | `boolean` | `true` | Automatic draw order sorting |
| `clippingPlanes` | `Plane[]` | `[]` | Global clipping planes |
| `localClippingEnabled` | `boolean` | `false` | Enable per-material clipping |
| `info` | `object` | -- | Render stats (calls, triangles, memory) |

### Critical Warnings

**NEVER** forget to cap pixel ratio -- uncapped `devicePixelRatio` on 3x+ screens causes 9x+ pixel load. ALWAYS use `Math.min(window.devicePixelRatio, 2)`.

**NEVER** change `shadowMap.type` after the first render -- it forces full shader recompilation. ALWAYS set it once at initialization.

**NEVER** use `preserveDrawingBuffer: true` in production render loops -- it disables buffer-swap optimizations. ONLY enable it when screenshots are needed.

**NEVER** set `near: 0` on cameras -- it causes Z-fighting everywhere. ALWAYS keep `far / near` ratio under 10,000.

**NEVER** forget `camera.updateProjectionMatrix()` after modifying `fov`, `aspect`, `near`, `far`, or `zoom` -- the projection matrix is NOT auto-updated.

**NEVER** use raw `requestAnimationFrame` in Three.js r160+ -- ALWAYS use `renderer.setAnimationLoop()` which handles WebXR sessions automatically.

**NEVER** skip `renderer.dispose()` on cleanup -- it leaks WebGL contexts, programs, textures, and framebuffers.

---

## Color Management

Three.js r160+ uses a linear workflow with automatic sRGB conversion on output.

### Color Space Rules

| Texture Type | colorSpace | Examples |
|-------------|-----------|----------|
| Color / albedo | `SRGBColorSpace` | Diffuse maps, emissive maps |
| Data | `LinearSRGBColorSpace` | Normal maps, roughness, metalness, AO, displacement |

**Rule:** Color textures are ALWAYS `SRGBColorSpace`. Data textures are ALWAYS `LinearSRGBColorSpace`. Mixing these up produces washed-out or over-saturated renders.

### Tone Mapping Decision Tree

| Constant | When to Use |
|----------|------------|
| `NoToneMapping` | Non-photorealistic rendering, UI overlays, unlit scenes |
| `LinearToneMapping` | Basic HDR clamping with minimal color transformation |
| `ReinhardToneMapping` | General-purpose, preserves color hues well |
| `CineonToneMapping` | Cinematic film stock look |
| `ACESFilmicToneMapping` | **Default choice for PBR.** Industry-standard filmic curve |
| `AgXToneMapping` | Better than ACES for saturated colors. Avoids ACES hue shift on bright blues/reds. (r160+) |
| `NeutralToneMapping` | When color accuracy is paramount, minimal artistic transformation |

**ALWAYS** use `ACESFilmicToneMapping` or `AgXToneMapping` for PBR workflows. `AgXToneMapping` is preferred when saturated colors must remain accurate.

---

## Shadow Map Configuration

```javascript
import { PCFSoftShadowMap } from 'three';

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = PCFSoftShadowMap;
```

| Type | Quality | Performance | Notes |
|------|---------|-------------|-------|
| `BasicShadowMap` | Low (hard edges) | Fastest | No filtering |
| `PCFShadowMap` | Medium | Medium | Default. Percentage-Closer Filtering |
| `PCFSoftShadowMap` | High (soft edges) | Slower | Bilinear PCF. Most popular choice |
| `VSMShadowMap` | High (very soft) | Slowest | Can exhibit light bleeding artifacts |

---

## Render Loop and Resize

### setAnimationLoop (preferred)

```javascript
renderer.setAnimationLoop((time) => {
  // time is DOMHighResTimeStamp in milliseconds
  renderer.render(scene, camera);
});

// Stop the loop
renderer.setAnimationLoop(null);
```

### Window Resize Handler

```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

ALWAYS update `camera.aspect` AND call `updateProjectionMatrix()` before `setSize()`.

---

## Camera System

### PerspectiveCamera

```javascript
import { PerspectiveCamera } from 'three';

const camera = new PerspectiveCamera(
  50,                                        // fov (vertical, degrees)
  window.innerWidth / window.innerHeight,    // aspect ratio
  0.1,                                       // near
  1000                                       // far
);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);
```

After modifying `fov`, `aspect`, `near`, `far`, or `zoom`, you MUST call `camera.updateProjectionMatrix()`.

### OrthographicCamera

```javascript
import { OrthographicCamera } from 'three';

const frustumSize = 10;
const aspect = window.innerWidth / window.innerHeight;
const camera = new OrthographicCamera(
  -frustumSize * aspect / 2,   // left
   frustumSize * aspect / 2,   // right
   frustumSize / 2,            // top
  -frustumSize / 2,            // bottom
  0.1, 1000
);
```

ALWAYS update all six frustum parameters (`left`, `right`, `top`, `bottom`, `near`, `far`) on resize, then call `updateProjectionMatrix()`.

### ArrayCamera

Renders multiple viewports in a single `render()` call. Each sub-camera has `camera.viewport = new Vector4(x, y, width, height)`. Used for split-screen and VR stereo.

### CubeCamera

Renders the scene from all 6 directions into a `WebGLCubeRenderTarget`. Used for dynamic environment maps. NEVER call `cubeCamera.update()` every frame for static environments -- it renders the scene 6 times per call.

---

## Render Targets

```javascript
import { WebGLRenderTarget } from 'three';

const renderTarget = new WebGLRenderTarget(1024, 1024);
renderer.setRenderTarget(renderTarget);
renderer.render(scene, camera);
renderer.setRenderTarget(null); // restore default framebuffer
// renderTarget.texture is now usable as a regular Texture
```

ALWAYS call `renderTarget.dispose()` when no longer needed.

---

## Shader Compilation

```javascript
// Synchronous -- blocks the thread
renderer.compile(scene, camera);

// Asynchronous -- non-blocking, prevents frame drops (r160+)
await renderer.compileAsync(scene, camera);
```

ALWAYS call `compileAsync()` after loading assets but before the first visible render to prevent jank from just-in-time shader compilation.

---

## Viewport and Scissor

```javascript
// Render to a sub-region of the canvas
renderer.setViewport(x, y, width, height);
renderer.setScissor(x, y, width, height);
renderer.setScissorTest(true);
renderer.render(scene, camera);

// Reset to full canvas
renderer.setScissorTest(false);
renderer.setViewport(0, 0, canvas.width, canvas.height);
```

---

## Clipping Planes

```javascript
import { Plane, Vector3 } from 'three';

// Global clipping (affects all objects)
renderer.clippingPlanes = [new Plane(new Vector3(0, -1, 0), 1)];

// Per-material clipping (MUST enable localClippingEnabled)
renderer.localClippingEnabled = true;
material.clippingPlanes = [plane];
material.clipIntersection = false; // false = union, true = intersection
material.clipShadows = true;       // also clip shadow geometry
```

---

## Cleanup and Disposal

```javascript
renderer.setAnimationLoop(null);
renderer.dispose();
renderer.domElement.remove();
```

ALWAYS call `dispose()` when removing a renderer. This releases the WebGL context, all compiled shader programs, textures, and framebuffers.

---

## WebGPU Renderer

Three.js includes an experimental `WebGPURenderer` with TSL (Three Shading Language) node-based materials. For WebGPU-specific guidance, see the `threejs-impl-webgpu` skill.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete WebGLRenderer and Camera API signatures
- [references/examples.md](references/examples.md) -- Working code examples
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do

### Official Sources

- https://threejs.org/docs/#api/en/renderers/WebGLRenderer
- https://threejs.org/docs/#api/en/cameras/PerspectiveCamera
- https://threejs.org/docs/#api/en/cameras/OrthographicCamera
- https://threejs.org/docs/#api/en/renderers/WebGLRenderTarget
