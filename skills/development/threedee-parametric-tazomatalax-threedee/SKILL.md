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
│   ├── main.js          # Main scene, camera, lighting, demo object
│   └── exporters.js     # STL/OBJ/glTF export utilities
├── user/
│   ├── models/          # User's parametric model definitions
│   └── exports/         # Generated mesh files (STL, OBJ, glTF)
└── index.html           # Viewport UI
```

## Quick Reference

### Creating Objects

Edit `src/main.js` in the "Demo Object" section:

```javascript
// Basic primitives
const geometry = new THREE.BoxGeometry(2, 1, 3);           // width, height, depth
const geometry = new THREE.SphereGeometry(1, 32, 32);      // radius, segments
const geometry = new THREE.CylinderGeometry(1, 1, 2, 32);  // topR, bottomR, height
const geometry = new THREE.TorusGeometry(1, 0.4, 16, 100); // radius, tube, segments
const geometry = new THREE.TorusKnotGeometry(1, 0.35, 128, 32); // current demo

// Material
const material = new THREE.MeshStandardMaterial({
  color: 0x4a5568,    // hex color
  metalness: 0.3,     // 0-1
  roughness: 0.4,     // 0-1
});

// Create mesh and add to scene
const mesh = new THREE.Mesh(geometry, material);
mesh.position.set(x, y, z);
mesh.castShadow = true;
scene.add(mesh);
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

For reusable models, use the pattern in `user/models/`:

```javascript
export const parameters = {
  width: 40,
  height: 20,
  depth: 40,
  color: 0x4a90d9,
};

export function createGeometry(params = parameters) {
  return new THREE.BoxGeometry(params.width, params.height, params.depth);
}

export function createMesh(params = parameters) {
  const geometry = createGeometry(params);
  const material = new THREE.MeshStandardMaterial({ color: params.color });
  return new THREE.Mesh(geometry, material);
}
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

## Workflow

1. User requests a 3D object or modification
2. Edit `src/main.js` (or create file in `user/models/`)
3. Save — Vite hot-reloads the viewport automatically
4. User sees result at http://localhost:3002
5. Export when ready via console commands

## Important Notes

- The viewport runs at `http://localhost:3002` (or next available port)
- Y-axis is up (standard Three.js convention)
- Objects should be positioned with `y > 0` to sit above the grid
- The `mesh` variable is exported and accessible in console
- All changes hot-reload instantly—no refresh needed

## References

For advanced geometry and CSG operations, see [references/geometry.md](references/geometry.md).
