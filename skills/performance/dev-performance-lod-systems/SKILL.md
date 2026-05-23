---
name: dev-performance-lod-systems
description: Level of Detail (LOD) techniques for R3F. Use when complex models cause FPS drops.
category: performance
---

# Level of Detail (LOD)

Reduce polygon count based on distance from camera.

## When to Use

Use when:
- FPS drops on zoom out
- Complex models in large scenes
- Mobile devices struggling

## Quick Start

```tsx
import { Detailed } from '@react-three/drei';

function LODTree({ position }) {
  return (
    <Detailed distances={[0, 20, 50, 100]} position={position}>
      {/* Closest - high detail */}
      <HighDetailTree />
      {/* Medium distance */}
      <MediumDetailTree />
      {/* Far - low detail */}
      <LowDetailTree />
      {/* Very far - billboard */}
      <mesh>
        <planeGeometry args={[1, 2]} />
        <meshBasicMaterial map={treeBillboard} transparent />
      </mesh>
    </Detailed>
  );
}
```

## Distance Guidelines

| Distance | Detail Level | Polygons | Use Case |
|----------|-------------|----------|----------|
| 0-10m | High | 10,000+ | Close inspection |
| 10-30m | Medium | 1,000-5,000 | Normal gameplay |
| 30-60m | Low | 100-500 | Background |
| 60m+ | Billboard | 2 triangles | Distant objects |

## LOD Component Models

```tsx
// High detail - close inspection only
function HighDetailTree() {
  return (
    <group>
      <mesh>
        {/* Full trunk with bark texture */}
        <cylinderGeometry args={[0.3, 0.5, 4, 16]} />
        <meshStandardMaterial map={barkTexture} />
      </mesh>
      <mesh position={[0, 2, 0]}>
        {/* Dense foliage */}
        <coneGeometry args={[2, 4, 8]} />
        <meshStandardMaterial map={leafTexture} />
      </mesh>
    </group>
  );
}

// Medium detail - gameplay distance
function MediumDetailTree() {
  return (
    <group>
      <mesh>
        {/* Simplified trunk */}
        <cylinderGeometry args={[0.25, 0.4, 4, 8]} />
        <meshStandardMaterial color="brown" />
      </mesh>
      <mesh position={[0, 2, 0]}>
        {/* Simplified foliage */}
        <coneGeometry args={[1.8, 4, 6]} />
        <meshStandardMaterial color="green" />
      </mesh>
    </group>
  );
}

// Low detail - background
function LowDetailTree() {
  return (
    <mesh>
      {/* Single merged geometry */}
      <cylinderGeometry args={[0.2, 1.5, 4, 6]} />
      <meshStandardMaterial color="darkgreen" />
    </mesh>
  );
}

// Billboard - very distant
function BillboardTree() {
  return (
    <mesh>
      <planeGeometry args={[1, 3]} />
      <meshBasicMaterial map={treeBillboard} transparent />
    </mesh>
  );
}
```

## Automatic LOD Generation

```tsx
import { useGLTF } from '@react-three/drei';

function AutoLOD({ modelPath }) {
  const { scene: highDetail } = useGLTF(`${modelPath}_high.glb`);
  const { scene: mediumDetail } = useGLTF(`${modelPath}_medium.glb`);
  const { scene: lowDetail } = useGLTF(`${modelPath}_low.glb`);

  return (
    <Detailed distances={[0, 15, 40]}>
      <primitive object={highDetail.clone()} />
      <primitive object={mediumDetail.clone()} />
      <primitive object={lowDetail.clone()} />
    </Detailed>
  );
}
```

## LOD with Skeletal Animation

```tsx
// Animated characters need special handling
function LODCharacter() {
  // High detail: full rig, many bones
  // Low detail: simplified rig, fewer bones
  // LODs must share animation structure

  const highDetail = useGLTF('/character_high.glb');
  const lowDetail = useGLTF('/character_low.glb');

  // Clone animations to both models
  const animations = highDetail.animations;

  return (
    <Detailed distances={[0, 25]}>
      <primitive object={highDetail.scene} animations={animations} />
      <primitive object={lowDetail.scene} animations={animations} />
    </Detailed>
  );
}
```

## Billboard Optimization

```tsx
// Use billboards for very distant objects
function BillboardSprite({ texture, position }) {
  const mesh = useRef<THREE.Mesh>(null);

  useFrame(({ camera }) => {
    if (mesh.current) {
      // Always face camera
      mesh.current.quaternion.copy(camera.quaternion);
    }
  });

  return (
    <mesh ref={mesh} position={position}>
      <planeGeometry args={[2, 2]} />
      <meshBasicMaterial map={texture} transparent />
    </mesh>
  );
}
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Too many LOD levels (>4) | 3-4 levels is sufficient |
| Abrupt distance transitions | Smooth distances (overlap) |
| No billboard for distant objects | Use 2-triangle billboards |
| Creating LODs manually | Use tools like SimplyGLTF |

## LOD Creation Tools

- **SimplyGLTF** - Online LOD generator
- **Blender** - Manual decimation modifier
- **meshoptimizer** - Command-line tool

## Reference

- [performance-basics.md](./performance-basics.md) - Core optimization
- [instancing.md](./instancing.md) - Instanced rendering
