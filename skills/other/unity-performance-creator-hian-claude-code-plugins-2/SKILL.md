---
name: unity-performance
description: Optimize Unity game performance through profiling, draw call reduction, and resource management. Masters batching, LOD, occlusion culling, and mobile optimization. Use for performance bottlenecks, frame rate issues, or optimization strategies.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity Performance Optimization

## Overview

Performance optimization for Unity games focusing on profiling and systematic optimization.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType, null-safe coding)

**Core Topics**:
- Unity Profiler analysis
- Draw call reduction
- GPU instancing and SRP Batcher
- LOD (Level of Detail)
- Occlusion culling
- Object pooling
- Memory optimization

## Quick Start

### Collection & Object Pooling

GC-free pooling is critical for performance. Use Unity's built-in `UnityEngine.Pool` namespace (2021.1+):

```csharp
using UnityEngine.Pool;

// Temporary collection pooling - eliminates GC spikes
List<Enemy> enemies;
using (ListPool<Enemy>.Get(out enemies))
{
    GetComponentsInChildren(enemies);
    ProcessEnemies(enemies);
} // Auto-released
```

> **See `unity-collection-pool` skill** for comprehensive patterns:
> - ListPool, HashSetPool, DictionaryPool for temporary collections
> - ObjectPool<T> for component/prefab pooling
> - Advanced patterns: Keyed pools, auto-return, ECS integration

## Performance Targets

- **Mobile**: 30-60 FPS, <100 draw calls
- **Desktop**: 60+ FPS, <500 draw calls
- **VR**: 90 FPS minimum, <200 draw calls

## Profiling Workflow

1. **Profile first**: Identify actual bottleneck (CPU/GPU/Memory)
2. **Measure baseline**: Record before optimization
3. **Optimize bottleneck**: Focus on biggest impact
4. **Measure improvement**: Validate changes
5. **Repeat**: Until target performance reached

## Optimization Checklist

### CPU Optimization
- ✅ Reduce Update/FixedUpdate calls
- ✅ Object pooling for frequently spawned objects
- ✅ Cache component references in Awake/Start
- ✅ Use events instead of polling

### GPU Optimization
- ✅ Static batching for static objects
- ✅ GPU instancing for identical meshes
- ✅ Reduce SetPass calls via material sharing
- ✅ LOD groups for distant objects
- ✅ Occlusion culling for large scenes

### Memory Optimization
- ✅ Texture compression
- ✅ Mesh optimization (reduce vertex count)
- ✅ Audio compression and streaming
- ✅ Asset bundle management
- ✅ Unload unused assets
- ✅ **Collection pooling** (see `unity-collection-pool` skill)

## Related Skills

- **unity-collection-pool**: GC-free collection management with ListPool, HashSetPool, DictionaryPool, and ObjectPool. Essential for eliminating GC spikes.

## Best Practices

1. **Profile on target platform**: Editor performance differs
2. **Optimize systematically**: Measure, optimize, validate
3. **Quality settings**: Provide options for different hardware
4. **Balance visuals vs performance**: Adjust based on target
5. **Test on low-end**: Ensure minimum spec performance
