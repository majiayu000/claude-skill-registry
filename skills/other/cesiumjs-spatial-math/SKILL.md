---
name: cesiumjs-spatial-math
description: "CesiumJS spatial math - Cartesian3, Cartographic, Matrix4, Quaternion, Transforms, Ellipsoid, BoundingSphere, projections, coordinate conversions. Use when converting between coordinate systems, computing positions on the ellipsoid, performing spatial intersection tests, building model matrices, or working with geographic projections."
---
# CesiumJS Spatial Math & Transforms

Version baseline: CesiumJS v1.139 (2026-03-05)

Mathematical foundation for every CesiumJS application: coordinate types, unit conversions, ellipsoid geometry, reference frame transforms, bounding volumes, intersection tests, and projections.

## Core Concepts

CesiumJS uses a right-handed Earth-Centered Earth-Fixed (ECEF) coordinate system:

- **Cartesian3** -- ECEF (x, y, z) in meters. Internal representation for all 3D positions.
- **Cartographic** -- (longitude, latitude, height). Angles are **radians**, height in meters above ellipsoid.

All angular values in core math are radians. Use `Math.toRadians()` / `Math.toDegrees()`. Math types use a **static-method-with-result** pattern: pass a `result` parameter to reuse allocations.

## Cartesian3 -- Positions and Vectors

```js
import { Cartesian3, Math as CesiumMath } from "cesium";

// From lon/lat degrees -- most common entry point
const pos = Cartesian3.fromDegrees(-105.0, 40.0);
const elevated = Cartesian3.fromDegrees(-105.0, 40.0, 1500.0); // with height

// Batch creation: [lon, lat, lon, lat, ...]
const ring = Cartesian3.fromDegreesArray([-105, 40, -100, 40, -100, 35]);

// With heights: [lon, lat, h, lon, lat, h, ...]
const wall = Cartesian3.fromDegreesArrayHeights([-105, 40, 500, -100, 40, 1000]);

// From raw ECEF or from radians
const raw = new Cartesian3(-1275096.0, -4797180.0, 4075270.0);
const fromRad = Cartesian3.fromRadians(-1.8326, 0.6981, 1500.0);

// Constants
Cartesian3.ZERO;   // (0,0,0)
Cartesian3.UNIT_X; // (1,0,0)
Cartesian3.UNIT_Y; // (0,1,0)
Cartesian3.UNIT_Z; // (0,0,1)
```

### Vector Operations

```js
const a = new Cartesian3(1.0, 2.0, 3.0);
const b = new Cartesian3(4.0, 5.0, 6.0);
const r = new Cartesian3(); // reusable scratch

Cartesian3.add(a, b, r);                // a + b
Cartesian3.subtract(a, b, r);           // a - b
Cartesian3.multiplyByScalar(a, 2.0, r); // a * 2
Cartesian3.negate(a, r);                // -a
Cartesian3.cross(a, b, r);              // cross product
Cartesian3.normalize(a, r);             // unit vector
Cartesian3.lerp(a, b, 0.5, r);         // linear interpolation
Cartesian3.midpoint(a, b, r);           // midpoint

const dot = Cartesian3.dot(a, b);       // dot product
const len = Cartesian3.magnitude(a);    // ||a||
const dist = Cartesian3.distance(a, b); // Euclidean distance
const distSq = Cartesian3.distanceSquared(a, b); // faster for comparisons
const angle = Cartesian3.angleBetween(a, b);     // radians
```

## Cartographic -- Geographic Coordinates

```js
import { Cartographic, Cartesian3, Math as CesiumMath } from "cesium";

const carto = Cartographic.fromDegrees(-105.0, 40.0, 1500.0);
const cartoRad = Cartographic.fromRadians(-1.8326, 0.6981, 1500.0);

// Cartesian3 <-> Cartographic
const position = Cartesian3.fromDegrees(-105.0, 40.0, 1500.0);
const geo = Cartographic.fromCartesian(position);
const lonDeg = CesiumMath.toDegrees(geo.longitude); // -105.0
const latDeg = CesiumMath.toDegrees(geo.latitude);  // 40.0
const backToCart = Cartographic.toCartesian(geo);
```

## CesiumMath Utilities

```js
import { Math as CesiumMath } from "cesium";

// Degree/radian conversion
const rad = CesiumMath.toRadians(90.0);    // PI/2
const deg = CesiumMath.toDegrees(Math.PI); // 180

// Constants: PI, TWO_PI, PI_OVER_TWO, PI_OVER_FOUR, RADIANS_PER_DEGREE
// EPSILON1 (0.1) through EPSILON21 (1e-21)

const clamped = CesiumMath.clamp(value, 0.0, 1.0);
const interp = CesiumMath.lerp(0.0, 100.0, 0.5);          // 50
const norm = CesiumMath.negativePiToPi(angle);              // [-PI, PI]
const pos = CesiumMath.zeroToTwoPi(angle);                  // [0, 2*PI]
const safeLon = CesiumMath.convertLongitudeRange(angle);    // [-PI, PI)
const eq = CesiumMath.equalsEpsilon(a, b, CesiumMath.EPSILON7); // float compare
```

## Ellipsoid

```js
import { Ellipsoid, Cartesian3, Cartographic } from "cesium";

// Built-in ellipsoids
Ellipsoid.WGS84;       // Earth (default)
Ellipsoid.UNIT_SPHERE;  // radius 1
Ellipsoid.MOON;         // lunar sphere
Ellipsoid.MARS;         // Mars (v1.133+)

// Change default (affects Ellipsoid.default everywhere)
Ellipsoid.default = Ellipsoid.MOON;

// Conversions on a specific ellipsoid
const cart = Ellipsoid.WGS84.cartographicToCartesian(
  Cartographic.fromDegrees(-75.0, 40.0, 100.0),
);
const carto = Ellipsoid.WGS84.cartesianToCartographic(cart);

// Surface normal at a position
const normal = Ellipsoid.WGS84.geodeticSurfaceNormal(cart, new Cartesian3());

// Project point onto ellipsoid surface
const onSurface = Ellipsoid.WGS84.scaleToGeodeticSurface(cart, new Cartesian3());
```

## Transforms -- Reference Frames

`Transforms` builds 4x4 matrices relating local frames to ECEF. The most commonly used function is `eastNorthUpToFixedFrame`.

### East-North-Up (ENU)

ENU: X = east, Y = north, Z = up. Standard frame for placing models on the globe.

```js
import { Cartesian3, Transforms, Matrix4 } from "cesium";

const origin = Cartesian3.fromDegrees(-105.0, 40.0);
const enuMatrix = Transforms.eastNorthUpToFixedFrame(origin);
// Columns: [east, north, up, origin] in ECEF
```

### Heading-Pitch-Roll Model Matrix

Standard way to position and orient a 3D model.

```js
import { Cartesian3, Transforms, HeadingPitchRoll, Math as CesiumMath } from "cesium";

const position = Cartesian3.fromDegrees(-105.0, 40.0, 0.0);
const hpr = new HeadingPitchRoll(
  CesiumMath.toRadians(90.0), // heading: 90 deg east
  0.0,                         // pitch: level
  0.0,                         // roll: none
);
const modelMatrix = Transforms.headingPitchRollToFixedFrame(position, hpr);

// Just the orientation quaternion (e.g., for Entity.orientation)
const orientation = Transforms.headingPitchRollQuaternion(position, hpr);
```

### HeadingPitchRoll

Heading = rotation about -Z (compass bearing, clockwise). Pitch = about -Y. Roll = about +X. Radians.

```js
import { HeadingPitchRoll, Math as CesiumMath } from "cesium";
const hpr = new HeadingPitchRoll(CesiumMath.toRadians(45.0), CesiumMath.toRadians(-10.0), 0.0);
const hprDeg = HeadingPitchRoll.fromDegrees(45.0, -10.0, 0.0); // convenience
```

### Other Local Frames

```js
import { Transforms, Cartesian3 } from "cesium";
const origin = Cartesian3.fromDegrees(-105.0, 40.0);

Transforms.northEastDownToFixedFrame(origin);  // NED (aviation)
Transforms.northUpEastToFixedFrame(origin);     // NUE

// Custom frame from any combo of east|north|up|west|south|down
const customFn = Transforms.localFrameToFixedFrameGenerator("north", "west");
const matrix = customFn(origin);

// Recover heading/pitch/roll from an existing model matrix
const hpr = Transforms.fixedFrameToHeadingPitchRoll(modelMatrix);
```

## Matrix4 -- 4x4 Transforms

Column-major storage (WebGL convention). Constructor takes row-major for readability.

```js
import { Matrix4, Matrix3, Cartesian3, Quaternion } from "cesium";

// Factory methods
Matrix4.fromTranslation(new Cartesian3(10, 20, 30));
Matrix4.fromRotationTranslation(Matrix3.fromRotationZ(Math.PI / 4), new Cartesian3(100, 0, 0));
Matrix4.fromTranslationQuaternionRotationScale(
  new Cartesian3(0, 0, 0), Quaternion.IDENTITY, new Cartesian3(2, 2, 2),
);
Matrix4.fromUniformScale(5.0);

// Combine, transform, invert
const combined = Matrix4.multiply(matA, matB, new Matrix4());
const worldPt = Matrix4.multiplyByPoint(enuMatrix, new Cartesian3(100, 0, 0), new Cartesian3());
const inv = Matrix4.inverseTransformation(enuMatrix, new Matrix4()); // rigid-body only

// Decompose
Matrix4.getTranslation(enuMatrix, new Cartesian3());
Matrix4.getMatrix3(enuMatrix, new Matrix3());
Matrix4.getScale(enuMatrix, new Cartesian3());
```

## Quaternion -- Rotation

```js
import { Quaternion, Cartesian3, HeadingPitchRoll, Math as CesiumMath, Matrix3 } from "cesium";

Quaternion.IDENTITY; // (0, 0, 0, 1)
const q1 = Quaternion.fromAxisAngle(Cartesian3.UNIT_Z, CesiumMath.toRadians(45.0));
const q2 = Quaternion.fromHeadingPitchRoll(new HeadingPitchRoll(CesiumMath.toRadians(90), 0, 0));
const q3 = Quaternion.fromRotationMatrix(Matrix3.fromRotationZ(Math.PI / 2));
const mid = Quaternion.slerp(q1, q2, 0.5, new Quaternion());       // interpolate
const composed = Quaternion.multiply(q1, q2, new Quaternion());     // compose
```

## Geodesic Distance

```js
import { Cartographic, EllipsoidGeodesic, Cartesian3 } from "cesium";

// Surface distance (great-circle via Vincenty)
const geodesic = new EllipsoidGeodesic(
  Cartographic.fromDegrees(-73.985, 40.758),  // New York
  Cartographic.fromDegrees(-0.1276, 51.5074), // London
);
const surfaceDist = geodesic.surfaceDistance;              // ~5,570 km
const midCarto = geodesic.interpolateUsingFraction(0.5);  // midpoint on surface

// Chord (straight-line) distance
const chord = Cartesian3.distance(Cartesian3.fromDegrees(-105, 40), Cartesian3.fromDegrees(-104, 40));
```

## BoundingSphere

```js
import { BoundingSphere, Cartesian3 } from "cesium";

const sphere = BoundingSphere.fromPoints(
  Cartesian3.fromDegreesArray([-105, 40, -100, 40, -100, 35]),
); // sphere.center (Cartesian3), sphere.radius (number)

const inside = Cartesian3.distance(sphere.center, Cartesian3.fromDegrees(-102, 37.5)) <= sphere.radius;
```

## Ray and Intersection Tests

```js
import { Ray, IntersectionTests, Plane, Cartesian3, Ellipsoid } from "cesium";

const ray = new Ray(new Cartesian3(0, 0, 6378137), new Cartesian3(0, 0, -1)); // auto-normalized
const ptOnRay = Ray.getPoint(ray, 1000.0, new Cartesian3());

// Ray-plane: returns Cartesian3 or undefined
const plane = Plane.fromPointNormal(Cartesian3.ZERO, Cartesian3.UNIT_Z);
const hit = IntersectionTests.rayPlane(ray, plane);

// Ray-ellipsoid: returns Interval {start, stop} or undefined
const camRay = new Ray(new Cartesian3(0, 0, 20000000), new Cartesian3(0, 0, -1));
const interval = IntersectionTests.rayEllipsoid(camRay, Ellipsoid.WGS84);
if (interval) {
  const nearPt = Ray.getPoint(camRay, interval.start, new Cartesian3());
}

// Ray-triangle: returns parametric t or undefined
const t = IntersectionTests.rayTriangleParametric(ray, p0, p1, p2, true);
```

## SceneTransforms -- World to Screen

```js
import { SceneTransforms, Cartesian3 } from "cesium";
// World -> pixel coordinates (Cartesian2 or undefined if off-screen)
const winPos = SceneTransforms.worldToWindowCoordinates(viewer.scene, Cartesian3.fromDegrees(-105, 40));
// High-DPI aware variant
const bufPos = SceneTransforms.worldToDrawingBufferCoordinates(viewer.scene, worldPos);
```

## Geographic Projections

```js
import { GeographicProjection, WebMercatorProjection, Cartographic, Ellipsoid } from "cesium";
const carto = Cartographic.fromDegrees(-105.0, 40.0);

// Plate Carree: project/unproject between Cartographic and Cartesian3
const geoProj = new GeographicProjection(Ellipsoid.WGS84);
const xy = geoProj.project(carto);           // Cartesian3
const back = geoProj.unproject(xy);          // Cartographic

// Web Mercator (EPSG:3857)
const merc = new WebMercatorProjection(Ellipsoid.WGS84);
const mercXY = merc.project(carto);
```

## Common Patterns

### Offset a Position in Local ENU

```js
import { Cartesian3, Transforms, Matrix4 } from "cesium";

const origin = Cartesian3.fromDegrees(-105.0, 40.0, 0.0);
const enu = Transforms.eastNorthUpToFixedFrame(origin);
// Move 500m east, 200m north, 100m up in local frame
const worldPt = Matrix4.multiplyByPoint(enu, new Cartesian3(500, 200, 100), new Cartesian3());
```

### Compare Positions with Tolerance

```js
import { Cartesian3, Math as CesiumMath } from "cesium";
const a = Cartesian3.fromDegrees(-105.0, 40.0);
const b = Cartesian3.fromDegrees(-105.0001, 40.0001);
Cartesian3.equalsEpsilon(a, b, CesiumMath.EPSILON7); // preferred over ===
if (Cartesian3.distance(a, b) < 10.0) { /* within 10m */ }
```

## Performance Tips

1. **Reuse scratch variables.** Pre-allocate `result` objects outside loops to avoid GC pauses.
2. **Use `distanceSquared`** instead of `distance` when comparing -- avoids `Math.sqrt`.
3. **Prefer `Cartesian3.fromDegrees`** over manual Cartographic creation then conversion.
4. **Cache model matrices.** Call `Transforms.eastNorthUpToFixedFrame` once if position is static.
5. **Use `Matrix4.inverseTransformation`** for rigid-body transforms -- faster and more stable than `inverse`.
6. **Batch position creation** with `fromDegreesArray` / `fromDegreesArrayHeights` instead of looping `fromDegrees`.
7. **Guard `Cartesian3.normalize`** -- it throws on zero-length vectors. Check magnitude first.
8. **Use `equalsEpsilon`** for float comparisons. `CesiumMath.EPSILON7` is a good default tolerance.
9. **Pre-compute HPR** outside render loops. Convert to quaternion/matrix only when orientation changes.
10. **Choose the right distance.** `Cartesian3.distance` = chord through Earth. `EllipsoidGeodesic.surfaceDistance` = great-circle.

## See Also

- **cesiumjs-camera** -- Camera positioning and flight animations that consume these coordinate types
- **cesiumjs-primitives** -- Geometry and Primitive API that uses model matrices from Transforms
- **cesiumjs-terrain-environment** -- Terrain height queries and globe surface interactions
