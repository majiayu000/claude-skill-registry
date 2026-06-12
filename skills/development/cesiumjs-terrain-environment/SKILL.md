---
name: cesiumjs-terrain-environment
description: "CesiumJS terrain, globe, and environment - TerrainProvider, Globe, sampleTerrain, atmosphere, sky, fog, lighting, shadows, panoramas. Use when configuring terrain providers, querying terrain heights, customizing atmosphere or sky rendering, adding panoramas, or adjusting scene lighting and shadows."
---
# CesiumJS Terrain, Globe & Environment

Version baseline: CesiumJS v1.139 | ES module imports (`import { ... } from "cesium";`)

## Terrain Providers

Terrain is served through `TerrainProvider` implementations. Use async factory methods
(`fromIonAssetId`, `fromUrl`), not the constructor directly.

### Cesium Ion World Terrain

```js
import { Viewer, Terrain } from "cesium";

const viewer = new Viewer("cesiumContainer", {
  terrain: Terrain.fromWorldTerrain({
    requestVertexNormals: true, // smoother lighting
    requestWaterMask: true,     // ocean water effect
  }),
});
```

### CesiumTerrainProvider from Ion Asset / URL

```js
import { CesiumTerrainProvider } from "cesium";

// By Ion asset ID (e.g. 3956 = Arctic DEM)
const tp = await CesiumTerrainProvider.fromIonAssetId(3956, {
  requestVertexNormals: true,
});
viewer.scene.globe.terrainProvider = tp;

// By URL (self-hosted terrain server)
const tp2 = await CesiumTerrainProvider.fromUrl(
  "https://my-server.example.com/terrain",
  { requestVertexNormals: true },
);
```

### EllipsoidTerrainProvider (Flat Globe)

```js
import { EllipsoidTerrainProvider } from "cesium";
// Flat ellipsoid -- no terrain data, useful for 2D/Columbus or testing
viewer.scene.globe.terrainProvider = new EllipsoidTerrainProvider();
```

### CustomHeightmapTerrainProvider (Procedural)

```js
import { CustomHeightmapTerrainProvider } from "cesium";

viewer.scene.globe.terrainProvider = new CustomHeightmapTerrainProvider({
  width: 32,
  height: 32,
  callback: function (x, y, level) {
    const buf = new Float32Array(32 * 32);
    for (let r = 0; r < 32; r++) {
      for (let c = 0; c < 32; c++) {
        buf[r * 32 + c] = Math.sin((x + c / 32) * 6.28) * 5000;
      }
    }
    return buf;
  },
});
```

## Sampling Terrain Heights

Both functions mutate the input `Cartographic[]` in place (setting `.height`) and
return a promise resolving to the same array.

```js
import { sampleTerrain, sampleTerrainMostDetailed, Cartographic } from "cesium";

const positions = [
  Cartographic.fromDegrees(86.925145, 27.988257), // Mt Everest
  Cartographic.fromDegrees(87.0, 28.0),
];

// Fixed LOD level -- fast, approximate
await sampleTerrain(viewer.scene.globe.terrainProvider, 11, positions);

// Max available LOD -- slower, most precise
// Requires provider.availability (e.g. CesiumTerrainProvider)
await sampleTerrainMostDetailed(viewer.scene.globe.terrainProvider, positions);
// positions[0].height is now populated

// Pass true as 3rd arg to reject on tile failure instead of undefined heights
await sampleTerrainMostDetailed(provider, positions, true);
```

## Globe Configuration

Access via `viewer.scene.globe`. Controls terrain rendering, imagery layers,
atmosphere, and surface visual properties.

```js
const globe = viewer.scene.globe;

globe.show = true;
globe.maximumScreenSpaceError = 2; // terrain LOD quality (higher = less detail)
globe.tileCacheSize = 100;         // tiles kept in memory

// Lighting
globe.enableLighting = true;
globe.dynamicAtmosphereLighting = true;
globe.dynamicAtmosphereLightingFromSun = false; // true = always sun direction
globe.lambertDiffuseMultiplier = 0.9;

// Atmosphere
globe.showGroundAtmosphere = true; // horizon glow (default true for WGS84)
globe.atmosphereHueShift = 0.0;
globe.atmosphereSaturationShift = 0.0;
globe.atmosphereBrightnessShift = 0.0;

// Surface behavior
globe.depthTestAgainstTerrain = false; // true = z-test entities vs terrain
globe.showWaterEffect = true;          // animated ocean (needs water mask)
globe.shadows = Cesium.ShadowMode.RECEIVE_ONLY;
globe.baseColor = Cesium.Color.BLUE;   // color when no imagery loaded
globe.backFaceCulling = true;
globe.showSkirts = true;
```

### Globe.pick and Globe.getHeight

```js
// Raycast to globe surface
const ray = viewer.camera.getPickRay(windowPosition);
const hit = viewer.scene.globe.pick(ray, viewer.scene);

// Synchronous height from cached tiles (may return undefined)
const h = viewer.scene.globe.getHeight(Cesium.Cartographic.fromDegrees(-105, 40));
```

### Terrain Exaggeration

```js
// Set on Scene, not Globe
viewer.scene.verticalExaggeration = 2.0;
viewer.scene.verticalExaggerationRelativeHeight = 0.0; // relative to sea level
```

## Globe Translucency

Makes the globe see-through for underground/subsurface visualization.

```js
const globe = viewer.scene.globe;
globe.translucency.enabled = true;
globe.translucency.frontFaceAlpha = 0.5;
globe.translucency.backFaceAlpha = 1.0;

// Distance-based alpha
globe.translucency.frontFaceAlphaByDistance = new Cesium.NearFarScalar(
  1.5e2, 0.5,  // near: 150m, alpha 0.5
  8.0e6, 1.0,  // far: 8000km, alpha 1.0
);

// Limit to geographic region
globe.translucency.rectangle = Cesium.Rectangle.fromDegrees(-120, 30, -80, 50);
```

## Elevation Band Material

Color the globe surface by elevation.

```js
import { createElevationBandMaterial, Color } from "cesium";

viewer.scene.globe.material = createElevationBandMaterial({
  scene: viewer.scene,
  layers: [{
    entries: [
      { height: 0,    color: new Color(0.0, 0.0, 0.5, 1.0) },
      { height: 500,  color: new Color(0.0, 0.8, 0.0, 1.0) },
      { height: 2000, color: new Color(0.6, 0.3, 0.1, 1.0) },
      { height: 5000, color: Color.WHITE },
    ],
  }],
});
```

## SkyAtmosphere

Atmospheric haze ring around the globe limb. 3D mode only.

```js
const sky = viewer.scene.skyAtmosphere;
sky.show = true;
sky.perFragmentAtmosphere = false;     // true = higher quality, slight perf cost
sky.atmosphereLightIntensity = 50.0;
sky.hueShift = 0.0;                    // 0..1
sky.saturationShift = 0.0;             // -1..1
sky.brightnessShift = 0.0;             // -1..1
// Scattering coefficients (advanced tuning)
sky.atmosphereRayleighCoefficient = new Cesium.Cartesian3(5.5e-6, 13.0e-6, 28.4e-6);
sky.atmosphereMieCoefficient = new Cesium.Cartesian3(21e-6, 21e-6, 21e-6);
sky.atmosphereMieAnisotropy = 0.9;
```

## SkyBox

Star field cube map behind the globe. 3D mode only.

```js
import { SkyBox } from "cesium";

viewer.scene.skyBox = SkyBox.createEarthSkyBox(); // default stars

viewer.scene.skyBox = new SkyBox({
  sources: {
    positiveX: "skybox_px.png", negativeX: "skybox_nx.png",
    positiveY: "skybox_py.png", negativeY: "skybox_ny.png",
    positiveZ: "skybox_pz.png", negativeZ: "skybox_nz.png",
  },
});
```

## Fog

Blends distant terrain toward atmosphere color and culls far tiles. 3D mode only.

```js
const fog = viewer.scene.fog;
fog.enabled = true;
fog.renderable = true;          // false = cull tiles but skip visual fog
fog.density = 0.0006;           // higher = thicker fog, more culling
fog.visualDensityScalar = 0.15; // visual-only multiplier
fog.maxHeight = 800000.0;       // fog disabled above this altitude (m)
fog.heightFalloff = 0.59;       // exponential falloff (must be >0)
fog.screenSpaceErrorFactor = 2.0;
fog.minimumBrightness = 0.03;   // prevents completely black fog
```

## Sun and Moon

```js
viewer.scene.sun = new Cesium.Sun();
viewer.scene.sun.show = true;
viewer.scene.moon.show = true; // follows real lunar ephemeris
```

## Lighting

`scene.light` controls the scene light source. Default is `SunLight` (follows clock).

```js
import { SunLight, DirectionalLight, Cartesian3, Color } from "cesium";

// SunLight -- follows the Sun position based on scene clock
viewer.scene.light = new SunLight({ color: Color.WHITE, intensity: 2.0 });

// DirectionalLight -- fixed direction for studio-style lighting
viewer.scene.light = new DirectionalLight({
  direction: new Cartesian3(0.2, -0.5, -0.8), // must be non-zero
  color: Color.WHITE,
  intensity: 1.5,
});

viewer.scene.globe.enableLighting = true; // required for light to affect terrain
```

`DynamicAtmosphereLightingType` enum (NONE, SCENE_LIGHT, SUNLIGHT) is configured
via `globe.enableLighting`, `globe.dynamicAtmosphereLighting`, and
`globe.dynamicAtmosphereLightingFromSun` flags.

## Shadows

Cascaded shadow maps from the scene light source.

```js
viewer.shadows = true;
const sm = viewer.shadowMap;
sm.maximumDistance = 5000.0; // cascade range (meters)
sm.softShadows = true;      // PCF for softer edges
sm.darkness = 0.3;           // 0 = invisible, 1 = black
sm.fadingEnabled = true;     // fade near horizon

viewer.scene.globe.shadows = Cesium.ShadowMode.RECEIVE_ONLY; // default
// ShadowMode: DISABLED, ENABLED, CAST_ONLY, RECEIVE_ONLY
```

## Panoramas (v1.139+)

360-degree imagery at a scene location. Two formats: equirectangular and cube map.

### EquirectangularPanorama

```js
import {
  EquirectangularPanorama, Cartesian3,
  HeadingPitchRoll, Transforms, Math as CesiumMath,
} from "cesium";

const position = Cartesian3.fromDegrees(-75.17, 39.95, 100.0);
const hpr = new HeadingPitchRoll(CesiumMath.toRadians(45), 0, 0);
const transform = Transforms.headingPitchRollToFixedFrame(position, hpr);

viewer.scene.primitives.add(new EquirectangularPanorama({
  transform,
  image: "path/to/equirectangular-360.jpg",
  radius: 100000.0,
}));
```

### CubeMapPanorama

```js
import { CubeMapPanorama, Cartesian3, Transforms, Matrix3, Matrix4 } from "cesium";

const pos = Cartesian3.fromDegrees(-122.42, 37.77, 10.0);
const northDown = Transforms.localFrameToFixedFrameGenerator("north", "down");
const xform = Matrix4.getMatrix3(northDown(pos), new Matrix3());

viewer.scene.primitives.add(new CubeMapPanorama({
  sources: {
    positiveX: "px.jpg", negativeX: "nx.jpg",
    positiveY: "py.jpg", negativeY: "ny.jpg",
    positiveZ: "pz.jpg", negativeZ: "nz.jpg",
  },
  transform: xform,
}));
```

### GoogleStreetViewCubeMapPanoramaProvider

```js
import { GoogleStreetViewCubeMapPanoramaProvider, Cartographic } from "cesium";

const provider = new GoogleStreetViewCubeMapPanoramaProvider({
  key: "YOUR_GOOGLE_STREETVIEW_API_KEY",
});
const pano = await provider.loadPanorama({
  cartographic: Cartographic.fromDegrees(-122.42, 37.77, 0),
});
viewer.scene.primitives.add(pano);
```

## Terrain Provider Events

```js
viewer.scene.globe.terrainProviderChanged.addEventListener((newProvider) => {
  console.log("Terrain changed:", newProvider.constructor.name);
});
```

## Performance Tips

1. **Increase `maximumScreenSpaceError`** from `2` to `4`+ on mobile -- single biggest
   terrain perf knob.
2. **Keep fog enabled** (default) -- culls distant tiles, reducing draw calls.
3. **Avoid per-frame `verticalExaggeration` changes** -- forces terrain tile reloads.
4. **Set `requestVertexNormals: true` only when lighting is enabled** -- doubles tile size.
5. **Skip `requestWaterMask`** (default false) when `showWaterEffect` is off.
6. **Prefer `sampleTerrain` over `sampleTerrainMostDetailed`** when approximate heights
   suffice -- resolves faster with fewer tile requests.
7. **Batch terrain sampling** -- pass all positions in one array to share tile loads.
8. **Tune `tileCacheSize`** -- increase for zoom-heavy workflows, decrease for memory.
9. **Disable `showGroundAtmosphere`** on non-Earth ellipsoids to avoid artifacts.
10. **Keep `depthTestAgainstTerrain = false`** (default) to avoid z-fighting with
    labels and billboards near the surface.

## Quick Reference

| Class / Function | Purpose |
|---|---|
| `CesiumTerrainProvider.fromIonAssetId(id, opts)` | Ion terrain asset |
| `CesiumTerrainProvider.fromUrl(url, opts)` | Self-hosted terrain |
| `EllipsoidTerrainProvider` | Flat ellipsoid (no terrain) |
| `CustomHeightmapTerrainProvider` | Procedural/callback terrain |
| `ArcGISTiledElevationTerrainProvider` | ArcGIS elevation service |
| `sampleTerrain(provider, level, positions)` | Heights at fixed LOD |
| `sampleTerrainMostDetailed(provider, positions)` | Heights at max LOD |
| `Globe` | Surface rendering, terrain, atmosphere |
| `GlobeTranslucency` | See-through globe for underground views |
| `createElevationBandMaterial` | Color surface by elevation |
| `SkyAtmosphere` | Atmospheric limb glow |
| `SkyBox` / `SkyBox.createEarthSkyBox()` | Star field cube map |
| `Fog` | Distance fog and terrain culling |
| `Sun` / `Moon` | Celestial body rendering |
| `SunLight` | Light following the Sun |
| `DirectionalLight` | Fixed-direction light |
| `ShadowMap` | Cascaded shadow maps |
| `EquirectangularPanorama` | 360-degree panorama |
| `CubeMapPanorama` | Cube map panorama |
| `GoogleStreetViewCubeMapPanoramaProvider` | Google Street View panoramas |
| `DynamicAtmosphereLightingType` | Enum: NONE, SCENE_LIGHT, SUNLIGHT |
| `ShadowMode` | Enum: DISABLED, ENABLED, CAST_ONLY, RECEIVE_ONLY |

## See Also

- **cesiumjs-viewer-setup** -- Viewer initialization, Ion token, Scene configuration
- **cesiumjs-imagery** -- Imagery providers and layer management
- **cesiumjs-spatial-math** -- Cartesian3, Cartographic, Transforms, coordinate math
