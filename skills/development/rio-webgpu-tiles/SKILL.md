---
name: rio-webgpu-tiles
description: WebGPU tile rendering for Rio Terminal via wgpu and sugarloaf. Extends
version: 1.0.0
---


# Rio WebGPU Tiles

GPU-accelerated tile rendering in Rio Terminal using wgpu and the sugarloaf brush architecture.

## Architecture Overview

```
OSC 1337 Sequence → rio-backend (parse) → RioEvent::InsertTile → rioterm (frontend) → sugarloaf TileBrush → wgpu render
```

### Core Files
| File | Purpose |
|------|---------|
| `sugarloaf/src/components/tiles/mod.rs` | TileBrush, TileWorldState, GPU buffers |
| `sugarloaf/src/sugarloaf.rs` | Main renderer integration, public API |
| `rio-backend/src/ansi/tile_protocol.rs` | OSC 1337 `Tile=` parsing |
| `rio-backend/src/performer/handler.rs` | OSC dispatch to handler |
| `rio-backend/src/event/mod.rs` | `InsertTile` event variant |
| `frontends/rioterm/src/application.rs` | Frontend event handling |

## Protocol: OSC 1337 Tile Extension

```bash
# Format: ESC ] 1337 ; Tile = key:value,key:value,... BEL
printf '\033]1337;Tile=shader:plasma,x:50,y:50,w:200,h:150\007'
```

### Parameters
| Key | Type | Description |
|-----|------|-------------|
| `shader` | string | `plasma`, `clock`, `noise`, or custom ID |
| `x`, `y` | f32 | Position in pixels |
| `w`, `h` | f32 | Size in pixels |
| `id` | u64 | Tile ID (0 = auto-assign) |
| `kind` | string | `persistent` (default) or `transient` |
| `r`, `g`, `b`, `a` | f32 | Custom color/data (0.0-1.0) |
| `time_offset` | f32 | Animation time offset |

## Tile Lifecycle

### Persistent Tiles
Remain until explicitly removed by ID:
```rust
let id = sugarloaf.create_persistent_tile(scene);
// ... later
sugarloaf.remove_persistent_tile(id);
```

### Transient Tiles
Cleared at `begin_frame()`, must be re-pushed each frame:
```rust
sugarloaf.push_transient_tile(scene);
```

## TileWorldState

Manages CPU state with high-precision time (f64), converted to modular f32 for GPU:

```rust
pub struct TileWorldState {
    persistent: HashMap<TileId, TileScene>,
    transient: Vec<TileScene>,
    world_time_seconds: f64,
    next_id: TileId,
}

impl TileWorldState {
    pub fn begin_frame(&mut self, dt_seconds: f64) {
        self.world_time_seconds += dt_seconds;
        self.transient.clear();
    }
}
```

## Writing WGSL Shaders

Uniform structure available in shaders:

```wgsl
struct Uniforms {
    position: vec2<f32>,  // NDC position
    size: vec2<f32>,      // NDC size
    time: f32,            // Animation time (modular)
    custom: vec4<f32>,    // r,g,b,a from protocol
}
@group(0) @binding(0) var<uniform> u: Uniforms;
```

### Vertex Shader Pattern
```wgsl
@vertex
fn vs_main(@location(0) pos: vec2<f32>, @location(1) uv: vec2<f32>) -> VertexOutput {
    var out: VertexOutput;
    let screen_pos = u.position + pos * u.size;
    out.position = vec4<f32>(screen_pos, 0.0, 1.0);
    out.uv = uv;
    return out;
}
```

### Fragment Shader Pattern
```wgsl
@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let t = u.time;
    // Your shader logic using in.uv, t, u.custom
    return vec4<f32>(color, 1.0);
}
```

## Demo Scripts

```bash
# Plasma effect
printf '\033]1337;Tile=shader:plasma,x:50,y:50,w:200,h:150,r:0.5,g:0.2,b:0.8\007'

# Clock display
printf '\033]1337;Tile=shader:clock,x:300,y:50,w:250,h:80\007'

# Remove by ID
printf '\033]1337;Tile=remove:42\007'
```

## Integration Checklist

1. **Add TileBrush to sugarloaf** - Register in brush list, call in render loop
2. **Parse OSC 1337 in rio-backend** - Extend performer handler
3. **Create RioEvent variant** - `InsertTile(TileSpec)`
4. **Handle in frontend** - Convert TileSpec → TileScene, call sugarloaf API
5. **Manage state** - Call `begin_frame(dt)` before each render

## Shader Examples

See `reference/shaders.md` for complete plasma, clock, and noise shader implementations.



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 9. Generic Procedures

**Concepts**: dispatch, multimethod, predicate dispatch, generic

### GF(3) Balanced Triad

```
rio-webgpu-tiles (+) + SDF.Ch9 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch10: Adventure Game Example

### Connection Pattern

Generic procedures dispatch on predicates. This skill selects implementations dynamically.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.