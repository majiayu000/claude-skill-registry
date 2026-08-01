---
name: threedee-parametric
description: 'Create and modify 3D parametric models in the threedee design environment.
  Use when: (1) creating new 3D objects, geometries, or meshes, (2) modifying parameters
  like dimensions, colors, materials, (3'
---

---
name: threedee-parametric
description: Create and modify 3D parametric models in the threedee design environment. Use when: (1) creating new 3D objects, geometries, or meshes, (2) modifying parameters like dimensions, colors, materials, (3) adding primitives (boxes, spheres, cylinders, torus knots), (4) setting up lighting or camera, (5) exporting models to STL/OBJ/glTF, (6) working with Three.js code in this project. Triggers on requests involving 3D modeling, CAD-like operations, parametric design, or mesh creation.
---

# threedee Parametric Design

A live-updating 3D viewport for parametric modeling with AI assistance. Edit code in VS Code, see results instantly in the browser.

## Project Structure

```
threedee/
├── src/
│   ├── main.js          # Main scene, camera, lighting, model loader
│   └── exporters.js     # STL/OBJ/glTF export utilities
├── user/
│   ├── models/          # User's parametric model definitions (auto-discovered!)
│   └── exports/         # Generated mesh files (STL, OBJ, glTF)
└── index.html           # Viewport UI with model selector
```

## Creating New Models (Recommended Workflow)

**Models are automatically discovered!** Simply create a new `.js` file in `user/models/` and it will appear in the UI dropdown after a page refresh.

### Step 1: Create a Model File

Create a new file in `user/models/` with a descriptive kebab-case name (e.g., `my-bracket.js`).
The filename becomes the model ID and is converted to Title Case in the UI.

### Step 2: Export Required Functions

Every model file **must** export a `createMesh()` function:

```javascript
// user/models/my-bracket.js
import * as THREE from 'three';

export const parameters = {
  width: 40,
  height: 20,
  thickness: 5,
  color: 0x4a90d9,
};

export function createMesh(userParams = {}) {
  const params = { ...parameters, ...userParams };

  const geometry = new THREE.BoxGeometry(
    params.width,
    params.height,
    params.thickness
  );
  const material = new THREE.MeshStandardMaterial({ color: params.color });
  const mesh = new THREE.Mesh(geometry, material);

  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.position.y = params.height / 2; // Sit on ground plane

  return mesh;
}
```

### Step 3: Save and View

1. Save the file
2. The browser will hot-reload (or refresh if needed)
3. Select your new model from the **MODEL** dropdown in the top-left
4. Export when ready using the **EXPORT MODEL** panel

## Quick Reference

### Basic Primitives

```javascript
const geometry = new THREE.BoxGeometry(2, 1, 3);           // width, height, depth
const geometry = new THREE.SphereGeometry(1, 32, 32);      // radius, segments
const geometry = new THREE.CylinderGeometry(1, 1, 2, 32);  // topR, bottomR, height
const geometry = new THREE.TorusGeometry(1, 0.4, 16, 100); // radius, tube, segments
const geometry = new THREE.TorusKnotGeometry(1, 0.35, 128, 32);
```

### Common Modifications

**Change object color:**
```javascript
material.color.setHex(0x22d3ee);  // cyan accent
```

**Position object:**
```javascript
mesh.position.y = 1.5;  // lift above ground
mesh.position.set(0, 1.5, 0);  // x, y, z
```

**Scale object:**
```javascript
mesh.scale.set(2, 1, 1);  // stretch in x
```

**Rotate object:**
```javascript
mesh.rotation.y = Math.PI / 4;  // 45 degrees
```

### Parametric Pattern

For reusable models, always merge with default parameters to handle partial updates correctly:

```javascript
export const parameters = {
  width: 40,
  height: 20,
  depth: 40,
  color: 0x4a90d9,
};

export function createGeometry(userParams = {}) {
  const params = { ...parameters, ...userParams };
  return new THREE.BoxGeometry(params.width, params.height, params.depth);
}

export function createMesh(userParams = {}) {
  const params = { ...parameters, ...userParams };
  const geometry = createGeometry(params);
  const material = new THREE.MeshStandardMaterial({ color: params.color });
  return new THREE.Mesh(geometry, material);
}
```

### Geometry Merging Best Practices

When combining different geometry types (e.g., mixing `BoxGeometry` with `ExtrudeGeometry`), they often have incompatible index buffers which causes `mergeGeometries` to fail.

**Always convert to non-indexed** before merging to ensure compatibility:

```javascript
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

// ... create geometries ...

// Convert all to non-indexed before merging to avoid attribute/index conflicts
const compatibleGeometries = [geo1, geo2, geo3].map(g => g.toNonIndexed());
const merged = mergeGeometries(compatibleGeometries);

// Optional: Weld vertices afterwards if smooth shading is needed
// import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
// const smooth = mergeVertices(merged);
```

### Exporting Models

Export the active 3D model to various formats using the browser console or programmatically:

#### Single Format Exports
```javascript
// STL (3D printing)
threedeeExport.stl(mesh, "my-part")         // Binary (recommended)
threedeeExport.stlAscii(mesh, "my-part")   // ASCII text format

// General interchange
threedeeExport.obj(mesh, "my-part")        // OBJ with UVs and normals

// Web and AR
threedeeExport.gltf(mesh, "my-part")       // glTF (JSON)
threedeeExport.glb(mesh, "my-part")        // GLB (binary, compact)

// CAD interchange
threedeeExport.step(mesh, "my-part")       // STEP Faceted B-Rep
```

#### Batch Export (All Formats)
```javascript
// Export to STL, OBJ, glTF, and STEP simultaneously
await threedeeExport.all(mesh, "my-part")

// Export to specific formats
await threedeeExport.all(mesh, "my-part", ['stl', 'step', 'obj'])
```

#### Export Notes
- Files are automatically timestamped: `my-part_2025-12-30_23-02-15.stl`
- Browser downloads are triggered automatically
- Console logs confirm successful exports
- The `mesh` variable is always available in the console and accessible via `window.mesh`

### Lighting Adjustment

```javascript
keyLight.intensity = 1.5;           // brighter
keyLight.position.set(10, 15, 10);  // move light
rimLight.color.setHex(0xff6600);    // orange rim
```

## Advanced Modeling & Slicer Compatibility

When creating complex procedural shapes (like gyroids or lattices) intended for 3D printing, follow these best practices to ensure "watertight" models and high-quality exports.

### Marching Cubes Best Practices

If using `MarchingCubes`, configure it for high resolution and clean boundaries:

1.  **Polygon Budget**: Always set a high `maxPolyCount` (e.g., `1,000,000`) for high-resolution meshes to prevent model sections from being "cut off" due to buffer limits.
2.  **Watertight Boundaries**: Use **padding** in your scalar field. Never let the isosurface (boundary) sit exactly on the domain edge. Sample a slightly larger domain than the actual object size to ensure the Marching Cubes algorithm can "close" the mesh.
3.  **Boundary Smoothing**: When clipping shapes (e.g., using `Math.max` for a cylinder boundary), use a multiplier (e.g., `* 5` or `* 10`) for the boundary distance to create a smooth gradient that the interpolator can follow.
4.  **Vertex Welding**: Always use `mergeVertices` from `BufferGeometryUtils` after `mc.update()` to weld coincident vertices. This fixes "cracks" and "open edges" that slicers often report.

```javascript
import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

// ... inside createMesh ...
const mc = new MarchingCubes(resolution, material, false, false, 1000000);
// ... fill field ...
mc.update();

// Weld and recompute normals
const welded = mergeVertices(mc.geometry, 1e-5);
welded.computeVertexNormals();
mc.geometry.dispose();
mc.geometry = welded;
```

### Ensuring Export Quality

The [src/exporters.js](src/exporters.js) utilities include an automated preparation step for STL exports that handles:
- Coordinate system normalization (baking world transforms).
- Vertex welding and normal correction.
- Removal of degenerate (zero-area) triangles.

## Workflow

### Creating vs Iterating

**IMPORTANT:** When asked to improve, refine, or iterate on an existing model:
- **DO:** Edit the existing model file directly (e.g., modify `user/models/tree.js`)
- **DON'T:** Create new files like `tree-v2.js`, `tree-improved.js`, `realistic-tree.js`

Only create a new file when the user explicitly asks for a **new, separate model**.

### Standard Workflow

1. User requests a new 3D object → Create a new file in `user/models/`
2. User requests improvements/changes → **Edit the existing model file**
3. Save — the viewport hot-reloads instantly
4. The user's selected model persists across page refreshes
5. Export when ready via the **EXPORT MODEL** panel

### Iteration Examples

**User says:** "Make the tree more realistic"
**Action:** Edit `user/models/tree.js` to improve the existing code

**User says:** "Add more branches and better textures"
**Action:** Edit `user/models/tree.js` to add the requested features

**User says:** "Create a pine tree (separate from the oak tree)"
**Action:** Create a new file `user/models/pine-tree.js`

### Console Commands

Models can also be loaded programmatically:
```javascript
// Load a model by ID (filename without .js)
await loadModel('shelf-bracket');

// List all available models
console.log(modelList);

// Access current mesh
window.mesh
```

## Important Notes

- The viewport runs at `http://localhost:3002` (or next available port)
- **Models are auto-discovered** from `user/models/*.js` — no manual registration needed!
- **Selected model persists** across page refreshes via localStorage
- Model filenames use kebab-case (e.g., `my-widget.js`) and display as Title Case in the UI
- Y-axis is up (standard Three.js convention)
- Objects should be positioned with `y > 0` to sit above the grid
- The `mesh` variable is exported and accessible in console via `window.mesh`
- All changes hot-reload instantly—no refresh needed
- **When iterating: edit the existing file, don't create new versions**

## References

For advanced geometry and CSG operations, see [references/geometry.md](references/geometry.md).
