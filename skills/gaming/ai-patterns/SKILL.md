---
name: AI & Behavior Patterns
description: |
  Use this skill for game AI: "enemy AI", "state machine", "FSM", "patrol", "pathfinding", "NPC behavior", "chase", "flee", "behavior tree", "A*", "steering".

  **Load references when:**
  - Hierarchical FSM, behavior trees → `references/advanced-fsm.md`
  - A*, waypoint graphs, nav mesh → `references/pathfinding-algorithms.md`
version: 1.1.0
---

# AI & Behavior Patterns for Nethercore ZX

Deterministic AI patterns for rollback netcode compatibility.

## Rollback Safety

| Correct | Incorrect |
|---------|-----------|
| `tick_count()` | System clock |
| `random()`, `random_range()` | `rand()` unseeded |
| Arrays, Vec | HashMap (non-deterministic) |
| Frame-based timers | Real-time delays |

---

## Finite State Machines

Foundation of game AI. Each entity has current state with defined transitions.

### Basic Pattern

```rust
#[derive(Clone, Copy, PartialEq)]
enum EnemyState { Idle, Patrol, Chase, Attack, Flee }

struct Enemy {
    state: EnemyState,
    x: f32, y: f32,
    state_timer: u32,
}

fn update(e: &mut Enemy, player: (f32,f32)) {
    match e.state {
        EnemyState::Idle => update_idle(e, player),
        EnemyState::Chase => update_chase(e, player),
        // ...
    }
    if e.state_timer > 0 { e.state_timer -= 1; }
}
```

### Transition Rules

Define clear conditions:
- `Idle → Chase`: Player in sight range AND line of sight clear
- `Chase → Attack`: Player in attack range
- `Any → Flee`: Health below threshold
- `Chase → Idle`: Lost sight for N frames

---

## Movement Behaviors

### Chase (Follow Target)

```rust
fn move_toward(e: &mut Enemy, tx: f32, ty: f32, speed: f32) {
    let dx = tx - e.x; let dy = ty - e.y;
    let dist = (dx*dx + dy*dy).sqrt();
    if dist > 0.1 { e.x += dx/dist * speed; e.y += dy/dist * speed; }
}
```

### Flee (Run Away)

Move in opposite direction from threat. Check safe distance to transition out.

### Patrol (Waypoints)

Cycle through waypoint array. Wait at each point (use timer). Check for player detection during patrol.

### Wander (Random)

Pick random direction every N frames using `random()`. Move toward that point.

---

## Sensing

### Line of Sight

Raycast from enemy to player. Check for wall intersections. See `physics-collision` for raycast implementation.

### Proximity (Hearing)

Simple distance check. Optionally increase range if player is running.

### Memory

Track last known player position. Decay memory over time (timer countdown). Move to last known position when player not visible.

```rust
struct Memory { last_x: f32, last_y: f32, timer: u32 }
// Update when player visible, countdown when not
```

---

## Steering Behaviors

### Seek

Move directly toward target at max speed.

### Arrive

Seek but slow down when approaching target (within arrival radius).

```rust
fn arrive(current: [f32;2], target: [f32;2], radius: f32) -> [f32;2] {
    let d = distance(current, target);
    let speed = if d < radius { MAX_SPEED * d/radius } else { MAX_SPEED };
    // Return normalized direction * speed
}
```

### Evade

Predict target's future position, flee from that point.

---

## Combat AI

### Attack Pattern

```rust
struct AttackState { cooldown: u32, windup: u32, active: u32 }
// Phases: Cooldown → Windup (telegraph) → Active (hitbox) → Cooldown
```

### Aggression Levels

| Level | Behavior |
|-------|----------|
| Passive | Only attacks if damaged |
| Defensive | Attacks if player close |
| Aggressive | Actively hunts player |

---

## Pathfinding Overview

### Grid-Based A*

1. Create grid from level geometry
2. Use priority queue (open list)
3. Track came_from for path reconstruction
4. Heuristic: Manhattan or Euclidean distance

### Waypoint Graph

Pre-placed waypoints with connections. Use A* on graph. Cheaper than grid for large levels.

See **`references/pathfinding-algorithms.md`** for implementations.

---

## Related Skills

- **`physics-collision`** — Raycasting for line of sight
- **`gameplay-mechanics`** — Combat hitboxes
- **`multiplayer-patterns`** — Determinism requirements
