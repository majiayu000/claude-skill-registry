---
name: ta-vfx-particles
description: GPU particle systems for high-performance visual effects. Use when creating particle effects, instanced rendering, GPU-accelerated VFX.
category: vfx
---

# GPU Particles Skill

> "Millions of particles at 60 FPS – GPU particles unlock impossible effects."

## When to Use This Skill

Use when:

- Creating fire, smoke, spark effects
- Rendering large numbers of particles (>1000)
- Implementing weather systems
- Building magical/sci-fi effects

## Quick Start

```tsx
import { Points, PointMaterial } from '@react-three/drei';

function BasicParticles({ count = 10000 }) {
  const particles = useMemo(() => {
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
    }
    return positions;
  }, [count]);

  return (
    <Points positions={particles}>
      <PointMaterial size={0.05} color="white" />
    </Points>
  );
}
```

## Decision Framework

| Need              | Approach           | Count      |
| ----------------- | ------------------ | ---------- |
| Simple sparks     | CPU particles      | < 500      |
| Fire/smoke        | GPU instanced      | 1K - 10K   |
| Star fields       | GPU points         | 10K - 100K |
| Fluid simulation  | GPU compute shader | 100K+      |

## Progressive Guide

### Level 1: Points with Animation

```tsx
import { Points, PointMaterial } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function AnimatedParticles({ count = 5000 }) {
  const particlesRef = useRef();

  const [positions, colors] = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10;

      // Color gradient based on position
      colors[i * 3] = Math.random();
      colors[i * 3 + 1] = Math.random() * 0.5;
      colors[i * 3 + 2] = 1.0;
    }

    return [positions, colors];
  }, [count]);

  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    }
  });

  return (
    <Points ref={particlesRef} positions={positions} colors={colors}>
      <PointMaterial size={0.05} vertexColors />
    </Points>
  );
}
```

### Level 2: Instanced Mesh Particles

```tsx
import { InstancedMesh } from '@react-three/drei';

function InstancedParticles({ count = 1000 }) {
  const meshRef = useRef();

  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    return Array.from({ length: count }, () => ({
      position: new THREE.Vector3(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      ),
      velocity: new THREE.Vector3(
        (Math.random() - 0.5) * 0.02,
        Math.random() * 0.02,
        (Math.random() - 0.5) * 0.02
      ),
      scale: Math.random() * 0.1 + 0.05,
    }));
  }, [count]);

  useFrame(() => {
    if (!meshRef.current) return;

    particles.forEach((p, i) => {
      // Update position
      p.position.add(p.velocity);

      // Reset if too high
      if (p.position.y > 5) {
        p.position.y = -5;
      }

      dummy.position.copy(p.position);
      dummy.scale.setScalar(p.scale);
      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);
    });

    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <InstancedMesh ref={meshRef} args={[null, null, count]}>
      <sphereGeometry args={[0.05, 8, 8]} />
      <meshStandardMaterial color="orange" />
    </InstancedMesh>
  );
}
```

### Level 3: Shader-Based Particles

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';

const ParticleShaderMaterial = shaderMaterial(
  { uTime: 0, uColor: new THREE.Color(1.0, 0.5, 0.0) },
  // Vertex shader
  `
    uniform float uTime;
    attribute float aScale;
    attribute vec3 aVelocity;
    varying vec3 vColor;

    void main() {
      vColor = position * 0.5 + 0.5;

      // Animate based on time and velocity
      vec3 pos = position;
      pos += aVelocity * uTime;
      pos.y = mod(pos.y + 5.0, 10.0) - 5.0;

      vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
      gl_PointSize = aScale * (300.0 / -mvPosition.z);
      gl_Position = projectionMatrix * mvPosition;
    }
  `,
  // Fragment shader
  `
    uniform vec3 uColor;
    varying vec3 vColor;

    void main() {
      // Circular particle
      vec2 center = gl_PointCoord - vec2(0.5);
      float dist = length(center);
      if (dist > 0.5) discard;

      // Soft edge
      float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
      gl_FragColor = vec4(uColor * vColor, alpha);
    }
  `
);

extend({ ParticleShaderMaterial });

function ShaderParticles({ count = 10000 }) {
  const materialRef = useRef();

  const [positions, velocities, scales] = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const velocities = new Float32Array(count * 3);
    const scales = new Float32Array(count);

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10;

      velocities[i * 3] = (Math.random() - 0.5) * 0.1;
      velocities[i * 3 + 1] = Math.random() * 0.2;
      velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.1;

      scales[i] = Math.random() * 20.0 + 10.0;
    }

    return [positions, velocities, scales];
  }, [count]);

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

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
          attach="attributes-aVelocity"
          count={count}
          array={velocities}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-aScale"
          count={count}
          array={scales}
          itemSize={1}
        />
      </bufferGeometry>
      <particleShaderMaterial ref={materialRef} transparent />
    </points>
  );
}
```

### Level 4: Fire Particle System

```tsx
function FireParticles({ count = 500 }) {
  const particles = useRef([]);

  const createParticle = () => ({
    position: new THREE.Vector3(
      (Math.random() - 0.5) * 2,
      0,
      (Math.random() - 0.5) * 2
    ),
    velocity: new THREE.Vector3(
      (Math.random() - 0.5) * 0.02,
      Math.random() * 0.05 + 0.02,
      (Math.random() - 0.5) * 0.02
    ),
    life: Math.random(),
    maxLife: Math.random() * 2 + 1,
    size: Math.random() * 0.1 + 0.05,
  });

  // Initialize particles
  useMemo(() => {
    for (let i = 0; i < count; i++) {
      particles.current.push(createParticle());
    }
  }, [count]);

  const geometry = useMemo(() => new THREE.BufferGeometry(), []);
  const positions = useMemo(() => new Float32Array(count * 3), [count]);
  const colors = useMemo(() => new Float32Array(count * 3), [count]);
  const sizes = useMemo(() => new Float32Array(count), [count]);

  useFrame(() => {
    particles.current.forEach((p, i) => {
      // Update
      p.life -= 0.016;
      if (p.life <= 0) {
        Object.assign(p, createParticle());
      }

      p.position.add(p.velocity);

      positions[i * 3] = p.position.x;
      positions[i * 3 + 1] = p.position.y;
      positions[i * 3 + 2] = p.position.z;

      // Color gradient: white -> yellow -> orange -> red
      const t = p.life / p.maxLife;
      if (t > 0.7) {
        colors[i * 3] = 1.0;
        colors[i * 3 + 1] = 1.0;
        colors[i * 3 + 2] = 0.5;
      } else if (t > 0.4) {
        colors[i * 3] = 1.0;
        colors[i * 3 + 1] = 0.5;
        colors[i * 3 + 2] = 0.0;
      } else {
        colors[i * 3] = 1.0;
        colors[i * 3 + 1] = 0.0;
        colors[i * 3 + 2] = 0.0;
      }

      sizes[i] = p.size * (p.life / p.maxLife);
    });

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    geometry.attributes.position.needsUpdate = true;
    geometry.attributes.color.needsUpdate = true;
    geometry.attributes.size.needsUpdate = true;
  });

  return (
    <points geometry={geometry}>
      <pointsMaterial
        size={0.1}
        vertexColors
        transparent
        opacity={0.8}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
}
```

## Particle Texture

```tsx
// Create soft particle texture
const createParticleTexture = () => {
  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext('2d');

  const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, 'rgba(255,255,255,1)');
  gradient.addColorStop(0.5, 'rgba(255,255,255,0.5)');
  gradient.addColorStop(1, 'rgba(255,255,255,0)');

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 64, 64);

  return new THREE.CanvasTexture(canvas);
};
```

## Anti-Patterns

❌ **DON'T:**

- Create new objects inside particle loop
- Use CPU particles for >1000 particles
- Enable depthWrite on additive particles
- Forget to reset particle life

✅ **DO:**

- Use object pooling
- Pre-allocate typed arrays
- Use additive blending for glow effects
- Disable depth write for transparent particles

## Checklist

Before implementing particle system:

- [ ] Particle count appropriate for effect
- [ ] GPU-based for >1000 particles
- [ ] Texture created for soft particles
- [ ] Blending mode set correctly
- [ ] Performance tested on target hardware

## Common Effects

| Effect    | Blend Mode              | Motion      | Color              |
| --------- | ----------------------- | ----------- | ------------------ |
| Fire      | Additive                | Up + noise  | White→Yellow→Red   |
| Smoke     | Normal/Alpha            | Up + spread | Grey gradient      |
| Sparks    | Additive                | Arc + gravity | Gold/White       |
| Snow      | Alpha                   | Fall + sway | White              |
| Dust      | Alpha                   | Float       | Brown/Grey         |
| Magic     | Additive                | Spiral/in   | Purple/Blue        |

## Related Skills

For R3F fundamentals: `Skill("ta-r3f-fundamentals")`
For post-processing: `Skill("ta-vfx-postfx")`

## External References

- [Three.js Points](https://threejs.org/docs/#api/en/objects/Points)
