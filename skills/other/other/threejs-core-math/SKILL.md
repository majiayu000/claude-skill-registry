---
name: threejs-core-math
description: >
  Use when working with 3D math in Three.js: vectors, matrices,
  quaternions, rotations, colors, or coordinate transforms. Prevents the
  common mistake of mutating shared vectors, using wrong rotation order,
  or confusing Euler gimbal lock. Covers Vector3, Matrix4, Quaternion,
  Euler, Color, MathUtils, Box3, Sphere, coordinate system.
  Keywords: Vector3, Matrix4, Quaternion, Euler, Color, MathUtils,
  lerp, slerp, cross, dot, normalize, degToRad, Y-up, right-handed.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-core-math

## Quick Reference

### Coordinate System

Three.js uses a **right-handed** coordinate system with **Y-up**:

| Axis | Direction | Notes |
|------|-----------|-------|
| **X** | Right | Positive toward screen right |
| **Y** | Up | Positive toward ceiling |
| **Z** | Toward viewer | Positive out of the screen |

**Import conversion rules:**

| Source | Convention | Conversion |
|--------|-----------|------------|
| Blender | Z-up | glTF exporter converts automatically |
| FBX | Z-up | `FBXLoader` converts automatically |
| OBJ | No standard | ALWAYS verify orientation after loading |
| IFC | Z-up | ALWAYS apply -90 degree X rotation or use a converting loader |

**NEVER** assume imported models match Three.js conventions -- ALWAYS verify orientation after loading.

### Core Math Classes

| Class | Purpose | Identity/Default |
|-------|---------|-----------------|
| `Vector3` | Position, direction, scale | `(0, 0, 0)` |
| `Vector2` | UV coordinates, 2D positions | `(0, 0)` |
| `Vector4` | Homogeneous coordinates, shader data | `(0, 0, 0, 0)` |
| `Matrix4` | 4x4 transformation matrix | Identity matrix |
| `Quaternion` | Rotation without gimbal lock | `(0, 0, 0, 1)` |
| `Euler` | Human-readable rotation angles | `(0, 0, 0, 'XYZ')` |
| `Color` | RGB color (0-1 range) | `(1, 1, 1)` white |
| `Box3` | Axis-aligned bounding box | Empty (+Inf min, -Inf max) |
| `Sphere` | Bounding sphere | Center origin, radius -1 |
| `Plane` | Infinite plane | Normal (1,0,0), constant 0 |
| `Ray` | Origin + direction | Origin (0,0,0), direction (0,0,-1) |
| `Frustum` | 6-plane view frustum | -- |

### Critical Warnings

**NEVER** modify a Vector3/Matrix4/Quaternion that is shared between objects -- most methods mutate in-place. ALWAYS use `.clone()` before modifying shared instances.

```javascript
// WRONG: mutates the shared vector
const offset = new Vector3(1, 0, 0);
meshA.position.add(offset);
meshB.position.add(offset); // offset is still (1, 0, 0) BUT if you
                             // had stored meshA.position somewhere,
                             // it would be mutated

// CORRECT: clone before mutation
const pos = sharedPosition.clone().add(offset);
```

**NEVER** interpolate Euler angles directly -- it produces incorrect rotation paths and triggers gimbal lock. ALWAYS convert to Quaternion, use `slerp()`, then convert back if needed.

**NEVER** manually set Quaternion `x`, `y`, `z`, `w` values unless you understand quaternion math. ALWAYS use `setFromAxisAngle()`, `setFromEuler()`, or `slerp()`.

**NEVER** use `lerp()` on Color for hue-shifting animations -- it produces muddy intermediate colors. ALWAYS use `lerpHSL()` for transitions through different hues.

**ALWAYS** use `MathUtils.degToRad()` when Three.js expects radians -- all rotation methods use radians, not degrees.

---

## Vector3

The most-used math class. All mutating methods return `this` for chaining.

**Arithmetic:** `add(v)`, `addScalar(s)`, `sub(v)`, `multiply(v)`, `multiplyScalar(s)`, `divide(v)`, `divideScalar(s)`, `negate()`

**Geometric:** `dot(v): number`, `cross(v)`, `length(): number`, `lengthSq(): number`, `normalize()`, `setLength(l)`, `reflect(normal)`, `project(camera)`, `unproject(camera)`

**Distance:** `distanceTo(v): number`, `distanceToSquared(v): number`, `manhattanDistanceTo(v): number`

**Interpolation:** `lerp(v, alpha)`, `lerpVectors(v1, v2, t)`, `clamp(min, max)`, `clampLength(min, max)`

**Transform:** `applyMatrix4(m)`, `applyQuaternion(q)`, `applyAxisAngle(axis, angle)`, `applyEuler(euler)`

**Conversion:** `setFromMatrixPosition(m)`, `setFromMatrixScale(m)`, `setFromSphericalCoords(r, phi, theta)`, `toArray(arr?, offset?)`, `fromArray(arr, offset?)`

**Assignment:** `set(x, y, z)`, `copy(v)`, `clone()`, `equals(v): boolean`

**Vector2** differs: has only `x`, `y`. No `cross()` (returns scalar via `cross(v): number`). No 3D transforms.

**Vector4** differs: has `x`, `y`, `z`, `w`. Used for homogeneous coordinates and shader uniforms.

---

## Matrix4

Column-major storage (WebGL convention). 16 floats in `elements` array:

```
elements[0]  elements[4]  elements[8]   elements[12]  // Translation = [12,13,14]
elements[1]  elements[5]  elements[9]   elements[13]
elements[2]  elements[6]  elements[10]  elements[14]
elements[3]  elements[7]  elements[11]  elements[15]
```

**Composition:** `compose(position, quaternion, scale)` / `decompose(position, quaternion, scale)` -- the standard TRS (Translate-Rotate-Scale) pattern.

**Multiplication order:** Right-to-left. `M1.multiply(M2)` means M2 is applied first, then M1. Use `premultiply(m)` for left-multiplication (`this = m * this`).

**Factory methods:** `makeTranslation(x,y,z)`, `makeScale(x,y,z)`, `makeRotationX(theta)`, `makeRotationY(theta)`, `makeRotationZ(theta)`, `makeRotationAxis(axis, angle)`, `lookAt(eye, target, up)`

**Operations:** `invert()`, `transpose()`, `determinant(): number`, `identity()`, `extractBasis(x, y, z)`, `extractRotation(m)`, `setPosition(v)`

---

## Quaternion

Represents rotation without gimbal lock. ALWAYS prefer Quaternion over Euler for interpolated animations and compound rotations.

```javascript
import { Quaternion } from 'three';
const q = new Quaternion(); // identity: (0, 0, 0, 1)
```

**Setters:** `setFromAxisAngle(axis, angle)`, `setFromEuler(euler)`, `setFromRotationMatrix(m)`, `setFromUnitVectors(vFrom, vTo)`

**Operations:** `multiply(q)` (q applied first, then this), `premultiply(q)`, `slerp(qb, t)`, `slerpQuaternions(qa, qb, t)`, `rotateTowards(q, step)`, `conjugate()`, `invert()`, `normalize()`

**Comparison:** `dot(q): number`, `angleTo(q): number`, `equals(q): boolean`

---

## Euler

Human-readable rotation in radians with a rotation order.

```javascript
import { Euler } from 'three';
const e = new Euler(0, Math.PI / 2, 0, 'XYZ');
```

**Rotation orders:** `'XYZ'` (default), `'YXZ'`, `'ZXY'`, `'ZYX'`, `'YZX'`, `'XZY'`

**Gimbal lock:** In `'XYZ'` order, gimbal lock occurs at Y = +/- 90 degrees. Symptoms: unexpected snapping, loss of one rotational axis.

**Methods:** `setFromRotationMatrix(m)`, `setFromQuaternion(q, order?)`, `reorder(newOrder)`, `equals(euler): boolean`

### Euler vs Quaternion Decision Tree

| Scenario | Use |
|----------|-----|
| Setting a fixed rotation | Euler -- human-readable |
| Smooth rotation animation | Quaternion + `slerp()` |
| Combining multiple rotations | Quaternion + `multiply()` |
| Avoiding gimbal lock | Quaternion |
| Reading rotation from user input (degrees) | Euler, convert via `quaternion.setFromEuler(euler)` |
| Storing rotation in scene graph | `object.rotation` (Euler) auto-syncs with `object.quaternion` |

---

## Color

```javascript
import { Color } from 'three';

new Color(0xff0000);               // hex integer
new Color('red');                   // CSS color name
new Color('rgb(255, 0, 0)');       // CSS rgb string
new Color('#ff0000');              // CSS hex string
new Color('hsl(0, 100%, 50%)');   // CSS hsl string
new Color(1.0, 0.0, 0.0);        // RGB floats (0-1 range)
```

**Properties:** `r`, `g`, `b` (number, 0-1 range).

**Setters:** `set(value)`, `setHex(hex)`, `setRGB(r,g,b)`, `setHSL(h,s,l)`, `setStyle(css)`, `setColorName(name)`

**Getters:** `getHex(): number`, `getHexString(): string`, `getHSL(target): {h,s,l}`, `getStyle(): string`

**Interpolation:** `lerp(color, alpha)` (RGB), `lerpHSL(color, alpha)` (perceptually better for hue shifts), `lerpColors(c1, c2, alpha)`

**Color space:** `convertSRGBToLinear()`, `convertLinearToSRGB()` -- ALWAYS convert texture colors to linear space for physically correct rendering.

---

## MathUtils

Static utility methods -- NEVER instantiate, ALWAYS access via `MathUtils.method()`.

```javascript
import { MathUtils } from 'three';

MathUtils.degToRad(90);           // 1.5707...
MathUtils.clamp(value, 0, 1);    // clamp to range
MathUtils.lerp(0, 100, 0.5);     // 50
MathUtils.mapLinear(5, 0, 10, 0, 100); // 50
MathUtils.smoothstep(0.5, 0, 1); // Hermite ease
MathUtils.damp(current, target, lambda, dt); // frame-rate-independent damping
MathUtils.generateUUID();         // RFC 4122 v4 UUID
```

`damp()` is particularly useful for smooth camera follow and UI animations -- it produces exponential decay that is frame-rate independent, unlike naive lerp in an animation loop.

---

## Bounding Volumes

### Box3 (Axis-Aligned Bounding Box)

```javascript
import { Box3, Vector3 } from 'three';

const box = new Box3();
box.setFromObject(mesh);                    // compute from mesh
box.containsPoint(new Vector3(1, 2, 3));   // boolean
box.intersectsBox(otherBox);               // boolean
box.getCenter(new Vector3());              // center point
box.getSize(new Vector3());                // dimensions
```

### Sphere, Plane, Ray, Frustum

- **Sphere**: `containsPoint()`, `intersectsBox()`, `intersectsSphere()`, `distanceToPoint()`
- **Plane**: `distanceToPoint()`, `projectPoint()`, `intersectLine()`
- **Ray**: `intersectBox()`, `intersectSphere()`, `intersectPlane()`, `distanceToPoint()`
- **Frustum**: `setFromProjectionMatrix(m)`, `containsPoint()`, `intersectsObject()`, `intersectsBox()`

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete method signatures for Vector3, Matrix4, Quaternion, Euler, Color, MathUtils, Box3, Sphere, Plane, Ray
- [references/examples.md](references/examples.md) -- Working code examples for common 3D math operations
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with Three.js math classes

### Official Sources

- https://threejs.org/docs/#api/en/math/Vector3
- https://threejs.org/docs/#api/en/math/Matrix4
- https://threejs.org/docs/#api/en/math/Quaternion
- https://threejs.org/docs/#api/en/math/Euler
- https://threejs.org/docs/#api/en/math/Color
- https://threejs.org/docs/#api/en/math/MathUtils
- https://threejs.org/docs/#api/en/math/Box3
