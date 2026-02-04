---
name: threejs-loaders
description: Three.js asset loading - GLTF, textures, images, models, async patterns. Use when loading 3D models, textures, HDR environments, or managing loading progress.
---

# Three.js Loaders

## LoadingManager

```javascript
const manager = new THREE.LoadingManager();

manager.onStart = (url, loaded, total) => console.log("Started");
manager.onLoad = () => console.log("All loaded!");
manager.onProgress = (url, loaded, total) => {
  console.log(`${(loaded / total * 100).toFixed(1)}%`);
};
manager.onError = (url) => console.error(`Error: ${url}`);

const textureLoader = new THREE.TextureLoader(manager);
const gltfLoader = new GLTFLoader(manager);
```

## GLTF/GLB Loading

```javascript
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

const loader = new GLTFLoader();
loader.load("model.glb", (gltf) => {
  const model = gltf.scene;
  scene.add(model);

  // Enable shadows
  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  // Animations
  const mixer = new THREE.AnimationMixer(model);
  gltf.animations.forEach(clip => mixer.clipAction(clip).play());
});
```

## GLTF with Draco Compression

```javascript
import { DRACOLoader } from "three/examples/jsm/loaders/DRACOLoader.js";

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath("https://www.gstatic.com/draco/versioned/decoders/1.5.6/");

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);
```

## HDR Loading

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

new RGBELoader().load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
});
```

## Promise-Based Loading

```javascript
function loadModel(url) {
  return new Promise((resolve, reject) => {
    new GLTFLoader().load(url, resolve, undefined, reject);
  });
}

async function init() {
  const [model, env] = await Promise.all([
    loadModel("model.glb"),
    loadRGBE("environment.hdr")
  ]);
  scene.add(model.scene);
  scene.environment = env;
}
```

## Other Formats

```javascript
// OBJ
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";

// FBX
import { FBXLoader } from "three/examples/jsm/loaders/FBXLoader.js";

// STL
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
```
