---
name: Physics & Collision for ZX
description: |
  Use this skill for physics/collision: "collision", "AABB", "raycast", "gravity", "hit detection", "bounding box", "sphere collision", "physics body".

  **Load references when:**
  - Capsule, swept tests, spatial partitioning → `references/advanced-collision.md`

  For CONCEPTUAL game feel and physics design: use game-design:core-loop-design instead.
version: 1.1.0
---

# Physics & Collision for Nethercore ZX

ZX provides rendering only — games implement physics in WASM. All physics code MUST be deterministic for rollback netcode.

## Determinism (Critical)

| Use | Correct | Incorrect |
|-----|---------|-----------|
| Time | `delta_time()` | `std::time`, wall clock |
| Random | `random()`, `random_range()` | `rand()` unseeded |
| Iteration | Arrays, Vec | HashMap (order varies) |

---

## Core Collision Types

### AABB (Axis-Aligned Bounding Box)

Fastest primitive. Use for rectangular objects and broad-phase.

```rust
struct AABB { min: [f32; 3], max: [f32; 3] }

fn intersects(a: &AABB, b: &AABB) -> bool {
    a.min[0] <= b.max[0] && a.max[0] >= b.min[0] &&
    a.min[1] <= b.max[1] && a.max[1] >= b.min[1] &&
    a.min[2] <= b.max[2] && a.max[2] >= b.min[2]
}
```

### Sphere

Ideal for characters, projectiles.

```rust
struct Sphere { center: [f32; 3], radius: f32 }

fn intersects(a: &Sphere, b: &Sphere) -> bool {
    let d = [a.center[0]-b.center[0], a.center[1]-b.center[1], a.center[2]-b.center[2]];
    let dist_sq = d[0]*d[0] + d[1]*d[1] + d[2]*d[2];
    dist_sq <= (a.radius + b.radius).powi(2)
}
```

### Raycast

For shooting, ground detection, line-of-sight.

```rust
struct Ray { origin: [f32; 3], direction: [f32; 3] }  // direction normalized
struct RayHit { t: f32, point: [f32; 3], normal: [f32; 3] }
```

Ray-AABB: Slab method (check each axis, track t_min/t_max).
Ray-Sphere: Quadratic formula (solve for intersection).

---

## Collision Response

### Penetration Resolution

Push overlapping objects apart along minimum translation vector:
1. Calculate overlap on each axis
2. Find axis with minimum overlap
3. Push along that axis (direction based on center positions)

### Slide Response

Remove velocity component along collision normal:
```rust
fn slide(vel: [f32;3], normal: [f32;3]) -> [f32;3] {
    let dot = vel[0]*normal[0] + vel[1]*normal[1] + vel[2]*normal[2];
    if dot >= 0.0 { return vel; }
    [vel[0] - dot*normal[0], vel[1] - dot*normal[1], vel[2] - dot*normal[2]]
}
```

### Bounce Response

Reflect velocity with restitution factor (0=stop, 1=full bounce).

---

## Basic Physics

### Integration (Semi-Implicit Euler)

```rust
fn integrate(pos: &mut [f32;3], vel: &mut [f32;3], accel: [f32;3], dt: f32) {
    vel[0] += accel[0] * dt; vel[1] += accel[1] * dt; vel[2] += accel[2] * dt;
    pos[0] += vel[0] * dt; pos[1] += vel[1] * dt; pos[2] += vel[2] * dt;
}
```

### Gravity + Terminal Velocity

```rust
const GRAVITY: f32 = -20.0;
const TERMINAL: f32 = -30.0;

fn apply_gravity(vel: &mut [f32;3], dt: f32) {
    vel[1] = (vel[1] + GRAVITY * dt).max(TERMINAL);
}
```

### Friction

```rust
fn apply_friction(vel: &mut [f32;3], friction: f32, dt: f32) {
    let f = (1.0 - friction * dt).max(0.0);
    vel[0] *= f; vel[2] *= f;
}
```

---

## Trigger vs Solid Colliders

| Type | Behavior |
|------|----------|
| **Solid** | Blocks movement, resolves penetration |
| **Trigger** | Detects overlap only (items, zones) |

Use collision layers (bitmask) to filter what collides with what.

---

## Ground Detection

Short downward raycast from feet:

```rust
fn is_grounded(pos: [f32;3], feet_offset: f32, world: &[AABB]) -> bool {
    let ray = Ray { origin: pos, direction: [0.0, -1.0, 0.0] };
    world.iter().any(|aabb| ray.intersect(aabb).map_or(false, |t| t <= feet_offset + 0.05))
}
```

---

## Physics Update Pattern

```rust
fn physics_update(entities: &mut [Entity], world: &[AABB], dt: f32) {
    for e in entities {
        apply_gravity(&mut e.vel, dt);
        integrate(&mut e.pos, &mut e.vel, [0.0;3], dt);
        // Collision detection + response against world
        // Apply friction based on grounded state
    }
}
```

---

## Related Skills

- **`multiplayer-patterns`** — Determinism, state serialization
- **`gameplay-mechanics`** — Movement and combat using physics
- **`game-design:core-loop-design`** — Conceptual physics feel
