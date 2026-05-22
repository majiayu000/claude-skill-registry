---
name: Debugging Guide
description: This skill should be used when the user asks about "debug panel", "F4 panel", "debug_register", "debug_watch", "sync test", "desync", "rollback debug", "--sync-test", "--p2p-test", "frame stepping", "time scale", "profiling", "debug group", "debugging ZX games", "inspect values", "live editing", or mentions debugging Nethercore ZX games, finding desyncs, testing multiplayer synchronization, or runtime value inspection.
version: 1.0.0
---

# Debugging Guide for Nethercore ZX

Debug ZX games using the built-in inspection system and testing tools. Press **F4** to open the debug panel during development.

## Debug System Overview

The debug inspection system provides:
- Live value editing (sliders, checkboxes, color pickers)
- Read-only watches for monitoring
- Grouped organization for complex games
- Frame control (pause, step, time scale)
- Zero overhead in release builds (compiles out)

Reference `nethercore/include/zx.rs` lines 1370-1478 for complete FFI signatures.

## F4 Debug Panel

Press **F4** during gameplay to toggle the debug panel. The panel displays all registered values and provides interactive controls.

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F4 | Toggle debug panel |
| F5 | Pause/unpause game |
| F6 | Step one frame (while paused) |
| F7 | Decrease time scale |
| F8 | Increase time scale |

## Registering Editable Values

Register values during `init()` to make them editable in the F4 panel:

```rust
static mut PLAYER_SPEED: f32 = 5.0;
static mut GRAVITY: f32 = 25.0;
static mut GOD_MODE: u8 = 0;
static mut ENEMY_COUNT: i32 = 5;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        // Basic registration
        debug_register_f32(b"Speed".as_ptr(), 5, &PLAYER_SPEED);
        debug_register_f32(b"Gravity".as_ptr(), 7, &GRAVITY);
        debug_register_bool(b"God Mode".as_ptr(), 8, &GOD_MODE);
        debug_register_i32(b"Enemies".as_ptr(), 7, &ENEMY_COUNT);
    }
}
```

### Range-Constrained Values (Sliders)

Use range variants for slider UI with min/max bounds:

```rust
static mut DIFFICULTY: i32 = 2;
static mut SPEED: f32 = 5.0;

fn init() {
    unsafe {
        debug_register_i32_range(b"Difficulty".as_ptr(), 10, &DIFFICULTY, 1, 5);
        debug_register_f32_range(b"Speed".as_ptr(), 5, &SPEED, 0.0, 20.0);
    }
}
```

### Compound Types

Register vectors, colors, and rects:

```rust
static mut PLAYER_POS: [f32; 3] = [0.0, 0.0, 0.0];
static mut TINT_COLOR: [u8; 4] = [255, 255, 255, 255];

fn init() {
    unsafe {
        debug_register_vec3(b"Position".as_ptr(), 8, PLAYER_POS.as_ptr());
        debug_register_color(b"Tint".as_ptr(), 4, TINT_COLOR.as_ptr());
    }
}
```

## Watch Functions (Read-Only)

Use watch functions to display values without allowing editing:

```rust
static mut FRAME_COUNT: u32 = 0;
static mut FPS: f32 = 0.0;
static mut PLAYER_VEL: [f32; 2] = [0.0, 0.0];

fn init() {
    unsafe {
        debug_watch_u32(b"Frame".as_ptr(), 5, &FRAME_COUNT);
        debug_watch_f32(b"FPS".as_ptr(), 3, &FPS);
        debug_watch_vec2(b"Velocity".as_ptr(), 8, PLAYER_VEL.as_ptr());
    }
}
```

## Organizing with Groups

Group related values for a cleaner debug panel:

```rust
fn init() {
    unsafe {
        debug_group_begin(b"Player".as_ptr(), 6);
        debug_register_vec3(b"Position".as_ptr(), 8, PLAYER_POS.as_ptr());
        debug_register_f32(b"Health".as_ptr(), 6, &PLAYER_HEALTH);
        debug_register_f32(b"Speed".as_ptr(), 5, &PLAYER_SPEED);
        debug_group_end();

        debug_group_begin(b"Physics".as_ptr(), 7);
        debug_register_f32(b"Gravity".as_ptr(), 7, &GRAVITY);
        debug_register_f32(b"Friction".as_ptr(), 8, &FRICTION);
        debug_group_end();

        debug_group_begin(b"Debug".as_ptr(), 5);
        debug_register_bool(b"God Mode".as_ptr(), 8, &GOD_MODE);
        debug_register_bool(b"Show Hitboxes".as_ptr(), 13, &SHOW_HITBOXES);
        debug_group_end();
    }
}
```

Groups are collapsible in the UI - click the header to expand/collapse.

## Frame Control

Query debug state to respect pause/time scale:

```rust
fn update() {
    unsafe {
        // Skip update when paused via debug panel
        if debug_is_paused() != 0 {
            return;
        }

        // Apply time scale to delta_time
        let dt = delta_time() * debug_get_time_scale();

        // Use scaled dt for all time-based logic
        PLAYER_VEL_Y += GRAVITY * dt;
        PLAYER_X += PLAYER_VEL_X * dt;
    }
}
```

**Time Scale Values:**
- F7 decreases: 0.5x, 0.25x, 0.1x
- F8 increases: 2x, 4x, 8x
- Default: 1.0x

## Multiplayer Sync Testing

Test rollback determinism with CLI flags:

### Sync Test Mode

Runs two parallel simulations and compares state:

```bash
nether run --sync-test
```

This launches two game instances in parallel:
1. Both receive identical inputs
2. State is compared after each frame
3. Any divergence is reported as a desync

**Desync causes:**
- Using external randomness instead of `random()`
- Reading wall-clock time instead of `delta_time()`/`tick_count()`
- Uninitialized memory
- Modifying state in `render()` instead of `update()`

### P2P Test Mode

Tests actual network rollback with two instances:

```bash
nether run --p2p-test
```

Creates a local two-player session:
1. Player 1 window (local)
2. Player 2 window (local)
3. GGRS netcode active between them

Use this to verify:
- Input synchronization works
- Rollbacks don't cause visual glitches
- State serialization is correct

## Common Debugging Patterns

### Visualizing Hitboxes

```rust
static mut SHOW_HITBOXES: u8 = 0;

fn init() {
    unsafe {
        debug_register_bool(b"Hitboxes".as_ptr(), 8, &SHOW_HITBOXES);
    }
}

fn render() {
    unsafe {
        if SHOW_HITBOXES != 0 {
            // Draw wireframe boxes around collision volumes
            for entity in entities.iter() {
                draw_rect(
                    entity.x - entity.half_w,
                    entity.y - entity.half_h,
                    entity.half_w * 2.0,
                    entity.half_h * 2.0,
                    0x00FF0080, // Semi-transparent green
                );
            }
        }
    }
}
```

### Debug HUD

```rust
fn render() {
    unsafe {
        // Show frame counter and FPS
        let frame = tick_count();
        // Draw debug text at top-left
        draw_text_str(&format!("Frame: {}", frame), 10.0, 10.0, 16.0, 0xFFFFFFFF);
    }
}
```

### Slow Motion for Animation Debugging

Use time scale controls (F7/F8) to:
1. Slow animations to 0.25x
2. Check interpolation smoothness
3. Verify state transitions
4. Frame-step with F6 for exact positioning

## Debugging Desyncs

When `--sync-test` reports a desync:

1. **Check random usage** - Every `random()` call must happen in same order
2. **Verify state location** - All game state in static variables?
3. **Review render()** - No state modifications allowed
4. **Check floating point** - Consistent operations across runs
5. **Inspect conditionals** - Same branches taken each simulation

Add debug watches to narrow down which variable diverges first.

## Helper Functions

Rust helper functions in `zx.rs`:

```rust
// String-based helpers
debug_f32("speed", &SPEED);        // debug_register_f32 wrapper
debug_i32("count", &COUNT);        // debug_register_i32 wrapper
debug_bool("enabled", &ENABLED);   // debug_register_bool wrapper
debug_group("Player");             // debug_group_begin wrapper
debug_group_close();               // debug_group_end wrapper
```

## Available Registration Functions

| Function | Type | UI Control |
|----------|------|------------|
| `debug_register_i8/i16/i32` | Signed integers | Number input |
| `debug_register_u8/u16/u32` | Unsigned integers | Number input |
| `debug_register_f32` | Float | Number input |
| `debug_register_bool` | Boolean (u8) | Checkbox |
| `debug_register_*_range` | Numbers | Slider |
| `debug_register_vec2/vec3` | Float arrays | Multi-input |
| `debug_register_rect` | 4 i16 | Multi-input |
| `debug_register_color` | 4 u8 RGBA | Color picker |
| `debug_register_fixed_*` | Fixed-point | Decimal display |

## Performance Notes

- Debug functions compile to no-ops in release builds
- Registration happens once in `init()`, not per-frame
- Watches read memory directly, no runtime cost
- F4 panel rendering uses separate draw path

## Additional Resources

- **`examples/debug-setup-rust.md`** - Complete Rust debug setup
- **`references/sync-test-checklist.md`** - Desync debugging checklist
- **`nethercore/include/zx.rs`** - Debug FFI (lines 1370-1478)
- **`nethercore/docs/book/src/api/debug.md`** - Full API reference
