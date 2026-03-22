---
name: threejs-core-scene-graph
description: >
  Use when creating Three.js scenes, adding objects, managing parent-child
  hierarchies, or organizing 3D content. Prevents the common mistake of
  using add() instead of attach() for reparenting, forgetting
  matrixAutoUpdate, or missing dispose() calls. Covers Object3D, Scene,
  Group, Mesh, Layers, Fog, traversal, coordinate conversion.
  Keywords: scene graph, Object3D, add, remove, traverse, layers, fog,
  parent, children, visibility, Three.js scene setup.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-core-scene-graph

## Quick Reference

### Scene Graph Hierarchy

| Class | Extends | Purpose |
|-------|---------|---------|
| `Object3D` | `EventDispatcher` | Base class for ALL 3D objects. Provides transform, hierarchy, traversal |
| `Scene` | `Object3D` | Root container. Adds background, environment, fog, overrideMaterial |
| `Group` | `Object3D` | Semantic container with no extra functionality. Use for logical grouping |
| `Mesh` | `Object3D` | Geometry + Material. The primary visible object in a scene |
| `Camera` | `Object3D` | View projection. ALWAYS add to scene for matrix updates |
| `Light` | `Object3D` | Illumination. ALWAYS add to scene for rendering |

### Object3D Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `position` | `Vector3` | `(0,0,0)` | Local position relative to parent |
| `rotation` | `Euler` | `(0,0,0,'XYZ')` | Local rotation. Linked to `quaternion` -- modifying one ALWAYS updates the other |
| `quaternion` | `Quaternion` | `(0,0,0,1)` | Local rotation as quaternion. Linked to `rotation` |
| `scale` | `Vector3` | `(1,1,1)` | Local scale. Non-uniform scale causes normal distortion |
| `visible` | `boolean` | `true` | When `false`, object and ALL descendants are skipped during rendering |
| `layers` | `Layers` | layer 0 | 32-bit bitmask for selective rendering and raycasting |
| `castShadow` | `boolean` | `false` | Whether object casts shadows |
| `receiveShadow` | `boolean` | `false` | Whether object receives shadows |
| `frustumCulled` | `boolean` | `true` | Set `false` for skyboxes or objects that MUST always render |
| `renderOrder` | `number` | `0` | Higher values render later. Use for transparency sorting |
| `name` | `string` | `""` | Human-readable label. Use `getObjectByName()` for lookup |
| `userData` | `object` | `{}` | Custom application data dictionary |

### Identity Properties

| Property | Type | Description |
|----------|------|-------------|
| `uuid` | `string` | Read-only RFC 4122 v4 identifier. Auto-generated |
| `id` | `number` | Auto-incrementing integer. Unique per runtime session |
| `name` | `string` | User-assigned. NEVER relied upon as unique identifier |
| `type` | `string` | Read-only class name (e.g., `"Mesh"`, `"Group"`) |

### Critical Warnings

**NEVER** modify `children` array directly -- ALWAYS use `add()`, `remove()`, `clear()`, or `attach()`. Direct modification breaks internal bookkeeping (parent references, event dispatch).

**NEVER** modify the children array during `traverse()` -- collect objects first, then modify after traversal completes. Adding during traversal causes unpredictable iteration.

**NEVER** use `add()` when reparenting an object that must keep its world position -- ALWAYS use `attach()` instead. `add()` preserves local transform; `attach()` preserves world transform.

**NEVER** read `matrixWorld` after changing position/rotation/scale in the same frame without calling `updateWorldMatrix(true, false)` first -- the world matrix is stale until the next render or explicit update.

**NEVER** store Three.js objects in `userData` without manual disposal -- `userData` is NOT automatically cleaned up by `dispose()`.

**NEVER** forget to dispose textures, geometries, and materials when removing objects -- `remove()` and `clear()` only detach from the scene graph, they do NOT free GPU memory.

---

## Hierarchy Methods

### add() vs attach() -- The Critical Difference

```javascript
import { Scene, Group, Mesh, BoxGeometry, MeshStandardMaterial } from 'three';

const scene = new Scene();
const groupA = new Group();
const groupB = new Group();
groupA.position.set(10, 0, 0);
groupB.position.set(0, 5, 0);
scene.add(groupA, groupB);

const mesh = new Mesh(new BoxGeometry(), new MeshStandardMaterial());
mesh.position.set(0, 0, 0);
groupA.add(mesh);
// mesh world position = (10, 0, 0) -- inherited from groupA

// WRONG: add() preserves LOCAL transform -- mesh jumps to (0, 5, 0) world
groupB.add(mesh); // auto-removes from groupA first

// CORRECT: attach() preserves WORLD transform -- mesh stays at (10, 0, 0) visually
groupA.add(mesh); // reset
groupB.attach(mesh); // mesh.position is recalculated to maintain world position
```

### remove(), removeFromParent(), clear()

```javascript
// Remove specific children
group.remove(meshA, meshB);

// Remove self from parent (safe when parent is null)
mesh.removeFromParent();

// Remove ALL children -- ALWAYS prefer over manual iteration
group.clear();
```

**Edge case:** `remove()` NEVER throws if the object is not a child -- it silently does nothing.

---

## Traversal

```javascript
// Depth-first traversal of ALL descendants
scene.traverse((object) => {
  if (object.isMesh) {
    object.castShadow = true;
  }
});

// Skip invisible objects and their subtrees
scene.traverseVisible((object) => {
  // only visits objects where visible === true
});

// Walk UP to root (does NOT include the starting object)
mesh.traverseAncestors((ancestor) => {
  console.log(ancestor.name);
});

// Find by name, id, or arbitrary property
const wall = scene.getObjectByName('north-wall');
const obj = scene.getObjectById(42);
const selectable = scene.getObjectByProperty('userData', { selectable: true });
```

**Performance:** All search methods are O(n). For frequent lookups, ALWAYS cache the reference.

---

## Matrix System

### Automatic Mode (Default)

The renderer calls `updateMatrixWorld()` on the scene before every render, which recursively:
1. Calls `updateMatrix()` on each object (composes `matrix` from position/rotation/scale)
2. Computes `matrixWorld = parent.matrixWorld * matrix`

### Manual Mode (Performance Optimization)

```javascript
// For static objects -- skip per-frame matrix recomputation
object.matrixAutoUpdate = false;
object.matrix.compose(position, quaternion, scale);
object.matrixWorldNeedsUpdate = true;
```

### Reading World-Space Values Mid-Frame

```javascript
import { Vector3, Quaternion } from 'three';

object.position.set(10, 0, 0);
object.updateWorldMatrix(true, false); // update parents first

const worldPos = new Vector3();
object.getWorldPosition(worldPos);

const worldQuat = new Quaternion();
object.getWorldQuaternion(worldQuat);

const worldScale = new Vector3();
object.getWorldScale(worldScale);

const worldDir = new Vector3();
object.getWorldDirection(worldDir);
```

### Coordinate Conversion

```javascript
// MUTATION WARNING: both methods modify the input vector in-place
const localPoint = new Vector3(5, 0, 0);
object.localToWorld(localPoint); // localPoint is now in world coordinates

const worldPoint = new Vector3(15, 3, 0);
object.worldToLocal(worldPoint); // worldPoint is now in object's local coordinates
```

---

## Scene Class

```javascript
import { Scene, Color, Fog, FogExp2, TextureLoader } from 'three';

const scene = new Scene();
scene.background = new Color(0x222222);         // solid color
scene.environment = hdrTexture;                  // IBL for all PBR materials
scene.environmentIntensity = 1.5;                // boost environment lighting
scene.environmentRotation.set(0, Math.PI, 0);   // rotate environment
scene.fog = new Fog(0xcccccc, 10, 100);         // linear fog
scene.overrideMaterial = depthMaterial;          // debug: force all objects to one material
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `background` | `Color \| Texture \| CubeTexture \| null` | `null` | Scene background |
| `environment` | `Texture \| null` | `null` | IBL environment map for all PBR materials without own `envMap` |
| `fog` | `Fog \| FogExp2 \| null` | `null` | Scene fog effect |
| `overrideMaterial` | `Material \| null` | `null` | Forces ALL objects to use this material |
| `backgroundBlurriness` | `number` | `0` | Blur for background (0-1) |
| `backgroundIntensity` | `number` | `1` | Background brightness multiplier |
| `backgroundRotation` | `Euler` | `(0,0,0)` | Background rotation |
| `environmentIntensity` | `number` | `1` | Environment map brightness multiplier |
| `environmentRotation` | `Euler` | `(0,0,0)` | Environment map rotation |

---

## Fog

### Fog (Linear Interpolation)

```javascript
import { Fog } from 'three';
scene.fog = new Fog(0xffffff, 10, 200); // color, near, far
```

### FogExp2 (Exponential Density)

```javascript
import { FogExp2 } from 'three';
scene.fog = new FogExp2(0xffffff, 0.01); // color, density
```

**Material interaction:** Every material has a `fog` property (default: `true`). `ShaderMaterial` and `RawShaderMaterial` default to `fog: false` -- you MUST set `fog: true` and include fog shader chunks manually for custom shaders to respond to fog.

---

## Group

`Group` extends `Object3D` with zero additional functionality. It exists purely as a semantic container for organizing objects:

```javascript
import { Group } from 'three';

const buildingGroup = new Group();
buildingGroup.name = 'building-01';
buildingGroup.add(walls, roof, foundation);
scene.add(buildingGroup);

// Transform all children together
buildingGroup.position.set(50, 0, 0);
buildingGroup.rotation.y = Math.PI / 4;
```

---

## Mesh

`Mesh` combines a `BufferGeometry` with a `Material` to create a visible surface:

```javascript
import { Mesh, BoxGeometry, MeshStandardMaterial } from 'three';

const mesh = new Mesh(
  new BoxGeometry(1, 1, 1),
  new MeshStandardMaterial({ color: 0x00ff00 })
);

// Multi-material with geometry groups
const materials = [materialA, materialB];
geometry.addGroup(0, 36, 0);   // start, count, materialIndex
geometry.addGroup(36, 36, 1);
const multiMesh = new Mesh(geometry, materials);

// Morph targets
mesh.morphTargetInfluences[0] = 0.5; // blend between base and morph target
```

---

## Layers System

A 32-bit bitmask system for selective rendering and raycasting:

```javascript
import { Layers } from 'three';

// Objects are on layer 0 by default
mesh.layers.set(1);        // ONLY layer 1 (removes from layer 0)
mesh.layers.enable(2);     // add layer 2 (keep layer 1)
mesh.layers.disable(1);    // remove layer 1
mesh.layers.toggle(3);     // flip layer 3

// Camera renders only objects with overlapping layers
camera.layers.enable(1);   // camera now sees layers 0 AND 1

// Test overlap
const visible = camera.layers.test(mesh.layers); // true if any layer overlaps
```

**Use cases:**
- Layer 0: default visible objects
- Layer 1: helpers/gizmos (disable on production camera)
- Layer 2: bloom-only objects (selective post-processing)
- Layers 3-31: custom (collision groups, selection sets, LOD groups)

---

## lookAt() Behavior Difference

```javascript
// Camera: points NEGATIVE-Z toward target (looks AT the target)
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);

// Non-camera objects: points POSITIVE-Z toward target
mesh.lookAt(targetPosition);
```

ALWAYS call `lookAt()` after setting `position` -- it computes rotation from the current position.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete Object3D, Scene, Group, Mesh, Layers API signatures
- [references/examples.md](references/examples.md) -- Working code examples for common scene graph operations
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with scene graph management

### Official Sources

- https://threejs.org/docs/#api/en/core/Object3D
- https://threejs.org/docs/#api/en/scenes/Scene
- https://threejs.org/docs/#api/en/scenes/Fog
- https://threejs.org/docs/#api/en/scenes/FogExp2
- https://threejs.org/docs/#api/en/objects/Group
- https://threejs.org/docs/#api/en/objects/Mesh
- https://threejs.org/docs/#api/en/core/Layers
