---
name: r3f-physics
description: React Three Fiber physics with Rapier - RigidBody, colliders, forces, joints. Use when adding physics simulation, collision detection, or character controllers.
---

# React Three Fiber Physics (Rapier)

## Setup

```bash
npm install @react-three/rapier
```

```tsx
import { Physics, RigidBody } from '@react-three/rapier'

function Scene() {
  return (
    <Physics gravity={[0, -9.81, 0]} debug>
      <RigidBody>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial />
        </mesh>
      </RigidBody>

      <RigidBody type="fixed">
        <mesh position={[0, -2, 0]}>
          <boxGeometry args={[10, 0.5, 10]} />
          <meshStandardMaterial />
        </mesh>
      </RigidBody>
    </Physics>
  )
}
```

## RigidBody Types

```tsx
// Dynamic - affected by gravity and forces
<RigidBody type="dynamic">...</RigidBody>

// Fixed - immovable
<RigidBody type="fixed">...</RigidBody>

// KinematicPosition - moved via position, affects others
<RigidBody type="kinematicPosition">...</RigidBody>

// KinematicVelocity - moved via velocity
<RigidBody type="kinematicVelocity">...</RigidBody>
```

## RigidBody Properties

```tsx
<RigidBody
  mass={1}
  friction={0.7}
  restitution={0.3}  // Bounciness
  linearDamping={0.5}
  angularDamping={0.5}
  gravityScale={1}
  lockTranslations  // Lock all translations
  lockRotations     // Lock all rotations
  enabledTranslations={[true, true, false]}  // Lock Z translation
  ccd  // Continuous collision detection
>
```

## Colliders

```tsx
// Auto-generated from mesh
<RigidBody colliders="cuboid">  // or "ball", "hull", "trimesh"
  <mesh>...</mesh>
</RigidBody>

// Manual colliders
import { CuboidCollider, BallCollider, CapsuleCollider } from '@react-three/rapier'

<RigidBody colliders={false}>
  <CuboidCollider args={[0.5, 0.5, 0.5]} />
  <BallCollider args={[0.5]} position={[0, 1, 0]} />
  <CapsuleCollider args={[0.5, 1]} />
</RigidBody>
```

## Forces & Impulses

```tsx
function PhysicsBox() {
  const ref = useRef()

  const jump = () => {
    ref.current.applyImpulse({ x: 0, y: 5, z: 0 }, true)
  }

  const push = () => {
    ref.current.applyForce({ x: 10, y: 0, z: 0 }, true)
  }

  return (
    <RigidBody ref={ref}>
      <mesh onClick={jump}>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>
    </RigidBody>
  )
}
```

## Collision Events

```tsx
<RigidBody
  onCollisionEnter={({ manifold, other }) => {
    console.log('Collision with', other.rigidBodyObject.name)
    console.log('Contact force', manifold.solverContactForce)
  }}
  onCollisionExit={({ other }) => {
    console.log('Stopped colliding with', other.rigidBodyObject.name)
  }}
>
```

## Sensors (Triggers)

```tsx
<RigidBody>
  <CuboidCollider
    args={[2, 2, 2]}
    sensor
    onIntersectionEnter={({ other }) => {
      console.log('Entered trigger zone')
    }}
    onIntersectionExit={({ other }) => {
      console.log('Left trigger zone')
    }}
  />
</RigidBody>
```

## Collision Groups

```tsx
import { interactionGroups } from '@react-three/rapier'

// Group 0 collides with groups 0 and 1
<RigidBody collisionGroups={interactionGroups(0, [0, 1])}>

// Group 1 only collides with group 0
<RigidBody collisionGroups={interactionGroups(1, [0])}>
```

## Joints

```tsx
import { useSphericalJoint, useRevoluteJoint } from '@react-three/rapier'

function Pendulum() {
  const anchor = useRef()
  const ball = useRef()

  useSphericalJoint(anchor, ball, [
    [0, 0, 0],  // Anchor point on first body
    [0, 2, 0],  // Anchor point on second body
  ])

  return (
    <>
      <RigidBody ref={anchor} type="fixed">...</RigidBody>
      <RigidBody ref={ball}>...</RigidBody>
    </>
  )
}
```

## Character Controller

```tsx
import { CapsuleCollider, RigidBody, useRapier } from '@react-three/rapier'

function Player() {
  const ref = useRef()
  const { rapier, world } = useRapier()

  useFrame(() => {
    // Move with velocity
    ref.current.setLinvel({ x: moveX * 5, y: ref.current.linvel().y, z: moveZ * 5 })
  })

  return (
    <RigidBody ref={ref} lockRotations>
      <CapsuleCollider args={[0.5, 0.5]} />
    </RigidBody>
  )
}
```

## Performance Tips

- Use simple collider shapes
- Avoid trimesh for dynamic bodies
- Enable sleeping for inactive bodies
- Use collision groups to limit checks
- Keep fixed timestep for stability
