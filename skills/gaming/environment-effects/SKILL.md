---
name: Environment Effects (EPU)
description: This skill should be used when the user asks about "EPU", "environment processing", "background effect", "env_gradient", "env_scatter", "env_lines", "env_silhouette", "env_rectangles", "env_room", "env_curtains", "env_rings", "procedural background", "sky effect", "draw_env", "env_blend", "dual layer", "environment layer", "space background", "synthwave grid", "portal effect", "star field", or needs implementation patterns for procedural backgrounds and environment rendering on Nethercore ZX.
version: 1.0.0
---

# Environment Processing Unit (EPU)

The ZX EPU generates procedural backgrounds without textures or meshes. It uses a dual-layer system where you configure a base layer (0) and optional overlay layer (1), then blend them together.

## Rendering Flow

Call `draw_env()` first in `render()`, before any geometry:

```rust
#[no_mangle]
pub extern "C" fn render() {
    unsafe { draw_env(); }  // Always first
    // Then draw meshes, sprites, etc.
}
```

## Dual-Layer System

Each of the 8 modes can be configured on either layer:

| Layer | Purpose | Typical Use |
|-------|---------|-------------|
| 0 (Base) | Primary background | Gradient sky, star field |
| 1 (Overlay) | Composited on top | Rain, fog, portal effect |

Configure layers in `init()` or `update()`, then blend with `env_blend()`:

```rust
// Base: gradient sky
env_gradient(0, 0x1a1a2eFF, 0x4a4a6aFF, 0x2a2a3aFF, 0x0a0a1aFF, 0.0, 0.0);
// Overlay: star field
env_scatter(1, 0, 200, 3, 20, 0, 0xFFFFFF00, 0xAAAAFF00, 100, 50, 0);
// Blend: additive for glowing stars
env_blend(1);
```

## Blend Modes

```rust
env_blend(mode: u32);  // 0=Alpha, 1=Add, 2=Multiply, 3=Screen
```

| Mode | Value | Effect | Use Case |
|------|-------|--------|----------|
| Alpha | 0 | Standard alpha blend | Transparent overlays |
| Add | 1 | Additive blend | Glowing effects, stars, neon |
| Multiply | 2 | Multiply blend | Shadows, darkening |
| Screen | 3 | Screen blend | Lighting, fog |

## Mode 0: Gradient

4-color vertical gradient with rotation:

```rust
env_gradient(
    layer: u32,           // 0 or 1
    zenith: u32,          // Color overhead (0xRRGGBBAA)
    sky_horizon: u32,     // Sky at horizon
    ground_horizon: u32,  // Ground at horizon
    nadir: u32,           // Color below
    rotation: f32,        // Y-axis rotation (radians)
    shift: f32,           // Horizon shift (-1.0 to 1.0)
);
```

**Example: Sunset sky**
```rust
env_gradient(0,
    0xFF6B35FF,  // Orange zenith
    0xFFB347FF,  // Yellow-orange horizon
    0x4A2C2AFF,  // Dark brown ground horizon
    0x1A0F0EFF,  // Near-black nadir
    0.0, 0.0
);
```

## Mode 1: Scatter (Stars, Rain, Warp)

Procedural particle field:

```rust
env_scatter(
    layer: u32,
    variant: u32,         // 0=Stars, 1=Vertical, 2=Horizontal, 3=Warp
    density: u32,         // Particle count (0-255)
    size: u32,            // Particle size (0-255)
    glow: u32,            // Bloom intensity (0-255)
    streak_length: u32,   // Elongation (0-63, 0=points)
    color_primary: u32,   // Main color (0xRRGGBB00)
    color_secondary: u32, // Variation color (0xRRGGBB00)
    parallax_rate: u32,   // Layer separation (0-255)
    parallax_size: u32,   // Size with depth (0-255)
    phase: u32,           // Animation (0-65535, wraps)
);
```

**Example: Rain effect**
```rust
// Animated rain - increment phase in update()
static mut RAIN_PHASE: u32 = 0;

fn update() {
    unsafe { RAIN_PHASE = RAIN_PHASE.wrapping_add(500); }
}

fn render() {
    unsafe {
        env_scatter(1, 1, 150, 2, 0, 30,
            0xAABBCC00, 0x8899AA00, 50, 20, RAIN_PHASE);
    }
}
```

**Example: Starfield**
```rust
env_scatter(0, 0, 200, 3, 40, 0,
    0xFFFFFF00, 0xAAAAFF00, 100, 50, 0);
```

## Mode 2: Lines (Synthwave Grid)

Infinite procedural grid:

```rust
env_lines(
    layer: u32,
    variant: u32,         // 0=Floor, 1=Ceiling, 2=Sphere
    line_type: u32,       // 0=Horizontal, 1=Vertical, 2=Grid
    thickness: u32,       // Line thickness (0-255)
    spacing: f32,         // Distance between lines
    fade_distance: f32,   // Fade start distance
    color_primary: u32,   // Main color (0xRRGGBBAA)
    color_accent: u32,    // Accent color (0xRRGGBBAA)
    accent_every: u32,    // Every Nth line uses accent
    phase: u32,           // Scroll phase (0-65535)
);
```

**Example: Synthwave floor grid**
```rust
static mut GRID_PHASE: u32 = 0;

fn update() {
    unsafe { GRID_PHASE = GRID_PHASE.wrapping_add(100); }
}

fn render() {
    unsafe {
        // Neon pink/cyan grid, scrolling toward camera
        env_lines(0, 0, 2, 3, 2.0, 50.0,
            0xFF00FFFF, 0x00FFFFFF, 4, GRID_PHASE);
    }
}
```

## Mode 3: Silhouette (Mountains, Cityscape)

Layered terrain silhouettes:

```rust
env_silhouette(
    layer: u32,
    jaggedness: u32,      // Roughness (0-255)
    layer_count: u32,     // Depth layers (1-3)
    color_near: u32,      // Nearest color (0xRRGGBBAA)
    color_far: u32,       // Farthest color (0xRRGGBBAA)
    sky_zenith: u32,      // Sky at top (0xRRGGBBAA)
    sky_horizon: u32,     // Sky at horizon (0xRRGGBBAA)
    parallax_rate: u32,   // Layer separation (0-255)
    seed: u32,            // Noise seed
);
```

**Example: Mountain range**
```rust
env_silhouette(0, 100, 3,
    0x2A3A4AFF, 0x1A2A3AFF,  // Near/far mountain colors
    0x87CEEBFF, 0xFFD700FF,  // Sky blue to golden horizon
    128, 42);
```

## Mode 4: Rectangles (City Windows)

Rectangular light sources:

```rust
env_rectangles(
    layer: u32,
    variant: u32,         // 0=Scatter, 1=Buildings, 2=Bands, 3=Panels
    density: u32,         // Count (0-255)
    lit_ratio: u32,       // Lit percentage (0-255, 128=50%)
    size_min: u32,        // Min size (0-63)
    size_max: u32,        // Max size (0-63)
    aspect: u32,          // Aspect bias (0-3, 0=square)
    color_primary: u32,   // Main color (0xRRGGBBAA)
    color_variation: u32, // Variation (0xRRGGBBAA)
    parallax_rate: u32,   // Layer separation (0-255)
    phase: u32,           // Flicker phase (0-65535)
);
```

**Example: Night cityscape**
```rust
env_rectangles(1, 1, 200, 100, 1, 4, 2,
    0xFFFF88FF, 0xFF8844FF, 80, 0);
```

## Mode 5: Room (Interior Spaces)

3D box interior with lighting:

```rust
env_room(
    layer: u32,
    color_ceiling: u32,   // Ceiling (0xRRGGBB00)
    color_floor: u32,     // Floor (0xRRGGBB00)
    color_walls: u32,     // Walls (0xRRGGBB00)
    panel_size: f32,      // Wall panel size
    panel_gap: u32,       // Gap between panels (0-255)
    light_dir_x: f32,     // Light direction XYZ
    light_dir_y: f32,
    light_dir_z: f32,
    light_intensity: u32, // Light strength (0-255)
    corner_darken: u32,   // Edge darkening (0-255)
    room_scale: f32,      // Size multiplier
    viewer_x: i32,        // Position (-128 to 127)
    viewer_y: i32,
    viewer_z: i32,
);
```

**Example: Sci-fi corridor**
```rust
env_room(0,
    0x40404000, 0x20202000, 0x30303000,  // Gray tones
    2.0, 10,
    0.0, -1.0, 0.5,  // Light from above-front
    200, 100, 1.0,
    0, 0, 0);
```

## Mode 6: Curtains (Trees, Pillars)

Vertical structures around viewer:

```rust
env_curtains(
    layer: u32,
    layer_count: u32,     // Depth layers (1-3)
    density: u32,         // Structures per cell (0-255)
    height_min: u32,      // Min height (0-63)
    height_max: u32,      // Max height (0-63)
    width: u32,           // Width (0-31)
    spacing: u32,         // Gap (0-31)
    waviness: u32,        // Wobble (0-255)
    color_near: u32,      // Near color (0xRRGGBBAA)
    color_far: u32,       // Far color (0xRRGGBBAA)
    glow: u32,            // Neon glow (0-255)
    parallax_rate: u32,   // Layer separation (0-255)
    phase: u32,           // Scroll phase (0-65535)
);
```

**Example: Neon forest**
```rust
env_curtains(0, 3, 30, 20, 50, 3, 8, 50,
    0xFF00FF80, 0x00FFFF40, 100, 100, 0);
```

## Mode 7: Rings (Portals, Vortex)

Concentric rings:

```rust
env_rings(
    layer: u32,
    ring_count: u32,      // Count (1-255)
    thickness: u32,       // Thickness (0-255)
    color_a: u32,         // First color (0xRRGGBBAA)
    color_b: u32,         // Second color (0xRRGGBBAA)
    center_color: u32,    // Center glow (0xRRGGBBAA)
    center_falloff: u32,  // Falloff (0-255)
    spiral_twist: f32,    // Spiral degrees (0=concentric)
    axis_x: f32,          // Axis direction (normalized)
    axis_y: f32,
    axis_z: f32,
    phase: u32,           // Rotation (0-65535)
);
```

**Example: Rotating portal**
```rust
static mut PORTAL_PHASE: u32 = 0;

fn update() {
    unsafe { PORTAL_PHASE = PORTAL_PHASE.wrapping_add(200); }
}

fn render() {
    unsafe {
        env_rings(1, 20, 15,
            0x8800FFFF, 0xFF0088FF, 0xFFFFFFFF, 200,
            45.0,  // Spiral twist
            0.0, 0.0, 1.0,  // Facing camera
            PORTAL_PHASE);
    }
}
```

## Recipe: Space Game

```rust
fn init() {
    // Base: deep space gradient
    env_gradient(0, 0x000011FF, 0x000022FF, 0x000011FF, 0x000005FF, 0.0, 0.0);
    // Overlay: star field
    env_scatter(1, 0, 255, 2, 30, 0, 0xFFFFFF00, 0x8888FF00, 150, 80, 0);
    env_blend(1);  // Additive for glow
}
```

## Recipe: Racing Game

```rust
fn init() {
    // Sunset sky
    env_gradient(0, 0x1a0a2eFF, 0xFF6B35FF, 0x3a2a1aFF, 0x0a0505FF, 0.0, -0.1);
}

fn render() {
    // Scrolling road grid
    env_lines(1, 0, 2, 2, 3.0, 80.0, 0x444444FF, 0xFFFFFFFF, 10, scroll_phase);
    env_blend(0);
}
```

## Animation via Phase

All modes with `phase` parameter animate by incrementing 0-65535:

```rust
phase = phase.wrapping_add(speed);  // Smooth wrap at 65536
```

- Slower speed = slower animation
- `wrapping_add` ensures seamless looping

## Additional Resources

- **`references/mode-parameters.md`** - Complete parameter reference for all 8 modes
- **`nethercore/include/zx.rs`** - EPU FFI source (lines 800-970)
