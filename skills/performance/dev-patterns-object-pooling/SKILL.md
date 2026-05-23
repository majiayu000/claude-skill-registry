---
name: dev-patterns-object-pooling
description: Object pooling for high-performance R3F components (decals, particles, projectiles)
category: patterns
---

# Object Pooling Pattern

> "Pre-allocate, reuse, recycle – eliminate runtime GC pauses."

## When to Use This Skill

Use when:
- Creating/destroying objects every frame (bullets, particles, decals)
- Targeting 60 FPS with many transient objects
- Seeing GC pauses in Chrome DevTools Performance tab
- Objects have identical initialization (can be pre-created)
- Maximum simultaneous objects is bounded (~500 or less)

## Quick Start

```tsx
// Basic object pool pattern
const POOL_SIZE = 500;
const MAX_ACTIVE = 200;

interface PoolSlot<T> {
  obj: T;
  active: boolean;
  lastUsed: number;
}

function useObjectPool<T>(
  create: () => T,
  activate: (obj: T) => void,
  deactivate: (obj: T) => void
) {
  const poolRef = useRef<PoolSlot<T>[]>([]);

  // Initialize pool on mount
  useEffect(() => {
    poolRef.current = Array.from({ length: POOL_SIZE }, () => ({
      obj: create(),
      active: false,
      lastUsed: 0,
    }));
    return () => {
      // Cleanup
      poolRef.current.forEach(slot => {
        if (slot.obj?.dispose) slot.obj.dispose();
      });
    };
  }, []);

  const acquire = useCallback(() => {
    const pool = poolRef.current;
    // Find inactive slot
    let slot = pool.find(s => !s.active);
    // If pool full, recycle LRU
    if (!slot) {
      slot = pool.reduce((oldest, s) =>
        s.lastUsed < oldest.lastUsed ? s : oldest
      );
      deactivate(slot.obj);
    }
    slot.active = true;
    slot.lastUsed = performance.now();
    activate(slot.obj);
    return slot.obj;
  }, [activate]);

  const release = useCallback((obj: T) => {
    const slot = poolRef.current.find(s => s.obj === obj);
    if (slot) slot.active = false;
  }, []);

  return { acquire, release };
}
```

## Decision Framework

| Scenario                     | Use Pool? | Reason                     |
| ---------------------------- | --------- | -------------------------- |
| Bullets (max ~100 active)    | Yes       | High create/destroy rate   |
| Decals (max ~200 visible)    | Yes       | Geometry allocation costly |
| Particles (max ~500)         | Yes       | Per-frame creation         |
| UI overlays (dynamic count)  | No        | Unpredictable count        |
| Player characters (1-32)     | No        | Low churn, complex init    |
| Static props                 | No        | Never destroyed            |

## LRU Eviction Pattern

When the pool is full, evict the **Least Recently Used** item:

```tsx
// LRU recycling
let slot = pool.find(s => !s.active);
if (!slot) {
  // Pool exhausted - recycle oldest decal
  slot = pool.reduce((oldest, s) =>
    s.lastUsed < oldest.lastUsed ? s : oldest
  );
  // Fade out before recycling
  fadeOutDecal(slot.obj);
}
```

**Why LRU?**
- Predictable: older content fades first (less noticeable)
- Fair: no single hot-spot gets preferential treatment
- Simple: O(n) scan is fine for pools < 1000

## GC-Avoidance: Temp Vector Reuse

```tsx
// BAD: Creates new objects every frame
useFrame(() => {
  const position = new Vector3();
  const quaternion = new Quaternion();
  // ... do work
});

// GOOD: Reuse temp objects
const _tempVec = useRef(new Vector3()).current;
const _tempQuat = useRef(new Quaternion()).current;

useFrame(() => {
  _tempVec.set(0, 0, 0);  // Reset, don't reallocate
  _tempQuat.identity();
  // ... do work
});
```

## Pool Size Guidelines

| Object Type   | Suggested Pool Size | Max Active | Rationale                           |
| ------------- | ------------------- | ---------- | ----------------------------------- |
| Bullets       | 200                 | 100        | Fast fire rate ~10/sec              |
| Particles     | 1000                | 500        | Explosions spawn many at once       |
| Decals        | 500                 | 200        | Persist 60s, but limited visibility |
| Audio sources | 32                  | 16         | WebAudio limit                      |

**Rule of thumb:** `poolSize = maxActive * 2` to `maxActive * 3`

## Implementation Checklist

- [ ] Pre-create all objects on mount (useEffect)
- [ ] Use `active` flag to track in-use slots
- [ ] Use `lastUsed` timestamp for LRU eviction
- [ ] Properly dispose geometries/materials in cleanup
- [ ] Reuse temp vectors with `useRef` or class fields
- [ ] Initialize materials per-slot (not shared) when needed
- [ ] Consider `frustumCulled={false}` for small objects

## Common Pitfalls

| Pitfall                        | Symptom              | Fix                              |
| ------------------------------ | -------------------- | -------------------------------- |
| Sharing material across slots  | All decals same color| Create unique material per slot   |
| Forgetting to reset state      | Stale data on reuse  | Reset all props in activate()     |
| Pool too small                 | Visible popping      | Increase pool or maxActive        |
| No disposal in useEffect       | Memory leak          | Add cleanup function              |
| Using `new` in useFrame        | GC stutter           | Use temp refs                     |

## Reference Implementation

See: `src/components/game/effects/PaintDecalManager.tsx`

Key sections:
- Pool initialization: lines 68-118
- Acquire/activate: lines 120-141
- LRU recycling: lines 142-153
- Release/deactivate: lines 155-162
- Temp vector reuse: lines 35-37
