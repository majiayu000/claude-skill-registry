---
name: dev-r3f-r3f-physics
description: Physics integration with Rapier for R3F game development
category: r3f
---

# R3F Physics

> "Physics makes games feel real – Rapier is fast and reliable."

## When to Use This Skill

Use when:
- Adding physics simulation to objects
- Implementing collision detection
- Creating vehicles or character controllers
- Building interactive environments

## Quick Start

```tsx
import { Physics, RigidBody } from '@react-three/rapier';

function PhysicsScene() {
  return (
    <Physics>
      {/* Falling cube */}
      <RigidBody>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial />
        </mesh>
      </RigidBody>

      {/* Static floor */}
      <RigidBody type="fixed">
        <mesh position={[0, -2, 0]}>
          <boxGeometry args={[10, 0.5, 10]} />
          <meshStandardMaterial />
        </mesh>
      </RigidBody>
    </Physics>
  );
}
```

## Decision Framework

| Need               | RigidBody Type      |
| ------------------ | ------------------- |
| Player/Vehicle     | `dynamic`           |
| Ground/Walls       | `fixed`             |
| Platforms (moving) | `kinematicPosition` |
| Triggers           | `fixed` + sensor    |

| Collision Shape | Use For                       |
| --------------- | ----------------------------- |
| `cuboid`        | Boxes, buildings              |
| `ball`          | Spheres, wheels               |
| `capsule`       | Characters                    |
| `convexHull`    | Complex convex shapes         |
| `trimesh`       | Complex concave (static only) |

## Progressive Guide

### Level 1: Basic Physics

```tsx
import { Physics, RigidBody } from '@react-three/rapier';

function BasicPhysics() {
  return (
    <Physics gravity={[0, -9.81, 0]}>
      {/* Dynamic body - affected by physics */}
      <RigidBody position={[0, 5, 0]}>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial color="red" />
        </mesh>
      </RigidBody>

      {/* Fixed body - doesn't move */}
      <RigidBody type="fixed">
        <mesh position={[0, -1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[20, 20]} />
          <meshStandardMaterial color="green" />
        </mesh>
      </RigidBody>
    </Physics>
  );
}
```

### Level 2: Collision Events

```tsx
import { RigidBody } from '@react-three/rapier';

function CollisionBox() {
  const handleCollisionEnter = (event) => {
    console.log('Collision with:', event.colliderObject);
  };

  const handleCollisionExit = (event) => {
    console.log('Collision ended with:', event.colliderObject);
  };

  return (
    <RigidBody onCollisionEnter={handleCollisionEnter} onCollisionExit={handleCollisionExit}>
      <mesh>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>
    </RigidBody>
  );
}
```

### Level 3: Sensors (Triggers)

```tsx
import { RigidBody, CuboidCollider } from '@react-three/rapier';

function TriggerZone() {
  const handleIntersection = (event) => {
    console.log('Something entered the zone!');
  };

  return (
    <RigidBody type="fixed">
      <CuboidCollider args={[2, 2, 2]} sensor onIntersectionEnter={handleIntersection} />
      {/* Visual representation (optional) */}
      <mesh>
        <boxGeometry args={[4, 4, 4]} />
        <meshStandardMaterial color="blue" transparent opacity={0.3} />
      </mesh>
    </RigidBody>
  );
}
```

### Level 4: Applying Forces

```tsx
import { useRef } from 'react';
import { RigidBody, RapierRigidBody } from '@react-three/rapier';
import { useFrame } from '@react-three/fiber';

function JumpingBall() {
  const rigidBodyRef = useRef<RapierRigidBody>(null);

  const jump = () => {
    rigidBodyRef.current?.applyImpulse({ x: 0, y: 10, z: 0 }, true);
  };

  useFrame(() => {
    // Apply continuous force (e.g., for movement)
    // rigidBodyRef.current?.applyForce({ x: 5, y: 0, z: 0 }, true);
  });

  return (
    <RigidBody ref={rigidBodyRef} onClick={jump}>
      <mesh>
        <sphereGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>
    </RigidBody>
  );
}
```

### Level 5: Vehicle Physics

```tsx
import { useRef } from 'react';
import { RigidBody, useRapier } from '@react-three/rapier';
import { useFrame } from '@react-three/fiber';

function Vehicle() {
  const chassisRef = useRef();
  const { rapier, world } = useRapier();

  useFrame(() => {
    if (!chassisRef.current) return;

    // Get velocity
    const vel = chassisRef.current.linvel();
    const speed = Math.sqrt(vel.x ** 2 + vel.z ** 2);

    // Apply steering based on input
    // ... implement steering logic
  });

  return (
    <RigidBody
      ref={chassisRef}
      colliders="cuboid"
      mass={1500}
      linearDamping={0.5}
      angularDamping={0.5}
    >
      <mesh>
        <boxGeometry args={[2, 0.5, 4]} />
        <meshStandardMaterial color="blue" />
      </mesh>
    </RigidBody>
  );
}
```

## Collision Groups

```tsx
// Define collision groups (bitmask)
const GROUPS = {
  PLAYER: 0b0001,
  ENEMY: 0b0010,
  GROUND: 0b0100,
  PROJECTILE: 0b1000,
};

// Player collides with ground and enemy, not projectiles
<RigidBody
  collisionGroups={interactionGroups(
    GROUPS.PLAYER,
    GROUPS.GROUND | GROUPS.ENEMY
  )}
>
```

## Anti-Patterns

**DON'T:**

- Use `trimesh` for dynamic bodies (not supported)
- Apply forces every frame without deltaTime
- Create/destroy RigidBodies frequently
- Use physics for non-interactive decorations
- Ignore collision layers (performance)

**DO:**

- Use appropriate collider shapes (simpler = faster)
- Use `fixed` for static environment
- Pool physics objects when possible
- Use collision groups for filtering
- Dispose physics world on scene change

## Physics Debugging

```tsx
import { Physics, Debug } from '@react-three/rapier';

function DebugScene() {
  return (
    <Physics>
      <Debug /> {/* Shows collision shapes */}
      {/* Your physics objects */}
    </Physics>
  );
}
```

## Checklist

Before implementing physics:

- [ ] Appropriate RigidBody type selected
- [ ] Collision shapes match visual reasonably
- [ ] Collision groups configured
- [ ] Events handled (if needed)
- [ ] Forces scaled by deltaTime
- [ ] Physics debug visualized during development

## Reference

- [Rapier documentation](https://rapier.rs/docs/)
- [@react-three/rapier docs](https://github.com/pmndrs/react-three-rapier)
- `developer/r3f/r3f-fundamentals.md` — R3F basics
