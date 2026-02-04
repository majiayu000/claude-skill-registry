---
name: threejs-lighting
description: Three.js lighting - light types, shadows, environment lighting. Use when adding lights, configuring shadows, setting up IBL, or optimizing lighting performance.
---

# Three.js Lighting

## Light Types

| Light | Description | Shadows |
|-------|-------------|---------|
| AmbientLight | Uniform everywhere | No |
| HemisphereLight | Sky/ground gradient | No |
| DirectionalLight | Parallel rays (sun) | Yes |
| PointLight | Omnidirectional (bulb) | Yes |
| SpotLight | Cone-shaped | Yes |
| RectAreaLight | Area light (window) | No |

## Basic Setup

```javascript
// Ambient
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);

// Directional (sun)
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 5);
scene.add(dirLight);

// Hemisphere
const hemi = new THREE.HemisphereLight(0x87ceeb, 0x8b4513, 0.6);
scene.add(hemi);
```

## Shadow Setup

```javascript
// 1. Enable on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// 2. Enable on light
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 50;
dirLight.shadow.camera.left = -10;
dirLight.shadow.camera.right = 10;
dirLight.shadow.camera.top = 10;
dirLight.shadow.camera.bottom = -10;
dirLight.shadow.bias = -0.0001;

// 3. Enable on objects
mesh.castShadow = true;
mesh.receiveShadow = true;
```

## Environment Lighting (IBL)

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

const pmremGenerator = new THREE.PMREMGenerator(renderer);

new RGBELoader().load("environment.hdr", (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;
  scene.environment = envMap;
  scene.background = envMap;
  texture.dispose();
  pmremGenerator.dispose();
});
```

## Three-Point Lighting

```javascript
// Key light (main)
const keyLight = new THREE.DirectionalLight(0xffffff, 1);
keyLight.position.set(5, 5, 5);

// Fill light (softer, opposite)
const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(-5, 3, 5);

// Back light (rim)
const backLight = new THREE.DirectionalLight(0xffffff, 0.3);
backLight.position.set(0, 5, -5);

// Ambient fill
const ambient = new THREE.AmbientLight(0x404040, 0.3);
```
