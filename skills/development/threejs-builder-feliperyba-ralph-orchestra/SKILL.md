---
name: threejs-builder
description: >
  Creates simple Three.js web apps with scene setup, lighting, geometries, materials,
  animations, and responsive rendering. Use for: "Create a threejs scene/app/showcase"
  or when user wants 3D web content. Supports ES modules, modern Three.js r150+ APIs.
---

# Three.js Builder

A focused skill for creating simple, performant Three.js web applications using modern ES module patterns.

## Reference Files

> **Important**: Read the appropriate reference file when working on specific topics.

| Topic | File | Use When |
|-------|------|----------|
| **FBX Models** | [fbx-loading-guide.md](references/fbx-loading-guide.md) | Loading, caching, cloning 3D models, SkeletonUtils |
| **Reference Frames** | [reference-frame-contract.md](references/reference-frame-contract.md) | Calibration, anchoring, axis correctness, debugging |
| **Game Development** | [game-patterns.md](references/game-patterns.md) | State machines, animation switching, parallax, object pooling |
| **Advanced Topics** | [advanced-topics.md](references/advanced-topics.md) | Post-processing, shaders, physics, instancing |
| **Calibration Helpers** | [scripts/README.md](scripts/README.md) | FBX calibration helper installation and usage |

---

## Philosophy: The Scene Graph Mental Model

Three.js is built on the **scene graph**—a hierarchical tree of objects where parent transformations affect children. Understanding this mental model is key to effective 3D web development.

**Before creating a Three.js app, ask**:
- What is the **core visual element**? (geometry, shape, model)
- What **interaction** does the user need? (none, orbit controls, custom input)
- What **performance** constraints exist? (mobile, desktop, WebGL capabilities)
- What **animation** brings it to life? (rotation, movement, transitions)

**Core principles**:

1. **Scene Graph First**: Everything added to `scene` renders. Use `Group` for hierarchical transforms.
2. **Primitives as Building Blocks**: Built-in geometries (Box, Sphere, Torus) cover 80% of simple use cases.
3. **Animation as Transformation**: Change position/rotation/scale over time using `requestAnimationFrame` or `renderer.setAnimationLoop`.
4. **Performance Through Simplicity**: Fewer objects, fewer draw calls, reusable geometries/materials.

---

## Three.js Coordinate System (CRITICAL)

Understanding Three.js's right-handed coordinate system is **essential** to avoid inverted movement, wrong-facing models, and broken collision detection.

### The Axes

```
      +Y (up)
       |
       |
       |_______ +X (right)
      /
     /
    +Z (toward camera/viewer)
```

**Memory aid**: Point your thumb (+X), index finger (+Y), middle finger (+Z) - that's right-handed coordinates.

| Axis | Direction | Common Usage |
|------|-----------|--------------|
| +X   | Right     | Strafe right, spawn right |
| -X   | Left      | Strafe left, spawn left |
| +Y   | Up        | Jump, height |
| -Y   | Down      | Fall, gravity |
| +Z   | Toward camera | Approach viewer, "forward" in many setups |
| -Z   | Away from camera | Retreat, **glTF models face -Z by default (FBX typically +Z)** |

### Model Default Orientation

**CRITICAL**: The default forward direction depends on the model format:
- **FBX models** (from Blender/Maya): Typically face **+Z** (toward viewer) by default
- **glTF models**: Face **-Z** (into the screen) by default

**Always calibrate** using the reference frame contract to confirm forward direction for your specific asset pack.

```javascript
// For glTF models (face -Z), to face +Z (toward camera):
model.rotation.y = Math.PI;  // 180° rotation

// For FBX models (typically face +Z), may not need rotation
// Always verify with calibration!

// To face +X (right):
model.rotation.y = -Math.PI / 2;  // -90°

// To face -X (left):
model.rotation.y = Math.PI / 2;   // +90°
```

### Camera-Relative Movement (CRITICAL for Games)

**PROBLEM**: When camera is at an angle (e.g., isometric view), raw WASD input moves wrong!

```javascript
// ❌ WRONG - Input is world-axis relative, not camera-relative
if (keyW) player.position.z -= speed;  // Moves toward -Z, not "forward" from player's view
if (keyD) player.position.x += speed;  // Moves +X, not "right" from camera's view

// ✓ CORRECT - Calculate camera-relative directions
function updateMovement(deltaTime) {
    // Get camera's forward direction, projected onto ground (XZ plane)
    const forward = new THREE.Vector3();
    camera.getWorldDirection(forward);
    forward.y = 0;
    forward.normalize();

    // Calculate right vector (cross product of forward and world up)
    const right = new THREE.Vector3();
    right.crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize();

    // Apply input relative to camera orientation
    const velocity = new THREE.Vector3();
    if (inputState.up) velocity.add(forward);
    if (inputState.down) velocity.sub(forward);
    if (inputState.right) velocity.add(right);
    if (inputState.left) velocity.sub(right);

    if (velocity.length() > 0) {
        velocity.normalize().multiplyScalar(speed * deltaTime);
        player.position.add(velocity);

        // Face movement direction
        player.rotation.y = Math.atan2(velocity.x, velocity.z);
    }
}
```

**Why this matters**: With camera at `(8, 11, -6)` looking at `(0, 1, 3)`:
- "Forward" visually is NOT `-Z`, it's roughly `+Z`
- "Right" visually is NOT `+X`, it's roughly `-X + Z`
- Raw axis input feels completely inverted to players

---

## Quick Start: Essential Setup

### Minimal HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Three.js App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { overflow: hidden; background: #000; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script type="module">
        import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

        // Scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });

        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        // Your 3D content here
        // ...

        camera.position.z = 5;

        // Animation loop
        renderer.setAnimationLoop((time) => {
            renderer.render(scene, camera);
        });

        // Handle resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
```

---

## Geometries

Built-in primitives cover most simple app needs. Use `BufferGeometry` only for custom shapes.

**Common primitives**:
- `BoxGeometry(width, height, depth)` - cubes, boxes
- `SphereGeometry(radius, widthSegments, heightSegments)` - balls, planets
- `CylinderGeometry(radiusTop, radiusBottom, height)` - tubes, cylinders
- `TorusGeometry(radius, tube)` - donuts, rings
- `PlaneGeometry(width, height)` - floors, walls, backgrounds
- `ConeGeometry(radius, height)` - spikes, cones
- `IcosahedronGeometry(radius, detail)` - low-poly spheres (detail=0)

**Usage**:
```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x44aa88 });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
```

---

## Materials

Choose material based on lighting needs and visual style.

**Material selection guide**:
- `MeshBasicMaterial` - No lighting, flat colors. Use for: UI, wireframes, unlit effects
- `MeshStandardMaterial` - PBR lighting. Default for realistic surfaces
- `MeshPhysicalMaterial` - Advanced PBR with clearcoat, transmission. Glass, water
- `MeshNormalMaterial` - Debug, rainbow colors based on normals
- `MeshPhongMaterial` - Legacy, shininess control. Faster than Standard

**Common material properties**:
```javascript
{
    color: 0x44aa88,           // Hex color
    roughness: 0.5,            // 0=glossy, 1=matte (Standard/Physical)
    metalness: 0.0,            // 0=non-metal, 1=metal (Standard/Physical)
    emissive: 0x000000,        // Self-illumination color
    wireframe: false,          // Show edges only
    transparent: false,        // Enable transparency
    opacity: 1.0,              // 0=invisible, 1=opaque (needs transparent:true)
    side: THREE.FrontSide      // FrontSide, BackSide, DoubleSide
}
```

---

## Lighting

No light = black screen (except BasicMaterial/NormalMaterial).

**Light types**:
- `AmbientLight(intensity)` - Base illumination everywhere. Use 0.3-0.5
- `DirectionalLight(color, intensity)` - Sun-like, parallel rays. Cast shadows
- `PointLight(color, intensity, distance)` - Light bulb, emits in all directions
- `SpotLight(color, intensity, angle, penumbra)` - Flashlight, cone of light

**Typical lighting setup**:
```javascript
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

const mainLight = new THREE.DirectionalLight(0xffffff, 1);
mainLight.position.set(5, 10, 7);
scene.add(mainLight);

const fillLight = new THREE.DirectionalLight(0x88ccff, 0.5);
fillLight.position.set(-5, 0, -5);
scene.add(fillLight);
```

**Shadows** (advanced, use when needed):
```javascript
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

mainLight.castShadow = true;
mainLight.shadow.mapSize.width = 2048;
mainLight.shadow.mapSize.height = 2048;

mesh.castShadow = true;
mesh.receiveShadow = true;
```

---

## Animation

Transform objects over time using the animation loop.

**Animation patterns**:

1. **Continuous rotation**:
```javascript
renderer.setAnimationLoop((time) => {
    mesh.rotation.x = time * 0.001;
    mesh.rotation.y = time * 0.0005;
    renderer.render(scene, camera);
});
```

2. **Wave/bobbing motion**:
```javascript
renderer.setAnimationLoop((time) => {
    mesh.position.y = Math.sin(time * 0.002) * 0.5;
    renderer.render(scene, camera);
});
```

3. **Mouse interaction**:
```javascript
const mouse = new THREE.Vector2();

window.addEventListener('mousemove', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
});

renderer.setAnimationLoop(() => {
    mesh.rotation.x = mouse.y * 0.5;
    mesh.rotation.y = mouse.x * 0.5;
    renderer.render(scene, camera);
});
```

---

## Camera Controls

Import OrbitControls from examples for interactive camera movement:

```html
<script type="module">
    import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
    import { OrbitControls } from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

    // ... scene setup ...

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    renderer.setAnimationLoop(() => {
        controls.update();
        renderer.render(scene, camera);
    });
</script>
```

---

## Common Scene Patterns

### Rotating Cube (Hello World)
```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff88 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

renderer.setAnimationLoop((time) => {
    cube.rotation.x = time * 0.001;
    cube.rotation.y = time * 0.001;
    renderer.render(scene, camera);
});
```

### Floating Particle Field
```javascript
const particleCount = 1000;
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(particleCount * 3);

for (let i = 0; i < particleCount * 3; i += 3) {
    positions[i] = (Math.random() - 0.5) * 50;
    positions[i + 1] = (Math.random() - 0.5) * 50;
    positions[i + 2] = (Math.random() - 0.5) * 50;
}

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const material = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1 });
const particles = new THREE.Points(geometry, material);
scene.add(particles);
```

### Animated Background with Foreground Object
```javascript
// Background grid
const gridHelper = new THREE.GridHelper(50, 50, 0x444444, 0x222222);
scene.add(gridHelper);

// Foreground object
const mainGeometry = new THREE.IcosahedronGeometry(1, 0);
const mainMaterial = new THREE.MeshStandardMaterial({
    color: 0xff6600,
    flatShading: true
});
const mainMesh = new THREE.Mesh(mainGeometry, mainMaterial);
scene.add(mainMesh);
```

---

## Colors

Three.js uses hexadecimal color format: `0xRRGGBB`

Common hex colors:
- Black: `0x000000`, White: `0xffffff`
- Red: `0xff0000`, Green: `0x00ff00`, Blue: `0x0000ff`
- Cyan: `0x00ffff`, Magenta: `0xff00ff`, Yellow: `0xffff00`
- Orange: `0xff8800`, Purple: `0x8800ff`, Pink: `0xff0088`

---

## Anti-Patterns to Avoid

### Basic Setup Mistakes

❌ **Not importing OrbitControls from correct path**
Why bad: Controls won't load, `THREE.OrbitControls` is undefined in modern Three.js
Better: Use `import { OrbitControls } from 'three/addons/controls/OrbitControls.js'` or unpkg examples/jsm path

❌ **Forgetting to add object to scene**
Why bad: Object won't render, silent failure
Better: Always call `scene.add(object)` after creating meshes/lights

❌ **Using old `requestAnimationFrame` pattern instead of `setAnimationLoop`**
Why bad: More verbose, doesn't handle XR/WebXR automatically
Better: `renderer.setAnimationLoop((time) => { ... })`

### Performance Issues

❌ **Creating new geometries in animation loop**
Why bad: Massive memory allocation, frame rate collapse
Better: Create geometry once, reuse it. Transform only position/rotation/scale

❌ **Using too many segments on primitives**
Why bad: Unnecessary vertices, GPU overhead
Better: Default segments are usually fine. `SphereGeometry(1, 32, 16)` not `SphereGeometry(1, 128, 64)`

❌ **Not setting pixelRatio cap**
Why bad: 4K/5K displays run at full resolution, poor performance
Better: `Math.min(window.devicePixelRatio, 2)`

### Code Organization

❌ **Everything in one giant function**
Why bad: Hard to modify, hard to debug
Better: Separate setup into functions: `createScene()`, `createLights()`, `createMeshes()`

❌ **Hardcoding all values**
Why bad: Difficult to tweak and experiment
Better: Define constants at top: `const CONFIG = { color: 0x00ff88, speed: 0.001 }`

---

## Variation Guidance

**IMPORTANT**: Each Three.js app should feel unique and context-appropriate.

**Vary by scenario**:
- **Portfolio/showcase**: Elegant, smooth animations, muted colors
- **Game/interactive**: Bright colors, snappy controls, particle effects
- **Data visualization**: Clean lines, grid helpers, clear labels
- **Background effect**: Subtle, slow movement, dark/gradient backgrounds
- **Product viewer**: Realistic lighting, PBR materials, smooth orbit

**Vary visual elements**:
- **Geometry choice**: Not everything needs to be a cube. Explore spheres, tori, icosahedra
- **Material style**: Mix flat shaded, glossy, metallic, wireframe
- **Color palettes**: Use complementary, analogous, or monochromatic schemes
- **Animation style**: Rotation, oscillation, wave motion, mouse tracking

**Avoid converging on**:
- Default green cube as first example every time
- Same camera angle (front-facing, z=5)
- Identical lighting setup (always directional light at 1,1,1)

---

## Remember

**Three.js is a tool for interactive 3D on the web.**

Effective Three.js apps:
- Start with the scene graph mental model
- Use primitives as building blocks
- Keep animations simple and performant
- Vary visual style based on purpose
- Import from modern ES module paths

**Modern Three.js (r150+) uses ES modules from `three` package or CDN.** CommonJS patterns and global `THREE` variable are legacy.

**Claude is capable of creating elegant, performant 3D web experiences. These patterns guide the way—they don't limit the result.**

For specific topics, see the **Reference Files** table at the top of this document.
