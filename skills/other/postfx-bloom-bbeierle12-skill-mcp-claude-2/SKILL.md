---
name: postfx-bloom
description: Bloom and glow effects using Three.js UnrealBloomPass with React Three Fiber. Use when implementing glow, bloom, luminance-based effects, selective bloom on specific meshes, or neon/ethereal lighting. Essential for cyberpunk aesthetics, energy effects, magic spells, and UI glow.
---

# Post-Processing Bloom

Bloom effects using UnrealBloomPass for luminance-based glow and selective object bloom.

## Quick Start

```bash
npm install three @react-three/fiber @react-three/postprocessing
```

```tsx
import { Canvas } from '@react-three/fiber';
import { EffectComposer, Bloom } from '@react-three/postprocessing';

function Scene() {
  return (
    <Canvas>
      <mesh>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial emissive="#00F5FF" emissiveIntensity={2} />
      </mesh>

      <EffectComposer>
        <Bloom
          luminanceThreshold={0.2}
          luminanceSmoothing={0.9}
          intensity={1.5}
        />
      </EffectComposer>
    </Canvas>
  );
}
```

## Core Concepts

### How Bloom Works

1. **Threshold** — Pixels brighter than threshold are extracted
2. **Blur** — Extracted pixels are blurred in multiple passes
3. **Composite** — Blurred result is added back to original image

### Key Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| `luminanceThreshold` | 0-1 | Brightness cutoff for bloom (lower = more glow) |
| `luminanceSmoothing` | 0-1 | Softness of threshold transition |
| `intensity` | 0-10 | Bloom brightness multiplier |
| `radius` | 0-1 | Blur spread/size |
| `levels` | 1-9 | Blur quality/iterations |

## Patterns

### Cosmic Glow Effect

```tsx
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import { KernelSize } from 'postprocessing';

function CosmicBloom() {
  return (
    <EffectComposer>
      <Bloom
        luminanceThreshold={0.1}
        luminanceSmoothing={0.9}
        intensity={2.5}
        radius={0.8}
        kernelSize={KernelSize.LARGE}
        mipmapBlur
      />
    </EffectComposer>
  );
}
```

### Neon Cyberpunk Bloom

```tsx
// High-contrast neon with sharp falloff
function NeonBloom() {
  return (
    <EffectComposer>
      <Bloom
        luminanceThreshold={0.4}
        luminanceSmoothing={0.2}
        intensity={3.0}
        radius={0.4}
        mipmapBlur
      />
    </EffectComposer>
  );
}

// Emissive material for neon objects
function NeonTube({ color = '#FF00FF' }) {
  return (
    <mesh>
      <cylinderGeometry args={[0.05, 0.05, 2]} />
      <meshStandardMaterial
        emissive={color}
        emissiveIntensity={4}
        toneMapped={false}
      />
    </mesh>
  );
}
```

### Selective Bloom with Layers

```tsx
import { useRef } from 'react';
import { useThree } from '@react-three/fiber';
import { EffectComposer, SelectiveBloom } from '@react-three/postprocessing';

function SelectiveGlow() {
  const glowRef = useRef();

  return (
    <>
      {/* Non-blooming object */}
      <mesh position={[-2, 0, 0]}>
        <boxGeometry />
        <meshStandardMaterial color="#333" />
      </mesh>

      {/* Blooming object */}
      <mesh ref={glowRef} position={[2, 0, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial
          emissive="#00F5FF"
          emissiveIntensity={3}
        />
      </mesh>

      <EffectComposer>
        <SelectiveBloom
          selection={glowRef}
          luminanceThreshold={0.1}
          intensity={2}
          mipmapBlur
        />
      </EffectComposer>
    </>
  );
}
```

### Multi-Selection Bloom

```tsx
import { Selection, Select, EffectComposer } from '@react-three/postprocessing';
import { SelectiveBloom } from '@react-three/postprocessing';

function MultiSelectBloom() {
  return (
    <Selection>
      {/* Non-blooming */}
      <mesh position={[-2, 0, 0]}>
        <boxGeometry />
        <meshStandardMaterial color="#333" />
      </mesh>

      {/* Blooming objects wrapped in Select */}
      <Select enabled>
        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[0.5]} />
          <meshStandardMaterial emissive="#00F5FF" emissiveIntensity={2} />
        </mesh>
      </Select>

      <Select enabled>
        <mesh position={[2, 0, 0]}>
          <octahedronGeometry args={[0.5]} />
          <meshStandardMaterial emissive="#FF00FF" emissiveIntensity={2} />
        </mesh>
      </Select>

      <EffectComposer>
        <SelectiveBloom
          luminanceThreshold={0.1}
          intensity={1.5}
          mipmapBlur
        />
      </EffectComposer>
    </Selection>
  );
}
```

### Animated Bloom Intensity

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { EffectComposer, Bloom } from '@react-three/postprocessing';

function PulsingBloom() {
  const bloomRef = useRef();

  useFrame(({ clock }) => {
    if (bloomRef.current) {
      const pulse = Math.sin(clock.elapsedTime * 2) * 0.5 + 1.5;
      bloomRef.current.intensity = pulse;
    }
  });

  return (
    <EffectComposer>
      <Bloom
        ref={bloomRef}
        luminanceThreshold={0.2}
        intensity={1.5}
        mipmapBlur
      />
    </EffectComposer>
  );
}
```

### Audio-Reactive Bloom

```tsx
function AudioReactiveBloom({ audioData }) {
  const bloomRef = useRef();

  useFrame(() => {
    if (bloomRef.current && audioData) {
      // Map bass frequency (0-255) to bloom intensity (1-4)
      const bassLevel = audioData[0] / 255;
      bloomRef.current.intensity = 1 + bassLevel * 3;

      // Map mid frequencies to threshold
      const midLevel = audioData[4] / 255;
      bloomRef.current.luminanceThreshold = 0.1 + (1 - midLevel) * 0.3;
    }
  });

  return (
    <EffectComposer>
      <Bloom
        ref={bloomRef}
        luminanceThreshold={0.2}
        intensity={1.5}
        mipmapBlur
      />
    </EffectComposer>
  );
}
```

## Emissive Materials

### Standard Emissive Setup

```tsx
// For bloom to work, objects need emissive materials
function GlowingSphere({ color = '#00F5FF', intensity = 2 }) {
  return (
    <mesh>
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial
        color="#000"
        emissive={color}
        emissiveIntensity={intensity}
        toneMapped={false}  // Important: prevents HDR clamping
      />
    </mesh>
  );
}
```

### Emissive with Texture

```tsx
import { useTexture } from '@react-three/drei';

function EmissiveTextured() {
  const emissiveMap = useTexture('/glow-pattern.png');

  return (
    <mesh>
      <planeGeometry args={[2, 2]} />
      <meshStandardMaterial
        emissiveMap={emissiveMap}
        emissive="#FFFFFF"
        emissiveIntensity={3}
        toneMapped={false}
      />
    </mesh>
  );
}
```

### Shader Material with Emissive

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';

const GlowMaterial = shaderMaterial(
  { uTime: 0, uColor: [0, 0.96, 1], uIntensity: 2.0 },
  // Vertex shader
  `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader - outputs HDR values for bloom
  `
    uniform float uTime;
    uniform vec3 uColor;
    uniform float uIntensity;
    varying vec2 vUv;

    void main() {
      float pulse = sin(uTime * 2.0) * 0.3 + 0.7;
      vec3 glow = uColor * uIntensity * pulse;
      gl_FragColor = vec4(glow, 1.0);
    }
  `
);

extend({ GlowMaterial });

function PulsingGlowMesh() {
  const materialRef = useRef();

  useFrame(({ clock }) => {
    materialRef.current.uTime = clock.elapsedTime;
  });

  return (
    <mesh>
      <sphereGeometry args={[1, 32, 32]} />
      <glowMaterial ref={materialRef} toneMapped={false} />
    </mesh>
  );
}
```

## Performance Optimization

### Resolution Scaling

```tsx
<EffectComposer
  multisampling={0}  // Disable MSAA for performance
>
  <Bloom
    luminanceThreshold={0.2}
    intensity={1.5}
    mipmapBlur        // More efficient blur method
    radius={0.8}
    levels={5}        // Reduce for performance (default: 8)
  />
</EffectComposer>
```

### Mobile-Optimized Bloom

```tsx
import { useDetectGPU } from '@react-three/drei';

function AdaptiveBloom() {
  const { tier } = useDetectGPU();

  const config = tier < 2
    ? { levels: 3, radius: 0.5, intensity: 1.0 }
    : { levels: 5, radius: 0.8, intensity: 1.5 };

  return (
    <EffectComposer multisampling={tier < 2 ? 0 : 4}>
      <Bloom
        luminanceThreshold={0.2}
        luminanceSmoothing={0.9}
        mipmapBlur
        {...config}
      />
    </EffectComposer>
  );
}
```

## Temporal Collapse Theme

Bloom configuration for the New Year countdown cosmic aesthetic:

```tsx
// Cosmic void with cyan/magenta glow
function TemporalCollapseBloom() {
  return (
    <EffectComposer>
      <Bloom
        luminanceThreshold={0.15}
        luminanceSmoothing={0.9}
        intensity={2.0}
        radius={0.85}
        mipmapBlur
      />
    </EffectComposer>
  );
}

// Color palette for emissive materials
const TEMPORAL_COLORS = {
  cyan: '#00F5FF',
  magenta: '#FF00FF',
  gold: '#FFD700',
  void: '#050508'
};

// Time digit with glow
function GlowingDigit({ digit, color = TEMPORAL_COLORS.cyan }) {
  return (
    <Text3D font="/fonts/cosmic.json" size={2} height={0.2}>
      {digit}
      <meshStandardMaterial
        color="#111"
        emissive={color}
        emissiveIntensity={3}
        toneMapped={false}
      />
    </Text3D>
  );
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No bloom visible | Ensure `emissiveIntensity > 1` and `toneMapped={false}` |
| Bloom too subtle | Lower `luminanceThreshold`, increase `intensity` |
| Performance issues | Reduce `levels`, enable `mipmapBlur`, disable multisampling |
| Selective bloom not working | Verify `ref` is passed and object has emissive material |
| Bloom bleeding everywhere | Raise `luminanceThreshold` to isolate bright areas |

## Reference

- See `postfx-composer` for EffectComposer setup patterns
- See `postfx-effects` for combining bloom with other effects
- See `shaders-glsl` for custom emissive shader techniques
