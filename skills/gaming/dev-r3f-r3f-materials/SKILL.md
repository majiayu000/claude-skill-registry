---
name: dev-r3f-r3f-materials
description: Material selection, shaders, and visual effects for R3F
category: r3f
---

# R3F Materials

> "Materials define the soul of your 3D objects – choose wisely."

## When to Use This Skill

Use when:
- Choosing material type for objects
- Creating custom shaders
- Implementing visual effects
- Optimizing material performance

## Quick Start

```tsx
// Standard PBR material (recommended default)
<meshStandardMaterial
  color="royalblue"
  roughness={0.5}
  metalness={0.5}
/>

// Basic material (unlit, best performance)
<meshBasicMaterial color="red" />

// Physical material (advanced PBR)
<meshPhysicalMaterial
  clearcoat={1}
  clearcoatRoughness={0.1}
  transmission={0.9}
  thickness={0.5}
/>
```

## Decision Framework

| Need            | Material               | Performance   |
| --------------- | ---------------------- | ------------- |
| Unlit color     | `meshBasicMaterial`    | ⚡ Fastest    |
| Simple shading  | `meshLambertMaterial`  | ⚡⚡ Fast     |
| Stylized look   | `meshToonMaterial`     | ⚡⚡ Fast     |
| Realistic PBR   | `meshStandardMaterial` | ⚡⚡⚡ Medium |
| Glass/water     | `meshPhysicalMaterial` | ⚡⚡⚡⚡ Slow |
| Custom effects  | `shaderMaterial`       | Varies        |
| Matcap lighting | `meshMatcapMaterial`   | ⚡⚡ Fast     |

## Progressive Guide

### Level 1: Standard Materials

```tsx
// Most common choice - good balance of quality and performance
<meshStandardMaterial
  color="#ff6600"
  roughness={0.7} // 0 = smooth, 1 = rough
  metalness={0.3} // 0 = dielectric, 1 = metal
  envMapIntensity={1}
/>
```

### Level 2: Textured Materials

```tsx
import { useTexture } from '@react-three/drei';

function TexturedMesh() {
  const [colorMap, normalMap, roughnessMap] = useTexture([
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg',
  ]);

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial map={colorMap} normalMap={normalMap} roughnessMap={roughnessMap} />
    </mesh>
  );
}
```

### Level 3: Matcap Materials (Fast & Stylized)

```tsx
import { useMatcapTexture } from '@react-three/drei';

function MatcapMesh() {
  const [matcap] = useMatcapTexture('3B3C3F_DAD9D5_929290_ABACA8');

  return (
    <mesh>
      <sphereGeometry />
      <meshMatcapMaterial matcap={matcap} />
    </mesh>
  );
}
```

### Level 4: Custom Shaders

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame } from '@react-three/fiber';

const WaveShaderMaterial = shaderMaterial(
  { uTime: 0, uColor: new THREE.Color('hotpink') },
  // Vertex shader
  `
    uniform float uTime;
    varying vec2 vUv;

    void main() {
      vUv = uv;
      vec3 pos = position;
      pos.z += sin(pos.x * 4.0 + uTime) * 0.1;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform vec3 uColor;
    varying vec2 vUv;

    void main() {
      gl_FragColor = vec4(uColor, 1.0);
    }
  `
);

extend({ WaveShaderMaterial });

function WavyPlane() {
  const materialRef = useRef();

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

  return (
    <mesh>
      <planeGeometry args={[4, 4, 32, 32]} />
      <waveShaderMaterial ref={materialRef} />
    </mesh>
  );
}
```

### Level 5: Transparent & Glass

```tsx
// Glass/water with transmission
<meshPhysicalMaterial
  transmission={0.95}      // 0-1, how much light passes through
  thickness={0.5}          // Simulated thickness
  roughness={0.05}
  ior={1.5}               // Index of refraction
  clearcoat={1}
  clearcoatRoughness={0.1}
/>

// Simple transparency
<meshStandardMaterial
  transparent
  opacity={0.5}
  side={THREE.DoubleSide}
/>
```

## Material Comparison

| Property     | Basic | Lambert | Standard | Physical     |
| ------------ | ----- | ------- | -------- | ------------ |
| Lighting     | No    | Diffuse | PBR      | Advanced PBR |
| Roughness    | No    | No      | Yes      | Yes          |
| Metalness    | No    | No      | Yes      | Yes          |
| Clearcoat    | No    | No      | No       | Yes          |
| Transmission | No    | No      | No       | Yes          |
| GPU Cost     | Low   | Low     | Medium   | High         |

## Anti-Patterns

**DON'T:**

- Use `meshPhysicalMaterial` everywhere (performance killer)
- Create new materials every render
- Forget `side={THREE.DoubleSide}` for visible interiors
- Use transmission without proper scene setup
- Skip texture optimization (uncompressed textures)

**DO:**

- Use simplest material that achieves the look
- Reuse materials across similar objects
- Use `meshBasicMaterial` for distant/small objects
- Compress textures (WebP, basis universal)
- Use material instances with drei

## Performance Tips

```tsx
// Share materials across instances
const sharedMaterial = useMemo(
  () => new THREE.MeshStandardMaterial({ color: 'red' }),
  []
);

// Use for many objects
<mesh material={sharedMaterial}>...</mesh>
<mesh material={sharedMaterial}>...</mesh>
```

## Checklist

Before finalizing materials:

- [ ] Appropriate material type for use case
- [ ] Textures are optimized (compressed, power-of-2)
- [ ] Materials shared where possible
- [ ] Transparent materials have `transparent: true`
- [ ] Double-sided materials explicitly set
- [ ] Shader uniforms use refs for animation

## Reference

- [Three.js Materials](https://threejs.org/docs/#api/en/materials/Material) — Official docs
- `developer/r3f/r3f-fundamentals.md` — R3F basics
- `developer/performance/performance-basics.md` — Optimization
