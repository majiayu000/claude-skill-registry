---
name: threejs-impl-post-processing
description: >
  Use when adding post-processing effects like bloom, SSAO, depth of
  field, or anti-aliasing to a Three.js scene. Prevents the common
  mistake of mixing Three.js EffectComposer with pmndrs/postprocessing,
  wrong pass order, or missing RenderPass. Covers EffectComposer,
  27+ passes, pmndrs/postprocessing, custom ShaderPass.
  Keywords: post-processing, EffectComposer, bloom, UnrealBloomPass,
  SSAO, outline, SMAA, FXAA, postprocessing, effects, render pass.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-post-processing

## Quick Reference

### Architecture Overview

Three.js offers TWO incompatible post-processing systems. NEVER mix them.

| System | Package | Approach | Best For |
|--------|---------|----------|----------|
| Built-in EffectComposer | `three/addons/postprocessing/` | One shader pass per effect | Simple setups, custom ShaderPass |
| pmndrs/postprocessing | `postprocessing` (npm) | Merges effects into single pass | Performance-critical, R3F apps |
| WebGPU PostProcessing | `three/addons/tsl/display/` | Node-based TSL graphs | WebGPU renderer only |

### Standard Pipeline (Built-in EffectComposer)

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const composer = new EffectComposer( renderer );
composer.addPass( new RenderPass( scene, camera ) ); // ALWAYS first
// ... effect passes here ...
composer.addPass( new OutputPass() );                 // ALWAYS last

function animate() {
  composer.render(); // replaces renderer.render( scene, camera )
}
```

### Pass Ordering Rules

1. `RenderPass` MUST be the FIRST pass -- it renders the scene to the internal buffer
2. Effect passes go in the MIDDLE in any order (bloom, SSAO, outline, etc.)
3. Anti-aliasing passes (SMAA, FXAA) go AFTER effect passes
4. `OutputPass` MUST be the LAST pass -- it applies tone mapping and color space conversion
5. NEVER omit `OutputPass` -- without it, colors appear washed out or incorrect

### Critical Warnings

**NEVER** mix `three/addons/postprocessing/EffectComposer` with `pmndrs/postprocessing` `EffectComposer`. They use incompatible buffer formats and will produce rendering artifacts or crashes.

**NEVER** forget to call `composer.setSize()` on window resize. Failing to resize the composer causes blurry or misaligned effects.

**NEVER** call `renderer.render( scene, camera )` when using EffectComposer. ALWAYS call `composer.render()` instead -- calling both renders the scene twice.

**NEVER** use WebGL post-processing passes with the WebGPU renderer. WebGPU uses an entirely separate node-based `PostProcessing` class.

**ALWAYS** include `RenderPass` as the first pass. Without it, subsequent passes receive an empty buffer.

---

## EffectComposer API

### Constructor

```js
new EffectComposer( renderer: WebGLRenderer, renderTarget?: WebGLRenderTarget )
```

- `renderer` -- the WebGLRenderer instance
- `renderTarget` -- optional custom render target; auto-created if omitted

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `.passes` | `Pass[]` | Ordered array of post-processing passes |
| `.readBuffer` | `WebGLRenderTarget` | Internal read buffer |
| `.writeBuffer` | `WebGLRenderTarget` | Internal write buffer |
| `.renderToScreen` | `boolean` | Whether the final pass renders to screen (default `true`) |
| `.renderer` | `WebGLRenderer` | The renderer instance |

### Methods

| Method | Description |
|--------|-------------|
| `.addPass( pass )` | Appends a pass to the end of the chain |
| `.insertPass( pass, index )` | Inserts a pass at a specific position |
| `.removePass( pass )` | Removes a pass from the chain |
| `.render( deltaTime? )` | Executes all enabled passes in order |
| `.setSize( width, height )` | Resizes all internal buffers and passes |
| `.setPixelRatio( ratio )` | Configures device pixel ratio |
| `.swapBuffers()` | Exchanges read/write buffers |
| `.reset( renderTarget? )` | Restores internal state |
| `.dispose()` | Frees all GPU resources |

---

## Available Pass Types

### Core Passes (ALWAYS needed)

| Pass | Import | Purpose |
|------|--------|---------|
| `RenderPass` | `postprocessing/RenderPass.js` | Renders scene to buffer; ALWAYS first |
| `OutputPass` | `postprocessing/OutputPass.js` | Tone mapping + color space; ALWAYS last |

### Effect Passes

| Pass | Constructor | Purpose |
|------|-------------|---------|
| `UnrealBloomPass` | `( resolution, strength?, radius?, threshold? )` | HDR bloom glow |
| `SSAOPass` | `( scene, camera, width?, height? )` | Screen-space ambient occlusion |
| `GTAOPass` | `( scene, camera, width?, height? )` | Ground truth AO (higher quality) |
| `SAOPass` | `( scene, camera )` | Scalable ambient obscurance |
| `OutlinePass` | `( resolution, scene, camera, selectedObjects? )` | Object selection outlines |
| `BokehPass` | `( scene, camera, params )` | Depth of field |
| `SSRPass` | `( params )` | Screen-space reflections |
| `FilmPass` | `( intensity?, grayscale? )` | Film grain / scanlines |
| `GlitchPass` | `( dtSize? )` | Digital glitch effect |
| `HalftonePass` | `( width, height, params )` | Halftone dot pattern |
| `DotScreenPass` | `( center?, angle?, scale? )` | Dot screen overlay |
| `AfterimagePass` | `( damp? )` | Motion trails / ghosting |
| `LUTPass` | `( params )` | Color LUT grading |
| `RenderPixelatedPass` | `( pixelSize, scene, camera )` | Pixelation effect |

### Anti-Aliasing Passes

| Pass | Constructor | Quality | Cost |
|------|-------------|---------|------|
| `FXAAPass` | `()` | Low -- fast approximation | Cheapest |
| `SMAAPass` | `( width, height )` | Medium -- subpixel morphological | Moderate |
| `SSAARenderPass` | `( scene, camera )` | High -- super-sampling | Expensive |
| `TAARenderPass` | `( scene, camera )` | High -- temporal accumulation | Expensive |

### Utility Passes

| Pass | Purpose |
|------|---------|
| `ShaderPass` | Custom GLSL shader effect |
| `MaskPass` | Stencil masking |
| `ClearMaskPass` | Clears stencil mask |
| `ClearPass` | Clears buffer |
| `TexturePass` | Renders a texture |
| `CubeTexturePass` | Renders cubemap background |
| `SavePass` | Saves current buffer to render target |
| `RenderTransitionPass` | Animated transition between two scenes |

ALL passes import from `three/addons/postprocessing/{PassName}.js`.

---

## Key Effect Configuration

### UnrealBloomPass

```js
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const bloom = new UnrealBloomPass(
  new THREE.Vector2( window.innerWidth, window.innerHeight ),
  1.5,  // strength -- bloom intensity [0, 3+]
  0.4,  // radius -- bloom spread [0, 1]
  0.85  // threshold -- luminance cutoff [0, 1]
);
```

Tone mapping MUST be enabled on the renderer for bloom to work correctly. Selective bloom (per-object) is NOT natively supported -- use the `layers` system with multiple render passes as a workaround.

### SSAOPass / GTAOPass

ALWAYS prefer `GTAOPass` over `SSAOPass` for production quality. Use `SSAOPass` only for prototyping.

```js
// SSAOPass (faster, lower quality)
const ssao = new SSAOPass( scene, camera, width, height );
ssao.kernelRadius = 8;
ssao.minDistance = 0.005;
ssao.maxDistance = 0.1;

// GTAOPass (slower, production quality)
const gtao = new GTAOPass( scene, camera, width, height );
```

### OutlinePass

```js
const outline = new OutlinePass(
  new THREE.Vector2( window.innerWidth, window.innerHeight ),
  scene, camera
);
outline.selectedObjects = [ mesh1, mesh2 ];
outline.edgeStrength = 3;
outline.edgeGlow = 0;
outline.edgeThickness = 1;
outline.visibleEdgeColor.set( 0xffffff );
outline.hiddenEdgeColor.set( 0x190a05 );
```

---

## Custom ShaderPass

```js
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';

const myShader = {
  uniforms: {
    tDiffuse: { value: null }, // ALWAYS include -- receives read buffer
    amount: { value: 0.5 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float amount;
    varying vec2 vUv;
    void main() {
      vec4 color = texture2D( tDiffuse, vUv );
      gl_FragColor = mix( color, vec4( 1.0 - color.rgb, color.a ), amount );
    }
  `
};

const customPass = new ShaderPass( myShader );
composer.insertPass( customPass, 1 ); // after RenderPass
```

The `textureID` parameter defaults to `'tDiffuse'`. If your shader uses a different uniform name for the input texture, pass it as the second argument: `new ShaderPass( myShader, 'myInputTexture' )`.

---

## pmndrs/postprocessing

### Architecture

The `pmndrs/postprocessing` library merges multiple effects into a SINGLE shader pass, reducing draw calls significantly compared to the built-in system.

```js
import { EffectComposer, EffectPass, RenderPass, BloomEffect,
         SMAAEffect } from 'postprocessing';

const composer = new EffectComposer( renderer );
composer.addPass( new RenderPass( scene, camera ) );
composer.addPass( new EffectPass( camera, new BloomEffect(), new SMAAEffect() ) );

function animate() {
  composer.render();
}
```

### Key Effects

| Effect | Purpose |
|--------|---------|
| `BloomEffect` | Configurable bloom with mipmaps |
| `SMAAEffect` | Subpixel morphological AA |
| `SSAOEffect` | Screen-space ambient occlusion |
| `DepthOfFieldEffect` | Bokeh depth-of-field |
| `ToneMappingEffect` | Tone mapping operators |
| `VignetteEffect` | Screen edge darkening |
| `ChromaticAberrationEffect` | Color fringing |
| `NoiseEffect` | Film grain |
| `GodRaysEffect` | Volumetric light scattering |

For React Three Fiber, use `@react-three/postprocessing` which wraps these effects as JSX components.

---

## Resize Handling

ALWAYS resize both the renderer AND the composer on window resize:

```js
window.addEventListener( 'resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize( window.innerWidth, window.innerHeight );
  composer.setSize( window.innerWidth, window.innerHeight ); // MUST resize
});
```

---

## WebGPU PostProcessing

The WebGPU renderer uses a SEPARATE node-based system:

```js
import { PostProcessing } from 'three/addons/tsl/display/PostProcessing.js';

const postProcessing = new PostProcessing( renderer );
// Uses TSL (Three Shading Language) node graphs for effects
```

This is entirely incompatible with both the built-in WebGL `EffectComposer` and `pmndrs/postprocessing`.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for EffectComposer, all passes, and pmndrs effects
- [references/examples.md](references/examples.md) -- Working code examples for common post-processing setups
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with post-processing

### Official Sources

- https://threejs.org/docs/#examples/en/postprocessing/EffectComposer
- https://threejs.org/examples/?q=postprocessing
- https://github.com/pmndrs/postprocessing
- https://docs.pmnd.rs/react-three-fiber/tutorials/post-processing
