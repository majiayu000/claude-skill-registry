---
name: threejs-impl-ifc-viewer
description: >
  Use when loading and viewing IFC/BIM models in a Three.js scene.
  Prevents the common mistake of using deprecated web-ifc-three,
  ignoring AGPL-3.0 license implications, or loading large IFC files
  without streaming. Covers web-ifc (MIT), @thatopen/components
  (AGPL-3.0), IFC loading, spatial tree, property extraction.
  Keywords: IFC, BIM, web-ifc, IFC viewer, @thatopen/components,
  building model, architecture, IFC loading, spatial tree, BIM viewer.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-ifc-viewer

## Quick Reference

### Library Comparison

| Library | License | Level | Status | Use Case |
|---------|---------|-------|--------|----------|
| `web-ifc` | MIT | Low-level WASM parser | Active (v0.77+) | Custom pipelines, full control |
| `@thatopen/components` | MIT (v3.x) | High-level BIM toolkit | Active (v3.3.2+) | Full BIM viewers, rapid prototyping |
| `@thatopen/components-front` | MIT | Browser-specific extensions | Active | UI, advanced visualization |
| `web-ifc-three` | — | Deprecated bridge | **DEAD** | **NEVER use** |
| `openbim-components` (v1) | — | Deprecated toolkit | **DEAD** | **NEVER use** |

### Package Installation

```bash
# Low-level approach (MIT, full control)
npm install web-ifc three

# High-level approach (MIT, batteries-included)
npm install @thatopen/components @thatopen/components-front web-ifc three
```

### Critical Warnings

**LICENSE HISTORY WARNING**: The @thatopen packages (v3.x) are licensed under **MIT**. However, older IFC.js ecosystem packages (openbim-components v1, IFC.js v0.x) used **AGPL-3.0**. ALWAYS verify the license of the exact package version you install. If using any package with AGPL-3.0, your entire application MUST be open-sourced under AGPL-3.0 or a compatible license.

**NEVER** use `web-ifc-three` -- it is deprecated and unmaintained. Use `web-ifc` directly or `@thatopen/components` instead.

**NEVER** use `openbim-components` (v1) -- it is deprecated. Use `@thatopen/components` (v3.x) instead.

**NEVER** load entire IFC geometry at once for files >50MB -- ALWAYS stream or load geometry on demand. WASM memory is limited and cannot be reclaimed without page reload.

**NEVER** forget to call `ifcApi.CloseModel(modelID)` after processing -- WASM memory leaks are permanent until page reload.

**ALWAYS** call `components.dispose()` when unmounting a @thatopen viewer -- failure to do so leaks GPU memory, Three.js objects, and event listeners.

**ALWAYS** initialize `IfcAPI` asynchronously -- `await ifcApi.Init()` MUST complete before any model operations.

---

## Approach 1: web-ifc (Low-Level WASM Parser)

### When to Use

- You need full control over geometry extraction and rendering
- You are building a custom rendering pipeline
- You want MIT-licensed code only
- You need to extract IFC properties without rendering geometry

### WASM Setup

```javascript
import * as WebIFC from 'web-ifc';

const ifcApi = new WebIFC.IfcAPI();
ifcApi.SetWasmPath('./');  // MUST point to directory containing web-ifc.wasm
await ifcApi.Init();       // ALWAYS await before any operations
```

**WASM file requirement**: The `web-ifc.wasm` file MUST be served from a location accessible by the browser. Copy it from `node_modules/web-ifc/` to your public/static directory. Bundlers like Vite require explicit configuration to serve WASM files.

### IfcAPI Core Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Init()` | `() => Promise<void>` | Initialize WASM module |
| `SetWasmPath(path)` | `(string) => void` | Set directory containing .wasm file |
| `OpenModel(data, settings?)` | `(Uint8Array, object?) => number` | Load IFC data, returns modelID |
| `CloseModel(modelID)` | `(number) => void` | Release model memory |
| `GetGeometry(modelID, expressID)` | `(number, number) => object` | Get geometry for element |
| `GetFlatMesh(modelID, expressID)` | `(number, number) => FlatMesh` | Get flattened mesh data |
| `GetPlacedGeometry(modelID, pg)` | `(number, PlacedGeometry) => MeshData` | Get positioned geometry with transform |
| `GetLine(modelID, expressID, flatten?)` | `(number, number, boolean?) => object` | Read single IFC entity by expressID |
| `GetAllLines(modelID)` | `(number) => number[]` | Get all express IDs in model |
| `GetLineIDsWithType(modelID, type)` | `(number, number) => number[]` | Get IDs by IFC type constant |
| `GetAllTypesOfModel(modelID)` | `(number) => TypeInfo[]` | List all entity types in model |

### Geometry Extraction Pattern

```javascript
const modelID = ifcApi.OpenModel(ifcData); // ifcData: Uint8Array

const wallIDs = ifcApi.GetLineIDsWithType(modelID, WebIFC.IFCWALL);
for (const wallID of wallIDs) {
  const flatMesh = ifcApi.GetFlatMesh(modelID, wallID);
  for (const pg of flatMesh.geometries) {
    const meshData = ifcApi.GetPlacedGeometry(modelID, pg);
    // meshData.vertexData: Float32Array (interleaved position + normal, 6 floats per vertex)
    // meshData.indexData: Uint32Array (triangle indices)
    // pg.flatTransformation: Float64Array (4x4 column-major matrix)
    // pg.color: { x: r, y: g, z: b, w: alpha } (0-1 range)
  }
}

ifcApi.CloseModel(modelID); // ALWAYS release when done
```

### Converting web-ifc Geometry to Three.js

```javascript
import * as THREE from 'three';

function ifcMeshToThree(meshData, placedGeometry) {
  const { vertexData, indexData } = meshData;

  // vertexData is interleaved: [px, py, pz, nx, ny, nz, px, py, pz, nx, ny, nz, ...]
  const posFloats = new Float32Array(vertexData.length / 2);
  const normFloats = new Float32Array(vertexData.length / 2);
  for (let i = 0; i < vertexData.length; i += 6) {
    const j = i / 2;
    posFloats[j]     = vertexData[i];
    posFloats[j + 1] = vertexData[i + 1];
    posFloats[j + 2] = vertexData[i + 2];
    normFloats[j]     = vertexData[i + 3];
    normFloats[j + 1] = vertexData[i + 4];
    normFloats[j + 2] = vertexData[i + 5];
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(posFloats, 3));
  geometry.setAttribute('normal', new THREE.BufferAttribute(normFloats, 3));
  geometry.setIndex(new THREE.BufferAttribute(indexData, 1));

  const { x: r, y: g, z: b, w: a } = placedGeometry.color;
  const material = new THREE.MeshPhongMaterial({
    color: new THREE.Color(r, g, b),
    opacity: a,
    transparent: a < 1,
    side: THREE.DoubleSide,
  });

  const mesh = new THREE.Mesh(geometry, material);

  // Apply the 4x4 transform matrix (column-major)
  const mat = new THREE.Matrix4();
  mat.fromArray(placedGeometry.flatTransformation);
  mesh.applyMatrix4(mat);

  return mesh;
}
```

### IFC Property Extraction

```javascript
// Read a specific entity
const wall = ifcApi.GetLine(modelID, wallExpressID, true); // flatten=true resolves references
console.log(wall.Name?.value);       // "Basic Wall:Generic - 200mm"
console.log(wall.GlobalId?.value);   // IFC GUID

// Get all property sets for an element
const relDefines = ifcApi.GetLineIDsWithType(modelID, WebIFC.IFCRELDEFINESBYPROPERTIES);
for (const relID of relDefines) {
  const rel = ifcApi.GetLine(modelID, relID, false);
  // Check if this relation references our element
  // rel.RelatedObjects contains expressIDs of related elements
  // rel.RelatingPropertyDefinition points to the property set
}
```

### IFC Type Constants

| Constant | IFC Entity |
|----------|-----------|
| `WebIFC.IFCWALL` | Walls |
| `WebIFC.IFCWALLSTANDARDCASE` | Standard walls |
| `WebIFC.IFCSLAB` | Slabs / floors |
| `WebIFC.IFCCOLUMN` | Columns |
| `WebIFC.IFCBEAM` | Beams |
| `WebIFC.IFCDOOR` | Doors |
| `WebIFC.IFCWINDOW` | Windows |
| `WebIFC.IFCROOF` | Roofs |
| `WebIFC.IFCSTAIR` | Stairs |
| `WebIFC.IFCSPACE` | Spaces / rooms |
| `WebIFC.IFCSITE` | Site |
| `WebIFC.IFCBUILDING` | Building |
| `WebIFC.IFCBUILDINGSTOREY` | Storey / floor level |
| `WebIFC.IFCPROJECT` | Project root |
| `WebIFC.IFCRELDEFINESBYPROPERTIES` | Property set relations |
| `WebIFC.IFCPROPERTYSET` | Property sets |
| `WebIFC.IFCPROPERTYSINGLEVALUE` | Individual property values |

---

## Approach 2: @thatopen/components (High-Level BIM Toolkit)

### When to Use

- You need a full-featured BIM viewer quickly
- You want built-in fragment optimization for large models
- You need element highlighting, section planes, or floor plans
- MIT license (v3.x) is acceptable for your project

### Architecture Setup

```javascript
import * as OBC from '@thatopen/components';

const components = new OBC.Components();
const worlds = components.get(OBC.Worlds);
const world = worlds.create();

// Scene
world.scene = new OBC.SimpleScene(components);
world.scene.setup(); // Adds default lights and grid

// Camera
world.camera = new OBC.SimpleCamera(components);
world.camera.controls.setLookAt(10, 10, 10, 0, 0, 0);

// Renderer (container is an HTMLDivElement)
world.renderer = new OBC.SimpleRenderer(components, container);

// ALWAYS call init after setup
components.init();
```

### Loading IFC Files

```javascript
const ifcLoader = components.get(OBC.IfcLoader);
await ifcLoader.setup(); // Downloads and initializes WASM

// Load from file input
const file = event.target.files[0];
const data = new Uint8Array(await file.arrayBuffer());
const model = await ifcLoader.load(data);

// model is added to the active world automatically
// model contains Three.js Group with fragment meshes
```

### Key Components

| Component | Access Pattern | Purpose |
|-----------|---------------|---------|
| `OBC.Components` | `new OBC.Components()` | Central manager for all subsystems |
| `OBC.Worlds` | `components.get(OBC.Worlds)` | Multi-world environment management |
| `OBC.SimpleScene` | Constructor | Three.js scene wrapper with defaults |
| `OBC.SimpleCamera` | Constructor | Camera with built-in orbit controls |
| `OBC.SimpleRenderer` | Constructor | WebGL renderer bound to DOM element |
| `OBC.IfcLoader` | `components.get(OBC.IfcLoader)` | IFC file loading and fragment conversion |
| `OBC.FragmentsManager` | `components.get(OBC.FragmentsManager)` | Efficient batched geometry management |
| `OBC.Highlighter` | `components.get(OBC.Highlighter)` | Element selection and highlighting |
| `OBC.Clipper` | `components.get(OBC.Clipper)` | Section plane tools |
| `OBC.Plans` | `components.get(OBC.Plans)` | Floor plan generation |

### Fragment System

The fragment system converts IFC geometry into batched draw calls. This is critical for performance with large BIM models (10,000+ elements).

- Each IFC type gets batched into a single fragment mesh
- Fragments share materials where possible, minimizing state changes
- Individual elements can still be picked, highlighted, and hidden by expressID
- ALWAYS use fragments for models with >1,000 elements

### Cleanup

```javascript
// ALWAYS dispose when unmounting the viewer
components.dispose();
// This releases: Three.js scene, renderer, geometries, materials, textures,
// WASM memory, event listeners, and all component state
```

---

## IFC Spatial Tree

IFC files follow a hierarchical spatial structure:

```
IFCPROJECT
  └── IFCSITE
        └── IFCBUILDING
              ├── IFCBUILDINGSTOREY (Level 0)
              │     ├── IFCWALL
              │     ├── IFCSLAB
              │     └── IFCSPACE
              └── IFCBUILDINGSTOREY (Level 1)
                    ├── IFCWALL
                    ├── IFCCOLUMN
                    └── IFCDOOR
```

Spatial containment is defined by `IFCRELCONTAINEDINSPATIALSTRUCTURE` and `IFCRELAGGREGATES` relationships. ALWAYS traverse these relationships to build a navigable tree -- do NOT assume flat element lists represent the building structure.

---

## Memory Management for Large IFC Files

| File Size | Strategy |
|-----------|----------|
| <10MB | Load entirely, render all geometry at once |
| 10-50MB | Load entirely, use fragment batching |
| 50-200MB | Stream geometry by storey or type, dispose unused |
| >200MB | Server-side preprocessing into fragments, load on demand |

### Rules

- ALWAYS monitor WASM heap usage -- web-ifc allocates in WASM linear memory which has a hard cap
- ALWAYS dispose geometry that is not currently visible (off-screen storeys, hidden types)
- NEVER keep duplicate geometry in both WASM and JavaScript heap
- ALWAYS use `BufferGeometry` (never legacy `Geometry`)
- ALWAYS call `geometry.dispose()` and `material.dispose()` when removing meshes from scene

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for web-ifc and @thatopen/components
- [references/examples.md](references/examples.md) -- Working code examples for IFC loading and viewing
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do when working with IFC in Three.js

### Official Sources

- https://github.com/IFCjs/web-ifc
- https://github.com/ThatOpen/engine_components
- https://docs.thatopen.com/
- https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/
