---
name: Native Asset Pipeline for ZX
description: This skill should be used when the user asks about "asset pipeline", "build process", "generator binary", "native vs WASM", "build.script", "nether.toml build", "how to integrate generators", "asset generation workflow", "procedural assets build", "compile time assets", "gitignore generated assets", "regenerate assets", or needs to understand how procedural asset generators integrate with the Nethercore ZX build system.
version: 1.0.0
---

# Native Asset Pipeline

## Core Concept

Asset generators are **native binaries** that run on your development machine during the build process. They are NOT WASM and do NOT run in the ZX console.

```
┌─────────────────────────────────────────────────────────────┐
│                    BUILD TIME (Native)                      │
│                                                             │
│  .studio/specs/      →  generated/        →  game.nczx     │
│  (Rust/Python/etc)      (PNG, OBJ, WAV)      (bundled ROM) │
│  Runs on your CPU       Standard formats      Final output  │
└─────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────┐
│                    RUN TIME (WASM)                          │
│                                                             │
│  game.nczx  →  ZX Console  →  rom_texture(), rom_mesh()    │
│  All assets pre-bundled      Assets loaded from ROM pack   │
└─────────────────────────────────────────────────────────────┘
```

---

## CRITICAL: FFI Module Usage

**NEVER copy FFI declarations inline.** Always use the canonical zx.rs module:

```bash
# Fetch the FFI module (do this once per project)
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs
```

Then in your code:
```rust
mod zx;       // FFI module - NEVER edit or copy inline
use zx::*;    // Access all FFI functions
```

## CRITICAL: Init-Only Resource Loading

**ALL resource loading MUST happen in `init()` ONLY!**

Loading resources in `update()` or `render()` will **CRASH** the game.

Init-only functions include:
- `rom_texture()`, `rom_texture_str()` - texture loading
- `rom_mesh()`, `rom_mesh_str()` - mesh loading  
- `rom_sound()`, `rom_sound_str()` - sound loading
- All procedural mesh functions: `cube()`, `sphere()`, `cylinder()`, etc.

---

## nether.toml Build Integration

The `[build]` section's `script` field chains commands. Generator runs BEFORE WASM compilation:

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"

# Build pipeline: generate assets THEN compile WASM
[build]
script = "python .studio/generate.py && cargo build -p game --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/game.wasm"

# Declare generated assets
[[assets.textures]]
id = "player"
path = "../generated/textures/player.png"

[[assets.meshes]]
id = "level"
path = "../generated/meshes/level.obj"

[[assets.sounds]]
id = "jump"
path = "../generated/sounds/jump.wav"
```

---

## Project Structure

### Studio Scaffold (Recommended)

Install the `.studio/` scaffold (generator + parsers) with `/init-procgen` and put specs under `.studio/specs/`:

```
my-game/
├── .studio/
│   ├── generate.py
│   ├── parsers/            # Installed by /init-procgen
│   └── specs/              # Source of truth (*.spec.py)
│       ├── textures/
│       ├── normals/
│       ├── sounds/
│       ├── instruments/
│       ├── music/
│       ├── meshes/
│       ├── characters/
│       └── animations/
├── game/
│   ├── Cargo.toml          # WASM library (cdylib)
│   ├── nether.toml         # Build config
│   └── src/
│       ├── lib.rs          # Game code (compiles to WASM)
│       └── zx.rs           # FFI module (fetch from GitHub)
├── generated/              # Procedural outputs (gitignored, regenerable)
│   ├── textures/
│   ├── normals/
│   ├── meshes/
│   ├── characters/
│   ├── animations/
│   ├── audio/
│   │   └── instruments/
│   └── tracks/
├── assets/                 # Human-made assets (committed to git)
└── .gitignore
```

### Directory Structure: Generated vs Assets

**Key Distinction:**
- `generated/` - Procedurally generated assets (gitignored)
  - Source of truth: specs in `.studio/specs/`
  - Rebuild anytime with: `python .studio/generate.py`
  - Not committed to git - regenerate after clone
  - Assets are fungible and reproducible

- `assets/` - Human-made assets (committed to git)
  - Source of truth: the files themselves
  - Manually created by artists/designers
  - Version controlled and precious
  - Assets are unique and irreplaceable

**nether.toml Distinction:**
```toml
# Reference procedural assets from generated/
[[assets.textures]]
id = "stone"
path = "../generated/textures/stone.png"  # Regenerated from code

# Reference human-made assets from assets/
[[assets.textures]]
id = "hero_portrait"
path = "../assets/textures/hero_portrait.png"  # Hand-painted, committed
```

### Generator Invocation

Run the unified generator before WASM compilation:

```toml
[build]
script = "python .studio/generate.py && cargo build -p game --target wasm32-unknown-unknown --release"
```

For Blender-dependent categories, run Blender on the same entrypoint:

```bash
blender --background --python .studio/generate.py -- --only meshes
blender --background --python .studio/generate.py -- --only characters
blender --background --python .studio/generate.py -- --only animations
```

---

## Loading Assets in Game (WASM)

**CRITICAL: Use the canonical zx.rs FFI module.** Never copy FFI declarations inline.

First, fetch the FFI bindings:
```bash
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs
```

**CRITICAL: ALL resource loading MUST happen in `init()` ONLY!**

```rust
// game/src/lib.rs
#![no_std]

mod zx;  // FFI module - fetched from GitHub, NEVER edit or copy inline
use zx::*;

static mut PLAYER_TEX: u32 = 0;
static mut LEVEL_MESH: u32 = 0;
static mut JUMP_SFX: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    // CRITICAL: ALL rom_*() calls MUST be in init() - nowhere else!
    unsafe {
        PLAYER_TEX = rom_texture_str("player");
        LEVEL_MESH = rom_mesh_str("level");
        JUMP_SFX = rom_sound_str("jump");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    // Game logic only - NO resource loading here!
}

#[no_mangle]
pub extern "C" fn render() {
    // Drawing only - NO resource loading here!
}
```

---

## Workflow Commands

```bash
# Full build (generate + compile + pack)
cd game
nether build

# Run game
nether run

# Skip generation (just recompile WASM)
nether build --no-compile
cargo build -p game --target wasm32-unknown-unknown --release
nether pack

# Run generators only (debug)
python .studio/generate.py

# Regenerate after git clone
cd game && nether build
```

---

## Key Principles

1. **Generators are Python scripts** - they run natively on your development machine
2. **Build.script chains commands** - run generator THEN WASM compilation
3. **Assets go to disk** - standard formats (PNG, OBJ, WAV) in `generated/` directory
4. **nether.toml declares assets** - `[[assets.*]]` entries reference generated files
5. **ROM functions load assets** - `rom_texture()`, `rom_mesh()`, `rom_sound()`
6. **ALL loading in init()** - Never load resources in update() or render()
7. **Use zx.rs module** - Never copy FFI declarations inline
8. **Generated files are gitignored** - code is source of truth
