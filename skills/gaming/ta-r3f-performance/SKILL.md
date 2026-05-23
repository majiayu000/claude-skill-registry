---
name: ta-r3f-performance
description: Performance optimization techniques for R3F and Three.js. Use when optimizing frame rate, reducing draw calls, mobile performance.
category: performance
---
# R3F Performance Skill

> "Optimize for mobile, scale up for desktop – 60 FPS is the goal."

## When to Use This Skill

Use when:

- FPS drops below 60
- Targeting mobile devices
- Rendering many objects
- Implementing LOD systems
- Debugging performance issues

## Quick Start

```tsx
// Performance-optimized Canvas
<Canvas
  dpr={[1, 2]} // Limit pixel ratio
  performance={{ min: 0.5 }} // Auto-reduce quality
  gl={{ antialias: false }} // Disable for mobile
>
  <Suspense fallback={null}>
    <Scene />
  </Suspense>
</Canvas>
```

## The 16ms Budget (60 FPS)

| System     | Budget      | Notes                 |
| ---------- | ----------- | --------------------- |
| Input      | ~1ms        | Event handling        |
| Physics    | ~3ms        | Rapier/Cannon updates |
| Game Logic | ~4ms        | State, AI, animations |
| Render     | ~5ms        | Three.js draw calls   |
| Buffer     | ~3ms        | Safety margin         |
| **Total**  | **16.67ms** | 60 FPS target         |

## Performance Monitoring Setup

Always establish performance monitoring before optimizing. Use Stats.js from drei:

```tsx
import { Stats } from '@react-three/drei';

function Scene() {
  const showStats = import.meta.env.DEV;

  return (
    <>
      {showStats && <Stats />}
      {/* Your scene content */}
    </>
  );
}

// In App.tsx
<Canvas>
  <Stats className="stats-position" />
  <Scene />
</Canvas>
```

### CSS for Stats Positioning

```css
.stats-position {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000;
}
```

### Performance Benchmarks to Establish

| Metric          | Target    | How to Measure        |
| --------------- | --------- | --------------------- |
| FPS             | 60+       | Stats.js              |
| Frame Time      | <16.67ms  | Stats.js MS           |
| Draw Calls      | <100      | renderer.info.render.calls |
| Triangles       | <100k     | renderer.info.render.triangles |
| Textures        | <50MB     | renderer.info.memory.textures |
| Geometries      | <20MB     | renderer.info.memory.geometries |

### Reading Renderer Info (Development)

```tsx
import { useThree } from '@react-three/fiber';

function PerfMonitor() {
  const { gl } = useThree();

  useEffect(() => {
    if (!import.meta.env.DEV) return;

    const info = gl.info;
    console.log('Render Info:', {
      calls: info.render.calls,
      triangles: info.render.triangles,
      points: info.render.points,
      lines: info.render.lines,
      textures: info.memory.textures,
      geometries: info.memory.geometries,
    });
  }, [gl]);

  return null;
}
```

## Decision Framework

| Symptom            | Likely Cause        | Solution            |
| ------------------ | ------------------- | ------------------- |
| Low FPS everywhere | Too many draw calls | Instancing, merging |
| FPS drops on zoom  | LOD not implemented | Add LOD system      |
| Mobile slow        | DPR too high        | Limit to 1.5        |
| Memory grows       | Dispose missing     | Add cleanup         |
| Stuttering         | GC pressure         | Object pooling      |

## Progressive Guide

### Level 1: Basic Optimizations

```tsx
// Limit device pixel ratio
<Canvas dpr={Math.min(window.devicePixelRatio, 2)}>

// Disable expensive features on mobile
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

<Canvas
  shadows={!isMobile}
  gl={{
    antialias: !isMobile,
    powerPreference: 'high-performance',
  }}
>
```

### Level 2: Instanced Rendering

```tsx
import { Instances, Instance } from '@react-three/drei';

// Instead of 1000 separate meshes
function OptimizedTrees({ positions }) {
  return (
    <Instances limit={positions.length}>
      <cylinderGeometry args={[0.1, 0.3, 2]} />
      <meshStandardMaterial color="brown" />
      {positions.map((pos, i) => (
        <Instance key={i} position={pos} />
      ))}
    </Instances>
  );
}
```

### Level 3: Level of Detail (LOD)

#### Using Drei's `<Detailed>` Component

```tsx
import { Detailed, useGLTF } from '@react-three/drei';

function LODTree({ position }: { position: [number, number, number] }) {
  // Load all LOD levels at once
  const [low, mid, high] = useGLTF([
    '/assets/models/tree-low.glb',
    '/assets/models/tree-mid.glb',
    '/assets/models/tree-high.glb',
  ]);

  return (
    <Detailed
      distances={[0, 10, 30]}  // Distance thresholds for each LOD
      position={position}
    >
      {/* 0-10 units: High detail */}
      <primitive object={high.scene} />
      {/* 10-30 units: Medium detail */}
      <primitive object={mid.scene} />
      {/* 30+ units: Low detail */}
      <primitive object={low.scene} />
    </Detailed>
  );
}
```

#### Using Native Three.js LOD

```tsx
import { useRef, useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

function NativeLODTree({ position }: { position: [number, number, number] }) {
  const lodRef = useRef<THREE.LOD>(null);
  const [low, mid, high] = useGLTF([
    '/assets/models/tree-low.glb',
    '/assets/models/tree-mid.glb',
    '/assets/models/tree-high.glb',
  ]);

  useEffect(() => {
    if (!lodRef.current) return;

    // Add LOD levels with distance thresholds
    lodRef.current.addLevel(high.scene.clone(), 0);    // 0-10 units
    lodRef.current.addLevel(mid.scene.clone(), 10);   // 10-30 units
    lodRef.current.addLevel(low.scene.clone(), 30);   // 30+ units

    // Optional: Auto-update LOD based on camera
    lodRef.current.update(camera);
  }, [high, mid, low]);

  return <lod ref={lodRef} position={position} />;
}
```

#### Billboard LOD for Distance Objects

```tsx
import { useRef, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { TextureLoader } from 'three';

function BillboardLOD({
  textureUrl,
  position,
}: {
  textureUrl: string;
  position: [number, number, number];
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const texture = new TextureLoader().load(textureUrl);
  const { camera } = useThree();

  // Make billboard always face camera
  useFrame(() => {
    if (meshRef.current && camera) {
      meshRef.current.lookAt(camera.position);
    }
  });

  return (
    <mesh ref={meshRef} position={position}>
      <planeGeometry args={[2, 4]} />
      <meshBasicMaterial
        map={texture}
        transparent
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}
```

#### LOD Distance Guidelines

| Object Type | Near (High) | Mid | Far (Low) | Billboard |
| ----------- | ----------- | ------- | --------- | --------- |
| Trees | 0-15m | 15-40m | 40-100m | 100m+ |
| Buildings | 0-20m | 20-60m | 60-150m | 150m+ |
| Characters | 0-10m | 10-25m | 25-50m | - |
| Props | 0-10m | 10-30m | 30m+ | - |

#### Polygon Budget per LOD Level

| Asset | LOD0 (Near) | LOD1 (Mid) | LOD2 (Far) | Billboard |
| ----- | ----------- | ---------- | ---------- | --------- |
| Character | 15K tris | 5K tris | 1K tris | N/A |
| Vehicle | 20K tris | 8K tris | 2K tris | N/A |
| Tree | 5K tris | 1K tris | 500 tris | 2 tris |
| Building | 10K tris | 3K tris | 1K tris | 2 tris |

**Learned from bugfix-005 retrospective (2026-01-22)**:
- LOD systems reduce GPU workload for distant objects
- Use `<Detailed>` from Drei for simpler React integration
- Consider billboards for very distant objects (trees, props)

### Level 4: Frustum Culling & BVH

```tsx
import { useBVH } from '@react-three/drei';

function OptimizedMesh() {
  const meshRef = useRef();

  // Enable BVH for faster raycasting
  useBVH(meshRef);

  return (
    <mesh ref={meshRef} frustumCulled>
      <complexGeometry />
      <meshStandardMaterial />
    </mesh>
  );
}
```

### Level 5: Object Pooling

```tsx
// Pool for frequently created/destroyed objects
const bulletPool = useMemo(() => {
  const pool = [];
  for (let i = 0; i < 100; i++) {
    pool.push({
      active: false,
      position: new THREE.Vector3(),
      velocity: new THREE.Vector3(),
    });
  }
  return pool;
}, []);

function getBullet() {
  return bulletPool.find((b) => !b.active);
}

function releaseBullet(bullet) {
  bullet.active = false;
}
```

## Mobile Optimization

| Feature         | Desktop | Mobile  |
| --------------- | ------- | ------- |
| Pixel Ratio     | 2.0     | 1.0-1.5 |
| Shadows         | On      | Off     |
| Anti-aliasing   | MSAA    | Off     |
| Post-processing | Full    | Minimal |
| Draw calls      | < 200   | < 50    |
| Polygons        | < 1M    | < 100K  |

```tsx
// Mobile detection and config
const config = useMemo(() => {
  const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);
  return {
    dpr: isMobile ? 1 : Math.min(window.devicePixelRatio, 2),
    shadows: !isMobile,
    antialias: !isMobile,
    maxDrawCalls: isMobile ? 50 : 200,
  };
}, []);
```

## Memory Management

```tsx
// CRITICAL: Dispose of Three.js objects
useEffect(() => {
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshStandardMaterial();

  return () => {
    geometry.dispose();
    material.dispose();
    // Also dispose textures
    if (material.map) material.map.dispose();
  };
}, []);
```

## Anti-Patterns

❌ **DON'T:**

- Create objects inside useFrame
- Use high polygon models without LOD
- Skip dispose() calls
- Use shadows on mobile without testing
- Render invisible objects
- Use uncompressed textures

✅ **DO:**

- Reuse Vector3, Quaternion instances
- Implement LOD for complex scenes
- Always dispose geometries and materials
- Profile before and after optimizations
- Use Instances for repeated objects
- Compress textures (WebP, Basis)

## Performance Monitoring

```tsx
import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';

function PerformanceMonitor() {
  const frameCount = useRef(0);
  const lastTime = useRef(performance.now());

  useFrame(() => {
    frameCount.current++;

    const now = performance.now();
    if (now - lastTime.current >= 1000) {
      console.log(`FPS: ${frameCount.current}`);
      frameCount.current = 0;
      lastTime.current = now;
    }
  });

  return null;
}
```

## Checklist

Performance review:

- [ ] DPR limited appropriately
- [ ] Instancing used for repeated objects
- [ ] LOD implemented for complex models
- [ ] Dispose called on cleanup
- [ ] No object creation in useFrame
- [ ] Shadows disabled on mobile
- [ ] Textures compressed
- [ ] Draw calls under budget
- [ ] FPS stable at 60

## Common Performance Killers

1. **Too many draw calls** → Use Instances
2. **High polygon count** → Use LOD
3. **Unoptimized textures** → Compress, resize
4. **No frustum culling** → Enable frustumCulled
5. **Memory leaks** → Call dispose()
6. **GC pressure** → Object pooling
7. **Expensive shaders** → Simplify, use mobile variants
8. **Post-processing** → Limit on mobile

## Related Skills

For R3F fundamentals: `Skill("ta-r3f-fundamentals")`
For material optimization: `Skill("ta-r3f-materials")`

## External References

- [Three.js Performance Tips](https://threejs.org/manual/#en/optimize-lots-of-objects)
