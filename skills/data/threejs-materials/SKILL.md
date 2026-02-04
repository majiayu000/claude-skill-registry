---
name: threejs-materials
description: Three.js materials - PBR, basic, phong, shader materials, material properties. Use when styling meshes, working with textures, creating custom shaders, or optimizing material performance.
---

# Three.js Materials

## Material Types

| Material | Use Case | Lighting |
|----------|----------|----------|
| MeshBasicMaterial | Unlit, flat colors | No |
| MeshLambertMaterial | Matte surfaces | Yes (diffuse) |
| MeshPhongMaterial | Shiny surfaces | Yes |
| MeshStandardMaterial | PBR, realistic | Yes (PBR) |
| MeshPhysicalMaterial | Advanced PBR | Yes (PBR+) |
| ShaderMaterial | Custom GLSL | Custom |

## MeshStandardMaterial (PBR)

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.5,
  metalness: 0.0,
  map: colorTexture,
  normalMap: normalTexture,
  roughnessMap: roughTexture,
  metalnessMap: metalTexture,
  aoMap: aoTexture,
  emissive: 0x000000,
  emissiveIntensity: 1,
  envMap: envTexture,
  envMapIntensity: 1,
});

// AO map requires second UV channel
geometry.setAttribute("uv2", geometry.attributes.uv);
```

## MeshPhysicalMaterial

```javascript
const glass = new THREE.MeshPhysicalMaterial({
  transmission: 1,
  thickness: 0.5,
  ior: 1.5,
  roughness: 0,
  metalness: 0,
});

const carPaint = new THREE.MeshPhysicalMaterial({
  clearcoat: 1,
  clearcoatRoughness: 0.1,
  metalness: 0.9,
  roughness: 0.5,
});
```

## ShaderMaterial

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    time: { value: 0 },
    color: { value: new THREE.Color(0xff0000) },
  },
  vertexShader: `
    void main() {
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform vec3 color;
    void main() {
      gl_FragColor = vec4(color, 1.0);
    }
  `,
});

// Update uniform
material.uniforms.time.value = clock.getElapsedTime();
```

## Common Properties

```javascript
material.transparent = true;
material.opacity = 0.5;
material.side = THREE.DoubleSide;
material.wireframe = true;
material.depthTest = true;
material.depthWrite = true;
```

## Environment Maps

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

new RGBELoader().load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
});
```
