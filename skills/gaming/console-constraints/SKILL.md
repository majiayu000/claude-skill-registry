---
name: ZX Console Constraints
description: This skill should be used when the user asks about "ZX capabilities", "memory limits", "render mode selection", "console specs", "what can ZX do", "ZX hardware", "ROM size", "RAM limits", "VRAM budget", "audio channels", "controller layout", "tick rate", "resolution", or discusses whether a game concept is feasible on Nethercore ZX.
version: 0.1.0
---

# ZX Console Constraints

Comprehensive reference for Nethercore ZX hardware capabilities and constraints. Use this knowledge to validate game concepts, plan memory budgets, and make informed design decisions.

## Core Specifications

| Spec | Value | Design Implication |
|------|-------|-------------------|
| Resolution | 960×540 fixed | UI safe zones required, 16:9 aspect |
| Color depth | 32-bit RGBA8 | Full color, no palette limitations |
| ROM | 16 MB | WASM + all assets must fit |
| RAM | 4 MB | Game state only (fast rollback) |
| VRAM | 4 MB | GPU textures and mesh buffers |
| Tick rate | 24/30/60/120 fps | Choose based on game needs |
| Max players | 4 | Local + remote mix supported |
| Alpha | 2-bit Bayer 4×4 | 16 threshold levels for transparency |

## Memory Budget Planning

### ROM Distribution (16 MB Total)

Typical allocation patterns:

**Fighting Game (~12 MB):**
- Characters (8): ~6 MB (meshes, textures, animations)
- Stages (4): ~3 MB
- Audio (SFX + music): ~2 MB
- Effects, UI, code: ~1 MB

**3D Platformer (~10 MB):**
- Player + animations: ~500 KB
- Levels (5 worlds × 4 stages): ~5 MB
- Enemies/NPCs: ~2 MB
- Audio: ~2 MB
- Code: ~500 KB

**Racing Game (~8 MB):**
- Vehicles (12): ~2 MB
- Tracks (6): ~4 MB
- Audio: ~1.5 MB
- Effects, UI, code: ~500 KB

### RAM Usage (4 MB Total)

Keep game state small for fast rollback:
- Typical game state: 50-200 KB
- 8-frame rollback at 60fps: ~2ms (well within budget)
- Stack + heap for logic: remaining space

### VRAM Budget (4 MB Total)

Active GPU resources:
- Loaded textures
- Mesh vertex/index buffers
- Careful: large textures consume quickly

## Render Modes

Choose ONE render mode in `init()` — cannot change at runtime.

| Mode | Name | Best For | Cost |
|------|------|----------|------|
| 0 | Lambert | 2D games, UI, sprites, flat stylized | Lowest |
| 1 | Matcap | Stylized 3D, toon shading, metallic | Low |
| 2 | MR-Blinn-Phong | PBR materials, realistic surfaces | Medium |
| 3 | Blinn-Phong | 5th-gen retro, artistic specular | Medium |

### Mode Selection Guidelines

**Mode 0 (Lambert)** — Side-scrollers, puzzles, retro aesthetics:
- Texture × vertex color (no lighting without normals)
- Simple Lambert shading if normals present
- Lowest GPU cost

**Mode 1 (Matcap)** — Stylized 3D, character games:
- View-space normal matcap sampling
- Lighting baked into matcap texture
- Good for toon/cartoon aesthetics

**Mode 2 (MR-Blinn-Phong)** — Modern/realistic:
- Metallic-roughness workflow
- 4 dynamic lights + procedural sun
- Energy-conserving specular

**Mode 3 (Blinn-Phong)** — Retro 3D, 5th-gen feel:
- Classic specular-shininess
- Rim lighting support
- Era-authentic aesthetic

## Audio System

| Spec | Value |
|------|-------|
| Sample rate | 22,050 Hz |
| Format | 16-bit signed PCM, mono |
| Sound channels | 16 simultaneous |
| Music channel | 1 dedicated (looping) |
| Panning | Equal-power stereo (-1.0 to +1.0) |

**Design implications:**
- Lower sample rate = retro sound quality (N64/PS1 era)
- Record/compress as mono, pan in software
- 16 channels is tight for orchestral — plan carefully
- Music via XM tracker format recommended for size

## Input System

6th-generation controller layout:

| Input | Type | Notes |
|-------|------|-------|
| D-Pad | 4-way digital | Best for 2D precision |
| Face buttons | A, B, X, Y | Standard action buttons |
| Bumpers | L1, R1 | Digital shoulder buttons |
| Triggers | L2, R2 | Analog (0.0-1.0) |
| Sticks | Left + Right | Analog (-1.0 to 1.0) with L3/R3 click |
| Menu | Start, Select | Standard menu buttons |

**Control scheme guidelines:**
- 3D games: prefer analog sticks + triggers
- 2D games: D-pad works well, consider stick as alternative
- Fighting games: all face buttons + D-pad
- Racing: triggers for accelerate/brake, stick for steering

## Multiplayer Constraints

- **Max 4 players** — any mix of local and remote
- **GGRS rollback netcode** — requires deterministic `update()`
- **Fast rollback** — small state enables 8-frame rollback in ~2ms

**Determinism requirements:**
- All randomness via seeded `random()` FFI
- Time from `tick_count()`, not system clock
- No floating-point precision tricks
- State changes ONLY in `update()`, never in `render()`

## What ZX Excels At

Based on hardware capabilities:
- 3D platformers and action games
- Fighting games (4-player, rollback netcode)
- Racing games (analog triggers, tracks in ROM)
- Third-person adventures
- Split-screen local multiplayer
- Online competitive games

## What Requires Careful Planning

- Large open worlds (16 MB ROM limit)
- Orchestral/complex soundtracks (16 channels, 22 kHz)
- Massive texture counts (4 MB VRAM)
- Complex physics simulations (determinism required)

## Additional Resources

### Reference Files

For detailed constraint breakdowns:
- **`references/memory-budget-calculator.md`** — ROM/RAM/VRAM allocation templates
- **`references/render-mode-comparison.md`** — Visual examples and use cases

### Validation

Before finalizing a game concept, validate:
1. Total asset size fits in 16 MB ROM
2. Game state fits comfortably in RAM for rollback
3. Render mode matches art style goals
4. Audio design fits 16-channel limit
5. Control scheme uses available inputs appropriately
