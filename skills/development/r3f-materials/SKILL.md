---
name: r3f-materials
description: React Three Fiber materials - PBR materials, Drei materials, shader materials. Use when styling meshes, creating custom materials, or implementing visual effects.
---

# React Three Fiber Materials

## Standard Materials

```tsx
<meshBasicMaterial color="red" />
<meshLambertMaterial color="green" />
<meshPhongMaterial color="blue" shininess={100} />
<meshStandardMaterial color="white" roughness={0.5} metalness={0.5} />
<meshPhysicalMaterial transmission={1} thickness={0.5} ior={1.5} />
```

## PBR with Textures

```tsx
import { useTexture } from '@react-three/drei'

function PBRMesh() {
  const textures = useTexture({
    map: '/textures/color.jpg',
    normalMap: '/textures/normal.jpg',
    roughnessMap: '/textures/roughness.jpg',
  })

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial {...textures} />
    </mesh>
  )
}
```

## Drei Special Materials

```tsx
import {
  MeshReflectorMaterial,
  MeshWobbleMaterial,
  MeshDistortMaterial,
  MeshTransmissionMaterial,
} from '@react-three/drei'

// Reflective floor
<mesh rotation={[-Math.PI / 2, 0, 0]}>
  <planeGeometry args={[10, 10]} />
  <MeshReflectorMaterial
    blur={[400, 100]}
    resolution={1024}
    mixStrength={0.5}
    color="#333"
  />
</mesh>

// Wobbly effect
<mesh>
  <torusKnotGeometry />
  <MeshWobbleMaterial factor={1} speed={2} color="hotpink" />
</mesh>

// Distortion
<mesh>
  <sphereGeometry args={[1, 64, 64]} />
  <MeshDistortMaterial distort={0.5} speed={2} color="cyan" />
</mesh>

// Glass/transmission
<mesh>
  <sphereGeometry />
  <MeshTransmissionMaterial
    transmission={1}
    thickness={0.5}
    roughness={0}
    chromaticAberration={0.06}
  />
</mesh>
```

## Emissive (Glow)

```tsx
<meshStandardMaterial
  color="black"
  emissive="#ff0000"
  emissiveIntensity={2}
  toneMapped={false}  // Required for bloom
/>
```

## Custom Shader Material

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend, useFrame } from '@react-three/fiber'

const CustomMaterial = shaderMaterial(
  { time: 0, color: new THREE.Color('hotpink') },
  // Vertex shader
  `varying vec2 vUv;
   void main() {
     vUv = uv;
     gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
   }`,
  // Fragment shader
  `uniform float time;
   uniform vec3 color;
   varying vec2 vUv;
   void main() {
     gl_FragColor = vec4(color * (sin(time + vUv.x * 10.0) * 0.5 + 0.5), 1.0);
   }`
)

extend({ CustomMaterial })

function ShaderMesh() {
  const ref = useRef()
  useFrame(({ clock }) => {
    ref.current.time = clock.elapsedTime
  })
  return (
    <mesh>
      <boxGeometry />
      <customMaterial ref={ref} />
    </mesh>
  )
}
```

## Environment Maps

```tsx
import { useEnvironment, Environment } from '@react-three/drei'

// Scene-wide
<Environment preset="sunset" background />

// Per-material
function EnvMesh() {
  const envMap = useEnvironment({ preset: 'sunset' })
  return (
    <mesh>
      <sphereGeometry />
      <meshStandardMaterial metalness={1} roughness={0} envMap={envMap} />
    </mesh>
  )
}
```

## Dynamic Materials

```tsx
function AnimatedMaterial() {
  const ref = useRef()

  useFrame(({ clock }) => {
    ref.current.color.setHSL((clock.elapsedTime * 0.1) % 1, 1, 0.5)
    ref.current.roughness = (Math.sin(clock.elapsedTime) + 1) / 2
  })

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial ref={ref} />
    </mesh>
  )
}
```
