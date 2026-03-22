---
name: threejs-impl-lighting
description: >
  Use when setting up lighting in a Three.js scene: ambient, directional,
  point, spot, area, or environment lighting. Prevents the common mistake
  of too many shadow-casting lights, wrong intensity units, or missing
  environment maps for PBR. Covers all 7 light types, PMREMGenerator,
  HDR environment maps, physically correct intensity, helpers.
  Keywords: lighting, AmbientLight, DirectionalLight, PointLight,
  SpotLight, RectAreaLight, HemisphereLight, environment map, HDR, IBL,
  PMREMGenerator, scene.environment.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-lighting

## Quick Reference

### Light Types at a Glance

| Light | Shadows | Direction | Cost | Intensity Unit (r160+) |
|-------|---------|-----------|------|----------------------|
| `AmbientLight` | NO | None (uniform) | Negligible | Unitless multiplier |
| `HemisphereLight` | NO | Vertical gradient | Negligible | Unitless multiplier |
| `DirectionalLight` | YES | Parallel rays | Moderate | Lux |
| `PointLight` | YES (6-pass!) | Omnidirectional | High | Candela |
| `SpotLight` | YES | Cone | High | Candela |
| `RectAreaLight` | NO | Planar emission | Very high | Nits (cd/m2) |
| `LightProbe` | NO | Spherical harmonics | Low | Unitless multiplier |

### Critical Warnings

**NEVER** use `AmbientLight` as the sole light source -- it produces flat, dimensionless rendering. ALWAYS combine it with at least one directional or point light.

**NEVER** forget to add `light.target` to the scene when repositioning a `DirectionalLight` or `SpotLight` target -- the direction vector will NOT update without it.

**NEVER** use `RectAreaLight` without calling `RectAreaLightUniformsLib.init()` first (WebGLRenderer) or `RectAreaLightTexturesLib` (WebGPURenderer) -- the light will render incorrectly or not at all.

**NEVER** use more than 1-2 shadow-casting `PointLight` instances -- each requires 6 shadow map render passes. Use `SpotLight` with shadows as a cheaper alternative.

**ALWAYS** call `pmremGenerator.dispose()` after generating environment maps -- PMREMGenerator allocates significant GPU memory.

**ALWAYS** set `renderer.toneMapping` when using physically correct intensity values -- without tone mapping, high lux/candela values produce blown-out white scenes.

---

## Light Class Hierarchy

All lights inherit from `Light`, which extends `Object3D`:

```
Object3D
  └── Light (abstract: .color, .intensity, .dispose())
        ├── AmbientLight        — uniform fill
        ├── HemisphereLight     — sky/ground gradient
        ├── DirectionalLight    — parallel rays (sun)
        ├── PointLight          — omnidirectional (bulb)
        ├── SpotLight           — cone (flashlight)
        ├── RectAreaLight       — planar (window/panel)
        └── LightProbe          — spherical harmonics (IBL)
```

The `Light` base class provides:
- `.color` (Color) -- light color, default `0xffffff`
- `.intensity` (number) -- strength multiplier, default `1`
- `.isLight` (boolean, readonly) -- ALWAYS `true`
- `.dispose()` -- releases GPU resources

---

## Physically Correct Lighting (r160+)

As of r160+, ALL lighting uses physically based units by default. The legacy `renderer.useLegacyLights` property was removed.

| Light Type | Intensity Unit | Description |
|-----------|---------------|-------------|
| DirectionalLight | **Lux** (lm/m2) | Sunlight: 50,000-100,000 lux |
| PointLight | **Candela** (lm/sr) | 100W bulb: ~1700 cd |
| SpotLight | **Candela** (lm/sr) | Stage spot: ~10,000 cd |
| RectAreaLight | **Nits** (cd/m2) | LED panel: ~500-5000 nits |
| AmbientLight | Unitless | Multiplier, no physical unit |
| HemisphereLight | Unitless | Multiplier, no physical unit |

The `.power` property on PointLight, SpotLight, and RectAreaLight gives luminous power in **lumens**:
- PointLight: `power = intensity * 4 * Math.PI`
- SpotLight: `power = intensity * Math.PI`

**ALWAYS** pair physically correct intensities with tone mapping:

```javascript
import * as THREE from 'three';

renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
```

---

## The 7 Light Types

### AmbientLight

Uniform fill light. NO direction, NO shadows. Use for base illumination only.

```javascript
const ambient = new THREE.AmbientLight(0x404040, 0.5);
scene.add(ambient);
```

### HemisphereLight

Sky-to-ground gradient. NO shadows. Simulates outdoor ambient with sky and ground bounce.

```javascript
const hemi = new THREE.HemisphereLight(0xffffbb, 0x080820, 1.0);
scene.add(hemi);
```

Properties: `.groundColor` (Color) -- lower hemisphere color.

### DirectionalLight

Parallel rays simulating distant light (sun). Direction = `light.position` to `light.target.position`.

```javascript
const sun = new THREE.DirectionalLight(0xffffff, 3);
sun.position.set(5, 10, 7.5);
scene.add(sun);
scene.add(sun.target); // REQUIRED for target repositioning
```

Properties: `.target` (Object3D), `.shadow` (DirectionalLightShadow).

### PointLight

Omnidirectional light from a single point. Shadows cost 6 render passes.

```javascript
const bulb = new THREE.PointLight(0xffaa44, 800, 20, 2);
bulb.position.set(0, 3, 0);
scene.add(bulb);
```

Properties: `.distance` (number, `0`=infinite), `.decay` (number, `2`=physically correct), `.power` (lumens).

### SpotLight

Cone-shaped light. ALWAYS set `penumbra >= 0.1` for realistic soft edges.

```javascript
const spot = new THREE.SpotLight(0xffffff, 1000);
spot.position.set(0, 10, 0);
spot.angle = Math.PI / 6;
spot.penumbra = 0.3;
spot.decay = 2;
scene.add(spot);
scene.add(spot.target); // REQUIRED for target repositioning
```

Properties: `.angle` (max `Math.PI/2`), `.penumbra` (0-1), `.distance`, `.decay`, `.power`, `.map` (cookie texture, REQUIRES `castShadow = true`), `.target`, `.shadow`.

### RectAreaLight

Planar emitter for windows, panels, strip lights. Works ONLY with `MeshStandardMaterial` and `MeshPhysicalMaterial`. CANNOT cast shadows.

```javascript
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

RectAreaLightUniformsLib.init(); // MUST call before creating any RectAreaLight

const panel = new THREE.RectAreaLight(0xffffff, 5, 4, 10);
panel.position.set(5, 5, 0);
panel.lookAt(0, 0, 0); // Orient using lookAt, NOT rotation
scene.add(panel);
```

Properties: `.width`, `.height`, `.power` (lumens).

### LightProbe

Spherical harmonics-based ambient lighting. Useful for AR and baked environment lighting.

```javascript
import { LightProbeGenerator } from 'three/addons/lights/LightProbeGenerator.js';

const probe = LightProbeGenerator.fromCubeTexture(cubeTexture);
scene.add(probe);
```

---

## Environment Maps (IBL)

Image-Based Lighting (IBL) provides the most realistic ambient illumination for PBR materials. The standard workflow uses `RGBELoader` + `PMREMGenerator`.

### Standard HDR Environment Workflow

```javascript
import * as THREE from 'three';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

const pmremGenerator = new THREE.PMREMGenerator(renderer);
const rgbeLoader = new RGBELoader();

rgbeLoader.load('environment.hdr', (hdrTexture) => {
  const envMap = pmremGenerator.fromEquirectangular(hdrTexture);

  scene.environment = envMap.texture;  // ALL PBR materials auto-use this
  scene.background = envMap.texture;   // Optional: visible HDR background

  hdrTexture.dispose();                // Free source texture
  pmremGenerator.dispose();            // ALWAYS dispose after use
});
```

### scene.environment vs scene.background

| Property | Effect | When to Use |
|----------|--------|-------------|
| `scene.environment` | PBR reflections + ambient lighting on all Standard/Physical materials | ALWAYS for realistic PBR |
| `scene.background` | Visible skybox/backdrop | When you want the HDR visible |
| Both set to same texture | Full IBL with visible environment | Most common for product shots |
| `scene.backgroundBlurriness` | Blur the background (0-1) | Depth-of-field effect on backdrop |
| `scene.environmentIntensity` | Scale IBL contribution | Fine-tune ambient level |
| `scene.environmentRotation` | Rotate the environment map | Adjust light direction without moving lights |

When `scene.environment` is set, ALL `MeshStandardMaterial` and `MeshPhysicalMaterial` instances AUTOMATICALLY use it for reflections and ambient lighting -- no per-material configuration needed.

### PMREMGenerator Methods

| Method | Input | Purpose |
|--------|-------|---------|
| `fromEquirectangular(texture)` | Equirectangular texture | Convert HDR panorama to PMREM |
| `fromScene(scene, sigma?)` | Three.js Scene | Generate PMREM from a 3D scene |
| `fromCubemap(texture)` | CubeTexture | Convert cubemap to PMREM |
| `dispose()` | -- | Free GPU memory (ALWAYS call) |

### EXR Alternative

```javascript
import { EXRLoader } from 'three/addons/loaders/EXRLoader.js';

new EXRLoader().load('environment.exr', (exrTexture) => {
  const envMap = pmremGenerator.fromEquirectangular(exrTexture);
  scene.environment = envMap.texture;
  exrTexture.dispose();
  pmremGenerator.dispose();
});
```

---

## Light Helpers

| Helper | Import | Constructor |
|--------|--------|-------------|
| `DirectionalLightHelper` | `three` | `new DirectionalLightHelper(light, size?, color?)` |
| `SpotLightHelper` | `three` | `new SpotLightHelper(light, color?)` |
| `PointLightHelper` | `three` | `new PointLightHelper(light, sphereSize?, color?)` |
| `HemisphereLightHelper` | `three` | `new HemisphereLightHelper(light, size, color?)` |
| `RectAreaLightHelper` | `three/addons/helpers/RectAreaLightHelper.js` | `new RectAreaLightHelper(light)` |
| `LightProbeHelper` | `three/addons/helpers/LightProbeHelper.js` | `new LightProbeHelper(probe, size)` |

**ALWAYS** call `helper.update()` after changing light properties if the helper does not auto-update.

```javascript
const helper = new THREE.DirectionalLightHelper(dirLight, 5);
scene.add(helper);
// After changing dirLight properties:
helper.update();
```

---

## Performance Budget

| Category | Budget |
|----------|--------|
| Mobile WebGL | Max 4-5 real-time lights total |
| Desktop WebGL | Max 8-16 lights depending on scene |
| Shadow-casting PointLights | Max 1-2 (6 passes each) |
| RectAreaLights | Max 2-3 (expensive LTC evaluation) |

**ALWAYS** prefer baked lighting for static environments over real-time lights.

**ALWAYS** use environment maps (IBL) as the primary ambient source instead of multiple fill lights.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for all light types and PMREMGenerator
- [references/examples.md](references/examples.md) -- Lighting recipes: outdoor, indoor, studio, product
- [references/anti-patterns.md](references/anti-patterns.md) -- Common lighting mistakes and fixes

### Official Sources

- https://threejs.org/docs/#api/en/lights/AmbientLight
- https://threejs.org/docs/#api/en/lights/DirectionalLight
- https://threejs.org/docs/#api/en/lights/PointLight
- https://threejs.org/docs/#api/en/lights/SpotLight
- https://threejs.org/docs/#api/en/lights/RectAreaLight
- https://threejs.org/docs/#api/en/lights/HemisphereLight
- https://threejs.org/docs/#api/en/lights/LightProbe
- https://threejs.org/docs/#api/en/extras/PMREMGenerator
