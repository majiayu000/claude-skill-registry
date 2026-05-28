---
name: Optimization Techniques
description: |
  This skill provides optimization methods for Nethercore ZX games. Use when the user asks about "optimize", "compress", "reduce size", "wasm-opt", "BC7", "LTO", "asset compression", "mesh optimization", "texture compression", or "state size".

  **Load references when:**
  - Detailed code examples → `references/code-examples.md`
version: 1.0.0
---

# Optimization Techniques for Nethercore ZX

## WASM Optimization

### Cargo.toml Settings

```toml
[profile.release]
lto = true           # Link-time optimization
opt-level = "z"      # Optimize for size
codegen-units = 1    # Better optimization
panic = "abort"      # Smaller than unwind
strip = true         # Strip symbols
```

### Post-Build

```bash
wasm-opt -Oz game.wasm -o game.wasm
```

**Typical savings:** 20-40%

## Texture Optimization

All textures use BC7 compression (4:1 ratio):

| Original | Compressed |
|----------|------------|
| 256×256 RGBA (256 KB) | 64 KB |
| 512×512 RGBA (1 MB) | 256 KB |

**Resolution targets:**
- UI elements: 256×256
- Characters: 256-512
- Environment: 128-256

## Mesh Optimization

| Format | Size/Vertex |
|--------|-------------|
| Position only | 12 bytes |
| Pos + UV | 20 bytes |
| Pos + UV + Normal | 32 bytes |
| Full | 40 bytes |

**Poly targets:**
- Background props: 50-200
- Interactive props: 100-500
- Characters: 500-2000

## Audio Optimization

- Sample rate: 22050 Hz (engine limit)
- Channels: Mono only
- Use XM modules for music (95% savings vs WAV)

## State Size Reduction

```rust
// Use compact types
struct Position { x: f32, y: f32 }  // 8 bytes
struct Position { x: i16, y: i16 }  // 4 bytes (fixed-point)

// Fixed arrays, not Vec
entities: [Entity; 64],  // Known size
```

## Quick Wins Checklist

- [ ] LTO and opt-level = "z" in Cargo.toml
- [ ] wasm-opt -Oz on final binary
- [ ] Texture resolutions at 256×256 default
- [ ] Music as XM format
- [ ] Fixed arrays instead of Vec
