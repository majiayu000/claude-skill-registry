---
name: cesiumjs-imagery
description: "CesiumJS imagery layers - ImageryProvider, ImageryLayer, ImageryLayerCollection, WMS, WMTS, Bing, OpenStreetMap, ArcGIS, Mapbox, tile discard policies. Use when adding or swapping base map layers, configuring imagery providers, layering multiple map sources, or creating split-screen imagery comparisons."
---
# CesiumJS Imagery Layers

> CesiumJS v1.139 -- Imagery providers supply raster tile data rendered on the Globe
> or draped over a Cesium3DTileset. The three core abstractions are **ImageryProvider**
> (fetches tiles), **ImageryLayer** (display settings), and
> **ImageryLayerCollection** (ordered stack on the globe).

```
ImageryProvider        (abstract -- fetches tile images)
  -> ImageryLayer      (wraps one provider; alpha, brightness, split, etc.)
    -> ImageryLayerCollection  (ordered stack; index 0 = base layer)
      -> Globe / Cesium3DTileset
```

Layers render bottom-to-top. Index 0 is the **base layer**, stretched to fill
the globe even if its rectangle does not cover the entire world.

## Quick Start and ImageryLayer Factories

When creating a viewer for imagery work, disable unneeded widgets so the imagery
is the visual focus. Use `camera.setView` (not `flyTo`) when you need the camera
in position immediately — `flyTo` animates and may not finish before your code
continues.

```js
import { Viewer, ImageryLayer, IonImageryProvider, IonWorldImageryStyle, Math as CesiumMath } from "cesium";

// Clean viewer -- disable widgets that distract from imagery
const viewer = new Viewer("cesiumContainer", {
  animation: false,
  timeline: false,
  navigationHelpButton: false,
  navigationInstructionsInitiallyVisible: false,
});

// Position camera immediately (no animation)
viewer.camera.setView({
  destination: Cesium.Cartesian3.fromDegrees(-73.0, 41.0, 1500000),
  orientation: {
    heading: 0.0,
    pitch: CesiumMath.toRadians(-90), // look straight down
    roll: 0.0,
  },
});

// Explicit base layer choice
const viewer2 = new Viewer("cesiumContainer", {
  baseLayer: ImageryLayer.fromWorldImagery(),
});

// fromProviderAsync -- wraps any async provider; returns ImageryLayer immediately
const nightLayer = ImageryLayer.fromProviderAsync(
  IonImageryProvider.fromAssetId(3812), // Earth at Night
);
nightLayer.alpha = 0.5;
nightLayer.brightness = 2.0;
viewer.imageryLayers.add(nightLayer);

// fromWorldImagery with style override
const roadLayer = ImageryLayer.fromWorldImagery({
  style: IonWorldImageryStyle.ROAD,
});
viewer.imageryLayers.add(roadLayer);
```

### Camera Height Reference for Imagery Scenes

Use `camera.setView` with these approximate heights:

| Scale | Height (m) | Example |
|---|---|---|
| Street / block | 500–2,000 | Downtown intersection |
| City | 5,000–25,000 | Washington DC, Paris |
| Metro area | 50,000–200,000 | Greater London |
| Region / state | 300,000–1,500,000 | Florida, Japan |
| Continent | 3,000,000–8,000,000 | Europe, North America |

For top-down (map-style) views set `pitch: CesiumMath.toRadians(-90)`.
For oblique 3D views set `pitch: CesiumMath.toRadians(-35)` to `CesiumMath.toRadians(-60)`.

## ImageryLayerCollection API

Access via `viewer.imageryLayers` (same as `viewer.scene.imageryLayers`).

```js
const layers = viewer.imageryLayers;

layers.add(myLayer);              // add on top
layers.add(myLayer, 0);           // add at index
layers.addImageryProvider(provider); // create layer + add

layers.raise(myLayer);            // move up one
layers.lower(myLayer);            // move down one
layers.raiseToTop(myLayer);       // move to top
layers.lowerToBottom(myLayer);    // move to bottom

layers.remove(myLayer);           // remove and destroy
layers.remove(myLayer, false);    // remove without destroying
layers.removeAll();

const count = layers.length;
const base  = layers.get(0);
const idx   = layers.indexOf(myLayer);
const has   = layers.contains(myLayer);
```

Events: `layerAdded(layer, index)`, `layerRemoved(layer, index)`,
`layerMoved(layer, newIndex, oldIndex)`, `layerShownOrHidden(layer, index, show)`.

## ImageryLayer Display Properties

Properties accept a number or a per-tile callback `(frameState, layer, x, y, level) => value`.

| Property | Default | Notes |
|---|---|---|
| `alpha` | 1.0 | 0 = transparent, 1 = opaque |
| `brightness` | 1.0 | < 1 darker, > 1 brighter |
| `contrast` | 1.0 | < 1 lower, > 1 higher |
| `hue` | 0.0 | Shift in radians |
| `saturation` | 1.0 | < 1 desaturated, > 1 oversaturated |
| `gamma` | 1.0 | Gamma correction |
| `show` | true | Visibility toggle |
| `splitDirection` | `SplitDirection.NONE` | LEFT, RIGHT, or NONE |
| `nightAlpha` / `dayAlpha` | 1.0 | Requires `Globe.enableLighting` |

Additional options: `rectangle`, `minimumTerrainLevel` / `maximumTerrainLevel`,
`cutoutRectangle`, `colorToAlpha` / `colorToAlphaThreshold`,
`minificationFilter` / `magnificationFilter` (LINEAR default, or NEAREST).

```js
// Adjust appearance at runtime
layer.alpha = 0.7;
layer.brightness = 1.3;
layer.contrast = 1.5;
layer.saturation = 0.5;
layer.gamma = 1.2;
```

## Swapping the Base Layer

Remove the default base layer and replace it at index 0. The replacement becomes
the new base layer, stretched to fill the globe.

```js
import { ImageryLayer, OpenStreetMapImageryProvider } from "cesium";

// Remove default Bing aerial
viewer.imageryLayers.remove(viewer.imageryLayers.get(0));

// Add OSM as new base layer at index 0
const osmLayer = new ImageryLayer(
  new OpenStreetMapImageryProvider({
    url: "https://tile.openstreetmap.org/",
    maximumLevel: 19,
    credit: "OpenStreetMap contributors",
  }),
);
viewer.imageryLayers.add(osmLayer, 0);
```

## Imagery Providers

### IonImageryProvider

```js
// Always use fromAssetId (async factory); never call constructor directly
const layer = ImageryLayer.fromProviderAsync(
  IonImageryProvider.fromAssetId(3812),
);
viewer.imageryLayers.add(layer);
```

### OpenStreetMapImageryProvider

Extends UrlTemplateImageryProvider for Slippy tile servers.

```js
const osm = new OpenStreetMapImageryProvider({
  url: "https://tile.openstreetmap.org/",
  maximumLevel: 19,
  credit: "OpenStreetMap contributors",
  // retinaTiles: true,  // request @2x tiles
});
viewer.imageryLayers.addImageryProvider(osm);
```

### UrlTemplateImageryProvider

The most flexible provider. Placeholders: `{x}`, `{y}`, `{z}`, `{s}`,
`{reverseX/Y/Z}`, `{west/south/east/northDegrees}`,
`{west/south/east/northProjected}`, `{width}`, `{height}`.

```js
import { UrlTemplateImageryProvider, GeographicTilingScheme, buildModuleUrl } from "cesium";

// TMS-style with Geographic tiling
const tms = new UrlTemplateImageryProvider({
  url: buildModuleUrl("Assets/Textures/NaturalEarthII") + "/{z}/{x}/{reverseY}.jpg",
  tilingScheme: new GeographicTilingScheme(),
  maximumLevel: 5,
});
viewer.imageryLayers.addImageryProvider(tms);

// Carto Positron with subdomains
const positron = new UrlTemplateImageryProvider({
  url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
  subdomains: "abcd",
  credit: "Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
});

// Custom tags for time-varying data
const custom = new UrlTemplateImageryProvider({
  url: "https://yourserver/{Time}/{z}/{y}/{x}.png",
  customTags: {
    Time: (imageryProvider, x, y, level) => "20240101",
  },
});
```

### WebMapServiceImageryProvider (WMS)

```js
import { WebMapServiceImageryProvider, ImageryLayer, Rectangle } from "cesium";

const wms = new WebMapServiceImageryProvider({
  url: "https://basemap.nationalmap.gov:443/arcgis/services/USGSHydroCached/MapServer/WMSServer",
  layers: "0",
  rectangle: Rectangle.fromDegrees(-180, -90, 180, 90),
  // parameters: { transparent: true, format: "image/png" },
  // crs: "EPSG:4326",  // WMS >= 1.3.0
  // srs: "EPSG:4326",  // WMS 1.1.x
});
viewer.imageryLayers.add(new ImageryLayer(wms));
```

### WebMapTileServiceImageryProvider (WMTS)

Required options: `url`, `layer`, `style`, `tileMatrixSetID`.

```js
import { WebMapTileServiceImageryProvider, Credit } from "cesium";

const wmts = new WebMapTileServiceImageryProvider({
  url: "https://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/WMTS",
  layer: "USGSShadedReliefOnly",
  style: "default",
  format: "image/jpeg",
  tileMatrixSetID: "default028mm",
  maximumLevel: 19,
  credit: new Credit("U. S. Geological Survey"),
});
viewer.imageryLayers.addImageryProvider(wmts);
```

### ArcGisMapServerImageryProvider

```js
import { ArcGisMapServerImageryProvider, ArcGisMapService, ArcGisBaseMapType, ImageryLayer } from "cesium";

ArcGisMapService.defaultAccessToken = "<YOUR_ARCGIS_TOKEN>";

// From basemap type enum: SATELLITE, OCEANS, HILLSHADE
const arcgis = ImageryLayer.fromProviderAsync(
  ArcGisMapServerImageryProvider.fromBasemapType(ArcGisBaseMapType.SATELLITE),
);
viewer.imageryLayers.add(arcgis);

// From a specific MapServer URL
const streets = ImageryLayer.fromProviderAsync(
  ArcGisMapServerImageryProvider.fromUrl(
    "https://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer",
  ),
);
```

### BingMapsImageryProvider

```js
import { BingMapsImageryProvider, BingMapsStyle, ImageryLayer } from "cesium";

const bing = ImageryLayer.fromProviderAsync(
  BingMapsImageryProvider.fromUrl("https://dev.virtualearth.net", {
    key: "<YOUR_BING_KEY>",
    mapStyle: BingMapsStyle.AERIAL_WITH_LABELS_ON_DEMAND,
  }),
);
viewer.imageryLayers.add(bing);
```

Styles: `AERIAL`, `AERIAL_WITH_LABELS_ON_DEMAND`, `ROAD_ON_DEMAND`,
`CANVAS_DARK`, `CANVAS_LIGHT`, `CANVAS_GRAY`.

### MapboxStyleImageryProvider

```js
import { MapboxStyleImageryProvider, ImageryLayer } from "cesium";

const mapbox = new MapboxStyleImageryProvider({
  styleId: "streets-v11",
  accessToken: "<YOUR_MAPBOX_TOKEN>",
  // tilesize: 512, scaleFactor: true  // retina
});
viewer.imageryLayers.add(new ImageryLayer(mapbox));
```

### SingleTileImageryProvider

```js
import { SingleTileImageryProvider, ImageryLayer, Rectangle } from "cesium";

const logo = ImageryLayer.fromProviderAsync(
  SingleTileImageryProvider.fromUrl("/images/overlay.png", {
    rectangle: Rectangle.fromDegrees(-75.0, 28.0, -67.0, 29.75),
  }),
);
viewer.imageryLayers.add(logo);
```

## Split-Screen Comparison

```js
import { ImageryLayer, IonImageryProvider, SplitDirection } from "cesium";

// Add an overlay that only appears on the left side of the split
const nightLayer = ImageryLayer.fromProviderAsync(IonImageryProvider.fromAssetId(3812));
nightLayer.splitDirection = SplitDirection.LEFT;
viewer.imageryLayers.add(nightLayer);

viewer.scene.splitPosition = 0.5; // 0-1 fraction of viewport width
```

`SplitDirection`: `LEFT` (-1), `NONE` (0), `RIGHT` (1).

## Cutout Rectangle

```js
import { Rectangle } from "cesium";

const cutout = Rectangle.fromDegrees(-90, 20, -70, 40);

// Cut a hole in the base layer to reveal imagery beneath
const base = viewer.imageryLayers.get(0);
base.cutoutRectangle = cutout;
```

## Color-to-Alpha

```js
import { Color } from "cesium";

const baseLayer = viewer.imageryLayers.get(0);
baseLayer.colorToAlpha = new Color(0.0, 0.016, 0.059); // dark ocean blue
baseLayer.colorToAlphaThreshold = 0.2; // tolerance (0-1)
```

## Draping Imagery on 3D Tiles

```js
import { Cesium3DTileset, ImageryLayer, IonImageryProvider } from "cesium";

const tileset = await Cesium3DTileset.fromUrl("/path/to/tileset.json");
viewer.scene.primitives.add(tileset);

const labelLayer = ImageryLayer.fromProviderAsync(
  IonImageryProvider.fromAssetId(2411391),
);
tileset.imageryLayers.add(labelLayer); // drape on tileset, not globe
labelLayer.show = false; // toggle off
```

## Debugging Providers

```js
import { TileCoordinatesImageryProvider, GridImageryProvider, ImageryLayer, Color } from "cesium";

// Show x/y/level labels on every tile
viewer.imageryLayers.add(new ImageryLayer(
  new TileCoordinatesImageryProvider({ color: Color.YELLOW }),
));
// Wireframe grid overlay
viewer.imageryLayers.add(new ImageryLayer(new GridImageryProvider()));
```

## Tile Discard Policies

| Policy | Behavior |
|---|---|
| `DiscardEmptyTileImagePolicy` | Discards zero-byte images (Bing Maps default) |
| `DiscardMissingTileImagePolicy` | Compares pixels against a known "missing" tile |
| `NeverTileDiscardPolicy` | Never discards (use when server always returns valid tiles) |

```js
import { NeverTileDiscardPolicy, UrlTemplateImageryProvider } from "cesium";

const provider = new UrlTemplateImageryProvider({
  url: "https://my-server/{z}/{x}/{y}.png",
  tileDiscardPolicy: new NeverTileDiscardPolicy(),
});
```

## Error Handling

```js
const layer = ImageryLayer.fromProviderAsync(IonImageryProvider.fromAssetId(3812));
viewer.imageryLayers.add(layer);

// Provider creation failure
layer.errorEvent.addEventListener((error) => {
  console.error("Layer creation failed:", error);
});

// Provider resolved -- listen for per-tile errors
layer.readyEvent.addEventListener((provider) => {
  provider.errorEvent.addEventListener((tileError) => {
    console.warn("Tile error:", tileError.message);
  });
});
```

## Time-Dynamic WMTS

Pass `clock` and `times` (a `TimeIntervalCollection`) for time-varying layers.

```js
import { WebMapTileServiceImageryProvider, TimeIntervalCollection, JulianDate, Credit } from "cesium";

const times = TimeIntervalCollection.fromIso8601({
  iso8601: "2015-07-30/2017-06-16/P1D",
  dataCallback: (interval) => ({ Time: JulianDate.toIso8601(interval.start) }),
});
const weather = new WebMapTileServiceImageryProvider({
  url: "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/AMSR2_Snow_Water_Equivalent/default/{Time}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png",
  layer: "AMSR2_Snow_Water_Equivalent",  style: "default",
  tileMatrixSetID: "2km",  maximumLevel: 5,  format: "image/png",
  clock: viewer.clock,  times: times,
  credit: new Credit("NASA Global Imagery Browse Services for EOSDIS"),
});
viewer.imageryLayers.addImageryProvider(weather);
```

## Performance Tips

1. **Limit simultaneous layers** -- 2-3 is typical; each layer multiplies tile requests and GPU texture memory.
2. **Set `hasAlphaChannel: false`** on opaque providers to reduce memory and upload time.
3. **Use `minimumTerrainLevel` / `maximumTerrainLevel`** to skip tile fetches at irrelevant zoom levels.
4. **Prefer `ImageryLayer.fromProviderAsync`** over manual await -- avoids blank globe during provider load.
5. **Set tight `rectangle` bounds** on regional providers to prevent out-of-extent tile requests.
6. **Reuse provider instances** -- remove with `destroy: false` and re-add instead of recreating.
7. **Use `NeverTileDiscardPolicy`** when tiles are always valid; pixel comparison adds overhead.
8. **Choose NEAREST filtering** only for classified raster data; LINEAR (default) is faster.

## See Also

- **cesiumjs-viewer-setup** -- Viewer constructor, Ion token, `createWorldImageryAsync`
- **cesiumjs-terrain-environment** -- Globe, terrain providers, atmosphere, lighting
