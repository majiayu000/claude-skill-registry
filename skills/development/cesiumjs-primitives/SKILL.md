---
name: cesiumjs-primitives
description: "CesiumJS primitives and geometry - Primitive, GeometryInstance, Appearance, Billboard/Label/PointPrimitive collections, built-in geometry shapes, ground primitives, classification. Use when rendering performance-critical static geometry, creating custom shapes, batching draw calls, or using low-level billboard, label, and point collections."
---
# CesiumJS Primitives & Geometry

> **Applies to:** CesiumJS v1.139+ (ES module imports, `??` instead of `defaultValue`)

## Architecture

The Primitive API is the low-level rendering layer beneath the Entity API, trading convenience for performance.

**Core formula:** `Primitive = GeometryInstance[] + Appearance`

- **GeometryInstance** -- positions a Geometry in world space with per-instance attributes (color, show).
- **Geometry** -- vertex data describing a shape (polygon, box, ellipsoid, etc.).
- **Appearance** -- GLSL shaders + render state + optional Material that shade the geometry.

Primitives are **immutable after first render** -- geometry cannot change, but per-instance attributes update via `primitive.getGeometryInstanceAttributes(id)`.

## Primitive

```js
import {
  Viewer, Primitive, GeometryInstance, EllipseGeometry,
  EllipsoidSurfaceAppearance, Material, Cartesian3, Math as CesiumMath,
} from "cesium";

const viewer = new Viewer("cesiumContainer");
const scene = viewer.scene;

const primitive = scene.primitives.add(new Primitive({
  geometryInstances: new GeometryInstance({
    geometry: new EllipseGeometry({
      center: Cartesian3.fromDegrees(-100.0, 40.0),
      semiMinorAxis: 250000.0,
      semiMajorAxis: 400000.0,
      rotation: CesiumMath.PI_OVER_FOUR,
      vertexFormat: EllipsoidSurfaceAppearance.VERTEX_FORMAT, // must match appearance
    }),
    id: "myEllipse", // returned by Scene.pick()
  }),
  appearance: new EllipsoidSurfaceAppearance({ material: Material.fromType("Stripe") }),
}));
```

### Key Options

| Option | Default | Purpose |
|---|---|---|
| `geometryInstances` | -- | Single instance or array |
| `appearance` | -- | Shading (Appearance subclass) |
| `show` | `true` | Toggle visibility |
| `modelMatrix` | `Matrix4.IDENTITY` | Transform all instances |
| `asynchronous` | `true` | Build geometry on web worker |
| `releaseGeometryInstances` | `true` | Free geometry after GPU upload |
| `allowPicking` | `true` | `false` saves GPU memory |
| `shadows` | `ShadowMode.DISABLED` | Cast/receive shadows |

## Batching Multiple Instances

All instances in one Primitive share a single draw call.

```js
import {
  Primitive, GeometryInstance, RectangleGeometry, EllipseGeometry,
  PerInstanceColorAppearance, ColorGeometryInstanceAttribute,
  Cartesian3, Rectangle, Color,
} from "cesium";

scene.primitives.add(new Primitive({
  geometryInstances: [
    new GeometryInstance({
      geometry: new RectangleGeometry({
        rectangle: Rectangle.fromDegrees(-140, 30, -100, 40),
        vertexFormat: PerInstanceColorAppearance.VERTEX_FORMAT,
      }),
      id: "rect",
      attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.RED.withAlpha(0.5)) },
    }),
    new GeometryInstance({
      geometry: new EllipseGeometry({
        center: Cartesian3.fromDegrees(-80, 35),
        semiMinorAxis: 200000.0,
        semiMajorAxis: 300000.0,
        vertexFormat: PerInstanceColorAppearance.VERTEX_FORMAT,
      }),
      id: "ellipse",
      attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.BLUE.withAlpha(0.5)) },
    }),
  ],
  appearance: new PerInstanceColorAppearance(),
}));
```

## Updating Per-Instance Attributes

```js
import { ColorGeometryInstanceAttribute, ShowGeometryInstanceAttribute } from "cesium";

// Wait for async geometry compilation
const removeListener = scene.postRender.addEventListener(() => {
  if (!primitive.ready) return;
  const attrs = primitive.getGeometryInstanceAttributes("rect");
  attrs.color = ColorGeometryInstanceAttribute.toValue(Color.YELLOW);
  attrs.show = ShowGeometryInstanceAttribute.toValue(true);
  removeListener();
});
```

## PrimitiveCollection

Nestable container -- `scene.primitives` is itself a PrimitiveCollection.

```js
import { PrimitiveCollection, BillboardCollection, LabelCollection } from "cesium";

const group = new PrimitiveCollection();
group.add(new BillboardCollection());
group.add(new LabelCollection());
scene.primitives.add(group);
group.show = false; // toggle all children
```

## Built-in Geometry Types (31)

All geometries take shape parameters and a `vertexFormat` matching the Appearance. Most have a paired `*OutlineGeometry`. Outlines require a separate Primitive.

### Filled + Outline Pattern

```js
import {
  Primitive, GeometryInstance, PolygonGeometry, PolygonOutlineGeometry,
  PolygonHierarchy, PerInstanceColorAppearance, ColorGeometryInstanceAttribute,
  Cartesian3, Color,
} from "cesium";

const positions = Cartesian3.fromDegreesArray([-115, 37, -115, 32, -107, 33, -102, 35]);

// Fill primitive
scene.primitives.add(new Primitive({
  geometryInstances: new GeometryInstance({
    geometry: new PolygonGeometry({
      polygonHierarchy: new PolygonHierarchy(positions),
      vertexFormat: PerInstanceColorAppearance.VERTEX_FORMAT,
    }),
    attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.CYAN.withAlpha(0.5)) },
  }),
  appearance: new PerInstanceColorAppearance(),
}));

// Outline primitive (separate draw call)
scene.primitives.add(new Primitive({
  geometryInstances: new GeometryInstance({
    geometry: new PolygonOutlineGeometry({ polygonHierarchy: new PolygonHierarchy(positions) }),
    attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.WHITE) },
  }),
  appearance: new PerInstanceColorAppearance({ flat: true }),
}));
```

### Geometry Catalog

Every `XxxGeometry` has a matching `XxxOutlineGeometry` unless noted.

**Surface** (work with GroundPrimitive): `CircleGeometry`, `CorridorGeometry`, `EllipseGeometry`, `PolygonGeometry`, `RectangleGeometry`.

**Volume** (need `modelMatrix`): `BoxGeometry` (`fromDimensions()`), `CylinderGeometry` (cone when topRadius != bottomRadius), `EllipsoidGeometry`, `SphereGeometry`, `FrustumGeometry`, `PlaneGeometry`.

**Path**: `CorridorGeometry` (buffered path), `PolylineVolumeGeometry` (2D shape extruded along path), `WallGeometry` (vertical curtain).

**Polygon**: `PolygonGeometry` (holes via `PolygonHierarchy`), `CoplanarPolygonGeometry` (non-Earth-surface).

**Line** (no outline): `PolylineGeometry` (pixel-width), `SimplePolylineGeometry` (1px), `GroundPolylineGeometry` (GroundPolylinePrimitive only).

### Positioning Off-Surface Geometry

Box, Ellipsoid, Cylinder, and Frustum need a `modelMatrix` on the GeometryInstance.

```js
import { GeometryInstance, BoxGeometry, PerInstanceColorAppearance,
  ColorGeometryInstanceAttribute, Cartesian3, Matrix4, Transforms, Color } from "cesium";

const modelMatrix = Matrix4.multiplyByTranslation(
  Transforms.eastNorthUpToFixedFrame(Cartesian3.fromDegrees(-105, 40)),
  new Cartesian3(0, 0, 250000), new Matrix4(),
);
new GeometryInstance({
  geometry: BoxGeometry.fromDimensions({
    dimensions: new Cartesian3(400000, 300000, 500000),
    vertexFormat: PerInstanceColorAppearance.VERTEX_FORMAT,
  }),
  modelMatrix,
  id: "floatingBox",
  attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.CORAL) },
});
```

## Appearances (7 Types)

| Appearance | Use Case | Material? |
|---|---|---|
| `PerInstanceColorAppearance` | Per-instance color | No |
| `MaterialAppearance` | Arbitrary geometry + Material | Yes |
| `EllipsoidSurfaceAppearance` | Surface geometry + Material (fewer attrs) | Yes |
| `PolylineColorAppearance` | Per-instance color polylines | No |
| `PolylineMaterialAppearance` | Polylines with Material | Yes |
| `DebugAppearance` | Visualize vertex attributes | No |
| `Appearance` | Base class / custom shaders | Optional |

The geometry `vertexFormat` **must** match the appearance. Use the appearance's static `VERTEX_FORMAT`. For `PerInstanceColorAppearance` without lighting, use `FLAT_VERTEX_FORMAT`.

### MaterialAppearance Example

```js
import { Primitive, GeometryInstance, WallGeometry, MaterialAppearance, Material, Cartesian3 } from "cesium";

scene.primitives.add(new Primitive({
  geometryInstances: new GeometryInstance({
    geometry: new WallGeometry({
      positions: Cartesian3.fromDegreesArrayHeights([-115, 44, 200000, -110, 44, 200000, -105, 44, 200000]),
      vertexFormat: MaterialAppearance.MaterialSupport.TEXTURED.vertexFormat,
    }),
  }),
  appearance: new MaterialAppearance({
    material: Material.fromType("Checkerboard"),
    faceForward: true, // shade both sides
  }),
}));
```

## GroundPrimitive

Drapes geometry onto terrain/3D Tiles. Supported: `CircleGeometry`, `CorridorGeometry`, `EllipseGeometry`, `PolygonGeometry`, `RectangleGeometry`.

```js
import { GroundPrimitive, GeometryInstance, PolygonGeometry, PolygonHierarchy,
  ColorGeometryInstanceAttribute, ClassificationType, Cartesian3, Color } from "cesium";

scene.groundPrimitives.add(new GroundPrimitive({
  geometryInstances: new GeometryInstance({
    geometry: new PolygonGeometry({
      polygonHierarchy: new PolygonHierarchy(
        Cartesian3.fromDegreesArray([-112, 36, -112, 36.1, -111.9, 36.1]),
      ),
    }),
    id: "groundPolygon",
    attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.RED.withAlpha(0.5)) },
  }),
  classificationType: ClassificationType.TERRAIN, // TERRAIN, CESIUM_3D_TILE, or BOTH
}));
```

## GroundPolylinePrimitive

```js
import { GroundPolylinePrimitive, GeometryInstance, GroundPolylineGeometry,
  PolylineColorAppearance, ColorGeometryInstanceAttribute, Cartesian3, Color } from "cesium";

scene.groundPrimitives.add(new GroundPolylinePrimitive({
  geometryInstances: new GeometryInstance({
    geometry: new GroundPolylineGeometry({
      positions: Cartesian3.fromDegreesArray([-112.13, 36.05, -112.09, 36.10, -112.13, 36.17]),
      width: 4.0,
      loop: true,
    }),
    attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.LIME.withAlpha(0.7)) },
  }),
  appearance: new PolylineColorAppearance(),
}));
```

## ClassificationPrimitive

Highlights volumes classifying terrain or 3D Tiles. Valid: `BoxGeometry`, `CylinderGeometry`, `EllipsoidGeometry`, `PolylineVolumeGeometry`, `SphereGeometry`, plus extruded surface geometries.

```js
import { ClassificationPrimitive, GeometryInstance, BoxGeometry, PerInstanceColorAppearance,
  ColorGeometryInstanceAttribute, ClassificationType, Cartesian3, Transforms, Color } from "cesium";

scene.primitives.add(new ClassificationPrimitive({
  geometryInstances: new GeometryInstance({
    geometry: BoxGeometry.fromDimensions({
      dimensions: new Cartesian3(100, 100, 50),
      vertexFormat: PerInstanceColorAppearance.VERTEX_FORMAT,
    }),
    modelMatrix: Transforms.eastNorthUpToFixedFrame(Cartesian3.fromDegrees(-75.59, 40.04, 25)),
    attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.YELLOW.withAlpha(0.5)) },
  }),
  classificationType: ClassificationType.BOTH,
}));
```

## BillboardCollection

GPU-efficient viewport-aligned images -- far more performant than entities at scale.

```js
import { BillboardCollection, Cartesian3, Color, NearFarScalar,
  HeightReference, HorizontalOrigin, VerticalOrigin } from "cesium";

const billboards = scene.primitives.add(new BillboardCollection({ scene }));
const b = billboards.add({
  position: Cartesian3.fromDegrees(-75.59, 40.04),
  image: "marker.png",
  horizontalOrigin: HorizontalOrigin.CENTER,
  verticalOrigin: VerticalOrigin.BOTTOM,
  heightReference: HeightReference.CLAMP_TO_GROUND,
  scaleByDistance: new NearFarScalar(1000, 1.5, 1e7, 0.3),
});
b.position = Cartesian3.fromDegrees(-75.60, 40.05); // update dynamically
billboards.remove(b);
```

## LabelCollection

```js
import { LabelCollection, Cartesian3, Cartesian2, Color, LabelStyle, VerticalOrigin } from "cesium";

const labels = scene.primitives.add(new LabelCollection({ scene }));
labels.add({
  position: Cartesian3.fromDegrees(-75.59, 40.04, 300),
  text: "Philadelphia",
  font: "16px sans-serif",
  fillColor: Color.WHITE,
  outlineColor: Color.BLACK,
  outlineWidth: 2,
  style: LabelStyle.FILL_AND_OUTLINE,
  verticalOrigin: VerticalOrigin.BOTTOM,
  pixelOffset: new Cartesian2(0, -10),
});
```

## PointPrimitiveCollection

```js
import { PointPrimitiveCollection, Cartesian3, Color, NearFarScalar } from "cesium";

const points = scene.primitives.add(new PointPrimitiveCollection());
points.add({
  position: Cartesian3.fromDegrees(-75.59, 40.04),
  pixelSize: 10,
  color: Color.YELLOW,
  outlineColor: Color.BLACK,
  outlineWidth: 2,
  scaleByDistance: new NearFarScalar(1000, 1.0, 1e7, 0.1),
});
```

## CloudCollection and PolylineCollection

```js
import { CloudCollection, PolylineCollection, Cartesian3, Cartesian2, Color, Material } from "cesium";

// Procedural cumulus clouds
const clouds = scene.primitives.add(new CloudCollection());
clouds.add({
  position: Cartesian3.fromDegrees(-75.59, 40.04, 1500),
  scale: new Cartesian2(40, 12),
  maximumSize: new Cartesian3(40, 12, 15),
  slice: 0.36,
});

// Low-level polyline collection
const polylines = scene.primitives.add(new PolylineCollection());
polylines.add({
  positions: Cartesian3.fromDegreesArray([-75, 40, -70, 42, -65, 38]),
  width: 3.0,
  material: Material.fromType("Color", { color: Color.AQUA }),
});
```

## Polyline via Primitive

```js
import { Primitive, GeometryInstance, PolylineGeometry, PolylineColorAppearance,
  ColorGeometryInstanceAttribute, Cartesian3, Color, ArcType } from "cesium";

scene.primitives.add(new Primitive({
  geometryInstances: new GeometryInstance({
    geometry: new PolylineGeometry({
      positions: Cartesian3.fromDegreesArray([0, 0, 5, 0]),
      width: 10.0,
      vertexFormat: PolylineColorAppearance.VERTEX_FORMAT,
      arcType: ArcType.GEODESIC, // GEODESIC, RHUMB, or NONE
    }),
    attributes: { color: ColorGeometryInstanceAttribute.fromColor(Color.WHITE) },
  }),
  appearance: new PolylineColorAppearance({ translucent: false }),
}));
```

## Enums

| Enum | Values | Used By |
|---|---|---|
| `ArcType` | `GEODESIC`, `RHUMB`, `NONE` | PolylineGeometry, PolygonGeometry |
| `CornerType` | `ROUNDED`, `MITERED`, `BEVELED` | CorridorGeometry, PolylineVolumeGeometry |
| `ClassificationType` | `TERRAIN`, `CESIUM_3D_TILE`, `BOTH` | GroundPrimitive, ClassificationPrimitive |
| `PrimitiveType` | `POINTS`, `LINES`, `TRIANGLES`, etc. | Low-level Geometry |
| `CloudType` | `CUMULUS` | CloudCollection |

## Performance Tips

1. **Batch aggressively.** Combine thousands of GeometryInstances into one Primitive for a single draw call.
2. **Use `PerInstanceColorAppearance`** when each instance only needs a distinct color.
3. **Set `flat: true`** on PerInstanceColorAppearance when lighting is unneeded; uses `FLAT_VERTEX_FORMAT`.
4. **Set `allowPicking: false`** on Primitives that will never be picked to save GPU memory.
5. **Keep `asynchronous: true`** (default). Check `primitive.ready` before accessing instance attributes.
6. **Prefer fewer large collections** for Billboard, Label, and PointPrimitive. Group by update frequency.
7. **Use `BlendOption.OPAQUE`** on BillboardCollection/PointPrimitiveCollection when all items are opaque (up to 2x gain).
8. **Use GroundPrimitive** for terrain draping instead of entity `heightReference`.
9. **Separate fill and outline** into two Primitives -- they cannot share a draw call.
10. **Match `vertexFormat` exactly** to the appearance to skip unused vertex attribute computation.
11. **Use `EllipsoidSurfaceAppearance`** over `MaterialAppearance` for surface geometry -- fewer vertex attributes.

## See Also

- **cesiumjs-entities** -- High-level Entity API wrapping primitives with time-dynamic properties.
- **cesiumjs-materials-shaders** -- Material (Fabric) system consumed by Appearances, post-processing.
- **cesiumjs-spatial-math** -- Cartesian3, Matrix4, Transforms, coordinate conversions for positioning geometry.
