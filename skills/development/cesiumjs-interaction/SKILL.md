---
name: cesiumjs-interaction
description: "CesiumJS interaction and picking - ScreenSpaceEventHandler, Scene.pick, Scene.drillPick, Scene.pickPosition, mouse and touch events. Use when handling user clicks on the globe, selecting entities or 3D Tiles features, implementing hover effects, or building drag-based interactions."
---
# CesiumJS Interaction & Picking

Version baseline: CesiumJS v1.139 (ES module imports, Ion token required).

## ScreenSpaceEventHandler

Central class for mouse, touch, and pointer events on the Cesium canvas.

```js
import { ScreenSpaceEventHandler, ScreenSpaceEventType,
  KeyboardEventModifier, defined } from "cesium";

const handler = new ScreenSpaceEventHandler(viewer.scene.canvas);

// Register a click handler
handler.setInputAction((event) => {
  console.log("Clicked at", event.position.x, event.position.y);
}, ScreenSpaceEventType.LEFT_CLICK);

// With keyboard modifier (Shift+Click)
handler.setInputAction((event) => {
  console.log("Shift+Click at", event.position);
}, ScreenSpaceEventType.LEFT_CLICK, KeyboardEventModifier.SHIFT);

// Query or remove actions
const action = handler.getInputAction(ScreenSpaceEventType.LEFT_CLICK);
handler.removeInputAction(ScreenSpaceEventType.LEFT_CLICK);

// Always destroy when done to avoid memory leaks
handler = handler && handler.destroy();
```

The Viewer also has a built-in handler at `viewer.screenSpaceEventHandler` -- use it to avoid creating a second handler for simple cases.

## ScreenSpaceEventType Reference

| Event | Callback shape | Notes |
|---|---|---|
| `LEFT_DOWN` / `LEFT_UP` / `LEFT_CLICK` | `({ position })` | Cartesian2 screen coords |
| `LEFT_DOUBLE_CLICK` | `({ position })` | Left only |
| `RIGHT_DOWN` / `RIGHT_UP` / `RIGHT_CLICK` | `({ position })` | |
| `MIDDLE_DOWN` / `MIDDLE_UP` / `MIDDLE_CLICK` | `({ position })` | |
| `MOUSE_MOVE` | `({ startPosition, endPosition })` | Fires on every pointer move |
| `WHEEL` | `(delta)` | Positive = scroll up |
| `PINCH_START` | `({ position1, position2 })` | Two-finger touch begins |
| `PINCH_END` | `()` | Two-finger touch ends |
| `PINCH_MOVE` | `({ distance, angleAndHeight })` | Two-finger move |

`KeyboardEventModifier`: `SHIFT`, `CTRL`, `ALT` -- optional third argument to `setInputAction`.

## Scene Picking Methods

### pick / pickAsync / drillPick / pickPosition

```js
import { Cartographic, Math as CesiumMath, defined } from "cesium";

// pick -- synchronous, returns top-most object or undefined
const picked = viewer.scene.pick(event.position);

// pickAsync -- non-blocking (WebGL2, v1.136+), falls back to sync on WebGL1
const picked2 = await viewer.scene.pickAsync(movement.endPosition);

// drillPick -- all objects at position, front-to-back; use limit to cap cost
const allPicked = viewer.scene.drillPick(event.position, 5);

// pickPosition -- world Cartesian3 from depth buffer
if (viewer.scene.pickPositionSupported) {
  const cartesian = viewer.scene.pickPosition(event.position);
  if (defined(cartesian)) {
    const c = Cartographic.fromCartesian(cartesian);
    console.log(CesiumMath.toDegrees(c.longitude), CesiumMath.toDegrees(c.latitude), c.height);
  }
}
```

Set `scene.pickTranslucentDepth = true` to include translucent primitives in `pickPosition`.

### pickVoxel (experimental)

```js
// Pick a voxel cell and read its properties
const voxelCell = viewer.scene.pickVoxel(event.position);
if (defined(voxelCell)) {
  console.log(voxelCell.getProperty("temperature"));
}
```

### Picking Return Values

| Picked object | Return shape | Key properties |
|---|---|---|
| Entity | `{ primitive, id }` | `id` is the `Entity` instance |
| Cesium3DTileFeature | `Cesium3DTileFeature` | `.getProperty(name)`, `.getPropertyIds()`, `.color` |
| Billboard/Label (collection) | `{ primitive, id }` | `id` is the user-set id |
| Primitive (geometry) | `{ primitive, id }` | `id` is the `GeometryInstance` id |
| Globe surface | `undefined` | Use `camera.pickEllipsoid()` or `pickPosition()` |

## Recipes

### 1. Entity Selection with Click

```js
handler.setInputAction((event) => {
  const picked = viewer.scene.pick(event.position);
  if (defined(picked) && defined(picked.id)) {
    viewer.selectedEntity = picked.id; // shows InfoBox
  } else {
    viewer.selectedEntity = undefined;
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

### 2. 3D Tiles Feature Picking and Property Inspection

```js
import { Cesium3DTileFeature, Color } from "cesium";

handler.setInputAction((event) => {
  const picked = viewer.scene.pick(event.position);
  if (picked instanceof Cesium3DTileFeature) {
    // Read properties
    const ids = picked.getPropertyIds();
    ids.forEach((id) => console.log(`${id}: ${picked.getProperty(id)}`));
    picked.color = Color.YELLOW; // highlight
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

### 3. Terrain Position Picking (Lon/Lat from Click)

```js
handler.setInputAction((event) => {
  const cartesian = viewer.camera.pickEllipsoid(
    event.position, viewer.scene.globe.ellipsoid);
  if (defined(cartesian)) {
    const c = Cartographic.fromCartesian(cartesian);
    console.log(`Lon: ${CesiumMath.toDegrees(c.longitude).toFixed(6)}`);
    console.log(`Lat: ${CesiumMath.toDegrees(c.latitude).toFixed(6)}`);
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

For height on 3D content, use `scene.pickPosition` instead (see above).

### 4. Multi-Pick with drillPick

```js
import { EntityCollection, CallbackProperty, ColorMaterialProperty, Color } from "cesium";

const pickedEntities = new EntityCollection();
const highlightColor = Color.YELLOW.withAlpha(0.5);

// Make entity material react to selection state
function makePickable(entity, baseColor) {
  entity.polygon.material = new ColorMaterialProperty(
    new CallbackProperty((time, result) => {
      return pickedEntities.contains(entity)
        ? highlightColor.clone(result) : baseColor.clone(result);
    }, false));
}

handler.setInputAction((movement) => {
  const all = viewer.scene.drillPick(movement.endPosition);
  pickedEntities.removeAll();
  for (const p of all) {
    if (defined(p.id)) pickedEntities.add(p.id);
  }
}, ScreenSpaceEventType.MOUSE_MOVE);
```

### 5. Hover Highlighting with MOUSE_MOVE

```js
import { Color } from "cesium";

const highlighted = { feature: undefined, originalColor: new Color() };

handler.setInputAction((movement) => {
  if (defined(highlighted.feature)) {
    highlighted.feature.color = highlighted.originalColor;
    highlighted.feature = undefined;
  }
  const picked = viewer.scene.pick(movement.endPosition);
  if (defined(picked) && defined(picked.color)) {
    highlighted.feature = picked;
    Color.clone(picked.color, highlighted.originalColor);
    picked.color = Color.YELLOW;
  }
}, ScreenSpaceEventType.MOUSE_MOVE);
```

### 6. Drag-Based Drawing and Measurement

```js
import { Cartographic, EllipsoidGeodesic, Ellipsoid, Color } from "cesium";

const positions = [];

handler.setInputAction((event) => {
  const cartesian = viewer.camera.pickEllipsoid(
    event.position, viewer.scene.globe.ellipsoid);
  if (!defined(cartesian)) return;
  positions.push(cartesian);

  if (positions.length === 2) {
    viewer.entities.add({
      polyline: { positions: positions.slice(), width: 3,
        material: Color.RED, clampToGround: true },
    });
    const start = Cartographic.fromCartesian(positions[0]);
    const end = Cartographic.fromCartesian(positions[1]);
    const geodesic = new EllipsoidGeodesic(start, end, Ellipsoid.WGS84);
    console.log(`Distance: ${(geodesic.surfaceDistance / 1000).toFixed(2)} km`);
    positions.length = 0;
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

### 7. Coordinate Readout on Mouse Move

```js
import { HorizontalOrigin, VerticalOrigin, Cartesian2 } from "cesium";

const coordLabel = viewer.entities.add({
  label: { show: false, showBackground: true, font: "14px monospace",
    horizontalOrigin: HorizontalOrigin.LEFT, verticalOrigin: VerticalOrigin.TOP,
    pixelOffset: new Cartesian2(15, 0) },
});

handler.setInputAction((movement) => {
  const cartesian = viewer.camera.pickEllipsoid(
    movement.endPosition, viewer.scene.globe.ellipsoid);
  if (defined(cartesian)) {
    const c = Cartographic.fromCartesian(cartesian);
    coordLabel.position = cartesian;
    coordLabel.label.show = true;
    coordLabel.label.text =
      `Lon: ${CesiumMath.toDegrees(c.longitude).toFixed(4)}\n` +
      `Lat: ${CesiumMath.toDegrees(c.latitude).toFixed(4)}`;
  } else {
    coordLabel.label.show = false;
  }
}, ScreenSpaceEventType.MOUSE_MOVE);
```

### 8. Conditional Behavior Based on Picked Object Type

```js
import { Cesium3DTileFeature } from "cesium";

handler.setInputAction((event) => {
  const picked = viewer.scene.pick(event.position);
  if (!defined(picked)) {
    console.log("No object picked");
  } else if (picked instanceof Cesium3DTileFeature) {
    console.log("3D Tile feature:", picked.getProperty("name"));
  } else if (defined(picked.id) && defined(picked.id.position)) {
    viewer.selectedEntity = picked.id; // Entity
  } else if (defined(picked.primitive)) {
    console.log("Primitive:", picked.primitive.constructor.name);
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

### 9. pickAsync for Non-Blocking Hover (v1.136+)

```js
const highlighted = { feature: undefined, originalColor: new Color() };

handler.setInputAction(async (movement) => {
  if (defined(highlighted.feature)) {
    highlighted.feature.color = highlighted.originalColor;
    highlighted.feature = undefined;
  }
  const picked = await viewer.scene.pickAsync(movement.endPosition);
  if (defined(picked) && defined(picked.color)) {
    highlighted.feature = picked;
    Color.clone(picked.color, highlighted.originalColor);
    picked.color = Color.YELLOW;
  }
}, ScreenSpaceEventType.MOUSE_MOVE);
```

### 10. Hover + Selection with Silhouettes (Full Pattern)

```js
import { PostProcessStageLibrary, Color } from "cesium";

const scene = viewer.scene;
const silhouetteHover = PostProcessStageLibrary.createEdgeDetectionStage();
silhouetteHover.uniforms.color = Color.BLUE;
silhouetteHover.uniforms.length = 0.01;
silhouetteHover.selected = [];

const silhouetteSelect = PostProcessStageLibrary.createEdgeDetectionStage();
silhouetteSelect.uniforms.color = Color.LIME;
silhouetteSelect.uniforms.length = 0.01;
silhouetteSelect.selected = [];

scene.postProcessStages.add(
  PostProcessStageLibrary.createSilhouetteStage([silhouetteHover, silhouetteSelect]));

let selectedFeature;

viewer.screenSpaceEventHandler.setInputAction((movement) => {
  silhouetteHover.selected = [];
  const picked = scene.pick(movement.endPosition);
  if (defined(picked) && picked !== selectedFeature) {
    silhouetteHover.selected = [picked];
  }
}, ScreenSpaceEventType.MOUSE_MOVE);

viewer.screenSpaceEventHandler.setInputAction((event) => {
  silhouetteSelect.selected = [];
  const picked = scene.pick(event.position);
  if (defined(picked)) {
    selectedFeature = picked;
    silhouetteSelect.selected = [picked];
    silhouetteHover.selected = [];
  } else {
    selectedFeature = undefined;
  }
}, ScreenSpaceEventType.LEFT_CLICK);
```

### 11. Wheel Zoom with Custom Logic

```js
handler.setInputAction((delta) => {
  // delta > 0 = scroll up (zoom in), delta < 0 = scroll out
  const zoomAmount = delta > 0 ? 0.9 : 1.1;
  viewer.camera.zoomIn(viewer.camera.positionCartographic.height * (1 - zoomAmount));
}, ScreenSpaceEventType.WHEEL);
```

### 12. Right-Click Context Menu

```js
viewer.scene.canvas.addEventListener("contextmenu", (e) => e.preventDefault());

handler.setInputAction((event) => {
  const picked = viewer.scene.pick(event.position);
  if (defined(picked) && defined(picked.id)) {
    showContextMenu(event.position, picked.id); // your app logic
  }
}, ScreenSpaceEventType.RIGHT_CLICK);
```

### 13. Drag Interaction (Move an Entity)

```js
let draggedEntity = null;
const sscc = viewer.scene.screenSpaceCameraController;

handler.setInputAction((event) => {
  const picked = viewer.scene.pick(event.position);
  if (defined(picked) && defined(picked.id)) {
    draggedEntity = picked.id;
    sscc.enableRotate = false;
    sscc.enableTranslate = false;
  }
}, ScreenSpaceEventType.LEFT_DOWN);

handler.setInputAction((movement) => {
  if (!defined(draggedEntity)) return;
  const cartesian = viewer.camera.pickEllipsoid(
    movement.endPosition, viewer.scene.globe.ellipsoid);
  if (defined(cartesian)) draggedEntity.position = cartesian;
}, ScreenSpaceEventType.MOUSE_MOVE);

handler.setInputAction(() => {
  draggedEntity = null;
  sscc.enableRotate = true;
  sscc.enableTranslate = true;
}, ScreenSpaceEventType.LEFT_UP);
```

## Performance Tips

1. **Prefer `pickAsync` over `pick` on MOUSE_MOVE** -- synchronous pick stalls the GPU pipeline; `pickAsync` yields to the GPU and resolves next frame (WebGL2, v1.136+).
2. **Use `drillPick` with a `limit`** -- without one, it re-renders the scene for every overlapping object.
3. **Avoid `pick` in MOUSE_MOVE when only click picking is needed** -- MOUSE_MOVE fires on every pointer move and triggers a pick render pass each time.
4. **Enable `depthTestAgainstTerrain`** for accurate `pickPosition` results over terrain.
5. **Destroy unused handlers** -- each one registers DOM listeners that leak memory if not cleaned up.
6. **Throttle expensive hover logic** -- debounce to 50-100ms for operations beyond simple highlighting.
7. **Check `scene.pickPositionSupported`** before using `pickPosition` -- falls back to `camera.pickEllipsoid` on unsupported GPUs.
8. **Set `scene.pickTranslucentDepth = true` only when needed** -- adds an extra render pass.
9. **Reuse result objects** -- pass a scratch `Cartesian3` to `pickPosition` to avoid GC pressure in MOUSE_MOVE.
10. **Use `scene.requestRenderMode = true`** with picking to avoid unnecessary renders; call `scene.requestRender()` only on state changes.

## See Also

- **cesiumjs-entities** -- Entity API, graphics types, DataSources
- **cesiumjs-3d-tiles** -- Cesium3DTileset, Cesium3DTileFeature, styling, metadata
- **cesiumjs-camera** -- Camera.pickEllipsoid, ScreenSpaceCameraController, flyTo
