---
name: Camera Systems
description: |
  This skill covers camera implementation for ZX games. Triggers on "camera follow", "orbit camera", "third person", "first person", "screen shake", "camera lerp", "dead zone", "camera FOV", "side-scroller camera", "top-down camera".

  **Load references when:**
  - Full implementations → `examples/camera-examples.md`
  - Matrix math, lerp/slerp → `references/camera-math.md`
  - 2D patterns, parallax → `references/side-scroller-patterns.md`
  - Coordinate conventions → `zx-game-development/references/coordinate-conventions.md`
version: 2.1.0
---

# Camera Systems for Nethercore ZX

Implement cameras using ZX FFI. All camera state in static variables for rollback safety.

**Coordinate Convention:** Y-up, right-handed, -Z forward. When yaw=0, camera looks toward -Z.

## Camera FFI

| Function | Purpose |
|----------|---------|
| `camera_set(x,y,z, tx,ty,tz)` | Position + look-at |
| `camera_fov(degrees)` | Field of view (default 60) |
| `push_view_matrix(m0..m15)` | Custom 4x4 view matrix |

## Camera Types

| Type | Best For | Complexity |
|------|----------|------------|
| Follow | Platformers, racing | Simple |
| Orbit | Action-adventure, RPGs | Medium |
| First-Person | FPS, exploration | Medium |
| Fixed | Puzzle, cinematic | Simple |

## Follow Camera (Core Pattern)

```rust
static mut CAM_X: f32 = 0.0;
static mut CAM_Y: f32 = 5.0;
static mut CAM_Z: f32 = 10.0;

fn update_follow_camera(tx: f32, ty: f32, tz: f32) {
    let dt = delta_time();
    let t = (5.0 * dt).min(1.0);  // Smoothing
    unsafe {
        CAM_X += (tx - CAM_X) * t;
        CAM_Y += (ty + 5.0 - CAM_Y) * t;  // Offset above
        CAM_Z += (tz + 10.0 - CAM_Z) * t; // Offset behind
    }
}

// In render():
camera_set(CAM_X, CAM_Y, CAM_Z, target_x, target_y, target_z);
```

## Orbit Camera (Core Pattern)

```rust
static mut CAM_YAW: f32 = 0.0;
static mut CAM_PITCH: f32 = 20.0;
static mut CAM_DIST: f32 = 8.0;

fn update_orbit(player: u32) {
    let dt = delta_time();
    unsafe {
        CAM_YAW += right_stick_x(player) * 120.0 * dt;
        CAM_PITCH = (CAM_PITCH - right_stick_y(player) * 120.0 * dt)
            .clamp(-30.0, 60.0);
    }
}

fn get_orbit_pos(tx: f32, ty: f32, tz: f32) -> (f32, f32, f32) {
    unsafe {
        let yaw = CAM_YAW.to_radians();
        let pitch = CAM_PITCH.to_radians();
        (
            tx - CAM_DIST * yaw.sin() * pitch.cos(),
            ty + CAM_DIST * pitch.sin(),
            tz + CAM_DIST * yaw.cos() * pitch.cos(),
        )
    }
}
```

## First-Person Camera (Core Pattern)

```rust
static mut LOOK_YAW: f32 = 0.0;
static mut LOOK_PITCH: f32 = 0.0;

fn update_first_person(player: u32) {
    let dt = delta_time();
    unsafe {
        LOOK_YAW += right_stick_x(player) * 90.0 * dt;
        LOOK_PITCH = (LOOK_PITCH - right_stick_y(player) * 90.0 * dt)
            .clamp(-85.0, 85.0);
    }
}

fn get_look_dir() -> (f32, f32, f32) {
    unsafe {
        let yaw = LOOK_YAW.to_radians();
        let pitch = LOOK_PITCH.to_radians();
        (-yaw.sin() * pitch.cos(), pitch.sin(), -yaw.cos() * pitch.cos())
    }
}

// In render():
let (dx, dy, dz) = get_look_dir();
camera_set(player_x, player_y + 1.6, player_z,
           player_x + dx, player_y + 1.6 + dy, player_z + dz);
```

## Screen Shake

```rust
static mut SHAKE_TRAUMA: f32 = 0.0;

fn add_shake(amount: f32) { unsafe { SHAKE_TRAUMA = (SHAKE_TRAUMA + amount).min(1.0); } }
fn update_shake() { unsafe { SHAKE_TRAUMA = (SHAKE_TRAUMA - delta_time() * 2.0).max(0.0); } }

fn get_shake_offset() -> (f32, f32) {
    unsafe {
        let shake = SHAKE_TRAUMA * SHAKE_TRAUMA * 10.0;
        ((random_f32() - 0.5) * shake, (random_f32() - 0.5) * shake)
    }
}
```

## Dead Zone

Prevents jitter when target is near camera center:

```rust
fn update_with_dead_zone(tx: f32, tz: f32) {
    let dx = tx - CAM_X;
    let dz = tz - (CAM_Z - OFFSET_Z);
    let dist = (dx*dx + dz*dz).sqrt();
    if dist > 2.0 {  // DEAD_ZONE
        let t = ((dist - 2.0) / dist) * 0.1;
        CAM_X += dx * t;
        CAM_Z += dz * t;
    }
}
```

## Perspective Selection

| Experience | Best Perspective |
|------------|------------------|
| Character action/story | Third-Person |
| Immersive world | First-Person |
| Precision platforming | Side-Scroller |
| Vehicle/tactical | Top-Down |

## Rollback Safety

All camera state uses static variables (auto-snapshotted). Use `delta_time()` for frame-rate independence, FFI `random()` for shake.
