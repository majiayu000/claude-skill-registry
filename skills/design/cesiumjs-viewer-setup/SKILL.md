---
name: cesiumjs-viewer-setup
description: "CesiumJS viewer setup - Viewer, CesiumWidget, widgets, Ion token, Scene configuration, SceneMode, factory helpers, geocoders, platform services. Use when initializing a CesiumJS application, configuring viewer widgets, setting Ion access tokens, creating default terrain or imagery, or bootstrapping a 3D globe."
---

# CesiumJS Viewer & Scene Setup

Reference for bootstrapping CesiumJS applications: Viewer, CesiumWidget, Ion/GoogleMaps/ITwinPlatform configuration, widgets, factory helpers, geocoder services, viewer mixins, Credits, and related enums.

## Quick Start

```js
import { Ion, Viewer, Terrain } from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";

// Always set your Ion token before any other Cesium calls
Ion.defaultAccessToken = "YOUR_CESIUM_ION_ACCESS_TOKEN";

const viewer = new Viewer("cesiumContainer", {
  terrain: Terrain.fromWorldTerrain(),
});
```

Required HTML: `<div id="cesiumContainer" style="width:100%;height:100vh"></div>`

## Ion & Platform Configuration

### Cesium Ion

```js
import { Ion } from "cesium";

Ion.defaultAccessToken = "YOUR_TOKEN";  // required for ion assets
Ion.defaultServer = "https://your-ion-server.example.com/"; // optional: self-hosted
```

### IonResource

```js
import { IonResource, Cesium3DTileset } from "cesium";

const resource = await IonResource.fromAssetId(96188);
const tileset = await Cesium3DTileset.fromUrl(resource);
viewer.scene.primitives.add(tileset);
```

### Google Maps Platform

```js
import { GoogleMaps, createGooglePhotorealistic3DTileset, Viewer, IonGeocodeProviderType } from "cesium";

GoogleMaps.defaultApiKey = "YOUR_GOOGLE_MAPS_API_KEY"; // optional: without key, served via ion

const viewer = new Viewer("cesiumContainer", {
  geocoder: IonGeocodeProviderType.GOOGLE, // required with Google 3D Tiles
});

const tileset = await createGooglePhotorealistic3DTileset({
  onlyUsingWithGoogleGeocoder: true,
});
viewer.scene.primitives.add(tileset);
```

### iTwin Platform (experimental)

```js
import { ITwinPlatform, ITwinData } from "cesium";

ITwinPlatform.defaultAccessToken = "YOUR_ITWIN_TOKEN";
const tileset = await ITwinData.createTilesetForIModel(viewer, "imodel-id");
```

## Viewer Constructor Options

`new Viewer(container, options?)` -- `container` is a DOM element or its string ID.

### Widget Toggles

| Option | Default | Purpose |
|--------|---------|---------|
| `animation` | `true` | Playback controls |
| `baseLayerPicker` | `true` | Imagery/terrain switcher |
| `fullscreenButton` | `true` | Fullscreen toggle |
| `vrButton` | `false` | WebVR toggle |
| `geocoder` | `IonGeocodeProviderType.DEFAULT` | Search bar (`false` to hide) |
| `homeButton` | `true` | Reset to home view |
| `infoBox` | `true` | Entity info popup |
| `sceneModePicker` | `true` | 2D/3D/Columbus toggle |
| `selectionIndicator` | `true` | Selection reticle |
| `timeline` | `true` | Time scrubber |
| `navigationHelpButton` | `true` | Mouse/touch help |
| `projectionPicker` | `false` | Perspective/ortho toggle |

### Scene & Rendering

| Option | Default | Purpose |
|--------|---------|---------|
| `sceneMode` | `SceneMode.SCENE3D` | Initial scene mode |
| `scene3DOnly` | `false` | Lock to 3D, saves GPU memory |
| `shadows` | `false` | Shadow casting |
| `terrainShadows` | `ShadowMode.RECEIVE_ONLY` | Terrain shadow mode |
| `requestRenderMode` | `false` | Render only on changes |
| `maximumRenderTimeChange` | `0.0` | Max sim-time delta for render |
| `msaaSamples` | `4` | MSAA (1 to disable) |
| `orderIndependentTranslucency` | `true` | Translucent ordering |
| `mapMode2D` | `MapMode2D.INFINITE_SCROLL` | 2D scroll behavior |

### Layers & Terrain

| Option | Default | Purpose |
|--------|---------|---------|
| `baseLayer` | `ImageryLayer.fromWorldImagery()` | Base imagery (`false` for none; needs `baseLayerPicker: false`) |
| `terrain` | none | Async terrain helper (cannot combine with `terrainProvider`) |
| `terrainProvider` | `EllipsoidTerrainProvider` | Sync terrain provider |
| `globe` | `new Globe()` | `false` for no globe (space scenes) |
| `skyBox` | auto (WGS84) | `false` disables sky/sun/moon |
| `skyAtmosphere` | auto (WGS84) | `false` disables limb glow |

### Minimal Viewer (No Widgets)

```js
import { Viewer, Ion, Terrain } from "cesium";
Ion.defaultAccessToken = "YOUR_TOKEN";

const viewer = new Viewer("cesiumContainer", {
  animation: false, baseLayerPicker: false, fullscreenButton: false,
  geocoder: false, homeButton: false, infoBox: false,
  sceneModePicker: false, selectionIndicator: false,
  timeline: false, navigationHelpButton: false,
  terrain: Terrain.fromWorldTerrain(),
});
```

## CesiumWidget (Lightweight Alternative)

No UI widgets, no Knockout dependency. Suitable for custom UIs or embedding.

```js
import { CesiumWidget, Ion } from "cesium";
Ion.defaultAccessToken = "YOUR_TOKEN";

const widget = new CesiumWidget("cesiumContainer", { shouldAnimate: true });
// Exposes: widget.scene, widget.camera, widget.entities
```

## SceneMode Enum

| Value | Description |
|-------|-------------|
| `SceneMode.SCENE3D` | Standard 3D globe (default) |
| `SceneMode.SCENE2D` | Top-down orthographic map |
| `SceneMode.COLUMBUS_VIEW` | 2.5D flat map with height |
| `SceneMode.MORPHING` | Transitioning between modes |

```js
import { Viewer, SceneMode } from "cesium";

const viewer = new Viewer("cesiumContainer", { sceneMode: SceneMode.SCENE2D });
viewer.scene.morphTo3D(2.0);          // animated transition
viewer.scene.morphToColumbusView(2.0);
```

## Scene Configuration

```js
const scene = viewer.scene;
scene.globe.depthTestAgainstTerrain = true; // entities interact with terrain
scene.globe.enableLighting = true;          // sun-based lighting

// Key sub-objects
scene.camera;           // Camera
scene.primitives;       // PrimitiveCollection
scene.groundPrimitives; // PrimitiveCollection (ground-clamped)
scene.imageryLayers;    // ImageryLayerCollection
scene.postProcessStages;

scene.requestRender();  // trigger frame in requestRenderMode
```

## Factory Helpers

### createOsmBuildingsAsync

```js
import { createOsmBuildingsAsync, Cesium3DTileStyle } from "cesium";

// Default styling (colors from OSM tags)
const tileset = await createOsmBuildingsAsync();
viewer.scene.primitives.add(tileset);

// Custom style
const styled = await createOsmBuildingsAsync({
  style: new Cesium3DTileStyle({
    color: { conditions: [
      ["${feature['building']} === 'hospital'", "color('#0000FF')"],
      [true, "color('#ffffff')"],
    ]},
  }),
});
```

### createGooglePhotorealistic3DTileset

```js
import { createGooglePhotorealistic3DTileset, IonGeocodeProviderType } from "cesium";

// Must use Google geocoder
const viewer = new Viewer("cesiumContainer", { geocoder: IonGeocodeProviderType.GOOGLE });
const tileset = await createGooglePhotorealistic3DTileset({ onlyUsingWithGoogleGeocoder: true });
viewer.scene.primitives.add(tileset);
```

### Terrain.fromWorldTerrain / fromWorldBathymetry

Preferred for the `terrain` constructor option. Non-blocking with error events.

```js
import { Viewer, Terrain } from "cesium";

// World terrain with normals and water
const viewer = new Viewer("cesiumContainer", {
  terrain: Terrain.fromWorldTerrain({ requestVertexNormals: true, requestWaterMask: true }),
});

// Bathymetry (ocean floor)
const viewer2 = new Viewer("cesiumContainer", {
  terrain: Terrain.fromWorldBathymetry({ requestVertexNormals: true }),
});
```

### Terrain Event Handling

```js
import { Terrain, CesiumTerrainProvider } from "cesium";

const terrain = new Terrain(CesiumTerrainProvider.fromUrl("https://my-terrain.example.com"));
viewer.scene.setTerrain(terrain);

terrain.readyEvent.addEventListener((provider) => {
  viewer.scene.globe.enableLighting = true;
});
terrain.errorEvent.addEventListener((error) => console.error("Terrain failed:", error));
```

### createWorldTerrainAsync / createWorldImageryAsync

Lower-level: return raw providers. Use when you need the provider directly.

```js
import { createWorldTerrainAsync, createWorldImageryAsync, IonWorldImageryStyle } from "cesium";

const terrainProvider = await createWorldTerrainAsync({ requestVertexNormals: true });
viewer.terrainProvider = terrainProvider;

const imageryProvider = await createWorldImageryAsync({ style: IonWorldImageryStyle.AERIAL_WITH_LABELS });
```

**IonWorldImageryStyle**: `AERIAL` (default) | `AERIAL_WITH_LABELS` | `ROAD`

## Geocoder Configuration

The `geocoder` option accepts `false`, an `IonGeocodeProviderType`, or a `GeocoderService[]`.

**IonGeocodeProviderType**: `DEFAULT` | `GOOGLE` (required with Google tiles) | `BING`

```js
import { Viewer, CartographicGeocoderService, IonGeocoderService, OpenCageGeocoderService } from "cesium";

// Multiple services (searched in order)
const viewer = new Viewer("cesiumContainer", {
  geocoder: [
    new CartographicGeocoderService(), // accepts "lat, lon" input
    new IonGeocoderService({ scene: viewer.scene }),
  ],
});
```

### Custom GeocoderService

```js
const myGeocoder = {
  async geocode(input, type) {
    // type: GeocodeType.SEARCH or GeocodeType.AUTOCOMPLETE
    const resp = await fetch(`https://api.example.com/search?q=${input}`);
    const data = await resp.json();
    return data.map((item) => ({
      displayName: item.name,
      destination: Cartesian3.fromDegrees(item.lon, item.lat),
    }));
  },
};
const viewer = new Viewer("cesiumContainer", { geocoder: [myGeocoder] });
```

## Viewer Mixins

```js
import { Viewer, viewerDragDropMixin, viewerCesium3DTilesInspectorMixin,
  viewerCesiumInspectorMixin, viewerPerformanceWatchdogMixin, viewerVoxelInspectorMixin } from "cesium";

const viewer = new Viewer("cesiumContainer");

// Drag-and-drop CZML/GeoJSON/KML loading
viewer.extend(viewerDragDropMixin, { dropTarget: "cesiumContainer", clearOnDrop: true });
viewer.dropError.addEventListener((handler, name, error) => console.error(error));

viewer.extend(viewerCesium3DTilesInspectorMixin);    // 3D Tiles debug panel
viewer.extend(viewerCesiumInspectorMixin);            // general scene inspector
viewer.extend(viewerPerformanceWatchdogMixin);        // low-FPS warning
viewer.extend(viewerVoxelInspectorMixin);             // voxel debug panel
```

## Key Viewer Properties & Methods

| Property | Type |
|----------|------|
| `viewer.scene` | `Scene` |
| `viewer.camera` | `Camera` |
| `viewer.entities` | `EntityCollection` |
| `viewer.dataSources` | `DataSourceCollection` |
| `viewer.imageryLayers` | `ImageryLayerCollection` |
| `viewer.terrainProvider` | `TerrainProvider` |
| `viewer.clock` / `clockViewModel` | `Clock` / `ClockViewModel` |
| `viewer.canvas` | `HTMLCanvasElement` |
| `viewer.screenSpaceEventHandler` | `ScreenSpaceEventHandler` |
| `viewer.selectedEntity` / `trackedEntity` | `Entity` |
| `viewer.shadows` | `boolean` |
| `viewer.resolutionScale` | `number` (default 1.0) |

```js
await viewer.flyTo(entity, { duration: 3.0, offset: headingPitchRange }); // animated
await viewer.zoomTo(tileset);   // instant
viewer.destroy();               // free all resources
```

## Credit & FrameRateMonitor

```js
import { Credit, FrameRateMonitor } from "cesium";

// Custom credit (showOnScreen = true)
viewer.creditDisplay.addStaticCredit(new Credit("Data by Example Corp", true));

// Monitor frame rate
const monitor = FrameRateMonitor.fromScene(viewer.scene);
monitor.lowFrameRate.addEventListener(() => console.warn("Low FPS"));
monitor.nominalFrameRate.addEventListener(() => console.log("FPS recovered"));
```

## Common Patterns

### Production Viewer with Terrain and OSM Buildings

```js
import { Ion, Viewer, Terrain, createOsmBuildingsAsync, Cartesian3, Math as CesiumMath } from "cesium";

Ion.defaultAccessToken = "YOUR_TOKEN";
const viewer = new Viewer("cesiumContainer", {
  terrain: Terrain.fromWorldTerrain(), animation: false, timeline: false,
});

viewer.scene.primitives.add(await createOsmBuildingsAsync());
viewer.scene.camera.flyTo({
  destination: Cartesian3.fromDegrees(-74.019, 40.6912, 750),
  orientation: { heading: CesiumMath.toRadians(20), pitch: CesiumMath.toRadians(-20) },
});
```

### Space Scene (No Globe)

```js
const viewer = new Viewer("cesiumContainer", {
  globe: false, skyAtmosphere: false, baseLayerPicker: false,
});
```

### Explicit Render Mode (Low Power)

```js
const viewer = new Viewer("cesiumContainer", {
  requestRenderMode: true, maximumRenderTimeChange: Infinity,
});
// Call viewer.scene.requestRender() after programmatic changes
```

### Custom Base Layer

```js
import { Viewer, ImageryLayer, OpenStreetMapImageryProvider } from "cesium";

const viewer = new Viewer("cesiumContainer", {
  baseLayerPicker: false,
  baseLayer: new ImageryLayer(new OpenStreetMapImageryProvider({
    url: "https://tile.openstreetmap.org/",
  })),
});
```

### Columbus View with Web Mercator

```js
import { Viewer, SceneMode, WebMercatorProjection } from "cesium";

const viewer = new Viewer("cesiumContainer", {
  sceneMode: SceneMode.COLUMBUS_VIEW, mapProjection: new WebMercatorProjection(),
});
```

## Performance Tips

1. **Set `requestRenderMode: true`** for mostly-static apps. Reduces CPU/GPU and battery drain. Call `scene.requestRender()` after changes.
2. **Use `scene3DOnly: true`** when 2D/Columbus View is not needed. Saves GPU memory per geometry instance.
3. **Disable unused widgets** (`animation: false`, `timeline: false`) to reduce DOM overhead.
4. **Set `msaaSamples: 1`** on low-power devices. Default `4` balances quality.
5. **Lower `resolutionScale`** (e.g., `0.75`) on HiDPI displays for better frame rates.
6. **Prefer `Terrain.fromWorldTerrain()`** over `await createWorldTerrainAsync()` -- non-blocking with error events.
7. **Enable `requestVertexNormals: true`** on terrain for proper lighting at negligible cost.
8. **Call `viewer.destroy()`** when removing from DOM to free WebGL contexts.
9. **Limit imagery layers** to 2-3. Each adds a texture lookup per fragment.

## See Also

- **cesiumjs-camera** -- Camera positioning, flyTo, lookAt, navigation constraints
- **cesiumjs-entities** -- Entity API, data sources, GeoJSON/KML/CZML loading
- **cesiumjs-imagery** -- Imagery providers, layer management, split-screen
- **cesiumjs-terrain-environment** -- Terrain providers, Globe, atmosphere, sky, lighting
