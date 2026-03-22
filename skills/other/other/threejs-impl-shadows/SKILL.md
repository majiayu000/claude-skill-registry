---
name: threejs-impl-shadows
description: >
  Use when enabling shadows in a Three.js scene or debugging shadow
  artifacts like acne, peter panning, or low resolution. Prevents the
  common mistake of wrong shadow camera frustum, too many PointLight
  shadows, or missing castShadow/receiveShadow flags. Covers shadow map
  types, per-light config, bias tuning, CameraHelper debugging.
  Keywords: shadows, shadowMap, shadow acne, peter panning, bias,
  normalBias, castShadow, receiveShadow, PCFSoftShadowMap, shadow camera.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-shadows

## Quick Reference

### Three-Step Shadow Opt-In

Shadows in Three.js require THREE explicit opt-in steps. Missing ANY step results in no shadows.

```js
import * as THREE from 'three';

// Step 1: Enable shadow maps on the renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Step 2: Enable shadow casting on the light
light.castShadow = true;

// Step 3: Enable per-mesh shadow behavior
mesh.castShadow = true;       // this mesh casts shadows
ground.receiveShadow = true;  // this mesh receives shadows
```

### Shadow Map Types

| Type | Constant | Quality | Cost | Supports `.radius` |
|------|----------|---------|------|---------------------|
| Basic | `THREE.BasicShadowMap` | Hard edges, aliased | Lowest | No |
| PCF | `THREE.PCFShadowMap` | Slightly softened | Moderate | No |
| PCF Soft | `THREE.PCFSoftShadowMap` | Soft penumbra | Higher | No (ignores it) |
| VSM | `THREE.VSMShadowMap` | Gaussian blur | Moderate | Yes |

- **Default** in r160+: `THREE.PCFShadowMap`
- **PCFSoftShadowMap**: best general-purpose choice; IGNORES the `shadow.radius` property
- **VSMShadowMap**: supports `shadow.radius` and `shadow.blurSamples` but can exhibit light bleeding on thin geometry

### Critical Warnings

**NEVER** forget any of the three opt-in steps -- missing even one produces zero shadows with no error message.

**NEVER** leave the DirectionalLight shadow camera frustum at default size -- it is almost ALWAYS wrong for your scene. ALWAYS configure it manually.

**NEVER** use more than 1-2 shadow-casting PointLights -- each PointLight shadow renders 6 cubemap faces per frame.

**ALWAYS** set `shadow.mapSize` to power-of-two values (512, 1024, 2048, 4096).

**ALWAYS** add `light.target` to the scene when repositioning a DirectionalLight or SpotLight target.

---

## Shadow Map Types -- Detailed Comparison

### BasicShadowMap

No filtering applied. Produces hard, aliased shadow edges. Use ONLY for debugging or stylized rendering where hard shadows are intentional.

### PCFShadowMap (Default)

Percentage-Closer Filtering with a fixed-size kernel. Produces slightly softened edges. Good balance of quality and performance. The `shadow.radius` property has NO effect.

### PCFSoftShadowMap

Uses a variable kernel for softer penumbra simulation. Higher quality than PCF but more expensive. The `shadow.radius` property is IGNORED -- softness is determined automatically by the filter.

### VSMShadowMap

Variance Shadow Maps use a Gaussian blur pass. Supports `shadow.radius` (blur size) and `shadow.blurSamples` (sample count). Produces smooth soft shadows but suffers from **light bleeding** artifacts where thin geometry meets shadow receivers. NEVER use VSM for scenes with many thin overlapping shadow casters.

---

## Per-Light Shadow Configuration

### DirectionalLight Shadows

Uses an **orthographic** shadow camera. The frustum MUST be manually sized to encompass the shadowed area.

```js
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 7.5);
dirLight.castShadow = true;

// Shadow map resolution
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;

// Orthographic frustum -- MUST size manually
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 500;
dirLight.shadow.camera.left = -50;
dirLight.shadow.camera.right = 50;
dirLight.shadow.camera.top = 50;
dirLight.shadow.camera.bottom = -50;

// Anti-acne bias
dirLight.shadow.bias = -0.0001;
dirLight.shadow.normalBias = 0.02;

scene.add(dirLight);
scene.add(dirLight.target); // REQUIRED if repositioning target
```

**Frustum sizing rule**: Make the frustum as TIGHT as possible around the area that needs shadows. A frustum that is too large wastes shadow map resolution; a frustum that is too small clips shadows.

### SpotLight Shadows

Uses a **perspective** shadow camera that auto-configures from the SpotLight `.angle` and `.distance`. Manual frustum configuration is typically unnecessary.

```js
const spotLight = new THREE.SpotLight(0xffffff, 1);
spotLight.position.set(0, 10, 0);
spotLight.angle = Math.PI / 6;
spotLight.penumbra = 0.3;
spotLight.castShadow = true;

spotLight.shadow.mapSize.width = 1024;
spotLight.shadow.mapSize.height = 1024;
spotLight.shadow.bias = -0.0001;

scene.add(spotLight);
scene.add(spotLight.target);
```

SpotLightShadow exposes:
- `.focus` (number, default `1`) -- adjusts shadow camera FOV relative to spotlight FOV, range `[0, 1]`

### PointLight Shadows

Uses a **cubemap** (6 perspective cameras, one per face). This is the MOST expensive shadow type -- rendering the scene 6 times per shadow-casting PointLight per frame.

```js
const pointLight = new THREE.PointLight(0xffffff, 1, 100);
pointLight.position.set(0, 5, 0);
pointLight.castShadow = true;

// Lower resolution to offset the 6x render cost
pointLight.shadow.mapSize.width = 512;
pointLight.shadow.mapSize.height = 512;
pointLight.shadow.bias = -0.001;
pointLight.shadow.camera.near = 0.5;
pointLight.shadow.camera.far = 50;

scene.add(pointLight);
```

**Performance rule**: ALWAYS prefer SpotLight shadows over PointLight shadows. A PointLight shadow costs 6x what a SpotLight shadow costs. Use PointLight shadows ONLY when omnidirectional shadow casting is absolutely required.

---

## Shadow Debugging with CameraHelper

ALWAYS use `CameraHelper` to visualize the shadow camera frustum when configuring shadows:

```js
const shadowHelper = new THREE.CameraHelper(dirLight.shadow.camera);
scene.add(shadowHelper);
```

The helper renders the frustum as wireframe lines. If shadows are clipped, missing, or low resolution, the helper reveals whether the frustum is too small, too large, or misaligned.

**ALWAYS** remove CameraHelper in production builds.

---

## Shadow Artifact Diagnosis Flowchart

```
Shadows not visible?
├── Check renderer.shadowMap.enabled === true
├── Check light.castShadow === true
├── Check mesh.castShadow / ground.receiveShadow === true
├── Check shadow camera frustum encompasses the scene (use CameraHelper)
└── Check shadow.camera.far is large enough

Striped lines on surfaces? (Shadow Acne)
├── Increase shadow.bias (start at -0.0001, go to -0.005)
├── Increase shadow.normalBias (0.02 to 0.1) for curved surfaces
└── Increase shadow.mapSize for more depth precision

Shadows float away from objects? (Peter Panning)
├── Reduce shadow.bias (you over-corrected for acne)
├── Use shadow.normalBias instead of shadow.bias
└── Increase shadow.mapSize resolution

Shadow edges shimmer when camera moves? (Shadow Swimming)
├── Increase shadow.mapSize resolution
├── Snap shadow camera to texel-aligned positions
└── Use Cascaded Shadow Maps (CSM) for large scenes

Light leaks through thin geometry? (Light Bleeding -- VSM only)
├── Switch from VSMShadowMap to PCFSoftShadowMap
├── Increase geometry thickness
└── Reduce shadow.radius value

Shadows on transparent/alpha-tested materials incorrect?
├── Set material.alphaTest threshold
├── Assign customDepthMaterial with matching alpha map
└── For fully transparent objects: use baked shadows or ContactShadows
```

---

## Transparent Material Shadows

By default, shadows treat ALL geometry as fully opaque. For alpha-tested materials (e.g., tree leaves), assign a `customDepthMaterial`:

```js
import * as THREE from 'three';

const alphaMap = new THREE.TextureLoader().load('leaf-alpha.png');

const leafMaterial = new THREE.MeshStandardMaterial({
  map: texture,
  alphaMap: alphaMap,
  alphaTest: 0.5,
  side: THREE.DoubleSide,
});

// Custom depth material for correct shadow casting
const depthMaterial = new THREE.MeshDepthMaterial({
  depthPacking: THREE.RGBADepthPacking,
  map: texture,
  alphaMap: alphaMap,
  alphaTest: 0.5,
});

leafMesh.material = leafMaterial;
leafMesh.customDepthMaterial = depthMaterial;
leafMesh.castShadow = true;
```

**NEVER** expect transparent objects (`opacity < 1` without `alphaTest`) to cast correct real-time shadows. Use baked shadows or screen-space techniques instead.

---

## Static Shadow Optimization

For scenes where lights and shadow casters do NOT move, disable automatic shadow updates:

```js
renderer.shadowMap.autoUpdate = false;
renderer.shadowMap.needsUpdate = true; // render shadows once
```

Set `renderer.shadowMap.needsUpdate = true` ONLY when something changes. This eliminates per-frame shadow map rendering entirely for static scenes.

Per-light control:
```js
light.shadow.autoUpdate = false;
light.shadow.needsUpdate = true; // update this light's shadow once
```

---

## ContactShadows Alternative (Drei / React Three Fiber)

For ground-plane shadows, Drei's `<ContactShadows>` provides high-quality soft shadows at lower cost than shadow maps:

```jsx
import { ContactShadows } from '@react-three/drei';

<ContactShadows
  position={[0, 0, 0]}
  opacity={0.5}
  scale={10}
  blur={1.5}
  far={1}
/>
```

**Limitations**: Works ONLY for ground-plane shadows. Does NOT project onto arbitrary geometry. Does NOT replace shadow maps for complex scenes.

---

## Performance Budget

| Shadow Type | Cost per Frame | Max Recommended |
|-------------|---------------|-----------------|
| DirectionalLight shadow | 1 render pass | 1-2 lights |
| SpotLight shadow | 1 render pass | 2-4 lights |
| PointLight shadow | 6 render passes | 1 light max |

**Shadow map resolution impact**: Doubling `mapSize` quadruples GPU memory usage. NEVER exceed 4096x4096 on mobile; prefer 2048x2048 or lower.

**ALWAYS** profile with `renderer.info.render.calls` to verify shadow pass count does not exceed your frame budget.

---

## Reference Links

- [references/methods.md](references/methods.md) -- LightShadow API signatures and shadow map type constants
- [references/examples.md](references/examples.md) -- Complete shadow setup examples for each light type
- [references/anti-patterns.md](references/anti-patterns.md) -- Shadow artifacts, causes, and fixes

### Official Sources

- https://threejs.org/docs/#api/en/lights/shadows/LightShadow
- https://threejs.org/docs/#api/en/lights/shadows/DirectionalLightShadow
- https://threejs.org/docs/#api/en/lights/shadows/SpotLightShadow
- https://threejs.org/docs/#api/en/lights/shadows/PointLightShadow
- https://threejs.org/docs/#api/en/renderers/WebGLRenderer (shadowMap property)
- https://threejs.org/docs/#api/en/helpers/CameraHelper
