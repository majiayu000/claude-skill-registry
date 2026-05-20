---
name: threejs-impl-xr
description: >
  Use when building VR or AR experiences with Three.js using WebXR.
  Prevents the common mistake of using requestAnimationFrame instead
  of setAnimationLoop, not handling controller events, or wrong
  reference space. Covers WebXRManager, VRButton, ARButton, controllers,
  hand tracking, hit testing, teleportation.
  Keywords: VR, AR, XR, WebXR, VRButton, ARButton, immersive,
  controller, hand tracking, hit test, teleportation, headset.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-xr

## Quick Reference

### WebXRManager Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | `boolean` | `false` | Enable XR rendering |
| `isPresenting` | `boolean` | read-only | Whether an XR session is active |
| `cameraAutoUpdate` | `boolean` | `true` | Auto-update camera from XR device pose |

### WebXRManager Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `getSession()` | `() => XRSession \| null` | Current XR session |
| `setSessionInit(options)` | `(XRSessionInit) => void` | Configure session features before entry |
| `setReferenceSpaceType(type)` | `(string) => void` | Set reference space type |
| `getController(index)` | `(number) => Group` | Get controller target ray space |
| `getControllerGrip(index)` | `(number) => Group` | Get controller grip space |
| `getHand(index)` | `(number) => Group` | Get hand tracking group |
| `setFoveation(level)` | `(number) => void` | Set foveated rendering (0.0–1.0) |
| `getFoveation()` | `() => number` | Get current foveation level |
| `getEnvironmentBlendMode()` | `() => string` | Get blend mode (opaque, additive, alpha-blend) |
| `setFramebufferScaleFactor(scale)` | `(number) => void` | Adjust XR render resolution |

### Session Types

| Type | Use Case |
|------|----------|
| `'immersive-vr'` | Full VR headset experience |
| `'immersive-ar'` | AR passthrough on headset or phone |
| `'inline'` | Non-immersive XR in a browser window |

### Reference Space Types

| Type | Origin | Use Case |
|------|--------|----------|
| `'viewer'` | Head position | HUD elements, gaze-locked UI |
| `'local'` | Initial head position | Seated experiences |
| `'local-floor'` | Floor level at start | Standing VR, ALWAYS preferred for room-scale |
| `'bounded-floor'` | Floor with boundary | Room-scale with guardian |
| `'unbounded'` | World origin | Large-scale AR experiences |

### XR Addon Classes

| Class | Import Path | Purpose |
|-------|-------------|---------|
| `VRButton` | `three/addons/webxr/VRButton.js` | Creates "Enter VR" button with feature detection |
| `ARButton` | `three/addons/webxr/ARButton.js` | Creates "Enter AR" button with feature detection |
| `XRControllerModelFactory` | `three/addons/webxr/XRControllerModelFactory.js` | Loads appropriate controller 3D model |
| `XRHandModelFactory` | `three/addons/webxr/XRHandModelFactory.js` | Creates hand tracking visualization |
| `XRHandPrimitiveModel` | `three/addons/webxr/XRHandPrimitiveModel.js` | Simple geometric hand representation |
| `XREstimatedLight` | `three/addons/webxr/XREstimatedLight.js` | AR environment lighting estimation |
| `XRPlanes` | `three/addons/webxr/XRPlanes.js` | AR plane detection visualization |

### Critical Warnings

**NEVER** use `requestAnimationFrame()` for XR rendering — ALWAYS use `renderer.setAnimationLoop()`. The WebXR API requires its own frame timing; `requestAnimationFrame` stops firing when an XR session is active.

**NEVER** apply heavy post-processing in VR — each effect runs TWICE (once per eye), doubling GPU cost. Dropped frames cause motion sickness.

**ALWAYS** target 72fps (Quest) or 90fps (PC VR) — dropped frames cause nausea and discomfort. There is NO acceptable lower target.

**ALWAYS** set `renderer.xr.enabled = true` BEFORE creating VRButton/ARButton — the button checks this property for feature detection.

**NEVER** forget to add controllers to the scene — `getController()` returns a `Group` that MUST be added via `scene.add()` or it will not render or fire events.

---

## VR Setup

### Minimal VR Scene

```javascript
import * as THREE from 'three';
import { VRButton } from 'three/addons/webxr/VRButton.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 100);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// Enable XR BEFORE creating VRButton
renderer.xr.enabled = true;
renderer.xr.setReferenceSpaceType('local-floor');
document.body.appendChild(VRButton.createButton(renderer));

// MUST use setAnimationLoop — NEVER requestAnimationFrame
renderer.setAnimationLoop((time, frame) => {
  renderer.render(scene, camera);
});
```

### AR Setup

```javascript
import * as THREE from 'three';
import { ARButton } from 'three/addons/webxr/ARButton.js';

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.xr.enabled = true;

// Configure AR features BEFORE creating ARButton
renderer.xr.setSessionInit({
  requiredFeatures: ['hit-test'],
  optionalFeatures: ['dom-overlay'],
  domOverlay: { root: document.getElementById('overlay') }
});

document.body.appendChild(ARButton.createButton(renderer, {
  requiredFeatures: ['hit-test']
}));

renderer.setAnimationLoop((time, frame) => {
  renderer.render(scene, camera);
});
```

---

## Controllers

### Controller Spaces

Three.js exposes THREE distinct spaces per physical controller:

| Method | Space | Use Case |
|--------|-------|----------|
| `getController(index)` | Target ray | Pointing direction, laser pointer |
| `getControllerGrip(index)` | Grip | Where the hand holds the controller |
| `getHand(index)` | Hand | Full hand tracking skeleton |

ALWAYS add ALL spaces you use to the scene. Each returns a `THREE.Group`.

### Controller Events

| Event | Trigger |
|-------|---------|
| `selectstart` | Primary trigger pressed |
| `selectend` | Primary trigger released |
| `select` | Primary trigger press-and-release |
| `squeezestart` | Grip button pressed |
| `squeezeend` | Grip button released |
| `squeeze` | Grip button press-and-release |
| `connected` | Controller detected (event.data = XRInputSource) |
| `disconnected` | Controller lost |

### Controller Models

```javascript
import { XRControllerModelFactory } from 'three/addons/webxr/XRControllerModelFactory.js';

const factory = new XRControllerModelFactory();

// Target ray space — for laser pointer / interaction ray
const controller0 = renderer.xr.getController(0);
controller0.addEventListener('selectstart', onSelectStart);
controller0.addEventListener('selectend', onSelectEnd);
scene.add(controller0);

// Grip space — for rendering the controller model
const grip0 = renderer.xr.getControllerGrip(0);
grip0.add(factory.createControllerModel(grip0));
scene.add(grip0);
```

### Laser Pointer Visual

```javascript
const geometry = new THREE.BufferGeometry().setFromPoints([
  new THREE.Vector3(0, 0, 0),
  new THREE.Vector3(0, 0, -5)
]);
const material = new THREE.LineBasicMaterial({ color: 0xffffff });
const line = new THREE.Line(geometry, material);
controller0.add(line);
```

---

## Hand Tracking

```javascript
import { XRHandModelFactory } from 'three/addons/webxr/XRHandModelFactory.js';

// Request hand-tracking feature
renderer.xr.setSessionInit({
  optionalFeatures: ['hand-tracking']
});

const handFactory = new XRHandModelFactory();

const hand0 = renderer.xr.getHand(0);
hand0.add(handFactory.createHandModel(hand0, 'mesh'));
scene.add(hand0);

const hand1 = renderer.xr.getHand(1);
hand1.add(handFactory.createHandModel(hand1, 'mesh'));
scene.add(hand1);
```

**Hand model profiles:** `'mesh'` (realistic), `'spheres'` (joint spheres), `'boxes'` (joint boxes).

Hand tracking events fire on the hand group:
- `connected` — hand detected
- `disconnected` — hand lost
- `pinchstart` / `pinchend` — thumb-index pinch gesture

---

## AR Hit Testing

Hit testing places virtual objects on real-world surfaces.

```javascript
let hitTestSource = null;
let hitTestSourceRequested = false;
const reticle = new THREE.Mesh(
  new THREE.RingGeometry(0.15, 0.2, 32).rotateX(-Math.PI / 2),
  new THREE.MeshBasicMaterial()
);
reticle.matrixAutoUpdate = false;
reticle.visible = false;
scene.add(reticle);

renderer.setAnimationLoop((time, frame) => {
  if (frame) {
    const session = renderer.xr.getSession();
    const referenceSpace = renderer.xr.getReferenceSpace();

    if (!hitTestSourceRequested) {
      session.requestReferenceSpace('viewer').then((viewerSpace) => {
        session.requestHitTestSource({ space: viewerSpace }).then((source) => {
          hitTestSource = source;
        });
      });
      hitTestSourceRequested = true;
    }

    if (hitTestSource) {
      const results = frame.getHitTestResults(hitTestSource);
      if (results.length > 0) {
        const pose = results[0].getPose(referenceSpace);
        reticle.visible = true;
        reticle.matrix.fromArray(pose.transform.matrix);
      } else {
        reticle.visible = false;
      }
    }
  }
  renderer.render(scene, camera);
});
```

---

## Teleportation Pattern

```javascript
const tempMatrix = new THREE.Matrix4();
const raycaster = new THREE.Raycaster();
const marker = new THREE.Mesh(
  new THREE.CircleGeometry(0.25, 32).rotateX(-Math.PI / 2),
  new THREE.MeshBasicMaterial({ color: 0x00ff00 })
);
scene.add(marker);

const controller = renderer.xr.getController(0);
controller.addEventListener('selectend', () => {
  tempMatrix.identity().extractRotation(controller.matrixWorld);
  raycaster.ray.origin.setFromMatrixPosition(controller.matrixWorld);
  raycaster.ray.direction.set(0, 0, -1).applyMatrix4(tempMatrix);

  const intersects = raycaster.intersectObject(floor);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    // Move the XR camera rig, NOT the camera directly
    cameraRig.position.set(point.x, 0, point.z);
  }
});
scene.add(controller);
```

**ALWAYS** move a camera rig group (containing the camera), NEVER the camera directly — the WebXR API controls camera position relative to its parent.

---

## VR Performance

### Target Frame Rates

| Platform | Target FPS | Notes |
|----------|-----------|-------|
| Meta Quest 2/3 | 72–120 fps | 72 default, 90/120 optional |
| PC VR (SteamVR) | 90 fps | Standard target |
| PSVR2 | 90–120 fps | Platform-dependent |

### Optimization Techniques

1. **Foveated rendering** — `renderer.xr.setFoveation(1.0)` for maximum performance. Range 0.0 (none) to 1.0 (maximum).
2. **Framebuffer scale** — `renderer.xr.setFramebufferScaleFactor(0.75)` to reduce resolution when GPU-bound.
3. **Minimize draw calls** — Use `THREE.InstancedMesh` for repeated objects. Target < 100 draw calls.
4. **Avoid post-processing** — Each effect renders TWICE in stereo. Remove bloom, SSAO, and anti-aliasing passes when possible.
5. **Use baked lighting** — Real-time shadows are expensive at 2x. Pre-bake where possible.
6. **LOD (Level of Detail)** — Use `THREE.LOD` to reduce polygon count for distant objects.
7. **Texture compression** — Use KTX2/Basis textures to reduce GPU memory.

### Camera Rig Pattern

ALWAYS use a camera rig group for VR locomotion:

```javascript
const cameraRig = new THREE.Group();
cameraRig.add(camera);
scene.add(cameraRig);

// Move the rig, not the camera
cameraRig.position.set(0, 0, 5);
```

The WebXR API sets camera position/rotation each frame relative to its parent. Moving the camera directly is overwritten immediately.

---

## XR Estimated Light (AR)

```javascript
import { XREstimatedLight } from 'three/addons/webxr/XREstimatedLight.js';

const xrLight = new XREstimatedLight(renderer);
xrLight.addEventListener('estimationstart', () => {
  scene.add(xrLight);
  scene.environment = xrLight.environment;
  // Remove default lights
});
xrLight.addEventListener('estimationend', () => {
  scene.remove(xrLight);
  scene.environment = null;
  // Restore default lights
});
```

---

## Reference Links

- [references/methods.md](references/methods.md) — Complete API signatures for WebXRManager and XR addon classes
- [references/examples.md](references/examples.md) — Working code examples for VR, AR, controllers, and hand tracking
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do in WebXR development

### Official Sources

- https://threejs.org/docs/#api/en/renderers/webxr/WebXRManager
- https://threejs.org/docs/#manual/en/introduction/How-to-create-VR-content
- https://immersiveweb.dev/
- https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API
