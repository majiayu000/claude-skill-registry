---
name: threejs-errors-performance
description: >
  Use when a Three.js scene has performance problems: low FPS, memory
  leaks, too many draw calls, or high GPU memory usage. Prevents the
  common mistake of forgetting dispose(), creating objects in the render
  loop, or not using InstancedMesh for repeated objects. Covers disposal
  patterns, draw call optimization, InstancedMesh, LOD, texture compression,
  renderer.info, Stats.js profiling.
  Keywords: performance, memory leak, dispose, draw calls, FPS, slow,
  optimization, InstancedMesh, LOD, renderer.info, Stats, profiling.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-errors-performance

## Performance Diagnosis Flowchart

```
Scene is slow / low FPS
│
├─ Check renderer.info.render.calls
│  ├─ > 200 draw calls ──────────────── Go to: Draw Call Optimization
│  └─ < 200 draw calls
│
├─ Check renderer.info.memory
│  ├─ geometries/textures growing ──── Go to: Memory Leak Diagnosis
│  └─ stable counts
│
├─ Check renderer.info.render.triangles
│  ├─ > 2M triangles ────────────────── Go to: Geometry Optimization (LOD, merge)
│  └─ < 2M triangles
│
├─ Check GPU load (DevTools Performance tab)
│  ├─ GPU-bound (long GPU tasks) ───── Go to: Shader / Material Optimization
│  └─ CPU-bound (long JS tasks) ────── Go to: CPU Optimization
│
└─ Check Stats.js memory panel
   ├─ JS heap growing ─────────────── Go to: JavaScript Object Leaks
   └─ Heap stable ──────────────────── Profile specific bottleneck
```

## Quick Reference

### renderer.info — Your First Diagnostic Tool

```javascript
import * as THREE from 'three';

// ALWAYS check renderer.info when diagnosing performance
console.log(renderer.info.render);
// { calls: number, triangles: number, points: number, lines: number, frame: number }

console.log(renderer.info.memory);
// { geometries: number, textures: number }

console.log(renderer.info.programs);
// Array of compiled shader programs (length = unique material combinations)
```

**Rule**: If `renderer.info.memory.geometries` or `renderer.info.memory.textures` grows continuously over time, you have a memory leak. ALWAYS monitor these values during development.

### Stats.js — FPS and Memory Monitoring

```javascript
import Stats from 'three/addons/libs/stats.module.js';

const stats = new Stats();
stats.showPanel(0); // 0 = FPS, 1 = MS per frame, 2 = MB heap
document.body.appendChild(stats.dom);

function animate() {
  stats.begin();
  renderer.render(scene, camera);
  stats.end();
  requestAnimationFrame(animate);
}
```

### Performance Budgets

| Metric | Target (60 FPS) | Warning | Critical |
|--------|-----------------|---------|----------|
| Draw calls | < 100 | 100-500 | > 500 |
| Triangles | < 1M | 1M-3M | > 3M |
| Textures (GPU) | < 50 | 50-200 | > 200 |
| Shader programs | < 20 | 20-50 | > 50 |
| Frame time | < 16.6ms | 16.6-33ms | > 33ms |

---

## Memory Management — Disposal Rules

### What MUST Be Disposed

Three.js allocates GPU resources that are NOT automatically garbage collected by JavaScript. ALWAYS dispose these manually:

| Object Type | Method | GPU Resource Released |
|-------------|--------|---------------------|
| `BufferGeometry` | `geometry.dispose()` | Vertex/index buffers |
| `Material` (all types) | `material.dispose()` | Shader programs, uniforms |
| `Texture` (all types) | `texture.dispose()` | GPU texture memory |
| `WebGLRenderTarget` | `renderTarget.dispose()` | Framebuffer + textures |
| `WebGLRenderer` | `renderer.dispose()` | Entire WebGL context |
| `PMREMGenerator` | `pmremGenerator.dispose()` | Prefiltered env maps |
| Controls (all types) | `controls.dispose()` | DOM event listeners |

### Complete Material Disposal

```javascript
function disposeMaterial(material) {
  const textureProps = [
    'map', 'lightMap', 'bumpMap', 'normalMap', 'specularMap',
    'envMap', 'alphaMap', 'aoMap', 'displacementMap',
    'emissiveMap', 'gradientMap', 'metalnessMap', 'roughnessMap',
    'clearcoatMap', 'clearcoatNormalMap', 'clearcoatRoughnessMap',
    'transmissionMap', 'thicknessMap', 'sheenColorMap', 'sheenRoughnessMap'
  ];
  for (const prop of textureProps) {
    if (material[prop]) material[prop].dispose();
  }
  material.dispose();
}
```

### Full Scene Disposal

```javascript
function disposeScene(scene) {
  scene.traverse((object) => {
    if (object.geometry) {
      object.geometry.dispose();
    }
    if (object.material) {
      if (Array.isArray(object.material)) {
        object.material.forEach(disposeMaterial);
      } else {
        disposeMaterial(object.material);
      }
    }
  });
  scene.clear();
}
```

### When to Dispose vs. When to Reuse

**ALWAYS dispose when:**
- Removing objects permanently from the scene
- Switching between completely different scenes
- Unloading loaded models (GLTF, FBX, OBJ)
- Component unmount (React, Vue, Angular)

**NEVER dispose when:**
- Temporarily hiding objects (use `visible = false` instead)
- Objects will be re-added to the scene later
- Multiple meshes share the same geometry/material (dispose ONLY when ALL users are done)

---

## Draw Call Optimization

### InstancedMesh — Render Thousands in One Call

ALWAYS use `InstancedMesh` when rendering more than ~100 copies of the same geometry+material combination.

```javascript
import * as THREE from 'three';

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const count = 5000;
const mesh = new THREE.InstancedMesh(geometry, material, count);

const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.set(Math.random() * 200 - 100, 0, Math.random() * 200 - 100);
  dummy.rotation.y = Math.random() * Math.PI * 2;
  dummy.scale.setScalar(0.5 + Math.random());
  dummy.updateMatrix();
  mesh.setMatrixAt(i, dummy.matrix);
}
// CRITICAL: without this, instances render at origin
mesh.instanceMatrix.needsUpdate = true;
scene.add(mesh);
```

| Instance Count | Recommendation |
|---------------|----------------|
| < 10 | Individual `Mesh` objects are fine |
| 10-100 | Either approach; profile your case |
| 100-10,000 | ALWAYS use `InstancedMesh` |
| > 10,000 | `InstancedMesh` with spatial subdivision or `BatchedMesh` (r160+) |

### BatchedMesh (r160+) — Multiple Geometries in One Call

`BatchedMesh` extends instancing to support different geometries and materials in a single draw call. Use for heterogeneous repeated objects.

### Geometry Merging — Static Objects

For static objects that NEVER move independently, merge them into a single geometry:

```javascript
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const geometries = meshArray.map((m) => {
  const geo = m.geometry.clone();
  geo.applyMatrix4(m.matrixWorld);
  return geo;
});
const merged = mergeGeometries(geometries, false);
const mergedMesh = new THREE.Mesh(merged, sharedMaterial);

// Dispose originals after merge
meshArray.forEach((m) => {
  m.geometry.dispose();
  scene.remove(m);
});
```

**Rule**: NEVER merge geometries that need independent transforms, materials, or raycasting targets. Merging makes individual object interaction impossible.

---

## LOD (Level of Detail)

```javascript
import * as THREE from 'three';

const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);    // visible 0-50 units
lod.addLevel(mediumDetailMesh, 50); // visible 50-200 units
lod.addLevel(lowDetailMesh, 200);   // visible 200+ units
scene.add(lod);

// ALWAYS call in animation loop for distance-based switching
lod.update(camera);
```

**Rule**: ALWAYS provide at least 3 LOD levels for objects visible across a wide distance range. Triangle counts MUST decrease by at least 50% between each level.

---

## Texture Optimization

| Technique | Impact | When to Use |
|-----------|--------|-------------|
| Resize textures | High | ALWAYS use the smallest resolution that looks acceptable |
| Power-of-two dimensions | Medium | Required for mipmaps; ALWAYS use (256, 512, 1024, 2048) |
| Compressed formats (KTX2/Basis) | High | ALWAYS for production; 4-6x smaller GPU footprint |
| Texture atlases | High | Combine multiple small textures into one to reduce draw calls |
| `texture.dispose()` on swap | Critical | ALWAYS dispose old texture before assigning new one |
| `generateMipmaps: false` | Low | Use for UI textures or textures that NEVER need filtering at distance |

### KTX2 Compressed Textures

```javascript
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader()
  .setTranscoderPath('three/addons/libs/basis/')
  .detectSupport(renderer);

ktx2Loader.load('texture.ktx2', (texture) => {
  material.map = texture;
  material.needsUpdate = true;
});
```

---

## Frustum Culling

Frustum culling is enabled by default (`object.frustumCulled = true`). The renderer skips objects outside the camera view.

**NEVER disable frustum culling globally.** Only set `frustumCulled = false` on specific objects that MUST render regardless of camera (skyboxes, large particle systems, full-screen post-processing quads).

**Rule**: For `InstancedMesh`, frustum culling operates on the entire instance group as one bounding sphere. If instances are spread across a large area, split them into spatial groups for effective culling.

---

## Object Pooling

NEVER create and destroy objects every frame. Use object pools for frequently spawned/despawned objects:

```javascript
class MeshPool {
  constructor(geometry, material, poolSize) {
    this.pool = [];
    for (let i = 0; i < poolSize; i++) {
      const mesh = new THREE.Mesh(geometry, material);
      mesh.visible = false;
      this.pool.push(mesh);
    }
    this.activeIndex = 0;
  }

  acquire() {
    if (this.activeIndex >= this.pool.length) return null;
    const mesh = this.pool[this.activeIndex++];
    mesh.visible = true;
    return mesh;
  }

  release(mesh) {
    mesh.visible = false;
    const idx = this.pool.indexOf(mesh);
    if (idx !== -1 && idx < this.activeIndex) {
      [this.pool[idx], this.pool[this.activeIndex - 1]] =
        [this.pool[this.activeIndex - 1], this.pool[idx]];
      this.activeIndex--;
    }
  }
}
```

---

## CPU-Side Optimization

### Static Object Matrix Optimization

For objects that NEVER move after initial placement:

```javascript
object.matrixAutoUpdate = false;
object.updateMatrix(); // compute once
```

This prevents the renderer from recalculating the local matrix every frame for static objects.

### Avoid Allocations in the Render Loop

```javascript
// WRONG: creates new Vector3 every frame — GC pressure
function animate() {
  const pos = new THREE.Vector3(1, 2, 3); // NEVER allocate in loop
  mesh.position.copy(pos);
}

// CORRECT: reuse pre-allocated objects
const _tempVec = new THREE.Vector3();
function animate() {
  _tempVec.set(1, 2, 3);
  mesh.position.copy(_tempVec);
}
```

**Rule**: ALWAYS declare temporary math objects (`Vector3`, `Matrix4`, `Quaternion`, `Color`, `Box3`) outside the animation loop. Prefix with `_` to indicate they are reusable scratch variables.

---

## Shader and Material Optimization

| Action | Impact |
|--------|--------|
| Use `MeshStandardMaterial` instead of `MeshPhysicalMaterial` | Fewer shader instructions unless you need clearcoat/transmission/sheen |
| Minimize unique material count | Fewer shader compilations; ALWAYS share materials across identical meshes |
| Set `material.precision = 'mediump'` on mobile | Faster fragment shading on mobile GPUs |
| Avoid `onBeforeCompile` unless necessary | Each unique modification creates a new shader variant |

---

## Chrome DevTools Profiling

1. **Performance tab**: Record a few seconds, look for long "GPU" tasks and JS frame duration
2. **Memory tab**: Take heap snapshots before and after scene changes to find unreleased objects
3. **`renderer.info` logging**: Add a periodic `console.log(renderer.info.memory)` to detect leaks
4. **WebGL Inspector** (browser extension): Inspect draw calls, textures, and shader programs

---

## Critical Warnings

**NEVER** create `BufferGeometry`, `Material`, or `Texture` objects inside the render/animation loop. This causes memory to grow without bound.

**NEVER** call `renderer.render()` after `renderer.dispose()`. The WebGL context is destroyed.

**NEVER** dispose shared geometry/material/texture while other meshes still reference it. Track reference counts or dispose only when ALL consumers are removed.

**ALWAYS** dispose old textures before replacing: `if (material.map) material.map.dispose(); material.map = newTexture;`

**ALWAYS** call `controls.dispose()` when removing OrbitControls or other control instances. Failing to do so leaks DOM event listeners.

**ALWAYS** set `instanceMatrix.needsUpdate = true` after calling `setMatrixAt()` on an `InstancedMesh`. Without this, instances render at the origin.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Disposal and profiling API signatures
- [references/examples.md](references/examples.md) -- Performance optimization code examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Common performance mistakes and fixes

### Official Sources

- Disposal guide: https://threejs.org/docs/#manual/en/introduction/How-to-dispose-of-objects
- WebGLRenderer.info: https://threejs.org/docs/#api/en/renderers/WebGLRenderer
- InstancedMesh: https://threejs.org/docs/#api/en/objects/InstancedMesh
- LOD: https://threejs.org/docs/#api/en/objects/LOD
- BufferGeometryUtils: https://threejs.org/docs/#examples/en/utils/BufferGeometryUtils
