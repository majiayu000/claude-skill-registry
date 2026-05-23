---
name: dev-performance-instancing
description: Instanced rendering for repeated objects in R3F. Use when rendering many identical objects.
category: performance
---

# Instanced Rendering

Render thousands of identical objects with a single draw call.

## When to Use

Use when:
- Rendering many identical objects (trees, grass, particles)
- Draw calls exceed 100
- Objects share same geometry and material

## Quick Start

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

## Performance Impact

| Approach | Objects | Draw Calls | FPS |
|----------|---------|------------|-----|
| Individual meshes | 1000 | 1000 | 15 |
| Instanced | 1000 | 1 | 60 |

## Dynamic Instancing

```tsx
import { Instances, Instance } from '@react-three/drei';

function DynamicParticles({ count = 100 }) {
  const particles = useRef<Array<{ x: number; y: number; z: number }>>([]);

  // Initialize particles
  useMemo(() => {
    for (let i = 0; i < count; i++) {
      particles.current.push({
        x: (Math.random() - 0.5) * 10,
        y: (Math.random() - 0.5) * 10,
        z: (Math.random() - 0.5) * 10,
      });
    }
  }, [count]);

  return (
    <Instances limit={count}>
      <sphereGeometry args={[0.1, 8, 8]} />
      <meshBasicMaterial color="orange" />
      {particles.current.map((pos, i) => (
        <Instance key={i} position={[pos.x, pos.y, pos.z]} />
      ))}
    </Instances>
  );
}
```

## Instancing with Colors

```tsx
function ColoredInstances() {
  const colors = useMemo(() =>
    Array.from({ length: 100 }, () => ({
      color: new THREE.Color(Math.random(), Math.random(), Math.random()),
    }))
  , []);

  return (
    <Instances limit={100}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial />
      {colors.map((props, i) => (
        <Instance
          key={i}
          position={[(i % 10) * 1.2, Math.floor(i / 10) * 1.2, 0]}
          color={props.color}
        />
      ))}
    </Instances>
  );
}
```

## Limitations

| ❌ Can't | ✅ Alternative |
|----------|----------------|
| Different geometries per instance | Use separate Instances groups |
| Different materials per instance | Use vertex colors or textures |
| Complex animations per instance | Use shader-based animation |

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Using individual meshes for repeated objects | Use Instances |
| Not setting limit prop | Always set limit higher than max count |
| Creating new Instance objects every frame | Use stable key, update position prop |

## When NOT to Use

- Objects have different geometries
- Objects have different materials
- Less than ~50 identical objects
- Objects need individual complex animations

## Reference

- [performance-basics.md](./performance-basics.md) - Core optimization
- [lod-systems.md](./lod-systems.md) - LOD techniques
