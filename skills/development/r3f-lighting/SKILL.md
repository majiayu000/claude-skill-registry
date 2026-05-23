---
name: r3f-lighting
description: React Three Fiber lighting - light types, shadows, environment, Drei helpers. Use when adding lights, configuring shadows, or setting up IBL.
---

# React Three Fiber Lighting

## Light Types

```tsx
<ambientLight intensity={0.5} color="white" />

<directionalLight position={[5, 5, 5]} intensity={1} />

<pointLight position={[0, 5, 0]} intensity={1} distance={100} decay={2} />

<spotLight
  position={[0, 10, 0]}
  angle={Math.PI / 6}
  penumbra={0.5}
  intensity={1}
/>

<hemisphereLight skyColor="#87ceeb" groundColor="#8b4513" intensity={0.6} />
```

## Shadow Setup

```tsx
// 1. Enable on Canvas
<Canvas shadows>

// 2. Configure light shadows
<directionalLight
  castShadow
  position={[5, 10, 5]}
  shadow-mapSize={[2048, 2048]}
  shadow-camera-left={-10}
  shadow-camera-right={10}
  shadow-camera-top={10}
  shadow-camera-bottom={-10}
  shadow-camera-near={0.5}
  shadow-camera-far={50}
  shadow-bias={-0.0001}
/>

// 3. Enable on objects
<mesh castShadow receiveShadow>
  <boxGeometry />
  <meshStandardMaterial />
</mesh>
```

## Drei Environment

```tsx
import { Environment } from '@react-three/drei'

// Presets: 'sunset', 'dawn', 'night', 'warehouse', 'forest', 'apartment', 'studio', 'city', 'park', 'lobby'
<Environment preset="sunset" background />

// Custom HDR
<Environment files="/hdri/studio.hdr" background />

// Background blur
<Environment preset="city" background blur={0.5} />
```

## Drei Lightformers

```tsx
import { Environment, Lightformer } from '@react-three/drei'

<Environment>
  <Lightformer
    intensity={2}
    position={[0, 5, -5]}
    scale={[10, 5, 1]}
    color="white"
  />
  <Lightformer
    form="ring"
    intensity={1}
    position={[0, 0, 5]}
    scale={2}
  />
</Environment>
```

## Fake Shadows

```tsx
import { ContactShadows, AccumulativeShadows, RandomizedLight } from '@react-three/drei'

// Contact shadows (fast, good for product shots)
<ContactShadows
  position={[0, 0, 0]}
  opacity={0.5}
  blur={2}
  scale={10}
  far={10}
/>

// Accumulative shadows (high quality, static)
<AccumulativeShadows temporal frames={100} position={[0, 0, 0]}>
  <RandomizedLight amount={8} position={[5, 5, -5]} />
</AccumulativeShadows>
```

## Stage (Quick Setup)

```tsx
import { Stage } from '@react-three/drei'

<Stage
  intensity={1}
  environment="city"
  shadows={{ type: 'contact', opacity: 0.5, blur: 2 }}
>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</Stage>
```

## Animated Lights

```tsx
function AnimatedLight() {
  const ref = useRef()

  useFrame(({ clock }) => {
    const t = clock.elapsedTime
    ref.current.position.x = Math.cos(t) * 5
    ref.current.position.z = Math.sin(t) * 5
  })

  return <pointLight ref={ref} intensity={1} color="orange" />
}
```

## Sky & Stars

```tsx
import { Sky, Stars } from '@react-three/drei'

<Sky
  distance={450000}
  sunPosition={[100, 10, 100]}
  inclination={0.5}
  azimuth={0.25}
/>

<Stars radius={100} depth={50} count={5000} factor={4} fade />
```
