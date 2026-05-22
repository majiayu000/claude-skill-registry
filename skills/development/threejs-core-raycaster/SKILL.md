---
name: threejs-core-raycaster
description: >
  Use when implementing mouse picking, hover detection, object selection,
  or line-of-sight checks in Three.js. Prevents the common mistake of
  raycasting every mousemove frame, not using layers for filtering, or
  missing recursive flag. Covers Raycaster, setFromCamera, intersection
  format, InstancedMesh picking, layers, performance.
  Keywords: Raycaster, mouse picking, intersectObjects, click, hover,
  setFromCamera, intersection, instanceId, object selection.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-core-raycaster

## Quick Reference

### Raycaster Constructor

```javascript
import * as THREE from 'three';

const raycaster = new THREE.Raycaster(
  origin,     // Vector3 — default: (0, 0, 0)
  direction,  // Vector3 — MUST be normalized, default: (0, 0, -1)
  near,       // number — minimum distance, default: 0
  far         // number — maximum distance, default: Infinity
);
```

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ray` | `Ray` | -- | Underlying Ray object (origin + direction) |
| `near` | `number` | `0` | Minimum intersection distance |
| `far` | `number` | `Infinity` | Maximum intersection distance |
| `camera` | `Camera` | -- | Required for raycasting against `Sprite` objects |
| `layers` | `Layers` | layer 0 | Layer mask -- only objects on matching layers are tested |
| `params` | `object` | see below | Per-type intersection thresholds |

### Params Defaults

```javascript
raycaster.params = {
  Mesh: {},
  Line: { threshold: 1 },    // world units distance for line hits
  LOD: {},
  Points: { threshold: 1 },  // world units distance for point hits
  Sprite: {}
};
```

### Critical Warnings

**NEVER** raycast on every `mousemove` event without throttling -- this causes severe frame drops on complex scenes. ALWAYS throttle to the render loop via `requestAnimationFrame` or limit to 30-60 checks per second.

**NEVER** pass `recursive: true` on large scene graphs when you have a flat array of target objects -- ALWAYS maintain a flat array of selectable objects and pass `recursive: false` to avoid unnecessary tree traversal.

**NEVER** forget to normalize the direction vector when using `raycaster.set()` -- an unnormalized direction produces incorrect distance values in all intersection results.

**NEVER** allocate a new results array every frame -- ALWAYS reuse an array via the `optionalTarget` parameter and clear it with `array.length = 0` after processing.

**NEVER** raycast against the entire `scene.children` when only a subset of objects is interactive -- ALWAYS maintain a separate array of selectable objects or use layers for filtering.

**NEVER** omit `raycaster.camera` when raycasting against `Sprite` objects -- the raycaster requires the camera reference to compute sprite screen-space bounds.

---

## Core Methods

### set(origin, direction)

Manually sets the ray origin and direction. Direction MUST be normalized.

```javascript
const origin = new THREE.Vector3(0, 1, 0);
const direction = new THREE.Vector3(0, -1, 0); // already normalized
raycaster.set(origin, direction);
```

### setFromCamera(coords, camera)

Sets the ray from normalized device coordinates (NDC) and a camera. This is the standard mouse-picking method.

- `coords`: `Vector2` with x and y in range [-1, +1]
- `camera`: `PerspectiveCamera` produces a ray from the camera through the point; `OrthographicCamera` produces a parallel ray

```javascript
const mouse = new THREE.Vector2();
mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
raycaster.setFromCamera(mouse, camera);
```

### intersectObject(object, recursive?, optionalTarget?)

Tests a single object (and optionally its descendants) for intersections.

- `recursive` (default: `true`): when `true`, tests all descendants
- `optionalTarget`: reusable array to avoid allocation
- Returns: `Intersection[]` ALWAYS sorted by distance (nearest first)

### intersectObjects(objects, recursive?, optionalTarget?)

Tests an array of objects for intersections.

- `recursive` (default: `true`): when `true`, tests descendants of each object
- `optionalTarget`: reusable array to avoid allocation
- Returns: `Intersection[]` ALWAYS sorted by distance (nearest first)

---

## Intersection Object Format

Every intersection in the returned array has this structure:

```typescript
interface Intersection {
  distance: number;       // distance from ray origin to hit point
  point: Vector3;         // hit point in world space
  face: Face | null;      // hit face ({a, b, c} vertex indices + normal)
  faceIndex: number;      // index of hit face in the geometry
  object: Object3D;       // the intersected object reference
  uv?: Vector2;           // UV coordinates at intersection point
  uv1?: Vector2;          // second UV set (if available)
  normal?: Vector3;       // interpolated surface normal at hit point
  instanceId?: number;    // instance index (only for InstancedMesh)
}
```

ALWAYS check `intersects.length > 0` before accessing `intersects[0]`. The array is empty when no objects are hit.

---

## NDC Conversion (Normalized Device Coordinates)

Converting DOM mouse coordinates to NDC is required for `setFromCamera`. The NDC space ranges from -1 (left/bottom) to +1 (right/top).

```javascript
// For fullscreen canvas (canvas fills entire window)
mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

// For non-fullscreen canvas (canvas has offset within page)
const rect = renderer.domElement.getBoundingClientRect();
mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
```

ALWAYS use `getBoundingClientRect()` when the canvas does NOT fill the entire viewport. Using `window.innerWidth/Height` on a partial canvas produces incorrect NDC values and misaligned picking.

---

## InstancedMesh Picking

When raycasting against `InstancedMesh`, the intersection result includes `instanceId` identifying which instance was hit:

```javascript
import * as THREE from 'three';

const intersects = raycaster.intersectObject(instancedMesh);
if (intersects.length > 0) {
  const instanceId = intersects[0].instanceId;
  // Retrieve the instance's transform matrix
  const matrix = new THREE.Matrix4();
  instancedMesh.getMatrixAt(instanceId, matrix);

  // Example: change the color of the hit instance
  const color = new THREE.Color();
  instancedMesh.getColorAt(instanceId, color);
  instancedMesh.setColorAt(instanceId, new THREE.Color(0xff0000));
  instancedMesh.instanceColor.needsUpdate = true;
}
```

ALWAYS check that `instanceId !== undefined` before using it -- non-InstancedMesh objects do not have this property.

---

## Layer Filtering

Raycaster respects the `Layers` system. Only objects whose layers overlap with `raycaster.layers` are tested.

```javascript
// Assign objects to layers
selectableMesh.layers.set(1);        // exclusively on layer 1
decorationMesh.layers.set(2);        // exclusively on layer 2

// Configure raycaster to only test layer 1
raycaster.layers.set(1);
// Now intersectObjects skips all objects NOT on layer 1

// Enable multiple layers
raycaster.layers.enable(1);
raycaster.layers.enable(2);
// Now tests objects on layer 1 OR layer 2

// Reset to default (layer 0 only)
raycaster.layers.set(0);
```

Use layers to create picking groups: interactive objects on layer 1, non-interactive decoration on layer 2, helpers/gizmos on layer 3.

---

## Performance Guidelines

1. **Throttle mousemove raycasting** -- NEVER raycast on every `mousemove` event. Use a flag checked in the render loop:
   ```javascript
   let needsRaycast = false;
   canvas.addEventListener('pointermove', (event) => {
     mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
     mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
     needsRaycast = true;
   });

   function animate() {
     if (needsRaycast) {
       raycaster.setFromCamera(mouse, camera);
       // perform intersection tests
       needsRaycast = false;
     }
     renderer.render(scene, camera);
     requestAnimationFrame(animate);
   }
   ```

2. **Use layers** -- assign interactive objects to a specific layer and set `raycaster.layers` accordingly to skip non-interactive geometry entirely.

3. **Maintain a flat selectable array** -- instead of raycasting against `scene` with `recursive: true`, keep a separate `selectableObjects[]` array and pass `recursive: false`.

4. **Reuse the intersections array** -- pass `optionalTarget` to avoid garbage collection:
   ```javascript
   const intersections = [];
   raycaster.intersectObjects(selectableObjects, false, intersections);
   // process results...
   intersections.length = 0;
   ```

5. **Bounding sphere pre-check** -- Three.js automatically tests bounding spheres before triangle intersection. Ensure `geometry.computeBoundingSphere()` has been called (it is called automatically on first render, but manual call is needed if raycasting before first render).

6. **Limit `near`/`far`** -- narrow the ray range when you know the expected intersection distance to skip distant objects early.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete Raycaster API signatures
- [references/examples.md](references/examples.md) -- Working code examples for picking, hover, and InstancedMesh
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with raycasting

### Official Sources

- https://threejs.org/docs/#api/en/core/Raycaster
- https://threejs.org/docs/#api/en/core/Layers
