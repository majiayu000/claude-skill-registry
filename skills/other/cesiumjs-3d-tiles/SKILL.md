---
name: cesiumjs-3d-tiles
description: "CesiumJS 3D Tiles - Cesium3DTileset, styling, metadata, feature picking, voxels, point clouds, I3S, Gaussian splats, clipping planes and polygons. Use when loading 3D Tiles tilesets, styling building features, querying metadata properties, working with voxels or point clouds, or clipping spatial data."
---
# CesiumJS 3D Tiles

Version baseline: CesiumJS v1.139 (ES module imports, async factory methods).

## Loading a Tileset

Always use async factory methods -- never call the constructor directly.

```js
import { Cesium3DTileset, HeadingPitchRange, Math as CesiumMath } from "cesium";

// From a URL
const tileset = await Cesium3DTileset.fromUrl(
  "https://example.com/tileset.json",
  { maximumScreenSpaceError: 16 }, // lower = higher quality
);
viewer.scene.primitives.add(tileset);
viewer.zoomTo(tileset, new HeadingPitchRange(
  0.0, CesiumMath.toRadians(-25.0), tileset.boundingSphere.radius * 2.0,
));
```

```js
// From Cesium ion
const tileset = await Cesium3DTileset.fromIonAssetId(75343);
viewer.scene.primitives.add(tileset);
```

```js
// Google Photorealistic 3D Tiles
import { createGooglePhotorealistic3DTileset } from "cesium";
const google3D = await createGooglePhotorealistic3DTileset({
  onlyUsingWithGoogleGeocoder: true,
});
viewer.scene.primitives.add(google3D);
```

```js
// OSM Buildings
import { createOsmBuildingsAsync } from "cesium";
const osmBuildings = await createOsmBuildingsAsync();
viewer.scene.primitives.add(osmBuildings);
```

## Key Constructor Options

| Option | Default | Purpose |
|--------|---------|---------|
| `maximumScreenSpaceError` | 16 | LOD quality threshold (pixels) |
| `cacheBytes` | 536870912 | Tile cache trim target (bytes) |
| `maximumCacheOverflowBytes` | 536870912 | Extra cache headroom |
| `shadows` | ShadowMode.ENABLED | Shadow casting/receiving |
| `modelMatrix` | Matrix4.IDENTITY | Root transform |
| `clippingPlanes` | undefined | ClippingPlaneCollection |
| `clippingPolygons` | undefined | ClippingPolygonCollection (WebGL 2) |
| `enableCollision` | false | Camera collision with tileset surface |
| `pointCloudShading` | undefined | Point attenuation options object |
| `classificationType` | undefined | TERRAIN, CESIUM_3D_TILE, or BOTH |
| `dynamicScreenSpaceError` | true | Horizon LOD optimization |
| `foveatedScreenSpaceError` | true | Center-screen tile priority |
| `preloadFlightDestinations` | true | Prefetch tiles at flight target |
| `featureIdLabel` | "featureId_0" | EXT_mesh_features ID set label |
| `backFaceCulling` | true | Cull back faces per glTF material |

## Tileset Events

```js
tileset.loadProgress.addEventListener((pending, processing) => {
  if (pending === 0 && processing === 0) console.log("Loaded");
});
tileset.initialTilesLoaded.addEventListener(() => { /* first view ready */ });
tileset.allTilesLoaded.addEventListener(() => { /* all visible tiles ready */ });
tileset.tileLoad.addEventListener((tile) => { /* tile content loaded */ });
tileset.tileUnload.addEventListener((tile) => { /* tile evicted from cache */ });
tileset.tileFailed.addEventListener(({ url, message }) => {
  console.error(`Tile ${url}: ${message}`);
});
// Per-frame manual styling
tileset.tileVisible.addEventListener((tile) => {
  const content = tile.content;
  for (let i = 0; i < content.featuresLength; i++) {
    content.getFeature(i).color = Cesium.Color.fromRandom();
  }
});
```

## Runtime Properties

```js
tileset.show = false;                     // toggle visibility
tileset.maximumScreenSpaceError = 8;      // increase quality
const { center, radius } = tileset.boundingSphere;

import { Matrix4, Cartesian3 } from "cesium";
tileset.modelMatrix = Matrix4.fromTranslation(new Cartesian3(0, 0, 100));
```

## Declarative Styling

Assign a `Cesium3DTileStyle` to `tileset.style`. Expressions reference feature
properties with `${PropertyName}`.

```js
import { Cesium3DTileStyle } from "cesium";

// Color by height conditions
tileset.style = new Cesium3DTileStyle({
  color: {
    conditions: [
      ["${Height} >= 100", "color('purple', 0.5)"],
      ["${Height} >= 50",  "color('red')"],
      ["true",             "color('blue')"],
    ],
  },
  show: "${Height} > 0",
});
```

```js
// Use defines to simplify repeated sub-expressions
tileset.style = new Cesium3DTileStyle({
  defines: { material: "${feature['building:material']}" },
  color: {
    conditions: [
      ["${material} === null",    "color('white')"],
      ["${material} === 'glass'", "color('skyblue', 0.5)"],
      ["${material} === 'brick'", "color('indianred')"],
      ["true",                    "color('white')"],
    ],
  },
});
```

```js
// Show/hide by property
tileset.style = new Cesium3DTileStyle({
  show: "${feature['building']} === 'office'",
});
```

```js
// Point cloud styling
tileset.style = new Cesium3DTileStyle({
  color: "vec4(${Temperature})",
  pointSize: "${Temperature} * 2.0",
});
```

```js
tileset.style = undefined; // reset to default appearance
```

### Color Blend Modes

```js
import { Cesium3DTileColorBlendMode } from "cesium";
tileset.colorBlendMode = Cesium3DTileColorBlendMode.REPLACE; // HIGHLIGHT | REPLACE | MIX
tileset.colorBlendAmount = 0.5; // only used with MIX
```

## Feature Picking and Properties

`Scene.pick` returns `Cesium3DTileFeature` for 3D Tiles features. Modifications
persist until the owning tile is evicted from the cache.

```js
import {
  ScreenSpaceEventHandler, ScreenSpaceEventType,
  Cesium3DTileFeature, Color,
} from "cesium";

const handler = new ScreenSpaceEventHandler(viewer.scene.canvas);

// Hover: read properties
handler.setInputAction((movement) => {
  const feature = viewer.scene.pick(movement.endPosition);
  if (feature instanceof Cesium3DTileFeature) {
    const ids = feature.getPropertyIds();
    for (const id of ids) console.log(`${id}: ${feature.getProperty(id)}`);
    feature.color = Color.YELLOW; // highlight
  }
}, ScreenSpaceEventType.MOUSE_MOVE);

// Click: inspect a single property
handler.setInputAction((movement) => {
  const feature = viewer.scene.pick(movement.position);
  if (feature instanceof Cesium3DTileFeature) {
    console.log("Height:", feature.getProperty("Height"));
    feature.setProperty("selected", true); // write custom property
    feature.show = false;                  // hide individual feature
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

### Inherited Metadata (3D Tiles 1.1 / EXT_structural_metadata)

```js
// Searches: batch table -> content -> tile -> subtree -> group -> tileset
const value = feature.getPropertyInherited("semanticOrPropertyName");
```

## Clipping Planes

`ClippingPlaneCollection` clips via half-space planes in the tileset's local
coordinate system.

```js
import {
  ClippingPlane, ClippingPlaneCollection,
  Cartesian3, Color, Matrix4,
} from "cesium";

const clippingPlanes = new ClippingPlaneCollection({
  planes: [new ClippingPlane(new Cartesian3(0.0, 0.0, -1.0), 0.0)],
  edgeWidth: 1.0,
  edgeColor: Color.WHITE,
  unionClippingRegions: false, // false = intersection (AND); true = union (OR)
});

const tileset = await Cesium3DTileset.fromUrl(url, { clippingPlanes });
// Or: tileset.clippingPlanes = clippingPlanes;

// Offset the clip boundary at runtime
clippingPlanes.modelMatrix = Matrix4.fromTranslation(new Cartesian3(0, 0, 50));
clippingPlanes.get(0).distance = 25.0;
```

## Clipping Polygons

`ClippingPolygonCollection` clips using arbitrary polygons. **WebGL 2 only.**

```js
import { ClippingPolygon, ClippingPolygonCollection, Cartesian3 } from "cesium";

const polygon = new ClippingPolygon({
  positions: Cartesian3.fromDegreesArray([
    -105.0077, 39.7519, -105.0095, 39.7504,
    -105.0071, 39.7513, -105.0077, 39.7519,
  ]),
});

tileset.clippingPolygons = new ClippingPolygonCollection({
  polygons: [polygon],
  inverse: false, // false = clip inside polygon; true = clip outside
});

// Also works on the globe
viewer.scene.globe.clippingPolygons = new ClippingPolygonCollection({
  polygons: [polygon],
});
```

## Point Cloud Shading

```js
const tileset = await Cesium3DTileset.fromUrl(pointCloudUrl, {
  pointCloudShading: {
    attenuation: true,           // scale points by geometric error
    geometricErrorScale: 1.0,
    maximumAttenuation: 10,      // max pixel size; undefined = maximumScreenSpaceError
    eyeDomeLighting: true,       // depth-aware edge enhancement
    eyeDomeLightingStrength: 1.0,
    eyeDomeLightingRadius: 1.0,
    backFaceCulling: false,      // requires normals in point data
    normalShading: true,
  },
});
viewer.scene.primitives.add(tileset);

// Runtime adjustment
tileset.pointCloudShading.eyeDomeLightingStrength = 2.0;
```

## Voxel Primitives

`VoxelPrimitive` renders volumetric data from a `Cesium3DTilesVoxelProvider`.
Shapes: `BOX`, `CYLINDER`, `ELLIPSOID` (see `VoxelShapeType`).

```js
import { VoxelPrimitive, Cesium3DTilesVoxelProvider, CustomShader } from "cesium";

const provider = await Cesium3DTilesVoxelProvider.fromUrl("voxel/tileset.json");

const voxelPrimitive = new VoxelPrimitive({
  provider,
  customShader: new CustomShader({
    fragmentShaderText: `void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
      material.diffuse = fsInput.metadata.a.rgb;
      material.alpha = fsInput.metadata.a.a;
    }`,
  }),
});
viewer.scene.primitives.add(voxelPrimitive);
voxelPrimitive.nearestSampling = true;
viewer.camera.flyToBoundingSphere(voxelPrimitive.boundingSphere, { duration: 0 });

// For voxel shader authoring — struct availability, raymarching semantics, metadata
// access — see the cesiumjs-custom-shader skill. This skill covers VoxelPrimitive setup.

// Optional inspector widget
viewer.extend(Cesium.viewerVoxelInspectorMixin);
viewer.voxelInspector.viewModel.voxelPrimitive = voxelPrimitive;
```

## I3S Data Provider

Load Esri I3S scene layers (3D Objects, IntegratedMesh, Building Scene Layer).

```js
import { I3SDataProvider, ArcGISTiledElevationTerrainProvider, Ellipsoid, Rectangle } from "cesium";

const geoidService = await ArcGISTiledElevationTerrainProvider.fromUrl(
  "https://tiles.arcgis.com/tiles/.../EGM2008/ImageServer",
);
const i3sProvider = await I3SDataProvider.fromUrl(
  "https://tiles.arcgis.com/tiles/.../SceneServer/layers/0",
  { geoidTiledTerrainProvider: geoidService },
);
viewer.scene.primitives.add(i3sProvider);

const center = Rectangle.center(i3sProvider.extent);
center.height = 5000.0;
viewer.camera.setView({
  destination: Ellipsoid.WGS84.cartographicToCartesian(center),
});
```

## Gaussian Splats

Loaded as standard 3D Tiles; CesiumJS handles `KHR_gaussian_splatting` automatically.

```js
const splats = await Cesium3DTileset.fromIonAssetId(3667783);
viewer.scene.primitives.add(splats);
viewer.zoomTo(splats);
```

## Classification

Drape tileset geometry as a classification overlay on terrain or other tilesets.

```js
import { Cesium3DTileset, ClassificationType } from "cesium";
const classified = await Cesium3DTileset.fromUrl(url, {
  classificationType: ClassificationType.BOTH, // TERRAIN | CESIUM_3D_TILE | BOTH
});
viewer.scene.primitives.add(classified);
```

## Adjusting Tileset Height

```js
import { Cartographic, Cartesian3, Matrix4 } from "cesium";
const cartographic = Cartographic.fromCartesian(tileset.boundingSphere.center);
const surface = Cartesian3.fromRadians(cartographic.longitude, cartographic.latitude, 0.0);
const offset = Cartesian3.fromRadians(cartographic.longitude, cartographic.latitude, heightOffset);
const translation = Cartesian3.subtract(offset, surface, new Cartesian3());
tileset.modelMatrix = Matrix4.fromTranslation(translation);
```

## Performance Tips

1. Keep `maximumScreenSpaceError` as high as acceptable (16 default; 32+ for mobile).
2. Leave `dynamicScreenSpaceError: true` for street-level views with large tilesets.
3. Leave `foveatedScreenSpaceError: true` to prioritize center-screen tiles.
4. Size `cacheBytes` and `maximumCacheOverflowBytes` to device memory (512 MB each default).
5. Use `preloadFlightDestinations: true` to prefetch tiles at the camera flight target.
6. Enable `skipLevelOfDetail: true` for large replacement-refined tilesets to reduce memory.
7. Avoid `maximumScreenSpaceError` below 4 -- diminishing returns, many more tile requests.
8. For point clouds, enable `attenuation` and `eyeDomeLighting` to fill gaps and add depth.
9. Keep `enableCollision: false` unless camera collision or CLAMP_TO_GROUND on tiles is needed.
10. Preload hidden tilesets with `show: false` and `preloadWhenHidden: true`.
11. Avoid translucent styles when possible -- they add rendering passes and disable optimizations.
12. Listen to `tileFailed` to log errors; call `trimLoadedTiles()` after large camera jumps.

## See Also

- **cesiumjs-custom-shader** -- GLSL authoring for `Cesium3DTileset.customShader` and `VoxelPrimitive.customShader` (struct reference, feature IDs, metadata)
- **cesiumjs-materials-shaders** -- ImageBasedLighting, post-processing stages for tilesets
- **cesiumjs-interaction** -- Scene.pick, drillPick, ScreenSpaceEventHandler for feature selection
- **cesiumjs-terrain-environment** -- Globe, terrain providers, atmosphere, lighting, shadows
