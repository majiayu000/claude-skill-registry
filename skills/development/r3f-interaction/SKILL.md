---
name: r3f-interaction
description: React Three Fiber interaction - pointer events, controls, raycasting. Use when handling user input, camera controls, or creating interactive experiences.
---

# React Three Fiber Interaction

## Pointer Events

```tsx
<mesh
  onClick={(e) => {
    e.stopPropagation()
    console.log(e.point, e.distance, e.object, e.uv)
  }}
  onContextMenu={(e) => console.log('Right click')}
  onDoubleClick={(e) => console.log('Double click')}
  onPointerOver={(e) => {
    e.stopPropagation()
    document.body.style.cursor = 'pointer'
  }}
  onPointerOut={(e) => {
    document.body.style.cursor = 'default'
  }}
  onPointerMove={(e) => console.log(e.point)}
  onPointerDown={(e) => console.log('Down')}
  onPointerUp={(e) => console.log('Up')}
/>
```

## OrbitControls

```tsx
import { OrbitControls } from '@react-three/drei'

<OrbitControls
  enableDamping
  dampingFactor={0.05}
  minDistance={2}
  maxDistance={50}
  minPolarAngle={0}
  maxPolarAngle={Math.PI / 2}
  autoRotate
  autoRotateSpeed={2}
/>
```

## Other Controls

```tsx
import {
  MapControls,
  FlyControls,
  FirstPersonControls,
  PointerLockControls,
  TrackballControls,
} from '@react-three/drei'

<MapControls />
<FlyControls movementSpeed={10} rollSpeed={0.5} />
<PointerLockControls />
```

## TransformControls

```tsx
import { TransformControls } from '@react-three/drei'

function Movable() {
  const ref = useRef()
  return (
    <>
      <mesh ref={ref}>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>
      <TransformControls object={ref} mode="translate" />
    </>
  )
}
```

## PivotControls

```tsx
import { PivotControls } from '@react-three/drei'

<PivotControls anchor={[0, 0, 0]} scale={0.75}>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</PivotControls>
```

## Drag with Gesture

```tsx
import { useDrag } from '@use-gesture/react'
import { useSpring, animated } from '@react-spring/three'

function DraggableBox() {
  const [spring, api] = useSpring(() => ({ position: [0, 0, 0] }))

  const bind = useDrag(({ movement: [mx, my], down }) => {
    api.start({
      position: down ? [mx / 100, -my / 100, 0] : [0, 0, 0]
    })
  })

  return (
    <animated.mesh {...bind()} position={spring.position}>
      <boxGeometry />
      <meshStandardMaterial color="hotpink" />
    </animated.mesh>
  )
}
```

## Keyboard Controls

```tsx
import { KeyboardControls, useKeyboardControls } from '@react-three/drei'

const controls = [
  { name: 'forward', keys: ['ArrowUp', 'KeyW'] },
  { name: 'backward', keys: ['ArrowDown', 'KeyS'] },
  { name: 'left', keys: ['ArrowLeft', 'KeyA'] },
  { name: 'right', keys: ['ArrowRight', 'KeyD'] },
  { name: 'jump', keys: ['Space'] },
]

function App() {
  return (
    <KeyboardControls map={controls}>
      <Canvas>
        <Player />
      </Canvas>
    </KeyboardControls>
  )
}

function Player() {
  const [, get] = useKeyboardControls()

  useFrame(() => {
    const { forward, backward, left, right } = get()
    // Move player based on keys
  })
}
```

## Scroll Controls

```tsx
import { ScrollControls, useScroll, Scroll } from '@react-three/drei'

function Scene() {
  return (
    <ScrollControls pages={3} damping={0.1}>
      <AnimatedContent />
      <Scroll html>
        <h1 style={{ position: 'absolute', top: '100vh' }}>Page 2</h1>
      </Scroll>
    </ScrollControls>
  )
}

function AnimatedContent() {
  const scroll = useScroll()

  useFrame(() => {
    const offset = scroll.offset  // 0 to 1
    meshRef.current.position.y = offset * 10
  })
}
```

## Html Overlay

```tsx
import { Html } from '@react-three/drei'

<mesh>
  <boxGeometry />
  <meshStandardMaterial />
  <Html position={[0, 1, 0]} center>
    <div className="label">Click me!</div>
  </Html>
</mesh>
```

## Screen to World

```tsx
function screenToWorld(screenX, screenY, camera, targetZ = 0) {
  const vec = new THREE.Vector3(
    (screenX / window.innerWidth) * 2 - 1,
    -(screenY / window.innerHeight) * 2 + 1,
    0.5
  ).unproject(camera)

  const dir = vec.sub(camera.position).normalize()
  const distance = (targetZ - camera.position.z) / dir.z
  return camera.position.clone().add(dir.multiplyScalar(distance))
}
```
