---
name: r3f-fundamentals
description: React Three Fiber fundamentals - Canvas, hooks (useFrame, useThree), JSX elements, events, refs. Use when setting up R3F scenes, creating components, handling the render loop, or working with Three.js objects in React.
---

# React Three Fiber Fundamentals

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

function RotatingBox() {
  const meshRef = useRef()

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta
    meshRef.current.rotation.y += delta * 0.5
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  )
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <RotatingBox />
    </Canvas>
  )
}
```

## Canvas Component

```tsx
<Canvas
  camera={{ position: [0, 5, 10], fov: 75, near: 0.1, far: 1000 }}
  gl={{ antialias: true, alpha: true }}
  dpr={[1, 2]}
  shadows
  frameloop="always"  // 'always' | 'demand' | 'never'
  onCreated={(state) => console.log('Ready')}
  style={{ width: '100%', height: '100vh' }}
>
  <Scene />
</Canvas>
```

## useFrame Hook

```tsx
useFrame((state, delta) => {
  // state: clock, camera, scene, gl, pointer, viewport
  // delta: time since last frame in seconds
  meshRef.current.rotation.y += delta

  // Time-based animation
  const t = state.clock.elapsedTime
  meshRef.current.position.y = Math.sin(t) * 2
})

// Render priority (lower = earlier)
useFrame(() => {}, -1)  // Pre-render
useFrame(() => {}, 1)   // Post-render
```

## useThree Hook

```tsx
const camera = useThree((state) => state.camera)
const gl = useThree((state) => state.gl)
const size = useThree((state) => state.size)
const viewport = useThree((state) => state.viewport)
const invalidate = useThree((state) => state.invalidate)
```

## JSX Elements

```tsx
<mesh position={[0, 0, 0]} rotation={[0, Math.PI, 0]} scale={1.5}>
  <boxGeometry args={[1, 1, 1]} />
  <meshStandardMaterial color="red" />
</mesh>

<group position={[5, 0, 0]}>
  <mesh>...</mesh>
  <mesh>...</mesh>
</group>

// Nested properties
<mesh position-x={5} rotation-y={Math.PI} />
<directionalLight shadow-mapSize={[2048, 2048]} />
```

## Event Handling

```tsx
<mesh
  onClick={(e) => {
    e.stopPropagation()
    console.log(e.point, e.distance, e.object)
  }}
  onPointerOver={(e) => setHovered(true)}
  onPointerOut={(e) => setHovered(false)}
  onPointerMove={(e) => console.log(e.uv)}
/>
```

## primitive & extend

```tsx
// Use existing Three.js objects
<primitive object={gltf.scene} position={[0, 0, 0]} />

// Register custom classes
import { extend } from '@react-three/fiber'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
extend({ OrbitControls })
<orbitControls args={[camera, gl.domElement]} />
```

## Performance

```tsx
// Use refs for animations (avoid re-renders)
const meshRef = useRef()
useFrame(() => {
  meshRef.current.rotation.y += 0.01
})

// Isolate animated components
function Scene() {
  return (
    <>
      <StaticMesh />
      <AnimatedMesh />  {/* Only this updates */}
    </>
  )
}
```
