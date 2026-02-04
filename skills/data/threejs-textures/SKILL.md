---
name: threejs-textures
description: Three.js textures - loading, configuration, UV mapping, environment maps. Use when loading images, configuring texture properties, or working with HDR environments.
---

# Three.js Textures

## Loading Textures

```javascript
const loader = new THREE.TextureLoader();
const texture = loader.load("texture.jpg", (tex) => {
  tex.colorSpace = THREE.SRGBColorSpace; // For color maps
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 2);
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
});
```

## Texture Configuration

```javascript
// Wrapping
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;

// Filtering
texture.minFilter = THREE.LinearMipmapLinearFilter;
texture.magFilter = THREE.LinearFilter;

// Transform
texture.repeat.set(4, 4);
texture.offset.set(0.5, 0.5);
texture.rotation = Math.PI / 4;
texture.center.set(0.5, 0.5);
```

## HDR Environment

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

new RGBELoader().load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
  scene.backgroundBlurriness = 0.5;
});
```

## Cube Textures

```javascript
const loader = new THREE.CubeTextureLoader();
const cubeTexture = loader.load([
  "px.jpg", "nx.jpg",
  "py.jpg", "ny.jpg",
  "pz.jpg", "nz.jpg"
]);
scene.background = cubeTexture;
```

## PBR Texture Set

```javascript
const material = new THREE.MeshStandardMaterial({
  map: colorTexture,           // sRGB
  normalMap: normalTexture,    // Linear
  roughnessMap: roughTexture,  // Linear
  metalnessMap: metalTexture,  // Linear
  aoMap: aoTexture,            // Linear, uses uv2
});

geometry.setAttribute("uv2", geometry.attributes.uv);
```

## Video Texture

```javascript
const video = document.createElement("video");
video.src = "video.mp4";
video.loop = true;
video.muted = true;
video.play();

const texture = new THREE.VideoTexture(video);
texture.colorSpace = THREE.SRGBColorSpace;
```

## Canvas Texture

```javascript
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
ctx.fillStyle = "red";
ctx.fillRect(0, 0, 256, 256);

const texture = new THREE.CanvasTexture(canvas);
texture.needsUpdate = true;
```
