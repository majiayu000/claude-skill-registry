---
name: threejs-interaction
description: Three.js interaction - raycasting, controls, mouse/touch input, object selection. Use when handling user input, implementing click detection, adding camera controls, or creating interactive 3D experiences.
---

# Three.js Interaction

## Raycasting

```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(clickableObjects);

  if (intersects.length > 0) {
    const { object, point, face, uv } = intersects[0];
    console.log("Clicked:", object.name, "at", point);
  }
}

window.addEventListener("click", onClick);
```

## Touch Support

```javascript
function onTouchStart(event) {
  if (event.touches.length === 1) {
    const touch = event.touches[0];
    mouse.x = (touch.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(touch.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(clickableObjects);
    // Handle intersects...
  }
}
```

## OrbitControls

```javascript
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI / 2;
controls.autoRotate = true;

function animate() {
  controls.update(); // Required for damping
}
```

## Other Controls

```javascript
// Fly controls
import { FlyControls } from "three/examples/jsm/controls/FlyControls.js";
const controls = new FlyControls(camera, renderer.domElement);
controls.movementSpeed = 10;
controls.update(clock.getDelta());

// Pointer lock (FPS)
import { PointerLockControls } from "three/examples/jsm/controls/PointerLockControls.js";
const controls = new PointerLockControls(camera, document.body);
document.addEventListener("click", () => controls.lock());
```

## TransformControls

```javascript
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";

const transformControls = new TransformControls(camera, renderer.domElement);
scene.add(transformControls);

transformControls.attach(selectedMesh);
transformControls.setMode("translate"); // "rotate", "scale"

transformControls.addEventListener("dragging-changed", (event) => {
  orbitControls.enabled = !event.value;
});
```

## Hover Effects

```javascript
let hoveredObject = null;

function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(hoverableObjects);

  if (hoveredObject) {
    hoveredObject.material.emissive.set(0x000000);
  }

  if (intersects.length > 0) {
    hoveredObject = intersects[0].object;
    hoveredObject.material.emissive.set(0x333333);
    document.body.style.cursor = "pointer";
  } else {
    hoveredObject = null;
    document.body.style.cursor = "default";
  }
}
```

## World-Screen Conversion

```javascript
// World to screen
function worldToScreen(position, camera) {
  const vector = position.clone().project(camera);
  return {
    x: ((vector.x + 1) / 2) * window.innerWidth,
    y: (-(vector.y - 1) / 2) * window.innerHeight,
  };
}

// Screen to world (on plane)
function screenToWorld(screenX, screenY, camera, targetZ = 0) {
  const vector = new THREE.Vector3(
    (screenX / window.innerWidth) * 2 - 1,
    -(screenY / window.innerHeight) * 2 + 1,
    0.5
  ).unproject(camera);

  const dir = vector.sub(camera.position).normalize();
  const distance = (targetZ - camera.position.z) / dir.z;
  return camera.position.clone().add(dir.multiplyScalar(distance));
}
```
