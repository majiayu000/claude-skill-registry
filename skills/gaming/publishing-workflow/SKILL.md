---
name: Nethercore ZX Publishing Workflow
description: |
  This skill covers publishing ZX games. Use when the user asks to "publish game", "release game", "upload game", "create ROM", "package game", "nether pack", or mentions ROM packaging, nethercore.systems upload.

  **Load references when:**
  - Full manifest examples → `references/manifest-examples.md`
version: 1.0.0
---

# Nethercore ZX Publishing Workflow

## nether CLI Commands

| Command | Purpose |
|---------|---------|
| `nether init` | Create nether.toml manifest |
| `nether compile` | Compile WASM from source |
| `nether pack` | Bundle WASM + assets into ROM |
| `nether build` | compile + pack (main command) |
| `nether run` | Build and launch in emulator |

## Game Manifest (nether.toml)

```toml
[game]
id = "my-game"              # Unique identifier
title = "My Game"           # Display name
author = "Your Name"        # Creator
version = "1.0.0"           # Semantic version
description = "A fun game"  # Short description
tags = ["arcade", "2d"]     # Searchable tags

[build]
script = "cargo build --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/my_game.wasm"

[[assets.textures]]
id = "player"
path = "assets/player.png"
```

## Upload to nethercore.systems

**Required:**
| File | Format |
|------|--------|
| Game | `.wasm` or `.nczx` |
| Icon | 64x64 PNG |

**Optional:**
- Screenshots (PNG, up to 5)
- Banner (1280x720 PNG)

**Process:**
1. Create account at nethercore.systems
2. Dashboard → "Upload New Game"
3. Fill metadata, upload files
4. Publish

## Pre-Release Checklist

- [ ] `nether build` succeeds
- [ ] `nether run --sync-test` passes (if multiplayer)
- [ ] ROM under 16MB
- [ ] Icon is 64x64 PNG
- [ ] Description is compelling

## Versioning

Semantic versioning: `major.minor.patch`

Update process:
1. Bump version in nether.toml
2. Rebuild
3. Re-upload to platform
