---
name: threejs-syntax-controls
description: >
  Use when adding camera controls to a Three.js scene: orbit, pan, zoom,
  fly, first-person, or object manipulation. Prevents the common mistake
  of forgetting controls.update() in the render loop, not calling
  dispose(), or mixing controls. Covers OrbitControls, MapControls,
  FlyControls, PointerLockControls, TransformControls.
  Keywords: OrbitControls, controls, camera controls, orbit, pan, zoom,
  MapControls, FlyControls, PointerLockControls, TransformControls.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-syntax-controls

## Quick Reference

### Control Selection Decision Tree

| Use Case | Control | Why |
|----------|---------|-----|
| Inspect a 3D model from all angles | OrbitControls | Orbit/pan/zoom around a target point |
| Top-down map or 2D-style navigation | MapControls | Left-drag pans, right-drag rotates |
| Free-flight editor or space scene | FlyControls | Six degrees of freedom, WASD + mouse |
| First-person game with pointer lock | PointerLockControls | Hides cursor, captures mouse movement |
| First-person without pointer lock | FirstPersonControls | Mouse-look without browser lock API |
| Move/rotate/scale objects via gizmo | TransformControls | Interactive translate/rotate/scale handles |
| Drag objects along a plane | DragControls | Click-and-drag object repositioning |
| Unconstrained rotation (no gimbal lock) | ArcballControls | Full spherical rotation with animation |
| Unconstrained rotation (simpler) | TrackballControls | Like OrbitControls but no pole constraint |

### Import Paths (Three.js r160+)

```javascript
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { MapControls } from 'three/addons/controls/MapControls.js';
import { FlyControls } from 'three/addons/controls/FlyControls.js';
import { FirstPersonControls } from 'three/addons/controls/FirstPersonControls.js';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';
import { TrackballControls } from 'three/addons/controls/TrackballControls.js';
import { ArcballControls } from 'three/addons/controls/ArcballControls.js';
import { DragControls } from 'three/addons/controls/DragControls.js';
```

**ALWAYS** use `'three/addons/controls/...'` for r160+. The legacy path `'three/examples/jsm/controls/...'` still works but is deprecated.

### Critical Warnings

**ALWAYS** call `controls.update()` in the animation loop when `enableDamping` or `autoRotate` is `true`. Failing to do so causes the camera to freeze after user interaction ends.

**ALWAYS** call `controls.dispose()` when removing controls. Failing to do so leaks DOM event listeners (pointermove, wheel, keydown) that cause memory leaks and ghost interactions.

**NEVER** attach two camera-control classes to the same camera simultaneously without disabling one. OrbitControls + FlyControls on the same camera causes erratic movement.

**ALWAYS** disable OrbitControls while TransformControls is dragging. Listen to the `dragging-changed` event and toggle `orbitControls.enabled`.

**ALWAYS** call `PointerLockControls.lock()` from a user gesture (click handler). Browsers reject pointer lock requests without user interaction.

**ALWAYS** pass `delta` time to `FlyControls.update(delta)`. Passing no argument or passing elapsed time causes speed to depend on frame rate.

---

## Controls Lifecycle

Every control follows the same lifecycle pattern:

```
construct --> configure --> attach to loop --> dispose on cleanup
```

### Step 1: Construct

```javascript
const controls = new OrbitControls(camera, renderer.domElement);
```

**ALWAYS** pass `renderer.domElement` as the second argument. Passing `document` or `document.body` causes controls to capture events globally, breaking UI overlays.

### Step 2: Configure

```javascript
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 50;
controls.target.set(0, 1, 0);
```

### Step 3: Update in Render Loop

```javascript
function animate() {
  requestAnimationFrame(animate);
  controls.update(); // REQUIRED when enableDamping or autoRotate is true
  renderer.render(scene, camera);
}
animate();
```

### Step 4: Dispose on Cleanup

```javascript
controls.dispose();
```

---

## OrbitControls

The most commonly used control. Orbits, pans, and zooms around a target point.

### Constructor

```javascript
new OrbitControls(camera: THREE.Camera, domElement: HTMLElement)
```

### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | `boolean` | `true` | Enable/disable all interaction |
| `target` | `Vector3` | `(0,0,0)` | Orbit focus point |
| `enableDamping` | `boolean` | `false` | Smooth inertial movement |
| `dampingFactor` | `number` | `0.05` | Inertia strength (0-1) |
| `autoRotate` | `boolean` | `false` | Auto-rotate around target |
| `autoRotateSpeed` | `number` | `2.0` | Degrees/sec at 60fps |
| `enablePan` | `boolean` | `true` | Allow panning |
| `enableRotate` | `boolean` | `true` | Allow rotation |
| `enableZoom` | `boolean` | `true` | Allow zooming |
| `minDistance` | `number` | `0` | Min zoom distance (PerspectiveCamera) |
| `maxDistance` | `number` | `Infinity` | Max zoom distance (PerspectiveCamera) |
| `minZoom` | `number` | `0` | Min zoom (OrthographicCamera) |
| `maxZoom` | `number` | `Infinity` | Max zoom (OrthographicCamera) |
| `minPolarAngle` | `number` | `0` | Min vertical angle (radians) |
| `maxPolarAngle` | `number` | `Math.PI` | Max vertical angle (radians) |
| `minAzimuthAngle` | `number` | `-Infinity` | Min horizontal angle (radians) |
| `maxAzimuthAngle` | `number` | `Infinity` | Max horizontal angle (radians) |
| `screenSpacePanning` | `boolean` | `true` | Pan in screen plane (true) or horizontal plane (false) |
| `zoomToCursor` | `boolean` | `false` | Zoom towards cursor position |
| `panSpeed` | `number` | `1.0` | Pan speed multiplier |
| `rotateSpeed` | `number` | `1.0` | Rotation speed multiplier |
| `zoomSpeed` | `number` | `1.0` | Zoom speed multiplier |
| `mouseButtons` | `object` | `{LEFT: ROTATE, MIDDLE: DOLLY, RIGHT: PAN}` | Mouse button mapping |
| `touches` | `object` | `{ONE: ROTATE, TWO: DOLLY_PAN}` | Touch gesture mapping |
| `keys` | `object` | `{LEFT, UP, RIGHT, BOTTOM}` | Arrow key codes for panning |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `update(deltaTime?)` | `(number?) => boolean` | Update controls state. MUST call every frame with damping/autoRotate |
| `dispose()` | `() => void` | Remove all event listeners |
| `saveState()` | `() => void` | Save current camera position/target/zoom |
| `reset()` | `() => void` | Restore to last saved state |
| `getDistance()` | `() => number` | Distance from camera to target |
| `getPolarAngle()` | `() => number` | Vertical angle in radians |
| `getAzimuthalAngle()` | `() => number` | Horizontal angle in radians |
| `listenToKeyEvents(el)` | `(HTMLElement) => void` | Enable keyboard panning |
| `stopListenToKeyEvents()` | `() => void` | Disable keyboard panning |

### Events

| Event | Trigger |
|-------|---------|
| `change` | Camera position or target changed |
| `start` | User interaction began (pointerdown) |
| `end` | User interaction ended (pointerup) |

---

## MapControls

Subclass of OrbitControls optimized for top-down map navigation.

| Button | OrbitControls | MapControls |
|--------|--------------|-------------|
| Left mouse | Rotate | Pan |
| Middle mouse | Dolly | Dolly |
| Right mouse | Pan | Rotate |

All properties, methods, and events are identical to OrbitControls. The ONLY differences are the default `mouseButtons` mapping and `screenSpacePanning` defaulting to `true`.

---

## FlyControls

Six-degrees-of-freedom flight camera. WASD for movement, QE for roll, RF for up/down.

### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `movementSpeed` | `number` | `1.0` | Translation speed |
| `rollSpeed` | `number` | `0.005` | Roll rotation speed |
| `dragToLook` | `boolean` | `false` | Require mouse drag to rotate (vs. always follow mouse) |
| `autoForward` | `boolean` | `false` | Move forward automatically |

### Methods

- `update(delta)` -- **ALWAYS** pass `delta` time from the clock. NEVER omit this argument.
- `dispose()` -- Remove event listeners.

---

## PointerLockControls

First-person camera using the Pointer Lock API. Hides and captures the mouse cursor.

### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `isLocked` | `boolean` | read-only | Whether pointer is currently locked |
| `maxPolarAngle` | `number` | `Math.PI` | Max vertical look angle |
| `minPolarAngle` | `number` | `0` | Min vertical look angle |
| `pointerSpeed` | `number` | `1.0` | Mouse sensitivity multiplier |

### Methods

| Method | Description |
|--------|-------------|
| `lock()` | Request pointer lock (MUST call from user gesture) |
| `unlock()` | Exit pointer lock |
| `connect()` | Attach event listeners |
| `disconnect()` | Remove event listeners |
| `dispose()` | Full cleanup (calls disconnect) |
| `getObject()` | Returns the controlled camera |
| `getDirection(target)` | Write look direction into target Vector3 |
| `moveForward(distance)` | Move camera forward |
| `moveRight(distance)` | Move camera sideways |

### Events

| Event | Trigger |
|-------|---------|
| `change` | Camera orientation changed |
| `lock` | Pointer lock acquired |
| `unlock` | Pointer lock released |

**ALWAYS** implement your own WASD movement in the animation loop. PointerLockControls handles look direction only, NOT position.

---

## TransformControls

Interactive gizmo for moving, rotating, and scaling scene objects.

### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `mode` | `string` | `'translate'` | `'translate'`, `'rotate'`, or `'scale'` |
| `space` | `string` | `'world'` | `'world'` or `'local'` coordinate space |
| `showX` | `boolean` | `true` | Show X axis handle |
| `showY` | `boolean` | `true` | Show Y axis handle |
| `showZ` | `boolean` | `true` | Show Z axis handle |
| `size` | `number` | `1` | Gizmo visual scale |
| `translationSnap` | `number|null` | `null` | Snap to grid (units) |
| `rotationSnap` | `number|null` | `null` | Snap rotation (radians) |
| `scaleSnap` | `number|null` | `null` | Snap scale increment |
| `dragging` | `boolean` | read-only | User is currently dragging |

### Methods

| Method | Description |
|--------|-------------|
| `attach(object)` | Attach gizmo to a scene object |
| `detach()` | Remove gizmo from current object |
| `setMode(mode)` | Set transform mode |
| `setSpace(space)` | Set coordinate space |
| `setSize(size)` | Set gizmo scale |
| `setTranslationSnap(snap)` | Set position snap |
| `setRotationSnap(snap)` | Set rotation snap |
| `setScaleSnap(snap)` | Set scale snap |
| `getRaycaster()` | Access internal raycaster |
| `dispose()` | Cleanup |

### Events

| Event | Trigger |
|-------|---------|
| `change` | Gizmo visual changed |
| `dragging-changed` | `event.value` is `true` when dragging starts, `false` when it ends |
| `objectChange` | Attached object's transform was modified |
| `mouseDown` | Pointer pressed on gizmo |
| `mouseUp` | Pointer released from gizmo |

### Critical Integration Pattern

**ALWAYS** disable camera controls during gizmo drag:

```javascript
transformControls.addEventListener('dragging-changed', (event) => {
  orbitControls.enabled = !event.value;
});
```

**ALWAYS** add TransformControls to the scene: `scene.add(transformControls.getHelper())` or `scene.add(transformControls)`.

---

## Brief Overview: Other Controls

### ArcballControls
Unconstrained rotation with animation states. No polar angle limit -- the camera rotates freely in all directions. Best for CAD-style model inspection.

### TrackballControls
Like OrbitControls without the polar angle constraint. The camera can rotate past the poles. Properties: `rotateSpeed`, `zoomSpeed`, `panSpeed`, `staticMoving`, `dynamicDampingFactor`.

### DragControls
Drag scene objects along a plane. Constructor: `new DragControls(objects, camera, domElement)`. Events: `dragstart`, `drag`, `dragend`, `hoveron`, `hoveroff`.

### FirstPersonControls
Mouse-look camera without pointer lock. Properties: `movementSpeed`, `lookSpeed`, `activeLook`, `constrainVertical`, `verticalMin`, `verticalMax`.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Full API signatures for all controls
- [references/examples.md](references/examples.md) -- Working code examples for each control type
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do

### Official Sources

- https://threejs.org/docs/#examples/en/controls/OrbitControls
- https://threejs.org/docs/#examples/en/controls/MapControls
- https://threejs.org/docs/#examples/en/controls/FlyControls
- https://threejs.org/docs/#examples/en/controls/PointerLockControls
- https://threejs.org/docs/#examples/en/controls/TransformControls
