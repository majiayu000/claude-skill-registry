---
name: Game Feel & Polish
description: |
  Use this skill for "game feel", "juice", "polish", "screen shake", "hit pause", "hitstop", "particles", "impact", "feedback", "responsiveness", making gameplay feel satisfying.

  **Load references when:**
  - Advanced techniques → `references/advanced-techniques.md`

  All code MUST be deterministic for rollback netcode compatibility.
version: 2.0.0
---

# Game Feel & Polish for Nethercore ZX

Game feel ("juice") transforms functional mechanics into satisfying experiences. All code MUST be deterministic for rollback netcode.

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Exaggeration** | Screen shake, scale bounces, speed lines |
| **Anticipation** | Wind-up animations, audio cues before action |
| **Follow-through** | Lingering effects after action ends |
| **Immediate feedback** | Visual + audio response within 1-2 frames |

## Screen Shake

```rust
struct ScreenShake {
    intensity: f32,
    duration: u32,
    remaining: u32,
}

impl ScreenShake {
    fn trigger(&mut self, intensity: f32, duration: u32) {
        self.intensity = intensity;
        self.duration = duration;
        self.remaining = duration;
    }

    fn update(&mut self) -> (f32, f32) {
        if self.remaining == 0 { return (0.0, 0.0); }

        let t = self.remaining as f32 / self.duration as f32;
        let current = self.intensity * t;
        let offset_x = (random() * 2.0 - 1.0) * current;
        let offset_y = (random() * 2.0 - 1.0) * current;

        self.remaining -= 1;
        (offset_x, offset_y)
    }
}
```

### Shake Intensity Guide

| Event | Intensity | Duration |
|-------|-----------|----------|
| Light hit | 2-4 px | 4-6 ticks |
| Heavy hit | 6-10 px | 8-12 ticks |
| Explosion | 12-20 px | 15-25 ticks |
| Boss attack | 15-25 px | 20-30 ticks |

## Hit Pause (Freeze Frames)

Momentary freeze on impact adds weight:

```rust
struct HitPause { remaining: u32 }

impl HitPause {
    fn trigger(&mut self, frames: u32) {
        self.remaining = self.remaining.max(frames);
    }

    fn is_paused(&self) -> bool { self.remaining > 0 }

    fn update(&mut self) {
        if self.remaining > 0 { self.remaining -= 1; }
    }
}

fn update(game: &mut Game) {
    game.hit_pause.update();
    if game.hit_pause.is_paused() { return; }  // Skip gameplay
    // Normal update...
}
```

### Hit Pause Guide

| Event | Duration |
|-------|----------|
| Light hit | 2-3 frames |
| Heavy hit | 4-6 frames |
| Critical | 8-10 frames |
| Boss stagger | 12-15 frames |

## Visual Feedback

### Flash on Hit
```rust
fn render_entity(e: &Entity) {
    if e.flash_timer > 0 {
        material_emissive(0xFFFFFFFF);  // White flash
    }
    draw_mesh(e.mesh);
    material_emissive(0x000000FF);  // Reset
}
```

### Scale Bounce
```rust
fn update_bounce(scale: &mut f32, target: f32, velocity: &mut f32) {
    let diff = target - *scale;
    *velocity += diff * 0.3;  // Spring force
    *velocity *= 0.8;  // Damping
    *scale += *velocity;
}
```

## Audio Feedback

| Event | Sound Type | Timing |
|-------|------------|--------|
| Button press | UI click | Immediate |
| Jump | Whoosh | On input |
| Land | Thud | On contact |
| Hit | Impact + voice | On collision |

```rust
fn on_hit(damage: i32) {
    play_sound(SOUND_HIT);
    if damage > 20 {
        play_sound(SOUND_HEAVY_HIT);
    }
}
```

## Particle Hints

For particle effects (dust, sparks, debris):

```rust
// Spawn burst on landing
if just_landed {
    for _ in 0..5 {
        spawn_particle(Particle {
            pos: player_pos,
            vel: (random() * 2.0 - 1.0, random() * 0.5),
            life: 15,
            color: 0x888888FF,
        });
    }
}
```

## Quick Checklist

- [ ] Screen shake on impacts
- [ ] Hit pause on heavy attacks
- [ ] Visual flash on damage
- [ ] Audio for all interactions
- [ ] Particles for contacts
- [ ] Anticipation before big moves
- [ ] Follow-through after actions

## References

- `references/advanced-techniques.md` - Complex effects, camera tricks

## Related Skills

- `zx-dev/rendering-techniques` - Visual effects implementation
- `procedural-sounds` - Sound effect generation
