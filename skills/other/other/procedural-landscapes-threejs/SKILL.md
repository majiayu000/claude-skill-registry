---
name: procedural-landscapes
description: >
  Generate procedural 3D landscapes and terrain in Three.js using WebGPU compute
  shaders with automatic WebGL2 fallback. Covers heightmap generation via FBM noise,
  ridged multifractal, and domain warping; chunked LOD terrain meshes; slope-based
  multi-material texturing; procedural water planes; atmospheric sky rendering;
  and instanced vegetation scattering. Use when building terrain generators, open-world
  environments, landscape visualizers, flight simulators, or any 3D scene requiring
  procedural ground surfaces. Triggers: "procedural terrain", "landscape generator",
  "heightmap", "terrain mesh", "procedural world", "open world", "terrain LOD",
  "terrain chunks", "noise terrain", "3D landscape".
---

# Procedural Landscapes

Generate performant, visually rich procedural terrain in Three.js with a WebGPU-first
architecture and automatic WebGL2 fallback.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Renderer Init                   │
│  WebGPU available? ──yes──► WebGPURenderer       │
│         │no                                      │
│         └──────────────► WebGLRenderer            │
├─────────────────────────────────────────────────┤
│              Terrain Pipeline                    │
│  1. Noise Generation (GPU compute or CPU)        │
│  2. Heightmap → Geometry (chunked grid)          │
│  3. Normal Computation (per-vertex)              │
│  4. Material Assignment (slope + height rules)   │
│  5. LOD Management (camera-distance based)       │
├─────────────────────────────────────────────────┤
│              Environment Layers                  │
│  Water plane ─ Sky dome ─ Fog ─ Vegetation       │
└─────────────────────────────────────────────────┘
```

## Renderer Setup with Dual Backend

Always attempt WebGPU first, fall back to WebGL2 gracefully.

```javascript
import * as THREE from 'three';
import WebGPU from 'three/addons/capabilities/WebGPU.js';
import WebGPURenderer from 'three/addons/renderers/webgpu/WebGPURenderer.js';

async function createRenderer(canvas) {
  let renderer;
  let gpuAvailable = false;

  if (WebGPU.isAvailable()) {
    renderer = new WebGPURenderer({ canvas, antialias: true });
    await renderer.init();
    gpuAvailable = true;
  } else {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
  }

  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  return { renderer, gpuAvailable };
}
```

**CDN usage (r170+)**:
```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
  }
}
</script>
```

## Noise Generation

### CPU Path (WebGL fallback)

Implement FBM noise on CPU when GPU compute is unavailable. Self-contained simplex noise
avoids external dependencies.

```javascript
function createNoise2D(seed = 0) {
  const perm = new Uint8Array(512);
  let s = seed;
  for (let i = 0; i < 256; i++) {
    s = (s * 16807 + 0) % 2147483647;
    perm[i] = perm[i + 256] = s & 255;
  }

  const G2 = (3 - Math.sqrt(3)) / 6;
  const grad = [[1,1],[-1,1],[1,-1],[-1,-1],[1,0],[-1,0],[0,1],[0,-1]];

  return function(x, y) {
    const s0 = (x + y) * 0.5 * (Math.sqrt(3) - 1);
    const i = Math.floor(x + s0), j = Math.floor(y + s0);
    const t0 = (i + j) * G2;
    const x0 = x - (i - t0), y0 = y - (j - t0);
    const i1 = x0 > y0 ? 1 : 0, j1 = x0 > y0 ? 0 : 1;
    const x1 = x0 - i1 + G2, y1 = y0 - j1 + G2;
    const x2 = x0 - 1 + 2 * G2, y2 = y0 - 1 + 2 * G2;
    const ii = i & 255, jj = j & 255;

    let n0 = 0, n1 = 0, n2 = 0;
    let t = 0.5 - x0*x0 - y0*y0;
    if (t > 0) { const g = grad[perm[ii + perm[jj]] & 7]; n0 = t*t*t*t * (g[0]*x0 + g[1]*y0); }
    t = 0.5 - x1*x1 - y1*y1;
    if (t > 0) { const g = grad[perm[ii+i1 + perm[jj+j1]] & 7]; n1 = t*t*t*t * (g[0]*x1 + g[1]*y1); }
    t = 0.5 - x2*x2 - y2*y2;
    if (t > 0) { const g = grad[perm[ii+1 + perm[jj+1]] & 7]; n2 = t*t*t*t * (g[0]*x2 + g[1]*y2); }
    return 70 * (n0 + n1 + n2);
  };
}
```

### FBM and Terrain Noise Functions

```javascript
function fbm(noise, x, y, octaves = 6, lacunarity = 2.0, gain = 0.5) {
  let sum = 0, amp = 1, freq = 1, maxAmp = 0;
  for (let i = 0; i < octaves; i++) {
    sum += noise(x * freq, y * freq) * amp;
    maxAmp += amp;
    amp *= gain;
    freq *= lacunarity;
  }
  return sum / maxAmp;
}

function ridgedMultifractal(noise, x, y, octaves = 6, lacunarity = 2.0, gain = 0.5) {
  let sum = 0, amp = 1, freq = 1, prev = 1;
  for (let i = 0; i < octaves; i++) {
    let n = 1 - Math.abs(noise(x * freq, y * freq));
    n = n * n * prev;
    sum += n * amp;
    prev = n;
    amp *= gain;
    freq *= lacunarity;
  }
  return sum;
}

function domainWarp(noise, x, y, strength = 0.3) {
  const qx = fbm(noise, x, y, 4);
  const qy = fbm(noise, x + 5.2, y + 1.3, 4);
  return fbm(noise, x + strength * qx, y + strength * qy, 6);
}
```

### GPU Compute Path (WebGPU)

For GPU-accelerated heightmap generation via WGSL compute shaders, see
`references/wgsl-shaders.md`. The compute path generates a heightmap texture
on the GPU, then samples it in vertex shaders or reads it back for collision.

## Terrain Geometry

### Single-Chunk Terrain

```javascript
function createTerrainGeometry(size, segments, heightFn, maxHeight = 50) {
  const geometry = new THREE.PlaneGeometry(size, size, segments, segments);
  geometry.rotateX(-Math.PI / 2);

  const position = geometry.attributes.position;
  const vertex = new THREE.Vector3();

  for (let i = 0; i < position.count; i++) {
    vertex.fromBufferAttribute(position, i);
    const nx = vertex.x / size + 0.5;
    const nz = vertex.z / size + 0.5;
    position.setY(i, heightFn(nx, nz) * maxHeight);
  }

  geometry.computeVertexNormals();
  position.needsUpdate = true;
  return geometry;
}
```

### Chunked Terrain with LOD

For larger worlds, divide terrain into chunks with distance-based LOD.

```javascript
class TerrainChunkManager {
  constructor(scene, chunkSize, viewDistance, heightFn, maxHeight) {
    this.scene = scene;
    this.chunkSize = chunkSize;
    this.viewDistance = viewDistance;
    this.heightFn = heightFn;
    this.maxHeight = maxHeight;
    this.chunks = new Map();
    this.lodLevels = [
      { distance: chunkSize * 2, segments: 64 },
      { distance: chunkSize * 5, segments: 32 },
      { distance: chunkSize * 10, segments: 16 },
      { distance: Infinity, segments: 8 },
    ];
  }

  update(cameraPosition) {
    const cx = Math.floor(cameraPosition.x / this.chunkSize);
    const cz = Math.floor(cameraPosition.z / this.chunkSize);
    const radius = Math.ceil(this.viewDistance / this.chunkSize);
    const activeKeys = new Set();

    for (let x = cx - radius; x <= cx + radius; x++) {
      for (let z = cz - radius; z <= cz + radius; z++) {
        const key = `${x},${z}`;
        activeKeys.add(key);
        const worldX = x * this.chunkSize;
        const worldZ = z * this.chunkSize;
        const dist = Math.hypot(cameraPosition.x - worldX, cameraPosition.z - worldZ);
        if (dist > this.viewDistance) continue;

        const lod = this.lodLevels.find(l => dist < l.distance);
        const existing = this.chunks.get(key);

        if (!existing || existing.lod !== lod.segments) {
          if (existing) { this.scene.remove(existing.mesh); existing.mesh.geometry.dispose(); }
          const mesh = this._createChunk(x, z, lod.segments);
          this.chunks.set(key, { mesh, lod: lod.segments });
          this.scene.add(mesh);
        }
      }
    }
    for (const [key, chunk] of this.chunks) {
      if (!activeKeys.has(key)) {
        this.scene.remove(chunk.mesh);
        chunk.mesh.geometry.dispose();
        this.chunks.delete(key);
      }
    }
  }

  _createChunk(cx, cz, segments) {
    const geo = createTerrainGeometry(
      this.chunkSize, segments,
      (nx, nz) => {
        const wx = (cx + nx) * this.chunkSize / 500;
        const wz = (cz + nz) * this.chunkSize / 500;
        return this.heightFn(wx, wz);
      },
      this.maxHeight
    );
    const mesh = new THREE.Mesh(geo, createTerrainMaterial());
    mesh.position.set(cx * this.chunkSize, 0, cz * this.chunkSize);
    mesh.receiveShadow = true;
    return mesh;
  }

  dispose() {
    for (const [, chunk] of this.chunks) {
      this.scene.remove(chunk.mesh);
      chunk.mesh.geometry.dispose();
    }
    this.chunks.clear();
  }
}
```

## Terrain Materials

### Slope + Height Shader (WebGL)

```javascript
function createTerrainMaterial() {
  return new THREE.ShaderMaterial({
    uniforms: {
      waterLevel:  { value: 0.05 },
      snowLevel:   { value: 0.75 },
      grassColor:  { value: new THREE.Color(0x4a7c3f) },
      rockColor:   { value: new THREE.Color(0x8b8680) },
      sandColor:   { value: new THREE.Color(0xc2b280) },
      snowColor:   { value: new THREE.Color(0xf0f0f5) },
      sunDir:      { value: new THREE.Vector3(0.5, 0.8, 0.3).normalize() },
      maxHeight:   { value: 50.0 },
    },
    vertexShader: `
      varying vec3 vWorldPos;
      varying vec3 vNormal;
      void main() {
        vWorldPos = (modelMatrix * vec4(position, 1.0)).xyz;
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform float waterLevel, snowLevel, maxHeight;
      uniform vec3 grassColor, rockColor, sandColor, snowColor, sunDir;
      varying vec3 vWorldPos;
      varying vec3 vNormal;
      void main() {
        float h = clamp(vWorldPos.y / maxHeight, 0.0, 1.0);
        float slope = 1.0 - dot(vNormal, vec3(0, 1, 0));
        vec3 color = grassColor;
        if (h < waterLevel + 0.05)
          color = mix(sandColor, grassColor, smoothstep(waterLevel, waterLevel + 0.05, h));
        if (h > snowLevel)
          color = mix(color, snowColor, smoothstep(snowLevel, snowLevel + 0.1, h));
        color = mix(color, rockColor, smoothstep(0.3, 0.6, slope));
        float light = max(dot(vNormal, sunDir), 0.0) * 0.7 + 0.3;
        gl_FragColor = vec4(color * light, 1.0);
      }
    `,
  });
}
```

### Node Material (WebGPU TSL)

When using WebGPURenderer, prefer Three.js Shading Language (TSL) node materials:

```javascript
import { color, normalWorld, positionWorld, mix, smoothstep,
         dot, vec3, float as tslFloat, MeshStandardNodeMaterial } from 'three/tsl';

function createTerrainNodeMaterial(maxHeight = 50) {
  const material = new MeshStandardNodeMaterial();
  const h = positionWorld.y.div(tslFloat(maxHeight)).clamp(0, 1);
  const slope = tslFloat(1).sub(dot(normalWorld, vec3(0, 1, 0)));

  const grass = color(0x4a7c3f);
  const rock  = color(0x8b8680);
  const sand  = color(0xc2b280);
  const snow  = color(0xf0f0f5);

  let c = mix(sand, grass, smoothstep(0.0, 0.1, h));
  c = mix(c, snow, smoothstep(0.75, 0.85, h));
  c = mix(c, rock, smoothstep(0.3, 0.6, slope));

  material.colorNode = c;
  material.roughnessNode = mix(tslFloat(0.9), tslFloat(0.5), slope);
  return material;
}
```

## Water

```javascript
function createWater(size, waterLevel = 2.5) {
  const geometry = new THREE.PlaneGeometry(size, size, 128, 128);
  geometry.rotateX(-Math.PI / 2);
  const material = new THREE.MeshPhysicalMaterial({
    color: 0x006994, transparent: true, opacity: 0.7,
    roughness: 0.1, metalness: 0.1, transmission: 0.3, thickness: 2.0,
  });
  const water = new THREE.Mesh(geometry, material);
  water.position.y = waterLevel;

  water.userData.animate = (time) => {
    const pos = geometry.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), z = pos.getZ(i);
      pos.setY(i, Math.sin(x * 0.05 + time) * 0.3 + Math.cos(z * 0.08 + time * 0.7) * 0.2);
    }
    pos.needsUpdate = true;
    geometry.computeVertexNormals();
  };
  return water;
}
```

## Sky & Atmosphere

```javascript
function createSky() {
  const geo = new THREE.SphereGeometry(500, 32, 16);
  const mat = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: {
      topColor:    { value: new THREE.Color(0x0077be) },
      bottomColor: { value: new THREE.Color(0xffeebb) },
      sunDir:      { value: new THREE.Vector3(0.3, 0.5, 0.4).normalize() },
    },
    vertexShader: `
      varying vec3 vDir;
      void main() {
        vDir = normalize(position);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 topColor, bottomColor, sunDir;
      varying vec3 vDir;
      void main() {
        float y = vDir.y * 0.5 + 0.5;
        vec3 sky = mix(bottomColor, topColor, pow(y, 0.6));
        float sun = smoothstep(0.97, 1.0, dot(vDir, sunDir));
        sky += vec3(1.0, 0.95, 0.8) * sun * 0.8;
        gl_FragColor = vec4(sky, 1.0);
      }
    `,
  });
  return new THREE.Mesh(geo, mat);
}
```

## Vegetation Scattering

Place instanced vegetation using height and slope constraints.

```javascript
function scatterVegetation(heightFn, terrainSize, maxHeight, count = 5000) {
  const trunkGeo = new THREE.CylinderGeometry(0.1, 0.15, 1.5, 6);
  const canopyGeo = new THREE.ConeGeometry(0.8, 2.0, 6);
  canopyGeo.translate(0, 2.0, 0);
  const merged = mergeBufferGeometries(trunkGeo, canopyGeo);
  const material = new THREE.MeshStandardMaterial({ color: 0x2d5a27, flatShading: true });
  const mesh = new THREE.InstancedMesh(merged, material, count);
  mesh.castShadow = true;

  const dummy = new THREE.Object3D();
  const noise = createNoise2D(42);
  let placed = 0;

  for (let i = 0; i < count * 3 && placed < count; i++) {
    const x = (Math.random() - 0.5) * terrainSize;
    const z = (Math.random() - 0.5) * terrainSize;
    const h = heightFn(x / terrainSize + 0.5, z / terrainSize + 0.5) * maxHeight;
    const nh = h / maxHeight;
    if (nh < 0.08 || nh > 0.65) continue;
    if (noise(x * 0.01, z * 0.01) < 0.0) continue;

    dummy.position.set(x, h, z);
    dummy.rotation.y = Math.random() * Math.PI * 2;
    dummy.scale.setScalar(0.5 + Math.random());
    dummy.updateMatrix();
    mesh.setMatrixAt(placed++, dummy.matrix);
  }

  mesh.count = placed;
  mesh.instanceMatrix.needsUpdate = true;
  return mesh;
}

function mergeBufferGeometries(a, b) {
  const na = a.toNonIndexed(), nb = b.toNonIndexed();
  const pA = na.attributes.position.array, pB = nb.attributes.position.array;
  const nA = na.attributes.normal.array, nB = nb.attributes.normal.array;
  const pos = new Float32Array(pA.length + pB.length);
  const nor = new Float32Array(nA.length + nB.length);
  pos.set(pA); pos.set(pB, pA.length);
  nor.set(nA); nor.set(nB, nA.length);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  return geo;
}
```

## Performance Guidelines

- **Geometry budget**: 64×64 for distant chunks, 256×256 for close. Never exceed 512×512.
- **Instanced rendering**: Always use `InstancedMesh` for repeated objects. One draw call for 10K instances beats 10K meshes by ~100×.
- **Dispose aggressively**: `.dispose()` geometry, materials, textures when removing chunks.
- **Shadow optimization**: One shadow-casting directional light. Use `CSM` addon for large terrains.
- **Vertex totals**: Mobile < 500K, Desktop < 2M across visible scene.
- **WebGPU compute**: 10–50× faster than CPU for 1024² heightmaps. Use for real-time sculpting.

## Noise Selection Guide

| Noise Type | Character | Best For |
|---|---|---|
| FBM | Smooth rolling hills | Meadows, plains |
| Ridged Multifractal | Sharp ridges/valleys | Mountains, canyons |
| Domain Warping | Organic twisted forms | Fantasy, alien terrain |
| Terraced FBM | Stepped plateaus | Mesas, rice paddies |

**Combine multiplicatively** for complex terrain:
```javascript
function complexTerrain(noise, x, y) {
  const base = fbm(noise, x * 0.5, y * 0.5, 4) * 0.5 + 0.5;
  const mountains = ridgedMultifractal(noise, x, y, 6) * 0.4;
  const detail = domainWarp(noise, x * 2, y * 2, 0.2) * 0.1;
  return Math.max(base * 0.5 + mountains * base + detail, 0);
}
```

## Common Pitfalls

1. **Normals not recomputed** after vertex modification → flat/unlit terrain. Always call `geometry.computeVertexNormals()`.
2. **Chunk seams** → sample identical world-space noise at shared edges.
3. **Z-fighting on water** → use `polygonOffset` or small Y offset.
4. **Memory leaks** → dispose geometries on chunk removal. Monitor with `renderer.info`.
5. **WebGPU silent failure** → always gate behind `WebGPU.isAvailable()`.

## References

- `references/wgsl-shaders.md` — Complete WGSL compute shaders for GPU heightmap generation, erosion simulation, and normal computation.
- `references/noise-algorithms.md` — Mathematical foundations and advanced noise variants (Voronoi, analytical derivatives, curl noise).
