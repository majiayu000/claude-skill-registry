---
name: cesiumjs-models-particles
description: "CesiumJS models, glTF, and particle effects - Model, ModelAnimation, ModelNode, ParticleSystem, emitters, GPM extensions. Use when loading glTF/GLB 3D models, playing model animations, positioning particle effects like fire or smoke, or working with geospatial positioning metadata."
---
# CesiumJS Models, glTF & Particle Effects

## Quick Reference

| Class | Purpose |
|---|---|
| `Model` | Low-level glTF/GLB primitive; positioned via `modelMatrix` |
| `ModelAnimation` | Active animation instance on a model |
| `ModelAnimationCollection` | Collection at `model.activeAnimations` |
| `ModelNode` | Named node with modifiable transform |
| `ModelFeature` | Per-feature styling/picking for feature-ID models |
| `ParticleSystem` | Billboard-based particle manager (fire, smoke, rain) |
| `Particle` | Single particle with position, velocity, life |
| `ParticleBurst` | Scheduled burst of particles |
| `BoxEmitter` / `CircleEmitter` | Emit within box volume / flat disk |
| `ConeEmitter` / `SphereEmitter` | Emit from cone tip / within sphere |

The Entity API exposes models through `ModelGraphics` (see cesiumjs-entities). The Primitive API uses `Model.fromGltfAsync` for full control over `modelMatrix`, animations, and node transforms.

---

## Loading a glTF/GLB Model

Always use the async factory -- never call the constructor directly.

```js
import { Model, Cartesian3, Transforms, HeadingPitchRoll, Math as CesiumMath } from "cesium";

const model = await Model.fromGltfAsync({ url: "path/to/model.glb" });
viewer.scene.primitives.add(model);
```

### Positioned Model with Heading

```js
const position = Cartesian3.fromDegrees(-123.074, 44.050, 5000);
const hpr = new HeadingPitchRoll(CesiumMath.toRadians(135), 0, 0);

const model = await Model.fromGltfAsync({
  url: "CesiumAir.glb",
  modelMatrix: Transforms.headingPitchRollToFixedFrame(position, hpr),
  minimumPixelSize: 128,  // never smaller than 128 px on screen
  maximumScale: 20000,    // cap for minimumPixelSize enlargement
  scale: 2.0,             // uniform scale multiplier
});
viewer.scene.primitives.add(model);
```

### Key `Model.fromGltfAsync` Options

| Option | Type | Default |
|---|---|---|
| `url` | `string\|Resource` | required |
| `modelMatrix` | `Matrix4` | `IDENTITY` |
| `scale` | `number` | `1.0` |
| `minimumPixelSize` | `number` | `0.0` |
| `maximumScale` | `number` | -- |
| `show` | `boolean` | `true` |
| `color` / `colorBlendMode` / `colorBlendAmount` | `Color` / `ColorBlendMode` / `number` | -- / `HIGHLIGHT` / `0.5` |
| `silhouetteColor` / `silhouetteSize` | `Color` / `number` | `RED` / `0.0` |
| `shadows` | `ShadowMode` | `ENABLED` |
| `heightReference` | `HeightReference` | `NONE` |
| `customShader` | `CustomShader` | -- |
| `id` | `any` | -- |
| `allowPicking` | `boolean` | `true` |

---

## Readiness and Lifecycle

`fromGltfAsync` resolves once glTF JSON is parsed, but WebGL resources may still load. Wait for `readyEvent` before accessing animations, nodes, or `boundingSphere`.

```js
const model = await Model.fromGltfAsync({ url: "robot.glb" });
viewer.scene.primitives.add(model);

model.readyEvent.addEventListener(() => {
  console.log("Bounding sphere:", model.boundingSphere);
});
```

```js
// Synchronous check
if (model.ready) { const bs = model.boundingSphere; }
```

---

## Animations

Managed through `model.activeAnimations` (`ModelAnimationCollection`).

### Play by Name / Play All

```js
model.readyEvent.addEventListener(() => {
  // Single animation
  const anim = model.activeAnimations.add({
    name: "Walk",                          // glTF animation name
    loop: Cesium.ModelAnimationLoop.REPEAT, // NONE | REPEAT | MIRRORED_REPEAT
    multiplier: 1.0,                       // playback speed (must be > 0)
  });
  anim.start.addEventListener((m, a) => console.log(`Started: ${a.name}`));

  // Or play all animations at once
  model.activeAnimations.addAll({
    loop: Cesium.ModelAnimationLoop.REPEAT,
    multiplier: 0.5,
  });
});
```

Additional `add` options: `index`, `reverse`, `startTime`, `stopTime`, `delay`, `removeOnStop`, `animationTime` (custom time callback).

### Animation Events

```js
animation.start.addEventListener((model, animation) => { });
animation.update.addEventListener((model, animation, time) => { });
animation.stop.addEventListener((model, animation) => { });
// Collection-level
model.activeAnimations.animationAdded.addEventListener((model, anim) => { });
```

```js
model.activeAnimations.remove(animation); // remove one
model.activeAnimations.removeAll();        // remove all
```

---

## Model Nodes

Override named node transforms for procedural animation (e.g., turret rotation).

```js
model.readyEvent.addEventListener(() => {
  const node = model.getNode("Turret");
  node.matrix = Cesium.Matrix4.fromScale(
    new Cesium.Cartesian3(5.0, 1.0, 1.0), node.matrix
  );
});
```

Properties: `name` (read-only), `id` (read-only index), `show` (boolean), `matrix` (Matrix4 -- set to `undefined` to restore original and re-enable glTF animations).

---

## Coloring, Silhouettes, and Feature Picking

```js
// Tint + silhouette
model.color = Cesium.Color.RED.withAlpha(0.5);
model.colorBlendMode = Cesium.ColorBlendMode.MIX;
model.colorBlendAmount = 0.5;
model.silhouetteColor = Cesium.Color.YELLOW;
model.silhouetteSize = 2.0;
```

When a glTF has `EXT_mesh_features` or `EXT_structural_metadata`, picking returns a `ModelFeature`:

```js
const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
handler.setInputAction((movement) => {
  const picked = viewer.scene.pick(movement.endPosition);
  if (picked instanceof Cesium.ModelFeature) {
    picked.getPropertyIds().forEach((name) => {
      console.log(`${name}: ${picked.getProperty(name)}`);
    });
    picked.color = Cesium.Color.YELLOW;
  }
}, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
```

---

## Height Reference

```js
// Primitive API -- scene is required for height reference
const model = await Model.fromGltfAsync({
  url: "truck.glb",
  heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
  scene: viewer.scene,
});

// Entity API
viewer.entities.add({
  position: Cartesian3.fromDegrees(-75.59, 40.03),
  model: { uri: "truck.glb", heightReference: Cesium.HeightReference.CLAMP_TO_GROUND },
});
```

Values: `NONE`, `CLAMP_TO_GROUND`, `RELATIVE_TO_GROUND`, `CLAMP_TO_TERRAIN`, `RELATIVE_TO_TERRAIN`, `CLAMP_TO_3D_TILE`, `RELATIVE_TO_3D_TILE`.

---

## Particle Systems

`ParticleSystem` renders billboard-based effects. Position with `modelMatrix` (world) and `emitterModelMatrix` (local offset).

### Smoke Trail

```js
import { ParticleSystem, CircleEmitter, Color, Cartesian2, Transforms, Cartesian3 } from "cesium";

const smokeSystem = new ParticleSystem({
  image: "smoke.png",
  startColor: Color.LIGHTGRAY.withAlpha(0.7),
  endColor: Color.WHITE.withAlpha(0.0),
  startScale: 1.0,
  endScale: 5.0,
  emissionRate: 10,
  minimumSpeed: 1.0,
  maximumSpeed: 4.0,
  minimumParticleLife: 1.2,
  maximumParticleLife: 3.0,
  imageSize: new Cartesian2(25, 25), // pixel size
  emitter: new CircleEmitter(2.0),   // radius in meters
  modelMatrix: Transforms.eastNorthUpToFixedFrame(Cartesian3.fromDegrees(-75.157, 39.978)),
  lifetime: 16.0,
  loop: true,
});
viewer.scene.primitives.add(smokeSystem);
```

### Emitter Types

```js
import { BoxEmitter, CircleEmitter, ConeEmitter, SphereEmitter } from "cesium";

new BoxEmitter(new Cesium.Cartesian3(10, 10, 10));  // 3D box, velocity outward
new CircleEmitter(2.0);                              // flat disk, velocity +Z
new ConeEmitter(Cesium.Math.toRadians(30));          // cone tip, velocity toward base
new SphereEmitter(5.0);                              // sphere, velocity radiates out
```

### Particle Bursts

```js
const firework = new ParticleSystem({
  image: getParticleCanvas(),
  startColor: Color.RED,
  endColor: Color.RED.withAlpha(0.0),
  particleLife: 1.0,
  speed: 100.0,
  imageSize: new Cartesian2(7, 7),
  emissionRate: 0,  // bursts only
  emitter: new SphereEmitter(0.1),
  bursts: [
    new Cesium.ParticleBurst({ time: 0.0, minimum: 100, maximum: 200 }),
    new Cesium.ParticleBurst({ time: 2.0, minimum: 50, maximum: 100 }),
    new Cesium.ParticleBurst({ time: 4.0, minimum: 200, maximum: 300 }),
  ],
  lifetime: 6.0,
  loop: false,
  modelMatrix: Transforms.eastNorthUpToFixedFrame(Cartesian3.fromDegrees(-75.597, 40.038)),
});
viewer.scene.primitives.add(firework);
```

### Update Callback (Gravity / Wind)

The `updateCallback` runs per-particle per-frame for forces like gravity.

```js
const gravityScratch = new Cesium.Cartesian3();
function applyGravity(particle, dt) {
  Cesium.Cartesian3.normalize(particle.position, gravityScratch);
  Cesium.Cartesian3.multiplyByScalar(gravityScratch, -9.8 * dt, gravityScratch);
  particle.velocity = Cesium.Cartesian3.add(particle.velocity, gravityScratch, particle.velocity);
}

const system = new ParticleSystem({
  image: "smoke.png",
  emissionRate: 20,
  emitter: new ConeEmitter(Cesium.Math.toRadians(45)),
  updateCallback: applyGravity,
  modelMatrix: Transforms.eastNorthUpToFixedFrame(Cartesian3.fromDegrees(-105, 40, 1000)),
});
viewer.scene.primitives.add(system);
```

---

## Attaching Particles to a Moving Model

Sync `modelMatrix` each frame via `scene.preUpdate`. Use `emitterModelMatrix` for a local offset (e.g., exhaust pipe).

```js
const entity = viewer.entities.add({
  position: sampledPosition,
  orientation: new Cesium.VelocityOrientationProperty(sampledPosition),
  model: { uri: "truck.glb", minimumPixelSize: 64 },
});

// Local offset to exhaust pipe
const trs = new Cesium.TranslationRotationScale();
trs.translation = new Cesium.Cartesian3(-4.0, 0.0, 1.4);
const emitterModelMatrix = Cesium.Matrix4.fromTranslationRotationScale(trs, new Cesium.Matrix4());

const exhaust = new ParticleSystem({
  image: "smoke.png",
  startColor: Color.GRAY.withAlpha(0.7),
  endColor: Color.TRANSPARENT,
  emissionRate: 8,
  speed: 2.0,
  particleLife: 1.5,
  imageSize: new Cartesian2(20, 20),
  emitter: new CircleEmitter(0.5),
  emitterModelMatrix: emitterModelMatrix,
});
viewer.scene.primitives.add(exhaust);

viewer.scene.preUpdate.addEventListener((scene, time) => {
  exhaust.modelMatrix = entity.computeModelMatrix(time, new Cesium.Matrix4());
});
```

---

## Canvas-Based Particle Images

Generate particle textures dynamically instead of loading image files.

```js
function createCircleImage() {
  const c = document.createElement("canvas");
  c.width = c.height = 20;
  const ctx = c.getContext("2d");
  ctx.beginPath();
  ctx.arc(10, 10, 10, 0, Math.PI * 2);
  ctx.fillStyle = "#fff";
  ctx.fill();
  return c;
}

// Pass canvas directly as image
new ParticleSystem({ image: createCircleImage(), /* ...other options */ });
```

---

## Entity API Model (ModelGraphics)

For simpler use cases, add a model through the Entity API (see cesiumjs-entities for full coverage).

```js
const entity = viewer.entities.add({
  name: "Aircraft",
  position: Cartesian3.fromDegrees(-123.074, 44.050, 5000),
  orientation: Cesium.Transforms.headingPitchRollQuaternion(
    Cartesian3.fromDegrees(-123.074, 44.050, 5000),
    new Cesium.HeadingPitchRoll(Cesium.Math.toRadians(135), 0, 0)
  ),
  model: {
    uri: "CesiumAir.glb",
    minimumPixelSize: 128,
    maximumScale: 20000,
    silhouetteColor: Color.RED,
    silhouetteSize: 2.0,
  },
});
viewer.trackedEntity = entity;
```

---

## GPM Extension (NGA_gpm_local)

CesiumJS experimentally supports the NGA Geospatial Positioning Metadata glTF extension. Types: `AnchorPointDirect`, `AnchorPointIndirect`, `CorrelationGroup`, `GltfGpmLocal`, `Spdcf`. Parsed automatically when loading a glTF with `NGA_gpm_local` -- the API is experimental and subject to change.

---

## Performance Tips

1. **Use `.glb` over `.gltf`** -- binary format avoids extra HTTP requests and is smaller on the wire.
2. **Enable Draco compression** (`KHR_draco_mesh_compression`) for 80-90% smaller meshes.
3. **Use KTX2/Basis textures** (`KHR_texture_basisu`) for GPU-compressed textures; keep dimensions power-of-two.
4. **Set `minimumPixelSize` carefully** -- large values force enlargement of distant models, increasing draw cost.
5. **Limit silhouettes** -- extra rendering pass per silhouetted model; more than 256 may cause stencil artifacts.
6. **Reuse scratch `Matrix4` objects** -- avoid allocating every frame when syncing particle systems to moving entities.
7. **Keep emission rates low** -- each particle is a billboard; rates above 200/s can hurt frame rate. Use bursts for short effects.
8. **Prefer pixel-sized particles** (`sizeInMeters: false`, default) -- meter-sized particles are expensive at close range.
9. **Set finite `lifetime`** on particle systems -- `Number.MAX_VALUE` (default) prevents pool cleanup.
10. **Disable picking for decorations** -- `allowPicking: false` saves GPU memory on models that need no interaction.
11. **Destroy when done** -- `viewer.scene.primitives.remove(model)` then `model.destroy()` to free WebGL resources.

---

## See Also

- **cesiumjs-custom-shader** -- GLSL authoring for `Model.customShader` (struct reference, feature IDs, metadata, vertex displacement)
- **cesiumjs-materials-shaders** -- ImageBasedLighting, post-processing stages for models
- **cesiumjs-entities** -- Entity API ModelGraphics, data sources, time-dynamic properties
- **cesiumjs-3d-tiles** -- Cesium3DTileset (uses Model internally), clipping, styling
