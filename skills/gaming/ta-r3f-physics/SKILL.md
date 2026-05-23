---
name: ta-r3f-physics
description: Physics integration with Rapier for R3F game development. Use when adding physics, colliders, rigid bodies.
category: performance
---
# R3F Physics Skill

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

## Collision Detection Patterns

### Simple Bounds vs. Mesh Collision

Choose collision approach based on use case:

| Scenario | Collision Type | When to Use |
|----------|---------------|-------------|
| Projectiles (paint balls) | Simple bounds (box/sphere) | Fast-moving, small objects |
| Terrain (raymarched voxels) | Height/raycast collision | Complex custom geometry |
| Buildings/POIs | Mesh collider (trimesh) | Static complex geometry |
| Player character | Capsule collider | Movement on surfaces |
| Vehicles | Compound colliders | Multiple collision shapes |

### Pattern 1: Simple Bounds (Projectiles)

```tsx
// Fast projectile collision - use simple bounds for performance
function checkProjectileCollision(position: Vector3, bounds: { min: number; max: number }) {
  const { min, max } = bounds;
  return (
    position.x >= min && position.x <= max &&
    position.y >= 0 && position.y <= 50 && // Ground check
    position.z >= min && position.z <= max
  );
}

// PaintGun.tsx - projectile bounds checking
const MAP_BOUNDS = { min: -20, max: 20 };
const GROUND_LEVEL = 0;

function updateProjectile(projectile: Projectile, delta: number) {
  // Apply gravity
  projectile.velocity.y -= 15 * delta;
  projectile.position.add(projectile.velocity.clone().multiplyScalar(delta));

  // Simple ground collision
  if (projectile.position.y <= GROUND_LEVEL) {
    projectile.position.y = GROUND_LEVEL;
    return { hit: true, normal: new Vector3(0, 1, 0) };
  }

  // Simple wall collision
  if (Math.abs(projectile.position.x) > MAP_BOUNDS.max ||
      Math.abs(projectile.position.z) > MAP_BOUNDS.max) {
    return { hit: true, normal: /* calculate from side */ };
  }

  return { hit: false };
}
```

### Pattern 2: Terrain Height Collision

```tsx
// For raymarched terrain (iter5-003), use height-based collision
interface TerrainCollision {
  getHeightAt(x: number, z: number): number;
  getNormalAt(x: number, z: number): Vector3;
}

function checkTerrainCollision(
  position: Vector3,
  terrain: TerrainCollision
): CollisionResult | null {
  const terrainHeight = terrain.getHeightAt(position.x, position.z);

  if (position.y <= terrainHeight) {
    return {
      hit: true,
      normal: terrain.getNormalAt(position.x, position.z),
      point: new Vector3(position.x, terrainHeight, position.z)
    };
  }

  return null;
}
```

### Pattern 3: Raycast for First-Person

```tsx
// Raycast from camera for shooting detection
import { useThree } from '@react-three/fiber';
import { Raycaster, Vector3 } from 'three';

function useShootingRaycast() {
  const { camera, scene } = useThree();
  const raycaster = new Raycaster();

  const shoot = () => {
    raycaster.setFromCamera(new Vector2(0, 0), camera); // Center of screen
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
      const hit = intersects[0];
      return {
        point: hit.point,
        normal: hit.face.normal,
        object: hit.object
      };
    }

    return null;
  };

  return { shoot };
}
```

### Pattern 4: Decal Surface Detection

```tsx
// Determine surface orientation for decal placement
function getSurfaceNormal(hitPoint: Vector3, hitNormal: Vector3): SurfaceType {
  const upDot = hitNormal.dot(new Vector3(0, 1, 0));

  if (upDot > 0.7) return 'floor';
  if (upDot < -0.7) return 'ceiling';
  return 'wall';
}

function orientDecal(normal: Vector3): Euler {
  // Calculate proper rotation for decal based on surface normal
  const up = new Vector3(0, 1, 0);
  const quaternion = new Quaternion().setFromUnitVectors(up, normal);
  return new Euler().setFromQuaternion(quaternion);
}
```

### When to Upgrade from Simple Bounds

Upgrade to mesh collision when:

1. **Terrain has complex overhangs** - Simple height-based fails
2. **Buildings have interiors** - Need proper wall/floor separation
3. **Precision is critical** - Player movement, not just projectiles

Stay with simple bounds when:

1. **Performance is priority** - Fast projectiles don't need accuracy
2. **Geometry is procedural** - Raymarching doesn't have mesh data
3. **Objects are small** - Paint balls, particles

## Anti-Patterns

❌ **DON'T:**

- Use `trimesh` for dynamic bodies (not supported)
- Apply forces every frame without deltaTime
- Create/destroy RigidBodies frequently
- Use physics for non-interactive decorations
- Ignore collision layers (performance)
- Use mesh collision for fast projectiles (overkill)
- Mix simple bounds and mesh collision without clear pattern

✅ **DO:**

- Use appropriate collider shapes (simpler = faster)
- Use `fixed` for static environment
- Pool physics objects when possible
- Use collision groups for filtering
- Dispose physics world on scene change
- Use simple bounds for projectiles and fast-moving objects
- Use raycast/height collision for custom terrain
- Document which collision pattern each feature uses

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

## Related Skills

For R3F fundamentals: `Skill("ta-r3f-fundamentals")`

## External References

- [Rapier documentation](https://rapier.rs/docs/)
- [@react-three/rapier docs](https://github.com/pmndrs/react-three-rapier)
