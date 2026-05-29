---
name: Rendering Techniques
description: |
  This skill covers advanced ZX rendering: render passes, stencil effects, custom fonts, billboard particles. Triggers on "render pass", "stencil buffer", "portal rendering", "mirror", "scope", "viewmodel", "z_index", "z-index", "depth clear", "custom font", "bitmap font", "billboard", "particles", "smoke/fire effect", "text rendering".

  **Load references when:**
  - Advanced stencil patterns → `references/render-passes.md`
  - Particle system examples → Reference skill body (core patterns below)
  - Font atlas creation → See details below
  - FFI details → Read `nethercore/include/zx.rs` lines 417-502 (render passes), 751-784 (font), 644-662 (billboard)
version: 3.0.0
---

# Rendering Techniques for Nethercore ZX

Advanced rendering: render passes, stencil buffer, custom fonts, billboard particles.

## Render Passes & Stencil Buffer

Create portals, scopes, mirrors, FPS viewmodels, and masked UI elements using render passes.

### Render Pass FFI

| Function | Purpose |
|----------|---------|
| `begin_pass(clear_depth)` | New pass with optional depth clear |
| `begin_pass_stencil_write(ref, clear_depth)` | Create stencil mask |
| `begin_pass_stencil_test(ref, clear_depth)` | Render inside mask |
| `begin_pass_full(...)` | Full control (8 params) |
| `z_index(n)` | 2D ordering within pass (0-255) |

### Constants

**Depth/Stencil Compare (`compare::*`):**
| Constant | Value | Use |
|----------|-------|-----|
| `NEVER` | 1 | Never pass |
| `LESS` | 2 | Standard depth (default) |
| `EQUAL` | 3 | Match exactly |
| `LESS_EQUAL` | 4 | Less or equal |
| `GREATER` | 5 | Greater than |
| `NOT_EQUAL` | 6 | Inverted masks |
| `GREATER_EQUAL` | 7 | Greater or equal |
| `ALWAYS` | 8 | Always pass |

**Stencil Operations (`stencil_op::*`):**
| Constant | Value | Effect |
|----------|-------|--------|
| `KEEP` | 0 | Keep current |
| `ZERO` | 1 | Set to zero |
| `REPLACE` | 2 | Set to ref |
| `INCREMENT_CLAMP` | 3 | Increment, clamp |
| `DECREMENT_CLAMP` | 4 | Decrement, clamp |
| `INVERT` | 5 | Bitwise invert |
| `INCREMENT_WRAP` | 6 | Increment, wrap |
| `DECREMENT_WRAP` | 7 | Decrement, wrap |

### Basic Stencil Flow

```rust
// 1. Create mask (geometry writes to stencil, not color)
begin_pass_stencil_write(1, 0);
draw_circle(SCREEN_CX, SCREEN_CY, 200.0);  // Mask shape

// 2. Render inside mask (only where stencil == ref)
begin_pass_stencil_test(1, 0);
draw_scene();  // Only visible inside circle

// 3. Return to normal
begin_pass(0);
```

### Scope Effect (Circular Mask)

```rust
fn render_scoped_view() {
    // Create circular mask
    begin_pass_stencil_write(1, 0);
    draw_circle(SCREEN_CX, SCREEN_CY, 200.0);

    // World only visible inside circle
    begin_pass_stencil_test(1, 0);
    camera_set(cam_x, cam_y, cam_z, tx, ty, tz);
    draw_env();
    draw_mesh(WORLD_MESH);

    // Return to normal, draw scope overlay
    begin_pass(0);
    texture_bind(SCOPE_OVERLAY);
    draw_sprite(0.0, 0.0, 960.0, 540.0);
}
```

### Portal Effect

```rust
fn render_portal() {
    // Draw main world first
    camera_set(main_cam...);
    draw_mesh(MAIN_WORLD);

    // Create portal mask
    begin_pass_stencil_write(1, 0);
    push_translate(portal_x, portal_y, portal_z);
    draw_mesh(PORTAL_FRAME);
    push_identity();

    // Other world inside portal (clear_depth=1 for separate view)
    begin_pass_stencil_test(1, 1);
    camera_set(other_cam...);
    draw_mesh(OTHER_WORLD);

    // Return to normal
    begin_pass(0);
}
```

### FPS Viewmodel (Gun on Top)

```rust
fn render_fps() {
    // Draw world
    camera_set(player_x, player_y, player_z, look_x, look_y, look_z);
    draw_env();
    draw_mesh(LEVEL);

    // New pass with depth clear - viewmodel always renders on top
    begin_pass(1);  // clear_depth = 1
    push_translate(0.3, -0.2, 0.5);
    push_rotate_y(sway_angle);
    draw_mesh(GUN);
    push_identity();
}
```

### Vignette (Inverted Mask)

```rust
fn render_vignette() {
    draw_scene();

    begin_pass_stencil_write(1, 0);
    draw_circle(SCREEN_CX, SCREEN_CY, 250.0);

    // Render OUTSIDE mask using NOT_EQUAL
    begin_pass_full(
        compare::LESS, 1, 0,
        compare::NOT_EQUAL, 1,
        stencil_op::KEEP, stencil_op::KEEP, stencil_op::KEEP,
    );
    set_color(0x000000AA);
    draw_rect(0.0, 0.0, 960.0, 540.0);

    begin_pass(0);
}
```

See `references/render-passes.md` for more advanced patterns (diagonal split, animated portals).

## Custom Fonts

Load bitmap fonts for styled text rendering.

### Font FFI

| Function | Purpose |
|----------|---------|
| `load_font(tex, w, h, first, count)` | Fixed-width font |
| `load_font_ex(tex, widths, h, first, count)` | Variable-width |
| `font_bind(handle)` | Bind for draw_text |

### Font Atlas Format

Glyphs in row-major grid. For ASCII printables: `first_codepoint=32`, `count=96`.

### Fixed-Width Font

```rust
static mut GAME_FONT: u32 = 0;

fn init() {
    let tex = rom_texture_str("pixel_font");
    GAME_FONT = load_font(tex, 8, 12, 32, 96);  // 8x12 glyphs
}

fn render() {
    font_bind(GAME_FONT);
    draw_text_str("SCORE: 1000", 10.0, 10.0, 24.0, 0xFFFFFFFF);
    font_bind(0);  // Back to default
}
```

### Recommended Sizes

| Style | Glyph | Atlas |
|-------|-------|-------|
| Tiny | 4x6 | 64x36 |
| Small | 8x8 | 128x48 |
| Medium | 8x12 | 128x72 |
| Large | 16x16 | 256x96 |

## Billboard Particles

Camera-facing sprites for effects.

### Billboard FFI

| Function | Purpose |
|----------|---------|
| `draw_billboard(w, h, mode, color)` | Full texture |
| `draw_billboard_region(w,h, sx,sy,sw,sh, mode, color)` | UV region |

### Billboard Modes

| Mode | Constant | Use |
|------|----------|-----|
| 1 | SPHERICAL | Particles (faces camera) |
| 2 | CYLINDRICAL_Y | Trees, grass (upright) |

### Particle System (Core Pattern)

```rust
const MAX: usize = 256;

#[derive(Copy, Clone, Default)]
struct Particle { x: f32, y: f32, z: f32, vx: f32, vy: f32, vz: f32, life: f32, size: f32, color: u32 }

static mut PARTICLES: [Particle; MAX] = [Particle { x:0.0, y:0.0, z:0.0, vx:0.0, vy:0.0, vz:0.0, life:0.0, size:1.0, color:0xFFFFFFFF }; MAX];

fn update_particles() {
    let dt = delta_time();
    for p in unsafe { PARTICLES.iter_mut() } {
        if p.life > 0.0 {
            p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
            p.vy -= 9.8 * dt;
            p.life -= dt;
        }
    }
}

fn render_particles(tex: u32) {
    texture_bind(tex);
    for p in unsafe { PARTICLES.iter() } {
        if p.life > 0.0 {
            let alpha = ((p.life / 1.0) * 255.0) as u8;
            push_translate(p.x, p.y, p.z);
            draw_billboard(p.size, p.size, 1, (p.color & 0xFFFFFF00) | alpha as u32);
            push_identity();
        }
    }
}
```

### Effect Recipes

**Smoke:** `vx/vz = ±0.5`, `vy = 1-2`, `life = 1-3s`, `color = 0x888888FF`
**Fire:** `vy = 2-3`, `life = 0.3-0.7s`, `colors = 0xFFFF88/FF8800/FF4400`
**Sparks:** `vx/vy/vz = ±5`, `life = 0.2-0.5s`, `size = 0.05-0.15`, `color = 0xFFFF00FF`

### Performance

| Particles | Impact |
|-----------|--------|
| 0-100 | Excellent |
| 100-500 | Good |
| 500-1000 | Moderate |
| 1000+ | Optimize |

**Tips:** Pool particles, LOD at distance, texture atlas, cull behind camera.

## Rollback Safety

All rendering is display-only. Particle state in static variables (auto-snapshotted). Use FFI `random()` for spawn variation.
