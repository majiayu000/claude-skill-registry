---
name: cesiumjs-time-properties
description: "CesiumJS time, properties, and animation - Clock, JulianDate, TimeInterval, Property, SampledProperty, CallbackProperty, interpolation, splines, CZML temporal data. Use when making entity attributes time-dynamic, configuring the simulation clock, interpolating positions over time, or working with sampled or callback properties."
---
# CesiumJS Time, Properties & Animation

Version baseline: CesiumJS v1.139.1

Covers the temporal data-binding layer: Clock/JulianDate time system, the Property hierarchy that makes entity attributes change over time, interpolation algorithms, splines, and material properties. Properties live here (not with Entities) because SampledProperty and CallbackProperty are meaningless without Clock/JulianDate. The Material class (Fabric) belongs in cesiumjs-materials-shaders.

## JulianDate -- The Time Primitive

Stores whole days + fractional seconds separately for precision. Always uses TAI internally.

```js
import { JulianDate } from "cesium";

// Creation: fromIso8601 (most common), fromDate, now
const date = JulianDate.fromIso8601("2025-06-15T12:00:00Z");
const jd = JulianDate.fromDate(new Date("2025-06-15T12:00:00Z"));
const now = JulianDate.now();

// Conversion: toIso8601, toDate, toGregorianDate
const iso = JulianDate.toIso8601(date); // "2025-06-15T12:00:00Z"
const greg = JulianDate.toGregorianDate(date); // {year, month, day, hour, ...}

// Arithmetic -- all require a result parameter to avoid allocations
const r = new JulianDate();
JulianDate.addSeconds(date, 3600, r); // also: addMinutes, addHours, addDays

// Differences and comparisons
const stop = JulianDate.addHours(date, 24, new JulianDate());
JulianDate.secondsDifference(stop, date); // 86400
JulianDate.lessThan(date, stop);          // true
JulianDate.compare(date, stop);           // negative (date < stop)
```

## Clock -- Simulation Time Controller

The Viewer creates a Clock automatically. Configure it to control playback speed and bounds.

```js
import { Viewer, JulianDate, ClockRange, ClockStep } from "cesium";

const viewer = new Viewer("cesiumContainer");
const start = JulianDate.fromIso8601("2025-06-15T00:00:00Z");
const stop = JulianDate.addHours(start, 24, new JulianDate());
viewer.clock.startTime = start.clone();
viewer.clock.stopTime = stop.clone();
viewer.clock.currentTime = start.clone();
viewer.clock.clockRange = ClockRange.LOOP_STOP; // loop at end
viewer.clock.multiplier = 60;                   // 60x real-time
viewer.clock.shouldAnimate = true;
viewer.timeline.zoomTo(start, stop);

viewer.clock.onTick.addEventListener((clock) => { // per-frame callback
  console.log(JulianDate.toIso8601(clock.currentTime));
});
```

| ClockRange | Behavior |
|---|---|
| `UNBOUNDED` | Advances forever in both directions |
| `CLAMPED` | Stops at start/stop time |
| `LOOP_STOP` | Wraps from stop back to start |

| ClockStep | Behavior |
|---|---|
| `TICK_DEPENDENT` | Each tick advances by `multiplier` seconds (frame-dependent) |
| `SYSTEM_CLOCK_MULTIPLIER` | Elapsed wall time x `multiplier` (default) |
| `SYSTEM_CLOCK` | Real-time; ignores multiplier |

## TimeInterval & TimeIntervalCollection

```js
import { TimeInterval, TimeIntervalCollection, JulianDate } from "cesium";

const interval = TimeInterval.fromIso8601({
  iso8601: "2025-06-15T00:00:00Z/2025-06-16T00:00:00Z",
  data: { phase: "daylight" },  // attach arbitrary data
});
TimeInterval.contains(interval, JulianDate.fromIso8601("2025-06-15T12:00:00Z")); // true

// Used by Entity.availability to cull entities outside the time window
const availability = new TimeIntervalCollection([
  new TimeInterval({
    start: JulianDate.fromIso8601("2025-06-15T00:00:00Z"),
    stop: JulianDate.fromIso8601("2025-06-16T00:00:00Z"),
  }),
]);
```

## Property System -- Time-Varying Values

Every entity attribute is a Property. CesiumJS calls `property.getValue(time)` each frame.

### ConstantProperty

Returns the same value regardless of time. CesiumJS auto-wraps raw values, so explicit use is rare.

```js
import { ConstantProperty, Color } from "cesium";
const prop = new ConstantProperty(Color.RED);
prop.setValue(Color.BLUE); // fires definitionChanged
```

### SampledProperty -- Interpolated Time Series

Stores discrete samples and interpolates. Type can be `Number`, `Cartesian3`, `Color`, or any `Packable`.

```js
import { SampledProperty, JulianDate, LagrangePolynomialApproximation, ExtrapolationType } from "cesium";

const prop = new SampledProperty(Number);
const t0 = JulianDate.fromIso8601("2025-06-15T00:00:00Z");
prop.addSample(t0, 1.0);
prop.addSample(JulianDate.addSeconds(t0, 60, new JulianDate()), 2.5);
prop.addSample(JulianDate.addSeconds(t0, 120, new JulianDate()), 1.0);
prop.getValue(JulianDate.addSeconds(t0, 30, new JulianDate())); // ~1.75

// Default: LinearApproximation degree 1. Switch to smoother Lagrange:
prop.setInterpolationOptions({ interpolationDegree: 5, interpolationAlgorithm: LagrangePolynomialApproximation });
prop.forwardExtrapolationType = ExtrapolationType.HOLD; // hold last value outside range
```

### SampledPositionProperty -- Interpolated Positions

Specialized for Cartesian3 positions. Supports reference frames (`ReferenceFrame.FIXED` default, or `INERTIAL`).

```js
import { SampledPositionProperty, JulianDate, Cartesian3, LagrangePolynomialApproximation, ExtrapolationType } from "cesium";

const position = new SampledPositionProperty();
const start = JulianDate.fromIso8601("2025-06-15T00:00:00Z");
for (let i = 0; i <= 360; i += 45) {
  const rad = (i * Math.PI) / 180;
  position.addSample(
    JulianDate.addSeconds(start, i, new JulianDate()),
    Cartesian3.fromDegrees(-112 + 0.045 * Math.cos(rad), 36 + 0.03 * Math.sin(rad), 2000 + Math.random() * 500),
  );
}
position.setInterpolationOptions({ interpolationDegree: 5, interpolationAlgorithm: LagrangePolynomialApproximation });
position.forwardExtrapolationType = ExtrapolationType.HOLD;
```

| Algorithm | Best For | Degree |
|---|---|---|
| `LinearApproximation` | Fast piecewise-linear | 1 (fixed) |
| `LagrangePolynomialApproximation` | Smooth curves from sparse samples | 1--9 |
| `HermitePolynomialApproximation` | Smooth curves with velocity derivatives | 1--9 |

### CallbackProperty -- Computed on Demand

Evaluates a function every frame. Second argument (`isConstant`) must be `false` if value changes.

```js
import { CallbackProperty, Color, JulianDate } from "cesium";

const startTime = JulianDate.now();
const pulse = new CallbackProperty((time, result) => {
  const s = JulianDate.secondsDifference(time, startTime);
  return Color.RED.withAlpha(0.5 + 0.5 * Math.sin(s * 2), result ?? new Color());
}, false);

// Growing polygon -- mutate the array, property auto-updates
const pts = [/* initial Cartesian3[] */];
const dynamicPts = new CallbackProperty(() => pts, false);
```

### CompositeProperty -- Stitching Properties Over Time

Delegates to different sub-properties for different time ranges. Each interval's `data` is a Property.

```js
import { CompositeProperty, ConstantProperty, SampledProperty, TimeInterval, JulianDate } from "cesium";

const composite = new CompositeProperty();
composite.intervals.addInterval(TimeInterval.fromIso8601({
  iso8601: "2025-06-15T00:00:00Z/2025-06-15T12:00:00Z", data: new ConstantProperty(1.0) }));
const sampled = new SampledProperty(Number);
sampled.addSample(JulianDate.fromIso8601("2025-06-15T12:00:00Z"), 1.0);
sampled.addSample(JulianDate.fromIso8601("2025-06-16T00:00:00Z"), 5.0);
composite.intervals.addInterval(TimeInterval.fromIso8601({
  iso8601: "2025-06-15T12:00:00Z/2025-06-16T00:00:00Z", isStartIncluded: false, data: sampled }));
```

### VelocityOrientationProperty -- Auto-Orient Along Path

Computes Quaternion from a position property's velocity. Essential for vehicles and aircraft.

```js
import { VelocityOrientationProperty, SampledPositionProperty } from "cesium";
const position = new SampledPositionProperty();
// ... add samples ...
viewer.entities.add({
  position, orientation: new VelocityOrientationProperty(position),
  model: { uri: "aircraft.glb", minimumPixelSize: 64 },
});
```

### ReferenceProperty -- Cross-Entity Binding

Links one entity's property to another by ID string (`"entityId#propertyPath"`).

```js
import { ReferenceProperty } from "cesium";
viewer.entities.add({ id: "leader", position: Cartesian3.fromDegrees(-75, 40, 1000) });
viewer.entities.add({ id: "follower",
  position: ReferenceProperty.fromString(viewer.entities, "leader#position"),
  point: { pixelSize: 10 } });
```

## Material Properties

Control entity surface appearance. All options accept raw values or Property instances for time-dynamic behavior. Surface types: `ColorMaterialProperty`, `ImageMaterialProperty`, `GridMaterialProperty`, `StripeMaterialProperty`, `CheckerboardMaterialProperty`. Polyline types: `PolylineArrowMaterialProperty`, `PolylineDashMaterialProperty`, `PolylineGlowMaterialProperty`, `PolylineOutlineMaterialProperty`.

```js
import { ColorMaterialProperty, SampledProperty, Color, JulianDate } from "cesium";

const solid = new ColorMaterialProperty(Color.RED);

// Time-varying color via SampledProperty
const colorProp = new SampledProperty(Color);
const t0 = JulianDate.fromIso8601("2025-06-15T00:00:00Z");
colorProp.addSample(t0, Color.BLUE);
colorProp.addSample(JulianDate.addHours(t0, 6, new JulianDate()), Color.RED);
const animated = new ColorMaterialProperty(colorProp);
```

## Splines -- Parametric Curve Interpolation

Splines use unitless parametric time (not JulianDate) for smooth animation curves.

```js
import { HermiteSpline, CatmullRomSpline, Cartesian3 } from "cesium";

// Natural cubic (C2, auto-tangents)
const spline = HermiteSpline.createNaturalCubic({
  times: [0, 1.5, 3, 4.5, 6],
  points: [
    new Cartesian3(1235398, -4810983, 4146266), new Cartesian3(1372574, -5345182, 4606657),
    new Cartesian3(-757983, -5542796, 4514323), new Cartesian3(-2821260, -5248423, 4021290),
    new Cartesian3(-2539788, -4724797, 3620093) ],
});
const point = spline.evaluate(2.0); // evaluate at parametric time t=2

// CatmullRom (C1, auto-tangents from control points)
const catmull = new CatmullRomSpline({ times: [0, 1, 2, 3], points: [p0, p1, p2, p3] });
```

| Spline | Use |
|---|---|
| `LinearSpline` | Piecewise-linear (C0), cheapest |
| `HermiteSpline` | Cubic with tangents (C1+); factories: `createNaturalCubic`, `createClampedCubic`, `createC1` |
| `CatmullRomSpline` | Auto-tangents from control points (C1) |
| `QuaternionSpline` | Rotation interpolation via SLERP (C1) |
| `ConstantSpline` | Single value for all times |
| `SteppedSpline` | Holds value until next control point |
| `MorphWeightSpline` | glTF morph target weights (C1) |

## CZML Temporal Data

CZML streams time-dynamic data. The `document` packet sets the clock; entity packets use `epoch` + offset arrays for compact positions. Position format: `[secondsFromEpoch, lon, lat, alt, ...]`.

```js
import { Viewer, CzmlDataSource } from "cesium";
const czml = [
  { id: "document", version: "1.0", clock: {
      interval: "2025-06-15T00:00:00Z/2025-06-15T06:00:00Z",
      currentTime: "2025-06-15T00:00:00Z", multiplier: 60,
      range: "LOOP_STOP", step: "SYSTEM_CLOCK_MULTIPLIER" } },
  { id: "aircraft", availability: "2025-06-15T00:00:00Z/2025-06-15T06:00:00Z",
    position: { epoch: "2025-06-15T00:00:00Z",
      cartographicDegrees: [0,-75,40,10000, 10800,-88,42,11000, 21600,-118,34,9000],
      interpolationAlgorithm: "LAGRANGE", interpolationDegree: 5 },
    point: { pixelSize: 10, color: { rgba: [255,255,0,255] } } },
];
const ds = await CzmlDataSource.load(czml);
const viewer = new Viewer("cesiumContainer", { shouldAnimate: true });
viewer.dataSources.add(ds);
viewer.zoomTo(ds);
```

## EasingFunction -- Camera Flight Curves

Constants for `camera.flyTo` timing (not Property interpolation). Common values: `LINEAR_NONE`, `CUBIC_IN_OUT`, `QUADRATIC_IN_OUT`. Full set includes `QUARTIC`, `QUINTIC`, `SINUSOIDAL`, `EXPONENTIAL`, `CIRCULAR`, `ELASTIC`, `BACK`, `BOUNCE` variants (each with `_IN`, `_OUT`, `_IN_OUT`).

```js
import { EasingFunction, Cartesian3 } from "cesium";
viewer.camera.flyTo({
  destination: Cartesian3.fromDegrees(-75, 40, 50000),
  duration: 3.0,
  easingFunction: EasingFunction.CUBIC_IN_OUT,
});
```

## Putting It Together: Animated Flight

Combines Clock, SampledPositionProperty, VelocityOrientationProperty, and availability.

```js
import {
  Viewer, JulianDate, ClockRange, SampledPositionProperty, VelocityOrientationProperty,
  TimeIntervalCollection, TimeInterval, Cartesian3, LagrangePolynomialApproximation,
} from "cesium";

const viewer = new Viewer("cesiumContainer", { shouldAnimate: true });
const start = JulianDate.fromIso8601("2025-06-15T16:00:00Z");
const stop = JulianDate.addSeconds(start, 360, new JulianDate());
viewer.clock.startTime = start.clone();
viewer.clock.stopTime = stop.clone();
viewer.clock.currentTime = start.clone();
viewer.clock.clockRange = ClockRange.LOOP_STOP;
viewer.clock.multiplier = 10;
viewer.timeline.zoomTo(start, stop);

const position = new SampledPositionProperty();
for (let i = 0; i <= 360; i += 45) {
  const r = (i * Math.PI) / 180;
  position.addSample(JulianDate.addSeconds(start, i, new JulianDate()),
    Cartesian3.fromDegrees(-112 + 0.045 * Math.cos(r), 36 + 0.03 * Math.sin(r), 2000));
}
position.setInterpolationOptions({ interpolationDegree: 5, interpolationAlgorithm: LagrangePolynomialApproximation });

viewer.trackedEntity = viewer.entities.add({
  availability: new TimeIntervalCollection([new TimeInterval({ start, stop })]),
  position, orientation: new VelocityOrientationProperty(position),
  model: { uri: "aircraft.glb", minimumPixelSize: 64 },
  path: { resolution: 1, width: 10 },
});
```

## Performance Tips

1. Prefer `SampledPositionProperty` over `CallbackProperty` for positions -- binary search is faster than per-frame callbacks.
2. Keep `interpolationDegree` at 5 or below; higher risks Runge's phenomenon with sparse data.
3. Reuse `JulianDate` result parameters in loops to avoid GC pressure.
4. Set entity `availability` to cull entities outside the current time window.
5. In `CallbackProperty`, return the `result` object to avoid allocations.
6. Load bulk temporal data via `CzmlDataSource` -- optimized for batch sample insertion.
7. Use `ExtrapolationType.HOLD` instead of duplicate trailing samples.
8. Use `ClockStep.TICK_DEPENDENT` for deterministic replay; `SYSTEM_CLOCK_MULTIPLIER` varies with frame rate.
9. Minimize `CallbackProperty` count -- each runs its function every frame.

## Key Enums

`ClockRange`: UNBOUNDED, CLAMPED, LOOP_STOP. `ClockStep`: TICK_DEPENDENT, SYSTEM_CLOCK_MULTIPLIER, SYSTEM_CLOCK. `ExtrapolationType`: NONE, HOLD, EXTRAPOLATE. `TimeStandard`: UTC, TAI. `ReferenceFrame`: FIXED, INERTIAL. `TrackingReferenceFrame` (v1.124+): AUTODETECT, ECI, ECEF, INERTIAL, ENU.

## See Also

- **cesiumjs-entities** -- Entity, Graphics types, DataSources (consumers of properties)
- **cesiumjs-viewer-setup** -- Viewer, ClockViewModel, Timeline widget
- **cesiumjs-models-particles** -- Model, ModelAnimation (uses time system for playback)
