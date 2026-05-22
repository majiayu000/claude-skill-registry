---
name: three-js
description: |
  This skill should be used when the user asks to "create a 3D scene", "add a mesh",
  "implement OrbitControls", "load a GLTF model", "add bloom post-processing",
  "write a custom shader", "create particle effects", "optimize Three.js performance",
  "use WebGPU", "add shadows", "animate a model", or mentions Three.js, threejs, WebGL,
  WebGPU, GLTF, raycaster, shader material, PBR material, or post-processing effects.

  IMPORTANT: This skill is for VANILLA Three.js (imperative JavaScript). For React Three
  Fiber (@react-three/fiber, R3F, drei), check the `r3f-best-practices` skill, although three-js skills helps when working with R3F since R3F is a React renderer for Three.js.

  Provides complete Three.js reference for 3D web graphics including scene setup,
  geometry, materials, textures, lighting, cameras, loaders, animation, controls,
  interaction, shaders, post-processing, performance optimization, TSL/node materials,
  WebGPU, physics, and VR/XR integration.
---

# Three.js Complete Reference (Vanilla)

> **React Three Fiber users**: This reference is for vanilla Three.js. For R3F/Drei patterns,
> use the **`r3f-best-practices`** skill. However, understanding Three.js concepts here
> helps when working with R3F since R3F is a React renderer for Three.js.

## Quick Start

```javascript
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);

camera.position.z = 5;

function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

## Reference Index

Load the appropriate reference file based on task:

### Core Foundation
| Reference | Use When |
|-----------|----------|
| `references/01-fundamentals.md` | Scene setup, renderer config, Object3D hierarchy, coordinate systems |
| `references/02-geometry.md` | Creating shapes, BufferGeometry, instancing, points, lines |
| `references/06-cameras.md` | Camera types, frustum, viewport, projection |
| `references/13-math.md` | Vector3, Matrix4, Quaternion, Euler, Color, MathUtils |

### Visual Appearance
| Reference | Use When |
|-----------|----------|
| `references/03-materials.md` | PBR materials, shader materials, all material types |
| `references/04-textures.md` | Texture loading, UV mapping, render targets, environment maps |
| `references/05-lighting.md` | Light types, shadows, IBL, light probes |
| `references/11-shaders.md` | Custom GLSL shaders, uniforms, varyings, shader patterns |

### Motion & Interaction
| Reference | Use When |
|-----------|----------|
| `references/08-animation.md` | Keyframe animation, skeletal, morph targets, procedural motion |
| `references/09-interaction.md` | Raycasting, selection, drag, coordinate conversion |
| `references/10-controls.md` | OrbitControls, FlyControls, PointerLockControls, etc. |

### Assets
| Reference | Use When |
|-----------|----------|
| `references/07-loaders.md` | GLTF, FBX, textures, HDR, Draco compression, async patterns |

### Effects
| Reference | Use When |
|-----------|----------|
| `references/12-postprocessing.md` | Bloom, DOF, SSAO, custom effects, EffectComposer |

### Advanced
| Reference | Use When |
|-----------|----------|
| `references/14-performance.md` | Optimization, profiling, LOD, culling, batching |
| `references/15-node-materials.md` | TSL (Three Shading Language), node-based materials |
| `references/16-physics-vr.md` | Physics engines, WebXR, VR/AR integration |
| `references/17-webgpu.md` | WebGPU renderer, compute shaders, WGSL |
| `references/18-patterns.md` | Architecture patterns, asset management, cleanup, state |

## Common Patterns Quick Reference

### Resize Handler
```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

### Cleanup/Dispose
```javascript
function dispose(obj) {
  obj.traverse(child => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(m => m.dispose());
      } else {
        child.material.dispose();
      }
    }
  });
}
```

### Animation Loop with Clock
```javascript
const clock = new THREE.Clock();

function animate() {
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();

  // Use delta for frame-rate independent animation
  mixer?.update(delta);

  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

## Import Patterns

```javascript
// Core
import * as THREE from 'three';

// Addons (controls, loaders, effects)
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';

// Compression support
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
```

## Version Notes

This reference targets Three.js r150+ with notes for:
- WebGPU support (r150+)
- Node materials / TSL
- Modern ES module imports

For version-specific APIs, check the Three.js migration guide.
