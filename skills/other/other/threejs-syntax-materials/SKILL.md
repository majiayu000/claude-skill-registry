---
name: threejs-syntax-materials
description: >
  Use when choosing or configuring materials, loading textures, or setting
  up PBR workflows in Three.js. Prevents the common mistake of wrong
  color space on textures, forgetting material.dispose(), or not calling
  material.needsUpdate after changes. Covers all 15+ material types, PBR
  metalness/roughness, MeshPhysicalMaterial, texture maps, color space.
  Keywords: MeshStandardMaterial, MeshPhysicalMaterial, material, texture,
  PBR, metalness, roughness, normalMap, color space, SRGBColorSpace.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-syntax-materials

## Quick Reference

### Material Type Decision Tree

| Use Case | Material | Why |
|----------|----------|-----|
| UI elements, unlit scenes | `MeshBasicMaterial` | Cheapest, no light computation |
| Matte diffuse (low-end devices) | `MeshLambertMaterial` | Fast diffuse, no specular |
| Legacy specular highlights | `MeshPhongMaterial` | Blinn-Phong model, not physically correct |
| General-purpose 3D (recommended) | `MeshStandardMaterial` | PBR metalness/roughness, industry standard |
| Glass, car paint, fabric, soap bubbles | `MeshPhysicalMaterial` | Advanced PBR (clearcoat, transmission, sheen, iridescence) |
| Cartoon/anime style | `MeshToonMaterial` | Discrete cel-shading steps |
| Sculpting previews, no lights | `MeshMatcapMaterial` | Matcap texture, zero light setup |
| Debug normals | `MeshNormalMaterial` | RGB = surface normal direction |
| Invisible shadow receiver | `ShadowMaterial` | Transparent shadow catcher |
| Solid lines | `LineBasicMaterial` | Simple colored lines |
| Dashed lines | `LineDashedMaterial` | Requires `line.computeLineDistances()` |
| Particles | `PointsMaterial` | Point cloud rendering |
| Billboards | `SpriteMaterial` | Always-facing-camera quads |

### Base Material Properties (All Materials)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `side` | `number` | `FrontSide` | `FrontSide`, `BackSide`, or `DoubleSide` |
| `transparent` | `boolean` | `false` | Enable alpha blending |
| `opacity` | `number` | `1` | Requires `transparent: true` to take effect below 1 |
| `depthWrite` | `boolean` | `true` | Write to depth buffer |
| `depthTest` | `boolean` | `true` | Test against depth buffer |
| `blending` | `number` | `NormalBlending` | `NoBlending`, `AdditiveBlending`, `SubtractiveBlending`, `MultiplyBlending`, `CustomBlending` |
| `alphaTest` | `number` | `0` | Discard fragments with alpha below this value |
| `visible` | `boolean` | `true` | Whether to render this material |
| `wireframe` | `boolean` | `false` | Wireframe rendering mode |
| `fog` | `boolean` | `true` | Affected by scene fog |
| `clippingPlanes` | `Plane[]` | `null` | Array of clipping planes |
| `clipIntersection` | `boolean` | `false` | Clip where ALL planes intersect (vs union) |
| `needsUpdate` | `boolean` | `false` | Set `true` to trigger shader recompilation |
| `toneMapped` | `boolean` | `true` | Apply renderer tone mapping |

### Base Material Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `clone` | `(): Material` | Clone the material |
| `copy` | `(source: Material): Material` | Copy properties from source |
| `dispose` | `(): void` | Free GPU resources -- ALWAYS call when removing |
| `onBeforeCompile` | `(shader, renderer): void` | Hook to modify shader before compilation |
| `setValues` | `(values: Object): void` | Set multiple properties at once |

### Critical Warnings

**NEVER** set `opacity < 1` without `transparent: true` -- the opacity value is silently ignored. ALWAYS pair them together.

**NEVER** use `MeshPhysicalMaterial` when `MeshStandardMaterial` suffices -- Physical compiles a significantly larger shader. ONLY use it when you need clearcoat, transmission, sheen, iridescence, or anisotropy.

**NEVER** set `SRGBColorSpace` on normal maps, roughness maps, metalness maps, or any data texture -- this corrupts the data and causes incorrect lighting. ONLY set `SRGBColorSpace` on diffuse/color/emissive textures.

**NEVER** forget to call `material.dispose()` and `texture.dispose()` when removing objects -- GPU memory leaks accumulate and crash the application.

**NEVER** set `linewidth > 1` on `LineBasicMaterial` -- it is silently ignored on most platforms due to WebGL limitations. ALWAYS use `Line2` + `LineMaterial` from `three/addons/lines/` for thick lines.

**ALWAYS** set `material.needsUpdate = true` after changing properties that affect shader compilation (e.g., toggling `flatShading`, changing `side`, adding/removing texture maps at runtime).

**ALWAYS** set `wrapS` and `wrapT` to `RepeatWrapping` when using `texture.repeat` values other than `(1, 1)` -- the default `ClampToEdgeWrapping` does NOT tile textures.

---

## MeshStandardMaterial (PBR)

The recommended material for most 3D scenes. Uses physically-based metalness/roughness workflow.

```javascript
import { MeshStandardMaterial, TextureLoader, SRGBColorSpace, RepeatWrapping } from 'three';

const loader = new TextureLoader();
const material = new MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.7,           // 0 = mirror, 1 = fully rough
  metalness: 0.0,           // 0 = dielectric, 1 = metal
  map: null,                // Diffuse/albedo texture
  roughnessMap: null,       // Per-pixel roughness
  metalnessMap: null,       // Per-pixel metalness
  normalMap: null,          // Surface normal perturbation
  normalScale: new Vector2(1, 1),
  aoMap: null,              // Ambient occlusion (requires uv2)
  aoMapIntensity: 1.0,
  emissive: 0x000000,       // Emissive color
  emissiveMap: null,        // Emissive texture
  emissiveIntensity: 1.0,
  envMap: null,             // Environment reflection map
  envMapIntensity: 1.0,
  bumpMap: null,            // Grayscale height map
  bumpScale: 1.0,
  displacementMap: null,    // Vertex displacement map
  displacementScale: 1.0,
  displacementBias: 0.0,
  alphaMap: null,           // Per-pixel transparency
  lightMap: null,           // Baked lighting (requires uv2)
  lightMapIntensity: 1.0,
  flatShading: false,
  wireframe: false,
  fog: true
});
```

---

## MeshPhysicalMaterial (Advanced PBR)

Extends `MeshStandardMaterial` with ALL its properties, plus:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `clearcoat` | `float` | `0.0` | Clear coat layer intensity (0-1) |
| `clearcoatRoughness` | `float` | `0.0` | Clear coat roughness |
| `clearcoatMap` | `Texture` | `null` | Clear coat intensity map |
| `clearcoatNormalMap` | `Texture` | `null` | Clear coat normal map |
| `transmission` | `float` | `0.0` | Physically-based transparency (0-1) |
| `transmissionMap` | `Texture` | `null` | Transmission map |
| `thickness` | `float` | `0.0` | Volume thickness for transmission |
| `thicknessMap` | `Texture` | `null` | Thickness map |
| `ior` | `float` | `1.5` | Index of refraction (1.0-2.333) |
| `attenuationDistance` | `float` | `Infinity` | Light attenuation distance in volume |
| `attenuationColor` | `Color` | `white` | Light attenuation tint |
| `sheen` | `float` | `0.0` | Sheen layer intensity (fabric-like) |
| `sheenColor` | `Color` | `0x000000` | Sheen tint color |
| `sheenRoughness` | `float` | `1.0` | Sheen roughness |
| `iridescence` | `float` | `0.0` | Thin-film interference (0-1) |
| `iridescenceIOR` | `float` | `1.3` | Iridescence index of refraction |
| `iridescenceThicknessRange` | `[float, float]` | `[100, 400]` | Thin-film thickness range (nm) |
| `anisotropy` | `float` | `0.0` | Anisotropic reflection strength |
| `anisotropyRotation` | `float` | `0.0` | Anisotropy rotation (radians) |
| `specularIntensity` | `float` | `1.0` | Specular layer intensity |
| `specularColor` | `Color` | `white` | Specular tint color |
| `dispersion` | `float` | `0.0` | Chromatic dispersion (rainbow effect) |
| `reflectivity` | `float` | `0.5` | Reflectivity at normal incidence |

---

## Texture System

### Color Space Rules (Critical)

| Map Type | Color Space | Channels Used |
|----------|-------------|---------------|
| `map` (diffuse/albedo) | `SRGBColorSpace` | RGB(A) |
| `emissiveMap` | `SRGBColorSpace` | RGB |
| `lightMap` | `SRGBColorSpace` | RGB |
| `envMap` | `SRGBColorSpace` | RGB |
| `sheenColorMap` | `SRGBColorSpace` | RGB |
| `specularColorMap` | `SRGBColorSpace` | RGB |
| `normalMap` | `NoColorSpace` | RGB |
| `roughnessMap` | `NoColorSpace` | G channel |
| `metalnessMap` | `NoColorSpace` | B channel |
| `aoMap` | `NoColorSpace` | R channel |
| `bumpMap` | `NoColorSpace` | R channel |
| `displacementMap` | `NoColorSpace` | R channel |
| `alphaMap` | `NoColorSpace` | R channel |
| `clearcoatMap` | `NoColorSpace` | R channel |
| `clearcoatRoughnessMap` | `NoColorSpace` | R channel |
| `clearcoatNormalMap` | `NoColorSpace` | RGB |
| `transmissionMap` | `NoColorSpace` | R channel |
| `thicknessMap` | `NoColorSpace` | R channel |
| `iridescenceMap` | `NoColorSpace` | R channel |
| `iridescenceThicknessMap` | `NoColorSpace` | R channel |
| `sheenRoughnessMap` | `NoColorSpace` | R channel |
| `anisotropyMap` | `NoColorSpace` | RG channels |
| `specularIntensityMap` | `NoColorSpace` | A channel |

**Rule**: Diffuse/emissive/color textures = `SRGBColorSpace`. ALL data textures = `NoColorSpace`. Getting this wrong causes washed-out or over-saturated rendering.

### Texture Loaders

| Loader | Format | Import |
|--------|--------|--------|
| `TextureLoader` | PNG, JPG, WebP | `three` core |
| `CubeTextureLoader` | 6x PNG/JPG cube maps | `three` core |
| `RGBELoader` | .hdr (Radiance HDR) | `three/addons/loaders/RGBELoader.js` |
| `EXRLoader` | .exr (OpenEXR HDR) | `three/addons/loaders/EXRLoader.js` |
| `KTX2Loader` | .ktx2 (GPU compressed) | `three/addons/loaders/KTX2Loader.js` |

### Wrapping Modes

| Constant | Description |
|----------|-------------|
| `ClampToEdgeWrapping` | Edge texels stretched (default) |
| `RepeatWrapping` | Texture tiles/repeats |
| `MirroredRepeatWrapping` | Tiles with alternating mirror |

### Filter Modes

| Constant | Type | Description |
|----------|------|-------------|
| `NearestFilter` | Mag/Min | Pixelated, crisp (retro, toon gradients) |
| `LinearFilter` | Mag/Min | Smooth interpolation |
| `LinearMipmapLinearFilter` | Min | Trilinear filtering (default, best quality) |

### Texture Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `wrapS` / `wrapT` | `number` | `ClampToEdgeWrapping` | Wrapping mode |
| `magFilter` | `number` | `LinearFilter` | Magnification filter |
| `minFilter` | `number` | `LinearMipmapLinearFilter` | Minification filter |
| `anisotropy` | `number` | `1` | Anisotropic filtering (max = `renderer.capabilities.getMaxAnisotropy()`) |
| `repeat` | `Vector2` | `(1, 1)` | UV repeat count |
| `offset` | `Vector2` | `(0, 0)` | UV offset |
| `rotation` | `number` | `0` | UV rotation in radians |
| `center` | `Vector2` | `(0, 0)` | Center of rotation |
| `flipY` | `boolean` | `true` | Flip vertically on upload |
| `colorSpace` | `string` | `NoColorSpace` | Color space interpretation |
| `generateMipmaps` | `boolean` | `true` | Auto-generate mipmaps |
| `needsUpdate` | `boolean` | `false` | Trigger GPU re-upload |

### flipY Rules

- `flipY = true` (default): Correct for loaded image textures (PNG, JPG)
- `flipY = false`: ALWAYS use for `WebGLRenderTarget` textures, `DataTexture`, and framebuffer textures

---

## Material Disposal

```javascript
// ALWAYS dispose materials and textures when removing objects
function disposeMesh(mesh) {
  if (mesh.material) {
    // Dispose all texture maps
    for (const key of Object.keys(mesh.material)) {
      const value = mesh.material[key];
      if (value && value.isTexture) {
        value.dispose();
      }
    }
    mesh.material.dispose();
  }
  if (mesh.geometry) {
    mesh.geometry.dispose();
  }
}
```

---

## needsUpdate Flag

ALWAYS set `material.needsUpdate = true` after changing these at runtime:
- Toggling `flatShading`
- Changing `side` (FrontSide/BackSide/DoubleSide)
- Adding or removing a texture map (e.g., setting `map` from `null` to a texture)
- Changing `transparent` or `alphaTest`
- Toggling `wireframe`
- Any property that changes the compiled shader variant

NEVER set `needsUpdate = true` every frame -- it forces expensive shader recompilation. ONLY set it once after the property change.

For textures: set `texture.needsUpdate = true` after modifying `texture.image` data to trigger GPU re-upload.

---

## Toon Material Special Rule

When using `MeshToonMaterial`, ALWAYS set `gradientMap.minFilter = NearestFilter` and `gradientMap.magFilter = NearestFilter`. Linear filtering blurs the discrete shading steps into smooth gradients, defeating the toon effect.

---

## Reference Links

- [references/methods.md](references/methods.md) -- All material types with constructor signatures and key properties
- [references/examples.md](references/examples.md) -- Complete working examples (PBR, textures, multi-material)
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do, with explanations

### Official Sources

- https://threejs.org/docs/#api/en/materials/Material
- https://threejs.org/docs/#api/en/materials/MeshStandardMaterial
- https://threejs.org/docs/#api/en/materials/MeshPhysicalMaterial
- https://threejs.org/docs/#api/en/textures/Texture
