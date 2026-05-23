---
name: Multiplayer Patterns for ZX
description: |
  Use this skill for ZX multiplayer: "GGRS", "rollback netcode", "determinism", "desync", "split screen", "viewport FFI", "player_count()", "local_player_mask()", "sync test".

  **Load references when:**
  - Determinism checklist → `references/determinism-checklist.md`
  - Netplay patterns → `references/netplay-patterns.md`
  - Viewport layouts → `references/viewport-layouts.md`

  For GAME DESIGN (co-op patterns, competitive balance): use game-design:multiplayer-design instead.
version: 2.1.0
---

# Multiplayer Patterns for Nethercore ZX

GGRS rollback netcode implementation. All gameplay code must be deterministic.

## ZX Capabilities

| Feature | Value |
|---------|-------|
| Max Players | 4 (local + remote mix) |
| Netcode | GGRS deterministic rollback |
| Rollback Window | 8 frames typical |
| State Target | < 100 KB |
| Resolution | 960×540 |

---

## How Rollback Works

1. **Predict** remote input (usually "same as last frame")
2. **Advance** game state with predictions
3. **Correct** when actual input arrives: restore snapshot, re-run with correct input
4. **Result** appears seamless to players

**Desync** = different game states = broken multiplayer.

---

## Determinism Rules

| Correct | Incorrect |
|---------|-----------|
| `tick_count()` | `std::time`, system clock |
| `random()`, `random_range()` | `rand()` unseeded |
| Arrays, sorted collections | HashMap iteration |
| Fixed-point for critical math | Float edge cases (NaN) |

---

## Session FFI

| Function | `update()` | `render()` |
|----------|------------|------------|
| `player_count()` | SAFE | SAFE |
| `local_player_mask()` | **NEVER** | SAFE |
| `viewport()` | N/A | SAFE |

**Why?** `update()` runs on ALL clients identically. `render()` is local-only.

```rust
fn is_local(player_id: u32) -> bool {
    (local_player_mask() & (1 << player_id)) != 0
}
```

---

## State Design

**Target: < 100 KB rollback state**

Include:
- Player positions, velocities, health
- Entity states
- RNG state
- World state

Exclude (visual-only):
- Particles, screen shake
- Audio state
- Cached calculations

---

## Viewport Layouts

| Players | Layout | Each Viewport |
|---------|--------|---------------|
| 2P Horiz | Side-by-side | 480×540 |
| 2P Vert | Top/bottom | 960×270 |
| 4P Grid | Quadrants | 480×270 |

```rust
fn render() {
    for (i, player_id) in local_players().enumerate() {
        set_viewport(i, local_count);
        render_player_view(player_id);
    }
    viewport_clear();
    draw_shared_ui();
}
```

See **`references/viewport-layouts.md`** for complete implementations.

---

## Common Mistakes

**WRONG** - local_player_mask in update():
```rust
fn update() {
    let mask = local_player_mask();  // DESYNC!
    if (mask & 1) != 0 { /* breaks determinism */ }
}
```

**CORRECT** - process all players in update():
```rust
fn update() {
    for i in 0..player_count() {
        process_input(i);  // All players, deterministic
    }
}
```

---

## Testing Progression

1. Local single-player
2. Local multiplayer (2-4 controllers)
3. Synthetic desync test (compare state hashes)
4. LAN test
5. Simulated latency (50-200ms)
6. Real online test

### Desync Debugging

1. Hash game state each frame
2. Find first divergent frame
3. Compare state dumps
4. Check: random, floats, hash iteration, uninitialized memory

---

## Performance

Each viewport = separate render pass. 4 viewports = ~4x render work.

Optimize: simpler effects in split-screen, LOD, reduced particles.

---

## Related Skills

- **`physics-collision`** — Deterministic physics
- **`zx-dev:rollback-reviewer`** — Agent to detect non-deterministic code
- **`game-design:multiplayer-design`** — Conceptual multiplayer design
