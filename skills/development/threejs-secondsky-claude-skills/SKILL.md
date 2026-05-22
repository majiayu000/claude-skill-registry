---
name: threejs
description: Three.js 3D graphics library - scene setup, geometry, materials, lighting, textures, animation, loaders, shaders, postprocessing, interaction. Use when building 3D web experiences, creating WebGL visualizations, working with GLTF models, implementing custom shaders, or adding interactive 3D elements to web applications.
metadata:
  version: "1.0.0"
license: MIT
---

# Three.js Skills

## Overview

Comprehensive knowledge base for building 3D web experiences with Three.js. This skill provides accurate API references, best practices, and working code examples across all major Three.js domains.

**Three.js version**: r160+ (January 2024)

## Quick Reference

### Core Topics

This skill covers 10 essential Three.js domains:

1. **Fundamentals** - Scene setup, cameras, renderer, Object3D hierarchy
2. **Geometry** - Built-in shapes, BufferGeometry, custom geometry, instancing
3. **Materials** - PBR materials, shader materials, material properties
4. **Lighting** - Light types, shadows, environment lighting
5. **Textures** - UV mapping, environment maps, render targets
6. **Animation** - Keyframe animation, skeletal animation, animation mixing
7. **Loaders** - GLTF/GLB loading, async patterns, caching
8. **Shaders** - GLSL basics, ShaderMaterial, custom effects
9. **Postprocessing** - EffectComposer, bloom, DOF, custom passes
10. **Interaction** - Raycasting, camera controls, mouse/touch input

## When to Load References

Load detailed reference files based on your current task:

- **Basic scene setup, cameras, renderer** → Load `references/threejs-fundamentals.md`
- **Creating shapes, custom geometry, instancing** → Load `references/threejs-geometry.md`
- **Material properties, PBR, shader materials** → Load `references/threejs-materials.md`
- **Adding lights, configuring shadows** → Load `references/threejs-lighting.md`
- **Texture loading, UV mapping, environment maps** → Load `references/threejs-textures.md`
- **Animating objects, GLTF animations, mixing** → Load `references/threejs-animation.md`
- **Loading GLTF/GLB models, Draco compression** → Load `references/threejs-loaders.md`
- **Writing GLSL shaders, custom visual effects** → Load `references/threejs-shaders.md`
- **Adding bloom, depth of field, screen effects** → Load `references/threejs-postprocessing.md`
- **Raycasting, mouse picking, camera controls** → Load `references/threejs-interaction.md`

## Quick Start Examples

### 1. Fundamentals: Basic Scene

```javascript
import * as THREE from 'three';

// Scene, camera, renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

// Create cube
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Add light
scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 5, 5);
scene.add(dirLight);

camera.position.z = 5;

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();

// Responsive
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

### 2. Geometry: Creating Shapes

```javascript
// Built-in geometries
const box = new THREE.BoxGeometry(1, 1, 1);
const sphere = new THREE.SphereGeometry(0.5, 32, 32);
const plane = new THREE.PlaneGeometry(10, 10);

// Custom BufferGeometry
const geometry = new THREE.BufferGeometry();
const vertices = new Float32Array([
  -1, -1,  0,  // vertex 0
   1, -1,  0,  // vertex 1
   1,  1,  0,  // vertex 2
  -1,  1,  0   // vertex 3
]);
geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));

// Indices for triangles
const indices = new Uint16Array([0, 1, 2, 0, 2, 3]);
geometry.setIndex(new THREE.BufferAttribute(indices, 1));

// Instancing for many copies
const count = 1000;
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
const dummy = new THREE.Object3D();

for (let i = 0; i < count; i++) {
  dummy.position.set(
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20
  );
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}
scene.add(instancedMesh);
```

### 3. Materials: PBR Materials

```javascript
// Standard PBR material
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  metalness: 0.5,
  roughness: 0.5,
  map: colorTexture,
  normalMap: normalTexture,
  roughnessMap: roughnessTexture,
  metalnessMap: metalnessTexture,
  envMap: environmentMap,
  envMapIntensity: 1
});

// Physical material (advanced PBR)
const glassMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  metalness: 0,
  roughness: 0,
  transmission: 1,     // Glass transparency
  thickness: 0.5,
  ior: 1.5,           // Index of refraction
  envMapIntensity: 1
});

// Shader material (custom)
const shaderMaterial = new THREE.ShaderMaterial({
  uniforms: {
    time: { value: 0 },
    color: { value: new THREE.Color(0xff0000) }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float time;
    uniform vec3 color;
    varying vec2 vUv;

    void main() {
      gl_FragColor = vec4(color * sin(vUv.x * 10.0 + time), 1.0);
    }
  `
});
```

### 4. Lighting: Basic Lighting

```javascript
// Ambient light (uniform everywhere)
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);

// Directional light (sun)
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 5);
dirLight.castShadow = true;

// Shadow configuration
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.camera.left = -10;
dirLight.shadow.camera.right = 10;
dirLight.shadow.camera.top = 10;
dirLight.shadow.camera.bottom = -10;
scene.add(dirLight);

// Point light (bulb)
const pointLight = new THREE.PointLight(0xffffff, 1, 100);
pointLight.position.set(0, 5, 0);
scene.add(pointLight);

// Enable shadows on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Enable on objects
mesh.castShadow = true;
mesh.receiveShadow = true;
```

### 5. Textures: Loading Textures

```javascript
const loader = new THREE.TextureLoader();

// Load color texture
const colorTexture = loader.load('texture.jpg');
colorTexture.colorSpace = THREE.SRGBColorSpace; // Important for color accuracy

// Configure texture
colorTexture.wrapS = THREE.RepeatWrapping;
colorTexture.wrapT = THREE.RepeatWrapping;
colorTexture.repeat.set(4, 4);

// HDR environment map
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

const rgbeLoader = new RGBELoader();
rgbeLoader.load('environment.hdr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
});

// Cube texture (skybox)
const cubeLoader = new THREE.CubeTextureLoader();
const cubeTexture = cubeLoader.load([
  'px.jpg', 'nx.jpg',  // +X, -X
  'py.jpg', 'ny.jpg',  // +Y, -Y
  'pz.jpg', 'nz.jpg'   // +Z, -Z
]);
scene.background = cubeTexture;
```

### 6. Animation: Simple Animation

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  const model = gltf.scene;
  scene.add(model);

  // Create animation mixer
  const mixer = new THREE.AnimationMixer(model);

  // Play all animations
  gltf.animations.forEach((clip) => {
    const action = mixer.clipAction(clip);
    action.play();
  });

  // Update in animation loop
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    mixer.update(delta);
    renderer.render(scene, camera);
  }
  animate();
});

// Procedural animation
function animate() {
  const time = clock.getElapsedTime();
  mesh.rotation.y = time;
  mesh.position.y = Math.sin(time) * 0.5;
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

### 7. Loaders: Loading GLTF Models

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

// Setup Draco compression support
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

// Load model
gltfLoader.load('model.glb', (gltf) => {
  const model = gltf.scene;

  // Enable shadows
  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  // Center and scale
  const box = new THREE.Box3().setFromObject(model);
  const center = box.getCenter(new THREE.Vector3());
  model.position.sub(center);

  scene.add(model);
});

// Async/Promise pattern
async function loadModel(url) {
  return new Promise((resolve, reject) => {
    gltfLoader.load(url, resolve, undefined, reject);
  });
}

const gltf = await loadModel('model.glb');
scene.add(gltf.scene);
```

### 8. Shaders: Custom Shader Material

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    time: { value: 0 },
    amplitude: { value: 0.5 }
  },
  vertexShader: `
    uniform float time;
    uniform float amplitude;
    varying vec2 vUv;

    void main() {
      vUv = uv;
      vec3 pos = position;

      // Wave displacement
      pos.z += sin(pos.x * 5.0 + time) * amplitude;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    uniform float time;
    varying vec2 vUv;

    void main() {
      vec3 color = vec3(vUv, 0.5 + 0.5 * sin(time));
      gl_FragColor = vec4(color, 1.0);
    }
  `
});

// Update in animation loop
function animate() {
  material.uniforms.time.value = clock.getElapsedTime();
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

### 9. Postprocessing: Adding Bloom

```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

// Create composer
const composer = new EffectComposer(renderer);

// Render scene pass
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// Bloom pass
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
);
composer.addPass(bloomPass);

// Use composer instead of renderer
function animate() {
  requestAnimationFrame(animate);
  composer.render(); // NOT renderer.render()
}

// Handle resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
});
```

### 10. Interaction: Raycasting

```javascript
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Camera controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Raycasting setup
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  // Convert mouse to normalized coordinates
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  // Raycast from camera
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);

  if (intersects.length > 0) {
    const object = intersects[0].object;
    console.log('Clicked:', object);
    console.log('Point:', intersects[0].point);

    // Highlight selected object
    object.material.emissive.set(0x444444);
  }
}

window.addEventListener('click', onMouseClick);

// Update controls in animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update(); // Required if enableDamping is true
  renderer.render(scene, camera);
}
```

## Common Patterns

### Proper Disposal

```javascript
// Dispose geometries, materials, textures
geometry.dispose();
material.dispose();
texture.dispose();

// Remove from scene
scene.remove(mesh);

// Dispose renderer
renderer.dispose();
```

### Responsive Rendering

```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});
```

### Performance Optimization

- Use instancing for repeated objects (`InstancedMesh`)
- Enable frustum culling (enabled by default)
- Dispose of unused resources
- Use proper LOD (Level of Detail) for complex scenes
- Minimize draw calls by merging geometries
- Limit active lights (each light adds shader complexity)
- Use texture atlases to reduce texture switches

## Version Information

**Three.js version**: r160+ (January 2024)
**Import format**: ES6 modules (`three`, `three/addons/*`)
**Verified**: 2024-01

## See Also

- **Official Documentation**: https://threejs.org/docs/
- **Examples**: https://threejs.org/examples/
- **Editor**: https://threejs.org/editor/
- **Source**: Based on [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills)
