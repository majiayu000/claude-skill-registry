---
name: r3f-textures
description: React Three Fiber textures - useTexture, environment maps, video textures. Use when loading images, PBR texture sets, HDR environments, or video.
---

# React Three Fiber Textures

## useTexture Hook

```tsx
import { useTexture } from '@react-three/drei'

// Single texture
const texture = useTexture('/textures/wood.jpg')

// Multiple textures (array)
const [color, normal, roughness] = useTexture([
  '/textures/color.jpg',
  '/textures/normal.jpg',
  '/textures/roughness.jpg',
])

// Named object (recommended for PBR)
const textures = useTexture({
  map: '/textures/color.jpg',
  normalMap: '/textures/normal.jpg',
  roughnessMap: '/textures/roughness.jpg',
})

<meshStandardMaterial {...textures} />
```

## Texture Configuration

```tsx
import * as THREE from 'three'

const texture = useTexture('/textures/tile.jpg', (tex) => {
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping
  tex.repeat.set(4, 4)
  tex.colorSpace = THREE.SRGBColorSpace  // For color maps
  tex.anisotropy = 16
})
```

## Environment Maps

```tsx
import { useEnvironment, Environment } from '@react-three/drei'

// As component
<Environment preset="sunset" background />

// As hook
const envMap = useEnvironment({ preset: 'sunset' })
<meshStandardMaterial envMap={envMap} metalness={1} roughness={0} />

// Custom HDR
const envMap = useEnvironment({ files: '/hdri/studio.hdr' })
```

## Video Texture

```tsx
import { useVideoTexture } from '@react-three/drei'

function VideoPlane() {
  const texture = useVideoTexture('/videos/sample.mp4', {
    start: true,
    loop: true,
    muted: true,
  })

  return (
    <mesh>
      <planeGeometry args={[16, 9].map(x => x * 0.5)} />
      <meshBasicMaterial map={texture} toneMapped={false} />
    </mesh>
  )
}
```

## Canvas Texture

```tsx
function DynamicTexture() {
  const textureRef = useRef()

  useEffect(() => {
    const canvas = document.createElement('canvas')
    canvas.width = canvas.height = 256
    const ctx = canvas.getContext('2d')
    ctx.fillStyle = 'red'
    ctx.fillRect(0, 0, 256, 256)
    ctx.fillStyle = 'white'
    ctx.font = '48px Arial'
    ctx.fillText('Hello', 50, 150)
    textureRef.current = new THREE.CanvasTexture(canvas)
  }, [])

  return (
    <mesh>
      <planeGeometry />
      <meshBasicMaterial map={textureRef.current} />
    </mesh>
  )
}
```

## Render Targets

```tsx
import { useFBO } from '@react-three/drei'

function RenderToTexture() {
  const fbo = useFBO(512, 512)

  useFrame(({ gl, scene, camera }) => {
    gl.setRenderTarget(fbo)
    gl.render(scene, camera)
    gl.setRenderTarget(null)
  })

  return (
    <mesh>
      <planeGeometry />
      <meshBasicMaterial map={fbo.texture} />
    </mesh>
  )
}
```

## Preloading

```tsx
// Preload at module level
useTexture.preload('/textures/hero.jpg')
useTexture.preload(['/tex1.jpg', '/tex2.jpg'])
```

## Material Texture Maps

```tsx
<meshStandardMaterial
  map={colorTexture}           // sRGB
  normalMap={normalTexture}    // Linear
  roughnessMap={roughTexture}  // Linear
  metalnessMap={metalTexture}  // Linear
  aoMap={aoTexture}            // Linear, requires uv2
  emissiveMap={emissiveTexture}
  displacementMap={dispTexture}
  displacementScale={0.1}
/>
```
