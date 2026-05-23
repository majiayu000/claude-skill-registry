---
name: r3f-postprocessing
description: React Three Fiber post-processing - EffectComposer, bloom, depth of field, custom effects. Use when adding visual effects or enhancing rendered output.
---

# React Three Fiber Post-Processing

## Setup

```tsx
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing'

function Scene() {
  return (
    <Canvas>
      <mesh>...</mesh>

      <EffectComposer>
        <Bloom luminanceThreshold={0.5} intensity={1.5} />
        <Vignette offset={0.3} darkness={0.5} />
      </EffectComposer>
    </Canvas>
  )
}
```

## Common Effects

```tsx
import {
  Bloom,
  DepthOfField,
  Noise,
  Vignette,
  ChromaticAberration,
  SMAA,
} from '@react-three/postprocessing'

<EffectComposer>
  {/* Bloom/Glow */}
  <Bloom
    luminanceThreshold={0.5}
    luminanceSmoothing={0.9}
    intensity={1.5}
    mipmapBlur
  />

  {/* Depth of Field */}
  <DepthOfField
    focusDistance={0.01}
    focalLength={0.02}
    bokehScale={2}
  />

  {/* Film grain */}
  <Noise opacity={0.1} />

  {/* Vignette */}
  <Vignette offset={0.3} darkness={0.5} />

  {/* Chromatic aberration */}
  <ChromaticAberration offset={[0.002, 0.002]} />

  {/* Anti-aliasing */}
  <SMAA />
</EffectComposer>
```

## Selective Bloom

```tsx
import { Selection, Select, EffectComposer, Bloom } from '@react-three/postprocessing'

function Scene() {
  return (
    <Selection>
      <EffectComposer>
        <Bloom intensity={1} luminanceThreshold={0} mipmapBlur />
      </EffectComposer>

      {/* Only selected objects bloom */}
      <Select enabled>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial emissive="red" emissiveIntensity={2} toneMapped={false} />
        </mesh>
      </Select>

      {/* Not selected, no bloom */}
      <mesh position={[2, 0, 0]}>
        <boxGeometry />
        <meshStandardMaterial color="blue" />
      </mesh>
    </Selection>
  )
}
```

## Outline Effect

```tsx
import { Selection, Select, EffectComposer, Outline } from '@react-three/postprocessing'

<Selection>
  <EffectComposer>
    <Outline
      blur
      visibleEdgeColor={0xffffff}
      edgeStrength={100}
      width={1000}
    />
  </EffectComposer>

  <Select enabled={hovered}>
    <mesh>...</mesh>
  </Select>
</Selection>
```

## N8AO (Ambient Occlusion)

```tsx
import { N8AO } from '@react-three/postprocessing'

<EffectComposer>
  <N8AO
    aoRadius={0.5}
    intensity={1}
    distanceFalloff={1}
    quality="high"
  />
</EffectComposer>
```

## God Rays

```tsx
import { GodRays } from '@react-three/postprocessing'

function Scene() {
  const sunRef = useRef()

  return (
    <>
      <mesh ref={sunRef} position={[0, 10, -20]}>
        <sphereGeometry args={[2]} />
        <meshBasicMaterial color="white" />
      </mesh>

      <EffectComposer>
        <GodRays sun={sunRef} density={0.96} decay={0.92} weight={0.3} />
      </EffectComposer>
    </>
  )
}
```

## Custom Effect

```tsx
import { Effect } from 'postprocessing'
import { forwardRef, useMemo } from 'react'

const fragmentShader = `
  uniform float time;
  void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
    vec2 offset = vec2(sin(uv.y * 50.0 + time) * 0.005, 0.0);
    outputColor = texture2D(inputBuffer, uv + offset);
  }
`

class WaveEffectImpl extends Effect {
  constructor() {
    super('WaveEffect', fragmentShader, { uniforms: new Map([['time', { value: 0 }]]) })
  }
}

const WaveEffect = forwardRef((props, ref) => {
  const effect = useMemo(() => new WaveEffectImpl(), [])
  return <primitive ref={ref} object={effect} />
})

// Usage
<EffectComposer>
  <WaveEffect />
</EffectComposer>
```

## Performance

- Limit effect count
- Reduce multisampling on mobile
- Use conditional rendering
- Prefer SMAA over MSAA
