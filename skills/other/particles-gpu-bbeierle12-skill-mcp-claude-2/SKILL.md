---
name: particles-gpu
description: GPU-based particle systems using instanced rendering, buffer attributes, Points geometry, and custom shaders. Use when rendering thousands to millions of particles efficiently, creating particle effects like snow, rain, stars, or abstract visualizations.
---

# GPU Particles

Render massive particle counts (10k-1M+) efficiently using GPU instancing and custom shaders.

## Quick Start

```tsx
import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function Particles({ count = 10000 }) {
  const points = useRef<THREE.Points>(null!);
  
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
    }
    return pos;
  }, [count]);
  
  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.05} color="#ffffff" />
    </points>
  );
}
```

## Rendering Approaches

| Approach | Particle Count | Complexity | Use Case |
|----------|---------------|------------|----------|
| Points | 10k - 500k | Low | Simple particles, stars |
| Instanced Mesh | 1k - 100k | Medium | 3D geometry particles |
| Custom Shader | 100k - 10M | High | Maximum control |

## Points Geometry

Simplest approach—each particle is a screen-facing point sprite.

### Basic Points

```tsx
function BasicPoints({ count = 5000 }) {
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = Math.cbrt(Math.random()) * 5;
      
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);
    }
    return pos;
  }, [count]);
  
  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.1}
        sizeAttenuation={true}
        transparent={true}
        opacity={0.8}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}
```

### Points with Texture

```tsx
function TexturedPoints({ count = 5000 }) {
  const texture = useTexture('/particle.png');
  
  return (
    <points>
      <bufferGeometry>
        {/* ... positions ... */}
      </bufferGeometry>
      <pointsMaterial
        size={0.5}
        map={texture}
        transparent={true}
        alphaTest={0.01}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}
```

## Custom Attributes

Add per-particle data like color, size, velocity:

```tsx
function ColoredParticles({ count = 10000 }) {
  const { positions, colors, sizes } = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const siz = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      // Position
      pos[i * 3] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
      
      // Color (HSL to RGB)
      const color = new THREE.Color();
      color.setHSL(Math.random(), 0.8, 0.5);
      col[i * 3] = color.r;
      col[i * 3 + 1] = color.g;
      col[i * 3 + 2] = color.b;
      
      // Size
      siz[i] = 0.05 + Math.random() * 0.1;
    }
    
    return { positions: pos, colors: col, sizes: siz };
  }, [count]);
  
  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={count}
          array={colors}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-size"
          count={count}
          array={sizes}
          itemSize={1}
        />
      </bufferGeometry>
      <pointsMaterial
        vertexColors
        size={0.1}
        sizeAttenuation
        transparent
        depthWrite={false}
      />
    </points>
  );
}
```

## Custom Shader Particles

Maximum control over particle appearance and animation:

```tsx
const vertexShader = `
  attribute float aSize;
  attribute vec3 aColor;
  attribute float aAlpha;
  
  uniform float uTime;
  uniform float uPixelRatio;
  
  varying vec3 vColor;
  varying float vAlpha;
  
  void main() {
    vColor = aColor;
    vAlpha = aAlpha;
    
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    
    // Size attenuation
    gl_PointSize = aSize * uPixelRatio * (300.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

const fragmentShader = `
  varying vec3 vColor;
  varying float vAlpha;
  
  void main() {
    // Circular particle
    float dist = length(gl_PointCoord - 0.5);
    if (dist > 0.5) discard;
    
    // Soft edge
    float alpha = 1.0 - smoothstep(0.4, 0.5, dist);
    
    gl_FragColor = vec4(vColor, alpha * vAlpha);
  }
`;

function ShaderParticles({ count = 50000 }) {
  const points = useRef<THREE.Points>(null!);
  
  const { positions, sizes, colors, alphas } = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const siz = new Float32Array(count);
    const col = new Float32Array(count * 3);
    const alp = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 20;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 20;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 20;
      
      siz[i] = 10 + Math.random() * 20;
      
      const color = new THREE.Color();
      color.setHSL(0.6 + Math.random() * 0.2, 0.8, 0.5);
      col[i * 3] = color.r;
      col[i * 3 + 1] = color.g;
      col[i * 3 + 2] = color.b;
      
      alp[i] = 0.3 + Math.random() * 0.7;
    }
    
    return { positions: pos, sizes: siz, colors: col, alphas: alp };
  }, [count]);
  
  useFrame(({ clock }) => {
    points.current.material.uniforms.uTime.value = clock.elapsedTime;
  });
  
  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
        <bufferAttribute attach="attributes-aSize" count={count} array={sizes} itemSize={1} />
        <bufferAttribute attach="attributes-aColor" count={count} array={colors} itemSize={3} />
        <bufferAttribute attach="attributes-aAlpha" count={count} array={alphas} itemSize={1} />
      </bufferGeometry>
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={{
          uTime: { value: 0 },
          uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) }
        }}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}
```

## Animated Particles

### Position Animation in Shader

```glsl
// Vertex shader with animation
attribute vec3 aVelocity;
attribute float aPhase;

uniform float uTime;

void main() {
  vec3 pos = position;
  
  // Simple oscillation
  pos.y += sin(uTime * 2.0 + aPhase) * 0.5;
  
  // Velocity-based movement
  pos += aVelocity * uTime;
  
  // Wrap around bounds
  pos = mod(pos + 10.0, 20.0) - 10.0;
  
  vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
  gl_PointSize = 10.0 * (300.0 / -mvPosition.z);
  gl_Position = projectionMatrix * mvPosition;
}
```

### CPU Animation (for dynamic systems)

```tsx
function AnimatedParticles({ count = 10000 }) {
  const points = useRef<THREE.Points>(null!);
  
  const velocities = useMemo(() => {
    const vel = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      vel[i * 3] = (Math.random() - 0.5) * 0.02;
      vel[i * 3 + 1] = (Math.random() - 0.5) * 0.02;
      vel[i * 3 + 2] = (Math.random() - 0.5) * 0.02;
    }
    return vel;
  }, [count]);
  
  useFrame(() => {
    const positions = points.current.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < count; i++) {
      positions[i * 3] += velocities[i * 3];
      positions[i * 3 + 1] += velocities[i * 3 + 1];
      positions[i * 3 + 2] += velocities[i * 3 + 2];
      
      // Wrap around
      for (let j = 0; j < 3; j++) {
        if (positions[i * 3 + j] > 5) positions[i * 3 + j] = -5;
        if (positions[i * 3 + j] < -5) positions[i * 3 + j] = 5;
      }
    }
    
    points.current.geometry.attributes.position.needsUpdate = true;
  });
  
  // ... geometry setup
}
```

## Instanced Mesh Particles

For 3D geometry particles (not just points):

```tsx
function InstancedParticles({ count = 1000 }) {
  const mesh = useRef<THREE.InstancedMesh>(null!);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  
  useEffect(() => {
    for (let i = 0; i < count; i++) {
      dummy.position.set(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      );
      dummy.rotation.set(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        0
      );
      dummy.scale.setScalar(0.05 + Math.random() * 0.1);
      dummy.updateMatrix();
      mesh.current.setMatrixAt(i, dummy.matrix);
    }
    mesh.current.instanceMatrix.needsUpdate = true;
  }, [count, dummy]);
  
  useFrame(({ clock }) => {
    for (let i = 0; i < count; i++) {
      mesh.current.getMatrixAt(i, dummy.matrix);
      dummy.matrix.decompose(dummy.position, dummy.quaternion, dummy.scale);
      
      dummy.rotation.x += 0.01;
      dummy.rotation.y += 0.01;
      
      dummy.updateMatrix();
      mesh.current.setMatrixAt(i, dummy.matrix);
    }
    mesh.current.instanceMatrix.needsUpdate = true;
  });
  
  return (
    <instancedMesh ref={mesh} args={[undefined, undefined, count]}>
      <icosahedronGeometry args={[1, 0]} />
      <meshStandardMaterial color="#ff6b6b" />
    </instancedMesh>
  );
}
```

## Buffer Geometry Patterns

### Sphere Distribution

```tsx
function spherePositions(count: number, radius: number) {
  const positions = new Float32Array(count * 3);
  
  for (let i = 0; i < count; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = Math.cbrt(Math.random()) * radius;  // Cube root for uniform volume
    
    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);
  }
  
  return positions;
}
```

### Galaxy Spiral

```tsx
function galaxyPositions(count: number, arms: number, spin: number) {
  const positions = new Float32Array(count * 3);
  
  for (let i = 0; i < count; i++) {
    const armIndex = i % arms;
    const armAngle = (armIndex / arms) * Math.PI * 2;
    
    const radius = Math.random() * 5;
    const spinAngle = radius * spin;
    const angle = armAngle + spinAngle;
    
    // Add randomness
    const randomX = (Math.random() - 0.5) * 0.5 * radius;
    const randomY = (Math.random() - 0.5) * 0.2;
    const randomZ = (Math.random() - 0.5) * 0.5 * radius;
    
    positions[i * 3] = Math.cos(angle) * radius + randomX;
    positions[i * 3 + 1] = randomY;
    positions[i * 3 + 2] = Math.sin(angle) * radius + randomZ;
  }
  
  return positions;
}
```

### Grid Distribution

```tsx
function gridPositions(countPerAxis: number, spacing: number) {
  const count = countPerAxis ** 3;
  const positions = new Float32Array(count * 3);
  const offset = (countPerAxis - 1) * spacing * 0.5;
  
  let index = 0;
  for (let x = 0; x < countPerAxis; x++) {
    for (let y = 0; y < countPerAxis; y++) {
      for (let z = 0; z < countPerAxis; z++) {
        positions[index * 3] = x * spacing - offset;
        positions[index * 3 + 1] = y * spacing - offset;
        positions[index * 3 + 2] = z * spacing - offset;
        index++;
      }
    }
  }
  
  return positions;
}
```

## Performance Tips

| Technique | Impact |
|-----------|--------|
| Use Points over InstancedMesh | 5-10x faster for simple particles |
| GPU animation (shader) vs CPU | 10-100x faster at scale |
| Disable depthWrite | Faster blending |
| Use Float32Array | Required for buffers |
| Frustum culling (default on) | Skip off-screen |

### Optimal Settings

```tsx
<pointsMaterial
  transparent
  depthWrite={false}           // Faster blending
  blending={THREE.AdditiveBlending}  // Good for glowing particles
  sizeAttenuation              // Perspective-correct size
/>
```

## File Structure

```
particles-gpu/
├── SKILL.md
├── references/
│   ├── buffer-patterns.md     # Distribution patterns
│   └── shader-examples.md     # Complete shader examples
└── scripts/
    ├── particles/
    │   ├── basic-points.tsx   # Simple points setup
    │   ├── shader-points.tsx  # Custom shader particles
    │   └── instanced.tsx      # Instanced mesh particles
    └── distributions/
        ├── sphere.ts          # Sphere distribution
        ├── galaxy.ts          # Galaxy spiral
        └── grid.ts            # Grid distribution
```

## Reference

- `references/buffer-patterns.md` — Position distribution patterns
- `references/shader-examples.md` — Complete particle shaders
