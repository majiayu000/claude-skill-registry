---
name: threejs-impl-physics
description: >
  Use when adding physics simulation to a Three.js scene: rigid bodies,
  collisions, constraints, or raycasting. Prevents the common mistake
  of wrong Vec3/Vector3 conversion, missing world.step(), or choosing
  the wrong engine. Covers cannon-es and Rapier with Three.js sync
  patterns, performance comparison.
  Keywords: physics, cannon-es, Rapier, rigid body, collider, collision,
  gravity, simulation, WASM, constraint, joint.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-physics

## Quick Reference

### Engine Selection Decision Tree

| Criterion | cannon-es | Rapier |
|-----------|-----------|--------|
| Scene size | < 100 bodies | 100–10,000+ bodies |
| Determinism needed | No | Yes (cross-platform) |
| CCD (fast objects) | Limited | Full support |
| Bundle size budget | ~100 KB | ~300–600 KB (WASM) |
| Initialization | Synchronous | Async (MUST `await init()`) |
| Prototyping speed | Faster (simpler API) | Slower (builder pattern) |
| R3F integration | `@react-three/cannon` | `@react-three/rapier` |

**Rule:** ALWAYS use Rapier for production applications requiring determinism, CCD, or > 100 bodies. Use cannon-es for prototyping and simple scenes.

### Critical Warnings

**NEVER** forget to call `world.step()` in the animation loop — physics bodies will NOT move without it.

**NEVER** use `mesh.position.copy(body.position)` with Rapier — Rapier returns plain `{x, y, z}` objects, NOT `CANNON.Vec3`. ALWAYS use `mesh.position.set(pos.x, pos.y, pos.z)`.

**NEVER** use Rapier APIs before `await RAPIER.init()` completes — ALL Rapier classes are undefined until WASM loads.

**NEVER** use `Trimesh` / `trimesh` colliders on dynamic bodies — triangle meshes are STATIC only in both engines. Use `ConvexPolyhedron` / `convexHull` for dynamic concave geometry.

**NEVER** create physics bodies without corresponding Three.js meshes unless intentionally creating invisible colliders — orphaned bodies waste simulation budget.

---

## cannon-es

### World Setup

```js
import * as CANNON from 'cannon-es';

const world = new CANNON.World();
world.gravity.set(0, -9.82, 0);
world.broadphase = new CANNON.SAPBroadphase(world);
world.solver.iterations = 10;
world.allowSleep = true;
```

ALWAYS set `world.allowSleep = true` — sleeping bodies skip simulation and dramatically improve performance.

ALWAYS use `SAPBroadphase` for scenes with > 20 bodies. `NaiveBroadphase` is O(n^2).

### Body Types

| Type | Mass | Behavior |
|------|------|----------|
| `CANNON.Body.DYNAMIC` | > 0 | Affected by forces and collisions |
| `CANNON.Body.STATIC` | 0 | Immovable, infinite mass |
| `CANNON.Body.KINEMATIC` | 0 | Moved programmatically, pushes dynamic bodies |

```js
const body = new CANNON.Body({
  mass: 5,
  position: new CANNON.Vec3(0, 10, 0),
  shape: new CANNON.Box(new CANNON.Vec3(1, 1, 1)), // half-extents
  linearDamping: 0.01,
  angularDamping: 0.01,
});
world.addBody(body);
```

### Shape Types

| Shape | Constructor | Notes |
|-------|------------|-------|
| `Box` | `new CANNON.Box(halfExtents: Vec3)` | Axis-aligned box |
| `Sphere` | `new CANNON.Sphere(radius)` | Cheapest collision shape |
| `Cylinder` | `new CANNON.Cylinder(rTop, rBottom, height, segments)` | Cylinder |
| `Plane` | `new CANNON.Plane()` | Infinite ground plane |
| `ConvexPolyhedron` | `new CANNON.ConvexPolyhedron({vertices, faces})` | Custom convex hull |
| `Trimesh` | `new CANNON.Trimesh(vertices, indices)` | STATIC only |
| `Heightfield` | `new CANNON.Heightfield(data, {elementSize})` | Terrain |
| `Particle` | `new CANNON.Particle()` | Point particle |

### Materials and Contacts

```js
const groundMat = new CANNON.Material('ground');
const ballMat = new CANNON.Material('ball');
const contact = new CANNON.ContactMaterial(groundMat, ballMat, {
  friction: 0.4,
  restitution: 0.6,
});
world.addContactMaterial(contact);

// Assign materials to bodies
groundBody.material = groundMat;
ballBody.material = ballMat;
```

ALWAYS assign materials to bodies after creating ContactMaterial — without assignment, the ContactMaterial has NO effect.

### Constraints

| Constraint | Constructor | Use Case |
|-----------|------------|----------|
| `PointToPointConstraint` | `(bodyA, pivotA, bodyB, pivotB)` | Ball joint |
| `DistanceConstraint` | `(bodyA, bodyB, distance)` | Fixed distance rod |
| `HingeConstraint` | `(bodyA, bodyB, {pivotA, axisA, pivotB, axisB})` | Door hinge |
| `LockConstraint` | `(bodyA, bodyB)` | Rigid lock |
| `ConeTwistConstraint` | `(bodyA, bodyB, options)` | Ragdoll joints |
| `Spring` | `(bodyA, bodyB, options)` | Damped spring |

```js
const hinge = new CANNON.HingeConstraint(bodyA, bodyB, {
  pivotA: new CANNON.Vec3(0, 0, 0),
  axisA: new CANNON.Vec3(0, 1, 0),
  pivotB: new CANNON.Vec3(-2, 0, 0),
  axisB: new CANNON.Vec3(0, 1, 0),
});
world.addConstraint(hinge);
```

### Events

```js
body.addEventListener('collide', (event) => {
  const { contact } = event;
  // contact.ni = contact normal
  // contact.ri = contact point relative to bodyA
  // contact.rj = contact point relative to bodyB
});
body.addEventListener('sleep', () => { /* body went to sleep */ });
body.addEventListener('wakeup', () => { /* body woke up */ });
```

### Stepping

```js
// ALWAYS use three-argument step for deterministic simulation
const fixedTimeStep = 1 / 60;
const maxSubSteps = 3;

function animate() {
  const delta = clock.getDelta();
  world.step(fixedTimeStep, delta, maxSubSteps);
}
```

---

## Rapier

### WASM Initialization

```js
import RAPIER from '@dimforge/rapier3d-compat';

await RAPIER.init(); // MUST await — ALL APIs undefined before this resolves

const gravity = { x: 0.0, y: -9.81, z: 0.0 };
const world = new RAPIER.World(gravity);
```

ALWAYS wrap Rapier usage in an async function or top-level await. Calling ANY Rapier constructor before `init()` resolves throws a runtime error.

### RigidBody Creation (Builder Pattern)

```js
// Dynamic body
const bodyDesc = RAPIER.RigidBodyDesc.dynamic()
  .setTranslation(0, 10, 0)
  .setLinvel(0, 0, 0)
  .setAngvel({ x: 0, y: 0, z: 0 })
  .setLinearDamping(0.01)
  .setAngularDamping(0.01)
  .setCcdEnabled(true);
const rigidBody = world.createRigidBody(bodyDesc);

// Static body
const staticDesc = RAPIER.RigidBodyDesc.fixed().setTranslation(0, 0, 0);
const staticBody = world.createRigidBody(staticDesc);

// Kinematic (position-based)
const kinDesc = RAPIER.RigidBodyDesc.kinematicPositionBased();
const kinBody = world.createRigidBody(kinDesc);

// Kinematic (velocity-based)
const kinVelDesc = RAPIER.RigidBodyDesc.kinematicVelocityBased();
```

### Collider Shapes

```js
const colliderDesc = RAPIER.ColliderDesc.cuboid(1, 1, 1)
  .setRestitution(0.5)
  .setFriction(0.7);
world.createCollider(colliderDesc, rigidBody);
```

| Shape | Constructor | Notes |
|-------|------------|-------|
| `ColliderDesc.cuboid(hx, hy, hz)` | Box half-extents | Most common |
| `ColliderDesc.ball(radius)` | Sphere | Cheapest shape |
| `ColliderDesc.capsule(halfHeight, radius)` | Capsule | Good for characters |
| `ColliderDesc.cylinder(halfHeight, radius)` | Cylinder | |
| `ColliderDesc.cone(halfHeight, radius)` | Cone | |
| `ColliderDesc.convexHull(vertices)` | Convex hull | From Float32Array |
| `ColliderDesc.trimesh(vertices, indices)` | Triangle mesh | STATIC only |
| `ColliderDesc.heightfield(nrows, ncols, heights, scale)` | Terrain | |
| `ColliderDesc.roundCuboid(hx, hy, hz, borderRadius)` | Rounded box | |

### Ray Casting

```js
const ray = new RAPIER.Ray({ x: 0, y: 10, z: 0 }, { x: 0, y: -1, z: 0 });
const hit = world.castRay(ray, 100, true);
if (hit) {
  const hitPoint = ray.pointAt(hit.timeOfImpact);
  const hitCollider = world.getCollider(hit.colliderHandle);
}
```

### CCD (Continuous Collision Detection)

ALWAYS enable CCD on fast-moving bodies to prevent tunneling through thin geometry:

```js
const desc = RAPIER.RigidBodyDesc.dynamic().setCcdEnabled(true);
```

### Collision Events

```js
const eventQueue = new RAPIER.EventQueue(true);
world.step(eventQueue);

eventQueue.drainCollisionEvents((handle1, handle2, started) => {
  // started === true: collision began
  // started === false: collision ended
});

eventQueue.drainContactForceEvents((event) => {
  const force = event.totalForceMagnitude();
});
```

### Debug Rendering

```js
const { vertices, colors } = world.debugRender();
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 4));
const material = new THREE.LineBasicMaterial({ vertexColors: true });
const lines = new THREE.LineSegments(geometry, material);
scene.add(lines);
```

---

## Three.js Sync Pattern

### cannon-es Sync

```js
// Store body-mesh pairs
const pairs = [];

function addPhysicsObject(mesh, body) {
  scene.add(mesh);
  world.addBody(body);
  pairs.push({ mesh, body });
}

function updatePhysics(delta) {
  world.step(1 / 60, delta, 3);
  for (const { mesh, body } of pairs) {
    mesh.position.copy(body.position);       // Vec3 → Vector3 (compatible)
    mesh.quaternion.copy(body.quaternion);    // Quaternion → Quaternion (compatible)
  }
}
```

cannon-es `Vec3` and `Quaternion` are directly compatible with Three.js `.copy()`.

### Rapier Sync

```js
const pairs = [];

function addPhysicsObject(mesh, rigidBody) {
  scene.add(mesh);
  pairs.push({ mesh, rigidBody });
}

function updatePhysics() {
  world.step();
  for (const { mesh, rigidBody } of pairs) {
    const pos = rigidBody.translation();   // returns {x, y, z}
    const rot = rigidBody.rotation();      // returns {x, y, z, w}
    mesh.position.set(pos.x, pos.y, pos.z);
    mesh.quaternion.set(rot.x, rot.y, rot.z, rot.w);
  }
}
```

NEVER use `.copy()` with Rapier return values — they are plain objects, NOT Three.js types.

---

## React Three Fiber Integration

### @react-three/rapier

```jsx
import { Physics, RigidBody } from '@react-three/rapier';

function Scene() {
  return (
    <Physics gravity={[0, -9.81, 0]}>
      <RigidBody type="fixed">
        <mesh position={[0, -1, 0]}>
          <boxGeometry args={[20, 1, 20]} />
          <meshStandardMaterial />
        </mesh>
      </RigidBody>
      <RigidBody>
        <mesh position={[0, 5, 0]}>
          <sphereGeometry args={[1]} />
          <meshStandardMaterial />
        </mesh>
      </RigidBody>
    </Physics>
  );
}
```

### @react-three/cannon

```jsx
import { Physics, useBox, useSphere } from '@react-three/cannon';

function Floor() {
  const [ref] = useBox(() => ({ mass: 0, args: [20, 1, 20], position: [0, -1, 0] }));
  return (
    <mesh ref={ref}>
      <boxGeometry args={[20, 1, 20]} />
      <meshStandardMaterial />
    </mesh>
  );
}
```

---

## Performance Comparison

| Feature | cannon-es | Rapier |
|---------|-----------|--------|
| Language | JavaScript | Rust compiled to WASM |
| Real-time bodies | ~1,000 | ~10,000+ |
| Bundle size | ~100 KB | ~300–600 KB |
| CCD | Limited | Full support |
| Deterministic | No | Yes (cross-platform) |
| Debug rendering | Manual | Built-in `world.debugRender()` |
| API style | Constructor-based | Builder pattern |

---

## Reference Links

- [references/methods.md](references/methods.md) — API signatures for cannon-es and Rapier
- [references/examples.md](references/examples.md) — Working integration examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common physics mistakes and fixes

### Official Sources

- https://pmndrs.github.io/cannon-es/docs/
- https://rapier.rs/docs/user_guides/javascript/getting_started
- https://github.com/pmndrs/react-three-rapier
- https://github.com/pmndrs/use-cannon
