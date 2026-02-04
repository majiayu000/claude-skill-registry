---
name: threejs-postprocessing
description: Three.js post-processing - EffectComposer, bloom, depth of field, custom passes. Use when adding visual effects, screen-space effects, or enhancing rendered output.
---

# Three.js Post-Processing

## Setup

```javascript
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
));

// Animation loop
function animate() {
  composer.render(); // Instead of renderer.render()
}

// Resize handling
function onResize() {
  composer.setSize(width, height);
}
```

## Common Effects

### Bloom
```javascript
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";

const bloomPass = new UnrealBloomPass(resolution, strength, radius, threshold);
composer.addPass(bloomPass);
```

### FXAA Anti-Aliasing
```javascript
import { ShaderPass } from "three/examples/jsm/postprocessing/ShaderPass.js";
import { FXAAShader } from "three/examples/jsm/shaders/FXAAShader.js";

const fxaaPass = new ShaderPass(FXAAShader);
fxaaPass.uniforms["resolution"].value.set(1 / width, 1 / height);
composer.addPass(fxaaPass);
```

### Film Grain
```javascript
import { FilmPass } from "three/examples/jsm/postprocessing/FilmPass.js";

const filmPass = new FilmPass(0.35, 0.025, 648, false);
composer.addPass(filmPass);
```

### Vignette
```javascript
import { ShaderPass } from "three/examples/jsm/postprocessing/ShaderPass.js";
import { VignetteShader } from "three/examples/jsm/shaders/VignetteShader.js";

const vignettePass = new ShaderPass(VignetteShader);
vignettePass.uniforms["offset"].value = 1.0;
vignettePass.uniforms["darkness"].value = 1.5;
composer.addPass(vignettePass);
```

## Custom Shader Pass

```javascript
import { ShaderPass } from "three/examples/jsm/postprocessing/ShaderPass.js";

const customShader = {
  uniforms: {
    tDiffuse: { value: null },
    time: { value: 0 },
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float time;
    varying vec2 vUv;

    void main() {
      vec4 color = texture2D(tDiffuse, vUv);
      // Apply effect here
      gl_FragColor = color;
    }
  `,
};

const customPass = new ShaderPass(customShader);
composer.addPass(customPass);

// Update
customPass.uniforms.time.value = clock.getElapsedTime();
```

## Selective Bloom (Layers)

```javascript
// Setup bloom layer
const BLOOM_LAYER = 1;
const bloomLayer = new THREE.Layers();
bloomLayer.set(BLOOM_LAYER);

// Add objects to bloom layer
glowingMesh.layers.enable(BLOOM_LAYER);

// Render bloom scene separately
// (See three.js selective bloom example for full implementation)
```

## Performance Tips
1. Disable unused passes
2. Reduce resolution for blur effects
3. Prefer FXAA over MSAA
4. Profile GPU usage
