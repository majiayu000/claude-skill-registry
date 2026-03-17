---
name: procedural-starfield
description: >
  Generate stunning procedural night skies, starfields, nebulae, and celestial phenomena
  in Three.js using WebGPU compute with WebGL2 fallback. Covers scientifically-grounded
  starfields with spectral color temperature, magnitude-based brightness, and twinkling;
  volumetric nebulae with emission/absorption/reflection types; the Milky Way band;
  constellations with optional line overlays; planets and moons with phase lighting;
  shooting stars and meteor showers; aurora integration; eclipses (solar and lunar);
  comets with ion/dust tails; galaxies as deep-sky backdrop objects; and a full
  sky dome controller with time-of-night progression, moon phases, and horizon glow.
  Triggers: "procedural starfield", "night sky", "star rendering", "nebula",
  "deep space", "milky way", "constellation", "shooting star", "meteor shower",
  "celestial", "space background", "starbox", "skybox stars", "galaxy background",
  "moon phases", "comet", "eclipse", "space scene", "star shader".
---

# Procedural Starfield & Celestial Phenomena

Generate breathtaking night skies in Three.js — from photorealistic starfields to
dreamy nebulae to dramatic celestial events.

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│               Night Sky Pipeline                      │
│                                                      │
│  SkyController (master orchestrator)                 │
│    ├── time progression (sunset → night → dawn)      │
│    ├── moon phase + position                         │
│    └── drives all layers:                            │
│                                                      │
│  ┌─ Layer 1: Sky Dome ──────────────────────────┐    │
│  │  Gradient background, horizon glow, zodiacal │    │
│  └──────────────────────────────────────────────┘    │
│  ┌─ Layer 2: Stars ─────────────────────────────┐    │
│  │  Points with spectral color + magnitude      │    │
│  │  Twinkle, proper motion (optional)           │    │
│  └──────────────────────────────────────────────┘    │
│  ┌─ Layer 3: Milky Way ─────────────────────────┐    │
│  │  Textured band or procedural FBM glow        │    │
│  └──────────────────────────────────────────────┘    │
│  ┌─ Layer 4: Nebulae ───────────────────────────┐    │
│  │  Volumetric raymarched or billboard sprites  │    │
│  └──────────────────────────────────────────────┘    │
│  ┌─ Layer 5: Celestial Bodies ──────────────────┐    │
│  │  Moon (phase lit), planets, sun glow         │    │
│  └──────────────────────────────────────────────┘    │
│  ┌─ Layer 6: Transients ────────────────────────┐    │
│  │  Shooting stars, comets, eclipses, satellites│    │
│  └──────────────────────────────────────────────┘    │
│  ┌─ Layer 7: Deep Space (optional) ─────────────┐    │
│  │  Distant galaxies, star clusters, dust lanes │    │
│  └──────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

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
  } catch (e) {}
  if (!renderer) {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
  }
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  return { renderer, gpuAvailable };
}
```

## Layer 1: Sky Dome

Gradient hemisphere that transitions from deep zenith to warm horizon glow, with
optional light pollution and twilight blending.

```javascript
function createSkyDome(radius = 500) {
  const geo = new THREE.SphereGeometry(radius, 32, 16);
  const material = new THREE.ShaderMaterial({
    uniforms: {
      zenithColor:   { value: new THREE.Color(0x020010) },
      midColor:      { value: new THREE.Color(0x0a0a2a) },
      horizonColor:  { value: new THREE.Color(0x15102a) },
      horizonGlow:   { value: new THREE.Color(0x1a1530) },
      glowStrength:  { value: 0.3 },
      lightPollution: { value: 0.0 },  // 0=pristine, 1=urban
      moonPos:       { value: new THREE.Vector3(0, 0.5, -1).normalize() },
      moonGlowStr:   { value: 0.15 },
    },
    vertexShader: `
      varying vec3 vWorldDir;
      void main() {
        vec4 worldPos = modelMatrix * vec4(position, 1.0);
        vWorldDir = normalize(worldPos.xyz);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: SKY_DOME_FRAG, // See references/celestial-shaders.md
    side: THREE.BackSide,
    depthWrite: false,
  });

  return new THREE.Mesh(geo, material);
}
```

## Layer 2: Starfield

The heart of the night sky. Each star is a `Points` particle with scientifically-
grounded color (spectral class → blackbody temperature), magnitude-based size/brightness,
and animated twinkle.

### Star Generation

```javascript
class Starfield {
  constructor(scene, options = {}) {
    this.scene = scene;
    this.count = options.count ?? 8000;
    this.radius = options.radius ?? 400;
    this.minMagnitude = options.minMagnitude ?? -1.5; // Brightest (Sirius)
    this.maxMagnitude = options.maxMagnitude ?? 6.5;  // Faintest visible
    this.twinkleSpeed = options.twinkleSpeed ?? 1.0;
    this.seed = options.seed ?? 42;

    this._build();
  }

  _build() {
    const positions = new Float32Array(this.count * 3);
    const starData = new Float32Array(this.count * 4); // r, g, b, magnitude

    let rng = this.seed;
    const random = () => { rng = (rng * 16807) % 2147483647; return rng / 2147483647; };

    for (let i = 0; i < this.count; i++) {
      // Uniform distribution on sphere
      const theta = random() * Math.PI * 2;
      const phi = Math.acos(2 * random() - 1);

      positions[i * 3]     = Math.sin(phi) * Math.cos(theta) * this.radius;
      positions[i * 3 + 1] = Math.sin(phi) * Math.sin(theta) * this.radius;
      positions[i * 3 + 2] = Math.cos(phi) * this.radius;

      // Magnitude: exponential distribution (many faint, few bright)
      const mag = this.minMagnitude + Math.pow(random(), 0.4) * (this.maxMagnitude - this.minMagnitude);

      // Spectral color from temperature
      const temp = this._randomStarTemp(random());
      const col = blackbodyColor(temp);

      starData[i * 4]     = col.r;
      starData[i * 4 + 1] = col.g;
      starData[i * 4 + 2] = col.b;
      starData[i * 4 + 3] = mag;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('aStarData', new THREE.BufferAttribute(starData, 4));

    this.material = new THREE.ShaderMaterial({
      uniforms: {
        time:          { value: 0 },
        twinkleSpeed:  { value: this.twinkleSpeed },
        brightnessExp: { value: 2.5 },  // Magnitude → size exponent
        baseSizePx:    { value: 2.5 },
        glowFalloff:   { value: 0.4 },
        exposure:      { value: 1.0 },
      },
      vertexShader: STAR_VERT,     // See references/celestial-shaders.md
      fragmentShader: STAR_FRAG,   // See references/celestial-shaders.md
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });

    this.mesh = new THREE.Points(geometry, this.material);
    this.mesh.frustumCulled = false;
    this.scene.add(this.mesh);
  }

  // Realistic star temperature distribution
  _randomStarTemp(r) {
    // Weighted toward cooler stars (M/K/G), fewer hot O/B
    if (r < 0.003)  return 30000 + r * 5000000;  // O: blue-white
    if (r < 0.01)   return 10000 + r * 1000000;   // B: blue
    if (r < 0.04)   return 7500 + r * 60000;      // A: white
    if (r < 0.11)   return 6000 + r * 15000;      // F: yellow-white
    if (r < 0.23)   return 5200 + r * 5000;       // G: yellow (Sun-like)
    if (r < 0.50)   return 3700 + r * 3000;       // K: orange
    return 2400 + r * 2600;                        // M: red
  }

  update(time) {
    this.material.uniforms.time.value = time;
  }

  dispose() {
    this.scene.remove(this.mesh);
    this.mesh.geometry.dispose();
    this.material.dispose();
  }
}
```

### Blackbody Color Function

Convert Kelvin temperature to RGB for accurate star colors:

```javascript
function blackbodyColor(tempK) {
  // Attempt a physically-grounded approximation (Tanner Helland algorithm)
  const t = tempK / 100;
  let r, g, b;

  if (t <= 66) {
    r = 255;
    g = 99.4708025861 * Math.log(t) - 161.1195681661;
    b = t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307;
  } else {
    r = 329.698727446 * Math.pow(t - 60, -0.1332047592);
    g = 288.1221695283 * Math.pow(t - 60, -0.0755148492);
    b = 255;
  }

  return new THREE.Color(
    Math.min(Math.max(r, 0), 255) / 255,
    Math.min(Math.max(g, 0), 255) / 255,
    Math.min(Math.max(b, 0), 255) / 255
  );
}
```

**Star spectral classes and their temperatures/colors:**

| Class | Temp (K) | Color | Fraction | Examples |
|-------|----------|-------|----------|----------|
| O | 30,000+ | Blue-violet | 0.003% | Mintaka |
| B | 10,000–30,000 | Blue-white | 0.1% | Rigel, Spica |
| A | 7,500–10,000 | White | 0.6% | Sirius, Vega |
| F | 6,000–7,500 | Yellow-white | 3% | Procyon |
| G | 5,200–6,000 | Yellow | 8% | Sun, Alpha Centauri |
| K | 3,700–5,200 | Orange | 12% | Arcturus |
| M | 2,400–3,700 | Red-orange | 76% | Betelgeuse, Proxima |

## Layer 3: Milky Way

A luminous band across the sky, rendered as a textured strip or procedural FBM glow
on the sky dome.

```javascript
function createMilkyWay(scene, radius = 450) {
  const geo = new THREE.SphereGeometry(radius, 64, 32);
  const material = new THREE.ShaderMaterial({
    uniforms: {
      time:       { value: 0 },
      brightness: { value: 0.25 },
      bandWidth:  { value: 0.18 },      // Angular width of the band
      bandTilt:   { value: 0.4 },       // Tilt angle in radians
      coreGlow:   { value: 0.6 },       // Sagittarius core brightness
      dustLanes:  { value: 0.4 },       // Dark lane intensity
      warmTint:   { value: new THREE.Color(0xffe8cc) },
      coolTint:   { value: new THREE.Color(0xccddff) },
    },
    vertexShader: `
      varying vec3 vWorldDir;
      void main() {
        vWorldDir = normalize((modelMatrix * vec4(position, 1.0)).xyz);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: MILKY_WAY_FRAG, // See references/celestial-shaders.md
    side: THREE.BackSide,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  const mesh = new THREE.Mesh(geo, material);
  scene.add(mesh);
  return { mesh, material };
}
```

## Layer 4: Nebulae

### Volumetric Nebula (WebGPU — Raymarched)

Full 3D nebula rendered by marching through an emission/absorption density field.

```javascript
function createVolumetricNebula(scene, options = {}) {
  const {
    position = new THREE.Vector3(100, 80, -200),
    scale = 80,
    type = 'emission',  // emission | reflection | dark | planetary
    color1 = new THREE.Color(0xff2266),
    color2 = new THREE.Color(0x4466ff),
    color3 = new THREE.Color(0x22ffaa),
  } = options;

  const geo = new THREE.BoxGeometry(1, 1, 1);
  const material = new THREE.ShaderMaterial({
    uniforms: {
      cameraPos:    { value: new THREE.Vector3() },
      nebulaScale:  { value: scale },
      color1:       { value: color1 },
      color2:       { value: color2 },
      color3:       { value: color3 },
      density:      { value: 0.5 },
      brightness:   { value: 1.2 },
      noiseOctaves: { value: 5 },
      time:         { value: 0 },
      nebulaType:   { value: NEBULA_TYPE_MAP[type] },
    },
    vertexShader: NEBULA_VERT,
    fragmentShader: NEBULA_FRAG, // See references/celestial-shaders.md
    transparent: true,
    depthWrite: false,
    side: THREE.BackSide,
    blending: THREE.AdditiveBlending,
  });

  const mesh = new THREE.Mesh(geo, material);
  mesh.position.copy(position);
  mesh.scale.setScalar(scale);
  scene.add(mesh);
  return { mesh, material };
}

const NEBULA_TYPE_MAP = { emission: 0, reflection: 1, dark: 2, planetary: 3 };
```

### Billboard Nebula (WebGL Fallback)

Canvas-generated nebula sprite for cheaper rendering.

```javascript
function createBillboardNebula(scene, options = {}) {
  const size = options.size ?? 512;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');

  // Layer multiple radial gradients with noise displacement
  const colors = options.colors ?? ['#ff2266', '#4466ff', '#22ffaa'];
  const centers = [
    { x: size * 0.45, y: size * 0.5 },
    { x: size * 0.55, y: size * 0.45 },
    { x: size * 0.5, y: size * 0.55 },
  ];

  ctx.globalCompositeOperation = 'screen';
  for (let i = 0; i < colors.length; i++) {
    const grad = ctx.createRadialGradient(
      centers[i].x, centers[i].y, 0,
      centers[i].x, centers[i].y, size * 0.4
    );
    grad.addColorStop(0, colors[i] + 'aa');
    grad.addColorStop(0.3, colors[i] + '44');
    grad.addColorStop(0.7, colors[i] + '11');
    grad.addColorStop(1, colors[i] + '00');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, size, size);
  }

  // Add noise texture for structure
  const imgData = ctx.getImageData(0, 0, size, size);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const idx = (y * size + x) * 4;
      const n = fbm2D(x / size * 8, y / size * 8, 5) * 0.5;
      for (let c = 0; c < 3; c++) {
        imgData.data[idx + c] = Math.min(255, imgData.data[idx + c] * (0.7 + n * 0.6));
      }
      imgData.data[idx + 3] = Math.min(255, imgData.data[idx + 3] * (0.5 + n * 0.5));
    }
  }
  ctx.putImageData(imgData, 0, 0);

  const tex = new THREE.CanvasTexture(canvas);
  const spriteMat = new THREE.SpriteMaterial({
    map: tex, transparent: true, blending: THREE.AdditiveBlending,
    depthWrite: false, opacity: options.opacity ?? 0.7,
  });
  const sprite = new THREE.Sprite(spriteMat);
  sprite.scale.setScalar(options.worldSize ?? 100);
  sprite.position.copy(options.position ?? new THREE.Vector3(100, 80, -200));
  scene.add(sprite);
  return sprite;
}

function fbm2D(x, y, octaves) {
  let sum = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    sum += (Math.sin(x * freq * 127.1 + y * freq * 311.7) * 0.5 + 0.5) * amp;
    max += amp; amp *= 0.5; freq *= 2;
  }
  return sum / max;
}
```

## Layer 5: Celestial Bodies

### Moon

Sphere with phase-accurate lighting based on sun-moon angle.

```javascript
class Moon {
  constructor(scene, options = {}) {
    this.scene = scene;
    this.radius = options.radius ?? 8;
    this.distance = options.distance ?? 350;
    this.phase = options.phase ?? 0.0; // 0=new, 0.5=full, 1=new

    const geo = new THREE.SphereGeometry(this.radius, 32, 32);
    this.material = new THREE.ShaderMaterial({
      uniforms: {
        sunDir:       { value: new THREE.Vector3() },
        moonColor:    { value: new THREE.Color(0xf5f0e0) },
        shadowColor:  { value: new THREE.Color(0x111115) },
        craterScale:  { value: 3.0 },
        craterDepth:  { value: 0.15 },
        glowColor:    { value: new THREE.Color(0xddeeff) },
        glowStrength: { value: 0.3 },
      },
      vertexShader: MOON_VERT,
      fragmentShader: MOON_FRAG, // See references/celestial-shaders.md
      transparent: true,
    });

    this.mesh = new THREE.Mesh(geo, this.material);
    // Glow sprite behind moon
    this.glow = this._createGlow();
    this.group = new THREE.Group();
    this.group.add(this.glow);
    this.group.add(this.mesh);
    this.scene.add(this.group);
  }

  _createGlow() {
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 128;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0, 'rgba(220,230,255,0.3)');
    grad.addColorStop(0.3, 'rgba(200,215,255,0.1)');
    grad.addColorStop(1, 'rgba(200,215,255,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 128, 128);
    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({
      map: tex, transparent: true, depthWrite: false,
      blending: THREE.AdditiveBlending,
    });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.setScalar(this.radius * 5);
    return sprite;
  }

  setPhaseAndPosition(phase, elevation, azimuth) {
    this.phase = phase;
    // Position on sky dome
    const elRad = elevation * Math.PI / 180;
    const azRad = azimuth * Math.PI / 180;
    this.group.position.set(
      Math.cos(elRad) * Math.sin(azRad) * this.distance,
      Math.sin(elRad) * this.distance,
      Math.cos(elRad) * Math.cos(azRad) * this.distance
    );
    // Sun direction relative to moon for phase lighting
    const phaseAngle = phase * Math.PI * 2;
    this.material.uniforms.sunDir.value.set(
      Math.sin(phaseAngle), 0.1, -Math.cos(phaseAngle)
    ).normalize();
  }

  dispose() { this.scene.remove(this.group); }
}
```

## Layer 6: Transient Events

### Shooting Stars / Meteors

Bright streak that flares and fades over 0.5–2 seconds.

```javascript
class MeteorSystem {
  constructor(scene, options = {}) {
    this.scene = scene;
    this.rate = options.rate ?? 0.15;     // Meteors per second
    this.skyRadius = options.skyRadius ?? 380;
    this.meteors = [];
    this._timer = 0;
  }

  _spawn() {
    // Random start point on upper hemisphere
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI * 0.4; // Upper sky
    const start = new THREE.Vector3(
      Math.sin(phi) * Math.cos(theta) * this.skyRadius,
      Math.cos(phi) * this.skyRadius,
      Math.sin(phi) * Math.sin(theta) * this.skyRadius
    );

    // Direction: roughly downward with lateral drift
    const dir = new THREE.Vector3(
      (Math.random() - 0.5) * 0.5,
      -0.7 - Math.random() * 0.3,
      (Math.random() - 0.5) * 0.5
    ).normalize();

    const length = 15 + Math.random() * 30;
    const end = start.clone().add(dir.clone().multiplyScalar(length));

    // Build trail geometry
    const positions = new Float32Array(6); // 2 points
    positions[0] = start.x; positions[1] = start.y; positions[2] = start.z;
    positions[3] = end.x;   positions[4] = end.y;   positions[5] = end.z;

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const mat = new THREE.LineBasicMaterial({
      color: 0xffffff, transparent: true, opacity: 1.0,
      blending: THREE.AdditiveBlending, depthWrite: false,
    });

    const line = new THREE.Line(geo, mat);
    this.scene.add(line);

    // Glow head
    const headMat = new THREE.SpriteMaterial({
      color: 0xffffcc, transparent: true, opacity: 0.8,
      blending: THREE.AdditiveBlending, depthWrite: false,
    });
    const head = new THREE.Sprite(headMat);
    head.scale.setScalar(2);
    head.position.copy(end);
    this.scene.add(head);

    const duration = 0.4 + Math.random() * 1.2;
    this.meteors.push({ line, head, mat, headMat, life: duration, maxLife: duration });
  }

  update(dt) {
    this._timer += dt;
    if (this._timer > 1 / this.rate) {
      this._timer = 0;
      if (Math.random() < 0.7) this._spawn(); // Some variance
    }

    for (let i = this.meteors.length - 1; i >= 0; i--) {
      const m = this.meteors[i];
      m.life -= dt;
      const t = m.life / m.maxLife;
      // Flare then fade: peak brightness at t≈0.7
      const brightness = t > 0.7 ? (1 - t) / 0.3 : t / 0.7;
      m.mat.opacity = brightness;
      m.headMat.opacity = brightness * 0.8;

      if (m.life <= 0) {
        this.scene.remove(m.line);
        this.scene.remove(m.head);
        m.line.geometry.dispose();
        this.meteors.splice(i, 1);
      }
    }
  }

  dispose() {
    for (const m of this.meteors) {
      this.scene.remove(m.line);
      this.scene.remove(m.head);
    }
  }
}
```

### Comet

Bright nucleus with two tails — blue-white ion tail (straight, away from sun) and
diffuse dust tail (curved, trailing orbit).

```javascript
function createComet(scene, options = {}) {
  const pos = options.position ?? new THREE.Vector3(-150, 100, -250);
  const sunDir = options.sunDir ?? new THREE.Vector3(0.3, -0.5, 0.8).normalize();

  const group = new THREE.Group();
  group.position.copy(pos);

  // Nucleus
  const nucleus = new THREE.Mesh(
    new THREE.SphereGeometry(1.5, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xeeeeff })
  );
  group.add(nucleus);

  // Coma glow
  const comaMat = new THREE.SpriteMaterial({
    color: 0xccddff, transparent: true, opacity: 0.5,
    blending: THREE.AdditiveBlending, depthWrite: false,
  });
  const coma = new THREE.Sprite(comaMat);
  coma.scale.setScalar(12);
  group.add(coma);

  // Ion tail (straight, anti-sun)
  const ionDir = sunDir.clone().negate();
  const ionPoints = [];
  for (let i = 0; i < 50; i++) {
    const t = i / 49;
    ionPoints.push(ionDir.clone().multiplyScalar(t * 120));
  }
  const ionGeo = new THREE.BufferGeometry().setFromPoints(ionPoints);
  const ionMat = new THREE.LineBasicMaterial({
    color: 0x4488ff, transparent: true, opacity: 0.4,
    blending: THREE.AdditiveBlending, depthWrite: false,
  });
  group.add(new THREE.Line(ionGeo, ionMat));

  // Dust tail (curved, broader)
  const dustDir = ionDir.clone().add(new THREE.Vector3(0.3, 0.1, 0)).normalize();
  const dustPoints = [];
  for (let i = 0; i < 40; i++) {
    const t = i / 39;
    const curve = dustDir.clone().multiplyScalar(t * 80);
    curve.x += Math.sin(t * 2) * 10 * t;
    curve.y += t * 5;
    dustPoints.push(curve);
  }
  const dustGeo = new THREE.BufferGeometry().setFromPoints(dustPoints);
  const dustMat = new THREE.LineBasicMaterial({
    color: 0xffddaa, transparent: true, opacity: 0.25,
    blending: THREE.AdditiveBlending, depthWrite: false,
  });
  group.add(new THREE.Line(dustGeo, dustMat));

  scene.add(group);
  return group;
}
```

## Sky Controller

Master orchestrator that coordinates all layers based on time and configuration.

```javascript
class NightSkyController {
  constructor(scene, camera, options = {}) {
    this.scene = scene;
    this.camera = camera;

    this.skyDome = createSkyDome();
    this.scene.add(this.skyDome);

    this.starfield = new Starfield(scene, {
      count: options.starCount ?? 8000,
      twinkleSpeed: options.twinkleSpeed ?? 1.0,
    });

    this.milkyWay = createMilkyWay(scene);
    this.moon = new Moon(scene);
    this.meteors = new MeteorSystem(scene, { rate: options.meteorRate ?? 0.1 });
    this.nebulae = [];

    // Time: 0=sunset, 0.5=midnight, 1=sunrise
    this.nightProgress = options.startTime ?? 0.5;
  }

  addNebula(options) {
    const nebula = createBillboardNebula(this.scene, options);
    this.nebulae.push(nebula);
    return nebula;
  }

  update(dt) {
    const t = performance.now() * 0.001;
    this.starfield.update(t);
    this.meteors.update(dt);

    // Moon position from night progress
    const moonElev = Math.sin(this.nightProgress * Math.PI) * 60;
    const moonAz = this.nightProgress * 180 - 90;
    this.moon.setPhaseAndPosition(this.moon.phase, moonElev, moonAz);

    // Milky Way rotation
    this.milkyWay.mesh.rotation.y = t * 0.001;
  }

  setNightProgress(t) { this.nightProgress = Math.max(0, Math.min(1, t)); }
  setMoonPhase(phase) { this.moon.phase = phase; }

  dispose() {
    this.starfield.dispose();
    this.moon.dispose();
    this.meteors.dispose();
    this.scene.remove(this.skyDome);
    this.scene.remove(this.milkyWay.mesh);
    for (const n of this.nebulae) this.scene.remove(n);
  }
}
```

## Night Sky Presets

```javascript
const SKY_PRESETS = {
  pristineMountain: {
    starCount: 12000, lightPollution: 0.0, milkyWayBrightness: 0.35,
    meteorRate: 0.12, moonPhase: 0.0,
    description: 'Remote mountain — maximum stars, vivid Milky Way, no moon',
  },
  fullMoonNight: {
    starCount: 4000, lightPollution: 0.05, milkyWayBrightness: 0.08,
    meteorRate: 0.05, moonPhase: 0.5,
    description: 'Bright full moon washes out fainter stars and Milky Way',
  },
  suburbanSky: {
    starCount: 2000, lightPollution: 0.4, milkyWayBrightness: 0.02,
    meteorRate: 0.08, moonPhase: 0.25,
    description: 'Light pollution hides faint stars, warm horizon glow',
  },
  meteorShower: {
    starCount: 10000, lightPollution: 0.0, milkyWayBrightness: 0.3,
    meteorRate: 0.8, moonPhase: 0.0,
    description: 'Peak Perseids — constant streaks across a pristine sky',
  },
  deepSpace: {
    starCount: 20000, lightPollution: 0.0, milkyWayBrightness: 0.5,
    meteorRate: 0.02, moonPhase: 0.0, nebulae: true, galaxies: true,
    description: 'Fantasy deep-space vista — dense stars, vivid nebulae, galaxies',
  },
  twilight: {
    starCount: 1000, lightPollution: 0.1, milkyWayBrightness: 0.0,
    meteorRate: 0.02, moonPhase: 0.4,
    description: 'Early evening — only brightest stars and planets visible',
  },
};
```

## Performance Guidelines

| Layer | Cost | Draw Calls | Notes |
|-------|------|-----------|-------|
| Sky Dome | Negligible | 1 | BackSide sphere, simple gradient |
| Starfield | Low | 1 (Points) | 8K–20K points, all in vertex shader |
| Milky Way | Low | 1 | FBM in fragment on BackSide sphere |
| Nebula (billboard) | Low | 1 per nebula | Sprite, pre-baked canvas texture |
| Nebula (volumetric) | High | 1 | Raymarched — limit steps to 48 |
| Moon | Low | 2 | Sphere + glow sprite |
| Meteors | Negligible | 0–3 | Ephemeral, 1–2 lines active at a time |
| Comet | Low | 3 | Nucleus + 2 tail lines |

**Total**: Full night sky runs at **5–8 draw calls** with additive blending everywhere.

**Key optimizations**:
- All star animation (twinkle) in vertex shader — zero JS per-star loops.
- `AdditiveBlending` on all layers — no sort order needed for transparent objects.
- `depthWrite: false` on everything except the sky dome — celestial objects never occlude each other via depth.
- Stars use `gl_PointSize` with magnitude-based scaling — one geometry, one draw call.
- Nebula billboard is pre-baked to canvas — fragment shader is a single texture sample.

## Common Pitfalls

1. **Stars visible through Moon / planets**: Sky layers need explicit render order. Set `renderOrder` so dome < stars < milky way < nebulae < moon.
2. **Stars look like a flat grid**: Ensure uniform sphere distribution using `acos(2r-1)` for phi, not linear sampling. Linear creates polar clustering.
3. **All stars same color**: Must use blackbody temperature → RGB conversion. Even subtle color variation (warm yellow, cool blue) is critical for realism.
4. **Milky Way too bright / uniform**: Use dust lane subtraction and core brightening near Sagittarius. The Milky Way is not a smooth band — it has structure.
5. **No sense of depth**: Layer multiple elements at slightly different radii and let parallax from camera rotation create subtle depth. Nebulae at 450, stars at 400, dome at 500.

## References

- `references/celestial-shaders.md` — Complete GLSL vertex/fragment shaders for sky dome, stars, Milky Way, nebula raymarching, moon surface, and WGSL star compute.
- `references/celestial-catalog.md` — Nebula type profiles, deep-sky objects, constellation data format, and artistic direction for different sky moods.
