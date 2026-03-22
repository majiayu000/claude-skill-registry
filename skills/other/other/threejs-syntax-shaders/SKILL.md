---
name: threejs-syntax-shaders
description: >
  Use when writing custom GLSL shaders, creating ShaderMaterial or
  RawShaderMaterial, defining uniforms, or patching built-in materials
  with onBeforeCompile. Prevents the common mistake of wrong uniform
  format, missing needsUpdate on uniforms, or not including required
  defines. Covers ShaderMaterial, RawShaderMaterial, GLSL, uniforms,
  ShaderChunk, onBeforeCompile, defines, GLSL3.
  Keywords: ShaderMaterial, RawShaderMaterial, GLSL, vertex shader,
  fragment shader, uniform, varying, ShaderChunk, onBeforeCompile, custom shader.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-syntax-shaders

## Quick Reference

### ShaderMaterial vs RawShaderMaterial

| Aspect | ShaderMaterial | RawShaderMaterial |
|--------|----------------|-------------------|
| Built-in uniforms | Automatically injected | NONE -- you MUST declare everything |
| Built-in attributes | Automatically declared | NONE -- you MUST declare everything |
| `#include <chunk>` | Supported | NOT supported |
| Precision declaration | Automatic | You MUST add `precision mediump float;` |
| Use case | Extend Three.js rendering | Full shader control, porting external shaders |
| Performance | Slight overhead from unused built-ins | Minimal shader overhead |

### Uniform Type Map

| GLSL Type | JavaScript Value |
|-----------|-----------------|
| `float` | `{ value: 1.0 }` |
| `int` | `{ value: 1 }` |
| `bool` | `{ value: true }` |
| `vec2` | `{ value: new THREE.Vector2() }` |
| `vec3` | `{ value: new THREE.Vector3() }` or `{ value: new THREE.Color() }` |
| `vec4` | `{ value: new THREE.Vector4() }` |
| `mat3` | `{ value: new THREE.Matrix3() }` |
| `mat4` | `{ value: new THREE.Matrix4() }` |
| `sampler2D` | `{ value: texture }` (a `THREE.Texture` instance) |
| `samplerCube` | `{ value: cubeTexture }` |
| `float[]` | `{ value: [1.0, 2.0, 3.0] }` |
| `vec3[]` | `{ value: [new THREE.Vector3(), ...] }` |

### Critical Warnings

**NEVER** pass a bare value as a uniform -- ALWAYS wrap it in `{ value: ... }`. Writing `uniforms: { uTime: 0.0 }` silently fails; ALWAYS write `uniforms: { uTime: { value: 0.0 } }`.

**NEVER** declare built-in uniforms or attributes in a `ShaderMaterial` shader -- Three.js injects them automatically. Redeclaring causes a GLSL compilation error.

**ALWAYS** declare ALL uniforms, attributes, and precision in `RawShaderMaterial` shaders -- nothing is injected for you.

**NEVER** use `gl_FragColor` or `texture2D()` when `glslVersion` is `THREE.GLSL3` -- use a declared `out vec4` variable and `texture()` instead.

**ALWAYS** call `material.needsUpdate = true` after changing `defines` -- defines are compiled into the shader, so changes require recompilation.

---

## ShaderMaterial

### Constructor

```javascript
import * as THREE from 'three';

const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0.0 },
    uColor: { value: new THREE.Color(0x00ff00) },
    uTexture: { value: someTexture },
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec3 uColor;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(uColor * vUv.x, 1.0);
    }
  `,
  transparent: false,
  wireframe: false,
  side: THREE.FrontSide,
});
```

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `uniforms` | `Object` | `{}` | `{ name: { value: ... } }` format |
| `uniformsGroups` | `Array` | `[]` | Uniform buffer objects (UBO) |
| `vertexShader` | `string` | -- | GLSL vertex shader source |
| `fragmentShader` | `string` | -- | GLSL fragment shader source |
| `defines` | `Object` | `{}` | Preprocessor `#define` directives |
| `extensions` | `Object` | `{}` | GLSL extensions to enable |
| `wireframe` | `boolean` | `false` | Wireframe rendering |
| `lights` | `boolean` | `false` | Pass light uniforms to shader |
| `fog` | `boolean` | `false` | Pass fog uniforms to shader |
| `clipping` | `boolean` | `false` | Enable clipping planes |
| `glslVersion` | `string \| null` | `null` | `null` for GLSL1, `THREE.GLSL3` for GLSL 3.0 ES |
| `defaultAttributeValues` | `Object` | -- | Fallback values for missing attributes |

---

## Built-in Uniforms (ShaderMaterial Only)

These are injected automatically. NEVER declare them yourself.

```glsl
// Transform matrices
uniform mat4 modelMatrix;           // Object -> World
uniform mat4 modelViewMatrix;       // Object -> Camera
uniform mat4 projectionMatrix;      // Camera -> Clip
uniform mat4 viewMatrix;            // World -> Camera
uniform mat3 normalMatrix;          // Transpose inverse of modelViewMatrix

// Camera
uniform vec3 cameraPosition;        // Camera world position

// When lights: true
uniform vec3 ambientLightColor;
// Plus structured arrays for directional, point, spot, hemisphere lights
```

## Built-in Attributes (ShaderMaterial Only)

These are injected automatically. NEVER declare them yourself.

```glsl
attribute vec3 position;    // Vertex position
attribute vec3 normal;      // Vertex normal
attribute vec2 uv;          // Primary UV coordinates
attribute vec2 uv2;         // Secondary UV (for aoMap, lightMap)
attribute vec4 tangent;     // Tangent vector (if computeTangents was called)
attribute vec3 color;       // Vertex color (if geometry has color attribute)
```

---

## RawShaderMaterial

Use when you need full control over the shader source. NOTHING is injected.

```javascript
const material = new THREE.RawShaderMaterial({
  uniforms: {
    uModelViewMatrix: { value: new THREE.Matrix4() },
    uProjectionMatrix: { value: new THREE.Matrix4() },
  },
  vertexShader: `
    precision highp float;
    attribute vec3 position;
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;
    void main() {
      gl_Position = uProjectionMatrix * uModelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    precision highp float;
    void main() {
      gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
  `,
});
```

**ALWAYS** add `precision highp float;` (or `mediump`) at the top of both shaders in `RawShaderMaterial`. Omitting precision causes a GLSL compilation error on mobile and some desktop drivers.

---

## ShaderChunk -- Reusing Three.js Shader Code

`THREE.ShaderChunk` contains all internal shader fragments. Use `#include <chunk_name>` in `ShaderMaterial` (NOT `RawShaderMaterial`).

### Common Chunks

| Chunk | Purpose |
|-------|---------|
| `<common>` | Shared constants and functions (PI, saturate, etc.) |
| `<fog_pars_vertex>` / `<fog_vertex>` | Fog support (vertex) |
| `<fog_pars_fragment>` / `<fog_fragment>` | Fog support (fragment) |
| `<shadowmap_pars_vertex>` / `<shadowmap_vertex>` | Shadow support (vertex) |
| `<shadowmap_pars_fragment>` / `<shadowmap_fragment>` | Shadow support (fragment) |
| `<lights_pars_begin>` | Light structure declarations |
| `<begin_vertex>` | Initializes `transformed` variable from `position` |
| `<project_vertex>` | Applies modelViewMatrix and projectionMatrix |
| `<normal_fragment_begin>` | Normal mapping setup |
| `<color_pars_vertex>` / `<color_vertex>` | Vertex color support |

### Accessing Chunks Programmatically

```javascript
// Read the source of any chunk
console.log(THREE.ShaderChunk.common);
console.log(THREE.ShaderChunk.fog_pars_vertex);
```

---

## onBeforeCompile -- Patching Built-in Materials

Modify an existing material's shader at compile time. This preserves PBR lighting, shadows, and all built-in features.

```javascript
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });

material.onBeforeCompile = (shader) => {
  shader.uniforms.uTime = { value: 0.0 };

  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    `
    #include <begin_vertex>
    transformed.y += sin(transformed.x * 5.0 + uTime) * 0.5;
    `
  );

  // Store reference for uniform updates
  material.userData.shader = shader;
};

// ALWAYS override customProgramCacheKey when using onBeforeCompile
material.customProgramCacheKey = () => 'my-wavy-material';

// In animation loop
if (material.userData.shader) {
  material.userData.shader.uniforms.uTime.value = clock.getElapsedTime();
}
```

**ALWAYS** override `customProgramCacheKey()` when using `onBeforeCompile` -- without it, Three.js may reuse a cached unpatched shader program, causing your modifications to silently disappear.

**ALWAYS** check `material.userData.shader` exists before accessing uniforms -- the shader object is created lazily on first render and can be recreated when `material.needsUpdate = true`.

---

## Defines -- Preprocessor Directives

```javascript
const material = new THREE.ShaderMaterial({
  defines: {
    USE_FOG: '',           // #define USE_FOG
    MAX_LIGHTS: 4,         // #define MAX_LIGHTS 4
    EPSILON: '0.001',      // #define EPSILON 0.001
  },
  // ...shaders
});
```

Changing defines at runtime:

```javascript
material.defines.MAX_LIGHTS = 8;
material.needsUpdate = true;  // REQUIRED -- triggers recompilation
```

---

## GLSL3 Mode

```javascript
const material = new THREE.ShaderMaterial({
  glslVersion: THREE.GLSL3,
  vertexShader: `
    in vec3 position;           // 'attribute' becomes 'in'
    uniform mat4 modelViewMatrix;
    uniform mat4 projectionMatrix;
    out vec3 vPosition;         // 'varying' becomes 'out'

    void main() {
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    precision highp float;
    in vec3 vPosition;          // 'varying' becomes 'in'
    out vec4 fragColor;         // replaces gl_FragColor

    void main() {
      fragColor = vec4(vPosition * 0.5 + 0.5, 1.0);
    }
  `,
});
```

### GLSL1 vs GLSL3 Syntax

| GLSL1 | GLSL3 | Context |
|-------|-------|---------|
| `attribute` | `in` | Vertex shader inputs |
| `varying` (vertex) | `out` | Vertex shader outputs |
| `varying` (fragment) | `in` | Fragment shader inputs |
| `gl_FragColor` | Declared `out vec4` | Fragment shader output |
| `texture2D()` | `texture()` | Texture sampling |
| `textureCube()` | `texture()` | Cube texture sampling |

---

## Uniform Update Pattern

```javascript
// At creation
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0.0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
    uMouse: { value: new THREE.Vector2() },
  },
  vertexShader: '...',
  fragmentShader: '...',
});

// In animation loop -- update the .value property directly
function animate() {
  material.uniforms.uTime.value = performance.now() / 1000;
  material.uniforms.uMouse.value.set(mouseX, mouseY);
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

**NEVER** replace the uniform object itself (e.g., `material.uniforms.uTime = { value: 5 }`). ALWAYS mutate the existing `.value` property. Replacing the object breaks the internal reference.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures
- [references/examples.md](references/examples.md) -- Working code examples
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do

### Official Sources

- https://threejs.org/docs/#api/en/materials/ShaderMaterial
- https://threejs.org/docs/#api/en/materials/RawShaderMaterial
- https://threejs.org/docs/#api/en/renderers/shaders/ShaderChunk
- https://threejs.org/docs/#api/en/renderers/shaders/UniformsLib
