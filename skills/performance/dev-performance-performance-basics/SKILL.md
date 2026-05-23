---
name: dev-performance-performance-basics
description: Core R3F/Three.js performance optimization principles. Use when FPS drops below 60.
category: performance
---

# Performance Optimization Basics

> "Optimize for mobile, scale up for desktop – 60 FPS is the goal."

## When to Use

Use when:
- FPS drops below 60
- Debugging performance issues
- Starting optimization work

## The 16ms Budget (60 FPS)

| System     | Budget      | Notes                 |
| ---------- | ----------- | --------------------- |
| Input      | ~1ms        | Event handling        |
| Physics    | ~3ms        | Rapier/Cannon updates |
| Game Logic | ~4ms        | State, AI, animations |
| Render     | ~5ms        | Three.js draw calls   |
| Buffer     | ~3ms        | Safety margin         |
| **Total**  | **16.67ms** | 60 FPS target         |

## Quick Start Canvas Config

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

## Decision Framework

| Symptom            | Likely Cause        | Solution            |
| ------------------ | ------------------- | ------------------- |
| Low FPS everywhere | Too many draw calls | Instancing, merging |
| FPS drops on zoom  | LOD not implemented | Add LOD system      |
| Mobile slow        | DPR too high        | Limit to 1.5        |
| Memory grows       | Dispose missing     | Add cleanup         |
| Stuttering         | GC pressure         | Object pooling      |

## Progressive Optimizations

### Level 1: Basic

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

### Level 2: Object Reuse

```tsx
// Reuse Vector3, Quaternion instances
const position = useRef(new THREE.Vector3());
const rotation = useRef(new THREE.Quaternion());

useFrame(() => {
  position.current.set(0, 0, 0); // Reuse, don't create
});
```

### Level 3: Memory Management

```tsx
// CRITICAL: Dispose of Three.js objects
useEffect(() => {
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshStandardMaterial();

  return () => {
    geometry.dispose();
    material.dispose();
    if (material.map) material.map.dispose();
  };
}, []);
```

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

## Anti-Patterns

❌ **DON'T:**
- Create objects inside useFrame
- Skip dispose() calls
- Use shadows on mobile without testing
- Render invisible objects
- Use uncompressed textures

✅ **DO:**
- Reuse Vector3, Quaternion instances
- Always dispose geometries and materials
- Profile before and after optimizations
- Compress textures (WebP, Basis)

## Checklist

- [ ] DPR limited appropriately
- [ ] No object creation in useFrame
- [ ] Dispose called on cleanup
- [ ] Shadows disabled on mobile
- [ ] Textures compressed
- [ ] FPS stable at 60

## Common Performance Killers

1. **Too many draw calls** → Use Instances
2. **High polygon count** → Use LOD
3. **Unoptimized textures** → Compress, resize
4. **No frustum culling** → Enable frustumCulled
5. **Memory leaks** → Call dispose()
6. **GC pressure** → Object pooling

## Reference

- [Three.js Performance Tips](https://threejs.org/manual/#en/optimize-lots-of-objects)
- [instancing.md](./instancing.md) - Instanced rendering
- [lod-systems.md](./lod-systems.md) - LOD techniques
