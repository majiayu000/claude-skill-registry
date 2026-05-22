---
name: threejs-syntax-loaders
description: >
  Use when loading 3D models (GLTF, FBX, OBJ), textures, or HDR
  environment maps in Three.js. Prevents the common mistake of not
  setting up DRACOLoader, wrong WASM path, or missing error handling.
  Covers GLTFLoader, DRACOLoader, KTX2Loader, TextureLoader, RGBELoader,
  FBXLoader, OBJLoader, LoadingManager.
  Keywords: GLTFLoader, GLTF, GLB, load model, DRACOLoader, texture,
  FBXLoader, OBJLoader, RGBELoader, HDR, LoadingManager, progress.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-syntax-loaders

## Quick Reference

### Loader Architecture

All Three.js loaders extend the `Loader` base class and share two loading patterns:

```javascript
// Callback style
loader.load(url, onLoad, onProgress, onError);

// Promise style (preferred)
const result = await loader.loadAsync(url, onProgress);
```

### Import Paths

| Loader | Import |
|--------|--------|
| `TextureLoader` | `import { TextureLoader } from 'three';` |
| `CubeTextureLoader` | `import { CubeTextureLoader } from 'three';` |
| `GLTFLoader` | `import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';` |
| `DRACOLoader` | `import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';` |
| `KTX2Loader` | `import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';` |
| `FBXLoader` | `import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';` |
| `OBJLoader` | `import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';` |
| `MTLLoader` | `import { MTLLoader } from 'three/addons/loaders/MTLLoader.js';` |
| `RGBELoader` | `import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';` |
| `MeshoptDecoder` | `import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';` |

### Format Recommendation

**ALWAYS prefer glTF/GLB** over other 3D formats. glTF is the recommended format for Three.js. It supports PBR materials, animations, cameras, lights, and scene hierarchy in a single file. Use `.glb` (binary glTF) for single-file distribution.

### Critical Warnings

**NEVER** call `loader.load()` inside `requestAnimationFrame` or any render loop. Load assets once at initialization and cache the result.

**NEVER** forget to set the DRACOLoader decoder path before loading Draco-compressed models. The path MUST point to a directory containing `draco_decoder.wasm`.

**NEVER** skip error handling on `loadAsync` calls. ALWAYS wrap in try/catch. Failed loads without error handlers crash silently.

**NEVER** forget to dispose loaded models when removing them. GLTF models contain meshes, materials, and textures that ALL require disposal.

**ALWAYS** set `texture.colorSpace = THREE.SRGBColorSpace` on diffuse/color textures (map, emissiveMap). NEVER set SRGBColorSpace on data textures (normalMap, roughnessMap, metalnessMap, aoMap).

**ALWAYS** call `dracoLoader.dispose()` after all Draco-compressed models are loaded to free the WASM decoder memory.

---

## Loader Base Class

Every loader inherits these methods from `Loader`:

| Method | Signature | Purpose |
|--------|-----------|---------|
| `load` | `(url, onLoad, onProgress, onError)` | Callback-based loading |
| `loadAsync` | `(url, onProgress) => Promise` | Promise-based loading |
| `setPath` | `(path: string)` | Set base URL prefix for all loads |
| `setResourcePath` | `(path: string)` | Set resource resolution path |
| `setCrossOrigin` | `(value: string)` | Set CORS mode |
| `setWithCredentials` | `(value: boolean)` | Enable credentials for cross-origin |
| `setRequestHeader` | `(header: object)` | Set custom HTTP headers |

---

## LoadingManager

Coordinates multiple loaders and tracks overall progress.

```javascript
import * as THREE from 'three';

const manager = new THREE.LoadingManager(
  () => { console.log('All assets loaded'); },
  (url, loaded, total) => { console.log(`Progress: ${loaded}/${total}`); },
  (url) => { console.error(`Failed to load: ${url}`); }
);

// Pass manager to any loader
const textureLoader = new THREE.TextureLoader(manager);
const gltfLoader = new GLTFLoader(manager);
```

### Manager Callbacks

| Callback | Signature | When |
|----------|-----------|------|
| `onStart` | `(url, itemsLoaded, itemsTotal)` | First item begins loading |
| `onLoad` | `()` | All items finished |
| `onProgress` | `(url, itemsLoaded, itemsTotal)` | Each item completes |
| `onError` | `(url)` | An item fails |

### Manager Methods

| Method | Purpose |
|--------|---------|
| `itemStart(url)` | Manually register a loading item |
| `itemEnd(url)` | Manually mark item as loaded |
| `itemError(url)` | Manually mark item as failed |
| `resolveURL(url)` | Resolve URL through modifiers |
| `setURLModifier(callback)` | Custom URL rewriting (blob URLs, service workers) |

---

## GLTFLoader

The primary loader for 3D models. glTF 2.0 supports meshes, PBR materials, animations, cameras, lights, and scene hierarchy.

### Setup with Draco Compression

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);
```

### Setup with KTX2 Textures

```javascript
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('/basis/');
ktx2Loader.detectSupport(renderer); // MUST pass renderer instance

gltfLoader.setKTX2Loader(ktx2Loader);
```

### Setup with Meshopt Decoder

```javascript
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';

await MeshoptDecoder.ready;
gltfLoader.setMeshoptDecoder(MeshoptDecoder);
```

### Loading a Model

```javascript
try {
  const gltf = await gltfLoader.loadAsync('model.glb');
  scene.add(gltf.scene);
} catch (error) {
  console.error('Failed to load model:', error);
}
```

### GLTF Result Object

```javascript
{
  scene: THREE.Group,                    // Root scene node -- add this to your scene
  scenes: THREE.Group[],                 // All scenes in the file
  cameras: THREE.Camera[],              // Embedded cameras
  animations: THREE.AnimationClip[],    // Animation data for AnimationMixer
  asset: { generator: string, version: string },  // File metadata
  parser: GLTFParser,                    // Internal parser (advanced use)
  userData: {}                           // Custom glTF extensions
}
```

### GLTFLoader Methods

| Method | Signature | Purpose |
|--------|-----------|---------|
| `load` | `(url, onLoad, onProgress, onError)` | Load with callbacks |
| `loadAsync` | `(url, onProgress) => Promise<GLTF>` | Load with Promise |
| `parse` | `(data, path, onLoad, onError)` | Parse ArrayBuffer or JSON directly |
| `setDRACOLoader` | `(dracoLoader: DRACOLoader)` | Enable Draco decompression |
| `setKTX2Loader` | `(ktx2Loader: KTX2Loader)` | Enable KTX2 texture decompression |
| `setMeshoptDecoder` | `(decoder)` | Enable meshopt decompression |
| `register` | `(plugin)` | Register a glTF extension plugin |
| `unregister` | `(plugin)` | Unregister a glTF extension plugin |

---

## DRACOLoader

Decodes Draco-compressed geometry. Reduces mesh file size by 80-90%.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `setDecoderPath` | `(path: string)` | Path to directory containing WASM decoders |
| `setDecoderConfig` | `(config: object)` | `{ type: 'js' \| 'wasm' }` -- WASM is default and faster |
| `preload` | `()` | Pre-fetch decoder WASM before first use |
| `dispose` | `()` | Free WASM decoder memory |

**ALWAYS** call `dracoLoader.dispose()` after loading all Draco-compressed models.

---

## TextureLoader

Loads 2D textures (PNG, JPG, WebP) into `THREE.Texture`.

```javascript
const loader = new THREE.TextureLoader();
const texture = await loader.loadAsync('diffuse.jpg');
texture.colorSpace = THREE.SRGBColorSpace; // ALWAYS for color textures
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
material.map = texture;
```

---

## CubeTextureLoader

Loads six images as a cube map for skyboxes or environment reflections.

```javascript
const cubeLoader = new THREE.CubeTextureLoader();
cubeLoader.setPath('/textures/cube/');
const cubeTexture = cubeLoader.load([
  'px.jpg', 'nx.jpg',  // positive-x, negative-x
  'py.jpg', 'ny.jpg',  // positive-y, negative-y
  'pz.jpg', 'nz.jpg'   // positive-z, negative-z
]);
scene.background = cubeTexture;
scene.environment = cubeTexture;
```

---

## RGBELoader

Loads HDR environment maps in Radiance `.hdr` format.

```javascript
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

const rgbeLoader = new RGBELoader();
rgbeLoader.load('environment.hdr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture; // PBR environment lighting
  scene.background = texture;  // Optional: visible HDR background
});
```

The RGBELoader sets color space automatically. NEVER manually override the color space on HDR textures.

---

## FBXLoader

Loads Autodesk FBX models. Supports meshes, materials, and skeletal animations.

```javascript
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';

const fbxLoader = new FBXLoader();
const model = await fbxLoader.loadAsync('character.fbx');
scene.add(model);
```

---

## OBJLoader + MTLLoader

Loads Wavefront OBJ geometry with optional MTL material files.

```javascript
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { MTLLoader } from 'three/addons/loaders/MTLLoader.js';

const mtlLoader = new MTLLoader();
const materials = await mtlLoader.loadAsync('model.mtl');
materials.preload();

const objLoader = new OBJLoader();
objLoader.setMaterials(materials);
const model = await objLoader.loadAsync('model.obj');
scene.add(model);
```

**ALWAYS** load the MTL file first, then pass the materials to OBJLoader before loading the OBJ file.

---

## Disposing Loaded Models

**ALWAYS** traverse and dispose ALL resources when removing a loaded model:

```javascript
function disposeModel(model) {
  model.traverse((child) => {
    if (child.isMesh) {
      child.geometry.dispose();
      if (Array.isArray(child.material)) {
        child.material.forEach((mat) => {
          disposeMaterial(mat);
        });
      } else {
        disposeMaterial(child.material);
      }
    }
  });
  model.removeFromParent();
}

function disposeMaterial(material) {
  for (const key of Object.keys(material)) {
    const value = material[key];
    if (value && typeof value === 'object' && 'dispose' in value) {
      value.dispose(); // Disposes textures
    }
  }
  material.dispose();
}
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for all loaders
- [references/examples.md](references/examples.md) -- Working code examples for common loading scenarios
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do when loading assets

### Official Sources

- https://threejs.org/docs/#api/en/loaders/Loader
- https://threejs.org/docs/#api/en/loaders/LoadingManager
- https://threejs.org/docs/#api/en/loaders/TextureLoader
- https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- https://threejs.org/docs/#examples/en/loaders/DRACOLoader
- https://threejs.org/docs/#examples/en/loaders/KTX2Loader
- https://threejs.org/docs/#examples/en/loaders/FBXLoader
- https://threejs.org/docs/#examples/en/loaders/OBJLoader
- https://threejs.org/docs/#examples/en/loaders/RGBELoader
