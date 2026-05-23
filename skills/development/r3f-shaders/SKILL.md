---
name: r3f-shaders
description: React Three Fiber shaders - shaderMaterial, custom GLSL, uniforms. Use when creating custom visual effects or extending materials.
---

# React Three Fiber Shaders

## shaderMaterial (Drei)

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

const WaveMaterial = shaderMaterial(
  // Uniforms
  { time: 0, color: new THREE.Color('hotpink') },
  // Vertex shader
  `uniform float time;
   varying vec2 vUv;
   void main() {
     vUv = uv;
     vec3 pos = position;
     pos.z += sin(pos.x * 10.0 + time) * 0.1;
     gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
   }`,
  // Fragment shader
  `uniform vec3 color;
   varying vec2 vUv;
   void main() {
     gl_FragColor = vec4(color * vUv.y, 1.0);
   }`
)

extend({ WaveMaterial })

function WaveMesh() {
  const ref = useRef()
  useFrame(({ clock }) => {
    ref.current.time = clock.elapsedTime
  })
  return (
    <mesh>
      <planeGeometry args={[5, 5, 32, 32]} />
      <waveMaterial ref={ref} key={WaveMaterial.key} />
    </mesh>
  )
}
```

## Raw ShaderMaterial

```tsx
function CustomShader() {
  const ref = useRef()

  useFrame(({ clock }) => {
    ref.current.uniforms.time.value = clock.elapsedTime
  })

  return (
    <mesh>
      <boxGeometry />
      <shaderMaterial
        ref={ref}
        uniforms={{
          time: { value: 0 },
          color: { value: new THREE.Color('cyan') },
        }}
        vertexShader={`
          varying vec2 vUv;
          void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `}
        fragmentShader={`
          uniform float time;
          uniform vec3 color;
          varying vec2 vUv;
          void main() {
            float strength = sin(vUv.x * 10.0 + time) * 0.5 + 0.5;
            gl_FragColor = vec4(color * strength, 1.0);
          }
        `}
      />
    </mesh>
  )
}
```

## Common Patterns

### Fresnel
```glsl
vec3 viewDir = normalize(cameraPosition - vWorldPosition);
float fresnel = pow(1.0 - dot(viewDir, vNormal), 3.0);
```

### Noise
```glsl
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
}
```

### Gradient
```glsl
vec3 color = mix(colorA, colorB, vUv.y);
```

### Dissolve
```glsl
float noise = texture2D(noiseMap, vUv).r;
if (noise < progress) discard;
```

## Extending Built-in Materials

```tsx
const material = new THREE.MeshStandardMaterial({ color: 'green' })

material.onBeforeCompile = (shader) => {
  shader.uniforms.time = { value: 0 }
  material.userData.shader = shader

  shader.vertexShader = 'uniform float time;\n' + shader.vertexShader
  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    `#include <begin_vertex>
     transformed.y += sin(position.x * 10.0 + time) * 0.1;`
  )
}

// Update in useFrame
if (material.userData.shader) {
  material.userData.shader.uniforms.time.value = clock.elapsedTime
}
```

## TypeScript

```tsx
declare global {
  namespace JSX {
    interface IntrinsicElements {
      waveMaterial: ReactThreeFiber.MaterialNode<
        THREE.ShaderMaterial & { time: number; color: THREE.Color },
        typeof WaveMaterial
      >
    }
  }
}
```

## Performance Tips

- Use `mix`/`step` instead of conditionals
- Precalculate values in JS when possible
- Use textures for complex functions
- Minimize texture lookups
