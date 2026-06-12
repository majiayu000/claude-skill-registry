---
name: cesiumjs-custom-shader
description: "CustomShader authoring — vertexShaderText and fragmentShaderText against VertexInput, FragmentInput, FeatureIds, Metadata, czm_modelMaterial. Use when reading EXT_mesh_features or EXT_structural_metadata property textures/tables, vertex displacement, or shading VoxelPrimitive."
---
# CesiumJS CustomShader

Version baseline: CesiumJS 1.139 (includes 1.139.1 patch). All imports use ES module style.

`CustomShader` injects user GLSL into the `Model` / `Cesium3DTileset` / `VoxelPrimitive` rendering pipeline. It exposes glTF attributes, feature IDs, and `EXT_structural_metadata` to per-vertex and per-fragment code, and returns values through the built-in `czm_modelVertexOutput` and `czm_modelMaterial` structs.

Use this skill for **writing the shader body**. Use:
- `cesiumjs-materials-shaders` — for Fabric `Material`, `ImageBasedLighting`, `PostProcessStage` (bloom, SSAO, FXAA, tonemapping).
- `cesiumjs-3d-tiles` — for declarative per-feature coloring via `Cesium3DTileStyle`, and for `VoxelPrimitive` setup/configuration.
- `cesiumjs-models-particles` — for `Model.fromGltfAsync`, animations, `ModelFeature.getProperty()`.

## Out of scope

- **Fabric `Material`** for entity polylines/polygons/walls — see `cesiumjs-materials-shaders`.
- **`PostProcessStage`** screen-space effects — see `cesiumjs-materials-shaders`.
- **`ImageBasedLighting`** — see `cesiumjs-materials-shaders`.
- **`Cesium3DTileStyle`** declarative JSON styling — see `cesiumjs-3d-tiles`. **Do not combine with CustomShader on the same tileset.**
- **Authoring `EXT_structural_metadata` / `EXT_mesh_features` in glTF** — tooling concern, not runtime.

## Minimal example

```js
import { CustomShader, Model } from "cesium";

const shader = new CustomShader({
  fragmentShaderText: `
    void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
      material.diffuse = vec3(1.0, 0.0, 0.0);
      material.alpha = 0.8;
    }
  `,
});

const model = await Model.fromGltfAsync({ url: "./aircraft.glb", customShader: shader });
viewer.scene.primitives.add(model);
```

## Applying a CustomShader

**Model** — constructor option or mutable property:

```js
const model = await Model.fromGltfAsync({ url, customShader });
model.customShader = newShader;     // hot-swap
model.customShader = undefined;     // clear
```

**Cesium3DTileset** — constructor option or mutable property. Only `Model`-backed tile content is affected (not native I3S or other formats):

```js
const tileset = await Cesium3DTileset.fromUrl(url, { customShader });
tileset.customShader = newShader;
```

> Per the `Cesium3DTileset.customShader` JSDoc: *"Using custom shaders with a `Cesium3DTileStyle` may lead to undefined behavior."* The property is also marked `@experimental` — it uses 3D Tiles spec surface that is not final and may change without Cesium's standard deprecation policy.

**VoxelPrimitive** — fragment-only subset (see "VoxelPrimitive shader subset" below):

```js
const voxelPrimitive = new VoxelPrimitive({ provider, customShader });
```

The engine calls `customShader.update(frameState)` automatically each frame. When finished with a CustomShader, call `customShader.destroy()` to release GPU texture resources owned by its `TextureManager`.

## Constructor reference

```js
new CustomShader({
  mode,                  // CustomShaderMode — default MODIFY_MATERIAL
  lightingModel,         // LightingModel — if omitted, model's default is preserved
  translucencyMode,      // CustomShaderTranslucencyMode — default INHERIT
  uniforms,              // { [name]: { type: UniformType, value } } — default {}
  varyings,              // { [name]: VaryingType } — default {}
  vertexShaderText,      // string or undefined
  fragmentShaderText,    // string or undefined
});
```

Either `vertexShaderText` or `fragmentShaderText` is typically required. See `REFERENCE.md` for exhaustive enum values.

## Shader function signatures

The runtime calls these from generated pipeline stages. Parameter names are part of the contract — renaming them breaks the shader.

```glsl
void vertexMain(VertexInput vsInput, inout czm_modelVertexOutput vsOutput) { ... }
void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) { ... }
```

## Uniforms

Declare uniforms with `{ type, value }`. The type is a `UniformType` value; the JS value type must match (e.g. `VEC3` → `Cartesian3`). Uniforms are accessible in GLSL by their declared name.

```js
import { CustomShader, UniformType, TextureUniform, Cartesian3 } from "cesium";

const shader = new CustomShader({
  uniforms: {
    u_tint:   { type: UniformType.VEC3,      value: new Cartesian3(1.0, 0.5, 0.2) },
    u_time:   { type: UniformType.FLOAT,     value: 0.0 },
    u_detail: { type: UniformType.SAMPLER_2D, value: new TextureUniform({ url: "./detail.png", repeat: true }) },
  },
  fragmentShaderText: `
    void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
      vec3 d = texture(u_detail, fsInput.attributes.texCoord_0).rgb;
      material.diffuse = mix(material.diffuse, u_tint, d.r + 0.1 * sin(u_time));
    }
  `,
});

// Update at runtime. For Cartesian/Matrix values, setUniform clones into existing storage.
shader.setUniform("u_time", performance.now() / 1000);
```

`TextureUniform` accepts either `url` (string or `Resource`) or `typedArray` + `width` + `height` — **exactly one** (constructor throws otherwise). Other options: `repeat` (default `true`), `pixelFormat`, `pixelDatatype`, `minificationFilter`, `magnificationFilter`, `maximumAnisotropy`.

**`SAMPLER_CUBE` is declared on `UniformType` but rejected at construction** — throws `DeveloperError("CustomShader does not support samplerCube uniforms")`. Only `SAMPLER_2D` is supported.

## Varyings

Declared varyings are emitted as `out <type> <name>` in the vertex shader and `in <type> <name>` in the fragment shader. Write in vertex, read in fragment.

```js
import { CustomShader, VaryingType } from "cesium";

const shader = new CustomShader({
  varyings: { v_worldHeight: VaryingType.FLOAT },
  vertexShaderText: `
    void vertexMain(VertexInput vsInput, inout czm_modelVertexOutput vsOutput) {
      v_worldHeight = vsInput.attributes.positionMC.z;
    }
  `,
  fragmentShaderText: `
    void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
      float t = clamp(v_worldHeight / 100.0, 0.0, 1.0);
      material.diffuse = mix(vec3(0.2,0.4,0.8), vec3(1.0,0.8,0.2), t);
    }
  `,
});
```

`VaryingType` supports `FLOAT`, `VEC2`–`VEC4`, `MAT2`–`MAT4`. No `INT`/`BOOL`/`SAMPLER` variants.

## Modes & lighting

**`CustomShaderMode`:**
- `MODIFY_MATERIAL` (default) — runs after the material stage, before lighting. `czm_modelMaterial` is populated with PBR/texture results; the shader refines them.
- `REPLACE_MATERIAL` — skips the material stage entirely. Shader sets every field procedurally. Cheaper when the source material is not needed.

**`LightingModel`:**
- `UNLIT` — skip lighting; `material.diffuse` becomes the final color (alpha still applied). Flat-shaded.
- `PBR` — physically-based with IBL when available.
- *Omitted* — preserves the model's default lighting. Omit unless overriding intentionally.

Pair `REPLACE_MATERIAL` + `UNLIT` for pure procedural flat shading (no material sampling, no lighting).

## Translucency

`CustomShaderTranslucencyMode` governs how alpha writes interact with the render pass:

- `INHERIT` (default) — alpha is only honored if the source material is translucent.
- `OPAQUE` — force opaque pass.
- `TRANSLUCENT` — force translucent pass.

**Pitfall:** writing `material.alpha` on an opaque model with `INHERIT` silently does nothing. Set `translucencyMode: CustomShaderTranslucencyMode.TRANSLUCENT` to make alpha writes effective. See `examples/04-translucent-override.js`.

## Attributes

`vsInput.attributes` and `fsInput.attributes` expose glTF vertex attributes. Names are case-sensitive and coordinate-space suffixes are required — the constructor rejects bare `position`/`normal`/`tangent`/`bitangent`.

Common fields (full table in `REFERENCE.md`):
- `positionMC` — model coords, valid in VS and FS
- `positionWC` — world (ECEF) coords, **fragment only**, low-precision
- `positionEC` — eye coords, **fragment only**
- `normalMC` / `normalEC` — vertex / fragment
- `tangentMC` / `tangentEC`, `bitangentMC` / `bitangentEC`
- `texCoord_N`, `color_N`, `joints_N`, `weights_N`

> **Coordinate-space validation.** The constructor scans shader text and throws `DeveloperError("<name> is not available in the <stage> shader. Did you mean <alt> instead?")` for invalid combinations. Examples: `positionEC` in vertex, `normalMC` in fragment.

Custom underscore-prefixed glTF attributes (`_FEATURE_ID_0`, `_SURFACE_TEMP`) are lowercased and un-prefixed: `fsInput.attributes.surface_temp`.

## FeatureIds

`vsInput.featureIds` / `fsInput.featureIds` unify three glTF sources into one struct:

- `featureId_N` — feature ID attributes and implicit attributes from `EXT_mesh_features` (N is the array index in the primitive's `featureIds` array). Also covers feature ID **textures**, which are fragment-shader-only.
- `instanceFeatureId_N` — per-instance feature IDs from `EXT_instance_features` + `EXT_mesh_gpu_instancing`.
- Named aliases — if glTF specifies `"label": "perVertex"`, then `featureIds.perVertex` is also available.
- Legacy 3D Tiles 1.0 `BATCH_ID` / `_BATCHID` → transparently renamed to `featureId_0`.

GLSL type is always `int`. WebGL 1 loses precision above 2^24.

```glsl
void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
  int id = fsInput.featureIds.featureId_0;
  if (id == 0)      material.diffuse = vec3(1.0, 0.2, 0.2);  // roof
  else if (id == 1) material.diffuse = vec3(0.2, 0.8, 0.2);  // wall
}
```

See `examples/03-feature-id-tileset.js`.

## Metadata

`EXT_structural_metadata` surfaces three source types (all addressable from shaders as of 1.139):

- **Property attributes** — per-vertex. Vertex and fragment shaders.
- **Property textures** — per-texel. **Fragment only.**
- **Property tables** — per-feature, keyed by feature ID. **Added in 1.139 (#13124).**

```glsl
void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
  float t = fsInput.metadata.temperature;
  float tMin = fsInput.metadataStatistics.temperature.minValue;
  float tMax = fsInput.metadataStatistics.temperature.maxValue;
  float v = (t - tMin) / (tMax - tMin);
  material.diffuse = vec3(v, 0.0, 1.0 - v);
}
```

**Property ID sanitization** (GLSL identifier rules):
- Non-alphanumeric runs → single `_` (`temperature ℃` → `temperature_`)
- Leading `gl_` stripped (`gl_custom` → `custom`)
- Leading digit prefixed with `_` (`12345` → `_12345`)
- Post-sanitization collisions → undefined behavior

**Sibling structs:** `metadataClass.<prop>.noData | defaultValue | minValue | maxValue` (class-schema bounds) and `metadataStatistics.<prop>.minValue | maxValue | mean | median | standardDeviation | variance | sum` (populated only when `tileset.json` declares `statistics`).

> **1.139 breaking change (#13135):** unsigned integer metadata is no longer cast to signed int. Assigning a `UINT` property to a GLSL `int` (`int x = fsInput.metadata.myUint;`) no longer compiles. Use the matching unsigned type.

**Public assets without `EXT_structural_metadata` on a `.glb` are scarce** — most real-world metadata lives on 3D Tiles. See `examples/06-metadata-ramp.js` (Cesium3DTileset target).

## czm_modelVertexOutput & czm_modelMaterial

**`czm_modelVertexOutput`** (vertex shader's `inout vsOutput`):
```glsl
struct czm_modelVertexOutput {
  vec3 positionMC;    // initialized to vsInput.attributes.positionMC
  float pointSize;    // overrides gl_PointSize and Cesium3DTileStyle point sizing
};
```

> **Gotcha:** mutating `positionMC` displaces vertices but does **not** update the primitive's bounding sphere. Heavily displaced vertices can be frustum-culled.

**`czm_modelMaterial`** (fragment shader's `inout material`). All colors are linear RGB. Conditional fields `specularWeight` / `anisotropic*` / `clearcoatFactor`... appear only when `KHR_materials_specular` / `_anisotropy` / `_clearcoat` is active on the primitive (see `REFERENCE.md` for the full `#ifdef`-guarded struct):

```glsl
struct czm_modelMaterial {
  vec4 baseColor; vec3 diffuse; float alpha;
  vec3 specular;  float roughness;
  vec3 normalEC;  float occlusion;  vec3 emissive;
  // + conditional PBR extension fields
};
```

## Built-in `czm_*` automatic uniforms

Available without declaration. Most useful for CustomShader: `czm_frameNumber`, `czm_pi`, `czm_model`, `czm_view`, `czm_projection`, `czm_modelView`, `czm_normal`, `czm_lightDirectionEC`, `czm_sunDirectionWC`, `czm_eyeHeight`, `czm_sceneMode`, `czm_viewerPositionWC`, `czm_splitPosition`. Full catalog in `REFERENCE.md`.

## VoxelPrimitive shader subset

Fragment-only. Executes at every raymarching step along the view ray; the final pixel composites all steps. Supplying `vertexShaderText` is silently ignored.

Reduced struct availability:
- `fsInput.attributes` — only `positionEC` and `normalEC`.
- `fsInput.featureIds` — **not present**.
- `fsInput.metadata` — fully supported.
- `fsInput.metadataClass` — **not present**.
- `fsInput.metadataStatistics` — only `minValue` and `maxValue`.

Assigning `customShader = undefined` falls back to `VoxelPrimitive.DefaultCustomShader`. See `examples/07-voxel-shader.js`. For `VoxelPrimitive` setup (provider, shape, modelMatrix, nearestSampling), see `cesiumjs-3d-tiles`.

> **1.130 breaking change (#12636):** `fsInput.voxel.positionUv | positionShapeUv | positionLocal` were removed. Use `fsInput.attributes.positionEC` instead. `fsInput.voxel.surfaceNormal` → `fsInput.attributes.normalEC`.

## Common patterns

| File | Target | Demonstrates |
|---|---|---|
| `examples/01-diffuse-tint.js` | Model | Time uniform driving `material.diffuse` |
| `examples/02-texture-swap.js` | Model | `TextureUniform`, `SAMPLER_2D`, `setUniform` |
| `examples/03-feature-id-tileset.js` | Cesium3DTileset | `fsInput.featureIds.featureId_0` classification coloring |
| `examples/04-translucent-override.js` | Model (opaque source) | `CustomShaderTranslucencyMode.TRANSLUCENT` |
| `examples/05-vertex-displacement.js` | Model | `vsOutput.positionMC` + normal offset |
| `examples/06-metadata-ramp.js` | Cesium3DTileset | `fsInput.metadata.<prop>` + `metadataStatistics` normalization |
| `examples/07-voxel-shader.js` | VoxelPrimitive | FS-only subset, per-voxel metadata |

## CesiumJS 1.139 version notes

Verbatim from upstream `CHANGES.md`:

**Breaking (1.139, #13135):**
> Custom Shaders that rely on metadata derived from the `EXT_structural_metadata` extension no longer cast unsigned integer metadata types to signed integers. Any existing custom shaders that assign UINT-type metadata to local integers (e.g. `int myMetadata = vsInput.metadata.myUintMetadata`) will no longer compile.

**Breaking (1.139, #13170):** Fixed precision of point cloud attributes when accessed in a custom fragment shader.

**Addition (1.139, #13124):** Access to metadata from property tables (previously only attributes/textures).

**Addition (1.139, #13135):** More metadata types via property textures.

**Fix (1.139, #13231):** Metadata variable regex extended to `metadataClass` and `metadataStatistics`.

**Fix (1.139.1, #13247):** NGA-GPM local extension + custom shader regression fix.

**Breaking (1.130, #12636):** Voxel `FragmentInput` restructured (see VoxelPrimitive section).

**Looking ahead (1.140):** #13258 stops disabling custom shaders on primitives with missing metadata when the class definition carries the property; #13323 adds limited double-precision metadata support via downcasting. Neither is available in 1.139.

## Gotchas & pitfalls

1. **Coordinate-space suffix required.** `positionEC` in vertex, `normalMC` in fragment, or any bare `position`/`normal`/`tangent`/`bitangent` throws `DeveloperError` at construction with a suggested alternative.
2. **`positionMC` is valid in fragment shader** — despite the `MC` suffix. Only `normalMC`/`tangentMC`/`bitangentMC` are FS-rejected.
3. **Vertex displacement does not update bounding sphere.** Displaced vertices may be frustum-culled unexpectedly.
4. **`Cesium3DTileStyle` + CustomShader = undefined behavior.** Per upstream JSDoc. Choose one per tileset.
5. **`SAMPLER_CUBE` rejected at construction.** Use `SAMPLER_2D` only.
6. **Parameter-name contract.** `vsInput`, `vsOutput`, `fsInput`, `material` are scanned by regex — renaming breaks codegen.
7. **`TextureUniform` URL-vs-typedArray XOR.** Supplying both or neither throws. `typedArray` requires `width` + `height`.
8. **Alpha writes on opaque models are silently ignored under `INHERIT`.** Set `translucencyMode: TRANSLUCENT`.
9. **`customShader.destroy()` required.** Call when disposing of a shader that holds texture uniforms — otherwise its `TextureManager` leaks GPU resources.
10. **`vsOutput.pointSize` overrides `Cesium3DTileStyle` point sizing.** Don't set it unless intended.
11. **Metadata property IDs are sanitized.** Non-alphanumeric → `_`; leading `gl_` stripped; collisions are undefined behavior.
12. **UINT metadata now preserves signedness (1.139+, #13135).** Use `uint x = fsInput.metadata.prop;`, not `int x = ...`.
13. **`customShader` on `Cesium3DTileset` is `@experimental`.** May change without Cesium's standard deprecation policy.
14. **Tilesets: only `Model`-backed tile content uses CustomShader.** Native I3S and other formats are unaffected.

## Performance tips

- `REPLACE_MATERIAL` skips the material stage (textures, PBR inputs not sampled).
- `LightingModel.UNLIT` skips lighting math — combine with `REPLACE_MATERIAL` for flat procedural shading.
- Write to varyings in vertex rather than recomputing per-fragment.
- Avoid per-frame `setUniform` of `SAMPLER_2D` — it triggers async texture reload. Use `url` once and hold the reference.
- Call `customShader.destroy()` on teardown to release GPU texture resources.

## See also

- **`REFERENCE.md`** — full struct tables (`Attributes`, `FeatureIds`, `Metadata`/`Class`/`Statistics`), enum value tables, built-in `czm_*` uniform catalog, coordinate-space validation error reference.
- **`examples/`** — seven compile-tested snippets. `examples/_sandcastle-template.html` is the internal scaffold; `examples/README.md` documents the layout.
- **`cesiumjs-materials-shaders`** — Fabric `Material`, `ImageBasedLighting`, `PostProcessStage`.
- **`cesiumjs-3d-tiles`** — `Cesium3DTileStyle`, `Cesium3DTileset` setup, `VoxelPrimitive` instantiation.
- **`cesiumjs-models-particles`** — `Model.fromGltfAsync`, `ModelFeature.getProperty()`, animations.
- **`cesiumjs-primitives`** — Fabric on Appearances for classic Primitive geometry.
- **CesiumJS Custom Shader Guide** — `Documentation/CustomShaderGuide/README.md` on `CesiumGS/cesium` `main`.
