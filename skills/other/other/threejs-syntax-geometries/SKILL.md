---
name: threejs-syntax-geometries
description: >
  Use when creating 3D shapes, custom geometry, or instanced meshes in
  Three.js. Prevents the common mistake of forgetting dispose(), not
  setting needsUpdate on BufferAttribute, or using non-indexed geometry
  when indexed is better. Covers BufferGeometry, BufferAttribute, all
  21 built-in geometries, InstancedMesh, ExtrudeGeometry, custom geometry.
  Keywords: BufferGeometry, BoxGeometry, SphereGeometry, PlaneGeometry,
  InstancedMesh, BufferAttribute, geometry, shape, extrude, custom mesh.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-syntax-geometries

## Quick Reference

### BufferGeometry — Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `attributes` | `Object` | `{}` | Hash map of named `BufferAttribute` instances |
| `index` | `BufferAttribute \| null` | `null` | Index buffer for indexed rendering |
| `morphAttributes` | `Object` | `{}` | Morph target attribute arrays |
| `morphTargetsRelative` | `Boolean` | `false` | If `true`, morph data = relative offsets |
| `groups` | `Array` | `[]` | `{ start, count, materialIndex }` for multi-material |
| `drawRange` | `Object` | `{ start: 0, count: Infinity }` | Portion of geometry to render |
| `boundingBox` | `Box3 \| null` | `null` | Cached — `null` until `computeBoundingBox()` |
| `boundingSphere` | `Sphere \| null` | `null` | Cached — `null` until `computeBoundingSphere()` |

### BufferGeometry — Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `setAttribute(name, attr)` | `this` | Add or replace a named attribute |
| `getAttribute(name)` | `BufferAttribute` | Retrieve attribute by name |
| `deleteAttribute(name)` | `this` | Remove a named attribute |
| `hasAttribute(name)` | `boolean` | Check if attribute exists |
| `setIndex(attr)` | — | Set the index buffer |
| `addGroup(start, count, materialIndex?)` | — | Define a render group for multi-material |
| `clearGroups()` | — | Remove all groups |
| `setDrawRange(start, count)` | — | Limit rendered range |
| `computeVertexNormals()` | — | Compute smooth normals from face topology |
| `computeTangents()` | — | Compute tangent vectors (requires position, normal, uv, index) |
| `computeBoundingBox()` | — | Compute and cache AABB |
| `computeBoundingSphere()` | — | Compute and cache bounding sphere |
| `toNonIndexed()` | new geometry | Create non-indexed copy with duplicated vertices |
| `translate(x, y, z)` | `this` | Translate vertex positions in-place |
| `rotateX/Y/Z(radians)` | `this` | Rotate vertex positions in-place |
| `scale(x, y, z)` | `this` | Scale vertex positions in-place |
| `center()` | `this` | Center geometry at the origin |
| `dispose()` | — | Free GPU resources |

### BufferAttribute — Constructor and Properties

```javascript
import * as THREE from 'three';

new THREE.BufferAttribute(array: TypedArray, itemSize: number, normalized?: boolean)
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `array` | `TypedArray` | — | The underlying data |
| `itemSize` | `number` | — | Values per vertex (1=scalar, 2=UV, 3=position, 4=RGBA) |
| `count` | `number` | computed | `array.length / itemSize` |
| `needsUpdate` | `boolean` | `false` | Set `true` to upload changes to GPU |
| `usage` | `number` | `StaticDrawUsage` | GPU usage hint |

### Typed Convenience Classes

| Class | Underlying Type | Use Case |
|-------|----------------|----------|
| `Float32BufferAttribute` | `Float32Array` | Positions, normals, UVs (most common) |
| `Float16BufferAttribute` | `Float16Array` | Memory-optimized attributes |
| `Uint16BufferAttribute` | `Uint16Array` | Index buffers (<65536 vertices) |
| `Uint32BufferAttribute` | `Uint32Array` | Index buffers (>65536 vertices) |
| `Uint8BufferAttribute` | `Uint8Array` | Byte colors (with `normalized=true`) |
| `Int8/Int16/Int32BufferAttribute` | Respective arrays | Signed integer data |

### Usage Hints

| Constant | When to Use |
|----------|-------------|
| `THREE.StaticDrawUsage` | Data uploaded once, read many times (default) |
| `THREE.DynamicDrawUsage` | Data updated frequently (particles, animated verts) |
| `THREE.StreamDrawUsage` | Data updated every frame and read once |

### Critical Warnings

**NEVER** forget `attribute.needsUpdate = true` after modifying BufferAttribute data via `setX/setXY/setXYZ` or direct array writes. Without this flag, changes will NOT reach the GPU.

**NEVER** assume `boundingBox` or `boundingSphere` are populated automatically. They are `null` until you explicitly call `computeBoundingBox()` / `computeBoundingSphere()`.

**ALWAYS** call `computeVertexNormals()` after building custom geometry if you need lighting. Without normals, `MeshStandardMaterial` and other lit materials render black.

**ALWAYS** call `geometry.dispose()` when removing geometry from the scene permanently. Failing to dispose leaks GPU memory. The garbage collector does NOT free GPU-side buffers.

**NEVER** call `translate()`, `rotateX()`, `scale()`, or other in-place transform methods in an animation loop. These modify the actual vertex data permanently. Use `mesh.position`, `mesh.rotation`, and `mesh.scale` for runtime transforms.

**ALWAYS** set `usage` to `DynamicDrawUsage` BEFORE the first render if you plan to update attribute data every frame. Changing usage after initial upload has no effect on some GPU drivers.

**NEVER** forget `instanceMatrix.needsUpdate = true` after calling `setMatrixAt()` on InstancedMesh. Without this flag, all instances render at the origin.

---

## Indexed vs Non-Indexed Geometry

| Aspect | Indexed | Non-Indexed |
|--------|---------|-------------|
| Memory | Lower (shared vertices) | Higher (duplicated vertices) |
| GPU cache | Better (vertex reuse) | No reuse |
| Flat shading | Requires duplicated normals | Natural per-face normals |
| Wireframe | Clean edges | May show diagonal lines |

**ALWAYS** use indexed geometry for smooth-shaded meshes with shared vertices. Use `geometry.toNonIndexed()` ONLY when you need per-face attributes (flat shading with unique normals).

---

## All 21 Built-in Geometries

### Primitives

| Geometry | Key Parameters |
|----------|---------------|
| `BoxGeometry` | `(width=1, height=1, depth=1, wSeg=1, hSeg=1, dSeg=1)` |
| `SphereGeometry` | `(radius=1, wSeg=32, hSeg=16, phiStart, phiLen, thetaStart, thetaLen)` |
| `PlaneGeometry` | `(width=1, height=1, wSeg=1, hSeg=1)` |
| `CylinderGeometry` | `(radTop=1, radBot=1, height=1, radSeg=32, hSeg=1, open, thetaStart, thetaLen)` |
| `ConeGeometry` | `(radius=1, height=1, radSeg=32, hSeg=1, open, thetaStart, thetaLen)` |
| `CapsuleGeometry` | `(radius=1, length=1, capSeg=4, radSeg=8)` |
| `TorusGeometry` | `(radius=1, tube=0.4, radSeg=12, tubSeg=48, arc=2PI)` |
| `TorusKnotGeometry` | `(radius=1, tube=0.4, tubSeg=64, radSeg=8, p=2, q=3)` |
| `CircleGeometry` | `(radius=1, seg=32, thetaStart=0, thetaLen=2PI)` |
| `RingGeometry` | `(inner=0.5, outer=1, thetaSeg=32, phiSeg=1, thetaStart, thetaLen)` |

### Polyhedra

All accept `(radius=1, detail=0)`. Detail controls subdivision level.

| Geometry | Base Faces |
|----------|-----------|
| `TetrahedronGeometry` | 4 |
| `OctahedronGeometry` | 8 |
| `DodecahedronGeometry` | 12 |
| `IcosahedronGeometry` | 20 |
| `PolyhedronGeometry` | custom (`vertices, indices, radius, detail`) |

### Path-Based

| Geometry | Description |
|----------|-------------|
| `ExtrudeGeometry(shapes, options)` | Extrude 2D Shape into 3D |
| `ShapeGeometry(shapes, curveSegments=12)` | Flat 2D geometry from Shape |
| `LatheGeometry(points, segments=12, phiStart, phiLength)` | Revolve 2D profile around Y axis |
| `TubeGeometry(path, tubSeg=64, radius=1, radSeg=8, closed)` | Tube along a Curve3 |

### Utility

| Geometry | Description |
|----------|-------------|
| `EdgesGeometry(geometry, thresholdAngle=1)` | Edges where angle > threshold (clean outlines) |
| `WireframeGeometry(geometry)` | ALL triangle edges (debug visualization) |

---

## ExtrudeGeometry Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `depth` | `number` | `1` | Extrusion depth |
| `steps` | `number` | `1` | Subdivision steps along depth |
| `bevelEnabled` | `boolean` | `true` | Enable beveled edges |
| `bevelThickness` | `number` | `0.2` | Bevel depth into shape |
| `bevelSize` | `number` | `bevelThickness - 0.1` | Bevel distance from outline |
| `bevelOffset` | `number` | `0` | Bevel offset from edge |
| `bevelSegments` | `number` | `3` | Bevel resolution |
| `curveSegments` | `number` | `12` | Points on curves |
| `extrudePath` | `Curve` | `undefined` | 3D path to extrude along |
| `UVGenerator` | `Object` | `WorldUVGenerator` | Custom UV generation |

---

## Shape Class — 2D Path Drawing

```javascript
import * as THREE from 'three';

const shape = new THREE.Shape();
shape.moveTo(x, y);                                    // Start new subpath
shape.lineTo(x, y);                                    // Straight line
shape.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y);   // Cubic Bezier
shape.quadraticCurveTo(cpx, cpy, x, y);                // Quadratic Bezier
shape.splineThru(points);                               // Smooth spline through Vector2[]
shape.arc(aX, aY, radius, startAngle, endAngle, cw);   // Relative arc
shape.absarc(aX, aY, radius, startAngle, endAngle, cw); // Absolute arc

// Holes
const holePath = new THREE.Path();
holePath.absarc(0, 0, 0.5, 0, Math.PI * 2);
shape.holes.push(holePath);
```

---

## Morph Targets

```javascript
import * as THREE from 'three';

// Define morph target positions
const morphPositions = new Float32Array([/* ... */]);
geometry.morphAttributes.position = [
  new THREE.BufferAttribute(morphPositions, 3)
];

// Control on the mesh
mesh.morphTargetInfluences[0] = 0.5; // 50% blend toward morph target 0

// Named morph targets (from glTF)
mesh.morphTargetDictionary; // { "smile": 0, "frown": 1 }
```

Set `geometry.morphTargetsRelative = true` when morph data represents offsets rather than absolute positions.

---

## InstancedMesh

```javascript
import * as THREE from 'three';

const mesh = new THREE.InstancedMesh(geometry, material, count);
```

| Property | Type | Description |
|----------|------|-------------|
| `instanceMatrix` | `InstancedBufferAttribute` | 4x4 matrices (16 floats per instance) |
| `instanceColor` | `InstancedBufferAttribute \| null` | Per-instance RGB (created on first `setColorAt`) |
| `count` | `number` | Instance count (read-only after construction) |

| Method | Description |
|--------|-------------|
| `setMatrixAt(index, matrix4)` | Set transform for instance |
| `getMatrixAt(index, matrix4)` | Read transform into target |
| `setColorAt(index, color)` | Set per-instance color |
| `getColorAt(index, color)` | Read per-instance color |

### Performance Guidelines

| Instance Count | Recommendation |
|---------------|----------------|
| < 10 | Use individual `Mesh` objects |
| 10 - 100 | Either approach; profile your case |
| 100 - 10,000 | ALWAYS use `InstancedMesh` |
| > 10,000 | Use `InstancedMesh` with spatial subdivision or `BatchedMesh` (r160+) |

### Custom Per-Instance Attributes

```javascript
import * as THREE from 'three';

const phases = new Float32Array(count);
for (let i = 0; i < count; i++) phases[i] = Math.random();
mesh.geometry.setAttribute('aPhase', new THREE.InstancedBufferAttribute(phases, 1));
// Access in vertex shader: attribute float aPhase;
```

---

## Multi-Material with Groups

```javascript
import * as THREE from 'three';

geometry.addGroup(0, 6, 0);    // First 6 indices -> material[0]
geometry.addGroup(6, 6, 1);    // Next 6 indices  -> material[1]
const mesh = new THREE.Mesh(geometry, [materialA, materialB]);
```

---

## InterleavedBuffer

For optimal GPU cache performance on large meshes (10,000+ vertices):

```javascript
import * as THREE from 'three';

const stride = 8; // 3 (position) + 3 (normal) + 2 (uv)
const buffer = new THREE.InterleavedBuffer(new Float32Array(vertexCount * stride), stride);

geometry.setAttribute('position', new THREE.InterleavedBufferAttribute(buffer, 3, 0));
geometry.setAttribute('normal',   new THREE.InterleavedBufferAttribute(buffer, 3, 3));
geometry.setAttribute('uv',       new THREE.InterleavedBufferAttribute(buffer, 2, 6));
```

**ALWAYS** use separate buffers when individual attributes are updated independently. Use interleaved buffers ONLY when all attributes are static or updated together.

---

## Disposal Rules

- **ALWAYS** call `geometry.dispose()` when removing geometry from the scene permanently
- Shared geometries (used by multiple meshes): dispose ONLY after ALL meshes are removed
- Built-in geometries: dispose when the mesh using them is removed
- The JavaScript garbage collector does NOT free GPU-side vertex buffers

---

## Reference Links

- [references/methods.md](references/methods.md) — Complete API signatures for BufferGeometry, BufferAttribute, InstancedMesh
- [references/examples.md](references/examples.md) — Working code examples for custom geometry, instancing, extrusion
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do with geometry in Three.js

### Official Sources

- https://threejs.org/docs/#api/en/core/BufferGeometry
- https://threejs.org/docs/#api/en/core/BufferAttribute
- https://threejs.org/docs/#api/en/objects/InstancedMesh
- https://threejs.org/docs/#api/en/geometries/ExtrudeGeometry
- https://threejs.org/docs/#api/en/extras/core/Shape
