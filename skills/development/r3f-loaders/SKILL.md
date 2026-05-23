---
name: r3f-loaders
description: React Three Fiber asset loading - useGLTF, useLoader, Suspense patterns. Use when loading 3D models, textures, or managing loading states.
---

# React Three Fiber Loaders

## useGLTF (Recommended)

```tsx
import { useGLTF } from '@react-three/drei'

function Model() {
  const { scene, nodes, materials, animations } = useGLTF('/models/robot.glb')
  return <primitive object={scene} />
}

// Preload
useGLTF.preload('/models/robot.glb')
```

## With Draco Compression

```tsx
import { useGLTF } from '@react-three/drei'

function Model() {
  const { scene } = useGLTF('/models/compressed.glb', true)  // true enables Draco
  return <primitive object={scene} />
}
```

## Clone for Multiple Instances

```tsx
import { Clone } from '@react-three/drei'

function Trees() {
  const { scene } = useGLTF('/models/tree.glb')
  return (
    <>
      <Clone object={scene} position={[0, 0, 0]} />
      <Clone object={scene} position={[5, 0, 0]} />
      <Clone object={scene} position={[-5, 0, 0]} />
    </>
  )
}
```

## useLoader (Core)

```tsx
import { useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { TextureLoader } from 'three'

const gltf = useLoader(GLTFLoader, '/model.glb')
const texture = useLoader(TextureLoader, '/texture.jpg')
```

## Suspense Loading

```tsx
import { Suspense } from 'react'

function Fallback() {
  return (
    <mesh>
      <boxGeometry />
      <meshBasicMaterial color="gray" wireframe />
    </mesh>
  )
}

function Scene() {
  return (
    <Suspense fallback={<Fallback />}>
      <Model />
    </Suspense>
  )
}
```

## Progress Tracking

```tsx
import { useProgress, Html } from '@react-three/drei'

function Loader() {
  const { progress, active } = useProgress()

  return active ? (
    <Html center>
      <div>{progress.toFixed(0)}%</div>
    </Html>
  ) : null
}
```

## Process GLTF Content

```tsx
function Model() {
  const { scene } = useGLTF('/model.glb')

  useEffect(() => {
    scene.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
  }, [scene])

  return <primitive object={scene} />
}
```

## Other Loaders

```tsx
import { useFBX, useOBJ } from '@react-three/drei'

const fbx = useFBX('/model.fbx')
const obj = useOBJ('/model.obj')
```

## TypeScript with gltfjsx

```bash
npx gltfjsx model.glb --types
```

Generates typed component with proper mesh/material access.
