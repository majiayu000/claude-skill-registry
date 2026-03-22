---
name: threejs-agents-model-optimizer
description: >
  Use when optimizing 3D models for web delivery: reducing file size,
  compressing meshes, optimizing textures, or generating LOD. Provides
  a complete GLTF optimization pipeline using Draco, KTX2, mesh
  simplification, and gltf-transform.
  Keywords: optimize model, reduce file size, Draco compression, KTX2,
  gltf-transform, mesh simplification, LOD, GLTF optimize, bundle size.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-agents-model-optimizer

## Quick Reference

### Optimization Pipeline Overview

```
INPUT (.glb/.gltf)
  |
  v
[1. ASSESS] ── polygon count, texture sizes, file size, draw calls
  |
  v
[2. MESH OPTIMIZE] ── dedup, flatten, join, weld, simplify
  |
  v
[3. TEXTURE OPTIMIZE] ── resize, KTX2 compress, atlas
  |
  v
[4. COMPRESS] ── Draco mesh compression, quantize attributes
  |
  v
[5. VALIDATE] ── visual diff, file size check, runtime test
  |
  v
OUTPUT (optimized .glb)
```

### Target File Size Budgets

| Platform | Max File Size | Max Polygons | Max Texture Size |
|----------|--------------|--------------|------------------|
| Mobile web | 2 MB | 50K triangles | 1024x1024 |
| Desktop web | 5 MB | 200K triangles | 2048x2048 |
| Desktop app | 20 MB | 500K triangles | 4096x4096 |
| Hero asset (single) | 1 MB | 30K triangles | 1024x1024 |

### Tool Selection

| Tool | Best For | Install |
|------|----------|---------|
| `gltf-transform` | Full pipeline, scriptable, Node.js API | `npm i @gltf-transform/cli` |
| `gltfpack` | Fast one-shot compression | `npm i -g gltfpack` |
| Blender | Manual mesh editing, UV repacking | Blender 3.6+ |

### Critical Warnings

**NEVER** skip the assessment step -- optimizing blindly wastes time and can produce worse results than the original.

**NEVER** apply Draco compression AND meshopt compression to the same file -- they are mutually exclusive. Choose ONE.

**NEVER** use KTX2 UASTC for diffuse color maps on mobile -- UASTC textures are 8-16 bytes/texel in VRAM. ALWAYS use ETC1S for color maps on mobile targets.

**NEVER** simplify meshes below 10% of original without visual validation -- aggressive simplification destroys silhouettes and UV mapping.

**ALWAYS** validate optimized models visually before shipping -- automated metrics cannot catch all visual artifacts.

**ALWAYS** keep the original unoptimized model in version control -- optimization is lossy and irreversible.

---

## Step 1: Assessment

Before optimizing, ALWAYS gather these metrics:

```bash
# Using gltf-transform CLI
npx gltf-transform inspect model.glb

# Key output to check:
# - Mesh count and total triangle count
# - Texture count, dimensions, and format
# - Total file size (uncompressed)
# - Accessor count (indicates potential deduplication)
# - Animation track count
```

### Assessment Decision Tree

```
File size > target budget?
├── YES: Textures > 50% of file size?
│   ├── YES → Start with texture optimization (Step 3)
│   └── NO → Start with mesh optimization (Step 2)
└── NO: Draw calls > 50?
    ├── YES → Merge meshes (join/flatten)
    └── NO → Only apply compression (Step 4)
```

### Polygon Count Guidelines

| Asset Type | Target Triangles | Notes |
|------------|-----------------|-------|
| Background prop | 100-500 | Minimal detail |
| Mid-ground object | 1K-5K | Visible but not hero |
| Hero/focus object | 10K-50K | High detail, close-up |
| Character | 15K-30K | With LOD chain |
| Full scene | 100K-300K | All objects combined |
| Architectural (BIM) | 200K-500K | Simplified from CAD |

---

## Step 2: Mesh Optimization

### gltf-transform Mesh Pipeline

ALWAYS run these operations in this order:

```bash
# 1. Remove duplicate accessors and unused data
npx gltf-transform dedup input.glb deduped.glb

# 2. Flatten node hierarchy (removes empty nodes)
npx gltf-transform flatten deduped.glb flat.glb

# 3. Join meshes sharing the same material
npx gltf-transform join flat.glb joined.glb

# 4. Weld vertices (merge vertices within tolerance)
npx gltf-transform weld joined.glb welded.glb --tolerance 0.0001

# 5. Simplify mesh (reduce triangle count)
npx gltf-transform simplify welded.glb simplified.glb \
  --ratio 0.5 \
  --error 0.001

# 6. Remove unused resources
npx gltf-transform prune simplified.glb output.glb
```

### Combined Pipeline (Single Command)

```bash
npx gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress ktx2
```

### Mesh Simplification Settings

| Quality Level | Ratio | Error Tolerance | Use Case |
|--------------|-------|-----------------|----------|
| Minimal | 0.75 | 0.0005 | Subtle reduction, preserves detail |
| Moderate | 0.50 | 0.001 | Balanced quality/size |
| Aggressive | 0.25 | 0.005 | LOD1/LOD2 generation |
| Extreme | 0.10 | 0.01 | LOD3, distant objects only |

### Weld Settings

| Tolerance | Effect |
|-----------|--------|
| 0.0001 | Conservative -- merges only nearly-identical vertices |
| 0.001 | Standard -- good for most models |
| 0.01 | Aggressive -- may cause visible seams on hard edges |

---

## Step 3: Texture Optimization

### Texture Decision Tree

```
Texture type?
├── Color/Diffuse (baseColorTexture)
│   ├── Mobile → ETC1S (KTX2), max 1024px
│   └── Desktop → UASTC (KTX2), max 2048px
├── Normal map
│   └── ALWAYS UASTC (KTX2) — ETC1S causes visible artifacts on normals
├── ORM (occlusion/roughness/metallic)
│   └── ETC1S (KTX2) — perceptual quality less critical
├── Emissive
│   └── ETC1S (KTX2) — unless HDR, then keep as-is
└── HDR environment
    └── Keep as .hdr or .exr — do NOT KTX2 compress
```

### KTX2 Compression Commands

```bash
# ETC1S — smaller file, lower quality (color maps, ORM)
npx gltf-transform ktx2 input.glb output.glb \
  --slots "baseColorTexture,emissiveTexture,occlusionTexture" \
  --filter "baseColorTexture=etc1s" \
  --quality 128

# UASTC — larger file, higher quality (normal maps)
npx gltf-transform ktx2 input.glb output.glb \
  --slots "normalTexture" \
  --filter "normalTexture=uastc"
```

### KTX2: ETC1S vs UASTC

| Property | ETC1S | UASTC |
|----------|-------|-------|
| File size | Very small (6-8x smaller) | Moderate (2-4x smaller) |
| VRAM usage | Small | Large (8-16 bytes/texel) |
| Quality | Good for color | Near-lossless |
| Decode speed | Fast | Requires transcoding |
| Best for | Color maps, ORM, emissive | Normal maps, detail textures |

### Texture Resize

```bash
# Resize all textures to max 1024x1024
npx gltf-transform resize input.glb output.glb --width 1024 --height 1024

# Resize only textures larger than 2048px
npx gltf-transform resize input.glb output.glb --width 2048 --height 2048
```

---

## Step 4: Mesh Compression

### Draco Compression

```bash
# Default Draco compression
npx gltf-transform draco input.glb output.glb

# Draco with quality settings
npx gltf-transform draco input.glb output.glb \
  --quantize-position 14 \
  --quantize-normal 10 \
  --quantize-texcoord 12 \
  --quantize-color 8
```

### Draco Quantization Bits

| Attribute | Default | High Quality | Aggressive |
|-----------|---------|-------------|------------|
| Position | 14 bits | 16 bits | 11 bits |
| Normal | 10 bits | 12 bits | 8 bits |
| TexCoord | 12 bits | 14 bits | 10 bits |
| Color | 8 bits | 10 bits | 6 bits |

Higher bits = better quality, larger file. 14-bit position is sufficient for most models.

### Quantize Without Draco

```bash
# Quantize attributes (reduces file size without Draco dependency)
npx gltf-transform quantize input.glb output.glb
```

### Loading Draco-Compressed Models in Three.js

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const dracoLoader = new DRACOLoader();
// ALWAYS set the decoder path — Draco uses WASM
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
dracoLoader.preload();

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

gltfLoader.load('model-draco.glb', (gltf) => {
  scene.add(gltf.scene);
});

// ALWAYS dispose when done
dracoLoader.dispose();
```

### Loading KTX2-Compressed Textures

```javascript
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader();
// ALWAYS set the transcoder path — KTX2 uses WASM basis_transcoder
ktx2Loader.setTranscoderPath('https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/basis/');
ktx2Loader.detectSupport(renderer);

const gltfLoader = new GLTFLoader();
gltfLoader.setKTX2Loader(ktx2Loader);
```

---

## Step 5: Validation

### Validation Checklist

After optimization, ALWAYS verify:

1. **File size** -- meets target budget from Step 1
2. **Visual quality** -- load in Three.js viewer, compare to original
3. **Bounding box** -- same dimensions as original (no scale errors)
4. **Materials** -- all textures load, no missing maps
5. **Animations** -- all clips play correctly (if applicable)
6. **Performance** -- measure draw calls, frame time

```bash
# Compare file sizes
ls -la original.glb optimized.glb

# Validate GLTF structure
npx gltf-transform inspect optimized.glb

# Check for errors
npx gltf-transform validate optimized.glb
```

---

## LOD Generation

### LOD Chain Strategy

| LOD Level | Screen Coverage | Triangle Ratio | Distance |
|-----------|----------------|----------------|----------|
| LOD0 | >30% screen | 1.0 (full) | Near |
| LOD1 | 10-30% screen | 0.5 | Medium |
| LOD2 | 3-10% screen | 0.25 | Far |
| LOD3 | <3% screen | 0.10 | Very far |

### Generating LODs with gltf-transform

```bash
# Generate LOD chain
npx gltf-transform simplify model.glb lod0.glb --ratio 1.0
npx gltf-transform simplify model.glb lod1.glb --ratio 0.5 --error 0.001
npx gltf-transform simplify model.glb lod2.glb --ratio 0.25 --error 0.005
npx gltf-transform simplify model.glb lod3.glb --ratio 0.10 --error 0.01
```

### Three.js LOD Implementation

```javascript
import * as THREE from 'three';

const lod = new THREE.LOD();

// ALWAYS add LODs from highest to lowest detail
lod.addLevel(meshLOD0, 0);    // distance 0 = closest
lod.addLevel(meshLOD1, 10);   // switch at 10 units
lod.addLevel(meshLOD2, 30);   // switch at 30 units
lod.addLevel(meshLOD3, 80);   // switch at 80 units

scene.add(lod);

// In render loop — ALWAYS call update for LOD switching
lod.update(camera);
```

---

## gltfpack Alternative

For quick one-shot optimization without a pipeline:

```bash
# Install
npm install -g gltfpack

# Optimize with meshopt compression
gltfpack -i input.glb -o output.glb -cc -tc

# Flags:
# -cc  mesh compression (meshopt)
# -tc  texture compression (KTX2/BasisU)
# -si N  simplify to ratio (0.0-1.0)
# -tp  texture power-of-two resize
```

**NEVER** mix gltfpack meshopt output with gltf-transform Draco -- the compression formats are incompatible.

### Loading Meshopt-Compressed Models

```javascript
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';

const gltfLoader = new GLTFLoader();
gltfLoader.setMeshoptDecoder(MeshoptDecoder);
```

---

## Blender Export Optimization

When exporting from Blender to glTF:

| Setting | Recommended Value | Why |
|---------|-------------------|-----|
| Format | glTF Binary (.glb) | Single file, smaller |
| Apply Modifiers | ON | Bakes procedural geometry |
| Compression | OFF | Compress with gltf-transform after |
| Textures | Include | Embedded in .glb |
| Limit to | Selected Objects | Avoid exporting hidden/unused |
| +Y Up | ON | Three.js convention |

**NEVER** enable Draco in Blender's exporter -- Blender's Draco implementation is outdated. ALWAYS compress with gltf-transform or gltfpack after export.

---

## Node.js Scripting with gltf-transform API

```javascript
import { NodeIO } from '@gltf-transform/core';
import { dedup, flatten, join, weld, simplify,
         textureCompress, draco, prune, quantize } from '@gltf-transform/functions';
import draco3d from 'draco3dgltf';
import sharp from 'sharp';

const io = new NodeIO()
  .registerExtensions(KHRONOS_EXTENSIONS)
  .registerDependencies({
    'draco3d.decoder': await draco3d.createDecoderModule(),
    'draco3d.encoder': await draco3d.createEncoderModule(),
  });

const document = await io.read('input.glb');

// ALWAYS run transforms in dependency order
await document.transform(
  dedup(),
  flatten(),
  join(),
  weld({ tolerance: 0.0001 }),
  simplify({ ratio: 0.5, error: 0.001 }),
  textureCompress({ targetFormat: 'ktx2' }),
  draco(),
  prune(),
  quantize(),
);

await io.write('output.glb', document);
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- gltf-transform API and Three.js loader methods
- [references/examples.md](references/examples.md) -- Complete optimization pipeline examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Common optimization mistakes

### Official Sources

- https://gltf-transform.dev/
- https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- https://threejs.org/docs/#examples/en/loaders/DRACOLoader
- https://threejs.org/docs/#examples/en/loaders/KTX2Loader
- https://threejs.org/docs/#api/en/objects/LOD
- https://github.com/zeux/meshoptimizer
