---
name: procedural-clouds
description: >
  Generate beautiful procedural clouds in Three.js using WebGPU raymarching with WebGL2
  billboard/mesh fallbacks. Covers all 10 major cloud genera (cumulus, stratus, cirrus,
  cumulonimbus, stratocumulus, altocumulus, altostratus, nimbostratus, cirrostratus,
  cirrocumulus) with physically-inspired lighting including silver linings, god rays,
  sunset coloring, and Mie/Rayleigh scattering approximation. Provides volumetric
  raymarching, billboard impostor, and mesh-cluster rendering paths with animated drift,
  morphing, and dynamic formation/dissipation. Use when building skies, cloudscapes,
  weather systems, flight scenes, atmospheric backgrounds, or any scene requiring
  clouds. Triggers: "procedural clouds", "cloud rendering", "volumetric clouds",
  "skybox clouds", "cloudscape", "cumulus", "cirrus", "storm clouds", "cloud shader",
  "cloud billboard", "raymarched clouds", "cloud lighting", "god rays", "sky rendering".
---

# Procedural Clouds

Generate visually stunning procedural clouds in Three.js with artistic emphasis —
volumetric raymarching on WebGPU, billboard/mesh fallbacks on WebGL2.

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                  Cloud Pipeline                       │
│                                                      │
│  Rendering Paths (select by capability + budget):    │
│                                                      │
│  ┌─ VOLUMETRIC (WebGPU) ─────────────────────────┐   │
│  │  Fullscreen quad → raymarching fragment shader │   │
│  │  Noise: 3D worley/perlin compute textures     │   │
│  │  Best quality, most expensive                  │   │
│  └───────────────────────────────────────────────┘   │
│                                                      │
│  ┌─ MESH CLUSTER (WebGL2/WebGPU) ────────────────┐   │
│  │  Instanced soft-particle spheres              │   │
│  │  Per-instance density, color, fade            │   │
│  │  Good quality, moderate cost                   │   │
│  └───────────────────────────────────────────────┘   │
│                                                      │
│  ┌─ BILLBOARD (WebGL2, mobile) ──────────────────┐   │
│  │  Camera-facing quads with noise texture       │   │
│  │  Cheapest, suitable for backgrounds           │   │
│  └───────────────────────────────────────────────┘   │
│                                                      │
│  Shared Systems:                                     │
│  Lighting ─ Drift ─ Time-of-Day ─ Formation         │
└──────────────────────────────────────────────────────┘
```

## Cloud Classification Quick Reference

| Genus | Altitude | Shape | Key Visual |
|-------|----------|-------|------------|
| Cumulus | Low (2km) | Puffy mounds | Flat base, cauliflower tops |
| Stratus | Low (2km) | Flat sheet | Uniform grey blanket |
| Stratocumulus | Low (2km) | Lumpy rolls | Patchy blanket with gaps |
| Cumulonimbus | Low→High | Towering anvil | Massive vertical, dark base |
| Altocumulus | Mid (2-6km) | Rippled patches | "Mackerel sky" pattern |
| Altostratus | Mid (2-6km) | Thin veil | Sun visible as bright spot |
| Nimbostratus | Mid (2-6km) | Thick dark sheet | Continuous rain cloud |
| Cirrus | High (6-12km) | Wispy streaks | Ice crystal hooks and mares' tails |
| Cirrostratus | High (6-12km) | Thin milky haze | Halo around sun |
| Cirrocumulus | High (6-12km) | Tiny ripples | Delicate fish-scale pattern |

Full profiles with shader parameters in `references/cloud-types.md`.

## Renderer Setup

```javascript
import * as THREE from 'three';

async function createRenderer(canvas) {
  let renderer, gpuAvailable = false;
  try {
    const WebGPU = (await import('three/addons/capabilities/WebGPU.js')).default;
    if (WebGPU.isAvailable()) {
      const { default: WebGPURenderer } = await import(
        'three/addons/renderers/webgpu/WebGPURenderer.js'
      );
      renderer = new WebGPURenderer({ canvas, antialias: true });
      await renderer.init();
      gpuAvailable = true;
    }
  } catch (e) { /* fallback */ }
  if (!renderer) {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
  }
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  return { renderer, gpuAvailable };
}
```

## 3D Noise Foundation

All cloud rendering depends on layered 3D noise. These functions are shared across
all three rendering paths.

```javascript
// GPU-friendly 3D hash (no lookup tables)
// Used in shaders — JavaScript equivalent for CPU cloud mesh placement
function hash3(x, y, z) {
  let h = x * 127.1 + y * 311.7 + z * 74.7;
  return (Math.sin(h) * 43758.5453) % 1;
}

// 3D value noise
function noise3D(x, y, z) {
  const ix = Math.floor(x), iy = Math.floor(y), iz = Math.floor(z);
  const fx = x - ix, fy = y - iy, fz = z - iz;
  const ux = fx * fx * (3 - 2 * fx);
  const uy = fy * fy * (3 - 2 * fy);
  const uz = fz * fz * (3 - 2 * fz);

  const h = (a, b, c) => hash3(ix + a, iy + b, iz + c);
  return lerp(uz,
    lerp(uy, lerp(ux, h(0,0,0), h(1,0,0)), lerp(ux, h(0,1,0), h(1,1,0))),
    lerp(uy, lerp(ux, h(0,0,1), h(1,0,1)), lerp(ux, h(0,1,1), h(1,1,1)))
  );
}
function lerp(t, a, b) { return a + t * (b - a); }

// FBM for cloud density
function cloudFBM(x, y, z, octaves = 5, lac = 2.0, gain = 0.5) {
  let sum = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    sum += noise3D(x * freq, y * freq, z * freq) * amp;
    max += amp; amp *= gain; freq *= lac;
  }
  return sum / max;
}
```

## Path 1: Volumetric Raymarching (WebGPU)

The highest-quality path renders clouds by marching rays through a density field defined
by 3D noise. Implemented as a fullscreen post-process pass.

### Cloud Density Field

The density function defines cloud shape, coverage, and type:

```javascript
// GLSL-style pseudocode for the density function (full GLSL in references)
float cloudDensity(vec3 p, float time) {
  // Altitude shaping — confine to cloud layer
  float altFade = smoothstep(cloudBase, cloudBase + 200.0, p.y)
                * smoothstep(cloudTop, cloudTop - 200.0, p.y);

  // Large-scale shape (coverage map)
  float shape = fbm3D(p * 0.0003 + wind * time, 3);
  shape = remap(shape, coverageThreshold, 1.0, 0.0, 1.0); // coverage control

  // Detail erosion (carves edges)
  float detail = fbm3D(p * 0.003 + wind * time * 2.0, 5);
  float density = shape - detail * detailStrength;

  return max(density * altFade, 0.0);
}
```

### Raymarching Loop

```javascript
// Core raymarching pattern (see references/cloud-shaders.md for full GLSL)
vec4 raymarchClouds(vec3 ro, vec3 rd) {
  float t = intersectCloudLayer(ro, rd); // Ray-slab intersection
  vec4 result = vec4(0.0);

  for (int i = 0; i < MAX_STEPS; i++) {
    if (result.a > 0.99 || t > maxDist) break;

    vec3 p = ro + rd * t;
    float density = cloudDensity(p, time);

    if (density > 0.001) {
      // Light marching — secondary ray toward sun
      float lightEnergy = lightMarch(p);

      // Phase function (Henyey-Greenstein)
      float phase = henyeyGreenstein(dot(rd, sunDir), 0.3)
                  + henyeyGreenstein(dot(rd, sunDir), 0.8) * 0.5;

      // Color from scattering
      vec3 cloudColor = sunColor * lightEnergy * phase + ambientSky * 0.15;

      // Silver lining — bright edge when sun is behind cloud
      float rim = pow(1.0 - abs(dot(rd, sunDir)), 4.0);
      cloudColor += sunColor * rim * 0.3 * lightEnergy;

      // Beer-Lambert absorption
      float alpha = 1.0 - exp(-density * stepSize * absorptionCoeff);
      result.rgb += cloudColor * alpha * (1.0 - result.a);
      result.a += alpha * (1.0 - result.a);
    }

    t += stepSize;
  }
  return result;
}
```

### Fullscreen Cloud Pass Setup

```javascript
function createVolumetricCloudPass(camera, scene) {
  const cloudMaterial = new THREE.ShaderMaterial({
    uniforms: {
      tDepth:           { value: null },       // Scene depth texture
      cameraPos:        { value: new THREE.Vector3() },
      invProjection:    { value: new THREE.Matrix4() },
      invView:          { value: new THREE.Matrix4() },
      sunDir:           { value: new THREE.Vector3(0.3, 0.8, 0.5).normalize() },
      sunColor:         { value: new THREE.Color(0xfff8e7) },
      ambientSky:       { value: new THREE.Color(0x6699cc) },
      time:             { value: 0 },
      cloudBase:        { value: 1500 },       // meters
      cloudTop:         { value: 3500 },
      coverage:         { value: 0.45 },       // 0-1, controls cloud amount
      detailStrength:   { value: 0.35 },
      windDirection:    { value: new THREE.Vector2(1, 0.3).normalize() },
      windSpeed:        { value: 15 },
      absorptionCoeff:  { value: 0.04 },
    },
    vertexShader: FULLSCREEN_VERT,    // See references/cloud-shaders.md
    fragmentShader: VOLUMETRIC_FRAG,  // See references/cloud-shaders.md
    transparent: true,
    depthWrite: false,
  });

  const quad = new THREE.Mesh(
    new THREE.PlaneGeometry(2, 2),
    cloudMaterial
  );
  quad.frustumCulled = false;

  return { quad, material: cloudMaterial };
}
```

### Light Marching & Scattering

The inner light march samples density toward the sun to compute self-shadowing:

```glsl
float lightMarch(vec3 p) {
  float accumDensity = 0.0;
  float stepL = (cloudTop - cloudBase) / float(LIGHT_STEPS);
  vec3 lightStep = normalize(sunDir) * stepL;

  for (int i = 0; i < LIGHT_STEPS; i++) {
    p += lightStep;
    accumDensity += max(cloudDensity(p, time), 0.0) * stepL;
  }

  // Beer-powder approximation (brighter at thin edges)
  float beer = exp(-accumDensity * absorptionCoeff);
  float powder = 1.0 - exp(-accumDensity * absorptionCoeff * 2.0);
  return mix(beer, beer * powder, 0.5);
}
```

## Path 2: Mesh Cluster Clouds

For mid-range quality, build clouds from instanced soft-particle spheres. Each cloud
is a cluster of overlapping translucent spheres with noise-modulated opacity.

```javascript
class MeshCloudSystem {
  constructor(scene, options = {}) {
    this.scene = scene;
    this.cloudBase = options.cloudBase ?? 80;
    this.spread = options.spread ?? 500;
    this.cloudCount = options.cloudCount ?? 30;
    this.particlesPerCloud = options.particlesPerCloud ?? 25;
    this.clouds = [];
  }

  generate(seed = 0) {
    const sphereGeo = new THREE.SphereGeometry(1, 12, 8);
    const material = this._createMaterial();

    for (let c = 0; c < this.cloudCount; c++) {
      const cx = (seededRandom(seed + c * 3) - 0.5) * this.spread;
      const cz = (seededRandom(seed + c * 3 + 1) - 0.5) * this.spread;
      const cy = this.cloudBase + seededRandom(seed + c * 3 + 2) * 30;

      const mesh = new THREE.InstancedMesh(
        sphereGeo, material, this.particlesPerCloud
      );

      const dummy = new THREE.Object3D();
      const cloudType = seededRandom(seed + c * 7);

      for (let i = 0; i < this.particlesPerCloud; i++) {
        const profile = this._cloudProfile(cloudType, i, this.particlesPerCloud, seed + c * 100 + i);
        dummy.position.set(
          cx + profile.x,
          cy + profile.y,
          cz + profile.z
        );
        dummy.scale.set(profile.sx, profile.sy, profile.sz);
        dummy.updateMatrix();
        mesh.setMatrixAt(i, dummy.matrix);
      }

      mesh.instanceMatrix.needsUpdate = true;
      this.scene.add(mesh);
      this.clouds.push({ mesh, basePos: new THREE.Vector3(cx, cy, cz) });
    }
  }

  // Cloud shape profiles — different particle distributions per cloud type
  _cloudProfile(type, index, total, seed) {
    const r = seededRandom;
    if (type < 0.4) {
      // Cumulus: dome top, flat base
      const angle = r(seed) * Math.PI * 2;
      const radius = r(seed + 1) * 15;
      const y = Math.max(r(seed + 2) * 12 - 2, 0); // Flat base (no negative y)
      return {
        x: Math.cos(angle) * radius,
        y: y,
        z: Math.sin(angle) * radius,
        sx: 5 + r(seed + 3) * 8,
        sy: 3 + r(seed + 4) * 5 * (1 - index / total), // Taller at center
        sz: 5 + r(seed + 5) * 8,
      };
    } else if (type < 0.7) {
      // Stratus: wide, flat, layered
      return {
        x: (r(seed) - 0.5) * 40,
        y: (r(seed + 1) - 0.5) * 3,
        z: (r(seed + 2) - 0.5) * 40,
        sx: 8 + r(seed + 3) * 12,
        sy: 1.5 + r(seed + 4) * 2,
        sz: 8 + r(seed + 5) * 12,
      };
    } else {
      // Cirrus: wispy elongated streaks
      const t = index / total;
      return {
        x: t * 30 - 15 + (r(seed) - 0.5) * 5,
        y: (r(seed + 1) - 0.5) * 2,
        z: (r(seed + 2) - 0.5) * 4,
        sx: 3 + r(seed + 3) * 4,
        sy: 0.5 + r(seed + 4) * 1,
        sz: 1.5 + r(seed + 5) * 2,
      };
    }
  }

  _createMaterial() {
    return new THREE.ShaderMaterial({
      uniforms: {
        sunDir:     { value: new THREE.Vector3(0.3, 0.8, 0.5).normalize() },
        sunColor:   { value: new THREE.Color(0xfff8e7) },
        ambientColor: { value: new THREE.Color(0xb0c4de) },
        baseColor:  { value: new THREE.Color(0xffffff) },
        opacity:    { value: 0.6 },
        time:       { value: 0 },
      },
      vertexShader: MESH_CLOUD_VERT,    // See references/cloud-shaders.md
      fragmentShader: MESH_CLOUD_FRAG,  // See references/cloud-shaders.md
      transparent: true,
      depthWrite: false,
      side: THREE.DoubleSide,
    });
  }

  update(time, windDir, windSpeed) {
    for (const cloud of this.clouds) {
      cloud.mesh.position.x = cloud.basePos.x + Math.sin(time * 0.01 * windSpeed) * 5;
      cloud.mesh.position.z = cloud.basePos.z + time * windSpeed * 0.1;
      // Wrap clouds
      if (cloud.mesh.position.z > this.spread / 2) {
        cloud.mesh.position.z -= this.spread;
      }
    }
    if (this.clouds[0]) {
      this.clouds[0].mesh.material.uniforms.time.value = time;
    }
  }

  dispose() {
    for (const cloud of this.clouds) {
      this.scene.remove(cloud.mesh);
      cloud.mesh.geometry.dispose();
    }
    this.clouds = [];
  }
}

function seededRandom(seed) {
  const s = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return s - Math.floor(s);
}
```

## Path 3: Billboard Clouds (Mobile/Background)

Camera-facing quads with procedural noise textures. Cheapest option for distant skies.

```javascript
class BillboardCloudSystem {
  constructor(scene, camera, options = {}) {
    this.scene = scene;
    this.camera = camera;
    this.count = options.count ?? 20;
    this.spread = options.spread ?? 400;
    this.altitude = options.altitude ?? 100;
    this.clouds = [];
  }

  generate(seed = 0) {
    const texture = this._generateCloudTexture(256);

    for (let i = 0; i < this.count; i++) {
      const material = new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        opacity: 0.5 + seededRandom(seed + i * 5) * 0.3,
        depthWrite: false,
        color: new THREE.Color().setHSL(0, 0, 0.9 + seededRandom(seed + i * 7) * 0.1),
      });

      const sprite = new THREE.Sprite(material);
      const sx = 30 + seededRandom(seed + i * 11) * 50;
      sprite.scale.set(sx, sx * (0.3 + seededRandom(seed + i * 13) * 0.3), 1);
      sprite.position.set(
        (seededRandom(seed + i * 2) - 0.5) * this.spread,
        this.altitude + seededRandom(seed + i * 3) * 30,
        (seededRandom(seed + i * 4) - 0.5) * this.spread,
      );

      this.scene.add(sprite);
      this.clouds.push(sprite);
    }
  }

  _generateCloudTexture(size) {
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = size;
    const ctx = canvas.getContext('2d');

    // Radial gradient base
    const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
    grad.addColorStop(0, 'rgba(255,255,255,0.9)');
    grad.addColorStop(0.4, 'rgba(255,255,255,0.6)');
    grad.addColorStop(0.7, 'rgba(240,240,255,0.2)');
    grad.addColorStop(1, 'rgba(240,240,255,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, size, size);

    // Add noise bumps for cloudlike edges
    const imgData = ctx.getImageData(0, 0, size, size);
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const idx = (y * size + x) * 4;
        const nx = x / size * 6, ny = y / size * 6;
        const n = simpleFBM2D(nx, ny, 4) * 0.3;
        imgData.data[idx + 3] = Math.max(0, imgData.data[idx + 3] + n * 255);
      }
    }
    ctx.putImageData(imgData, 0, 0);

    const tex = new THREE.CanvasTexture(canvas);
    tex.needsUpdate = true;
    return tex;
  }

  update(time, windSpeed = 5) {
    for (const sprite of this.clouds) {
      sprite.position.x += windSpeed * 0.02;
      if (sprite.position.x > this.spread / 2) sprite.position.x -= this.spread;
    }
  }

  dispose() {
    for (const s of this.clouds) { this.scene.remove(s); s.material.dispose(); }
    this.clouds = [];
  }
}

function simpleFBM2D(x, y, octaves) {
  let sum = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    sum += (Math.sin(x * freq * 127.1 + y * freq * 311.7) * 0.5 + 0.5) * amp;
    max += amp; amp *= 0.5; freq *= 2;
  }
  return sum / max;
}
```

## Lighting Model

Cloud lighting is the single most important factor for beauty. All three paths share
the same lighting concepts.

### Henyey-Greenstein Phase Function

Controls how light scatters through cloud particles. Two-lobe version for realism:

```glsl
float henyeyGreenstein(float cosTheta, float g) {
  float g2 = g * g;
  return (1.0 - g2) / (4.0 * 3.14159 * pow(1.0 + g2 - 2.0 * g * cosTheta, 1.5));
}

// Two-lobe: forward scattering (silver linings) + back scattering (soft glow)
float cloudPhase(float cosTheta) {
  return henyeyGreenstein(cosTheta, 0.6) * 0.7   // forward lobe
       + henyeyGreenstein(cosTheta, -0.3) * 0.3;  // back lobe
}
```

### Silver Lining Effect

When the sun is behind a cloud, edges glow brilliantly:

```glsl
float silverLining(vec3 viewDir, vec3 sunDir, float density, float edgeDist) {
  float backlit = max(dot(-viewDir, sunDir), 0.0);
  float rim = pow(1.0 - edgeDist, 3.0);      // Stronger at edges
  return backlit * rim * exp(-density * 0.5); // Fades into thick cloud
}
```

### Time-of-Day Coloring

Shift cloud colors based on sun elevation for sunrise/sunset/golden hour:

```javascript
function cloudColorForTimeOfDay(sunElevation) {
  // sunElevation: -0.1 (below horizon) to 1.0 (noon)
  if (sunElevation < 0) {
    // Night: dark blue-grey
    return {
      sunColor: new THREE.Color(0x112244),
      ambientColor: new THREE.Color(0x0a0a1a),
      cloudTint: new THREE.Color(0x1a1a2e),
    };
  } else if (sunElevation < 0.1) {
    // Golden hour / sunset
    return {
      sunColor: new THREE.Color(0xff6622),
      ambientColor: new THREE.Color(0x553322),
      cloudTint: new THREE.Color(0xff8844),
    };
  } else if (sunElevation < 0.3) {
    // Morning / late afternoon
    return {
      sunColor: new THREE.Color(0xffcc88),
      ambientColor: new THREE.Color(0x667799),
      cloudTint: new THREE.Color(0xffeedd),
    };
  } else {
    // Midday
    return {
      sunColor: new THREE.Color(0xfff8e7),
      ambientColor: new THREE.Color(0xb0c4de),
      cloudTint: new THREE.Color(0xffffff),
    };
  }
}
```

### God Rays (Crepuscular Rays)

Post-process radial blur from sun position for volumetric light shafts:

```javascript
function createGodRayPass() {
  return new THREE.ShaderMaterial({
    uniforms: {
      tInput:      { value: null },
      sunScreenPos: { value: new THREE.Vector2(0.5, 0.7) },
      exposure:    { value: 0.3 },
      decay:       { value: 0.96 },
      density:     { value: 0.8 },
      weight:      { value: 0.4 },
      samples:     { value: 60 },
    },
    fragmentShader: GOD_RAY_FRAG, // See references/cloud-shaders.md
    vertexShader: FULLSCREEN_VERT,
  });
}
```

## Cloud Presets

Quick-start configurations. Full details in `references/cloud-types.md`.

```javascript
const CLOUD_PRESETS = {
  clearDay: {
    coverage: 0.15, cloudBase: 2000, cloudTop: 3000,
    type: 'cumulus', detailStrength: 0.4, absorptionCoeff: 0.04,
    description: 'Scattered fair-weather cumulus, mostly blue sky',
  },
  partlyCloudy: {
    coverage: 0.45, cloudBase: 1500, cloudTop: 3500,
    type: 'cumulus', detailStrength: 0.3, absorptionCoeff: 0.04,
    description: 'Classic partly cloudy — picturesque cumulus fields',
  },
  overcast: {
    coverage: 0.85, cloudBase: 800, cloudTop: 2000,
    type: 'stratus', detailStrength: 0.2, absorptionCoeff: 0.06,
    description: 'Flat grey blanket, diffused light',
  },
  dramatic: {
    coverage: 0.6, cloudBase: 1000, cloudTop: 6000,
    type: 'cumulonimbus', detailStrength: 0.5, absorptionCoeff: 0.08,
    description: 'Towering storm clouds with dark bases and bright anvils',
  },
  sunset: {
    coverage: 0.4, cloudBase: 1500, cloudTop: 3000,
    type: 'stratocumulus', detailStrength: 0.35, absorptionCoeff: 0.03,
    sunElevation: 0.05,
    description: 'Golden hour stratocumulus lit from below',
  },
  highCirrus: {
    coverage: 0.3, cloudBase: 8000, cloudTop: 12000,
    type: 'cirrus', detailStrength: 0.6, absorptionCoeff: 0.01,
    description: 'Delicate ice crystal wisps at high altitude',
  },
  mackerelSky: {
    coverage: 0.5, cloudBase: 3000, cloudTop: 5000,
    type: 'altocumulus', detailStrength: 0.45, absorptionCoeff: 0.03,
    description: 'Rippled altocumulus creating a textured sky pattern',
  },
};
```

## Complete Scene Assembly

```javascript
async function init() {
  const canvas = document.querySelector('#canvas');
  const { renderer, gpuAvailable } = await createRenderer(canvas);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 1, 10000);
  camera.position.set(0, 20, 100);

  const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.maxPolarAngle = Math.PI * 0.49;

  // Sky gradient background
  scene.background = createSkyGradient();

  // Ground
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(2000, 2000),
    new THREE.MeshStandardMaterial({ color: 0x4a7c3f, roughness: 0.9 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  // Lighting
  const sun = new THREE.DirectionalLight(0xfff4e5, 1.5);
  sun.position.set(200, 300, 150);
  scene.add(sun);
  scene.add(new THREE.HemisphereLight(0x87ceeb, 0x4a7c3f, 0.6));

  // Clouds — select path based on capability
  let cloudSystem;
  if (gpuAvailable) {
    // Volumetric raymarching (see references for full setup)
    cloudSystem = new MeshCloudSystem(scene, { cloudBase: 80, cloudCount: 25 });
  } else {
    cloudSystem = new MeshCloudSystem(scene, { cloudBase: 80, cloudCount: 20 });
  }
  cloudSystem.generate(12345);

  // Animate
  const clock = new THREE.Clock();
  renderer.setAnimationLoop(() => {
    const t = clock.getElapsedTime();
    cloudSystem.update(t, 8);
    controls.update();
    renderer.render(scene, camera);
  });

  window.addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  });
}

function createSkyGradient() {
  const canvas = document.createElement('canvas');
  canvas.width = 2; canvas.height = 256;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, 0, 256);
  grad.addColorStop(0, '#0a4a8a');   // Zenith
  grad.addColorStop(0.5, '#5b9bd5'); // Mid-sky
  grad.addColorStop(0.8, '#c8ddf0'); // Horizon
  grad.addColorStop(1, '#e8dcc8');   // Below horizon
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 2, 256);
  const tex = new THREE.CanvasTexture(canvas);
  tex.mapping = THREE.EquirectangularReflectionMapping;
  return tex;
}

init();
```

## Performance Guidelines

| Path | Cost | Max Clouds | Target FPS |
|------|------|-----------|------------|
| Volumetric | High | Full sky coverage | 30+ (desktop) |
| Mesh Cluster | Medium | 20–40 cloud groups | 60 (desktop), 30 (mobile) |
| Billboard | Low | 50+ sprites | 60 everywhere |

**Volumetric optimization**:
- Reduce `MAX_STEPS` (64 for quality, 32 for performance).
- Quarter-resolution render target, bilateral upsample.
- Temporal reprojection: reuse previous frame, march 1/4 of rays per frame.
- Blue noise dithering on step offset to hide banding.

**Mesh cluster optimization**:
- Merge particles into fewer draw calls via `InstancedMesh`.
- Reduce `particlesPerCloud` for distant clouds.
- Sort back-to-front per frame for correct transparency (or use additive blending).

**Shared tips**:
- `depthWrite: false` on all cloud materials — clouds don't occlude each other properly via depth.
- Distance fade: dissolve clouds beyond a radius with alpha.
- Skybox fallback: for extreme distance, bake clouds into a cubemap.

## Common Pitfalls

1. **Flat/boring clouds**: Insufficient octaves in FBM. Use 5+ octaves for the detail pass and vary `coverage` to create interesting negative space.
2. **Grey mush at sunset**: Must tint cloud color by sun angle. Apply `cloudColorForTimeOfDay()` and increase scattering at low elevation.
3. **Banding in raymarching**: Add jitter to initial ray offset: `t += hash(screenUV) * stepSize`. Blue noise texture gives best results.
4. **Transparent sorting artifacts (mesh path)**: Sort instances back-to-front, or use additive blending (loses dark cloud bases).
5. **Clouds clip through terrain**: Cloud base must be above camera + terrain. Use depth buffer to composite volumetric clouds behind geometry.

## References

- `references/cloud-shaders.md` — Complete GLSL vertex/fragment shaders for all three paths, WGSL compute noise, god ray post-process.
- `references/cloud-types.md` — Detailed profiles for all 10 cloud genera with density field parameters, lighting settings, and artistic direction.
