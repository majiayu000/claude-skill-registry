---
name: cesiumjs-entities
description: "CesiumJS entities and data sources - Entity, EntityCollection, DataSource, GeoJsonDataSource, KmlDataSource, CzmlDataSource, Graphics types, Visualizers. Use when adding points, labels, models, polygons, or polylines to the map, loading GeoJSON/KML/CZML/GPX data, or working with the high-level Entity API."
---
# CesiumJS Entities & DataSources

> **Version baseline:** CesiumJS 1.139 -- ES module imports: `import { ... } from "cesium";`
> **Ownership rule:** `*Graphics` classes belong here; `*Geometry` classes belong in cesiumjs-primitives. Properties (SampledProperty, CallbackProperty, MaterialProperty subtypes) belong in cesiumjs-time-properties.

## Architecture

The Entity API is the high-level, data-driven layer of CesiumJS. Entities combine position, orientation, and one or more Graphics types into a single object managed by an EntityCollection. DataSources load external formats (GeoJSON, KML, CZML, GPX) and populate an EntityCollection automatically. Visualizers and GeometryUpdaters translate Entity descriptions into Primitives each frame.

```
DataSource --> EntityCollection --> Entity
                                     |-- position / orientation
                                     |-- billboard / point / label / model / polygon / polyline / ...
                                     |-- properties (PropertyBag)
```

- `viewer.entities` is a shortcut to the default DataSource's EntityCollection
- `viewer.dataSources` holds all loaded DataSources; each owns an `EntityCollection`

## Entity Basics

### Point

```javascript
import { Viewer, Cartesian3, Color, HeightReference } from "cesium";

const viewer = new Viewer("cesiumContainer");
const entity = viewer.entities.add({
  id: "my-point",                 // optional; auto-generated GUID if omitted
  name: "Sample Point",
  position: Cartesian3.fromDegrees(-75.59777, 40.03883),
  point: {
    pixelSize: 10,
    color: Color.YELLOW,
    outlineColor: Color.BLACK,
    outlineWidth: 2,
    heightReference: HeightReference.CLAMP_TO_GROUND,
  },
});
viewer.zoomTo(entity);
```

### Billboard with Label

```javascript
import { Viewer, Cartesian3, Cartesian2, Color, VerticalOrigin, HeightReference, LabelStyle } from "cesium";

const viewer = new Viewer("cesiumContainer");
viewer.entities.add({
  position: Cartesian3.fromDegrees(-122.4175, 37.7749),
  billboard: {
    image: "/assets/marker.png",
    scale: 0.5,
    verticalOrigin: VerticalOrigin.BOTTOM,
    heightReference: HeightReference.CLAMP_TO_GROUND,
  },
  label: {
    text: "San Francisco",
    font: "14px sans-serif",
    fillColor: Color.WHITE,
    outlineColor: Color.BLACK,
    outlineWidth: 2,
    style: LabelStyle.FILL_AND_OUTLINE,
    pixelOffset: new Cartesian2(0, -36),
    heightReference: HeightReference.CLAMP_TO_GROUND,
  },
});
```

### Polygon (flat, extruded, with holes)

```javascript
import { Viewer, Cartesian3, Color, PolygonHierarchy } from "cesium";

const viewer = new Viewer("cesiumContainer");
// Flat polygon
viewer.entities.add({
  polygon: {
    hierarchy: Cartesian3.fromDegreesArray([-115, 37, -115, 32, -107, 33, -102, 31, -102, 35]),
    material: Color.RED.withAlpha(0.5),
    outline: true,
    outlineColor: Color.BLACK,
  },
});
// Extruded polygon with hole
viewer.entities.add({
  polygon: {
    hierarchy: new PolygonHierarchy(
      Cartesian3.fromDegreesArray([-99, 30, -85, 30, -85, 40, -99, 40]),
      [new PolygonHierarchy(Cartesian3.fromDegreesArray([-97, 32, -87, 32, -87, 38, -97, 38]))]
    ),
    extrudedHeight: 300000,
    material: Color.BLUE.withAlpha(0.6),
    closeTop: true,
    closeBottom: true,
  },
});
```

### Polyline

```javascript
import { Viewer, Cartesian3, Color, ArcType } from "cesium";

const viewer = new Viewer("cesiumContainer");
viewer.entities.add({
  polyline: {
    positions: Cartesian3.fromDegreesArray([-75, 35, -125, 35]),
    width: 5,
    material: Color.RED,
    arcType: ArcType.GEODESIC,
    clampToGround: true,
  },
});
```

### 3D Model

```javascript
import { Viewer, Cartesian3, HeadingPitchRoll, Transforms, Math as CesiumMath, Color } from "cesium";

const viewer = new Viewer("cesiumContainer");
const position = Cartesian3.fromDegrees(-123.075, 44.045, 5000);
const hpr = new HeadingPitchRoll(CesiumMath.toRadians(135), 0, 0);

viewer.entities.add({
  position,
  orientation: Transforms.headingPitchRollQuaternion(position, hpr),
  model: {
    uri: "/assets/CesiumAir/Cesium_Air.glb",
    minimumPixelSize: 64,
    maximumScale: 20000,
    silhouetteColor: Color.RED,
    silhouetteSize: 2,
  },
});
```

### Box, Cylinder, Ellipsoid, Ellipse

```javascript
import { Viewer, Cartesian3, Color } from "cesium";
const viewer = new Viewer("cesiumContainer");

viewer.entities.add({  // Box
  position: Cartesian3.fromDegrees(-107, 40, 300000),
  box: { dimensions: new Cartesian3(400000, 300000, 500000), material: Color.BLUE.withAlpha(0.5) },
});
viewer.entities.add({  // Cylinder (topRadius: 0 for a cone)
  position: Cartesian3.fromDegrees(-100, 40, 200000),
  cylinder: { length: 400000, topRadius: 200000, bottomRadius: 200000, material: Color.GREEN.withAlpha(0.5) },
});
viewer.entities.add({  // Ellipsoid (sphere when all radii equal)
  position: Cartesian3.fromDegrees(-93, 40, 300000),
  ellipsoid: { radii: new Cartesian3(200000, 200000, 300000), material: Color.RED.withAlpha(0.5) },
});
viewer.entities.add({  // Ellipse (circle when axes equal)
  position: Cartesian3.fromDegrees(-86, 40),
  ellipse: { semiMajorAxis: 300000, semiMinorAxis: 300000, material: Color.PURPLE.withAlpha(0.5) },
});
```

### Corridor, Rectangle, Wall

```javascript
import { Viewer, Cartesian3, Color, Rectangle, CornerType } from "cesium";
const viewer = new Viewer("cesiumContainer");

viewer.entities.add({  // Corridor: path with width
  corridor: { positions: Cartesian3.fromDegreesArray([-80, 40, -90, 40, -90, 35]), width: 200000, material: Color.ORANGE.withAlpha(0.6), cornerType: CornerType.ROUNDED },
});
viewer.entities.add({  // Rectangle by geographic bounds
  rectangle: { coordinates: Rectangle.fromDegrees(-110, 20, -80, 25), material: Color.GREEN.withAlpha(0.5), extrudedHeight: 50000 },
});
viewer.entities.add({  // Wall: vertical curtain
  wall: { positions: Cartesian3.fromDegreesArrayHeights([-115, 44, 200000, -90, 44, 200000]), minimumHeights: [100000, 100000], material: Color.CYAN.withAlpha(0.7) },
});
```

## EntityCollection Operations

```javascript
viewer.entities.getById("my-point");               // retrieve by ID
viewer.entities.getOrCreateEntity("some-id");       // get or create
viewer.entities.values;                             // Entity[] (read-only)
viewer.entities.remove(entity);                     // remove by reference
viewer.entities.removeById("my-point");             // remove by ID
viewer.entities.removeAll();                        // clear all

// Batch updates -- suspend events for bulk add/remove
viewer.entities.suspendEvents();
for (let i = 0; i < 1000; i++) viewer.entities.add({ /* ... */ });
viewer.entities.resumeEvents();  // fires one collectionChanged event

viewer.entities.collectionChanged.addEventListener((collection, added, removed, changed) => {
  console.log(`Added: ${added.length}, Removed: ${removed.length}`);
});
```

## DataSources

### GeoJSON / TopoJSON

```javascript
import { Viewer, GeoJsonDataSource, Color } from "cesium";
const viewer = new Viewer("cesiumContainer");

// Load from URL with styling options
const ds = await GeoJsonDataSource.load("/data/counties.geojson", {
  stroke: Color.HOTPINK, fill: Color.PINK.withAlpha(0.5), strokeWidth: 3, clampToGround: true,
});
viewer.dataSources.add(ds);
viewer.zoomTo(ds);

// Post-load styling: iterate and customize
for (const entity of ds.entities.values) {
  if (entity.polygon) entity.polygon.material = Color.fromRandom({ alpha: 0.8 });
}
```

`GeoJsonDataSource.load()` also accepts an inline GeoJSON object instead of a URL.

### KML / KMZ

```javascript
import { KmlDataSource } from "cesium";
const ds = await KmlDataSource.load("/data/sample.kml", {
  camera: viewer.scene.camera, canvas: viewer.scene.canvas, clampToGround: true,
});
viewer.dataSources.add(ds);
viewer.flyTo(ds);
```

### CZML

```javascript
import { CzmlDataSource } from "cesium";
const ds = await CzmlDataSource.load("/data/vehicle.czml");
viewer.dataSources.add(ds);
await ds.process("/data/vehicle-update.czml");  // append without clearing
```

### GPX

```javascript
import { GpxDataSource } from "cesium";
const ds = await GpxDataSource.load("/data/trail.gpx");
viewer.dataSources.add(ds);
viewer.zoomTo(ds);
```

### CustomDataSource

```javascript
import { CustomDataSource, Cartesian3, Color } from "cesium";

const customDs = new CustomDataSource("sensors");
customDs.entities.add({
  position: Cartesian3.fromDegrees(-95, 40),
  point: { pixelSize: 8, color: Color.LIME },
});
viewer.dataSources.add(customDs);
customDs.show = false;  // toggle entire group visibility
```

## Entity Clustering

```javascript
import { GeoJsonDataSource, Color, VerticalOrigin, PinBuilder } from "cesium";
const ds = await GeoJsonDataSource.load("/data/facilities.geojson");
viewer.dataSources.add(ds);

ds.clustering.enabled = true;
ds.clustering.pixelRange = 40;
ds.clustering.minimumClusterSize = 3;

const pinBuilder = new PinBuilder();
ds.clustering.clusterEvent.addEventListener((entities, cluster) => {
  cluster.label.show = false;
  cluster.billboard.show = true;
  cluster.billboard.verticalOrigin = VerticalOrigin.BOTTOM;
  cluster.billboard.image = pinBuilder.fromText(`${entities.length}`, Color.VIOLET, 48).toDataURL();
});
```

## Parent-Child Visibility

Setting `parent.show = false` hides all descendants without changing their individual `show` flags.

```javascript
const parent = viewer.entities.add({ name: "Group" });
viewer.entities.add({ parent, position: Cartesian3.fromDegrees(-90, 35), point: { pixelSize: 6, color: Color.RED } });
viewer.entities.add({ parent, position: Cartesian3.fromDegrees(-91, 36), point: { pixelSize: 6, color: Color.BLUE } });

parent.show = false;  // both children disappear
parent.show = true;   // both reappear
```

## Entity Description and Custom Properties

```javascript
// InfoBox HTML: displayed when user clicks the entity
viewer.entities.add({
  name: "Station Alpha",
  position: Cartesian3.fromDegrees(-75.17, 39.95),
  point: { pixelSize: 12, color: Color.CYAN },
  description: `<table class="cesium-infoBox-defaultTable"><tr><th>Status</th><td>Active</td></tr></table>`,
  properties: { population: 500000, category: "metro" },
});
// Read custom properties
// entity.properties.population.getValue()  --> 500000
```

## Export to KML

```javascript
import { exportKml } from "cesium";

const result = await exportKml({ entities: viewer.entities, kmz: true });
// result.kmz is a Blob; result.kml is a string when kmz: false
const url = URL.createObjectURL(result.kmz);
```

## All 17 Graphics Types

| Graphics | Key Properties |
|----------|---------------|
| `PointGraphics` | pixelSize, color, outlineColor, outlineWidth |
| `BillboardGraphics` | image, scale, rotation, sizeInMeters, heightReference |
| `LabelGraphics` | text, font, fillColor, style, showBackground |
| `ModelGraphics` | uri, scale, silhouetteColor, runAnimations, colorBlendMode |
| `PolygonGraphics` | hierarchy, height, extrudedHeight, material, perPositionHeight |
| `PolylineGraphics` | positions, width, material, clampToGround, arcType |
| `EllipseGraphics` | semiMajorAxis, semiMinorAxis, rotation, extrudedHeight |
| `RectangleGraphics` | coordinates (Rectangle), height, extrudedHeight |
| `BoxGraphics` | dimensions (Cartesian3), material, outline |
| `CylinderGraphics` | length, topRadius, bottomRadius |
| `EllipsoidGraphics` | radii (Cartesian3) |
| `CorridorGraphics` | positions, width, cornerType |
| `WallGraphics` | positions, minimumHeights, maximumHeights |
| `PolylineVolumeGraphics` | positions, shape (Cartesian2[]) |
| `PlaneGraphics` | plane (Plane), dimensions (Cartesian2) |
| `PathGraphics` | resolution, leadTime, trailTime, width |
| `Cesium3DTilesetGraphics` | uri |

## Key Enums

| Enum | Values |
|------|--------|
| `HeightReference` | NONE, CLAMP_TO_GROUND, RELATIVE_TO_GROUND |
| `HorizontalOrigin` | LEFT, CENTER, RIGHT |
| `VerticalOrigin` | TOP, CENTER, BOTTOM, BASELINE |
| `LabelStyle` | FILL, OUTLINE, FILL_AND_OUTLINE |
| `ColorBlendMode` | HIGHLIGHT, REPLACE, MIX |
| `ShadowMode` | DISABLED, ENABLED, CAST_ONLY, RECEIVE_ONLY |

## Performance Tips

1. **Use `suspendEvents()`/`resumeEvents()`** when bulk-adding entities to batch change notifications.
2. **Prefer constant properties** for static data -- CesiumJS optimizes non-changing entities.
3. **Use `DistanceDisplayCondition`** to hide entities beyond a useful range.
4. **Switch to Primitives** for 10k+ static shapes; Primitives avoid per-entity overhead.
5. **Enable clustering** on DataSources with many point-like entities.
6. **Set `disableDepthTestDistance`** on billboards/labels to prevent terrain occlusion.
7. **Minimize outlines** on ground-clamped polygons -- extra rendering passes required.
8. **Use `clampToGround` only when needed** -- requires terrain-conforming subdivision.
9. **Batch CZML updates** with `process()` to append, not `load()` which replaces all.
10. **Cache PinBuilder canvases** -- reuse results to avoid regenerating identical images.

## See Also

- **cesiumjs-time-properties** -- SampledProperty, CallbackProperty, MaterialProperty types for time-dynamic entity attributes
- **cesiumjs-primitives** -- Low-level Primitive API for performance-critical static geometry (`*Geometry` classes)
- **cesiumjs-interaction** -- ScreenSpaceEventHandler, Scene.pick, entity selection and hover patterns
